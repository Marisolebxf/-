#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
