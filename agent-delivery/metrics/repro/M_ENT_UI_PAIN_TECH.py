#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_UI_PAIN_TECH · 技术研发（企业发展痛难点分析·痛难点维度）

UI：科技专题服务系统 企业分析>企业发展痛难点分析>诊断范围「技术研发」勾选维（诊断范围码 tech_rd）。
需求文档未给该维判定口径。SYSINT-TOPIC-CHAIN-ALIGN-02-L01 对照：久新候选
M_TECH_MATURITY_LEVEL / M_TECH_STAGE_JUDGE（ads_technology_stage_assessment 38,860 行有数据），
但久新是「技术节点」粒度而非「企业研发痛难点」粒度——口径不同粒，不能直读。

本件口径（推测定义）：技术研发维可观测面 = 企业专利活动强度（gkx dwd_patent 申请+授权，
assignee org 关联）+ 研发投入（live enterprise_base.rd_staff_count/rd_staff_ratio 列在、行级覆盖另测）。

数据源：gkx 专利 293.99 万件 + live enterprise_base 研发列。产出：out/M_ENT_UI_PAIN_TECH_out.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _gkxdb import gkx, live, gkx_count, live_count  # noqa: E402


def main():
    cur = gkx()
    out = {
        "metric_id": "M_ENT_UI_PAIN_TECH",
        "batch": "TOPIC-UI-GAP-L01",
        "ui_evidence": [
            "live 30892 企业分析>企业发展痛难点分析>诊断范围「技术研发」（20261104 盘点实拍）",
            "02-缺口指标清单.xlsx seq28（SYSINT 表标注久新候选 M_TECH_MATURITY_LEVEL 等）",
        ],
        "facts": {},
        "derived": {},
        "absence_probe": [],
        "support_judgment": None,
        "notes": [],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面件：专利存量与研发人员存量。",
        "ctx_refs": {"note": "正文引用型数字登记。", "refs": []},
    }

    # F1 gkx 专利面（企业维）
    out["facts"]["patent_rows"] = gkx_count("dwd_patent")
    cur.execute("SHOW TABLES FROM gkx LIKE '%assignee%'")
    out["facts"]["assignee_tables"] = [r[0] for r in cur.fetchall()]
    for t in out["facts"]["assignee_tables"]:
        if "bak" not in t:
            cur.execute(f"SELECT COUNT(*) FROM gkx.{t}")
            out["facts"]["assignee_rows"] = cur.fetchone()[0]
            cur.execute(f"SHOW COLUMNS FROM gkx.{t}")
            out["facts"]["assignee_cols"] = [r[0] for r in cur.fetchall()][:14]
            break

    # F2 live 研发列
    try:
        lc = live()
        lccur = lc.cursor()
        lccur.execute("SELECT COUNT(*) FROM enterprise_base")
        out["facts"]["live_enterprise_base_rows"] = list(lccur.fetchone().values())[0]
        lccur.execute("SELECT COUNT(*) FROM enterprise_base WHERE rd_staff_count IS NOT NULL")
        out["facts"]["live_rd_staff_nonnull"] = list(lccur.fetchone().values())[0]
        lccur.execute("SELECT COUNT(*) FROM enterprise_base WHERE rd_staff_ratio IS NOT NULL")
        out["facts"]["live_rd_ratio_nonnull"] = list(lccur.fetchone().values())[0]
    except Exception as e:
        out["facts"]["live_error"] = f"ERR:{e}"

    # F3 久新面（技术节点粒度，口径不同粒披露）
    out["facts"]["jiuxin_note"] = ("ads_technology_stage_assessment 38,860 行（技术节点×阶段研判），"
                                   "粒度为技术节点非企业；M_ENT_UI_PAIN_BATCH_PROBE 探针留证。")

    # D 派生
    if "live_rd_staff_nonnull" in out["facts"] and out["facts"].get("live_enterprise_base_rows"):
        out["derived"]["rd_staff_coverage_pct"] = {
            "value": round(out["facts"]["live_rd_staff_nonnull"] / out["facts"]["live_enterprise_base_rows"] * 100, 4),
            "numerator": out["facts"]["live_rd_staff_nonnull"],
            "denominator": out["facts"]["live_enterprise_base_rows"],
            "denominator_note": "rd_staff_count 非空行 / live enterprise_base 总行数（同表同 WHERE）",
        }

    out["support_judgment"] = "部分支持"
    out["notes"].append("专利面 gkx 全量在；live 研发列存在但覆盖待扩（见 derived 覆盖率）；"
                        "「构成技术研发痛难点」的模型判定未闭合 → 部分支持。")
    p = HERE / "out" / "M_ENT_UI_PAIN_TECH_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", p)
    print("patent_rows =", out["facts"]["patent_rows"], "| live eb rows =", out["facts"].get("live_enterprise_base_rows"))


if __name__ == "__main__":
    main()
