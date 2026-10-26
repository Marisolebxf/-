从 dwd.md 原样复制。空表，不从 ADS 拷行。

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_dwd`.`policy_text_parse` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `policy_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `summary` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '摘要',
  `structured_elements` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '结构化要素',
  `auto_tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '自动标签',
  `model_version` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '规则基线产物须在 UI 标注模型版本',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='D1 政策文本解析：摘要 + 结构化要素 + 自动标签';
```
