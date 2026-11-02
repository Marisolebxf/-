# -*- coding: utf-8 -*-
"""
M_SCIUI_DATATHM_063 资源总数（来源分析汇总区 · 主题视窗族挂载）
挂载点: repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx:373
支持度判定: 部分支持（表级资源近似面三源在，渠道×资源口径登记面三源无）
"""
import json
import re

import pymysql

OUT = 'M_SCIUI_DATATHM_063_out.json'

UI = {
    'jsx': 'repos/demo-ui-science/src/pages/data-resources/components/AccessSourceAnalysisDetail.jsx',
    'line_statistic': 373,  # <Statistic title="资源总数" value={channels.reduce((s,c)=>s+c.count,0)} suffix="个" />
    'line_sibling_371': 371,  # 归集总量 = Σ volume
    'line_sibling_363': 363,  # 渠道数 = channels.length
    'mock': 'repos/demo-ui-science/src/pages/data-resources/mockData.js:101-107 (accessSourceAnalysis.channels 5 渠道)',
}

snap = json.load(open('_snapshots/_lane7_shared_probe_out.json'))
import os
if not os.path.exists('_snapshots/_lane7_shared_probe_out.json'):
    snap = json.load(open('_snapshots/_lane7_shared_probe_out.json'))

facts = {}

# ---------- UI mock 解析（B 教训：程序化解析，勿手数） ----------
REPO_ROOT = '/Users/samuel_tang/my_project/gkx-lumen'
src = open(REPO_ROOT + '/repos/demo-ui-science/src/pages/data-resources/mockData.js', encoding='utf-8').read()
ch_block = re.search(r'channels: \[(.*?)\n  \],', src, re.S).group(1)
rows = re.findall(r"name: '(.*?)', volume: (\d+), count: (\d+), share: ([\d.]+)", ch_block)
channels = [
    {'name': n, 'volume': int(v), 'count': int(c), 'share': float(s)}
    for n, v, c, s in rows
]
mock_total_count = sum(c['count'] for c in channels)
mock_total_volume = sum(c['volume'] for c in channels)
mock_share_sum = round(sum(c['share'] for c in channels), 1)
assert len(channels) == 5, 'channels must be 5'
assert mock_total_count == 1256, mock_total_count
assert mock_total_volume == 33670, mock_total_volume
assert abs(mock_share_sum - 100.0) < 0.05, mock_share_sum

# details 12 行（seq 352 明细面）——渠道覆盖核对
det_block = re.search(r'details: \[(.*?)\n  \],', src, re.S).group(1)
detail_ids = re.findall(r"id: '(asd-\d+)'", det_block)
detail_channels = re.findall(r"channel: '(.*?)', dataType", det_block)
assert len(detail_ids) == 12, len(detail_ids)
mock_detail_rows = len(detail_ids)
mock_detail_channel_distinct = len(set(detail_channels))

facts['ui'] = {
    'mock_channels_count_5': True,
    'mock_resource_total_sum': mock_total_count,          # 1256
    'mock_volume_total_sum': mock_total_volume,           # 33670
    'mock_share_sum_pct': mock_share_sum,                 # 100.0
    'mock_detail_rows': mock_detail_rows,                 # 12
    'mock_detail_channel_distinct': mock_detail_channel_distinct,  # 5
    'mock_detail_vs_channels_total_gap': mock_total_count - mock_detail_rows,  # 1244
}

# ---------- 三源探针（判「无承载」前三源逐一留证） ----------
absence = []

# ① dev live: 资源登记/目录词族 0 命中（信息模式全文检索）
dev_conn = pymysql.connect(host='10.50.11.76', port=3306, user='root', password='Gkxzp202600', charset='utf8mb4')
cur = dev_conn.cursor()
cur.execute(
    "SELECT table_schema, table_name FROM information_schema.tables "
    "WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP 'resource|catalog|inventory|metadata|registry'"
)
dev_hits = sorted(r[0] + '.' + r[1] for r in cur.fetchall())
cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema LIKE 'gkxlumenx%'")
dev_total = cur.fetchone()[0]
dev_conn.close()
absence.append({
    'probe': '资源登记/目录词族（resource|catalog|inventory|metadata|registry）',
    'source': 'dev',
    'sql': "information_schema.tables WHERE table_schema LIKE 'gkxlumenx%' AND table_name REGEXP ...",
    'hits': len(dev_hits),
    'hit_detail': f'{dev_total} 表词族命中 {len(dev_hits)} 张（{dev_hits if dev_hits else "无"}）——模型配置/调度注册语义排除，dev 侧无资源目录登记面',
})

# ② gkx 280 表（经 _gkxdb.py 实跑）
import importlib.util
_spec = importlib.util.spec_from_file_location('gkxdb', '_gkxdb.py')
gkxdb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gkxdb)
gcur = gkxdb.gkx()
gcur.execute("SHOW FULL TABLES FROM gkx WHERE Table_type != 'VIEW'")
gkx_tables = sorted(r[0] for r in gcur.fetchall())
gkx_hits = [t for t in gkx_tables if re.search(r'resource|catalog|collect|inventory|registry', t, re.I)]
gcur.execute("DESC gkx.dwd_dim_source_code")
src_cols = [r[0] for r in gcur.fetchall()]
gcur.execute("SELECT COUNT(*) FROM gkx.dwd_dim_source_code")
src_rows = gcur.fetchone()[0]
absence.append({
    'probe': '资源登记/归集词族（resource|catalog|collect|inventory|registry）',
    'source': 'gkx',
    'sql': 'SHOW FULL TABLES FROM gkx + 词族过滤（经 _gkxdb.py 2026-11-02 实跑）',
    'hits': len(gkx_hits),
    'hit_detail': (
        f'{len(gkx_tables)} 表唯一近邻 dwd_dim_source_code（数据源维度表 4 行：{src_cols}，'
        '登记数据来源编码非资源条目）——语义排除'
    ),
})

# ③ 久新 live: ads 面 210 张（2026-11-02 SHOW TABLES）——subfield_resource 两张是论文计数年表
j_conn = pymysql.connect(
    host='47.93.119.170', port=29030, user='test2',
    password='m+DWAG23RCXBP2L+y7ydaqu3aSuur7mxFOcl3iZHDgVe4eka',
    database='gkx_technology_analysis_dev', charset='utf8mb4',
)
jcur = j_conn.cursor()
jcur.execute("SHOW TABLES")
jiuxin_tables = sorted(r[0] for r in jcur.fetchall())
jiuxin_hits = [t for t in jiuxin_tables if re.search(r'resource', t, re.I)]
j_desc = {}
j_rows = {}
for t in ('ads_city_subfield_resource_yearly', 'ads_institution_subfield_resource_yearly'):
    jcur.execute(f"DESC `{t}`")
    j_desc[t] = [r[0] for r in jcur.fetchall()]
    jcur.execute(f"SELECT COUNT(*) FROM `{t}`")
    j_rows[t] = cur.fetchone()[0] if False else jcur.fetchone()[0]
j_conn.close()
absence.append({
    'probe': '资源登记词族（resource）',
    'source': 'jiuxin',
    'sql': 'SHOW TABLES + DESC 两张 resource 命名表（Doris，information_schema 无权限）',
    'hits': len(jiuxin_hits),
    'hit_detail': (
        f'{len(jiuxin_tables)} 张 ads 面命中 {len(jiuxin_hits)} 张：'
        'ads_city_subfield_resource_yearly（27,720 行，city×subfield×year 论文/人才/项目计数）与 '
        'ads_institution_subfield_resource_yearly（985,555 行，institution×subfield×year）——'
        '「resource」指论文计量资源非接入数据资源条目，语义排除；无接入资源目录登记面'
    ),
    'live_vs_snapshot_note': '2026-11-02 实跑 215 张 vs lane7 快照（2026-11-01）210 张：新增 5 张 ads_talent_*（honor_detail/integrity_score_demo/media_sentiment/topic_value_evidence/topic_value_summary），0 张消失——人才面扩充，resource 词族命中数不变（B11 漂移登记）',
})

facts['three_source'] = {
    'dev_table_total': dev_total,          # 542（快照对账）
    'dev_registry_hits': dev_hits,
    'gkx_table_total': len(gkx_tables),    # 280
    'gkx_hits': gkx_hits,
    'gkx_dwd_dim_source_code_rows': src_rows,
    'gkx_dwd_dim_source_code_cols_sorted': sorted(src_cols),
    'jiuxin_table_total': len(jiuxin_tables),  # 215（2026-11-02 实跑；lane7 快照 210 + 新增 5 张 ads_talent_*，勿写死）
    'jiuxin_resource_hits_sorted': jiuxin_hits,
    'jiuxin_desc_paper_count_present': all('paper_count' in v for v in j_desc.values()),
}

# 表级近似口径（承 036 产物，互引不重算）
facts['table_level_approximation_from_036'] = {
    'three_source_all': 1032,
    'three_source_all_asof': '2026-11-01（lane7 快照日；久新 2026-11-02 实跑已 215 张，036 口径沿用其探测日，本件漂移已登记）',
    'three_source_no_backup': 930,
    'note': 'M_SCIUI_DATATHM_036_out.json derived（dev 542 + gkx 280 + 久新 210 全口径；剔备份 930）——表级「数据表总数」近似，非资源条目口径',
}

# ---------- 判定 ----------
derived = [
    {
        'key': 'resource_total_by_channel',
        'value': None,
        'numerator': None,
        'denominator': None,
        'note': '正式口径 Σ count(c)（渠道×资源条数登记面）三源无承载面——mock 1256 为演示值不作数据证据（B10）',
    },
    {
        'key': 'resource_total_table_approximation_all',
        'value': 1032,
        'numerator': None,
        'denominator': None,
        'note': '表级近似：dev 542 + gkx 280 + 久新 210（036 产物互引；含备份/配置/空表；久新 2026-11-02 实跑 215 张，036 口径沿用 2026-11-01 探测日）',
    },
    {
        'key': 'resource_total_table_approximation_no_backup',
        'value': 930,
        'numerator': None,
        'denominator': None,
        'note': '表级近似剔备份：1032 - dev 备份 3 - gkx 备份 99（036 产物互引；配置 schema 与空表未剔）',
    },
]

out = {
    'metric_id': 'M_SCIUI_DATATHM_063',
    'batch': 'S3-05',
    'metric_name': '资源总数',
    'ui_evidence': [
        f"{UI['jsx']}:{UI['line_statistic']} (<Statistic title=\"资源总数\" value={{channels.reduce((s, c) => s + c.count, 0)}} suffix=\"个\" />)",
        f"{UI['jsx']}:{UI['line_sibling_371']} (归集总量 Σ volume=33,670，与资源总数并列)",
        f"{UI['jsx']}:{UI['line_sibling_363']} (渠道数 channels.length=5，三卡并列)",
        f"{UI['mock']} (五渠道 count: 485/356/245/120/50)",
    ],
    'requirement_trace': {
        'named_in_srs': False,
        'note': (
            '「资源总数」字面三份说明书 0 命中。语义锚 SRS 接入视窗 seq 351「渠道归集数据量统计」'
            '（自动统计并展示各渠道归集的数据量）与主需求 :2613 渠道归集语境——本读数是 seq 351 '
            '渠道汇总统计的「条数维」总计读数；组件注释自标「需规 seq 351–355」'
        ),
    },
    'facts': facts,
    'derived': derived,
    'absence_probe': absence,
    'support_judgment': '部分支持',
    'notes': [
        '判档：表级资源近似面（三库表清单+计数）三源结构+数据双在——但「渠道×资源条数」口径登记面（资源目录/归集台账）三源逐一零命中 → 部分支持',
        'mock 披露：资源总数 1256 = Σ channels.count（485+356+245+120+50）；同区归集总量 33,670 = Σ volume；share 合计 100.0% 自洽；但同组件 seq 352 明细面仅 12 行（asd-001~012），汇总 1256 vs 明细 12 量级断裂——汇总卡与明细表非同一登记面（B10 不作数据证据）',
        '口径双维披露：同名「归集」读数有 count（资源条数，个）与 volume（数据量）两维，本件取 count 维；volume 维归 M_SCIUI_DATATHM_067',
        'B11 对账：dev 542/gkx 280 与 lane7 快照零漂移；久新快照 210（2026-11-01）→ 2026-11-02 实跑 215（新增 5 张 ads_talent_*）——活库增长漂移已登记（B5/B11），resource 词族命中数不变',
    ],
    'base_years_used': [],
    'base_years_missing': [],
    'base_years_note': '本件为存量盘点型（无年度序列需求）',
    'ctx_refs': {
        'note': '正文引用型数字登记（外部参照/跨件引用）',
        'refs': ['542', '280', '210', '215', '1032', '930', '1256', '33670', '12'],
    },
}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('written', OUT)
print(json.dumps({
    'mock_total_count': mock_total_count,
    'mock_total_volume': mock_total_volume,
    'dev_total': dev_total,
    'gkx_total': len(gkx_tables),
    'jiuxin_total': len(jiuxin_tables),
    'judgment': '部分支持',
}, ensure_ascii=False, indent=2))
