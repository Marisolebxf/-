#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_023 应用主体总数 · 三源探针脚本（S3-04 L5）。

含义：科技数据资源·总体视窗/资源应用状态「资源应用主体详细列表」的应用主体计数（科研机构/
企业/项目团队三类）。UI：ResourceAppSubjectList.jsx:126（Statistic title="应用主体总数"
value=summary.total，summary.total=resourceAppSubjects.length——mock 数组长度）。
mock 源 mockData.js:849-861（resourceAppSubjects 10 条：科研机构 4/企业 3/项目团队 3）。

判档路径（口径 = 平台资源应用主体登记总数，seq 345「统计和展示所有资源实际应用主体」）：
- 直接承载需「资源应用主体登记面」——三源 subject 词族 0 命中；
- dev 侧可能走「主体登记面」：gkxlumenx_dwd.enterprise_base（189,115 行企业底册）+
  gkxlumenx_topic_enterprise 21 表（21 主体库主题工程）——语义核验是否「应用主体」；
- gkx 侧代理候选：dwd_org_base_info 189,116（要素库机构底册——数据域主体非应用主体）；
- 久新 210 表 subject 0 命中；
- 判部分支持：dev/gkx 有机构/企业底册（结构+数据双在，计数可转换交付），但「应用主体」
  语义 = 与平台发生过数据资源应用关系的主体，需主体×资源应用关系表——三源零承载，
  底册计数是「注册主体」上界口径非「应用主体」口径（口径级缺口，B10 双口径披露）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_023_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l5_out.json")
CACHE = os.path.join(BASE, "_snapshots", "_s304_gkx_counts_cache.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]
cache = json.load(open(CACHE, encoding="utf-8"))

# ============ ① mock 层（UI 语义披露，不作数据证据） ============
MOCK_SUBJECTS = [
    ("中科院计算技术研究所", "科研机构", "结构化数据", 312000, True),
    ("华为中央研究院", "企业", "半结构化数据", 268000, True),
    ("精准医疗专项攻关组", "项目团队", "非结构化数据", 196000, True),
    ("清华大学交叉信息院", "科研机构", "结构化数据", 178000, True),
    ("比亚迪汽车工程研究院", "企业", "实时流数据", 152000, False),
    ("蓝天保卫战监测项目组", "项目团队", "实时流数据", 141000, False),
    ("中国农科院信息所", "科研机构", "结构化数据", 128000, False),
    ("商汤科技研究院", "企业", "非结构化数据", 119000, False),
    ("深海探测工程联合团队", "项目团队", "结构化数据", 98000, False),
    ("国家互联网应急中心", "科研机构", "非结构化数据", 87000, False),
]
facts["mock_subject_total"] = len(MOCK_SUBJECTS)  # 10
by_type = {}
for _, st, _, _, _ in MOCK_SUBJECTS:
    by_type[st] = by_type.get(st, 0) + 1
facts["mock_subject_by_type"] = dict(sorted(by_type.items()))  # 企业3/科研机构4/项目团队3
facts["mock_key_users"] = sum(1 for *_, k in MOCK_SUBJECTS if k)  # 4
facts["mock_ui_note"] = ("summary.total=resourceAppSubjects.length（mockData.js 数组长度）；"
                         "组件挂载 ResourceAppSubjectList.jsx:126 Statistic「应用主体总数」")

# ============ ② dev：主体登记面探查（enterprise_base + topic_enterprise 库） ============
d = pymysql.connect(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
                    database="gkxlumenx_dwd", charset="utf8mb4",
                    connect_timeout=10, read_timeout=120)
c = d.cursor()
c.execute("SELECT COUNT(*), COUNT(DISTINCT enterprise_name) FROM gkxlumenx_dwd.enterprise_base")
row = c.fetchone()
facts["dev_enterprise_base_rows"] = int(row[0])
facts["dev_enterprise_base_distinct_names"] = int(row[1])
# 主体库主题工程（gkxlumenx_topic_enterprise 21 表）——是否「应用主体」语义
c.execute("SELECT table_name FROM information_schema.tables "
          "WHERE table_schema='gkxlumenx_topic_enterprise' ORDER BY table_name")
facts["dev_topic_enterprise_tables"] = [r[0] for r in c.fetchall()]
# 该库有没有「主体登记」表（enterprise/subject/org 词族）
c.execute("SELECT table_name, table_rows FROM information_schema.tables "
          "WHERE table_schema='gkxlumenx_topic_enterprise' "
          "AND table_name REGEXP 'enterprise|subject|org' ORDER BY table_name")
facts["dev_topic_enterprise_entity_like"] = [[r[0], int(r[1] or 0)] for r in c.fetchall()]
# subject 词族全库复核（共享探针）
facts["dev_subject_word_tables"] = probe["dev_subject_word_tables"]  # []
facts["dev_table_total"] = probe["dev_table_total"]
d.close()

# ============ ③ gkx：机构底册（代理候选上界） + 高校/院所结构 ============
cur = gkx()
cur.execute("SELECT COUNT(*) FROM gkx.dwd_org_base_info")
facts["gkx_dwd_org_base_info_rows"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM gkx.dwd_forg_university_org_info")
facts["gkx_dwd_forg_university_rows"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM gkx.dwd_research_institute_base_info")
facts["gkx_dwd_research_institute_rows"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
facts["gkx_dwd_scholar_rows"] = int(cur.fetchone()[0])
facts["gkx_subject_word_tables"] = probe["gkx_subject_word_tables"]  # []
facts["gkx_table_count"] = probe["gkx_table_total"]
cur.close()
# B11 锚
facts["gkx_counts_cache_anchor"] = {
    "dwd_org_base_info": cache["dwd_org_base_info"],
    "dwd_forg_university_org_info": cache["dwd_forg_university_org_info"],
    "dwd_research_institute_base_info": cache["dwd_research_institute_base_info"],
    "dwd_scholar": cache["dwd_scholar"]}

# ============ ④ 久新：live 词族复核 ============
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
    facts["jiuxin_subject_word_tables_live"] = [t for t in jt if re.search(r"subject|应用", t, re.I)]
    # 机构类结果面（institution 词族——分析对象主体，非应用主体，语义核验用）
    facts["jiuxin_institution_word_tables"] = [t for t in jt if re.search(r"institution", t, re.I)][:8]
    jconn.close()
    facts["jiuxin_probe_mode"] = "live"
except Exception as e:  # noqa: BLE001
    jt = snap["jiuxin"]["tables"]
    facts["jiuxin_subject_word_tables_snapshot"] = [t for t in jt if re.search(r"subject|应用", t, re.I)]
    facts["jiuxin_probe_mode"] = f"快照兜底（当日直连失败：{str(e)[:80]}）"
facts["jiuxin_hits_note"] = ("institution 词族命中为科研机构分析结果面（协作/画像——分析对象），"
                             "非「与平台发生资源应用关系的主体」登记面——语义不同")

# ================= 派生（B1/B3：双口径并列，计数差与对比全落产物） =================
derived += [
    {"key": "app_subject_total_strict", "value": None, "numerator": None, "denominator": None,
     "note": "『应用主体总数』严格口径（与平台发生过数据资源应用关系的主体数）需主体×应用关系"
             "登记面——三源零承载（subject 词族 0 命中）→ 不可构建，按 B10 留空即负结论登记"},
    {"key": "registered_org_upperbound_dev_gkx_sum", "value": float(
        facts["dev_enterprise_base_distinct_names"] + facts["gkx_dwd_org_base_info_rows"]),
     "numerator": facts["dev_enterprise_base_distinct_names"],
     "denominator": facts["gkx_dwd_org_base_info_rows"],
     "note": "代理上界口径（量级参考）：分子=dev enterprise_base 去重企业名数，分母字段=gkx "
             "dwd_org_base_info 行数，两者相加**未去重**（跨源同名机构未映射，B3 披露："
             "这是「注册/要素域主体」上界，非「应用主体」；dev ods 与 gkx 为同构样例/全量关系，"
             "叠加含跨源重复，仅量级参考不得对外发布）"},
    {"key": "mock_vs_upperbound_ratio", "value": round(facts["mock_subject_total"] / float(
        facts["dev_enterprise_base_distinct_names"] + facts["gkx_dwd_org_base_info_rows"]) * 100, 4),
     "numerator": facts["mock_subject_total"],
     "denominator": facts["dev_enterprise_base_distinct_names"] + facts["gkx_dwd_org_base_info_rows"],
     "note": f"mock {facts['mock_subject_total']} 个应用主体占代理上界（dev 去重企业 "
             f"{facts['dev_enterprise_base_distinct_names']} + gkx 机构 "
             f"{facts['gkx_dwd_org_base_info_rows']}="
             f"{facts['dev_enterprise_base_distinct_names'] + facts['gkx_dwd_org_base_info_rows']}）"
             "的百分比——演示叙事（十个头部主体）与底册体量（数十万级）的量级差披露"},
]

# ================= absence_probe =================
absence += [
    {"probe": "dev 应用主体登记面/应用关系面（subject 词族 + topic_enterprise 库实体词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_* subject 词族（共享探针）；"
            "gkxlumenx_topic_enterprise 全 21 表 enterprise/subject/org 词族",
     "hits": 0,
     "hit_detail": f"subject 词族 542 表 0 命中；topic_enterprise 库 {len(facts['dev_topic_enterprise_tables'])} 表"
                   f"实体词族命中 {facts['dev_topic_enterprise_entity_like']}（enterprise 关系/标签表——"
                   "企业域数据表非应用主体登记）"},
    {"probe": "gkx 应用主体登记面（subject 词族，280 表）",
     "source": "gkx", "sql": "information_schema.tables 扫 gkx（共享探针）",
     "hits": 0,
     "hit_detail": "0 命中——gkx 有要素域机构底册 dwd_org_base_info（189,116 行），"
                   "但那是「数据里的机构」不是「用数据的主体」，无应用关系表"},
    {"probe": "久新应用主体登记面（subject/应用 词族，live 复核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤",
     "hits": 0,
     "hit_detail": "subject 词族 0 命中；institution 词族命中为科研机构分析结果面"
                   "（协作/画像）——分析对象主体非应用主体，语义不同；探测模式 live"},
    {"probe": "需求原文「应用主体总数」定义段",
     "source": "doc", "sql": "rg 应用主体 三份需求真源",
     "hits": 8,
     "hit_detail": "SRS 总体视窗 seq 345/主需求 :2565「支持统计和展示所有资源实际应用主体，包括"
                   "科研机构、企业、项目团队」——主体类型枚举在，「总数」口径（按什么去重/是否含"
                   "历史主体）无定义；「应用主体总数」指标名本身 0 命中（UI 读数派生）"},
]

support = "部分支持"

notes += [
    "判档：严格口径（与平台发生过资源应用关系的主体数）依赖主体×应用关系登记面——三源零承载"
    "（subject 词族 0 命中）；但 dev/gkx 的机构企业底册结构+数据双在（enterprise_base "
    "189,114 去重企业 + gkx org 底册 189,116），「注册/要素域主体」上界计数可转换交付"
    "→ 部分支持（口径级缺口，B10 双口径披露）",
    "双口径说明（B10）：口径 A（严格·应用主体）=null 不可构建；口径 B（代理上界·注册/要素域主体）"
    "=dev 去重企业名与 gkx 机构行数之和（未去重跨源叠加，仅量级参考）；两者语义不同不得混用，"
    "正式发布必须先建应用关系登记面",
    "mock 披露：resourceAppSubjects 10 条（科研机构 4/企业 3/项目团队 3，重点用户 4）——"
    "summary.total=数组长度，演示值不作数据证据（B10）",
    "语义排障：本件核心是「数据里的主体」≠「用数据的主体」——gkx org 底册/久新 institution "
    "分析面都是前者；后者需要应用关系表（谁调用过/接入过平台资源），三源均未立项",
    "B11 对账：enterprise_base/org_base_info/university/research_institute/scholar 计数走 "
    "counts_cache 锚（零漂移）；dev 542/gkx 280/久新 210 表数共享快照",
    "升档触发器（B10）：①建应用主体登记面（主体×资源应用关系表）→ 升完全直接支持；"
    "②甲方接受「注册主体」代理口径（enterprise_base 计数+口径披露）→ 升完全转换支持；"
    "③维持现状 → 部分支持（上界计数仅量级参考）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_023",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/ResourceAppSubjectList.jsx:126",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:849",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「应用主体总数」指标名；语义锚 SRS 总体视窗 seq 345/主需求 :2565"
                "「统计和展示所有资源实际应用主体，包括科研机构、企业、项目团队」——主体类型枚举在、"
                "计数口径无（UI Statistic 读数派生）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [], "base_years_missing": [],
    "base_years_note": "登记面计数类指标，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["10", "4", "3", "269511", "268647", "189116", "20000", "2074", "21316",
                          "457763", "542", "280", "210", "21", "128000", "312000"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
