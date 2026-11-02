# -*- coding: utf-8 -*-
"""
M_SCIUI_DATATHM_066 数据资源类型数（总体视窗 KPI 卡「资源类型数 4 类」）
挂载点: repos/demo-ui-science/src/pages/data-resources/mockData.js:1655 (overviewKPIs 首卡) + OverviewWindow.jsx:605 (KPICard 渲染)
支持度判定: 部分支持（表级类型近似面三源在——dwd 前缀可作要素域轴候选；资源×类型口径登记面三源无，类型主轴未裁）
"""
import json
import re

import pymysql

OUT = 'M_SCIUI_DATATHM_066_out.json'
REPO_ROOT = '/Users/samuel_tang/my_project/gkx-lumen'

facts = {}
absence = []

# ---------- UI mock 解析 ----------
src = open(REPO_ROOT + '/repos/demo-ui-science/src/pages/data-resources/mockData.js', encoding='utf-8').read()

# overviewKPIs 首卡（:1655-1658）
m = re.search(r'export const overviewKPIs = \[(.*?)\n\];', src, re.S)
rows = re.findall(r"label: '(.*?)', value: '([\d,\.]+)', unit: '(.*?)'", m.group(1))
kpis = [{'label': lb, 'value': v, 'unit': u} for lb, v, u in rows]
assert len(kpis) == 3, kpis
type_kpi = [k for k in kpis if k['label'] == '资源类型数'][0]
assert type_kpi['value'] == '4' and type_kpi['unit'] == '类'

# 饼图 4 类（065 同源——枚举计数一致性）
md = re.search(r'export const resourceTypeDistribution = \[(.*?)\n\];', src, re.S)
dist_rows = re.findall(r"name: '(.*?)', value: (\d+)", md.group(1))
assert len(dist_rows) == 4

# dataType 值域 9 类 vs KPI 4 类（065 双轴断裂的枚举计数面）
types_in_file = sorted(set(re.findall(r"dataType: '(.*?)'", src)))

facts['ui'] = {
    'mount': 'mockData.js:1655 (overviewKPIs 首卡「资源类型数 4 类」) + OverviewWindow.jsx:605-612 (KPICard 渲染) + :631 (收起态文案「资源类型与数量」)',
    'mock_kpi_type_count': int(type_kpi['value']),               # 4
    'mock_kpi_siblings': kpis,                                    # 资源总量 30,398 / 主题库数量 28
    'mock_pie_distinct_types': len(dist_rows),                    # 4（与 KPI 卡一致——枚举计数与分布同源）
    'mock_type_domain_file': types_in_file,                       # 9 类（双轴值域承 065）
    'mock_kpi_vs_domain_gap': len(types_in_file) - 4,             # 5（专利/论文/项目/情报/实验数据不在 KPI 计数内）
    'kpi_change_note': 'change: 0（环比 0%——类型数静态语义）',
}

# ---------- 三源探针（承 065 类型词族排除——本件补 dwd 前缀要素域轴实算） ----------
# ① dev：承 063（资源目录词族 0 命中）+ 065（type/category 全为表结构域语义）
dev_conn = pymysql.connect(host='10.50.11.76', port=3306, user='root', password='Gkxzp202600', charset='utf8mb4')
cur = dev_conn.cursor()
cur.execute("SELECT COUNT(*), COUNT(DISTINCT table_schema) FROM information_schema.tables WHERE table_schema LIKE 'gkxlumenx%'")
dev_total, dev_schemas = cur.fetchone()
# dev 侧「类型轴」候选：schema 维度（16 schema 是系统域轴非资源类型轴）——披露不作类型读数
cur.execute(
    "SELECT table_schema, COUNT(*) FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' GROUP BY table_schema ORDER BY table_schema"
)
dev_schema_counts = [[r[0], r[1]] for r in cur.fetchall()]
dev_conn.close()
absence.append({
    'probe': '资源×类型登记面（承 065 类型词族排除）+ dev schema 域轴核验',
    'source': 'dev',
    'sql': "information_schema.tables GROUP BY table_schema（16 schema 域轴）+ 063/065 词族结论复用",
    'hits': 0,
    'hit_detail': (
        f'{dev_total} 表/{dev_schemas} schema：schema 域轴（app/ads/bi/codegen/config/dwd/flow/job 等）是**系统功能域**'
        '分类非数据资源类型轴；type/category 词族全为表结构域语义（承 065）；资源目录词族 0 命中（承 063）——'
        'dev 侧无资源类型枚举面'
    ),
})

# ② gkx：dwd 前缀要素域轴实算（表级近似候选——要素域 COUNT DISTINCT）
import importlib.util
_spec = importlib.util.spec_from_file_location('gkxdb', '_gkxdb.py')
gkxdb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gkxdb)
gcur = gkxdb.gkx()
gcur.execute("SHOW FULL TABLES FROM gkx WHERE Table_type != 'VIEW'")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
# 前缀提取：以表名首个业务词为域（dwd_patent_*/dim_org_*/ads_* 等）——收敛到主要素域白名单
CORE_DOMAINS = ['patent', 'paper', 'talent', 'org', 'institution', 'fund', 'project', 'scholar', 'policy', 'drug', 'clinical', 'material', 'substance', 'news', 'industry']
prefixes = {}
for t in gkx_tables:
    body = re.sub(r'^(dwd|dim|ads|ods)_', '', t)
    first = body.split('_')[0] if '_' in body else body
    dom = first if first in CORE_DOMAINS else ('other')
    prefixes.setdefault(dom, []).append(t)
gkx_domain_counts = sorted([[k, len(v)] for k, v in prefixes.items() if k != 'other'] + ([['other', len(prefixes.get('other', []))]] if prefixes.get('other') else []))
gkx_domain_total_covered = sum(len(v) for k, v in prefixes.items() if k != 'other')
absence.append({
    'probe': '资源类型枚举面（type/category/kind/format 承 065 语义排除）+ dwd 要素域前缀轴实算',
    'source': 'gkx',
    'sql': 'SHOW FULL TABLES + 前缀正则提取（经 _gkxdb.py 2026-11-02 实跑）',
    'hits': 0,
    'hit_detail': (
        f'{len(gkx_tables)} 表：类型词族 3 张承 065 DESC 实查语义排除（内容标签/情报条目）；'
        f'dwd 要素域前缀轴实算：主要素域 {len([k for k in prefixes if k != "other"])} 域覆盖 '
        f'{gkx_domain_total_covered} 表（{gkx_domain_counts}）——要素域轴**可数**但与 UI 存储形态四分型'
        '**不同轴**（两轴不兼容承 065），映射规则无登记——表级类型数近似不可直接转正'
    ),
})

# ③ 久新：承 065（institution_type 是机构类型轴）——学科分类轴承 062
j_conn = pymysql.connect(
    host='47.93.119.170', port=29030, user='test2',
    password='m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka',
    database='gkx_technology_analysis_dev', charset='utf8mb4',
)
jcur = j_conn.cursor()
jcur.execute("SHOW TABLES")
jiuxin_tables = sorted(r[0] for r in jcur.fetchall())
discipline_like = [t for t in jiuxin_tables if re.search(r'discipline|field|domain|subfield', t, re.I)]
j_conn.close()
absence.append({
    'probe': '资源类型枚举面（type 承 065 语义排除）+ 学科分类轴复核（承 062）',
    'source': 'jiuxin',
    'sql': 'SHOW TABLES + discipline/field/domain 词族过滤（Doris，information_schema 无权限）',
    'hits': 0,
    'hit_detail': (
        f'{len(jiuxin_tables)} 张 ads 面（2026-11-02 实跑，漂移承 063）：类型词族 2 张承 065 语义排除'
        f'（机构类型轴）；学科分类词族 {len(discipline_like)} 张（{sorted(discipline_like) if discipline_like else "0"}）'
        '承 062 已探明 4 级学科表——论文学科轴非数据资源类型轴——久新无「资源类型」枚举面'
    ),
})

facts['three_source'] = {
    'dev_table_total': dev_total,                        # 542
    'dev_schema_count': dev_schemas,                     # 16（系统功能域轴，非类型轴）
    'dev_schema_table_counts_sorted': dev_schema_counts, # B5 sorted
    'gkx_table_total': len(gkx_tables),                  # 280
    'gkx_domain_prefix_counts_sorted': gkx_domain_counts,# 要素域前缀轴（表级候选）
    'gkx_domain_prefix_total_covered': gkx_domain_total_covered,
    'jiuxin_table_total': len(jiuxin_tables),            # 215（实跑；快照 210+5 承 063）
    'jiuxin_discipline_tables_sorted': sorted(discipline_like),
    'exclusion_refs': 'M_SCIUI_DATATHM_065_out.json（type 词族三源 DESC 语义排除复用）+ 063（resource 词族）+ 062（学科分类轴）',
}

# ---------- 判定 ----------
derived = [
    {
        'key': 'data_resource_type_count',
        'value': None,
        'numerator': None,
        'denominator': None,
        'note': '正式口径 COUNT(DISTINCT type)（资源×类型登记面+类型主轴裁定）三源无承载——mock KPI 4 为演示值不作数据证据（B10）',
    },
    {
        'key': 'data_resource_type_count_domain_axis_approx',
        'value': len([k for k in prefixes if k != 'other']),
        'numerator': None,
        'denominator': None,
        'note': f'表级近似（要素域轴）：gkx dwd 主要素域 COUNT(DISTINCT)={len([k for k in prefixes if k != "other"])}（覆盖 {gkx_domain_total_covered}/{len(gkx_tables)} 表，白名单 {gkx_domain_counts}）——与 UI 存储形态轴不同轴（两轴不兼容承 065），仅作候选口径登记不作正式值（B10 注记）',
    },
]

out = {
    'metric_id': 'M_SCIUI_DATATHM_066',
    'batch': 'S3-05',
    'metric_name': '数据资源类型数',
    'ui_evidence': [
        'repos/demo-ui-science/src/pages/data-resources/mockData.js:1655-1658 (overviewKPIs 首卡 {label:资源类型数, value:4, unit:类, change:0})',
        'repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:605-612 (overviewKPIs.map -> KPICard 渲染)',
        'repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:631 (收起态文案「资源类型与数量」)',
        'repos/demo-ui-science/src/pages/data-resources/mockData.js:6-11 (resourceTypeDistribution 4 类——KPI 与分布同源)',
    ],
    'requirement_trace': {
        'named_in_srs': True,
        'srs_anchor': '总体视窗 seq 330 资源接入情况总览：可一键展示当前已接入的所有科技数据资源**类型与数量**……',
        'main_req_anchor': '主需求 :2489（与 seq 330 同文）',
        'note': '「类型与数量」在需求原文有立项级锚（seq 330/:2489——与 065「分布比例」同句）；「资源类型数」是「类型」的枚举计数形态——但枚举域（主轴）无定义',
    },
    'facts': facts,
    'derived': derived,
    'absence_probe': absence,
    'support_judgment': '部分支持',
    'notes': [
        '判档：表级要素域轴候选面 gkx 实算在（dwd 前缀 COUNT DISTINCT）——但「资源×类型」登记面三源零承载 + 类型主轴未裁（065 双轴断裂）→ 部分支持',
        'mock 披露：KPI 卡 4 类与饼图 4 类同源一致（枚举计数=分布类数——065/066 同轴同源）；但同文件 dataType 值域 9 类（5 要素+4 形态并存）——KPI 的 4 只计存储形态子轴，双轴断裂承 065；change:0（类型数环比 0%——静态枚举语义）',
        '表级候选披露：gkx dwd 主要素域轴白名单 15 域在册、实匹配域数见 derived[1]（org 58/patent 13/scholar 12 等为大域）——要素域轴可数但与 UI 存储形态轴不同轴，两轴映射无登记，近似值与 UI 演示值 4 语义不同，不可直接转正',
        'B11 对账：dev 542/16 schema、gkx 280 与 lane7/036 逐键一致；久新 210→215 漂移承 063；4 与 065 件饼图类数对账一致',
    ],
    'base_years_used': [],
    'base_years_missing': [],
    'base_years_note': '本件为存量枚举型（类型数无年度序列需求；change:0 静态语义）',
    'ctx_refs': {
        'note': '正文引用型数字登记（外部参照/跨件引用）',
        'refs': ['542', '280', '210', '215', '1032', '930', '4', '9', '16'],
    },
}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', OUT)
print(json.dumps({
    'mock_kpi': 4,
    'mock_domain_file': len(types_in_file),
    'gkx_domain_axis_matched': len([k for k in prefixes if k != 'other']),
    'gkx_domain_covered': gkx_domain_total_covered,
    'domains': {k: len(v) for k, v in sorted(prefixes.items())},
    'judgment': '部分支持',
}, ensure_ascii=False, indent=2))
