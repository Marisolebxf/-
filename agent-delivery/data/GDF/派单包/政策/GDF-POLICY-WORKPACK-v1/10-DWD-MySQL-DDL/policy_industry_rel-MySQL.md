# `policy_industry_rel`（Wave C 建表，不参与 Wave B Mapping）

> **日期**：2026-10-23  
> **谁写**：POLICY-C1 抽取产业。Wave B 的 CDC **不要**洗这张表，也不要从 ODS 灌主题名进来。  
> DWD 与 ADS **同结构**。抽取写 DWD 后，按 `policy_id` 把该政策的行替换进 ADS（`id` 一致）。

库：`gkxlumenx_dwd` 与 `gkxlumenx_ads`。下面 DDL 两库各执行一次。

```sql
CREATE TABLE IF NOT EXISTS `policy_industry_rel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `policy_id` varchar(128) NOT NULL COMMENT '对应 policy_base_info.policy_id',
  `industry_name` varchar(200) NOT NULL DEFAULT '' COMMENT '产业名',
  `industry_link_code` varchar(128) NOT NULL DEFAULT '' COMMENT 'chain: / segment:；仅名称时为空串',
  `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '0 有效，1 逻辑删除',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_policy_industry_rel_pid` (`policy_id`, `is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='政策–产业关联。抽取写入，不回写主表';
```

读有效关联：`is_deleted=0`。覆盖度只计 DWD 上带 `industry_link_code` 的有效行，ADS 镜像不另计。
