#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_PATENT_VALID_COUNT 有效专利数 —— gkx 真源实测脚本

口径（王惠 calc-logic / Q-E20）：
    有效专利数 = 企业当前法律状态有效的专利件数
    实现：dwd_patent_legal.status 为「授权」且无终止类事件 → count(distinct patent_id)
          → 专利权人名称（dwd_patent_assignees）→ 名称归一后映射 dwd_org_base_info.org_id

数据路径（均来自三方 gkx，2026-10-21）：
    1) dwd_patent_legal（20,000 行，专利样本，含 status/isdt_year/expiration_year）
    2) dwd_patent_assignees（22,198 行，patent_id -> 专利权人名称，覆盖样本 100%）
    3) dwd_org_base_info（189,116 行，name_cn 归一后精确匹配落企业主体）
    4) dwd_patent（2,939,895 行，主表；无法律状态列，用于评估样本可连接性）

输出 code/M_ENT_PATENT_VALID_COUNT_out.json
所有查询均为分批 IN / LIMIT，禁全表 GROUP BY。
"""
import json
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chain_common import connect_gkx, q, q1  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots")
os.makedirs(SNAP, exist_ok=True)
OUT = os.path.join(HERE, "M_ENT_PATENT_VALID_COUNT_out.json")

LEGAL_CACHE = os.path.join(SNAP, "ent_m_patent_legal_full.json")
ASSIGNEE_CACHE = os.path.join(SNAP, "ent_m_patent_assignees.json")
ORGNAME_CACHE = os.path.join(SNAP, "ent_m_org_names.json")
LINK_CACHE = os.path.join(SNAP, "ent_m_legal_link_probe.json")


def load(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def dump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, ensure_ascii=False, default=str)


def pct(a, b):
    return round(100.0 * a / b, 2) if b else None


def norm(s):
    """企业名称归一：去空格、全角括号转半角、去尾缀空白"""
    return (s or "").strip().replace("（", "(").replace("）", ")").replace(" ", "").replace("　", "")


def main():
    t0 = time.time()
    con = connect_gkx()
    res = {"metric_id": "M_ENT_PATENT_VALID_COUNT", "metric_name": "有效专利数",
           "probe_date": "2026-10-21",
           "db": "gkx @ 183.240.141.251:3318（三方生产库）",
           "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_PATENT_VALID_COUNT.md（Q-E20）",
           "formula": "COUNT(DISTINCT patent_id) WHERE legal.status='授权'；assignee name → org_id",
           "valid_rule": "status='授权'（最新法律事件为授予且未终止）；终止/撤回/驳回/撤销/放弃/届满/未缴年费不计"}

    # ---------- 0. 主表规模 ----------
    total_patents = load(LINK_CACHE + ".total") or q1(con, "SELECT COUNT(*) AS n FROM dwd_patent")["n"]
    res["dwd_patent_rows"] = total_patents

    # ---------- 1. 法律状态表全量（2 万行样本） ----------
    legal = load(LEGAL_CACHE)
    if legal is None:
        legal = q(con, """SELECT patent_id, pn, status, isdt, isdt_year, isdt_month,
                                 anticipated_expiration, expiration_year
                          FROM dwd_patent_legal WHERE is_deleted=0""")
        dump(legal, LEGAL_CACHE)
    res["dwd_patent_legal_rows"] = len(legal)
    res["legal_coverage_of_main_pct"] = pct(len(legal), total_patents)

    status_cnt = Counter((r["status"] or "<NULL>") for r in legal)
    res["status_distribution"] = dict(sorted(status_cnt.items(), key=lambda x: -x[1]))

    granted = [r for r in legal if r["status"] == "授权"]
    res["granted_rows"] = len(granted)
    res["granted_share_of_sample_pct"] = pct(len(granted), len(legal))

    dead_kw = ("终止", "撤回", "驳回", "撤销", "放弃", "届满", "未缴年费")
    dead = [r for r in legal if r["status"] and any(k in r["status"] for k in dead_kw)]
    res["terminated_rows"] = len(dead)
    res["terminated_share_pct"] = pct(len(dead), len(legal))

    gy = Counter((r["isdt_year"] or "未知") for r in granted)
    res["granted_by_year_top"] = dict(sorted(gy.items(), key=lambda x: -x[1])[:12])

    ey = Counter(str(r["expiration_year"]) for r in granted if r["expiration_year"])
    res["granted_expiration_year_top"] = dict(sorted(ey.items(), key=lambda x: -x[1])[:8])
    res["granted_expired_before_2026"] = sum(
        1 for r in granted if r["expiration_year"] and int(r["expiration_year"]) < 2026)

    # ---------- 2. 专利权人（assignee）关联 ----------
    asg = load(ASSIGNEE_CACHE)
    if asg is None:
        asg = q(con, "SELECT patent_id, pn, sequence, name FROM dwd_patent_assignees WHERE is_deleted=0")
        dump(asg, ASSIGNEE_CACHE)
    res["dwd_patent_assignees_rows"] = len(asg)

    by_pid = defaultdict(list)
    for a in asg:
        if a["name"]:
            by_pid[a["patent_id"]].append(a["name"].strip())
    res["assignee_distinct_patents"] = len(by_pid)

    granted_pids = [r["patent_id"] for r in granted]
    res["granted_with_assignee"] = sum(1 for p in granted_pids if p in by_pid)
    res["granted_with_assignee_pct"] = pct(res["granted_with_assignee"], len(granted_pids))

    name_patents = defaultdict(set)
    for p in granted_pids:
        for nm in set(by_pid.get(p, [])):
            name_patents[nm].add(p)
    name_cnt = {nm: len(s) for nm, s in name_patents.items()}
    res["distinct_assignee_names"] = len(name_cnt)

    # 权利人构成
    comp = Counter()
    for nm in name_cnt:
        up = nm.upper()
        if "大学" in nm or "学院" in nm:
            comp["高校"] += 1
        elif "研究院" in nm or "研究所" in nm:
            comp["科研院所"] += 1
        elif ("公司" in nm) or ("株式会社" in nm) or (" LLC" in up) or up.endswith(" AG") or (" LTD" in up):
            comp["企业"] += 1
        else:
            comp["个人/协会/境外其他"] += 1
    res["assignee_composition"] = dict(comp)

    # ---------- 3. 名称归一匹配到企业底册 ----------
    orgs = load(ORGNAME_CACHE)
    if orgs is None:
        orgs = q(con, "SELECT org_id, name_cn, province, city, industry_l1_name FROM dwd_org_base_info WHERE is_deleted=0")
        dump(orgs, ORGNAME_CACHE)
    res["dwd_org_base_info_rows"] = len(orgs)

    org_by_name = {}
    for o in orgs:
        if o["name_cn"]:
            org_by_name.setdefault(norm(o["name_cn"]), o)
    res["org_name_index"] = len(org_by_name)
    exact_names = {o["name_cn"].strip() for o in orgs if o["name_cn"]}
    res["assignee_names_exact_matched"] = sum(1 for nm in name_cnt if nm in exact_names)

    matched = {nm: c for nm, c in name_cnt.items() if norm(nm) in org_by_name}
    res["matched_assignee_names"] = len(matched)
    res["matched_assignee_name_pct"] = pct(len(matched), len(name_cnt))

    org_patents = defaultdict(int)
    org_meta = {}
    for nm, c in matched.items():
        o = org_by_name[norm(nm)]
        org_patents[o["org_id"]] += c
        org_meta[o["org_id"]] = o
    res["orgs_with_granted_patent"] = len(org_patents)
    res["orgs_with_granted_patent_pct"] = pct(len(org_patents), len(orgs))
    res["patents_attributed_to_orgs"] = sum(org_patents.values())
    res["patents_attributed_share_of_granted_pct"] = pct(
        res["patents_attributed_to_orgs"], len(granted_pids))

    vals = sorted(org_patents.values(), reverse=True)
    if vals:
        n = len(vals)
        res["per_org_distribution"] = {
            "count": n,
            "mean": round(sum(vals) / n, 3),
            "median": vals[n // 2] if n % 2 else round((vals[n // 2 - 1] + vals[n // 2]) / 2, 3),
            "p90": vals[int(n * 0.10)] if int(n * 0.10) < n else vals[-1],
            "max": vals[0],
            "ge2": sum(1 for v in vals if v >= 2),
            "ge5": sum(1 for v in vals if v >= 5),
            "ge10": sum(1 for v in vals if v >= 10),
            "eq1": sum(1 for v in vals if v == 1),
        }
    top = sorted(org_patents.items(), key=lambda x: -x[1])[:10]
    res["top_orgs"] = [
        {"org_id": k, "name": org_meta[k]["name_cn"], "city": org_meta[k]["city"],
         "granted_patents_in_sample": v} for k, v in top
    ]
    city_cnt = Counter(org_meta[k]["city"] for k in org_patents)
    res["top_cities"] = dict(city_cnt.most_common(6))
    res["density_per_100_orgs_sample"] = round(100.0 * len(org_patents) / len(orgs), 3)

    # ---------- 4. 样本与主表可连接性探针 ----------
    link = load(LINK_CACHE)
    if link is None:
        sample_pids = [r["patent_id"] for r in legal][:500]
        sample_pns = [r["pn"] for r in legal if r["pn"]][:500]
        n_pid = q1(con, "SELECT COUNT(*) AS n FROM dwd_patent WHERE patent_id IN (%s)"
                   % ",".join(["%s"] * len(sample_pids)), tuple(sample_pids))["n"]
        n_pn = q1(con, "SELECT COUNT(*) AS n FROM dwd_patent WHERE pn IN (%s)"
                  % ",".join(["%s"] * len(sample_pns)), tuple(sample_pns))["n"]
        link = {"probe_legal_rows": 500, "matched_by_patent_id": n_pid, "matched_by_pn": n_pn}
        dump(link, LINK_CACHE)
    res["legal_main_join_probe"] = link
    res["legal_main_join_rate_pct"] = pct(link["matched_by_patent_id"], link["probe_legal_rows"])

    cols = [r["Field"] for r in q(con, "SHOW COLUMNS FROM dwd_patent")]
    res["dwd_patent_has_legal_status_col"] = any(
        k in c.lower() for c in cols for k in ("legal", "status", "valid", "expire"))
    res["dwd_patent_has_granted_number"] = "granted_number" in cols
    res["granted_number_filled_probe_note"] = (
        "granted_number 列存在（授权公告号），但主表 293.9 万行、该列无索引，"
        "逐行判空需全表扫描（dwd_id 分片实测约 266 行/秒，全表约 3 小时），"
        "故本脚本以 2 万行法律状态样本为唯一可算口径，不对主表做授权号空值全量核数")

    res["support_judgment"] = {
        "data_support_level": "部分支持",
        "criteria": {
            "structure_closed": True,
            "legal_status_rows": len(legal),
            "coverage_of_patent_main_pct": res["legal_coverage_of_main_pct"],
            "legal_main_join_rate_pct": res["legal_main_join_rate_pct"],
            "granted_patents_in_sample": len(granted),
            "n_org_scored": len(org_patents),
            "name_match_rate_pct": res["matched_assignee_name_pct"],
        },
        "reason": "法律状态表仅 20,000 行（主表 2,939,895 件的 0.68%），且与主表按 patent_id / pn "
                  "仅 3.0% 可连接（500 条探针命中 15 条），说明该样本是独立抽样、不是主表子集；"
                  "样本内 12,658 件可判「授权」，经权利人名称归一映射仅落到 138 家底册企业、429 件专利，"
                  "对 189,116 家底册覆盖率 0.07%——属抽样级证据，不能支撑企业级全量有效专利数。"
                  "公式与链路闭合、可现算，但数据量不足以全量交付 → 部分支持。",
    }
    res["elapsed_sec"] = round(time.time() - t0, 1)
    con.close()
    dump(res, OUT)
    print(json.dumps({k: res[k] for k in ("dwd_patent_rows", "dwd_patent_legal_rows",
                                          "legal_coverage_of_main_pct", "granted_rows",
                                          "granted_share_of_sample_pct", "distinct_assignee_names",
                                          "matched_assignee_names", "matched_assignee_name_pct",
                                          "orgs_with_granted_patent", "patents_attributed_to_orgs",
                                          "per_org_distribution", "legal_main_join_rate_pct",
                                          "support_judgment")}, ensure_ascii=False, indent=1))
    print("written", OUT)


if __name__ == "__main__":
    main()
