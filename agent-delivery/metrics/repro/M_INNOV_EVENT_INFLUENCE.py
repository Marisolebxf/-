#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_INNOV_EVENT_INFLUENCE · 事件影响力（20261021 换源版）

旧稿公式（照抄，王惠 20260904）
------------------------------
influence = 0.45×媒体层级 + 0.35×央媒报道量 + 0.20×周内报道跨度（均 0—1 归一后 ×100）。

换源结论：**完全不支持，只写需求**
--------------------------------
1. `gkx.dwd_event` 只有 20 行会议公告，无事件 id / 无报道 / 无媒体源，见
   `M_INNOV_DS_01_EVENTS_003` 的同批取证。
2. `dwd_industry_chain_news_info` 有 108,052 条资讯、206 个 source，但**没有 event_id、
   没有事件簇 id、没有媒体层级**；只有标题/日期/来源。要得到「一个事件的报道集合」，
   必须先做跨源事件聚类（旧稿用标题相似度把 108,072 条聚成 6,406 簇），
   这是**本件未获授权、也未验收的模型**，不能把聚类结果当事件真值。
3. 媒体层级表不存在：206 个 source 只有名称，没有央媒/全国/行业/地方的权威度标注。
   用称谓规则硬分级属于人工规则，不是库内数据。
4. 注意：旧稿上游 `dwd_policy_base` 的 rank/theme 在本库也不可用（rank 不存在、
   theme 全 0），政策代理同样不成立。

按本批规则：没有事件流就判完全不支持，不许用新闻串伪事件。
本件只输出需求规格、字段缺口与修复路径，不产出任何影响力分值。

输出：`code/M_INNOV_EVENT_INFLUENCE_out.json`
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVENT = HERE / "_snapshots21" / "event21_probe_20261022.json"
NEWS = HERE / "_snapshots21" / "news21_chain_items_20261022.json"
INV = HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json"
OUT = HERE / "M_INNOV_EVENT_INFLUENCE_out.json"
METRIC = "M_INNOV_EVENT_INFLUENCE"
NAME = "事件影响力"

REQUIRED = [
    ("event_id", "事件簇主键（跨源聚类后）"),
    ("report_id", "单条报道主键"),
    ("source_name", "媒体源名称"),
    ("source_tier", "媒体层级（央媒/全国/行业/地方）"),
    ("publish_time", "报道发布时间（精确到小时）"),
    ("is_central", "是否央媒（0/1，可由 source_tier 派生）"),
    ("event_time", "事件首发时间（算周内跨度）"),
    ("dedup_key", "同源转载去重键（标题指纹/URL 规范）"),
]


def main() -> None:
    ev = json.loads(EVENT.read_text(encoding="utf-8"))
    news = json.loads(NEWS.read_text(encoding="utf-8"))
    inv = json.loads(INV.read_text(encoding="utf-8"))
    rows = news["rows"]
    src = Counter(r[5] for r in rows)
    cols = news["meta"]["columns"]
    dates = sorted({r[4] for r in rows})
    event_cols = [c[0] for c in ev["meta"]["columns"]]
    has_news = {k: (k in cols) for k, _ in REQUIRED}
    event_tables = {k: v for k, v in inv.items() if "event" in k.lower()}

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": (
            "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）：dwd_event 20 行 + "
            "dwd_industry_chain_news_info 108,052 行"
        ),
        "formula": "0.45×媒体层级 + 0.35×央媒报道量 + 0.20×周内报道跨度；本件因事件簇缺失不执行",
        "verdict": "完全不支持",
        "event_table": {"rows": ev["meta"]["rows"], "columns": event_cols,
                        "dates": sorted({r["start_date"] for r in ev["rows"] if r["start_date"]})},
        "news_table": {
            "rows": len(rows), "columns": cols,
            "date_min": dates[0], "date_max": dates[-1],
            "distinct_sources": len(src),
            "top_sources": src.most_common(10),
            "has_event_id": "event_id" in cols,
            "has_cluster_id": any("cluster" in c.lower() for c in cols),
        },
        "field_audit": {
            "required": [{"field": k, "purpose": v, "exists_in_news": has_news[k]}
                         for k, v in REQUIRED],
            "n_required": len(REQUIRED),
            "n_present_in_news": sum(1 for v in has_news.values() if v),
            "available_proxies": {
                "source_name": "有（206 个，仅名称）",
                "publish_time": "有（日期，无小时）",
                "title": "有（可做聚类输入，但聚类未验收）",
                "source_tier": "无",
                "event_id": "无",
                "report_id": "有 pk_id 行号，不是报道业务 id",
            },
            "blocking_gaps": ["event_id", "source_tier", "is_central", "dedup_key", "event_time"],
        },
        "clustering_boundary": {
            "old_approach": "标题归一 + 相似度阈值，把 108,072 条聚成 6,406 簇",
            "why_rejected": (
                "聚类是模型产物，不是库内事件真值；阈值一变簇数与影响力全变，"
                "且没有人工标注集做准召评估。用未验收的簇冒充事件，会把"
                "「同题转载」与「同一事件」混为一谈。"
            ),
            "would_need": ["人工标注 500 对报道", "准召 ≥0.9", "簇 id 落表并版本化"],
        },
        "requirements": {
            "grain": "一行 = 一个事件簇；报道明细单独一张表",
            "tables": [
                {"name": "dwd_event_cluster", "fields": ["event_id", "event_time", "title",
                                                          "chain_id", "event_type", "status", "updated_at"]},
                {"name": "dwd_event_report", "fields": ["report_id", "event_id", "source_name",
                                                         "source_tier", "publish_time", "url", "title"]},
                {"name": "dim_media_tier", "fields": ["source_name", "tier", "is_central", "weight"]},
            ],
            "derived": [
                {"field": "media_tier_score", "formula": "Σ(报道 tier 权重)/报道数，归一到 0—1"},
                {"field": "central_count_norm", "formula": "央媒报道数 / 该事件报道数"},
                {"field": "span_days_norm", "formula": "min(1, (末次报道−首次报道)/7 天)"},
                {"field": "influence", "formula": "100×(0.45×tier + 0.35×central + 0.20×span)"},
            ],
            "acceptance": [
                "每个事件至少 2 条报道、至少 1 个可回溯 URL",
                "媒体层级表覆盖率 ≥90% 的报道量",
                "跨源转载去重后，单事件重复率 <5%",
                "影响力分布不得 90% 集中在同一档",
            ],
        },
        "remediation": [
            {"step": 1, "action": "先做事件聚类并人工验收（准召≥0.9），落 event_cluster", "owner": "算法", "blocking": True},
            {"step": 2, "action": "建媒体层级维表（206 源全量标注 tier/is_central）", "owner": "数据治理", "blocking": True},
            {"step": 3, "action": "把报道明细落 event_report，保留 publish_time 到小时", "owner": "数据接入", "blocking": True},
            {"step": 4, "action": "按 0.45/0.35/0.20 合成 influence 并版本化", "owner": "算法", "blocking": False},
        ],
        "support_judgment": {
            "data_support_level": "完全不支持",
            "reason": (
                f"事件表只有 {ev['meta']['rows']} 行会议公告，无报道明细；"
                f"资讯表虽有 {len(rows):,} 条、{len(src)} 个源，但没有 event_id/簇 id/媒体层级，"
                f"{len(REQUIRED)} 个必需字段里资讯表原样只有 {sum(1 for v in has_news.values() if v)} 个；"
                "要算影响力必须先聚类并建媒体层级表，两者都不存在或未验收。"
                "旧稿用新闻聚类 + 称谓规则硬分级，属于模型/人工假设，不是库内事件数据；"
                "本批规则禁止用新闻串伪事件，故判完全不支持。"
            ),
            "criteria": {
                "event_table_rows": ev["meta"]["rows"],
                "news_rows": len(rows),
                "distinct_sources": len(src),
                "event_id_in_news": False,
                "media_tier_table": False,
                "clustering_validated": False,
                "policy_proxy_used": False,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "事件表只有 2026-05-13/14 两天；资讯表覆盖 2025-02—2026-07，但没有事件簇，"
            "不能形成年度事件序列。used/missing 为空表示无年度基期，不是缺年补 0。"
        ),
        "sources": [
            {"path": "code/_snapshots21/event21_probe_20261022.json", "table": "gkx.dwd_event",
             "rows": ev["meta"]["rows"], "role": "事件表全量取证"},
            {"path": "code/_snapshots21/news21_chain_items_20261022.json",
             "table": "gkx.dwd_industry_chain_news_info", "rows": len(rows), "role": "报道明细（无事件簇）"},
            {"path": "_work_gkx21/GKX_INVENTORY.json", "role": "280 张表清单"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("event rows", ev["meta"]["rows"], "news rows", len(rows), "sources", len(src),
          "news fields", sum(1 for v in has_news.values() if v))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
