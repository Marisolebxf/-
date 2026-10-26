#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_BUSINESS_POWER_SCORE 商业力得分 — 六维依赖侧实测脚本（20261021 改源版）

王惠口径（calc-logic/ENT/M_ENT_BUSINESS_POWER_SCORE.md）：
  六维（市场/产品/品牌/技术合作/产业链覆盖率/关键环节参与度）极值归一 0-100 加权，权重 Q014 待定。
  12 个三级指标中 4 个「现库无字段待建」（新产品收入占比、产品质量、外部专家人月、行业声誉 tag 待定），
  1 个关键源表 dwd_org_industry_chain_dtl 两侧均不存在。
本脚本逐维探结构+填充，输出 support_judgment。
主算：三方库 gkx（全表名 gkx.<表名>）；行数只读 _work_gkx21/GKX_INVENTORY.json。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
ROOT = CODE_DIR.parent
sys.path.insert(0, str(CODE_DIR))

from _gkxdb import gkx, gkx_exists  # noqa: E402

OUT = Path(__file__).with_name("M_ENT_BUSINESS_POWER_SCORE_out.json")
INVENTORY = ROOT / "_work_gkx21" / "GKX_INVENTORY.json"


def inv_rows() -> dict:
    d = json.loads(INVENTORY.read_text(encoding="utf-8"))
    return {k: int(v["rows"]) for k, v in d.items()}


def q(sql: str, args=None):
    cur = gkx()
    try:
        cur.execute(sql, args)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def q1(sql: str, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def main():
    report = {"metric_id": "M_ENT_BUSINESS_POWER_SCORE", "metric_name": "商业力得分",
              "script": Path(__file__).name, "data_source": "gkx"}
    inv = inv_rows()
    p = {}
    p["chain_dtl_gkx"] = "TABLE" if gkx_exists("dwd_org_industry_chain_dtl") else "NO_TABLE"
    p["chain_info_gkx"] = inv["dwd_industry_chain_info"]
    p["fin_rows"] = inv["dwd_org_annual_financial_info"]
    p["fin_rev_profit_filled"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_annual_financial_info "
        "WHERE operating_revenue>0 AND pure_profit IS NOT NULL")["n"])
    p["tech_tag_filled"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_tech_tag WHERE org_tag IS NOT NULL AND org_tag<>''")["n"])
    p["news_rows"] = inv["dwd_org_important_news_info"]
    p["main_prod_filled"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_org_product_info WHERE main_prod IS NOT NULL AND main_prod<>''")["n"])
    p["patent_rows"] = inv["dwd_patent"]
    p["base_industry_l1"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE industry_l1_code IS NOT NULL AND industry_l1_code<>''")["n"])
    report["probe"] = p

    dims = {
        "市场": {
            "营业收入": f"fin 填充 {p['fin_rev_profit_filled']}/{p['fin_rows']:,}（营收+净利非空）——低覆盖但非零",
            "市场占有率": f"行业归属可用（base L1 填充 {p['base_industry_l1']}），行业总营收需聚合",
            "盈利能力": "同营业收入口径",
            "verdict": f"部分（覆盖率 {round(100.0 * p['fin_rev_profit_filled'] / p['fin_rows'], 2)}%）",
        },
        "产品": {
            "产品线覆盖广度": f"dwd_org_industry_chain_dtl 两侧均无表（gkx={p['chain_dtl_gkx']}）；main_prod 辅助 {p['main_prod_filled']}",
            "新产品收入占比": "现库无新产品销售收入字段（王惠标注待建）",
            "产品质量水平": "现库无质量字段（待建）",
            "verdict": "缺（关键表无+2 待建字段）",
        },
        "品牌": {
            "品牌声量": f"资讯表 {p['news_rows']:,} 行可用（内容量口径可算）",
            "行业声誉": f"tech_tag 填充 {p['tech_tag_filled']:,}（王惠标注「是否含品牌荣誉待定」）",
            "verdict": "部分（声量可算；荣誉 tag 语义待核）",
        },
        "技术合作": {
            "产学研合作专利": f"patent {p['patent_rows']:,} 行，applicants 联合申请可解析",
            "外部专家人月": "现库无字段（待建）",
            "verdict": "部分",
        },
        "产业链覆盖率": {
            "环节覆盖率": f"chain_dtl 无表 + chain_info gkx {p['chain_info_gkx']:,} 行（链定义在）",
            "verdict": "缺（企业×节点关联无表）",
        },
        "关键环节参与度": {
            "关键环节覆盖": "同上，且 node_stage/chain_score 字段依赖 chain_dtl",
            "verdict": "缺",
        },
    }
    report["dimension_detail"] = dims
    report["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"六维中：市场维财务填充率低（{p['fin_rev_profit_filled']}/{p['fin_rows']:,}，"
            f"{round(100.0 * p['fin_rev_profit_filled'] / p['fin_rows'], 2)}%）；产品/产业链覆盖/关键环节三维依赖的 "
            f"dwd_org_industry_chain_dtl 在 gkx（及 live）均不存在（gkx industry_chain_info={p['chain_info_gkx']:,} 仅链定义，无企业×节点关联）；"
            f"品牌维资讯 {p['news_rows']:,} 行可算声量、tech_tag {p['tech_tag_filled']:,} 待核荣誉语义；"
            f"技术合作维专利 {p['patent_rows']:,} 行可解析联合申请、外部专家人月无字段。"
            "4 个待建字段 + 1 张关键表缺失 → 始终有依赖维不闭合 → 部分支持。"
        ),
        "criteria": {
            "chain_dtl_exists_gkx": p["chain_dtl_gkx"] != "NO_TABLE",
            "pending_fields_wanghui": ["新产品销售收入", "产品质量", "外部专家人月数", "行业荣誉tag语义"],
            "weights_closed": False,
        },
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
