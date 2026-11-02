#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_POLCMP_053 跨部门协同率 · 三源探针与复现脚本（S3-03 Lane 4）。

含义：政策分析评价（DS-11 政策画像卡）metrics 行——「跨部门协同率 68%」（policyData.js:2185）。
export 自认「计算方法需要立项调研后才能确定」。权威形态：政策文献量化的联合发文口径
（R1 环境治理 976 份联合行文；R4 京津冀/长三角「多部门联合发布政策数量」横向协同测度）。
口径问题：「跨部门」以发文机关多部门联合为准（横向主体协同），非执行侧数据共享率。

三源实况（全部实探，2026-11-01）：
- gkx：dwd_policy_base.ministry 19,989 非空；顿号分隔联合署名 336 行——但 DISTINCT 仅
  1 个值「北京市科学技术委员会、中关村科技园区管委会」（×336）；斜杠分隔 118 行待细分。
  可算面：联合发文代理率极小且形态单一（同市两部门），无部级多部门联合样本。
- dev：policy_time_series_indicator.dept_distribution 列在但表 0 行；政策族 33 表中
  机关侧仅 policy_base_info.publish_organization（39989 非空，同步自 gkx ministry）。
- 久新：210 张 ads_* 扫 policy/dept/coord/collab/joint 命中面语义排除（无联合发文承载）。
判档：部分支持——结构侧 ministry/publish_organization 列在且有量（19,989/39,989 非空），
联合发文口径可算但当前联合署名仅 336 行（1.68%）且单值坍缩，分母侧「应协同政策集」
口径未定义；联合发文率可作代理读数交付（披露口径限制）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_POLCMP_053_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []


def _ser(v):
    from decimal import Decimal
    import datetime as _dt
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (_dt.date, _dt.datetime)):
        return str(v)
    return v


# ============ ① gkx：ministry 联合署名面（联合发文口径的可算侧） ============
gcur = gkx()
def qg(sql):
    gcur.execute(sql)
    return gcur.fetchall()

facts["gkx_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_policy_base")[0][0])
# ministry 覆盖面
facts["gkx_ministry_nonnull"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE ministry IS NOT NULL "
    "AND ministry != '' AND ministry != 'null'")[0][0])
facts["gkx_ministry_null_literal"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE ministry = 'null'")[0][0])
# 分隔符全形态（顿号/斜杠/空格联合）
facts["gkx_ministry_dunhao_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE ministry LIKE '%、%'")[0][0])
facts["gkx_ministry_slash_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE ministry LIKE '%/%'")[0][0])
# 顿号联合的值形态（是否多值分布）
rows = qg("SELECT ministry, COUNT(*) FROM gkx.dwd_policy_base WHERE ministry LIKE '%、%' "
          "GROUP BY ministry ORDER BY 2 DESC LIMIT 10")
facts["gkx_ministry_dunhao_distinct"] = [[r[0], int(r[1])] for r in rows]
# 斜杠样本（语义判别：机关联合还是文号/路径）
rows = qg("SELECT DISTINCT ministry FROM gkx.dwd_policy_base WHERE ministry LIKE '%/%' "
          "AND ministry NOT LIKE '%、%' LIMIT 8")
facts["gkx_ministry_slash_sample"] = [r[0][:80] for r in rows]
# 部门词表计数（多部门词共现——机关名级联合的补充判定）
DEPTS = ["科学技术", "财政", "税务", "发展改革", "工业和信息化", "人力资源", "教育",
         "商务", "市场监管", "住房城乡建设", "农业农村", "卫生健康", "国资委", "人民银行",
         "知识产权", "自然科学基金"]
cases = " + ".join("(CASE WHEN ministry LIKE '%%%s%%' THEN 1 ELSE 0 END)" % d for d in DEPTS)
sql = ("SELECT dept_hits, COUNT(*) FROM (SELECT (" + cases + ") AS dept_hits "
       "FROM gkx.dwd_policy_base WHERE ministry IS NOT NULL AND ministry != '' "
       "AND ministry != 'null') t GROUP BY dept_hits ORDER BY dept_hits")
facts["gkx_ministry_dept_hits_dist"] = [[int(r[0]), int(r[1])] for r in qg(sql)]
# 两层融合联合发文（UNION 去重——两集合交集实测 1 行）
n_comb = int(qg(
    "SELECT COUNT(*) FROM (SELECT id FROM gkx.dwd_policy_base WHERE ministry LIKE '%、%' "
    "UNION SELECT id FROM gkx.dwd_policy_base WHERE title REGEXP "
    "'(厅|委员会|局)(广东|北京|上海|浙江|江苏|福建|四川|陕西|山东|河南|湖北|湖南|安徽)') u")[0][0])
facts["gkx_joint_publish_combined_rows"] = n_comb
facts["gkx_joint_publish_overlap_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE ministry LIKE '%、%' AND title REGEXP "
    "'(厅|委员会|局)(广东|北京|上海|浙江|江苏|福建|四川|陕西|山东|河南|湖北|湖南|安徽)'")[0][0])
rows = qg("SELECT CASE WHEN CHAR_LENGTH(ministry)<=10 THEN 'a<=10' "
          "WHEN CHAR_LENGTH(ministry)<=20 THEN 'b11-20' "
          "WHEN CHAR_LENGTH(ministry)<=40 THEN 'c21-40' ELSE 'd>40' END len_band, COUNT(*) "
          "FROM gkx.dwd_policy_base WHERE ministry IS NOT NULL AND ministry != '' "
          "AND ministry != 'null' GROUP BY len_band ORDER BY len_band")
facts["gkx_ministry_len_band"] = [[r[0], int(r[1])] for r in rows]
# title 层多机关连写探针（「厅」后紧跟「厅/委员会/局」无分隔符——联合发文的标题证据）
facts["gkx_title_concat_org_rows"] = int(qg(
    "SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE title REGEXP "
    "'(厅|委员会|局)(广东|北京|上海|浙江|江苏|福建|四川|陕西|山东|河南|湖北|湖南|安徽)"
    "'")[0][0])
rows = qg("SELECT title FROM gkx.dwd_policy_base WHERE title REGEXP "
          "'(厅|委员会|局)(广东|北京|上海|浙江|江苏|福建|四川|陕西|山东|河南|湖北|湖南|安徽)' "
          "LIMIT 5")
facts["gkx_title_concat_org_sample"] = [r[0][:100] for r in rows]
# 文本面「协同」叙述面（政策自述协同语言）
TF = ("CONCAT_WS(' ',IFNULL(title,''),IFNULL(theme,''),IFNULL(content,''),"
      "IFNULL(keywords,''),IFNULL(keypoints,''))")
facts["gkx_text_xietong_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TF} LIKE '%协同%'")[0][0])
facts["gkx_text_xietong_dept_rows"] = int(qg(
    f"SELECT COUNT(*) FROM gkx.dwd_policy_base WHERE {TF} LIKE '%部门间%' OR "
    f"{TF} LIKE '%跨部门%'")[0][0])
# 全球面（域外多机构署名形态对照）
facts["gkx_global_policy_rows"] = int(qg("SELECT COUNT(*) FROM gkx.dwd_global_policy_base")[0][0])
gcur.close()

# ============ ② dev：机关列同构 + 部门分布落位表 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=120)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute("SELECT COUNT(*) FROM policy_base_info WHERE publish_organization IS NOT NULL "
             "AND publish_organization != '' AND publish_organization != 'null'")
facts["dev_publish_organization_nonnull"] = int(lcur.fetchall()[0][0])
lcur.execute("SELECT COUNT(*) FROM policy_base_info WHERE publish_organization LIKE '%、%'")
facts["dev_publish_organization_dunhao_rows"] = int(lcur.fetchall()[0][0])
# 部门分布落位表（时间序列指标表含 dept_distribution 列）
lcur.execute("SHOW COLUMNS FROM policy_time_series_indicator")
facts["dev_policy_time_series_indicator_cols"] = [r[0] for r in lcur.fetchall()]
lcur.execute("SELECT COUNT(*) FROM policy_time_series_indicator")
facts["dev_policy_time_series_indicator_rows"] = int(lcur.fetchone()[0])
lconn.close()

# ============ ③ 久新：政策/部门协同面 ============
JX = dict(host="47.93.119.170", port=29030, user="test2",
          password="m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka",
          database="gkx_technology_analysis_dev",
          connect_timeout=10, read_timeout=300)
try:
    jconn = pymysql.connect(**JX)
    jcur = jconn.cursor()
    jcur.execute("SHOW TABLES")
    jx_tables = sorted(r[0] for r in jcur.fetchall())
    facts["jiuxin_table_count"] = len(jx_tables)
    facts["jiuxin_policy_dept_like_tables"] = [t for t in jx_tables if re.search(
        r"policy|dept|coord|collab|joint|syner|coop", t, re.I)]
    jconn.close()
except Exception as e:  # noqa: BLE001
    facts["jiuxin_unreachable"] = str(e)[:120]

# ============ 派生与登记 ============
# 联合发文代理率（口径 A：顿号分隔联合署名 / ministry 非空全行——同基相除同表同列）
derived.append({
    "key": "joint_publish_share_dunhao_pct",
    "value": round(facts["gkx_ministry_dunhao_rows"] / facts["gkx_ministry_nonnull"] * 100, 3),
    "numerator": facts["gkx_ministry_dunhao_rows"],
    "denominator": facts["gkx_ministry_nonnull"],
    "note": "口径 A 联合发文代理率：分子=顿号分隔联合署名行，分母=ministry 非空行"
            "（同表同列同 WHERE）；代理读数非指标本体——「应协同政策集」分母口径未定义，"
            "且顿号联合 DISTINCT 仅 1 值（北京市科委+中关村管委会 ×336）形态单值坍缩",
})
# 负结论登记键（结构化协同率不可直查）
derived.append({
    "key": "joint_publish_proxy_combined_pct",
    "value": round(facts["gkx_joint_publish_combined_rows"]
                   / facts["gkx_ministry_nonnull"] * 100, 3),
    "numerator": facts["gkx_joint_publish_combined_rows"],
    "denominator": facts["gkx_ministry_nonnull"],
    "note": "两层融合联合发文代理率（UNION 去重口径）：分子=顿号联合署名∪title 层机关"
            "连写去重计数（两集合交集 1 行），分母=ministry 非空行（同表同 WHERE）；"
            "title 正则保守（仅 13 省份词表），读数语义是联合发文占比非协同率本体",
})

absence = [
    {"probe": "gkx 部门协同关系面",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）扫 dept/coord/collab/joint/syner/coop + "
            "dwd_policy_base 33 列扫协同类列",
     "hits": 0,
     "hit_detail": "280 表无部门协同关系表；33 列无协同列——唯一机关承载是 ministry"
                   "（发布机关名文本列，19,989 非空）"},
    {"probe": "dev 部门分布落位表",
     "source": "dev",
     "sql": "SHOW COLUMNS + COUNT：policy_time_series_indicator（含 dept_distribution 列）",
     "hits": 0,
     "hit_detail": "dept_distribution 列在（部门分布的时间序列落位设计）但全表 0 行——"
                   "结构在数据空；政策族 33 表无联合发文/会签承载表"},
    {"probe": "久新政策/部门协同面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（实测 210 张，探测日 2026-11-01）扫 policy/dept/coord/collab/"
            "joint/syner/coop",
     "hits": 0,
     "hit_detail": "命中面为政策证据/年度计数/合作类表（talent_institution_cooperation"
                   "是人才-机构合作非部门协同；institution cooperation 类同），"
                   "无一张是政府部门间协同关系承载"},
    {"probe": "需求文档定义",
     "source": "doc",
     "sql": "rg 跨部门协同/协同率 主需求 + SRS 政策族四文件 + 核增 17 叶 + 算法库",
     "hits": 0,
     "hit_detail": "「跨部门协同」仅现于主需求非政策域语境（:2435 引进成本导出便利/"
                   ":2625 数据来源明细导出/:2879 日志导出/:3267 成果筛查/:3465 载体协同"
                   "治理——均为「便于跨部门协同使用」的导出功能语，非政策域协同率指标）；"
                   "「协同率」三源 0 命中；export 自认计算方法需立项调研"},
]

support = "部分支持"

notes = [
    "判档：结构侧有量（ministry/publish_organization 列在、19,989/39,989 非空）但语义"
    "不足——联合发文口径可算而当前联合署名面单值坍缩（顿号 336 行全部是同一值「北京市"
    "科学技术委员会、中关村科技园区管委会」，1.682% 且非部级跨部门形态）；「应协同"
    "政策集」分母口径未定义；执行侧协同面（会签/数据共享）三源全无。口径可裁剪+输入面"
    "有缺陷 → 部分支持",
    "权威口径参照（R1/R4 核验在案）：联合发文是学界测度部际协同的标准观测窗——武汉大学"
    "环境治理研究以 976 份中央部门联合行文policy为样本（两部门联合 45%/两部门以上 55%）；"
    "京津冀/长三角创新政策研究以「多部门联合发布政策数量」为横向主体协同指标（京 46/"
    "津 38/冀 41；沪 91/苏 53/浙 49/皖 56）。对照可见本库 336 行单值形态离该口径的"
    "数据要求差距极大（联合署名解析需先做机关名切分与规范化）",
    "同名连写形态的修正证据：ministry 列长度分布三段（≤10 字 16,309 / 11-20 字 3,344 / "
    "21-40 字 336）——21-40 字段恰是顿号联合值；「广东省科学技术厅广东省发展和改革委员会…」"
    "五机关连写形态实际出现在 title 层（本件 title 探针在案），ministry 层连写 0 行。"
    "结论：ministry 列以单机关短值为主（≤20 字占 98.3%），多机关署名信息分散在 ministry "
    "顿号（336 行单值）与 title 连写两层——联合发文的完整计数需两层数据融合（机关名切分"
    "+ title 回退解析），工程量非平凡",
    "dev publish_organization 与 gkx ministry 同步同构（顿号 336 行一致）——两库同源"
    "同步（Lane6 r2 探针共证）；policy_time_series_indicator.dept_distribution 列在"
    "但 0 行，是「规划过落位、从未写入」形态（与 POLCMP_008 的 policy_public_opinion"
    "同族证据）",
    "UI mock 披露：policyData.js:2185「跨部门协同率 68%」是 DS-11 政策画像卡 metrics "
    "行 mock 常量（演示值不参与支持度结论）——68% 的量级远超库内联合署名面（1.682%），"
    "mock 值更接近「部门间数据共享率」类政务系统口径（R2 辽宁框架的跨部门数据共享率"
    "指标），恰说明 UI 语义与联合发文学术语境存在口径歧义，须甲方裁定",
    "升档触发器（B10）：①机关名切分与规范化工程（词表+边界识别）落地 → 联合发文口径"
    "闭合，升完全转换支持（ministry 19,989 行原料在）；②若甲方裁定口径为执行侧"
    "「跨部门数据共享率」→ 需政务共享平台日志对接（外部源），单独立项；③若裁定为"
    "「会签部门数/政策」→ 需会签流水，三源无承载",
]

out = {
    "metric_id": "M_SCIUI_POLCMP_053",
    "batch": "S3-03",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2185",
        "repos/demo-ui-science/src/pages/policy-tracking/policyData.js:2178",
        "repos/demo-ui-science/src/pages/policy-tracking/analysis/PortraitTrio.jsx:40",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求真源无「跨部门协同率」指标名；主需求 5 处「跨部门协同」均为"
                "非政策域导出功能语；UI DS-11 政策画像卡 metrics 行是唯一实证；"
                "export 自认计算方法需立项调研",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "联合署名面无年度序列计算（口径未闭合）；叙述面年度分布无计算意义",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": [str(facts.get("gkx_ministry_nonnull", "")),
                          str(facts.get("gkx_ministry_dunhao_rows", "")),
                          str(facts.get("gkx_ministry_slash_rows", "")),
                          str(facts.get("gkx_text_xietong_rows", "")),
                          str(facts.get("jiuxin_table_count", "")),
                          "68", "336"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("written:", OUT)
