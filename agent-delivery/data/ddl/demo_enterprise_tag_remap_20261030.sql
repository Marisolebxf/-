-- enterprise_tag 标签码重映射修复（demo 库，as-built 2026-10-30）
-- 背景：gdf_sim.map_tags（lumen-algo-py/vendor/entan-py）曾把三方 55 中文标签
--       粗归并成 6 个英文码 + sme_tech 兜底，同码多条不同 tag_value 导致
--       /profile/qualifications 同码重复（如 国家级/普通高新技术企业 挤在 high_tech）。
-- 修复：按 tag_value = tag_dict.tag_name 精确字面 JOIN，重写 tag_code/tag_name/tag_category。
-- 前置：tag_dict 55 值种子已灌（gkxlumenx_dwd_tag_dict_supplier_seed-executed.sql）。
-- 注意：demo 表 enterprise_tag 无 tag_level 列（GDF 09 §3.9 口径：层级只留 tag_dict），
--       故 UPDATE 不含 tag_level；tag_value='1' 的 key_enterprise 标记行不动（非三方标签）。
-- 执行：2026-10-30 经 database MCP（连接 gkxlumenx-dwd-public）
--       备份表 demo_gkxlumenx_dwd.enterprise_tag_bak_20261030（230,555 行）
--       两步 UPDATE 各 affectedRows = 202,423
-- 后续：ETL tag_info full 重刷 ES（MYSQL_DWD_DB=demo_gkxlumenx_dwd）→ 60,078 orgs 0 errors，
--       ES tags.tag_code 呈 55 新码 + key_enterprise，同码多 value 归并消除。

-- 1) tag_code ← 字典（字面精确匹配，只动 55 值内的行）
UPDATE demo_gkxlumenx_dwd.enterprise_tag t
JOIN demo_gkxlumenx_dwd.tag_dict d ON d.tag_name = t.tag_value
SET t.tag_code = d.tag_code;

-- 2) tag_name / tag_category ← 字典（如需 tag_level，先 ALTER 加列）
UPDATE demo_gkxlumenx_dwd.enterprise_tag t
JOIN demo_gkxlumenx_dwd.tag_dict d ON d.tag_name = t.tag_value
SET t.tag_name = d.tag_name,
    t.tag_category = d.tag_category;
