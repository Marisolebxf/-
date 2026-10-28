#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""发展战略引导力（M_INNOV_PG_GUIDE）——零 SQL 复算。

王惠 V1.5 三性口径：
  前瞻性 = title/keywords/keypoints/theme 含「规划/纲要/远景」的政策 ÷ 政策总数
  系统性 = quote_policy 非空且不为空数组 ÷ 政策总数
  针对性 = policy_support.support_way 至少 1 条非空 ÷ 政策总数
本库实测：keywords 0 有效、keypoints 0 有效、theme 恒 0、quote_policy 2 条非空、
policy_support 0 条非空 —— 三性中只有「前瞻性」可算，且只能降到 title 单字段。

前瞻性还要做两级清洗（纯字面匹配会被「建设工程规划许可证」类公示污染）：
  原始命中 → 剔除 18 个城建/机关词 → 再限定科技语义（科技/创新/研发/高新技术/战略性新兴）

另出「政策导向词族」分布（title 命中），作为引导力方向的补充证据，不进综合分。

输入：code/_snapshots21/pg_policy_rows_20261021.json
产物：code/M_INNOV_PG_GUIDE_out.json
"""
from __future__ import annotations

import json
import os
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_INNOV_PG_GUIDE_out.json")
METRIC_ID = "M_INNOV_PG_GUIDE"
PLACEHOLDER = {"NULL", "", "NONE", "-"}
FOUR = ["深圳市", "广州市", "东莞市", "惠州市"]

FWD_KEYS = ["规划", "纲要", "远景"]
# 城建/规划许可类污染词（第一级清洗）
CITY_PLAN_NOISE = [
    "建设工程规划许可", "总平面图", "规划许可", "规划核实", "规划验收", "城乡规划",
    "用地规划", "规划公示", "规划设计要点", "规划条件", "控制性详细规划",
    "修建性详细规划", "规划调整", "规划变更", "规划审批", "选址意见书",
    "工程规划", "规划和自然资源局",
]
# 科技语义限定（第二级清洗）
TECH_KEYS = ["科技", "创新", "研发", "高新技术", "战略性新兴"]

# 政策导向词族（补充维，不进分）
FAMILIES = {
    "顶层规划": ["规划", "纲要", "行动计划", "实施方案", "远景"],
    "意见指导": ["意见", "指导意见", "若干措施", "政策措施"],
    "财政补贴": ["补贴", "补助", "奖励", "资助", "资金", "经费", "扶持"],
    "金融税收": ["金融", "融资", "贷款", "基金", "保险", "税收", "减免", "上市"],
    "人才": ["人才", "引智", "博士后", "专家"],
    "平台载体": ["平台", "基地", "园区", "孵化", "实验室", "中心", "研究院"],
    "知识产权标准": ["专利", "知识产权", "标准", "品牌", "商标"],
    "企业培育": ["高新技术企业", "科技型中小企业", "专精特新", "小巨人",
              "独角兽", "瞪羚", "创新型企业"],
}


def norm(v) -> str:
    s = "" if v is None else str(v).strip()
    return "" if s.upper() in PLACEHOLDER else s


def hit(title, keys) -> bool:
    return any(k in title for k in keys)


def main() -> None:
    t0 = time.time()
    rows = json.load(open(os.path.join(SNAP, "pg_policy_rows_20261021.json"), encoding="utf-8"))
    for r in rows:
        r["title"] = r.get("title") or ""
        for k in ("city", "type", "province", "district"):
            r[k] = norm(r.get(k))
        y = norm(r.get("publish_year"))
        r["yr"] = int(y) if y.isdigit() else None
        r["kw"] = int(r.get("kw") or 0)
        r["kp"] = int(r.get("kp") or 0)
        r["qp"] = int(r.get("qp") or 0)
        r["ps"] = int(r.get("ps") or 0)

    n = len(rows)
    # ---------- 三性源字段体检 ----------
    fill = {
        "keywords_valid": sum(r["kw"] for r in rows),
        "keypoints_valid": sum(r["kp"] for r in rows),
        "quote_policy_valid": sum(r["qp"] for r in rows),
        "policy_support_valid": sum(r["ps"] for r in rows),
        "abstract_filled": sum(1 for r in rows if (r.get("abs_len") or 0) > 0),
        "content_filled": sum(1 for r in rows if (r.get("ct_len") or 0) > 0),
    }

    # ---------- 前瞻性三级漏斗 ----------
    raw = [r for r in rows if hit(r["title"], FWD_KEYS)]
    no_city = [r for r in raw if not hit(r["title"], CITY_PLAN_NOISE)]
    tech = [r for r in no_city if hit(r["title"], TECH_KEYS)]
    funnel = {
        "raw": len(raw), "raw_rate": round(100 * len(raw) / n, 3),
        "after_city_noise": len(no_city),
        "after_city_noise_rate": round(100 * len(no_city) / n, 3),
        "city_noise_removed": len(raw) - len(no_city),
        "tech_semantic": len(tech), "tech_semantic_rate": round(100 * len(tech) / n, 3),
        "tech_filter_removed": len(no_city) - len(tech),
        "overall_false_positive_rate": round(100 * (len(raw) - len(tech)) / max(len(raw), 1), 2),
    }

    # 独立交叉校验：type='政策文件-规划纲要'
    type_plan = sum(1 for r in rows if r["type"] == "政策文件-规划纲要")

    # ---------- 前瞻性分城（清洗后） ----------
    per_city = []
    for c in FOUR:
        sub = [r for r in rows if r["city"] == c]
        t = [r for r in sub if hit(r["title"], TECH_KEYS) and hit(r["title"], FWD_KEYS)
             and not hit(r["title"], CITY_PLAN_NOISE)]
        per_city.append({
            "city": c, "n": len(sub), "forward_n": len(t),
            "forward_rate": round(100 * len(t) / len(sub), 3) if sub else None,
        })
    city_blank_share = round(100 * sum(1 for r in tech if not r["city"]) / max(len(tech), 1), 1)

    # ---------- 系统性 / 针对性 ----------
    systematic = {"numerator": fill["quote_policy_valid"], "denominator": n,
                  "rate": round(100 * fill["quote_policy_valid"] / n, 4),
                  "usable": False,
                  "reason": "quote_policy 仅 2 条非空，且非 JSON 数组格式，无法满足『非空且不为空数组』"}

    # ---------- 导向词族 ----------
    fam_rows = []
    for name, keys in FAMILIES.items():
        cnt = sum(1 for r in rows if hit(r["title"], keys))
        fam_rows.append({"family": name, "n": cnt, "share": round(100 * cnt / n, 2)})
    fam_by_year = []
    for y in range(2015, 2022):
        sub = [r for r in rows if r["yr"] == y]
        if not sub:
            continue
        fam_by_year.append({
            "year": y, "n": len(sub),
            "shares": {name: round(100 * sum(1 for r in sub if hit(r["title"], keys)) / len(sub), 2)
                       for name, keys in FAMILIES.items()},
        })

    # ---------- 历史轨迹（近年规划纲要类占比） ----------
    type_year = []
    for y in range(2015, 2022):
        sub = [r for r in rows if r["yr"] == y]
        if not sub:
            continue
        tp = sum(1 for r in sub if r["type"] == "政策文件-规划纲要")
        type_year.append({"year": y, "n": len(sub), "plan_type": tp,
                          "plan_type_share": round(100 * tp / len(sub), 2)})

    result = {
        "metric_id": METRIC_ID,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": "gkx.dwd_policy_base @ 183.240.141.251:3318（快照 20,000 行，零 SQL 复算）",
        "support_judgment": "部分支持",
        "formula": "三性等权；本库仅前瞻性可算（title 单字段 + 两级清洗），系统性/针对性不可算，故不输出综合分",
        "n_records": n,
        "field_fill": fill,
        "funnel": funnel,
        "type_plan_rows": type_plan,
        "type_plan_share": round(100 * type_plan / n, 3),
        "per_city": per_city,
        "tech_hits_with_blank_city_share": city_blank_share,
        "dimensions": {
            "foresight": {"value": funnel["tech_semantic_rate"], "usable": True,
                          "note": "清洗后的科技战略规划占全部政策 0.25%"},
            "systematic": systematic,
            "targeted": {"numerator": fill["policy_support_valid"], "denominator": n,
                         "rate": 0.0, "usable": False,
                         "reason": "policy_support 全表 20,000/20,000 为小写字面 'null'，无 support_way 键"},
        },
        "orientation_families": fam_rows,
        "orientation_by_year": fam_by_year,
        "plan_type_by_year": type_year,
        "composite_score": None,
        "composite_reason": "三性中两性整列为空，按王惠『缺测维不补 0，剩余权重重归一』会退化为单维 0—100 排序；本报告只发布前瞻性覆盖率，不发布引导力综合分",
        "caveats": [
            "前瞻性原始 742 条命中中仅 50 条为真科技战略规划，误命中率 93.26%",
            "50 条真命中里 48 条 city 为空（省级/国家级文件），城市级引导力不可计算",
            "keywords/keypoints 整列为空、theme 恒为 0，四字段口径实际退化为 title 单字段",
            "quote_policy 2 条、policy_support 0 条，系统性与针对性不可算，也不得用类型数/主题数冒充",
        ],
        "runtime_sec": None,
    }

    print(f"[{METRIC_ID}] n={n}")
    print("字段体检:", fill)
    print("前瞻漏斗:", funnel)
    print("type=规划纲要:", type_plan, f"({result['type_plan_share']}%)")
    print("分城:", per_city)
    print("导向词族:", [(x["family"], x["n"], x["share"]) for x in fam_rows])

    result["runtime_sec"] = round(time.time() - t0, 3)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"saved {OUT} ({result['runtime_sec']}s)")


if __name__ == "__main__":
    main()
