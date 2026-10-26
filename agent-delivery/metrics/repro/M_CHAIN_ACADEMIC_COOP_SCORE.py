#!/usr/bin/env python3
"""M_CHAIN_ACADEMIC_COOP_SCORE 产学研合作强度 — 实测计算脚本（20261021 修订版）

口径（calc-logic AI 补漏稿，三维等权，待算法 Lead 会签）与实测落地差异：
  ① 联合专利：calc-logic 登记 dwd_patent.applicants 共现判定——当日实测 SHOW COLUMNS
     发现 gkx.dwd_patent **无 applicants 列**（仅 first_applicant_name/first_current_assignee_name），
     多申请人共现结构缺失 → 退化为「第一申请人分桶」弱代理（链上企业专利量 / 学研方专利量），
     并在 out.json 如实披露结构断点。
  ② 合作论文：dwd_zh_paper.author_info_list 为 JSON 数组（含每作者 affiliation/institution）
     → 全量拉取本地解析，判定「同一篇论文作者机构中同时出现链上企业名 与 高校/科研机构名」
     （真共现，前缀字典加速匹配）。
  ③ 人才流动：dwd_scholar.scholar_org_id 当日实测全为空串（id 轨断裂）、每学者单机构名
     → 校企双重任职不可算，todo 所列「人才流动轨迹表」确认为真实缺口。

输出：M_CHAIN_ACADEMIC_COOP_SCORE_out.json
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _chain_common import connect_gkx, q, q1, write_out  # noqa: E402

METRIC = "M_CHAIN_ACADEMIC_COOP_SCORE"
TARGET_CHAIN = "INB1309"
PATENT_SAMPLE = 300_000


def build_prefix_dict(names):
    """4 字前缀 → 候选全名列表（中文机构名前缀区分度高）。"""
    d = {}
    for nm in names:
        if len(nm) >= 6:
            d.setdefault(nm[:4], []).append(nm)
    return d


def match_names(blob, pdict):
    """滑动 4-gram 查前缀字典，命中后验证全名子串。返回命中的全名集合。"""
    hits = set()
    if not blob:
        return hits
    n = len(blob)
    for i in range(0, n - 3):
        cand = pdict.get(blob[i:i + 4])
        if cand:
            for nm in cand:
                if nm in blob:
                    hits.add(nm)
    return hits


def main():
    t0 = time.time()
    conn = connect_gkx()
    report = {"metric_id": METRIC, "metric_name": "产学研合作强度",
              "date": "2026-10-21",
              "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_ACADEMIC_COOP_SCORE.md（AI 补漏，三维等权，待会签）",
              "target_chain": TARGET_CHAIN}
    try:
        # --- 行数探针 ---
        probe = {}
        for t in ("dwd_industry_chain_info", "dwd_org_industry_tags", "dwd_org_heis_info",
                  "dwd_research_institute_base_info", "dwd_patent", "dwd_zh_paper", "dwd_scholar"):
            probe[t] = int(q1(conn, f"SELECT COUNT(*) n FROM {t}")["n"])
        report["probe_rows"] = probe

        chain = q1(conn, "SELECT industry_code, industry_name FROM dwd_industry_chain_info WHERE industry_code=%s", (TARGET_CHAIN,))
        report["chain"] = chain

        # --- 链上企业（单/双引号 JSON 串双 pattern，20261021 实测修正） ---
        firms_raw = q(conn, """
            SELECT company_name, credit_code FROM dwd_org_industry_tags
            WHERE (industry_code LIKE %s OR industry_code LIKE %s)
              AND company_name IS NOT NULL AND company_name != ''
        """, (f'%"{TARGET_CHAIN}"%', f"%['{TARGET_CHAIN}']%"))
        firms, seen = [], set()
        for r in firms_raw:
            nm = (r["company_name"] or "").strip()
            key = (r["credit_code"] or "").strip() or nm
            if len(nm) >= 6 and key not in seen:
                firms.append(nm)
                seen.add(key)
        # 学研方（高校 + 科研机构全量名称）
        heis = [r["name_cn"].strip() for r in q(conn, "SELECT name_cn FROM dwd_org_heis_info WHERE name_cn IS NOT NULL AND name_cn != ''")]
        ris = [r["name_cn"].strip() for r in q(conn, "SELECT name_cn FROM dwd_research_institute_base_info WHERE name_cn IS NOT NULL AND name_cn != ''")]
        acad = [nm for nm in set(heis + ris) if len(nm) >= 6]
        report["inputs"] = {
            "chain_rows": len(firms_raw), "chain_firms_dedup_ge6": len(firms),
            "heis_rows": len(heis), "ri_rows": len(ris), "academia_dedup_ge6": len(acad),
            "firm_sample3": firms[:3], "acad_sample3": acad[:3],
        }

        firm_pdict = build_prefix_dict(firms)
        acad_pdict = build_prefix_dict(acad)

        # --- ② 合作论文（真共现，全量 10 万行） ---
        coop_papers = []
        n_papers = 0
        corp_only = acad_only = 0
        offset = 0
        while True:
            rows = q(conn, "SELECT id, author_info_list FROM dwd_zh_paper LIMIT 20000 OFFSET %s", (offset,))
            if not rows:
                break
            for r in rows:
                n_papers += 1
                blob = r["author_info_list"] or ""
                if len(blob) < 10:
                    continue
                f_hit = match_names(blob, firm_pdict)
                a_hit = match_names(blob, acad_pdict)
                if f_hit and a_hit:
                    coop_papers.append({"id": str(r["id"]), "firm": sorted(f_hit)[0][:30],
                                         "acad": sorted(a_hit)[0][:30]})
                elif f_hit:
                    corp_only += 1
                elif a_hit:
                    acad_only += 1
            offset += 20000
            if len(rows) < 20000:
                break
        report["subitem_joint_papers"] = {
            "papers_scanned": n_papers,
            "coop_firm_x_acad": len(coop_papers),
            "firm_only": corp_only, "acad_only": acad_only,
            "sample5": coop_papers[:5],
        }

        # --- ① 联合专利（第一申请人分桶弱代理 + applicants 列缺失披露） ---
        pat_cols = [c["Field"] for c in q(conn, "SHOW COLUMNS FROM dwd_patent")]
        has_applicants = "applicants" in pat_cols
        patent_firm = patent_acad = 0
        scanned = 0
        offset = 0
        while scanned < PATENT_SAMPLE:
            rows = q(conn, "SELECT pn, first_applicant_name FROM dwd_patent LIMIT 50000 OFFSET %s", (offset,))
            if not rows:
                break
            for r in rows:
                nm = (r["first_applicant_name"] or "").strip()
                if len(nm) >= 4:
                    if match_names(nm, firm_pdict):
                        patent_firm += 1
                    elif match_names(nm, acad_pdict):
                        patent_acad += 1
            scanned += len(rows)
            offset += 50000
            if len(rows) < 50000:
                break
        report["subitem_joint_patents"] = {
            "has_applicants_column": has_applicants,
            "structure_note": "dwd_patent 无 applicants 列（当日 SHOW COLUMNS 实测）——calc-logic 登记的多申请人共现判定不可执行；"
                              "退化为第一申请人分桶：链上企业名下专利 vs 学研方名下专利，共现结构缺失如实披露",
            "patents_scanned": scanned,
            "first_applicant_is_chain_firm": patent_firm,
            "first_applicant_is_academia": patent_acad,
        }

        # --- ③ 人才流动（scholar_org_id 全空串 + 单机构名，如实披露） ---
        scholars = q(conn, "SELECT scholar_id, scholar_org_id, scholar_org_name_zh FROM dwd_scholar")
        mobility_like = []
        for s in scholars:
            org = s["scholar_org_name_zh"] or ""
            if len(org) >= 8 and (org.endswith("公司") or "有限公司" in org):
                # 机构名本身校企混合（如 XX大学XX有限公司）——唯一可探的弱信号
                if any(k in org for k in ("大学", "学院", "研究院", "研究所")):
                    mobility_like.append({"scholar_id": str(s["scholar_id"]), "org": org[:50]})
        report["subitem_talent_mobility"] = {
            "scholar_total": len(scholars),
            "scholar_org_id_nonempty": sum(1 for s in scholars if s["scholar_org_id"]),
            "hybrid_orgname_scholars": len(mobility_like),
            "sample3": mobility_like[:3],
            "note": "scholar_org_id 当日全为空串（id 轨断裂）；单机构名无法判定校企双重任职；人才流动轨迹表确为真实缺口",
        }

        # --- 汇总 ---
        raw = {"joint_papers": len(coop_papers),
               "joint_patent_weak_proxy": 0 if has_applicants else None,
               "talent_mobility": len(mobility_like)}
        # 单链试算：唯一可真算维=合作论文；以「链上机构参与论文总量」为刻度做归一演示
        denom = max(len(coop_papers) + corp_only + acad_only, 1)
        report["score_demo_single_chain"] = {
            "coop_paper_share_pct": round(len(coop_papers) / denom * 100, 2),
            "note": "三维中仅合作论文维可真算；联合专利维结构断列、人才流动维结构断表 → 单维演示占比，正式三维加权不可出分",
        }

        hits = len(coop_papers) + len(mobility_like)
        if hits >= 10:
            level, reason = "部分支持", (
                f"gkx 源在且合作论文维实测命中 {len(coop_papers)} 篇真校企共现；"
                "但联合专利维缺 applicants 列（结构断）、人才流动维缺轨迹表且 scholar_org_id 全空 → 三维缺两维，仅部分依赖维可算")
        else:
            level, reason = "部分支持", f"当日校企共现命中 {hits}（偏少），两维结构断裂，如实披露"
        report["support_judgment"] = {"data_support_level": level, "reason": reason,
                                       "criteria": {"coop_papers": len(coop_papers),
                                                     "hybrid_mobility": len(mobility_like),
                                                     "dims_broken": 2}}
    finally:
        conn.close()
    report["elapsed_sec"] = round(time.time() - t0, 1)
    write_out(METRIC, report)


if __name__ == "__main__":
    main()
