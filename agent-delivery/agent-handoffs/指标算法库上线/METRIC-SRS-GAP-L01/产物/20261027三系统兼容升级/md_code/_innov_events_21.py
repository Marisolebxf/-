#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20261021 · 科创事件簇共用算路（EVENTS_001 关注度 / EVENTS_002 影响力）。

只读三方库 gkx，禁引 demo / _devdb。

关键口径（对齐 20261020 版，不重写公式）
----------------------------------------
* 事件单元 = `gkx.dwd_policy_base` 的一行（`id` 唯一，实测 20,000 行 / 20,000 个 id）。
* 正文规模 = max(LENGTH(content), LENGTH(abstract))；两列都做占位符清洗——
  gkx 把「无值」写成字面量 `'NULL'`（content 797 行、abstract 7,841 行），
  若不清洗会把 4 个字符的 `'NULL'` 当成正文，凭空抬高覆盖率（DATA_FACTS §3.4）。
* 主题/引用：`UPPER(TRIM(col)) NOT IN ('NULL','','NONE','-')`，实测各只有 2 条有效。
* `rank` 是 JSON 数组字符串，按「国家级4/省级3/市级2/区县级1/园区级1/其他0」取 max。

事件去重审计（本簇专项风险）
----------------------------
`dwd_policy_base` 以 `id` 为主键，但存在同题多行：19,945 个不同 title 对应 20,000 行
（53 组、55 行重复题名）。其中含「公示」「公告」这类通用题名，按 title 去重会把不同
事件错并；因此本版仍以 `id` 为事件单元，同时输出 `dedup_audit` 披露：
  - title 去重后事件数；
  - 「title + publish_date + province + city」严格键下的重复组与多余行。
"""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

import _gkx21_common as C

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_snapshots21" / "policy_base_20261021.json"

PLACEHOLDER = ("NULL", "", "NONE", "-")
LEVEL_RX = re.compile(r"国家级|省级|市级|区县级|区级|园区级")
LEVEL_MAP = {"国家级": 4, "省级": 3, "市级": 2, "区县级": 1, "区级": 1, "园区级": 1}


def _n(v):
    return int(v) if v is not None else 0


def load_policy(force=False):
    """20,000 行政策事件，带占位符清洗后的正文长度与维度标记。"""
    if CACHE.exists() and not force:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    rows = C.qd("""
        SELECT id, title, publish_date, province, city, district, ministry,
               LENGTH(NULLIF(UPPER(TRIM(content)),'NULL'))  clen,
               LENGTH(NULLIF(UPPER(TRIM(abstract)),'NULL')) alen,
               CASE WHEN UPPER(TRIM(theme))        IN ('NULL','','NONE','-') THEN 0 ELSE 1 END th,
               CASE WHEN UPPER(TRIM(quote_policy)) IN ('NULL','','NONE','-') THEN 0 ELSE 1 END qp,
               CASE WHEN UPPER(TRIM(province))     IN ('NULL','','NONE','-') THEN 0 ELSE 1 END pv,
               CASE WHEN UPPER(TRIM(city))         IN ('NULL','','NONE','-') THEN 0 ELSE 1 END ct,
               CASE WHEN UPPER(TRIM(district))     IN ('NULL','','NONE','-') THEN 0 ELSE 1 END dt,
               `rank`
        FROM gkx.dwd_policy_base
    """)
    out = []
    for r in rows:
        body = max(_n(r["clen"]), _n(r["alen"]))
        lv = max([LEVEL_MAP.get(k, 0) for k in LEVEL_RX.findall(r["rank"] or "")] or [0])
        out.append({"id": r["id"], "title": r["title"], "date": r["publish_date"],
                    "province": r["province"], "city": r["city"], "district": r["district"],
                    "ministry": r["ministry"], "body_len": body,
                    "theme": int(r["th"]), "quote": int(r["qp"]),
                    "geo": int(r["pv"]) + int(r["ct"]) + int(r["dt"]),
                    "level": lv})
    CACHE.write_text(json.dumps(out, ensure_ascii=False, default=str), encoding="utf-8")
    return out


def norm(v):
    lo, hi = min(v), max(v)
    return [0.5] * len(v) if hi == lo else [(x - lo) / (hi - lo) for x in v]


def body_stats(rows):
    b = [r["body_len"] for r in rows]
    return {"min": min(b), "max": max(b), "avg": round(sum(b) / len(b), 1),
            "n_zero": sum(1 for x in b if x == 0)}


def dedup_audit(rows):
    """事件去重审计：title 级与严格键级。"""
    titles = {}
    strict = {}
    for r in rows:
        titles[r["title"]] = titles.get(r["title"], 0) + 1
        k = (r["title"], str(r["date"] or ""), str(r["province"] or ""), str(r["city"] or ""))
        strict[k] = strict.get(k, 0) + 1
    tg = {k: v for k, v in titles.items() if v > 1}
    sg = {k: v for k, v in strict.items() if v > 1}
    return {
        "event_unit": "gkx.dwd_policy_base.id（1 行 = 1 份政策文件）",
        "n_rows": len(rows),
        "n_distinct_id": len({r["id"] for r in rows}),
        "n_distinct_title": len(titles),
        "title_dup_groups": len(tg),
        "title_dup_extra_rows": sum(tg.values()) - len(tg),
        "strict_key": "title+publish_date+province+city",
        "strict_dup_groups": len(sg),
        "strict_dup_extra_rows": sum(sg.values()) - len(sg),
        "decision": ("保留 id 粒度，不按 title 去重：重复题名中含「公示」「公告」等通用题名，"
                     "按 title 去重会错并不同事件；严格键重复仅按 id 计数，占比见上。"),
    }


def score_attention(rows):
    nb = norm([r["body_len"] for r in rows])
    nt = norm([r["theme"] for r in rows])
    nq = norm([r["quote"] for r in rows])
    scored = []
    for i, r in enumerate(rows):
        s = round(100 * (nb[i] + nt[i] + nq[i]) / 3, 1)
        scored.append({"policy_id": r["id"], "body_len": r["body_len"],
                       "theme_n": r["theme"], "quote_n": r["quote"], "attention_score": s})
    scored.sort(key=lambda x: (-x["attention_score"], -x["body_len"], str(x["policy_id"])))
    return scored


def score_influence(rows):
    nl = norm([r["level"] for r in rows])
    ng = norm([r["geo"] for r in rows])
    nt = norm([r["theme"] for r in rows])
    scored = []
    for i, r in enumerate(rows):
        s = round(100 * (nl[i] + ng[i] + nt[i]) / 3, 1)
        scored.append({"policy_id": r["id"], "level": r["level"], "geo_cov": r["geo"],
                       "theme_n": r["theme"], "influence_score": s})
    scored.sort(key=lambda x: (-x["influence_score"], str(x["policy_id"])))
    return scored


def level_dist(rows):
    keys = ["国家级", "省级", "市级", "区县/园区", "其他0"]
    d = {k: 0 for k in keys}
    for r in rows:
        d[{4: "国家级", 3: "省级", 2: "市级", 1: "区县/园区", 0: "其他0"}[r["level"]]] += 1
    return d
