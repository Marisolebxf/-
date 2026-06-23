# 产业链域数据库设计（v1）

> **要素**：产业链（CHAIN / E2）
> **作者**：data-agent（coordinator 接续）
> **日期**：2026-06-23
> **参照**：企业域数据库设计(v1).md（9 DWD + 13 ADS + NebulaGraph）
> **业务键真源**：`gkx-platform-business-keys.md`（`chain_id: VARCHAR(64)`）

---

## 1. 总览

| 层 | 表数量 | 字段总数 |
|----|--------|---------|
| DWD（gkx_chain） | 8 | ~80 |
| ADS（gkx_chain） | 11 | ~120 |
| NebulaGraph | 4 Tags + 6 Edges | — |
| cfg | 2（cfg_metric + cfg_metric_lineage） | 复用平台 |

---

## 2. DWD 标准表

### 2.1 dwd.industry_chain — 产业链主表

| 字段 | 类型 | 注释 | 来源 ODS | 映射状态 |
|------|------|------|---------|---------|
| chain_id | VARCHAR(64) PK | 产业链节点 ID（`chain:{seq}`） | 派生 | ✅ |
| chain_name | VARCHAR(128) | 产业链名称 | dwd_industry_chain_info.chain_name | ✅ |
| parent_chain_id | VARCHAR(64) | 父产业链 ID | dwd_industry_chain_info.parent_chain | ✅ |
| node_name | VARCHAR(128) | 环节名称 | dwd_industry_chain_info.node_name | ✅ |
| node_stage | ENUM('upstream','midstream','downstream') | 上/中/下游 | dwd_industry_chain_info.node_stage | ✅ |
| node_level | INT | 层级（1=产业链，2=环节，3=子环节） | 派生自 parent_chain_id | ✅ |
| is_key_node | TINYINT(1) | 是否关键环节 | 🔧 M8 关键环节识别模型产出 | 🔧 |
| high_value_index | DECIMAL(5,2) | 高端化指数（0~100） | 🔧 M8 产出 | 🔧 |
| description | TEXT | 产业链/环节描述 | dwd_industry_chain_info.description | ✅ |
| calc_batch_id | VARCHAR(64) | 计算批次 | 系统 | ✅ |
| ext | JSON | 扩展字段 | — | ✅ |

### 2.2 dwd.industry_chain_enterprise — 产业链-企业关联

| 字段 | 类型 | 注释 | 来源 ODS | 映射状态 |
|------|------|------|---------|---------|
| id | BIGINT PK AUTO_INCREMENT | 自增主键 | — | ✅ |
| chain_id | VARCHAR(64) | 产业链 ID | dwd_org_industry_chain_dtl.chain_name→chain_id | ✅ |
| enterprise_code | VARCHAR(64) | 企业统一社会信用代码 | dwd_org_industry_chain_dtl.org_name→enterprise_code | ✅ |
| chain_role | VARCHAR(32) | 链中角色（上游/中游/下游） | dwd_org_industry_chain_dtl→node_stage | ✅ |
| participation_depth | DECIMAL(5,2) | 参与深度（0~100） | dwd_org_industry_chain_dtl.chain_score | 🔧 |
| chain_score | DECIMAL(5,2) | 产业链关联得分 | dwd_org_industry_chain_dtl.chain_score | ✅ |
| calc_batch_id | VARCHAR(64) | 计算批次 | 系统 | ✅ |

### 2.3 dwd.industry_chain_product — 产业链-产品关联

| 字段 | 类型 | 注释 | 来源 ODS | 映射状态 |
|------|------|------|---------|---------|
| id | BIGINT PK AUTO_INCREMENT | 自增主键 | — | ✅ |
| chain_id | VARCHAR(64) | 产业链 ID | dwd_org_industry_chain_prod_dtl | ✅ |
| product_name | VARCHAR(256) | 产品名称 | dwd_org_industry_chain_prod_dtl.product_name | ✅ |
| enterprise_code | VARCHAR(64) | 企业代码 | dwd_org_industry_chain_prod_dtl.org_name→code | ✅ |
| segment_key | VARCHAR(64) | 环节标识 | dwd_org_industry_chain_prod_dtl.segment_key | ✅ |
| calc_batch_id | VARCHAR(64) | 计算批次 | 系统 | ✅ |

### 2.4 dwd.industry_chain_patent — 产业链-专利关联

| 字段 | 类型 | 注释 | 来源 ODS | 映射状态 |
|------|------|------|---------|---------|
| id | BIGINT PK AUTO_INCREMENT | 自增主键 | — | ✅ |
| chain_id | VARCHAR(64) | 产业链 ID | dwd_org_industry_chain_pat_dtl | ✅ |
| patent_id | VARCHAR(64) | 专利 ID | dwd_org_industry_chain_pat_dtl.patent_id | ✅ |
| patent_title | VARCHAR(512) | 专利标题 | dwd_org_industry_chain_pat_dtl.patent_title | ✅ |
| enterprise_code | VARCHAR(64) | 企业代码 | dwd_org_industry_chain_pat_dtl.org_name→code | ✅ |
| segment_key | VARCHAR(64) | 环节标识 | dwd_org_industry_chain_pat_dtl.segment_key | ✅ |
| patent_type | VARCHAR(32) | 专利类型（发明/实用新型/外观） | dwd_org_industry_chain_pat_dtl.patent_type | ✅ |
| calc_batch_id | VARCHAR(64) | 计算批次 | 系统 | ✅ |

### 2.5 dwd.industry_chain_news — 产业链动态资讯

| 字段 | 类型 | 注释 | 来源 ODS | 映射状态 |
|------|------|------|---------|---------|
| id | BIGINT PK AUTO_INCREMENT | 自增主键 | — | ✅ |
| chain_id | VARCHAR(64) | 产业链 ID | dwd_industry_chain_news_info | ✅ |
| title | VARCHAR(512) | 资讯标题 | dwd_industry_chain_news_info.title | ✅ |
| publish_date | DATE | 发布日期 | dwd_industry_chain_news_info.publish_date | ✅ |
| source | VARCHAR(128) | 来源 | dwd_industry_chain_news_info.source | ✅ |
| heat_score | DECIMAL(5,2) | 热度得分 | dwd_industry_chain_news_info.heat_score | ✅ |
| is_hot | TINYINT(1) | 是否热点 | 🔧 阈值判定 | 🔧 |
| news_type | VARCHAR(32) | 类型（融资/并购/新品/政策） | 🔧 NLP 分类 | 🔧 |
| calc_batch_id | VARCHAR(64) | 计算批次 | 系统 | ✅ |

### 2.6 dwd.industry_cycle — 产业周期判定

| 字段 | 类型 | 注释 | 来源 | 映射状态 |
|------|------|------|------|---------|
| chain_id | VARCHAR(64) PK | 产业链 ID | — | ✅ |
| cycle_stage | ENUM('intro','growth','mature','decline') | 周期阶段 | 🔧 M6 产出 | 🔧 |
| stage_score | DECIMAL(5,2) | 阶段评分 | 🔧 M6 产出 | 🔧 |
| confidence | DECIMAL(3,2) | 置信度 | 🔧 M6 产出 | 🔧 |
| reference_date | DATE | 判定参考日期 | — | ✅ |
| calc_batch_id | VARCHAR(64) | 计算批次 | 系统 | ✅ |

### 2.7 dwd.industry_bottleneck — 产业瓶颈识别

| 字段 | 类型 | 注释 | 来源 | 映射状态 |
|------|------|------|------|---------|
| id | BIGINT PK AUTO_INCREMENT | 自增主键 | — | ✅ |
| chain_id | VARCHAR(64) | 产业链 ID | — | ✅ |
| bottleneck_type | ENUM('tech','talent','market','capital','policy') | 瓶颈类型 | 🔧 M9 产出 | 🔧 |
| severity | ENUM('high','medium','low') | 严重程度 | 🔧 M9 产出 | 🔧 |
| description | TEXT | 瓶颈描述 | 🔧 M9 产出 | 🔧 |
| solution_hint | TEXT | 解决方案建议 | 🔧 M9 产出 | 🔧 |
| calc_batch_id | VARCHAR(64) | 计算批次 | 系统 | ✅ |

### 2.8 dwd.industry_region_index — 区域产业指数

| 字段 | 类型 | 注释 | 来源 | 映射状态 |
|------|------|------|------|---------|
| id | BIGINT PK AUTO_INCREMENT | 自增主键 | — | ✅ |
| chain_id | VARCHAR(64) | 产业链 ID | — | ✅ |
| region_code | VARCHAR(20) | 区域代码 | dim_region | ✅ |
| enterprise_power_score | DECIMAL(5,2) | 企业能力竞争力得分 | 🔧 M10 产出 | 🔧 |
| academic_power_score | DECIMAL(5,2) | 学术生态竞争力得分 | 🔧 M10 产出 | 🔧 |
| support_power_score | DECIMAL(5,2) | 配套生态竞争力得分 | 🔧 M10 产出 | 🔧 |
| composite_index | DECIMAL(5,2) | 综合指数 | 🔧 M10 产出 | 🔧 |
| calc_batch_id | VARCHAR(64) | 计算批次 | 系统 | ✅ |

---

## 3. ADS 契约表（Java 只读）

### 3.1 ads_chain_overview — 产业链概览

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) PK | 产业链 ID | — |
| chain_name | VARCHAR(128) | 产业链名称 | — |
| enterprise_count | INT | 关联企业数 | M_CHAIN_ENTERPRISE_COUNT |
| institution_count | INT | 关联机构数 | M_CHAIN_INSTITUTION_COUNT |
| total_revenue | DECIMAL(15,2) | 市场规模（亿元） | M_CHAIN_MARKET_SIZE |
| growth_rate | DECIMAL(5,2) | 增长率% | M_CHAIN_MARKET_GROWTH |
| invest_total | DECIMAL(15,2) | 投融资总额（亿元） | M_CHAIN_INVEST_TOTAL |
| node_count | INT | 产业链环节总数 | M_CHAIN_NODE_COUNT |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.2 ads_chain_panorama — 全景图谱

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) PK | 产业链 ID | — |
| graph_nodes | JSON | 图谱节点列表 | — |
| graph_edges | JSON | 图谱边列表 | — |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.3 ads_chain_cycle — 周期阶段

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) PK | 产业链 ID | — |
| cycle_stage | VARCHAR(16) | 周期阶段 | M_CHAIN_CYCLE_STAGE |
| stage_score | DECIMAL(5,2) | 阶段评分 | M_CHAIN_STAGE_SCORE |
| phase_determination | VARCHAR(32) | 阶段判定 | M_CHAIN_PHASE_DETERMINATION |
| confidence | DECIMAL(3,2) | 置信度 | — |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.4 ads_chain_region_index — 区域指数

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) | 产业链 ID | — |
| region_code | VARCHAR(20) | 区域代码 | — |
| region_name | VARCHAR(64) | 区域名称 | — |
| composite_index | DECIMAL(5,2) | 综合指数 | M_CHAIN_REGION_INDEX |
| enterprise_power | DECIMAL(5,2) | 企业能力 | M_CHAIN_ENTERPRISE_POWER |
| academic_power | DECIMAL(5,2) | 学术生态 | M_CHAIN_ACADEMIC_POWER |
| support_power | DECIMAL(5,2) | 配套生态 | M_CHAIN_SUPPORT_POWER |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.5 ads_chain_key_node — 关键环节

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) | 产业链 ID | — |
| node_name | VARCHAR(128) | 环节名称 | — |
| is_key_node | TINYINT(1) | 是否关键环节 | — |
| high_value_index | DECIMAL(5,2) | 高端化指数 | M_CHAIN_HIGH_VALUE_RATIO |
| strategic_importance | DECIMAL(5,2) | 战略重要性 | M_CHAIN_STRATEGIC_IMPORTANCE |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.6 ads_chain_bottleneck — 瓶颈堵点

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) | 产业链 ID | — |
| bottleneck_type | VARCHAR(16) | 瓶颈类型 | — |
| severity | VARCHAR(8) | 严重程度 | M_CHAIN_BOTTLENECK_SEVERITY |
| description | TEXT | 描述 | — |
| solution_hint | TEXT | 建议方案 | — |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.7 ads_chain_shenzhen — 深圳产业

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) PK | 产业链 ID | — |
| sz_enterprise_count | INT | 深圳企业数 | M_CHAIN_SZ_ENTERPRISE_COUNT |
| chain_completeness | DECIMAL(5,2) | 产业链完整度 | M_CHAIN_SZ_COMPLETENESS |
| sz_position | VARCHAR(32) | 深圳链中定位 | M_CHAIN_SZ_POSITION |
| advantage_score | DECIMAL(5,2) | 优势评分 | M_CHAIN_SZ_ADVANTAGE_SCORE |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.8 ads_chain_market — 市场规模

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) | 产业链 ID | — |
| stat_year | INT | 统计年份 | — |
| total_revenue | DECIMAL(15,2) | 总收入（亿元） | M_CHAIN_MARKET_SIZE |
| growth_rate | DECIMAL(5,2) | 增长率% | M_CHAIN_MARKET_GROWTH |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.9 ads_chain_investment — 投融资

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) | 产业链 ID | — |
| stat_year | INT | 统计年份 | — |
| invest_total | DECIMAL(15,2) | 投融资总额 | M_CHAIN_INVEST_TOTAL |
| invest_count | INT | 投融资事件数 | M_CHAIN_INVEST_COUNT |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.10 ads_chain_news_stat — 动态资讯统计

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) | 产业链 ID | — |
| stat_month | VARCHAR(7) | 统计月份 | — |
| news_count | INT | 资讯数量 | M_CHAIN_NEWS_COUNT |
| hot_news_count | INT | 热点资讯数 | M_CHAIN_HOT_NEWS_COUNT |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

### 3.11 ads_chain_competitiveness — 区域竞争力

| 字段 | 类型 | 注释 | metric_ids |
|------|------|------|-----------|
| chain_id | VARCHAR(64) | 产业链 ID | — |
| region_code | VARCHAR(20) | 区域代码 | — |
| competitiveness_index | DECIMAL(5,2) | 竞争力指数 | M_CHAIN_COMPETITIVENESS_INDEX |
| rank_nationwide | INT | 全国排名 | M_CHAIN_COMPETITIVENESS_RANK |
| calc_batch_id | VARCHAR(64) | 计算批次 | — |

---

## 4. NebulaGraph Schema

Space: `gkx_chain`

### Tags

| Tag | 属性 | 说明 |
|-----|------|------|
| chain | chain_id, chain_name, node_stage, is_key_node, high_value_index | 产业链/环节节点 |
| enterprise | enterprise_code, enterprise_name, chain_role | 企业节点（引用 gkx_enterprise） |
| institution | org_uid, org_name | 机构节点（引用 dim_org_master） |
| region | region_code, region_name | 区域节点 |

### Edges

| Edge | src → dst | 属性 | 说明 |
|------|----------|------|------|
| belongs_to | segment → chain | node_level | 环节→产业链归属 |
| participates | enterprise → chain | chain_role, participation_depth, chain_score | 企业→产业链参与 |
| supplies | enterprise → enterprise | relation_type, relation_strength | 供应链关系 |
| depends_on | segment → segment | relation_type(upstream/downstream) | 上下游依赖 |
| located_in | enterprise → region | — | 企业→区域归属 |
| serves | institution → chain | service_type | 机构→产业链服务 |

---

## 5. 主键与业务键策略

| 表 | 业务键 | NebulaGraph vid |
|----|--------|----------------|
| industry_chain | `chain_id`（`chain:{seq}`） | `chain:{chain_id}` |
| industry_chain_enterprise | `(chain_id, enterprise_code)` | — |
| industry_cycle | `chain_id` | — |
| industry_bottleneck | `(chain_id, bottleneck_type)` UQ | — |
| industry_region_index | `(chain_id, region_code)` UQ | — |

---

## 6. DQ 规则

| 编号 | 类型 | 对象 | 规则 | 级别 |
|------|------|------|------|------|
| DQ-C01 | 非空 | industry_chain.chain_id | NOT NULL | 🔴 阻断 |
| DQ-C02 | 非空 | industry_chain.chain_name | NOT NULL | 🔴 阻断 |
| DQ-C03 | 枚举 | industry_chain.node_stage | IN ('upstream','midstream','downstream') | 🔴 阻断 |
| DQ-C04 | 值域 | industry_cycle.stage_score | [0, 100] | 🟡 告警 |
| DQ-C05 | 值域 | industry_region_index.composite_index | [0, 100] | 🟡 告警 |
| DQ-C06 | 枚举 | industry_bottleneck.bottleneck_type | IN ('tech','talent','market','capital','policy') | 🔴 阻断 |
| DQ-C07 | 完整性 | cfg_metric 8 件套 | metric 上线前 8 字段非空（D9） | 🔴 阻断 |
| DQ-C08 | 图谱对齐 | graph_node.node_key | 与 Nebula vid 一致（chain: 前缀） | 🟡 告警 |
| DQ-C09 | 批次幂等 | Mock 生成器 | 同 calc_batch_id 可 DELETE+INSERT 重跑 | 🟢 监控 |

---

## 7. 字段映射覆盖率

| 状态 | 字段数 | 占比 |
|------|--------|------|
| ✅ 可直查 | 52 | 65.0% |
| 🔧 待算法 | 24 | 30.0% |
| ⚠️ 待确认 | 2 | 2.5% |
| ❌ 无来源 | 2 | 2.5% |
| **合计** | **80** | **100%** |

> ❌ 无来源字段：市场份额（无市调数据源）、品牌声量（无舆情数据源）
> ⚠️ 待确认：participation_depth 算法口径（Q013）、cycle_stage 阈值（待登记决策项）

---

## 8. 与企业域的关系

产业链 DWD 与企业域 DWD 共享以下外键：
- `industry_chain_enterprise.enterprise_code` → `dwd.enterprise.enterprise_code`
- `industry_region_index.region_code` → `dim_region.region_code`
- NebulaGraph 跨 space 查询：`gkx_chain` ↔ `gkx_enterprise`（通过 enterprise_code 关联）

---

## 9. 变更记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-23 | 初版：8 DWD + 11 ADS + NebulaGraph 4T6E；字段映射覆盖率 65%✅ / 30%🔧 / 2.5%⚠️ / 2.5%❌ |
