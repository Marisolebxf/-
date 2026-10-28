#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_DEEP_125_1 —— 产业瓶颈堵点识别模型（五维加权综合分）

旧稿读 chain_bottleneck 的五维得分（tech/talent/market/capital/policy）与
comprehensive_score，当日 0 行。本件不依赖结果表，用 gkx 现算五维原值后按
固定权重合成。权重是本件设定（旧稿模型权重未公开、Q015 未闭合），写死如下：
  技术 0.25、市场（产品）0.20、资本 0.20、主体规模 0.20、政策 0.15
各维先做 12 链 min-max 归一到 0—100，再加权。人才维在 gkx 无链级源
（学者/机构无法挂链，本批已实测 join 0），用「主体规模」替代并披露。
"""
from __future__ import annotations
import ast, json, os, re, time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_DEEP_125_1_out.json")
TOK = re.compile(r"INB\d+")

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
W = {"tech": 0.25, "market": 0.20, "capital": 0.20, "scale": 0.20, "policy": 0.15}


def L(n):
    with open(os.path.join(SNAP, n), encoding="utf-8") as f:
        return json.load(f)


def parse_list(s):
    if not s:
        return []
    try:
        v = ast.literal_eval(s)
        return [str(x).strip() for x in v if str(x).strip()] if isinstance(v, list) else [str(v).strip()]
    except Exception:
        return [x.strip(" '\"[]") for x in re.split(r"[,，;；]", s) if x.strip(" '\"[]")]


layer = L("chain21_layer_20261022.json")
chains, cc, names = layer["chain_name"], layer["chain_city"], layer["names"]
union = L("region_index_patent_union.json")
prods = L("chain21_products_20261022.json")["rows"]
fin = L("chain21_fin_degree_20261022.json")["fin"]
policy = L("policy_base_20261021.json")

N = {ch: sum(v for k, v in cc.items() if k.startswith(ch + "|")) for ch in chains}
P = {ch: sum(v for k, v in union.items() if k.startswith(ch + "|")) for ch in chains}
R = {}
for codes, cat, cn, plist, nm in prods:
    for t in {x[:7] for x in TOK.findall(codes or "")}:
        R[t] = R.get(t, 0) + len(parse_list(plist))
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

RAW = {
    "tech": {ch: 1000.0 * P.get(ch, 0) / N[ch] for ch in chains},
    "market": {ch: R.get(ch, 0) / N[ch] for ch in chains},
    "capital": {ch: 1000.0 * F.get(ch, 0) / N[ch] for ch in chains},
    "scale": {ch: float(N[ch]) for ch in chains},
    "policy": {ch: 1000.0 * O.get(ch, 0) / N[ch] for ch in chains},
}


def minmax(d):
    lo, hi = min(d.values()), max(d.values())
    return {k: (100.0 * (v - lo) / (hi - lo) if hi > lo else 50.0) for k, v in d.items()}


NORM = {k: minmax(v) for k, v in RAW.items()}
rows = []
for ch, nm in chains.items():
    score = sum(W[k] * NORM[k][ch] for k in W)
    rows.append({
        "chain_code": ch, "chain_name": nm,
        "dim_norm": {k: round(NORM[k][ch], 2) for k in W},
        "dim_raw": {k: round(RAW[k][ch], 4) for k in W},
        "composite_score": round(score, 2),
    })
rows.sort(key=lambda r: -r["composite_score"])
for i, r in enumerate(rows, 1):
    r["rank"] = i

payload = {
    "metric_id": "M_CHAIN_DEEP_125_1",
    "metric_name": "产业瓶颈堵点识别模型",
    "support_judgment": "部分支持",
    "base_years_used": ["2021", "2022", "2023", "2024"],
    "base_years_missing": ["2025", "2026"],
    "base_years_note": "技术维按 application_year ≤2024 截断；其余四维为存量或含 2025 事件，不摊年度序列。",
    "sources": [
        "gkx @ 183.240.141.251:3318: gkx.dwd_org_industry_tags（链成员 2,283,762 行）",
        "gkx @ 183.240.141.251:3318: gkx.dwd_patent（≤2024）",
        "gkx @ 183.240.141.251:3318: gkx.dwd_org_industry_product_tags（80,258 行）",
        "gkx @ 183.240.141.251:3318: gkx.dwd_org_financing_info（25,654 行）",
        "gkx @ 183.240.141.251:3318: gkx.dwd_policy_base（20,000 行）",
        "code/_snapshots21/：chain21_layer / region_index_patent_union / chain21_products / chain21_fin_degree / policy_base",
    ],
    "rule": {
        "weights": W,
        "normalization": "每维 12 链 min-max ×100（最小值链=0，最大值链=100）",
        "tech": "专利件数 / 成员企业数 ×1000",
        "market": "产品条目数 / 成员企业数",
        "capital": "融资事件数 / 成员企业数 ×1000",
        "scale": "成员企业数（绝对规模，直接 min-max）",
        "policy": "政策标题命中数 / 成员企业数 ×1000",
        "talent_substitution": "人才维无链级源，以 scale 替代；权重 0.20 由旧稿人才维让出",
        "pool": "与 M_CHAIN_ENTERPRISE_COUNT / M_CHAIN_BOTTLENECK_SEVERITY 同池",
    },
    "chains": rows,
    "stats": {
        "n": len(rows), "max": rows[0]["composite_score"], "min": rows[-1]["composite_score"],
        "mean": round(sum(r["composite_score"] for r in rows) / len(rows), 2),
        "median": round(sorted(r["composite_score"] for r in rows)[len(rows) // 2], 2),
        "member_sum": sum(N.values()), "member_min": min(N.values()), "member_max": max(N.values()),
    },
    "difference_vs_old_draft": {
        "old_source": "演示库 chain_bottleneck（tech_score/talent_score/market_score/capital_score/policy_score/comprehensive_score），当日 0 行",
        "old_result": "comprehensive_score = null，旧稿只能写「待模型灌数」",
        "now_result": "五维原值全部现算，综合分 12 链齐全、可排序",
        "caliber_gap": "①旧稿五维为模型输出（0—1 分），本件为强度归一分；②人才维→主体规模；③权重为本件设定（0.25/0.20/0.20/0.20/0.15），未经算法 Lead 会签（Q015 未闭合）",
        "bias": "综合分是相对分：最高链恒 100、最低链恒 min，不能跨年或跨批比较；scale 权重让大链（软件 101 万成员）天然占优",
    },
    "gaps": [
        "人才维缺失：学者/高校/科研机构都无法挂链（join 0），用企业数替代会把「人多」误当「人才强」",
        "五维之间高度相关（专利与产品、融资同向），等权/固定权会重复计分，综合分的解释力弱于单维排序",
        "min-max 对极值敏感：软件链成员数是低空经济的 186 倍，scale 归一后其余 11 链被压在 0—15 分区间",
        "旧稿模型权重未公开，本件权重不能声称与旧稿同口径",
    ],
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "elapsed_sec": round(time.time() - T0, 2),
}
json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in rows:
    print(r["rank"], r["chain_code"], r["chain_name"], r["composite_score"], r["dim_norm"])
print("wrote", OUT)
