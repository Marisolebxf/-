#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M_ENT_REGION_HOT_COUNT 复现脚本（2026-10-22 改源版 · 只用三方库 gkx）。

口径（calc-logic/ENT/M_ENT_REGION_HOT_COUNT.md）：
  「按区域分组后企业数最多的 TOP N 区域的企业数」。
  本脚本把 N 作为参数（默认 10），输出 TOP N 曲线、CR4/CR10、HHI，
  并同时给出「热点区域个数 = N」这一字面解释的对照，避免口径歧义被
  隐式选定。

改源说明（20261021 版唯一变动）：
  数据面由开发库 ODS 换成三方库 `gkx`（与旧库逐表镜像，行数一致）；公式、
  N 默认值、输出结构、产业构成校验全部原样保留。取数只做**一次**全表分组
  （province × city × industry_l1_name），城市/省两级家数与总行数都由这一次
  分组在 Python 侧累加得到，避免对 18.9 万行主档重复扫表（该表无覆盖索引，
  单次无条件 COUNT(*) 实测 87.7 秒）。

输出：code/M_ENT_REGION_HOT_COUNT_out.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _gkxdb  # noqa: E402

OUT = Path(__file__).resolve().parent / "M_ENT_REGION_HOT_COUNT_out.json"
T = "gkx.dwd_org_base_info"
N_DEFAULT = 10


def q(sql, args=None):
    cur = _gkxdb.gkx()
    try:
        cur.execute(sql, args) if args else cur.execute(sql)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def main():
    t0 = time.time()
    # 一次分组拿全：省 × 市 × 行业一级。城市/省家数与总量在 Python 侧累加。
    rows = q("SELECT province, city, industry_l1_name, COUNT(*) n FROM " + T + " "
             "GROUP BY province, city, industry_l1_name")
    total = sum(int(r["n"]) for r in rows)

    city_map, prov_map = {}, {}
    city_industry: dict[str, dict[str, int]] = {}
    for r in rows:
        n = int(r["n"])
        key = (r["province"], r["city"])
        city_map[key] = city_map.get(key, 0) + n
        prov_map[r["province"]] = prov_map.get(r["province"], 0) + n
        city_industry.setdefault(r["city"], {})[r["industry_l1_name"]] = n

    city = sorted([{"province": p, "city": c, "n": n} for (p, c), n in city_map.items()],
                  key=lambda x: -x["n"])
    prov = sorted([{"province": p, "n": n} for p, n in prov_map.items()], key=lambda x: -x["n"])

    curve = []
    cum = 0
    for i, r in enumerate(city, start=1):
        cum += r["n"]
        if i in (1, 3, 5, 10, 20, 30, 50):
            curve.append({"N": i, "top_sum": cum, "share": round(cum / total * 100, 4),
                          "rest": total - cum, "n_regions_total": len(city)})

    def cr(k):
        return sum(r["n"] for r in city[:k])

    hhi_city = sum((r["n"] / total) ** 2 for r in city) * 10000
    hhi_prov = sum((r["n"] / total) ** 2 for r in prov) * 10000

    topN = city[:N_DEFAULT]
    top_cities = [r["city"] for r in topN[:4]]
    industry = []
    for ct in top_cities:
        for ind, n in sorted(city_industry.get(ct, {}).items(), key=lambda kv: -kv[1]):
            industry.append({"city": ct, "industry_l1_name": ind, "n": n})

    out = {
        "metric_id": "M_ENT_REGION_HOT_COUNT",
        "name": "区域热点企业数（未注册）",
        "probe_date": "2026-10-22",
        "source": "gkx.dwd_org_base_info（三方库 gkx，只读）",
        "elapsed_sec": round(time.time() - t0, 1),
        "param": {"N_default": N_DEFAULT, "N_status": "calc-logic 未钉死；Q24 仅记「TOP N」"},
        "probes": {
            "n_rows": total,
            "n_city_regions": len(city),
            "n_province_regions": len(prov),
            "guangdong_share": round(sum(r["n"] for r in prov if "广东" in (r["province"] or "")) / total * 100, 4),
        },
        "topn_curve": curve,
        "top10": [{"rank": i + 1, "province": r["province"], "city": r["city"], "cnt": r["n"],
                   "share": round(r["n"] / total * 100, 4)} for i, r in enumerate(topN)],
        "rest_after_top10": {
            "n_regions": len(city) - N_DEFAULT,
            "n_enterprises": total - cr(N_DEFAULT),
            "share": round((total - cr(N_DEFAULT)) / total * 100, 4),
        },
        "concentration": {
            "cr1": round(cr(1) / total * 100, 4),
            "cr3": round(cr(3) / total * 100, 4),
            "cr4": round(cr(4) / total * 100, 4),
            "cr10": round(cr(10) / total * 100, 4),
            "hhi_city_x10000": round(hhi_city, 2),
            "hhi_province_x10000": round(hhi_prov, 2),
            "effective_n_city": round(10000 / hhi_city, 2),
        },
        "top4_industry_mix": industry,
        "alternative_reading": {
            "hot_region_count_literal": N_DEFAULT,
            "note": ("若按指标名「热点区域数」字面理解，交付值就是 N 本身（默认 10），"
                     "与分布无关；本报告采用 calc-logic 的「TOP N 区域的企业数」口径，"
                     "因为该口径才携带分布信息。两种解释都已给出，供甲方裁决。"),
        },
        "support_judgment": {
            "level": "完全转换支持",
            "reason": ("区域家数分布可由 gkx.dwd_org_base_info 一次 GROUP BY city 得到，"
                       "TOP N 求和与集中度均为确定性派生；结构+数据量均够，"
                       "缺的只是 N 的甲方取值与目标表。"),
            "blocking": [
                "N 未钉死（Q24）：N=1/3/5/10 的交付值差异极大（50.55%~99.94%），N 必须由甲方确认。",
                "无目标结果表：enterprise_region_summary 在 gkx 与 live 均零命中（0 行）。",
                "省外样本 340 家（0.18%），TOP 榜在城市层面不可作全国热点解释。",
            ],
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ["probes", "topn_curve", "concentration", "rest_after_top10"]},
                     ensure_ascii=False, indent=1, default=str))
    print("elapsed", out["elapsed_sec"], "s; support:", out["support_judgment"]["level"])


if __name__ == "__main__":
    main()
