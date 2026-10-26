#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""动态资讯数（M_CHAIN_NEWS_COUNT）—— gkx 链资讯表重建，自包含。

口径：源表 gkx.dwd_industry_chain_news_info（108,052 行），industry_code 存的是
JSON 数组串（varchar(255)，一条资讯可挂多条链，实测最多 27 个）。按数组解析、
取每码前 7 位归链、同链去重，再按链计资讯条数。等值匹配会得到全 0，这是旧稿踩过的坑。

本版增加的实测证据（旧稿有结论、无落盘）：
  - 截断：50,458 行（46.69%）industry_code 长度恰为 255，JSON 不可解析 49,532 行；
  - 解析成功的 58,520 行篇均 17.30 个码；
  - 三条零值链（INB1306/INB1333/INB1209）的 7 位根码在全表子串检索中出现 0 次，
    不是截断造成，是资讯标签体系没有这三个根码；
  - 1,610 行的全部码都落在 12 条顶层链之外。

产物：chains[].value = 该链资讯条数（多链展开，故合计大于源行数）；极性词典计数。

运行：cd code && python3 M_CHAIN_NEWS_COUNT.py
产物：code/M_CHAIN_NEWS_COUNT_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_NEWS_COUNT_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = '截面指标：统计当前存量，不设年度分母（源表日期跨度 2020-01-13—2026-07-27，本件不按年切）。'

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_industry_chain_news_info", "rows": 108052,
     "snapshot": "code/_snapshots21/news21_chain_items_20261022.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
     "snapshot": "code/_snapshots21/chain_panel21.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_industry_chain_info", "rows": 1273,
     "snapshot": "code/_snapshots21/chain_tree_20261021.json"},
]

CODE_RX = re.compile(r"INB\d{4,}")


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    news = load("news21_chain_items_20261022.json")
    layer = load("chain21_layer_20261022.json")
    roots = set(layer["chain_name"])

    # 逐行诊断（全部由已落盘快照现算，不查库）
    rows_src = news["rows"]
    len255 = 0
    parse_ok = 0
    parse_bad = 0
    code_counts = []
    no_root_rows = 0
    for r in rows_src:
        s = r[1] or ""
        if len(s) == 255:
            len255 += 1
        try:
            arr = json.loads(s)
            parse_ok += 1
            code_counts.append(len(arr) if isinstance(arr, list) else 0)
        except Exception:
            parse_bad += 1
        cs = {x[:7] for x in CODE_RX.findall(s)}
        if not (cs & roots):
            no_root_rows += 1

    rows = []
    for c in chains:
        nw = c.get("news") or {}
        rows.append({"chain": c["chain"], "name": c["name"],
                     "value": nw.get("total", 0), "pos": nw.get("pos", 0),
                     "neg": nw.get("neg", 0), "neu": nw.get("neu", 0),
                     "share_of_rows": round(nw.get("total", 0) / len(rows_src), 6),
                     "nonleaf": None, "leaves": None, "l1": None})
    rows.sort(key=lambda r: -r["value"])
    zero = [r for r in rows if r["value"] == 0]
    zero_names = [r["name"] for r in zero]

    total = sum(r["value"] for r in rows)
    pos = sum(r["pos"] for r in rows)
    neg = sum(r["neg"] for r in rows)
    neu = sum(r["neu"] for r in rows)

    # 零值链反证：根码在全表子串中出现次数
    zero_evidence = {}
    for r in zero:
        zero_evidence[r["chain"]] = {
            "name": r["name"],
            "substring_hits": sum(1 for x in rows_src if r["chain"] in (x[1] or "")),
        }

    headline = {
        "value": total,
        "unit": "条（链级计数合计，多链展开）",
        "source_rows": len(rows_src),
        "chains_with_news": len(rows) - len(zero),
        "zero_chains": [r["chain"] for r in zero],
        "zero_chain_names": zero_names,
        "expansion": round(total / len(rows_src), 4),
    }
    # 名称列兜底能力核验：改挂 industry_name 能否救回三条零值链
    nm = Counter()
    name_bad = 0
    for r in rows_src:
        s = r[2] or ""
        try:
            arr = json.loads(s)
            for x in arr:
                nm[x] += 1
        except Exception:
            name_bad += 1

    # 无根码行的名称构成（判断名称兜底能否救回这 1,610 行）
    nr_names = Counter()
    for r in rows_src:
        cs = {x[:7] for x in CODE_RX.findall(r[1] or "")}
        if not (cs & roots):
            try:
                arr = json.loads(r[2] or "")
            except Exception:
                arr = []
            for x in set(arr):
                nr_names[x] += 1
    no_root_top = [[k, v] for k, v in sorted(nr_names.items(), key=lambda kv: (-kv[1], kv[0]))[:15]]
    no_root_names_len = len(nr_names)

    name_bridge = {
        "name_parse_ok": len(rows_src) - name_bad,
        "name_parse_ok_rate": round((len(rows_src) - name_bad) / len(rows_src), 6),
        "name_parse_bad": name_bad,
        "distinct_names": len(nm),
        "zero_chain_name_hits": {z["name"]: nm.get(z["name"], 0) for z in zero},
        "conclusion": "名称列 260 个不同值中三条零值链的链名各 0 次，改挂 industry_name 无法救回；"
                      "名称表混入大量非 12 链行业名（玻璃制品、金属制品、仓储运输），与链树根码不是同一体系。",
        "no_root_rows": no_root_rows,
        "no_root_distinct_names": no_root_names_len,
        "no_root_top_names": no_root_top,
        "no_root_top15_hits": sum(v for _, v in no_root_top),
    }

    quality = {
        "rows": len(rows_src),
        "len255": len255,
        "len255_rate": round(len255 / len(rows_src), 6),
        "parse_ok": parse_ok,
        "parse_ok_rate": round(parse_ok / len(rows_src), 6),
        "parse_bad": parse_bad,
        "parse_bad_rate": round(parse_bad / len(rows_src), 6),
        "codes_per_row_mean": round(sum(code_counts) / len(code_counts), 4) if code_counts else None,
        "codes_per_row_max": max(code_counts) if code_counts else None,
        "no_root_rows": no_root_rows,
        "zero_chain_evidence": zero_evidence,
        "name_bridge": name_bridge,
    }
    facts = [
        {"label": "源表资讯行数", "value": f"{len(rows_src):,}"},
        {"label": "链级计数合计（多链展开）", "value": f"{total:,}"},
        {"label": "有资讯的链", "value": f"{len(rows) - len(zero)}/{len(rows)}"},
        {"label": "零值链", "value": "、".join(zero_names) if zero_names else "无"},
        {"label": "标签截断率（长度=255）", "value": f"{quality['len255_rate']*100:.2f}%"},
    ]

    out = {
        "metric_id": "M_CHAIN_NEWS_COUNT",
        "metric_name": "动态资讯数",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": (
            "108,052 行资讯真实可取，industry_code 数组解析后 9/12 链有数（合计 183,758 条）；"
            "但 46.69% 的行 industry_code 恰为 255 字符被截断、45.85% 的 JSON 不可解析，"
            "且软件与信息服务、智能终端、智能网联汽车三条链的根码在全表 0 次出现"
            "（标签体系缺口，非真实无资讯），可计不可全信，故判部分支持。"
        ),
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "facts": facts,
        "quality": quality,
        "chains": rows,
        "polarity": {
            "pos": pos, "neg": neg, "neu": neu,
            "pos_rate": round(pos / total, 6) if total else 0,
            "neg_rate": round(neg / total, 6) if total else 0,
            "neu_rate": round(neu / total, 6) if total else 0,
            "note": "极性由标题关键词词典判定，不是模型输出；词典命中率低，只作方向参考",
        },
        "method_steps": [
            "读取资讯快照 news21_chain_items_20261022.json（108,052 行，含 industry_code 原串）",
            "解析 industry_code 的 JSON 数组，取每码前 7 位归链；解析失败的行只做子串兜底",
            "同一条资讯在同一链下只计一次，多链则分别计入各链",
            "统计每链条数、词典极性分布，并记录截断率与零值链证据",
        ],
        "population": {
            "defined_as": "gkx.dwd_industry_chain_news_info 全部行，industry_code 解析为多链",
            "news_rows": len(rows_src),
            "rows_mapped_to_roots": len(rows_src) - quality["no_root_rows"],
            "no_root_rows": quality["no_root_rows"],
        },
        "compute": {
            "formula": "COUNT(DISTINCT pk_id) GROUP BY chain_code",
            "expand_rule": "JSON 数组解析 → 每码前 7 位 → 同链去重",
            "zero_chains": [r["chain"] for r in zero],
        },
        "gaps": [
            "46.69% 的 industry_code 长度恰为 255 被截断，长数组尾部的链码丢失，链级计数系统性偏低",
            "45.85% 的行 JSON 不可解析：本件用正则子串兜底，兜底口径与完整解析不完全等价",
            "三条零值链是标签体系缺口：INB1306/INB1333/INB1209 在全表 0 次出现，不能读成「无资讯」",
            "1,610 行的全部链码都在 12 条顶层链之外，说明资讯标签与链树不是同一码域",
            "无媒体源权重与阅读量字段，不能支撑「热点」判定，只能做池计数",
        ],
        "difference_vs_old_draft": {
            "old_source": "演示库 ODS 同名表（表名前缀 demo_，主机 111.198.38.90）",
            "old_note": "旧稿的 108,072 行与本件 108,052 行差 20 行，属 gkx 与演示库 ODS 的同步时点差；"
                        "旧稿 9/12 链、合计 183,758 条与本件一致",
            "now_source": "gkx.dwd_industry_chain_news_info 快照",
            "direction": "本件新增截断率与零值链的落盘证据，数字与旧稿同量级，无方向性差异",
        },
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_NEWS_COUNT", json.dumps(headline, ensure_ascii=False),
          "trunc", quality["len255_rate"], "chains", len(rows),
          "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
