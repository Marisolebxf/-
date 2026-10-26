#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_DEEP_142_1 企业发展历程模型（企业重大事件时间线）。

口径（calc-logic ALGO-ENT-DEEP-142，项目侧规范化，非王惠）：
    把企业五类重大事件按 event_time 归并、倒序排成一条时间线：
      E1 上市/挂牌   E2 股权融资   E3 并购（作为交易当事人）
      E4 对外投资     E5 股权结构（股东快照）
    另以 E0 成立年作时间线锚点。

取数（只连三方库 gkx，只读；不引任何 demo_* schema）：
    gkx.dwd_org_base_info                     189,116 行（城市/成立年/上市状态，来自本地快照）
    gkx.dwd_org_financing_info                 25,654 行（completion_date 全有，金额为文本）
    gkx.dwd_merger_acquisition_events_party_info 20,000 行（ggrq 公告日）
    gkx.dwd_org_merger_acquisition_info          3,444 行（ma_amount，单位存疑）
    gkx.dwd_org_invest_info                     46,967 行（investment_amount，无业务日期）
    gkx.dwd_org_shareholder_info               400,286 行（当前快照，无变更日期）

产物：code/M_ENT_DEEP_142_1_out.json
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import _gkxdb

BASE = Path(__file__).parent
SNAP = BASE / "_snapshots21"
OUT = BASE / "M_ENT_DEEP_142_1_out.json"
METRIC = "M_ENT_DEEP_142_1"
CITY4 = ["深圳市", "广州市", "东莞市", "惠州市"]
BIG_INVEST_WAN = 1000.0          # 1000 万元，单位按库内「万元」解释（见 notes 的单位风险）


def load(name):
    return json.loads((SNAP / name).read_text(encoding="utf-8"))


def parse_amount_wan(txt):
    """把『8320.0万人民币』『1.2亿』『3000万元』解析成万元；解析不了返回 None。"""
    if txt is None:
        return None
    s = str(txt).strip()
    if not s:
        return None
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)", s.replace(",", ""))
    if not m:
        return None
    v = float(m.group(1))
    if "亿" in s:
        return v * 10000.0
    if "万" in s:
        return v
    if "元" in s:
        return v / 10000.0
    return v


def main():
    t0 = time.time()
    base = load("base_20261021.json")
    info = {}
    for r in base:
        info[r[0]] = {"name": r[2], "city": r[4], "inc_year": r[5]}
    city4_ids = {oid for oid, d in info.items() if d["city"] in CITY4}

    cur = _gkxdb.gkx()

    def q(sql, args=None):
        cur.execute(sql, args)
        return cur.fetchall()

    # ---------------------------------------------------------------- 探针
    probe = {}
    probe["base_rows"] = len(base)
    probe["base_city4"] = len(city4_ids)
    a = q("SELECT COUNT(*) n, COUNT(listing_date) ld, SUM(listing_status<>'') ls "
          "FROM gkx.dwd_org_base_info")[0]
    probe["listing"] = {"rows": int(a[0]), "listing_date_nonnull": int(a[1]),
                        "listing_status_nonempty": int(a[2])}

    a = q("SELECT COUNT(*) n, COUNT(completion_date) dt, MIN(completion_date) mn, "
          "MAX(completion_date) mx FROM gkx.dwd_org_financing_info")[0]
    probe["financing"] = {"rows": int(a[0]), "dated": int(a[1]),
                          "min_date": str(a[2]), "max_date": str(a[3])}

    a = q("SELECT COUNT(*) n, COUNT(ggrq) dt, MIN(ggrq) mn, MAX(ggrq) mx, "
          "SUM(ggrq='1900-01-01') sentinel "
          "FROM gkx.dwd_merger_acquisition_events_party_info")[0]
    probe["ma_party"] = {"rows": int(a[0]), "dated": int(a[1]), "min_date": str(a[2]),
                         "max_date": str(a[3]), "sentinel_1900": int(a[4])}

    a = q("SELECT COUNT(*) n, COUNT(ma_amount) amt, SUM(ma_amount>0) pos, "
          "MAX(ma_amount) mx FROM gkx.dwd_org_merger_acquisition_info")[0]
    probe["ma_main"] = {"rows": int(a[0]), "amount_nonnull": int(a[1]),
                        "amount_pos": int(a[2]), "max_amount": float(a[3] or 0)}

    a = q("SELECT COUNT(*) n, COUNT(investment_amount) amt, SUM(investment_amount>0) pos, "
          "SUM(investment_amount>=%s) ge_threshold, MAX(investment_amount) mx "
          "FROM gkx.dwd_org_invest_info", (BIG_INVEST_WAN,))[0]
    probe["invest"] = {"rows": int(a[0]), "amount_nonnull": int(a[1]), "amount_pos": int(a[2]),
                       "ge_1000wan": int(a[3]), "max_amount": float(a[4] or 0)}

    a = q("SELECT COUNT(*) n, COUNT(DISTINCT org_id) orgs FROM gkx.dwd_org_shareholder_info")[0]
    probe["shareholder"] = {"rows": int(a[0]), "orgs": int(a[1])}

    # ---------------------------------------------------------------- 事件明细
    fin_rows = q("SELECT org_id, completion_date, funding_round, funding_amount "
                 "FROM gkx.dwd_org_financing_info")
    ma_rows = q("SELECT jgid, ggrq, dsrjslx, dsrmc FROM gkx.dwd_merger_acquisition_events_party_info")
    inv_rows = q("SELECT org_id, investment_amount, investment_ratio FROM gkx.dwd_org_invest_info")
    ma_main_rows = q("SELECT acquiring_org_id, acquiring_name, ma_amount "
                     "FROM gkx.dwd_org_merger_acquisition_info")
    cur.close()

    events = {}          # org_id -> [{date, type, detail, city}]
    fin_orgs, ma_orgs, inv_orgs = set(), set(), set()
    fin_orgs_raw, ma_party_orgs_raw, inv_orgs_raw = set(), set(), set()
    ma_main_orgs_raw = set()
    fin_dated = fin_bad_amount = 0
    year_hist = {}
    round_hist = {}

    for oid, dt, rnd, amt in fin_rows:
        fin_orgs_raw.add(oid)
        d = info.get(oid)
        if d is None:
            continue
        fin_orgs.add(oid)
        if dt is None:
            continue
        fin_dated += 1
        wan = parse_amount_wan(amt)
        if wan is None:
            fin_bad_amount += 1
        ev = {"date": str(dt), "type": "E2 股权融资",
              "detail": f"{rnd or '轮次未披露'}；金额 {amt if str(amt or '').strip() else '未披露'}"}
        events.setdefault(oid, []).append(ev)
        y = str(dt)[:4]
        year_hist[y] = year_hist.get(y, 0) + 1
        round_hist[str(rnd or "未披露")] = round_hist.get(str(rnd or "未披露"), 0) + 1

    ma_dated = ma_sentinel = 0
    for jgid, ggrq, role, name in ma_rows:
        ma_party_orgs_raw.add(jgid)
        d = info.get(jgid)
        if d is None or ggrq is None:
            continue
        ma_orgs.add(jgid)
        if str(ggrq) == "1900-01-01":
            ma_sentinel += 1
            continue
        ma_dated += 1
        ev = {"date": str(ggrq), "type": "E3 并购当事人",
              "detail": f"当事人角色码 {role}；主体 {name}"}
        events.setdefault(jgid, []).append(ev)
        y = str(ggrq)[:4]
        year_hist[y] = year_hist.get(y, 0) + 1

    for oid, amt, ratio in inv_rows:
        inv_orgs_raw.add(oid)
        if oid in info:
            inv_orgs.add(oid)

    for oid, name, amt in ma_main_rows:
        ma_main_orgs_raw.add(oid)
        if oid in info:
            ma_orgs.add(oid)

    # 去重：同一企业同日同类型同描述只保留一条（当事人表存在一对多重复行）
    raw_events = sum(len(v) for v in events.values())
    dedup = {}
    for oid, evs in events.items():
        seen = set()
        keep = []
        for e in evs:
            k = (e["date"], e["type"], e["detail"])
            if k in seen:
                continue
            seen.add(k)
            keep.append(e)
        dedup[oid] = keep
    events = dedup
    dup_removed = raw_events - sum(len(v) for v in events.values())

    # ---------------------------------------------------------------- 覆盖统计
    def city_of(oid):
        return info[oid]["city"] if oid in info else "未匹配"

    def cover(s):
        return sum(1 for o in s if o in city4_ids)

    by_city = {c: {"financing": 0, "ma": 0, "invest": 0, "any": 0} for c in CITY4}
    for oid in fin_orgs | ma_orgs | inv_orgs:
        c = city_of(oid)
        if c not in by_city:
            continue
        by_city[c]["financing"] += 1 if oid in fin_orgs else 0
        by_city[c]["ma"] += 1 if oid in ma_orgs else 0
        by_city[c]["invest"] += 1 if oid in inv_orgs else 0
        by_city[c]["any"] += 1

    any_orgs = fin_orgs | ma_orgs | inv_orgs

    coverage = {
        "base_rows": len(base),
        "city4_rows": len(city4_ids),
        "financing_orgs": len(fin_orgs),
        "financing_orgs_city4": cover(fin_orgs),
        "financing_orgs_raw": len(fin_orgs_raw),
        "financing_match_pct": round(100.0 * len(fin_orgs) / len(fin_orgs_raw), 2),
        "ma_party_orgs_raw": len(ma_party_orgs_raw),
        "ma_party_orgs_matched": len(ma_party_orgs_raw & set(info)),
        "ma_party_match_pct": round(100.0 * len(ma_party_orgs_raw & set(info)) / len(ma_party_orgs_raw), 2),
        "ma_orgs": len(ma_orgs),
        "ma_orgs_city4": cover(ma_orgs),
        "invest_orgs": len(inv_orgs),
        "invest_orgs_city4": cover(inv_orgs),
        "invest_orgs_raw": len(inv_orgs_raw),
        "invest_match_pct": round(100.0 * len(inv_orgs) / len(inv_orgs_raw), 2),
        "any_event_orgs": len(any_orgs),
        "any_event_orgs_city4": cover(any_orgs),
        "any_event_pct_of_city4": round(100.0 * cover(any_orgs) / len(city4_ids), 4),
        "undated_only_orgs": len(any_orgs - set(events)),
        "dup_events_removed": dup_removed,
        "event_inventory": [
            {"type": "E0 成立", "source": "dwd_org_base_info.incorporation_year", "rows": len(base),
             "dated": len(base), "date_granularity": "年", "usable": True},
            {"type": "E1 上市/挂牌", "source": "dwd_org_base_info.listing_status/listing_date",
             "rows": int(probe["listing"]["listing_status_nonempty"]),
             "dated": int(probe["listing"]["listing_date_nonnull"]), "date_granularity": "无", "usable": False},
            {"type": "E2 股权融资", "source": "dwd_org_financing_info.completion_date",
             "rows": int(probe["financing"]["rows"]), "dated": int(probe["financing"]["dated"]),
             "date_granularity": "日", "usable": True},
            {"type": "E3 并购当事人", "source": "dwd_merger_acquisition_events_party_info.ggrq",
             "rows": int(probe["ma_party"]["rows"]), "dated": int(probe["ma_party"]["dated"]),
             "date_granularity": "日（公告日）", "usable": True},
            {"type": "E4 对外投资", "source": "dwd_org_invest_info（无业务日期）",
             "rows": int(probe["invest"]["rows"]), "dated": 0, "date_granularity": "无（仅入库时间）", "usable": False},
            {"type": "E5 股权结构", "source": "dwd_org_shareholder_info（当前快照）",
             "rows": int(probe["shareholder"]["rows"]), "dated": 0, "date_granularity": "无", "usable": False},
        ],
        "dates_available": {"financing": fin_dated, "ma_party": ma_dated,
                            "listing": 0, "invest": 0, "shareholder": 0},
        "by_city": by_city,
    }

    # 每家企业可用事件类型数（0—5）
    type_sets = {}
    for oid in any_orgs:
        s = set()
        if oid in fin_orgs:
            s.add("E2")
        if oid in ma_orgs:
            s.add("E3")
        if oid in inv_orgs:
            s.add("E4")
        type_sets[oid] = s
    dist = {}
    for oid, s in type_sets.items():
        k = len(s)
        dist[str(k)] = dist.get(str(k), 0) + 1

    # ---------------------------------------------------------------- 样例时间线
    ranked = sorted(events.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:12]
    timelines = []
    for oid, evs in ranked:
        d = info.get(oid, {})
        evs = sorted(evs, key=lambda e: e["date"], reverse=True)[:12]
        anchor = f"{int(d['inc_year'])} 年成立" if d.get("inc_year") else "成立年缺失"
        timelines.append({
            "org_id": oid, "name": d.get("name"), "city": d.get("city"),
            "anchor": anchor, "n_dated_events": len(events[oid]),
            "types": sorted(type_sets.get(oid, [])),
            "events": evs,
        })

    # ---------------------------------------------------------------- 判档
    support = {
        "data_support_level": "部分支持",
        "criteria": {
            "listing_date_ready": False,
            "financing_dated": fin_dated > 0,
            "ma_dated": ma_dated > 0,
            "invest_business_date_ready": False,
            "equity_change_history_ready": False,
            "threshold_config_ready": False,
        },
        "reason": (
            f"五类事件只有两类带业务日期：E2 融资 {fin_dated:,} 条有 completion_date、"
            f"E3 并购当事人 {ma_dated:,} 条有公告日 ggrq（另有 {ma_sentinel} 条 1900-01-01 哨兵值）；"
            f"E1 上市 listing_date 全库 0 行非空（listing_status 非空 1,971 家只有状态无日期）；"
            f"E4 对外投资 {probe['invest']['rows']:,} 行只有入库时间 created_time、无投资发生日；"
            f"E5 股权结构 {probe['shareholder']['rows']:,} 行为当前快照、无变更日期与历史版本。"
            "五类中两类可定位到日、一类只有状态、两类无日期 → 时间线只能覆盖部分事件，判部分支持。"
        ),
        "upgrade_path": [
            "E1：补 listing_date（交易所上市日期）→ 上市事件可入线",
            "E4：补 investment_date / 交割日 → 对外投资可入线",
            "E5：建股东变更历史表（变更日 + 变更前后比例）→ 股权变更可入线",
            "E3：补并购事件主表日期字段，替代当事人表 ggrq 间接定位",
        ],
    }

    out = {
        "metric_id": METRIC,
        "metric_name": "企业发展历程模型",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(time.time() - t0, 2),
        "support_judgment": support,
        "definition": {
            "unit": "企业×事件",
            "event_types": ["E0 成立", "E1 上市/挂牌", "E2 股权融资", "E3 并购当事人",
                            "E4 对外投资", "E5 股权结构"],
            "dated_types": ["E0（年粒度）", "E2（日）", "E3（日）"],
            "undated_types": ["E1", "E4", "E5"],
            "threshold": f"对外投资「重大」阈值 {BIG_INVEST_WAN:.0f} 万元（库内金额单位按万元解释）",
        },
        "probe": probe,
        "coverage": coverage,
        "type_dist": dist,
        "round_hist_top": dict(sorted(round_hist.items(), key=lambda kv: -kv[1])[:12]),
        "year_hist": dict(sorted(year_hist.items())),
        "fin_amount_unparsable": fin_bad_amount,
        "timelines": timelines,
        "notes": [
            "金额单位风险：investment_amount / ma_amount 无单位列（ma 有 currency_code 但全 CNY），"
            "按量级判断为万元；若实为元，则 1000 万元阈值下的事件数需除以 10,000，结论方向不变但计数全变。",
            "E3 日期来自当事人表 ggrq（公告日），不是交易完成日；20,000 行中 2 行为 1900-01-01 哨兵值，已剔除。",
            "E2 金额为文本（『8320.0万人民币』『1.2亿』），本脚本解析为万元仅用于分布统计，不参与计数口径。",
            "E4/E5 的 created_time 是入库时间（多为 2026-08），不是业务发生时间，禁止当事件日期使用。",
            "覆盖分母为四城底册 188,774 家（base 快照），不是湾区 11 城。",
        ],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("coverage", "type_dist")}, ensure_ascii=False, indent=1))
    print("support:", support["data_support_level"], "| elapsed", out["elapsed_sec"], "s")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
