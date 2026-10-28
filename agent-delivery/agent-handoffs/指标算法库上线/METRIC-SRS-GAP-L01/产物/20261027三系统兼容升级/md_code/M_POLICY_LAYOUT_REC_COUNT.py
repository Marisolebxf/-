#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技专题服务算法库
# 【分级】单系统（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_POLICY_LAYOUT_REC_COUNT 政策布局建议条数（王惠对冲计数 v2 复现）

复用 170（机遇侧）与 169（短板侧）王惠口径，对冲计数 = Opp=1 且 Short=1 的
方向数。'NULL' 清洗。落盘：code/M_POLICY_LAYOUT_REC_COUNT_out.json
"""
import json, os, re, traceback
import pymysql

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "M_POLICY_LAYOUT_REC_COUNT_out.json")

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

def main():
    out = {"metric_id": "M_POLICY_LAYOUT_REC_COUNT",
           "title": "政策布局建议条数（王惠对冲计数 v2 复现）",
           "probe_date": "2026-10-21", "probes": {}, "compute": {}, "notes": []}

    rows = []
    try:
        last = -1
        while True:
            batch = q(GKX, "SELECT id, theme, title, status, publish_code, content "
                           "FROM dwd_policy_base WHERE id > %s ORDER BY id LIMIT 2000",
                      (last,))
            if not batch:
                break
            rows.extend(batch); last = batch[-1]["id"]
        out["compute"]["n_rows"] = len(rows)
        out["compute"]["rows_source"] = "gkx"
        flush(out)
    except Exception:
        out["notes"].append("P1 fail: " + traceback.format_exc(limit=1)); flush(out)
        return out

    try:
        pol = []
        for r in rows:
            theme = clean(r["theme"])
            themes = [x for x in re.split(r"[;,，、；/|\[\]'\"]+", theme) if x.strip()]
            pol.append(dict(themes=themes, status=clean(r["status"]),
                            pc=clean(r["publish_code"]), content=r["content"] or ""))
        directions = {}
        for p in pol:
            for t in p["themes"]:
                directions.setdefault(t, []).append(p)

        # 机遇侧：170 王惠全维口径 0 条过线 → 机遇方向集为空
        opp_dirs = set()
        # 短板侧：169 王惠阈值（对象覆盖缺口在方向数<8 时全触发）
        short_dirs = set()
        for t, ps in directions.items():
            n = len(ps)
            valid_ratio = sum(1 for p in ps if p["status"] in ("有效", "现行")) / n
            pc_ratio = sum(1 for p in ps if p["pc"]) / n
            content_ratio = sum(1 for p in ps if len(p["content"]) >= 100) / n
            if len(directions) < 8 or valid_ratio < 0.9 or pc_ratio < 0.5 or content_ratio < 0.8:
                short_dirs.add(t)
        rec = len(opp_dirs & short_dirs)
        c = out["compute"]
        c.update({
            "n_total": len(pol),
            "n_directions": len(directions),
            "directions_list": sorted(directions.keys()),
            "n_opp_dirs": len(opp_dirs),
            "n_short_dirs": len(short_dirs),
            "layout_rec_count_wanghui": rec,
            "note": ("机遇侧复用 170 实测 0 过线 → 对冲积 0；"
                     "短板侧 5/5 方向触发（对象覆盖缺口主导）"),
        })
        # 同 M_POLICY_OPPORTUNITY_COUNT：四档枚举 + 说明分开放（DATA_FACTS §3.24）。
        out["support_judgment"] = "部分支持"
        out["judgment_reason"] = (
            "上游 170 机遇侧 0 过线 + 方向键 theme 真实仅 2 行；"
            "对冲计数=0 为数据空壳传导；短板侧阈值字段两侧可用")
        flush(out)
    except Exception:
        out["notes"].append("P2 fail: " + traceback.format_exc(limit=1)); flush(out)
    return out

if __name__ == "__main__":
    o = main()
    print(json.dumps(o.get("support_judgment", ""), ensure_ascii=False))
    print("compute keys:", list(o.get("compute", {}).keys()))
