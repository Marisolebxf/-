#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_SHORTBOARD_COUNT｜政策短板清单条数（169 三维阈值口径的计数件，零 SQL）

KPI 定义：短板清单条数 = 触发阈值的「维度」数（0—3），与 M_POLICY_DEEP_169_1 的
shortboard_count 严格同口径，避免同一批政策在两个页面给出两个条数。

三维六子项（阈值固定，缺子项不纳入、不按 0 摊入）：
  覆盖性 主题覆盖率（theme 2 行 → 不可算）/ 类型覆盖率（八类功能词表）  < 60% 触发
  有效性 有效政策占比（status 单值 100%，样本构造）                     < 70% 触发
  合规性 文号规范率〔YYYY〕XX号 / [YYYY]XX号；正文完整率 >100 字          < 90% 触发

辅助视图（不计入 KPI）：方向级短板 = 在有 theme 的 5 个方向上按同一阈值判定；
对象覆盖缺口 = 5 个方向 / 301 个产业锚点环节，单列为结构性缺口。

数据：只读 code/_snapshots21，零 SQL。
"""
import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_POLICY_SHORTBOARD_COUNT_out.json")

CODE_STD = re.compile(r"〔[0-9]{4}〕[0-9]+号|\[[0-9]{4}\][0-9]+号")
PLACEHOLDER = {"", "NULL", "NONE", "-", "[]"}
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
TH = {"coverage": 60.0, "validity": 70.0, "compliance": 90.0}


def nn(v):
    if v is None:
        return ""
    s = str(v).strip()
    return "" if s.upper() in PLACEHOLDER or s == "null" else s


def load(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return json.load(f)


def theme_items(raw):
    raw = nn(raw)
    if not raw:
        return []
    if raw.startswith("["):
        try:
            return [str(x).strip() for x in json.loads(raw) if str(x).strip()]
        except Exception:
            return [x.strip(" \"'") for x in raw.strip("[]").split(",") if x.strip(" \"'")]
    return [raw]


def main():
    rows = load("pg_policy_rows_20261021.json")
    content = load("policy_content_20261021.json")
    fields = load("policy_fields_a23_20261021.json")
    aux = load("policy_aux_20261022.json")
    n = len(rows)
    txt = {r[0]: (nn(r[2]), nn(r[4])) for r in content}

    # ---- 覆盖性 ----
    theme_fill = int(fields["fills"]["rows"][0][13])
    type_hit = collections.Counter()
    for r in rows:
        body, abs_ = txt.get(r["id"], ("", ""))
        blob = " ".join([nn(r.get("title")), body, abs_])
        for cls, words in TYPE8.items():
            if any(w in blob for w in words):
                type_hit[cls] += 1
    type_cov = len(type_hit) / len(TYPE8) * 100

    # ---- 有效性 ----
    status = aux["probes"].get("status_dist") or {}
    valid_ratio = 100.0 * status.get("有效", 0) / n
    timeliness = None   # implementation/expire 全为 0000-00-00，不可算

    # ---- 合规性 ----
    code_fmt = {k: int(v) for k, v in fields["code_fmt"]["rows"]}
    code_ok_n = code_fmt.get("bracket", 0) + code_fmt.get("square", 0)
    code_ok_pct = 100.0 * code_ok_n / n
    content_ok_n = sum(1 for r in rows if (r.get("ct_len") or 0) > 100)
    content_ok_pct = 100.0 * content_ok_n / n

    dims = [
        {"dim": "覆盖性", "value_pct": round(type_cov, 2), "threshold": TH["coverage"],
         "short": type_cov < TH["coverage"],
         "basis": "类型覆盖 8/8；主题覆盖 theme 仅 2 行不可算（不纳入）"},
        {"dim": "有效性", "value_pct": round(valid_ratio, 2), "threshold": TH["validity"],
         "short": valid_ratio < TH["validity"],
         "basis": "status 单值「有效」=100%（样本框构造）；时效子项零日期不可算"},
        {"dim": "合规性", "value_pct": round(code_ok_pct, 2), "threshold": TH["compliance"],
         "short": (code_ok_pct < TH["compliance"]) or (content_ok_pct < TH["compliance"]),
         "basis": f"文号规范 {code_ok_pct:.2f}% / 正文完整 {content_ok_pct:.2f}%"},
    ]
    count = sum(1 for d in dims if d["short"])

    # ---- 方向级辅助视图（5 个 theme 方向，同一阈值） ----
    theme_rows = aux["probes"].get("theme_quote_rows", [])
    theme_fields = {r["id"]: r for r in aux["probes"].get("theme_row_fields", [])}
    by_id = {r["id"]: r for r in rows}
    dirs = {}
    for tr in theme_rows:
        pid = tr["id"]
        f = theme_fields.get(pid, {})
        for d in theme_items(tr.get("theme")):
            dirs.setdefault(d, []).append({"id": pid, "field": f, "base": by_id.get(pid, {})})

    dir_rows = []
    anchor = int(aux["probes"].get("industry_links_distinct") or 0)
    obj_gap = bool(anchor and len(dirs) < 8)
    for d, ps in sorted(dirs.items()):
        k = len(ps)
        vr = 100.0 * sum(1 for p in ps if nn(p["field"].get("status")) == "有效") / k
        cr = 100.0 * sum(1 for p in ps if CODE_STD.search(nn(p["field"].get("publish_code")))) / k
        tr = 100.0 * sum(1 for p in ps if int(p["field"].get("content_len") or 0) > 100) / k
        trig = []
        if obj_gap:
            trig.append("对象覆盖缺口(方向键 5 / 锚点 301)")
        if vr < TH["validity"]:
            trig.append(f"有效 {vr:.0f}% <70%")
        if cr < TH["compliance"]:
            trig.append(f"文号 {cr:.0f}% <90%")
        if tr < TH["compliance"]:
            trig.append(f"正文 {tr:.0f}% <90%")
        dir_rows.append({"direction": d, "n_policies": k, "valid_pct": round(vr, 1),
                         "code_std_pct": round(cr, 1), "content_ok_pct": round(tr, 1),
                         "triggers": trig, "short": bool(trig)})
    n_short_dirs = sum(1 for x in dir_rows if x["short"])

    obj_cov = 100.0 * len(dirs) / anchor if anchor else None

    out = {
        "metric_id": "M_POLICY_SHORTBOARD_COUNT",
        "title": "政策短板清单条数",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": ("三维里合规性可算并实际触发（文号 34.16% < 90%）；覆盖性的主题子项因 theme 仅 2 行"
                           "不可算、退化为八类词表后 100%；有效性的时效子项因零日期不可算。"
                           "有必需子项始终无法取值 → 部分支持。"),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("本指标为截面阈值计数，不设跨年基期。政策表年份不进入任何分母；"
                            "2023 年库内 0 行、2022 年后为采集残片，故不做「短板数逐年变化」的时序结论。"),
        "sources": {
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（ct_len/publish_year）",
            "policy_content": "code/_snapshots21/policy_content_20261021.json（18,763 行正文/摘要）",
            "field_probe": "code/_snapshots21/policy_fields_a23_20261021.json（文号格式分布/theme 填充）",
            "policy_aux": "code/_snapshots21/policy_aux_20261022.json（status 分布/行业链 301 环节）",
            "db": "gkx @ 183.240.141.251:3318（只读；本脚本零 SQL）",
        },
        "kpi_definition": "清单条数 = 触发阈值的维度数（0—3），与 M_POLICY_DEEP_169_1.shortboard_count 同口径",
        "population": {"rows": n, "status_dist": status,
                       "theme_fill_n": theme_fill, "rows_with_content_snapshot": len(txt)},
        "dimensions": dims,
        "shortboard_count": count,
        "coverage": {
            "theme_fill_n": theme_fill,
            "theme_coverage": None,
            "type_coverage_pct": round(type_cov, 2),
            "type_classes_hit": len(type_hit),
            "type_note": "八类词表全中只能证明词表覆盖，不能证明政策体系无盲区",
        },
        "validity": {
            "valid_ratio_pct": round(valid_ratio, 2),
            "timeliness": timeliness,
            "note": "status 单值「有效」；implementation_date / expire_date 全为 0000-00-00，时效不可判（不按 0 计入）",
        },
        "compliance": {
            "code_rows": code_fmt,
            "code_ok_n": code_ok_n,
            "code_ok_pct": round(code_ok_pct, 2),
            "empty_n": code_fmt.get("empty", 0),
            "content_ok_n": content_ok_n,
            "content_ok_pct": round(content_ok_pct, 2),
        },
        "direction_view": {
            "n_directions": len(dirs),
            "n_short_dirs": n_short_dirs,
            "rows": dir_rows,
            "note": "方向级按同一阈值判定，用于 171 的短板侧；它不是 KPI 条数，避免与 169 的维度计数混用",
        },
        "object_coverage_view": {
            "n_directions": len(dirs),
            "industry_anchor_links": anchor,
            "cover_pct": round(obj_cov, 4) if obj_cov is not None else None,
            "gap": bool(anchor and len(dirs) < 8),
            "note": "对象覆盖缺口为结构性信号，不计入三维阈值条数；171 引用它作为方向级短板触发条件",
        },
        "verdict": ("短板清单条数 = 1（合规性：文号规范率 34.16% < 90%）。"
                    "方向级辅助视图 5/5 触发（对象覆盖 + 文号），但其中对象覆盖是全局缺口，"
                    "不能重复加总；覆盖与有效的「不触发」是代理造成的，必须与条数同时披露。"),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "shortboard_count",
                                          "dimensions", "direction_view", "object_coverage_view")},
                     ensure_ascii=False, indent=1)[:3200])
    print("->", OUT)


if __name__ == "__main__":
    main()
