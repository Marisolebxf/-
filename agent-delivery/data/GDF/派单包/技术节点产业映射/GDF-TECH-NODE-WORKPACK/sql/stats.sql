-- 只读。不是作业。已映射 = 至少一条非空 node_id。未映射 = 已同步但没有这样的行。
-- name_zh 原样列出。展示名由调用方在中文为空时改用 name_en，本查询不把英文写进中文列。

SELECT 'mapped' AS side, technology_node_id, MAX(name_zh) AS name_zh, MAX(name_en) AS name_en
FROM `gkxlumenx_dwd`.`dwd_tech_node_industry_map`
GROUP BY technology_node_id
HAVING SUM(CASE WHEN node_id IS NOT NULL AND node_id <> '' THEN 1 ELSE 0 END) > 0
UNION ALL
SELECT 'unmapped' AS side, technology_node_id, MAX(name_zh) AS name_zh, MAX(name_en) AS name_en
FROM `gkxlumenx_dwd`.`dwd_tech_node_industry_map`
GROUP BY technology_node_id
HAVING SUM(CASE WHEN node_id IS NOT NULL AND node_id <> '' THEN 1 ELSE 0 END) = 0;
