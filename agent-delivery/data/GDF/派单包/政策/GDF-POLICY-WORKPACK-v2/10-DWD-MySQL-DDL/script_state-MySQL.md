# `script_state`（C1 / C2 作业留痕）

> **日期**：2026-10-30  
> **状态**：要执行的文件是 [sql/script_state.sql](../sql/script_state.sql)。在 `gkxlumenx_dwd` 执行一次。本仓不代跑。脚本发现缺表时退出码 4，并且不建表。  
> **谁写**：`scripts/policy_c1_industry.py`、`scripts/policy_c2_clauses.py`。不是 Wave B 的 Mapping 表。

`policy_id` 为 `varchar(100)`，排序规则 `utf8mb4_0900_ai_ci`，与 `policy_base_info.policy_id` 一致。两边不一致时，列对列比较会报 1267。

下面与 `sql/script_state.sql` 是同一份建表语句。执行以那个文件为准。不要 `DROP`。

```sql
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
```

无产出（`empty` / `no_match` / `degraded` / `llm_unavailable`）也必须留一行。否则下一轮会反复选中同一条，出现写了 0 行但退出码 0。

这张表不是业务写库边，不进 `01-data-flow.md`。
