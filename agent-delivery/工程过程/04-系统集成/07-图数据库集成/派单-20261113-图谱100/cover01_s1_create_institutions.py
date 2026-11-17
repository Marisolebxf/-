#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KG-GRAPH-COVER-01 步骤1：建 17,227 个缺失的 tech_institution 点。

依据：派单-A 第 1 步 + 11-说明 §六步1、§四4.1（缺 17,227 家 / 124,014 行边暂不可写）。
铁律：只建 tech_institution 点，不动 schema、不建空间、不删任何点边；
      默认 dry-run，--apply 才真写；可断点续（checkpoint）；每批后探活计数。
字段：institution_id / name_zh / name_en / data_version / year(=first_evidence_year)
      ——institution_type 在 Tag 中无对应字段（禁改 schema），不入库，记入对账说明。
用法：python3 cover01_s1_create_institutions.py [--apply] [--batch-size 500]
凭据：环境变量 NEBULA_USER/NEBULA_PASS（不进 git）。
"""
import csv
import json
import os
import sys
import time

from nebula3.gclient.net import ConnectionPool
try:
    from nebula3.Config import Config as NebulaConfig
except ImportError:
    from nebula3.Config import Configs as NebulaConfig

WORK = "/home/zhangzhong_e43d4db3/qiliantupu/kg100-work"
SRC_CSV = os.path.join(WORK, "missing_institutions_fields.csv")
CKPT = os.path.join(WORK, "s1_checkpoint.json")
LOG = os.path.join(WORK, "s1_batch_log.csv")
SPACE = "demo_gkx_chain"
VID_PREFIX = "tech_institution:"
BATCH_NOTE = "kg100-cover-01-s1"  # 记录用批标识（点无 props JSON，批号只入日志与对账）


def esc(v):
    if v is None or v == "":
        return "NULL"
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def load_rows():
    with open(SRC_CSV, newline="") as f:
        return [r for r in csv.DictReader(f) if r["institution_id"].strip()]


def build_stmt(batch):
    vals = []
    for r in batch:
        vid = VID_PREFIX + r["institution_id"]
        year = r["first_evidence_year"].strip()
        y = (str(int(float(year))) if year else "NULL")
        vals.append(f"\"{vid}\":({esc(r['institution_id'])}, {esc(r['name_zh'])}, "
                    f"{esc(r['name_en'])}, {esc(r['data_version'])}, {y})")
    return ("INSERT VERTEX tech_institution"
            "(institution_id, name_zh, name_en, data_version, year) VALUES "
            + ", ".join(vals) + ";")


def main():
    apply = "--apply" in sys.argv
    bsz = 500
    if "--batch-size" in sys.argv:
        bsz = int(sys.argv[sys.argv.index("--batch-size") + 1])

    rows = load_rows()
    ckpt = json.load(open(CKPT)) if os.path.exists(CKPT) else {"done_batches": [], "created": 0, "skipped_exist": 0}
    done = set(ckpt["done_batches"])

    pool = ConnectionPool()
    assert pool.init([("10.50.75.136", 9669)], NebulaConfig()), "图库建连失败"
    s = pool.get_session(os.environ["NEBULA_USER"], os.environ["NEBULA_PASS"])
    assert s.execute(f"USE {SPACE};").is_succeeded()

    r = s.execute("MATCH (v:tech_institution) RETURN count(v) AS c;")
    base = list(r.as_primitive()[0].values())[0]
    print(f"[探活] 起点 tech_institution = {base:,}；目标新建 {len(rows):,}；模式={'APPLY 真写' if apply else 'DRY-RUN'}")

    logf = open(LOG, "a", newline="")
    logw = csv.writer(logf)
    t0 = time.time()
    for i in range(0, len(rows), bsz):
        bi = i // bsz
        if bi in done:
            continue
        batch = rows[i:i + bsz]
        # 已存在防重（幂等续跑）：FETCH 一批 VID，存在即跳过
        vids = ",".join(VID_PREFIX + r["institution_id"] for r in batch)
        r = s.execute(f"FETCH PROP ON tech_institution {vids} YIELD id(vertex) AS vid;")
        exist = set()
        if r.is_succeeded():
            exist = {row["vid"] for row in r.as_primitive()}
        todo = [r_ for r_ in batch if (VID_PREFIX + r_["institution_id"]) not in exist]
        stmt = build_stmt(todo)
        if apply and todo:
            res = s.execute(stmt)
            if not res.is_succeeded():
                print(f"[停] 批 {bi} 写入失败：{res.error_msg()[:200]}")
                logw.writerow([time.strftime("%F %T"), bi, "FAIL", len(todo), res.error_msg()[:200]])
                logf.close(); s.release(); pool.close(); sys.exit(1)
        r = s.execute("MATCH (v:tech_institution) RETURN count(v) AS c;")
        now = list(r.as_primitive()[0].values())[0]
        if apply:  # dry-run 不落 checkpoint，避免把真跑的批次标记成已完成
            ckpt["created"] += len(todo)
            ckpt["skipped_exist"] += len(batch) - len(todo)
            done.add(bi)
            ckpt["done_batches"] = sorted(done)
            json.dump(ckpt, open(CKPT, "w"))
        logw.writerow([time.strftime("%F %T"), bi, "OK" if apply else "DRY", len(todo),
                       f"count={now:,}", f"+{now - base:,}"])
        print(f"[批 {bi:02d}/{(len(rows)+bsz-1)//bsz:02d}] 本批 {len(todo):>4}（跳过已存在 {len(batch)-len(todo):>3}）"
              f"｜图内计数 {now:,}（累计 +{now - base:,}）｜{time.time()-t0:5.1f}s")
        base = now

    print(f"\n[完] 拟建/已建 {ckpt['created']:,}，跳过已存在 {ckpt['skipped_exist']:,}，"
          f"模式={'APPLY' if apply else 'DRY-RUN（未写，加 --apply 真跑）'}")
    logf.close(); s.release(); pool.close()


if __name__ == "__main__":
    main()
