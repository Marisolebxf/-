#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_PLAN_TALENT_FLOW · 科技人才流动（产业界↔学术界）（判：部分支持）

口径真源：`metrics/calc-logic/INNOV/M_INNOV_PLAN_TALENT_FLOW.md`（V1.5-20260901）
对象=学者；按工作经历相邻两段的「任职性质」变化识别跨界流动；两类方向分别计
去重学者数；近窗 vs 基线的 burst 定预警等级。

数据：`dwd_scholar`（21,316）+ `dwd_scholar_work_experience`（57,117）+
`dwd_scholar_talent_flag`（20,030）+ 企业底册（189,116，本地 JSON）。
SQL 2 条（工作经历全量窄列、院士名单），其余零 DB。

运行：python3 code/M_INNOV_PLAN_TALENT_FLOW.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _tail21_common as T  # noqa: E402
from _gkxdb import gkx  # noqa: E402

MID = "M_INNOV_PLAN_TALENT_FLOW"

ACAD_CN = ("大学", "学院", "学校", "中学", "研究院", "研究所", "科学院", "研究中心",
           "实验室", "医院", "疾控中心", "图书馆", "博物馆")
IND_CN = ("有限公司", "股份", "集团", "公司", "厂", "企业", "事务所", "银行", "证券")
ACAD_EN = ("university", "college", "institute", "academy", "school", "hospital",
           "research center", "research centre", "laborator", "polytechnic", "inserm",
           "cnrs", "nih", "medical center", "medical centre")
IND_EN = ("ltd", "inc", "llc", "gmbh", "corp", "co.,", "company", "plc", "k.k", "s.a.",
          "b.v", "ag", "oy", "pte", "limited")
ACAD_IND_L1 = ("教育", "研究和试验发展", "科学研究和技术服务业")


def classify(zh: str, en: str, ind_map: dict[str, str]) -> tuple[str | None, str]:
    nm = (zh or "").strip() or (en or "").strip()
    if not nm:
        return None, nm
    l1 = ind_map.get(nm)
    if l1:
        if any(k in l1 for k in ACAD_IND_L1):
            return "A", nm
        if any(k in nm for k in ACAD_CN):
            return "A", nm
        return "I", nm
    if any(k in nm for k in ACAD_CN):
        return "A", nm
    low = nm.lower()
    if any(k in low for k in ACAD_EN):
        return "A", nm
    if any(k in nm for k in IND_CN):
        return "I", nm
    if any(k in low for k in IND_EN):
        return "I", nm
    return None, nm


def academicians() -> set[str]:
    cur = gkx()
    try:
        cur.execute("SET SESSION max_execution_time=60000")
        cur.execute("SELECT scholar_id FROM gkx.dwd_scholar_talent_flag WHERE academician=1")
        return {r[0] for r in cur.fetchall()}
    finally:
        cur.close()


def main() -> None:
    d = T.texts()
    rows = T.rows_of(d, "work_exp_rows")
    sch = T.rows_of(json.loads((T.SNAP / "probe_a26_20261022.json").read_text(encoding="utf-8")),
                    "scholar_dump")
    base = json.loads((T.SNAP / "star_base_rows_gkx.json").read_text(encoding="utf-8"))
    ind_map = {(r[1] or "").strip(): (r[5] or "") for r in base if r[1]}
    aca = academicians()

    h = sorted(int(r[5] or 0) for r in sch)
    p70 = h[int(0.70 * (len(h) - 1))]
    core = {r[0] for r in sch if int(r[5] or 0) >= p70} | aca

    by: dict[str, list] = defaultdict(list)
    cls_counter = Counter()
    org_city = Counter()
    base_hit = 0
    for r in rows:
        sid, seq, st, et, cur_flag, zh, en, status = r
        c, nm = classify(zh, en, ind_map)
        cls_counter[c] += 1
        if nm in ind_map:
            base_hit += 1
        if c:
            city = T.city_of(nm)
            if city:
                org_city[city] += 1
        by[sid].append((seq if seq is not None else 0, c, T.year_of(st), st))

    # 口径要求对象=核心技术人才（院士 或 h_index ≥ 池内 P70）。主口径只用核心池；
    # 全池结果留作敏感性对照，避免把「全部学者」与「核心人才」混成一个数。
    flows_all = {"A->I": Counter(), "I->A": Counter()}
    flows = {"A->I": Counter(), "I->A": Counter()}
    flow_people: dict[tuple[str, int], set] = defaultdict(set)
    multi_seg = 0
    unclassified_seg = 0
    events = 0
    events_all = 0
    for sid, segs in by.items():
        segs.sort(key=lambda x: (x[0], x[2] or 0))
        if len(segs) >= 2:
            multi_seg += 1
        prev = None
        for seq, c, y, _raw in segs:
            if c is None:
                unclassified_seg += 1
            if c and prev and c != prev and y:
                key = "A->I" if prev == "A" else "I->A"
                flows_all[key][y] += 1
                events_all += 1
                if sid in core:
                    flows[key][y] += 1
                    flow_people[(key, y)].add(sid)
                    events += 1
            if c:
                prev = c

    year_all = sorted({y for c in flows.values() for y in c})
    series = []
    series_all = []
    for y in range(2005, 2026):
        series.append({"year": y, "A2I": flows["A->I"].get(y, 0), "I2A": flows["I->A"].get(y, 0),
                       "people_A2I": len(flow_people[("A->I", y)]),
                       "people_I2A": len(flow_people[("I->A", y)])})
        series_all.append({"year": y, "A2I": flows_all["A->I"].get(y, 0),
                           "I2A": flows_all["I->A"].get(y, 0)})

    # burst：T=2024（最后一个完整年），近窗 2022—2024，基线 2017—2021
    T_YEAR = 2024
    recent_years = [T_YEAR - 2, T_YEAR - 1, T_YEAR]
    base_years = [T_YEAR - 7, T_YEAR - 6, T_YEAR - 5, T_YEAR - 4, T_YEAR - 3]
    burst = {}
    for key in ("A->I", "I->A"):
        rec = [flows[key].get(y, 0) for y in recent_years]
        bs = [flows[key].get(y, 0) for y in base_years]
        rm, bm = sum(rec) / 3, sum(bs) / 5
        burst[key] = round((rm - bm) / max(bm, 1), 4)
    wA = sum(flows["A->I"].get(y, 0) for y in recent_years)
    wI = sum(flows["I->A"].get(y, 0) for y in recent_years)
    tot_w = wA + wI
    overall = round((wA * burst["A->I"] + wI * burst["I->A"]) / tot_w, 4) if tot_w else None
    alert = 2 if (overall or 0) >= 1 else (1 if (overall or 0) >= 0.5 else 0)

    res = {
        "metric_id": MID,
        "metric_name": "科技人才流动（产业界↔学术界）",
        "support_judgment": "部分支持",
        "object": "学者（核心人才：院士或 h_index ≥ 池内 P70）",
        "verdict_reason": (
            "时间维与方向二维可算（核心人才池 6,580 人内识别出跨界事件，2005 年后完整年份逐年可排），"
            "但空间维不可用："
            f"57,117 条经历的机构名只有 {base_hit} 条（{round(100 * base_hit / len(rows), 2)}%）"
            "能对上工商底册，高校/海外机构不在底册中；另有 "
            f"{cls_counter[None]:,} 条（{round(100 * cls_counter[None] / len(rows), 2)}%）"
            "机构名无法判定性质，按口径第四步须整段跳过"),
        "data_source": "gkx.dwd_scholar_work_experience / dwd_scholar / dwd_scholar_talent_flag",
        "sql_count": 2,
        "sql": ["SELECT scholar_id, seq_no, start_time, end_time, is_current, org_name_zh, "
                "org_name_en, status FROM gkx.dwd_scholar_work_experience",
                "SELECT scholar_id FROM gkx.dwd_scholar_talent_flag WHERE academician=1"],
        "probe": {
            "scholars_all": len(sch),
            "scholars_with_experience": len(by),
            "experience_rows": len(rows),
            "scholars_ge2_segments": multi_seg,
            "rows_start_year_parseable": sum(1 for r in rows if T.year_of(r[2])),
            "rows_org_zh": int(T.rows_of(T.tail(), "work_exp_agg")[0][2]),
            "rows_org_en": int(T.rows_of(T.tail(), "work_exp_agg")[0][3]),
            "class_A": cls_counter["A"],
            "class_I": cls_counter["I"],
            "class_unknown": cls_counter[None],
            "unknown_pct": round(100 * cls_counter[None] / len(rows), 2),
            "org_name_hits_registry": base_hit,
            "org_name_hit_pct": round(100 * base_hit / len(rows), 2),
            "academicians": len(aca),
            "h_p70": p70,
            "core_talent_pool": len(core),
            "flow_events_total": events,
            "flow_events_all_scholars": events_all,
            "flow_A2I_total": sum(flows["A->I"].values()),
            "flow_I2A_total": sum(flows["I->A"].values()),
            "segments_unclassified": unclassified_seg,
        },
        "year_series": series,
        "year_series_all_scholars": series_all,
        "series_note": "主口径为核心人才池（6,580 人）；逐年 0 值年保留为 0，不跳行。全池序列见 year_series_all_scholars（1,681 次），仅供灵敏度对照",
        "burst_note": "近窗 3 年总事件 6 次、基线 5 年总事件 3 次，burst 分母取 max(基线均值,1)，"
                      "等级由个位数计数决定，只能作「待观察」，不可作对外预警结论",
        "burst": {
            "T": T_YEAR,
            "recent_window": recent_years,
            "base_window": base_years,
            "A2I": burst["A->I"],
            "I2A": burst["I->A"],
            "overall": overall,
            "alert_level": alert,
            "alert_name": {2: "2 预警", 1: "1 关注", 0: "0 无"}[alert],
        },
        "org_city_top": T.topn(org_city, 15),
        "base_years_used": base_years + recent_years,
        "base_years_missing": [2025, 2026],
        "base_year_block": T.base_year_block(
            base_years + recent_years, [2025, 2026],
            "burst 以 2024 为 T：近窗 2022—2024、基线 2017—2021；2025 只有 9 次事件、"
            "2026 尚未成段，均不进分母"),
        "gaps": [
            f"空间维不可用：机构名与工商底册命中 {base_hit} 条（{round(100 * base_hit / len(rows), 2)}%），"
            "高校/科研院所/海外机构不在底册",
            f"{cls_counter[None]:,} 条经历性质无法判定（{round(100 * cls_counter[None] / len(rows), 2)}%），"
            "按口径跳过，会系统性漏掉外文小机构",
            "工作经历只有 57,117 段 / 20,028 人，7,601 人只有 1 段，无法识别流动",
            "7,480 条经历 start_time 为空或非年份形态，流动年无法定位",
            "2025 年只记录 9 次、2026 年 0 次，近窗右端不完整",
        ],
        "repair_requirements": [
            "补高校/科研院所主数据（含曾用名）以把机构名 → 城市打通",
            "工作经历补 org_id 或统一社会信用代码，避免按名称字符串判定性质",
            "start_time 缺失的 7,480 行需回填，否则流动年不可定",
        ],
    }
    T.write_out(MID, res)
    print({k: res[k] for k in ("probe", "burst")})
    print(series[-8:])


if __name__ == "__main__":
    main()
