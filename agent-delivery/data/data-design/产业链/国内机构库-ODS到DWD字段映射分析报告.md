# 国内机构库 ODS→DWD/ADS 字段映射分析报告

> **现行存储入口（S4）**：[`../storage/CHAIN/README.md`](../storage/CHAIN/README.md)  
> 本稿为 **国内机构库专项映射分析**（CHAIN-INST 附属）；产业链存储导航仍走 `storage/CHAIN`。冲突以 `storage/CHAIN` 为准。

> 生成时间: 2026-07-29 ｜ 数据源: `gkxlumenx_ods`（`111.198.38.90:34306`）
> 任务: CHAIN-INST-DATA-ANALYSIS-L01（DoD-2: 国内机构库数据源分析）
> 作者: [human:李伟] + [agent:architect]

---

## 1. ODS 源表概况

### 1.1 机构相关 ODS 表全览

| # | ODS 表 | 中文名 | 行数 | 状态 |
|---|--------|--------|------|------|
| 1 | `dwd_org_innovation_carrier` | 创新载体（实验室/工程中心/孵化器等） | **1,404** | ✅ 有数据 |
| 2 | `dwd_forg_shareholder` | 外资企业股东信息 | **21,006** | ✅ 有数据 |
| 3 | `dwd_org_reg_info` | 机构注册信息 | **0** | ❌ 空表 |
| 4 | `dwd_org_sc_info` | 科技机构信息 | **0** | ❌ 空表 |
| 5 | `dwd_org_hels_info` | 高校科研院所信息 | **0** | ❌ 空表 |
| 6 | `dwd_org_executive_info` | 机构高管信息 | **0** | ❌ 空表 |
| 7 | `dwd_org_shareholder_info` | 机构股东信息 | **0** | ❌ 空表 |
| 8 | `dwd_org_stock_base` | 机构上市基础信息 | **0** | ❌ 空表 |
| 9 | `dwd_org_stock_finance_info` | 机构上市财务信息 | **0** | ❌ 空表 |
| 10 | `dwd_forg_executive_info` | 外资企业高管信息 | **0** | ❌ 空表 |
| 11 | `dwd_forg_shareholder_info` | 外资企业股东详情 | **0** | ❌ 空表 |
| 12 | `dwd_forg_stock_fin_info` | 外资企业上市财务 | **0** | ❌ 空表 |
| 13 | `dwd_hycy_marine_energy_industry_carrier` | 海洋能源产业载体 | **0** | ❌ 空表 |

**结论**：13 张机构相关表中，仅 **2 张有数据**（`dwd_org_innovation_carrier` 1,404 行 + `dwd_forg_shareholder` 21,006 行），其余 11 张均为空表。

---

### 1.2 有数据表详解

#### ① `dwd_org_innovation_carrier` — 创新载体（1,404 行）

```sql
CREATE TABLE `dwd_org_innovation_carrier` (
  `carrier_type` varchar(50) DEFAULT NULL,       -- 载体类型（实验室/工程中心/孵化器等）
  `carrier_name` varchar(200) DEFAULT NULL,      -- 载体名称
  `carrier_level` varchar(50) DEFAULT NULL,      -- 载体级别（国家级/省级等）
  `create_year` int DEFAULT NULL,                -- 成立年份
  `area` varchar(50) DEFAULT NULL,               -- 所在地区（省份）
  `area_code` varchar(50) DEFAULT NULL,          -- 地区代码
  `org_id` varchar(50) DEFAULT NULL,             -- 机构ID
  `org_name` varchar(200) DEFAULT NULL,          -- 依托单位名称
  `social_credit_code` varchar(50) DEFAULT NULL, -- 统一社会信用代码
  `announcement` varchar(500) DEFAULT NULL,      -- 公告名称
  `publish_org` varchar(50) DEFAULT NULL,        -- 发布机构
  `publish_date` varchar(50) DEFAULT NULL,       -- 发布日期
  `source_url` varchar(500) DEFAULT NULL         -- 来源链接
);
```

**载体类型分布（31 种，前 10）**：

| carrier_type | 数量 |
|--------------|------|
| 工程研究中心 | 150 |
| 工程技术研究中心 | 150 |
| 工程实验室 | 136 |
| 重点实验室 | 118 |
| 企业技术中心 | 100 |
| 科技企业孵化器 | 64 |
| 公共技术服务平台 | 50 |
| 产业技术研究院 | 50 |
| 工业设计中心 | 50 |
| 技术创新中心 | 50 |
| ...其余 21 种 | 286 |

**样本数据**：

| carrier_type | carrier_name | carrier_level | create_year | area | org_name | social_credit_code |
|--------------|-------------|---------------|-------------|------|----------|-------------------|
| 重点实验室 | 省部共建公共大数据国家重点实验室 | 国家级 | 2021 | 贵州省 | 贵州大学 | 12520000429203011T |
| 重点实验室 | 中低品位磷矿国家重点实验室 | 国家级 | 2015 | 贵州省 | 瓮福(集团)有限责任公司 | 91520000214419966X |
| 企业技术中心 | 北京博睿宏远数据科技股份有限公司技术中心 | 国家级 | 2025 | 北京市 | 北京博睿宏远数据科技股份有限公司 | 91110105672840619D |
| 企业技术中心 | 天津药明康德新药开发有限公司技术中心 | 国家级 | 2025 | 天津市 | 天津药明康德新药开发有限公司 | 91120116789350111X |

#### ② `dwd_forg_shareholder` — 外资企业股东（21,006 行）

```sql
CREATE TABLE `dwd_forg_shareholder` (
  `ename_en` varchar(500) DEFAULT NULL,    -- 企业英文名称
  `sh_name` varchar(255) DEFAULT NULL,     -- 股东名称
  `sh_entity_type` varchar(255) DEFAULT NULL, -- 股东实体类型
  `sh_country_code` varchar(255) DEFAULT NULL, -- 股东国家代码
  `sh_direct_pct` varchar(50) DEFAULT NULL,   -- 直接持股比例(%)
  `sh_total_pct` varchar(50) DEFAULT NULL     -- 总持股比例(%)
);
```

> ⚠️ 此表无 `credit_code` / `org_id` 关联键，且字段语义偏向"企业股东"而非"机构主体"，**与产业链机构库关系不大**。

---

## 2. DWD/ADS 目标表

### 2.1 机构相关目标表清单

| # | 库 | 表名 | 当前行数 | 用途 |
|---|-----|------|---------|------|
| 1 | `gkxlumenx_ads` | `chain_institution_stat` | 40 (mock) | 产业链机构数量统计 |
| 2 | `gkxlumenx_ads` | `realdata_research_org_stat` | 0 | 科研机构能力统计 |
| 3 | `gkxlumenx_dwd` | `org_achievement_year` | 1,312 (mock) | 机构年度成果统计 |

### 2.2 目标表结构

#### `chain_institution_stat` — 产业链机构统计（ADS）

```sql
CREATE TABLE `chain_institution_stat` (
  `chain_id` varchar(16) NOT NULL,               -- 产业链编码
  `chain_name` varchar(64) DEFAULT NULL,         -- 产业链名称
  `stat_year` int NOT NULL,                      -- 统计年份
  `institution_count` int DEFAULT NULL,           -- 机构数量
  `growth_rate` decimal(8,2) DEFAULT NULL,        -- 增长率
  PRIMARY KEY (`chain_id`, `stat_year`)
);
```

#### `realdata_research_org_stat` — 科研机构能力统计（ADS）

```sql
CREATE TABLE `realdata_research_org_stat` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_id` varchar(64) DEFAULT NULL,             -- 机构ID
  `org_name` varchar(200) DEFAULT NULL,          -- 机构名称
  `org_type` varchar(50) DEFAULT NULL,           -- 机构类型
  `province` varchar(50) DEFAULT NULL,           -- 省份
  `city` varchar(50) DEFAULT NULL,               -- 城市
  `scholar_count` int DEFAULT NULL,              -- 学者数量
  `academician_count` int DEFAULT NULL,           -- 院士数量
  `research_fields` int DEFAULT NULL,             -- 研究领域数
  `capability_score` decimal(6,2) DEFAULT NULL,   -- 能力评分
  `model_version` varchar(40) DEFAULT NULL,       -- 模型版本
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);
```

#### `org_achievement_year` — 机构年度成果（DWD）

```sql
CREATE TABLE `org_achievement_year` (
  `org_uid` varchar(64) NOT NULL,                -- 机构UID
  `stat_year` smallint NOT NULL,                 -- 统计年份
  `domain_id` varchar(64) NOT NULL,              -- 领域ID
  `paper_cnt` int DEFAULT NULL,                  -- 论文数
  `paper_sci_cnt` int DEFAULT NULL,              -- SCI论文数
  `patent_apply_cnt` int DEFAULT NULL,           -- 专利申请数
  `patent_grant_inv_cnt` int DEFAULT NULL,       -- 发明专利授权数
  `patent_pct_cnt` int DEFAULT NULL,             -- PCT专利数
  `project_cnt` int DEFAULT NULL,                -- 项目数
  `project_amount` decimal(20,2) DEFAULT NULL,    -- 项目金额
  `financing_cnt` int DEFAULT NULL,              -- 融资次数
  `financing_amount` decimal(20,2) DEFAULT NULL,  -- 融资金额
  `event_cnt` int DEFAULT NULL,                  -- 事件数
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`org_uid`, `stat_year`, `domain_id`)
);
```

---

## 3. 字段映射分析

### 3.1 `chain_institution_stat` — 产业链机构统计

| # | DWD 字段 | 中文含义 | 类型 | 状态 | 来源 ODS | 映射方式 |
|---|---------|---------|------|------|---------|----------|
| 1 | `chain_id` | 产业链编码 | varchar(16) | ⚠️ | — | 需定编码方案（与产业链同问题） |
| 2 | `chain_name` | 产业链名称 | varchar(64) | ❌ | — | ❌ ODS 无产业链关联字段 |
| 3 | `stat_year` | 统计年份 | int | 🔧 | `dwd_org_innovation_carrier.create_year` | 取载体成立年份统计 |
| 4 | `institution_count` | 机构数量 | int | 🔧 | `dwd_org_innovation_carrier.org_id` | COUNT DISTINCT GROUP BY year |
| 5 | `growth_rate` | 增长率 | decimal(8,2) | 🔧 | — | 算法计算（当年/上年-1） |

**覆盖率**: 2/5 = 40%（排除编码阻塞）

### 3.2 `realdata_research_org_stat` — 科研机构能力统计

| # | DWD 字段 | 中文含义 | 类型 | 状态 | 来源 ODS | 映射方式 |
|---|---------|---------|------|------|---------|----------|
| 1 | `org_id` | 机构ID | varchar(64) | ✅ | `dwd_org_innovation_carrier.org_id` | 直接映射 |
| 2 | `org_name` | 机构名称 | varchar(200) | ✅ | `dwd_org_innovation_carrier.org_name` | 直接映射 |
| 3 | `org_type` | 机构类型 | varchar(50) | 🔧 | `dwd_org_innovation_carrier.carrier_type` | 类型映射（实验室/工程中心等） |
| 4 | `province` | 省份 | varchar(50) | ✅ | `dwd_org_innovation_carrier.area` | 直接映射 |
| 5 | `city` | 城市 | varchar(50) | ❌ | — | ODS 仅有省份（area），无城市字段 |
| 6 | `scholar_count` | 学者数量 | int | ❌ | — | 无来源（`dwd_org_hels_info` 空表） |
| 7 | `academician_count` | 院士数量 | int | ❌ | — | 无来源 |
| 8 | `research_fields` | 研究领域数 | int | ❌ | — | 无来源 |
| 9 | `capability_score` | 能力评分 | decimal(6,2) | 🔧 | — | 需算法计算 |
| 10 | `model_version` | 模型版本 | varchar(40) | 🟦 | — | 系统 |
| 11 | `updated_at` | 更新时间 | datetime | 🟦 | — | 系统 |

**覆盖率**: 3/9 = 33%（排除系统列）

### 3.3 `org_achievement_year` — 机构年度成果

| # | DWD 字段 | 中文含义 | 类型 | 状态 | 来源 ODS | 映射方式 |
|---|---------|---------|------|------|---------|----------|
| 1 | `org_uid` | 机构UID | varchar(64) | ✅ | `dwd_org_innovation_carrier.org_id` | 直接映射 |
| 2 | `stat_year` | 统计年份 | smallint | 🔧 | `dwd_org_innovation_carrier.create_year` | 取成立年份 |
| 3 | `domain_id` | 领域ID | varchar(64) | ❌ | — | ODS 无领域/学科分类字段 |
| 4 | `paper_cnt` | 论文数 | int | ❌ | — | 无来源 |
| 5 | `paper_sci_cnt` | SCI论文数 | int | ❌ | — | 无来源 |
| 6 | `patent_apply_cnt` | 专利申请数 | int | 🔧 | `dwd_org_industry_chain_pat_dtl` | 可关联专利表 COUNT（但仅 888 行且非机构维度） |
| 7 | `patent_grant_inv_cnt` | 发明专利授权数 | int | ❌ | — | 无来源 |
| 8 | `patent_pct_cnt` | PCT专利数 | int | ❌ | — | 无来源 |
| 9 | `project_cnt` | 项目数 | int | ❌ | — | 无来源 |
| 10 | `project_amount` | 项目金额 | decimal(20,2) | ❌ | — | 无来源 |
| 11 | `financing_cnt` | 融资次数 | int | ❌ | — | 无来源（投融资表空） |
| 12 | `financing_amount` | 融资金额 | decimal(20,2) | ❌ | — | 无来源 |
| 13 | `event_cnt` | 事件数 | int | ❌ | — | 无来源 |
| 14 | `updated_time` | 更新时间 | datetime | 🟦 | — | 系统 |

**覆盖率**: 1/12 = 8%（排除系统列）— **极低**

---

## 4. NebulaGraph 机构节点

根据 `产业链域数据库设计(v1).md` §8，NebulaGraph `gkx_industry` Space 中有机构相关 Tag/Edge：

### 4.1 institution Tag

```ngql
CREATE TAG IF NOT EXISTS institution (
  org_uid string,      -- 机构UID
  org_name string,     -- 机构名称
  props string
);
```

### 4.2 serves Edge（机构→产业链）

```ngql
CREATE EDGE IF NOT EXISTS serves (
  service_type string,  -- 服务类型
  props string
);
```

**灌数可行性**：

| Nebula 对象 | 来源 ODS | 状态 |
|-------------|---------|------|
| institution Tag | `dwd_org_innovation_carrier.org_id` + `org_name` | ✅ 可灌（1,404 个机构节点） |
| serves Edge | ❌ 无来源 | ODS 无机构→产业链关联字段 |

---

## 5. 数据缺口与风险

| 类型 | 编号 | 项 | 影响 | 严重度 | 建议 |
|------|------|-----|------|--------|------|
| ❌ | INST-01 | **机构主体表全空**：`dwd_org_reg_info` / `dwd_org_sc_info` / `dwd_org_hels_info` 均为 0 行 | `realdata_research_org_stat` 多数字段无源 | 🔴 | 向供应方索要数据 |
| ❌ | INST-02 | **机构→产业链关联缺失**：`dwd_org_innovation_carrier` 无 `industry_code` 字段 | `chain_institution_stat` 无法按链统计、Nebula `serves` Edge 无法灌 | 🔴 | 需建立机构-产业链映射（可人工标注或 NLP 推导） |
| ❌ | INST-03 | **机构成果数据缺失**：论文/项目/融资/事件等字段无来源 | `org_achievement_year` 12 个字段中 11 个无源 | 🔴 | 需对接学术论文库/项目库/投融资库 |
| ❌ | INST-04 | **城市维度缺失**：`dwd_org_innovation_carrier` 仅有 `area`（省份），无城市 | `realdata_research_org_stat.city` 无源 | 🟡 | 可 JOIN `dwd_org_base_info` 补充（若有 social_credit_code） |
| ⚠️ | INST-05 | 编码阻塞 | `chain_institution_stat.chain_id` | 🟡 | 与产业链同问题，需定编码方案 |
| 🔧 | INST-06 | `dwd_forg_shareholder` 数据量大但无关联键 | 无法与机构/产业链关联 | 🟢 | 暂不使用 |

---

## 6. 灌数可行性评估

### 6.1 可灌数的表

| 目标表 | 可灌字段 | 数据来源 | 灌数方式 |
|--------|---------|---------|----------|
| `realdata_research_org_stat` | org_id / org_name / org_type / province（4/9） | `dwd_org_innovation_carrier` | 直接映射 + 类型转换 |
| Nebula `institution` Tag | org_uid / org_name | `dwd_org_innovation_carrier` | Python 灌数 |

### 6.2 不可灌数的表

| 目标表 | 原因 |
|--------|------|
| `chain_institution_stat` | ❌ 机构→产业链关联缺失（INST-02）+ 编码阻塞（INST-05） |
| `org_achievement_year` | ❌ 成果数据几乎全缺（INST-03），仅 org_uid 可映射 |
| Nebula `serves` Edge | ❌ 机构→产业链关联缺失（INST-02） |

---

## 7. 综合结论

1. **机构库 ODS 数据极度匮乏**：13 张相关表中仅 1 张（`dwd_org_innovation_carrier`，1,404 行）有实质数据，且该表是"创新载体"而非"机构主体"。

2. **核心缺口是机构→产业链关联**：`dwd_org_innovation_carrier` 没有 `industry_code` 字段，无法将机构关联到具体产业链，导致 `chain_institution_stat` 和 Nebula `serves` Edge 均无法灌数。

3. **机构成果数据完全缺失**：论文、项目、融资、专利等指标字段无任何 ODS 来源，`org_achievement_year` 的 12 个业务字段中 11 个无源。

4. **可灌范围有限**：仅 `realdata_research_org_stat` 的 4 个基础字段（org_id/org_name/org_type/province）和 Nebula `institution` Tag 可从 `dwd_org_innovation_carrier` 灌入。

5. **建议升级决策**：
   - 🟡 向数据供应方索要 `dwd_org_reg_info` / `dwd_org_hels_info` / `dwd_org_sc_info` 的数据
   - 🟡 建立机构→产业链映射（人工标注或 NLP 从 `carrier_name` / `org_name` 推导）
   - 🟡 对接学术论文库/项目库补充机构成果数据

---

## 8. 与产业链报告的关系

本报告是 `产业链-ODS到DWD字段映射分析报告(v3).md` 的补充，覆盖任务 DoD-2（国内机构库数据源分析）。两份报告共同构成 CHAIN-INST-DATA-ANALYSIS-L01 的数据源分析产出。

| 域 | 主报告 | 核心发现 |
|----|--------|---------|
| 产业链 | 产业链-ODS到DWD字段映射分析报告(v3).md | 4 张 ODS 表有数据，覆盖率 48%，编码阻塞 |
| 机构库 | 本报告 | 1 张 ODS 表有数据，覆盖率极低，机构→产业链关联缺失 |

---

*报告生成时间: 2026-07-29 ｜ 作者: [human:李伟] + [agent:architect] ｜ 任务: CHAIN-INST-DATA-ANALYSIS-L01*
