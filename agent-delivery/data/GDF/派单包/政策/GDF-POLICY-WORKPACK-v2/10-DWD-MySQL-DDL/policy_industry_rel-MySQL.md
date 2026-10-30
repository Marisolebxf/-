# `policy_industry_rel`（Wave C 建表，不参与 Wave B Mapping）

> **日期**：2026-10-26  
> **谁写**：POLICY-C1 抽取产业。Wave B 的 CDC **不要**洗这张表，也不要从 ODS 灌主题名进来。  
> DWD 与 ADS **同结构**。抽取写 DWD 后，按 `policy_id` 把该政策的行替换进 ADS（`id` 一致）。

结构真源：[dwd.md 的 `policy_industry_rel` 节](../../../../../data-design/storage/POLICY/stores/mysql/dwd.md)。库名 `demo_gkxlumenx_dwd`。

ADS 同结构，只换库名，见 [ads.md](../../../../../data-design/storage/POLICY/stores/mysql/ads.md)。库名 `demo_gkxlumenx_ads`。

产线执行时把 `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` 换成 `gkxlumenx_dwd` / `gkxlumenx_ads`。表结构不另写。

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`policy_industry_rel` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `policy_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '对应 policy_base_info.policy_id',
  `industry_name` varchar(200) NOT NULL DEFAULT '' COMMENT '产业名',
  `industry_link_code` varchar(128) NOT NULL DEFAULT '' COMMENT 'chain: / segment:；仅名称时为空串',
  `is_deleted` tinyint NOT NULL DEFAULT 0 COMMENT '0 有效，1 逻辑删除',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '写入时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '最近一次同步时间',
  PRIMARY KEY (`id`),
  KEY `idx_policy_industry_rel_pid` (`policy_id`, `is_deleted`),
  KEY `idx_policy_industry_rel_code` (`industry_link_code`, `is_deleted`, `policy_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='政策–产业关联。抽取写入，不回写主表';
```

目标键，现网未改：`(policy_id, industry_link_code)` 唯一。DWD 与 ADS 同一目标。上面的 CREATE 仍是现网已有结构。清重口径待确认。现网若已有重复行，不能加这个键。不要按这句话去改现网。
