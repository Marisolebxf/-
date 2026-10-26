#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_SZ_REGION_COUNT 深圳区域数（区县覆盖数）—— 可运行复现脚本（2026-10-21 · gkx 改源版）

指标：产业链分析 / 产业链总览 / 深圳统计 · 深圳区域数
数据源：三方库 gkx（183.240.141.251:3318），经 `_gkxdb.gkx()` 只读连接，
        表：gkx.dwd_org_base_info / gkx.dwd_org_industry_tags。
口径（仿王惠）：COUNT(DISTINCT area) WHERE city='深圳市' AND 链上主体。
实测约束：
  - `dwd_org_base_info.area` 全表填充 82.28%，但**分城市极不均衡**：深圳 95,581/95,600、
    广州 49,603/49,605、惠州 9,920/9,979、**东莞 33,590 行全空**；
  - 深圳只有 9 个区县取值（缺大鹏新区/深汕合作区）；
  - 任何有规模的链都覆盖全部 9 个区 → 指标饱和、区分度≈0。

产出：code/M_CHAIN_SZ_REGION_COUNT_out.json
"""
from __future__ import annotations

import ast
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gkxdb import gkx  # noqa: E402
from _sz_chain import to_chain15  # noqa: E402

MID = "M_CHAIN_SZ_REGION_COUNT"
OUT = Path(__file__).parent / f"{MID}_out.json"
t0 = time.time()
res: dict = {"metric_id": MID, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
             "data_source": "gkx（三方库 gkx.dwd_org_base_info / dwd_org_industry_tags，只读）"}

_cur = gkx()


def parse_tags(raw: str) -> list[str]:
    """把 `["A","B"]` 形态的标签串解析成列表。

    库内实际存的是单引号形态（`['A','B']`），json.loads 会失败，故用 ast 兜底；
    两者都失败时按逗号切分并剥引号——宁可退化也不能让整件崩掉。
    """
    s = (raw or "").strip()
    if not s or s == "[]":
        return []
    for parser in (json.loads, ast.literal_eval):
        try:
            v = parser(s)
        except (ValueError, SyntaxError):
            continue
        if isinstance(v, (list, tuple)):
            return [str(x).strip() for x in v if str(x).strip()]
        if isinstance(v, str):
            return [v.strip()] if v.strip() else []
    return [x.strip().strip("'\"") for x in s.strip("[]").split(",") if x.strip().strip("'\"")]


def q(sql, args=None):
    if args:
        _cur.execute(sql, args)
    else:
        _cur.execute(sql)
    cols = [c[0] for c in _cur.description]
    return [dict(zip(cols, r)) for r in _cur.fetchall()]


def q1(sql, args=None):
    rows = q(sql, args)
    return rows[0] if rows else None


def step(name, fn):
    t = time.time()
    try:
        res[name] = fn()
    except Exception as e:  # noqa: BLE001
        res[name] = f"ERR {str(e)[:200]}"
    print(f"[{time.time()-t:6.1f}s] {name}: {str(res[name])[:280]}", flush=True)


# ------------------------------------------- 1 area 填充与取值域（单次扫描派生）
CITY_AREA = q("""
SELECT city, area, COUNT(*) n
FROM gkx.dwd_org_base_info
WHERE city IS NOT NULL AND city<>''
GROUP BY city, area""")

_agg: dict[str, dict] = {}
for r in CITY_AREA:
    c = r["city"]
    a = _agg.setdefault(c, {"city": c, "n": 0, "area_n": 0, "areas": set()})
    n = int(r["n"])
    a["n"] += n
    if r["area"] is not None and r["area"] != "":
        a["area_n"] += n
        a["areas"].add(r["area"])

area_fill = sorted(
    [{"city": a["city"], "n": a["n"], "area_n": a["area_n"], "areas": len(a["areas"]),
      "fill_pct": round(a["area_n"] / a["n"] * 100, 2) if a["n"] else 0.0}
     for a in _agg.values()],
    key=lambda x: -x["n"])[:8]
for r in area_fill:
    r["area_n"] = str(r["area_n"])
    r["fill_pct"] = f"{r['fill_pct']:.2f}"
res["area_fill_by_city"] = area_fill

res["sz_area_dist"] = sorted(
    [{"area": r["area"], "n": int(r["n"])} for r in CITY_AREA
     if r["city"] == "深圳市" and r["area"] not in (None, "")],
    key=lambda x: -x["n"])
res["sz_total"] = {"n": _agg.get("深圳市", {}).get("n", 0)}
res["sz_district_count"] = {"n": len(_agg.get("深圳市", {}).get("areas", ()))}
print(f"[  0.0s] area_fill_by_city: {res['area_fill_by_city'][:2]}", flush=True)


# ------------------------------------------------ 2 链切片（15 顶层链·代理）
def chain_slice():
    rows = q("""
SELECT t.company_name, t.industry_name, t.industry_link_name, t.industry_code, b.area
FROM gkx.dwd_org_industry_tags t
JOIN gkx.dwd_org_base_info b
  ON b.external_id = CONVERT(t.credit_code USING utf8mb4) COLLATE utf8mb4_0900_ai_ci
WHERE t.is_deleted=0 AND b.city='深圳市' AND b.area IS NOT NULL AND b.area<>''
""")
    chain_dist: dict[str, set] = {}
    chain_cos: dict[str, set] = {}
    for r in rows:
        ch = to_chain15(r["industry_name"], r["industry_link_name"])
        if ch is None:
            continue
        chain_dist.setdefault(ch, set()).add(r["area"])
        chain_cos.setdefault(ch, set()).add(r["company_name"])

    res["chain_coverage"] = {
        "tag_rows_with_area": len(rows),
        "chains_covered": len(chain_dist),
        "sz_companies_tagged": len({r["company_name"] for r in rows}),
    }
    res["chain_region_count"] = sorted([
        {"chain": ch, "districts": len(v), "district_list": sorted(v), "companies": len(chain_cos[ch])}
        for ch, v in chain_dist.items()
    ], key=lambda x: -x["companies"])

    # 原生行业码切片（真实码族）
    # 注意：industry_name / industry_link_name 都是「JSON 数组字符串」，不是标量码。
    # 同一个标签集合会以不同排列重复出现（['智能终端','软件与信息服务'] 与
    # ['软件与信息服务','智能终端'] 是同一组标签、两条不同字符串），直接以原串做
    # 字典键会把一个语义类别拆成两三个桶。所以这里先解析 → 排序去重 → 用规范键分组，
    # 同时保留「原串个数 / 规范键个数」作为拆分诊断（DATA_FACTS §3.32）。
    native: dict[tuple, dict] = {}
    raw_keys: set[str] = set()
    for r in rows:
        raw = r["industry_name"]
        if raw in (None, "", "[]"):
            continue
        raw_keys.add(raw)
        tags = sorted(set(parse_tags(raw)))
        if not tags:
            continue
        key = tuple(tags)
        d = native.setdefault(key, {"industry_tags": tags, "areas": set(), "cos": set()})
        d["areas"].add(r["area"])
        d["cos"].add(r["company_name"])
    res["native_code_region"] = sorted(
        [{"industry_tags": list(k), "industry_key": "|".join(k), "n_tags": len(k),
          "districts": len(v["areas"]), "cos": len(v["cos"])} for k, v in native.items()],
        key=lambda x: -x["cos"])[:20]
    res["native_tag_diag"] = {
        "rows_with_area": len(rows),
        "raw_tag_strings": len(raw_keys),
        "canonical_tag_sets": len(native),
        "split_by_order": len(raw_keys) - len(native),
        "note": "raw_tag_strings 为原串去重数，canonical_tag_sets 为「排序去重后的标签集合」数；"
                "两者之差即被数组排列顺序拆开的桶数",
    }
    return "ok"


step("chain_slice", chain_slice)


# ------------------------------------------------ 4 区分度：区县数的取值分布
def discrimination():
    rows = res.get("native_code_region") or []
    if not isinstance(rows, list) or not rows:
        return "ERR"
    vals = [int(r["districts"]) for r in rows]
    return {
        "n_codes": len(vals),
        "min": min(vals), "max": max(vals),
        "mode": max(set(vals), key=vals.count),
        "pct_at_max": round(sum(1 for v in vals if v == max(vals)) / len(vals) * 100, 2),
    }


step("discrimination", discrimination)

res["support_judgment"] = "部分支持"
res["support_reason"] = (
    "深圳侧 COUNT(DISTINCT area) 可现算（面积填充 95,581/95,600=99.98%，9 个区县取值）；"
    "但「指定产业链」这一限定在真实数据上无法闭合：15 条顶层链与 tags 的 INB13xx/15xx/25xx 码族无交叉表，"
    "tags 仅覆盖 19,909 家深圳企业（20.8%），且映射后仅落 8 条链；"
    "同时东莞 33,590 行 area 全空，跨市对比不可做；指标在规模链上饱和为 9 —— 故判部分支持。"
)
res["_elapsed_s"] = round(time.time() - t0, 1)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
print("wrote", OUT, f"{res['_elapsed_s']}s")
