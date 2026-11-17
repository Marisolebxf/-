#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KG-GRAPH-COVER-01 步骤2：灌 tech_has_institution 全量（非企业，目标 2,377,981 条）。

依据：派单-A 第 1 步 + 11-说明 §五（只收 is_company=0）、§六步2、§七坑1/2/3。
要点：
  - 每批 ≤200,000 条（§七坑1），批号 kg100-cover-01-ins-01..NN 只记录在台账与分批文件——
    边型 tech_has_institution 无 props 列（实测 schema 仅 relation_strength，禁改 schema），
    派单原文的 props.batch / CONTAINS 回读不可行；偏离以「分批文件 + 全量 count 差 + 每批抽验」
    代替，写入对账文档 §五。
  - 每批后回读用 O(1) 探活 + 50 对 FETCH 抽验（全表 count(e) 在 2.4M 边下较慢，
    不逐批做；中段与终段各做一次全量 count 对账）。
  - 断点续跑（2026-11-17 评审修复版）：**不按批号跳批**——每次启动重导图内全部已有端点对
    （have），已写过的对天然被 have 过滤、不会重写（幂等）；组内查询带 ORDER BY 保证
    批次组成确定。旧版按 checkpoint 批号跳批存在两个缺陷：①Doris GROUP BY 组内顺序
    不保证确定，续跑时批边界可能漂移导致漏写；②续跑后期望值把 checkpoint 里已写批
    重复累计（base_total 已含已写批 + ckpt.inserted 再加一次）。
    【实际影响声明】2026-11-17 正式执行为单程完成（每批全绿、中段/终段两次全量 count
    分毫不差），未触发续跑路径，图内数据不受上述缺陷影响；本修复保证复跑正确性。
  - 任何失败立即停（§七坑1）。
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
    pool = ConnectionPool()
    assert pool.init([("10.50.75.136", 9669)], NebulaConfig()), "图库建连失败"
    s = pool.get_session(os.environ["NEBULA_USER"], os.environ["NEBULA_PASS"])
    assert s.execute(f"USE {SPACE};").is_succeeded()
    base_total = count_edges(s)
    print(f"[探活] 当前 tech_has_institution = {base_total:,}；模式={'APPLY 真写' if apply else 'DRY-RUN'}", flush=True)

    # 1) 图内全部已有端点对 = 防重集 + 续跑幂等基础（每次启动重导，含历史与已写批）
    r = s.execute("MATCH (a:tech_point)-[e:tech_has_institution]->(b:tech_institution) "
                  "RETURN id(a) AS x, id(b) AS y;")
    have = set((row["x"].split(":", 1)[1], row["y"].split(":", 1)[1]) for row in r.as_primitive())
    probe_vid = "tech_institution:" + next(iter(have))[1]
    assert alive(s, probe_vid), "探活失败"
    print(f"[防重] 图内已有端点对 {len(have):,}（续跑时已写批天然落入此集，不会重写）", flush=True)

    # 2) 分组拉源表（非企业）：先 DISTINCT 机构，再按组 IN(...) + GROUP BY 去重 + ORDER BY 定序
    conn = pymysql.connect(host=os.environ["DORIS_HOST"], port=int(os.environ["DORIS_PORT"]),
                           user=os.environ["DORIS_USER"], password=os.environ["DORIS_PASS"],
                           database=os.environ["DORIS_DB"], connect_timeout=15, read_timeout=300)
    cur = conn.cursor()
    t_d = time.time()
    cur.execute("SELECT DISTINCT institution_id FROM ads_technology_institution WHERE is_company=0")
    insts = sorted(row[0] for row in cur.fetchall() if row[0])
    print(f"[源] 非企业机构 {len(insts):,} 家（DISTINCT {time.time()-t_d:.1f}s）", flush=True)

    inserted_this_run = 0   # 仅本次进程新写数（期望值不再用 checkpoint 累计，防重复计数）
    last_batch = 0
    buf = []
    seen = set()            # 本程待写去重（GROUP BY 已去重，双保险）
    dup_in_src = skipped_exist = 0
    t0 = time.time()
    logf = open(LOG, "a", newline="")
    logw = csv.writer(logf)

    def run_batch(batch_no, batch_pairs):
        nonlocal inserted_this_run, last_batch
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
        inserted_this_run += len(batch_pairs)
        last_batch = batch_no
        if apply:
            json.dump({"last_batch": last_batch, "inserted_this_run": inserted_this_run},
                      open(CKPT, "w"))  # 观测用；续跑正确性不依赖它
            # 中段（第 6 批后）全量 count 对账：期望 = 起点基数 + 本程已写（不叠加 checkpoint）
            if batch_no == 6:
                c = count_edges(s)
                exp = base_total + inserted_this_run
                print(f"[中段对账] 全量 count = {c:,}（期望 {exp:,}）{'✅' if c == exp else '❌'}｜{time.time()-t0:6.1f}s", flush=True)
                logw.writerow([time.strftime("%F %T"), name, "MIDCOUNT", c, exp])
                if c != exp:
                    print("[停] 中段全量对账不符，立即停", flush=True)
                    logf.close(); s.release(); pool.close(); conn.close(); sys.exit(1)

    for gi in range(0, len(insts), GROUP_INSTS):
        group = insts[gi:gi + GROUP_INSTS]
        inlist = ",".join("'" + i.replace("'", "''") + "'" for i in group)
        cur.execute("SELECT technology_node_id, institution_id FROM ads_technology_institution "
                    f"WHERE is_company=0 AND institution_id IN ({inlist}) "
                    "GROUP BY technology_node_id, institution_id "
                    "ORDER BY technology_node_id, institution_id")   # 定序：批次组成确定
        for tcn, ins in cur.fetchall():
            pair = (tcn, ins)
            if pair in have:            # 历史遗留 + 续跑时本单已写的对，一律跳过（幂等）
                skipped_exist += 1; continue
            if pair in seen:
                dup_in_src += 1; continue
            seen.add(pair)
            buf.append(pair)
        # 批按组边界切：累计 ≥20 万即切一批（单组超 20 万时允许超大批并告警）
        if len(buf) >= BATCH_SIZE:
            run_batch(last_batch + 1, buf[:BATCH_SIZE])
            buf = buf[BATCH_SIZE:]
            if len(buf) >= BATCH_SIZE:
                print(f"[告警] 组溢出 {len(buf):,} 对，单独成批", flush=True)
                run_batch(last_batch + 1, buf[:BATCH_SIZE])
                buf = buf[BATCH_SIZE:]
    if buf:
        run_batch(last_batch + 1, buf)
    conn.close()

    final = count_edges(s)
    expect = base_total + len(seen)     # 期望只算本程新写，与已写批无关
    print(f"\n[完] 模式={'APPLY' if apply else 'DRY-RUN'}｜本程新写 {len(seen):,}"
          f"｜源内重复对 {dup_in_src:,}｜图中已有跳过 {skipped_exist:,}（含历史遗留与续跑已写）"
          f"\n[终值对账] 全量 count = {final:,}｜期望 = {expect:,}（起点 {base_total:,} + 本程新写）"
          f"{'✅' if final == expect else '❌不一致，需排查'}｜总耗时 {time.time()-t0:.0f}s", flush=True)
    logw.writerow([time.strftime("%F %T"), "FINAL", "OK" if final == expect else "MISMATCH", final, expect])
    logf.close(); s.release(); pool.close()


if __name__ == "__main__":
    main()
