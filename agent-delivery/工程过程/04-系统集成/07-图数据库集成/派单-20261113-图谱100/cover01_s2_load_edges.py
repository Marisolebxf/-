#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KG-GRAPH-COVER-01 步骤2：灌 tech_has_institution 全量（非企业，目标 2,377,981 条）。

依据：派单-A 第 1 步 + 11-说明 §五（只收 is_company=0）、§六步2、§七坑1/2/3。
要点：
  - 每批 ≤200,000 条（§七坑1），批号 kg100-cover-01-ins-01..NN 只记录在台账与分批文件——
    边型 tech_has_institution 无 props 列（实测 schema 仅 relation_strength，禁改 schema），
    派单原文的 props.batch / CONTAINS 回读不可行；偏离以「分批文件 + 中段/终段全量 count 差
    + 每批 O(1) 探活与 50 对 FETCH 抽验」代替，写入对账文档。
  - 源表拉取：单条 ORDER BY 大查询在 Doris 服务端 Query timeout（实测 2026-11-17，~40 万行后
    断流，报 errCode=2 Query timeout）——改为「DISTINCT institution_id（33,026）→ 按机构分组
    IN(...) + GROUP BY 两列」小查询，组内行数 ~1.2 万，绝不触发超时；批次按组边界切分，
    续跑时批组成确定不变。
  - 写前重导图内已有端点对做集合差（§七坑2 防重）；断点续跑（checkpoint）；
    任何失败立即停（§七坑1）。
用法：python3 cover01_s2_load_edges.py [--apply]
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
CKPT = os.path.join(WORK, "s2_checkpoint.json")
LOG = os.path.join(WORK, "s2_batch_log.csv")
BATCH_SIZE = 200000
CHUNK = 5000            # 每条 INSERT 语句的边数
GROUP_INSTS = 150       # 每个源查询包含的机构数（~1.2 万行/组，防 Doris 查询超时）
BATCH_PREFIX = "kg100-cover-01-ins-"
SPACE = "demo_gkx_chain"


def count_edges(s):
    r = s.execute("MATCH ()-[e:tech_has_institution]->() RETURN count(e) AS c;")
    return list(r.as_primitive()[0].values())[0]


def alive(s, probe_vid):
    r = s.execute(f"FETCH PROP ON tech_institution \"{probe_vid}\" YIELD id(vertex) AS v;")
    return r.is_succeeded() and len(r.as_primitive()) > 0


def main():
    apply = "--apply" in sys.argv
    ckpt = json.load(open(CKPT)) if os.path.exists(CKPT) else {"done_batches": 0, "inserted": 0}

    pool = ConnectionPool()
    assert pool.init([("10.50.75.136", 9669)], NebulaConfig()), "图库建连失败"
    s = pool.get_session(os.environ["NEBULA_USER"], os.environ["NEBULA_PASS"])
    assert s.execute(f"USE {SPACE};").is_succeeded()
    base_total = count_edges(s)
    print(f"[探活] 当前 tech_has_institution = {base_total:,}；模式={'APPLY 真写' if apply else 'DRY-RUN'}", flush=True)

    # 1) 重导图内全部已有端点对（防漂移，§七坑2）；探活点从真实数据取
    r = s.execute("MATCH (a:tech_point)-[e:tech_has_institution]->(b:tech_institution) "
                  "RETURN id(a) AS x, id(b) AS y;")
    have = set((row["x"].split(":", 1)[1], row["y"].split(":", 1)[1]) for row in r.as_primitive())
    probe_vid = "tech_institution:" + next(iter(have))[1]
    assert alive(s, probe_vid), "探活失败"
    print(f"[防重] 图内已有端点对 {len(have):,}", flush=True)

    # 2) 分组拉源表（非企业）：先 DISTINCT 机构，再按组 IN(...) + GROUP BY 去重
    conn = pymysql.connect(host=os.environ["DORIS_HOST"], port=int(os.environ["DORIS_PORT"]),
                           user=os.environ["DORIS_USER"], password=os.environ["DORIS_PASS"],
                           database=os.environ["DORIS_DB"], connect_timeout=15, read_timeout=300)
    cur = conn.cursor()
    t_d = time.time()
    cur.execute("SELECT DISTINCT institution_id FROM ads_technology_institution WHERE is_company=0")
    insts = sorted(row[0] for row in cur.fetchall() if row[0])
    print(f"[源] 非企业机构 {len(insts):,} 家（DISTINCT {time.time()-t_d:.1f}s）", flush=True)

    bi = 0               # 已完成批数（checkpoint 口径）
    buf = []
    seen = set()         # 源内自去重（GROUP BY 已去重，双保险）
    dup_in_src = skipped_exist = src_rows = 0
    t0 = time.time()
    logf = open(LOG, "a", newline="")
    logw = csv.writer(logf)

    def run_batch(batch_no, batch_pairs):
        """batch_no：1 起的展示批号。"""
        name = f"{BATCH_PREFIX}{batch_no:02d}"
        t1 = time.time()
        if apply:
            json.dump(batch_pairs, open(os.path.join(WORK, f"batch_{name}.json"), "w"))
            for i in range(0, len(batch_pairs), CHUNK):
                b = batch_pairs[i:i + CHUNK]
                vals = ",".join(f"\"tech_point:{x}\"->\"tech_institution:{y}\":(NULL)" for x, y in b)
                res = s.execute(f"INSERT EDGE tech_has_institution(relation_strength) VALUES {vals};")
                if not res.is_succeeded():
                    print(f"[停] {name} 段 {i//CHUNK} 写入失败：{res.error_msg()[:200]}", flush=True)
                    logw.writerow([time.strftime("%F %T"), name, "FAIL", len(b), res.error_msg()[:200]])
                    logf.close(); s.release(); pool.close(); conn.close(); sys.exit(1)
        # 每批回读：O(1) 探活 + 50 对 FETCH 抽验（仅 APPLY；无 props 列的替代回读）
        a_ok = alive(s, probe_vid)
        n_spot = min(50, len(batch_pairs))
        if apply:
            spot = 0
            for x, y in random.sample(batch_pairs, n_spot):
                fr = s.execute(f"FETCH PROP ON tech_has_institution \"tech_point:{x}\"->\"tech_institution:{y}\" YIELD edge AS e;")
                spot += 1 if (fr.is_succeeded() and len(fr.as_primitive()) > 0) else 0
        else:
            spot = "—"
        ok = a_ok and (spot == n_spot if apply else True)
        print(f"[{name}] 本批 {len(batch_pairs):,}｜探活 {'✅' if a_ok else '❌'}｜抽验 {spot}/{n_spot}"
              f"｜{'✅' if ok else '❌'}｜写 {time.time()-t1:5.1f}s｜累计 {time.time()-t0:6.1f}s", flush=True)
        logw.writerow([time.strftime("%F %T"), name, "OK" if apply else "DRY", len(batch_pairs),
                       f"alive={a_ok}", f"spot={spot}/{n_spot}"])
        if not ok:
            print(f"[停] {name} 回读不合格，按 §七坑1 立即停", flush=True)
            logf.close(); s.release(); pool.close(); conn.close(); sys.exit(1)
        if apply:
            ckpt["done_batches"] = batch_no
            ckpt["inserted"] += len(batch_pairs)
            json.dump(ckpt, open(CKPT, "w"))
            # 中段（第 6 批后）做一次全量 count 对账
            if batch_no == 6:
                c = count_edges(s)
                exp = base_total + ckpt["inserted"]
                print(f"[中段对账] 全量 count = {c:,}（期望 {exp:,}）{'✅' if c == exp else '❌'}｜{time.time()-t0:6.1f}s", flush=True)
                logw.writerow([time.strftime("%F %T"), name, "MIDCOUNT", c, exp])
                if c != exp:
                    print("[停] 中段全量对账不符，立即停", flush=True)
                    logf.close(); s.release(); pool.close(); conn.close(); sys.exit(1)

    skip_upto = ckpt["done_batches"] if apply else 0
    for gi in range(0, len(insts), GROUP_INSTS):
        group = insts[gi:gi + GROUP_INSTS]
        inlist = ",".join("'" + i.replace("'", "''") + "'" for i in group)
        cur.execute("SELECT technology_node_id, institution_id FROM ads_technology_institution "
                    f"WHERE is_company=0 AND institution_id IN ({inlist}) "
                    "GROUP BY technology_node_id, institution_id")
        for tcn, ins in cur.fetchall():
            src_rows += 1
            pair = (tcn, ins)
            if pair in have:
                skipped_exist += 1; continue
            if pair in seen:
                dup_in_src += 1; continue
            seen.add(pair)
            buf.append(pair)
        # 批按组边界切：累计 ≥20 万即切一批（单组超 20 万时允许超大批并告警）
        if len(buf) >= BATCH_SIZE:
            if bi >= skip_upto:
                run_batch(bi + 1, buf[:BATCH_SIZE])
            else:
                print(f"[跳过] 批 {bi+1:02d}（checkpoint 已完成）", flush=True)
            bi += 1
            buf = buf[BATCH_SIZE:]
            if len(buf) >= BATCH_SIZE:  # 理论仅当单组 >20 万时发生
                print(f"[告警] 组溢出 {len(buf):,} 对，单独成批", flush=True)
                if bi >= skip_upto:
                    run_batch(bi + 1, buf[:BATCH_SIZE])
                bi += 1
                buf = buf[BATCH_SIZE:]
    if buf:
        run_batch(bi + 1, buf)
    conn.close()

    final = count_edges(s)
    expect = base_total + (ckpt["inserted"] if apply else len(seen))
    print(f"\n[完] 模式={'APPLY' if apply else 'DRY-RUN'}｜本程声明新写 {(ckpt['inserted'] if apply else len(seen)):,}"
          f"｜源唯一对 {len(seen)+dup_in_src+skipped_exist:,}（组内重复 {dup_in_src:,}）"
          f"｜图中已有跳过 {skipped_exist:,}"
          f"\n[终值对账] 全量 count = {final:,}｜期望 = {expect:,}（起点 {base_total:,} + 新写）"
          f"{'✅' if final == expect else '❌不一致，需排查'}｜总耗时 {time.time()-t0:.0f}s", flush=True)
    logw.writerow([time.strftime("%F %T"), "FINAL", "OK" if final == expect else "MISMATCH", final, expect])
    logf.close(); s.release(); pool.close()


if __name__ == "__main__":
    main()
