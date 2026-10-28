#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_BUSINESS_POWER_SCORE 商业力得分 —— 20261027 三系统兼容版（D2 配置型·单接口）

【适用系统】科技专题服务算法库 + 科技专题系统（E-23 页面挂专题侧；展示系统消费同段出参）
【维护者】唐绍祖
【兼容设计】见 ../第三方库指标计算过程/M_ENT_BUSINESS_POWER_SCORE.md「一・三、三系统需求兼容性设计」
          与 ../过程文件/04_兼容接口设计规约.md
【判定】D2 口径级分歧·可兼容·配置型：算法库六维 vs 专题/展示自定义维度子集，
        同一「维度加权引擎」以 dims/weights 参数吸收，无需拆分 _ZT/_ZS。

三系统调用注意（后端必读）
--------------------------
1. **当前是探针模式**：3/6 维依赖 dwd_org_industry_chain_dtl（两侧库均不存在）、
   4 个字段待建 → compute() 返回支持度诊断，**不是业务分数**，切勿落库当评分。
2. 算法库同事：数据补齐 + Q014 权重落定后，`compute({"weights": {...}})` 即正式出分；
   在此之前传 weights 只作引擎试算（assumptions 声明等权占位）。
3. 专题系统同事：`compute({"dims": ["市场", "品牌", "技术合作", "产业链覆盖率"]})` 出四维雷达；
   传未实现维度名不会 500，会进 assumptions 警告并忽略。
4. 展示系统同事：与专题同段出参（score_radar / ranking）；E-23 无独立卡片。
5. 本接口签名在数据补齐后不变——这是配置型 D2 不拆分的收益。

王惠口径（calc-logic/ENT/M_ENT_BUSINESS_POWER_SCORE.md，与基线一致未改动）：
  六维（市场/产品/品牌/技术合作/产业链覆盖率/关键环节参与度）极值归一 0-100 加权，权重 Q014 待定。
  12 个三级指标中 4 个「现库无字段待建」，1 个关键源表 dwd_org_industry_chain_dtl 两侧均不存在。
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

APPLICABLE = ["科技专题服务算法库", "科技专题系统"]

ALL_DIMS = ["市场", "产品", "品牌", "技术合作", "产业链覆盖率", "关键环节参与度"]

# 缺省参数（md「入参兼容策略」表与此一一对应）
DEFAULTS = {
    "dims": None,          # 维度子集；None → 六维全开（算法库姿势）；专题/展示传子集
    "weights": None,       # 维度权重 dict；None → 等权占位（Q014 未定，assumptions 声明）
    "org_scope": None,     # 企业清单/行业过滤；None → 全量探测（当前探针模式）
    "normalize": "minmax", # 归一化方法；缺省 minmax 与 calc-logic 极值归一一致
}


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


def compute(params: dict | None = None) -> dict:
    """三系统统一入口（维度加权引擎·探针模式）。

    返回结构（供三个系统消费，段划分见模块 docstring 与 md「出参兼容策略」）：
      probe / dimension_detail : 算法库侧消费（分维度报告与结构探针）
      display                  : 专题/展示侧消费（雷达与排名的引擎结构位）
      assumptions              : 本次运行的缺省假设与警告（必读）
      support_judgment         : 可出分性判定（当前=部分支持）
    """
    p_in = dict(params or {})
    p = {**DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions: list[str] = []

    dims = list(p["dims"]) if p["dims"] else list(ALL_DIMS)
    unknown = [d for d in dims if d not in ALL_DIMS]
    if unknown:
        assumptions.append(f"传入未实现维度 {unknown}，已忽略（可选维度集={ALL_DIMS}）")
        dims = [d for d in dims if d in ALL_DIMS]
    if not dims:
        dims = list(ALL_DIMS)
    if p["weights"]:
        assumptions.append("weights 为引擎试算：Q014 甲方权重未落定，结果不可当正式值发布")
    else:
        assumptions.append("weights 缺省 → 等权占位（Q014 未定）")
    if p["org_scope"]:
        assumptions.append("org_scope 已接收：当前探针模式不区分企业子集（全量结构探测）")
    assumptions.append("3/6 维数据断链（dwd_org_industry_chain_dtl 无表 + 4 待建字段），当前不可出总分")

    report = {"metric_id": "M_ENT_BUSINESS_POWER_SCORE", "metric_name": "商业力得分",
              "script": Path(__file__).name, "data_source": "gkx",
              "applicable_systems": APPLICABLE,
              "params_effective": {"dims": dims, "weights": p["weights"],
                                   "org_scope": p["org_scope"], "normalize": p["normalize"]},
              "assumptions": assumptions}
    inv = inv_rows()
    p2 = {}
    p2["chain_dtl_gkx"] = "TABLE" if gkx_exists("dwd_org_industry_chain_dtl") else "NO_TABLE"
    p2["chain_info_gkx"] = inv["dwd_industry_chain_info"]
    p2["fin_rows"] = inv["dwd_org_annual_financial_info"]
    p2["fin_rev_profit_filled"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_annual_financial_info "
        "WHERE operating_revenue>0 AND pure_profit IS NOT NULL")["n"])
    p2["tech_tag_filled"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_tech_tag WHERE org_tag IS NOT NULL AND org_tag<>''")["n"])
    p2["news_rows"] = inv["dwd_org_important_news_info"]
    p2["main_prod_filled"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_org_product_info WHERE main_prod IS NOT NULL AND main_prod<>''")["n"])
    p2["patent_rows"] = inv["dwd_patent"]
    p2["base_industry_l1"] = int(q1(
        "SELECT COUNT(*) n FROM gkx.dwd_org_base_info WHERE industry_l1_code IS NOT NULL AND industry_l1_code<>''")["n"])
    report["probe"] = p2

    # 六维明细与探针（口径与 20261021 基线逐字一致；dims 开关只决定哪些维参与未来加权）
    full_dims = {
        "市场": {
            "营业收入": f"fin 填充 {p2['fin_rev_profit_filled']}/{p2['fin_rows']:,}（营收+净利非空）——低覆盖但非零",
            "市场占有率": f"行业归属可用（base L1 填充 {p2['base_industry_l1']}），行业总营收需聚合",
            "盈利能力": "同营业收入口径",
            "verdict": f"部分（覆盖率 {round(100.0 * p2['fin_rev_profit_filled'] / p2['fin_rows'], 2)}%）",
        },
        "产品": {
            "产品线覆盖广度": f"dwd_org_industry_chain_dtl 两侧均无表（gkx={p2['chain_dtl_gkx']}）；main_prod 辅助 {p2['main_prod_filled']}",
            "新产品收入占比": "现库无新产品销售收入字段（王惠标注待建）",
            "产品质量水平": "现库无质量字段（待建）",
            "verdict": "缺（关键表无+2 待建字段）",
        },
        "品牌": {
            "品牌声量": f"资讯表 {p2['news_rows']:,} 行可用（内容量口径可算）",
            "行业声誉": f"tech_tag 填充 {p2['tech_tag_filled']:,}（王惠标注「是否含品牌荣誉待定」）",
            "verdict": "部分（声量可算；荣誉 tag 语义待核）",
        },
        "技术合作": {
            "产学研合作专利": f"patent {p2['patent_rows']:,} 行，applicants 联合申请可解析",
            "外部专家人月": "现库无字段（待建）",
            "verdict": "部分",
        },
        "产业链覆盖率": {
            "环节覆盖率": f"chain_dtl 无表 + chain_info gkx {p2['chain_info_gkx']:,} 行（链定义在）",
            "verdict": "缺（企业×节点关联无表）",
        },
        "关键环节参与度": {
            "关键环节覆盖": "同上，且 node_stage/chain_score 字段依赖 chain_dtl",
            "verdict": "缺",
        },
    }
    report["dimension_detail"] = {d: full_dims[d] for d in dims}   # 只回所请求维度
    report["engine"] = {                            # 维度加权引擎结构位（数据到位后即出分）
        "normalize": p["normalize"],
        "weights_effective": p["weights"] or {d: round(1.0 / len(dims), 4) for d in dims},
        "dims_active": dims,
        "dims_blocked": [d for d in dims if full_dims[d]["verdict"].startswith("缺")],
        "ready": False,
        "blockers": ["Q014 权重未落定", "dwd_org_industry_chain_dtl 无表",
                     "4 个三级指标字段待建（新产品收入占比/产品质量/外部专家人月/行业荣誉tag语义）"],
    }
    report["support_judgment"] = {
        "data_support_level": "部分支持",
        "reason": (
            f"六维中：市场维财务填充率低（{p2['fin_rev_profit_filled']}/{p2['fin_rows']:,}，"
            f"{round(100.0 * p2['fin_rev_profit_filled'] / p2['fin_rows'], 2)}%）；产品/产业链覆盖/关键环节三维依赖的 "
            f"dwd_org_industry_chain_dtl 在 gkx（及 live）均不存在（gkx industry_chain_info={p2['chain_info_gkx']:,} 仅链定义，无企业×节点关联）；"
            f"品牌维资讯 {p2['news_rows']:,} 行可算声量、tech_tag {p2['tech_tag_filled']:,} 待核荣誉语义；"
            f"技术合作维专利 {p2['patent_rows']:,} 行可解析联合申请、外部专家人月无字段。"
            "4 个待建字段 + 1 张关键表缺失 → 始终有依赖维不闭合 → 部分支持。"
        ),
        "criteria": {
            "chain_dtl_exists_gkx": p2["chain_dtl_gkx"] != "NO_TABLE",
            "pending_fields_wanghui": ["新产品销售收入", "产品质量", "外部专家人月数", "行业荣誉tag语义"],
            "weights_closed": False,
        },
    }
    report["display"] = {              # 专题/展示侧（E-23）消费段：引擎结构位，当前无数值
        "score_radar": {"dims": dims, "values": None,
                        "note": "数据到位后此处返回 0-100 分（minmax 归一 + weights 加权）"},
        "ranking": {"note": "同上；当前探针模式不产出企业排名"},
    }
    return report


def main():
    # 缺省运行 = 算法库姿势（六维全开 + 等权占位）；探针结果与 20261021 基线一致
    report = compute()
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["support_judgment"], ensure_ascii=False, indent=2), flush=True)
    print("wrote", OUT, flush=True)


if __name__ == "__main__":
    main()
