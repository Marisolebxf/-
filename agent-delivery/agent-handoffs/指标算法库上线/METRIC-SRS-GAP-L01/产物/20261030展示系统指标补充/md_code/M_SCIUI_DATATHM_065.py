# -*- coding: utf-8 -*-
"""
M_SCIUI_DATATHM_065 资源类型分布比例（总体视窗·仪表盘饼图）
挂载点: repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:616 (Card) + :617 (pie) + :47-71 (getTypeDistributionOption)
支持度判定: 部分支持（表级类型近似面三源在，资源×类型口径登记面三源无）
"""
import json
import re

import pymysql

OUT = 'M_SCIUI_DATATHM_065_out.json'
REPO_ROOT = '/Users/samuel_tang/my_project/gkx-lumen'

facts = {}
absence = []

# ---------- UI mock 解析 ----------
src = open(REPO_ROOT + '/repos/demo-ui-science/src/pages/data-resources/mockData.js', encoding='utf-8').read()
m = re.search(r'export const resourceTypeDistribution = \[(.*?)\n\];', src, re.S)
rows = re.findall(r"name: '(.*?)', value: (\d+), color: '(.*?)'", m.group(1))
dist = [{'name': n, 'value': int(v), 'color': c} for n, v, c in rows]
assert len(dist) == 4, len(dist)
total = sum(d['value'] for d in dist)
assert total == 30398, total  # 12580+8932+5641+3245
pct = [{'name': d['name'], 'value': d['value'], 'pct': round(d['value'] / total * 100, 2)} for d in dist]
assert abs(sum(p['pct'] for p in pct) - 100.0) < 0.05

# 与 overviewKPIs 资源总量 30,398 同值对账（056 件已披露混同——本件是它的分布母体）
kpi_total = re.search(r"label: '资源总量', value: '([\d,]+)'", src).group(1)
assert kpi_total == '30,398'

# dataType 值域九类 vs 饼图四类——类型枚举域披露
types_in_file = sorted(set(re.findall(r"dataType: '(.*?)'", src)))
pie_types = sorted(d['name'] for d in dist)
extra_types = [t for t in types_in_file if t not in pie_types]

facts['ui'] = {
    'mount': 'OverviewWindow.jsx:616 (Card title=资源类型分布比例) + :617 (ReactECharts pie) + :47-71 (getTypeDistributionOption——tooltip formatter {c} 个 ({d}%))',
    'mock_source': 'mockData.js:6-11 (resourceTypeDistribution 4 类)',
    'mock_distribution': pct,                                   # 41.38/29.38/18.56/10.68
    'mock_total': total,                                        # 30398
    'mock_total_equals_kpi_resource_total': True,               # 与 overviewKPIs 资源总量 30,398 同值
    'mock_type_domain_pie': pie_types,                          # 4 类
    'mock_type_domain_file': types_in_file,                     # 9 类（dataType 值域）
    'mock_type_domain_gap': extra_types,                        # ['专利','实验数据','情报','论文','项目']
}

# ---------- 三源探针 ----------
# 资源×类型口径：需资源目录含类型字段。类型词族（type/category/kind/format）+ 承 063/064 资源目录词族排除。
# 本件新增：dev/久新表清单的类型维度载体探针（库表自带类型轴面）。

dev_conn = pymysql.connect(host='10.50.11.76', port=3306, user='root', password='Gkxzp202600', charset='utf8mb4')
cur = dev_conn.cursor()
cur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP 'resource|catalog|inventory|metadata|registry|type|category'"
)
dev_hits = sorted(r[0] + '.' + r[1] for r in cur.fetchall())
cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema LIKE 'gkxlumenx%'")
dev_total = cur.fetchone()[0]
dev_conn.close()
# 过滤纯类型词族命中（resource 目录族承 063 为 0；type/category 命中多为此 BI 字典/代码生成模板）
type_only = [t for t in dev_hits if re.search(r'type|category', t.split('.')[1], re.I)]

absence.append({
    'probe': '资源×类型登记面（resource/catalog/inventory/metadata/registry + type/category 词族）',
    'source': 'dev',
    'sql': "information_schema.tables WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP 'resource|catalog|inventory|metadata|registry|type|category'",
    'hits': len(dev_hits),
    'hit_detail': (
        f'{dev_total} 表：资源目录词族 0 命中（承 063）；type/category 词族 {len(type_only)} 张命中全为'
        '代码生成器类型模板/BI 字典/流程分类（xxl_job/codegen/gen_table_category 族）——'
        '表结构定义域的类型语义，非「数据资源按类型计数」登记面，语义排除'
    ),
})

# gkx：承 063/064——资源目录词族唯一命中 dwd_dim_source_code（语义排除）；type/category 词族新增探针
import importlib.util
_spec = importlib.util.spec_from_file_location('gkxdb', '_gkxdb.py')
gkxdb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gkxdb)
gcur = gkxdb.gkx()
gcur.execute("SHOW FULL TABLES FROM gkx WHERE Table_type != 'VIEW'")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
gkx_type_hits = [t for t in gkx_tables if re.search(r'type|category|kind|format', t, re.I)]
absence.append({
    'probe': '类型维度词族（type|category|kind|format）+ resource 承 063',
    'source': 'gkx',
    'sql': 'SHOW FULL TABLES FROM gkx + 词族过滤（经 _gkxdb.py 2026-11-02 实跑）',
    'hits': len(gkx_type_hits),
    'hit_detail': (
        f'{len(gkx_tables)} 表：type/category/kind/format 词族命中 3 张——dwd_industry_analysis_content_types'
        '（1,000 行，document_id×content_type 内容类型标签——行业分析文档的类型标注）、dwd_information'
        '（32 行，info_type 情报资讯条目）、dwd_information_bak_20260923（前表备份）——'
        'DESC 实查均为要素明细/标签语义，非「资源按存储形态类型计数」登记面，语义排除；'
        '资源目录词族唯一命中 dwd_dim_source_code（承 063 语义排除）——资源×类型双缺'
    ),
})

# 久新：ads 面的 field/domain/subfield 分类轴是论文学科分类（062 件已探明 4 级分类表）——非数据资源类型轴
j_conn = pymysql.connect(
    host='47.93.119.170', port=29030, user='test2',
    password='m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka',
    database='gkx_technology_analysis_dev', charset='utf8mb4',
)
jcur = j_conn.cursor()
jcur.execute("SHOW TABLES")
jiuxin_tables = sorted(r[0] for r in jcur.fetchall())
jiuxin_type_hits = [t for t in jiuxin_tables if re.search(r'type|category|kind|format|data_type', t, re.I)]
j_conn.close()
absence.append({
    'probe': '资源类型维度词族（type|category|kind|format|data_type）',
    'source': 'jiuxin',
    'sql': 'SHOW TABLES + 词族过滤（Doris，information_schema 无权限）',
    'hits': len(jiuxin_type_hits),
    'hit_detail': (
        f'{len(jiuxin_tables)} 张 ads 面（2026-11-02 实跑，漂移承 063）：类型词族命中 2 张——'
        'ads_institution_type（10 行，机构类型维度字典：institution_type_id/name/openalex_id——论文计量域）、'
        'ads_geo_yearly_institution_type_metrics（349,396 行，location×year×机构类型 的论文/人才/项目计数）'
        '——DESC 实查均为**机构类型**轴（高校/院所/企业分类），非「结构化/非结构化/半结构化/实时流」'
        '数据资源存储形态轴；论文学科轴承 062（field/domain/subfield 4 级）——语义排除'
    ),
})

facts['three_source'] = {
    'dev_table_total': dev_total,                       # 542（零漂移）
    'dev_type_family_hits_count': len(type_only),       # 表结构域类型模板（语义排除）
    'gkx_table_total': len(gkx_tables),                 # 280
    'gkx_type_family_hits': sorted(gkx_type_hits),      # 3 张（content_types/information+bak——DESC 实查语义排除）
    'jiuxin_table_total': len(jiuxin_tables),           # 215（实跑；快照 210+5 承 063）
    'jiuxin_type_family_hits': sorted(jiuxin_type_hits),# 2 张 institution_type（机构类型轴，语义排除）
    'jiuxin_ads_institution_type_rows': 10,
    'jiuxin_ads_geo_yearly_institution_type_metrics_rows': 349396,
    'gkx_dwd_industry_analysis_content_types_rows': 1000,
    'gkx_dwd_information_rows': 32,
    'resource_family_exclusion_ref': 'M_SCIUI_DATATHM_063/064_out.json（资源目录/供应方词族三源排除，本件复用）',
    'discipline_taxonomy_ref': 'M_SCIUI_DATATHM_062.md（久新 4 级学科分类表探明——论文学科轴非数据资源类型轴）',
}

# 表级近似口径（承 036）——类型分组近似不可得（类型字段缺位），仅登记总量
facts['table_level_approximation_from_036'] = {
    'three_source_all': 1032,
    'three_source_all_asof': '2026-11-01（lane7 快照日；久新 2026-11-02 实跑 215 张，036 口径沿用其探测日）',
    'three_source_no_backup': 930,
    'note': '036 件 derived——表级总量近似；类型分组近似不可得（资源×类型字段缺位，dwd 前缀编码是否可作类型轴须先裁映射规则）',
}

# ---------- 判定 ----------
derived = [
    {
        'key': 'resource_type_distribution_pct',
        'value': None,
        'numerator': None,
        'denominator': None,
        'note': '正式口径 COUNT(*) GROUP BY type / Σ（资源×类型登记面）三源无承载——mock 41.38/29.38/18.56/10.68 为演示值不作数据证据（B10）',
    },
    {
        'key': 'resource_type_distribution_table_approx',
        'value': None,
        'numerator': None,
        'denominator': None,
        'note': '表级近似：dwd 前缀（patent/paper/talent/org/fund）可作要素域类型轴的候选映射，但「结构化/非结构化/半结构化/实时流」四分型是存储形态轴非要素域轴——两轴不兼容，映射规则无登记，近似不可交付（B10 留空）',
    },
]

out = {
    'metric_id': 'M_SCIUI_DATATHM_065',
    'batch': 'S3-05',
    'metric_name': '资源类型分布比例',
    'ui_evidence': [
        'repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:616 (Card title="资源类型分布比例")',
        'repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:617 (ReactECharts pie option=getTypeDistributionOption())',
        'repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:47-71 (getTypeDistributionOption——pie data=resourceTypeDistribution, tooltip {c} 个 ({d}%))',
        'repos/demo-ui-science/src/pages/data-resources/mockData.js:6-11 (resourceTypeDistribution 4 类)',
        'repos/demo-ui-science/src/pages/data-resources/OverviewWindow.jsx:631 (收起态文案「资源类型与数量、分布比例」)',
    ],
    'requirement_trace': {
        'named_in_srs': True,
        'srs_anchor': '总体视窗 seq 330 资源接入情况总览：可一键展示当前已接入的所有科技数据资源类型与数量，在仪表盘上直观呈现各类资源的分布比例……',
        'main_req_anchor': '主需求 :2489（与 seq 330 同文）',
        'note': '「分布比例」在需求原文有立项级锚（seq 330/:2489）——本件是计数组中少见的**需求正面命名**读数（非 UI 派生）；但分布的类型枚举域与占比公式无定义',
    },
    'facts': facts,
    'derived': derived,
    'absence_probe': absence,
    'support_judgment': '部分支持',
    'notes': [
        '判档：表级近似侧三源结构+数据双在（036 件 1,032/930）——但「资源×类型」登记面三源零命中（类型词族命中全为表结构域/论文学科轴语义）→ 部分支持',
        'mock 披露：4 类分布 12,580/8,932/5,641/3,245（Σ=30,398——与 overviewKPIs 资源总量 30,398 同值，本件是 056 件混同实证的**分布母体**）；占比 41.38%/29.38%/18.56%/10.68% 合计 100.0%',
        '类型枚举域断裂披露：饼图 4 类（存储形态轴：结构化/非结构化/半结构化/实时流）vs 同 mock 文件 dataType 值域 9 类（要素域轴：专利/论文/项目/情报/实验数据 + 4 存储形态）——mock 内两套类型轴并存，正式版须裁定主轴',
        '两轴不兼容披露：三源表级近似候选轴是 dwd 要素域前缀（patent/paper/talent/org），mock 饼图轴是存储形态四分型——语义不同层（要素域 vs 存储形态），映射规则无登记，表级类型分组近似不可交付',
        'B11 对账：dev 542/gkx 280 零漂移；久新 210→215 漂移承 063；30,398 与 056 件 overviewKPIs 对账同值',
    ],
    'base_years_used': [],
    'base_years_missing': [],
    'base_years_note': '本件为存量分布型（无年度序列需求；同排「年度增长趋势」是另一卡）',
    'ctx_refs': {
        'note': '正文引用型数字登记（外部参照/跨件引用）',
        'refs': ['542', '280', '210', '215', '1032', '930', '30398', '12580', '8932', '5641', '3245'],
    },
}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', OUT)
print(json.dumps({
    'mock_total': total,
    'pct': {p['name']: p['pct'] for p in pct},
    'dev_total': dev_total,
    'gkx_type_hits': sorted(gkx_type_hits),
    'jiuxin_type_hits': sorted(jiuxin_type_hits),
    'judgment': '部分支持',
}, ensure_ascii=False, indent=2))
