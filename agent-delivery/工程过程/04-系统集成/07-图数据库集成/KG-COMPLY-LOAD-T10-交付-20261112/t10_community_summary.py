#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T10 · 需规 435 社群属性与特征汇总生成器

输入：t10/out/t10_full_s42_r8.0_all.json（B′ 定案参数 partition，python-louvain）
     + 图库只读重读 tech_rel（算内部边数/度）
输出：T10-435-社群属性汇总.md（每社群规模/内部边数/平均度/核心节点 Top5）

铁律：只读图库（MATCH/GO），凭据走环境变量。
"""
import json
import os
from collections import defaultdict
from datetime import datetime

from t10_pipeline import connect, read_points, read_edges, build_graph

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "out", "t10_full_s42_r8.0_all.json")


def main():
    with open(SRC) as f:
        res = json.load(f)
    part = res["partition"]
    params = res["params"]
    print(f"partition：{len(part)} 点 / {len(set(part.values()))} 社群 / 参数 {params}")

    pool, sess = connect()
    points = read_points(sess)
    edges = read_edges(sess, points)
    sess.release(); pool.close()
    G, _ = build_graph(points, edges, "all")

    comm_members = defaultdict(list)
    for v, c in part.items():
        comm_members[c].append(v)

    rows = []
    for c, members in comm_members.items():
        mset = set(members)
        inner = 0
        deg = defaultdict(int)
        for v in members:
            for nb in G.neighbors(v):
                deg[v] += 1
                if nb in mset:
                    inner += 1
        inner_e = inner // 2  # 无向边每条数两次
        core = sorted(members, key=lambda v: -deg[v])[:5]
        rows.append({
            "cid": c, "size": len(members), "inner_edges": inner_e,
            # inner=2E（有向计数），标准无向平均度 2E/N=inner/N。
            # 2026-11-12 验收附条修正：原 2*inner/N=4E/N 系统性大 2 倍（networkx 双向边未去重同源）
            "avg_deg": round(inner / len(members), 2) if members else 0,
            # 无向密度 2E/(N(N-1))；成形群 N≥2 分母安全（单点群不入表）
            "density": round(2 * inner_e / (len(members) * (len(members) - 1)), 6)
            if len(members) >= 2 else 0,
            "core": core, "core_deg": [deg[v] for v in core],
        })
    rows.sort(key=lambda r: -r["size"])

    out = [f"# T10 · 435 社群属性与特征汇总（{datetime.now():%Y-%m-%d %H:%M}）", ""]
    out.append(f"> 主口径 B′：Louvain / seed {params['seed']} / resolution {params['resolution']} / "
               f"全量边不滤（SDD §2.2 #4 定案参数）。实现 python-louvain：**{len(rows)} 个社群，"
               f"其中成形（≥2 点）{sum(1 for r in rows if r['size'] >= 2)} 个**、单点群 "
               f"{sum(1 for r in rows if r['size'] == 1)} 个；模块度 {res['result']['modularity']}。")
    out.append("> 与定案 178 个成形社群差 2 个（跨实现收敛抖动，networkx 实现给 176；详见 "
               "T10-交付骨架.md §2）。单点群在表尾合并列出。\n")

    formed = [r for r in rows if r["size"] >= 2]
    singles = [r for r in rows if r["size"] == 1]

    out.append("## 成形社群（按规模降序）\n")
    out.append("| community_id | 规模 | 内部边数 | 平均度 | 密度 | 核心节点 Top5（度数） |")
    out.append("|---|---:|---:|---:|---:|---|")
    for i, r in enumerate(formed, 1):
        core_str = "; ".join(f"{v.split(':')[-1][:12]}… ({d})" for v, d in zip(r["core"], r["core_deg"]))
        out.append(f"| {r['cid']} | {r['size']} | {r['inner_edges']} | {r['avg_deg']} | {r['density']} | {core_str} |")

    out.append(f"\n合计：成形社群 **{len(formed)}** 个，覆盖 "
               f"{sum(r['size'] for r in formed)} 点；总内部边 "
               f"{sum(r['inner_edges'] for r in formed)}。\n")

    out.append(f"## 单点群（{len(singles)} 个，技术点层孤点，不参与社群结构分析）\n")
    out.append("> VID 清单见 `out/t10_full_s42_r8.0_all.json`（partition 值对应表尾社群 ID）。\n")

    out.append("## 汇总口径说明\n")
    out.append("- 规模：社群内技术点数；内部边数 E：两端均在社群内的 tech_rel 无向边数；"
               "平均度：2E/规模（社群内度）；密度：2E/(N(N-1))（无向）；核心节点：社群内度数 Top5。")
    out.append("- 2026-11-12 验收附条闭环：原表平均度误为 4E/N（大一倍）已修正为 2E/N；"
               "补密度列 2E/(N(N-1))（DoD 点名，验收记录 KG-COMPLY-ACCEPT-T10）。")
    out.append("- 数据源：demo_gkx_chain 技术点层（19,430 点 / 541,428 边，只读，2026-11-11 实测）。")
    out.append("- 复现：`python3 t10_pipeline.py --mode full --seed 42 --resolution 8.0 --evidence all` "
               f"→ `python3 t10_community_summary.py`。")

    md = "\n".join(out) + "\n"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "T10-435-社群属性汇总.md")
    with open(path, "w") as f:
        f.write(md)
    print(f"✅ {path}（成形 {len(formed)} + 单点 {len(singles)}）")
    print(f"   Top5 社群规模：{[r['size'] for r in formed[:5]]}")


if __name__ == "__main__":
    main()
