> **【GDF-ENT-WORKPACK-v3.1.3】** 本文 = 汇总表结构对照。GDF **不算** 8 件套 / 算法分；第 4 类 KPI 不洗。不施工 demo。

---

# DWD 表结构设计—企业指标汇总表—MySQL v3.1

> **现行存储入口（S4）**：[`../storage/ENT/stores/mysql/dwd-aggregate.md`](../storage/ENT/stores/mysql/dwd-aggregate.md) · 总览 [`../storage/ENT/README.md`](../storage/ENT/README.md)  
> 本文保留为 **as-built DDL 细表真源**（stores 外链至此）。

> 整理日期：2026-08-11；现网纠偏复核：2026-08-12
> 整理范围：从已归档旧版 `agent-delivery/_archive/2026-08/data-design-企业-legacy/DWD表结构设计-企业模块-old.md` 中摘出的指标/统计汇总类表
> 现网核对库：MySQL 8.0 `gkxlumenx_dwd`
> 执行记录：2026-08-12 经 human:徐滕强授权完成 `enterprise_risk_summary` 长表重建，详见 §7

## 1. 适用边界

旧版文档混合了 PostgreSQL 草案、工商实体、司法明细、算法评分、配置名单和统计汇总。本次只保留旧版明确作为**统计汇总或预聚合**设计的 8 张表：

| # | 表名 | 统计粒度 | 旧版来源 | 现网状态 |
|---:|---|---|---|---|
| 1 | `enterprise_region_summary` | 区域 × 类型 × 统计日 | §3.4b / §5.1 | 已落库，结构基本一致 |
| 2 | `enterprise_industry_distribution` | 区域 × 产业链 × 统计日 | §3.4b / §5.2 | 已落库，结构基本一致 |
| 3 | `enterprise_growth_trend` | 区域 × 年 × 月 × 统计日 | §3.4b / §5.3 | 已落库，结构基本一致 |
| 4 | `enterprise_industry_summary` | 产业链 × 年 × 统计日 | §3.4c / §5.4 | 已落库，结构基本一致 |
| 5 | `enterprise_stat_summary` | 统计类型 × 维度 × 年 × 统计日 | §3.4d / §7b.1 | 已落库，结构基本一致 |
| 6 | `enterprise_type_scale_stats` | 类型 × 规模 × 区域 × 统计日 | §3.4d / §7b.2 | 已落库，结构与 v3.0 当前目标一致 |
| 7 | `shenzhen_enterprise_summary` | 统计类型 × 维度 × 年 × 统计日 | §10 | 已落库，结构基本一致 |
| 8 | `enterprise_risk_summary` | 企业 × 风险类型 | §3.5 / §6（原文小节 5.3） | 2026-08-12 已按目标长表重建 |
| 9 | `enterprise_org_type` | 企业 × 机构类型 | 2026-08-12 新增 | 已落库，0 行 |

本文不是指标元数据目录，不替代 `cfg_metric`、指标 8 件套或四维就绪度矩阵。

## 2. 明确排除

| 表名 | 排除原因 | 去向 |
|---|---|---|
| `enterprise_score` | 算法评分产物，旧版已明确归 ADS，不是 DWD 汇总表 | 算法/ADS 设计 |
| `enterprise_star` | 人工维护的明星企业配置名单，不是指标表 | 配置/运营设计 |
| `enterprise_distribution` | v3.0 后新增，不属于本次“从旧版文档摘出”的范围 | `DWD表结构设计-企业模块-MySQL-v3.0.md` |
| `sz_city_benchmark` | v3.0 后新增，不属于本次“从旧版文档摘出”的范围 | `DWD表结构设计-企业模块-MySQL-v3.0.md` |
| `enterprise_patent_history` / `enterprise_finance_history` | 企业级历史明细/快照，可作为指标原料，但不是跨企业预聚合表 | 工商/实体设计 |

## 3. 表结构摘编

以下字段采用 **MySQL 现网名称和类型**；统计语义来自旧版文档。未把旧版 PostgreSQL `FILTER`、`LATERAL`、`generate_series` 等示例 SQL 搬入，避免被误当作 MySQL 可执行脚本。

### 3.1 `enterprise_region_summary`

- 用途：区域 KPI 卡片和区域热力。
- 唯一粒度：`region_id + region_type + stat_date`。
- 字段：`id bigint AI PK`、`region_id varchar(20)`、`region_name varchar(100)`、`region_type varchar(20)`、`parent_region_id varchar(20)`、`stat_date date`、`enterprise_total bigint`、`new_enterprise_count bigint`、`active_enterprise_count bigint`、`total_revenue decimal(20,2)`、`create_time datetime`、`update_time datetime`。

### 3.2 `enterprise_industry_distribution`

- 用途：区域内产业分布。
- 唯一粒度：`region_id + chain_code + stat_date`。
- 字段：`id bigint AI PK`、`region_id varchar(20)`、`chain_code varchar(64)`、`chain_name varchar(255)`、`enterprise_count bigint`、`stat_date date`、`create_time datetime`、`update_time datetime`。

### 3.3 `enterprise_growth_trend`

- 用途：区域企业月度增长趋势。
- 唯一粒度：`region_id + stat_year + stat_month + stat_date`。
- 字段：`id bigint AI PK`、`region_id varchar(20)`、`stat_year int`、`stat_month int`、`new_enterprise_count bigint`、`stat_date date`、`create_time datetime`、`update_time datetime`。

### 3.4 `enterprise_industry_summary`

- 用途：产业维度 KPI、产业对比和年度趋势。
- 唯一粒度：`chain_code + stat_year + stat_date`。
- 字段：`id bigint AI PK`、`chain_code varchar(64)`、`chain_name varchar(255)`、`stat_year int`、`enterprise_count bigint`、`research_staff_total bigint`、`patent_total bigint`、`high_tech_count bigint`、`stat_date date`、`create_time datetime`、`update_time datetime`。
- 特殊语义：旧版约定 `chain_code='ALL'` 表示跨产业按 `org_id` 去重后的汇总行，不能直接累加各产业行代替。

### 3.5 `enterprise_stat_summary`

- 用途：重点企业、明星企业、资质和产业企业数等通用单维统计。
- 唯一粒度：`stat_type + dim_code + stat_year + stat_date`。
- 字段：`id bigint AI PK`、`stat_type varchar(50)`、`dim_code varchar(100)`、`dim_name varchar(255)`、`stat_year int`、`stat_value bigint`、`stat_date date`、`create_time datetime`、`update_time datetime`。
- 旧版已定义的 `stat_type`：`key_enterprise_chain`、`key_enterprise_node`、`key_enterprise_district`、`qualification_count`、`industry_enterprise_count`、`star_enterprise_node`、`star_enterprise_district`、`patent_valid_count`、`high_value_patent_count`。
- 注意：上述枚举是旧版设计清单，不代表其数据已经全部生产就绪。

### 3.6 `enterprise_type_scale_stats`

- 用途：企业类型 × 企业规模 × 区域的三维交叉统计。
- 现网唯一粒度：`company_type + enterprise_scale + region_level + region_id + stat_date`。
- 现网字段：`id bigint AI PK`、`company_type varchar(100)`、`enterprise_scale varchar(20)`、`region_level varchar(20)`、`region_id varchar(20)`、`region_name varchar(100)`、`enterprise_count bigint`、`stat_date date`、`create_time datetime`、`update_time datetime`。
- 旧稿曾使用 `region_code`；v3.0 当前目标和现网均使用 `region_id`，不再列为现网结构问题。

### 3.7 `shenzhen_enterprise_summary`

- 用途：深圳企业总数、重点企业数、产业分布和历年累计增长。
- 唯一粒度：`stat_type + dim_code + stat_year + stat_date`。
- 字段：`id bigint AI PK`、`stat_type varchar(50)`、`dim_code varchar(100)`、`dim_name varchar(255)`、`stat_year int`、`stat_value bigint`、`stat_date date`、`create_time datetime`、`update_time datetime`。
- 旧版已定义的 `stat_type`：`enterprise_total`、`key_enterprise_total`、`industry_distribution`、`yearly_growth`。
- 特殊语义：`yearly_growth` 是截至该年末的累计企业数，不是该年新增企业数。

### 3.8 `enterprise_risk_summary`

- 粒度：`org_id + risk_type`。
- 用途：企业检索风险筛选、企业详情风险计数；接口不再扫描原始风险明细表。
- 现网字段：`id bigint AI PK`、`org_id varchar(64) COLLATE utf8mb4_general_ci NOT NULL`、`risk_type varchar(50) NOT NULL`、`total_count int NOT NULL`、`current_count int NOT NULL`、`history_count int NOT NULL`、`latest_date date`、`create_time datetime`、`update_time datetime`。
- 唯一约束：`UNIQUE(org_id, risk_type)`。
- 索引：`(risk_type, total_count)`、`(org_id)`。
- 2026-08-12 实际结果：28,758 个“企业 × 风险类型”汇总行，覆盖 28,183 个 `org_id`，累计 87,396 条风险记录；所有行满足 `total_count = current_count + history_count`。

## 4. 设计原则

1. 汇总表只服务稳定统计粒度；区域、产业、时间和多维交叉不要强塞进同一张万能表。
2. 跨产业总数必须按企业去重，不能把各产业数量相加。
3. `stat_type` 只能使用受控枚举；新增口径需同步指标元数据和 ETL，不允许页面自行解释。
4. 汇总表必须保留 `stat_date`，接口读取时明确最新成功批次，不能默认“表内所有行都是当前值”。
5. 业务口径未确认时保持待确认状态，不在文档或数据中擅自改绿。

## 5. 当前问题与后续动作

| 优先级 | 问题 | 影响 | 建议动作 |
|---|---|---|---|
| 已关闭 | `enterprise_risk_summary` 原全局 1 行宽表缺企业标识 | 2026-08-12 已按 `org_id + risk_type` 重建 | 保留 `enterprise_risk_summary__pre_fix_20260812` 供观察期回退 |
| 已关闭 | `enterprise_type_scale_stats` 旧稿使用 `region_code` | v3.0 与现网均为 `region_id` | 按现行契约保持不变 |
| P1 | 多个统计口径仍依赖重点企业、科研人员、明星企业等业务定义 | 指标值可能口径不一致 | 对照客户决策清单和指标矩阵确认后再生产化 |
| P2 | 旧版 ETL 示例为 PostgreSQL 语法 | 不能直接在 MySQL 执行 | 后续单独编写并验证 MySQL ETL SQL |

## 6. 核对结论

- 从旧版文档中确认并摘出统计汇总类表：**8 张**。
- `enterprise_distribution`、`sz_city_benchmark` 不再混入本次摘编。
- `enterprise_score`、`enterprise_star` 不再作为 DWD 指标汇总表列入。
- 除 `enterprise_risk_summary` 外，其余 7 张汇总表本次未改结构。

## 7. 2026-08-12 `enterprise_risk_summary` As-built

- 执行脚本：`agent-delivery/data/ddl/gkxlumenx_dwd_enterprise_schema_align_20260812.sql`。
- 原全局 1 行宽表已原子切换为规范长表；原表保留为
  `enterprise_risk_summary__pre_fix_20260812`。
- 汇总来源：`risk_judicial_case`、`risk_executed`、`risk_bankruptcy + risk_bankruptcy_party`、`risk_abnormal`、`risk_punishment`、`risk_illegal`、`risk_tax_punish`。
- 当前/历史规则：异常和严重违法按 `remove_date` 判定；破产按主表 `history_status` 判定；其余来源无历史信号的有效记录暂按当前记录计数。该规则只反映源数据可用字段，不伪造历史状态。
- 数据完整性：必填键缺失 0、唯一键重复 0、汇总等式异常 0。
- 关联键：`enterprise_risk_summary.org_id` 与全部含 `org_id` 的规范风险表
  已统一为 `utf8mb4_general_ci`，与 `enterprise_base.org_id` 直接 JOIN
  验证通过。
- 兼容验证：`lumen-algo-py` DWD 读取测试 7/7 通过；topic-py 风险 ORM/Repository 契约测试 37/37 通过；现网汇总查询 smoke test 通过。

### 7.1 As-built `CREATE TABLE`（2026-10-22 从现网 `information_schema` 逐列核对补录，与 GDF round2 问询 #30 对应）

```sql
CREATE TABLE `enterprise_risk_summary` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `org_id` varchar(64) NOT NULL COMMENT '企业唯一标识（gkxlumenx_dwd.enterprise_base.org_id）',
  `risk_type` varchar(50) NOT NULL COMMENT '风险类型（judicial_case/executed/bankruptcy/abnormal/punishment/illegal/tax_punish）',
  `total_count` int NOT NULL COMMENT '风险记录总数',
  `current_count` int NOT NULL COMMENT '当前有效记录数',
  `history_count` int NOT NULL COMMENT '历史记录数',
  `latest_date` date DEFAULT NULL COMMENT '最新风险事件日期',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_org_risk` (`org_id`,`risk_type`),
  KEY `idx_risk_type_count` (`risk_type`,`total_count`),
  KEY `idx_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业风险汇总长表（企业 × 风险类型）';
```

## 8. 2026-08-12 `enterprise_org_type` 新增

### 8.1 用途

企业机构类型标签表。一个企业可以同时具有多个机构类型（如既是科研机构又是服务机构）。

| 机构类型 | org_type | 说明 | 打标规则（初版） |
|---|---|---|---|
| 服务机构 | `service_org` | 提供专业服务的机构（律所、咨询、检测、知识产权等） | 🟡 待细化：按经营范围关键词匹配 |
| 科研机构 | `research_org` | 科研院所、高校实验室、研发型企业等 | 从科研机构表（`dwd_research_institute_base_info`）读出的 org_id 直接打标 |
| 政策机构 | `policy_org` | 政府部门、政策研究机构、事业单位等 | 🟡 待细化：按登记机关/企业类型/经营范围匹配 |
| 常规企业 | `regular_ent` | 一般工商企业 | 默认值，未打标的企业即为常规企业，可不显式写入 |

> `regular_ent` 可不显式打标——不在本表中的企业默认为常规企业，查询时 LEFT JOIN 未命中即为常规。

### 8.2 DDL

```sql
CREATE TABLE `enterprise_org_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT '企业机构ID（关联 enterprise_base.org_id）',
  `org_type` varchar(32) COLLATE utf8mb4_general_ci NOT NULL COMMENT '机构类型：service_org=服务机构 / research_org=科研机构 / policy_org=政策机构 / regular_ent=常规企业',
  `org_type_name` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '机构类型中文名（冗余，便于查询展示）',
  `source` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '打标来源：manual=人工 / rule=规则匹配 / algo=算法识别',
  `is_primary` tinyint NOT NULL DEFAULT 0 COMMENT '是否主类型 0/1（一个企业最多一个主类型）',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_org_type` (`org_id`, `org_type`),
  KEY `idx_org_type` (`org_type`),
  KEY `idx_org_id` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='企业机构类型标签（一个企业可多类型）';
```

### 8.3 设计说明

- **唯一键 `uk_org_type (org_id, org_type)`**：防止同一企业同一类型重复打标，支持 upsert 幂等
- **`is_primary`**：一个企业可多类型，但主类型只能有一个，用于默认展示和统计
- **`source`**：记录打标来源，科研机构从源表直接读取消化为 `rule`，经营范围匹配的也为 `rule`，人工调整的为 `manual`
- **打标规则（初版）**：
  - 科研机构：从 `dwd_research_institute_base_info` 读取 org_id，直接打 `research_org`
  - 服务机构/政策机构：🟡 待细化，初步方向是按 `enterprise_extra.business_scope` 经营范围关键词匹配
  - 常规企业：不显式打标，默认值
- **与 `enterprise_tag` 的关系**：`enterprise_tag` 是资质/荣誉/规模维度（高新技术企业、上市企业等），`enterprise_org_type` 是机构性质维度（科研/服务/政策），两者独立，一个企业可以同时有资质标签和机构类型标签
