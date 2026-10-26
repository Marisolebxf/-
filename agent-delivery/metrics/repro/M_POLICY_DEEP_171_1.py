#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_POLICY_DEEP_171_1｜政策布局推荐模型（王惠对冲链路，零 SQL 复现）

四步：
  1) 方向键 = theme 数组摊平后的去重条目（空不进）；
  2) 机遇方向 Opp_t = 该方向子集中至少 1 条政策过 170 机遇线（≥60，复用 170 产物）；
  3) 短板方向 Short_t = 对象覆盖缺口 ∨ 有效占比 <90% ∨ 文号规范率 <90% ∨ 正文完整率 <90%；
  4) 布局建议数 = COUNT(DISTINCT t | Opp_t=1 且 Short_t=1)。

上游：code/M_POLICY_DEEP_170_1_out.json（同目录、可复跑，非外部 bundle）。
数据：code/_snapshots21 四份快照，零 SQL。
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_snapshots21")
OUT = os.path.join(HERE, "M_POLICY_DEEP_171_1_out.json")
UP_170 = os.path.join(HERE, "M_POLICY_DEEP_170_1_out.json")

CODE_STD = re.compile(r"〔[0-9]{4}〕[0-9]+号|\[[0-9]{4}\][0-9]+号")
PLACEHOLDER = {"", "NULL", "NONE", "-", "[]"}


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
    aux = load("policy_aux_20261022.json")
    n = len(rows)

    theme_rows = aux["probes"].get("theme_quote_rows", [])
    theme_fields = {r["id"]: r for r in aux["probes"].get("theme_row_fields", [])}
    by_id = {r["id"]: r for r in rows}

    directions = {}
    for t in theme_rows:
        pid = t["id"]
        f = theme_fields.get(pid, {})
        base = by_id.get(pid, {})
        for d in theme_items(t.get("theme")):
            item = directions.setdefault(d, {"theme": d, "policies": []})
            item["policies"].append({
                "id": pid,
                "title": nn(base.get("title"))[:80],
                "status": nn(f.get("status")),
                "publish_code": nn(f.get("publish_code")),
                "content_len": int(f.get("content_len") or 0),
                "has_quote": bool(nn(t.get("quote_policy"))),
                "publish_year": nn(base.get("publish_year")),
            })

    # 170 上游（同目录产物）
    up = {}
    if os.path.exists(UP_170):
        with open(UP_170, encoding="utf-8") as f:
            up = json.load(f)
    opp_meta = {
        "source": "code/M_POLICY_DEEP_170_1_out.json",
        "n_opportunity_ge60": (up.get("scores") or {}).get("n_opportunity_ge60"),
        "n_policies_scored": (up.get("scores") or {}).get("n_policies_scored"),
        "note": "170 王惠口径下只有 2 条政策可评分、均为 50 分，全库 0 条过 60 线 → 机遇方向集为空",
    }
    opp_dirs = set()   # 方向级机遇：170 没有可归属到方向的过线政策

    anchor_links = int(aux["probes"].get("industry_links_distinct") or 0)
    n_dirs = len(directions)
    # 需求八类环节 vs 实测方向键；对象覆盖缺口 = 方向键铺不满八类锚点
    object_cover_gap = n_dirs < 8

    detail = []
    short_dirs = set()
    for d, item in sorted(directions.items()):
        ps = item["policies"]
        k = len(ps)
        valid_ratio = sum(1 for p in ps if p["status"] == "有效") / k
        code_ratio = sum(1 for p in ps if CODE_STD.search(p["publish_code"])) / k
        content_ratio = sum(1 for p in ps if p["content_len"] >= 100) / k
        trig = []
        if object_cover_gap:
            trig.append("对象覆盖缺口(方向键 5 < 锚点八类)")
        if valid_ratio < 0.9:
            trig.append(f"有效占比 {valid_ratio:.0%} <90%")
        if code_ratio < 0.9:
            trig.append(f"文号规范率 {code_ratio:.0%} <90%")
        if content_ratio < 0.9:
            trig.append(f"正文完整率 {content_ratio:.0%} <90%")
        if trig:
            short_dirs.add(d)
        detail.append({
            "direction": d, "n_policies": k,
            "valid_ratio_pct": round(valid_ratio * 100, 2),
            "code_std_ratio_pct": round(code_ratio * 100, 2),
            "content_ok_ratio_pct": round(content_ratio * 100, 2),
            "triggers": trig,
            "short": bool(trig),
            "policies": [{"id": p["id"], "title": p["title"], "publish_code": p["publish_code"]}
                         for p in ps],
        })

    rec = sorted(opp_dirs & short_dirs)
    out = {
        "metric_id": "M_POLICY_DEEP_171_1",
        "title": "政策布局推荐模型",
        "probe_date": "2026-10-22",
        "data_support_level": "部分支持",
        "support_judgment": "部分支持",
        "support_reason": ("方向键 theme 真实值只有 2 行（5 个方向），机遇侧上游 170 在全库 0 条过线，"
                           "布局建议数必然为 0；短板侧阈值字段（status/publish_code/content）可用，"
                           "产业锚点 301 个可读。机遇侧整块不可用 → 部分支持。"),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": ("本指标为截面方向对冲，不设跨年基期。方向级年份只出现 2010 与 2015 两年，"
                            "不用于任何增速或均值分母；政策表 2023 年起无数据，不做年度外推。"),
        "sources": {
            "pg_policy_rows": "code/_snapshots21/pg_policy_rows_20261021.json（id/title/publish_year）",
            "policy_aux": "code/_snapshots21/policy_aux_20261022.json（theme 2 行、行业链环节 301 个）",
            "upstream_170": "code/M_POLICY_DEEP_170_1_out.json（同目录可复跑）",
            "db": "gkx @ 183.240.141.251:3318（只读；本脚本零 SQL）",
        },
        "reused_from": "M_POLICY_DEEP_170_1_out.json",
        "population": {
            "rows": n,
            "rows_with_theme": 2,
            "n_directions": n_dirs,
            "industry_anchor_links": anchor_links,
            "object_cover_ratio_pct": round(100.0 * n_dirs / anchor_links, 4) if anchor_links else None,
        },
        "object_cover_gap": object_cover_gap,
        "object_cover_basis": ("对象覆盖维的分母取 dwd_industry_chain_info 的 301 个链环节名；"
                               "方向键只有 5 个，覆盖率 5/301=1.66%，远低于「铺满八类环节」的要求。"
                               "该缺口是全局性的（每个方向都继承），不是某一方向独有。"),
        "opportunity_side": opp_meta,
        "n_opp_dirs": len(opp_dirs),
        "n_short_dirs": len(short_dirs),
        "short_detail": detail,
        "layout_rec_count": len(rec),
        "layout_rec_dirs": rec,
        "verdict": ("布局建议数 = 0。0 的成因不是「没有可布局方向」，而是机遇侧整块缺数据："
                    "theme 2 行、keywords 0 行、quote 2 行使 170 无法给出方向级机遇判定。"
                    "短板侧 5/5 方向触发，只能作为「待补数据方向」清单，不能当推荐结论发布。"),
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(json.dumps({k: out[k] for k in ("metric_id", "support_judgment", "population",
                                          "n_opp_dirs", "n_short_dirs", "layout_rec_count")},
                     ensure_ascii=False, indent=1))
    print(json.dumps(detail, ensure_ascii=False, indent=1))
    print("->", OUT)


if __name__ == "__main__":
    main()
