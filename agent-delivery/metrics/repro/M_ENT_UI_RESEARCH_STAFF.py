#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_RESEARCH_STAFF · 科研人数（门户服务>企业发展>企业整体概况 badge）

UI：科技专题服务系统 门户服务>企业发展>企业整体概况「科研人数」读数（live 30892，20261104 盘点）。
SYSINT-TOPIC-CHAIN-ALIGN-02-L01 对照：久新候选 M_TALENT_SUPPLY_STRUCT（ads_talent_yearly_metrics
1,278,048 行 / ads_talent_profile 100,000 行，实测有数据）；久新为人才粒度非企业粒度，
「某企业科研人数」需经 current_institution 关联到我方 org 才可算（口径未对齐，待三分清单）。

本件口径（推测定义）：企业维科研人数 = live enterprise_base.rd_staff_count（企业研发人员数列，
直读列）；区域汇总 = Σ rd_staff_count。久新路径并列表述（人才粒度原料在、企业粒度结果需自算）。

数据源：live gkxlumenx_dwd.enterprise_base（主）+ 久新 ads_talent_*（旁证披露）。产出：out/M_ENT_UI_RESEARCH_STAFF_out.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _gkxdb import live  # noqa: E402


def main():
    out = {
        "metric_id": "M_ENT_UI_RESEARCH_STAFF",
        "batch": "TOPIC-UI-GAP-L01",
        "ui_evidence": [
            "live 30892 门户服务>企业发展>企业整体概况「科研人数」badge（20261104 盘点实拍）",
            "02-缺口指标清单.xlsx seq161（SYSINT 表标注久新候选 M_TALENT_SUPPLY_STRUCT 等）",
        ],
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "存量截面：rd_staff_count 为时点值。",
        "ctx_refs": {"note": "正文引用型数字登记。", "refs": []},
    }

    lc = live()
    c = lc.cursor()
    c.execute("SELECT COUNT(*) AS n FROM enterprise_base")
    out["facts"]["eb_rows"] = list(c.fetchone().values())[0]
    c.execute("SELECT COUNT(*) AS n FROM enterprise_base WHERE rd_staff_count IS NOT NULL")
    out["facts"]["rd_nonnull_rows"] = list(c.fetchone().values())[0]
    c.execute("SELECT COUNT(*) AS n FROM enterprise_base WHERE rd_staff_count > 0")
    out["facts"]["rd_pos_rows"] = list(c.fetchone().values())[0]
    c.execute("""SELECT MIN(rd_staff_count) AS mn, MAX(rd_staff_count) AS mx,
                        ROUND(AVG(rd_staff_count), 2) AS avg_v
                 FROM enterprise_base WHERE rd_staff_count > 0""")
    r = list(c.fetchone().values())
    out["facts"]["rd_pos_stats"] = {"min": r[0], "max": r[1], "avg": float(r[2]) if r[2] is not None else None}
    c.execute("""SELECT name, rd_staff_count FROM enterprise_base
                 WHERE rd_staff_count > 0 ORDER BY rd_staff_count DESC LIMIT 5""")
    out["facts"]["top5"] = [{"org": list(x.values())[0], "rd_staff": list(x.values())[1]} for x in c.fetchall()]
    c.execute("SELECT SUM(rd_staff_count) AS s FROM enterprise_base")
    out["facts"]["rd_total_sum"] = list(c.fetchone().values())[0]

    out["derived"]["rd_pos_row_share_pct"] = {
        "value": round(out["facts"]["rd_pos_rows"] / max(out["facts"]["eb_rows"], 1) * 100, 4),
        "numerator": out["facts"]["rd_pos_rows"],
        "denominator": out["facts"]["eb_rows"],
        "denominator_note": "rd_staff_count>0 行 / enterprise_base 总行数（同表）",
    }
    out["derived"]["rd_nonnull_row_share_pct"] = {
        "value": round(out["facts"]["rd_nonnull_rows"] / max(out["facts"]["eb_rows"], 1) * 100, 4),
        "numerator": out["facts"]["rd_nonnull_rows"],
        "denominator": out["facts"]["eb_rows"],
        "denominator_note": "rd_staff_count 非空行 / 总行数（非空与>0 两口径并列，B1 键名服从算法）",
    }

    out["support_judgment"] = "完全转换支持"
    out["notes"].append("live rd_staff_count 列直读即可复现页面语义（企业研发人员数）；"
                        "久新 ads_talent_* 为人才粒度原料（current_institution 关联后可算企业维），"
                        "口径未对齐待三分清单，不构成降档——我方列直查已完全可算。")
    p = HERE / "out" / "M_ENT_UI_RESEARCH_STAFF_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", p)
    print("eb_rows =", out["facts"]["eb_rows"], "| rd>0 rows =", out["facts"]["rd_pos_rows"],
          "| rd sum =", out["facts"]["rd_total_sum"])


if __name__ == "__main__":
    main()
