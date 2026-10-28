#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_PAINPOINT_TOPIC · 痛点主题（gkx 单库代理版）

定义
----
把企业痛点归到可读的主题上，供企业画像「痛点标签」与筛选器使用。
旧稿的主题来自 `enterprise_diagnosis.pain_point` 字段（诊断模型的输出），
该结果面在 gkx 不存在（source_absent，见 TABLE_ABSENCE_EVIDENCE §enterprise_diagnosis）。

本件的主题构造
--------------
不训练模型、不做文本聚类，只用**结构化原因字段**做确定性归类：
  1) 经营异常表的 abn_reason 原文 → 四类：住所失联 / 年报未公示 / 信息隐瞒 / 无照经营
  2) 失信与被执行 → 债务违约
  3) 行政处罚 → 行政违规
  4) 严重违法 → 严重违法
  5) 税务处罚 → 涉税违规
每条主题都带「原始条数 / 占全部痛点比例 / 涉及企业数」，可逐条对回原始表。
这样得到的是**规则主题**，不是语义主题：它不做「融资受阻」「人才流失」这类推断。

输出：code/M_ENT_PAINPOINT_TOPIC_out.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_ENT_PAINPOINT_TOPIC_out.json"
METRIC = "M_ENT_PAINPOINT_TOPIC"

SRC_LABEL = {"abnormal": "经营异常", "illegal": "严重违法", "punish": "行政处罚",
             "shixin": "失信被执行", "zhixing": "被执行人", "tax_punish": "税务处罚"}


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def abn_topic(reason: str) -> str:
    r = reason or ""
    if "无法联系" in r or "无法取得联系" in r:
        return "住所失联"
    if "年度报告" in r or "年报" in r:
        return "年报未公示"
    if "隐瞒" in r or "弄虚作假" in r:
        return "信息隐瞒"
    if "未在登记" in r or "未在登记所" in r:
        return "无照经营"
    return "其他经营异常"


def main() -> None:
    agg = {SRC_LABEL[r[0]]: {"records": r[1], "orgs": r[2]}
           for r in load("pain_risk_counts_20261022.json")["rows"]}

    topics = defaultdict(lambda: {"records": 0, "orgs": 0, "sources": []})
    total = sum(v["records"] for v in agg.values())

    # 经营异常按 abn_reason 拆四类；orgs 无法在 reason 层去重，按记录占比分摊并标注
    pt = load("pain_topics_20261022.json")
    abn_total = agg["经营异常"]["records"]
    abn_orgs = agg["经营异常"]["orgs"]
    abn_rows = pt["abn_reason"]["rows"] if pt.get("abn_reason", {}).get("ok") else []
    reason_agg = defaultdict(int)
    for reason, n in abn_rows:
        reason_agg[abn_topic(reason)] += n
    covered = sum(reason_agg.values())
    for topic, n in reason_agg.items():
        est_orgs = round(abn_orgs * n / covered) if covered else 0
        topics[topic]["records"] += n
        topics[topic]["orgs"] += est_orgs
        topics[topic]["sources"].append(f"dwd_org_company_abnormal.abn_reason({n} 条，"
                                        f"占异常记录 {n / abn_total:.1%})")

    direct = {
        "失信被执行": "债务违约",
        "被执行人": "债务违约",
        "行政处罚": "行政违规",
        "严重违法": "严重违法",
        "税务处罚": "涉税违规",
    }
    assigned = covered
    for src, topic in direct.items():
        topics[topic]["records"] += agg[src]["records"]
        topics[topic]["orgs"] += agg[src]["orgs"]
        topics[topic]["sources"].append(f"{src}({agg[src]['records']} 条 / {agg[src]['orgs']} 家)")
        assigned += agg[src]["records"]
    if abn_total > covered:
        rest = abn_total - covered
        topics["其他经营异常"]["records"] += rest
        topics["其他经营异常"]["sources"].append(f"abn_reason 未覆盖部分({rest} 条)")

    rows = [{"topic": k, "records": v["records"],
             "share": round(v["records"] / total, 4),
             "orgs": v["orgs"], "sources": v["sources"]}
            for k, v in topics.items()]
    rows.sort(key=lambda r: -r["records"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    out = {
        "metric_id": METRIC,
        "metric_name": "痛点主题",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）+ code/_snapshots21/ 落盘快照",
        "formula": "topic = f(风险表, 结构化原因字段)；records = Σ 命中条数；share = 该主题条数 / 全部痛点条数",
        "blocking_tables": {
            "enterprise_diagnosis": {
                "triage": "source_absent",
                "evidence": "_work_gkx21/TABLE_ABSENCE_EVIDENCE.md §enterprise_diagnosis",
            }
        },
        "proxy_path": "六张风险表 + abn_reason 关键词四分类 → 规则主题",
        "proxy_deviation": "主题是规则归类不是语义聚类：只有合规/司法/行政侧主题，没有「融资受阻、人才流失、供应链断供」这类经营痛点；abn_reason 的主题企业数按记录占比分摊（原因字段无 org 去重），标注为估算值；一条记录只归一个主题，不做多标签；「涉及企业数」是各源表 orgs 直接相加，跨表未去重（同一家企业既失信又被执行会被计两次），只作量级参考",
        "taxonomy": {
            "level": "规则主题（确定性）",
            "topics": [r["topic"] for r in rows],
            "not_covered": ["融资受阻", "人才流失", "供应链断供", "产能利用率低", "价格战"],
        },
        "totals": {"records": total, "topics": len(rows),
                   "by_source": agg},
        "topics": rows,
        "support_judgment": {
            "data_support_level": "部分支持",
            "reason": "痛点诊断结果面不存在，但主题构造所需的结构化原因字段在库内是真实的：经营异常 5,862 条带 abn_reason 原文（可拆四类），失信 76,035、被执行 550,334、处罚 65,997、严重违法 247、税务处罚 528 都能直接映射主题，合计 69.9 万条。规则主题可复现、可对回原始记录，故判部分支持；缺少经营侧痛点与语义主题，主题体系只覆盖合规侧。",
            "criteria": {
                "result_table_exists": False,
                "records": total,
                "topics": len(rows),
                "semantic_model_used": False,
                "proxy_used": True,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "风险表是事件流水，本件按「截至抓取时点的累计条数」归类，不做年度切分，故无基期年份；表内带发生日期，年度主题迁移需另做按年聚合。",
        "sources": [
            {"path": "code/_snapshots21/pain_risk_counts_20261022.json",
             "table": "gkx 六张风险表", "rows": 699003, "role": "主题条数与涉及企业数"},
            {"path": "code/_snapshots21/pain_topics_20261022.json",
             "table": "gkx.dwd_org_company_abnormal", "rows": 15,
             "role": "abn_reason 前 15 类原文与条数"},
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] {METRIC} -> {OUT.name} topics={len(rows)} records={total}")
    for r in rows:
        print(f"  #{r['rank']} {r['topic']:<10} {r['records']:<7} share={r['share']} orgs≈{r['orgs']}")


if __name__ == "__main__":
    main()
