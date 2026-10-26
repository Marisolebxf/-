#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_CHAIN_BOTTLENECK_TYPE_DIST —— 瓶颈类型分布（12 链 × 4 类型 = 48 判定位）

旧稿读演示库的 metric_dist 桶（chain_id × bucket × cnt，publish_status='published'
最新批次），当日 0 行。gkx 内没有 chain_bottleneck，也没有任何「瓶颈类型」结果面
（见 _work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_bottleneck），因此本件把「类型」
重新定义为**相对短板的类型**：四维强度里低于 0.8 × 12 链中位数的那一维，就是该链
在该类型上的瓶颈。

判定（每链 4 个判定位，共 48 个）：
  hit(chain, type) = intensity < 0.8 × median_12
  intensity = 0 时阈值判定必然命中（0 恒小于正值），无需特判。
  primary = argmin(intensity / threshold)，即「最紧的那一维」。

与 M_CHAIN_BOTTLENECK_SEVERITY 同池、同强度、同中位数基线，两件的 12 条链强度
必须逐位相等（正文 §2.6 有对账）。0.8 是本件自定义阈值，待甲方确认。

数据纪律：
  * 只读 code/_snapshots21/ 下落盘快照（由 gkx 183.240.141.251:3318 拉取）；
  * 不发任何 SQL、不连演示库、不 import 本目录以外的模块。

产物：code/M_CHAIN_BOTTLENECK_TYPE_DIST_out.json
"""
from __future__ import annotations

import ast
import json
import os
import re
import time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_BOTTLENECK_TYPE_DIST_out.json")
TOK = re.compile(r"INB\d+")

DIMS = ["tech", "product", "capital", "policy"]
TYPE_CN = {"tech": "技术型", "product": "产品型", "capital": "资本型", "policy": "政策型"}

KW = {
    "INB1204": ["机器人", "工业机器人", "服务机器人", "人形机器人"],
    "INB1209": ["智能网联汽车", "自动驾驶", "车联网", "智能汽车"],
    "INB1236": ["低空经济", "无人机", "通用航空", "eVTOL"],
    "INB1303": ["集成电路", "芯片", "半导体", "晶圆"],
    "INB1306": ["软件", "信息技术服务", "工业软件", "开源"],
    "INB1309": ["人工智能", "大模型", "智能算法", "智算"],
    "INB1323": ["传感器", "智能传感器", "MEMS"],
    "INB1333": ["智能终端", "消费电子", "智能手机", "可穿戴"],
    "INB1354": ["具身智能", "人形机器人", "灵巧手"],
    "INB1502": ["数字创意", "动漫", "数字内容", "游戏产业"],
    "INB2503": ["生物医药", "创新药", "医疗器械", "医药产业"],
    "INB2505": ["合成生物", "生物制造", "生物基"],
}

RATIO = 0.8          # 本件自定义判定阈值（相对中位数），正文 §2.6 已标注待甲方确认


def L(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def parse_list(s):
    if not s:
        return []
    try:
        v = ast.literal_eval(s)
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        return [str(v).strip()]
    except Exception:  # noqa: BLE001
        return [x.strip(" '\"[]") for x in re.split(r"[,，;；]", s) if x.strip(" '\"[]")]


def median(vals):
    v = sorted(vals)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0


def main():
    layer = L("chain21_layer_20261022.json")
    chains, cc, names = layer["chain_name"], layer["chain_city"], layer["names"]
    union = L("region_index_patent_union.json")
    prods = L("chain21_products_20261022.json")["rows"]
    fin = L("chain21_fin_degree_20261022.json")["fin"]
    policy = L("policy_base_20261021.json")

    N = {ch: sum(v for k, v in cc.items() if k.startswith(ch + "|")) for ch in chains}
    P = {ch: sum(v for k, v in union.items() if k.startswith(ch + "|")) for ch in chains}
    R = {}
    for codes, _cat, _cn, plist, _nm in prods:
        items = len(parse_list(plist))
        for t in {x[:7] for x in TOK.findall(codes or "")}:
            R[t] = R.get(t, 0) + items
    F = {}
    for r in fin:
        ch = names.get(r[1])
        if ch:
            F[ch] = F.get(ch, 0) + 1
    O = {ch: 0 for ch in chains}
    for p in policy:
        t = p.get("title") or ""
        for ch, kws in KW.items():
            if any(k in t for k in kws):
                O[ch] += 1

    raw = {
        "tech": {ch: 1000.0 * P.get(ch, 0) / N[ch] for ch in chains},
        "product": {ch: R.get(ch, 0) / N[ch] for ch in chains},
        "capital": {ch: 1000.0 * F.get(ch, 0) / N[ch] for ch in chains},
        "policy": {ch: 1000.0 * O.get(ch, 0) / N[ch] for ch in chains},
    }
    med = {k: median(list(v.values())) for k, v in raw.items()}
    threshold = {k: RATIO * med[k] for k in DIMS}

    rows = []
    for ch, nm in chains.items():
        hit = [k for k in DIMS if raw[k][ch] < threshold[k]]
        primary = (min(hit, key=lambda k: raw[k][ch] / threshold[k]) if hit
                   else "无明显瓶颈")
        rows.append({
            "chain_code": ch,
            "chain_name": nm,
            "types_hit": [TYPE_CN[k] for k in hit],
            "n_types": len(hit),
            "intensity": {k: round(raw[k][ch], 4) for k in DIMS},
            "threshold": {k: round(threshold[k], 4) for k in DIMS},
            "ratio_to_threshold": {k: round(raw[k][ch] / threshold[k], 4) for k in DIMS},
            "primary": TYPE_CN.get(primary, primary),
        })
    rows.sort(key=lambda r: (-r["n_types"], r["chain_code"]))

    dist = {TYPE_CN[k]: sum(1 for r in rows if TYPE_CN[k] in r["types_hit"]) for k in DIMS}
    hits = sum(r["n_types"] for r in rows)
    slots = len(rows) * len(DIMS)
    # 阈值敏感性：只换倍数、不换强度，用来回答「0.8 是不是挑出来的」
    sens = {}
    for rr in (0.6, 1.0):
        h = sum(1 for ch in chains for k in DIMS if raw[k][ch] < rr * med[k])
        sens["%.1f" % rr] = {"hits": h, "hit_rate_pct": round(100.0 * h / slots, 2)}
    payload = {
        "metric_id": "M_CHAIN_BOTTLENECK_TYPE_DIST",
        "metric_name": "瓶颈类型分布",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "48 个「链 × 类型」判定位全部现算、四类型均有非零命中（合计 %d 个），"
            "但两处口径无法闭合：①旧稿的 bucket 枚举取自演示库 metric_dist 结果面，"
            "gkx 内不存在该表，本件的四类型是按强度维重定义，名称对齐而枚举不等价；"
            "②「类型」在这里是相对短板（低于 0.8 倍中位数），不是政策文本或专家标注的"
            "瓶颈成因，且 0.8 倍阈值是本件自定义。语义降格 + 阈值未会签 = 部分支持。"
            % hits
        ),
        "verdict_kind": "computed_with_declared_gap",
        "base_years_used": ["2021", "2022", "2023", "2024"],
        "base_years_missing": ["2025", "2026"],
        "base_years_note": (
            "专利维 ≤2024 截断；产品/融资/政策三维无年度窗口，故分布是截面而非年度分布。"
        ),
        "sources": [
            "gkx @ 183.240.141.251:3318: gkx.dwd_org_industry_tags / dwd_patent / "
            "dwd_org_industry_product_tags / dwd_org_financing_info / dwd_policy_base",
            "code/_snapshots21/chain21_layer_20261022.json（链成员与链名，与 M_CHAIN_ENTERPRISE_COUNT 同池）",
            "code/_snapshots21/region_index_patent_union.json、chain21_products_20261022.json、"
            "chain21_fin_degree_20261022.json、policy_base_20261021.json",
        ],
        "rule": {
            "unit": "条（每命中「链 × 类型」计 1）",
            "judge": "强度 < 0.8 × 12 链中位数 → 该链该类型存在瓶颈；强度 = 0 直接命中",
            "types": "技术型（专利/企业）、产品型（产品条目/企业）、资本型（融资事件/企业）、政策型（标题命中/企业）",
            "multi_hit": "一条链可命中多类；12 链 × 4 类 = 48 个判定位",
            "consistency": "与 M_CHAIN_BOTTLENECK_SEVERITY 同池同强度、同中位数基线",
        },
        "medians": {k: round(med[k], 6) for k in DIMS},
        "thresholds": {k: round(threshold[k], 4) for k in DIMS},
        "sensitivity": sens,
        "pool_atoms": {
            "tags_rows": layer.get("rows"),
            "product_rows": len(prods),
            "fin_rows": len(fin),
            "policy_rows": len(policy),
            "member_sum": sum(N.values()),
            "member_min": min(N.values()),
            "member_max": max(N.values()),
            "patent_min": min(P.values()),
            "patent_max": max(P.values()),
        },
        "distribution": dist,
        "distribution_pct": {k: round(100.0 * v / hits, 2) for k, v in dist.items()},
        "chains": rows,
        "stats": {
            "judgement_slots": slots,
            "hits": hits,
            "hit_rate_pct": round(100.0 * hits / slots, 2),
            "n_chains_with_hit": sum(1 for r in rows if r["n_types"] > 0),
            "n_chains_clean": sum(1 for r in rows if r["n_types"] == 0),
        },
        "difference_vs_old_draft": {
            "old_source": "演示库 metric_dist 桶（chain_id × bucket × cnt），publish_status='published' 最新批次，当日 0 行",
            "old_result": "分布桶 0 行，旧稿判「发布面未灌」",
            "now_result": "48 个判定位现算出命中分布，四类型均有非零",
            "caliber_gap": "旧桶的 bucket 枚举值（如 tech/capital/…）未在库内出现，"
                           "本件的四类型是按强度维重定义，名称对齐、枚举不等于旧桶",
            "bias": "0.8 倍中位数是判定阈值，可枚举但仍是人为选择；阈值改为 0.6 或 1.0 会改变各类型计数（见 §四）",
        },
        "gaps": [
            "「类型」由强度维定义，不是政策文本/专家标注的瓶颈成因，语义上是「相对短板类型」",
            "产品维 3 条链（智能网联汽车/低空经济/生物医药）在 gkx 产品标签表零行，"
            "产品型瓶颈直接判满，无法区分「真的没产品」与「没填报」",
            "政策维关键词表只有 3—4 个词/链，长尾政策（如「具身智能」专项）可能漏命中",
            "阈值 0.8 倍中位数未会签；阈值变动会同时改变类型计数与 primary 归类",
            "同一链可命中多类，四类型计数之和（%d）大于有瓶颈的链数（%d），"
            "不能读作「链的份额」" % (hits, sum(1 for r in rows if r["n_types"] > 0)),
        ],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - T0, 2),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("[ok] %s slots=%d hits=%d rate=%.2f%% dist=%s"
          % (payload["metric_id"], slots, hits, 100.0 * hits / slots, dist))
    for r in rows:
        print("  %-10s %-8s n=%d %-28s primary=%s"
              % (r["chain_code"], r["chain_name"], r["n_types"],
                 ",".join(r["types_hit"]) or "-", r["primary"]))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
