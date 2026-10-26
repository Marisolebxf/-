#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""资讯正面情感占比（M_CHAIN_NEWS_SENTIMENT_RATIO）—— 词典代理，自包含。

口径：gkx 全库没有任何情感/极性列（information_schema 检索 sentiment / polarity /
    emotion 零命中），链资讯表 13 个字段里也没有极性字段。正式口径不可执行，
    只能用标题词典代理：
        pos = 命中「增长/突破/获批/签约/融资…」20 个正向词
        neg = 命中「下降/亏损/处罚/诉讼/停产…」20 个负向词
        极性 = pos>neg 正 / neg>pos 负 / 持平中性；比例 = pos/(pos+neg)，中性不进分母。
这不是正式值：正式值需甲方提供情感标注或可核验模型，代理值只作排序参考。

上游：极性由 `code/_build_chain_panel21.py`（同一目录、可运行）按上述 40 词逐条判定后
落进 `chain_panel21.json`；本脚本只做链级汇总，不重判文本，保证与资讯数同源同批行。

产物：chains[].value = 正面占比（小数，4 位）；同时给 pos/neg/neu。

运行：cd code && python3 M_CHAIN_NEWS_SENTIMENT_RATIO.py
产物：code/M_CHAIN_NEWS_SENTIMENT_RATIO_out.json（覆盖写）
"""
from __future__ import annotations

import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_NEWS_SENTIMENT_RATIO_out.json")

BASE_USED = []
BASE_MISSING = []
BASE_NOTE = "截面指标：统计当前存量资讯的极性分布，不设年度分母；资讯表无年度字段。"

POS = ["增长", "突破", "领先", "获批", "签约", "融资", "扩产", "创新", "提升", "利好",
       "合作", "中标", "投产", "成功", "发布", "新高", "落地", "增资", "量产", "上市"]
NEG = ["下降", "亏损", "裁员", "停产", "处罚", "违规", "风险", "诉讼", "召回", "下滑",
       "退出", "破产", "事故", "质疑", "失败", "延期", "解约", "罚", "退市", "欠款"]

SOURCES = [
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_industry_chain_news_info", "rows": 108052,
     "snapshot": "code/_snapshots21/news21_chain_items_20261022.json",
     "pulled_at": "2026-10-22T14:55:07"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_org_industry_tags", "rows": 2283762,
     "snapshot": "code/_snapshots21/chain_panel21.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "gkx.dwd_industry_chain_info", "rows": 1273,
     "snapshot": "code/_snapshots21/chain_tree_links_20261022.json"},
    {"library": "gkx", "host": "183.240.141.251:3318", "user": "gkx_reader_zp",
     "table": "information_schema.COLUMNS（情感列检索）", "rows": 0,
     "snapshot": "code/_snapshots21/batch5_probe2_20261022.json"},
]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def main():
    t0 = time.time()
    panel = load("chain_panel21.json")
    chains = panel["chains"]
    diag = load("news21_code_diag_20261022.json")
    rows = []
    for c in chains:
        nw = c.get("news") or {}
        pos, neg, neu = nw.get("pos", 0), nw.get("neg", 0), nw.get("neu", 0)
        den = pos + neg
        rows.append({"chain": c["chain"], "name": c["name"],
                     "value": round(pos / den, 4) if den else None,
                     "pos": pos, "neg": neg, "neu": neu, "denom": den,
                     "samples": pos + neg + neu})
    rows.sort(key=lambda r: -(r["value"] if r["value"] is not None else -1))
    tp = sum(r["pos"] for r in rows)
    tn = sum(r["neg"] for r in rows)
    tneu = sum(r["neu"] for r in rows)
    zero = [r["chain"] for r in rows if not r["denom"]]
    headline = {
        "value": round(tp / (tp + tn), 4) if (tp + tn) else None,
        "unit": "正面占比（0—1）", "pos": tp, "neg": tn, "neutral": tneu,
        "formula": "pos/(pos+neg)，中性不进分母",
        "polar_rows": tp + tn,
        "neutral_share": round(tneu / (tp + tn + tneu), 4) if (tp + tn + tneu) else None,
        "chains_with_samples": len(rows) - len(zero),
        "zero_chains": zero,
        "caveat": "词典代理值，非情感标注金标，不进口径",
    }
    facts = [
        {"label": "链级正/负/中性条数", "value": f"{tp:,} / {tn:,} / {tneu:,}"},
        {"label": "总体正面占比（代理）", "value": headline["value"]},
        {"label": "中性占比", "value": headline["neutral_share"]},
        {"label": "有极性样本的链", "value": f"{len(rows) - len(zero)}/{len(rows)}"},
        {"label": "零样本链", "value": "、".join(r["name"] for r in rows if not r["denom"])},
        {"label": "gkx 情感/极性列个数", "value": 0},
        {"label": "资讯标签体系 7 位码个数", "value": diag["distinct_7digit_codes"]},
        {"label": "与 12 链根码重合的根码数", "value": diag["roots_hit"]},
        {"label": "零命中根码", "value": "、".join(diag["roots_zero"])},
    ]
    population = {
        "defined_as": "有资讯且标题命中正/负词典的链级样本（一条资讯可挂多链）",
        "news_rows": diag["news_rows"],
        "pos": tp, "neg": tn, "neutral": tneu,
        "chain_label_expansion": tp + tn + tneu,
    }
    compute = {
        "formula": "pos/(pos+neg)",
        "lexicon_size": len(POS) + len(NEG),
        "lexicon_pos": POS,
        "lexicon_neg": NEG,
        "polarity_rule": "标题内正词数 > 负词数判正，反之判负，相等判中性",
        "neutral_policy": "中性不计入分母",
        "chain_rule": "industry_code JSON 数组逐码取前 7 位归链，同链去重",
        "proxy": True,
        "zero_chain_reason": "资讯表 230 个 7 位码与 12 链根码仅 9 个重合；INB1306/INB1333/INB1209 零命中，"
                             "是资讯标签体系覆盖缺口，不是这三条链真的没有资讯",
    }
    STEPS = ["读取资讯快照 news21_chain_items_20261022.json（108,052 行标题）",
             "上游按 20 正 / 20 负词典逐条判极性并落进 chain_panel21.json",
             "按 industry_code 前 7 位归链、同链去重后汇总 pos/neg/neu",
             "算 pos/(pos+neg)，中性不进分母",
             "标注代理属性并用标签体系诊断解释 3 条零样本链"]
    out = {
        "metric_id": "M_CHAIN_NEWS_SENTIMENT_RATIO",
        "metric_name": "资讯正面情感占比",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "support_judgment": "部分支持",
        "judgment_reason": "链资讯 108,052 条标题可取，但 gkx 全库没有任何情感/极性列（information_schema "
                           "检索 sentiment/polarity/emotion 零命中），40 词词典代理值只能作排序参考、不能作验收值；"
                           "另有 3 条链因资讯标签体系与链树根码不重合而无样本。",
        "sources": SOURCES,
        "base_years_used": BASE_USED,
        "base_years_missing": BASE_MISSING,
        "base_years_note": BASE_NOTE,
        "headline": headline,
        "facts": facts,
        "chains": rows,
        "method_steps": STEPS,
        "population": population,
        "compute": compute,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("[ok]", "M_CHAIN_NEWS_SENTIMENT_RATIO", json.dumps(headline, ensure_ascii=False),
          "chains", len(rows), "sec", round(time.time() - t0, 2))


if __name__ == "__main__":
    main()
