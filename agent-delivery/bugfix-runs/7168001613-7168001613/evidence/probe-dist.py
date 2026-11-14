# 7168001613 追加诊断：分布链维 SQL 是否能跑通（对齐 enterprise_distribution.py 117-121 实际下发 SQL）
import sys

sys.path.insert(0, r"d:\web\gkx-lumen\repos\lumen-topic-py")
from gkx_common.db import dwd_table, dim_table, query

CASES = [
    ("global", ""),
    (
        "national",
        "JOIN {cr} cr ON cr.level = '1' AND cr.name = eb.province AND eb.province IS NOT NULL AND eb.province <> ''",
    ),
    (
        "regional",
        "JOIN {cr} cr ON cr.level = '2' AND cr.name = eb.city AND eb.province = '广东省' AND eb.city IS NOT NULL AND eb.city <> ''",
    ),
    (
        "city",
        "JOIN {cr} cr ON cr.level = '3' AND cr.name = eb.district AND eb.city = '深圳市' AND eb.district IS NOT NULL AND eb.district <> ''",
    ),
]
SELECTS = {
    "global": "'CHN' AS region_id, '中国' AS region_name",
    "national": "cr.code AS region_id, cr.name AS region_name",
    "regional": "cr.code AS region_id, cr.name AS region_name",
    "city": "cr.code AS region_id, cr.name AS region_name",
}

for code in ("INB2503", "INB170301"):
    for dim, join in CASES:
        sql = (
            f"SELECT {SELECTS[dim]}, COUNT(DISTINCT eb.org_id) AS enterprise_count "
            f"FROM {dwd_table('enterprise_base')} eb "
            f"INNER JOIN {dwd_table('enterprise_industry_chain')} c "
            f"ON c.org_id = eb.org_id AND c.chain_code = %(chain_code)s "
            + join.format(cr=dim_table('code_region'))
            + " GROUP BY region_id, region_name ORDER BY enterprise_count DESC"
        )
        try:
            rows = query(sql, {"chain_code": code})
            print(f"[OK] {code} {dim}: rows={len(rows)} top={rows[0] if rows else None}")
        except Exception as exc:
            print(f"[FAIL] {code} {dim}: {type(exc).__name__}: {exc}")
