#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_INNOV_DS_04_CARRIER_RANK_002 多维度排名展示
# 【维护者】唐绍祖
# 【适用系统】科技专题系统 + 科技信息展示系统
# 【差异分级】D4 互补级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_INNOV_DS_04_CARRIER_RANK_002.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
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


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题系统', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_INNOV_DS_04_CARRIER_RANK_002_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_INNOV_DS_04_CARRIER_RANK_002.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_INNOV_DS_04_CARRIER_RANK_002",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
