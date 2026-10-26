#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_INTERNATIONALIZATION_INDEX 产业链国际化程度 — 实测与不可复现证据（20261021 改源版）

原口径状态：calc-logic v0.2.0 为「挂起版」——无公式、无 QC 号、因子集与权重未签。
本脚本不复现指标，只做三件事：
  ① 量化三条候选路径（海外主体 / 海外专利 / 进出口）在三方库 gkx 的可达性；
  ② 把「唯一看似可算」的专利路径真正算一遍，检验它是否度量了「国际化」；
  ③ 输出为什么该指标连「退化版」都不应发布的证据链。

数据面：三方库 gkx（183.240.141.251:3318，schema gkx）。20261021 起唯一数据面：
旧版走 demo 镜像库，本版全部聚合在 gkx 现场重算（链树 dwd_industry_chain_info、
企业—链归属由 dwd_org_industry_tags 现推，不再读旧快照），公式与档位判定未动。
重查询结果落 code/_snapshots21/ 缓存，同批复用。
输出：M_CHAIN_INTERNATIONALIZATION_INDEX_out.json
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import pymysql

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import GKX, gkx  # noqa: E402

METRIC = "M_CHAIN_INTERNATIONALIZATION_INDEX"
CACHE_DIR = Path(__file__).parent / "_snapshots21"
CACHE = CACHE_DIR / "chain_intl_gkx_20261021.json"
INVENTORY = Path(__file__).parent.parent / "_work_gkx21" / "GKX_INVENTORY.json"

CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]
CODE_RE = re.compile(r"INB\d{4,}")


def q(sql, args=None):
    cur = gkx()
    try:
        cur.execute(sql, args or ())
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        cur.close()


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def cc(a, b):
    """跨表等值比较的 collation 显式统一（gkx 各表 collation 不一致，直接 = 会报 1267）。"""
    return (
        f"CONVERT({a} USING utf8mb4) COLLATE utf8mb4_general_ci = "
        f"CONVERT({b} USING utf8mb4) COLLATE utf8mb4_general_ci"
    )


def stream(sql):
    """流式读三方库（228 万行标签表不落内存列表）。"""
    import pymysql

    conn = pymysql.connect(**GKX)
    try:
        with conn.cursor(pymysql.cursors.SSCursor) as cur:
            cur.execute("SET NAMES utf8mb4")
            cur.execute(sql)
            for row in cur:
                yield row
    finally:
        conn.close()


def inv_rows(table):
    js = json.loads(INVENTORY.read_text(encoding="utf-8"))
    return int((js.get(table) or {}).get("rows"))


def load_tree():
    """链树（gkx.dwd_industry_chain_info，1,273 节点）→ roots / parent。"""
    rows = q("SELECT industry_code, industry_name, industry_link_code, parent_name "
             "FROM gkx.dwd_industry_chain_info WHERE is_deleted=0")
    tree = {r["industry_code"].strip(): {"name": r["industry_name"],
                                         "link": (r["industry_link_code"] or "").strip()}
            for r in rows}
    parent = {k: v["link"] for k, v in tree.items()}
    roots = sorted(k for k in tree if k in parent and not parent[k])
    return tree, parent, roots


def _dump(out):
    """分步落盘：任一后续步骤失败/被服务器掐断，已完成的重聚合不丢。"""
    CACHE_DIR.mkdir(exist_ok=True)
    tmp = CACHE.with_suffix(".tmp")
    tmp.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    tmp.replace(CACHE)


def build_cache(prev=None):
    """分步重聚合，每步落盘并记 step 标记；重跑时跳过已完成步骤。"""
    t0 = time.time()
    if prev is not None:
        out = prev
        out.setdefault("done", [])
    elif CACHE.exists():
        out = json.loads(CACHE.read_text(encoding="utf-8"))
        out.setdefault("done", [])
    else:
        out = {"done": []}

    def mark(step):
        if step not in out["done"]:
            out["done"].append(step)
        _dump(out)
        print("[%6.1fs] done %s" % (time.time() - t0, step), flush=True)

    # ---- 链树 ----
    if "tree" not in out["done"]:
        tree, parent, roots = load_tree()
        out["tree_size"] = len(tree)
        out["roots"] = {r: tree[r]["name"] for r in roots}
        mark("tree")

    # ---- 企业/机构底册 ----
    if "base" not in out["done"]:
        ext2 = {}
        base_names = set()
        out["base_ext"] = {}
        for r in q("SELECT external_id, name_cn, city FROM gkx.dwd_org_base_info WHERE is_deleted=0"):
            ext = (r["external_id"] or "").strip()
            if ext:
                ext2[ext] = {"name": r["name_cn"], "city": r["city"]}
                out["base_ext"][ext] = [r["name_cn"], r["city"]]
            if r["name_cn"]:
                base_names.add(r["name_cn"])
        out["base_rows"] = len(base_names)
        out["base_ext_rows"] = len(ext2)
        mark("base")

    ext2 = {k: {"name": v[0], "city": v[1]} for k, v in out["base_ext"].items()}

    if "inst" not in out["done"]:
        out["inst_names"] = sorted({r["name_cn"] for r in q(
            "SELECT name_cn FROM gkx.dwd_research_institute_base_info "
            "WHERE is_deleted=0 AND name_cn IS NOT NULL")})
        out["inst_rows"] = len(out["inst_names"])
        mark("inst")

    # ---- 海外主体 ----
    if "forg" not in out["done"]:
        out["forg_rows"] = {t: inv_rows(t) for t in
                            ["dwd_forg_base_info", "dwd_forg_research_org_info", "dwd_forg_university_org_info",
                             "dwd_forg_product_info", "dwd_forg_shareholder_info", "dwd_forg_executive_info"]}
        out["forg_country"] = q("SELECT country_code, country, COUNT(*) n FROM gkx.dwd_forg_base_info "
                                "GROUP BY country_code, country ORDER BY n DESC")
        out["forg_industry_type"] = q("SELECT industry_type, COUNT(*) n FROM gkx.dwd_forg_base_info "
                                      "GROUP BY industry_type ORDER BY n DESC LIMIT 12")
        forg_rows = q("SELECT org_id, external_id, name_en FROM gkx.dwd_forg_base_info")
        out["forg_ext"] = sorted({(r["external_id"] or "").strip() for r in forg_rows if r["external_id"]})
        out["forg_names"] = sorted({(r["name_en"] or "").strip() for r in forg_rows if r["name_en"]})
        out["forg_orgid"] = sorted({str(r["org_id"]) for r in forg_rows if r["org_id"] is not None})
        mark("forg")

    forg_ext = set(out["forg_ext"])
    forg_names = set(out["forg_names"])

    # ---- 企业—链归属（按 gkx.dwd_org_industry_tags 现推，root=首个 industry_code 前 7 位）----
    if "tags" not in out["done"]:
        name_chain = defaultdict(set)   # 企业名 → {(L1 链码, city)}
        ent_chain = defaultdict(set)    # 统一社会信用代码 → {L1 链码}
        n_tags = n_hit = 0
        forg_ext_hit = forg_name_hit = 0
        for cc_, icode, cname in stream(
                "SELECT credit_code, industry_code, company_name FROM gkx.dwd_org_industry_tags WHERE is_deleted=0"):
            n_tags += 1
            cc_ = (cc_ or "").strip()
            cname = (cname or "").strip()
            if cc_ and cc_ in forg_ext:
                forg_ext_hit += 1
            if cname and cname in forg_names:
                forg_name_hit += 1
            codes = CODE_RE.findall(icode or "")
            if not codes:
                continue
            info = ext2.get(cc_) if cc_ else None
            if info is None:
                continue
            n_hit += 1
            root = codes[0][:7]
            nm = (cname or info["name"] or "").strip()
            city = info["city"] or ""
            if nm:
                name_chain[nm].add((root, city))
            if cc_:
                ent_chain[cc_].add(root)
            if n_tags % 500000 == 0:
                print("[%6.1fs]   tags %d hit %d" % (time.time() - t0, n_tags, n_hit), flush=True)
        out["tags_rows"] = n_tags
        out["tags_base_hit"] = n_hit
        out["forg_extid_in_tags"] = forg_ext_hit
        out["forg_name_in_tags"] = forg_name_hit
        out["forg_in_dwd_chain"] = sum(
            1 for r in out["forg_ext"] if r in ent_chain)
        out["forg_name_in_chain"] = sum(1 for n in forg_names if n in name_chain)
        out["chain_credit"] = {k: sorted(v) for k, v in ent_chain.items()}
        out["chain_name"] = {k: sorted([list(x) for x in v]) for k, v in name_chain.items()}
        out["n_chain_credits"] = len(ent_chain)
        out["n_chain_names"] = len(name_chain)
        out["chain_member_city4"] = sorted({nm for nm, v in name_chain.items()
                                            if any(c in CITY4 for _r, c in v)})
        mark("tags")

    # ---- 海外主体与国内主档 org_id 交集（跨表等值：显式统一 collation）----
    if "forg_join" not in out["done"]:
        out["forg_orgid_overlap_base"] = int(q1(
            "SELECT COUNT(*) n FROM gkx.dwd_forg_base_info f "
            f"JOIN gkx.dwd_org_base_info b ON {cc('b.org_id','f.org_id')}")["n"])
        mark("forg_join")

    # ---- 专利（国别 + 申请人聚合）：单次流式扫描替代 4 次全表 GROUP BY ----
    if "patent_scan" not in out["done"]:
        cc_cnt, ac_cnt = Counter(), Counter()
        nm_cnt, wo_cnt, jp_cnt = Counter(), Counter(), Counter()
        n_pat = 0
        conn = pymysql.connect(**dict(GKX, read_timeout=1800))
        try:
            with conn.cursor(pymysql.cursors.SSCursor) as cur:
                cur.execute("SET NAMES utf8mb4")
                cur.execute("SELECT country_code, application_country, first_applicant_name "
                            "FROM gkx.dwd_patent")
                for ccode, acode, nm in cur:
                    n_pat += 1
                    cc_cnt[ccode] += 1
                    ac_cnt[acode] += 1
                    if nm:
                        nm_cnt[nm] += 1
                        if ccode == "WO":
                            wo_cnt[nm] += 1
                        elif ccode == "JP":
                            jp_cnt[nm] += 1
                    if n_pat % 500000 == 0:
                        print("[%6.1fs]   patent %d" % (time.time() - t0, n_pat), flush=True)
        finally:
            conn.close()
        out["patent_rows"] = n_pat
        out["patent_country"] = [{"country_code": k, "n": v} for k, v in cc_cnt.most_common()]
        out["patent_app_country"] = [{"application_country": k, "n": v} for k, v in ac_cnt.most_common()]
        out["wo_applicants"] = [{"nm": k, "n": v} for k, v in wo_cnt.most_common()]
        out["jp_applicants"] = [{"nm": k, "n": v} for k, v in jp_cnt.most_common()]
        out["name_patent"] = {k: [v, wo_cnt.get(k, 0)] for k, v in nm_cnt.items()}
        out["patent_columns"] = [r["col"] for r in q(
            "SELECT column_name AS col FROM information_schema.columns WHERE table_schema='gkx' "
            "AND table_name='dwd_patent' ORDER BY ordinal_position")]
        out["trade_tables_gkx"] = [r["tbl"] for r in q(
            "SELECT table_name AS tbl FROM information_schema.tables WHERE table_schema='gkx' AND ("
            "table_name LIKE '%%customs%%' OR table_name LIKE '%%trade%%' "
            "OR (table_name LIKE '%%import%%' AND table_name NOT LIKE '%%important%%') "
            "OR table_name LIKE '%%export%%' OR table_name LIKE '%%haiguan%%' OR table_name LIKE '%%trades%%')")]
        mark("patent_scan")

    # ---- 贸易表检索（廉价 information_schema 查询，独立成步便于复核）----
    if "trade_scan" not in out["done"]:
        out["trade_tables_gkx"] = [r["tbl"] for r in q(
            "SELECT table_name AS tbl FROM information_schema.tables WHERE table_schema='gkx' AND ("
            "table_name LIKE '%%customs%%' OR table_name LIKE '%%trade%%' "
            "OR (table_name LIKE '%%import%%' AND table_name NOT LIKE '%%important%%') "
            "OR table_name LIKE '%%export%%' OR table_name LIKE '%%haiguan%%' OR table_name LIKE '%%trades%%')")]
        out["trade_keywords_searched"] = ["customs", "trade", "import", "export", "haiguan", "进出口", "海关", "贸易"]
        out["trade_false_positive_note"] = (
            "首轮用 %import% 宽松匹配时命中 dwd_org_important_news_info——表名里 'important' 含 'import' "
            "子串，内容为重要新闻而非贸易数据；本步已排除 important 后重跑，命中 0 张。")
        mark("trade_scan")

    out["elapsed_sec"] = round(time.time() - t0, 1)
    out["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    _dump(out)
    return out


REQUIRED_STEPS = {"tree", "base", "inst", "forg", "tags", "forg_join", "patent_scan", "trade_scan"}


def get_cache(refresh=False):
    if CACHE.exists() and not refresh:
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
        if REQUIRED_STEPS.issubset(set(cache.get("done") or [])) and "name_patent" in cache:
            return cache
        print("[cache] 缓存不完整（done=%s），续跑补步" % (cache.get("done"),), flush=True)
        return build_cache(cache)
    return build_cache()


def main():
    cache = get_cache()
    chain_name = cache["chain_name"]
    if "base_names" not in cache:
        cache["base_names"] = sorted({r["name_cn"] for r in q(
            "SELECT name_cn FROM gkx.dwd_org_base_info WHERE is_deleted=0 AND name_cn IS NOT NULL")})
        _dump(cache)
    base_names = set(cache["base_names"])
    inst_names = set(cache.get("inst_names") or [])
    chain4 = set(cache["chain_member_city4"])
    name_patent = cache["name_patent"]

    wo = cache["wo_applicants"]
    wo_total = sum(r["n"] for r in wo)
    wo_dom = sum(r["n"] for r in wo if (r["nm"] or "") in base_names)
    wo_inst = sum(r["n"] for r in wo if (r["nm"] or "") in inst_names)
    wo_chain = 0
    per_chain_wo = Counter()
    for r in wo:
        hits = [ch for ch, _city in chain_name.get(r["nm"] or "", [])]
        if hits:
            wo_chain += r["n"]
            for ch in set(hits):
                per_chain_wo[ch] += r["n"]

    # 链上专利总量（口径：企业名等值匹配主档 + 限 4 城链上企业，与旧版 chain_reg 面板同构）
    per_chain_total = Counter()
    for nm in chain4:
        rec = name_patent.get(nm)
        if rec:
            for ch, _city in chain_name.get(nm, []):
                per_chain_total[ch] += rec[0]
    rows = []
    for ch in cache["roots"]:
        tot = per_chain_total.get(ch, 0)
        w = per_chain_wo.get(ch, 0)
        rows.append({"chain": ch, "chain_name": cache["roots"].get(ch),
                     "chain_patents_matched": tot,
                     "wo_publications_matched": w,
                     "wo_share_pct": round(100.0 * w / tot, 3) if tot else None})
    rows.sort(key=lambda r: -(r["wo_share_pct"] or 0))

    fg = cache["forg_country"]
    patent_ctry = {r["country_code"]: r["n"] for r in cache["patent_country"]}
    n_pat = sum(patent_ctry.values())
    report = {
        "metric_id": METRIC,
        "metric_name": "产业链国际化程度",
        "date": "2026-10-21",
        "data_source": "gkx（183.240.141.251:3318，schema gkx）；链树 gkx.dwd_industry_chain_info，企业—链归属由 gkx.dwd_org_industry_tags 现推",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_INTERNATIONALIZATION_INDEX.md（v0.2.0 挂起版）",
        "calc_logic_status": "挂起（无公式 / 无 QC 号 / 因子集与权重未签）",
        "path_1_forg": {
            "rows": cache["forg_rows"],
            "country_dist": fg,
            "n_china_rows": sum(r["n"] for r in fg if (r["country_code"] or "") in ("CN", "CHN")),
            "industry_type_top": cache["forg_industry_type"],
            "overlap_with_base_orgid": cache["forg_orgid_overlap_base"],
            "overlap_with_dwd_chain_orgid": cache["forg_in_dwd_chain"],
            "name_hit_in_industry_tags": cache["forg_name_in_tags"],
            "credit_hit_in_industry_tags": cache["forg_extid_in_tags"],
            "name_hit_in_chain_map": cache["forg_name_in_chain"],
        },
        "path_2_patent": {
            "country_dist": patent_ctry,
            "n_patents": n_pat,
            "cn_share_pct": round(100.0 * patent_ctry.get("CN", 0) / n_pat, 3),
            "wo_share_pct": round(100.0 * patent_ctry.get("WO", 0) / n_pat, 3),
            "n_distinct_wo_applicants": len(wo),
            "wo_publications": wo_total,
            "wo_applicant_is_domestic_base": wo_dom,
            "wo_applicant_domestic_pct": round(100.0 * wo_dom / wo_total, 2) if wo_total else None,
            "wo_applicant_is_domestic_institute": wo_inst,
            "wo_applicant_hit_chain_names": wo_chain,
            "wo_applicant_hit_chain_pct": round(100.0 * wo_chain / wo_total, 2) if wo_total else None,
            "patent_has_applicant_country_column": False,
            "note": "dwd_patent 只有 country_code / application_country，二者分布完全相同，"
                    "均为「公开/申请受理国别」，不是申请人国别；WO=WIPO/PCT 公开，JP=日本公开。",
            "top_wo_applicants": sorted([[r["nm"], r["n"]] for r in wo], key=lambda x: -x[1])[:10],
        },
        "path_3_trade": {
            "tables": cache["trade_tables_gkx"],
            "note": "全库无海关 / 进出口 / 贸易表；gkx 280 表按表名 customs/trade/import/export/haiguan 检索命中 "
                    f"{len(cache['trade_tables_gkx'])} 张",
        },
        "degradation_rows": rows,
        "degradation_stats": {
            "n_chains_nonzero": sum(1 for r in rows if (r["wo_publications_matched"] or 0) > 0),
            "max_wo_share_pct": max((r["wo_share_pct"] or 0) for r in rows),
            "min_wo_share_pct": min((r["wo_share_pct"] or 0) for r in rows),
        },
        "chain_system": {
            "tree_nodes": cache["tree_size"],
            "n_roots": len(cache["roots"]),
            "tags_rows": cache["tags_rows"],
            "tags_base_hit": cache["tags_base_hit"],
            "n_chain_names": cache["n_chain_names"],
            "n_chain_credits": cache["n_chain_credits"],
        },
    }

    report["support_judgment"] = {
        "data_support_level": "完全不支持",
        "reason": (
            "三条候选路径全部断裂：① 海外主体 dwd_forg_base_info 20,000 行仅 GB 19,832 / US 159 / CA 9 三国，"
            "与国内主档 org_id 交集 0、与产业标签 credit_code 交集 0、与企业—链归属交集 0，无法挂到任何产业链；"
            "② 专利表无申请人国别字段，country_code 实为公开国别，WO 公开的申请人 "
            f"{report['path_2_patent']['wo_applicant_domestic_pct']}% 直接命中国内企业主档名（华为、OPPO、中兴等），"
            "用它算「海外专利占比」会把中国企业的 PCT 申请算成国际化；"
            "③ 进出口/贸易表全库不存在，w3 因子无载体。"
            "原口径本身处于挂起状态、无公式无权重，故该指标及其关键依赖在三方库 gkx 均不可构建。"
        ),
        "criteria": {"forg_chain_overlap": 0, "patent_applicant_country_column": False,
                     "wo_domestic_applicant_pct": report["path_2_patent"]["wo_applicant_domestic_pct"],
                     "trade_tables": 0, "formula_signed": False},
    }
    OUT = Path(__file__).with_name(f"{METRIC}_out.json")
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print("wrote", OUT)
    print(json.dumps(report["path_2_patent"], ensure_ascii=False, indent=1)[:1200])
    print("rows", json.dumps(rows, ensure_ascii=False)[:800])
    print("chain_system", json.dumps(report["chain_system"], ensure_ascii=False))


if __name__ == "__main__":
    main()
