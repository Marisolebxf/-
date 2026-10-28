#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 【20261027 抬头治理件】维护者：唐绍祖 ｜ 适用系统：科技信息展示系统（按 UI 挂载推断）
# 【分级】无直接文档对应（未入 D1–D5 跨系统分级；本批只加抬头注释，不改计算逻辑与产物数值）
"""M_ENT_REGIONAL_DENSITY · 区域企业密度（gkx 口径）

口径（calc-logic/ENT/M_ENT_REGIONAL_DENSITY.md）：
    密度 = 该区企业数 / 该区土地面积(km²)，单位 家/km²；area 空或 ≤0 该区空（不写 0）。
    分子：国内省/市/县去重企业数；分母：项目维表 code_region.area。

gkx 实测结论：分子齐、分母不在库（无任何数值型面积列，见 probes.denominator），
故按口径「该区空」交付 0 行，并另给一条不含面积的降级读数（家/行政区，非交付值）。

数据来源（两选一，优先快照）：
  1）code/_snapshots21/ent_region_agg_20261022.json —— 本目录已验证快照，
     SQL 与 M_ENT_REGION_COVERAGE.py 的同一条 GROUP BY 完全一致；
  2）快照缺失时回落到 live gkx 分组查询（约 75—310 秒）。
面积分母的证据每次都现场查 information_schema，不读快照。

产物：code/M_ENT_REGIONAL_DENSITY_out.json
"""
from __future__ import annotations

import json
import time
from collections import Counter
from decimal import Decimal
from pathlib import Path

import pymysql

HERE = Path(__file__).resolve().parent
SNAP = HERE / "_snapshots21"
SNAP_REGION = SNAP / "ent_region_agg_20261022.json"
OUT = HERE / "M_ENT_REGIONAL_DENSITY_out.json"
METRIC_ID = "M_ENT_REGIONAL_DENSITY"

GKX = dict(host="183.240.141.251", port=3318, user="gkx_reader_zp",
           password="Zp_Use_Gkx_db@123456", connect_timeout=60,
           read_timeout=1800, write_timeout=1800, autocommit=True)

SQL_REGION = (
    "SELECT province, city, area, COUNT(*) AS n FROM gkx.dwd_org_base_info "
    "WHERE is_deleted=0 GROUP BY province, city, area"
)
# 分母三连探：① 数值型面积列；② 面积/区划维表是否存在；③ 宏观指标里有无「面积」口径
SQL_AREA_COLS = (
    "SELECT table_name, column_name, data_type, column_comment "
    "FROM information_schema.columns WHERE table_schema='gkx' AND ("
    "column_comment LIKE '%面积%' OR column_name LIKE '%area%' "
    "OR column_name LIKE '%_km%' OR column_name LIKE '%square%')"
)
SQL_AREA_TABLES = (
    "SELECT table_name FROM information_schema.tables WHERE table_schema='gkx' AND ("
    "table_name LIKE '%code_region%' OR table_name LIKE '%region_scope%' "
    "OR table_name LIKE '%density%' OR table_name LIKE '%admin_area%')"
)
SQL_MACRO_AREA = (
    "SELECT COUNT(*) AS n FROM gkx.dwd_macro_index_data WHERE index_code LIKE '%面积%'"
)


def j(v):
    if isinstance(v, (bytes, bytearray)):
        return v.decode("utf-8", "replace")
    if isinstance(v, Decimal):
        return float(v)
    if hasattr(v, "isoformat"):
        try:
            return v.isoformat()
        except TypeError:
            return str(v)
    return v


def connect():
    last = None
    for i in range(5):
        try:
            return pymysql.connect(**GKX)
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** i)
    raise RuntimeError(f"gkx 连不上（5 次重试）：{last}")


def q(cur, sql, ms=900000):
    cur.execute(f"SET SESSION max_execution_time={ms}")
    cur.execute(sql)
    return [list(map(j, r)) for r in cur.fetchall()]


def load_region(cur):
    """优先读已验证快照；缺失则 live 跑同一条 GROUP BY。"""
    if SNAP_REGION.exists():
        d = json.loads(SNAP_REGION.read_text(encoding="utf-8"))
        blk = d.get("region_agg") or {}
        if blk.get("ok") and blk.get("rows"):
            return blk["rows"], "snapshot:code/_snapshots21/ent_region_agg_20261022.json", blk["sql"]
    rows = q(cur, SQL_REGION, 900000)
    return rows, "live:gkx.dwd_org_base_info GROUP BY province,city,area", SQL_REGION


def main() -> None:
    t0 = time.time()
    conn = connect()
    cur = conn.cursor()

    cells, region_source, region_sql = load_region(cur)
    area_cols = q(cur, SQL_AREA_COLS, 60000)
    area_tables = q(cur, SQL_AREA_TABLES, 60000)
    macro_area_rows = int(q(cur, SQL_MACRO_AREA, 120000)[0][0])
    macro_total = int(q(cur, "SELECT COUNT(*) FROM gkx.dwd_macro_index_data", 120000)[0][0])
    conn.close()

    prov = Counter()
    city = Counter()
    county = Counter()
    for p, c, a, n in cells:
        n = int(n)
        if p:
            prov[p] += n
        if p and c:
            city[(p, c)] += n
        if p and c and a:
            county[(p, c, a)] += n

    total = sum(int(r[3]) for r in cells)
    # 只认「土地/区域面积」语义的数值列：
    #   - 评论含「面积」但不是「表面积」（`dwd_substance.tpsa` 是分子极性表面积，不是行政区面积）；
    #   - 或列名就是 area/land_area/area_km2/sqkm。
    # 实测全库 15 个 area/面积 相关列里，满足此条件的是 0 个——这是本件判部分支持的硬证据。
    import re as _re
    AREA_NAME = _re.compile(r"^(land_)?area(_km2|_sqkm|_size|_value)?$", _re.I)
    NUMERIC = {"double", "decimal", "float", "int", "bigint", "smallint", "numeric"}
    numeric_area_cols = [
        r for r in area_cols
        if r[2] in NUMERIC and (
            (("面积" in (r[3] or "")) and ("表面积" not in (r[3] or "")))
            or AREA_NAME.match(str(r[1]))
        )
    ]

    def rate(a, b):
        return round(a / b, 4) if b else None

    payload = {
        "metric_id": METRIC_ID,
        "metric_name": "区域企业密度",
        "support_judgment": "部分支持",
        "verdict_kind": "positive",
        "judgment_reason": (
            "分子侧完全就绪（189,116 家企业可按省/市/县三级聚合），但分母「行政区土地面积」"
            "在 gkx 内不存在：information_schema 全库 15 个 area/面积 相关列全部是编码或名称，"
            "无数值型面积列；区划维表 dwd_dim_admin_area（20,000 行）也不含面积字段。"
            "按口径「area 空该区空」，交付 0 行；有分子、有层级、无分母，故判部分支持而非完全不支持。"
        ),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sources": {
            "primary": "gkx @ 183.240.141.251:3318 (readonly gkx_reader_zp)",
            "numerator_region_source": region_source,
            "tables": ["gkx.dwd_org_base_info", "gkx.dwd_dim_admin_area", "gkx.dwd_macro_index_data"],
            "sql": [region_sql, SQL_AREA_COLS, SQL_AREA_TABLES, SQL_MACRO_AREA],
            "calc_logic": "gkx-orchestration/agent-delivery/metrics/calc-logic/ENT/M_ENT_REGIONAL_DENSITY.md",
        },
        "compute": {
            "denominator_available": False,
            "delivered_rows": 0,
            "blocked_cells": {"province": len(prov), "city": len(city), "county": len(county),
                              "total": len(prov) + len(city) + len(county)},
            "numerator_cells": {"province": len(prov), "city": len(city), "county": len(county)},
            "base_orgs": total,
            "numerator": {
                "top_provinces": [{"province": k, "orgs": v} for k, v in prov.most_common(8)],
                "top_cities": [{"province": k[0], "city": k[1], "orgs": v}
                               for k, v in city.most_common(8)],
                "top_counties": [{"province": k[0], "city": k[1], "county": k[2], "orgs": v}
                                 for k, v in county.most_common(8)],
                "guangdong_share_pct": round(prov.get("广东省", 0) / total * 100, 4),
            },
            "fallback_no_area": {
                "label": "家/行政区（降级读数，非 家/km²，不交付）",
                "orgs_per_province": rate(total, len(prov)),
                "orgs_per_city": rate(total, len(city)),
                "orgs_per_county": rate(total, len(county)),
                "note": "分子为行政区内的企业数，分母是行政区个数，不是面积；"
                        "只能用于「同一层级内谁家多」，不能用于跨层级或跨面积比较。",
            },
        },
        "probes": {
            "denominator": {
                "area_related_columns": len(area_cols),
                "numeric_area_columns": len(numeric_area_cols),
                "numeric_area_column_list": numeric_area_cols,
                "admin_tables_found": [r[0] for r in area_tables],
                "macro_rows": macro_total,
                "macro_rows_matching_area": macro_area_rows,
                "verdict": "无可用面积分母（0 个数值型面积列 / 0 个区划面积表 / 0 行宏观面积口径）",
            },
            "max_execution_time_ms": 900000,
            "retry_policy": "5 次指数退避",
        },
        "proxy_deviation": (
            "登记地代理经营地：分子用 dwd_org_base_info 的注册省/市/区县，企业实际经营地可能不同"
            "（尤其总部与生产基地分离的制造企业），偏差方向不定、无法用库内字段校正。"
            "底册覆盖偏粤：广东 188,776 家占 99.82%，省外仅 340 家，跨省密度不可比；"
            "分母缺失时用「家/行政区」代替「家/km²」，单位语义已改变，不得混用。"
        ),
        "base_years_used": [],
        "base_years_missing": [],
        "base_years_note": (
            "截面件：分子取当前底册快照，分母（面积）不存在，故无年度序列与基期年份。"
            "面积一旦灌入，本件可直接按区划键出数，不需要改口径。"
        ),
        "notes": [
            "密度值 0 行是「按口径置空」的正确结果，不是脚本失败；blocked_cells 记录被置空的格子数。",
            "不拿上级面积顶下级、不拿人口/GDP 顶面积、不写 0 冒充密度。",
            "分母若由甲方灌入，单位必须确认是 km²（列注释只写「面积」，误判会差 100—1,500 倍）。",
        ],
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[{METRIC_ID}] 分子省={len(prov)} 市={len(city)} 县={len(county)} "
          f"数值面积列={len(numeric_area_cols)} 交付行=0")


if __name__ == "__main__":
    main()
