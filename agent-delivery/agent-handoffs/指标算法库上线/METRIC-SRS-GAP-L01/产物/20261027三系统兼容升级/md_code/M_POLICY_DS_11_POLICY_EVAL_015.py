#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_DS_11_POLICY_EVAL_015 —— 实施路径与风险辅助（P1 政策评估族第一件）

口径来源
--------
无同 ID calc-logic 正本；注册表 `cfg_metric-POLICY-seed.yaml` 的 formula 为
`pending_cosign: human:唐绍祖（未签）`，临时读面写的是 `policy_simulate.curve/explanation`。
两库都没有 `policy_simulate` 可用数据（见 M_POLICY_SIMULATE 的否定性证据），
所以本件按需求原文自拟口径：从政策正文抽「实施环节提及」与「风险词提及」，
能算的只有「环节可见性」，时间进度表与关键节点不可算。

取数
----
零 SQL。读四个共享快照：
  _snapshots21/policy_base_20261021.json      20,000 条（id/title/city/level/body_len）
  _snapshots21/policy_content_20261021.json   18,763 条正文（[id,title,content,year,city]）
  _snapshots21/policy_struct_20261023.json    日期可用性 / 有效状态
  _snapshots21/policy_dims_20261023.json      层级 / 类型 / 城市分布
所有比例同时落分子与分母，正文数字可在本产物逐项复算。
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_POLICY_DS_11_POLICY_EVAL_015_out.json")

# ---------------------------------------------------------------- 词表
STAGES = [
    ("S1", "发布告知", ["印发", "发布", "公布", "现将", "通知", "公告"]),
    ("S2", "申报受理", ["申报", "受理", "申请", "报送", "申报材料", "提交材料"]),
    ("S3", "评审评估", ["评审", "论证", "审核", "审查", "专家评审"]),
    ("S4", "资金拨付", ["拨付", "补助", "资助", "补贴", "奖励", "经费"]),
    ("S5", "效果评估", ["绩效评价", "绩效考核", "验收", "考核", "后评估", "绩效目标"]),
]

RISKS = [
    ("R1", "合规追责", ["违规", "处罚", "追责", "惩戒", "失信"]),
    ("R2", "资金挪用", ["挪用", "截留", "虚报", "骗取", "挤占"]),
    ("R3", "执行不达", ["逾期", "未按期", "整改", "撤销", "中止", "终止"]),
    ("R4", "监督审计", ["监督管理", "监督检查", "审计", "抽查", "监督"]),
]

GENERIC = ["通知", "资金", "评估", "支持", "项目"]


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def pct(a, b, nd=4):
    return round(a * 100.0 / b, nd) if b else None


def main():
    base = load("policy_base_20261021.json")
    content = load("policy_content_20261021.json")
    struct = load("policy_struct_20261023.json")
    dims = load("policy_dims_20261023.json")
    fill = load("policy_field_fill_20261022.json")

    n_base = len(base)
    n_text = len(content)
    text_ids = {r[0] for r in content}
    title_only = [b["id"] for b in base if b["id"] not in text_ids]

    stage_hits = {code: 0 for code, _, _ in STAGES}
    stage_count_dist = {i: 0 for i in range(len(STAGES) + 1)}
    risk_hits = {code: 0 for code, _, _ in RISKS}
    risk_count_dist = {i: 0 for i in range(len(RISKS) + 1)}
    per_doc = []
    generic_tokens = {g: 0 for g in GENERIC}

    for r in content:
        pid, title, body = r[0], r[1] or "", r[2] or ""
        txt = title + "\n" + body
        s_codes = [code for code, _, ws in STAGES if any(w in txt for w in ws)]
        r_codes = [code for code, _, ws in RISKS if any(w in txt for w in ws)]
        for c in s_codes:
            stage_hits[c] += 1
        for c in r_codes:
            risk_hits[c] += 1
        stage_count_dist[len(s_codes)] += 1
        risk_count_dist[len(r_codes)] += 1
        for g in GENERIC:
            generic_tokens[g] += txt.count(g)
        per_doc.append((pid, len(s_codes), len(r_codes)))

    total_stage_marks = sum(stage_hits.values())
    total_risk_marks = sum(risk_hits.values())
    n_any_stage = n_text - stage_count_dist[0]
    n_any_risk = n_text - risk_count_dist[0]
    n_full5 = stage_count_dist[len(STAGES)]
    avg_stages = round(sum(k * v for k, v in stage_count_dist.items()) / n_text, 4)
    avg_risks = round(sum(k * v for k, v in risk_count_dist.items()) / n_text, 4)

    stage_rows = []
    for code, name, ws in STAGES:
        stage_rows.append({
            "code": code,
            "name": name,
            "lexicon": ws,
            "docs_hit": stage_hits[code],
            "denominator": n_text,
            "rate_pct": pct(stage_hits[code], n_text),
            "share_of_marks_pct": pct(stage_hits[code], total_stage_marks),
        })

    risk_rows = []
    for code, name, ws in RISKS:
        risk_rows.append({
            "code": code,
            "name": name,
            "lexicon": ws,
            "docs_hit": risk_hits[code],
            "denominator": n_text,
            "rate_pct": pct(risk_hits[code], n_text),
            "share_of_marks_pct": pct(risk_hits[code], total_risk_marks),
        })

    validity = struct["validity"]
    impl_nonnull = validity["implementation_date_nonnull"]
    expire_nonnull = validity["expire_date_nonnull"]
    pub_null = struct["publish_date"]["null_rows"]
    pub_bad = struct["publish_date"]["bad_zero_date_rows"]
    pub_usable = n_base - pub_null - pub_bad

    timeline_nodes_required = 5
    timeline_nodes_available = 1
    stage_dates_available = 0

    city_full = dims["city_dist"]
    city_profile = struct["city_profile"]
    bj = city_profile.get("北京市", {})
    sh = city_profile.get("上海市", {})

    def city_stage(pid_set):
        c_dist = {i: 0 for i in range(len(STAGES) + 1)}
        for pid, sc, _ in per_doc:
            if pid in pid_set:
                c_dist[sc] += 1
        n = sum(c_dist.values())
        return {
            "docs_with_content": n,
            "stage_full5": c_dist[len(STAGES)],
            "stage_full5_pct": pct(c_dist[len(STAGES)], n),
            "avg_stages": round(sum(k * v for k, v in c_dist.items()) / n, 4) if n else None,
            "stage_zero": c_dist[0],
        }

    by_level = {}
    level_of = {b["id"]: b.get("level") for b in base}
    for lv in sorted({b.get("level") for b in base}):
        ids = {pid for pid, sc, _ in per_doc if level_of.get(pid) == lv}
        by_level[str(lv)] = city_stage(ids)

    sz_ids = {r[0] for r in content if r[4] == "深圳市"}

    elements = [
        {
            "element": "落地路径图",
            "computable": True,
            "kind": "文本代理",
            "evidence": f"五环节文本提及率可算（{n_any_stage:,}/{n_text:,} 条至少命中一个环节），"
                        f"给出的是「环节是否被提及」，不是「真实流转路径」",
        },
        {
            "element": "时间进度表",
            "computable": False,
            "kind": "缺字段",
            "evidence": f"implementation_date 有效 0/{n_base:,}（全表 0000-00-00）、"
                        f"expire_date 有效 0/{n_base:,}；无环节级日期列，"
                        f"五个节点里只有 publish_date 可用（{pub_usable:,}/{n_base:,}）",
        },
        {
            "element": "关键节点",
            "computable": False,
            "kind": "缺字段",
            "evidence": "除发布日外没有任何节点日期或责任主体字段；"
                        "「关键节点」需要可排序的多个时间点，库内只有 1 个",
        },
        {
            "element": "风险分析",
            "computable": False,
            "kind": "文本代理（不可作风险清单）",
            "evidence": f"风险词只在 {n_any_risk:,}/{n_text:,} 条正文出现，"
                        f"无风险事件表、无风险等级、无责任主体；"
                        f"「提到风险」不等于「存在风险」",
        },
    ]
    computable_elements = sum(1 for e in elements if e["computable"])

    out = {
        "metric_id": "M_POLICY_DS_11_POLICY_EVAL_015",
        "metric_name_zh": "实施路径与风险辅助",
        "support_judgment": "部分支持",
        "verdict_kind": "partial_support",
        "judgment_reason": (
            "需求四要素里只有「落地路径」可用正文环节词做文本代理；"
            "时间进度表、关键节点、风险清单三要素缺日期字段与风险事件表，"
            "两库均无法构建。按四档定义属「始终有部分依赖维度无法得到足够数据」→ 部分支持。"
        ),
        "publishable": True,
        "registered_metric_value": None,
        "custom_thresholds": {
            "stage_lexicon_size": sum(len(ws) for _, _, ws in STAGES),
            "risk_lexicon_size": sum(len(ws) for _, _, ws in RISKS),
            "note": "五环节词表与四类风险词表为本件自拟，注册表 formula 为 pending_cosign（未签），"
                    "不得称为甲方口径或官方算法",
        },
        "population": {
            "policy_rows": n_base,
            "rows_with_content_snapshot": n_text,
            "rows_title_only": len(title_only),
            "content_chars": sum(len(r[2] or "") for r in content),
        },
        "population_context": {
            "content_nonempty_field_rows": fill["fields"]["content"]["nonempty"],
            "content_snapshot_gap_rows": fill["fields"]["content"]["nonempty"] - n_text,
            "policy_base_columns": 33,
            "innodb_table_rows_estimate": dims["known_estimate"]["information_schema_table_rows"],
            "city_null_rows": dims["city_dist"].get("__NULL__", 0),
            "province_null_rows": dims["province_dist"].get("__NULL__", 0),
            "province_null_national_rows": dims["national"]["province_null_national_rows"],
            "province_null_non_national_rows": dims["national"]["province_null_non_national_rows"],
            "level0_rows": dims["level_dist"].get("0", 0),
            "note": "分母口径的上下文：正文快照 18,763 与字段非空 19,203 差 440 行，"
                    "差额来源无元数据可还原，故文本类指标一律以 18,763 为分母（见正文 §2.1）",
        },
        "stages": stage_rows,
        "stage_count_dist": {str(k): v for k, v in sorted(stage_count_dist.items())},
        "stage_count_pct": {str(k): pct(v, n_text) for k, v in sorted(stage_count_dist.items())},
        "stage_summary": {
            "docs_any_stage": n_any_stage,
            "docs_any_stage_pct": pct(n_any_stage, n_text),
            "docs_all_five": n_full5,
            "docs_all_five_pct": pct(n_full5, n_text),
            "avg_stages_per_doc": avg_stages,
            "total_stage_marks": total_stage_marks,
            "single_stage_only": stage_count_dist[1],
            "single_stage_only_pct": pct(stage_count_dist[1], n_text),
        },
        "risks": risk_rows,
        "risk_count_dist": {str(k): v for k, v in sorted(risk_count_dist.items())},
        "risk_summary": {
            "docs_any_risk": n_any_risk,
            "docs_any_risk_pct": pct(n_any_risk, n_text),
            "avg_risk_classes_per_doc": avg_risks,
            "total_risk_marks": total_risk_marks,
        },
        "generic_word_watch": {
            "counts": generic_tokens,
            "note": "泛词（通知/资金/评估/支持/项目）在正文里的出现次数；"
                    "环节词命中里含相当比例的这类泛词，故环节率只能读成「文本可见性」",
        },
        "timeline": {
            "nodes_required": timeline_nodes_required,
            "nodes_available": timeline_nodes_available,
            "stage_level_date_columns": stage_dates_available,
            "publish_date_usable": pub_usable,
            "publish_date_null": pub_null,
            "publish_date_zero": pub_bad,
            "implementation_date_usable": impl_nonnull,
            "expire_date_usable": expire_nonnull,
            "implementation_zero_date_rows": n_base,
            "rule": "MySQL 零值日期 0000-00-00 不是 NULL；COUNT(col) 会返回 20,000 的假象，"
                    "必须 DATE_FORMAT 归一再判（DATA_FACTS §3.61）",
        },
        "elements": elements,
        "elements_computable": computable_elements,
        "elements_total": len(elements),
        "slices": {
            "shenzhen": {"policy_rows": city_full.get("深圳市", 0), **city_stage(sz_ids)},
            "beijing_impl_rows": bj.get("impl_rows"),
            "shanghai_impl_rows": sh.get("impl_rows"),
            "all_city_impl_rows": sum(v.get("impl_rows", 0) for v in city_profile.values()),
            "by_level": by_level,
        },
        "cross_checks": {
            "layout_171_not_substitute": "M_POLICY_LAYOUT_REC_COUNT 输出布局建议，无路径图/进度表/风险清单专出；"
                                         "按页面裁定不得以 171 mapped 顶替本叶",
            "bottleneck_166_not_substitute": "M_POLICY_DEEP_166_1 的「堵点」是文本焦点，不是方案实施风险",
            "text_parse_precision_caveat": "M_POLICY_TEXT_PARSE 已实测：20 条抽检 7 正确/8 部分/5 错，"
                                           "本件同样是词表法，精度不得高于该件",
        },
        "sources": [
            "code/_snapshots21/policy_base_20261021.json（gkx.dwd_policy_base 20,000 行窄投影）",
            "code/_snapshots21/policy_content_20261021.json（18,763 条正文）",
            "code/_snapshots21/policy_struct_20261023.json（日期可用性）",
            "code/_snapshots21/policy_dims_20261023.json（层级/类型/城市）",
            "gkx @ 183.240.141.251:3318（只读用户 gkx_reader_zp）",
        ],
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": "截面指标：以 20,000 条政策的当前快照为总体，按发布年跨 1981—2024 聚合不做时序，"
                           "故无基期年。正文里的年份分布只作描述，不进入任何分母。",
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"population={n_base} with_content={n_text} title_only={len(title_only)}")
    print("stages=", {s['name']: s['docs_hit'] for s in stage_rows})
    print(f"any_stage={n_any_stage} full5={n_full5} avg={avg_stages}")
    print("risks=", {r['name']: r['docs_hit'] for r in risk_rows})
    print(f"any_risk={n_any_risk} avg={avg_risks}")
    print("timeline nodes", timeline_nodes_available, "/", timeline_nodes_required)
    print("shenzhen", out["slices"]["shenzhen"])
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
