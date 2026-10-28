#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_INNOV_KEYD_POTENTIAL · 区域科技创新发展潜力（0—100）· gkx 换源重建。

口径（仿王惠 ai-1020，按库内实测的三个陷阱改造）
------------------------------------------------------------
陷阱 1：`dwd_patent.apdt_year` 只有 2021—2026，且 2025/2026 不完整
        （2021—2024 年各 60 万件量级，2025 只有 44.0 万、2026 只有 7.5 万）
        → 专利增速用 2021→2024 年化 CAGR，只取两个真实存在的年，不把缺失年摊 0。
陷阱 2：`dwd_zh_paper` 2024 年 32,379 篇，是 2023 年（6,651）的 4.87 倍，属批量补录
        → 论文窗口避开 2024：近窗 2021—2023、基窗 2018—2020。
陷阱 3：底册按成立年统计的新设家数自 2021 年起单调衰减，是样本近年覆盖不足
        → D2 改用「新设强度」（2024—2025 新设家数 ÷ 万家企业），不做增速。

D1 产出增速 = 0.5·minmax(专利 CAGR 2021→2024) + 0.5·minmax(论文 2021-2023 vs 2018-2020 增幅)
D2 新主体   = minmax((2024+2025 新设家数) ÷ 万家企业)
D3 转化活跃 = minmax((转入+转出专利件数 2021—2025) ÷ 万家企业)
综合分 = 100 × (D1 + D2 + D3)/3

数据来源（全部只读落盘快照，脚本内零 SQL）：
  code/_snapshots21/base_20261021.json                     底册 189,116 行（含成立年、城市）
  code/_snapshots_gkx21/city_patent_year_gkx.json          城市×年份专利件数（重名 1/k 计权）
  code/_snapshots21/a25_paper_panel.json                   中文论文 100,900 篇
  code/_snapshots21/patent_transfer_rows_20261022.json     专利转让 22,809 行（gkx 直取）

输出：code/M_INNOV_KEYD_POTENTIAL_out.json
"""
from __future__ import annotations

import collections
import json
import time
from pathlib import Path

import _synth21_common as S

HERE = Path(__file__).resolve().parent
MID = "M_INNOV_KEYD_POTENTIAL"
CITIES = ["深圳市", "广州市", "东莞市", "惠州市"]

PAT_CITY_YEAR = S.SNAP.parent / "_snapshots_gkx21" / "city_patent_year_gkx.json"
TRANSFER = S.SNAP / "patent_transfer_rows_20261022.json"


def ymap(d):
    out = {}
    for k, v in (d or {}).items():
        try:
            out[int(float(k))] = float(v)
        except (TypeError, ValueError):
            continue
    return out


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else 0.0


def minmax(d, keys):
    vals = [d[k] for k in keys if d.get(k) is not None]
    if len(vals) < 2 or max(vals) == min(vals):
        return {k: None for k in keys}
    lo, hi = min(vals), max(vals)
    return {k: round((d[k] - lo) / (hi - lo) * 100, 2) if d.get(k) is not None else None
            for k in keys}


def dec(value, num, den, note):
    """v8 §一：每个派生值自带分子/分母。value 逐位等于原先的标量/分城市字典。

    本件 7 个派生键的值都是「城市 → 数值」字典，故 numerator/denominator 也用同键字典，
    保证每个城市各自能对出分子分母，而不是拿四城合计凑一个数。
    """
    return {"value": value, "numerator": num, "denominator": den,
            "denominator_note": note}


def main() -> None:
    t0 = time.time()

    # ---------- 底册：城市存量 + 分年新设 ----------
    base = json.loads((S.SNAP / "base_20261021.json").read_text(encoding="utf-8"))
    org_n = collections.Counter()
    org_y = {c: collections.Counter() for c in CITIES}
    name_city = collections.defaultdict(list)
    yr_missing = 0
    for row in base:
        oid, _cc, nm, _prov, city, yr = (list(row) + [None] * 6)[:6]
        if city:
            org_n[city] += 1
        if nm:
            name_city[str(nm)].append(city)
        if city in org_y:
            try:
                y = int(float(yr))
            except (TypeError, ValueError):
                yr_missing += 1
                continue
            org_y[city][y] += 1

    # ---------- 专利：城市 × 年份 ----------
    pcy = json.loads(PAT_CITY_YEAR.read_text(encoding="utf-8"))
    pat_y = {c: collections.Counter() for c in CITIES}
    for key, n in pcy["groups"].items():
        city, ys = key.split("|")
        if city in pat_y:
            pat_y[city][int(ys)] += float(n)

    # ---------- 论文：城市 × 年份 ----------
    pap_y = {c: collections.Counter() for c in CITIES}
    for p in S.papers():
        if not p["year"]:
            continue
        for c in p["cities"]:
            if c in pap_y:
                pap_y[c][p["year"]] += 1

    # ---------- 专利转让：归属城市 ----------
    tr = json.loads(TRANSFER.read_text(encoding="utf-8"))
    tr_in = {c: collections.Counter() for c in CITIES}
    tr_out = {c: collections.Counter() for c in CITIES}
    n_rows = 0
    n_year_ok = 0
    n_attributed = 0
    n_any_side_attr = 0
    country = collections.Counter()

    def cities_of(blob):
        """转让方/受让方 JSON → {city: 权重}；重名 1/k 摊。"""
        try:
            arr = json.loads(blob) if isinstance(blob, str) else (blob or [])
        except Exception:
            arr = []
        w = collections.Counter()
        for a in arr if isinstance(arr, list) else []:
            nm = (a.get("name") or "").strip() if isinstance(a, dict) else ""
            if not nm:
                continue
            cs = [x for x in name_city.get(nm, []) if x]
            if not cs:
                continue
            k = 1.0 / len(cs)
            for x in cs:
                w[x] += k
        return w

    for pn, before, after, date, ctry in tr["rows"]:
        n_rows += 1
        country[ctry] += 1
        y = None
        if date and len(date) >= 4 and date[:4].isdigit():
            y = int(date[:4])
        if y:
            n_year_ok += 1
        wb, wa = cities_of(before), cities_of(after)
        if wb or wa:
            n_attributed += 1
        if y and 2021 <= y <= 2025:
            for c, w in wb.items():
                if c in tr_out:
                    tr_out[c][y] += w
            for c, w in wa.items():
                if c in tr_in:
                    tr_in[c][y] += w
        if (wb or wa) and y and 2021 <= y <= 2025:
            n_any_side_attr += 1

    # ---------- 派生指标 ----------
    pat_cagr, pap_g, new_intensity, young_share, tr_cnt, tr_per_10k = {}, {}, {}, {}, {}, {}
    for c in CITIES:
        a, b = pat_y[c].get(2021), pat_y[c].get(2024)
        pat_cagr[c] = round((b / a) ** (1 / 3) - 1, 4) if a and b else None

        near = mean([pap_y[c].get(y) for y in (2021, 2022, 2023)])
        far = mean([pap_y[c].get(y) for y in (2018, 2019, 2020)])
        pap_g[c] = round(near / far - 1, 4) if far else None

        new_intensity[c] = round((org_y[c].get(2024, 0) + org_y[c].get(2025, 0))
                                 / org_n[c] * 10000, 2) if org_n[c] else None
        young_share[c] = round(sum(org_y[c].get(y, 0) for y in range(2019, 2026))
                               / org_n[c], 4) if org_n[c] else None
        tr_cnt[c] = round(sum(tr_in[c].values()) + sum(tr_out[c].values()), 2)
        tr_per_10k[c] = round(tr_cnt[c] / org_n[c] * 10000, 2) if org_n[c] else None

    mm_pat = minmax(pat_cagr, CITIES)
    mm_pap = minmax(pap_g, CITIES)
    d1 = {c: round(0.5 * mm_pat[c] + 0.5 * mm_pap[c], 2)
          if mm_pat[c] is not None and mm_pap[c] is not None else None for c in CITIES}
    mm_new = minmax(new_intensity, CITIES)
    mm_tr = minmax(tr_per_10k, CITIES)
    d2 = {c: mm_new[c] for c in CITIES}
    d3 = {c: mm_tr[c] for c in CITIES}
    comp = {c: round((d1[c] + d2[c] + d3[c]) / 3, 2)
            if None not in (d1[c], d2[c], d3[c]) else None for c in CITIES}
    order = sorted([c for c in CITIES if comp[c] is not None], key=lambda x: -comp[x])
    rank = {c: i + 1 for i, c in enumerate(order)}

    mm_young = minmax(young_share, CITIES)
    comp_alt = {c: round((d1[c] + mm_young[c] + d3[c]) / 3, 2)
                if None not in (d1[c], mm_young[c], d3[c]) else None for c in CITIES}
    order_alt = sorted([c for c in CITIES if comp_alt[c] is not None], key=lambda x: -comp_alt[x])
    rank_alt = {c: i + 1 for i, c in enumerate(order_alt)}

    share_attr = round(n_any_side_attr / n_rows, 4) if n_rows else None

    out = {
        "metric_id": MID,
        "metric_name": "区域科技创新发展潜力",
        "formula_owner": "仿王惠 ai-1020（20261022 gkx 换源重建）",
        "generated_at": "2026-10-22",
        "db": "gkx（三方库 183.240.141.251:3318，只读）；本脚本零 SQL，只读落盘快照",
        "scope": {
            "regions": CITIES,
            "patent_window": "2021→2024 年化 CAGR（两个真实完整年；2025/2026 不完整已剔除）",
            "paper_window": "2021-2023 均值 / 2018-2020 均值（2024 补录尖峰已剔除）",
            "new_actor_window": "2024+2025 新设家数 ÷ 万家企业（强度口径，非增速）",
            "transfer_window": "2021—2025 转让生效年（按年归属；跨境记录按权利人名称归城）",
        },
        "data_traps": {
            "patent_years": ("dwd_patent 仅 2021—2026；2021-2024 逐年 60.5/60.2/61.2/60.6 万件，"
                             "2025=440,401、2026=74,810 属采集截断；2017—2020 零行，不摊 0"),
            "paper_2024_spike": "dwd_zh_paper 2024 年 32,379 篇，为 2023 年 6,651 篇的 4.87 倍，属批量补录",
            "org_new_decay": "底册按成立年的新设家数近年单调下降（覆盖不足），故 D2 用强度不用增速",
        },
        "inputs": {
            "orgs_by_city": {c: org_n[c] for c in CITIES},
            "patent_by_year": {c: dict(sorted(pat_y[c].items())) for c in CITIES},
            "paper_by_year": {c: dict(sorted(pap_y[c].items())) for c in CITIES},
            "new_orgs_by_year": {c: dict(sorted(org_y[c].items())) for c in CITIES},
            "org_founding_year_missing": yr_missing,
            "transfer_in_by_city_year": {c: dict(sorted(tr_in[c].items())) for c in CITIES},
            "transfer_out_by_city_year": {c: dict(sorted(tr_out[c].items())) for c in CITIES},
        },
        "national": {
            "patent_by_year": pcy.get("year_coverage", {}).get("year_all", {}),
            "paper_by_year": {str(y): n for y, n in sorted(
                collections.Counter(p["year"] for p in S.papers() if p["year"]).items())},
            "four_city_orgs": sum(org_n[c] for c in CITIES),
            "org_rows": len(base),
            "four_city_patent_share_2021": round(
                sum(pat_y[c].get(2021, 0) for c in CITIES)
                / max(1, int(pcy.get("year_coverage", {}).get("year_all", {}).get("2021", 0))), 4),
            "four_city_patent_by_year": {str(y): round(sum(pat_y[c].get(y, 0) for c in CITIES), 2)
                                        for y in (2021, 2022, 2023, 2024)},
        },
        "derived": {
            "patent_cagr_2021_2024": dec(
                pat_cagr,
                {c: pat_y[c].get(2024) for c in CITIES},
                {c: pat_y[c].get(2021) for c in CITIES},
                "分城市字典。分子=该市 2024 年专利件数（dwd_patent app_year 面板 × 底册 name→city，"
                "重名按 1/k 计权）；分母=该市 2021 年专利件数；value=(2024 件数/2021 件数)^(1/3)−1，"
                "指数 3 = 2021 到 2024 的间隔年数。2025/2026 采集不完整，不进端点"),
            "paper_growth_2021_2023_vs_2018_2020": dec(
                pap_g,
                {c: round(mean([pap_y[c].get(y) for y in (2021, 2022, 2023)]), 2) for c in CITIES},
                {c: round(mean([pap_y[c].get(y) for y in (2018, 2019, 2020)]), 2) for c in CITIES},
                "分城市字典。分子=该市近窗 2021—2023 年均论文篇数；分母=该市基窗 2018—2020 年均篇数；"
                "value=分子/分母−1。两个均值另见 paper_window_means（同值两位小数）；"
                "value 用未舍入均值计算，按 4 位小数发布。2024 年属批量补录尖峰，两窗均已避开"),
            "paper_window_means": dec(
                {c: {"base_2018_2020": round(mean([pap_y[c].get(y) for y in (2018, 2019, 2020)]), 2),
                     "recent_2021_2023": round(mean([pap_y[c].get(y) for y in (2021, 2022, 2023)]), 2)}
                 for c in CITIES},
                {c: round(mean([pap_y[c].get(y) for y in (2021, 2022, 2023)]), 2) for c in CITIES},
                {c: round(mean([pap_y[c].get(y) for y in (2018, 2019, 2020)]), 2) for c in CITIES},
                "分城市字典。分子=近窗 2021—2023 年均论文篇数（value.recent_2021_2023）；"
                "分母=基窗 2018—2020 年均篇数（value.base_2018_2020）；"
                "每个窗口各为该市 dwd_zh_paper 三个整年篇数的算术平均，缺年不补"),
            "young_org_share_2019_2025": dec(
                young_share,
                {c: sum(org_y[c].get(y, 0) for y in range(2019, 2026)) for c in CITIES},
                {c: org_n[c] for c in CITIES},
                "分城市字典。分子=该市底册 2019—2025 年成立的企业数（org_y 逐年相加，7 个年份）；"
                "分母=该市底册企业总数 org_n。value 为比例（非百分数），未乘 100"),
            "new_org_intensity_per_10k": dec(
                new_intensity,
                {c: org_y[c].get(2024, 0) + org_y[c].get(2025, 0) for c in CITIES},
                {c: org_n[c] for c in CITIES},
                "分城市字典。分子=该市 2024+2025 年新设企业数（org_y 两年相加）；"
                "分母=该市底册企业总数 org_n；value=分子/分母×10,000（每万家企业新设强度）。"
                "用强度不用增速，规避底册近年覆盖衰减"),
            "transfer_count_2021_2025": dec(
                tr_cnt,
                {c: tr_cnt[c] for c in CITIES}, None,
                "计数，无分母：该市 2021—2025 生效年的专利转让件数（转入 tr_in + 转出 tr_out 相加）；"
                "权利人名称按底册 1/k 计权归属城市，故可为小数。件数≠交易笔数，一行一件"),
            "transfer_per_10k_orgs": dec(
                tr_per_10k,
                {c: tr_cnt[c] for c in CITIES},
                {c: org_n[c] for c in CITIES},
                "分城市字典。分子=该市 2021—2025 专利转让件数（转入+转出，见 transfer_count_2021_2025）；"
                "分母=该市底册企业总数 org_n；value=分子/分母×10,000（每万家转让件数）"),
        },
        "dims": {
            "D1_output_growth": d1,
            "D2_new_actor": d2,
            "D3_transfer": d3,
            "minmax_inputs": {"D1a_patent_cagr": mm_pat, "D1b_paper_growth": mm_pap,
                              "D2_new_intensity": mm_new, "D3_transfer_intensity": mm_tr},
        },
        "composite": comp,
        "rank": rank,
        "sensitivity": {
            "d2_alt_young_share": mm_young,
            "composite_alt": comp_alt,
            "rank_alt": rank_alt,
            "rank_changed": rank != rank_alt,
        },
        "transfer_coverage": {
            "transfer_rows": n_rows,
            "rows_with_effective_year": n_year_ok,
            "rows_any_side_matched": n_attributed,
            "rows_attributed_2021_2025": n_any_side_attr,
            "attribution_share": share_attr,
            "country_top": dict(country.most_common(6)),
            "note": ("dwd_patent_transfer 是**全球**专利转让记录（含 AU/BR/US 等），"
                     "只有权利人名称能与本地底册对上的记录可归属城市；"
                     "D3 只代表「本库主体参与的转让」，不代表区域全部技术交易。"),
        },
        "probes": {
            "org_rows": len(base),
            "patent_rows": 2939895,
            "paper_rows": S.paper_meta()["n"],
            "patent_panel_complete": pcy.get("panel_complete"),
            "patent_unmapped_rows": pcy.get("unmapped_rows"),
            "patent_unmapped_all_rows": pcy.get("unmapped_all_rows"),
        },
        "support_judgment": "部分支持",
        "support_reason": (
            "D1 的两个子项都可算（专利 CAGR 用 2021/2024 两个真实完整年，论文增幅用 2018-2020 对 2021-2023、"
            "四城均千级样本）；D2 已从『增速』降级为『新设强度』，规避底册近年覆盖衰减；"
            "但 D3 的属地可归率只有 %.2f%%（%d/%d 条转让记录至少一侧能对上本地底册），"
            "且转让表是按件离散记录、不含技术合同登记，无法支撑『区域技术交易活跃度』的完整口径。"
            "三维能算、一维量不足，按四档定义判部分支持。"
            % ((share_attr or 0) * 100, n_any_side_attr, n_rows)),
        "upgrade_path": ("补入国内专利转让/技术合同登记（带统一社会信用代码与生效日、"
                         "且覆盖非上市中小企业）后，D3 可升为完整口径，本指标可升为完全转换支持。"),
        "sources": [
            {"file": "code/_snapshots21/base_20261021.json",
             "content": "底册 189,116 行（org_id/名称/省/市/成立年）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_org_base_info"},
            {"file": "code/_snapshots_gkx21/city_patent_year_gkx.json",
             "content": "城市×年份专利件数（面板 app_year × 底册 name→city，重名 1/k 计权）",
             "source": "离线派生自 patent_panel_innov_20261021.json（gkx dwd_patent 全量 2,939,895 行）"},
            {"file": "code/_snapshots21/a25_paper_panel.json",
             "content": "中文论文 100,900 篇（含 author_info_list 与年份）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_zh_paper"},
            {"file": "code/_snapshots21/patent_transfer_rows_20261022.json",
             "content": "专利转让 22,809 行（转让前后权利人、生效日、国别）",
             "source": "gkx @ 183.240.141.251:3318 / dwd_patent_transfer（2026-10-22 直取）"},
        ],
        "elapsed_sec": None,
    }
    out.update(S.base_year_block(
        [2021, 2022, 2023, 2024, 2025], [],
        "专利侧只用 2021/2024 两个真实完整年做 CAGR 端点（dwd_patent 2017—2020 零行，"
        "缺失年不按 0 摊入分母）；论文侧基窗 2018—2020、近窗 2021—2023；"
        "新设强度用 2024—2025；转让用 2021—2025 生效年。2026 为残年，全部排除。"))
    out["elapsed_sec"] = round(time.time() - t0, 1)
    S.write_out(MID, out)

    print(json.dumps({"derived": out["derived"], "dims": out["dims"]["D1_output_growth"],
                      "D2": d2, "D3": d3, "composite": comp, "rank": rank,
                      "attr_share": share_attr, "transfers": [n_rows, n_any_side_attr]},
                     ensure_ascii=False, indent=1))
    print("orgs", dict(org_n), "elapsed", out["elapsed_sec"], "s")


if __name__ == "__main__":
    main()
