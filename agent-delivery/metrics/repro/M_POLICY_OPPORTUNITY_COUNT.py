#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_OPPORTUNITY_COUNT 政策机遇清单条数（王惠机遇计数 v2 全维复现）

王惠第四步：机遇综合分 ≥60 的政策数。本 v2 对齐 M_POLICY_DEEP_170_1 王惠四步
全维口径（'NULL' 占位清洗），输出真实分布与样例。
落盘：code/M_POLICY_OPPORTUNITY_COUNT_out.json
"""
import json, os, re, traceback
import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_POLICY_OPPORTUNITY_COUNT_out.json")

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", database="gkx",
           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
           connect_timeout=15, read_timeout=600)

def flush(out):
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

def q(conf, sql, args=None):
    with pymysql.connect(**conf) as conn, conn.cursor() as cur:
        cur.execute(sql, args or ())
        return cur.fetchall()

def clean(v):
    s = (v or "").strip() if isinstance(v, str) else ("" if v is None else str(v).strip())
    return "" if s in ("NULL", "null", "None") else s

def runlen(years):
    if not years:
        return 0
    ys = sorted(years); best = cur = 1
    for i in range(1, len(ys)):
        cur = cur + 1 if ys[i] == ys[i - 1] + 1 else 1
        best = max(best, cur)
    return best

def main():
    out = {"metric_id": "M_POLICY_OPPORTUNITY_COUNT",
           "title": "政策机遇清单条数（王惠机遇计数 v2 全维复现）",
           "probe_date": "2026-10-21", "probes": {}, "compute": {}, "notes": []}
    try:
        out["probes"]["gkx_dwd_policy_base"] = q(GKX,
            "SELECT COUNT(*) n FROM dwd_policy_base")[0]["n"]
        for f in ["theme", "keywords", "quote_policy"]:
            out["probes"][f"gkx_real_{f}"] = q(GKX,
                "SELECT COUNT(*) n FROM dwd_policy_base WHERE `{0}` IS NOT NULL "
                "AND `{0}` NOT IN ('NULL','null','')".format(f))[0]["n"]
        flush(out)
    except Exception:
        out["notes"].append("P1 fail: " + traceback.format_exc(limit=1)); flush(out)

    rows = []
    try:
        last = -1
        while True:
            batch = q(GKX, "SELECT id, theme, keywords, content, ministry, "
                           "quote_policy, publish_year, title FROM dwd_policy_base "
                           "WHERE id > %s ORDER BY id LIMIT 2000", (last,))
            if not batch:
                break
            rows.extend(batch); last = batch[-1]["id"]
        out["compute"]["n_rows"] = len(rows)
        flush(out)
    except Exception:
        out["notes"].append("P2 fail: " + traceback.format_exc(limit=1)); flush(out)
        return out

    try:
        pol = []
        for r in rows:
            theme = clean(r["theme"])
            kw_raw = clean(r["keywords"])
            content = r["content"] or ""
            ministry = clean(r["ministry"])
            qp = clean(r["quote_policy"])
            kw_list = [w for w in re.split(r"[;,，、；\s|\[\]'\"]+", kw_raw) if len(w) >= 2][:20]
            n_chars = len(content)
            kw_freq = sum(content.count(w) for w in kw_list)
            dens = kw_freq / n_chars * 100 if (kw_list and n_chars >= 50) else None
            mins = [m for m in re.split(r"[;,，、；/|]+", ministry) if m.strip()]
            year = None
            try:
                if r["publish_year"]:
                    year = int(str(r["publish_year"])[:4])
            except Exception:
                year = None
            pol.append(dict(id=r["id"], title=(r["title"] or "")[:80], theme=theme,
                            dens=dens, mins=mins, qp=qp, year=year))
        N = len(pol)
        theme_cnt, theme_minis, theme_years = {}, {}, {}
        for p in pol:
            if p["theme"]:
                theme_cnt[p["theme"]] = theme_cnt.get(p["theme"], 0) + 1
                theme_minis.setdefault(p["theme"], set()).update(p["mins"])
                if p["year"]:
                    theme_years.setdefault(p["theme"], set()).add(p["year"])

        subs = []
        for p in pol:
            t = p["theme"]
            subs.append(dict(
                theme_den=theme_cnt.get(t, 0) if t else None,
                dens=p["dens"],
                mcnt=len(theme_minis.get(t, ())) if t else None,
                qp=1 if p["qp"] else None,
                cont=runlen(theme_years.get(t, ())) if t and theme_years.get(t) else None,
            ))

        def norm_col(key):
            vals = [s[key] for  s in subs if s[key] is not None]
            if not vals:
                return {}
            lo, hi = min(vals), max(vals)
            return {i: (50.0 if hi == lo else (s[key] - lo) / (hi - lo) * 100)
                    for i, s in enumerate(subs) if s[key] is not None}

        z_td, z_de, z_mc, z_qp, z_ct = (norm_col(k) for k in
            ("theme_den", "dens", "mcnt", "qp", "cont"))
        z = {"theme_den": z_td, "dens": z_de, "mcnt": z_mc, "qp": z_qp, "cont": z_ct}
        att, infl, stab = [], [], []
        for i in range(N):
            pa = [z[k][i] for k in ("theme_den", "dens") if i in z[k]]
            att.append(sum(pa) / len(pa) if pa else None)
            pi = [z[k][i] for k in ("mcnt", "qp") if i in z[k]]
            infl.append(sum(pi) / len(pi) if pi else None)
            stab.append(z_ct.get(i))
        scores = []
        for i in range(N):
            vs = [v for v in (att[i], infl[i], stab[i]) if v is not None]
            scores.append(sum(vs) / len(vs) if vs else None)
        sc = sorted(s for s in scores if s is not None)
        n_opp = sum(1 for s in sc if s >= 60)

        c = out["compute"]
        c.update({
            "n_total": N,
            "theme_nonzero": sum(1 for p in pol if p["theme"]),
            "dens_scored": sum(1 for p in pol if p["dens"] is not None),
            "scored_anydim": len(sc),
            "n_opportunity_ge60": n_opp,
            "score_max": sc[-1] if sc else None,
            "score_min": sc[0] if sc else None,
        })
        idx_sc = [(scores[i], i) for i in range(N) if scores[i] is not None]
        idx_sc.sort(key=lambda x: -x[0])
        c["top_examples"] = [
            {"title": pol[i]["title"], "theme": pol[i]["theme"][:40],
             "score": round(s, 2)} for s, i in idx_sc[:5]]
        # 判档字段必须是四档枚举之一，附带说明另放 judgment_reason。
        # 此前把括号说明拼在 support_judgment 里，downstream `v in TIERS` 判不中 → 静默拿到 None
        # （DATA_FACTS §3.24 的残留形态：键名对了，值却不是一个合法枚举）。
        out["support_judgment"] = "部分支持"
        out["judgment_reason"] = (
            "与 170 同源：真实 theme 2/20000、keywords 0、quote 2；"
            "机遇计数=0；三子指标数据空壳，非方法不可行")
        flush(out)
    except Exception:
        out["notes"].append("P3 fail: " + traceback.format_exc(limit=1)); flush(out)
    return out

if __name__ == "__main__":
    o = main()
    print(json.dumps({k: o[k] for k in ("probes", "support_judgment") if k in o},
                     ensure_ascii=False, indent=1))
    print("compute keys:", list(o.get("compute", {}).keys()))
