#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_SCIUI_DATATHM_030 数据资源总记录数 · 三源探针与复现脚本（S3-04 L2 主题库窗组）。

含义：科技数据资源·主题视窗·统计概览第三卡「总记录数」（ThemeWindow.jsx:389
StatCard value="10.2" unit="亿条"——mock 演示值；siblings：主题库总数 28/数据表
1,248/存储总量 18.6TB）。需求侧：指标名三份真源 0 命中；主需求 :2729「数据量」是
元数据属性项非总记录指标。

判档路径（口径=「三源全库记录合计」盘点面，双基并列）：
- 久新：lane7 快照 210 表 rowcounts 合计 182,707,016（活库只读，信息量最全的结果面）；
- gkx：280 表——大表（dwd_patent 2.9M）COUNT 走 s3_01 快照精确值，其余表本件逐一精确 COUNT；
- dev：gkxlumenx_* 16 schema 542 表 information_schema.table_rows 估算口径
  （B9 note：0 值可信非 0 为量级）。
→ 记录合计三源可算（数据量充足），但 mock 口径「10.2 亿」的三源对应读数与口径
  裁定（是否含配置表/空表/结果面重复计数）无登记 → 部分支持。
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_SCIUI_DATATHM_030_out.json")
SNAP = os.path.join(BASE, "_snapshots", "_lane7_shared_probe_out.json")
SNAP01 = os.path.join(BASE, "_snapshots", "_shared_probe_s3_01_out.json")
sys.path.insert(0, BASE)

import pymysql  # noqa: E402
import _gkxdb  # noqa: E402

facts, derived, notes, absence = {}, [], [], []
snap = json.load(open(SNAP, encoding="utf-8"))

# ============ ① dev：16 schema 542 表行数合计（information_schema 估算口径） ============
DEV = dict(host="10.50.11.76", port=3306, user="root", password="Gkxzp202600",
           database="gkxlumenx_dwd", charset="utf8mb4", connect_timeout=10, read_timeout=300)
lconn = pymysql.connect(**DEV)
lcur = lconn.cursor()
lcur.execute(
    "SELECT table_schema, SUM(table_rows) FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%%' GROUP BY table_schema ORDER BY table_schema")
per_schema = [(r[0], int(r[1]) if r[1] is not None else 0) for r in lcur.fetchall()]
facts["dev_rows_sum_by_schema_sorted"] = [[s, n] for s, n in sorted(per_schema)]
facts["dev_rows_sum_estimated"] = int(sum(n for _, n in per_schema))
lconn.close()

# ============ ② gkx：280 表逐一精确 COUNT（大表走快照锚；全量计数落缓存防重打） ============
CACHE = os.path.join(BASE, "_snapshots", "_s304_gkx_counts_cache.json")
gcur = _gkxdb.gkx()
gcur.execute("SHOW TABLES FROM gkx")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
facts["gkx_table_count"] = len(gkx_tables)

# 快照已有精确值（避免重复 COUNT 大表）
snapshot_counts = {"dwd_zh_paper": 100900, "dwd_patent": 2939895}
cache = {}
if os.path.exists(CACHE):
    cache = json.load(open(CACHE, encoding="utf-8"))
# 7.98M 招聘表等大表按 s3_01 纪律采样过的（未含），全部逐一 COUNT 但单表设 read_timeout
gkx_counts = {}
errors = []
for t in gkx_tables:
    if t in snapshot_counts:
        gkx_counts[t] = snapshot_counts[t]
        continue
    if t in cache:
        gkx_counts[t] = cache[t]
        continue
    try:
        gcur.execute(f"SELECT COUNT(*) FROM gkx.{t}")
        gkx_counts[t] = int(gcur.fetchone()[0])
    except Exception as e:  # noqa: BLE001
        errors.append([t, str(e)[:120]])
        gkx_counts[t] = None
gcur.close()
# 回写缓存（仅成功值；同日只读库幂等）
for t, v in gkx_counts.items():
    if v is not None:
        cache[t] = v
with open(CACHE, "w", encoding="utf-8") as fjson:
    json.dump(cache, fjson, ensure_ascii=False, indent=1, sort_keys=True)
facts["gkx_rows_by_table_sorted"] = [[t, gkx_counts[t]] for t in sorted(gkx_counts)]
facts["gkx_rows_sum_exact"] = int(sum(v for v in gkx_counts.values() if v is not None))
facts["gkx_count_error_tables"] = sorted(errors)
facts["gkx_zero_tables"] = sorted(t for t, v in gkx_counts.items() if v == 0)

# ============ ③ 久新：210 表 rowcounts 合计（lane7 快照 B11 锚） ============
jx_rc = snap["jiuxin"]["rowcounts"]
facts["jiuxin_table_count"] = len(jx_rc)
facts["jiuxin_rows_sum"] = int(sum(jx_rc.values()))
facts["jiuxin_nonzero_rows_sum"] = int(sum(v for v in jx_rc.values() if v > 0))
facts["jiuxin_zero_table_count"] = sum(1 for v in jx_rc.values() if v == 0)
facts["jiuxin_top10_rows_sorted"] = sorted(
    [[t, int(v)] for t, v in jx_rc.items()], key=lambda x: -x[1])[:10]

# ============ ④ mock 对照（演示值披露） ============
facts["ui_mock_total_records_display"] = "10.2亿条"  # ThemeWindow.jsx:389 演示值
facts["mock_records_field_values"] = [  # themeDatabases 7 库 records 字段（演示字符串）
    "2.3亿", "1.8亿", "1.5亿", "0.9亿", "0.76亿", "0.68亿", "0.45亿",
]
facts["mock_records_field_sum_yi"] = round(sum(
    [2.3, 1.8, 1.5, 0.9, 0.76, 0.68, 0.45]), 2)  # mock 数组合计（亿，脚本解析同源值）

# dev 配置面行数（bi/cfg/cms/config 四 schema 合计——语义非数据资源）
facts["dev_config_schema_rows_sum"] = int(sum(
    n for s, n in per_schema if s in ("gkxlumenx_bi", "gkxlumenx_cfg",
                                      "gkxlumenx_cms", "gkxlumenx_config")))
# dev↔gkx 同名专利族重复计数上界（读 029 产物 dev 专利族合计——同快照同口径）
p029 = json.load(open(os.path.join(BASE, "M_SCIUI_DATATHM_029_out.json"), encoding="utf-8"))
facts["dev_gkx_overlap_rows_upperbound"] = int(
    p029["facts"]["dev_patent_family_rows_sum"])

# ================= 派生（双基并列，不加总为单一值） =================
three_sum = (facts["dev_rows_sum_estimated"] + facts["gkx_rows_sum_exact"]
             + facts["jiuxin_rows_sum"])
derived.append({
    "key": "total_records_three_source_sum",
    "value": float(three_sum),
    "numerator": None,
    "denominator": None,
    "note": "三源全库记录合计=dev " + f"{facts['dev_rows_sum_estimated']:,}" +
            "（information_schema.table_rows 估算口径，B9：0 值可信非 0 为量级）+ gkx " +
            f"{facts['gkx_rows_sum_exact']:,}（280 表逐一精确 COUNT，大表走 s3_01 快照锚）+ 久新 " +
            f"{facts['jiuxin_rows_sum']:,}（lane7 快照 rowcounts 合计）；三源口径异构"
            "（估算/精确/快照）且可能重复计数（同数据多源），合计仅作量级参考非正式口径",
})
derived.append({
    "key": "data_resource_total_records",
    "value": None,
    "numerator": None,
    "denominator": None,
    "note": "『数据资源总记录数』正式口径（资源中心边界=哪些库表计入、去重规则）三源无"
            "登记面；mock 10.2 亿为演示值；按 B10 不写伪指标值，此键留空即负结论登记",
})
# mock 量级比（演示值 vs 实测合计）
three_yi = round(three_sum / 1e8, 2)
# 万单位换算键族（MD 行文口径）
facts["three_source_sum_wan_unit"] = round(three_sum / 1e4)
facts["gkx_rows_sum_wan_unit"] = round(facts["gkx_rows_sum_exact"] / 1e4)
facts["jiuxin_rows_sum_wan_unit"] = round(facts["jiuxin_rows_sum"] / 1e4)
facts["dev_rows_sum_wan_unit"] = round(facts["dev_rows_sum_estimated"] / 1e4)
facts["jiuxin_share_pct_of_three_source"] = round(
    100.0 * facts["jiuxin_rows_sum"] / three_sum, 1)
facts["gkx_patent_family_rows_wan_unit"] = round(
    sum(v for t, v in gkx_counts.items()
        if "patent" in t.lower() and v), 0) / 1e4
derived.append({
    "key": "mock_vs_measured_ratio",
    "value": round(10.2 / three_yi, 1),
    "numerator": 10.2,
    "denominator": three_yi,
    "note": "分子=UI StatCard 硬编码演示值 10.2 亿；分母=三源实测合计 " + str(three_yi)
            + " 亿（total_records_three_source_sum/1e8）；演示值是实测的倍数（量级失配披露用）",
})
# 重复计数占比上界（dev 专利族合计 / 三源合计）
derived.append({
    "key": "dev_gkx_overlap_share_pct_upperbound",
    "value": round(100.0 * facts["dev_gkx_overlap_rows_upperbound"] / three_sum, 2),
    "numerator": facts["dev_gkx_overlap_rows_upperbound"],
    "denominator": three_sum,
    "note": "分子=dev 专利族 17 表行数合计（与 gkx 同名族的直加重复上界）；"
            "分母=三源合计；行政直加口径的重复计数占比上界（实际重复以同名表行数较小侧计）",
})

# ================= absence_probe =================
absence += [
    {"probe": "dev/gkx/久新全库行数合计面（资源中心总记录的直查结果面）",
     "source": "dev",
     "sql": "information_schema 三源全表行数聚合（542+280+210 表）",
     "hits": 0,
     "hit_detail": "三源均无『总记录数』汇总结果面（无 view/汇总表/ADS 指标表承载该读数）；"
                   "可经全表行数聚合转换得到（本件产物），但口径（含不含配置表 job/pay/bi、"
                   "去不去跨源重复）需裁定"},
    {"probe": "需求原文「总记录数/数据资源总记录数」命名检索（三份真源）",
     "source": "doc",
     "sql": "rg 总记录数/数据资源总记录数 三份需求真源",
     "hits": 0,
     "hit_detail": "指标名 0 命中；主需求 :2729「数据量」是数据集元数据属性项"
                   "（『包括名称、所属主题库、数据类型、数据量、来源单位……』）非平台级"
                   "总记录指标；UI StatCard 10.2 亿为 mock 演示值",
    },
]

support = "部分支持"

notes += [
    "判档：三源全库记录合计 " + f"{three_sum:,}" + " 条（量级亿级，数据量充足可转换），"
    "但『总记录数』的正式口径（资源中心边界/去重规则/单位）三源无登记面且需求未立项"
    "→ 口径可转换但需裁定 → 部分支持（B10 双基并列交付）",
    "mock 披露：ThemeWindow.jsx:389 StatCard value=10.2 亿条为演示值；mock themeDatabases "
    "7 库 records 字段合计≈8.39 亿（2.3+1.8+1.5+0.9+0.76+0.68+0.45）与 UI 硬编码 10.2 亿"
    "不一致——演示框架自身失配，均不作数据证据（B10）",
    "B11 对账：久新 rowcounts 全取 lane7 快照（210 表）；gkx 大表（dwd_zh_paper/dwd_patent）"
    "取 s3_01 快照精确 COUNT；dev 走 information_schema（与 DATAOV_001 同口径）",
    "久新活库：2026-11-01 L1 组登记连接失败 2 次，本件久新读数全走 lane7 快照（B11 锚）",
    "升档触发器（B10）：①建资源登记面（边界=哪些库表计入总记录）→ 升完全直接支持；"
    "②甲方裁定口径（如仅计数据类表、跨源去重规则）→ 升完全转换支持",
]

out = {
    "metric_id": "M_SCIUI_DATATHM_030",
    "batch": "S3-04",
    "ui_evidence": [
        "repos/demo-ui-science/src/pages/data-resources/ThemeWindow.jsx:389",
        "repos/demo-ui-science/src/pages/data-resources/mockData.js:477",
    ],
    "requirement_trace": {
        "named_in_srs": False,
        "note": "三份需求说明书未出现该指标名。主需求 :2729「数据量」为数据集元数据属性项"
                "非平台级总记录指标；SRS 数据资源分册命名检索 0 命中；UI StatCard 10.2 亿为演示值",
    },
    "facts": facts,
    "derived": derived,
    "absence_probe": absence,
    "support_judgment": support,
    "notes": notes,
    "base_years_used": [],
    "base_years_missing": [],
    "base_years_note": "本件为存量盘点型（无年度序列需求；年度增长面由 DATAOV_002 承接）",
    "ctx_refs": {"note": "正文引用型数字登记（外部参照/跨件引用/万单位换算）",
                 "refs": ["10.2", "8.39", "2.58", "3.9", "0.11", "28", "1248",
                          "155721", "20", "270PB", "184.42PB", "798", "10"]},
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
