#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T04 灌数脚本（源：久新 Doris → 目标：demo_gkx_chain）定案版 2026-11-12

口径依据：唐绍祖 11-11 答复 + SDD T04 卡重写（修订 27）：
  M07 不建（无源）；M08 只真隶属 17,426（role 非空，方向对调 机构→项目）；
  M09 专利段 85,069；点：person 100,000 / research 83,745 全量（主数据）、
  project 17,402 / patent 70,496 随边补建、paper 0。
  对账分母=应灌子集数。批号格式 comply-<日期>-t04。

⚠️ 写库脚本。--probe/--dry-run 只读不写；真灌须显式 --pilot N / --full + --batch。
铁律：
  - 目标空间恒为 demo_gkx_chain，绝不写 gkx_chain。
  - 边 props 带 batch + 源字段 JSON；随边补建点 props 带批号与来源标记。
  - 端点先批量 FETCH 探测，缺则建（防 Nebula 静默空壳点）；仍缺的边跳过留档 CSV。
  - 幂等：rank 恒 0，(src,dst) 去重后写入（同键重灌=覆盖不翻倍）；已存在点跳过。
  - 凭据走环境变量，不落盘。

用法：
  export NEBULA_ADDR=... NEBULA_USER=... NEBULA_PASS=...
  export DORIS_ADDR=47.93.119.170:29030 DORIS_USER=test2 DORIS_PASS=...
  python3 t04_loader.py --rel m09 --probe
  python3 t04_loader.py --rel m09 --dry-run 100
  python3 t04_loader.py --rel m09 --pilot 1000 --batch comply-20261112-t04-1
  python3 t04_loader.py --rel m09 --full   --batch comply-20261112-t04-2
  python3 t04_loader.py --rel person --full --batch comply-20261112-t04-p1   # 主数据点全量
"""
import argparse
import json
import os
import sys

SPACE = "demo_gkx_chain"
DORIS_DB = "gkx_technology_analysis_dev"
M08_WHERE = "a.institution_role_code IS NOT NULL AND a.institution_role_code != ''"

# ── 任务定义（kind: edge=边 / points=主数据点全量）─────────────────
# VID 口径（11-12 实测：画像表无 patent_no/project_no 列 → 按 SDD 退路规则用主键 *_id）：
#   person:<talent_id> / inst:<institution_id> / patent:<patent_id> / proj:<project_id>
RELS = {
    # M09 人才 author_of 专利（person→patent 不许反转），应灌 85,069
    # name 走 LEFT JOIN 一次带出（实测 IN 批查 177 万行画像表公网需 ~50 分钟，JOIN 全量 47s 级）
    "m09": {
        "kind": "edge",
        "src_sql": (f"SELECT a.talent_id, a.patent_id, b.title AS dst_name_col "
                    f"FROM {DORIS_DB}.ads_talent_patent a "
                    f"LEFT JOIN {DORIS_DB}.ads_patent_profile b ON a.patent_id = b.patent_id"),
        "src_tag": "person", "dst_tag": "patent",
        "src_prefix": "person:", "dst_prefix": "patent:",
        "src_key": "talent_id", "dst_key": "patent_id",
        "edge": "author_of", "edge_props": {},
        "dst_name": {"table": "ads_patent_profile", "key": "patent_id", "col": "title"},
        "count_sql": f"SELECT count(*) FROM {DORIS_DB}.ads_talent_patent",
        "expect": 85069,
    },
    # M08 机构 participate 项目（research→project；源表方向 项目→机构 已在 SELECT 对调），应灌 17,426
    "m08": {
        "kind": "edge",
        "src_sql": (f"SELECT a.institution_id, a.project_id, a.relation_type, a.institution_role_code, "
                    f"b.name AS dst_name_col "
                    f"FROM {DORIS_DB}.ads_project_institution a "
                    f"LEFT JOIN {DORIS_DB}.ads_project_profile b ON a.project_id = b.project_id "
                    f"WHERE {M08_WHERE}"),
        "src_tag": "research", "dst_tag": "project",
        "src_prefix": "inst:", "dst_prefix": "proj:",
        "src_key": "institution_id", "dst_key": "project_id",
        "edge": "participate", "edge_props": {"relation_type": "relation_type",
                                              "institution_role_code": "institution_role_code"},
        "dst_name": {"table": "ads_project_profile", "key": "project_id", "col": "name"},
        "count_sql": (f"SELECT count(*) FROM {DORIS_DB}.ads_project_institution a "
                      f"WHERE {M08_WHERE}"),
        "expect": 17426,
    },
    # 主数据点全量：person 100,000
    "person": {
        "kind": "points",
        "src_sql": f"SELECT talent_id, name AS name FROM {DORIS_DB}.ads_talent_profile",
        "tag": "person", "prefix": "person:", "key_col": "talent_id", "name_col": "name",
        "extra_props": {}, "count_sql": f"SELECT count(*) FROM {DORIS_DB}.ads_talent_profile",
        "expect": 100000,
    },
    # 主数据点全量：research 83,745（institution_type_id 原值入 props）
    "research": {
        "kind": "points",
        "src_sql": (f"SELECT institution_id, name AS name, institution_type_id AS institution_type_id "
                    f"FROM {DORIS_DB}.ads_institution_profile"),
        "tag": "research", "prefix": "inst:", "key_col": "institution_id", "name_col": "name",
        "extra_props": {"institution_type_id": "institution_type_id"},
        "count_sql": f"SELECT count(*) FROM {DORIS_DB}.ads_institution_profile",
        "expect": 83745,
    },
}
PROBE_TABLES = ["ads_talent_patent", "ads_project_institution", "ads_patent_profile",
                "ads_project_profile", "ads_talent_profile", "ads_institution_profile"]
PAGE = 20000
FETCH_BATCH = 200   # 批量 FETCH / 批量 INSERT 点数
EDGE_BATCH = 200    # 批量 INSERT 边数


def doris_connect():
    import pymysql
    addr = os.environ.get("DORIS_ADDR", "47.93.119.170:29030")
    user, pw = os.environ.get("DORIS_USER"), os.environ.get("DORIS_PASS")
    if not user or not pw:
        sys.exit("❌ 未设置 DORIS_USER / DORIS_PASS")
    host, port = addr.split(":")
    return pymysql.connect(host=host, port=int(port), user=user, password=pw,
                           charset="utf8mb4", read_timeout=600), addr


def nebula_connect():
    from nebula3.gclient.net import ConnectionPool
    from nebula3.Config import Config as NebulaConfig
    addr = os.environ.get("NEBULA_ADDR", "10.50.75.136:9669")
    user, pw = os.environ.get("NEBULA_USER"), os.environ.get("NEBULA_PASS")
    host, port = addr.split(":")
    pool = ConnectionPool()
    if not pool.init([(host, int(port))], NebulaConfig()):
        sys.exit(f"❌ 连不上 {addr}")
    sess = pool.get_session(user, pw)
    if not sess.execute(f"USE {SPACE}").is_succeeded():
        sys.exit(f"❌ 进不了 {SPACE}（绝不写 gkx_chain）")
    return pool, sess


def q(s):
    # nGQL 字符串字面量：反斜杠/引号/换行/回车/制表全部转义（源表名含裸换行曾致语句断裂）
    s = str(s)
    for a, b in (("\\", "\\\\"), ('"', '\\"'), ("\n", "\\n"), ("\r", "\\r"), ("\t", "\\t")):
        s = s.replace(a, b)
    return '"' + s + '"'


def read_src(conn, sql, limit):
    """读源查询，返回 list[dict]（一次性拉全量——Doris LIMIT/OFFSET 无序深翻页
    既慢（MPP 每轮重扫）又有漏/重行风险，全量 10 万行×数列仅数 MB）"""
    cur = conn.cursor()
    cur.execute(sql if limit is None else f"{sql} LIMIT {limit}")
    batch = cur.fetchall()
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, b)) for b in batch]


def fetch_existing(sess, tag, vids):
    """批量探测点存在性，返回 {vid: name}（空壳/兜底名靠它识别）"""
    exist = {}
    for i in range(0, len(vids), FETCH_BATCH):
        chunk = vids[i:i + FETCH_BATCH]
        nql = (f"FETCH PROP ON {tag} " + ",".join(q(v) for v in chunk) +
               f" YIELD id(vertex) AS v, `{tag}`.name AS name")
        r = sess.execute(nql)
        if r.is_succeeded():
            for row in (r.as_primitive() or []):
                exist[row.get("v")] = row.get("name") or ""
    return exist


def insert_points(sess, tag, items, batch_label, extra=None):
    """批量建点 items=[(vid, name, props_dict)]，返回成功数"""
    ok = 0
    for i in range(0, len(items), FETCH_BATCH):
        chunk = items[i:i + FETCH_BATCH]
        vals = []
        for vid, name, props in chunk:
            pj = dict(props)
            pj["batch"] = batch_label
            if extra:
                pj.update(extra)
            vals.append(f"{q(vid)}:({q(name or vid.split(':', 1)[1])}, "
                        f"{q(json.dumps(pj, ensure_ascii=False))})")
        nql = f"INSERT VERTEX {tag} (name, props) VALUES " + ", ".join(vals) + ";"
        r = sess.execute(nql)
        if r.is_succeeded():
            ok += len(chunk)
        else:
            print(f"  ⚠ 建点批失败（{len(chunk)} 个）: {r.error_msg()[:80]}")
    return ok


def fetch_names(conn, table, key_col, name_col, keys):
    """批量 IN 查询 key→name 映射（Doris MPP，分批 1000）"""
    out = {}
    if not keys:
        return out
    cur = conn.cursor()
    for i in range(0, len(keys), 1000):
        chunk = keys[i:i + 1000]
        in_list = ",".join(f"'{k}'" for k in chunk)
        try:
            cur.execute(f"SELECT {key_col}, {name_col} FROM {DORIS_DB}.{table} "
                        f"WHERE {key_col} IN ({in_list})")
            for k, v in cur.fetchall():
                if v is not None:
                    out[k] = str(v)
        except Exception as ex:
            print(f"  ⚠ name 查询批失败（{len(chunk)}）: {ex}")
    return out


def run_edge(sess, cfg, rows, batch, skip_log, dry=False, doris_conn=None):
    """边任务：去重→端点探测补建（dst 带画像名）→批量写边"""
    seen, dedup = set(), []
    for r in rows:
        if not r.get(cfg["src_key"]):
            continue
        if not r.get(cfg["dst_key"]):
            skip_log.write(f",{r.get(cfg['dst_key'])},dst_key_null\n")
            continue
        svid = cfg["src_prefix"] + str(r[cfg["src_key"]])
        dvid = cfg["dst_prefix"] + str(r[cfg["dst_key"]])
        k = (svid, dvid)
        if k in seen:
            continue
        seen.add(k)
        dedup.append((svid, dvid, r))
    print(f"  去重后边 {len(dedup)}（源行 {len(rows)}，重复 {len(rows) - len(dedup)}）")

    stmts = []  # (svid, dvid, props_json)
    for svid, dvid, r in dedup:
        pj = {"batch": batch}
        for p, c in cfg["edge_props"].items():
            if r.get(c) is not None:
                pj[p] = str(r[c])
        stmts.append((svid, dvid, json.dumps(pj, ensure_ascii=False)))
    if dry:
        for svid, dvid, pj in stmts[:5]:
            print(f'  INSERT EDGE {cfg["edge"]} (weight, props) VALUES '
                  f'{q(svid)}->{q(dvid)}:(1.0, {q(pj)});')
        print(f"  …共 {len(stmts)} 条边语句（未写库）")
        return len(dedup), 0, 0

    # 端点先探后补（防空壳）；dst 新建/名兜底点带画像表名称（JOIN 行内名优先，IN 兜底）
    src_vids = sorted({s for s, _, _ in dedup})
    dst_vids = sorted({d for _, d, _ in dedup})
    print(f"  端点：src {len(src_vids)} / dst {len(dst_vids)}，探测中…")
    src_exist = fetch_existing(sess, cfg["src_tag"], src_vids)
    dst_exist = fetch_existing(sess, cfg["dst_tag"], dst_vids)
    src_new = [(v, "", {"source": "T04随边建点"}) for v in src_vids if v not in src_exist]
    dst_todo = [v for v in dst_vids if v not in dst_exist]
    dst_fix = [v for v in dst_vids if v in dst_exist
               and (not dst_exist[v] or dst_exist[v] == v.split(":", 1)[1])]
    row_names = {}   # JOIN 带出的行内名
    for svid, dvid, r in dedup:
        nm = r.get("dst_name_col")
        if nm and dvid not in row_names:
            row_names[dvid] = str(nm)
    need = dst_todo + dst_fix
    dst_names = {v: row_names[v] for v in need if v in row_names}
    missing = [v for v in need if v not in dst_names]
    if missing and doris_conn is not None and "dst_name" in cfg:
        dn = cfg["dst_name"]
        raw_keys = [v.split(":", 1)[1] for v in missing]
        got = fetch_names(doris_conn, dn["table"], dn["key"], dn["col"], raw_keys)
        dst_names.update({cfg["dst_prefix"] + k: v for k, v in got.items()})
        print(f"  画像名称：JOIN 带出 {len(need) - len(missing)}，IN 兜底命中 {len(got)}/{len(missing)}")
    dst_new = [(v, dst_names.get(v, ""), {"source": "T04随边建点"}) for v in need]
    made = insert_points(sess, cfg["src_tag"], src_new, batch)
    made += insert_points(sess, cfg["dst_tag"], dst_new, batch)
    print(f"  已存在点：src {len(src_exist)} + dst {len(dst_exist)}"
          f"（dst 名兜底待修 {len(dst_fix)}）；补建 src {len(src_new)} + dst {len(need)}（成功 {made}）")

    ok = skipped = 0
    for i in range(0, len(stmts), EDGE_BATCH):
        chunk = stmts[i:i + EDGE_BATCH]
        values = ", ".join(f"{q(s)}->{q(d)}:(1.0, {q(pj)})"
                           for s, d, pj in chunk)
        r = sess.execute(f'INSERT EDGE {cfg["edge"]} (weight, props) VALUES {values};')
        if r.is_succeeded():
            ok += len(chunk)
        else:
            # 整批失败则逐条重试定位坏行
            for svid, dvid, pj in chunk:
                r2 = sess.execute(f'INSERT EDGE {cfg["edge"]} (weight, props) VALUES '
                                  f'{q(svid)}->{q(dvid)}:(1.0, {q(pj)});')
                if r2.is_succeeded():
                    ok += 1
                else:
                    skipped += 1
                    skip_log.write(f"{svid},{dvid},{r2.error_msg()[:60]}\n")
        if (i // EDGE_BATCH) % 10 == 0:
            print(f"    边 {i + len(chunk)}/{len(stmts)}：ok {ok} / skip {skipped}", flush=True)
    return len(dedup), ok, skipped


def run_points(sess, cfg, rows, batch, dry=False):
    """主数据点任务：全量→探测→补缺→计数"""
    items = []
    for r in rows:
        if not r.get(cfg["key_col"]):
            continue
        vid = cfg["prefix"] + str(r[cfg["key_col"]])
        props = {}
        for p, c in cfg["extra_props"].items():
            if r.get(c) is not None:
                props[p] = str(r[c])
        items.append((vid, r.get(cfg["name_col"]) or "", props))
    print(f"  源点 {len(items)}（应灌 {cfg['expect']}）")
    if dry:
        print(f"  样例：{items[0] if items else '无'}")
        return len(items), 0, 0
    vids = [v for v, _, _ in items]
    exist = fetch_existing(sess, cfg["tag"], vids)
    # 覆盖写：主数据全量=源表真值，幂等覆盖随边/T03 兜底名点（终态全带真名，批号可溯）
    for _, _, p in items:
        p["source"] = "T04主数据全量"
    made = insert_points(sess, cfg["tag"], items, batch)
    print(f"  已存在 {len(exist)}（含随边/T03 所建，覆盖写真名）；全量覆盖写 {len(items)}（成功 {made}）")
    return len(items), made, len(items) - made


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rel", choices=list(RELS), required=True)
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--dry-run", type=int, metavar="N")
    ap.add_argument("--pilot", type=int, metavar="N")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--batch")
    args = ap.parse_args()
    cfg = RELS[args.rel]
    write_n = args.dry_run or args.pilot or (None if args.full else 3)

    conn, daddr = doris_connect()
    if args.probe:
        cur = conn.cursor()
        cur.execute(cfg["count_sql"])
        row = cur.fetchone()
        print(f"== {args.rel} 探查（{daddr}）==\n总行数：{row[0] if row else '?'}（应灌 {cfg['expect']}）")
        for r in read_src(conn, cfg["src_sql"], 3):
            print(" ", r)
        for t in PROBE_TABLES:
            try:
                cur.execute(f"SHOW COLUMNS FROM {DORIS_DB}.{t}")
                names = [c[0] for c in cur.fetchall()]
                hits = [c for c in ("patent_no", "project_no", "talent_id", "institution_id",
                                    "name", "institution_role_code", "relation_type") if c in names]
                print(f"  {t}: 关键列命中 {hits}")
            except Exception as ex:
                print(f"  {t}: ❌ {ex}")
        conn.close()
        return

    if (args.pilot or args.full) and not args.batch:
        sys.exit("❌ 真灌必须 --batch 批号（格式 comply-<日期>-t04[-序号]）")
    rows = read_src(conn, cfg["src_sql"], write_n)
    print(f"== {args.rel} {'dry-run' if args.dry_run else '真灌 ' + args.batch} ==")
    print(f"源行 {len(rows)}")

    skip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             f"skip-{args.rel}-{(args.batch or 'dryrun').replace('/', '_')}.csv")
    skip_log = open(skip_path, "w")
    skip_log.write("src_vid,dst_vid,reason\n")

    pool = None
    try:
        pool, sess = nebula_connect()
        if cfg["kind"] == "edge":
            run_edge(sess, cfg, rows, args.batch, skip_log,
                     dry=bool(args.dry_run), doris_conn=conn)
        else:
            run_points(sess, cfg, rows, args.batch, dry=bool(args.dry_run))
        if not args.dry_run:
            # 回读对账（按批号）
            if cfg["kind"] == "edge":
                r = sess.execute(f'MATCH ()-[e:{cfg["edge"]}]->() WHERE e.props CONTAINS '
                                 f'{q(args.batch)} RETURN count(e) AS c')
            else:
                # TRS 方言：MATCH WHERE 里点属性须带 tag 前缀（无前缀静默不命中）
                r = sess.execute(f'MATCH (v:{cfg["tag"]}) WHERE v.`{cfg["tag"]}`.props CONTAINS '
                                 f'{q(args.batch)} RETURN count(v) AS c')
            data = r.as_primitive() if r.is_succeeded() else None
            readback = data[0]["c"] if data else f"❌ {r.error_msg()}"
            print(f"\n回读（批号计数）：{readback}｜应灌 "
                  f"{cfg['expect'] if args.full else '(试点)'}")
    finally:
        skip_log.close()
        conn.close()
        if pool:
            pool.close()
    print(f"跳过留档：{skip_path}")


if __name__ == "__main__":
    main()
