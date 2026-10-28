#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_HOT_NEWS_COUNT · 链热门资讯数（20261021 换源版）

旧稿公式（照抄）
----------------
正式口径 = 链内资讯热度分（heat_score）≥ 全库 P90 分位的资讯条数（Top 10%）。
临时口径 = 链资讯全量代热点，与 M_CHAIN_NEWS_COUNT 同源同数。

换源后的硬事实
--------------
1. `gkx` 里**没有 heat_score 字段**（`dwd_industry_chain_news_info` 只有
   pk_id/industry_code/industry_name/title/publish_date/abstract/source）。
   本脚本不伪造该字段，改用三个**可观测替代量**组成 0—3 的热度代理：
     I_reprint = 同一归一化标题被 ≥2 个不同 source 报道（跨源转载）
     I_burst   = 该资讯所在 ISO 周的全库资讯量 ≥ 全库周量 P90（报道峰值周）
     I_salience= 标题命中高显著度词（突破/首次/全球首/最大/融资/获批…）
   热度分 = 三项之和；全库 P90 = 1，按「严格大于 P90」取 ≥2 为热门，
   避免阈值并列把 38.9% 的资讯都算成热门。
2. 链归属不用 `industry_code` 多值数组：实测 105,407/108,052 行是多值，
   平均 20.11 个码/行、52,057 行被 varchar(255) 截断；按数组计数会让
   12 条链里有 9 条同时得到 8 万条左右，完全没有区分度（见 sensitivity）。
   本件改用**标题命中链级实体词表**做主口径，数组口径只作敏感性对照。
3. 数据窗口只有 2025-02-01—2026-07-27（18 个月），不能做年度趋势。

输出：`code/M_CHAIN_HOT_NEWS_COUNT_out.json`
"""
from __future__ import annotations

import datetime as dt
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21" / "news21_chain_items_20261022.json"
OUT = HERE / "M_CHAIN_HOT_NEWS_COUNT_out.json"
METRIC = "M_CHAIN_HOT_NEWS_COUNT"
NAME = "链热门资讯数"

CHAIN = {
    "INB1306": ("软件与信息服务", ["软件", "信息服务", "SaaS", "工业软件"]),
    "INB1309": ("人工智能", ["人工智能", "大模型", "算力", "AI"]),
    "INB1333": ("智能终端", ["智能终端", "消费电子", "手机", "可穿戴"]),
    "INB1502": ("数字创意", ["数字创意", "数字文化", "文化创意", "游戏", "影视"]),
    "INB2505": ("合成生物", ["合成生物", "生物制造", "生物合成"]),
    "INB1204": ("机器人", ["机器人"]),
    "INB1303": ("集成电路", ["集成电路", "半导体", "芯片"]),
    "INB1323": ("传感器", ["传感器"]),
    "INB1354": ("具身智能", ["具身智能", "人形机器人"]),
    "INB1209": ("智能网联汽车", ["智能网联汽车", "新能源汽车", "车联网", "自动驾驶"]),
    "INB1236": ("低空经济", ["低空经济", "低空", "无人机", "eVTOL"]),
    "INB2503": ("生物医药", ["生物医药", "创新药", "医疗器械", "医药"]),
}
SALIENCE = ["突破", "首次", "首个", "全球首", "最大", "领先", "发布", "上市", "融资",
            "签约", "投产", "中标", "获批", "落地", "开工", "增资", "并购", "量产", "新高"]
ASCII_TOKEN = re.compile(r"^[A-Za-z0-9+./-]+$")


def code_list(s: str) -> list[str]:
    """industry_code 是 JSON 数组字面量；截断行按正则兜底抽取。"""
    s = s or ""
    try:
        v = json.loads(s)
        if isinstance(v, list):
            return [str(x) for x in v]
    except Exception:
        pass
    return re.findall(r"[A-Z]{3}\d{4,}", s)


def norm_title(t: str) -> str:
    return re.sub(r"[\s\W_]+", "", t or "").lower()


def token_hit(title: str, token: str) -> bool:
    if ASCII_TOKEN.match(token):
        return re.search(r"(?<![A-Za-z])" + re.escape(token) + r"(?![A-Za-z])", title) is not None
    return token in title


def iso_week(d: str):
    y, m, dd = (int(x) for x in d.split("-"))
    return dt.date(y, m, dd).isocalendar()[:2]


def stats(vals):
    vals = sorted(v for v in vals if v is not None)
    if not vals:
        return {"n": 0}
    n = len(vals)
    return {
        "n": n, "min": round(vals[0], 4), "max": round(vals[-1], 4),
        "mean": round(sum(vals) / n, 4), "median": round(statistics.median(vals), 4),
        "p90": round(vals[int(0.9 * (n - 1))], 4),
        "distinct": len({round(v, 6) for v in vals}),
    }


def rank(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    out = [0.0] * len(vals)
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = r
        i = j + 1
    return out


def spearman(a, b):
    if len(a) < 3:
        return None
    ra, rb = rank(a), rank(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return round(num / den, 4) if den else None


def main() -> None:
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    rows = snap["rows"]
    n = len(rows)

    # ---------- 可观测热度代理 ----------
    title_sources = defaultdict(set)
    for r in rows:
        title_sources[norm_title(r[3])].add(r[5])
    week_volume = Counter(iso_week(r[4]) for r in rows)
    week_vals = sorted(week_volume.values())
    week_p90 = week_vals[int(0.9 * (len(week_vals) - 1))]

    def heat(r):
        k = norm_title(r[3])
        rep = 1 if len(title_sources[k]) >= 2 else 0
        burst = 1 if week_volume[iso_week(r[4])] >= week_p90 else 0
        sal = 1 if any(token_hit(r[3], w) for w in SALIENCE) else 0
        return rep + burst + sal, rep, burst, sal

    score_dist = Counter(heat(r)[0] for r in rows)
    hot_threshold = 2  # 全库 P90=1，严格大于 P90

    per = {c: {"n": 0, "hot": 0, "src": Counter(), "hot_titles": []} for c in CHAIN}
    mapped = multi = 0
    for r in rows:
        title = r[3]
        hits = [c for c, (_nm, toks) in CHAIN.items() if any(token_hit(title, t) for t in toks)]
        if hits:
            mapped += 1
        if len(hits) > 1:
            multi += 1
        sc, rep, burst, sal = heat(r)
        for c in hits:
            d = per[c]
            d["n"] += 1
            d["src"][r[5]] += 1
            if sc >= hot_threshold:
                d["hot"] += 1
                if len(d["hot_titles"]) < 5:
                    d["hot_titles"].append([title[:80], r[4], r[5], sc, rep, burst, sal])

    per_chain = []
    for c, (cn, _toks) in CHAIN.items():
        d = per[c]
        top_src = d["src"].most_common(3)
        per_chain.append({
            "chain": c, "chain_name": cn,
            "n_items": d["n"], "n_hot": d["hot"],
            "hot_share_pct": round(100.0 * d["hot"] / d["n"], 2) if d["n"] else None,
            "n_sources": len(d["src"]),
            "top_sources": [[a, b] for a, b in top_src],
            "top_hot_titles": d["hot_titles"],
        })
    per_chain.sort(key=lambda x: -x["n_hot"])

    # ---------- 数组口径敏感性（说明为什么不用它） ----------
    code_all = Counter()
    code_first = Counter()
    avg_codes = 0
    trunc = 0
    for r in rows:
        cs = code_list(r[1])
        avg_codes += len(cs)
        if len(r[1] or "") >= 250:
            trunc += 1
        for x in set(cs):
            if x in CHAIN:
                code_all[x] += 1
        if cs and cs[0] in CHAIN:
            code_first[cs[0]] += 1
    avg_codes = round(avg_codes / n, 2) if n else 0
    all_counts = [code_all.get(c, 0) for c in CHAIN]
    nz = [v for v in all_counts if v]
    flat_ratio = round(max(nz) / min(nz), 2) if len(nz) > 1 and min(nz) else None
    token_counts = [per[c]["n"] for c in CHAIN]

    # ---------- 交叉核对 ----------
    month_dist = Counter(r[4][:7] for r in rows)
    src_counter = Counter(r[5] for r in rows)
    top_titles = sorted(title_sources.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]

    total_hot = sum(d["hot"] for d in per.values())
    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）/ dwd_industry_chain_news_info",
        "formula": (
            "hot_item = I_reprint + I_burst + I_salience ≥ 2；"
            "hot_count(c) = Σ hot_item·[标题命中链 c 的实体词表]"
        ),
        "heat_score_available": False,
        "heat_score_note": (
            "gkx 资讯表无 heat_score 字段；本件不伪造热度值，改用跨源转载、"
            "全库周报道峰值、标题显著度三项可观测替代量。三项等权是**本件自定义、需甲方确认**。"
        ),
        "probes": {
            "rows": n,
            "date_min": min(r[4] for r in rows),
            "date_max": max(r[4] for r in rows),
            "distinct_sources": len(src_counter),
            "top_sources": [[a, b] for a, b in src_counter.most_common(10)],
            "distinct_titles": len(title_sources),
            "multi_code_rows": sum(1 for r in rows if len(code_list(r[1])) > 1),
            "truncated_code_rows": trunc,
            "avg_codes_per_row": avg_codes,
            "chain_mapped_rows": mapped,
            "chain_unmapped_rows": n - mapped,
            "chain_mapped_pct": round(100.0 * mapped / n, 2) if n else None,
            "multi_chain_rows": multi,
            "weeks": len(week_vals),
            "weekly_volume_p90": week_p90,
            "weekly_volume_max": max(week_vals),
            "months": dict(sorted(month_dist.items())),
        },
        "heat_proxy": {
            "components": {
                "I_reprint": "同一归一化标题的 distinct source ≥ 2",
                "I_burst": "所在 ISO 周全库资讯量 ≥ 全库周量 P90",
                "I_salience": "标题命中 " + "/".join(SALIENCE),
            },
            "component_weights": {"I_reprint": 1, "I_burst": 1, "I_salience": 1},
            "score_dist": {str(k): v for k, v in sorted(score_dist.items())},
            "p90_score": 1,
            "hot_threshold": hot_threshold,
            "hot_items": total_hot,
            "hot_share_pct": round(100.0 * total_hot / n, 2) if n else None,
            "title_reprint_dist": {
                "distinct_titles": len(title_sources),
                "sources_ge2": sum(1 for v in title_sources.values() if len(v) >= 2),
                "sources_ge3": sum(1 for v in title_sources.values() if len(v) >= 3),
            },
        },
        "per_chain": per_chain,
        "stats_hot": stats([r["n_hot"] for r in per_chain]),
        "stats_items": stats([r["n_items"] for r in per_chain]),
        "sensitivity": {
            "count_threshold_ge1": sum(v for k, v in score_dist.items() if k >= 1),
            "count_threshold_ge2": total_hot,
            "count_threshold_ge3": score_dist.get(3, 0),
            "n_items_sum": sum(r["n_items"] for r in per_chain),
            "code_array_all": {c: code_all.get(c, 0) for c in CHAIN},
            "code_array_first": {c: code_first.get(c, 0) for c in CHAIN},
            "code_array_flat_ratio": flat_ratio,
            "spearman_token_vs_code_all": spearman(token_counts, all_counts),
            "note": (
                "industry_code 为多值 JSON 数组，平均 "
                f"{avg_codes}/{round(100.0*trunc/n,2)}% 行被截断；"
                f"按数组全量计数时 12 条链里有 {sum(1 for v in all_counts if v == 0)} 条为 0，"
                f"非零链最大/最小比 {flat_ratio}，与标题口径的 Spearman 仅 "
                f"{spearman(token_counts, all_counts)}，不具区分度。"
                f"标题词表口径覆盖 {round(100.0*mapped/n,2)}% 的资讯，"
                "未覆盖部分不进分子，也不补 0。"
            ),
        },
        "top_titles_by_sources": [[t, len(s)] for t, s in top_titles],
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": (
                f"链资讯 {n:,} 行真实、可计数，2025-02 至 2026-07 连续 18 个月；"
                f"但 heat_score 字段整库不存在，本件只能用三项可观测替代量定义热度，"
                f"代理在 {len(CHAIN)} 条链上产出 {total_hot:,} 条热门资讯（{round(100.0*total_hot/n,2)}%），"
                "热度语义（读者触达/传播效果）无法与原文口径对齐；"
                f"标题词表只覆盖 {round(100.0*mapped/n,2)}% 的资讯，"
                "industry_code 多值且 48.2% 被截断，不能作为链归属依据；"
                "窗口仅 18 个月，无法支撑年度趋势。故最高判部分支持。"
            ),
            "criteria": {
                "heat_score_field_exists": False,
                "observable_proxy_defined": True,
                "proxy_weights_official": False,
                "chain_attribution": "title_token（非库内数组）",
                "chain_mapped_pct": round(100.0 * mapped / n, 2) if n else None,
                "window_months": 18,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "本指标不做年度同比，分母不是年度序列：资讯窗口为 2025-02-01—2026-07-27 的"
            "全量截面。used/missing 为空表示没有年度基期，不是「缺年按 0 摊入」。"
        ),
        "sources": [
            {"path": "code/_snapshots21/news21_chain_items_20261022.json",
             "table": "gkx.dwd_industry_chain_news_info",
             "host": "183.240.141.251:3318", "role": "资讯主表 108,052 行"},
            {"path": "code/_build_news21_snapshot.py", "role": "快照构建脚本（一次性）"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("rows", n, "hot", total_hot, "threshold", hot_threshold)
    for r in per_chain:
        print(r["chain"], r["chain_name"], r["n_items"], r["n_hot"], r["hot_share_pct"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
