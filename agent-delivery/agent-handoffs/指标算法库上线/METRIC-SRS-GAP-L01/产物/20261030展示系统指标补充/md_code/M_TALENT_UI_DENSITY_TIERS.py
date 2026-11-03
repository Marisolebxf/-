#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_DENSITY_TIERS · 人才密度分层区域数（UI 地图图例「高/中/一般密度区域」）

展示系统 UI 实扫指标（20261030 批 2）：
repos/demo-ui-science/src/pages/talent-trend/components/DistributionInsightView.jsx:376-378
legendItems = 高密度(#165dff)/中密度(#4080ff)/一般(#93c5fd)；:381-385 intensity = round(value/8500*100)
——mock 把区域 talent 数除以常数 8500 归一为 0-100 热力强度，即 UI 的分层本质是
「区域人才数三分位」。SRS 叶「人才分布信息查看」(seq 243) 要求"通过颜色深浅或热力显示
不同地区的人才密度"，未给分层数与阈值。

口径（推测定义，非甲方闭合）：
  区域 = 国家（dwd_forg_university_org_info.country，与批 1 GLOBAL_STOCK 口径 B 同一地理链）；
  区域人才数 = 可地理解析学者的国别计数；
  分层 = 按区域人才数降序的三分位（高/中/一般），阈值由数据分位决定，不用 mock 常数 8500。
  并列披露：等频三分位的断点值与各区计数。

数据源：gkx。产出：M_TALENT_UI_DENSITY_TIERS_out.json。
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
        "metric_id": "M_TALENT_UI_DENSITY_TIERS",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/DistributionInsightView.jsx:376",
            "repos/demo-ui-science/src/pages/talent-trend/components/DistributionInsightView.jsx:381",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "note": "SRS 叶「人才分布信息查看」(seq 243, excel_row 246)：『通过颜色深浅或热力显示不同地区的人才密度』；"
                    "未定义分层数与阈值。mock 用 value/8500*100 归一。",
        },
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：在任履历→国别截面计数，基期=数据装载日。",
        "ctx_refs": {"note": "正文引用型数字登记，供闸5比对。", "refs": ["183.240", "141.251", "3318", "376", "378", "381", "8500", "243", "246", "2.1", "2.2", "2.3", "2.4"]},
    }

    # F1 区域人才计数（国别，批1同链）
    cur.execute(
        "SELECT u.country, COUNT(DISTINCT we.scholar_id) AS n "
        "FROM gkx.dwd_scholar_work_experience we "
        "JOIN gkx.dwd_forg_university_org_info u "
        "  ON CONVERT(u.name_std USING utf8mb4) COLLATE utf8mb4_general_ci "
        "     = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci "
        "WHERE we.is_current = 1 AND u.country IS NOT NULL AND u.country != '' "
        "GROUP BY u.country ORDER BY n DESC")
    rows = cur.fetchall()
    out["facts"]["country_count"] = len(rows)
    out["facts"]["top10"] = [{"country": c, "scholars": n} for c, n in rows[:10]]
    total_geo = sum(n for _, n in rows)
    out["facts"]["geo_resolvable_scholars"] = total_geo

    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
    total_all = cur.fetchone()[0]
    out["facts"]["scholar_total"] = total_all

    # 分层：等频三分位（按国别数）
    vals = [n for _, n in rows]
    k = len(vals)
    hi_cut = vals[k // 3] if k >= 3 else vals[0]
    mid_cut = vals[2 * k // 3] if k >= 3 else vals[-1]
    hi = [v for v in vals if v >= hi_cut]
    mid = [v for v in vals if mid_cut <= v < hi_cut]
    low = [v for v in vals if v < mid_cut]
    out["facts"]["tier_cuts"] = {"high_min": hi_cut, "mid_min": mid_cut}
    out["facts"]["tier_country_counts"] = {"high": len(hi), "mid": len(mid), "low": len(low)}
    out["facts"]["tier_scholar_sums"] = {"high": sum(hi), "mid": sum(mid), "low": sum(low)}

    # D 派生
    def pct(num, den):
        return round(num * 100.0 / den, 4) if den else None
    out["derived"]["geo_coverage_pct"] = {
        "value": pct(total_geo, total_all), "numerator": total_geo, "denominator": total_all,
        "note": "地理可解析学者 / 主档全量（批 1 GLOBAL_STOCK 口径 B 同链，数字应一致）",
    }
    out["derived"]["high_tier_country_share_pct"] = {
        "value": pct(len(hi), k), "numerator": len(hi), "denominator": k,
        "note": "高密度国家数 / 全部国家数（等频三分位）",
    }
    out["derived"]["high_tier_scholar_share_pct"] = {
        "value": pct(sum(hi), total_geo), "numerator": sum(hi), "denominator": total_geo,
        "note": "高密度国家人才合计 / 可解析人才总量（分层代表性）",
    }

    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "分层结构可行（国别人才数可算、分位阈值可复算）；但地理覆盖仅约四成（同批 1 口径 B），"
        "未覆盖学者无法进入分层，密度地图存在高校集中偏差，故部分支持。"
        "升档触发器：非高校机构地理编码补全后按同一三分位规则重算。")
    out["notes"].append("mock 的 8500 常数被替换为数据分位阈值，正式版热力图读数会与 demo 不同，属预期。")

    dest = _HERE / "M_TALENT_UI_DENSITY_TIERS_out.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("saved", dest)
    for k, v in out["facts"].items():
        print(k, "=", str(v)[:80])
    for k, v in out["derived"].items():
        print(k, "=", v["value"])


if __name__ == "__main__":
    main()
