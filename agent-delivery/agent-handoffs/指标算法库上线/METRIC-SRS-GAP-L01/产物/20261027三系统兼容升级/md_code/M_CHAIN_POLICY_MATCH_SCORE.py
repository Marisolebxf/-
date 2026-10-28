#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_POLICY_MATCH_SCORE 产业政策匹配度（gkx 三方库，20261023 重建版）。

口径（calc-logic/CHAIN/M_CHAIN_POLICY_MATCH_SCORE.md）三维等权：
  政策标签匹配度 / 政策支持覆盖度 / 政策支持强度。

本件只做**供给侧的产业链—政策文本匹配**，并明确三点降级：
  1. `keywords` / `keypoints` 两列在 20,000 行里 **0 行有值** → 标签维只能用 title；
  2. `policy_support` 全表 20,000 行都是**小写字符串 'null'** → 支持覆盖度维不可算；
  3. `theme` 只有 2 行非空 → 不能用 theme 做链归属。
  剩下「标题命中数（供给密度）」与「国家级占比（支持强度代理）」两维。

匹配词典是**本件自拟**的链锚词（每链 3—6 个），不是甲方口径；
词典全文落在 `probes.lexicon`，可逐词复核。命中是多标签：一条政策可同时命中多条链，
故命中数之和（202）大于去重政策数。

打分：两维各取百分位秩（0—100），等权 0.5/0.5；
`match_score` 是**相对指数**，不是「匹配概率」，也不代表企业需求被满足。

产物：code/M_CHAIN_POLICY_MATCH_SCORE_out.json
"""
from __future__ import annotations

from collections import Counter, defaultdict

import _chain5_common as C

METRIC = "M_CHAIN_POLICY_MATCH_SCORE"

LEXICON = {
    "INB1309": ["人工智能", "智能算力", "大模型", "生成式人工智能", "机器学习", "智算"],
    "INB1306": ["软件", "信息技术服务", "工业软件", "开源", "信息系统集成"],
    "INB1333": ["智能终端", "智能手机", "可穿戴", "智能硬件", "超高清视频", "虚拟现实"],
    "INB2503": ["生物医药", "创新药", "医疗器械", "生物制药", "细胞治疗", "基因治疗"],
    "INB1303": ["集成电路", "芯片", "半导体", "晶圆", "封装测试"],
    "INB1323": ["传感器", "智能传感", "MEMS"],
    "INB2505": ["合成生物", "生物制造", "生物基材料", "酶催化"],
    "INB1204": ["机器人", "工业机器人", "服务机器人"],
    "INB1236": ["低空经济", "无人机", "通用航空", "eVTOL", "低空空域"],
    "INB1502": ["数字创意", "动漫", "游戏产业", "网络文学", "数字文化", "电竞"],
    "INB1354": ["具身智能", "人形机器人"],
    "INB1209": ["智能网联汽车", "自动驾驶", "车联网", "智能汽车"],
}
# 不是产业政策文本：采购/招标/展会/安保通告等。剔除后仍保留「通知/公告/办法」类政策。
EXCLUDE = ["招标", "采购", "中标", "成交", "竞争性磋商", "询价", "招聘",
           "培训服务", "博览会", "展会", "安全管理", "通告"]


def rank_desc(values: dict) -> dict:
    """百分位秩（值越大分越高），并列取平均秩。"""
    items = sorted(values.items(), key=lambda kv: kv[1])
    n, out, i = len(items), {}, 0
    while i < n:
        j = i
        while j + 1 < n and items[j + 1][1] == items[i][1]:
            j += 1
        s = 0.0 if n == 1 else round((i + j) / 2.0 / (n - 1) * 100, 2)
        for k in range(i, j + 1):
            out[items[k][0]] = s
        i = j + 1
    return out


def spearman(a: dict, b: dict) -> float:
    keys = [k for k in a if k in b]
    n = len(keys)
    if n < 3:
        return 0.0
    ra = {k: i for i, k in enumerate(sorted(keys, key=lambda k: a[k]))}
    rb = {k: i for i, k in enumerate(sorted(keys, key=lambda k: b[k]))}
    d2 = sum((ra[k] - rb[k]) ** 2 for k in keys)
    return round(1 - 6 * d2 / (n * (n * n - 1)), 4)


def main():
    pol = C.load("policy_base_20261021.json")
    idx = C.load("chain_firm_index_20261023.json")
    names = idx["chain_name"]

    invalid_date = [p for p in pol if not p.get("date") or p["date"] == "0000-00-00"]
    in_window = [p for p in pol if p not in invalid_date and "2015-01-01" <= p["date"] <= "2024-12-31"]
    eligible = [p for p in in_window if not any(x in p["title"] for x in EXCLUDE)]
    excluded_docs = len(in_window) - len(eligible)

    hits = defaultdict(list)
    multi = 0
    for p in eligible:
        matched = [c for c, kws in LEXICON.items() if any(k in p["title"] for k in kws)]
        if len(matched) > 1:
            multi += 1
        for c in matched:
            hits[c].append(p)

    rows = []
    for c in C.ROOTS:
        hs = hits[c]
        nat = sum(1 for p in hs if p.get("level") == 4)
        sz = sum(1 for p in hs if p.get("city") == "深圳市")
        firms = idx["chain_firms"].get(c, 0)
        rows.append({
            "chain": c, "chain_name": names.get(c), "firms": firms,
            "policy_hits": len(hs), "national_hits": nat, "shenzhen_hits": sz,
            "non_shenzhen_hits": len(hs) - sz,
            "density_per_1000_firms": round(len(hs) / firms * 1000, 4) if firms else None,
            "national_share_pct": round(100.0 * nat / len(hs), 2) if hs else None,
            "examples": [p["title"][:60] for p in hs[:3]],
        })

    dscore = rank_desc({r["chain"]: r["density_per_1000_firms"] for r in rows})
    nscore = rank_desc({r["chain"]: (r["national_share_pct"] or 0.0) for r in rows})
    for r in rows:
        r["density_score"] = dscore[r["chain"]]
        r["national_score"] = nscore[r["chain"]] if r["policy_hits"] else None
        if r["policy_hits"]:
            r["match_score"] = round(0.5 * r["density_score"] + 0.5 * r["national_score"], 2)
            r["weight_coverage"] = 0.5
        else:
            r["match_score"] = 0.0
            r["weight_coverage"] = 0.5
    rows.sort(key=lambda r: -r["match_score"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    base_scores = {r["chain"]: r["density_score"] for r in rows}
    comp_scores = {r["chain"]: r["match_score"] for r in rows}
    rho = spearman(base_scores, comp_scores)

    report = {
        "metric_name": "产业政策匹配度",
        "unit": "0—100（相对指数）",
        "calc_logic_ref": "gkx-orchestration/agent-delivery/metrics/calc-logic/CHAIN/M_CHAIN_POLICY_MATCH_SCORE.md",
        "data_source": {
            "engine": "只读快照（源：三方库 gkx @ 183.240.141.251:3318）",
            "tables": ["gkx.dwd_policy_base", "gkx.dwd_org_industry_tags"],
            "snapshots": ["code/_snapshots21/policy_base_20261021.json",
                          "code/_snapshots21/policy_field_fill_20261022.json",
                          "code/_snapshots21/chain_firm_index_20261023.json"],
        },
        "probes": {
            "policy_rows": len(pol),
            "invalid_date_rows": len(invalid_date),
            "in_window_rows": len(in_window),
            "excluded_non_policy_docs": excluded_docs,
            "eligible_rows": len(eligible),
            "date_min": min(p["date"] for p in pol if p.get("date") and p["date"] != "0000-00-00"),
            "date_max": max(p["date"] for p in pol),
            "date_window": "2015-01-01—2024-12-31（表内最晚 2024-02-18，2025/2026 无政策）",
            "multi_chain_hit_docs": multi,
            "hit_pairs": sum(len(v) for v in hits.values()),
            "unique_hit_docs": len({p["id"] for v in hits.values() for p in v}),
            "level_distribution": dict(Counter(p.get("level") for p in pol)),
            "keywords_nonempty_rows": 0,
            "keypoints_nonempty_rows": 0,
            "theme_nonempty_rows": sum(1 for p in pol if str(p.get("theme")) not in ("0", "None", "NULL")),
            "policy_support_literal_null_rows": 20000,
            "policy_support_total_rows": 20000,
            "node_code_columns": 0,
            "lexicon": LEXICON,
            "exclude_terms": EXCLUDE,
            "rank_correlation_density_vs_composite": rho,
            "judgment_note": "政策支持覆盖度维整维不可算；标签维只剩 title；强度维用 level=4 占比代理。",
            "sensitivity": {
                "software_without_word_ruanjian_hits": sum(1 for p in eligible if any(
                    k in p["title"] for k in ["信息技术服务", "工业软件", "开源", "信息系统集成"])),
                "icv_with_xinnengyuan_hits": sum(1 for p in eligible if any(
                    k in p["title"] for k in ["智能网联汽车", "自动驾驶", "车联网", "智能汽车", "新能源汽车"])),
                "note": "只给命中数变化，不重算全表排名；用于证明词典选择对这两条链敏感。",
            },
        },
        "chain_rows": rows,
        "notes": [
            "`policy_support` 20,000 行全为小写字符串 'null'（占位符，不是 SQL NULL），故「支持对象覆盖」不可算。",
            "`keywords`/`keypoints` 各 0 行非空；`theme` 仅 2 行非空，不能用于链归属。",
            "level 映射：4=国家级、3=省级、2=市级、1=区县级、0=未知；全国级 2,174 条。",
            "一条政策可命中多条链（12 条），命中数之和 202 > 去重政策数；不做互斥拆分。",
            "密度分母是链企业数（同一快照），不是政策数；`match_score` 只用于 12 条链互排。",
            "深圳市政策（city=深圳市）单独计数，但不进得分——本件评的是产业链，不是区域。",
        ],
    }
    report.update(C.base_decl(
        [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024], [2025, 2026],
        "政策表是存量表，2015—2024 为可用区间；表内最晚发布日 2024-02-18，2025、2026 年零行，"
        "故不把这两年按 0 摊入任何年度均值。本件是截面（全窗口累计），不做年度增速。"))
    report["support_judgment"] = "部分支持"
    report["support_reason"] = (
        "三维里只有「标题命中密度」与「国家级占比」可算，政策支持覆盖度维因 policy_support "
        "整列为字符串 'null' 而永久不可得，标签维也因 keywords/keypoints 全空退化为只读标题。")

    C.write_out(METRIC, report)
    print("eligible", len(eligible), "pairs", sum(len(v) for v in hits.values()), "rho", rho)
    for r in rows:
        print(r["chain"], r["chain_name"], r["policy_hits"], r["national_hits"], r["match_score"])


if __name__ == "__main__":
    main()
