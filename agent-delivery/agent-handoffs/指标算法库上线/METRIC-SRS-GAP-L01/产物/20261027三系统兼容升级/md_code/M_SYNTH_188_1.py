#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_188_1 区域创新要素层次综合评价模型 —— gkx 重建版（20261022）。

王惠口径：七结构 ×（成熟度 = 结构内叶子极值归一等权；均衡度 = 熵 H/ln(n)×100，
n=1 不可定义 → None），结构得分 = 成熟度与均衡度等权（缺均衡度时取成熟度），
七结构等权合成 0—100。

叶子**不另取**（王惠原文「不另取叶子」）：直接读同目录 `M_SYNTH_187_1_out.json` 的
`leaves`。该文件由 `M_SYNTH_187_1.py` 在本目录产出、可独立运行，`leaf_source`
因此指向一个真实存在且能跑的上游（旧版指向的 187 产物在 gkx 批次里根本不存在，
见 DATA_FACTS §3.20，本版是那条事故的重建）。

本脚本零数据库连接，只读 187 的产物。
输出：`code/M_SYNTH_188_1_out.json`
"""
from __future__ import annotations

import collections
import json
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
import _synth18x_common as S  # noqa: E402

METRIC = "M_SYNTH_188_1"
UPSTREAM = "M_SYNTH_187_1_out.json"

# 与 `M_SYNTH_187_1.py` 的 STRUCT_LEAVES 逐字一致；187 改了叶子名而 188 没跟，
# 这里会立刻 KeyError，而不是安静地少算一片叶子。
STRUCT_LEAVES = collections.OrderedDict([
    ("人才结构", ["D1_学者密度", "D1_高学历人才占比"]),
    ("企业结构", ["D2_新注册企业数2024", "D2_科技型企业占比", "D2_大型企业占比"]),
    ("政策结构", ["D3_政策文件数", "D3_政策类型数"]),
    ("服务机构结构", ["D4_科技服务业企业数", "D4_科技服务业企业占比"]),
    ("科研机构结构", ["D5_科研机构数", "D5_科研机构类型数", "D5_RI对齐2024授权"]),
    ("资金结构", ["D6_上市研发2024", "D6_融资笔数2024"]),
    ("空间结构", ["D7_园区代理数"]),
])


def main():
    up_path = os.path.join(HERE, UPSTREAM)
    if not os.path.exists(up_path):
        raise SystemExit("缺上游产物 %s——请先在本目录运行 `python3 M_SYNTH_187_1.py`" % UPSTREAM)
    up = json.loads(open(up_path, encoding="utf-8").read())
    leaves = up["leaves"]

    missing = [k for keys in STRUCT_LEAVES.values() for k in keys if k not in leaves]
    if missing:
        raise SystemExit("187 产物缺叶子 %s——叶子契约被改过，188 不能静默少算" % missing)

    # 叶子归一：与 187 的 leaf_norm 同式（批内 min-max），并做一次逐位对账。
    leaf_norm = {k: S.mm(leaves[k]) for k in leaves}
    drift = [k for k in leaf_norm if leaf_norm[k] != up.get("leaf_norm", {}).get(k)]
    if drift:
        raise SystemExit("叶子归一与 187 产物不一致：%s——上游口径已变，需重跑 187" % drift)

    maturity, balance, struct_scores = {}, {}, {}
    degen = set(up.get("leaves_degenerate_excluded", {}) or {})
    for st, keys in STRUCT_LEAVES.items():
        mat, bal = {}, {}
        use = [k for k in keys if k not in degen]
        for c in S.CITIES:
            xs = [leaf_norm[k].get(c) for k in use]
            xs = [x for x in xs if x is not None]
            mat[c] = S.wmean(xs)
            bal[c] = S.entropy_norm(xs)
        maturity[st] = mat
        balance[st] = bal
        struct_scores[st] = {c: S.wmean([mat[c], bal[c]]) for c in S.CITIES}

    index = {c: S.wmean([struct_scores[st][c] for st in STRUCT_LEAVES]) for c in S.CITIES}
    rank = sorted([c for c in S.CITIES if index[c] is not None], key=lambda x: -index[x])

    n_leaf_by_city = {c: sum(1 for k in leaves if leaf_norm[k].get(c) is not None)
                      for c in S.CITIES}

    # ---- 敏感性：四条替代口径（全现算）----
    w07 = {c: S.wmean([0.7 * maturity[st][c] + 0.3 * balance[st][c]
                       if balance[st][c] is not None else maturity[st][c]
                       for st in STRUCT_LEAVES]) for c in S.CITIES}
    mat_only = {c: S.wmean([maturity[st][c] for st in STRUCT_LEAVES]) for c in S.CITIES}
    no_talent = {c: S.wmean([struct_scores[st][c] for st in STRUCT_LEAVES
                             if st != "人才结构"]) for c in S.CITIES}
    # 旧规则：退化叶进分子 + n=1 均衡度记 60
    old_struct = collections.OrderedDict()
    for st, keys in STRUCT_LEAVES.items():
        m2 = {c: S.wmean([leaf_norm[k].get(c) for k in keys]) for c in S.CITIES}
        b2 = {}
        for c in S.CITIES:
            xs = [leaf_norm[k].get(c) for k in keys]
            xs = [x for x in xs if x is not None]
            b2[c] = S.entropy_norm(xs) if len(xs) > 1 else (60.0 if xs else None)
        old_struct[st] = {c: S.wmean([m2[c], b2[c]]) for c in S.CITIES}
    old_rule = {c: S.wmean([old_struct[st][c] for st in STRUCT_LEAVES]) for c in S.CITIES}
    sensitivity = {
        "成熟度0.7_均衡度0.3": w07,
        "只取成熟度": mat_only,
        "剔除人才结构": no_talent,
        "旧规则_含退化叶_n1记60": old_rule,
    }

    out = {
        "metric_id": METRIC,
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "上游 M_SYNTH_187_1_out.json（gkx @ 183.240.141.251:3318 派生）；本脚本零数据库连接",
        "leaf_source": "code/M_SYNTH_187_1_out.json（同目录、真实存在、可独立运行；王惠：不另取叶子）",
        "upstream_generated_at": up.get("generated_at"),
        "evaluation_set": S.CITIES,
        "maturity": {k: {c: (round(v, 1) if v is not None else None) for c, v in m.items()}
                     for k, m in maturity.items()},
        "balance_entropy": {k: {c: (round(v, 1) if v is not None else None) for c, v in b.items()}
                            for k, b in balance.items()},
        "struct_scores": {k: {c: (round(v, 1) if v is not None else None) for c, v in s.items()}
                          for k, s in struct_scores.items()},
        "index_0_100": {c: (round(index[c], 1) if index[c] is not None else None)
                        for c in S.CITIES},
        "rank": rank,
        "n_leaves_by_structure": {st: len(keys) for st, keys in STRUCT_LEAVES.items()},
        "n_leaves_effective_by_structure": {
            st: len([k for k in keys if k not in degen]) for st, keys in STRUCT_LEAVES.items()},
        "excluded_degenerate_leaves": sorted(degen),
        "n_leaves_available_by_city": n_leaf_by_city,
        "sensitivity": sensitivity,
        "params": {
            "maturity": "结构内叶子批内极值归一等权（缺叶不进分母）",
            "balance": "熵 H/ln(n)×100；n=1 均衡度不可定义 → None（该结构只用成熟度代表）；合计 0 记 0",
            "structure": "成熟度与均衡度等权（均衡度为 None 时取成熟度）",
            "index": "七结构等权",
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "层次指数全部叶子继承 187 的类型指数口径，缺口同源：人才结构维研发人员分母整列为空、"
            "高学历占比只有深穗两城有样本；服务机构维由演示 ADS 的六类分类退化为行业口径；"
            "空间维只有名称关键词代理；政策维库内止于 2022-06 且惠州零记录。"
            "七结构里六结构在四城均有读数、指数非退化，但至少四处叶子被迫降级，"
            "且惠州在人才/政策/空间三结构上是真实 0 端，熵均衡度因此被采集偏差放大，判部分支持"),
        "note": "旧版（20261020）的叶子来自演示库，且 188 当时读不到 187 的产物、脚本无法运行；"
                "本版叶子由本目录 187 现算，见 MD §〇.2。",
    }
    out.update(S.base_block(
        [S.T_YEAR],
        [y for y in S.PATENT_YEARS if y != S.T_YEAR],
        "188 是 187 的二次合成，不做年度除法；187 的叶子都是 2024 年截面值或当年比率，"
        "故 188 的基期规则与 187 完全一致：只用 2024，不把任何缺失年摊进分母。"))
    S.write_out(METRIC, out)
    print("index", out["index_0_100"], "rank", rank)


if __name__ == "__main__":
    main()
