#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20261021 版 · 研究领域分析族（DS_09 RESEARCH_001-004）共用算路。

数据面：**只读三方库 gkx**（唯一入口 `_gkxdb.gkx()`，该模块见 `demo_` 直接 raise）。
口径与原 20261020 版逐项一致：三维 Jaccard（IPC4 / 关键词 / 学者）+ 可用维等权；
本文件只换数据面，不改公式。

本文件集中承担四件事，避免 001-004 各自重复扫 294 万件专利：
  1. 企业入集（专利 TopN 申请人 x 机构底册，一次聚合落缓存）；
  2. 三维集合抽取：IPC4 全量 GROUP BY、关键词按企业抽样、学者按机构名精确对齐；
  3. 论文-企业机构边（`dwd_zh_author.institution` 精确 + 前缀两套口径）；
  4. 002 的特征缓存，供 003 / 004 复用。

行数一律取自 `_work_gkx21/GKX_INVENTORY.json`（库存实测值），本文件不对大表重复
`COUNT(*)`；只跑指标专属聚合（去重 / 分桶 / 占比 / 前缀匹配）。
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import _gkxdb

HERE = Path(__file__).parent
CACHE = HERE / "_snapshots21"
CACHE.mkdir(exist_ok=True)
WORK = HERE.parent / "_work_gkx21"

G = "gkx."
MIN_PATENTS = 30          # 入集门槛（与旧版一致）
CAND_N = 120              # 002/003/004 候选申请人
UNIVERSE_N = 60           # 002/003/004 入集企业数
N_COMPANY_001 = 40        # 001 入集机构数
KW_TOP = 80               # 001 关键词集合 Top80
KW_SAMPLE_002 = 1200      # 002/003/004 每家企业关键词抽样件数
KW_SAMPLE_001 = 12000     # 001 每家企业关键词抽样上限


# ------------------------------------------------------------------ 连接
def q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def qd(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


# ------------------------------------------------------------------ 缓存
def cache_path(name):
    return CACHE / name


def load_cache(name):
    p = cache_path(name)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def save_cache(name, obj):
    p = cache_path(name)
    p.write_text(json.dumps(obj, ensure_ascii=False, default=str), encoding="utf-8")
    return p


def write_out(metric_id, payload, name=None):
    path = HERE / (name or f"{metric_id}_out.json")
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str),
                    encoding="utf-8")
    return path


# ------------------------------------------------------------------ 库存行数
def inventory():
    """gkx 逐表实测行数（GKX_INVENTORY.json）。行数只读库存，不重复摸大表。"""
    return json.loads((WORK / "GKX_INVENTORY.json").read_text(encoding="utf-8"))


def rows_of(table):
    d = inventory().get(table)
    return int(d["rows"]) if d else None


# ------------------------------------------------------------------ 底册
def base_rows():
    """189,116 行机构底册（org_id, external_id, name_cn, province, city, incorporation_year）。

    复用产业链簇已落盘的 `_snapshots21/base_20261021.json`，避免对
    `dwd_org_base_info` 再做大表全扫（该表无覆盖索引，全表 COUNT(*) 实测 87.7 秒）。
    """
    import _gkx21_common as c21
    return c21.base_rows()


def base_by_name():
    """name_cn -> {org_id, city, province}；重名 47 组先按 name 去重（保留首行），
    避免按名称聚合时把专利/论文重复计数（见 DATA_FACTS 3.5）。"""
    out = {}
    for r in base_rows():
        nm = r[2]
        if nm and nm not in out:
            out[nm] = {"org_id": r[0], "external_id": r[1], "city": r[4],
                       "province": r[3], "incorporation_year": r[5]}
    return out


# ------------------------------------------------------------------ 申请人
def applicants():
    """专利量 >=30 的申请人及其专利数（降序）。

    一次 `GROUP BY first_applicant_name` 全表聚合后落缓存；这是本族唯一需要扫
    294 万行宽表的地方，其余指标一律读缓存或按申请人 IN 列表取数。
    """
    d = load_cache("research_applicants_20261021.json")
    if d is not None:
        return d
    rows = q("SELECT first_applicant_name n, COUNT(*) c FROM " + G + "dwd_patent "
             "WHERE first_applicant_name IS NOT NULL AND first_applicant_name<>'' "
             "GROUP BY 1 HAVING COUNT(*) >= %s ORDER BY 2 DESC", (MIN_PATENTS,))
    d = [{"name": r[0], "patents": int(r[1])} for r in rows]
    save_cache("research_applicants_20261021.json", d)
    return d


def universe_002():
    """002/003/004 的 60 家入集企业：Top120 申请人 交 底册精确同名 -> 前 60。

    与旧版逐字同规则（候选 120、求交、取前 60），只把数据面从旧开发库（已停用、不再使用）换成 gkx。
    """
    d = load_cache("research_universe_002_20261021.json")
    if d is not None:
        return d
    bn = base_by_name()
    cand = applicants()[:CAND_N]
    matched = [(a["name"], a["patents"]) for a in cand if a["name"] in bn]
    univ = matched[:UNIVERSE_N]
    d = {"candidate_n": len(cand), "matched": len(matched),
         "names": [n for n, _ in univ], "patents": {n: c for n, c in univ},
         "org": {n: bn[n] for n, _ in univ}}
    save_cache("research_universe_002_20261021.json", d)
    return d


def universe_001():
    """001 的 40 家入集机构：底册 city 含「深圳」且专利 >=30 件，按专利量取前 40。"""
    d = load_cache("research_universe_001_20261021.json")
    if d is not None:
        return d
    bn = base_by_name()
    picked = []
    for a in applicants():
        b = bn.get(a["name"])
        if not b:
            continue
        if "深圳" in (b["city"] or "") and a["patents"] >= MIN_PATENTS:
            picked.append({"name": a["name"], "patents": a["patents"],
                           "org_id": b["org_id"], "city": b["city"]})
        if len(picked) >= N_COMPANY_001:
            break
    d = {"names": [p["name"] for p in picked], "rows": picked}
    save_cache("research_universe_001_20261021.json", d)
    return d


# ------------------------------------------------------------------ 三维集合
def ipc_sets(names, tag=""):
    """IPC4 集合（全量 GROUP BY，不抽样）+ 每家企业 IPC4 出现次数。"""
    d = load_cache(f"research_ipc_{tag or len(names)}_20261021.json")
    if d is not None:
        return d
    ph = ",".join(["%s"] * len(names))
    rows = q("SELECT first_applicant_name n, LEFT(main_classification_ipcr,4) ipc4, "
             "COUNT(*) c FROM " + G + "dwd_patent WHERE first_applicant_name IN (" + ph + ") "
             "AND main_classification_ipcr IS NOT NULL AND main_classification_ipcr<>'' "
             "GROUP BY 1,2", names)
    out = {n: {} for n in names}
    for n, k, c in rows:
        if k and re.match(r"^[A-H]\d{2}[A-Z]$", k):
            out[n][k] = int(c)
    d = {"sets": {n: sorted(v) for n, v in out.items()}, "counts": out}
    save_cache(f"research_ipc_{tag or len(names)}_20261021.json", d)
    return d


def parse_kw(raw):
    """`dwd_patent.keywords` 为 JSON 数组字符串；解析失败返回空（坏值计入披露）。"""
    if raw is None:
        return [], 0
    s = str(raw).strip()
    if not s:
        return [], 0
    try:
        v = json.loads(s)
        if isinstance(v, list):
            return [str(t).strip() for t in v if str(t).strip()], 1
        return [], 0
    except Exception:
        return [], 0


def kw_sets(names, sample, tag):
    """关键词集合：每家企业前 `sample` 件专利的 keywords 并集。"""
    d = load_cache(f"research_kw_{tag}_20261021.json")
    if d is not None:
        return d
    sets, ok, bad = {}, 0, 0
    for n in names:
        got = set()
        rows = q("SELECT keywords FROM " + G + "dwd_patent WHERE first_applicant_name=%s "
                 "AND keywords IS NOT NULL AND keywords<>'' LIMIT %s", (n, sample))
        for (raw,) in rows:
            toks, good = parse_kw(raw)
            got |= set(toks)
            ok += good
            bad += (1 - good)
        sets[n] = got
    d = {"sets": {n: sorted(v) for n, v in sets.items()},
         "json_ok": ok, "json_bad": bad, "sample_per_firm": sample}
    save_cache(f"research_kw_{tag}_20261021.json", d)
    return d


def scholar_sets(names):
    """学者集合：`dwd_scholar.scholar_org_name_zh` 精确等于企业名 -> scholar_id 集合。

    注意学者宇宙：`dwd_scholar` 21,316 位，与 `dwd_scholar_talent_flag` 20,030 位
    的交集仅 1,858（8.72%）。本指标只用前者，且**分母固定写 21,316**，不与人才
    标签宇宙混算（见正文 3.x 双基线披露）。
    """
    d = load_cache("research_scholar_sets_20261021.json")
    if d is not None:
        return d
    ph = ",".join(["%s"] * len(names))
    rows = q("SELECT scholar_org_name_zh org, scholar_id sid FROM " + G + "dwd_scholar "
             "WHERE scholar_org_name_zh IN (" + ph + ")", names)
    out = {n: set() for n in names}
    for org, sid in rows:
        if org in out:
            out[org].add(str(sid))
    d = {"sets": {n: sorted(v) for n, v in out.items()}}
    save_cache("research_scholar_sets_20261021.json", d)
    return d


def paper_edges(names):
    """论文-企业机构边：`dwd_zh_author.institution` 精确 + 前缀两套口径。

    返回 {name: [paper_id...]}、精确命中篇数、`dwd_zh_paper_classification` 关键词。
    前缀匹配是必要的：论文署名几乎都带院系后缀（「华南理工大学化学与化工学院」），
    精确匹配会把 60 家企业压到个位数篇。
    """
    d = load_cache("research_paper_edges_20261021.json")
    if d is not None:
        return d
    ph = ",".join(["%s"] * len(names))
    exact = {}
    for inst, pid in q("SELECT institution inst, paper_id pid FROM " + G + "dwd_zh_author "
                       "WHERE institution IN (" + ph + ")", names):
        if inst and pid:
            exact.setdefault(inst, set()).add(pid)
    prefix = {}
    for n in names:
        rows = q("SELECT paper_id pid FROM " + G + "dwd_zh_author WHERE institution LIKE %s",
                 (n + "%",))
        prefix[n] = {r[0] for r in rows if r[0]}
    allpid = sorted({p for s in prefix.values() for p in s})
    pk = {}
    if allpid:
        for i in range(0, len(allpid), 4000):
            chunk = allpid[i:i + 4000]
            ph2 = ",".join(["%s"] * len(chunk))
            for pid, kw in q("SELECT id, keywords FROM " + G + "dwd_zh_paper_classification "
                             "WHERE id IN (" + ph2 + ")", chunk):
                toks, _ = parse_kw(kw)
                if toks:
                    pk[str(pid)] = toks
    d = {"papers": {n: sorted(v) for n, v in prefix.items()},
         "exact_papers": sum(len(v) for v in exact.values()),
         "prefix_papers": sum(len(v) for v in prefix.values()),
         "n_firm_with_paper": sum(1 for n in names if prefix[n]),
         "paper_keywords": pk,
         "_exact_by_name": {k: sorted(v) for k, v in exact.items()}}
    save_cache("research_paper_edges_20261021.json", d)
    return d


# ------------------------------------------------------------------ 论文作者（001 D3）
def iter_papers(size=8000):
    """逐篇产出 {id, year, title, insts, authors, bad}。

    与旧版 `_innov_w6_common.iter_papers` 字段契约一致；按主键分页，避免一次拉
    100,900 篇的 `author_info_list` 撑爆内存。
    """
    off = 0
    while True:
        rows = q("SELECT id, zh_name, en_name, cover_year_start y, author_info_list ai "
                 "FROM " + G + "dwd_zh_paper ORDER BY id LIMIT %s OFFSET %s", (size, off))
        if not rows:
            return
        for r in rows:
            ai = r[4]
            insts, authors, bad = set(), [], False
            if ai:
                try:
                    arr = json.loads(ai)
                except Exception:
                    bad = True
                    arr = []
                if isinstance(arr, list):
                    for a in arr:
                        if not isinstance(a, dict):
                            continue
                        nm = (a.get("zh_name") or a.get("en_name") or "").strip()
                        aff = (a.get("institution") or a.get("affiliation") or "").strip()
                        parts = [p.strip() for p in re.split(r"[;；]", aff) if len(p.strip()) >= 4]
                        insts.update(parts)
                        if nm:
                            authors.append((nm, parts))
            yield {"id": r[0], "year": r[3], "title": r[1] or r[2] or "",
                   "insts": insts, "authors": authors, "bad": bad}
        if len(rows) < size:
            return
        off += size


IND_RX = re.compile(
    r"公司|集团|有限|股份|控股|实业|工厂|企业|厂$|"
    r"Inc\.?|Ltd\.?|LLC|Corp\.?|Co\.,|Company|Group|GmbH")


# ------------------------------------------------------------------ 统计
def jac(a, b):
    if not a or not b:
        return None
    u = len(a | b)
    return len(a & b) / u if u else None


def pct(vals, p):
    s = sorted(vals)
    return s[min(len(s) - 1, int(p * (len(s) - 1)))]


def stats(vals, nd=4):
    if not vals:
        return {"n": 0}
    s = sorted(vals)
    n = len(s)
    return {"n": n, "min": round(s[0], nd), "max": round(s[-1], nd),
            "mean": round(sum(s) / n, nd),
            "median": round((s[(n - 1) // 2] + s[n // 2]) / 2, nd),
            "p90": round(s[int(0.9 * (n - 1))], nd),
            "n_zero": sum(1 for x in s if x == 0)}


def minmax(vals):
    lo, hi = min(vals), max(vals)
    if hi - lo == 0:
        return [0.5 for _ in vals]
    return [(v - lo) / (hi - lo) for v in vals]


if __name__ == "__main__":
    t0 = time.time()
    print("patent rows(inventory)", rows_of("dwd_patent"))
    print("applicants", len(applicants()), round(time.time() - t0, 1))
    u2 = universe_002()
    print("universe_002", u2["candidate_n"], u2["matched"], len(u2["names"]))
    u1 = universe_001()
    print("universe_001", len(u1["names"]))
    print("base", len(base_rows()))
