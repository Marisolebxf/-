#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_033 分组归集数据量 · 三源探针与复现脚本（S3-04 L4）。

含义：接入视窗·资源来源分析和详情组件（AccessSourceAnalysisDetail，承接 SRS seq 351-355）
渠道归集数据量统计卡的「业务类型」细分视图——getBizTypeBarOption 堆叠柱图（:141-163，
yAxis name='归集量' :152）：按业务类型（基础研究/产业应用/开源汇聚/政务统计）×渠道
（科研院所/企业/第三方平台）堆叠的归集量明细。组清单 l3「按质量等级＞归集量」——
组清单把明细读数位记在分组维语境（152=柱图 yAxis / 98=柱图 yAxis name）。

判档路径（口径=「业务类型（或质量等级）×渠道的归集量交叉明细」）：
- 直接承载无：归集台账+资源级明细面三源零承载（027/028 探针在案，本件互引）；
- 交叉维的两轴：渠道轴=血缘维近似（dev data_source，027 在案）；业务类型轴/质量等级轴
  零承载（028 质量词族 3 处全偏移；biz_type 词族本件独立扫）；
- mock 交叉表复算（byBizType 4 型×3 渠道）+行合计恒等校验；
- 判部分支持。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_033_out.json")
GROUP = os.path.join(BASE, "_snapshots", "_probe_s304_l4_group_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l4_collect_out.json")

group = json.load(open(GROUP, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))

facts, derived, notes, absence = {}, [], [], []

# ============ ① UI mock 交叉表复算（byBizType 4 型×3 渠道） ============
BY_BIZ = [
    {"name": "基础研究", "科研院所": 5200, "企业": 800, "第三方平台": 1200},
    {"name": "产业应用", "科研院所": 2100, "企业": 4200, "第三方平台": 1500},
    {"name": "开源汇聚", "科研院所": 900, "企业": 1100, "第三方平台": 2800},
    {"name": "政务统计", "科研院所": 600, "企业": 400, "第三方平台": 300},
]
facts["ui_mock_biztype_matrix"] = [
    [b["name"], b["科研院所"], b["企业"], b["第三方平台"]] for b in BY_BIZ]
# 行/列合计（B3 同基：同一矩阵的两种切片）
row_sums = {b["name"]: b["科研院所"] + b["企业"] + b["第三方平台"] for b in BY_BIZ}
col_sums = {c: sum(b[c] for b in BY_BIZ) for c in ("科研院所", "企业", "第三方平台")}
facts["ui_mock_biztype_row_sums"] = [[k, v] for k, v in sorted(
    row_sums.items(), key=lambda kv: (-kv[1], kv[0]))]
facts["ui_mock_biztype_col_sums"] = [[k, v] for k, v in sorted(
    col_sums.items(), key=lambda kv: (-kv[1], kv[0]))]
facts["ui_mock_biztype_grand_total"] = sum(row_sums.values())

# ============ ② dev：业务类型/质量等级词族独立扫（B4 本件留证） ============
import pymysql

DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="information_schema", charset="utf8mb4",
           connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()
c.execute(
    "SELECT table_schema, table_name, column_name FROM information_schema.columns "
    "WHERE table_schema LIKE 'gkxlumenx%' AND column_name REGEXP 'biz_type|business_type'")
facts["dev_biztype_like_columns"] = sorted(f"{a}.{b}.{col}" for a, b, col in c.fetchall())
d.close()

# ============ ③ 组探针/族探针快照复用 ============
facts["dev_enterprise_base_rows"] = group["dev"]["enterprise_base_rows"]
facts["dev_enterprise_base_data_source_dist"] = group["dev"][
    "enterprise_base_data_source_dist"]
facts["dev_quality_like_columns"] = group["dev"]["quality_like_columns"]
facts["gkx_table_count"] = probe["gkx_table_count"]
facts["gkx_collect_like_tables"] = probe["gkx_collect_like_tables"]
facts["jiuxin_table_count"] = probe["jiuxin_table_count"]
facts["jiuxin_status"] = probe["jiuxin_status"]
facts["jiuxin_collect_like_tables"] = probe["jiuxin_collect_like_tables"]

# 交叉表行列合计恒等校验（B3 同基：Σ行合计 = Σ列合计 = 总计）
derived.append({
    "key": "ui_mock_biztype_rowcol_sum_identity",
    "value": sum(row_sums.values()),
    "numerator": sum(col_sums.values()),
    "denominator": sum(row_sums.values()),
    "note": "分子=列合计之和（Σ渠道 21,100）；分母=行合计之和（Σ业务类型 21,100）——同一 "
            "4×3 矩阵的两种切片求和恒等（交叉表完备性校验）。对账披露：矩阵总计 21,100 "
            "vs mock channels 三渠道 volume 之和 27,740（差 6,640）——mock 内部 channels "
            "与 byBizType 两面不对账（渠道列合计 8,800/6,500/5,800 vs channels volume "
            "12,580/8,920/6,240）；且高等院校 4,120/政府部门 1,810 两渠道未入柱图（柱图"
            "仅取前三渠道）——演示值不作数据证据",
})
# dev 血缘维分组（明细端交付形态的分组基面）
grp = facts["dev_enterprise_base_data_source_dist"]
derived.append({
    "key": "dev_group_by_data_source_volume_sum",
    "value": sum(v for _, v in grp),
    "numerator": sum(v for _, v in grp),
    "denominator": facts["dev_enterprise_base_rows"],
    "note": "分子=按 data_source 分组的 5 组行数合计；分母=enterprise_base 总行数——恒等 "
            "269,511（与 027/028 派生键同值，族内 B11 对账）；血缘分组是明细端交叉维"
            "『渠道轴』的最近邻工程面",
})
# 指标负结论登记（B10）
derived.append({
    "key": "biztype_channel_cross_volume",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『业务类型×渠道的归集量交叉明细（或按质量等级>归集量分组）』——交叉两轴"
            "（业务类型/质量等级 × 正式渠道 taxonomy）三源零承载（biz_type 词族 0 命中、"
            "质量词族 3 处全偏移、渠道轴 taxonomy 分叉）；按 B10 留空",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 业务类型轴（biz_type/business_type 词族）",
     "source": "dev",
     "sql": "information_schema.columns 扫 gkxlumenx_*（542 表）——本件独立复跑",
     "hits": 0,
     "hit_detail": "命中 []——0 处列承载；『业务类型』分组轴在 dev 无列级承载"
                   "（mock byBizType 的四型：基础研究/产业应用/开源汇聚/政务统计，"
                   "库内无同构编目）",
     },
    {"probe": "dev 质量等级轴 + 资源级明细面",
     "source": "dev",
     "sql": "质量词族列扫（组探针）+台账词族（族探针，027/028 在案）",
     "hits": 3,
     "hit_detail": "质量词族 3 处列全语义偏移（score_level 评分档/time_quality 时间质量/"
                   "company_quality 台企列，028 在案）；组清单 l3『按质量等级＞归集量』的"
                   "质量分组轴零承载；资源级明细面零承载（028 §3.3 同证）",
     },
    {"probe": "gkx 业务类型/质量等级轴 + 明细面",
     "source": "gkx",
     "sql": "280 表词族扫（族探针）+dwd_org_base_info 列清单（组探针）",
     "hits": 1,
     "hit_detail": "台账词族命中 dwd_org_changerecord_info（语义排除，族探针）；280 表为"
                   "要素明细库，无『业务类型×渠道×量』交叉编目；dwd_org_base_info 38 列"
                   "无 biz_type/质量列",
     },
    {"probe": "久新业务类型/质量等级轴 + 明细面",
     "source": "jiuxin",
     "sql": "SHOW TABLES（live，211 表）词族扫（族探针）",
     "hits": 0,
     "hit_detail": "命中 []——211 张 ads_* 全为分析结果面（学科/人才/专利/项目/技术），"
                   "无业务类型×渠道归集交叉面",
     },
    {"probe": "需求原文「分组归集数据量/业务类型细分」定义段",
     "source": "doc",
     "sql": "rg 分组归集数据量/业务类型 三份需求真源 + SRS 接入视窗.md",
     "hits": 1,
     "hit_detail": "「分组归集数据量」0 命中；细分维语义叶=seq 351『支持按时间、业务类型、"
                   "来源类别进行细分』（SRS :61-70/主需求 :2607）——『业务类型』作为细分"
                   "维被需求明列（举例式），但其 taxonomy（分几型、型名）与量纲无定义；"
                   "UI byBizType 四型为演示约定",
     },
]

support = "部分支持"

notes += [
    "判档：需求语义=『业务类型（或质量等级）×渠道的归集量交叉明细』；交叉两轴零承载"
    "（biz_type 词族本件独立扫 0 命中/质量词族 3 处全偏移/渠道轴 taxonomy 分叉）→ 需求"
    "交叉不可直算；血缘维分组（5 组恒等 269,511）+ 存量读数可交付 → 部分支持",
    f"mock 交叉复算：byBizType 4 型×3 渠道矩阵，行合计 {facts['ui_mock_biztype_row_sums']}"
    f"，列合计 {facts['ui_mock_biztype_col_sums']}，总计 {facts['ui_mock_biztype_grand_total']}"
    "——行/列切片恒等（派生键）；柱图仅取前三渠道（科研院所/企业/第三方平台），高等院校"
    "4,120+政府部门 1,810 未入图（覆盖面披露）；演示值不作数据证据",
    f"业务类型轴独立扫：biz_type/business_type 词族 dev 542 表 0 命中"
    f"（{facts['dev_biztype_like_columns']}）——四型 taxonomy 无库内编目",
    "三件套恒等：033（交叉明细）Σ=028（分组合计）Σ=027（总量）——数学恒等；本件是明细端"
    "（交叉矩阵），修复依赖最深（两轴编目+明细面）",
    "B5 确定性：矩阵复算行/列合计按值降序+键名字典序双键；词族 sorted()",
    "B11 对账：data_source 5 组/enterprise_base 269,511 与 027/028 同快照同值；族探针表数"
    "（dev 542/gkx 280/久新 211）族内一致",
    "升档触发器（B10）：①建资源级明细面+业务类型字典+渠道字典（交叉两轴编目）→ 交叉明细"
    "直查升完全直接支持（族级并项，seq 351/352/354 五叶受益）；②甲方裁明细维=血缘轴单维"
    "（放弃交叉）→ 完全转换支持（本件交付形态退化为分组明细单维）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_033",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:152",
        "repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:141",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:115",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "「分组归集数据量」指标名三份真源 0 命中——UI 派生读数；细分维语义叶=seq 351"
                "『支持按时间、业务类型、来源类别进行细分』（业务类型被需求明列为细分维，"
                "taxonomy 与量纲无定义）；组清单 l3『按质量等级＞归集量』的分组位在 UI 由"
                "分组下拉（GROUP_OPTIONS qualityLevel）承接，质量轴零承载（028 在案）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件无基期年份依赖（交叉明细读数；mock 时间细分位属 002 族）",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["269511", "189115", "21100", "27740", "6640", "4120",
                          "1810", "12580", "8920", "6240", "8800"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
