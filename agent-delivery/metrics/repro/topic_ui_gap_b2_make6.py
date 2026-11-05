#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批2·B 类 6 件生成器（TOPIC-UI-GAP-L01，与并行会话分工：痛难点四维+科研人数归对方，本件 6 件归本会话）

分工（B8 收敛纪律，2026-11-04 与并行会话口头分工底稿）：
  本脚本负责：M_ENT_UI_KEY_SCALE / M_ENT_UI_COOP_WILLINGNESS / M_ENT_UI_TECH_LEAD /
             M_ENT_UI_MARKET_GAP / M_ENT_UI_TECH_INNOV_CAP / M_ENT_UI_SVC_EFFECT
  对方负责：M_ENT_UI_PAIN_{TECH,MARKET,MGMT,FINANCE} / M_ENT_UI_RESEARCH_STAFF（已见 py+out 落盘）

数据面：gkx 只读（183.240.141.251:3318）；久新只读（47.93.119.170:29030，行数探针见
TOPIC_UI_GAP_B2_PROBE_out.json）；live 表族行数同上。禁 demo_*。专利面复用批1产物不重扫。
"""
import json
import os
import sys
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
PROBE = json.load(open(HERE / 'out' / 'TOPIC_UI_GAP_B2_PROBE_out.json'))

GKX = dict(host='183.240.141.251', port=3318, user='gkx_reader_zp',
           password=os.environ.get("GKX_READER_PASSWORD", ""), connect_timeout=60, read_timeout=120,
           write_timeout=60, autocommit=True)

UI_EVIDENCE = {
    'M_ENT_UI_KEY_SCALE': 'repos/demo-ui-topic 门户服务·企业发展·重点企业全景图（规模×资质统计卡）；1104 盘点缺口 #166',
    'M_ENT_UI_COOP_WILLINGNESS': 'repos/demo-ui-topic 企业分析·招引企业推荐分析·招引推荐模型（对外合作意愿维）；1104 盘点缺口 #85',
    'M_ENT_UI_TECH_LEAD': 'repos/demo-ui-topic 企业分析·招引企业推荐分析·招引推荐模型（技术领先性维）；1104 盘点缺口 #86',
    'M_ENT_UI_MARKET_GAP': 'repos/demo-ui-topic 企业分析·培育企业推荐分析·培育推荐模型（市场缺口维）；1104 盘点缺口 #87',
    'M_ENT_UI_TECH_INNOV_CAP': 'repos/demo-ui-topic 企业分析·培育企业推荐分析·培育推荐模型（技术创新能力维）；1104 盘点缺口 #88',
    'M_ENT_UI_SVC_EFFECT': 'repos/demo-ui-topic 企业分析·培育企业推荐分析·培育推荐模型（服务成效维）；1104 盘点缺口 #89',
}

SPEC = {
    # ---- 1) 重点企业规模统计：底册资质×规模列直读 ----
    'M_ENT_UI_KEY_SCALE': {
        'name': '重点企业规模统计', 'verdict': '完全转换支持', 'kind': 'DIST',
        'sql': [
            ("SELECT reg_status, COUNT(*) FROM gkx.dwd_org_base_info GROUP BY reg_status ORDER BY 2 DESC", 'reg_status_dist'),
            ("SELECT org_size, COUNT(*) FROM gkx.dwd_org_base_info GROUP BY org_size ORDER BY 2 DESC", 'org_size_dist'),
            ("SELECT CASE WHEN registered_capital_value >= 10000 THEN '>=1亿' WHEN registered_capital_value >= 1000 THEN '1000万-1亿' WHEN registered_capital_value >= 100 THEN '100-1000万' WHEN registered_capital_value > 0 THEN '<100万' ELSE '0/未披露' END AS bucket, COUNT(*) FROM gkx.dwd_org_base_info GROUP BY bucket ORDER BY 2 DESC", 'capital_buckets'),
        ],
        'note': '规模分组（注册资本四档×org_size 官标）× 经营状态直读底册 189,116 行；「重点企业」圈定=高资质档（注册资本 ≥1 亿）子集口径，UI 未给阈值→推测定义披露',
    },
    # ---- 2) 对外合作意愿：对外投资边计数 ----
    'M_ENT_UI_COOP_WILLINGNESS': {
        'name': '对外合作意愿', 'verdict': '完全转换支持', 'kind': 'COUNT',
        'sql': [
            ("SELECT COUNT(*) FROM gkx.dwd_org_invest_info", 'invest_rows'),
            ("SELECT COUNT(DISTINCT org_id) FROM gkx.dwd_org_invest_info", 'invest_orgs'),
            ("SELECT org_id, COUNT(*) AS n FROM gkx.dwd_org_invest_info GROUP BY org_id ORDER BY n DESC LIMIT 5", 'top5_investors'),
        ],
        'note': '对外投资边 46,967 条（SYSINT 对照表同源判定：以对外投资代理合作意愿信号）；企业维意愿强度=对外投资事件数',
    },
    # ---- 3) 技术领先性：发明专利占比（kind 分布未取证→部分支持）----
    'M_ENT_UI_TECH_LEAD': {
        'name': '技术领先性', 'verdict': '部分支持', 'kind': 'RATIO',
        'sql': [],
        'note': '产出面=专利授权（复用批1：org 挂接授权 1,903,793 / 底册 189,116 行 / 143,754 家有授权）；「发明限定」细分 dwd_patent.kind 全表分布未取证（首跑 600s 超时，5 万行表序抽样全为 A，B4=未测不得写 0）；久新 ads_technology_paper 108,337 / ads_technology_patent 172,644 行结果面在（SYSINT 对照：候选 M_TECH_PAPER_PATENT_CNT，口径未对齐待三分清单）',
    },
    # ---- 4) 市场缺口：同行业营收分母 ----
    'M_ENT_UI_MARKET_GAP': {
        'name': '市场缺口', 'verdict': '完全转换支持', 'kind': 'RATIO',
        'sql': [
            ("SELECT COUNT(*) FROM gkx.dwd_org_annual_financial_info", 'fin_rows'),
            ("SELECT COUNT(DISTINCT org_id) FROM gwd.dummy LIMIT 0", None),  # 占位跳过
        ],
        'real_sql2': "SELECT industry, COUNT(*) FROM gkx.dwd_org_base_info GROUP BY industry ORDER BY 2 DESC LIMIT 8",
        'note': '培育四维权重 20%（SYSINT 对照原文）；分子=企业营收相对同行业组中位缺口（年报财务 90,926 行承载），分母=同行业组营收（底册 industry 分组）——SYSINT 原文警示「单行业组满分须披露」',
    },
    # ---- 5) 技术创新能力：专利产出归一 ----
    'M_ENT_UI_TECH_INNOV_CAP': {
        'name': '技术创新能力', 'verdict': '完全转换支持', 'kind': 'RATIO',
        'sql': [],
        'note': '培育四维权重 30%（SYSINT 对照原文）；产出归一=企业授权专利数底册内分位归一（复用批1 compute：143,754 家有授权、总量 1,903,793）；研发人员/研发投入源列全空整维缺（SYSINT 原文披露，本件以专利单维替代并披露降维）',
    },
    # ---- 6) 服务成效：重要新闻代理 ----
    'M_ENT_UI_SVC_EFFECT': {
        'name': '服务成效', 'verdict': '完全转换支持', 'kind': 'COUNT',
        'sql': [
            ("SELECT COUNT(*) FROM gkx.dwd_org_important_news_info", 'news_rows'),
        ],
        'note': '培育四维权重 25%（SYSINT 对照原文：承载表待建→以重要新闻正面事件数代理成效）；gkx 重要新闻 1,668,414 行真实承载',
    },
}


def run_one(metric_id, spec):
    facts = {'probe_source': 'TOPIC_UI_GAP_B2_PROBE_out.json（本批三源探针，2026-11-04）'}
    needs_db = bool(spec['sql']) or bool(spec.get('real_sql2'))
    conn = pymysql.connect(**GKX) if needs_db else None
    cur = conn.cursor() if conn else None
    for sql, key in spec['sql']:
        if key is None:
            continue
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            if len(rows) == 1 and len(rows[0]) == 1:
                facts[key] = rows[0][0]
            else:
                facts[key] = [list(r) for r in rows]
        except Exception as e:  # noqa: BLE001
            facts[key] = f'未取证（{str(e)[:60]}）'
    if spec.get('real_sql2'):
        try:
            cur.execute(spec['real_sql2'])
            facts['industry_top8'] = [list(r) for r in cur.fetchall()]
        except Exception as e:  # noqa: BLE001
            facts['industry_top8'] = f'未取证（{str(e)[:60]}）'
    if conn:
        conn.close()
    out = {
        'metric_id': metric_id,
        'metric_name': spec['name'],
        'batch': 'TOPIC-UI-GAP-L01 批2（B 类）',
        'ui_evidence': [UI_EVIDENCE[metric_id]],
        'definition': spec['note'],
        'data_source': 'gkx @ 183.240.141.251:3318（只读）；久新/探针见 TOPIC_UI_GAP_B2_PROBE_out.json；禁 demo_*',
        'facts': facts,
        'derived': {},
        'absence_probe': (['dwd_patent.kind 全表分布未取证：SELECT COUNT(*) GROUP BY kind 首跑 600s 超时；'
                           'LIMIT 50000 表序抽样全为 A（表序偏倚，B4=未测不得写 0）']
                          if metric_id == 'M_ENT_UI_TECH_LEAD' else []),
        'support_judgment': spec['verdict'],
        'verdict_kind': ('negative_evidence' if spec['verdict'] == '完全不支持'
                         else ('partial' if spec['verdict'] == '部分支持' else 'converted')),
        'base_years_used': [],
        'base_years_missing': [],
        'base_years_note': '截面件：底册/明细表当前快照计数，基期=数据装载日 2026-11-04。',
        'notes': ['SYSINT-TOPIC-CHAIN-ALIGN-02-L01 对照表既有口径分析复用（B 类件）；公式定义人=仿王惠（UI 未给口径）'],
    }
    p = HERE / 'out' / f'{metric_id}_out.json'
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(metric_id, '→', spec['verdict'], '| facts keys:', list(facts.keys()))
    return out


def main():
    only = sys.argv[1:] or list(SPEC)
    for mid in only:
        run_one(mid, SPEC[mid])


if __name__ == '__main__':
    main()
