从 ads.md 原样复制，库名不改。

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_level_dist` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `stat_date` date DEFAULT NULL COMMENT '统计日期/批次快照日',
  `level` bigint DEFAULT NULL COMMENT '层级 1国家/2省/3市/4区县；NULL=全量汇总行',
  `policy_count` bigint DEFAULT NULL COMMENT '政策去重数',
  `ratio` decimal(38,10) DEFAULT NULL COMMENT '占比%',
  `valid_count` bigint DEFAULT NULL COMMENT '有效政策数（M_POLICY_VALIDITY_RATE 分子）',
  `validity_rate` decimal(38,10) DEFAULT NULL COMMENT '政策时效=有效/总数%',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_LEVEL_DIST/M_POLICY_TOTAL_COUNT/M_POLICY_VALIDITY_RATE',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='层级/总数/时效';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_type_dist` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `policy_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `policy_count` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `ratio` decimal(38,10) DEFAULT NULL COMMENT '占比%',
  `yoy` decimal(38,10) DEFAULT NULL COMMENT '同比增长率%',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_TYPE_DIST',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='类型分布';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_timeseries` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `period_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'Y/Q/M 粒度',
  `period_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '如 2025 / 2025Q1 / 2025-03',
  `publish_count` bigint DEFAULT NULL COMMENT '发布量',
  `growth_rate` decimal(38,10) DEFAULT NULL COMMENT '环比增长率%',
  `continuity_rate` decimal(38,10) DEFAULT NULL COMMENT '连续性指标%',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_TIMESERIES',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='发布时序';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_national_dist` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `province_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '省级区划码 <- dim_region',
  `province_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `policy_count` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `yoy` decimal(38,10) DEFAULT NULL COMMENT '同比增长率%',
  `center_lng` decimal(38,10) DEFAULT NULL COMMENT '省中心经度(地图渲染)',
  `center_lat` decimal(38,10) DEFAULT NULL COMMENT '省中心纬度',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_NATIONAL_DIST',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='分省';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_sz_dist` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `district_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '深圳区县区划码 <- dim_region',
  `district_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '福田/南山/宝安/龙岗…',
  `policy_count` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `yoy` decimal(38,10) DEFAULT NULL COMMENT '增长趋势%',
  `center_lng` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `center_lat` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_SZ_DIST',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='深圳分区';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_focus` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `policy_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '单政策粒度；NULL=区域/产业汇总',
  `region_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `focus_score` decimal(38,10) DEFAULT NULL COMMENT '政策焦点指数（QPOL-02）',
  `opportunity_cnt` bigint DEFAULT NULL COMMENT '政策机遇数（QPOL-02）',
  `relation_degree` decimal(38,10) DEFAULT NULL COMMENT '政策关联度（QPOL-03，图谱度中心性）',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_FOCUS_INDEX/M_POLICY_OPPORTUNITY_COUNT/M_POLICY_RELATION_DEGREE',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='焦点/机遇/关联';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_intensity` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `scope_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'province/city/policy 粒度',
  `scope_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '区划码或 policy_id',
  `scope_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `intensity_index` decimal(38,10) DEFAULT NULL COMMENT '政策力度指数（QPOL-02）',
  `intensity_score` decimal(38,10) DEFAULT NULL COMMENT '单政策力度评分（QPOL-02）',
  `industry_coverage` decimal(38,10) DEFAULT NULL COMMENT '产业覆盖度%',
  `rank_no` bigint DEFAULT NULL COMMENT '力度排行',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_INTENSITY_INDEX/M_POLICY_INTENSITY_SCORE/M_POLICY_INDUSTRY_COVERAGE',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='力度/产业覆盖';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_effect` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `scope_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `scope_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `scope_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `effect_score` decimal(38,10) DEFAULT NULL COMMENT '政策效果评分（QPOL-02，含待采购输入）',
  `shortboard_cnt` bigint DEFAULT NULL COMMENT '政策短板数（QPOL-02）',
  `layout_rec_cnt` bigint DEFAULT NULL COMMENT '政策布局建议数（QPOL-02）',
  `impl_effect` decimal(38,10) DEFAULT NULL COMMENT '落地实效性（QPOL-02，含待采购输入）',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='效果/短板/布局';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_metric_timeseries` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'M_POLICY_SUPPORT_STRENGTH/M_POLICY_INDUSTRY_FIT/M_POLICY_IMPLEMENTATION_EFFECT 等',
  `region_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '区域/对标地区',
  `industry_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '目标产业(三维框架)',
  `stat_date` date DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `metric_value` decimal(38,10) DEFAULT NULL COMMENT '指标值',
  `yoy` decimal(38,10) DEFAULT NULL COMMENT '同比%',
  `dim_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '维度键(支持力度/产业适配/落地实效)',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `ext` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'JSON 扩展',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='三维/通用时序';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_graph_node` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `node_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `node_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `weight` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `props` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='点镜像；Nebula 失败时 /v1/policy/graph 可读';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_graph_edge` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `src_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `dst_key` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `relation_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `weight` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `props` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='边镜像';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_entity` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `policy_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `entity_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '取值 policy/level/type/org/region/time/keyword/industry/enterprise/talent/service',
  `entity_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `attributes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `source_field` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '该实体从 DWD 哪一列抽出，D9 字段级血缘',
  `confidence` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `model_version` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='政策核心实体抽取结果，图谱构建的上游';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_text_parse` (
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

目标键：`policy_id` 仍是 `longtext`，不改类型。前 64 个字符的唯一索引在 `sql/update_round1.sql`，只改 ADS。完整 `policy_id` 相同的重复行留最新；全文不同、仅前 64 字相同的不删，加索引会停住。上面的 CREATE 仍是现网结构。DWD 同名表本轮不改。本仓不代跑。

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_match` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `subject_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `subject_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `subject_name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `policy_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `policy_title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `match_score` decimal(38,10) DEFAULT NULL COMMENT '匹配打分',
  `match_reasons` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '匹配理由',
  `rank_no` bigint DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `model_version` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '规则基线产物须在 UI 标注模型版本',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='D2 政策匹配推送：主体 ↔ 政策的匹配打分与理由';
```

```sql
CREATE TABLE IF NOT EXISTS `demo_gkxlumenx_ads`.`policy_simulate` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '现网 demo 有此列，口径待补',
  `scenario_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `scope_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `scope_code` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `params` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `baseline_value` decimal(38,10) DEFAULT NULL COMMENT '基线',
  `simulated_value` decimal(38,10) DEFAULT NULL COMMENT '仿真值',
  `delta_rate` decimal(38,10) DEFAULT NULL COMMENT '现网 demo 有此列，口径待补',
  `curve` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '曲线',
  `explanation` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `model_version` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '规则基线产物须在 UI 标注模型版本',
  `metric_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '现网 demo 有此列，口径待补',
  `calc_batch_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT 'mock_ 前缀区分 Mock',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '现网 demo 有此列，口径待补',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='D3 政策效果推演仿真：基线 vs 仿真值与曲线';
```
