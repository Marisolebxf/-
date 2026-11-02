#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_016 平台月活跃用户数 · 三源探针脚本（S3-04 L5）。

含义：科技数据资源·应用视窗「资产应用总览」调用趋势图的「活跃用户数」序列——平台月去重
活跃用户数（MAU）。UI：ApplicationWindow.jsx:66（getCallTrendOption legend）/ :76（活跃用户数
虚线序列，mock usageCallTrend.users 日粒度 3,200-3,510）。mock 源 mockData.js:840-845。

判档路径（口径 = 月度去重活跃用户，活跃行为=登录/访问/调用任一）：
- 计算前提是「用户行为日志面」（用户标识 × 行为时间戳 × 行为类型，月窗去重）——三源
  user/active/visit/login/online 词族：dev 命中全部为框架管理面（sys_user 3 个运维账号/
  sys_log 1060 行管理日志/xxl_job_user/mp.wx_account 等），无终端用户行为流水；
  gkx 280 表 0 命中（要素库无用户表）；久新 210 表 live 复核唯一命中
  ads_technology_community_member（学科社区成员面——成员名册非行为流水，且非本平台用户）；
- 判完全不支持（指标及关键依赖三源均无法构建）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_016_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l5_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]

# ============ ① mock 层（UI 语义披露，不作数据证据） ============
MOCK_TREND = {
    "dates": ["05-16", "05-17", "05-18", "05-19", "05-20", "05-21", "05-22"],
    "calls": [78200, 82100, 79500, 84300, 86800, 85200, 85600],
    "users": [3200, 3350, 3280, 3420, 3510, 3480, 3456],
}
facts["mock_series_granularity"] = "日（非月）"
facts["mock_dates"] = MOCK_TREND["dates"]
facts["mock_users_series"] = MOCK_TREND["users"]
facts["mock_users_last_value"] = MOCK_TREND["users"][-1]  # 3456
facts["mock_users_max_value"] = max(MOCK_TREND["users"])  # 3510
facts["mock_users_min_value"] = min(MOCK_TREND["users"])  # 3200
facts["mock_semantics_note"] = ("users 序列是日活（DAU）口径的演示序列且未标注去重口径；"
                                "月活（MAU）需按月窗去重，mock 无月粒度序列")

# ============ ② dev：词族命中语义核验（共享探针 + 逐面定性） ============
facts["dev_table_total"] = probe["dev_table_total"]
facts["dev_user_active_word_tables"] = probe["dev_user_active_word_tables"]  # 16 张
# 逐面定性（共享探针已取计数；此处引用+登记）
facts["dev_sys_user_rows"] = probe["dev_sys_user_rows"]  # 3
facts["dev_sys_user_usernames"] = probe["dev_sys_user_usernames"]  # admin/admin1/gkxtest01
facts["dev_sys_user_max_update_time"] = probe["dev_sys_user_max_update_time"]
facts["dev_sys_tenant_rows"] = probe["dev_sys_tenant_rows"]  # 1
facts["dev_sys_tenant_user_rows"] = probe["dev_sys_tenant_user_rows"]  # 3
facts["dev_sys_log_rows"] = probe["dev_sys_log_rows"]  # 1060
facts["dev_sys_log_title_top8"] = probe["dev_sys_log_title_top8"]
facts["dev_sys_log_max_create_time"] = probe["dev_sys_log_max_create_time"]
facts["dev_user_word_hits_note"] = (
    "16 张命中全部为框架管理面：pig 后台账号系（sys_user/sys_tenant_user/xxl_job_user）、"
    "管理操作日志（sys_log）、小程序账号配置（mp.wx_account）、内容点赞收藏（app_social_details）、"
    "图成员（ads.graph_membership）、流程指派（flow.process_node_record_assign_user）、"
    "superset 配置（config.users）、区域范围成员（dim.region_scope_member）、文章收藏"
    "（app.app_article_collect）——无一张是终端用户行为流水")
# sys_log 按月分布（若管理日志可按月去重用户——量级证据）
d = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                    database="gkxlumenx_dwd", charset="utf8mb4",
                    connect_timeout=10, read_timeout=120)
c = d.cursor()
c.execute("SELECT DATE_FORMAT(create_time,'%Y-%m'), COUNT(*), COUNT(DISTINCT create_by) "
          "FROM gkxlumenx.sys_log GROUP BY DATE_FORMAT(create_time,'%Y-%m') "
          "ORDER BY DATE_FORMAT(create_time,'%Y-%m') ASC")
facts["dev_sys_log_monthly_dist"] = [[str(a), int(b), int(cc)] for a, b, cc in c.fetchall()]
d.close()

# ============ ③ gkx：词族复核（共享探针 0 命中） ============
facts["gkx_table_count"] = probe["gkx_table_total"]  # 280
facts["gkx_user_active_word_tables"] = probe["gkx_user_active_word_tables"]  # []

# ============ ④ 久新：live 词族复核（唯一命中=社区成员面，语义核） ============
try:
    JX = dict(host="47.93.119.170", port=29030, user="test2",
              password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
              database="gkx_technology_analysis_dev",
              connect_timeout=10, read_timeout=300)
    jconn = pymysql.connect(**JX)
    jc = jconn.cursor()
    jc.execute("SHOW TABLES")
    jt = sorted(r[0] for r in jc.fetchall())
    facts["jiuxin_table_count_live"] = len(jt)
    hits = [t for t in jt if re.search(r"user|account|member|active|visit|login|online", t, re.I)]
    facts["jiuxin_user_active_word_tables_live"] = hits
    # 唯一命中 ads_technology_community_member 语义核验（DESC 无权限则 SHOW COLUMNS）
    try:
        jc.execute("DESC ads_technology_community_member")
        facts["jiuxin_community_member_cols"] = sorted(r[0] for r in jc.fetchall())
        jc.execute("SELECT COUNT(*) FROM ads_technology_community_member")
        facts["jiuxin_community_member_rows"] = int(jc.fetchone()[0])
    except Exception as e:  # noqa: BLE001
        facts["jiuxin_community_member_desc_error"] = str(e)[:120]
    jconn.close()
    facts["jiuxin_probe_mode"] = "live"
except Exception as e:  # noqa: BLE001
    jt = snap["jiuxin"]["tables"]
    facts["jiuxin_user_active_word_tables_snapshot"] = [
        t for t in jt if re.search(r"user|account|member|active|visit|login|online", t, re.I)]
    facts["jiuxin_probe_mode"] = f"快照兜底（当日直连失败：{str(e)[:80]}）"
facts["jiuxin_hits_note"] = ("唯一词族命中 ads_technology_community_member 是学科技术社区"
                             "成员名册（成员登记面），非本平台用户的行为流水——语义排除")

# ================= 派生（负结论登记，B10） =================
derived += [
    {"key": "platform_mau", "value": None, "numerator": None, "denominator": None,
     "note": "『平台月活跃用户数』需用户行为日志面（用户标识×行为时间戳×月窗去重）——三源零承载"
             "（dev 命中全为框架管理面；gkx 0 命中；久新唯一命中为学科社区成员名册）→ 不可构建，"
             "按 B10 留空即负结论登记"},
]

# ================= absence_probe =================
absence += [
    {"probe": "dev 用户行为日志面（user/account/member/active/visit/login/online 词族，542 表）",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*（共享探针 _probe_s304_l5）",
     "hits": len([t for t in facts["dev_user_active_word_tables"] if "log" in t.lower()]),
     "hit_detail": "16 张命中无一行为流水：sys_log 是管理操作日志（title Top 登录成功 912/登录失败 140），"
                   "create_by 全为 admin 等运维账号——后台登录行为，非终端用户访问/调用行为"},
    {"probe": "dev 用户主档量级（MAU 分母侧最近邻）",
     "source": "dev", "sql": "SELECT COUNT(*) FROM gkxlumenx.sys_user / sys_tenant_user",
     "hits": 0,
     "hit_detail": f"sys_user {facts['dev_sys_user_rows']} 行（{facts['dev_sys_user_usernames']}——"
                   "运维测试账号）；sys_tenant 1 / sys_tenant_user 3——无终端用户注册面，"
                   "月活无从谈起"},
    {"probe": "gkx 用户/活跃面（同词族，280 表）",
     "source": "gkx", "sql": "information_schema.tables 扫 gkx（共享探针）",
     "hits": len(facts["gkx_user_active_word_tables"]),
     "hit_detail": "0 命中——gkx 为要素明细库（论文/专利/机构/学者），无任何用户行为表"},
    {"probe": "久新用户/活跃面（同词族，live 复核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤 + DESC 语义核",
     "hits": 1,
     "hit_detail": "唯一命中 ads_technology_community_member——学科技术社区成员名册"
                   "（成员登记非行为流水），且非本平台用户体系——语义排除；探测模式见 "
                   "facts.jiuxin_probe_mode"},
    {"probe": "需求原文「月活跃用户数」定义段",
     "source": "doc", "sql": "rg 活跃用户 三份需求真源",
     "hits": 2,
     "hit_detail": "主需求 :2813 与 SRS seq 387「展示主题数据被调用次数、活跃用户、业务系统分布等"
                   "多项指标」——「活跃用户」是图表伴随维度（功能分句），月度口径/去重规则/"
                   "活跃行为定义均无；「平台月活跃用户数」指标名 0 命中；mock users 是日粒度演示序列"},
]

support = "完全不支持"

notes += [
    "判档：MAU 需「用户标识×行为时间戳×行为类型」的终端用户行为日志（月窗去重）——dev 命中全为"
    "框架管理面（3 个运维账号/1060 行管理日志），gkx 0 命中，久新唯一命中为学科社区成员名册"
    "（语义排除）→ 指标及关键依赖三源均无法构建 → 完全不支持",
    "权威口径（R1 国家统计局互联网经济统计报表制度 U202/U203 表）：平台「月度活跃用户数」为法定"
    "报表指标（重点互联网出行/医疗平台按季填报）——官方仅要求填数、未公开去重口径细则；"
    "业界口径（R2/R3）：MAU=统计月内发生活跃行为的去重用户（设备 ID 或账号 ID），"
    "活跃行为定义（启动/登录/关键行为）由平台自定且须披露",
    "mock 披露：usageCallTrend.users=[3200…3510]（7 个自然日，日粒度）——是 DAU 形态的演示序列"
    "且无去重标注；与 MAU（月窗去重）不同粒度不同口径，不作数据证据（B10）",
    "最近邻证据（dev sys_log，语义排除披露用）：1060 行管理操作日志按月分布 "
    f"{facts['dev_sys_log_monthly_dist']}——月去重操作人 create_by 仅 admin 级账号，"
    "是后台运维登录行为，非平台终端用户活跃",
    "B11 对账：dev 542/gkx 280/久新 210 表数共享快照；sys_user/sys_log 读数与 020 件同锚"
    "（sys_log 活表计数随时间增长：020 件 1,060 行与本件实时读数同量级）",
    "升档触发器（B10）：①埋点/访问日志接入（用户标识×行为时间戳）→ 升完全直接支持（工程立项）；"
    "②建平台注册用户面 → 注册数可算但活跃不可算（仍缺行为日志，最多升部分支持且须口径披露"
    "「注册用户数非月活」）；③维持现状 → 完全不支持（UI 该位建议「暂无数据」）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_016",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:66",
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:76",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:840",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「平台月活跃用户数」指标名；语义锚 SRS 应用视窗 seq 387"
                "「活跃用户」（图表伴随维度分句）/主需求 :2813 同文——月度口径/去重规则无定义",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [], "base_years_missing": [],
    "base_years_note": "活跃度类监控指标，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["3200", "3350", "3280", "3420", "3510", "3480", "3456", "3", "1060",
                          "912", "140", "542", "280", "210", "1"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
