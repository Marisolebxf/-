-- 宏观包 · 区划反解自检（只读，跑在三方库 gkx 或 gkxlumenx_ods 上；表名同为 dwd_*）
-- 用途：Wave A 贴源后、Wave B 之前核一遍 04 §3 的区划反解规则。断言写在 04 §3.5。
-- 规则顺序与 09 §3.1 `area_resolve` 派生一致。查询只读，不改任何表。
-- 2026-11-09 12:35 在 gkx 实跑过一次（见 04 §3.5 基线数）。换库名即可在 gkxlumenx_ods 上复核。

WITH
city AS (SELECT DISTINCT city_code     AS k FROM dwd_dim_admin_area WHERE is_deleted = 0 AND city_code     IS NOT NULL),
prov AS (SELECT DISTINCT province_code AS k FROM dwd_dim_admin_area WHERE is_deleted = 0 AND province_code IS NOT NULL),
dist AS (SELECT DISTINCT area_code     AS k FROM dwd_dim_admin_area WHERE is_deleted = 0 AND area_code     IS NOT NULL),
r AS (
  SELECT f.area_code_type,
         f.area_code,
         CASE
           WHEN CHAR_LENGTH(f.area_code) = 12 AND c.k IS NOT NULL                   THEN 'city_by_city_code'
           WHEN f.area_code IN ('11','12','31','50') AND p.k IS NOT NULL            THEN 'municipality_by_province_code'
           WHEN CHAR_LENGTH(f.area_code) = 12 AND d.k IS NOT NULL                   THEN 'district_by_area_code'
           ELSE 'unresolved'
         END AS area_resolve
  FROM dwd_macro_index_data f
  LEFT JOIN city c ON c.k = f.area_code
  LEFT JOIN prov p ON p.k = f.area_code
  LEFT JOIN dist d ON d.k = f.area_code
  WHERE f.is_deleted = 0
)
SELECT area_code_type, area_resolve, COUNT(*) AS fact_rows, COUNT(DISTINCT area_code) AS area_codes
FROM r
GROUP BY area_code_type, area_resolve
ORDER BY area_code_type, area_resolve;

-- 键唯一（含 area_code_type）。期望 0 行。
SELECT index_code, occur_period, area_code, area_code_type, dim_cal, dim_dur, COUNT(*) AS n
FROM dwd_macro_index_data
GROUP BY index_code, occur_period, area_code, area_code_type, dim_cal, dim_dur
HAVING COUNT(*) > 1;

-- 事实侧维度键孤儿。期望三个 0。
SELECT
  (SELECT COUNT(*) FROM dwd_macro_index_data f LEFT JOIN dwd_dim_index_attribute a ON a.index_code = f.index_code WHERE a.index_code IS NULL) AS orphan_attr,
  (SELECT COUNT(*) FROM dwd_macro_index_data f LEFT JOIN dwd_dim_index_cal       c ON c.dim_cal    = f.dim_cal    WHERE c.dim_cal    IS NULL) AS orphan_cal,
  (SELECT COUNT(*) FROM dwd_macro_index_data f LEFT JOIN dwd_dim_index_dur       u ON u.dim_dur    = f.dim_dur    WHERE u.dim_dur    IS NULL) AS orphan_dur,
  (SELECT COUNT(*) FROM dwd_macro_index_data f LEFT JOIN dwd_dim_source_code     s ON s.source_code = f.source_code WHERE s.source_code IS NULL) AS orphan_source;
