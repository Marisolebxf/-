#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_DEEP_127_1 —— 深圳问题识别模型（问题项计数）

旧稿读 chain_sz_problem(chain_id, chain_name, problem_count)，当日 0 行。
本件把「问题项」定义为可枚举的判定：
  对每条链，比较「深圳强度」与「全国该链强度」，五个判定位逐位判：
    P1 技术：深圳专利/深圳成员 < 全国专利/全国成员
    P2 产品：深圳产品条目/深圳成员 < 全国产品条目/全国成员
    P3 资本：深圳融资事件/深圳成员 < 全国融资/全国成员
    P4 政策：深圳可适用政策命中/深圳成员 < 全国政策命中/全国成员
    P5 配套：深圳产业链完整度 < 90%（节点覆盖率绝对线，链树节点口径）
  命中即 1 个问题项，problem_count ∈ [0,5]。
「问题项」是链 × 判定位的布尔计数，不是企业数；5 条判定位固定，可逐位复核。
"""
from __future__ import annotations
import ast, json, os, re, time

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_CHAIN_DEEP_127_1_out.json")
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
cov = L("chain21_sz_nodecov_20261022.json")["chains"]

N = {ch: sum(v for k, v in cc.items() if k.startswith(ch + "|")) for ch in chains}
NS = {ch: cc.get(ch + "|深圳市", 0) for ch in chains}
P = {ch: sum(v for k, v in union.items() if k.startswith(ch + "|")) for ch in chains}
PS = {ch: union.get(ch + "|深圳市", 0) for ch in chains}
R = {}
RS = {}
for codes, cat, cn, plist, nm in prods:
    items = len(parse_list(plist))
    is_sz = (nm or "").strip()[2:6] == "4403"
    for t in {x[:7] for x in TOK.findall(codes or "")}:
        R[t] = R.get(t, 0) + items
        if is_sz:
            RS[t] = RS.get(t, 0) + items
F = {}
FS = {}
for r in fin:
    ch = names.get(r[1])
    if not ch:
        continue
    F[ch] = F.get(ch, 0) + 1
    if (r[2] or "").strip()[2:6] == "4403":
        FS[ch] = FS.get(ch, 0) + 1
O = {ch: 0 for ch in chains}
OS = {ch: 0 for ch in chains}
for p in policy:
    t = p.get("title") or ""
    city = (p.get("city") or "").strip()
    prov = (p.get("province") or "").strip()
    sz_ok = ("深圳" in city) or ("深圳" in t) or prov == "广东省" or p.get("level") == 1
    for ch, kws in KW.items():
        if any(k in t for k in kws):
            O[ch] += 1
            if sz_ok:
                OS[ch] += 1

rows = []
for ch, nm in chains.items():
    nat = {"tech": 1000.0 * P[ch] / N[ch], "product": R.get(ch, 0) / N[ch],
           "capital": 1000.0 * F.get(ch, 0) / N[ch], "policy": 1000.0 * O[ch] / N[ch]}
    sz = {"tech": 1000.0 * PS[ch] / NS[ch] if NS[ch] else 0.0,
          "product": RS.get(ch, 0) / NS[ch] if NS[ch] else 0.0,
          "capital": 1000.0 * FS.get(ch, 0) / NS[ch] if NS[ch] else 0.0,
          "policy": 1000.0 * OS[ch] / NS[ch] if NS[ch] else 0.0}
    comp = 100.0 * cov[ch]["k_covered"] / cov[ch]["K_nodes"] if cov.get(ch) else 0.0
    hit = [k for k in nat if sz[k] < nat[k]]
    if comp < 90.0:
        hit.append("completeness")
    rows.append({
        "chain_code": ch, "chain_name": nm,
        "sz_members": NS[ch], "national_members": N[ch],
        "sz_intensity": {k: round(v, 4) for k, v in sz.items()},
        "national_intensity": {k: round(v, 4) for k, v in nat.items()},
        "sz_completeness_pct": round(comp, 2),
        "problems": hit, "problem_count": len(hit),
    })
rows.sort(key=lambda r: -r["problem_count"])

payload = {
    "metric_id": "M_CHAIN_DEEP_127_1",
    "metric_name": "深圳问题识别模型",
    "support_judgment": "部分支持",
    "base_years_used": ["2021", "2022", "2023", "2024"],
    "base_years_missing": ["2025", "2026"],
    "base_years_note": "技术维按 application_year ≤2024 截断；产品/融资/政策/完整度四维无年度窗口，故为截面问题清单，不做年度对比。",
    "sources": [
        "gkx @ 183.240.141.251:3318: gkx.dwd_org_industry_tags / dwd_patent / dwd_org_industry_product_tags / dwd_org_financing_info / dwd_policy_base / dwd_industry_chain_info",
        "code/_snapshots21/chain21_layer_20261022.json（链成员、深圳成员，同池）",
        "code/_snapshots21/region_index_patent_union.json、chain21_products_20261022.json、chain21_fin_degree_20261022.json、chain21_sz_nodecov_20261022.json",
    ],
    "rule": {
        "P1": "深圳专利/深圳成员 < 全国专利/全国成员",
        "P2": "深圳产品条目/深圳成员 < 全国产品条目/全国成员",
        "P3": "深圳融资事件/深圳成员 < 全国融资/全国成员",
        "P4": "深圳可适用政策命中/深圳成员 < 全国政策命中/全国成员",
        "P5": "深圳产业链完整度 < 90%（节点覆盖，与 M_CHAIN_SZ_COMPLETENESS 同一快照）",
        "sz_scope": "credit_code[2:6]='4403'；深圳可适用政策 = 政策 city 含深圳 / 标题含深圳 / 省级广东 / 国家级",
        "count": "problem_count = 命中判定位数，0—5；一链一值，可逐位复核",
    },
    "chains": rows,
    "stats": {
        "n": len(rows), "total_problems": sum(r["problem_count"] for r in rows),
        "slots": len(rows) * 5,
        "max": rows[0]["problem_count"], "min": rows[-1]["problem_count"],
        "mean": round(sum(r["problem_count"] for r in rows) / len(rows), 2),
        "by_dim": {k: sum(1 for r in rows if k in r["problems"])
                   for k in ["tech", "product", "capital", "policy", "completeness"]},
        "pool_atoms": {"product_rows": len(prods), "fin_rows": len(fin), "policy_rows": len(policy)},
    },
    "difference_vs_old_draft": {
        "old_source": "演示库 chain_sz_problem(chain_id, chain_name, problem_count)，当日 0 行",
        "old_result": "problem_count = null，旧稿写「问题项表未灌数」",
        "now_result": "12 链 × 5 判定位现算，问题项总数与逐链清单见 chains",
        "caliber_gap": "旧表的 problem_count 由外部模型给出（问题定义未公开），本件用「深圳 vs 全国强度差 + 完整度绝对线」重定义，数值不可与旧表逐行对号",
        "bias": "深圳成员少（低空经济 263 家）时强度比噪声大，容易把小样本波动判成问题；建议与 sz_members 列同看",
    },
    "gaps": [
        "「问题」是相对强度差，不是专家认定的堵点；某链深圳全面强于全国时 problem_count=0，不等于无堵点",
        "P4 政策命中用标题关键词 + 适用性代理（省级/国家级视为可适用），会把不针对深圳的省级政策算进来",
        "P5 完整度阈值 90% 是绝对线，与 P1—P4 的相对比较不同源，混在同一计数里需在读数时分开",
        "深圳成员数最小 263 家（低空经济），强度比的分母小，单链结论不稳",
    ],
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "elapsed_sec": round(time.time() - T0, 2),
}
json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("stats", payload["stats"])
for r in rows:
    print(r["chain_code"], r["chain_name"], r["problem_count"], r["problems"])
print("wrote", OUT)
