#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KG-GRAPH-COVER-01 步骤3：tech_rel 差分补齐（目标 45,824 条）。

依据：派单-A 第 2 步 + 11-说明 §4.2 / §六步3。
铁律：**只补差集，禁止整表重灌**（冲掉已有边的 props）；差集 = 源 587,252 − 图内已有 541,428。
要点：
  - 图内已有对全量导出（锚定 MATCH）→ 与源做集合差 → 只插缺的。
  - 源拉取按 source 技术点分组小查询（同 s2，防 Doris Query timeout；GROUP BY 六列去重）。
  - 写入带源表四属性：relation_type / evidence_level / relation_confidence_score /
    direction_status（tag 即有此四列；batch 列不存在——批号 kg100-cover-01-rel 只记录在台账）。
  - 批内先 FETCH 两端点（11-说明实测 18,567/18,860 点均在图，预期 skip=0，仍留计数）。
  - 单批 45,824 < 20 万上限；写前写后各一次全量 count；抽验 50 对。
用法：python3 cover01_s3_fill_tech_rel.py [--apply]
凭据：环境变量 NEBULA_* / DORIS_*（不进 git）。
"""
import csv
import json
import os
import random
import sys
import time

import pymysql
from nebula3.gclient.net import ConnectionPool
try:
    from nebula3.Config import Config as NebulaConfig
except ImportError:
    from nebula3.Config import Configs as NebulaConfig

WORK = "/home/zhangzhong_e43d4db3/qiliantupu/kg100-work"
LOG = os.path.join(WORK, "s3_batch_log.csv")
CKPT = os.path.join(WORK, "s3_checkpoint.json")
CHUNK = 5000
GROUP_SZ = 100        # 每个源查询的 source 技术点数（~3k 行/组）
BATCH_NAME = "kg100-cover-01-rel"
SPACE = "demo_gkx_chain"


def esc(v):
    if v is None or v == "":
        return "NULL"
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def count_rel(s):
    r = s.execute("MATCH ()-[e:tech_rel]->() RETURN count(e) AS c;")
    return list(r.as_primitive()[0].values())[0]


def main():
    apply = "--apply" in sys.argv
    pool = ConnectionPool()
    assert pool.init([("10.50.75.136", 9669)], NebulaConfig()), "图库建连失败"
    s = pool.get_session(os.environ["NEBULA_USER"], os.environ["NEBULA_PASS"])
    assert s.execute(f"USE {SPACE};").is_succeeded()
    t0 = time.time()

    # 1) 图内已有对（锚定导出）
    r = s.execute("MATCH (a:tech_point)-[e:tech_rel]->(b:tech_point) RETURN id(a) AS x, id(b) AS y;")
    have = set()
    for row in r.as_primitive():
        have.add((row["x"].split(":", 1)[1], row["y"].split(":", 1)[1]))
    base = len(have)
    print(f"[图内] tech_rel 已有 {base:,} 对（count 查询另证：{count_rel(s):,}）｜{time.time()-t0:.0f}s", flush=True)

    # 2) 分组拉源表（六列 GROUP BY 去重）
    conn = pymysql.connect(host=os.environ["DORIS_HOST"], port=int(os.environ["DORIS_PORT"]),
                           user=os.environ["DORIS_USER"], password=os.environ["DORIS_PASS"],
                           database=os.environ["DORIS_DB"], connect_timeout=15, read_timeout=300)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT source_technology_node_id FROM ads_technology_graph_edge")
    srcs = sorted(row[0] for row in cur.fetchall() if row[0])
    print(f"[源] source 技术点 {len(srcs):,} 个", flush=True)
    diff, seen, dup = [], set(), 0
    for gi in range(0, len(srcs), GROUP_SZ):
        group = srcs[gi:gi + GROUP_SZ]
        inlist = ",".join("'" + i.replace("'", "''") + "'" for i in group)
        cur.execute("SELECT source_technology_node_id, target_technology_node_id, relation_type, "
                    "evidence_level, relation_confidence_score, direction_status "
                    "FROM ads_technology_graph_edge WHERE source_technology_node_id IN ("
                    f"{inlist}) GROUP BY 1,2,3,4,5,6")
        for srcn, tgtn, rtype, elev, conf, dstat in cur.fetchall():
            pair = (srcn, tgtn)
            if pair in seen:
                dup += 1; continue          # 六列级重复（同对多指标行）只灌一次
            seen.add(pair)
            if pair not in have:
                diff.append((srcn, tgtn, rtype, elev, float(conf) if conf is not None else None, dstat))
    conn.close()
    json.dump(diff, open(os.path.join(WORK, "s3_diff_pairs.json"), "w"))
    print(f"[差集] 源唯一对 {len(seen):,}｜源内六列级重复 {dup:,}｜图内已有 {min(base,len(seen)):,}"
          f"｜拟补 {len(diff):,}（11-说明预计 45,824）｜{time.time()-t0:.0f}s", flush=True)

    # 3) 端点防重与写入（单批）
    logf = open(LOG, "a", newline="")
    logw = csv.writer(logf)
    if apply and diff:
        ck = json.load(open(CKPT)) if os.path.exists(CKPT) else {"inserted": 0, "done": False}
        if ck["done"]:
            print("[续跑] 本批已完成，跳过", flush=True)
        else:
            # 端点存在性：源端 FETCH 一把（目标端在 11-说明 已证在图；此处再核一次，取差集涉及点）
            vids = sorted({f"tech_point:{p[0]}" for p in diff} | {f"tech_point:{p[1]}" for p in diff})
            exist = set()
            for i in range(0, len(vids), 500):
                vv = ",".join(f"\"{v}\"" for v in vids[i:i + 500])
                fr = s.execute(f"FETCH PROP ON tech_point {vv} YIELD id(vertex) AS vid;")
                if fr.is_succeeded():
                    exist |= {row["vid"] for row in fr.as_primitive()}
            missing_ep = [p for p in diff
                          if f"tech_point:{p[0]}" not in exist or f"tech_point:{p[1]}" not in exist]
            todo = [p for p in diff if p not in missing_ep]
            print(f"[端点] 涉及点 {len(vids):,}｜缺端点跳过 {len(missing_ep):,}（须逐条留证）", flush=True)
            if missing_ep:
                json.dump(missing_ep, open(os.path.join(WORK, "s3_skip_missing_endpoint.json"), "w"))
            cnt0 = count_rel(s)
            for i in range(0, len(todo), CHUNK):
                b = todo[i:i + CHUNK]
                vals = ",".join(
                    f"\"tech_point:{x}\"->\"tech_point:{y}\":({esc(rt)}, {esc(ev)}, "
                    f"{('NULL' if cf is None else repr(cf))}, {esc(ds)})"
                    for x, y, rt, ev, cf, ds in b)
                res = s.execute(f"INSERT EDGE tech_rel(relation_type, evidence_level, "
                                f"relation_confidence_score, direction_status) VALUES {vals};")
                if not res.is_succeeded():
                    print(f"[停] 段 {i//CHUNK} 写入失败：{res.error_msg()[:200]}", flush=True)
                    logw.writerow([time.strftime("%F %T"), BATCH_NAME, "FAIL", len(b), res.error_msg()[:200]])
                    logf.close(); s.release(); pool.close(); sys.exit(1)
            cnt1 = count_rel(s)
            spot = 0
            for x, y, *_ in random.sample(todo, min(50, len(todo))):
                fr = s.execute(f"FETCH PROP ON tech_rel \"tech_point:{x}\"->\"tech_point:{y}\" YIELD edge AS e;")
                spot += 1 if (fr.is_succeeded() and len(fr.as_primitive()) > 0) else 0
            ok = (cnt1 - cnt0 == len(todo)) and spot == min(50, len(todo))
            print(f"[{BATCH_NAME}] 拟写 {len(todo):,}｜增量 {cnt1-cnt0:,}｜抽验 {spot}/{min(50,len(todo))}"
                  f"｜{'✅' if ok else '❌'}｜全量终值 {cnt1:,}（目标 587,252）｜总耗时 {time.time()-t0:.0f}s", flush=True)
            logw.writerow([time.strftime("%F %T"), BATCH_NAME, "OK" if ok else "MISMATCH",
                           len(todo), cnt1 - cnt0, f"spot={spot}/{min(50,len(todo))}", f"total={cnt1}"])
            if not ok:
                print("[停] 对账不符，立即停", flush=True)
                logf.close(); s.release(); pool.close(); sys.exit(1)
            json.dump({"inserted": len(todo), "done": True}, open(CKPT, "w"))
    else:
        print(f"{'[DRY-RUN] 未写' if not apply else '[空差集] 无需写'}：拟补 {len(diff):,}", flush=True)
        logw.writerow([time.strftime("%F %T"), BATCH_NAME, "DRY" if not apply else "EMPTY", len(diff)])
    logf.close(); s.release(); pool.close()


if __name__ == "__main__":
    main()
