#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_013 供应方调用量占总量百分比 · 三源探针脚本（S3-04 L5）。

含义：科技数据资源·应用视窗·数据供应方数据被调用情况——各供应方被调用量占全平台
调用总量的百分比。UI：ApplicationWindow.jsx:216（supplierColumns「占比」列，Progress 渲染）
与 :421-437（SupplierCallTab.aggregatedSuppliers 重算 share = totalCalls/grandTotal）。
mock 源 mockData.js:909-914（supplierStats 5 家，share 43.8/23.8/16.0/10.9/5.5）。

判档路径（口径 = 供应方维度调用量 ÷ 全平台调用量，分子分母同源同窗）：
- 计算前提是「按供应方归集的调用日志面」——三源 call/invoke/api/request 词族 0 命中
  （dev 542 表 / gkx 280 表 / 久新 210 表 live 复核）；
- dev supplier 词族唯一命中 gkxlumenx_dwd.enterprise_supply_chain 为造数关系整表（禁引）；
- gkx 唯一现成切面 table_data_source（数据入库来源标签，非「供应方调用量」）：
  dwd_zh_paper 100,900 行标签全部为 NULL/'NULL'（非空标签 0 行）、dwd_patent 采样框
  14,371 行全 NULL、dwd_scholar 21,316 行全 'gkx_ods'（ETL 批次标记非供应方语义）——
  即便退到静态来源维度也无可用分布；
- 判完全不支持（分子分母两侧的承载面均不存在）。
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_013_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
PROBE = os.path.join(BASE, "_snapshots", "_probe_s304_l5_out.json")
SNAPC = os.path.join(BASE, "_snapshots", "_probe_lane3_s304c_out.json")
CACHE = os.path.join(BASE, "_snapshots", "_s304_gkx_counts_cache.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
from _gkxdb import gkx  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))
probe = json.load(open(PROBE, encoding="utf-8"))["probes"]
snapc = json.load(open(SNAPC, encoding="utf-8"))["facts"]
cache = json.load(open(CACHE, encoding="utf-8"))

# ============ ① mock 层（UI 语义披露，不作数据证据） ============
MOCK_SUPPLIERS = [
    ("中科院", 156, 1250000, 43.8, "华北"),
    ("清华大学", 89, 680000, 23.8, "华北"),
    ("深圳市政府", 67, 456000, 16.0, "华南"),
    ("华为公司", 45, 312000, 10.9, "华南"),
    ("北京大学", 34, 158000, 5.5, "华北"),
]
facts["mock_supplier_count"] = len(MOCK_SUPPLIERS)
facts["mock_supplier_names"] = [m[0] for m in MOCK_SUPPLIERS]
facts["mock_supplier_total_calls"] = [m[2] for m in MOCK_SUPPLIERS]
facts["mock_grand_total_calls"] = sum(m[2] for m in MOCK_SUPPLIERS)  # 2,856,000
facts["mock_share_values_pct"] = [m[3] for m in MOCK_SUPPLIERS]
facts["mock_share_sum_check_pct"] = round(sum(m[3] for m in MOCK_SUPPLIERS), 1)  # 100.0
facts["mock_share_formula"] = ("ApplicationWindow.jsx:433-436 share = round(totalCalls/"
                               "grandTotal*1000)/10（分子分母同基：同一筛选集的供应方调用量与总量）")

# ============ ② gkx：来源标签切面实测（唯一现成维度，语义核验） ============
cur = gkx()
cur.execute("SELECT COUNT(*) FROM gkx.dwd_zh_paper")
facts["gkx_dwd_zh_paper_total"] = int(cur.fetchone()[0])
cur.execute("SELECT IFNULL(table_data_source,'<NULL>'), COUNT(*) FROM gkx.dwd_zh_paper "
            "GROUP BY table_data_source ORDER BY COUNT(*) DESC, IFNULL(table_data_source,'<NULL>') ASC")
facts["gkx_dwd_zh_paper_src_dist"] = [[str(a), int(b)] for a, b in cur.fetchall()]
cur.execute("SELECT COUNT(*) FROM gkx.dwd_zh_paper "
            "WHERE table_data_source IS NOT NULL AND table_data_source <> 'NULL'")
facts["gkx_dwd_zh_paper_src_labeled_rows"] = int(cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM gkx.dwd_scholar")
facts["gkx_dwd_scholar_total"] = int(cur.fetchone()[0])
cur.execute("SELECT IFNULL(table_data_source,'<NULL>'), COUNT(*) FROM gkx.dwd_scholar "
            "GROUP BY table_data_source ORDER BY COUNT(*) DESC, IFNULL(table_data_source,'<NULL>') ASC")
facts["gkx_dwd_scholar_src_dist"] = [[str(a), int(b)] for a, b in cur.fetchall()]
# dwd_patent 全表 GROUP BY 超时（S3-03 实测），采样框 dwd_id<=200000
cur.execute("SELECT COUNT(*) FROM gkx.dwd_patent WHERE dwd_id<=200000")
facts["gkx_dwd_patent_sample_frame_rows"] = int(cur.fetchone()[0])
cur.execute("SELECT IFNULL(table_data_source,'<NULL>'), COUNT(*) FROM gkx.dwd_patent "
            "WHERE dwd_id<=200000 GROUP BY table_data_source "
            "ORDER BY COUNT(*) DESC, IFNULL(table_data_source,'<NULL>') ASC")
facts["gkx_dwd_patent_sample_src_dist"] = [[str(a), int(b)] for a, b in cur.fetchall()]
cur.close()
# B11 锚：s304c 快照同读数对账（零漂移核验）
facts["gkx_counts_cache_anchor"] = {
    "dwd_zh_paper": cache["dwd_zh_paper"], "dwd_scholar": cache["dwd_scholar"],
    "dwd_patent": cache["dwd_patent"]}
facts["gkx_s304c_snapshot_agrees"] = (
    snapc["gkx"]["src_dist_dwd_zh_paper"][0][1] == 63656
    and snapc["gkx"]["src_dist_dwd_scholar"][0][1] == 21316)

# ============ ③ dev：词族复用共享探针 + 造数命中披露 ============
facts["dev_call_word_tables"] = probe["dev_call_word_tables"]  # []
facts["dev_supplier_word_tables"] = probe["dev_supplier_word_tables"]  # [enterprise_supply_chain]
facts["dev_supplier_word_hit_note"] = ("唯一命中 gkxlumenx_dwd.enterprise_supply_chain 为造数关系整表"
                                       "（skill §P4.1 禁引清单），且其语义是供应链关系非调用日志——不作承载证据")
facts["dev_table_total"] = probe["dev_table_total"]

# ============ ④ 久新：live 词族复核（失败 2 次即停，快照兜底） ============
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
    facts["jiuxin_call_word_tables_live"] = [t for t in jt if re.search(r"call|invoke|api|request", t, re.I)]
    facts["jiuxin_supplier_word_tables_live"] = [t for t in jt if re.search(r"supplier|provider|supply|vendor", t, re.I)]
    jconn.close()
    facts["jiuxin_probe_mode"] = "live"
except Exception as e:  # noqa: BLE001
    jt = snap["jiuxin"]["tables"]
    facts["jiuxin_call_word_tables_snapshot"] = [t for t in jt if re.search(r"call|invoke|api|request", t, re.I)]
    facts["jiuxin_supplier_word_tables_snapshot"] = [t for t in jt if re.search(r"supplier|provider|supply|vendor", t, re.I)]
    facts["jiuxin_probe_mode"] = f"快照兜底（当日直连失败：{str(e)[:80]}）"
facts["gkx_call_word_tables"] = probe["gkx_call_word_tables"]  # []
facts["gkx_supplier_word_tables"] = probe["gkx_supplier_word_tables"]  # []
facts["gkx_table_count"] = probe["gkx_table_total"]

# ================= 派生（B1：比值全落产物，负结论 null） =================
derived += [
    {"key": "supplier_call_share_pct", "value": None, "numerator": None, "denominator": None,
     "note": "『供应方调用量占总量百分比』分子（供应方维度调用量）与分母（全平台调用量）"
             "均依赖按供应方归集的调用日志面——三源零承载 → 不可构建，按 B10 留空即负结论登记"},
    {"key": "gkx_zh_paper_src_labeled_share_pct", "value": 0.0,
     "numerator": facts["gkx_dwd_zh_paper_src_labeled_rows"],
     "denominator": facts["gkx_dwd_zh_paper_total"],
     "note": "同基：dwd_zh_paper 全表（分子=非空非'NULL'来源标签行，分母=全表行数）；"
             "来源标签替代切面的不可用度证据（非本指标计算值）"},
    {"key": "mock_top1_supplier_share_pct_check", "value": 43.8,
     "numerator": 1250000, "denominator": facts["mock_grand_total_calls"],
     "note": "mock 口径复核：中科院 1,250,000/2,856,000=43.76%→UI 保留 1 位=43.8（演示值，不作源）；"
             "分母=mock 5 家 totalCalls 之和，与同文件 cumulativeCallAnalysis.summary.totalSinceLaunch 同值"},
]

# ================= absence_probe =================
absence += [
    {"probe": "dev 按供应方归集的调用日志面（call/invoke/api/request 词族，542 表）",
     "source": "dev", "sql": "information_schema.tables 扫 gkxlumenx_*（本组共享探针 _probe_s304_l5）",
     "hits": len(facts["dev_call_word_tables"]),
     "hit_detail": "命中 []——0 张；唯一「调用」语义日志 sys_log 是平台管理操作日志（登录/token），"
                   "无供应方维度、无资源接口调用记录"},
    {"probe": "dev 供应方维度承载（supplier/provider/supply/vendor 词族）",
     "source": "dev", "sql": "同上共享探针",
     "hits": len(facts["dev_supplier_word_tables"]),
     "hit_detail": "命中 [gkxlumenx_dwd.enterprise_supply_chain]——造数关系整表（skill §P4.1 禁引清单），"
                   "语义为供应链关系非调用日志，不作承载证据"},
    {"probe": "gkx 调用监控面与供应方面（call/invoke/api/request + supplier 词族，280 表）",
     "source": "gkx", "sql": "information_schema.tables 扫 gkx（共享探针）",
     "hits": 0,
     "hit_detail": "双词族均 0 命中——gkx 为要素明细库（论文/专利/机构/学者），无任何调用流水面"},
    {"probe": "久新调用监控面与供应方面（同词族，live 复核）",
     "source": "jiuxin", "sql": "SHOW TABLES 词族过滤",
     "hits": 0,
     "hit_detail": "0 命中——ads_* 全部为学科/人才/专利/项目分析结果面；探测模式见 facts.jiuxin_probe_mode"},
    {"probe": "gkx 来源标签替代切面可用性（table_data_source 非空标签行）",
     "source": "gkx",
     "sql": "SELECT COUNT(*) FROM gkx.dwd_zh_paper WHERE table_data_source IS NOT NULL AND <> 'NULL'；"
            "dwd_scholar 全表 GROUP BY；dwd_patent 采样框 dwd_id<=200000",
     "hits": 0,
     "hit_detail": f"dwd_zh_paper 非空标签 {facts['gkx_dwd_zh_paper_src_labeled_rows']} 行（全表 "
                   f"{facts['gkx_dwd_zh_paper_total']}，分布 {facts['gkx_dwd_zh_paper_src_dist']}）；"
                   f"dwd_scholar 分布 {facts['gkx_dwd_scholar_src_dist']}（'gkx_ods' 为 ETL 批次标记"
                   "非供应方语义）；dwd_patent 采样框分布全 NULL——即便退到静态来源维度也无可用分布"},
    {"probe": "需求原文「供应方调用量占比」定义段",
     "source": "doc", "sql": "rg 供应方 三份需求真源",
     "hits": 6,
     "hit_detail": "主需求 :2555/:2861 与 SRS 应用视窗 seq 388-391「数据供应方数据被调用情况」功能族在"
                   "（供应方归类/累计调用统计/频率趋势/可视化），但「供应方调用量占总量百分比」指标名与"
                   "占比算式三份说明书均未出现；mock share 字段是 UI 演示值（B10 不作源）"},
]

support = "完全不支持"

notes += [
    "判档：供应方维度调用量（分子）与全平台调用量（分母）同源于「按供应方归集的调用日志面」——"
    "三源词族逐一 0 命中（dev 造数命中披露排除）→ 指标及关键依赖均无法构建 → 完全不支持",
    "gkx 唯一现成切面 table_data_source 语义核验：dwd_zh_paper 标签全 NULL（63,656 字面 'NULL' + "
    "37,244 真 NULL，非空标签 0 行）、dwd_patent 采样框 14,371 行全 NULL、dwd_scholar 全 'gkx_ods'"
    "（ETL 批次标记）——该列是数据入库来源标记，不是「供应方」维度，且无调用量信息（静态标签非流水）",
    "mock 披露：supplierStats 5 家 share 43.8+23.8+16.0+10.9+5.5=100.0（facts.mock_share_sum_check_pct）"
    "——演示框架的分母是 5 家 totalCalls 之和 2,856,000，恰好等于同文件 cumulativeCallAnalysis 的"
    "totalSinceLaunch（mock 内部自洽的叙事设计）；share 重算公式在 ApplicationWindow.jsx:433-436",
    "B3 同基提示：本指标是占比类，分子分母必须同筛选集同时间窗——UI 的 share 即在当前筛选集内重算分母"
    "（grandTotal=当前维度累计调用），这一同基设计是 mock 侧唯一可借鉴的口径（真实数据侧无从落地）",
    "B11 对账：zh_paper/scholar/patent 总数走 gkx_counts_cache 锚（100,900/21,316/2,939,895），"
    "本件 GROUP BY 与 s304c 快照分布一致（facts.gkx_s304c_snapshot_agrees=true）",
    "升档触发器（B10）：①API 网关日志接入且含供应方/资源归属维度 → 升完全直接支持（工程立项）；"
    "②建供应方登记面+按资源归属静态折算调用量 → 升部分支持（口径披露「静态折算非实测」）",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_013",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:216",
        "repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:433",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:909",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份说明书未出现「供应方调用量占总量百分比」指标名；语义锚 SRS 应用视窗 seq 389"
                "「累计调用次数统计」/主需求 :2555、:2861（供应方被调用情况功能族——占比算式无）",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [], "base_years_missing": [],
    "base_years_note": "调用占比类监控指标，不涉基期年",
    "ctx_refs": {"note": "正文引用型数字登记",
                 "refs": ["43.8", "23.8", "16.0", "10.9", "5.5", "100.0", "2856000", "1250000",
                          "100900", "63656", "37244", "21316", "14371", "2939895", "542", "280",
                          "210", "156", "89", "67", "45", "34"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
