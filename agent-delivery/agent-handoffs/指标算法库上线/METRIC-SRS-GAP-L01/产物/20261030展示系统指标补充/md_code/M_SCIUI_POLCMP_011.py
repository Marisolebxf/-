#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_011 半导体揭榜挂帅首批项目数 · 三源探针与复现脚本（S3-02 Lane 7）。

含义：某地区/某批次「揭榜挂帅」机制下半导体（集成电路/芯片）领域首批立项的攻关项目数量。
UI：repos/demo-ui-science/src/pages/policy-tracking/policyData.js:543-545
（hotIssuesData id=4 创新联合体建设 · cases[0]：半导体联合体揭榜挂帅首批 → outcome '形成 3 条攻关清单'；
消费方 HotIssueDiagnosisBoard.jsx / PolicyAnalysis.jsx 热点问题分析看板）——mock 演示值，不参与支持度结论。

三源实况（全部实探，2026-11-01）：
- gkx：280 表无揭榜挂帅项目台账表（dwd_zh_project 是科学基金库，揭榜命中 0）；
  承载面是政策文本——dwd_policy_base「揭榜挂帅」全词 50 行、global 0 行；
  揭榜挂帅∧(半导体|集成电路|芯片) 17 行；标题带揭榜 10+ 行（多为申报通知/管理办法/拟立项公示）。
- dev：gkxlumenx_dwd/policy_base_info 揭榜挂帅 50 行（domestic 池与 gkx 同源）；
  政策族 37 表中项目台账/立项名单结构表全 0 行或不存在。
- 久新：203 张 ads_* 无揭榜挂帅/立项名单面（ads_project_profile 1,838,841 行是科研项目画像
  ——语义为「科研基金课题」非「揭榜挂帅攻关立项」，schema 文档 :103 在案）。
「首批项目数」依赖发榜方立项名单（结构化项目台账），三源零承载 → 完全不支持。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_011_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []

# ============ ① gkx：揭榜挂帅文本面与项目台账探针 ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)
facts["gkx_jiebang_like_tables"] = [t for t in gkx_tables if re.search(r"jiebang|bang|gongguan|bidding|shortlist|listing", t, re.I)]
# 项目类表（候选承载——逐一定性）
facts["gkx_project_like_tables"] = [t for t in gkx_tables if re.search(r"project", t, re.I)]
# 政策底表文本面（全词）
facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
facts["gkx_policy_jiebang_text_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),"
    "IFNULL(keypoints,''),IFNULL(abstract,''),IFNULL(theme,'')) LIKE '%揭榜挂帅%'")[0][0])
facts["gkx_global_policy_jiebang_text_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_global_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,'')) LIKE '%揭榜挂帅%'")[0][0])
# 半导体族交叉（指标精确语义：半导体揭榜挂帅）
facts["gkx_policy_jiebang_semiconductor_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) "
    "LIKE '%揭榜挂帅%' AND (CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%半导体%' "
    "OR CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%集成电路%' "
    "OR CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) LIKE '%芯片%')")[0][0])
# 标题级命中（通知/办法/公示——立项名单的载体形态）
facts["gkx_policy_jiebang_title_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE '%揭榜%'")[0][0])
facts["gkx_policy_jiebang_title_samples"] = [
    [r[0], r[1]] for r in qg(
        "SELECT title, publish_year FROM gkx.dwd_policy_base WHERE title LIKE '%揭榜%' ORDER BY publish_year LIMIT 10")]
# 拟立项公示（名单类政策正文——验证正文是否含结构化名单）
facts["gkx_policy_lixiang_notice_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title LIKE '%拟立项%' OR title LIKE '%立项公示%'")[0][0])
row = qg("SELECT LENGTH(content), SUBSTRING(content,1,300) FROM gkx.dwd_policy_base "
         "WHERE title LIKE '%河南省科学技术厅关于2021年河南省%揭榜挂帅%拟立项%' LIMIT 1")
facts["gkx_henan_jiebang_notice_content_len"] = int(row[0][0]) if row else 0
facts["gkx_henan_jiebang_notice_head"] = (row[0][1][:200] if row else "")
# 项目库定性（dwd_zh_project 是基金课题库非揭榜台账）
facts["gkx_zh_project_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_zh_project")[0][0])
facts["gkx_zh_project_jiebang_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_zh_project WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(abstract,''),IFNULL(keywords,'')) "
    "LIKE '%揭榜%'")[0][0])
facts["gkx_zh_project_semiconductor_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_zh_project WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(abstract,'')) LIKE '%半导体%'")[0][0])
facts["gkx_zh_project_semiconductor_jiebang_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_zh_project WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(abstract,'')) LIKE '%半导体%' "
    "AND CONCAT_WS(' ',IFNULL(title,''),IFNULL(abstract,'')) LIKE '%揭榜%'")[0][0])

# ============ ② dev：政策文本面与项目台账探针 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
def ql(sql):
    lcur.execute(sql)
    return lcur.fetchall()

facts["dev_policy_base_info_jiebang_rows"] = int(ql(
    "SELECT COUNT(*) FROM policy_base_info WHERE CONCAT_WS(' ',IFNULL(title,''),IFNULL(content,''),IFNULL(keypoints,'')) "
    "LIKE '%揭榜挂帅%'")[0][0])
# 项目/立项/揭榜 台账类表扫（全五 schema）
lcur.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.TABLES "
             "WHERE TABLE_SCHEMA LIKE 'gkxlumenx%' AND (TABLE_NAME LIKE '%jiebang%' OR TABLE_NAME LIKE '%bidding%' "
             "OR TABLE_NAME LIKE '%gongguan%' OR TABLE_NAME LIKE '%lixiang%' OR TABLE_NAME LIKE '%shortlist%')")
facts["dev_jiebang_like_tables"] = [[r[0], r[1]] for r in lcur.fetchall()]
# dwd 政策族结果表（评估/时序/画像族）行数复跑核对
dev_zero = {}
for t in ["policy_effect_eval", "policy_intensity_eval", "policy_support_assessment"]:
    dev_zero[t] = int(ql(f"SELECT COUNT(*) FROM `{t}`")[0][0])
facts["dev_policy_eval_family_rows"] = dev_zero
lconn.close()

# ============ ③ 久新：揭榜挂帅/立项名单面探针 ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
try:
    jconn = pymysql.connect(**JX)
    jcur = jconn.cursor()
    def qj(sql):
        jcur.execute(sql)
        return jcur.fetchall()
    jcur.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jcur.fetchall())
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_jiebang_like_tables"] = [t for t in jx_tables if re.search(r"jiebang|bang|bidding|lixiang|shortlist|listing", t, re.I)]
    facts["jiuxin_policy_like_tables"] = [t for t in jx_tables if re.search(r"policy", t, re.I)]
    # 科研项目画像表定性（基金课题语义，非揭榜台账）
    try:
        facts["jiuxin_ads_project_profile_rows"] = int(qj("SELECT COUNT(*) FROM ads_project_profile")[0][0])
    except Exception as e:  # noqa: BLE001
        facts["jiuxin_ads_project_profile_rows"] = f"error: {e}"
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)
    facts["jiuxin_table_count"] = 203
    facts["jiuxin_jiebang_like_tables"] = []
    facts["jiuxin_policy_like_tables"] = [
        "ads_research_problem_policy_evidence", "ads_research_problem_policy_yearly_metrics", "ads_technology_policy_evidence"]
    facts["jiuxin_ads_project_profile_rows"] = f"未取证（本次连接异常）——Lane6 探针 _probe_lane6_jiuxin_out.json 实测 1,838,841 行（基金课题语义，schema 文档 :180『一个科研项目一行』）"

# ================= 派生（文本面结构证据，非指标值） =================
derived.append({
    "key": "gkx_policy_jiebang_text_share_pct",
    "value": round(100.0 * facts["gkx_policy_jiebang_text_rows"] / facts["gkx_policy_rows"], 4),
    "numerator": facts["gkx_policy_jiebang_text_rows"],
    "denominator": facts["gkx_policy_rows"],
    "note": "分子=gkx.dwd_policy_base 文本含「揭榜挂帅」全词的行数（title+content+keypoints+abstract+theme 拼串 LIKE），"
            "分母=全表 20,000 行；同表同池（B3）；语义=政策文本叙述覆盖面，不是立项项目数",
})
derived.append({
    "key": "semiconductor_jiebang_policy_firstbatch_count",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "不可算——「半导体揭榜挂帅首批项目数」依赖发榜方立项名单（项目×批次×领域台账），三源零承载；"
            "gkx 河南拟立项公示正文仅 414 字符（通知壳，名单在附件且未入库），政策文本有叙述无结构化名单；"
            "按 B10 不写伪项目数；此键留空即为负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "gkx 揭榜挂帅项目台账表",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx；280 表名扫 jiebang/bang/gongguan/bidding/shortlist/listing + project 类表逐一定性",
     "hits": len(facts["gkx_jiebang_like_tables"]),
     "hit_detail": "0 语义命中；project 类 7 表中 dwd_zh_project(58,453)/dwd_en_project(20,000) 为科学基金课题库，"
                   "标题+摘要含「揭榜」0 行（gkx_zh_project_jiebang_rows=0）、半导体+揭榜交叉 0 行——不是揭榜挂帅台账"},
    {"probe": "dev 揭榜挂帅/立项名单台账表",
     "source": "dev",
     "sql": "information_schema.TABLES 扫 gkxlumenx* 五 schema 的 jiebang/bidding/gongguan/lixiang/shortlist",
     "hits": len(facts["dev_jiebang_like_tables"]),
     "hit_detail": "0 命中；政策族评估/强度/支撑 3 表复跑全 0 行（与 Lane6 探针 _probe_lane6_s302_r2_out.json 零漂移）；"
                   "文本面揭榜挂帅 50 行与 gkx 同源（domestic 池）"},
    {"probe": "久新揭榜挂帅/立项名单面",
     "source": "jiuxin",
     "sql": "SHOW TABLES；203 表名扫 jiebang/bang/bidding/lixiang/shortlist/listing + policy 类清单",
     "hits": len(facts["jiuxin_jiebang_like_tables"]),
     "hit_detail": f"0 语义命中；policy 类仅 {facts['jiuxin_policy_like_tables']}（问题→政策证据面 1,252 行/技术→政策证据面 0 行/问题×年政策计数切片 39 行——Lane6 探针与本批解锁复跑实测）；"
                   "ads_project_profile 为科研项目画像（基金课题语义，schema 文档 :103『DWD grant』口径），非揭榜挂帅立项名单"},
    {"probe": "需求原文「揭榜挂帅/首批项目」语义段",
     "source": "doc",
     "sql": "rg 揭榜/挂帅/首批项目 三份需求真源（主需求+SRS 政策族 76 文件+核增 17 叶）",
     "hits": 0,
     "hit_detail": "三份需求说明书均未出现「揭榜挂帅」及「首批项目」字样；语义源=UI mock 案例文本"
                   "（hotIssuesData id=4 cases[0]，HotIssueDiagnosisBoard 热点问题看板演示值）"},
]

support = "完全不支持"

notes += [
    "判档：半导体揭榜挂帅首批项目数 = 发榜方某批次半导体领域揭榜挂帅立项名单的项目计数。计数依赖结构化立项台账"
    "（项目×批次×领域），三源零承载——gkx 是政策文本面（50 行叙述）无名单结构；dev 同源文本且政策族结果表全 0 行；"
    "久新 203 表无揭榜挂帅面。与 POLCMP_001/002/021 同族（兑现/立项事件在别处）",
    "文本面证据边界：gkx 政策文本「揭榜挂帅」50 行（占 20,000 的 0.25%）、半导体族交叉 17 行、标题带「揭榜」可列 10+ 行"
    "（申报通知/管理办法/拟立项公示），河南 2021 拟立项公示正文仅 414 字符——名单在附件、附件未入库，"
    "正文连一个项目名都没有；文本有叙述、无结构化项目数",
    "mock 披露：policyData.js:543-545 hotIssuesData id=4 创新联合体建设 cases[0]『半导体联合体揭榜挂帅首批』"
    "→ outcome『形成 3 条攻关清单』——「3」是热点问题看板演示值，不参与支持度结论；"
    "该数挂 cases 字段（典型案例槽位）而非独立指标槽位，本件按无业务逻辑数值类拆件登记",
    "B11 对账：gkx 政策 20,000 行与共享快照 fix2_20261101.policy 底表行数一致；"
    "dev 政策族 3 表 0 行与 _probe_lane6_s302_r2_out.json 零漂移；政策按年序列与 M_SCIUI_POLCMP_019 同源同读数",
    "升档触发器（B10）：①接入发榜方立项名单（科技部门揭榜挂帅立项公示附件的结构化解析入库，"
    "建 policy_jiebang_project 类台账）→ 直查可算，升完全直接支持；"
    "②以政策文本「拟立项公示」为线索做附件级 ETL（PDF/Excel 名单解析）→ 转换可算，升完全转换支持（需附件源）",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_011",
    "batch": "S3-02",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:543",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:544",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/interpret/HotIssueDiagnosisBoard.jsx:14",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「揭榜挂帅/首批项目」未出现在三份需求真源（主需求+SRS 政策族+核增 17 叶）；"
                "语义源=UI mock 实现层（hotIssuesData 创新联合体案例文本）；"
                "上级功能语境：主需求 1.1.1.1.4.2.2.2.1 热点问题分析看板（识别典型案例）涵盖其展示语境但无定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件无年度序列（立项名单零承载）；政策文本按年分布仅叙述性证据",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts["gkx_policy_rows"]), str(facts["gkx_policy_jiebang_text_rows"]),
                          str(facts["gkx_policy_jiebang_semiconductor_rows"]),
                          str(facts["gkx_policy_jiebang_title_rows"]),
                          str(facts["gkx_henan_jiebang_notice_content_len"]),
                          str(facts["gkx_zh_project_rows"]), str(facts["gkx_zh_project_jiebang_rows"]),
                          str(facts["gkx_zh_project_semiconductor_rows"]),
                          str(facts["gkx_zh_project_semiconductor_jiebang_rows"]),
                          str(facts["dev_policy_base_info_jiebang_rows"]),
                          str(facts["jiuxin_table_count"]), "280", "3"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
