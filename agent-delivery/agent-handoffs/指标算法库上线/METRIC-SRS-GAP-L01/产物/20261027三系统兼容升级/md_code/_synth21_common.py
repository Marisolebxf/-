#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SYNTH 五件（182/189/191/006/007）共享装载层 —— 只读 gkx 派生的本地缓存。

零专利 SQL：专利侧只读 `_snapshots21/` 已建成缓存
  patent_2024_by_name_20261021.json   2024 年申请人 → [pn 去重, 授权行数]
  patent_scan_20261021.pkl            city×year pn 集合 + 2024 申请人价值最大值
  patent_value_agg_gkx.json           全表 value 分布（P70=3,500 由 top3 占比复核）
  city_patent_year_gkx.json           城市×年份件数（重名 1/k 计权）
论文侧只读 `a25_paper_panel.json`（100,900 篇，含 author_info_list）与
`probe_a26_20261022.json`（被引 20,031 行）；机构/学者/年报侧读 `probe_synth21.json`
（本批 `_probe_synth21.py` 逐条限时落盘，7 条 ≤6 万行小表）。

口径约定（全批统一）：
  * 评价集 = 深圳、广州、东莞、惠州（gkx 底册 99.82% 落在这四市，DATA_FACTS §3.8）；
    北京、上海只出「论文维度参考读数」，不进综合指数（专利申请人不可归属，见 §三）。
  * 统计年 T=2024（完整年）；专利库真实年份 2021–2026，2017–2020 零行（§3.16）。
  * 任何跨年分母只除真实存在年份，输出 `base_years_used` / `base_years_missing`。
"""
from __future__ import annotations

import collections
import json
import math
import pickle
import re
import statistics
from pathlib import Path

HERE = Path(__file__).parent
SNAP = HERE / "_snapshots21"

CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
REF_CITIES = ["北京市", "上海市"]
CITY_ALIAS = {"深圳": "深圳市", "广州": "广州市", "东莞": "东莞市", "惠州": "惠州市",
              "北京": "北京市", "上海": "上海市"}
T_YEAR = 2024
PATENT_YEARS = (2021, 2022, 2023, 2024, 2025, 2026)
VALUE_P70 = 3500.0          # 全表 value 的 P70（top3 取值占 71.19%，见 patent_value_agg_gkx.json）

# 机构名 → 城市白名单：仅补「不含城市名」的常见主体；命中顺序在「城市名包含」之后。
INST_WHITELIST = {
    "中山大学": "广州市", "华南理工大学": "广州市", "暨南大学": "广州市",
    "华南师范大学": "广州市", "华南农业大学": "广州市", "广州大学": "广州市",
    "广东工业大学": "广州市", "南方医科大学": "广州市", "广州医科大学": "广州市",
    "深圳大学": "深圳市", "南方科技大学": "深圳市", "香港中文大学(深圳)": "深圳市",
    "清华大学": "北京市", "北京大学": "北京市", "中国人民大学": "北京市",
    "北京师范大学": "北京市", "北京航空航天大学": "北京市", "北京理工大学": "北京市",
    "中国农业大学": "北京市", "中国科学院": "北京市", "中国社会科学院": "北京市",
    "北京协和医学院": "北京市",
    "复旦大学": "上海市", "上海交通大学": "上海市", "同济大学": "上海市",
    "华东师范大学": "上海市", "华东理工大学": "上海市", "上海大学": "上海市",
}

_C: dict[str, object] = {}


def _load(name):
    p = SNAP / name
    if not p.exists():
        return None
    if name.endswith(".pkl"):
        with open(p, "rb") as f:
            return pickle.load(f)
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- 底册
def base():
    """name → [city...]（47 个重名）、org_id → city、city 总量。"""
    if "base" in _C:
        return _C["base"]
    rows = _load("star_base_rows_gkx.json") or []
    byname = collections.defaultdict(list)
    byid = {}
    city_tot = collections.Counter()
    for r in rows:
        oid, nm, _prov, city = (list(r) + [None] * 4)[:4]
        if nm:
            byname[nm].append(city)
        if oid:
            byid[oid] = city
        city_tot[city or ""] += 1
    _C["base"] = {"name": dict(byname), "id": byid, "city_tot": city_tot,
                  "n_rows": len(rows), "n_names": len(byname),
                  "n_dup": sum(1 for v in byname.values() if len(v) > 1)}
    return _C["base"]


def name_city_weights(nm: str) -> dict[str, float]:
    """机构名 → {city: 权重}；重名按 1/k 摊。查不到返回空。"""
    cand = base()["name"].get(nm)
    if not cand:
        return {}
    w = 1.0 / len(cand)
    out = collections.Counter()
    for c in cand:
        if c:
            out[c] += w
    return dict(out)


def inst_city(text: str) -> str | None:
    """机构串 → 城市：城市名包含优先，其次高校/院所白名单。"""
    s = str(text or "")
    if not s:
        return None
    for a, full in CITY_ALIAS.items():
        if a in s:
            return full
    for k, v in INST_WHITELIST.items():
        if k in s:
            return v
    return None


def papers() -> list[dict]:
    """100,900 篇中文论文：id / year / cites / insts / cities。"""
    if "papers" in _C:
        return _C["papers"]
    panel = _load("a25_paper_panel.json") or {}
    cit = {str(r[0]): int(r[1] or 0)
           for r in (_load("probe_a26_20261022.json")["zh_citation"]["rows"])}
    out = []
    for r in panel.get("paper", []):
        try:
            lst = json.loads(r.get("author_info_list") or "[]")
        except Exception:
            lst = []
        insts = set()
        if isinstance(lst, list):
            for a in lst:
                ins = (a.get("institution") or a.get("affiliation") or "").strip()
                if ins:
                    insts.add(ins)
        cities = {c for c in (inst_city(i) for i in insts) if c}
        try:
            y = int(str(r.get("y"))[:4])
        except Exception:
            y = None
        out.append({"id": str(r.get("id")), "year": y,
                    "cites": cit.get(str(r.get("id")), 0),
                    "journal": str(r.get("publication_zh_name") or "").strip(),
                    "insts": sorted(insts), "cities": cities})
    _C["papers"] = out
    _C["paper_meta"] = {"n": len(out), "n_with_inst": sum(1 for p in out if p["insts"]),
                        "n_with_city": sum(1 for p in out if p["cities"]),
                        "n_cited": sum(1 for p in out if p["cites"] > 0)}
    return out


def paper_meta():
    papers()
    return _C["paper_meta"]


def journal_impact() -> dict:
    """期刊 → 篇均被引（dwd_zh_journal 的 cite_nums / paper_nums）。"""
    if "jmap" in _C:
        return _C["jmap"]
    d = _load("zh_journal_stats_20261022.json") or {}
    m = {}
    for nm, cites, pn, _cyc in d.get("rows", []):
        try:
            cites, pn = float(cites or 0), float(pn or 0)
        except Exception:
            continue
        if nm and pn > 0:
            m[str(nm).strip()] = cites / pn
    vals = sorted(m.values())
    p90 = vals[int(len(vals) * 0.9)] if vals else 0.0
    _C["jmap"] = {"map": m, "p90": round(p90, 4), "n_journals": len(m),
                  "median": round(statistics.median(vals), 4) if vals else 0.0}
    return _C["jmap"]


# ---------------------------------------------------------------- 专利缓存
def patent2024() -> dict[str, list]:
    if "p2024" not in _C:
        _C["p2024"] = _load("patent_2024_by_name_20261021.json") or {}
    return _C["p2024"]


def value2024() -> dict[str, float]:
    if "v2024" not in _C:
        d = _load("patent_scan_20261021.pkl") or {}
        _C["v2024"] = d.get("value_2024", {})
    return _C["v2024"]


def city_year_pn() -> dict[tuple, int]:
    if "cy" not in _C:
        d = _load("patent_scan_20261021.pkl") or {}
        _C["cy"] = d.get("city_year_pn", {})
    return _C["cy"]


def grants2024_by_city() -> dict:
    """2024 年授权行数按第一申请人名归城（重名 1/k 摊），并统计未归属。"""
    if "g24" in _C:
        return _C["g24"]
    by_city = collections.Counter()
    unmapped = 0
    total = 0
    n_names = 0
    for nm, v in patent2024().items():
        try:
            gr = float(v[1] or 0)
        except Exception:
            gr = 0.0
        total += gr
        n_names += 1
        w = name_city_weights(nm)
        if not w:
            unmapped += gr
            continue
        for c, k in w.items():
            by_city[c] += gr * k
    _C["g24"] = {"by_city": dict(by_city), "total": total,
                 "unmapped": unmapped, "n_names": n_names}
    return _C["g24"]


def high_value2024_by_city(threshold: float = VALUE_P70) -> dict:
    """2024 年申请人价值最大值 ≥ 阈值的授权行数，按城市归并（P70 分位代理）。"""
    key = f"hv{threshold}"
    if key in _C:
        return _C[key]
    p24 = patent2024()
    v24 = value2024()
    by_city = collections.Counter()
    n_hv_names, n_hv_grants, unmapped = 0, 0.0, 0.0
    for nm, val in v24.items():
        try:
            val = float(val)
        except Exception:
            continue
        if val < threshold or nm not in p24:
            continue
        gr = float(p24[nm][1] or 0)
        n_hv_names += 1
        n_hv_grants += gr
        w = name_city_weights(nm)
        if not w:
            unmapped += gr
            continue
        for c, k in w.items():
            by_city[c] += gr * k
    _C[key] = {"by_city": dict(by_city), "n_hv_names": n_hv_names,
               "n_hv_grants": n_hv_grants, "unmapped": unmapped,
               "threshold": threshold, "value_universe": len(v24)}
    return _C[key]


def transfer2024_by_city() -> dict:
    """2024 年专利转移：转移前权利人按城市归并。"""
    if "tr24" in _C:
        return _C["tr24"]
    rows = _load("cityfam_transfer_2024_20261021.json") or []
    by_city = collections.Counter()
    unmapped = 0
    for r in rows:
        try:
            names = json.loads(r[1]) if isinstance(r[1], str) else (r[1] or [])
        except Exception:
            names = []
        for a in names if isinstance(names, list) else []:
            nm = (a.get("name") or "").strip() if isinstance(a, dict) else ""
            if not nm:
                continue
            c = inst_city(nm)
            if c:
                by_city[c] += 1
            else:
                w = name_city_weights(nm)
                if w:
                    for cc, k in w.items():
                        by_city[cc] += k
                else:
                    unmapped += 1
    _C["tr24"] = {"n_transfers": len(rows), "by_city": dict(by_city), "unmapped_names": unmapped}
    return _C["tr24"]


# ---------------------------------------------------------------- 小表探针
def probe() -> dict:
    if "probe" not in _C:
        _C["probe"] = _load("probe_synth21.json") or {}
    return _C["probe"]


def institutes() -> list[dict]:
    if "inst" not in _C:
        rows = probe().get("institute", {}).get("rows") or []
        _C["inst"] = [{"city": r[0], "name": r[1], "type": r[2]} for r in rows]
    return _C["inst"]


def macro_latest() -> dict:
    """{indicator: {city: {period, value}}}，各城取最新 12 月期末值。"""
    if "macro" in _C:
        return _C["macro"]
    code_map = {"gmjj_jjzl_01": "gdp", "gmjj_jjzl_01_02_01_01": "ind_va"}
    code_city = {"440300000000": "深圳市", "440100000000": "广州市",
                 "441900000000": "东莞市", "441300000000": "惠州市",
                 "110000000000": "北京市", "310000000000": "上海市"}
    out: dict[str, dict] = {"gdp": {}, "ind_va": {}}
    for r in probe().get("macro", {}).get("rows") or []:
        code, ic, period, val = r[0], r[1], int(r[2]), float(r[3] or 0)
        key = code_map.get(ic)
        city = code_city.get(code)
        if not key or not city:
            continue
        cur = out[key].get(city)
        if cur is None or period > cur["period"]:
            out[key][city] = {"period": period, "value": val}
    _C["macro"] = out
    return out


def annual_latest() -> dict:
    """org_id → {emp, rev, year}：取该企业最近一个有值的年报年。"""
    if "annual" in _C:
        return _C["annual"]
    rows = probe().get("annual2024", {}).get("rows") or []
    out = {}
    for oid, emp, rev in rows:
        rec = out.setdefault(oid, {"emp": None, "emp_year": None,
                                   "rev": None, "rev_year": None})
        # probe 只取 2024；保留字段结构以便未来扩窗
        if emp is not None:
            rec["emp"] = float(emp)
            rec["emp_year"] = 2024
        if rev is not None:
            rec["rev"] = float(rev)
            rec["rev_year"] = 2024
    _C["annual"] = out
    return out


def scholar_rows() -> list[dict]:
    if "sch" not in _C:
        rows = (_load("probe_a26_20261022.json")["scholar_dump"]["rows"])
        _C["sch"] = [{"id": r[0], "name": r[1], "org": (r[2] or "").strip(),
                      "papers": int(r[3] or 0), "cites": int(r[4] or 0),
                      "h": int(r[5] or 0)} for r in rows]
    return _C["sch"]


def scholar_edu_ids() -> set[str]:
    if "sedu" not in _C:
        _C["sedu"] = {str(r[0]) for r in (probe().get("scholar_edu", {}).get("rows") or [])}
    return _C["sedu"]


def tech_tag_orgs() -> list[str]:
    if "ht" not in _C:
        _C["ht"] = _load("cityfam_hightech_20261021.json") or []
    return _C["ht"]


# ---------------------------------------------------------------- 创新要素层（189 用）
def heis_universities() -> dict[str, str]:
    """全国普通高校名单 3,501 行 → {校名: 城市}（用于学者机构串归城）。"""
    if "heis" in _C:
        return _C["heis"]
    rows = (probe_talent().get("heis", {}) or {}).get("rows") or []
    m = {}
    for r in rows:
        nm, _prov, city = str(r[0]).strip(), str(r[1]).strip(), str(r[2]).strip()
        if nm and city:
            m[nm] = city
    _C["heis"] = m
    return m


def probe_talent() -> dict:
    if "pt" not in _C:
        _C["pt"] = _load("probe_talent21_20261022.json") or {}
    return _C["pt"]


def _heis_prefix() -> dict:
    if "heisp" in _C:
        return _C["heisp"]
    d = collections.defaultdict(list)
    for nm, city in heis_universities().items():
        if len(nm) >= 4:
            d[nm[:4]].append((nm, city))
    _C["heisp"] = dict(d)
    return _C["heisp"]


def org_city(text: str) -> str | None:
    """机构串 → 城市：城市名 → 白名单 → 高校名单（4 字前缀命中）。

    与 inst_city 的区别是接了全国高校名单，学者机构串的归城率从 16.1% 升到 97%+。
    """
    s = str(text or "")
    if not s:
        return None
    for a, full in CITY_ALIAS.items():
        if a in s:
            return full
    for k, v in INST_WHITELIST.items():
        if k in s:
            return v
    for nm, city in _heis_prefix().get(s[:4], ()):
        if nm in s:
            return city
    return None


def scholars() -> list[dict]:
    """21,316 位学者：id / name / org / city / papers / cites / h。"""
    if "sch_city" in _C:
        return _C["sch_city"]
    out = []
    for r in scholar_rows():
        out.append({**r, "city": org_city(r["org"])})
    _C["sch_city"] = out
    return out


def scholar_degrees() -> dict[str, str]:
    """scholar_id → 学位（博士/硕士/学士）。"""
    if "sdeg" in _C:
        return _C["sdeg"]
    rows = (probe_talent().get("edu", {}) or {}).get("rows") or []
    m = {}
    for r in rows:
        sid, _school, deg_zh = str(r[0]), str(r[1] or ""), str(r[2] or "")
        if not sid:
            continue
        cur = m.get(sid)
        rank = {"博士": 3, "硕士": 2, "学士": 1}
        lvl = 3 if "博士" in deg_zh else 2 if "硕士" in deg_zh else 1 if "学士" in deg_zh else 0
        if cur is None or rank.get(cur, 0) < lvl:
            m[sid] = "博士" if lvl == 3 else "硕士" if lvl == 2 else "学士" if lvl == 1 else "其他"
    _C["sdeg"] = m
    return m


def hightech_by_city() -> dict[str, int]:
    """国家级高新技术企业（27,936 个 org_id）→ 城市。"""
    if "htc" in _C:
        return _C["htc"]
    byid = base()["id"]
    c = collections.Counter()
    for oid in tech_tag_orgs():
        city = byid.get(oid)
        if city:
            c[city] += 1
    _C["htc"] = dict(c)
    return c


def tech_tags() -> dict[str, list]:
    if "tt" not in _C:
        _C["tt"] = _load("tech_tags_20261021.json") or {}
    return _C["tt"]


def tag_counts_by_city(tag_kw: str) -> dict[str, int]:
    """含指定关键词的资质标签（如「专精特新」）→ 城市企业数。"""
    byid = base()["id"]
    c = collections.Counter()
    for oid, tags in tech_tags().items():
        if any(tag_kw in str(t) for t in (tags or [])):
            city = byid.get(oid)
            if city:
                c[city] += 1
    return dict(c)


def ipc_name_rows() -> list:
    if "ipcn" not in _C:
        _C["ipcn"] = _load("patent_ipc4_by_name_20261021.json") or []
    return _C["ipcn"]


def ipc_breadth_by_city() -> dict:
    """每城覆盖的 IPC 小类数 + 集中度（1-HHI，按件数）。"""
    if "ipcb" in _C:
        return _C["ipcb"]
    cov = collections.defaultdict(set)
    cnt = collections.defaultdict(collections.Counter)
    for ipc4, nm, n in ipc_name_rows():
        w = name_city_weights(nm)
        for c, k in w.items():
            cov[c].add(ipc4)
            cnt[c][ipc4] += float(n or 0) * k
    out = {}
    for c, s in cov.items():
        tot = sum(cnt[c].values())
        hhi = sum((v / tot) ** 2 for v in cnt[c].values()) if tot else 0.0
        out[c] = {"ipc4": len(s), "hhi": round(hhi, 6),
                  "diversity": round(1 - hhi, 6), "patents": round(tot)}
    _C["ipcb"] = out
    return out


def rd_by_city() -> dict:
    """上市主体研发费用（亿元）：2024 年值 + 有值主体数。"""
    if "rd" in _C:
        return _C["rd"]
    d = _load("gba_rd_20261021.json") or {}
    out = {"by_city_2024_yi": {}, "orgs_by_city": d.get("orgs_by_city", {}),
           "source_rule": d.get("rule", ""), "anomaly": d.get("anomaly", {}),
           "by_city_year_yi": d.get("by_city_year_yi", {}),
           "orgs_total": d.get("orgs_total", 0)}
    for c, yrs in out["by_city_year_yi"].items():
        out["by_city_2024_yi"][c] = yrs.get("2024")
    _C["rd"] = out
    return out


# ---------------------------------------------------------------- 数值工具
def mm(vals: dict) -> dict:
    """批内极值归一 0–100；单点或全同 → None。"""
    vs = [v for v in vals.values() if v is not None]
    if len(vs) < 2 or max(vs) == min(vs):
        return {k: None for k in vals}
    lo, hi = min(vs), max(vs)
    return {k: (None if v is None else round((v - lo) / (hi - lo) * 100.0, 2))
            for k, v in vals.items()}


def wmean(xs):
    v = [x for x in xs if x is not None]
    return round(sum(v) / len(v), 2) if v else None


def pct(vals, q):
    s = sorted(vals)
    if not s:
        return None
    k = (len(s) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    return round(s[lo] + (s[hi] - s[lo]) * (k - lo), 4)


def st(vals) -> dict:
    v = [float(x) for x in vals if x is not None]
    if not v:
        return {"n": 0}
    return {"n": len(v), "min": round(min(v), 4), "max": round(max(v), 4),
            "mean": round(statistics.mean(v), 4), "median": round(statistics.median(v), 4),
            "p90": pct(v, 0.9)}


def base_year_block(used, missing, note) -> dict:
    return {"base_years_used": list(used), "base_years_missing": list(missing),
            "base_years_note": note}


def write_out(metric: str, payload: dict) -> Path:
    out = HERE / f"{metric}_out.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str),
                   encoding="utf-8")
    print("wrote", out.name, out.stat().st_size, "bytes")
    return out


if __name__ == "__main__":
    print("base", {k: v for k, v in base().items() if k in ("n_rows", "n_names", "n_dup")})
    print("papers", paper_meta())
    g = grants2024_by_city()
    print("grants2024", {k: round(v) for k, v in g["by_city"].items()}, "unmapped", round(g["unmapped"]))
    hv = high_value2024_by_city()
    print("hv2024", {k: round(v) for k, v in hv["by_city"].items()}, "names", hv["n_hv_names"])
    tr = transfer2024_by_city()
    print("transfer2024", tr["n_transfers"], {k: round(v) for k, v in tr["by_city"].items()})
    print("macro", json.dumps(macro_latest(), ensure_ascii=False))
    print("institute", collections.Counter(i["city"] for i in institutes()))
