#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_P10_044 创新券抵扣金额（科技创新券）—— 薄壳校验脚本。

共享探针真源：code/_shared_s308_laneC.py（三源券词族 + 支付/补贴词族）
UI：incubation-carrier-new/mockData.js:709 政策步骤条目「券额抵扣」。
需规背景：阶段一·五对账 5 个「否」之一——创新券抵扣金额为需求文档真未覆盖（演示数据或超需求范围）。
三源券词族（voucher/coupon）0 命中 → 完全不支持。
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SHARED = "_snapshots/_shared_s308_laneC_out.json"
OUT = "M_SCIUI_P10_044_out.json"


def main() -> None:
    with open(SHARED, encoding="utf-8") as f:
        snap = json.load(f)
    dev = snap["dev"]
    gkx = snap["gkx"]
    jx = snap["jiuxin"]

    assert dev["dev_voucher_family_table_hits"] == []
    assert gkx["gkx_voucher_family"] == []
    assert jx["jiuxin_voucher_family"] == []

    out = {
        "metric_id": "M_SCIUI_P10_044",
        "batch": "S3-08",
        "ui_evidence": [
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/mockData.js:709",
            "repos/demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/mockData.js:703-716",
        ],
        "requirement_trace": {
            "named_in_srs": False,
            "note": "「创新券抵扣金额」为阶段一·五需求对账 5 个「否」之一（01 清单 550 行 5 否）：经人工核实为需求文档真未覆盖（演示数据或超需求范围）——bid-reference 全文 rg 创新券 0 命中。UI 挂载为政策卡 P08 步骤条目「券额抵扣」（mockData.js:709），非数值指标位。",
        },
        "facts": {
            "ui_mount": "mockData.js:703-716 政策 P08「深圳市科技创新券支持政策」：:704 summary（凭创新券抵扣）/ :705 benefit（每年最高申领 50 万元）/ :706-711 steps 四步（领券申请→服务对接→:709 券额抵扣→机构兑付）/ :713-716 milestones（2026-01-15 申领开放/11-30 用券截止/12-31 兑付截止）",
            "ui_mount_note": "挂载位是政策流程步骤条目与政策福利文案，无任何金额数值位（benefit 50 万元为政策原文上限非统计值）——ui_demo_fallback 披露",
            "probe_dev_voucher_tables": dev["dev_voucher_family_table_hits"],
            "probe_dev_pay_family_tables": dev["dev_pay_family_table_hits"],
            "probe_gkx_voucher_family": gkx["gkx_voucher_family"],
            "probe_jiuxin_voucher_family": jx["jiuxin_voucher_family"],
            "probe_dev_table_total": dev["dev_table_total"],
            "probe_gkx_table_count": gkx["gkx_table_count"],
            "probe_jiuxin_table_count_live": jx["jiuxin_table_count_live"],
            "reqdoc_check": "bid-reference 全文（主需求+核增+SRS 33 页）rg 创新券/科技券/兑付 → 0 命中（2026-11-02 实查）",
        },
        "derived": [
            {
                "name": "innovation_voucher_deduction_amount",
                "value": None,
                "note": "负结论 null 登记：创新券兑付/抵扣金额流水三源零承载（voucher/coupon 词族 dev 0/gkx 0/jiuxin 0）；dev pay_* 商城支付语义（goods/refund/trade）与创新券财政兑付不同域，不可代理。",
            },
        ],
        "absence_probe": [
            {
                "probe": "dev 17 schema（542 表）创新券词族（voucher/coupon 表名+列名）",
                "source": "dev",
                "sql": "information_schema 词族扫描（快照 dev_voucher_family_table_hits=[]）；pay/fund/subsid 词族命中 14 表全为商城支付（pay_*）或项目资助（fund_project/enterprise_forg_finance_history）语义",
                "hits": 0,
            },
            {
                "probe": "gkx 280 表创新券词族",
                "source": "gkx",
                "sql": "information_schema.tables REGEXP voucher|coupon（快照 gkx_voucher_family=[]）",
                "hits": 0,
            },
            {
                "probe": "jiuxin 218 表（SHOW TABLES 实数）创新券词族",
                "source": "jiuxin",
                "sql": "SHOW TABLES + 表名匹配（快照 jiuxin_voucher_family=[]）；fund 词族命中为科研方向资助证据表（research_problem_funding_evidence/shenzhen_institution_*_funding）非券兑付流水",
                "hits": 0,
            },
        ],
        "support_judgment": "完全不支持",
        "notes": [
            "判档理由：创新券抵扣金额=兑付流水聚合（企业×服务机构×合同金额×抵扣比例），承载要求是券平台交易流水表——三源 voucher/coupon 词族 0 命中（dev 542/gkx 280/jiuxin 218 逐一实查）；dev pay_* 族是商城支付域（goods_order/refund/trade）与财政创新券兑付不同域；jiuxin fund 词族是科研资助证据语义非券流水。需求侧 bid-reference 全文 0 命中（对账 5 否之一）→ 完全不支持。",
            "需求定位披露：本件是 01 清单 550 行中 5 个需求未覆盖位之一（阶段一·五人工核实结论），UI 挂载为政策卡步骤条目（mockData.js:709「券额抵扣」流程步骤）非数值统计位——若按非数值位口径本件可不立项，按清单既定行号仍交付负结论留证。",
            "深圳市科技创新券为真实政策（每年最高申领 50 万元，政策原文在 mock P08 卡引用），数据源在市科创委创新券服务平台（外部系统），三源无镜像。",
            "修复路径：对接深圳市科技创新券服务平台兑付数据（或科创委公开年报口径）→ 完全转换支持。",
        ],
        "base_years_used": [],
        "base_years_missing": ["2021", "2022", "2023", "2024", "2025", "2026"],
        "base_years_note": "创新券兑付为年度财政周期（mock milestones：申领 1 月/用券截止 11-30/兑付截止 12-31）；三源无任何年份兑付数据。若接入券平台流水可建年度序列。",
        "ctx_refs": {
            "note": "正文引用型数字登记",
            "refs": sorted(["50", "5", "542", "280", "218", "14", "2026", "709", "P08"]),
        },
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written:", OUT)
    print("judgment: 完全不支持 | voucher hits dev/gkx/jiuxin:",
          dev["dev_voucher_family_table_hits"], gkx["gkx_voucher_family"], jx["jiuxin_voucher_family"])


if __name__ == "__main__":
    main()
