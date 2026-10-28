#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_ENT_PATENT_VALID_COUNT 有效专利数（未注册）
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_ENT_PATENT_VALID_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
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


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

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
    out_json = here / "M_ENT_PATENT_VALID_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_ENT_PATENT_VALID_COUNT.py 等价）
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
        "metric_id": "M_ENT_PATENT_VALID_COUNT",
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
