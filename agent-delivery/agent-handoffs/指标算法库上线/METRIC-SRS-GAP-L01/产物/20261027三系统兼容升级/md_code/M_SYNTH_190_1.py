#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_190_1 区域创新要素综合分析模型 —— 王惠口径现转实测（20261021 SYNTH-b 批）。
三维：类型(187) / 层次(188) / 领域(189) 等权合成；缺维不补 0、不进平均。"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def wmean(xs):
    vs = [x for x in xs if x is not None]
    return sum(vs) / len(vs) if vs else None


def main():
    idx = {}
    for mid in ["M_SYNTH_187_1", "M_SYNTH_188_1", "M_SYNTH_189_1"]:
        with open(os.path.join(HERE, mid + "_out.json"), encoding="utf-8") as f:
            idx[mid] = json.load(f)["index_0_100"]

    dims = {"类型": idx["M_SYNTH_187_1"], "层次": idx["M_SYNTH_188_1"], "领域": idx["M_SYNTH_189_1"]}
    index = {ct: (round(wmean([dims[k][ct] for k in dims]), 1) if wmean([dims[k][ct] for k in dims]) is not None else None)
             for ct in dims["类型"]}
    rank = sorted(dims["类型"], key=lambda x: -(index[x] if index[x] is not None else -1))

    out = {
        "metric_id": "M_SYNTH_190_1",
        "probe_date": "2026-10-21",
        "sub_index": dims,
        "index_0_100": index,
        "rank": rank,
        "support_judgment": "部分支持",
        "support_reason": (
            "三维入口全部可现转（类型 87.2/26.4/19.6/44.0、层次、领域三子指数已跑通）；"
            "但三子指数各自继承上游缺口：187 人才/科研机构维京沪缺失、188 熵均衡被采集偏差放大、"
            "189 宏观事实表京沪无行——综合指数为『缺叶降维合成』，判部分支持"
        ),
        "note": "王惠口径 190 现转实测 20261021；类型/层次/领域分别直接取 187/188/189 的 index_0_100，三维等权。缺维不补 0、不进平均。",
    }
    with open(os.path.join(HERE, "M_SYNTH_190_1_out.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({"index": index, "rank": rank}, ensure_ascii=False))


if __name__ == "__main__":
    main()
