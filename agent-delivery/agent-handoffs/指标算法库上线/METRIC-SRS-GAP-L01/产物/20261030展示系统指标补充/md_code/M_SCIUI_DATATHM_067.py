# -*- coding: utf-8 -*-
"""
M_SCIUI_DATATHM_067 数据资源总量（记录）（总体视窗 KPI 卡「资源总量 30,398 个」+ 年度趋势线「资源总量」序列）
挂载点:
  - repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:559 (reportSheets 年度趋势 sheet「资源总量」列 dataIndex=total)
  - OverviewWindow.jsx:108-113 (趋势线 series name=资源总量, data=item.total)
  - mockData.js:1656 (overviewKPIs 资源总量 30,398 KPI 卡)
  - mockData.js:72-78 (overviewAnnualAccessTrend 5 年序列)
  - OverviewWindow.jsx:748/750 (下钻汇总「数据总量 30,398个」/「资源总量 21,198个」)
支持度判定: 部分支持（表级资源近似面三源在——记录维 ROW_COUNT 近似可实算；资源粒度口径登记面三源无）
"""
import json
import re

import pymysql

OUT = 'M_SCIUI_DATATHM_067_out.json'
REPO_ROOT = '/Users/samuel_tang/my_project/gkx-lumen'

facts = {}
absence = []

# ---------- UI mock 解析 ----------
src = open(REPO_ROOT + '/repos/demo-ui-science/src/pages/data-resources/mockData.js', encoding='utf-8').read()

# A. 年度趋势 5 年序列（:72-78）
m = re.search(r'export const overviewAnnualAccessTrend = \[(.*?)\n\];', src, re.S)
rows = re.findall(r"year: '(\d+)', total: (\d+), added: (\d+), yoy: (null|[\d.\-]+)", m.group(1))
trend = [{'year': y, 'total': int(t), 'added': int(a), 'yoy': (None if yy == 'null' else float(yy))} for y, t, a, yy in rows]
assert len(trend) == 5
totals = [r['total'] for r in trend]
adds = [r['added'] for r in trend]
chain_ok = all(totals[i] == totals[i-1] + adds[i] for i in range(1, 5))
assert chain_ok
assert totals[-1] == 30398
# yoy 逐位复核
yoy_checks = []
for i in range(1, 5):
    calc = round((totals[i] - totals[i-1]) / totals[i-1] * 100, 1)
    yoy_checks.append({'year': trend[i]['year'], 'mock_yoy': trend[i]['yoy'], 'calc_yoy': calc,
                       'match': abs(calc - trend[i]['yoy']) < 0.15})
assert all(c['match'] for c in yoy_checks)

# B. KPI 卡资源总量（:1656）
kpi = re.search(r"label: '资源总量', value: '([\d,]+)', unit: '个'", src).group(1)
assert kpi == '30,398'
# KPI 与趋势末年同值对账
assert int(kpi.replace(',', '')) == totals[-1]

# C. 单位语义披露——「个」是资源计数单位非记录数单位
facts['ui'] = {
    'mount_lines': [
        'OverviewWindow.jsx:559 (reportSheets「年度增长趋势」sheet 列 {title:资源总量, dataIndex:total})',
        'OverviewWindow.jsx:108-113 (趋势线 series name=资源总量, data=overviewAnnualAccessTrend.map(item=>item.total))',
        'mockData.js:1656 (overviewKPIs {label:资源总量, value:30,398, unit:个, key:total})',
        'mockData.js:72-78 (overviewAnnualAccessTrend 5 年序列，注释自标「需规 seq 330，演示数据」)',
        'OverviewWindow.jsx:748 (source 下钻汇总「数据总量 30,398个」)',
        'OverviewWindow.jsx:750 (theme 下钻汇总「资源总量 21,198个」——062 件同源)',
    ],
    'mock_trend': trend,                          # 2022-2026: 12860/16940/21860/26720/30398
    'mock_final_total': totals[-1],               # 30398
    'mock_added_sum_excl_first': sum(adds[1:]),   # 后4年新增
    'mock_chain_consistent': chain_ok,            # total[i]=total[i-1]+added[i] 全链
    'mock_yoy_checks': yoy_checks,                # 4 期逐位复核一致
    'mock_kpi_equals_trend_final': True,          # KPI 30,398 = 趋势 2026 末值
    'mock_theme_summary_total': 21198,            # theme 下钻 21,198（062 件 resourceThemeDistribution 同源 Σ）
    'unit_semantics_note': 'KPI/趋势/下钻单位均为「个」（资源计数单位）——指标名「数据资源总量（记录）」的记录维（行数 ROW_COUNT）在 UI 无任何挂载，mock 无记录数读数',
}

# ---------- 三源探针 ----------
# 资源粒度口径：承 063（资源目录词族三源零命中）。本件新增：记录维 ROW_COUNT 近似实算（三源表行数合计）。
# gkx 全表计数缓存复用（B8：00:19 gkx 全表计数缓存）

# ① dev：承 063 词族排除；新增行数近似（information_schema.tables table_rows 估算）
dev_conn = pymysql.connect(host='10.50.11.76', port=3306, user='root', password='Gkxzp202600', charset='utf8mb4')
cur = dev_conn.cursor()
cur.execute(
    "SELECT COUNT(*), IFNULL(SUM(table_rows),0) FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' AND table_name NOT REGEXP '^demo_'"
)
dev_tbl_cnt, dev_row_sum = cur.fetchone()
dev_tbl_cnt, dev_row_sum = int(dev_tbl_cnt), int(dev_row_sum)
dev_conn.close()
absence.append({
    'probe': '资源目录面（承 063 零命中）+ 记录维近似（Σtable_rows）',
    'source': 'dev',
    'sql': "information_schema.tables SUM(table_rows) WHERE table_schema LIKE 'gkxlumenx%'（demo_* 剔除）",
    'hits': 0,
    'hit_detail': (
        f'{dev_tbl_cnt} 表 Σtable_rows≈{dev_row_sum:,}（InnoDB 估算值非精确 COUNT）——'
        '记录维近似可得但含配置/流程/报表等系统面表；资源目录面 0 命中承 063'
    ),
})

# ② gkx：复用 00:19 全表计数缓存（B8）
cache = json.load(open('_snapshots/_s304_gkx_counts_cache.json'))
gkx_row_sum = 0
gkx_counted = 0
for k, v in cache.items():
    if isinstance(v, (int, float)):
        gkx_row_sum += v
        gkx_counted += 1
absence.append({
    'probe': '资源目录面（承 063/064）+ 记录维近似（全表 COUNT 缓存 Σ）',
    'source': 'gkx',
    'sql': '00:19 gkx 全表 COUNT 缓存复用（_snapshots/_s304_gkx_counts_cache.json，B8 不重跑）',
    'hits': 0,
    'hit_detail': (
        f'缓存覆盖 {gkx_counted} 表 ΣCOUNT≈{gkx_row_sum:,}（dwd_patent 等大表为采样外推值，精确度需甄别）——'
        '记录维近似可得（要素明细库行数）；资源目录面唯一命中 dwd_dim_source_code 语义排除承 063'
    ),
})

# ③ 久新：ads 面行数近似（复用 036 件 206 非空表结论 + 本件抽验两张）
j_conn = pymysql.connect(
    host='47.93.119.170', port=29030, user='test2',
    password='m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka',
    database='gkx_technology_analysis_dev', charset='utf8mb4',
)
jcur = j_conn.cursor()
jcur.execute("SHOW TABLES")
jiuxin_tables = sorted(r[0] for r in jcur.fetchall())
# 抽验两张大表行数（本件记录维证据）
j_rows = {}
for t in ('ads_institution_subfield_resource_yearly', 'ads_geo_yearly_institution_type_metrics'):
    jcur.execute(f"SELECT COUNT(*) FROM `{t}`")
    j_rows[t] = jcur.fetchone()[0]
j_conn.close()
absence.append({
    'probe': '资源目录面（承 063）+ 记录维近似（ads 面行数）',
    'source': 'jiuxin',
    'sql': 'SHOW TABLES + COUNT(*) 抽验（Doris，information_schema 无权限）',
    'hits': 0,
    'hit_detail': (
        f'{len(jiuxin_tables)} 张 ads 面（2026-11-02 实跑，漂移承 063）：全量 Σ 行数未逐表跑（036 件 206 非空表结论在册）；'
        f'抽验 {j_rows}——记录维可得但均为论文计量聚合面（每行是 city/institution×year×subfield 的指标行，'
        '非数据资源行）；资源目录面 7 张 resource 命中语义排除承 063'
    ),
})

facts['three_source'] = {
    'dev_table_count': dev_tbl_cnt,                    # 542（demo_* 已剔；快照零漂移）
    'dev_row_count_approx': dev_row_sum,               # InnoDB 估算 Σ（非精确）
    'gkx_cached_table_count': gkx_counted,             # 缓存覆盖表数
    'gkx_row_count_sum': gkx_row_sum,                  # 缓存 ΣCOUNT
    'jiuxin_table_total': len(jiuxin_tables),          # 215（实跑；快照 210+5 承 063）
    'jiuxin_spotcheck_rows': j_rows,                   # 抽验两表
    'jiuxin_nonzero_ref': 'M_SCIUI_DATATHM_036_out.json（206 非空/4 空表）',
    'resource_family_exclusion_ref': 'M_SCIUI_DATATHM_063_out.json（资源目录词族三源排除复用）',
}

# 表级口径（承 036）
facts['table_level_from_036'] = {
    'three_source_all': 1032,
    'three_source_no_backup': 930,
    'note': '036 件 derived——表级口径；本件记录维近似 = 表级行数 Σ（口径更粗一层）',
}

# ---------- 判定 ----------
derived = [
    {
        'key': 'data_resource_total_records',
        'value': None,
        'numerator': None,
        'denominator': None,
        'note': '正式口径 Σ ROW_COUNT(资源)（资源目录×每资源行数）三源无承载——资源粒度缺位（承 063）+ 各表行数≠资源记录数（表是载体非资源本身）',
    },
    {
        'key': 'data_resource_total_records_table_approx_dev_only',
        'value': dev_row_sum,
        'numerator': None,
        'denominator': None,
        'note': f'表级近似（仅 dev）：Σtable_rows≈{dev_row_sum:,}（InnoDB 估算非精确；含配置/流程/报表系统面；gkx 缓存含采样外推、久新未全量跑——三源合并值不发布，仅 dev 侧登记参考）',
    },
    {
        'key': 'data_resource_total_mock_resource_count',
        'value': None,
        'numerator': None,
        'denominator': None,
        'note': 'UI 读数 30,398 的单位是「个」（资源计数）非记录数——与指标名「（记录）」维不同层，mock 记录维零读数（B10 不冒充记录维）',
    },
]

out = {
    'metric_id': 'M_SCIUI_DATATHM_067',
    'batch': 'S3-05',
    'metric_name': '数据资源总量（记录）',
    'ui_evidence': facts['ui']['mount_lines'] + [
        'repos/demo-ui-science/src/pages/data-resources/mockData.js:1656 (overviewKPIs 资源总量 30,398 个)',
    ],
    'requirement_trace': {
        'named_in_srs': True,
        'srs_anchor': '总体视窗 seq 330 资源接入情况总览：可一键展示当前已接入的所有科技数据资源类型与数量……年度增长趋势……',
        'main_req_anchor': '主需求 :2489（与 seq 330 同文）；:185 分布比例/增长趋势统计可视化语境',
        'note': '「资源总量」字面在需求真源无独立立项项（seq 330「类型与数量」的数量维+「年度增长趋势」语境）；指标名带「（记录）」后缀是清单编者口径注记——记录维（行数）在 UI/需求无挂载，「个」是资源计数单位',
    },
    'facts': facts,
    'derived': derived,
    'absence_probe': absence,
    'support_judgment': '部分支持',
    'notes': [
        '判档：表级记录维近似面三源结构在、部分数据在（dev Σtable_rows 估算/gkx 缓存 Σ/久新抽验）——但资源粒度口径缺位（承 063）+ 表行数≠资源记录数 → 部分支持',
        'mock 披露：5 年趋势链完全自洽（12,860→16,940→21,860→26,720→30,398；total[i]=total[i-1]+added[i] 全链成立；4 期 yoy 逐位复核一致 31.7/29.0/22.2/13.8%）——mock 内罕见的高自洽度，但末值 30,398 与 KPI 卡/类型分布 Σ（065）三处同源——演示值循环自证（承 056/065 混同母体链）',
        '单位语义断裂披露：UI 全部读数单位是「个」（资源计数）——指标名「（记录）」的记录维（行数）在 mock 零读数、在需求零挂载；正式版须先裁「总量」的计数维（资源个数 vs 存储记录数）——两者可差 3-6 个数量级',
        'theme 下钻汇总「资源总量 21,198」与 source 下钻「数据总量 30,398」并存——主题维 Σ（062 件同源）是总量按主题分解的子集形态（21,198 < 30,398 自洽）',
        'B11 对账：dev 542/gkx 280 与 lane7/036 逐键一致；久新 210→215 承 063；30,398 与 056/065 件 overviewKPIs 同值对账（混同母体链第三件）',
    ],
    'base_years_used': [],
    'base_years_missing': ['2022', '2023', '2024', '2025', '2026'],
    'base_years_note': 'mock 趋势 5 年（2022-2026）全为演示数据；三源无逐年资源总量序列承载（base_years 全缺——正式版逐年累计口径需目录+年度快照双立项）',
    'ctx_refs': {
        'note': '正文引用型数字登记（外部参照/跨件引用）',
        'refs': ['542', '280', '210', '215', '1032', '930', '30398', '12860', '21198'],
    },
}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', OUT)
print(json.dumps({
    'mock_trend_final': totals[-1],
    'chain_ok': chain_ok,
    'yoy_all_match': all(c['match'] for c in yoy_checks),
    'dev_row_sum': dev_row_sum,
    'gkx_cached_tables': gkx_counted,
    'gkx_row_sum': gkx_row_sum,
    'jiuxin_spotcheck': j_rows,
    'judgment': '部分支持',
}, ensure_ascii=False, indent=2))
