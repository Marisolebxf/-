-- 只读核验；Doris / gkx_technology_analysis_dev。
-- 凭据通过进程环境提供，不写在 SQL 中。

-- M01：源 5,051,578 行，规范方向 2,525,789 行，无自环。
SELECT COUNT(*) AS source_rows,
       SUM(talent_id < collaborator_talent_id) AS canonical_rows,
       SUM(talent_id = collaborator_talent_id) AS self_loops,
       SUM(co_project_count IS NULL) AS co_project_null
FROM ads_talent_collaborator;

-- M03：202,795 行的机构端 100% 为 company，不能记为人才—科研机构。
SELECT COUNT(*) AS source_rows,
       SUM(i.institution_type_id = 'company') AS company_rows,
       COUNT(DISTINCT c.institution_id) AS institution_count
FROM ads_talent_institution_cooperation c
LEFT JOIN ads_institution_profile i ON c.institution_id = i.institution_id;

-- M04：72,503 个工作关系对包含 404 个 company 对。
SELECT COUNT(*) AS work_rows,
       COUNT(DISTINCT CONCAT(e.talent_id, '|', e.institution_id)) AS work_pairs,
       SUM(i.institution_type_id = 'company') AS company_rows,
       COUNT(DISTINCT CASE WHEN i.institution_type_id = 'company'
                          THEN CONCAT(e.talent_id, '|', e.institution_id) END) AS company_pairs
FROM ads_talent_experience e
JOIN ads_institution_profile i ON e.institution_id = i.institution_id
WHERE e.experience_type = 2;

-- M04：最终应灌分母为 84,169 行工作经历合并成的 72,099 对。
SELECT COUNT(*) AS eligible_work_rows,
       COUNT(DISTINCT CONCAT(e.talent_id, '|', e.institution_id)) AS eligible_work_pairs
FROM ads_talent_experience e
JOIN ads_institution_profile i ON e.institution_id = i.institution_id
WHERE e.experience_type = 2 AND i.institution_type_id <> 'company';

-- 图中机构 Tag 仍承载完整主数据，不能在点层面去掉 company。
SELECT institution_type_id, COUNT(*) AS source_rows
FROM ads_institution_profile
GROUP BY institution_type_id ORDER BY institution_type_id;

-- M02 已按 832923ec 移交 T02，此文件不查询或导入机构合作年表。
