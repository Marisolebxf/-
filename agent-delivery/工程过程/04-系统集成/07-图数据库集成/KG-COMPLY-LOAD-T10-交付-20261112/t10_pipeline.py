#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T10 · 社群发现参数化管道（读图 → 滤边 → Louvain，B′ 复现工具）

三开关（B′=178 的参数出处答复到后，枚举参数组合复现）：
  --seed 42            随机种子（11-07 实跑锚点 = 42）
  --resolution 1.0     Louvain 分辨率
  --evidence all|hm|h  边证据过滤：all=全边(541,428) / hm=HIGH+MEDIUM(171, maybe) / h=仅 HIGH

铁律：
  - 只读图库：MATCH / GO / SHOW，不写任何东西。
  - 凭据只从环境变量读。

校准锚点：--seed 42 --resolution 1.0 --evidence all --weight none
应复现 2026-11-07 实跑结果：113 个社群、模块度 0.5198（qiliantupu1/docs/kg-comply/20261107 算法实跑结果）。

用法：
  export NEBULA_ADDR=10.50.75.136:9669 NEBULA_USER=... NEBULA_PASS=...
  python3 t10_pipeline.py --mode smoke      # 2000 点子图验证管道
  python3 t10_pipeline.py --mode full       # 全量 19,430 点
输出：t10/out/<标签>.json + 终端摘要
"""
import argparse
import json
import os
import random
import time
from datetime import datetime

SPACE = "demo_gkx_chain"
VID_PREFIX = "tech_point:tcn_"


def connect():
    from nebula3.gclient.net import ConnectionPool
    from nebula3.Config import Config as NebulaConfig
    addr = os.environ.get("NEBULA_ADDR", "10.50.75.136:9669")
    user, pw = os.environ.get("NEBULA_USER"), os.environ.get("NEBULA_PASS")
    if not user or not pw:
        raise SystemExit("❌ 未设置 NEBULA_USER / NEBULA_PASS")
    host, port = addr.split(":")
    pool = ConnectionPool()
    if not pool.init([(host, int(port))], NebulaConfig()):
        raise SystemExit(f"❌ 连不上 {addr}")
    sess = pool.get_session(user, pw)
    if not sess.execute(f"USE {SPACE}").is_succeeded():
        raise SystemExit(f"❌ 进不了空间 {SPACE}")
    return pool, sess


def read_points(sess, limit=None):
    nql = "MATCH (v:tech_point) RETURN id(v) AS vid"
    if limit:
        nql += f" LIMIT {limit}"
    r = sess.execute(nql)
    if not r.is_succeeded():
        raise SystemExit(f"❌ 读点失败: {r.error_msg()}")
    return [row["vid"] for row in r.as_primitive()]


def read_edges(sess, vids, batch=200):
    """GO 分批读 tech_rel（小批量防 graphd 大 IN 打爆，trsgraph-oom-runbook 教训）"""
    edges = []  # (src, dst, evidence, conf)
    for i in range(0, len(vids), batch):
        chunk = vids[i:i + batch]
        quoted = ",".join(f'"{v}"' for v in chunk)
        nql = (f"GO FROM {quoted} OVER tech_rel YIELD "
               f"src(edge) AS s, dst(edge) AS d, "
               f"properties(edge).evidence_level AS ev, "
               f"properties(edge).relation_confidence_score AS conf")
        r = sess.execute(nql)
        if not r.is_succeeded():
            raise SystemExit(f"❌ 读边失败（批 {i}）: {r.error_msg()}")
        for row in r.as_primitive():
            edges.append((row["s"], row["d"], row.get("ev") or "", row.get("conf")))
        if (i // batch) % 20 == 0:
            print(f"  …读边 {i + len(chunk)}/{len(vids)} 点，累计 {len(edges)} 边", flush=True)
    return edges


def build_graph(points, edges, evidence):
    import networkx as nx
    keep = {"all": None, "hm": {"HIGH", "MEDIUM"}, "h": {"HIGH"}}[evidence]
    vidset = set(points)
    G = nx.Graph()
    G.add_nodes_from(points)
    seen = set()
    dropped = 0
    for s, d, ev, conf in edges:
        if s not in vidset or d not in vidset:
            continue  # smoke 子图诱导
        if keep is not None and ev not in keep:
            dropped += 1
            continue
        key = (s, d) if s <= d else (d, s)
        if key in seen:
            continue
        seen.add(key)
        G.add_edge(s, d)
    return G, dropped


def louvain(G, seed, resolution, weight):
    import community as community_louvain  # python-louvain
    random.seed(seed)
    # 无权（11-07 口径）：不传 weight，每边按 1 计（该版本传 None 会在 induced_graph 炸）
    kwargs = {"resolution": resolution, "random_state": seed}
    if weight != "none":
        kwargs["weight"] = weight
    return community_louvain.best_partition(G, **kwargs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["smoke", "full"], default="smoke")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--resolution", type=float, default=1.0)
    ap.add_argument("--evidence", choices=["all", "hm", "h"], default="all")
    ap.add_argument("--weight", choices=["none"], default="none")  # 先无权（11-07 口径）
    args = ap.parse_args()

    t0 = time.time()
    pool, sess = connect()
    print(f"✅ 已连入（只读）。模式={args.mode}")

    points = read_points(sess, limit=2000 if args.mode == "smoke" else None)
    print(f"点：{len(points)}")
    edges = read_edges(sess, points)
    print(f"原始边（GO 全部往返）：{len(edges)}")
    sess.release()
    pool.close()

    G, dropped = build_graph(points, edges, args.evidence)
    print(f"建图：{G.number_of_nodes()} 点 / {G.number_of_edges()} 无向边"
          f"（滤掉证据边 {dropped} 条）")

    part = louvain(G, args.seed, args.resolution, args.weight)
    n_comm = len(set(part.values()))

    import networkx as nx
    mod = nx.community.modularity(G, [
        {v for v in part if part[v] == c} for c in set(part.values())])

    sizes = {}
    for v, c in part.items():
        sizes[c] = sizes.get(c, 0) + 1
    top = sorted(sizes.values(), reverse=True)
    singletons = sum(1 for s in sizes.values() if s == 1)

    tag = f"{args.mode}_s{args.seed}_r{args.resolution}_{args.evidence}"
    res = {
        "tag": tag, "timestamp": datetime.now().isoformat(timespec="seconds"),
        "params": {"mode": args.mode, "seed": args.seed,
                   "resolution": args.resolution, "evidence": args.evidence,
                   "weight": args.weight},
        "input": {"points_read": len(points), "edges_raw": len(edges),
                  "graph_nodes": G.number_of_nodes(), "graph_edges": G.number_of_edges(),
                  "edges_dropped_by_evidence": dropped},
        "result": {"communities": n_comm, "modularity": round(mod, 4),
                   "largest_sizes_top10": top[:10], "singleton_communities": singletons},
        "partition": part,
    }
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"),
                exist_ok=True)
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "out", f"t10_{tag}.json")
    with open(out_path, "w") as f:
        json.dump(res, f, ensure_ascii=False)

    print(f"\n═══ 结果（{tag}）═══")
    print(f"社群数：{n_comm}   模块度：{mod:.4f}")
    print(f"最大 10 群尺寸：{top[:10]}   单点群：{singletons}")
    print(f"校准锚点（全量+seed42+r1.0+all）应为 113 群 / 模块度 0.5198")
    print(f"耗时 {time.time() - t0:.0f}s → {out_path}")


if __name__ == "__main__":
    main()
