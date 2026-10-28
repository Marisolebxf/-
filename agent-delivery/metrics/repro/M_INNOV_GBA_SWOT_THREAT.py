#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_GBA_SWOT_THREAT · 湾区创新能力威胁因素（gkx 口径重建件，零 SQL）

口径（照抄旧稿三维，逐维实测后标注可行性）：
  D1 政策退坡 = 近窗失效政策数 / max(近窗有效政策数, 1) ≥ 0.3
  D2 竞争挤压 = 近窗专利份额 − 基线专利份额 ≤ −0.02（−2pp）
  D3 结构风险 = HHI(IPC4) ≥ 0.25
  威胁分 0—100 = D2 触发记 50 + D3 相对集中度（HHI/四城中位每高 10% 记 10 分，上限 50）

实测结论（写进产物，不许改写）：
  D1 三重不可算：① 政策表 20,000 行 status 全为「有效」，无失效样本；
     ② 表内无 expire_date 列（不是空值，是列不存在）；③ 近窗 2023—2025 全国仅 1 条。
  D2 可算；2025—2026 为公布滞后残年，单列删失敏感性，不进主口径。
  D3 可算，但 0.25 的阈值在 IPC4（数百个小类）上不可达，必须补「相对四城中位」连续判据。

【本件自定义、待甲方确认】
  −2pp 阈值、0.25 HHI 阈值、威胁分 50/50 权重与 10%/10 分斜率，均为旧稿设定，无官方出处。

数据源（零 SQL）：
  _snapshots21/gba_patent_20261021.json       四城×年 专利件数（面板 app_year × 底册归城）
  _snapshots21/patent_scan_20261021.pkl       四城×年×IPC4，pn 去重（算 HHI）
  _snapshots21/gba_policy_20261021.json       政策 20,000 行（status 全有效）
  _snapshots21/policy_base_20261021.json      政策日期/城市/标题

运行：cd code && python3 M_INNOV_GBA_SWOT_THREAT.py
产物：code/M_INNOV_GBA_SWOT_THREAT_out.json
"""
from __future__ import annotations

import collections
import json
import os
import pickle
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

MID = "M_INNOV_GBA_SWOT_THREAT"
CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]
SHORT = {"深圳市": "深圳", "广州市": "广州", "东莞市": "东莞", "惠州市": "惠州"}
BASE_Y = {"2021", "2022"}
REC_Y = {"2023", "2024"}
CENS_Y = {"2025"}


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def hhi(counter):
    tot = sum(counter.values())
    return round(sum((v / tot) ** 2 for v in counter.values()), 4) if tot else 0.0


def main():
    pat = load("gba_patent_20261021.json")
    pol_meta = load("gba_policy_20261021.json")
    pol = load("policy_base_20261021.json")

    # ---------------- D1 政策退坡
    by_year = collections.Counter((p.get("date") or "")[:4] for p in pol)
    recent_nat = sum(by_year.get(y, 0) for y in ("2023", "2024", "2025"))
    d1 = {
        "status_distribution": {"有效": pol_meta["rows"]},
        "status_note": pol_meta["status_note"],
        "expire_date_column_exists": False,
        "expire_date_parseable": 0,
        "recent_policy_national_2023_2025": recent_nat,
        "policy_rows": pol_meta["rows"],
        "policy_year_tail": {y: by_year.get(y, 0) for y in ("2019", "2020", "2021", "2022", "2023", "2024", "2025")},
        "policy_by_city": pol_meta["by_city"],
        "evaluable": False,
        "blocks": [
            f"status 全表 {pol_meta['rows']:,} 行均为「有效」，失效记录 0 条 → 分子恒 0、退坡率恒 0，无区分度",
            "表内无 expire_date 列（不是空值），无法按到期日判定退坡",
            f"近窗（2023—2025）全国政策合计 {recent_nat} 条 → 分母近 0，比值无意义",
        ],
    }

    # ---------------- D2 竞争挤压
    def shares(years):
        tot = {c: sum(int(pat["city_year"].get(c, {}).get(y, 0)) for y in years) for c in CITIES}
        s = sum(tot.values())
        return ({c: (tot[c] / s if s else None) for c in CITIES}, tot)

    s_base, v_base = shares(BASE_Y)
    s_rec, v_rec = shares(REC_Y)
    s_cens, v_cens = shares(CENS_Y)

    d2 = {}
    for c in CITIES:
        delta = (s_rec[c] - s_base[c]) * 100 if s_base[c] is not None else None
        delta_c = ((s_cens[c] - s_base[c]) * 100
                   if (s_cens.get(c) is not None and s_base.get(c) is not None) else None)
        d2[c] = {
            "patents_baseline_2y": v_base[c], "share_baseline": round(s_base[c], 4),
            "patents_recent_2y": v_rec[c], "share_recent": round(s_rec[c], 4),
            "delta_pp": round(delta, 2), "trigger": bool(delta is not None and delta <= -2.0),
            "censored_variant": {
                "share_2025_only": round(s_cens[c], 4) if s_cens.get(c) is not None else None,
                "patents_2025": v_cens[c],
                "delta_pp": round(delta_c, 2) if delta_c is not None else None,
                "trigger": bool(delta_c is not None and delta_c <= -2.0),
            },
        }

    # ---------------- D3 结构风险（IPC4 HHI，2023—2024）
    with open(os.path.join(SNAP, "patent_scan_20261021.pkl"), "rb") as f:
        scan = pickle.load(f)
    # 注意：pkl 里的城市键已是短名（深圳/广州/东莞/惠州），不是「深圳市」
    SHORTS = set(SHORT.values())
    ipc = collections.defaultdict(lambda: collections.Counter())
    for (city, y, code), pns in scan["ipc_pn"].items():
        if city in SHORTS and int(y) in (2023, 2024):
            ipc[city][code] += len(pns)

    d3 = {}
    for c in CITIES:
        c4 = ipc[SHORT[c]]
        c3 = collections.Counter()
        for k, v in c4.items():
            c3[k[:3]] += v
        tot = sum(c4.values())
        top = c4.most_common(3)
        d3[c] = {
            "hhi_ipc4": hhi(c4), "hhi_ipc3": hhi(c3),
            "n_ipc4": len(c4), "n_ipc3": len(c3), "assignments": tot,
            "top3_ipc4": [{"ipc4": k, "n": v, "share_pct": round(v / tot * 100, 2)} for k, v in top],
            "top3_share_pct": round(sum(v for _, v in top) / tot * 100, 2),
            "trigger_hhi_025": bool(hhi(c4) >= 0.25),
            "threshold_note": (f"HHI=0.25 等价于「两个领域各占 50%」；本城 IPC4 有 {len(c4)} 个，"
                               "结构上不可能达到 0.25"),
        }

    med_h = statistics.median([d3[c]["hhi_ipc4"] for c in CITIES])
    for c in CITIES:
        d3[c]["hhi_vs_panel_median"] = round(d3[c]["hhi_ipc4"] / med_h, 3) if med_h else None

    # ---------------- 合成
    score, city_out = {}, {}
    for c in CITIES:
        s = 50.0 if d2[c]["trigger"] else 0.0
        rel = d3[c]["hhi_vs_panel_median"] or 1.0
        s += min(max((rel - 1) / 0.3, 0) * 50, 50)
        score[c] = round(s, 2)
        th = []
        if d2[c]["trigger"]:
            th.append(f"竞争挤压：份额 {d2[c]['share_baseline']:.2%} → {d2[c]['share_recent']:.2%}"
                      f"（{d2[c]['delta_pp']:+.2f}pp，阈值 −2.00pp）")
        if d3[c]["trigger_hhi_025"]:
            th.append(f"结构风险：HHI(IPC4)={d3[c]['hhi_ipc4']} ≥ 0.25")
        elif (d3[c]["hhi_vs_panel_median"] or 1) >= 1.15:
            th.append(f"结构相对集中：HHI(IPC4)={d3[c]['hhi_ipc4']}，为四城中位数的 "
                      f"{d3[c]['hhi_vs_panel_median']:.2f} 倍，前三领域占 {d3[c]['top3_share_pct']}%")
        city_out[c] = {
            "score_0_100": score[c],
            "policy_rollback": {"evaluable": False},
            "competition_squeeze": d2[c],
            "structural_risk": d3[c],
            "threat_list": th or ["未检出达到阈值的威胁（政策维不可评）"],
            "response": (["对份额下滑领域做定向招商与研发补贴核验"] if d2[c]["trigger"] else [])
            + (["对高度集中领域做多元化布局"] if (d3[c]["hhi_vs_panel_median"] or 1) >= 1.15 else [])
            or ["维持现有监测频率"],
        }

    payload = {
        "metric_id": MID,
        "metric_name": "湾区创新能力威胁因素",
        "domain": "TOPIC-INNOV / 湾区创新监测",
        "formula_owner": "王惠（旧稿口径，D1 弃算、D3 补相对判据）",
        "support_judgment": "部分支持",
        "support_reason": (
            f"D2/D3 在 {sum(d3[c]['assignments'] for c in CITIES):,} 条 IPC4 归属性上可算，四城威胁分 "
            f"{min(score.values()):.1f}—{max(score.values()):.1f} 有区分度；但 D1 政策退坡三重阻断"
            f"（status 全有效 {pol_meta['rows']:,} 行、无 expire_date 列、近窗 {recent_nat} 条），"
            "而政策恰恰是需求最关心的威胁来源。11 城中只有 4 城可评，港澳与珠西五市无数据。"
        ),
        "generated_at": "2026-10-22",
        "main_db": "gkx @ 183.240.141.251:3318（gkx_reader_zp，只读）",
        "sql_count": 0,
        "sources": [
            "code/_snapshots21/gba_patent_20261021.json（面板 2,939,895 行 × 底册归城，四城 2,126,758 件）",
            "code/_snapshots21/patent_scan_20261021.pkl（四城×年×IPC4）",
            "code/_snapshots21/gba_policy_20261021.json（20,000 行，status 全有效）",
            "code/_snapshots21/policy_base_20261021.json（日期/城市）",
        ],
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": [2017, 2018, 2019, 2020],
        "base_years_note": (
            "基线 2021—2022、近窗 2023—2024（四个完整年）；快照 gba_patent.city_year 只落到 2024，"
            "2025/2026 虽有全表件数（440,401 / 74,810，分别为完整年的 72.6% / 12.3%）但未归城，"
            "故删失敏感性本件不可算（字段为 null），不拿全国残年冒充四城份额；"
            "2017—2020 在 dwd_patent 为零行，未补 0、未外推。政策表日期止于 2024（2024 年 1 条）。"
        ),
        "definition_note": (
            "本件自定义、待甲方确认：−2pp 挤压阈值、0.25 HHI 阈值、威胁分 50/50 权重与"
            "「每高 10% 记 10 分」的斜率，均为旧稿设定，无官方出处；HHI 阈值在 IPC4 粒度上不可达，"
            "本件以四城中位相对倍数替代，属改写。"
        ),
        "universe": {"cities_documented": 11, "cities_evaluable": 4, "cities": CITIES},
        "windows": {"baseline": "2021-2022", "recent": "2023-2024",
                    "censored": "2025-2026（公布滞后，不入主口径）"},
        "rule_rewrites": {
            "D1": {"rule": "近窗失效政策数 / max(近窗有效政策数,1) ≥ 0.3", "status": "不可算"},
            "D2": {"rule": "近窗份额 − 基线份额 ≤ −0.02", "status": "保留",
                   "added": "并列 2025 单年删失敏感性，识别伪威胁"},
            "D3": {"rule": "HHI(IPC4) ≥ 0.25", "status": "保留但不可触发",
                   "added": "补「相对四城中位 HHI」连续判据"},
        },
        "panel_hhi_median": round(med_h, 4),
        "cities": city_out,
        "ranking": sorted([{"city": SHORT[c], "score": score[c]} for c in CITIES],
                          key=lambda x: -x["score"]),
        "gaps": [
            "政策退坡维整体不可算：无失效状态、无到期日列、近窗无样本（三重独立阻断）；",
            "HHI 0.25 阈值与 IPC4 粒度不匹配，原规则在任何城市都不触发；本件改用相对中位倍数；",
            "11 城中仅 4 城可评：港澳、珠海、佛山、中山、江门、肇庆无专利归城数据；",
            "政策属地覆盖率低：深圳 879 / 广州 325 / 东莞 8 / 惠州 0，且 9,706 行为占位（province/city 为 'NULL'）；",
            "份额与集中度均基于「语料内」专利（四城占可归城行的 99.95%），不是全国口径；",
            "2025—2026 无法归城：gba_patent.city_year 只覆盖 2021—2024，删失敏感性因此为空，不能据此判断「份额流失」；",
        ],
    }

    out = os.path.join(HERE, f"{MID}_out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    print("wrote", os.path.basename(out))
    print(f"{'城市':<6}{'威胁分':>8}{'份额Δpp':>10}{'HHI4':>9}{'HHI3':>8}{'vs中位':>8}{'前3占比':>9}")
    for c in sorted(CITIES, key=lambda x: -score[x]):
        print(f"{SHORT[c]:<6}{score[c]:>8.1f}{d2[c]['delta_pp']:>10.2f}{d3[c]['hhi_ipc4']:>9.4f}"
              f"{d3[c]['hhi_ipc3']:>8.4f}{d3[c]['hhi_vs_panel_median']:>8.2f}{d3[c]['top3_share_pct']:>9.2f}")
    print("censored", {SHORT[c]: d2[c]["censored_variant"]["delta_pp"] for c in CITIES})
    print("policy recent", recent_nat, "by_year", d1["policy_year_tail"])


if __name__ == "__main__":
    main()
