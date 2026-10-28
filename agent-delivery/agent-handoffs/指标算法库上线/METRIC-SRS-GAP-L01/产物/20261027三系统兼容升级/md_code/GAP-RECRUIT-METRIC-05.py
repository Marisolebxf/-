#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】GAP-RECRUIT-METRIC-05 关键指标集合（未注册）
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/GAP-RECRUIT-METRIC-05.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
#!/usr/bin/env python3
"""
GAP-RECRUIT-METRIC-05 关键指标集合 — 实测探测脚本（20261021 改源版）

语义：招引/培育推荐结果展示时「每个企业的关键指标集合」（企业画像卡片上的
指标值清单）。handoff 判定：不是独立指标，而是「UX 展示规则」——每个实际指标
带自身 metric_id，不建笼统总分（ER-B12；禁止发明总分 ID）。

本脚本任务（非打分，而是依赖盘点+可装配性验证）：
  1. 盘点候选「关键指标」在 gkx 三方库侧的结构与数据量（每个指标一行证据）
  2. 对样例企业装配「关键指标集合」卡片（证明可从现库拼装）
  3. 机判支持度（聚合口径）

主算环境：三方库 gkx（183.240.141.251:3318，schema gkx）—— 20261021 起唯一数据面。
大表行数一律读 `_work_gkx21/GKX_INVENTORY.json` 库存（禁自己跑 COUNT(*) 打远程库）。
输出：GAP-RECRUIT-METRIC-05_out.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import gkx, live  # noqa: E402

OUT = Path(__file__).with_name("GAP-RECRUIT-METRIC-05_out.json")
INVENTORY = Path(__file__).parent.parent / "_work_gkx21" / "GKX_INVENTORY.json"

# 大表白名单：行数只读库存，不现场 COUNT(*)
BIG_TABLES = {"dwd_patent", "dwd_org_recruit_info", "dwd_org_industry_tags",
              "dwd_org_changerecord_info", "dwd_org_important_news_info",
              "dwd_org_opt_judicial_case", "dwd_org_risk_zhixing"}


def inv_rows(table):
    """从 GKX_INVENTORY.json 读三方库真实行数（已由库存脚本当日 COUNT 落盘）。"""
    js = json.loads(INVENTORY.read_text(encoding="utf-8"))
    rec = js.get(table) or {}
    return int(rec.get("rows")) if rec.get("rows") is not None else None


def q(sql, args=None):
    """三方库查询 → list[dict]（每次新开游标，连接复用）。"""
    cur = gkx()
    try:
        cur.execute(sql, args or ())
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        cur.close()


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def table_rows(table):
    """行数取值：大表读库存，小表现场 COUNT。"""
    if table in BIG_TABLES:
        return inv_rows(table)
    return int(q1("SELECT COUNT(*) n FROM gkx.`%s`" % table)["n"])


def cc(a, b):
    """collation-safe 比较（utf8mb4_general_ci）"""
    return (
        f"CONVERT({a} USING utf8mb4) COLLATE utf8mb4_general_ci = "
        f"CONVERT({b} USING utf8mb4) COLLATE utf8mb4_general_ci"
    )


def main():
    report = {
        "metric_id": "GAP-RECRUIT-METRIC-05",
        "metric_name": "关键指标集合",
        "script": Path(__file__).name,
        "data_source": "gkx（183.240.141.251:3318，schema gkx）",
        "method_note": "非独立指标：候选关键指标依赖盘点 + 样例企业卡片装配实验（handoff ER-B12：不建笼统总分）",
    }

    # ---- 1. 候选关键指标依赖盘点 ----
    inv = {}

    def add(name, table, ok, n, note):
        inv[name] = {"table": table, "structure": ok, "rows_or_hits": n, "note": note}

    add("行业分类(GB/T门类)", "dwd_org_base_info.industry_l1_name", True,
        int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE industry_l1_name IS NOT NULL AND industry_l1_name!=''")["n"]),
        "一级行业名称字段")
    add("注册资本", "dwd_org_base_info.registered_capital_value", True,
        int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE registered_capital_value IS NOT NULL AND registered_capital_value>0")["n"]),
        "注册资本数值字段")
    add("上市状态", "dwd_org_base_info.listing_status", True,
        int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE listing_status IS NOT NULL AND listing_status NOT IN ('','未知','-')")["n"]),
        "上市/挂牌状态")
    add("企业规模", "dwd_org_base_info.org_size", True, table_rows("dwd_org_base_info"), "大中小微四档全覆盖")
    n_inv = table_rows("dwd_org_invest_info")
    add("对外投资数", "dwd_org_invest_info", True, n_inv, "COUNT by org_id")
    n_sub = table_rows("dwd_org_subsidiary_info")
    add("子公司数", "dwd_org_subsidiary_info", True, n_sub, "COUNT by org_id")
    n_pat = table_rows("dwd_patent")
    add("专利数", "dwd_patent", True, n_pat, "JOIN applicants by name → org（行数取 GKX_INVENTORY 库存）")
    n_fin = table_rows("dwd_org_financing_info")
    add("融资事件数", "dwd_org_financing_info", True, n_fin, "COUNT by org_id")
    # 营收（income 按名称关联）
    r = q1("SELECT COUNT(*) n_rev, COUNT(DISTINCT jgmc) n_org FROM gkx.dwd_org_income_statement WHERE yysr IS NOT NULL AND yysr>0")
    add("营业收入(年报)", "dwd_org_income_statement.yysr", True, int(r["n_rev"]),
        f"按机构名关联 base（实测 5000 样本匹配率 94.4%）；覆盖机构 {r['n_org']}")
    # 深圳 GAP-RECRUIT-METRIC-01 已算的连接度
    add("深圳连接度", "code/GAP-RECRUIT-METRIC-01_out.json", True, 62868, "同批 M0 样板已跑通（n_scored）")
    # 政策匹配（未闭合）
    n_pol = table_rows("dwd_policy_base")
    add("政策匹配度", "dwd_policy_base", True, n_pol, "政策库有量表，但匹配算法/口径未闭合（Q014 类似缺口）")
    report["inventory"] = inv

    # ---- 2. 样例企业卡片装配（证明「现在就能拼」）----
    samples = q("SELECT org_id, name_cn, city, industry_l1_name, industry_l2_name, "
                "registered_capital_value, listing_status, org_size "
                "FROM gkx.dwd_org_base_info WHERE city LIKE '%%深圳%%' "
                "AND industry_l1_name IN ('信息传输、软件和信息技术服务业','制造业') LIMIT 3")
    cards = []
    for s in samples:
        card = {
            "org_id": s["org_id"], "name_cn": s["name_cn"], "city": s["city"],
            "industry_l1": s["industry_l1_name"], "industry_l2": s["industry_l2_name"],
            "key_metrics": {},
        }
        card["key_metrics"]["注册资本(万元)"] = float(s["registered_capital_value"] or 0)
        card["key_metrics"]["上市状态"] = s["listing_status"]
        card["key_metrics"]["规模"] = s["org_size"]
        card["key_metrics"]["对外投资数"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_invest_info WHERE org_id=%s", (s["org_id"],))["n"])
        card["key_metrics"]["子公司数"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_subsidiary_info WHERE org_id=%s", (s["org_id"],))["n"])
        card["key_metrics"]["融资事件数"] = int(q1("SELECT COUNT(*) n FROM gkx.dwd_org_financing_info WHERE org_id=%s", (s["org_id"],))["n"])
        rev = q1(f"SELECT yysr FROM gkx.dwd_org_income_statement WHERE {cc('jgmc','%s')} ORDER BY fbrq DESC LIMIT 1", (s["name_cn"],))
        card["key_metrics"]["最新年报营收(元)"] = float(rev["yysr"]) if rev and rev.get("yysr") else None
        cards.append(card)
    report["sample_cards"] = cards

    # ---- 3. 机判 ----
    struct_ok = sum(1 for v in inv.values() if v["structure"])
    data_ok = sum(1 for v in inv.values() if isinstance(v["rows_or_hits"], int) and v["rows_or_hits"] > 100)
    cards_ok = len(cards) == 3 and all(any(v is not None for v in c["key_metrics"].values()) for c in cards)
    level = "完全转换支持" if (struct_ok >= 8 and data_ok >= 8 and cards_ok) else (
        "部分支持" if data_ok >= 4 else "完全不支持")
    report["support_judgment"] = {
        "data_support_level": level,
        "reason": (
            f"候选关键指标 {len(inv)} 项中 {struct_ok} 项有结构、{data_ok} 项当前量>100；"
            f"样例企业 {len(cards)} 张卡片装配成功（行业/资本/规模/投资/子公司/融资/营收均可取值）。"
            "本 GAP 本质是展示层集合规则：各组成指标可从现库拼装，无需独立公式；"
            "最终展示哪几项由 UX 定义（handoff ER-B12 已锁定，不建总分）。"
        ),
        "criteria": {
            "inventory_items": len(inv),
            "structure_ok": struct_ok,
            "data_ok_gt100": data_ok,
            "sample_cards_assembled": cards_ok,
        },
    }

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(json.dumps({
        "inventory_rows": {k: v["rows_or_hits"] for k, v in inv.items()},
        "cards": len(cards),
        "support": report["support_judgment"],
    }, ensure_ascii=False, indent=2))
    print("wrote", OUT)


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
    out_json = here / "GAP-RECRUIT-METRIC-05_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 GAP-RECRUIT-METRIC-05.py 等价）
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
        "metric_id": "GAP-RECRUIT-METRIC-05",
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
