-- 政策 round1 产线变更。只执行本文件一次。本仓不代跑。
-- 库：gkxlumenx_dwd、gkxlumenx_ads。不要 DROP。不改已有列类型。
-- 不改 policy_base_info 的主键，也不改唯一键 (source_plane, policy_id)。
-- 不回刷 policy_support。不碰备份表。
--
-- 清重口径（2026-10-30 确定）：
-- 1. policy_industry_rel（DWD、ADS 各做一遍）：
--    键是 (policy_id, industry_link_code)，空串也算一个键。
--    同一键多行时留一行：优先 is_deleted=0；同状态下 update_time 最新；时间相同留 id 最大。
--    其余物理删除。不能只改 is_deleted，唯一键不含删除标记，软删行仍占键。
--    链码为空、产业名不同的多行也并成一行。这是该唯一键的结果。
-- 2. policy_text_parse（只改 ADS）：
--    完整 policy_id 相同的多行，留 update_time 最新，时间相同留 id 最大，其余物理删除。
--    完整 policy_id 不同、仅前 64 字相同：不删。后面的唯一索引会失败，到此停。
--    policy_id 为 NULL 的行不参与清重。
-- 3. policy_base_info：只加普通索引，不删行。两平面相同 policy_id 都保留。
-- 4. DWD 的 policy_text_parse 本轮不改。C2 只写 ADS。

-- ---------- 1. 新建 script_state ----------

CREATE TABLE IF NOT EXISTS `gkxlumenx_dwd`.`script_state` (
  `job`          varchar(16)  NOT NULL COMMENT '作业标识：c1 抽取产业 / c2 条款结构化',
  `policy_id`    varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '对应 policy_base_info.policy_id',
  `content_hash` varchar(32)  NOT NULL DEFAULT '' COMMENT '输入指纹；变了才重算（C1=title+keywords+abstract+content，C2=title+abstract+content）',
  `status`       varchar(20)  NOT NULL COMMENT 'done|empty|no_match|degraded|failed|llm_unavailable',
  `batch_id`     varchar(32)  NOT NULL DEFAULT '' COMMENT '本趟运行标识 yyyyMMddHHmmss',
  `tried_at`     datetime     NOT NULL COMMENT '最近一次尝试时间',
  `next_try_at`  datetime     DEFAULT NULL COMMENT '下次可重试时间；NULL=终态不再自动重试',
  `try_count`    int          NOT NULL DEFAULT 0 COMMENT '累计尝试次数',
  `note`         varchar(500) NOT NULL DEFAULT '' COMMENT '备注，如命中链码数、失败原因',
  PRIMARY KEY (`job`, `policy_id`),
  KEY `idx_job_due` (`job`, `next_try_at`, `policy_id`),
  KEY `idx_job_status` (`job`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='脚本作业状态：一次处理一行，供增量判定与排障使用';

-- ---------- 2. 关联表清重后加唯一键 ----------

DELETE t
FROM `gkxlumenx_dwd`.`policy_industry_rel` AS t
INNER JOIN `gkxlumenx_dwd`.`policy_industry_rel` AS k
  ON k.`policy_id` = t.`policy_id`
 AND k.`industry_link_code` = t.`industry_link_code`
 AND (
      (k.`is_deleted` = 0 AND t.`is_deleted` <> 0)
   OR (
        k.`is_deleted` = t.`is_deleted`
        AND (
             IFNULL(k.`update_time`, '1000-01-01 00:00:00') > IFNULL(t.`update_time`, '1000-01-01 00:00:00')
          OR (
               IFNULL(k.`update_time`, '1000-01-01 00:00:00') = IFNULL(t.`update_time`, '1000-01-01 00:00:00')
               AND k.`id` > t.`id`
             )
        )
      )
    );

DELETE t
FROM `gkxlumenx_ads`.`policy_industry_rel` AS t
INNER JOIN `gkxlumenx_ads`.`policy_industry_rel` AS k
  ON k.`policy_id` = t.`policy_id`
 AND k.`industry_link_code` = t.`industry_link_code`
 AND (
      (k.`is_deleted` = 0 AND t.`is_deleted` <> 0)
   OR (
        k.`is_deleted` = t.`is_deleted`
        AND (
             IFNULL(k.`update_time`, '1000-01-01 00:00:00') > IFNULL(t.`update_time`, '1000-01-01 00:00:00')
          OR (
               IFNULL(k.`update_time`, '1000-01-01 00:00:00') = IFNULL(t.`update_time`, '1000-01-01 00:00:00')
               AND k.`id` > t.`id`
             )
        )
      )
    );

SET @sql := (
  SELECT IF(
    EXISTS (
      SELECT 1 FROM information_schema.statistics
      WHERE table_schema = 'gkxlumenx_dwd'
        AND table_name = 'policy_industry_rel'
        AND index_name = 'uk_pid_code'
    ),
    'SELECT 1',
    'ALTER TABLE `gkxlumenx_dwd`.`policy_industry_rel` ADD UNIQUE KEY `uk_pid_code` (`policy_id`, `industry_link_code`)'
  )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    EXISTS (
      SELECT 1 FROM information_schema.statistics
      WHERE table_schema = 'gkxlumenx_ads'
        AND table_name = 'policy_industry_rel'
        AND index_name = 'uk_pid_code'
    ),
    'SELECT 1',
    'ALTER TABLE `gkxlumenx_ads`.`policy_industry_rel` ADD UNIQUE KEY `uk_pid_code` (`policy_id`, `industry_link_code`)'
  )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ---------- 3. 条款表：只删完整 policy_id 相同的重复行，再加前缀唯一索引 ----------

DELETE t
FROM `gkxlumenx_ads`.`policy_text_parse` AS t
INNER JOIN `gkxlumenx_ads`.`policy_text_parse` AS k
  ON t.`policy_id` IS NOT NULL
 AND k.`policy_id` = t.`policy_id`
 AND (
      IFNULL(k.`update_time`, '1000-01-01 00:00:00') > IFNULL(t.`update_time`, '1000-01-01 00:00:00')
   OR (
        IFNULL(k.`update_time`, '1000-01-01 00:00:00') = IFNULL(t.`update_time`, '1000-01-01 00:00:00')
        AND k.`id` > t.`id`
      )
    );

-- 完整 policy_id 不同、前 64 字相同：不删。有这种行时下面这条失败，后面的索引不要改前缀去绕。
SET @pfx := (
  SELECT COUNT(*) FROM (
    SELECT LEFT(`policy_id`, 64) AS p64
    FROM `gkxlumenx_ads`.`policy_text_parse`
    WHERE `policy_id` IS NOT NULL
    GROUP BY LEFT(`policy_id`, 64)
    HAVING COUNT(DISTINCT `policy_id`) > 1
  ) d
);
SET @sql := IF(
  @pfx = 0,
  'SELECT 1',
  'SELECT `stop_policy_id_prefix64_clash` FROM `gkxlumenx_ads`.`policy_text_parse` LIMIT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql := (
  SELECT IF(
    EXISTS (
      SELECT 1 FROM information_schema.statistics
      WHERE table_schema = 'gkxlumenx_ads'
        AND table_name = 'policy_text_parse'
        AND index_name = 'uk_ptp_pid'
    ),
    'SELECT 1',
    'ALTER TABLE `gkxlumenx_ads`.`policy_text_parse` ADD UNIQUE KEY `uk_ptp_pid` (`policy_id`(64))'
  )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ---------- 4. 主表普通索引。不清重 ----------

SET @sql := (
  SELECT IF(
    EXISTS (
      SELECT 1 FROM information_schema.statistics
      WHERE table_schema = 'gkxlumenx_dwd'
        AND table_name = 'policy_base_info'
        AND index_name = 'idx_pid'
    ),
    'SELECT 1',
    'ALTER TABLE `gkxlumenx_dwd`.`policy_base_info` ADD KEY `idx_pid` (`policy_id`)'
  )
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
