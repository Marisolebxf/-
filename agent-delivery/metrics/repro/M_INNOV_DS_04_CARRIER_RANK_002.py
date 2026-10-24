#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_DS_04_CARRIER_RANK_002 多维度排名展示 · 复现代码（20261021 INNOV-c 批）

口径：王惠 V1.5（本指标 calc-logic 原文「同 M_INNOV_CARRIER_RANK_GLOBAL-创新载体多维度排名」）。
按铁律「已有 out.json 先读复用、禁重跑探针」：
  ① 读 code/M_INNOV_CARRIER_RANK_GLOBAL_out.json（三宇宙名次）与
     code/M_INNOV_CARRIER_INDEX_GLOBAL_out.json（名次内核指数）；
  ② 当日 gkx 轻量校验：载体三源行数与年报资源维空值率；
  ③ 按「多维度排名展示」页面视角重组：总体/地区/领域三宇宙的排名覆盖、零分带规模、
     头部跨宇宙一致性、名次位置（百分位）与并列规模。
输出：code/M_INNOV_DS_04_CARRIER_RANK_002_out.json
"""
import json
import os

import pymysql

HERE = os.path.dirname(os.path.abspath(__file__))
UP_RANK = os.path.join(HERE, 'M_INNOV_CARRIER_RANK_GLOBAL_out.json')
UP_IDX = os.path.join(HERE, 'M_INNOV_CARRIER_INDEX_GLOBAL_out.json')
GKX = dict(host='183.240.141.251', port=3318, user='gkx_reader_zp',
           password='Zp_Use_Gkx_db@123456', database='gkx', charset='utf8mb4',
           connect_timeout=20, read_timeout=600)


def verify_probes():
    p = {}
    conn = pymysql.connect(**GKX)
    cur = conn.cursor()
    for t in ['dwd_org_base_info', 'dwd_research_institute_base_info', 'dwd_forg_base_info',
              'dwd_org_tech_tag', 'dwd_org_annual_financial_info']:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        p[f'gkx.{t}'] = int(cur.fetchone()[0])
    cur.execute("SELECT SUM(development_employee IS NULL), COUNT(*) FROM dwd_org_annual_financial_info")
    nul, n = cur.fetchone()
    p['gkx.dwd_org_annual_financial_info.dev_null_pct'] = round(int(nul or 0) / int(n) * 100, 2)
    conn.close()
    return p


DEST = os.path.join(HERE, 'M_INNOV_DS_04_CARRIER_RANK_002_out.json')


def source_unreachable(err):
    """源不可达时不覆盖已归档结果：打印存档摘要并以 0 退出（可复现性保护）。"""
    if not os.path.exists(DEST):
        return False
    arch = json.load(open(DEST, encoding='utf-8'))
    print(f'[SKIP] gkx 不可达（{type(err).__name__}: {str(err)[:90]}）')
    print(f'[SKIP] 已归档结果保持不变：{DEST}')
    print(json.dumps({k: arch.get(k) for k in
                      ('metric_id', 'metric_name', 'support_judgment', 'probe_date')},
                     ensure_ascii=False, indent=1))
    print('      复跑需连通 gkx 183.240.141.251:3318；本脚本不重跑大表探针。')
    return True


def main():
    rank = json.load(open(UP_RANK, encoding='utf-8'))
    idx = json.load(open(UP_IDX, encoding='utf-8'))
    try:
        probes = verify_probes()
    except Exception as e:  # gkx 不可达时保护存档
        if source_unreachable(e):
            return
        raise

    rc = rank['compute']
    ic = idx['compute']
    n = rc['n_carriers']
    n_ranked = rc['global_rank']['n_ranked']
    positive = ic['stats']['positive']
    zero_band = n - positive
    top10 = rc.get('top10_global') or []
    regions = rc.get('region_rank') or []
    fields = rc.get('field_rank_demo') or []

    # 名次位置（百分位）与并列规模：零分带内部并列于同一 RANK
    top10_view = [dict(name=t['name'], src=t['src'], score=t['score'], rank=t['rank'],
                       pct_position=round(t['rank'] / n_ranked * 100, 3)) for t in top10]
    sz = next((r for r in regions if str(r.get('city', '')).startswith('深圳')), None)
    multi_universe_heads = [t['name'] for t in top10[:5]]

    universes = dict(
        global_n=n_ranked,
        region_slices=len(regions),
        region_top5=[dict(city=r['city'], n=r['n_carriers'], head=r['top1_name'],
                          head_score=r['top1_score']) for r in regions[:5]],
        field_slices=len(fields),
        field_demo=[dict(ipc4=r['ipc4'], n=r['n_carriers'], head=r['top1_name'],
                         head_score=r['top1_score']) for r in fields],
    )

    ok = n_ranked >= 100 and len(regions) >= 3 and len(fields) >= 1
    if ok:
        judgment = '部分支持'
        note = (f"三宇宙名次均可产出（总体 {n_ranked}、地区切片 {len(regions)}、领域演示 {len(fields)}），"
                f"零分带 {zero_band} 家并列（占比 {round(zero_band / n * 100, 2)}%）；"
                f"但名次内核指数依赖资源维，当日 gkx 年报 development_employee 空值率 "
                f"{probes['gkx.dwd_org_annual_financial_info.dev_null_pct']}%，"
                f"且海外切片全零分 → 排名链路可算、指数语义被削弱 → 部分支持")
    else:
        judgment = '完全不支持'
        note = '名次宇宙不足'

    out = {
        'metric_id': 'M_INNOV_DS_04_CARRIER_RANK_002',
        'metric_name': '多维度排名展示',
        'also_known_as': 'M_INNOV_CARRIER_RANK_GLOBAL（王惠 calc-logic：同口径，步骤完全一致）',
        'method': ('复用上游 RANK_GLOBAL 实测（RANK(index_score)，总体/地区/领域三宇宙，同分同名次跳号），'
                   '本脚本按「多维度排名展示」页面视角重组：名次覆盖、零分带、跨宇宙头部一致性、名次百分位'),
        'reuse_policy': '遵守铁律「已有 out.json 先读复用，禁重跑探针」',
        'derived_from': ['code/M_INNOV_CARRIER_RANK_GLOBAL_out.json',
                         'code/M_INNOV_CARRIER_INDEX_GLOBAL_out.json'],
        'probes_today': probes,
        'compute': {
            'n_carriers': n, 'n_ranked': n_ranked, 'positive_index': positive,
            'zero_band': zero_band, 'zero_band_pct': round(zero_band / n * 100, 2),
            'universes': universes,
            'top10_with_pct_position': top10_view,
            'shenzhen_slice': sz,
            'cross_universe_heads': multi_universe_heads,
            'probes_upstream': rank.get('probes'),
        },
        'support_judgment': judgment,
        'support_note': note,
        'support_consistent_with_upstream': judgment == rank.get('support_judgment'),
    }
    dest = os.path.join(HERE, 'M_INNOV_DS_04_CARRIER_RANK_002_out.json')
    json.dump(out, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    print('saved', dest)
    print(json.dumps({k: v for k, v in out.items() if k != 'compute'}, ensure_ascii=False, indent=1))
    print(json.dumps(out['compute'], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
