#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_DS_01_EVENTS_003 · 重要性等级（20261021 换源版）

旧稿公式（照抄）
----------------
综合分 = 0.5×关注度 + 0.5×影响力；≥P70 高、≤P30 低、其余中（样本<20 用 70/40 分位）。

换源结论：**完全不支持，只写需求**
--------------------------------
`gkx.dwd_event` 确实存在，但它是**会议/论坛名录**，不是事件流：
  - 20 行、15 列，全部是 2026-05-13/14 两天的医药论坛公告；
  - 字段只有 event_name / organizer / start_date / end_date / event_url；
  - 没有 event_id 之外的稳定主键语义、没有 chain_id、没有关注度、没有影响力、
    没有报道量、没有媒体源、没有事件状态、没有更新时间；
  - 全库 280 张表里带 event 的只有 `dwd_event` 与 `dwd_merger_acquisition_events_party_info`
    （并购当事方，不是科创事件），不存在事件簇/事件结果面。
按本批规则：没有事件表就判完全不支持，**不许用新闻或政策串成伪事件**。
旧稿用 `dwd_policy_base` 20,000 条政策当事件代理，本件明确拒绝。

输出：`code/M_INNOV_DS_01_EVENTS_003_out.json`
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
EVENT = HERE / "_snapshots21" / "event21_probe_20261022.json"
INV = HERE.parent / "_work_gkx21" / "GKX_INVENTORY.json"
OUT = HERE / "M_INNOV_DS_01_EVENTS_003_out.json"
METRIC = "M_INNOV_DS_01_EVENTS_003"
NAME = "重要性等级"

REQUIRED = [
    ("event_id", "事件稳定主键（跨源去重后）"),
    ("event_time", "事件发生/首发时间，精确到日"),
    ("chain_id", "所属产业链（12 条顶层链之一，可多值）"),
    ("event_type", "事件类型（融资/并购/新品/政策/专利/人事…）"),
    ("attention_score", "关注度 0—100（报道量、搜索量、互动量合成）"),
    ("influence_score", "影响力 0—100（媒体层级、覆盖范围、持续时长合成）"),
    ("event_status", "事件状态（萌芽/发酵/消退），用于实时更新"),
    ("updated_at", "等级最近重算时间"),
    ("report_count", "报道条数（关注度的最小可核验原子）"),
    ("source_list", "报道源列表（影响力的最小可核验原子）"),
]


def main() -> None:
    ev = json.loads(EVENT.read_text(encoding="utf-8"))
    inv = json.loads(INV.read_text(encoding="utf-8"))
    rows = ev["rows"]
    cols = [c[0] for c in ev["meta"]["columns"]]
    dates = sorted({r["start_date"] for r in rows if r["start_date"]})
    domains = Counter(urlparse(r["event_url"]).netloc for r in rows if r["event_url"])
    organizers = Counter(r["organizer"] for r in rows)
    names = [r["event_name"] for r in rows]

    has = {k: (k in cols) for k, _ in REQUIRED}
    # 语义等价的兜底判断：event_name 可当 event_id 的弱替代，date 可当 event_time
    semantic = {
        "event_id": "dwd_id（自增行号，不是业务事件 id）",
        "event_time": "start_date（仅会议开始日）",
        "chain_id": None,
        "event_type": None,
        "attention_score": None,
        "influence_score": None,
        "event_status": None,
        "updated_at": "updated_time（行更新时间，不是事件状态更新时间）",
        "report_count": None,
        "source_list": "event_url（单条官网链接，不是报道源列表）",
    }
    event_tables = {
        k: v for k, v in inv.items()
        if "event" in k.lower() or "events" in k.lower()
    }

    report = {
        "metric_id": METRIC,
        "metric_name": NAME,
        "date": "2026-10-22",
        "data_source": "gkx @ 183.240.141.251:3318（只读 gkx_reader_zp）/ dwd_event 全表 20 行",
        "formula": "0.5×关注度 + 0.5×影响力；P70/P30 三档；本件因输入不存在，不执行",
        "verdict": "完全不支持",
        "context_news_rows": 108052,
        "tested_tables": event_tables,
        "event_probe": {
            "rows": ev["meta"]["rows"],
            "columns": cols,
            "n_columns": len(cols),
            "date_min": dates[0] if dates else None,
            "date_max": dates[-1] if dates else None,
            "distinct_dates": dates,
            "distinct_names": len(set(names)),
            "distinct_organizers": len(organizers),
            "top_organizers": organizers.most_common(5),
            "url_domains": domains.most_common(10),
            "sample": rows[:5],
        },
        "field_audit": {
            "required": [{"field": k, "purpose": v, "exists": has[k],
                          "semantic_substitute": semantic[k]} for k, v in REQUIRED],
            "n_required": len(REQUIRED),
            "n_exists": sum(1 for v in has.values() if v),
            "n_semantically_usable": 2,
            "hard_missing": ["chain_id", "event_type", "attention_score",
                             "influence_score", "event_status", "report_count", "source_list"],
        },
        "why_not_proxy": (
            "旧稿用 dwd_policy_base 的 20,000 条政策当事件代理，并用主题/引用/区域字段合成"
            "关注度与影响力。政策不是事件：没有发生时间线、没有传播过程、没有事件状态；"
            "本批规则明确禁止用新闻/政策串伪事件，故本件不产出任何等级。"
        ),
        "requirements": {
            "grain": "一行 = 一个去重后的科创事件（跨媒体报道聚类后）",
            "minimum_rows": 20000,
            "refresh": "日更；事件状态变化时增量重算",
            "fields": [{"field": k, "purpose": v} for k, v in REQUIRED],
            "derived": [
                {"field": "importance_score", "formula": "0.5×attention_score + 0.5×influence_score"},
                {"field": "importance_level", "formula": "≥P70 高；≤P30 低；其余中（样本<20 用 P70/P40）"},
            ],
            "acceptance": [
                "每个事件至少有 1 条可回溯报道 URL 与 1 个媒体源",
                "attention/influence 均有 0—100 标度说明与版本号",
                "同一事件跨源重复报道必须聚为一行，重复率 <5%",
                "等级分布不得出现单一档位 >60%",
            ],
        },
        "remediation": [
            {"step": 1, "action": "接入事件流（新闻聚类/招标/融资/专利/政策五源），建 event 主表",
             "owner": "数据接入", "blocking": True},
            {"step": 2, "action": "建媒体源层级表（央媒/全国/行业/地方），给 influence 提供权威度",
             "owner": "数据治理", "blocking": True},
            {"step": 3, "action": "跑关注度/影响力两件上游，落 0—100 分与版本号", "owner": "算法", "blocking": True},
            {"step": 4, "action": "按 P70/P30 切档，输出 importance_level 与重算时间", "owner": "算法", "blocking": False},
        ],
        "support_judgment": {
            "data_support_level": "完全不支持",
            "reason": (
                f"dwd_event 只有 {ev['meta']['rows']} 行、{len(cols)} 列，"
                f"日期仅 {dates[0] if dates else '—'} 至 {dates[-1] if dates else '—'}，"
                "内容是医药论坛名录，不是科创事件流；"
                f"{len(REQUIRED)} 个必需字段里原样存在的只有 {sum(1 for v in has.values() if v)} 个，"
                "chain_id/事件类型/关注度/影响力/事件状态/报道量/报道源全部缺失；"
                "全库没有事件簇表或事件结果面。没有输入就不能合成等级，"
                "用政策或新闻代理会伪造事件语义，故判完全不支持。"
            ),
            "criteria": {
                "event_table_exists": True,
                "event_table_is_stream": False,
                "rows": ev["meta"]["rows"],
                "required_fields": len(REQUIRED),
                "fields_present": sum(1 for v in has.values() if v),
                "upstream_attention_exists": False,
                "upstream_influence_exists": False,
                "policy_proxy_used": False,
            },
        },
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "事件表只有 2026-05-13/14 两天，且不是年度序列；本指标没有可用的年度基期。"
            "used/missing 为空不是「缺年补 0」，而是事件流本身不存在。"
        ),
        "sources": [
            {"path": "code/_snapshots21/event21_probe_20261022.json",
             "table": "gkx.dwd_event", "rows": ev["meta"]["rows"], "role": "事件表全量取证"},
            {"path": "_work_gkx21/GKX_INVENTORY.json", "role": "280 张表清单，确认无事件簇表"},
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("rows", ev["meta"]["rows"], "cols", len(cols), "dates", dates,
          "fields", sum(1 for v in has.values() if v))
    print("event tables", event_tables)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
