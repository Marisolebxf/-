#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20261021 版 · 城市对标同族 5 指标共用的「城市口径」层（只读 gkx，禁引 demo）。

本批 5 件（M_INNOV_CARRIER_VALUE_RANK_SZ / M_INNOV_CITY_BENCHMARK_GLOBAL /
M_INNOV_CITY_COMPARE_SZ / M_INNOV_CITY_COMPETE_SZ / M_INNOV_CITY_FACTOR_GLOBAL）
共用同一套城市口径，避免「同一城市在不同文档里排名矛盾」。三条共同约定：

1. 城市名归一 norm_city()
   - 占位符：'NULL' / 'null' / '' / 'NONE' / '-' / 'NAN' 一律归空串（= 无城市归属）；
   - 后缀：去掉末尾「市」（深圳/深圳市 同键）；
   - 区县：南山区/福田区…按 DISTRICT_TO_CITY 上卷到地级市（防止 area/district 列被误当 city）；
   - 实测：dwd_org_base_info.city 只有 66 个取值、全部为「X市」、无 'NULL' 字面量、无区县级值；
     占位符只出现在 dwd_policy_base.city（'NULL' 9,706 行）与 dwd_org_base_info.area（区县列，本批不用）。
2. 标杆城市集合（谁进对比组）
   - 深圳锚定件（COMPARE / COMPETE / FACTOR）：深圳 + 广州 + 东莞——机构底册四市（深圳 95,600 /
     广州 49,605 / 东莞 33,590 / 惠州 9,979）之外的省外样本仅 340 家（0.18%），北京 163、上海 16，
     跨省对比会把「库覆盖差」读成「创新差距」，故对标组限可信区三城；
   - 全球对标件（BENCHMARK）：深圳 + 北京 + 上海 + 广州——有意保留两个覆盖薄弱城作反例，
     并在结果里逐条披露「京沪低值是覆盖问题」；它与深圳锚定件的分工是「带反例的全球视图 vs 可信区对比」。
3. 基准形态：五件一律用总量基准（专利件数、机构家数、研发经费合计、政策件数），
   不用人均/地均——库内无城市 GDP、常住人口、R&D 人员全时当量，人均基准无法构造。

本模块只做取数与归一，不做指标合成；合成公式留在各指标脚本里，便于逐件复核。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _gkxdb  # noqa: E402

CACHE = Path(__file__).parent / "_snapshots21"
CACHE.mkdir(exist_ok=True)

# 可信区四市（机构底册均有万级样本）
TRUST_CITIES = ["深圳", "广州", "东莞", "惠州"]
# 深圳锚定件的对标组
SZ_BENCH = ["深圳", "广州", "东莞"]
# 全球对标件演示选城（含两个覆盖薄弱城，故意暴露覆盖差）
GLOBAL_CITIES = ["深圳", "北京", "上海", "广州"]

PLACEHOLDER = {"NULL", "NONE", "NAN", "N/A", "-", "", "无", "未知"}

DISTRICT_TO_CITY = {
    "南山": "深圳", "福田": "深圳", "宝安": "深圳", "龙岗": "深圳", "罗湖": "深圳",
    "龙华": "深圳", "坪山": "深圳", "光明": "深圳", "盐田": "深圳", "大鹏": "深圳",
    "天河": "广州", "越秀": "广州", "海珠": "广州", "荔湾": "广州", "白云": "广州",
    "黄埔": "广州", "番禺": "广州", "花都": "广州", "南沙": "广州", "增城": "广州",
    "从化": "广州",
    "松山湖": "东莞", "虎门": "东莞", "长安": "东莞", "厚街": "东莞",
    "惠城": "惠州", "惠阳": "惠州", "博罗": "惠州", "惠东": "惠州", "龙门": "惠州",
    "海淀": "北京", "朝阳": "北京", "东城": "北京", "西城": "北京", "丰台": "北京",
    "石景山": "北京", "通州": "北京", "昌平": "北京", "大兴": "北京", "顺义": "北京",
    "浦东": "上海", "黄浦": "上海", "徐汇": "上海", "长宁": "上海", "静安": "上海",
    "普陀": "上海", "虹口": "上海", "杨浦": "上海", "闵行": "上海", "宝山": "上海",
    "嘉定": "上海", "松江": "上海", "青浦": "上海", "奉贤": "上海",
}


def norm_city(v) -> str:
    """城市名归一：占位符归空串、去「市」后缀、区县上卷到地级市。"""
    if v is None:
        return ""
    s = str(v).strip()
    if s.upper() in PLACEHOLDER:
        return ""
    if s.endswith("市"):
        s = s[:-1]
    if s in DISTRICT_TO_CITY:
        return DISTRICT_TO_CITY[s]
    for k, c in DISTRICT_TO_CITY.items():
        if s.startswith(k):
            return c
    return s


def looks_like_placeholder(v) -> bool:
    return v is None or str(v).strip().upper() in PLACEHOLDER


# ---------------------------------------------------------------- 取数（只读 gkx）

def _q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        return cur.fetchall()
    finally:
        cur.close()


INVENTORY = Path(__file__).parent.parent / "_work_gkx21" / "GKX_INVENTORY.json"


def inventory_rows(table):
    """行数只读库存 json（GKX_INVENTORY.json，实测 COUNT(*) 落盘），不重复摸大表。"""
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    rec = inv.get(table)
    return int(rec["rows"]) if rec else None


def _cache(name, fn):
    p = CACHE / name
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    obj = fn()
    p.write_text(json.dumps(obj, ensure_ascii=False, default=str), encoding="utf-8")
    return obj


def org_rows():
    """机构底册：[org_id, name_cn, city, reg_status]（企业 + 科研机构）。

    189,116 + 2,074 行；实测 reg_status 的存续态写作「存续（在营、开业、在册）」，
    LIKE '%存续%' 仍可命中 168,830 行——换源后这一点必须复核，否则入集会归零。
    """
    def build():
        rows = _q("SELECT org_id, name_cn, city, reg_status FROM gkx.dwd_org_base_info "
                  "WHERE is_deleted=0")
        rows2 = _q("SELECT org_id, name_cn, city, reg_status FROM gkx.dwd_research_institute_base_info "
                   "WHERE is_deleted=0")
        return [[oid, nm, norm_city(city), st] for oid, nm, city, st in list(rows) + list(rows2)]
    return _cache("cityfam_orgs_20261021.json", build)


def org_base_rows():
    """仅企业底册 `dwd_org_base_info`：[org_id, name_cn, city(归一), reg_status]。

    为何单列：20261020 旧脚本的城市口径全部只查企业底册（`city LIKE '%X%'`），
    科研机构底册只用于「载体入集」。若把两张表混进城市名集合，学者/论文的
    城内命中会虚增（实测深圳学者 212 vs 旧 168），故按用途拆开。
    """
    def build():
        return [[oid, nm, norm_city(city), st] for oid, nm, city, st in
                _q("SELECT org_id, name_cn, city, reg_status FROM gkx.dwd_org_base_info "
                   "WHERE is_deleted=0")]
    return _cache("cityfam_orgbase_20261021.json", build)


def org_index():
    """org_id -> [org_id, name, city, status]"""
    return {r[0]: r for r in org_rows()}


def city_name_sets(cities=None, base_only=False):
    """城市 -> 机构名集合（用于专利申请人/论文单位/学者单位的名对齐）。

    base_only=True 复刻 20261020 旧脚本口径（只取企业底册）；False 为底册并集。
    """
    cities = cities or (TRUST_CITIES + ["北京", "上海"])
    out = {c: set() for c in cities}
    for _oid, nm, c, _st in (org_base_rows() if base_only else org_rows()):
        if c in out and nm:
            out[c].add(nm)
    return out


def surviving_org_count(cities=None):
    """城内存续机构家数（COUNT(DISTINCT org_id)，reg_status LIKE '%存续%'，仅企业底册）。"""
    out = {c: 0 for c in (cities or GLOBAL_CITIES)}
    seen = set()
    for oid, _nm, c, st in org_base_rows():
        if c not in out:
            continue
        if st and "存续" in str(st) and oid not in seen:
            seen.add(oid)
            out[c] += 1
    return out


def name_to_city(cities=None, priority=None):
    """机构名 -> 城市（同名跨城时按 priority 优先，默认深圳优先，与旧脚本循环顺序一致）。"""
    cities = cities or (TRUST_CITIES + ["北京", "上海"])
    priority = priority or cities
    sets = city_name_sets(cities)
    m = {}
    for c in priority:
        for nm in sets.get(c, ()):
            m.setdefault(nm, c)
    return m


def scholar_rows():
    """[scholar_id, scholar_org_name_zh]（21,316 行）。"""
    def build():
        return [[sid, org or ""] for sid, org in
                _q("SELECT scholar_id, scholar_org_name_zh FROM gkx.dwd_scholar WHERE is_deleted=0")]
    return _cache("cityfam_scholars_20261021.json", build)


def policy_rows():
    """[id, city(归一), province, status]（20,000 行，全表存量、不按发布年截断）。"""
    def build():
        return [[pid, norm_city(city), (prov or "").strip(), st] for pid, city, prov, st in
                _q("SELECT id, city, province, status FROM gkx.dwd_policy_base")]
    return _cache("cityfam_policy_20261021.json", build)


def hightech_org_ids():
    """挂「高新技术」标签的 org_id 集合（202,424 行标签表，单列去重）。

    旧口径 org_tag LIKE '%高新技术%' 会同时命中「高新技术企业」「国家级高新技术企业」
    「曾获国家级高新技术企业」三类标签；本批沿用，避免改口径导致读数漂移。
    """
    def build():
        return sorted({r[0] for r in
                       _q("SELECT DISTINCT org_id FROM gkx.dwd_org_tech_tag "
                          "WHERE is_deleted=0 AND org_tag LIKE '%高新技术%'")})
    return _cache("cityfam_hightech_20261021.json", build)


def stock_rows(y0=2019, y1=2026):
    """[org_id, occur_period, research_development_amount]（上市财报，窗内）。"""
    def build():
        return [[oid, per, amt] for oid, per, amt in
                _q("SELECT org_id, occur_period, research_development_amount "
                   "FROM gkx.dwd_org_stock_finance_info "
                   "WHERE LEFT(occur_period,4) BETWEEN %s AND %s AND is_deleted=0", (str(y0), str(y1)))]
    return _cache(f"cityfam_stock_{y0}_{y1}_20261021.json", build)


def paper_institution_stats(year=2024):
    """论文 -> 机构名（指定覆盖年）：{机构名: {"papers", "download", "cited"}}。

    两步取数再本地联接，避免 10 万×6 万的大 JOIN：
    ① `dwd_zh_paper` 按 cover_year_start（有索引）取当年论文 id + download_num；
    ② `dwd_zh_author` 按 paper_id 游标扫，命中当年 id 的机构累计；
    ③ `dwd_zh_paper_citation`（20,031 行）按 id 预载 citation_num。
    """
    def build():
        down = {}
        for pid, dl in _q("SELECT id, download_num FROM gkx.dwd_zh_paper "
                          "WHERE cover_year_start=%s AND is_deleted=0", (str(year),)):
            down[pid] = float(dl or 0)
        cited = {pid: float(n or 0) for pid, n in
                 _q("SELECT id, citation_num FROM gkx.dwd_zh_paper_citation WHERE is_deleted=0")}
        out = {}
        cur = _gkxdb.gkx()
        try:
            cur.execute("SELECT paper_id, institution FROM gkx.dwd_zh_author WHERE is_deleted=0")
            while True:
                batch = cur.fetchmany(20000)
                if not batch:
                    break
                for pid, inst in batch:
                    if pid in down and inst:
                        d = out.setdefault(inst, {"papers": set(), "download": 0.0, "cited": 0.0})
                        if pid not in d["papers"]:
                            d["papers"].add(pid)
                            d["download"] += down[pid]
                            d["cited"] += cited.get(pid, 0.0)
        finally:
            cur.close()
        return {k: {"papers": len(v["papers"]), "download": v["download"], "cited": v["cited"]}
                for k, v in out.items()}
    return _cache(f"cityfam_paper_{year}_20261021.json", build)


def dev_employee_probe():
    """研发人员列实测：(总行数, 非空行数, SUM)。gkx 实测 (90,926, 0, None) → 人才维不能兜底。"""
    def build():
        rows = _q("SELECT COUNT(*), SUM(development_employee IS NOT NULL), "
                  "SUM(development_employee) FROM gkx.dwd_org_annual_financial_info")
        n, nn, s = rows[0]
        return {"rows": int(n), "nonnull": int(nn or 0), "sum": (float(s) if s is not None else None)}
    return _cache("cityfam_dev_employee_20261021.json", build)


def transfer_2024():
    """2024 年生效的专利权属变更：[pn, transfer_before, transfer_after]（7,711 行）。"""
    def build():
        return [[pn, tb, ta] for pn, tb, ta in
                _q("SELECT pn, transfer_before, transfer_after FROM gkx.dwd_patent_transfer "
                   "WHERE transfer_effective_date BETWEEN '20240101' AND '20241231'")]
    return _cache("cityfam_transfer_2024_20261021.json", build)


def patent_scan():
    """专利底表一次性扫描缓存（见 _patent_scan_20261021.py）。"""
    import pickle
    p = CACHE / "patent_scan_20261021.pkl"
    if not p.exists():
        raise SystemExit("缺专利扫描缓存，请先运行 code/_patent_scan_20261021.py")
    st = pickle.loads(p.read_bytes())
    if not st.get("done"):
        raise SystemExit("专利扫描未完成（请等 _patent_scan_20261021.py 跑完）")
    return st


# ---------------------------------------------------------------- 共用聚合

def patents_2024_by_name():
    """2024 年申请人 → 去重 pn 件数（共享缓存 `patent2024_scan_20261021.json`，83 块全量合并）。

    来源：`_carrier21_common.patent_scan()`（`WHERE apdt_year=2024`，按 `dwd_id` 50 万/块扫，
    `COUNT(DISTINCT pn)` 按申请人名去重）。实测按城内机构名合计得 深圳 275,908 / 广州 140,395 /
    北京 132 / 上海 1，与 20261020 旧脚本 `JOIN ... COUNT(DISTINCT p.pn)` 逐位相同——
    说明 2024 年同城共同申请人重复量 < 0.2%，两口径可互换。
    """
    p = CACHE / "patent2024_scan_20261021.json"
    if not p.exists():
        raise SystemExit("缺 2024 申请人缓存 patent2024_scan_20261021.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    return {k: v[0] for k, v in d["by_name"].items()}


def patents_2024_by_city(cities=None):
    """城市 → 2024 去重专利件数（城内机构名合计，与旧脚本同口径）。"""
    sets = city_name_sets(cities, base_only=True)
    by = patents_2024_by_name()
    return {c: sum(by[n] for n in names if n in by) for c, names in sets.items()}


def patents_by_city_year(scan=None):
    """(city, year) -> 去重专利件数（COUNT(DISTINCT pn)，与旧脚本同口径）。"""
    scan = scan or patent_scan()
    return {k: len(v) for k, v in scan["city_year_pn"].items()}


def policies_by_city(cities=None, share_province=True):
    """城市 -> 有效政策件数（市级命中 + 省级共享）。

    口径与 20261020 旧脚本一致：status='有效'（gkx 全表单值）+ 城市直计；
    省级共享 = 城市无归属（含字面量 'NULL'）且 province 含「广东」的政策，均摊给粤城。
    旧脚本用 city IS NULL，在 gkx 上会因 'NULL' 是字符串而恒得 0——本模块改为
    looks_like_placeholder(city)，这是换源后必须修的一处。
    """
    cities = cities or SZ_BENCH
    city_cnt = {c: 0 for c in cities}
    prov = 0
    for _pid, c, province, st in policy_rows():
        if st != "有效":
            continue
        if c in city_cnt:
            city_cnt[c] += 1
        elif not c and "广东" in province:
            prov += 1
    shared = prov if share_province else 0
    return {c: {"city": city_cnt[c], "prov_shared": shared,
                "total": city_cnt[c] + shared} for c in cities}, prov


def hightech_by_city(cities=None, surviving=False):
    """城内存续高企家数。surviving=True 复刻 BENCHMARK 旧口径（reg_status LIKE '%存续%'）。"""
    idx = org_index()
    tag = set(hightech_org_ids())
    out = {c: 0 for c in (cities or SZ_BENCH)}
    for oid in tag:
        r = idx.get(oid)
        if not r or r[2] not in out:
            continue
        if surviving and not (r[3] and "存续" in str(r[3])):
            continue
        out[r[2]] += 1
    return out


def scholars_by_city_names(cities=None):
    """学者数（机构名精确 IN 城内机构名集合，FACTOR 旧口径：逐城计数、不互斥）。"""
    sets = city_name_sets(cities, base_only=True)
    hits = {c: set() for c in sets}
    for sid, org in scholar_rows():
        if not org:
            continue
        for c, names in sets.items():
            if org in names:
                hits[c].add(sid)
    return {c: len(v) for c, v in hits.items()}


def scholars_by_city_like(cities=None):
    """学者数（机构名 LIKE '%城市%'，COMPARE 旧口径）。"""
    cities = cities or SZ_BENCH
    out = {c: set() for c in cities}
    for sid, org in scholar_rows():
        if not org:
            continue
        for c in cities:
            if c in org:
                out[c].add(sid)
                break
    return {c: len(v) for c, v in out.items()}


def papers_by_city(cities=None, year=2024, base_only=True):
    """论文去重件数（作者单位精确等于城内机构名，与 COMPARE/BENCHMARK 旧 JOIN 同口径）。"""
    sets = city_name_sets(cities, base_only=base_only)
    inst = paper_institution_stats(year)
    out = {c: 0 for c in sets}
    for name, d in inst.items():
        for c, names in sets.items():
            if name in names:
                out[c] += d["papers"]
                break
    return out


def paper_sums_by_name(names, year=2024):
    """按机构名返回 (论文影响分合计, 下载合计, 被引合计)。impact_score 全表 NULL → 恒 0。"""
    inst = paper_institution_stats(year)
    dl = sum(inst[n]["download"] for n in names if n in inst)
    cited = sum(inst[n]["cited"] for n in names if n in inst)
    return 0.0, dl, cited


def rd_by_city(cities=None, y0=2019, y1=2024):
    """上市研发经费合计（occur_period 前 4 位落在窗内）。"""
    idx = org_index()
    out = {c: 0.0 for c in (cities or SZ_BENCH)}
    for oid, per, amt in stock_rows(y0, 2026):
        if amt is None:
            continue
        if not (y0 <= int(str(per)[:4]) <= y1):
            continue
        r = idx.get(oid)
        if r and r[2] in out:
            out[r[2]] += float(amt)
    return out


if __name__ == "__main__":
    print("norm_city:", [norm_city(x) for x in
                         ["深圳市", "深圳", "南山区", "NULL", "null", "", "东莞市", "浦东新区"]])
    print("orgs:", len(org_rows()))
    print("scholars:", len(scholar_rows()))
    print("policy:", len(policy_rows()))
    print("hightech orgs:", len(hightech_org_ids()))
    print("policies:", policies_by_city(SZ_BENCH))
    print("papers2024:", papers_by_city(GLOBAL_CITIES))
    print("rd 2019-2024:", rd_by_city(SZ_BENCH))
