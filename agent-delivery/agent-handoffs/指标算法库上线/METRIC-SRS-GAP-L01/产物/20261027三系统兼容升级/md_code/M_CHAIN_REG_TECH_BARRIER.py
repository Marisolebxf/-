#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_REG_TECH_BARRIER 区域技术壁垒（技术力叶子）（20261021 改源版）

口径（calc-logic/CHAIN/M_CHAIN_REG_TECH_BARRIER.md v0.2.0，徐滕强 2026-10-14 拍板）：
  Barrier(c,r) = (minmax(空白得分) + minmax(封锁得分)) / 2，两个子项各自在**同链 4 市截面**归一。
  空白：区域链上企业中，统计窗内发明授权量为 0 的企业占比 ×100；
  封锁：区域链上企业专利的 IPC 首字母 8 大维占比向量，与该链其余 3 市的平均欧氏距离。

改源后能守住的与必须降级的：
  · 能守住：链上企业集合（35,046 家，credit 唯一）、按申请人名落专利、IPC 首字母分布、48 个单元闭合；
  · 必须降级：①「统计年及前 3 年」的 4 年窗无法复现——`dwd_patent` 只有 2021—2026，
    离线缓存只按**全期**与**2024 单年**两档给了授权计数，故空白子项用全期为主值、2024 单年为敏感性；
    ② `kind='B'` 无法单独切出——缓存里的 `granted` 是「granted_number 非空」的行数，含发明授权与
    实用新型/外观授权，方向为**低估空白**（把有实用新型的企业也算作有授权）；
    ③ 封锁子项的 IPC 分布是全期，不是 3 年窗。
  以上三点使本指标只能判 **部分支持**，不能沿用 20261020 版的「完全转换支持」结论。

零 DB：`star_applicant_agg_gkx.json`（agg: name → [件数, 授权数]，授权子项唯一入口；
**勿用** chain_intl 的 name_patent[1]，该列合计 89,935 = WO 行数，是 PCT 计数不是授权）、
`chain_intl_gkx_20261021.json`（name → [件数, PCT 数]）、
`patent_ipc4_by_name_20261021.json`（IPC 小类 × 申请人，581,585 组）、
`patent_2024_by_name_20261021.json`（2024 授权行数）、`bridge_20261021.json`。

输出：code/M_CHAIN_REG_TECH_BARRIER_out.json
"""
from __future__ import annotations

import math
import time
from collections import Counter, defaultdict

from _reg5_common import (CHAIN_AXIS, CHAIN_CN, CITY4, SNAP, _load, cells, chain_firms, minmax,
                          pct, stats, write_out)

MID = "M_CHAIN_REG_TECH_BARRIER"


def main() -> None:
    t0 = time.time()
    ci = _load("chain_intl_gkx_20261021.json", {})
    name_patent = ci["name_patent"]
    ipc4_name = _load("patent_ipc4_by_name_20261021.json", [])
    grant_2024 = _load("patent_2024_by_name_20261021.json", {})
    agg = _load("star_applicant_agg_gkx.json", {}).get("agg", {})
    if not agg:
        raise SystemExit("缺 star_applicant_agg_gkx.json（全量申请人 [件数, 授权数]），先跑 _build_patent_caches21.py 的 merge")
    cf, nc, ec = cells()
    firms_all = chain_firms()

    # ---------- 空白子项 ----------
    blank, blank_2024, blank_detail = {}, {}, {}
    for ch in CHAIN_AXIS:
        for city in CITY4:
            fs = cf.get((ch, city), set())
            if not fs:
                blank[(ch, city)] = None
                continue
            zero = sum(1 for f in fs if int(agg.get(f, [0, 0])[1]) == 0)
            zero24 = sum(1 for f in fs if int(grant_2024.get(f, [0, 0])[1]) == 0)
            blank[(ch, city)] = round(100 * zero / len(fs), 4)
            blank_2024[(ch, city)] = round(100 * zero24 / len(fs), 4)
            blank_detail[(ch, city)] = {"n_firms": len(fs), "n_zero": zero,
                                        "n_with_grant": len(fs) - zero,
                                        "n_zero_2024": zero24}

    # ---------- 封锁子项 ----------
    name_cells = defaultdict(list)
    for ch in CHAIN_AXIS:
        for city in CITY4:
            for f in cf.get((ch, city), ()):
                name_cells[f].append((ch, city))
    ipc = defaultdict(Counter)
    used = 0
    for ipc4, nm, c in ipc4_name:
        k = name_cells.get(nm)
        if not k:
            continue
        used += int(c)
        letter = str(ipc4)[0]
        for cell in k:
            ipc[cell][letter] += int(c)

    def vec(counter):
        s = sum(counter.values())
        return {k: v / s for k, v in counter.items()} if s else {}

    block, block_detail = {}, {}
    for ch in CHAIN_AXIS:
        for city in CITY4:
            va = vec(ipc.get((ch, city), {}))
            if not va:
                block[(ch, city)] = None
                block_detail[(ch, city)] = {"n_ipc_rows": 0}
                continue
            ds = []
            for c2 in CITY4:
                if c2 == city:
                    continue
                vb = vec(ipc.get((ch, c2), {}))
                if not vb:
                    continue
                ds.append(math.sqrt(sum((va.get(k, 0) - vb.get(k, 0)) ** 2
                                        for k in set(va) | set(vb))))
            block[(ch, city)] = round(sum(ds) / len(ds), 6) if ds else None
            block_detail[(ch, city)] = {"n_ipc_rows": sum(ipc[(ch, city)].values()),
                                        "ipc1_share": {k: round(v, 4) for k, v in sorted(va.items())}}

    def normalize(d):
        out = {}
        for ch in CHAIN_AXIS:
            keys = [k for k in d if k[0] == ch and d[k] is not None]
            if not keys:
                for c in CITY4:
                    out[(ch, c)] = None
                continue
            z = dict(zip(keys, minmax([d[k] for k in keys])))
            for c in CITY4:
                out[(ch, c)] = round(100 * z[(ch, c)], 2) if (ch, c) in z else None
        return out

    bz, kz = normalize(blank), normalize(block)
    comp = {}
    for ch in CHAIN_AXIS:
        for city in CITY4:
            parts = [v for v in (bz.get((ch, city)), kz.get((ch, city))) if v is not None]
            comp[(ch, city)] = round(sum(parts) / len(parts), 2) if parts else None

    matrix = []
    for ch in CHAIN_AXIS:
        row = {"chain": ch, "chain_name": CHAIN_CN[ch], "cells": {}}
        for city in CITY4:
            k = (ch, city)
            row["cells"][city] = {
                "blank_share_pct": blank[k],
                "blank_share_2024_pct": blank_2024.get(k),
                "blank_score": bz.get(k),
                "blockade_distance": block.get(k),
                "blockade_score": kz.get(k),
                "barrier_score": comp.get(k),
                "n_firms": blank_detail.get(k, {}).get("n_firms", 0),
                "n_with_grant": blank_detail.get(k, {}).get("n_with_grant"),
                "n_ipc_rows": block_detail.get(k, {}).get("n_ipc_rows", 0),
            }
        matrix.append(row)

    vals = [comp[(ch, c)] for ch in CHAIN_AXIS for c in CITY4]
    blank_vals = [v for v in blank.values() if v is not None]
    block_vals = [v for v in block.values() if v is not None]
    flat = sorted(((row["chain_name"], c, row["cells"][c]["barrier_score"])
                   for row in matrix for c in CITY4), key=lambda x: -x[2])
    thin = [{"chain": CHAIN_CN[ch], "city": c, "n_firms": len(cf.get((ch, c), ()))}
            for ch in CHAIN_AXIS for c in CITY4 if len(cf.get((ch, c), ())) < 30]
    firm_links = sum(len(v) for v in cf.values())
    uniq = {f for v in firms_all.values() for f in v}
    with_pat = sum(1 for f in uniq if int(name_patent.get(f, [0, 0])[0]) > 0)

    payload = {
        "metric_id": MID,
        "metric_name": "区域技术壁垒（技术力叶子）",
        "date": "2026-10-22",
        "formula_owner": "徐滕强（calc-logic v0.2.0，2026-10-14 拍板；非王惠口径）",
        "formula": "Barrier=(minmax(BlankShare)+minmax(MeanEuclidDist))/2",
        "stat_year": 2025,
        "window_blank": "全期（表内 2021—2026；原稿要求统计年及前 3 年）",
        "window_blank_sensitivity": "2024 单年",
        "window_blockade": "全期 IPC 首字母分布（原稿要求 3 年窗 2022—2024）",
        "region_axis": CITY4,
        "chain_axis": len(CHAIN_AXIS),
        "matrix": matrix,
        "stats_blank_share": stats(blank_vals),
        "stats_blank_share_2024": stats([v for v in blank_2024.values() if v is not None]),
        "stats_blockade_distance": stats(block_vals),
        "stats_barrier_score": stats(vals),
        "top5_barrier": [{"chain": a, "city": b, "barrier_score": v} for a, b, v in flat[:5]],
        "bottom5_barrier": [{"chain": a, "city": b, "barrier_score": v} for a, b, v in flat[-5:]],
        "probes": {
            "chain_firm_links": firm_links,
            "unique_firms": len(uniq),
            "firms_with_any_patent": with_pat,
            "firms_with_any_patent_pct": pct(with_pat, len(uniq)),
            "name_patent_names": len(name_patent),
            "ipc_rows": len(ipc4_name),
            "ipc_rows_attributed": used,
            "cells_with_ipc": len(block_vals),
            "cells_with_blank": len(blank_vals),
            "n_cells": 48,
            "thin_cells_lt30": thin,
            "grant_2024_names": len(grant_2024),
            "granted_rows_total": sum(int(v[1]) for v in agg.values()),
            "grant_rate_pct": pct(sum(int(v[1]) for v in agg.values()),
                                  sum(int(v[0]) for v in agg.values())),
        },
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"两个子项都算出了 48 个单元：空白占比 {stats(blank_vals)['min']}%—{stats(blank_vals)['max']}%，"
                f"48/48 非空；封锁距离 {stats(block_vals)['min']}—{stats(block_vals)['max']}，48/48 有 IPC 样本；"
                f"合成后 {stats(vals)['n_distinct']} 个不同取值。但口径有三个无法复原的缺口："
                f"①原稿的「统计年及前 3 年」窗口要求 2022—2025 逐年授权，缓存只有全期与 2024 单年两档；"
                f"②原稿要求 `kind='B'`（发明授权），缓存只能给「granted_number 非空」，含实用新型与外观，"
                f"导致空白占比被系统性低估；③封锁向量的 IPC 分布是全期而非 3 年窗。"
                f"三项均为口径级降级，故判部分支持，不沿用旧版的完全转换支持。"
            ),
            "criteria": {"n_cells": 48, "cells_with_blank": len(blank_vals),
                         "cells_with_ipc": len(block_vals),
                         "n_distinct_score": stats(vals)["n_distinct"],
                         "window_degraded": True, "kind_degraded": True},
        },
        "notes": [
            "空白子项的分母是链上企业名集合（12 链合计 52,906 条链-企链接、去重后 33,000 余家），"
            "同一企业多链时在每条链各计一次。",
            "企业—专利连接按 `first_applicant_name = 企业名` 等值匹配，链上企业里只有 "
            f"{pct(with_pat, 52_906)}% 能在专利表找到同名申请人；未命中的企业一律计入「零授权」，"
            "方向是高估空白，已在正文披露。",
            "封锁子项的 IPC 只取小类前 4 位首字母（A—H 八大维），未做 IPC 全码距离，"
            "这是原稿拍板的简化方案。",
            "4 市截面 min-max 会强制每链产生 0 分与 100 分，分数只在本链内有意义，跨链不可比。",
            "低空经济×东莞（12 家）、×惠州（8 家）样本过小，单家企业翻转即可改变数个百分点。",
            "若甲方要求恢复原口径，最小补数是「按年 × kind 的申请人授权计数」缓存，"
            "需对 294 万行专利表重扫一次（约 30 分钟、全局并发限 2 条），不建议在未排期时启动。",
        ],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    write_out(MID, payload)
    print("blank", stats(blank_vals), "block", stats(block_vals), "score", stats(vals))
    print("cells", len(blank_vals), len(block_vals), "thin", thin)
    print("top5", payload["top5_barrier"])


if __name__ == "__main__":
    main()
