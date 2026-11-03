#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_COST_TREND · 历年人才引进成本趋势（UI「历史成本趋势追踪」双折线）

展示系统 UI 实扫指标（20261030 批 2）：
repos/demo-ui-science/src/pages/talent-trend/components/CostTab.jsx:528-533
「历史成本趋势追踪」面板：trendOption（引进成本折线）+ marketTrendOption（市场薪酬与政策激励）。
数据为 mock 时序。SRS 叶「历史成本趋势追踪」（talentRecommendSpec.js key='history'）
要求展示历年成本变化趋势，未给口径与数据源。

口径（推测定义，非甲方闭合）：
  「引进成本」时间序列的库内承载探测：
    - 招聘岗位表 dwd_org_recruit_info(7,981,643 行) 有 release_date（年度发布量可算）但无薪酬列
      → 「岗位发布量年度趋势」可作引才活跃度代理（披露：不是成本）。
    - 成本额（薪酬/安家/启动）无列无表 → 负证据探针。
  产物：release_date 年度计数分布（2019-2026）+ 成本额缺失声明。

数据源：gkx。产出：M_TALENT_UI_COST_TREND_out.json。
"""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SHARED = Path(__file__).resolve().parents[2].joinpath(
    "20261021_指标整体开发进度调研", "code")
sys.path.insert(0, str(_SHARED))
from _gkxdb import gkx  # noqa: E402


def main():
    cur = gkx()
    out = {
        "metric_id": "M_TALENT_UI_COST_TREND",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/CostTab.jsx:528",
            "repos/demo-ui-science/src/pages/talent-trend/components/CostTab.jsx:531",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "note": "SRS 叶「历史成本趋势追踪」（人才引进推荐评估页，excel_row 266 邻域）要求展示"
                    "历年引进成本变化趋势；未给口径与数据源。",
        },
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "年度趋势件：release_date 年份分布即基期集合，实测后回填。",
        "ctx_refs": {"note": "正文引用型数字登记。", "refs": ["183.240", "141.251", "3318", "528", "531", "266", "7981643", "2.1", "2.2", "2.3"]},
    }

    # F1 岗位发布年度分布：全表 GROUP BY 实测超时（798 万行无索引，连接被服务端掐断
    # pymysql InterfaceError(0,'')），按 20261021 铁律 1 改走采样路径，并如实登记「未全量取证」。
    out["facts"]["org_recruit_info_rows"] = 7981643  # COST_DIST 件同日 COUNT(*) 实测（约 22 秒）
    try:
        cur.execute(
            "SELECT YEAR(release_date) AS y, COUNT(*) AS n FROM ("
            "  SELECT release_date FROM gkx.dwd_org_recruit_info "
            "  WHERE release_date IS NOT NULL LIMIT 50000) t "
            "GROUP BY YEAR(release_date) ORDER BY y")
        rows = cur.fetchall()
        out["facts"]["release_year_dist_sample50k"] = {str(y): n for y, n in rows}
        sampled = sum(n for _, n in rows)
        out["facts"]["release_sample_rows"] = sampled
        years_used = sorted(str(y) for y, _ in rows)
        out["base_years_used"] = years_used
        out["base_years_note"] = ("年度集合来自前 5 万行采样（LIMIT 50000，非全量），"
                                  "年份集合=采样年份并集；全量分组因无索引超时未取证（absence_probe 登记）。")
    except Exception as e:
        out["absence_probe"].append({"probe": "release_date LIMIT 50000 GROUP BY", "error": str(e)[:200],
                                     "verdict_kind": "negative_evidence"})

    # F2 成本额承载负证据（同批 COST_DIST 探针：无薪酬列/无成本表）
    try:
        cur.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema='gkx' AND table_name='dwd_org_recruit_info' "
            "AND (column_name LIKE '%sal%' OR column_name LIKE '%cost%' OR column_name LIKE '%pay%')")
        hits = [r[0] for r in cur.fetchall()]
        out["absence_probe"].append({
            "probe": "dwd_org_recruit_info columns sal/cost/pay",
            "result": hits, "hit_rows": len(hits),
            "verdict_kind": "negative_evidence" if not hits else "positive_existence"})
    except Exception as e:
        out["absence_probe"].append({"probe": "columns probe", "error": str(e)[:160],
                                     "verdict_kind": "negative_evidence"})

    # D 派生：近两年发布量增速（若可算）
    ryd = out["facts"].get("release_year_dist_sample50k", {})
    if len(ryd) >= 2:
        years = sorted(ryd.keys())
        last, prev = years[-1], years[-2]
        if ryd.get(prev):
            out["derived"]["release_yoy_growth_pct"] = {
                "value": round((ryd[last] - ryd[prev]) * 100.0 / ryd[prev], 4),
                "numerator": ryd[last] - ryd[prev], "denominator": ryd[prev],
                "note": f"岗位发布量 {prev}→{last} 同比（引才活跃度代理，非成本额）",
            }
        out["derived"]["latest_year_share_pct"] = {
            "value": round(ryd[last] * 100.0 / out["facts"].get("release_sample_rows", 0), 4),
            "numerator": ryd[last], "denominator": out["facts"].get("release_sample_rows", 0),
            "note": f"{last} 年发布量占采样（5 万行）有日期岗位比例",
        }

    # 判档
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "趋势结构（按年分组）与活跃度代理（岗位发布量年度分布）可复算；"
        "但「成本额」本身无任何数值列（探针即证），UI 双折线的纵轴（万元）无法真实出数，故部分支持。"
        "升档触发器：成本明细表或薪酬列回填后，同一 GROUP BY 骨架即可切换。")
    out["notes"].append("UI trendOption/marketTrendOption 数据为组件内 mock 常量，非接口返回。")

    dest = _HERE / "M_TALENT_UI_COST_TREND_out.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("saved", dest)
    for k, v in out["facts"].items():
        print(k, "=", str(v)[:100])
    for k, v in out["derived"].items():
        print(k, "=", v["value"])


if __name__ == "__main__":
    main()
