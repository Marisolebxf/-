#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KG-GRAPH-COVER-01 步骤4：tech_point.community_id 回填（19,430 点）。

依据：派单-A 第 4 步 + 11-说明 §4.4 / §六步4。
要点：
  - 源：ads_technology_community_member（每技术点一行，共 19,430）。
  - UPDATE VERTEX ON tech_point SET community_id=...；空串不是 NULL，
    校验必须用 v.tech_point.community_id != '' 而非 IS NOT NULL（派单原文坑）。
  - 单批 19,430 < 2 万上限；写后全量校验 = 19,430。
用法：python3 cover01_s4_backfill_community.py [--apply]
凭据：环境变量 NEBULA_* / DORIS_*（不进 git）。
"""
import csv
import json
import os
import sys
import time

import pymysql
from nebula3.gclient.net import ConnectionPool
try:
    from nebula3.Config import Config as NebulaConfig
except ImportError:
    from nebula3.Config import Configs as NebulaConfig

WORK = "/home/zhangzhong_e43d4db3/qiliantupu/kg100-work"
LOG = os.path.join(WORK, "s4_batch_log.csv")
CKPT = os.path.join(WORK, "s4_checkpoint.json")
CHUNK = 100           # 每次连接发送的语句数上限（实测 >256 触发 The maximum number of statements has been exceeded）
BATCH_NAME = "kg100-cover-01-comm"
SPACE = "demo_gkx_chain"


def esc(v):
    if v is None or v == "":
        return "NULL"
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def main():
    apply = "--apply" in sys.argv
    t0 = time.time()
    # 1) 源数据（19,430 行小结果集，单查询即可）
    conn = pymysql.connect(host=os.environ["DORIS_HOST"], port=int(os.environ["DORIS_PORT"]),
                           user=os.environ["DORIS_USER"], password=os.environ["DORIS_PASS"],
                           database=os.environ["DORIS_DB"], connect_timeout=15, read_timeout=120)
    cur = conn.cursor()
    cur.execute("SELECT technology_node_id, community_id FROM ads_technology_community_member "
                "GROUP BY technology_node_id, community_id")
    rows = [(r[0], r[1]) for r in cur.fetchall() if r[0] and r[1]]
    conn.close()
    print(f"[源] (技术点,社群) 唯一行 {len(rows):,}（应为 19,430）", flush=True)

    pool = ConnectionPool()
    assert pool.init([("10.50.75.136", 9669)], NebulaConfig()), "图库建连失败"
    s = pool.get_session(os.environ["NEBULA_USER"], os.environ["NEBULA_PASS"])
    assert s.execute(f"USE {SPACE};").is_succeeded()

    # 2) 写前基线：当前非空串的 tech_point
    r = s.execute("MATCH (v:tech_point) WHERE v.tech_point.community_id != '' RETURN count(v) AS c;")
    before = list(r.as_primitive()[0].values())[0]
    print(f"[基线] community_id 非空串 = {before:,}（应为 0）", flush=True)

    logf = open(LOG, "a", newline="")
    logw = csv.writer(logf)
    if apply and rows:
        ck = json.load(open(CKPT)) if os.path.exists(CKPT) else {"done": False, "updated": 0}
        if ck["done"]:
            print("[续跑] 已完成，跳过写入", flush=True)
        else:
            stmts = []
            for tcn, comm in rows:
                stmts.append(f"UPDATE VERTEX ON tech_point \"tech_point:{tcn}\" "
                             f"SET community_id={esc(comm)};")
            for i in range(0, len(stmts), CHUNK):
                b = stmts[i:i + CHUNK]
                res = s.execute(" ".join(b))
                if not res.is_succeeded():
                    print(f"[停] 段 {i//CHUNK} 失败：{res.error_msg()[:200]}", flush=True)
                    logw.writerow([time.strftime("%F %T"), BATCH_NAME, "FAIL", len(b), res.error_msg()[:200]])
                    logf.close(); s.release(); pool.close(); sys.exit(1)
            ck = {"done": True, "updated": len(stmts)}
            json.dump(ck, open(CKPT, "w"))
    # 3) 写后校验（空串不是 NULL，必须 != ''）
    r = s.execute("MATCH (v:tech_point) WHERE v.tech_point.community_id != '' RETURN count(v) AS c;")
    after = list(r.as_primitive()[0].values())[0]
    ok = (after == 19430)
    print(f"[校验] 非空串 = {after:,}（目标 19,430）{'✅' if ok else '❌'}｜"
          f"模式={'APPLY' if apply else 'DRY-RUN'}｜{time.time()-t0:.0f}s", flush=True)
    logw.writerow([time.strftime("%F %T"), BATCH_NAME, "OK" if ok else "MISMATCH",
                   "APPLY" if apply else "DRY", after])
    logf.close(); s.release(); pool.close()
    if apply and not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
