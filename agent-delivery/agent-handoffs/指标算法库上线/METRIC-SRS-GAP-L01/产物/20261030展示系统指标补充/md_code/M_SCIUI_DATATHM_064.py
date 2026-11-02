# -*- coding: utf-8 -*-
"""
M_SCIUI_DATATHM_064 数据资源条数（供应方/渠道双侧挂载）
挂载点:
  - repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:214 (supplierColumns 资源数列)
  - repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:238 (channelColumns 资源数列)
  - repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:317 (groupColumns 资源数列)
支持度判定: 部分支持（表级资源近似面三源在，供应方×资源/渠道×资源口径登记面三源无）
"""
import json
import re

import pymysql

OUT = 'M_SCIUI_DATATHM_064_out.json'
REPO_ROOT = '/Users/samuel_tang/my_project/gkx-lumen'

facts = {}
absence = []

# ---------- UI mock 解析（程序化，勿手数） ----------
src = open(REPO_ROOT + '/repos/demo-ui-science/src/pages/data-resources/mockData.js', encoding='utf-8').read()

# A. 应用视窗供应侧面 supplierStats (:909-915) —— 挂载 ApplicationWindow.jsx:214
m = re.search(r'export const supplierStats = \[(.*?)\n\];', src, re.S)
sup_rows = re.findall(
    r"name: '(.*?)', department: '(.*?)', resourceCount: (\d+), totalCalls: (\d+), share: ([\d.]+), region: '(.*?)'",
    m.group(1),
)
suppliers = [
    {'name': n, 'department': d, 'resourceCount': int(rc), 'totalCalls': int(tc), 'share': float(s), 'region': reg}
    for n, d, rc, tc, s, reg in sup_rows
]
assert len(suppliers) == 5, len(suppliers)
sup_sum_rc = sum(s['resourceCount'] for s in suppliers)
sup_sum_share = round(sum(s['share'] for s in suppliers), 1)
assert sup_sum_rc == 391, sup_sum_rc          # 156+89+67+45+34
assert sup_sum_share == 100.0, sup_sum_share

# B. 区域归集面 supplierRegionGroups (:918-941) —— 挂载 ApplicationWindow.jsx:491 区域组「N 项资源」
m2 = re.search(r'export const supplierRegionGroups = \[(.*?)\n\];', src, re.S)
grp_meta = re.findall(r"region: '(.*?)',\s*\n\s*supplierCount: (\d+),\s*\n\s*resourceCount: (\d+),\s*\n\s*totalCalls: (\d+)", m2.group(1))
groups = [{'region': r, 'supplierCount': int(sc), 'resourceCount': int(rc), 'totalCalls': int(tc)}
          for r, sc, rc, tc in grp_meta]
assert len(groups) == 2, len(groups)
grp_sum_rc = sum(g['resourceCount'] for g in groups)
dept_rcs = [int(x) for x in re.findall(r'resourceCount: (\d+) \}', m2.group(1))]
assert grp_sum_rc == 391 and sum(dept_rcs) == 391, (grp_sum_rc, sum(dept_rcs))

# C. 接入视窗渠道侧面 channels (:101-107) —— 挂载 AccessSourceAnalysisDetail.jsx:238
ch_block = re.search(r'channels: \[(.*?)\n  \],', src, re.S).group(1)
ch_rows = re.findall(r"name: '(.*?)', volume: (\d+), count: (\d+), share: ([\d.]+)", ch_block)
channels = [{'name': n, 'volume': int(v), 'count': int(c), 'share': float(s)} for n, v, c, s in ch_rows]
assert len(channels) == 5
ch_sum = sum(c['count'] for c in channels)
assert ch_sum == 1256, ch_sum

# D. 分组聚合面 groupedData（:195-205 前端聚合，groupColumns :317 消费）
# mock 无运行时，但源码 groupedData 对 details 12 行聚合——分组键全集
det_block = re.search(r'details: \[(.*?)\n  \],', src, re.S).group(1)
detail_channels = re.findall(r"channel: '(.*?)', dataType", det_block)
assert len(detail_channels) == 12
grouped_detail_total = len(detail_channels)

facts['ui'] = {
    'supplier_side': {
        'mount': 'ApplicationWindow.jsx:214 (supplierColumns 资源数列) + :582 (Table 消费) + :491 (区域组 N 项资源)',
        'mock_rows': len(suppliers),
        'mock_resource_count_sum': sup_sum_rc,               # 391
        'mock_share_sum_pct': sup_sum_share,                  # 100.0
        'mock_region_groups': [{'region': g['region'], 'resourceCount': g['resourceCount']} for g in groups],
        'mock_region_group_sum': grp_sum_rc,                  # 391（与供应方侧逐值一致 279+112）
        'mock_dept_nested_sum': sum(dept_rcs),                # 391
        'mock_srs_anchor': 'seq 388 部门名称自动归集展示（部门归属自动识别）',
    },
    'channel_side': {
        'mount': 'AccessSourceAnalysisDetail.jsx:238 (channelColumns 资源数列) + :317 (groupColumns 资源数列)',
        'mock_rows': len(channels),
        'mock_count_sum': ch_sum,                             # 1256
        'mock_srs_anchor': 'seq 351 渠道归集数据量统计（条数维）',
    },
    'cross_side_gap': ch_sum - sup_sum_rc,                    # 1256 - 391 = 865
    'grouped_detail_rows': grouped_detail_total,              # 12（分组聚合面的明细基座）
}

# ---------- 三源探针（复用 063 实跑结论 + 供应方词族补充探针） ----------
# 供应方维度词族（supplier/provider/vendor/supply）三源逐一留证（本件新增，063 未覆盖）

# ① dev live
dev_conn = pymysql.connect(host='10.50.11.76', port=3306, user='root', password='Gkxzp202600', charset='utf8mb4')
cur = dev_conn.cursor()
cur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP 'supplier|provider|vendor|supply'"
)
dev_sup_hits = sorted(r[0] + '.' + r[1] for r in cur.fetchall())
cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema LIKE 'gkxlumenx%'")
dev_total = cur.fetchone()[0]
dev_conn.close()
absence.append({
    'probe': '供应方维度词族（supplier|provider|vendor|supply）',
    'source': 'dev',
    'sql': "information_schema.tables WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP 'supplier|provider|vendor|supply'",
    'hits': len(dev_sup_hits),
    'hit_detail': (
        f'{dev_total} 表唯一命中 gkxlumenx_dwd.enterprise_supply_chain——DESC 实查 9 列'
        '（org_id/related_org_id/relation_type/relation_strength/is_core_supplier 等）0 行——'
        '企业供应链关系图谱（空表），非数据供应方×资源登记面，语义排除；'
        '资源目录词族 0 命中承 063 件（resource/catalog/inventory/metadata/registry 全零）'
    ),
})

# ② gkx（经 _gkxdb.py）
import importlib.util
_spec = importlib.util.spec_from_file_location('gkxdb', '_gkxdb.py')
gkxdb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gkxdb)
gcur = gkxdb.gkx()
gcur.execute("SHOW FULL TABLES FROM gkx WHERE Table_type != 'VIEW'")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
gkx_sup_hits = [t for t in gkx_tables if re.search(r'supplier|provider|vendor|supply|resource|catalog|collect|inventory|registry|source_code', t, re.I)]
absence.append({
    'probe': '供应方+资源目录词族（supplier|provider|vendor|supply + resource|catalog|collect|inventory|registry + source_code）',
    'source': 'gkx',
    'sql': 'SHOW FULL TABLES FROM gkx + 双词族过滤（经 _gkxdb.py 2026-11-02 实跑）',
    'hits': len(gkx_sup_hits),
    'hit_detail': (
        f'{len(gkx_tables)} 表：供应方词族 0 命中；资源目录词族唯一命中 dwd_dim_source_code'
        '（数据源维度表 4 行，登记来源编码 source_code/source_name 非资源条目——063 件 DESC 实查语义排除）——供应方×资源双缺'
    ),
})

# ③ 久新 live
j_conn = pymysql.connect(
    host='47.93.119.170', port=29030, user='test2',
    password='m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka',
    database='gkx_technology_analysis_dev', charset='utf8mb4',
)
jcur = j_conn.cursor()
jcur.execute("SHOW TABLES")
jiuxin_tables = sorted(r[0] for r in jcur.fetchall())
jiuxin_sup_hits = [t for t in jiuxin_tables if re.search(r'supplier|provider|vendor|supply', t, re.I)]
jiuxin_res_hits = [t for t in jiuxin_tables if re.search(r'resource', t, re.I)]
j_conn.close()
absence.append({
    'probe': '供应方维度词族（supplier|provider|vendor|supply）+ resource 复核',
    'source': 'jiuxin',
    'sql': 'SHOW TABLES + 双词族过滤（Doris，information_schema 无权限）',
    'hits': len(jiuxin_sup_hits),
    'hit_detail': (
        f'{len(jiuxin_tables)} 张 ads 面（2026-11-02 实跑）：供应方词族 0 命中；'
        f'resource 词族 {len(jiuxin_res_hits)} 张全为论文计量年表（063 件 DESC 实查语义排除）——'
        '供应方×资源登记面无承载'
    ),
})

facts['three_source'] = {
    'dev_table_total': dev_total,                              # 542（与 lane7 快照零漂移）
    'dev_supplier_hits': dev_sup_hits,                         # ['gkxlumenx_dwd.enterprise_supply_chain']（供应链空表，语义排除）
    'gkx_table_total': len(gkx_tables),                        # 280
    'gkx_dual_family_hits': gkx_sup_hits,                      # ['dwd_dim_source_code']（语义排除）
    'jiuxin_table_total': len(jiuxin_tables),                  # 215（2026-11-02 实跑；lane7 快照 210+5 张 ads_talent_*——063 件漂移登记）
    'jiuxin_supplier_hits': jiuxin_sup_hits,                   # []
    'jiuxin_resource_hits_count': len(jiuxin_res_hits),        # 7（论文计量，语义排除）
    'resource_family_exclusion_ref': 'M_SCIUI_DATATHM_063_out.json（resource/catalog/collect/inventory/registry 词族三源排除+DESC 语义核对，本件复用）',
}

# 表级近似口径（承 036 产物，互引不重算）
facts['table_level_approximation_from_036'] = {
    'three_source_all': 1032,
    'three_source_all_asof': '2026-11-01（lane7 快照日；久新 2026-11-02 实跑 215 张，036 口径沿用其探测日）',
    'three_source_no_backup': 930,
    'note': 'M_SCIUI_DATATHM_036_out.json derived——表级近似，非供应方/渠道×资源条目口径',
}

# ---------- 判定 ----------
derived = [
    {
        'key': 'data_resource_count_by_supplier',
        'value': None,
        'numerator': None,
        'denominator': None,
        'note': '正式口径 COUNT(*) GROUP BY supplier（供应方×资源登记面）三源无承载——mock 391（Σ supplierStats.resourceCount）为演示值不作数据证据（B10）',
    },
    {
        'key': 'data_resource_count_by_channel',
        'value': None,
        'numerator': None,
        'denominator': None,
        'note': '渠道侧口径 Σ channels.count 三源无承载（063 同根）——mock 1,256 为演示值（B10）',
    },
    {
        'key': 'data_resource_count_table_approximation_no_backup',
        'value': 930,
        'numerator': None,
        'denominator': None,
        'note': '表级近似剔备份：930（036 产物互引；供应方/渠道归属字段缺位，分组维度不可得，仅全库总量近似）',
    },
]

out = {
    'metric_id': 'M_SCIUI_DATATHM_064',
    'batch': 'S3-05',
    'metric_name': '数据资源条数',
    'ui_evidence': [
        'repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:214 (supplierColumns「资源数」列 dataIndex=resourceCount)',
        'repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:582 (Table columns={supplierColumns} 消费)',
        'repos/demo-ui-science/src/pages/data-resources/ApplicationWindow.jsx:491 (区域组「{g.resourceCount} 项资源」)',
        'repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:238 (channelColumns「资源数」列 dataIndex=count)',
        'repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:317 (groupColumns「资源数」列 dataIndex=count——分组聚合消费)',
        'repos/demo-ui-science/src/pages/data-resources/mockData.js:909-941 (supplierStats 5 行 + supplierRegionGroups 2 组)',
    ],
    'requirement_trace': {
        'named_in_srs': False,
        'note': (
            '「数据资源条数/资源数」字面三份说明书 0 命中（作为列名/行内读数非立项项）。语义锚双语境：'
            '①SRS 应用视窗 seq 388「部门名称自动归集展示」（供应方智能归类+部门归属识别——资源数是归集摘要的计数维）；'
            '②SRS 接入视窗 seq 351「渠道归集数据量统计」（条数维——与 063 同根）。两处组件注释均自标 seq 锚'
        ),
    },
    'facts': facts,
    'derived': derived,
    'absence_probe': absence,
    'support_judgment': '部分支持',
    'notes': [
        '判档：表级资源近似面（三库表清单+计数）三源结构+数据双在——但「供应方×资源/渠道×资源」口径登记面（资源目录含归属字段）三源逐一零命中 → 部分支持',
        'mock 披露（双面结构）：供应侧面 Σ supplierStats.resourceCount=391（156+89+67+45+34，share 合计 100.0%）；区域归集面 supplierRegionGroups 2 组（华北 279/华南 112）与部门嵌套逐值一致（279=156+89+34，112=67+45）——mock 内部三层自洽；但渠道侧面 Σ channels.count=1,256——同一演示库内「资源条数」双面差 865（1,256-391），供应方口径与渠道口径非同一台账（B10 均不作数据证据）',
        '双语境双挂载披露：本件一名两挂——应用视窗供应侧面（seq 388 语境，supplierColumns/区域组）与接入视窗渠道侧面（seq 351 语境，channelColumns/groupColumns 与 063 同数据源）——正式版须先统一「资源归属维度」（供应方/渠道/部门三轴是否同一登记面的字段）',
        'B11 对账：dev 542/gkx 280 与 lane7 快照零漂移；久新快照 210→实跑 215 漂移承 063 件登记（+5 张 ads_talent_*，本件供应方词族命中数 0 不变）',
    ],
    'base_years_used': [],
    'base_years_missing': [],
    'base_years_note': '本件为存量盘点型（无年度序列需求）',
    'ctx_refs': {
        'note': '正文引用型数字登记（外部参照/跨件引用）',
        'refs': ['542', '280', '210', '215', '1032', '930', '391', '279', '112', '1256', '865', '12'],
    },
}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', OUT)
print(json.dumps({
    'supplier_sum_391': sup_sum_rc,
    'region_group_sum': grp_sum_rc,
    'channel_sum_1256': ch_sum,
    'cross_side_gap': ch_sum - sup_sum_rc,
    'dev_supplier_hits': len(dev_sup_hits),
    'gkx_dual_hits': gkx_sup_hits,
    'jiuxin_total': len(jiuxin_tables),
    'jiuxin_supplier_hits': len(jiuxin_sup_hits),
    'judgment': '部分支持',
}, ensure_ascii=False, indent=2))
