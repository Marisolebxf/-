-- 只读核对。不要放进同步或关联作业。
-- 已映射 = 该 subfield_id 至少有一条非空 node_id。
-- 未映射 = 已在表里、但没有任何非空 node_id。

SELECT 'mapped' AS side, subfield_id, MAX(name_zh) AS name_zh
FROM `gkxlumenx_dim`.`subfield_topic_map`
GROUP BY subfield_id
HAVING SUM(CASE WHEN node_id IS NOT NULL AND node_id <> '' THEN 1 ELSE 0 END) > 0
UNION ALL
SELECT 'unmapped' AS side, subfield_id, MAX(name_zh) AS name_zh
FROM `gkxlumenx_dim`.`subfield_topic_map`
GROUP BY subfield_id
HAVING SUM(CASE WHEN node_id IS NOT NULL AND node_id <> '' THEN 1 ELSE 0 END) = 0
ORDER BY side, name_zh, subfield_id;
