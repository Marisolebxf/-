#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_POLICY_SHORTBOARD_COUNT 政策短板数
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_POLICY_SHORTBOARD_COUNT.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
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


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技信息展示系统']

# 缺省参数：三系统可传子集；快照/探针粒度上不可再分的参数会在 assumptions 显式声明
COMPAT_DEFAULTS = {
    "start_date": None,        # 算法库/展示常传；缺省 → 基线口径窗口（产物 base_years_*）
    "end_date": None,          # 同上；缺省 → 基线口径窗口
    "region": None,            # 地域过滤；缺省 → 全区域（基线口径）
    "industry_tag": None,      # 链/领域标签；缺省 → 全量（基线口径）
    "weights": None,           # 维度权重（模型型指标）；缺省 → 基线内置权重（Q014 类未定项不擅自赋值）
    "dims": None,              # 维度子集（模型型指标）；缺省 → 基线全维度
    "format": None,            # "detail"/"display"；缺省 → 两段都返回
}


def compute(params=None):
    """三系统统一入口：执行基线 main() 的计算逻辑，读取其产物并附兼容元数据返回。

    返回 dict：
      value / detail   : 主值与明细（透传基线产物 headline/stats，数值逐位=基线）
      display          : 展示系统友好结构（headline 精简 + 明细首层序列化）
      assumptions      : 本次运行采用的缺省假设（缺参时非空，前端可提示）
      applicable_systems / params_effective / metric_id / metric_name / generated_at
    典型调用：
      算法库  : compute({"start_date": ..., "end_date": ..., "region": ...})   全参
      专题系统: compute({}) 或 compute({"industry_tag": "..."})               少传参
      展示系统: compute({"format": "display"})                                只要展示段
    """
    import importlib.util, json as _json, time as _time
    from pathlib import Path as _Path

    p_in = dict(params or {})
    eff = {**COMPAT_DEFAULTS, **{k: v for k, v in p_in.items() if v is not None}}
    assumptions = []
    for k, v in eff.items():
        if v is not None and k in ("start_date", "end_date", "region", "industry_tag", "weights", "dims"):
            assumptions.append(f"{k}={v!r} 已接收：本件快照/探针粒度为基线口径，参数生效范围见同名 md「入参兼容策略」"
                               "（不可再分时返回基线口径值并在此声明）")
    assumptions.append("本件为 20261021 基线口径包装（兼容层不改数学定义）；三系统主值同源")

    t0 = _time.time()
    here = _Path(__file__).resolve().parent
    out_json = here / "M_POLICY_SHORTBOARD_COUNT_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_POLICY_SHORTBOARD_COUNT.py 等价）
        run_baseline()
    data = _json.loads(out_json.read_text(encoding="utf-8"))

    headline = data.get("headline") or {}
    value = headline.get("value") if isinstance(headline, dict) and "value" in headline else None
    if value is None and isinstance(headline, dict):
        value = next((headline[k] for k in ("total_le2024", "total", "sz_total", "score", "index", "n", "count")
                      if k in headline and isinstance(headline[k], (int, float))), None)
    if value is None:   # 无 headline 结构的产物：从顶层常见键提取（KPI/分布型）
        for k in ("total", "value", "n_total", "count", "org_total", "sz_total", "sum", "amount"):
            v = data.get(k)
            if isinstance(v, (int, float)):
                value = v
                break
            if isinstance(v, dict):
                for kk in ("total", "value", "n", "sz"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
                if value is not None:
                    break
    if value is None:   # 探针/分布型产物：从 population / audit_chain / probe 找主计数
        for sec in ("population", "audit_chain", "probe", "stats"):
            v = data.get(sec)
            if isinstance(v, dict):
                for kk in ("distinct_org_id", "total", "n", "count", "org_count", "rows",
                           "filled", "polar_rows", "chain_members_total"):
                    if isinstance(v.get(kk), (int, float)):
                        value = v[kk]
                        break
            if value is not None:
                break
    if value is None:   # 兜底声明：无单一主值（分布/明细型产物），value=None 属正常而非错误
        assumptions.append("本件为分布/明细型产物（无单一主值键），value=None；调用方请消费 detail/display 段")
    detail = {k: data[k] for k in ("stats", "facts", "population", "rule", "support_judgment",
                                   "base_years_used", "base_years_missing", "sources") if k in data}
    display = {"headline": headline, "rows_preview": None}
    for k in ("chains", "rows", "items", "list", "ranking", "detail_list"):
        if isinstance(data.get(k), list):
            display["rows_preview"] = {"key": k, "n": len(data[k]), "sample": data[k][:5]}
            break
    if eff.get("format") == "display":
        detail = {"support_judgment": data.get("support_judgment")}
    return {
        "metric_id": "M_POLICY_SHORTBOARD_COUNT",
        "metric_name": data.get("metric_name"),
        "applicable_systems": APPLICABLE,
        "params_effective": eff,
        "assumptions": assumptions,
        "value": value,
        "detail": detail,
        "display": display,
        "generated_at": _time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_sec": round(_time.time() - t0, 2),
        "baseline_generated_at": data.get("generated_at"),
    }


def run_baseline():
    """原样执行基线 main()（兼容层调用；产物 _out.json 由基线逻辑写盘，铁律：产物只由脚本产出）。"""
    main()  # noqa: F821  ← 基线入口（上方原代码定义）
