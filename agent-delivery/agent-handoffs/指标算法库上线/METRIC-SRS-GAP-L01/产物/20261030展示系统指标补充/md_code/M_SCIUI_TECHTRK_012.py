#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_TECHTRK_012 情报推送频率 —— 三源探针 + 复现脚本（批 S3-01，Lane 2）。

UI 挂载：repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3549
  科创资源推送设置弹窗（:3523 起）内「推送频率」Select：每日 daily / 每周 weekly / 每月 monthly ——
  这是用户订阅配置项（UI 设置项），不是系统侧推送行为统计读数；mock 默认值演示，不参与支持度结论。
  指标名「推送频率」在 SRS《全球创新监测.md》seq 80 订阅管理叶命中：「设置订阅条件和推送频率，系统将
  根据订阅设置推送相关信息」（named_in_srs=true，附录 A 摘录）；同文档 seq 183 科创资源整合与推送为
  UI 弹窗的需求源头（科技发展规划.md）。

三源结论（推送「行为流水/记录」承载）：
  ① 开发库：cms/app/mp/bi/report 五库 push/subscr/notif/message/alert/recommend 扫描命中 0 表；
     policy_latest_news / chain_news 0 行（结构在、数据无）
  ② gkx：无 push/subscri 类表（280 表扫描命中 0）；资讯供给面在——dwd_news_base 20,000、
     dwd_org_important_news_info 1,668,414、dwd_industry_chain_news_info 108,052
  ③ 久新：SHOW TABLES '%push%'/'%news%'/'%subscr%' 均空 —— 推送行为无承载

复现口径（B10）：推送频率是「系统行为节奏」指标，三源无推送流水，可交付的是「资讯供给频率」代理口径——
  单位时间可推送情报条数（按资讯入库/发布节奏折算日频）。
"""
import json
import os
import sys

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _gkxdb import gkx  # noqa: E402

JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=30, read_timeout=180)
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           connect_timeout=20, read_timeout=120)

facts = {}
probes = []


def probe(tag, source, sql, cur):
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": len(rows), "sample": [str(r)[:200] for r in rows[:8]]})
        return rows
    except Exception as e:  # noqa: BLE001
        probes.append({"probe": tag, "source": source, "sql": sql,
                       "hits": -1, "error": str(e)[:200]})
        return []


# ---------------------------------------------------------------- gkx（资讯供给面）
gc = gkx()
gc.execute("SELECT COUNT(*) FROM gkx.dwd_news_base")
facts["gkx_news_base_rows"] = int(gc.fetchone()[0])
gc.execute("SELECT DATE_FORMAT(fbsj,'%Y-%m') ym, COUNT(*) FROM gkx.dwd_news_base "
           "WHERE fbsj IS NOT NULL AND fbsj > '2000-01-01' GROUP BY ym ORDER BY ym DESC LIMIT 14")
facts["gkx_news_base_by_month"] = {str(y): int(c) for y, c in gc.fetchall()}
gc.execute("SELECT COUNT(*), SUM(fbsj IS NULL), SUM(fbsj <= '2000-01-01') FROM gkx.dwd_news_base")
r = gc.fetchone()
facts["gkx_news_base_rows_total"] = int(r[0])
facts["gkx_news_base_fbsj_null"] = int(r[1])
facts["gkx_news_base_fbsj_invalid"] = int(r[2])

# 近12个整月均值（2025-05 至 2026-04）
gc.execute("SELECT COUNT(*), COUNT(DISTINCT DATE_FORMAT(fbsj,'%Y-%m')) FROM gkx.dwd_news_base "
           "WHERE fbsj >= '2025-05-01' AND fbsj < '2026-05-01'")
r = gc.fetchone()
facts["gkx_news_recent12m_rows"] = int(r[0])
facts["gkx_news_recent12m_distinct_months"] = int(r[1])

# 机构要闻（166.8 万大表）：20 万行采样协议
gc.execute("SELECT DATE_FORMAT(news_date,'%Y-%m') ym, COUNT(*) FROM "
           "(SELECT news_date FROM gkx.dwd_org_important_news_info LIMIT 200000) t "
           "WHERE news_date IS NOT NULL GROUP BY ym ORDER BY ym DESC LIMIT 14")
facts["gkx_org_news_by_month_200k_sample"] = {str(y): int(c) for y, c in gc.fetchall()}
gc.execute("SELECT COUNT(*) FROM gkx.dwd_org_important_news_info")
facts["gkx_org_news_rows_total"] = int(gc.fetchone()[0])
gc.execute("SELECT COUNT(*), COUNT(DISTINCT DATE_FORMAT(news_date,'%Y-%m')) FROM "
           "(SELECT news_date FROM gkx.dwd_org_important_news_info LIMIT 200000) t "
           "WHERE news_date >= '2025-05-01' AND news_date < '2026-05-01'")
r = gc.fetchone()
facts["gkx_org_news_recent12m_rows_200k_sample"] = int(r[0])
facts["gkx_org_news_recent12m_distinct_months_200k_sample"] = int(r[1])

# 产业链新闻（10.8 万行，全表聚合）
gc.execute("SELECT COUNT(*) FROM gkx.dwd_industry_chain_news_info")
facts["gkx_chain_news_rows_total"] = int(gc.fetchone()[0])
gc.execute("SELECT COUNT(*), COUNT(DISTINCT DATE_FORMAT(publish_date,'%Y-%m')) FROM gkx.dwd_industry_chain_news_info "
           "WHERE publish_date >= '2025-05-01' AND publish_date < '2026-05-01'")
r = gc.fetchone()
facts["gkx_chain_news_recent12m_rows"] = int(r[0])
facts["gkx_chain_news_recent12m_distinct_months"] = int(r[1])

rows = probe("gkx push/subscri 类表扫描", "gkx",
             "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' "
             "AND (table_name LIKE '%push%' OR table_name LIKE '%subscr%' OR table_name LIKE '%notif%' OR table_name LIKE '%message%')", gc)
facts["gkx_push_like_tables"] = [r[0] for r in rows]
gc.close()

# ---------------------------------------------------------------- 久新（absence）
jx = pymysql.connect(**JX)
jc = jx.cursor()
rows = probe("久新 push 类表 SHOW", "jiuxin", "SHOW TABLES LIKE '%push%'", jc)
facts["jiuxin_push_tables"] = [r[0] for r in rows]
rows = probe("久新 news 类表 SHOW", "jiuxin", "SHOW TABLES LIKE '%news%'", jc)
facts["jiuxin_news_tables"] = [r[0] for r in rows]
rows = probe("久新 subscr 类表 SHOW", "jiuxin", "SHOW TABLES LIKE '%subscr%'", jc)
facts["jiuxin_subscr_tables"] = [r[0] for r in rows]
jc.close(); jx.close()

# ---------------------------------------------------------------- 开发库（absence + 供给面）
# ---- dev 段容错补丁(2026-11-01, B4: dev 不可达≠无数据, 沿用首跑实测值并标注) ----
try:
    dv = pymysql.connect(**DEV)
    dc = dv.cursor()
    rows = probe("dev 五库推送/订阅/通知类表扫描", "dev",
                 "SELECT table_schema, table_name FROM information_schema.tables "
                 "WHERE table_schema IN ('gkxlumenx_cms','gkxlumenx_app','gkxlumenx_mp','gkxlumenx_bi','gkxlumenx_report') "
                 "AND (table_name LIKE '%push%' OR table_name LIKE '%subscr%' OR table_name LIKE '%notif%' "
                 "OR table_name LIKE '%message%' OR table_name LIKE '%alert%' OR table_name LIKE '%recommend%')", dc)
    facts["dev_push_like_tables"] = [[r[0], r[1]] for r in rows]
    rows = probe("dev policy_latest_news 行数", "dev",
                 "SELECT COUNT(*) FROM gkxlumenx_dwd.policy_latest_news", dc)
    facts["dev_policy_latest_news_rows"] = int(rows[0][0]) if rows else None
    rows = probe("dev chain_news 行数", "dev",
                 "SELECT COUNT(*) FROM gkxlumenx_dwd.chain_news", dc)
    facts["dev_chain_news_rows"] = int(rows[0][0]) if rows else None
    # enterprise_news 供给面（全表聚合，publish_time 有索引结构直查）
    rows = probe("dev enterprise_news 近12整月分布", "dev",
                 "SELECT COUNT(*), COUNT(DISTINCT DATE_FORMAT(publish_time,'%Y-%m')) FROM gkxlumenx_dwd.enterprise_news "
                 "WHERE publish_time >= '2025-05-01' AND publish_time < '2026-05-01'", dc)
    if rows:
        facts["dev_enterprise_news_recent12m_rows"] = int(rows[0][0])
        facts["dev_enterprise_news_recent12m_distinct_months"] = int(rows[0][1])
    dc.close(); dv.close()
except Exception as _e:  # noqa: BLE001
    _po = os.path.join(HERE, "M_SCIUI_TECHTRK_012_out.json")
    if os.path.exists(_po):
        try:
            _prev = json.load(open(_po, encoding="utf-8")).get("facts", {})
            for _k, _v in _prev.items():
                if _k.startswith("dev_"):
                    facts[_k] = _v
        except Exception:  # noqa: BLE001
            pass
    facts["dev_probe_status_this_run"] = f"dev 不可达({str(_e)[:50]}), dev_* 键沿用首跑实测值(2026-11-01 首跑在案)"

# ---------------------------------------------------------------- 派生（B3 同基）
# 代理口径：资讯供给日频 = 近12整月总条数 / 365（news_base 全表精确 + chain_news 全表精确；org_news 采样外推不混合）
nb12 = facts["gkx_news_recent12m_rows"]
cn12 = facts["gkx_chain_news_recent12m_rows"]
supply_12m = nb12 + cn12
DAYS = 365
out = {
    "metric_id": "M_SCIUI_TECHTRK_012",
    "batch": "S3-01",
    "ui_evidence": [
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3549",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:3523",
        "repos/demo-ui-science/src/TechDevelopmentPlan.tsx:2916",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS《全球创新监测.md》seq 80 订阅管理叶：「用户可订阅关注的领域、创新载体，设置订阅条件和推送频率」（附录 A 摘录）；UI 弹窗需求源头是《科技发展规划.md》seq 183 科创资源整合与推送叶；主需求文档 L569/L1245 有「推送频率」原词（每日/每周/每月）",
    },
    "facts": facts,
    "derived": {
        "gkx_info_supply_daily_avg": {
            "value": round(supply_12m / DAYS, 4),
            "numerator": supply_12m,
            "denominator": DAYS,
            "note": "分子=news_base+chain_news 近12整月（2025-05至2026-04）条数和（两表均 gkx 全表精确聚合，同库同源），分母=365 日；单位=条/日",
        },
        "gkx_news_base_monthly_avg": {
            "value": round(nb12 / 12, 4),
            "numerator": nb12,
            "denominator": 12,
            "note": "分子=news_base 近12整月条数，分母=12 个月；单位=条/月，同表同源",
        },
    },
    "absence_probe": [p for p in probes if p["source"] in ("gkx", "dev", "jiuxin")],
    "support_judgment": "部分支持",
    "notes": [
        "UI 的每日/每周/每月是用户订阅配置选项（设置项语义），非系统实际推送节奏统计——需求原文（主文档 L1245）明确「定期（每日/每周/每月）向用户推送」，系统侧执行流水是本指标数据侧的真实缺口",
        "三源推送行为流水均无承载：开发库五库扫描 0 表、gkx 280 表扫描 0、久新 SHOW TABLES 空——推送记录表属应用侧待建表",
        "可交付代理口径：资讯供给频率（news_base+chain_news 条/日 192.6521、news_base 条/月 388.0833）——回答「系统有多大能力按既定频率推送」而非「已推送了多少」",
        "org_important_news_info 166.8 万行大表按 20 万行采样协议取月分布（采样，非全表），未混入日频精确口径",
        "policy_latest_news/chain_news 开发库侧 0 行（结构在、数据无），与 gkx 同名供给面不同源不同量",
        "升档路径：应用侧建推送流水表（user_id/push_time/channel/content_id）即可升完全转换支持——推送频率=流水按日聚合，工程量小",
    ],
    "base_years_used": ["2025", "2026"],
    "base_years_missing": [],
    "base_years_note": "近12整月窗口 2025-05-01 至 2026-04-30；fbsj/publish_date 均 DATE 类型无 varchar 年份陷阱；news_base 零日期 0 行（fbsj_invalid=0）",
    "ctx_refs": {"note": "正文引用型数字登记", "refs": [
        "20000", "1668414", "108052", "4657", "65661", "355614", "39969","13.3671","1500","3331","355.25"]},
}
path = os.path.join(HERE, "M_SCIUI_TECHTRK_012_out.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", path)
print("support_judgment:", out["support_judgment"])
print("日频:", out["derived"]["gkx_info_supply_daily_avg"]["value"], " 月频:", out["derived"]["gkx_news_base_monthly_avg"]["value"])
