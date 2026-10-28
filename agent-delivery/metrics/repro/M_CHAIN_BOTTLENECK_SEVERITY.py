#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_CHAIN_BOTTLENECK_SEVERITY —— 瓶颈严重度（12 链 × 四维强度缺口）

本件不读任何结果面表：gkx 内没有 chain_bottleneck（旧稿读的是演示库应用层汇总表，
见 _work_gkx21/TABLE_ABSENCE_EVIDENCE.md §chain_bottleneck），因此四维强度全部现算。

四维强度（链内标准化，均除以该链成员企业数）：
  技术 tech    = 专利件数 / 成员企业数 × 1000
  产品 product = 产品条目数 / 成员企业数
  资本 capital = 融资事件数 / 成员企业数 × 1000
  政策 policy  = 政策标题命中数 / 成员企业数 × 1000

严重度（相对指标，基线是同一批 12 条链的中位数，不做跨年/跨城归一）：
  severity(chain) = 100 × mean_over_4_dims( max(0, 1 − intensity / median_12) )
  即只在「低于中位数」的方向计缺口；高于中位数的维记 0。

阈值 60 / 40 是本件自定义（旧稿模型阈值未公开），正文已标注待甲方确认。

数据纪律：
  * 只读 code/_snapshots21/ 下落盘快照（快照由 gkx 183.240.141.251:3318 拉取）；
  * 不发任何 SQL、不连演示库、不 import 本目录以外的模块；
  * 与 M_CHAIN_DEEP_125_1 / M_CHAIN_BOTTLENECK_TYPE_DIST / M_CHAIN_ENTERPRISE_COUNT 同池。

产物：code/M_CHAIN_BOTTLENECK_SEVERITY_out.json
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
OUT = os.path.join(HERE, "M_CHAIN_BOTTLENECK_SEVERITY_out.json")
TOK = re.compile(r"INB\d+")

DIMS = ["tech", "product", "capital", "policy"]

# 每链固定 3—4 个关键词，标题包含任一即计 1 次；同一政策可被多链计（已披露）
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

# 本件自定义阈值（旧稿模型阈值未公开），正文 §2.6 已标注待甲方确认
HIGH, MID = 60.0, 40.0


def L(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def parse_list(s):
    """产品标签列是 Python 列表字面量，偶有逗号串；两种都解析。"""
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

    # 链成员：只认 7 位 INB 前缀，city 维度全部相加得到全国口径
    N = {ch: sum(v for k, v in cc.items() if k.startswith(ch + "|")) for ch in chains}
    P = {ch: sum(v for k, v in union.items() if k.startswith(ch + "|")) for ch in chains}

    # 产品条目：一行产品标签可挂多链（codes 里的 INB token），按链累加条目数
    R = {}
    for codes, _cat, _cn, plist, _nm in prods:
        items = len(parse_list(plist))
        for t in {x[:7] for x in TOK.findall(codes or "")}:
            R[t] = R.get(t, 0) + items

    # 融资事件：names 是「企业名 → 链码」字典，融资表按企业名挂链
    F = {}
    for r in fin:
        ch = names.get(r[1])
        if ch:
            F[ch] = F.get(ch, 0) + 1

    # 政策命中：标题关键词，一条政策可命中多链
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

    rows = []
    for ch, nm in chains.items():
        gaps = {k: max(0.0, 1.0 - raw[k][ch] / med[k]) if med[k] else 0.0 for k in DIMS}
        score = 100.0 * sum(gaps.values()) / len(DIMS)
        label = "高" if score >= HIGH else ("中" if score >= MID else "低")
        rows.append({
            "chain_code": ch,
            "chain_name": nm,
            "members": N[ch],
            "patents": P.get(ch, 0),
            "products": R.get(ch, 0),
            "financing_events": F.get(ch, 0),
            "policy_hits": O.get(ch, 0),
            "intensity": {k: round(raw[k][ch], 4) for k in DIMS},
            "gap_ratio": {k: round(gaps[k], 4) for k in DIMS},
            "severity_score": round(score, 2),
            "severity_label": label,
        })
    rows.sort(key=lambda r: -r["severity_score"])

    sev = [r["severity_score"] for r in rows]
    payload = {
        "metric_id": "M_CHAIN_BOTTLENECK_SEVERITY",
        "metric_name": "瓶颈严重度",
        "support_judgment": "部分支持",
        "judgment_reason": (
            "四维强度（技术/产品/资本/政策）在本件全部现算、12 条链全部非空，"
            "但旧稿口径的第五维「人才」在 gkx 无链级源：dwd_scholar 的 scholar_org_id "
            "整列为空（0/21,316），学者与高校/院所都无法挂到产业链节点上，"
            "因此只能用产品维顶替，维数从 5 降到 4；同时严重度是中位数相对量、"
            "阈值 60/40 为本件自定义，未经甲方会签。缺一维 + 阈值未会签 = 部分支持，不抬档。"
        ),
        "verdict_kind": "computed_with_declared_gap",
        "base_years_used": ["2021", "2022", "2023", "2024"],
        "base_years_missing": ["2025", "2026"],
        "base_years_note": (
            "专利维按 application_year ≤2024 截断（2025—2026 公开不全）；"
            "产品/融资/政策三维为存量或含 2025 事件，无年度窗口，故不摊年度序列。"
        ),
        "sources": [
            "gkx @ 183.240.141.251:3318: gkx.dwd_org_industry_tags（链成员）",
            "gkx @ 183.240.141.251:3318: gkx.dwd_patent（专利件数，≤2024）",
            "gkx @ 183.240.141.251:3318: gkx.dwd_org_industry_product_tags（80,258 行）",
            "gkx @ 183.240.141.251:3318: gkx.dwd_org_financing_info（25,654 行）",
            "gkx @ 183.240.141.251:3318: gkx.dwd_policy_base（20,000 行标题）",
            "code/_snapshots21/：chain21_layer / region_index_patent_union / "
            "chain21_products / chain21_fin_degree / policy_base",
        ],
        "rule": {
            "dims": ["技术（专利/企业）", "产品（产品条目/企业）",
                     "资本（融资事件/企业）", "政策（标题命中/企业）"],
            "baseline": "12 链强度中位数，不做跨年/跨城归一",
            "severity": "100 × mean(max(0, 1 − intensity/median))，四维等权；高于中位数记 0",
            "label": "≥60 高 / 40—60 中 / <40 低（阈值写死，不随样本调；本件自定义、待甲方确认）",
            "policy_hits": "每条链固定 3—4 个关键词，标题包含任一即计 1 次；同一政策可被多链计",
        },
        "medians": {k: round(med[k], 6) for k in DIMS},
        "pool_atoms": {
            "tags_rows": layer.get("rows"),
            "multi_chain_rows": layer.get("multi_chain_rows"),
            "bad_code_rows": layer.get("bad_code_rows"),
            "member_sum": sum(N.values()),
        },
        "chains": rows,
        "stats": {
            "n": len(rows),
            "max": max(sev),
            "min": min(sev),
            "mean": round(sum(sev) / len(sev), 2),
            "n_high": sum(1 for r in rows if r["severity_label"] == "高"),
            "n_mid": sum(1 for r in rows if r["severity_label"] == "中"),
            "n_low": sum(1 for r in rows if r["severity_label"] == "低"),
        },
        "difference_vs_old_draft": {
            "old_source": "演示库汇总层 chain_bottleneck（五维得分 + 综合分），当日 0 行，旧稿只能写「无数据」",
            "old_result": "severity_score = null，双字段同返待模型灌数",
            "now_result": "四维强度现算，严重度 12 链全部非空（min/max/mean 见 stats）",
            "caliber_gap": "旧稿五维含「人才维」，gkx 无链级人才源（学者不可挂链），本件以产品维替代人才维；"
                           "权重从旧稿未公开的模型权重改为四维等权",
            "bias": "等权 + 中位数基线会放大「小链」的严重度（低空经济 5,450 家企业但政策/融资命中少），"
                    "读数时应结合 members 列看绝对规模",
        },
        "gaps": [
            "政策维用标题关键词，不读正文；一条政策可同时命中多链，O 之和大于政策总数",
            "专利维只认第一申请人，链内企业作为共同申请人时漏计",
            "融资口径是「企业发生过融资事件」，不区分金额与轮次；未融资不等于缺资本",
            "严重度是相对指标：全批 12 链都强时仍会有一半链被判「高于中位数」，不能跨批比较",
            "人才维缺失：学者/高校/院所无法挂链（scholar_org_id 非空 0 行），"
            "产品维只是替代，不能读作「人才瓶颈」",
            "阈值 60/40 与四维等权均为本件自定义，未会签；换阈值会改变高/中/低分布",
        ],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - T0, 2),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("[ok] %s medians=%s" % (payload["metric_id"],
                                  {k: round(v, 4) for k, v in med.items()}))
    for r in rows:
        print("  %-10s %-8s %6.2f %s  (%s)" % (r["chain_code"], r["chain_name"],
                                               r["severity_score"], r["severity_label"],
                                               ", ".join("%s=%.4f" % (k, r["gap_ratio"][k])
                                                         for k in DIMS)))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
