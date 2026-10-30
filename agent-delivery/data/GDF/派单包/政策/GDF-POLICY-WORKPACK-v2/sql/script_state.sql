-- C1 / C2 作业留痕。库 gkxlumenx_dwd。
-- 可重复执行。不要 DROP。
-- policy_id 排序规则必须与 policy_base_info.policy_id 同为 utf8mb4_0900_ai_ci。
-- 缺这张表时脚本退出码 4，脚本自己不建表。

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
