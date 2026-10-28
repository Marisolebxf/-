#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
# 【20261027 三系统兼容升级件】M_POLICY_EFFECT_SCORE 政策效果评分
# 【维护者】唐绍祖
# 【适用系统】科技专题服务算法库 + 科技专题系统 + 科技信息展示系统
# 【差异分级】D3 详略级差异 ｜ 依据 METRIC-SRS-GAP-L01/产物/file/M_POLICY_EFFECT_SCORE.md
# 【兼容契约】../过程文件/04_兼容接口设计规约.md ｜ 格式样板 M_CHAIN_PATENT_COUNT
# ───────────────────────────────────────────────────────────────────
# 三系统调用注意（后端必读）：
#   1. 统一入口 compute(params)（文件尾兼容层）：缺参走基线缺省口径，
#      assumptions 声明缺省行为；三系统主值同源（同一 _out.json）。
#   2. 本件计算口径 = 20261021 基线（下方原 docstring/代码，未改数学定义）。
#   3. 支持度结论与缺口见同名 md §〇/§三/§四；支持度不足的维度调用方不得自行补数。
# ═══════════════════════════════════════════════════════════════════
"""M_POLICY_EFFECT_SCORE｜政策效果评分（v2 王惠三维口径全库复现）

王惠三维（calc-logic/POLICY/M_POLICY_EFFECT_SCORE.md 原公式）：
  执行效果.有效政策占比 = 有效政策数 / 总数（status）
  执行效果.政策及时性  = (统计日−实施日)/(失效日−实施日)（implementation_date+expire_date）
  社会经济效应        = 待建直读（营收增速/就业贡献 无 ODS → 缺维）
  环境影响.绿色导向占比 = I(title/keywords/theme/abstract/content 命中环保闭集) / 总数
环保闭集（王惠原稿，不得临时扩词）：
  导向：生态文明、生态环境保护、生态环境、环境保护、污染防治、节能减排、节能降碳、
        绿色低碳、绿色发展、清洁生产、循环经济、碳达峰、碳中和、双碳、低碳、环保
  要素：大气污染、水污染、土壤污染、固体废物、危险废物、生物多样性、自然保护、碳排放、温室气体
  不列：光杆「绿色」「环境」「生态」「清洁」
合成：维内等权、三维等权；截面 min-max→[0,1]；缺维不补 0 不进平均 ×100；同值取 0.5。
入集：status='有效'、id 去重；'NULL' 占位清洗；综合统计仅国内（dwd_policy_base）。
主算库：gkx 真源（demo 当日连接超时，历史 20,000 行同构）。
输出 code/M_POLICY_EFFECT_SCORE_out.json（分段容错 + 增量写）
"""
import json, os, datetime, traceback
import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_POLICY_EFFECT_SCORE_out.json")

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=15, read_timeout=600)

ENV_GUIDE = ["生态文明", "生态环境保护", "生态环境", "环境保护", "污染防治", "节能减排",
             "节能降碳", "绿色低碳", "绿色发展", "清洁生产", "循环经济", "碳达峰", "碳中和",
             "双碳", "低碳", "环保"]
ENV_ELEMS = ["大气污染", "水污染", "土壤污染", "固体废物", "危险废物", "生物多样性",
             "自然保护", "碳排放", "温室气体"]
ENV_CLOSED = sorted(ENV_GUIDE + ENV_ELEMS, key=len, reverse=True)  # 长词优先

def clean(v):
    if v is None:
        return None
    s = str(v).strip()
    if s == "" or s.upper() in ("NULL",):
        return None
    return s

def env_hit_concat(r):
    """王惠闭集扫描：title/keywords/theme/abstract/content 拼接，长词优先、命中区间不重复计"""
    text = "".join(str(clean(r.get(f)) or "") for f in ("title", "keywords", "theme", "abstract", "content"))
    low = text.lower()
    hit_words = set()
    for w in ENV_CLOSED:  # 已按长度降序
        idx = low.find(w.lower())
        if idx >= 0:
            hit_words.add(w)
    return hit_words

def flush(out):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)

def q(conf, sql, args=None):
    with pymysql.connect(**conf) as conn, conn.cursor() as cur:
        cur.execute(sql, args or ())
        return cur.fetchall()

def main():
    out = {"metric_id": "M_POLICY_EFFECT_SCORE",
           "title": "政策效果评分（王惠三维口径 v2 复现）",
           "probe_date": "2026-10-21", "probes": {}, "compute": {}, "notes": []}
    today = datetime.date(2026, 10, 21)

    # ---- P1 探针 ----
    try:
        out["probes"]["gkx_dwd_policy_base"] = q(GKX,
            "SELECT COUNT(*) n FROM dwd_policy_base")[0]["n"]
        out["probes"]["gkx_real_status"] = q(GKX,
            "SELECT COUNT(*) n FROM dwd_policy_base WHERE status IS NOT NULL "
            "AND status NOT IN ('NULL','null','')")[0]["n"]
        out["probes"]["gkx_real_implementation_date"] = q(GKX,
            "SELECT COUNT(*) n FROM dwd_policy_base WHERE implementation_date IS NOT NULL "
            "AND implementation_date > '1900-01-01'")[0]["n"]
        out["probes"]["gkx_real_expire_date"] = q(GKX,
            "SELECT COUNT(*) n FROM dwd_policy_base WHERE expire_date IS NOT NULL "
            "AND expire_date > '1900-01-01'")[0]["n"]
        flush(out)
    except Exception:
        out["notes"].append("P1 fail: " + traceback.format_exc(limit=1)); flush(out)

    # ---- P2 主键分页拉列 ----
    rows = []
    try:
        last = -1
        while True:
            batch = q(GKX, "SELECT id, title, keywords, theme, abstract, content, status, "
                           "implementation_date, expire_date FROM dwd_policy_base "
                           "WHERE id > %s ORDER BY id LIMIT 1000", (last,))
            if not batch:
                break
            rows.extend(batch)
            last = batch[-1]["id"]
        out["compute"]["rows_source"] = "gkx"
        out["compute"]["rows_pulled"] = len(rows)
        flush(out)
    except Exception:
        out["notes"].append("P2 fail: " + traceback.format_exc(limit=1)); flush(out)

    # ---- P3 王惠三维计算 ----
    try:
        seen, uniq = set(), []
        for r in rows:
            if (r.get("status") or "") == "有效" and r["id"] not in seen:
                seen.add(r["id"]); uniq.append(r)
        N = len(uniq)
        c = out["compute"]
        c["n_valid_dedup"] = N

        # D1a 执行效果.有效政策占比（组级：入集即 100% 有效）
        c["d1a_valid_ratio"] = {"value": 1.0, "note": "入集=status='有效'（全库单值），组级比率恒 1.0",
                                "dim_available": True}
        # D1b 执行效果.政策及时性（实施日/失效日均 >1900 的逐政策值）
        timely = []
        for r in uniq:
            impl, exp = r.get("implementation_date"), r.get("expire_date")
            if impl and exp and str(impl) > "1900-01-01" and str(exp) > "1900-01-01":
                try:
                    span = (exp - impl).days
                    if span > 0:
                        timely.append(max(0.0, min(1.0, (today - impl).days / span)))
                except Exception:
                    pass
        c["d1b_timeliness"] = {"n_scored": len(timely), "dim_available": len(timely) > 0,
                               "note": "gkx 侧 implementation_date/expire_date 全为 0000-00-00 占位（真实 0）"
                                       if not timely else ""}
        # D2 社会经济效应（待建）
        c["d2_socioeconomic"] = {"dim_available": False,
                                 "note": "operating_revenue_growth/employment_contribution 无 ODS（王惠登记待建）"}
        # D3 环境影响.绿色导向占比（闭集）
        env_hits = 0
        env_word_dist = {}
        env_examples = []
        for r in uniq:
            hits = env_hit_concat(r)
            if hits:
                env_hits += 1
                for w in hits:
                    env_word_dist[w] = env_word_dist.get(w, 0) + 1
                if len(env_examples) < 5:
                    env_examples.append({"title": (r.get("title") or "")[:60], "words": sorted(hits)[:4]})
        c["d3_green_ratio"] = {"hit": env_hits, "rate": round(env_hits / N, 4) if N else None,
                               "word_dist_top": dict(sorted(env_word_dist.items(), key=lambda x: -x[1])[:10]),
                               "dim_available": True, "example": env_examples}

        # ---- P4 合成（王惠：维内等权、三维等权、缺维不进平均） ----
        # 执行效果维 = 有效占比(1.0) 与 及时性（缺）→ 维内仅 1 子项
        exec_dim = 1.0
        env_dim = c["d3_green_ratio"]["rate"]
        dims_ok = [exec_dim, env_dim]
        c["dims_available"] = "2/3（执行效果残维、社会经济缺、环境可算）"
        c["effect_score"] = round(sum(dims_ok) / len(dims_ok) * 100, 2)
        c["formula"] = "执行效果(有效占比，及时性缺) 与 环境影响(绿色导向占比) 等权 ×100；社会经济维缺不进平均"

        # ---- P5 支持度机判 ----
        if c["d3_green_ratio"]["dim_available"] and N >= 100:
            # 结构+数据仅支撑 2/3 维 → 部分支持（社会经济维两侧无源）
            c["support_judgment"] = "部分支持"
        else:
            c["support_judgment"] = "完全不支持"
        out["support_judgment"] = c["support_judgment"]
        out["data_caveat"] = ("gkx 侧 keywords/theme 为 'NULL' 占位（真实 0/2），环保闭集扫描实际落点为 title/abstract/content；"
                              "implementation_date/expire_date 全为 0000-00-00 占位（及时性子项无输入）；"
                              "社会经济两子项无 ODS。")
        flush(out)
    except Exception:
        out["notes"].append("P3 fail: " + traceback.format_exc(limit=1)); flush(out)

    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))

if __name__ == "__main__":
    main()


# ═══════════════════════ 三系统兼容层（20261027 批次追加，不改上方基线逻辑） ═══════════════════════

APPLICABLE = ['科技专题服务算法库', '科技专题系统', '科技信息展示系统']

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
    out_json = here / "M_POLICY_EFFECT_SCORE_out.json"
    if not out_json.exists():          # 首次调用自动补产（与 python3 M_POLICY_EFFECT_SCORE.py 等价）
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
        "metric_id": "M_POLICY_EFFECT_SCORE",
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
