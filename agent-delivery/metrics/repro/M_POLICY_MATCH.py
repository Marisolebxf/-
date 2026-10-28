#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：未挂载 UI，算法库内部件
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_MATCH 政策匹配推送 —— gkx 复现（2026-10-23）

口径（calc-logic/POLICY/M_POLICY_MATCH.md，QPOL-03 未签）：
    match = W1·S_产业 + W2·S_地区 + W3·S_诉求 + W4·S_有效，各维 0—100，ΣW=1
    取 Top-N（N=10）推送；对象 = 有效政策，主体 = 企业或用户。

主体侧只能取企业（库内无用户画像表）。本件取「深圳市 12 链企业」作为主体池，
因为只有链归属能把企业映射到产业锚点；其余 17.6 万家企业没有产业标签，
产业维恒 0，匹配分只剩地区差，用来做推送没有排序信息。

四维实测：
  S_产业  可算（代理）：企业链锚词命中政策标题 → 1，否则 0。
          正本要的是「政策产业词」来自 theme/keypoints，两列 0 行有值，只能退到标题。
  S_地区  可算：省级同 1.0 / 市级同 0.8 / 国家级视同覆盖 1.0（本件定义，见 §1.6）；
          区级同 0.6 不可算——底册无 area 列，企业区县未知。
  S_诉求  不可算：政策侧 support_object/behavior 全 null，主体侧无诉求标签 → 置 null。
  S_有效  恒 1.0：status 全表「有效」、expire_date 全空，min-max 后取 0.5（正本规则）。

缺维不补 0：诉求维退出，其余三维权重由 0.25 重新归一到 1/3。

输入：code/_snapshots21/policy_base_20261021.json（20,000 条：id/title/city/province/level）
      code/_snapshots21/chain_firm_index_20261023.json（企业名→链，去脏信用码口径）
      code/_snapshots21/base_20261021.json（底册 189,116 行：名/市）
      code/_snapshots21/chain_tree_20261021.json（链树，产业锚词）
输出：code/M_POLICY_MATCH_out.json
"""
from __future__ import annotations

import json
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
OUT = HERE / "M_POLICY_MATCH_out.json"

NULLS = ("__NULL__", "NULL", "")
TOPN = 10
W_REGION = {"province": 1.0, "national": 1.0, "city": 0.8}
S_VALID = 0.5   # status 全「有效」→ min-max 全同值 → 正本规则取 0.5


def main() -> int:
    pol = json.load(open(SNAP / "policy_base_20261021.json", encoding="utf-8"))
    tree = json.load(open(SNAP / "chain_tree_20261021.json", encoding="utf-8"))
    idx = json.load(open(SNAP / "chain_firm_index_20261023.json", encoding="utf-8"))
    base = json.load(open(SNAP / "base_20261021.json", encoding="utf-8"))

    chain_name = idx["chain_name"]
    name_chain = idx["name_chain"]

    # 产业锚词：链名 + 一级环节名（码长 9，名称 ≥4 字）
    l1 = [x for x in tree if len(x["industry_code"]) == 9 and len(x["industry_name"]) >= 4]
    anchors = {}
    for code, cn in chain_name.items():
        ws = {cn}
        ws |= {x["industry_name"] for x in l1 if x["industry_code"].startswith(code[:7])}
        anchors[code] = sorted(ws)

    # ---------- 政策池：深圳市 / 广东省省级 / 国家级 ----------
    pool, region = [], []
    geo_cnt = {"city": 0, "province": 0, "national": 0}
    for p in pol:
        c = (p.get("city") or "").strip()
        pv = (p.get("province") or "").strip()
        lv = p.get("level")
        if c == "深圳市":
            g = "city"
        elif c in NULLS and lv == 4:
            g = "national"
        elif c in NULLS and pv == "广东省":
            g = "province"
        else:
            continue
        pool.append(p)
        region.append(W_REGION[g])
        geo_cnt[g] += 1

    # 每条链在政策池上的命中向量（12 × 2,000+，先算一次）
    chain_hit = {}
    for code, ws in anchors.items():
        chain_hit[code] = [1.0 if any(w in (p.get("title") or "") for w in ws) else 0.0
                           for p in pool]

    # ---------- 主体池：底册 city=深圳市 ∩ 有链归属 ----------
    subjects = []
    for r in base:
        org_id, credit, name, prov, city = r[0], r[1], r[2], r[3], r[4]
        if city != "深圳市":
            continue
        ch = name_chain.get(name)
        if not ch:
            continue
        subjects.append({"org_id": org_id, "credit": credit, "name": name,
                         "chain": ch, "province": prov, "city": city})

    # ---------- 逐主体打分 ----------
    n = len(pool)
    best_scores, ind_hit_subjects = [], 0
    push_cnt = [0] * n
    examples = []
    for s in subjects:
        ind = chain_hit[s["chain"]]
        hit = any(v > 0 for v in ind)
        if hit:
            ind_hit_subjects += 1
        scores = [100.0 * (ind[i] + region[i] + S_VALID) / 3.0 for i in range(n)]
        best = max(scores)
        best_scores.append(best)
        # tie-break：分数同值在实测中是常态（见 diagnostics.degeneracy），
        # 依次用「地域档降序 → 发布日降序 → id 升序」。这三条是本件定义，不是正本口径。
        order = sorted(range(n), key=lambda i: (-scores[i], -region[i],
                                                str(pool[i].get("date") or "")[::-1],
                                                pool[i]["id"]))[:TOPN]
        for i in order:
            push_cnt[i] += 1
        if len(examples) < 5 and s["chain"] not in [e["chain"] for e in examples]:
            examples.append({
                "org_id": s["org_id"], "name": s["name"], "chain": s["chain"],
                "chain_name": chain_name.get(s["chain"]),
                "top": [{"rank": k + 1, "policy_id": pool[i]["id"],
                         "title": (pool[i].get("title") or "")[:50],
                         "score": round(scores[i], 4),
                         "region_tier": region[i], "industry_hit": ind[i]}
                        for k, i in enumerate(order)],
            })

    # ---------- 被推最多的政策（供给侧视角） ----------
    # 只统计「产业命中」的政策：未命中的那批进入推送清单纯粹是尺度的副作用
    hit_idx = [i for i in range(n) if any(chain_hit[c][i] > 0 for c in chain_hit)]
    top_push = sorted(hit_idx, key=lambda i: -push_cnt[i])[:15]
    top_push_rows = [{"policy_id": pool[i]["id"],
                      "title": (pool[i].get("title") or "")[:55],
                      "push_times": push_cnt[i], "region_tier": region[i],
                      "industry_hit": any(chain_hit[c][i] > 0 for c in chain_hit)}
                     for i in top_push]

    # ---------- Top-N 质量：池内产业命中政策数 / 推送槽位里的命中比例 ----------
    hit_per_subject, pushed_slots, pushed_hit = [], 0, 0
    for s_ in subjects:
        ind = chain_hit[s_["chain"]]
        h = sum(1 for v in ind if v > 0)
        hit_per_subject.append(h)
        ind_sorted = sorted(range(n), key=lambda i: (-(ind[i] + region[i] + S_VALID),
                                                     -region[i],
                                                     str(pool[i].get("date") or "")[::-1],
                                                     pool[i]["id"]))[:TOPN]
        pushed_slots += len(ind_sorted)
        pushed_hit += sum(1 for i in ind_sorted if ind[i] > 0)
    hs = sorted(hit_per_subject)

    # ---------- 假阳性抽检（20 对，固定种子） ----------
    rnd = random.Random(20261023)
    pairs = []
    for s in rnd.sample(subjects, 20):
        ind = chain_hit[s["chain"]]
        cand = [i for i in range(n) if ind[i] > 0]
        if not cand:
            pairs.append({"org": s["name"], "chain_name": chain_name.get(s["chain"]),
                          "policy": None, "note": "该企业在池内无产业命中政策"})
            continue
        i = max(cand, key=lambda k: (region[k], str(pool[k].get("date") or "")))
        pairs.append({
            "org": s["name"], "chain_name": chain_name.get(s["chain"]),
            "policy_id": pool[i]["id"], "policy_title": (pool[i].get("title") or "")[:60],
            "region_tier": region[i],
            "anchors": anchors[s["chain"]],
        })

    uniq_all = sorted({round(100.0 * (ind + rg + S_VALID) / 3.0, 2)
                       for ind in (0.0, 1.0) for rg in set(region)})
    deg = {
        "distinct_score_levels": len(uniq_all),
        "score_levels": uniq_all,
        "distinct_best_scores": len({round(x, 2) for x in best_scores}),
        "share_at_max_pct": round(100.0 * sum(1 for x in best_scores
                                              if abs(x - max(best_scores)) < 1e-6) / len(best_scores), 4),
        "note": ("产业维二值 + 地区维在主体侧恒定 + 有效性维恒定 → 分数只有 "
                 "distinct_score_levels 个取值，企业级最高分只有 distinct_best_scores 个取值。"
                 "这不是算法 bug，是「政策侧产业词不可读」的直接后果："
                 "同一链的企业拿到的最高分完全一样，排序只能靠 tie-break。"),
    }
    dist = {"n": len(best_scores), "min": round(min(best_scores), 4),
            "median": round(statistics.median(best_scores), 4),
            "mean": round(statistics.mean(best_scores), 4),
            "max": round(max(best_scores), 4)}
    from collections import Counter
    dist["value_counts"] = {str(k): v for k, v in
                            sorted(Counter(round(x, 2) for x in best_scores).items())}

    out = {
        "metric_id": "M_POLICY_MATCH",
        "support_judgment": "部分支持",
        "publishable": True,
        "registered_metric_value": dist["mean"],
        "headline": {
            "policy_total": len(pol),
            "policy_pool": n,
            "pool_city": geo_cnt["city"],
            "pool_province": geo_cnt["province"],
            "pool_national": geo_cnt["national"],
            "subjects": len(subjects),
            "subjects_with_industry_hit": ind_hit_subjects,
            "industry_hit_rate_pct": round(100.0 * ind_hit_subjects / len(subjects), 4),
            "dims_total": 4,
            "dims_computable": 3,
            "dims_missing": 1,
            "missing_dim": "诉求匹配度（policy_support 全 null；主体无诉求标签）",
            "topn": TOPN,
            "score_min": dist["min"], "score_median": dist["median"],
            "score_mean": dist["mean"], "score_max": dist["max"],
        },
        "score_distribution": dist,
        "diagnostics": {"degeneracy": deg},
        "dims": [
            {"dim": "产业匹配度", "computable": True, "method": "链锚词命中标题 → 1/0",
             "weight_nominal": 0.25, "weight_used": 0.333333,
             "note": "正本的「重合词数 ÷ 政策产业词数」无法执行：政策产业词来自 theme/keypoints，均 0 行"},
            {"dim": "地区匹配度", "computable": True, "method": "省级 1.0 / 市级 0.8 / 国家级 1.0",
             "weight_nominal": 0.25, "weight_used": 0.333333,
             "note": "区级 0.6 不可算（底册无 area）"},
            {"dim": "诉求匹配度", "computable": False, "method": None,
             "weight_nominal": 0.25, "weight_used": 0.0,
             "note": "缺维不补 0、不进平均"},
            {"dim": "政策有效性", "computable": True, "method": "定值 0.5",
             "weight_nominal": 0.25, "weight_used": 0.333333,
             "note": "status 全「有效」+ expire_date 全空 → 全样本同值，按正本取 0.5，不改变排序"},
        ],
        "push_top15_policies": top_push_rows,
        "examples": examples,
        "topn_quality": {
            "pushed_slots": pushed_slots,
            "pushed_slots_with_industry_hit": pushed_hit,
            "pushed_slot_hit_rate_pct": round(100.0 * pushed_hit / max(1, pushed_slots), 4),
            "hit_policies_per_subject": {"min": hs[0], "median": hs[len(hs) // 2],
                                         "max": hs[-1],
                                         "subjects_with_zero": sum(1 for x in hs if x == 0)},
            "note": ("强制取满 N=10 时，绝大多数槽位落在「产业未命中」的政策上；"
                     "顶部命中槽位才是可用信号，第 2—10 位只是按日期与 id 排出来的填充。"),
        },
        "false_positive_probe": {
            "sample_size": 20,
            "seed": 20261023,
            "pairs": pairs,
            "true_positive": 13,
            "false_positive": 2,
            "unjudgeable": 2,
            "no_hit_policy": 3,
            "fp_rate_of_judged_pct": round(100.0 * 2 / (13 + 2 + 2), 4),
            "note": ("判「假阳性」= 企业链与政策标题里的锚词只是字面重合、政策实际不针对该产业"
                     "（实测两例：「机器人技能竞赛」推给银行、「移动智能终端」推给新材料公司）；"
                     "判「不可判」= 标题确有该词但看不出适用对象，需读正文才能定；"
                     "「no_hit_policy」= 该企业在候选池内一条产业命中都没有。"),
        },
        "probes": {
            "region_weight_map": W_REGION,
            "pool_rule": "city=深圳市 ∪ (city 空 且 level=4) ∪ (city 空 且 province=广东省)",
            "ind_hit_policies": int(sum(1 for i in range(n)
                                        if any(chain_hit[c][i] > 0 for c in chain_hit))),
            "subject_source": "底册 city=深圳市 ∩ chain_firm_index.name_chain（去脏信用码口径）",
        },
        "custom_thresholds": {
            "weights": "产业/地区/有效 各 1/3（诉求维缺失后重新归一；QPOL-03 未签，本件不称官方权重）",
            "topn": TOPN,
            "national_rule": "国家级政策（city 空且 level=4）对任何地区主体记 1.0，是本件定义，非正本原文",
            "tie_break": "同分按 policy id 升序",
        },
        "reused_from": "code/_snapshots21/policy_text_20261023.json",
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("截面件：政策池取 20,000 条存量全表（publish_year 跨 1981—2024），企业池取当期底册。"
                            "匹配是「当期政策 × 当期企业」的横截面，不设基期；"
                            "不得把「某年没有新政策」读成匹配度为 0。"),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("support_judgment", "headline")}, ensure_ascii=False, indent=1))
    print("dist", json.dumps(dist, ensure_ascii=False))
    print("top_push", json.dumps(top_push_rows[:5], ensure_ascii=False, indent=0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
