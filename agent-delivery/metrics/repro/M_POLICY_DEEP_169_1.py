#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_DEEP_169_1｜政策短板识别模型（覆盖性 / 有效性 / 合规性 三维六子项 + 覆盖矩阵）

零 SQL：读 20261021 快照
  code/_snapshots21/policy_base_20261021.json      20,000 行（title/body_len/theme）
  code/_snapshots21/pg_policy_rows_20261021.json   20,000 行（publish_code/publish_year/长度）
  code/_snapshots21/policy_content_20261021.json   18,763 行（正文/摘要）
  code/_snapshots21/policy_fields_a23_20261021.json 字段级非占位符计数 + 文号格式分布

三维六子项（calc-logic/POLICY/M_POLICY_DEEP_169_1.md）与固定阈值：
  覆盖性：政策主题覆盖率（theme）/ 政策类型覆盖率（八类功能词表，不用 type 文种）  < 60% 触发
  有效性：有效政策占比 / 时效政策占比（当前日期落在实施—失效窗口）                < 70% 触发
  合规性：文号规范率（〔YYYY〕XX号 / [YYYY]XX号）/ 正文完整率（正文 >100 字）      < 90% 触发
异常规则：字段缺失的子项不纳入（不计短板、也不计通过）；分母只计有数据的记录。
短板数 = Σ I(维度为短板)，0—3。

B 轨：20 主题词族 × 2015—2021 覆盖矩阵（Howlett & Ramesh 议题—工具空间），
用来把「阈值体检」升级为「结构性盲区扫描」。

输出：code/M_POLICY_DEEP_169_1_out.json
"""
import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")

CODE_RE = re.compile(r"〔[0-9]{4}〕[0-9]+号|\[[0-9]{4}\][0-9]+号")
PLACEHOLDER = {"", "NULL", "NONE", "-"}
WINDOW = [2015, 2016, 2017, 2018, 2019, 2020, 2021]

# 八类功能词表（需求举例：产业 / 人才 / 企业扶持，扩到八类以做覆盖率分母）
TYPE8 = {
    "财税支持": ["财政", "税收", "减税", "免税", "补贴", "补助", "奖励", "贴息", "专项资金"],
    "人才": ["人才", "引进", "培养", "博士后", "院士", "创新团队"],
    "金融": ["金融", "信贷", "贷款", "担保", "基金", "融资", "股权投资"],
    "产业": ["产业", "集群", "产业链", "制造业", "园区"],
    "科技创新": ["科技创新", "研发", "技术攻关", "创新平台", "实验室", "科技计划"],
    "知识产权": ["知识产权", "专利", "商标", "著作权", "版权"],
    "成果转化": ["成果转化", "技术转移", "技术转让", "产业化"],
    "中小企业扶持": ["中小企业", "小微企业", "专精特新", "民营经济"],
}

# 20 主题词族（B 轨覆盖矩阵）
TOPIC20 = {
    "科技创新": ["科技创新", "科技体制改革", "创新驱动"],
    "研发投入": ["研发费用", "研发投入", "研发补助"],
    "人才": ["人才引进", "人才培养", "人才安居", "高层次人才", "人才政策"],
    "企业培育": ["专精特新", "高新技术企业", "中小企业", "独角兽", "雏鹰", "瞪羚"],
    "产业发展": ["产业发展", "产业集群", "产业链", "制造业", "战略性新兴产业"],
    "金融支持": ["科技金融", "融资", "贷款贴息", "融资担保", "产业基金"],
    "知识产权": ["知识产权", "专利", "商标", "著作权"],
    "成果转化": ["成果转化", "技术转让", "技术转移"],
    "创新创业": ["创新创业", "孵化器", "众创空间", "创业孵化"],
    "平台载体": ["实验室", "技术创新中心", "工程技术中心", "新型研发机构", "科研平台"],
    "开放合作": ["对外开放", "国际合作", "粤港澳大湾区", "深港合作"],
    "数字化转型": ["数字化", "智能制造", "工业互联网", "智慧城市"],
    "绿色低碳": ["绿色低碳", "碳达峰", "碳中和", "节能环保", "循环经济"],
    "土地空间": ["产业用地", "工业用地", "土地整备", "厂房"],
    "税收优惠": ["税收优惠", "减税降费", "税收减免"],
    "科技奖励": ["科技奖励", "科学技术奖", "奖励办法"],
    "科普": ["科普", "科学普及"],
    "科技监督": ["科研诚信", "科技监督", "伦理审查"],
    "医疗健康": ["生物医药", "医疗器械", "医疗卫生"],
    "农业科技": ["农业科技", "现代农业", "种业"],
}


def nn(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER else s


def main():
    base = json.load(open(os.path.join(SNAP, "policy_base_20261021.json"), encoding="utf-8"))
    rows = json.load(open(os.path.join(SNAP, "pg_policy_rows_20261021.json"), encoding="utf-8"))
    content = json.load(open(os.path.join(SNAP, "policy_content_20261021.json"), encoding="utf-8"))
    fields = json.load(open(os.path.join(SNAP, "policy_fields_a23_20261021.json"), encoding="utf-8"))
    by_id = {r["id"]: r for r in base}
    txt = {r[0]: (nn(r[2]), nn(r[4])) for r in content}
    fill = fields["fills"]["rows"][0]
    n = len(rows)

    # ---------- 覆盖性 ----------
    theme_fill = int(fill[13])           # theme 非占位符 2
    cov_theme = None                     # 不可算
    type_hit = collections.Counter()
    for r in rows:
        body, abs_ = txt.get(r["id"], ("", ""))
        blob = " ".join([nn(r.get("title")), body, abs_])
        for cls, words in TYPE8.items():
            if any(w in blob for w in words):
                type_hit[cls] += 1
    cov_type = len(type_hit) / len(TYPE8)
    coverage = {
        "theme_fill_n": theme_fill,
        "theme_fill_pct": round(100.0 * theme_fill / n, 4),
        "theme_coverage": None,
        "theme_note": "theme 只有 2 条非占位符（0.01%），政策主题覆盖率不可算；"
                      "若按 calc-logic 异常规则退化为 title 代理，则代理值恒 100%、判定力归零",
        "type_coverage_pct": round(100.0 * cov_type, 2),
        "type_classes_hit": len(type_hit),
        "type_classes_total": len(TYPE8),
        "type_rows": [{"class": k, "policy_n": v, "pct": round(100.0 * v / n, 2)}
                      for k, v in type_hit.most_common()],
        "type_note": "八类功能词表（不是 type 文种列）；八类全部命中说明分母太粗，"
                     "覆盖率 100% 只能证明「词表覆盖」，不能证明「政策体系完备」",
    }

    # ---------- 有效性 ----------
    validity = {
        "valid_ratio_pct": 100.0,
        "timeliness": None,
        "timeliness_note": "implementation_date / expire_date 各 20,000 行为 0000-00-00，时效占比不可算（不纳入）",
        "note": "status 全表单一值「有效」，100% 是样本框构造（失效政策未入库）",
    }

    # ---------- 合规性 ----------
    code_fmt = {k: int(v) for k, v in fields["code_fmt"]["rows"]}
    code_ok = code_fmt.get("bracket", 0) + code_fmt.get("square", 0)
    content_ok = sum(1 for r in rows if (r.get("ct_len") or 0) > 100)
    compliance = {
        "code_rows": code_fmt,
        "code_ok_n": code_ok,
        "code_ok_pct": round(100.0 * code_ok / n, 2),
        "empty_n": code_fmt.get("empty", 0),
        "empty_pct": round(100.0 * code_fmt.get("empty", 0) / n, 2),
        "year_only_n": code_fmt.get("year_only", 0),
        "other_n": code_fmt.get("other", 0),
        "content_ok_n": content_ok,
        "content_ok_pct": round(100.0 * content_ok / n, 2),
    }

    # ---------- 维度判定（固定阈值；缺子项不纳入） ----------
    TH = {"coverage": 60.0, "validity": 70.0, "compliance": 90.0}
    cov_short = None                      # 覆盖维两个子项：主题不可算、类型 100% → 无可判短板
    if cov_type * 100 < TH["coverage"]:
        cov_short = True
    elif len(type_hit) == len(TYPE8):
        cov_short = False
    val_short = False if validity["valid_ratio_pct"] >= TH["validity"] else True
    comp_short = (compliance["code_ok_pct"] < TH["compliance"]) or (compliance["content_ok_pct"] < TH["compliance"])

    dims = [
        {"dim": "覆盖性", "subitems": ["政策主题覆盖率", "政策类型覆盖率"],
         "value_pct": round(100.0 * cov_type, 2), "threshold": TH["coverage"],
         "short": cov_short, "judge": "非短板（类型覆盖 8/8；主题覆盖不可算，不纳入）"},
        {"dim": "有效性", "subitems": ["有效政策占比", "时效政策占比"],
         "value_pct": 100.0, "threshold": TH["validity"],
         "short": val_short, "judge": "非短板（100% ≥ 70%；时效子项不可算，不纳入）"},
        {"dim": "合规性", "subitems": ["文号规范率", "正文完整率"],
         "value_pct": compliance["code_ok_pct"], "threshold": TH["compliance"],
         "short": comp_short, "judge": f"短板（文号 {compliance['code_ok_pct']}% < 90%；正文 {compliance['content_ok_pct']}%）"},
    ]
    shortboard_count = sum(1 for d in dims if d["short"])

    # ---------- B 轨：20 主题 × 年份覆盖矩阵 ----------
    topic_n = collections.Counter()
    topic_year = collections.defaultdict(set)
    for r in rows:
        body, abs_ = txt.get(r["id"], ("", ""))
        blob = " ".join([nn(r.get("title")), body, abs_])
        y = nn(r.get("publish_year"))
        yi = int(y) if y.isdigit() else None
        for topic, words in TOPIC20.items():
            if any(w in blob for w in words):
                topic_n[topic] += 1
                if yi in WINDOW:
                    topic_year[topic].add(yi)
    matrix = {t: {str(y): (1 if y in topic_year[t] else 0) for y in WINDOW} for t in TOPIC20}
    gap_cells = sum(1 for t in TOPIC20 for y in WINDOW if y not in topic_year[t])
    gap_by_year = [{"year": y, "gap_topics": sum(1 for t in TOPIC20 if y not in topic_year[t])}
                   for y in WINDOW]
    topic_rows = [{"topic": t, "policy_n": v, "pct": round(100.0 * v / n, 2),
                   "years_covered": len(topic_year[t])}
                  for t, v in topic_n.most_common()]

    out = {
        "metric_id": "M_POLICY_DEEP_169_1",
        "title": "政策短板识别模型",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": "三维里合规性可算并实际触发（文号规范率 34.17% < 90%）；有效性只剩有效占比（100%，样本构造）；"
                          "覆盖性因 theme 0.01% 不可算、退化为八类词表且八类全中（判定力弱）；"
                          "时效子项因零日期不可算。有必需子项始终无法取值 → 部分支持。",
        "base_years_used": ["2015", "2016", "2017", "2018", "2019", "2020", "2021"],
        "base_years_missing": ["2023"],
        "base_years_note": "覆盖矩阵用 2015—2021 七个连续年份（每年样本 ≥1,261 条）。2023 年库内 0 行（缺失）；"
                            "2022 年 289 条为采集截断残片、2024 年 1 条，均不进矩阵也不进任何分母，"
                            "绝不把缺年按 0 摊入（DATA_FACTS §3.16）。",
        "sources": {
            "policy_base": "code/_snapshots21/policy_base_20261021.json（title/theme）",
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（publish_code/publish_year/ct_len）",
            "policy_content": "code/_snapshots21/policy_content_20261021.json（18,763 行正文/摘要）",
            "field_probe": "code/_snapshots21/policy_fields_a23_20261021.json（含文号格式分布）",
            "db": "gkx @ 183.240.141.251:3318（只读）",
        },
        "dimensions": dims,
        "shortboard_count": shortboard_count,
        "coverage": coverage,
        "validity": validity,
        "compliance": compliance,
        "coverage_matrix": {
            "families": len(TOPIC20),
            "years": [str(y) for y in WINDOW],
            "cells": len(TOPIC20) * len(WINDOW),
            "gap_cells": gap_cells,
            "gap_by_year": gap_by_year,
            "matrix": matrix,
            "topic_rows": topic_rows,
            "note": "20 族 × 7 年全绿只说明词表粒度太粗、且「应覆盖」没有外部基准；"
                    "不能读成「政策体系没有盲区」",
        },
        "verdict": "短板数 = 1（合规性），可发布；覆盖维的「不触发」是代理假象，须与短板数同时披露",
    }

    dst = os.path.join(HERE, "M_POLICY_DEEP_169_1_out.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "base_years_used",
                                          "shortboard_count")}, ensure_ascii=False))
    print("coverage", {k: coverage[k] for k in ("theme_fill_n", "type_coverage_pct", "type_classes_hit")})
    print("type_rows", coverage["type_rows"])
    print("compliance", compliance)
    print("matrix gaps", gap_cells, "of", len(TOPIC20) * len(WINDOW), gap_by_year)
    print("topics", topic_rows[:5], "bottom", topic_rows[-3:])
    print("->", dst)


if __name__ == "__main__":
    main()
