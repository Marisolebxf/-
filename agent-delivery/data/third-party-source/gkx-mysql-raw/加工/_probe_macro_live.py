# -*- coding: utf-8 -*-
"""One-shot live probe for 宏观行业 6 tables. Do not print secrets."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_row_counts import ENV_PATH, connect, load_env  # noqa: E402

TABLES = [
    "dwd_macro_index_data",
    "dwd_dim_index_attribute",
    "dwd_dim_admin_area",
    "dwd_dim_index_cal",
    "dwd_dim_index_dur",
    "dwd_dim_source_code",
]

EXCEL_COLS = {
    "dwd_macro_index_data": [
        "rid", "index_code", "occur_period", "occur_period_t", "occur_period_year",
        "occur_period_month", "area_code", "dim_cal", "dim_dur", "index_value",
        "unit_use", "label", "update_time", "source_code", "area_code_type",
    ],
    "dwd_dim_index_attribute": [
        "rid", "uid", "index_name", "index_code", "unit_show", "unit_use",
        "data_freq", "time_attr_tag", "create_time",
    ],
    "dwd_dim_admin_area": [
        "rid", "qh_base_id", "source_code", "update_time", "cur_code", "cur_name",
        "parent_code", "country_code", "country_name", "province_code", "province_name",
        "city_code", "city_name", "area_code", "area_name", "street_code", "street_name",
        "community_code", "community_name", "cur_level",
    ],
    "dwd_dim_index_cal": ["rid", "dim_cal", "dim_cal_name", "dim_cal_desc", "create_time"],
    "dwd_dim_index_dur": ["rid", "dim_dur", "dim_dur_name", "dim_dur_desc", "create_time"],
    "dwd_dim_source_code": ["rid", "source_code", "source_name", "create_time"],
}

TECH = {
    "dwd_id", "created_time", "updated_time", "creater", "updater",
    "table_data_source", "operator_remarks", "is_deleted", "insert_remark",
}


def q(cur, sql, args=None):
    cur.execute(sql, args or ())
    return cur.fetchall()


def main() -> int:
    conn = connect(load_env(ENV_PATH))
    cur = conn.cursor()
    out: dict = {"db": None, "tables": {}}

    row = q(cur, "SELECT VERSION(), DATABASE(), NOW()")[0]
    out["db"] = {"version": row[0], "database": row[1], "now": str(row[2])}

    names = ",".join(f"'{t}'" for t in TABLES)
    meta = q(
        cur,
        f"""
        SELECT TABLE_NAME, TABLE_ROWS, DATA_LENGTH, CREATE_TIME, UPDATE_TIME
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME IN ({names})
        """,
    )
    meta_map = {r[0]: r for r in meta}

    for t in TABLES:
        info: dict = {"exists": t in meta_map}
        if t not in meta_map:
            out["tables"][t] = info
            print(f"MISSING {t}", flush=True)
            continue
        m = meta_map[t]
        info["info_schema_rows"] = int(m[1] or 0)
        info["data_length"] = int(m[2] or 0)
        info["create_time"] = str(m[3])
        info["update_time"] = str(m[4])

        cols = q(
            cur,
            """
            SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION
            """,
            (t,),
        )
        live_cols = [c[0] for c in cols]
        info["columns"] = [
            {"name": c[0], "type": c[1], "null": c[2], "key": c[3], "extra": c[4]}
            for c in cols
        ]
        excel = EXCEL_COLS[t]
        info["excel_missing_in_live"] = [c for c in excel if c not in live_cols]
        info["live_extra_vs_excel"] = [c for c in live_cols if c not in excel]
        info["live_extra_business"] = [
            c for c in live_cols if c not in excel and c not in TECH
        ]

        idx = q(cur, f"SHOW INDEX FROM `{t}`")
        info["indexes"] = sorted({(r[2], r[4], bool(r[1] == 0)) for r in idx})

        has_del = "is_deleted" in live_cols
        n_all = q(cur, f"SELECT COUNT(*) FROM `{t}`")[0][0]
        n_biz = (
            q(cur, f"SELECT COUNT(*) FROM `{t}` WHERE is_deleted = 0")[0][0]
            if has_del
            else n_all
        )
        info["count_all"] = int(n_all)
        info["count_biz"] = int(n_biz)
        info["has_is_deleted"] = has_del
        print(f"{t}: all={n_all} biz={n_biz}", flush=True)
        out["tables"][t] = info

    # --- dim dumps (small) ---
    for t, cols in (
        ("dwd_dim_index_cal", "dim_cal, dim_cal_name, dim_cal_desc"),
        ("dwd_dim_index_dur", "dim_dur, dim_dur_name, dim_dur_desc"),
        ("dwd_dim_source_code", "source_code, source_name"),
    ):
        rows = q(cur, f"SELECT {cols} FROM `{t}` WHERE is_deleted = 0")
        out[t] = [list(r) for r in rows]

    # attribute catalog
    out["attr"] = {
        "freq": [
            list(r)
            for r in q(
                cur,
                """
                SELECT IFNULL(data_freq,'<NULL>'), COUNT(*)
                FROM dwd_dim_index_attribute WHERE is_deleted=0
                GROUP BY data_freq ORDER BY COUNT(*) DESC
                """,
            )
        ],
        "code_prefix": [
            list(r)
            for r in q(
                cur,
                """
                SELECT SUBSTRING_INDEX(index_code, '_', 1) pref, COUNT(*)
                FROM dwd_dim_index_attribute WHERE is_deleted=0
                GROUP BY pref ORDER BY COUNT(*) DESC LIMIT 20
                """,
            )
        ],
        "keyword_hits": {},
    }
    keywords = ["GDP", "生产总值", "产业", "工业", "投资", "就业", "进出口", "研发", "专利", "政策", "科创", "深圳"]
    for kw in keywords:
        n = q(
            cur,
            """
            SELECT COUNT(*) FROM dwd_dim_index_attribute
            WHERE is_deleted=0 AND index_name LIKE %s
            """,
            (f"%{kw}%",),
        )[0][0]
        samples = q(
            cur,
            """
            SELECT index_code, index_name, data_freq, unit_use
            FROM dwd_dim_index_attribute
            WHERE is_deleted=0 AND index_name LIKE %s
            LIMIT 8
            """,
            (f"%{kw}%",),
        )
        out["attr"]["keyword_hits"][kw] = {"n": int(n), "samples": [list(r) for r in samples]}

    out["attr"]["sample20"] = [
        list(r)
        for r in q(
            cur,
            """
            SELECT index_code, index_name, data_freq, unit_use
            FROM dwd_dim_index_attribute WHERE is_deleted=0
            ORDER BY index_code LIMIT 20
            """,
        )
    ]

    # area
    out["area"] = {
        "levels": [
            list(r)
            for r in q(
                cur,
                """
                SELECT cur_level, COUNT(*) FROM dwd_dim_admin_area
                WHERE is_deleted=0 GROUP BY cur_level ORDER BY cur_level
                """,
            )
        ],
        "sz": [
            list(r)
            for r in q(
                cur,
                """
                SELECT cur_level, cur_code, cur_name, city_name, province_name
                FROM dwd_dim_admin_area
                WHERE is_deleted=0 AND (
                    cur_name LIKE %s OR city_name LIKE %s
                )
                ORDER BY cur_level LIMIT 15
                """,
                ("%深圳%", "%深圳%"),
            )
        ],
        "n_gd": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_dim_admin_area
                WHERE is_deleted=0 AND (province_name LIKE %s OR cur_name=%s)
                """,
                ("%广东%", "广东省"),
            )[0][0]
        ),
    }

    # fact quality
    out["fact"] = {
        "period": list(
            q(
                cur,
                """
                SELECT MIN(occur_period), MAX(occur_period),
                       COUNT(DISTINCT occur_period),
                       COUNT(DISTINCT index_code),
                       COUNT(DISTINCT area_code),
                       COUNT(DISTINCT dim_cal),
                       COUNT(DISTINCT dim_dur),
                       COUNT(DISTINCT source_code),
                       COUNT(DISTINCT label)
                FROM dwd_macro_index_data WHERE is_deleted=0
                """,
            )[0]
        ),
        "dim_cal": [
            list(r)
            for r in q(
                cur,
                """
                SELECT dim_cal, COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 GROUP BY dim_cal ORDER BY COUNT(*) DESC
                """,
            )
        ],
        "dim_dur": [
            list(r)
            for r in q(
                cur,
                """
                SELECT dim_dur, COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 GROUP BY dim_dur ORDER BY COUNT(*) DESC
                """,
            )
        ],
        "source": [
            list(r)
            for r in q(
                cur,
                """
                SELECT source_code, COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 GROUP BY source_code ORDER BY COUNT(*) DESC LIMIT 15
                """,
            )
        ],
        "label": [
            list(r)
            for r in q(
                cur,
                """
                SELECT label, COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 GROUP BY label
                """,
            )
        ],
        "area_code_type": [
            list(r)
            for r in q(
                cur,
                """
                SELECT area_code_type, COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 GROUP BY area_code_type
                """,
            )
        ],
        "area_looks_cn": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 AND area_code REGEXP '[\\u4e00-\\u9fff]'
                """,
            )[0][0]
        ),
        "area_looks_digit": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 AND area_code REGEXP '^[0-9]+$'
                """,
            )[0][0]
        ),
        "area_samples": [
            list(r)
            for r in q(
                cur,
                """
                SELECT area_code, COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 GROUP BY area_code ORDER BY COUNT(*) DESC LIMIT 12
                """,
            )
        ],
        "year": [
            list(r)
            for r in q(
                cur,
                """
                SELECT occur_period_year, COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 GROUP BY occur_period_year ORDER BY occur_period_year
                """,
            )
        ],
        "join_attr": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_index_attribute a
                  ON a.index_code = f.index_code AND a.is_deleted=0
                WHERE f.is_deleted=0 AND a.index_code IS NULL
                """,
            )[0][0]
        ),
        "join_cal_code": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_index_cal c
                  ON c.dim_cal = f.dim_cal AND c.is_deleted=0
                WHERE f.is_deleted=0 AND c.dim_cal IS NULL
                """,
            )[0][0]
        ),
        "join_cal_name": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_index_cal c
                  ON c.dim_cal_name = f.dim_cal AND c.is_deleted=0
                WHERE f.is_deleted=0 AND c.dim_cal IS NULL
                """,
            )[0][0]
        ),
        "join_dur_code": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_index_dur d
                  ON d.dim_dur = f.dim_dur AND d.is_deleted=0
                WHERE f.is_deleted=0 AND d.dim_dur IS NULL
                """,
            )[0][0]
        ),
        "join_dur_name": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_index_dur d
                  ON d.dim_dur_name = f.dim_dur AND d.is_deleted=0
                WHERE f.is_deleted=0 AND d.dim_dur IS NULL
                """,
            )[0][0]
        ),
        "join_area": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_admin_area a
                  ON a.cur_code = f.area_code AND a.is_deleted=0
                WHERE f.is_deleted=0 AND a.cur_code IS NULL
                """,
            )[0][0]
        ),
        "join_source_code": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_source_code s
                  ON s.source_code = f.source_code AND s.is_deleted=0
                WHERE f.is_deleted=0 AND s.source_code IS NULL
                """,
            )[0][0]
        ),
        "join_source_name": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_source_code s
                  ON s.source_name = f.source_code AND s.is_deleted=0
                WHERE f.is_deleted=0 AND s.source_code IS NULL
                """,
            )[0][0]
        ),
        "sz_rows": int(
            q(
                cur,
                """
                SELECT COUNT(*) FROM dwd_macro_index_data
                WHERE is_deleted=0 AND area_code LIKE %s
                """,
                ("%深圳%",),
            )[0][0]
        ),
        "top_index": [
            list(r)
            for r in q(
                cur,
                """
                SELECT f.index_code, a.index_name, COUNT(*) n
                FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_index_attribute a
                  ON a.index_code=f.index_code AND a.is_deleted=0
                WHERE f.is_deleted=0
                GROUP BY f.index_code, a.index_name
                ORDER BY n DESC LIMIT 15
                """,
            )
        ],
        "sample_rows": [
            list(r)
            for r in q(
                cur,
                """
                SELECT f.index_code, a.index_name, f.occur_period, f.area_code,
                       f.dim_cal, f.dim_dur, f.index_value, f.unit_use,
                       f.label, f.source_code, f.area_code_type
                FROM dwd_macro_index_data f
                LEFT JOIN dwd_dim_index_attribute a
                  ON a.index_code=f.index_code AND a.is_deleted=0
                WHERE f.is_deleted=0
                ORDER BY f.rid
                LIMIT 12
                """,
            )
        ],
    }

    dest = Path(__file__).with_name("_probe_macro_live.json")
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("WROTE", dest, flush=True)
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
