#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_TECH_DEEP_140_1 · 深圳技术发展重点布局领域推荐模型（20261022 三方库版）

口径（单一）：
  主体 = 深圳；领域 = 深圳「20+8」产业集群（28 个），IPC4 按 SZ208_MAP 的书写顺序做
  「确定性归属」（一个 IPC4 只进一个产业，避免并集重复计数）。专利窗口 2021—2024，按 pn 去重。
  全国只作 LQ 分母对照；深圳合计与全国合计分列。

推荐分 = 0.35·LQ(2024) + 0.25·2021→2024 增速 + 0.20·规模(log) + 0.20·政策供给，
四项各自 min-max 归一后加权；专家策略、科技项目、技术文献三维缺源，按缺口披露。

运行：python3 code/M_TECH_DEEP_140_1.py（零 SQL）
"""
from __future__ import annotations

import collections
import json
import math
import sys

sys.path.insert(0, ".")
import _tech21_scope as S  # noqa: E402

MID = "M_TECH_DEEP_140_1"


def main():
    sz, sz_year = S.load_sz_ipc()
    nat, nat_year = S.load_nat_ipc()

    # 每个 IPC4 的产业归属（确定性）
    all_prefixes = {p for ps in S.SZ208_MAP.values() for p in ps}
    dom_ind = {ipc: S.ipc_industry(ipc) for ipc in all_prefixes}
    # 深圳申请人名集合（用于产业主体数）
    sz_names = {g["nm"] for g in S.load_sz_groups()}

    app_cnt = collections.defaultdict(set)
    for ipc, nm, n in S.load_ipc_name():
        ind = dom_ind.get(ipc)
        if ind and nm in sz_names:
            app_cnt[ind].add(nm)

    pol_cnt, pol_total = S.industry_policy_counts()

    rows = []
    for ind in S.SZ208_MAP:
        ipcs = [p for p in S.industry_prefixes(ind) if dom_ind.get(p) == ind]
        s21 = sum(sz.get((p, 2021), 0) for p in ipcs)
        s24 = sum(sz.get((p, 2024), 0) for p in ipcs)
        n21 = sum(nat.get((p, 2021), 0) for p in ipcs)
        n24 = sum(nat.get((p, 2024), 0) for p in ipcs)
        if n24 <= 0:
            continue
        lq24 = (s24 / sz_year[2024]) / (n24 / nat_year[2024])
        rows.append({
            "industry": ind,
            "ipc4_n": len(ipcs),
            "ipc4": ipcs,
            "sz21": s21, "sz24": s24,
            "nat21": n21, "nat24": n24,
            "lq24": round(lq24, 4),
            "growth": round((s24 - s21) / s21, 4) if s21 else None,
            "n_applicants": len(app_cnt.get(ind, ())),
            "policy_hits": int(pol_cnt.get(ind, 0)),
        })

    # 只对 2021 与 2024 都为正的产业打分（增长率可算）
    scored = [r for r in rows if r["sz21"] > 0 and r["sz24"] > 0]
    lq_n = S.minmax([r["lq24"] for r in scored])
    g_n = S.minmax([r["growth"] for r in scored])
    sc_n = S.minmax([math.log1p(r["sz24"]) for r in scored])
    p_n = S.minmax([r["policy_hits"] for r in scored])
    for r, a, b, c, d in zip(scored, lq_n, g_n, sc_n, p_n):
        r["norm"] = {"lq": round(a, 4), "growth": round(b, 4), "scale": round(c, 4), "policy": round(d, 4)}
        raw = 100 * (0.35 * a + 0.25 * b + 0.20 * c + 0.20 * d)
        # 问题规避：相对劣势且绝对收缩的产业不进推荐位；LQ 仍高但四年跌超 20% 的产业降权 15%
        r["blocked"] = bool(r["lq24"] < 0.80 and (r["growth"] or 0) < 0)
        r["penalty"] = 0.85 if (r["growth"] is not None and r["growth"] <= -0.20) else 1.0
        r["score"] = round(raw * r["penalty"], 2)
    scored.sort(key=lambda r: -r["score"])
    for i, r in enumerate(scored, 1):
        r["rank"] = i

    recommend = [r for r in scored if not r["blocked"]][:8]
    watch = [r for r in scored if r["blocked"]]

    # 敏感性：等权、规模优先两套权重下的 Top5
    def top5(w):
        tmp = sorted(scored, key=lambda r: -sum(w[k] * r["norm"][k] for k in w) * r["penalty"])
        return [r["industry"] for r in tmp[:5]]

    sens = {
        "base_weights": top5({"lq": 0.35, "growth": 0.25, "scale": 0.20, "policy": 0.20}),
        "equal_weights": top5({"lq": 0.25, "growth": 0.25, "scale": 0.25, "policy": 0.25}),
        "scale_heavy": top5({"lq": 0.20, "growth": 0.20, "scale": 0.50, "policy": 0.10}),
        "policy_heavy": top5({"lq": 0.25, "growth": 0.20, "scale": 0.15, "policy": 0.40}),
    }

    mapped24 = sum(r["sz24"] for r in rows)
    all24 = sz_year[2024]
    payload = {
        "metric_id": MID,
        "metric_name": "深圳技术发展重点布局领域推荐模型",
        "caliber": {
            "主体": "深圳",
            "领域粒度": "深圳 20+8 产业集群 28 个；IPC4 确定性归属（一个域只进一个产业）",
            "专利窗口": "申请年 2021—2024，按 pn 去重，IPC 主分类前 4 位",
            "全国角色": "仅作 LQ 分母；深圳/全国合计分列，不混算",
            "政策口径": f"深圳市政策存量全表 {pol_total} 条，不按年截断（DATA_FACTS §3.7）",
            "映射覆盖": f"{mapped24:,}/{all24:,} = {mapped24 / all24:.2%}（2024 年深圳 IPC4 归属次）",
        },
        "base_years_used": [2021, 2022, 2023, 2024],
        "base_years_missing": S.MISSING_BASE_YEARS,
        "base_years_note": "dwd_patent 只有 2021—2026；2021 是唯一可用基期，2017—2020 不得按 0 摊入分母。",
        "weights": {"lq": 0.35, "growth": 0.25, "scale": 0.20, "policy": 0.20},
        "policy_total_sz": pol_total,
        "scored_industries": len(scored),
        "coverage": {
            "sz24_mapped": mapped24, "sz24_all": all24,
            "mapped_share": round(mapped24 / all24, 4),
            "unmapped_note": "SZ208_MAP 之外的 570 余个 IPC4 不进入产业级推荐；139 号件按 IPC4 单列覆盖。",
        },
        "ranking": scored,
        "recommend_top8": recommend,
        "blocked_industries": watch,
        "sensitivity": sens,
        "support_judgment": {
            "data_support_level": "部分支持",
            "criteria": {
                "技术优势(LQ)": "可算",
                "增长动能": "可算（2021→2024）",
                "创新主体规模": "可算（深圳申请人去重）",
                "政策供给": "可算（深圳市政策存量 + 关键词词典，推测口径）",
                "科技项目": "缺（dwd_zh_project 无领域/产业标签缓存，不能按产业汇总）",
                "技术文献": "缺（dwd_zh_paper 无 IPC/产业分类，作者单位只能定城市）",
                "专家策略": "缺（无专家登记表）",
            },
            "note": "专利+政策四维可算并给出推荐位；科技项目、技术文献、专家策略三维缺源，推荐分不含专家权重，判部分支持",
        },
    }
    S.write_out(MID, payload)

    print(json.dumps({k: payload[k] for k in ("caliber", "coverage", "weights")}, ensure_ascii=False, indent=1))
    print("scored", len(scored), "policy_total", pol_total)
    print("top8", [(r["industry"], r["score"], r["lq24"], r["growth"], r["sz24"], r["policy_hits"]) for r in recommend])
    print("blocked", [(r["industry"], r["lq24"], r["growth"]) for r in watch])
    print("sens", json.dumps(sens, ensure_ascii=False))


if __name__ == "__main__":
    main()
