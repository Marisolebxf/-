#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATAIN_002 归集数据量统计 · 三源探针与复现脚本（S3-04 L4）。

含义：接入视窗·资源接入情况总览的「归集数据量统计」卡（需求明列叶 SRS seq 349）——
「自动归集并更新接入数据的总量与明细，支持按类型、来源或时间周期进行细分统计」。
UI（AccessWindow.jsx:490 实查确认）：Card title="归集数据量统计"，月度/周度/日度
Radio 切换 + getAccessTrendOption 折线（新增资源/更新资源双序列）；mock 源
mockData.js:41-68 resourceAccessTrend（月度 12 点 450-920 / 320-780 等演示值）。

判档路径（口径=「接入数据总量与明细，按类型/来源/时间细分」）：
- 直接承载无：三源无资源接入流水台账——归集数据量登记（资源×量×时间×来源）不存在
  （DATAOV_002/DATAIN_001/003 族内已证词族 0 命中，本件独立复跑留证）；
- 转换承载（总量口径=对象级行数三源双在）：dev enterprise_base 269,511（+批次面
  2026-08-27:188,767）、gkx 11 表主量面（专利 2,939,895 领衔）、久新 210 表合计
  182,707,016——「平台有多少数据」可数；「接入数据的总量」的动作语义须台账；
- 时间细分代理：dev update_time 月维分布（2026-08:269,163 / 2026-09:348——仅两月，
  批次式非逐月）；来源/类型细分轴零承载（DATAIN_003 已证标签轴空载，本件登记互引）；
- 判部分支持。
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATAIN_002_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l4_collect_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")

probe = json.load(open(PROBE, encoding="utf-8"))
snap = json.load(open(SNAP, encoding="utf-8"))

facts, derived, notes, absence = {}, [], [], []

import pymysql

# ============ ① dev：enterprise_base 行数 + 月维分布（时间细分代理）+ 台账词族独立复跑 ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4",
           connect_timeout=10, read_timeout=120)
d = pymysql.connect(**DEV)
c = d.cursor()
c.execute("SELECT COUNT(*) FROM enterprise_base")
facts["dev_enterprise_base_rows"] = int(c.fetchone()[0])
# 月维分布（新增/更新双序列的最近邻代理：update_time 按月；B9 DATE_FORMAT 归一）
c.execute(
    "SELECT DATE_FORMAT(update_time,'%Y-%m') m, COUNT(*) FROM enterprise_base "
    "GROUP BY m ORDER BY m")
facts["dev_enterprise_update_month_dist"] = [[a, int(b)] for a, b in c.fetchall()]
# 台账词族独立复跑（B4 本件留证，不抄族内结论）
c.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' "
    "AND table_name REGEXP 'access_log|access_history|resource_access|ingest|collect'")
facts["dev_access_registry_tables"] = sorted(f"{a}.{b}" for a, b in c.fetchall())
d.close()

# ============ ② gkx：主量面（探针快照复用，经 _gkxdb.py） ============
facts["gkx_main_table_rows"] = probe["gkx_main_table_rows"]
facts["gkx_table_count"] = probe["gkx_table_count"]
rc = snap["jiuxin"]["rowcounts"]

# ============ ③ 久新：探针快照（live 211 表）+ 210 表合计 ============
facts["jiuxin_status"] = probe["jiuxin_status"]
facts["jiuxin_table_count"] = probe["jiuxin_table_count"]
facts["jiuxin_main_table_rows"] = probe["jiuxin_main_table_rows"]
derived.append({
    "key": "jiuxin_all_ads_rows_sum_210tables",
    "value": sum(rc.values()),
    "numerator": sum(rc.values()),
    "denominator": snap["jiuxin"]["table_count"],
    "note": "分子=共享快照 210 张 ads_* 表逐表行数之和；分母=表数（210，2026-11-01 快照日）；"
            "久新库对象级总量（与 DATATHM_039 同键同值，族内 B11 对账）",
})

# ================= 指标负结论登记（B10） =================
derived.append({
    "key": "collected_data_volume_total",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『接入数据的归集总量（动作口径：新增/更新资源序列）』三源无接入台账承载"
            "（词族 0 命中，本件独立复跑）；本件交付存量口径总量（三源对象级行数）与时间"
            "细分代理（update_time 月维 2 点），语义=库内数据资产存量≠接入动作量；"
            "按 B10 留空即负结论登记",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev 资源接入流水台账（access_log/access_history/resource_access/ingest/collect 词族）",
     "source": "dev",
     "sql": "information_schema.tables 扫 gkxlumenx_*（542 表）——本件独立复跑",
     "hits": len(facts["dev_access_registry_tables"]),
     "hit_detail": f"命中 {facts['dev_access_registry_tables']}——0 张接入流水表（与 "
                   "DATAOV_002/DATAIN_001/003 族内词族同结论，独立留证）；无『资源×量×时间×"
                   "来源』归集登记，接入动作量不可直算",
     },
    {"probe": "gkx 接入/归集台账（collect/ingest/access/resource/dataset/volume/record 词族）",
     "source": "gkx",
     "sql": "SHOW TABLES FROM gkx（280 表）词族扫（L4 族探针）",
     "hits": 1,
     "hit_detail": "命中 ['dwd_org_changerecord_info']——企业变更记录明细（名近 record 而义为"
                   "变更流水），语义排除；280 表为要素明细库无接入台账",
     },
    {"probe": "久新接入/归集台账（同词族）",
     "source": "jiuxin",
     "sql": "SHOW TABLES（live，211 表，2026-11-01 探测日）词族扫（L4 族探针）",
     "hits": 0,
     "hit_detail": "命中 []——211 张 ads_* 全部为分析结果面；快照管理形态（DATAIN_003 已证"
                   "metrics_as_of_date 单日一期）无逐期接入记录",
     },
    {"probe": "需求原文「归集数据量统计」定义段",
     "source": "doc",
     "sql": "rg 归集数据量统计 三份需求真源",
     "hits": 1,
     "hit_detail": "SRS 接入视窗.md seq 349（excel_row 352）+主需求 :2593-2595（1.1.1.1.4."
                   "4.2.1.3）：『自动归集并更新接入数据的总量与明细，支持按类型、来源或时间"
                   "周期进行细分统计』——功能行为在；『总量』的度量对象（记录数/资源数/体量）"
                   "与『明细』的粒度无定义；UI 折线双序列（新增/更新资源）为 mock 演示形态",
     },
]

support = "部分支持"

notes += [
    "判档：需求语义=『接入数据总量与明细（类型/来源/时间三维细分）』；接入台账三源零承载"
    "（独立复跑+族探针双证）→ 动作口径不可直算；存量口径总量（三源对象级行数）+ 时间细分"
    "代理（update_time 月维）可交付 → 部分支持",
    f"存量口径读数：dev enterprise_base {facts['dev_enterprise_base_rows']}（全库估算 "
    "9,855,673 见 DATATHM_039 键）、gkx 11 表（专利 2,939,895 领衔）、久新 210 表合计 "
    "182,707,016（快照求和）——『平台有多少数据』三源可数",
    f"时间细分代理：enterprise_base.update_time 月维分布 {facts['dev_enterprise_update_month_dist']}"
    "——仅 2026-08/2026-09 两点（三大批次日集中 8 月，DATAIN_001 同法），批次式非逐月接入"
    "节奏；mock 月度 12 点（450-920）为演示形态，库内无同构逐月序列",
    "来源/类型细分轴：gkx table_data_source 标签轴实测空载（DATAIN_003 已证：dwd_scholar "
    "单标签/dwd_zh_paper 100% 无效/dwd_patent 采样全 null）——本件登记互引不重复展开；"
    "类型轴（资源类型分类）三源无资源编目（DATAOV_001 资产目录缺口同根）",
    "mock 披露：AccessWindow.jsx:490 归集数据量统计卡消费 resourceAccessTrend（月度新增 "
    "450-920/更新 320-780、周度 8 点、日度 7 点，mockData.js:41-68）——演示值不作数据证据（B10）",
    "跨窗对齐：本件与 DATATHM_039（数据资源数据量·条）跨窗同根——本件挂接入动作面"
    "（seq 349 总览叶『归集』语义）、039 挂资源存量面（BigDataCenterDetail 记录数）；"
    "两件同缺资源登记/台账面，对象级读数共用 L4 族探针（互引登记；台账+登记面并项建议"
    "见 MD §1.7）",
    "B9 规避：DATE_FORMAT 月维归一（无零日期比较）；久新合计快照日口径标注",
    "B11 对账：dev 542/gkx 280/久新 211（live）与族探针一致；jiuxin 合计键与 DATATHM_039 "
    "同值 182,707,016；enterprise_base 269,511 与 DATAIN_001/003/DATATHM_015 族内一致",
    "升档触发器（B10）：①建接入台账（资源×量×时间×来源流水）→ 动作口径直查升完全直接"
    "支持（与 DATAOV_002/DATAIN_001/003 触发器①共用）；②甲方裁总量口径=库内对象级存量 → "
    "完全转换支持（本件交付形态即该口径）",
]

out = {
    "metric_id": "M_SCIUI_DATAIN_002",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:490",
        "repos/demo-ui-science/src/pages/data-resources/AccessWindow.jsx:493",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:41",
    ],
    "requirement_trace": {
        "named_in_srs": True,
        "note": "SRS《02-科技信息展示系统/科技数据资源/接入视窗.md》seq 349（excel_row 352）+"
                "主需求 :2593-2595（1.1.1.1.4.4.2.1.3 归集数据量统计）需求明列叶：『自动归集"
                "并更新接入数据的总量与明细，支持按类型、来源或时间周期进行细分统计』——"
                "功能在、度量口径无；核增需求与算法库 0 命中",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件时间面为月维代理（2026-08/2026-09 两点），无基期年份依赖",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["269511", "188767", "40396", "40000", "2939895", "182707016", "542",
                          "280", "211", "210", "450", "920"][:12]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
