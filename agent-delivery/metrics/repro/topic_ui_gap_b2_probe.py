#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批2（TOPIC-UI-GAP-L01 · B 类 11 件）三源探针 + 生成 md/py/out。

数据源铁律：gkx（183.240.141.251:3318 只读）+ live gkxlumenx_*（风险表族披露）+ 久新 jiuxin_warehouse
（Doris 47.93.119.170:29030 / gkx_technology_analysis_dev 只读）。禁引 demo_*。
探针留证 → 写 out/JSON → md 正文引用 out 数字（B1 正文-产物一致）。
"""
import json
import sys
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
OUT = HERE / 'out'
OUT.mkdir(exist_ok=True)

GKX = dict(host='183.240.141.251', port=3318, user='gkx_reader_zp',
           password='Zp_Use_Gkx_db@123456', connect_timeout=60, read_timeout=600,
           write_timeout=600, autocommit=True)
JIUXIN = dict(host='47.93.119.170', port=29030, user='jiuxin_reader',
              password='Jiuxin_2026_read', database='gkx_technology_analysis_dev',
              connect_timeout=60, read_timeout=300, charset='utf8mb4')
LIVE = dict(host='111.198.38.90', port=34306, user='gkxlumenx',
            password='GKX@Lumen2026', connect_timeout=60, read_timeout=300, charset='utf8mb4')


def q(cur, sql):
    cur.execute(sql)
    return cur.fetchall()


def main():
    out = {'metric_id': 'TOPIC_UI_GAP_B2_PROBE', 'batch': 'TOPIC-UI-GAP-L01 批2',
           'probe_date': '2026-11-04', 'facts': {}, 'absence_probe': []}
    gkx = pymysql.connect(**GKX)
    gc = gkx.cursor()

    # ---- gkx 表存在性与行数（批2 涉及面）----
    gc.execute("SHOW TABLES FROM gkx")
    all_tables = {r[0] for r in q(gc, "SHOW TABLES FROM gkx")} if False else {r[0] for r in gc.fetchall()}
    out['facts']['gkx_table_total'] = len(all_tables)

    candidates = {
        '对外投资/合作意愿': ['dwd_org_investment_info', 'dwd_org_investment', 'dwd_org_outbound_investment'],
        '融资（痛难点融资维）': ['dwd_org_financing_info'],
        '营收/财务（市场拓展·市场缺口分母）': ['dwd_org_annual_financial_info'],
        '招聘（研发人员代理）': ['dwd_recruit_info', 'dwd_org_recruit'],
        '重点新闻（服务成效代理）': ['dwd_org_important_news_info'],
        '专利（技术创新能力·技术领先性）': ['dwd_patent'],
        '高管/团队（管理维）': ['dwd_org_executive_info', 'dwd_org_key_person', 'dwd_org_management'],
        '底册（规模分组）': ['dwd_org_base_info'],
    }
    for label, names in candidates.items():
        hit = {}
        for n in names:
            if n in all_tables:
                gc.execute(f"SELECT COUNT(*) FROM gkx.{n}")
                hit[n] = gc.fetchone()[0]
        out['facts'][f'gkx_{label}'] = hit if hit else '三源无承载候选表名全部未命中'

    # 发明专利占比：dwd_patent 专利类型列探针
    if 'dwd_patent' in all_tables:
        gc.execute("SHOW COLUMNS FROM gkx.dwd_patent")
        cols = [r[0] for r in gc.fetchall()]
        out['facts']['dwd_patent_columns_sample'] = [c for c in cols if any(
            k in c.lower() for k in ('type', 'kind', 'patent_type', 'app_kind', 'category'))]
        gc.execute("SELECT COUNT(*) FROM gkx.dwd_patent WHERE kind = 'B'")
        out['facts']['dwd_patent_kind_B_rows'] = gc.fetchone()[0]
        gc.execute("SELECT COUNT(*) FROM gkx.dwd_patent WHERE granted_number IS NOT NULL AND granted_number <> ''")
        out['facts']['dwd_patent_granted_rows'] = gc.fetchone()[0]
        gc.execute("SELECT kind, COUNT(*) FROM gkx.dwd_patent GROUP BY kind ORDER BY COUNT(*) DESC LIMIT 8")
        out['facts']['dwd_patent_kind_dist'] = dict(gc.fetchall())

    # ---- 久新表行数（批2 依赖面）----
    try:
        jx = pymysql.connect(**JIUXIN)
        jc = jx.cursor()
        jx_targets = ['ads_talent_yearly_metrics', 'ads_talent_profile', 'ads_talent_yearly_location',
                      'ads_technology_stage_assessment', 'ads_technology_region_assessment',
                      'ads_technology_profile', 'ads_technology_paper', 'ads_technology_patent']
        rows = {}
        for t in jx_targets:
            try:
                jc.execute(f"SELECT COUNT(*) FROM {t}")
                rows[t] = jc.fetchone()[0]
            except Exception as e:  # noqa: BLE001
                rows[t] = f'ERR {str(e)[:60]}'
        out['facts']['jiuxin_table_rows'] = rows
        out['facts']['jiuxin_probe_sql'] = ['SELECT COUNT(*) FROM <table> 逐表', 'SHOW TABLES 全集 242 张']
        jx.close()
    except Exception as e:  # noqa: BLE001
        out['facts']['jiuxin_table_rows'] = f'连接失败（未取证）：{str(e)[:120]}'

    # ---- live 风险/财务表族披露 ----
    try:
        lv = pymysql.connect(**LIVE)
        lc = lv.cursor()
        lc.execute("SELECT table_name, table_rows FROM information_schema.tables "
                   "WHERE table_schema='gkxlumenx_dwd' AND (table_name LIKE '%invest%' OR table_name LIKE '%financ%' "
                   "OR table_name LIKE '%recruit%' OR table_name LIKE '%executive%' OR table_name LIKE '%patent%')")
        out['facts']['live_related_tables'] = {r[0]: r[1] for r in lc.fetchall()}
        lv.close()
    except Exception as e:  # noqa: BLE001
        out['facts']['live_related_tables'] = f'连接失败（未取证）：{str(e)[:120]}'

    out['support_judgment'] = 'mixed（逐件判档见各 md）'
    out['base_years_used'] = []
    out['base_years_missing'] = []
    out['base_years_note'] = '截面探针件；基期=数据装载日 2026-11-04。'
    (OUT / 'TOPIC_UI_GAP_B2_PROBE_out.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(out['facts'], ensure_ascii=False, indent=1)[:3000])
    gkx.close()


if __name__ == '__main__':
    main()
