#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TALENT_UI_IR_SPLIT · 人才产研结构对比（学术界 vs 产业界占比，UI「产研对比分析」分组柱图）

展示系统 UI 实扫指标（20261030 批 2）：
repos/demo-ui-science/src/pages/talent-trend/components/InsightPanel.jsx:131 irOption
（series name「科研」「产业」双柱，x 轴 labels=技术领域）；mock 数据源
pages/talent-trend/data.js:1161 generateIrSplit()（5 领域硬编码随机值）。
SRS 叶「产研对比分析」(seq 251) 只要求「展示学术界与产业界人才分布对比」，未给定义方法。

口径（推测定义，非甲方闭合）：
  学术 = 学者最近在任履历机构名命中高校表(dwd_forg_university_org_info.name_std)；
  产业 = 在任有机构名 − 学术（保守减法代理，误差方向：未收录院所被计入产业）。
  分子分母同池：在任(is_current=1)且 org_name_en 非空的 distinct 学者。

数据源：gkx（183.240.141.251:3318，只读）。产出：M_TALENT_UI_IR_SPLIT_out.json。
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
        "metric_id": "M_TALENT_UI_IR_SPLIT",
        "batch": "20261030_展示系统指标补充",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/talent-trend/components/InsightPanel.jsx:131",
            "repos/demo-ui-science/src/pages/talent-trend/data.js:1161",
        ],
        "requirement_trace": {
            "named_in_srs": True,
            "note": "SRS 叶「产研对比分析」(seq 251, excel_row 254) 要求展示学术界与产业界人才分布对比；"
                    "两份需求真源均未给计算口径，本件为推测定义。",
        },
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：在任履历截面（is_current=1），基期=数据装载日；无年份维。",
        "ctx_refs": {"note": "正文引用型数字登记，供闸5比对，不参与派生算术。",
                     "refs": ["183.240", "141.251", "3318", "34306", "1161", "131", "251", "254", "2.1", "2.2", "2.3", "1267"]},
    }

    # F1 主档与在任池
    cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
    out["facts"]["scholar_total"] = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(DISTINCT scholar_id) FROM gkx.dwd_scholar_work_experience "
        "WHERE is_current = 1")
    out["facts"]["current_exp_scholars"] = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(DISTINCT scholar_id) FROM gkx.dwd_scholar_work_experience "
        "WHERE is_current = 1 AND org_name_en IS NOT NULL AND org_name_en != ''")
    denom = cur.fetchone()[0]
    out["facts"]["current_exp_with_org_name"] = denom

    # F2 学术侧：高校表精确等值
    cur.execute(
        "SELECT COUNT(DISTINCT we.scholar_id) "
        "FROM gkx.dwd_scholar_work_experience we "
        "JOIN gkx.dwd_forg_university_org_info u "
        "  ON CONVERT(u.name_std USING utf8mb4) COLLATE utf8mb4_general_ci "
        "     = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci "
        "WHERE we.is_current = 1 AND we.org_name_en IS NOT NULL")
    academic = cur.fetchone()[0]
    out["facts"]["academic_university_scholars"] = academic

    # F3 研究院表负证据探针（列名假设不猜，报错即记）
    try:
        cur.execute(
            "SELECT COUNT(DISTINCT we.scholar_id) "
            "FROM gkx.dwd_scholar_work_experience we "
            "JOIN gkx.dwd_research_institute_base_info i "
            "  ON CONVERT(i.name_en USING utf8mb4) COLLATE utf8mb4_general_ci "
            "     = CONVERT(we.org_name_en USING utf8mb4) COLLATE utf8mb4_general_ci "
            "WHERE we.is_current = 1 AND we.org_name_en IS NOT NULL")
        inst_hits = cur.fetchone()[0]
        out["facts"]["institute_matched_scholars"] = inst_hits
        academic_total = academic + inst_hits
    except Exception as e:
        out["absence_probe"].append({
            "probe": "gkx.dwd_research_institute_base_info JOIN i.name_en = we.org_name_en",
            "error": str(e)[:200],
            "verdict_kind": "negative_evidence",
        })
        inst_hits = None
        academic_total = academic

    # F4 产业侧 = 池 − 学术并集
    industry = max(denom - academic_total, 0)
    out["facts"]["industry_scholars_proxy"] = industry
    out["facts"]["academic_total_used"] = academic_total

    # D 派生比（B 形态 dict：键名带分母）
    def pct(num, den):
        return round(num * 100.0 / den, 4) if den else None

    out["derived"]["academic_share_of_named_current_pct"] = {
        "value": pct(academic_total, denom),
        "numerator": academic_total,
        "denominator": denom,
        "note": "分母 = facts.current_exp_with_org_name（在任且有机构名的 distinct 学者），"
                "分子 = 高校表命中" + ("" if inst_hits is None else " + 研究院表命中"),
    }
    out["derived"]["industry_share_of_named_current_pct"] = {
        "value": pct(industry, denom),
        "numerator": industry,
        "denominator": denom,
        "note": "分子 = 分母 − 学术侧（保守减法代理）",
    }
    out["derived"]["industry_per_academic_ratio"] = {
        "value": round(industry / academic_total, 4) if academic_total else None,
        "numerator": industry,
        "denominator": academic_total,
        "note": "产业人数 / 学术人数（UI 双柱比值形态）",
    }
    out["derived"]["current_exp_share_pct"] = {
        "value": pct(out["facts"]["current_exp_scholars"], out["facts"]["scholar_total"]),
        "numerator": out["facts"]["current_exp_scholars"],
        "denominator": out["facts"]["scholar_total"],
        "note": "在任履历覆盖率（口径池相对主档 21,316）",
    }

    # 判档
    out["support_judgment"] = "部分支持"
    out["notes"].append(
        "学术侧链路（履历→高校表名等值）结构+数据量足；产业侧无机构类型字典字段支撑直分，"
        "只能做减法代理（absence_probe 记录研究院表探测结果），故部分支持。"
        "升档触发器：机构类型字典上线后按字典直分学术/产业/其他三分类。")
    out["notes"].append(
        "collation 归一沿用共享快照：JOIN 两表必须 CONVERT...COLLATE utf8mb4_general_ci。")
    out["notes"].append(
        "UI mock（data.js:1161-1165）为 5 领域硬编码随机值，正式版替换后双柱读数以本件口径为准。")

    dest = _HERE / "M_TALENT_UI_IR_SPLIT_out.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("saved", dest)
    print(json.dumps(out["facts"], ensure_ascii=False))
    for k, v in out["derived"].items():
        print(k, "=", v["value"])


if __name__ == "__main__":
    main()
