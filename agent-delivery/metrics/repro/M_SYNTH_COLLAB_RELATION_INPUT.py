#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_SYNTH_COLLAB_RELATION_INPUT 协同关系输入统计（gkx 换源重建，零 SQL）。

口径（项目内 calc-logic 0.3.2，非王惠 xlsx）：
  relation_type ∈ {joint_patent, coop_project, talent_flow}
  事件粒度 relation_event_id；有效门槛：主体 ≥2 / 项目跨 ≥2 机构 / 人员跨机构 ≥1
  输出 GROUP BY relation_type, region 的事件计数（本批按 region 出全国 + 四城归属）

三类事件的构造：
  joint_patent  同一 `pn` 下申请人数 ≥2 记 1 事件；若同一专利内同时出现企业主体
                （有限公司/股份/集团/厂）与高校院所主体（大学/学院/研究院/所/医院），
                另记 1 个产学研（IUR）子事件
  talent_flow   同一 `scholar_id` 的任职机构序列去掉连续重复后长度 ≥2，记 len−1 次迁移
  coop_project  项目表 `funded_institution` 非空 0 行、`participating_institution` 每项目仅 1 家，
                无法按「跨 ≥2 机构」成事件 → 结构性缺失（见 §三/§四）

数据来源（唯一）：
  code/_snapshots21/collab_inputs21.json
    gkx.dwd_patent_applicants         28,964 行 / 20,000 个 pn
    gkx.dwd_scholar_work_experience   57,117 行
    gkx.dwd_zh_project                58,453 行（仅取字段级填充率）
  城市归属用 code/_snapshots21/base_20261021.json 的 name→city（重名 1/k 摊）

输出：code/M_SYNTH_COLLAB_RELATION_INPUT_out.json
"""
from __future__ import annotations

import collections
import json
import re
import time

import _synth21_common as S

MID = "M_SYNTH_COLLAB_RELATION_INPUT"
CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
CACHE = S.SNAP / "collab_inputs21.json"

ENT_RE = re.compile(r"(有限公司|股份|集团|公司|厂|企业|合伙企业|LLC|LTD|INC|CORP|GMBH)")
UNI_RE = re.compile(r"(大学|学院|研究院|研究所|科学院|研究中心|医院|SCHOOL|UNIV|INSTITUT|COLLEGE)")


def city_of(org: str) -> dict:
    """机构串 → {city: 权重}：先用城市名/白名单，再用底册名称字典；重名 1/k 摊。"""
    w = {}
    c = S.inst_city(org)
    if c:
        w[c] = w.get(c, 0.0) + 1.0
        return w
    return S.name_city_weights(org)


def main() -> None:
    t0 = time.time()
    cache = json.loads(CACHE.read_text(encoding="utf-8"))

    # ---------------- 联合专利事件 ----------------
    by_pn = collections.defaultdict(set)
    for pn, nm in cache["patent_applicants"]:
        if pn and nm:
            by_pn[pn].add(nm)
    multi = {k: v for k, v in by_pn.items() if len(v) >= 2}
    iur = {}
    for pn, names in multi.items():
        has_ent = any(ENT_RE.search(n) for n in names)
        has_uni = any(UNI_RE.search(n) for n in names)
        if has_ent and has_uni:
            iur[pn] = names
    part = collections.Counter()
    for names in multi.values():
        # sorted：set 的遍历序随 PYTHONHASHSEED 变，会让同票主体的插入序漂移，
        # 进而让 most_common 的同票并列顺序在两次重跑之间互换（实测 61 票的三家
        # 主体在 BAXTER HEALTHCARE SA / VANTIVE US HEALTHCARE LLC 之间换位）。
        for n in sorted(names):
            part[n] += 1

    def top_participants(k: int = 10):
        # 先按票数降序，再按名称升序，彻底消掉同票并列的顺序依赖。
        return sorted(part.items(), key=lambda kv: (-kv[1], kv[0]))[:k]

    # 城市归属：事件级（一篇专利内所有主体归城后合并）
    jp_city = collections.Counter()
    jp_within, jp_cross = 0, 0
    jp_events_with_city = 0
    for pn, names in multi.items():
        w = collections.Counter()
        for n in names:
            for c, k in city_of(n).items():
                w[c] += k
        gba = {c: v for c, v in w.items() if c in CITIES}
        if gba:
            jp_events_with_city += 1
            for c, v in gba.items():
                jp_city[c] += v
            if len(gba) >= 2:
                jp_cross += 1
            else:
                jp_within += 1

    # ---------------- 人才流动事件 ----------------
    seq = collections.defaultdict(list)
    for sid, org, start, _end, _cur in cache["work_experience"]:
        if sid and org:
            seq[sid].append((start, org))
    movers = 0
    transitions = 0
    pair_counter = collections.Counter()
    flow_city = collections.Counter()
    flow_within, flow_cross = 0, 0
    flow_no_city = 0
    for sid, rows in seq.items():
        rows.sort(key=lambda t: t[0])
        seen = []
        for _st, org in rows:
            if not seen or seen[-1] != org:
                seen.append(org)
        uniq = []
        for o in seen:
            if o not in uniq:
                uniq.append(o)
        if len(uniq) >= 2:
            movers += 1
            transitions += len(uniq) - 1
            for a, b in zip(uniq, uniq[1:]):
                pair_counter[(a, b)] += 1
                ca, cb = city_of(a), city_of(b)
                ga = {c: v for c, v in ca.items() if c in CITIES}
                gb = {c: v for c, v in cb.items() if c in CITIES}
                if not ga or not gb:
                    flow_no_city += 1
                    continue
                for c, v in gb.items():
                    flow_city[c] += v
                if set(ga) == set(gb):
                    flow_within += 1
                else:
                    flow_cross += 1

    # ---------------- 合作项目 ----------------
    pj = cache["project_fill"]

    out = {
        "metric_id": MID,
        "metric_name": "协同关系输入统计",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读落盘快照",
        "source": cache["source"],
        "source_snapshot": {"file": "code/_snapshots21/collab_inputs21.json",
                            "generated_at": cache["generated_at"],
                            "queries": cache["queries"]},
        "event_grain": {
            "joint_patent": {
                "distinct_patents": len(by_pn),
                "events_national": len(multi),
                "share_multi_applicant": round(len(multi) / max(1, len(by_pn)), 4),
                "iur_events": len(iur),
                "iur_share_of_events": round(len(iur) / max(1, len(multi)), 4),
                "top_participants": top_participants(),
                "universe_note": ("申请人表只有 20,000 个 pn / 28,964 行，是抽样表而非全量；"
                                  "全量 2,939,895 件专利的共同申请人未落表"),
            },
            "talent_flow": {
                "scholars_total": len(seq),
                "movers": movers,
                "events_national": transitions,
                "mean_moves_per_mover": round(transitions / max(1, movers), 3),
                "top_pairs": [{"from": a, "to": b, "n": n} for (a, b), n in pair_counter.most_common(8)],
            },
            "coop_project": {
                "rows": pj["rows"],
                "funded_institution_nonnull": pj["funded_institution_nonnull"],
                "participating_institution_nonnull": pj["participating_institution_nonnull"],
                "participating_institution_distinct": pj["participating_institution_distinct"],
                "project_host_nonnull": pj["project_host_nonnull"],
                "events_national": 0,
                "status": ("结构性缺失：funded_institution（资助机构）非空 0 行；"
                           "participating_institution（承担机构）虽有 %d 行，但每行只写 1 家机构"
                           "（%d 个项目 → 1,592 个不同机构名），project_host 存的是人名而非机构，"
                           "无法按『跨 ≥2 机构』成事件"
                           % (pj["participating_institution_nonnull"],
                              pj["rows"])),
            },
        },
        "city_scoped": {
            "regions": CITIES,
            "joint_patent": {
                "events_with_city": jp_events_with_city,
                "events_with_city_share": round(jp_events_with_city / max(1, len(multi)), 4),
                "within_city": jp_within,
                "cross_city": jp_cross,
                "by_city_attribution": {c: round(jp_city[c], 2) for c in CITIES},
            },
            "talent_flow": {
                "transitions_with_city": flow_within + flow_cross,
                "transitions_with_city_share": round((flow_within + flow_cross)
                                                     / max(1, transitions), 4),
                "within_city": flow_within,
                "cross_city": flow_cross,
                "no_city": flow_no_city,
                "inflow_by_city": {c: round(flow_city[c], 2) for c in CITIES},
            },
            "coop_project": {"events": 0, "note": "输入表不可构事件"},
        },
        "type_coverage": {
            "declared_types": 3,
            "computable_types": 2,
            "coverage_pct": 66.7,
            "missing": ["coop_project"],
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "三类关系中联合专利与人才流动两路可现转（全国事件级 %d / %d；四城中可归城事件 "
            "%d（%.2f%%）/ %d（%.2f%%）），但合作项目一路结构性缺失——dwd_zh_project %d 行中"
            "funded_institution 非空 0 行，participating_institution 每项目仅 1 家机构、"
            "无参与单位列表字段，无法按『跨 ≥2 机构』成事件；三类口径只能出两类（66.7%%），"
            "且联合专利一侧用的是 20,000 件抽样表、不是 293.99 万件全量，"
            "区域维可归城率不足 2%%。按四档定义判部分支持。"
            % (len(multi), transitions,
               jp_events_with_city, jp_events_with_city / max(1, len(multi)) * 100,
               flow_within + flow_cross,
               (flow_within + flow_cross) / max(1, transitions) * 100,
               pj["rows"])),
        "note": ("事件门槛按 calc-logic：多申请人专利去重后 ≥2 主体记 1 事件；"
                 "学者跨机构任职变迁记 1 事件（同机构连续记录先合并）。"
                 "城市归属用底册 name→city（重名 1/k 摊）+ 城市名/高校白名单，"
                 "可归城率随机构串质量变化，见 §三。"),
        "sources": [
            {"file": "code/_snapshots21/collab_inputs21.json",
             "content": "dwd_patent_applicants 28,964 行 / dwd_scholar_work_experience 57,117 行 / dwd_zh_project 字段填充率",
             "source": cache["source"]},
            {"file": "code/_snapshots21/base_20261021.json",
             "content": "底册 189,116 行（机构名→城市，重名 1/k 摊）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_org_base_info"},
        ],
        "elapsed_sec": None,
    }
    out.update(S.base_year_block(
        [], [],
        "三类事件都是**全历史累计**口径（专利申请人表无年份字段、任职经历按 start_time 排序但"
        "不按年截断、项目表为存量），本指标不做跨年除法，因此没有分母年、也没有缺失年可摊 0。"))
    out["elapsed_sec"] = round(time.time() - t0, 1)
    S.write_out(MID, out)

    print(json.dumps({"joint_patent": {k: out["event_grain"]["joint_patent"][k]
                                       for k in ("distinct_patents", "events_national",
                                                 "iur_events", "iur_share_of_events")},
                      "talent_flow": {k: out["event_grain"]["talent_flow"][k]
                                      for k in ("scholars_total", "movers", "events_national")},
                      "city": out["city_scoped"],
                      "coverage": out["type_coverage"]},
                     ensure_ascii=False, indent=1)[:2600])
    print("elapsed", out["elapsed_sec"], "s")


if __name__ == "__main__":
    main()
