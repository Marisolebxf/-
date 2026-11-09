#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""GDF-FIN-WORKPACK-v1 生成 / 自检脚本（本侧维护用；GDF 不需要运行）。

单一真源 = 本文件里的 TARGETS（Mapping 规格）+ 20261109 行数报告「金融要素库」节。
  python gen_fin_pack.py --check   只自检（不写文件）：31 张表齐、规格引用的源列都在报告里、parse_wan 断言
  python gen_fin_pack.py           自检通过后重写：02 yaml、09a 源表列清单、09 §3 矩阵（标记段）、10/fin-dwd-draft.md

ponytail: 列清单取自 Excel 抽取的报告，不连 live。live 结构以 GDF 开工前 SHOW CREATE TABLE 为准（00 §0.3）。
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.dirname(HERE)
REPORT = os.path.normpath(os.path.join(
    PACK, "..", "..", "..", "..", "third-party-source", "gkx-mysql-raw", "加工",
    "GKX数据源表及行数报告-20261109-1026.MD"))

TECH = {"t_id", "dwd_id", "created_time", "updated_time", "creater", "updater",
        "table_data_source", "operator_remarks", "is_deleted", "insert_remark"}

# ---- 31 张物理表分类：phase / mapping / owner --------------------------------
# P0/P1 = 本包 v1 洗入项目 DWD；P2 = v1 只贴不洗；ZERO = 0 行只贴；ENT = 贴源与洗数归 ENT-v4
CLASS = {
    "dwd_corp_basic_info": "P0", "dwd_sec_basic_info": "P0",
    "dwd_industrial_fund_basic_info": "P0", "dwd_industrial_fund_management_institution": "P0",
    "dwd_industrial_fund_lp_info": "P0", "dwd_industrial_fund_investment_strategy": "P0",
    "dwd_industrial_fund_investment_project_info": "P0",
    "dwd_sci_tech_inno_bonds": "P0", "dwd_high_tech_industry_bonds": "P0",
    "dwd_corp_his_sw_ic": "P1", "dwd_corp_his_crsc_ic": "P1", "dwd_corp_his_citic_ic": "P1",
    "dwd_hk_corp_his_sw_ic": "P1",
    "dwd_main_business_composition_industry": "P1", "dwd_main_business_composition_prod": "P1",
    "dwd_main_business_composition_area": "P1",
    "dwd_astock_val_indicators": "P1", "dwd_hk_stock_val_indicators": "P1", "dwd_us_stock_val_ind": "P1",
    "dwd_ls_stock_daily_quotation": "P2", "dwd_hk_sec_daily_quotation": "P2",
    "dwd_us_sec_daily_quotation": "P2", "dwd_option_daily_quotation": "P2",
    "dwd_option_basic_info": "P2", "dwd_foreign_exchange_info": "P2",
    "dwd_fund_basic_info": "ZERO", "dwd_fund_equity_sector_allocation": "ZERO",
    "dwd_fund_bond_allocation": "ZERO",
    "dwd_org_financing_info": "ENT", "dwd_org_invest_info": "ENT",
    "dwd_org_merger_acquisition_info": "ENT",
}

# ---- Mapping 规格 -------------------------------------------------------------
# C(目标列, MySQL 类型, 注释, 映射)；映射：str=所有源表同名列；dict={源表: 表达式}
# 表达式：源列名 | None(该源无此列→NULL) | "'字面量'" | "FN:parse_wan(列)"
def C(col, typ, cmt, m=None):
    return (col, typ, cmt, col if m is None else m)


T_CORP = "dwd_corp_basic_info"
T_SEC = "dwd_sec_basic_info"
T_FB = "dwd_industrial_fund_basic_info"
T_SCI = "dwd_sci_tech_inno_bonds"
T_HT = "dwd_high_tech_industry_bonds"
T_SW, T_CRSC, T_CITIC, T_HKSW = ("dwd_corp_his_sw_ic", "dwd_corp_his_crsc_ic",
                                 "dwd_corp_his_citic_ic", "dwd_hk_corp_his_sw_ic")
T_MI, T_MP, T_MA = ("dwd_main_business_composition_industry",
                    "dwd_main_business_composition_prod", "dwd_main_business_composition_area")
T_VA, T_VH, T_VU = "dwd_astock_val_indicators", "dwd_hk_stock_val_indicators", "dwd_us_stock_val_ind"

TARGETS = [
    dict(name="fin_corp_basic", phase="P0", cn="上市公司基本资料（沪深港美）", idx=["org_id"], cols=[
        C("org_id", "varchar(255) NOT NULL", "机构ID（供应方 org_id，原样；与 enterprise_base.org_id 对照见 09 §4）"),
        C("org_name_cn", "varchar(500) NULL", "机构名称（中文）"),
        C("org_name_en", "varchar(500) NULL", "机构名称（英文）"),
        C("reg_region", "varchar(255) NULL", "注册国家或地区"),
        C("established_date", "date NULL", "成立日期"),
        C("business_reg_num", "varchar(255) NULL", "工商登记号"),
    ], src=[T_CORP]),
    dict(name="fin_security", phase="P0", cn="证券基本资料", idx=["sec_id", "sec_code", "org_id"], cols=[
        C("sec_id", "varchar(255) NOT NULL", "证券ID（供应方 sec_id）"),
        C("sec_code", "varchar(255) NULL", "证券代码"),
        C("sec_full_name", "varchar(500) NULL", "证券全称"),
        C("sec_full_name_en", "varchar(500) NULL", "证券英文全称"),
        C("sec_type", "varchar(255) NULL", "证券类别"),
        C("td_mkt", "varchar(255) NULL", "交易市场"),
        C("td_currency_name", "varchar(255) NULL", "交易货币名称"),
        C("listed_board_name", "varchar(255) NULL", "上市板名称"),
        C("listed_status", "varchar(255) NULL", "上市状态"),
        C("is_listing", "smallint NULL", "是否上市 0否1是"),
        C("is_delisted", "smallint NULL", "是否摘牌 0否1是"),
        C("listed_date", "date NULL", "上市日期"),
        C("stop_listing_date", "date NULL", "终止上市日期"),
        C("org_id", "varchar(255) NULL", "机构ID"),
        C("sec_issuer_id", "varchar(255) NULL", "证券发行主体ID（基金/指数/期货用）"),
        C("issue_org_id", "varchar(255) NULL", "发行机构ID"),
        C("bond_code", "varchar(255) NULL", "债券关联代码（关联 fin_bond.bond_code）"),
        C("issuer_name", "varchar(255) NULL", "公司名称", {T_SEC: "name_cn"}),
        C("credit_code", "varchar(255) NULL", "统一社会信用代码", {T_SEC: "external_id"}),
    ], src=[T_SEC]),
    dict(name="fin_industrial_fund", phase="P0", cn="产业基金基本信息", idx=["industrial_fund_id"], cols=[
        C("industrial_fund_id", "varchar(255) NOT NULL", "产业基金ID"),
        C("fund_short_name", "varchar(255) NULL", "基金简称", {T_FB: "industrial_fund_short_name"}),
        C("fund_name", "varchar(255) NULL", "基金名称", {T_FB: "industrial_fund_name"}),
        C("reg_region", "varchar(255) NULL", "注册地区（原样，形如 天津市-西青区）"),
        C("est_date", "date NULL", "成立日期"),
        C("fund_type", "varchar(255) NULL", "基金类型", {T_FB: "industrial_fund_type"}),
        C("currency_ctgry", "varchar(255) NULL", "投资币种"),
        C("capital_source", "varchar(255) NULL", "资本来源"),
        C("fund_year", "int NULL", "基金存续年限", {T_FB: "industrial_fund_year"}),
        C("state_owned", "varchar(255) NULL", "国资背景"),
        C("reg_status", "varchar(255) NULL", "设立状态"),
        C("proposed_reg_date", "date NULL", "拟设立时间"),
        C("reg_address", "text NULL", "注册地址"),
        C("reg_capital_raw", "varchar(255) NULL", "注册资本原文（含单位）", {T_FB: "reg_capital"}),
        C("reg_capital_wan", "decimal(20,4) NULL", "注册资本（万元人民币）：仅 元/万元/亿元 可解析；含外币或解析失败为 NULL，不写 0、不换汇",
          {T_FB: "FN:parse_wan(reg_capital)"}),
        C("real_capital_raw", "varchar(255) NULL", "实缴资本原文", {T_FB: "real_capital"}),
        C("credit_code", "varchar(255) NULL", "统一社会信用代码", {T_FB: "external_id"}),
        C("est_status", "varchar(255) NULL", "经营状态"),
    ], src=[T_FB]),
    dict(name="fin_industrial_fund_gp", phase="P0", cn="产业基金管理机构（GP）", idx=["industrial_fund_id", "gp_org_id"], cols=[
        C("industrial_fund_id", "varchar(255) NOT NULL", "产业基金ID"),
        C("gp_org_id", "varchar(255) NOT NULL", "GP机构ID"),
        C("gp_org_name", "varchar(255) NULL", "GP名称全称"),
        C("brand_institution_name", "varchar(255) NULL", "归属品牌机构名称（简称）"),
        C("brand_institution_tag", "varchar(255) NULL", "归属品牌机构标签"),
        C("brand_institution_region", "varchar(255) NULL", "归属品牌机构总部地区"),
        C("brand_institution_type", "varchar(255) NULL", "归属品牌机构类型"),
    ], src=["dwd_industrial_fund_management_institution"]),
    dict(name="fin_industrial_fund_lp", phase="P0", cn="产业基金LP信息", idx=["industrial_fund_id", "lp_org_id"], cols=[
        C("industrial_fund_id", "varchar(255) NOT NULL", "产业基金ID"),
        C("lp_org_id", "varchar(255) NOT NULL", "LP机构ID"),
        C("lp_org_name", "varchar(255) NULL", "LP机构全称"),
        C("lp_org_type", "text NULL", "LP类型"),
        C("lp_state_owned", "varchar(255) NULL", "LP是否国资背景"),
        C("state_lp_sub_ratio", "decimal(20,2) NULL", "国资LP认缴比例（源列 solp_rub_ratio）", {"dwd_industrial_fund_lp_info": "solp_rub_ratio"}),
        C("lp_region_name", "varchar(255) NULL", "LP所在地区"),
        C("lp_first_inv_date", "date NULL", "LP首次出资时间"),
        C("sub_capital", "decimal(20,2) NULL", "LP认缴金额（单位待供应方确认 OPEN-FIN-03，原样）"),
        C("lp_inv_ratio", "decimal(20,2) NULL", "LP出资比例"),
        C("lp_real_capital", "decimal(20,2) NULL", "LP实缴金额（单位同上）"),
        C("lp_brand_institution", "varchar(255) NULL", "LP归属品牌"),
        C("is_lp_exited", "varchar(255) NULL", "LP是否退出"),
    ], src=["dwd_industrial_fund_lp_info"]),
    dict(name="fin_industrial_fund_strategy", phase="P0", cn="产业基金投资策略", idx=["industrial_fund_id"], cols=[
        C("industrial_fund_id", "varchar(255) NOT NULL", "产业基金ID"),
        C("inv_field", "text NULL", "投资领域（多值，源内以换行分隔，原样不拆）"),
        C("inv_round", "varchar(255) NULL", "投资轮次"),
        C("inv_industry", "varchar(255) NULL", "投资行业"),
        C("strategy_desc", "text NULL", "策略描述"),
    ], src=["dwd_industrial_fund_investment_strategy"]),
    dict(name="fin_industrial_fund_inv_summary", phase="P0", cn="产业基金投资汇总（基金级，非项目级）", idx=["industrial_fund_id"], cols=[
        C("industrial_fund_id", "varchar(255) NOT NULL", "产业基金ID"),
        C("latest_inv_date", "date NULL", "最新投资时间"),
        C("inv_event_count", "int NULL", "投资事件数量"),
        C("total_inv_companies_count", "int NULL", "投资企业总数"),
        C("cum_inv_amount", "decimal(20,2) NULL", "累计投资金额（单位待确认 OPEN-FIN-03，原样）"),
        C("listed_companies_count", "int NULL", "投后企业上市数量"),
    ], src=["dwd_industrial_fund_investment_project_info"]),
    dict(name="fin_bond", phase="P0", cn="科创债 / 高新技术产业债", idx=["bond_code", "issuer"], cols=[
        C("bond_class", "varchar(32) NOT NULL", "债券类别：SCI_TECH_INNO / HIGH_TECH_INDUSTRY",
          {T_SCI: "'SCI_TECH_INNO'", T_HT: "'HIGH_TECH_INDUSTRY'"}),
        C("bond_code", "varchar(255) NOT NULL", "债券代码"),
        C("bond_name", "varchar(255) NULL", "债券名称"),
        C("issue_amount_yi", "decimal(20,4) NULL", "发行总额（亿）；源为 -- 的不写 0", {T_SCI: "issue_amount", T_HT: "issue_amount"}),
        C("issue_term_years", "decimal(20,4) NULL", "发行期限（年）；仅高新债有", {T_SCI: None, T_HT: "issue_term_years"}),
        C("issue_price", "decimal(20,4) NULL", "发行价格；仅高新债有", {T_SCI: None, T_HT: "issue_price"}),
        C("current_coupon_rate", "decimal(20,4) NULL", "当期票面利率（%）"),
        C("interest_rate_type", "varchar(255) NULL", "利率类型；仅高新债有", {T_SCI: None, T_HT: "interest_rate_type"}),
        C("payment_frequency", "varchar(255) NULL", "付息频率"),
        C("issue_date", "date NULL", "发行日期"),
        C("maturity_date", "date NULL", "到期日期"),
        C("latest_bond_rating", "varchar(255) NULL", "最新债项评级"),
        C("latest_issuer_rating", "varchar(255) NULL", "最新主体信用评级"),
        C("issue_issuer_rating", "varchar(255) NULL", "发行时主体评级"),
        C("gics_l1", "varchar(255) NULL", "GICS一级行业", {T_SCI: "gics_sector", T_HT: "gics_c_name"}),
        C("gics_l2", "varchar(255) NULL", "GICS二级行业", {T_SCI: "gics_industry_group", T_HT: "gics_l_name"}),
        C("gics_l3", "varchar(255) NULL", "GICS三级行业", {T_SCI: "gics_industry", T_HT: "gics_m_name"}),
        C("gics_l4", "varchar(255) NULL", "GICS四级行业", {T_SCI: "gics_sub_industry", T_HT: "gics_s_name"}),
        C("issuer", "varchar(255) NULL", "发行人"),
        C("issuer_type", "varchar(255) NULL", "发行人类型"),
        C("trading_market", "varchar(255) NULL", "交易市场"),
    ], src=[T_SCI, T_HT]),
    dict(name="fin_industry_class_his", phase="P1", cn="上市公司行业分类全量（申万/证监会/中信/港股申万）", idx=["org_id", "class_system"], cols=[
        C("class_system", "varchar(16) NOT NULL", "分类体系：SW_CN / CRSC_CN / CITIC_CN / SW_HK",
          {T_SW: "'SW_CN'", T_CRSC: "'CRSC_CN'", T_CITIC: "'CITIC_CN'", T_HKSW: "'SW_HK'"}),
        C("org_id", "varchar(255) NOT NULL", "机构ID"),
        C("org_name", "varchar(255) NULL", "公司名称", {t: "name_cn" for t in (T_SW, T_CRSC, T_CITIC, T_HKSW)}),
        C("credit_code", "varchar(255) NULL", "统一社会信用代码", {t: "external_id" for t in (T_SW, T_CRSC, T_CITIC, T_HKSW)}),
        C("industry_type", "varchar(255) NULL", "行业类别"),
        C("industry_level", "int NULL", "行业级别"),
        C("inclusion_date", "date NULL", "纳入日期"),
        C("eliminate_date", "date NULL", "剔除日期"),
        C("industry_code", "varchar(255) NULL", "行业代码"),
        C("industry_name", "varchar(255) NULL", "行业名称"),
        C("is_latest", "smallint NULL", "最新标志 1最新；港股申万源无此列→NULL，ADS 以 eliminate_date IS NULL 判最新",
          {T_SW: "lastest_symbol", T_CRSC: "lastest_symbol", T_CITIC: "lastest_symbol", T_HKSW: None}),
    ], src=[T_SW, T_CRSC, T_CITIC, T_HKSW]),
    dict(name="fin_main_biz_composition", phase="P1", cn="沪深上市企业主营业务构成（行业/产品/地区）", idx=["org_id", "dim_type", "occur_period"], cols=[
        C("dim_type", "varchar(16) NOT NULL", "构成维度：INDUSTRY / PRODUCT / AREA",
          {T_MI: "'INDUSTRY'", T_MP: "'PRODUCT'", T_MA: "'AREA'"}),
        C("dim_name", "varchar(255) NOT NULL", "维度名称（行业名/产品名/地区名）",
          {T_MI: "industry_name", T_MP: "prod_name", T_MA: "area_name"}),
        C("org_id", "varchar(255) NOT NULL", "机构ID"),
        C("credit_code", "varchar(255) NULL", "统一社会信用代码", {t: "external_id" for t in (T_MI, T_MP, T_MA)}),
        C("stock_code", "varchar(255) NULL", "股票代码"),
        C("stock_name", "varchar(255) NULL", "代码简称", {t: "stock_noun" for t in (T_MI, T_MP, T_MA)}),
        C("occur_period", "varchar(255) NOT NULL", "报告期（源样例 202603，原样字符串；OPEN-FIN-04）"),
        C("core_biz_income", "decimal(20,4) NULL", "主营业务收入（万元）"),
        C("core_biz_income_prop", "decimal(20,4) NULL", "主营业务收入占比（%）"),
        C("core_biz_income_gr", "decimal(20,4) NULL", "主营业务收入增长率（%）"),
        C("core_biz_cost", "decimal(20,4) NULL", "主营业务成本（万元）"),
        C("core_biz_cost_prop", "decimal(20,4) NULL", "主营业务成本占比（%）"),
        C("core_biz_cost_gr", "decimal(20,4) NULL", "主营业务成本增长率（%）"),
        C("core_biz_profit", "decimal(20,4) NULL", "主营业务利润（万元）"),
        C("core_biz_profit_prop", "decimal(20,4) NULL", "主营业务利润占比（%）"),
        C("gross_margin", "decimal(20,4) NULL", "毛利率（%）"),
        C("gross_margin_change", "decimal(20,4) NULL", "毛利率变动"),
        C("csrc_industry", "varchar(255) NULL", "行业_证监会（新）"),
        C("shenwan_industry", "varchar(255) NULL", "行业_申万"),
    ], src=[T_MI, T_MP, T_MA]),
    dict(name="fin_valuation_daily", phase="P1", cn="股票估值指标日表（A股/港股/美股）", idx=["sec_id", "dt", "market"], cols=[
        C("market", "varchar(8) NOT NULL", "市场：CN / HK / US", {T_VA: "'CN'", T_VH: "'HK'", T_VU: "'US'"}),
        C("sec_id", "varchar(255) NOT NULL", "证券ID（关联 fin_security.sec_id）"),
        C("dt", "date NOT NULL", "日期"),
        C("pe_ttm_ed", "decimal(20,4) NULL", "市盈率 PE(TTM)"),
        C("pb_mrq", "decimal(20,4) NULL", "市净率 PB(MRQ)"),
        C("pcf_ttm_ed", "decimal(20,4) NULL", "市现率 PCF(经营现金流TTM)"),
        C("ps_ttm_ed", "decimal(20,4) NULL", "市销率 PS(TTM)"),
        C("tmv_rmb", "decimal(20,4) NULL", "总市值（人民币）"),
        C("cir_tmv", "decimal(20,4) NULL", "流通市值；仅 A 股有", {T_VA: "cir_tmv", T_VH: None, T_VU: None}),
        C("tmv_hkd", "decimal(20,4) NULL", "总市值（港币）；A 股无", {T_VA: None, T_VH: "tmv_hkd", T_VU: "tmv_hkd"}),
        C("tmv_usd", "decimal(20,4) NULL", "总市值（美元）；A 股无", {T_VA: None, T_VH: "tmv_usd", T_VU: "tmv_usd"}),
        C("org_id", "varchar(255) NULL", "机构ID；仅港股源有", {T_VA: None, T_VH: "org_id", T_VU: None}),
        C("org_name", "varchar(255) NULL", "公司名称；仅港股源有", {T_VA: None, T_VH: "name_cn", T_VU: None}),
    ], src=[T_VA, T_VH, T_VU]),
]


# ---- 可执行规则：注册资本解析（09 §3.3 / 12 §2.1 同口径）-----------------------
_WAN = re.compile(r"^\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(万元|亿元|元)(?:人民币)?\s*$")


def parse_wan(s):
    """'30000.00万元'→30000.0；'1.5亿元'→15000.0；'5000元'→0.5；含外币/解析失败→None（不写0、不换汇）。"""
    if s is None:
        return None
    m = _WAN.match(str(s))
    if not m:
        return None
    v = float(m.group(1).replace(",", ""))
    return {"万元": v, "亿元": v * 10000.0, "元": v / 10000.0}[m.group(2)]


def _self_check_rules():
    assert parse_wan("30000.00万元") == 30000.0
    assert parse_wan("1.5亿元") == 15000.0
    assert parse_wan("5000元") == 0.5
    assert parse_wan("1,200万元人民币") == 1200.0
    assert parse_wan("5000万美元") is None
    assert parse_wan("/") is None and parse_wan("") is None and parse_wan(None) is None


# ---- 解析行数报告 -------------------------------------------------------------
def parse_report():
    txt = io.open(REPORT, encoding="utf-8").read().splitlines()
    i0 = next(i for i, l in enumerate(txt) if l.strip() == "# 金融要素库")
    i1 = next(i for i in range(i0 + 1, len(txt)) if txt[i].startswith("# ") and txt[i].strip() != "# 金融要素库")
    tabs, sections, cur = {}, 0, None
    for l in txt[i0:i1]:
        m = re.match(r"^## (.+)\((dwd_[a-z0-9_]+)\)\s*$", l)
        if m:
            sections += 1
            cn, code = m.group(1), m.group(2)
            cur = tabs.setdefault(code, {"cn": cn, "rows": 0, "cols": {}, "sections": 0})
            cur["sections"] += 1
            continue
        if cur is None:
            continue
        m = re.match(r"^- \*\*数据行数\*\*：([\d,]+)", l)
        if m:
            cur["rows"] = int(m.group(1).replace(",", ""))
            continue
        if l.startswith("| ") and not l.startswith("| 序号") and not l.startswith("|:"):
            p = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(p) >= 12 and p[0].isdigit():
                cur["cols"].setdefault(p[2], dict(cn=p[1], typ=p[3], ln=p[4], nul=p[6], pk=p[8]))
    return tabs, sections


def check(tabs, sections):
    assert sections == 32, "报告金融节应有 32 个 section（含 dwd_corp_basic_info 重复一条），实际 %d" % sections
    assert len(tabs) == 31, "物理表应为 31，实际 %d" % len(tabs)
    assert set(tabs) == set(CLASS), "CLASS 与报告不一致：%s" % (set(tabs) ^ set(CLASS))
    wash = {t for t, c in CLASS.items() if c in ("P0", "P1")}
    used = set()
    for t in TARGETS:
        for s in t["src"]:
            used.add(s)
        for col, _typ, _cmt, m in t["cols"]:
            for s in t["src"]:
                e = m.get(s) if isinstance(m, dict) else m
                if isinstance(m, dict):
                    assert s in m, "%s.%s 缺源表 %s 的映射" % (t["name"], col, s)
                if e is None or e.startswith("'"):
                    continue
                name = re.match(r"FN:\w+\((\w+)\)", e).group(1) if e.startswith("FN:") else e
                assert name in tabs[s]["cols"], "%s.%s ← %s.%s 不在报告列清单中" % (t["name"], col, s, name)
                assert name not in TECH, "%s 引用了技术字段 %s" % (t["name"], name)
    assert used == wash, "P0/P1 表与 TARGETS 源表不一致：%s" % (used ^ wash)
    _self_check_rules()


# ---- 输出 ---------------------------------------------------------------------
def esc(s):
    return str(s).replace("|", "\\|")


def gen_yaml(tabs):
    pn = {"P0": "P0", "P1": "P1", "P2": "P2", "ZERO": "P2", "ENT": None}
    ent_note = {
        "dwd_org_financing_info": "ENT-v4 P0 wash → enterprise_financing；FIN 不重复配贴源作业，只读 ENT DWD",
        "dwd_org_invest_info": "ENT-v4 P0 wash → enterprise_invest；FIN 不重复配贴源作业，只读 ENT DWD",
        "dwd_org_merger_acquisition_info": "ENT-v4 P2 mirror_only（Q-WP3-21 只贴不洗）；FIN 沿用，不洗",
    }
    out = []
    out.append("# GDF-FIN Wave A 贴源表清单（金融要素库）")
    out.append("# 由 script/gen_fin_pack.py 从 20261109 行数报告生成；手改请同步改脚本 CLASS。")
    out.append("# 源：gkx.<表名> 只读 → 目标：gkxlumenx_ods.<同名>；结构以 live gkx 为准（00 §0.3）")
    out.append("# mapping: wash=按 09 洗入 gkxlumenx_dwd | mirror_only=本期只贴源不洗")
    out.append("# owner: FIN=本包配贴源作业 | ENT-v4=贴源与洗数归企业包（FIN 不重复建作业）")
    out.append("")
    out.append("version: GDF-FIN-WORKPACK-v1.0")
    out.append('updated: "2026-11-09"')
    out.append("source_authority: third-party-source/gkx-mysql-raw/加工/GKX数据源表及行数报告-20261109-1026.MD")
    out.append("mapping_authority: 09-金融域-ETL-Mapping明细-源表到DWD.md")
    out.append("source_db: gkx")
    out.append("target_db: gkxlumenx_ods")
    out.append("mirror_mode: isomorphic")
    out.append('default_filter: "is_deleted = 0"')
    out.append("priority_status: team_default")
    out.append("")
    out.append("exclude:")
    out.append('  - { pattern: "ods_*", reason: 供应方不暴露 }')
    out.append('  - { pattern: "*_bak_*", reason: "供应方备份副本（如 dwd_main_business_composition_*_bak_20260911），不贴不洗" }')
    out.append("")
    groups = [
        ("fin_master", "P0 主数据 / 产业基金 / 债券（v1 洗）", [t for t, c in CLASS.items() if c == "P0"]),
        ("fin_p1", "P1 行业分类 / 主营构成 / 估值（v1 洗）", [t for t, c in CLASS.items() if c == "P1"]),
        ("fin_p2", "P2 日行情 / 期权 / 外汇（v1 只贴不洗，v1.1 另议）", [t for t, c in CLASS.items() if c == "P2"]),
        ("fin_zero", "公募基金三表（live 0 行，只贴；供应方补数前不洗）", [t for t, c in CLASS.items() if c == "ZERO"]),
        ("fin_shared_ent", "与企业包重叠三表（贴源与洗数归 ENT-v4）", [t for t, c in CLASS.items() if c == "ENT"]),
    ]
    out.append("groups:")
    for gid, title, names in groups:
        out.append("  - id: %s" % gid)
        out.append("    title: %s" % title)
        out.append("    source_sheet: 金融要素库")
        out.append("    tables:")
        for t in names:
            c = CLASS[t]
            tb = tabs[t]
            if c in ("P0", "P1"):
                mp, owner, note = "wash", "FIN", "→ 见 09 §3；live 行数 {:,}（20261109）".format(tb["rows"])
            elif c == "ENT":
                mp = "wash" if t != "dwd_org_merger_acquisition_info" else "mirror_only"
                owner, note = "ENT-v4", ent_note[t] + "；live 行数 {:,}".format(tb["rows"])
            elif c == "ZERO":
                mp, owner, note = "mirror_only", "FIN", "live 0 行（20261109）；供应方补数前不洗，贴源后回报行数"
            else:
                mp, owner, note = "mirror_only", "FIN", "v1 只贴不洗；live 行数 {:,}{}".format(
                    tb["rows"], "（大表，贴源策略见 04 §3）" if tb["rows"] > 100000 else "")
            pr = pn[c] or ("P0" if t != "dwd_org_merger_acquisition_info" else "P2")
            out.append('      - { name: %s, priority: %s, cn: "%s", mapping: %s, owner: %s, rows_20261109: %d, note: "%s" }'
                       % (t, pr, tb["cn"], mp, owner, tb["rows"], note))
        out.append("")
    out.append("summary:")
    out.append("  physical_tables: 31   # 行数报告列 32 行，dwd_corp_basic_info 在报告里出现两次（同一物理表）")
    out.append("  fin_owned_wave_a: 28  # 本包配贴源作业；另 3 张归 ENT-v4")
    out.append("  wash_v1: 19           # P0 9 + P1 10；→ 目标 DWD 11 张（09 §2）")
    out.append("  mirror_only_v1: 9     # P2 6 + 公募基金 0 行 3")
    out.append("  shared_with_ent: 3")
    return "\n".join(out) + "\n"


def gen_09a(tabs):
    o = ["# 09a · 金融要素库 31 表 · 源表业务列清单（生成件）", "",
         "> 生成：`script/gen_fin_pack.py`，来源 20261109 行数报告「金融要素库」节（Excel 抽取）。**不是 live 结构**。",
         "> **live gkx 为准**：GDF 开工前对每张表 `SHOW CREATE TABLE` 核对；本清单与 live 不一致时以 live 为准，并在回签里登记。",
         "> 本清单已去掉 `t_id`（Excel 多出，live 库无）和 9 个技术字段（`dwd_id` / `created_time` / `updated_time` / `creater` / `updater` / `table_data_source` / `operator_remarks` / `is_deleted` / `insert_remark`）。",
         "> `dwd_corp_basic_info` 报告里有两段 Excel 描述（8 列技术壳 + 9 列业务），live 是 16 列并集：已合并。", ""]
    lab = {"P0": "P0 洗", "P1": "P1 洗", "P2": "P2 只贴", "ZERO": "0 行只贴", "ENT": "归 ENT-v4"}
    o.append("| # | 表 | 中文名 | live 行数 | 分期 | 业务列数 |")
    o.append("|---|---|---|---:|---|---:|")
    for i, (t, c) in enumerate(sorted(CLASS.items(), key=lambda x: (x[1], x[0])), 1):
        nb = len([k for k in tabs[t]["cols"] if k not in TECH])
        o.append("| %d | `%s` | %s | %s | %s | %d |" % (i, t, esc(tabs[t]["cn"]), "{:,}".format(tabs[t]["rows"]), lab[c], nb))
    o.append("")
    for t, c in sorted(CLASS.items(), key=lambda x: (x[1], x[0])):
        tb = tabs[t]
        o.append("## `%s` · %s（%s · {:,} 行）".format(tb["rows"]) % (t, esc(tb["cn"]), lab[c]))
        o.append("")
        o.append("| 列 | 中文名 | 类型 | 长度 | 空值 | 源标主键 |")
        o.append("|---|---|---|---|---|---|")
        for k, v in tb["cols"].items():
            if k in TECH:
                continue
            o.append("| `%s` | %s | %s | %s | %s | %s |" % (k, esc(v["cn"]), v["typ"], v["ln"], v["nul"], v["pk"]))
        o.append("")
    return "\n".join(o)


def src_expr(e, s):
    if e is None:
        return "—（该源无此列→NULL）"
    if e.startswith("'"):
        return "字面量 %s" % e
    if e.startswith("FN:"):
        return "`%s`（规则见 §3.3）" % e[3:]
    return "`%s`" % e


def gen_matrices():
    o = []
    for n, t in enumerate(TARGETS, 4):
        multi = len(t["src"]) > 1
        o.append("### 3.%d `%s` · %s（%s）" % (n, t["name"], t["cn"], t["phase"]))
        o.append("")
        o.append("源：" + "、".join("`%s`" % s for s in t["src"]) +
                 ("（UNION ALL，`src_table` 区分来源）" if multi else "（1:1）"))
        o.append("")
        hdr = "| 目标列 | 类型 | 说明 |" + "".join(" `%s` |" % s.replace("dwd_", "") for s in t["src"])
        o.append(hdr)
        o.append("|---|---|---|" + "---|" * len(t["src"]))
        o.append("| `src_dwd_id` | bigint NOT NULL | 供应方 dwd_id（追溯） |" + "".join(" `dwd_id` |" for _ in t["src"]))
        if multi:
            o.append("| `src_table` | varchar(64) NOT NULL | 来源物理表 |" + "".join(" 字面量 '%s' |" % s for s in t["src"]))
        for col, typ, cmt, m in t["cols"]:
            cells = ""
            for s in t["src"]:
                e = m.get(s) if isinstance(m, dict) else m
                cells += " %s |" % src_expr(e, s)
            o.append("| `%s` | %s | %s |%s" % (col, typ, esc(cmt), cells))
        o.append("| `etl_time` | datetime | GDF 写入时间（默认 CURRENT_TIMESTAMP） |" + "".join(" — |" for _ in t["src"]))
        o.append("")
        pk = "(`src_table`,`src_dwd_id`)" if multi else "(`src_dwd_id`)"
        o.append("键：PK=%s；普通索引 %s。业务自然键是否唯一以验收抽检为准（OPEN-FIN-02）。" % (pk, "、".join("`%s`" % c for c in t["idx"])))
        o.append("")
    return "\n".join(o)


def gen_ddl():
    o = ["# fin-dwd-draft · 金融 DWD 建表草稿（生成件）", "",
         "> **草稿，未签收**。库 `gkxlumenx_dwd`（GDF 只写正式库，禁 demo）。`demo_gkxlumenx_dwd` / 线上 lumen 库均**未建**这些表。",
         "> 结构真源待架构师入 `storage/FIN/stores/mysql/dwd.md`（OPEN-FIN-01）；入仓前以本文件为准，入仓后本文件改指针。",
         "> 生成：`script/gen_fin_pack.py`。字符集 `utf8mb4_0900_ai_ci`（`mysql-ddl-convention.md` §2）。", "", "```sql"]
    for t in TARGETS:
        multi = len(t["src"]) > 1
        o.append("CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`%s` (" % t["name"])
        o.append("  `src_dwd_id` bigint NOT NULL COMMENT '供应方 dwd_id（追溯）',")
        if multi:
            o.append("  `src_table` varchar(64) NOT NULL COMMENT '来源物理表',")
        for col, typ, cmt, _m in t["cols"]:
            o.append("  `%s` %s COMMENT '%s'," % (col, typ, cmt.replace("'", "''")))
        o.append("  `etl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'GDF 写入时间',")
        o.append("  PRIMARY KEY (%s)%s" % ("`src_table`,`src_dwd_id`" if multi else "`src_dwd_id`", "," if t["idx"] else ""))
        for i, c in enumerate(t["idx"]):
            o.append("  KEY `idx_%s` (`%s`)%s" % (c, c, "," if i < len(t["idx"]) - 1 else ""))
        o.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='%s';" % t["cn"])
        o.append("")
    o.append("```")
    return "\n".join(o) + "\n"


def splice(path, begin, end, body):
    s = io.open(path, encoding="utf-8").read()
    a, b = s.index(begin) + len(begin), s.index(end)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s[:a] + "\n" + body + "\n" + s[b:])


def w(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)


def main():
    tabs, sections = parse_report()
    check(tabs, sections)
    print("OK 自检通过：报告 section=%d 物理表=%d；P0/P1 源表=%d；目标 DWD=%d" % (
        sections, len(tabs), len([1 for c in CLASS.values() if c in ("P0", "P1")]), len(TARGETS)))
    if "--check" in sys.argv:
        return
    w(os.path.join(PACK, "02-WaveA-贴源表清单.yaml"), gen_yaml(tabs))
    w(os.path.join(PACK, "09a-源表业务列清单-金融31表.md"), gen_09a(tabs))
    w(os.path.join(PACK, "10-DWD-MySQL-DDL", "fin-dwd-draft.md"), gen_ddl())
    p09 = os.path.join(PACK, "09-金融域-ETL-Mapping明细-源表到DWD.md")
    if os.path.exists(p09):
        splice(p09, "<!-- BEGIN GEN §3 -->", "<!-- END GEN §3 -->", gen_matrices())
    print("已写：02 / 09a / 10/fin-dwd-draft / 09 §3")


if __name__ == "__main__":
    main()
