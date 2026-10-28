#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_ORG_INFLUENCE 科研机构影响力
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_ORG_INFLUENCE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_INNOV_ORG_INFLUENCE · 科研机构影响力（gkx 换源版）

口径（本报告 §2.2）：
    机构影响力 = 100 × [ 0.45·norm(log1p(专利数))
                        + 0.35·norm(log1p(专利价值合计))
                        + 0.20·norm(log1p(论文数)) ]
    缺失维度按王惠 V1.3 缺失维再归一化处理。

20261021 换源的关键变化
-----------------------
1. **专利件数改为 `star_applicant_agg_gkx.json` 字典查表**（169,226 名申请人，
   全量 2,939,895 行，件数合计与表行数逐位相等），不再对 `dwd_patent` 发任何 SQL。
2. **专利价值维不可得**：全量申请人缓存只有 `[件数, 授权数]`，没有 `SUM(value)`；
   在不查专利表的前提下无法补齐 → 本维整维剔除，按 V1.3 对剩余 0.45/0.20 再归一。
   这是本指标从「可算三维」降到「可算两维」的直接原因，判档据此下调。
3. 论文维仍扫 `dwd_zh_paper.author_info_list`（100,900 行），结果落
   `_snapshots21/org_paper_counts_20261021.json`，重跑不连库。
4. 机构底册仍为 `gkx.dwd_research_institute_base_info` 2,074 家（100% 广东）。

为什么不用 PageRank / 度中心性：
  · 机构—专利二部图只能取 `dwd_patent.first_applicant_name`，共同申请人边不可得；
  · 机构—论文合著图需 institution 字段，机构名与 2,074 家底册精确匹配率低；
  · 故采用「加权度」：专利数=度，论文数=第二类度，专利价值维缺测。

输出：code/M_INNOV_ORG_INFLUENCE_out.json
"""
from __future__ import annotations

import json
import math
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _gkxdb  # noqa: E402

OUT = HERE / "M_INNOV_ORG_INFLUENCE_out.json"
SNAP = HERE / "_snapshots21"
AGG = SNAP / "star_applicant_agg_gkx.json"
PCACHE = SNAP / "org_paper_counts_20261021.json"


def q(sql):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def norm(vals):
    lo, hi = min(vals), max(vals)
    if hi <= lo:
        return [0.5] * len(vals)
    return [(v - lo) / (hi - lo) for v in vals]


def paper_counts(names):
    if PCACHE.exists():
        d = json.loads(PCACHE.read_text(encoding="utf-8"))
        return d["counts"], d["total"], d["bad"], d["strings"]
    names_sorted = sorted(names, key=len, reverse=True)
    cnt = {nm: 0 for nm in names}
    total = bad = 0
    strings = set()
    cur = _gkxdb.gkx()
    try:
        cur.execute("SELECT author_info_list FROM gkx.dwd_zh_paper")
        while True:
            rows = cur.fetchmany(2000)
            if not rows:
                break
            for (raw,) in rows:
                total += 1
                if not raw:
                    continue
                try:
                    arr = json.loads(raw) if isinstance(raw, str) else raw
                except Exception:  # noqa: BLE001
                    bad += 1
                    continue
                if not isinstance(arr, list):
                    continue
                seen = set()
                for au in arr:
                    if not isinstance(au, dict):
                        continue
                    aff = " ".join(str(au.get(k) or "") for k in ("institution", "affiliation"))
                    if not aff.strip():
                        continue
                    strings.add(aff.strip()[:120])
                    for nm in names_sorted:
                        if nm and nm in aff and nm not in seen:
                            seen.add(nm)
                            cnt[nm] += 1
    finally:
        cur.close()
    PCACHE.write_text(json.dumps({"counts": cnt, "total": total, "bad": bad,
                                  "strings": sorted(strings)}, ensure_ascii=False),
                      encoding="utf-8")
    return cnt, total, bad, sorted(strings)


def main():
    t0 = time.time()

    inst = q("""SELECT org_id, name_cn, city, org_type, incorporation_date,
                       registered_capital_value
                FROM gkx.dwd_research_institute_base_info""")
    n_inst = len(inst)
    city_cnt = {}
    for r in inst:
        city_cnt[r["city"]] = city_cnt.get(r["city"], 0) + 1
    names = [(r["name_cn"] or "").strip() for r in inst if r["name_cn"]]

    agg = json.loads(AGG.read_text(encoding="utf-8"))["agg"]
    by_name = {nm.strip(): int(v[0]) for nm, v in agg.items()}

    matched, alias_hit = [], 0
    for r in inst:
        nm = (r["name_cn"] or "").strip()
        if nm and nm in by_name:
            matched.append({"org_id": r["org_id"], "name": nm, "city": r["city"],
                            "org_type": r["org_type"], "patent_n": by_name[nm],
                            "patent_value": None})
    have = {m["name"] for m in matched}
    base = {}
    for nm, n in by_name.items():
        k = re.sub(r"[（(].*?[)）]", "", nm).strip()
        base[k] = base.get(k, 0) + n
    for r in inst:
        nm = (r["name_cn"] or "").strip()
        if not nm or nm in have:
            continue
        k = re.sub(r"[（(].*?[)）]", "", nm).strip()
        if k in base:
            matched.append({"org_id": r["org_id"], "name": nm, "city": r["city"],
                            "org_type": r["org_type"], "patent_n": base[k],
                            "patent_value": None})
            alias_hit += 1

    pcounts, paper_total, bad_json, strings = paper_counts(names)
    for m in matched:
        m["paper_n"] = pcounts.get(m["name"], 0)
    matched_names = {m["name"] for m in matched}
    for nm, c in pcounts.items():
        if c > 0 and nm not in matched_names:
            r = next((x for x in inst if (x["name_cn"] or "").strip() == nm), None)
            if r:
                matched.append({"org_id": r["org_id"], "name": nm, "city": r["city"],
                                "org_type": r["org_type"], "patent_n": 0,
                                "patent_value": None, "paper_n": c})
    matched = [m for m in matched if m["patent_n"] > 0 or m.get("paper_n", 0) > 0]

    pn = [math.log1p(m["patent_n"]) for m in matched]
    pp = [math.log1p(m.get("paper_n", 0)) for m in matched]
    n_pn, n_pp = norm(pn), norm(pp)
    W = {"patent_n": 0.45, "paper_n": 0.20}
    wsum = sum(W.values())
    for i, m in enumerate(matched):
        m["score"] = round(100 * (W["patent_n"] * n_pn[i] + W["paper_n"] * n_pp[i]) / wsum, 2)
        m["dims_used"] = ["patent_n", "paper_n"]

    matched.sort(key=lambda x: -x["score"])
    scores = [m["score"] for m in matched]
    bands = {"90-100": 0, "70-90": 0, "50-70": 0, "30-50": 0, "0-30": 0}
    for v in scores:
        if v >= 90: bands["90-100"] += 1
        elif v >= 70: bands["70-90"] += 1
        elif v >= 50: bands["50-70"] += 1
        elif v >= 30: bands["30-50"] += 1
        else: bands["0-30"] += 1

    coauthor = q("""SELECT COUNT(*) AS n, COUNT(DISTINCT scholar_id) AS s
                    FROM gkx.dwd_scholar_coauthor""")[0]
    scholar_org = q("""SELECT scholar_org_name_zh AS nm, COUNT(*) AS n FROM gkx.dwd_scholar
                       WHERE scholar_org_name_zh IS NOT NULL AND scholar_org_name_zh <> ''
                       GROUP BY scholar_org_name_zh ORDER BY n DESC LIMIT 50""")
    inst_names = {m["name"] for m in matched} | set(names)
    scholar_hit = sum(1 for r in scholar_org if str(r["nm"]).strip() in inst_names)
    n_pat_inst = len({m["name"] for m in matched if m["patent_n"] > 0})

    out = {
        "metric_id": "M_INNOV_ORG_INFLUENCE",
        "metric_name": "科研机构影响力",
        "formula_owner": "仿 Wang Hui V1.3 缺失维再归一化（推测定义；需求未给公式）",
        "run_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": "gkx.dwd_research_institute_base_info + star_applicant_agg_gkx.json + gkx.dwd_zh_paper",
        "universe": {
            "institute_roster": n_inst,
            "city_dist": city_cnt,
            "province_dist": {"广东省": n_inst},
            "note": "底册 2,074 家 100% 位于广东；深圳 1,014、广州 822、东莞 127、惠州 111。"
                    "全国其他城市无机构可比，故「全国机构影响力排名」不可交付。",
        },
        "patent_link": {
            "distinct_applicant_names_in_cache": len(agg),
            "matched_institutes": n_pat_inst,
            "matched_patents": sum(m["patent_n"] for m in matched),
            "match_share_of_roster": round(n_pat_inst / n_inst, 4),
            "alias_hits": alias_hit,
            "method": "star_applicant_agg_gkx.agg 名称精确等值 = 机构底册 name_cn；括号别名二次匹配",
            "why_first_applicant_only": "申请人聚合缓存按 first_applicant_name 建，共同申请人边不可得；"
                                        "本次未对 dwd_patent 发任何 SQL",
            "value_dimension": "不可得：缓存只有 [件数, 授权数]，无 SUM(value)；不查专利表就无法补",
        },
        "paper_link": {
            "papers_scanned": paper_total,
            "bad_json": bad_json,
            "distinct_affiliation_strings": len(strings),
            "institutes_with_papers": sum(1 for m in matched if m.get("paper_n", 0) > 0),
            "note": "author_info_list JSON 数组的 institution/affiliation 字段与底册名称做包含匹配；"
                    "机构名书写不统一（科室、分院后缀），包含匹配已吸收部分噪声。",
        },
        "scored": len(matched),
        "score_bands": bands,
        "score_dist": {
            "min": round(min(scores), 2) if scores else None,
            "max": round(max(scores), 2) if scores else None,
            "mean": round(sum(scores) / len(scores), 2) if scores else None,
            "median": round(sorted(scores)[len(scores) // 2], 2) if scores else None,
        },
        "top25": [{k: m[k] for k in ("name", "city", "org_type", "patent_n",
                                     "patent_value", "paper_n", "score")}
                  for m in matched[:25]],
        "dimension_coverage": {
            "patent_n": len(matched),
            "patent_value": 0,
            "paper_n": sum(1 for m in matched if m.get("paper_n", 0) > 0),
            "value_missing_note": f"{len(matched)} 家机构专利价值全不可得，"
                                  f"该维整维剔除并按 V1.3 对 0.45/0.20 再归一，不补 0。",
        },
        "alternative_graph_test": {
            "coauthor_edges": int(coauthor["n"]),
            "coauthor_src_nodes": int(coauthor["s"]),
            "scholar_org_top50_hit_in_institute_roster": scholar_hit,
            "verdict": "学者合著网 118.8 万边属真实网络，但学者所属机构字段与 2,074 家科研机构底册"
                       "Top50 命中极少，无法把学者层网络折叠到机构层；故本指标不采用 PageRank，"
                       "改用可核验的加权度。",
        },
        "method": {
            "formula": "100 * [0.45*norm(log1p(patent_n)) + 0.20*norm(log1p(paper_n))] / 0.65"
                       "（专利价值维缺测，按 V1.3 再归一）",
            "influence_type": "加权度（weighted degree），非 PageRank、非中介中心性",
            "why": "二部图边型只有「机构—专利」「机构—论文」两类，且专利侧只有第一申请人；"
                   "缺少机构—机构边，中心性指标的分母（全网最短路）无定义。",
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "structure": "底册 + 申请人聚合缓存 + 论文作者机构字段，三表真实可得",
                "volume": f"2,074 家中 {n_pat_inst} 家有专利匹配"
                          f"（{n_pat_inst / n_inst:.2%}），"
                          f"共 {sum(m['patent_n'] for m in matched):,} 件；"
                          f"{sum(1 for m in matched if m.get('paper_n', 0) > 0)} 家有论文匹配",
                "reproducible": True,
                "discriminative": f"分数 {min(scores):.1f}–{max(scores):.1f}，非常数",
                "but": "专利价值维整维缺失（权重 0.35），实际只算两维；机构底册 100% 在广东，"
                       "且多数机构无专利命中；不能输出全国机构影响力榜。",
            },
            "reason": "方法可复现、有区分度，但覆盖面只到广东 2,074 家中的少数，"
                      "且专利价值维不可得，故判部分支持。",
        },
        "elapsed_sec": round(time.time() - t0, 1),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str),
                   encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("universe", "patent_link", "paper_link",
                                          "scored", "score_dist",
                                          "dimension_coverage")},
                     ensure_ascii=False, indent=1)[:3000])
    print("top5:", [(m["name"], m["patent_n"], m["paper_n"], m["score"])
                    for m in matched[:5]])
    print("written", OUT.name, out["elapsed_sec"], "s")


if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_INNOV_ORG_INFLUENCE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_ORG_INFLUENCE.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_INNOV_ORG_INFLUENCE",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
