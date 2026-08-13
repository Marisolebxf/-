# 产业链相关 ODS → DWD 字段映射分析报告（v3）

> **现行存储入口（S4）**：[`../storage/CHAIN/README.md`](../storage/CHAIN/README.md) · sources [`../storage/CHAIN/sources/inventory.md`](../storage/CHAIN/sources/inventory.md)  
> 本稿为 **映射分析过程稿**（v3）；ODS 建表真源 = `doc/`/`md-extract`（见 S2），项目 DWD = v5。冲突以 `storage/CHAIN` 为准。

> 生成时间: 2026-07-24 ｜ 版本: v3（ODS 数据库: `gkxlumenx_ods`@`111.198.38.90:34306`）
> 分析范围: **产业链（CHAIN）** 数据域
> 任务: CHAIN-INST-DATA-ANALYSIS-L01
> 前版: v2（2026-06-23，基于要素库 5 表 + 宏观补充）

---

## 背景与版本变更

**v2 → v3 的核心变化**：

| 项 | v2（旧 ODS） | v3（新 ODS `gkxlumenx_ods`） |
|----|-------------|---------------------------|
| 核心源表 | `dwd_org_industry_chain_dtl`（企业-链映射，**已缺失**） | `dwd_org_industry_tags`（企业-产业链标签，**4,912 行**） |
| 产品源表 | `dwd_org_industry_chain_prod_dtl`（**已缺失**） | `dwd_org_industry_product_tags`（企业-产业链-产品标签，**5,000 行**） |
| 图谱源表 | `dwd_industry_chain_info`（含 node_id/node_type/node_stage 等节点属性） | `dwd_industry_chain_info`（**字段结构大幅简化**，仅有 hierarchy tree 字段） |
| 编码体系 | 旧版预期有 `chain_code`（独立字段） | 实际是 JSON 数组 `industry_code` / `industry_link_code`（可为多值） |
| 投融资源 | 预期 `dwd_org_financing_info` / `dwd_org_invest_info` 有数据 | **实际均为空表（0 行）** |
| 创新载体 | 无 | `dwd_org_innovation_carrier`（**1,449 行**） |
| 企业主数据 | 预期 `dwd_company_base` | `dwd_org_base_info`（**10,996 行**） |
| DWD 物理库 | 设计 `gkx_dwd.industry_chain*`（8 表） | 实际 `gkxlumenx_dwd.chain*`（**7 表**，命名简化，当前仅 mock） |

**映射状态图例**：
- ✅**直接映射**：ODS 有对应字段，可直接取值或简单类型/枚举转换
- 🔧**需计算/算法**：有数据源但需聚合、去重、推导或算法模型
- ⚠️**待确认/质量待验**：需业务确认或口径待甲方定稿
- ❌**无来源**：ODS 中无相关数据
- 🟦**系统/预留**：主键、时间戳、扩展位等由 ETL 填充

---

## 1. ODS 源表概况（`gkxlumenx_ods`，有数据的产业链相关表）

### 1.1 核心四表（均有数据）

| # | ODS 表 | 行数 | 字段数 | 核心用途 |
|---|--------|------|--------|----------|
| 1 | `dwd_industry_chain_info` | **527** | 13 | 产业链体系树（0–6 层级），INB 编码 |
| 2 | `dwd_org_industry_tags` | **4,912** | 14 | 企业→产业链标签映射（JSON 数组存多产业归属） |
| 3 | `dwd_org_industry_product_tags` | **5,000** | 15 | 企业→产业链→产品标签（比 ② 多 `product_name`） |
| 4 | `dwd_industry_chain_news_info` | **5,000** | 14 | 产业链动态资讯 |

### 1.2 辅助表（可补充 DWD 字段）

| # | ODS 表 | 行数 | 用途 |
|---|--------|------|------|
| 5 | `dwd_org_base_info` | **10,996** | 企业工商信息（city/district/reg_year 等） |
| 6 | `dwd_org_industry_chain_pat_dtl` | **888** | 产业链关联专利 |
| 7 | `dwd_org_innovation_carrier` | **1,449** | 创新载体（高企/实验室/工程中心） |
| 8 | `dwd_org_invest_info` | **0**（空） | ❌ 无数据 |
| 9 | `dwd_org_financing_info` | **0**（空） | ❌ 无数据 |

### 1.3 核心表字段详情

#### ① `dwd_industry_chain_info` — 产业链体系树（527 行）

```sql
CREATE TABLE `dwd_industry_chain_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT,
  `industry_code` varchar(255) NOT NULL,       -- 产业代码（如 INB1204）
  `industry_name` varchar(255) NOT NULL,       -- 产业名称
  `industry_link_code` varchar(255) NOT NULL,  -- 环节代码（如 INB120401010101）
  `industry_link_name` varchar(255) NOT NULL,  -- 环节名称
  `level` int NOT NULL,                        -- 层级 0–6
  `parent_code` varchar(255) DEFAULT NULL,     -- 父节点代码
  `is_deleted` smallint NOT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime DEFAULT NULL,
  `creater` varchar(100) DEFAULT NULL,
  `updater` varchar(100) DEFAULT NULL,
  `table_data_source` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
);
```

**层级分布**：

| level | 含义 | 行数 |
|-------|------|------|
| 0 | 产业大类根 | 4 |
| 1 | 一级分类 | 15 |
| 2 | 二级分类 | 48 |
| 3 | 三级分类 | 130 |
| 4 | 四级分类 | 210 |
| 5 | 五级分类 | 89 |
| 6 | 六级分类 | 31 |

**4 个产业大类**：

| industry_code | industry_name | 环节节点数 |
|---------------|---------------|-----------|
| INB1204 | 集成电路 | ~150+ |
| INB1303 | 人工智能 | ~120+ |
| INB1354 | 生物医药 | ~140+ |
| INB1309 | 新材料 | ~110+ |

**层级示例（INB1204）：**

```
INB1204 (0) 集成电路
├── INB120401 (1) 集成电路设计
│   ├── INB12040101 (2) 数字芯片设计
│   │   ├── INB1204010101 (3) CPU设计
│   │   │   ├── INB120401010101 (4) 高性能CPU
│   │   │   └── INB120401010102 (4) 嵌入式CPU
│   │   │       ├── INB12040101010201 (5) ARM架构
│   │   │       └── INB12040101010202 (5) RISC-V架构
│   │   └── INB120401010103 (4) GPU设计
```

#### ② `dwd_org_industry_tags` — 企业-产业标签（4,912 行）

```sql
CREATE TABLE `dwd_org_industry_tags` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT,
  `industry_code` varchar(255) NOT NULL,       -- JSON数组，如 ["INB1309","INB1354"]
  `industry_name` varchar(255) NOT NULL,       -- JSON数组，如 ["新材料","生物医药"]
  `industry_link_code` varchar(3000) NOT NULL, -- JSON数组，产业链环节代码列表
  `industry_link_name` varchar(2000) NOT NULL, -- JSON数组，环节名称列表
  `company_name` varchar(500) NOT NULL,        -- 企业名称
  `credit_code` varchar(255) NOT NULL,         -- 统一社会信用代码
  `is_deleted` smallint NOT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime DEFAULT NULL,
  `creater` varchar(100) DEFAULT NULL,
  `updater` varchar(100) DEFAULT NULL,
  `table_data_source` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
);
```

**关键特征**：
- 4,912 行 = 4,912 个企业（credit_code 去重后一致）
- 一条企业可关联多个产业（`industry_code` 是 JSON 数组）
- 每个产业下可关联多个环节（`industry_link_code` 是 JSON 数组）

**企业产业归属分布（前 10）**：

| industry_code | 企业数 |
|---------------|--------|
| ["INB1309"] | 3,291 |
| ["INB1303"] | 459 |
| ["INB1354"] | 188 |
| ["INB1204"] | 120 |
| ["INB1204","INB1354"] | 135 |
| ["INB1204","INB1354","INB1309"] | 84 |
| ["INB1204","INB1309"] | 64 |
| ["INB1303","INB1309"] | 102 |
| 其他多产业组合 | ~469 |

**跨产业企业占比**：约 14% 的企业（~700）属于 2+ 产业。

#### ③ `dwd_org_industry_product_tags` — 企业-产业-产品（5,000 行）

```sql
CREATE TABLE `dwd_org_industry_product_tags` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT,
  `industry_code` varchar(255) NOT NULL,       -- JSON数组
  `industry_name` varchar(255) NOT NULL,       -- JSON数组
  `industry_link_code` text NOT NULL,          -- JSON数组，产业链环节代码
  `industry_link_name` text NOT NULL,          -- JSON数组，环节名称
  `company_name` varchar(500) NOT NULL,        -- 企业名称
  `credit_code` varchar(255) DEFAULT NULL,     -- 统一社会信用代码
  `product_name` text NOT NULL,                -- JSON数组，产品名称列表
  `is_deleted` smallint NOT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime DEFAULT NULL,
  `creater` varchar(100) DEFAULT NULL,
  `updater` varchar(100) DEFAULT NULL,
  `table_data_source` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`pk_id`)
);
```

**与 ② 的差异**：多了 `product_name`（JSON 数组），缺失 `dwd_org_industry_tags` 不存在的 `credit_code` 非空约束（可为 NULL）。

#### ④ `dwd_industry_chain_news_info` — 产业动态资讯（5,000 行）

```sql
CREATE TABLE `dwd_industry_chain_news_info` (
  `pk_id` bigint NOT NULL AUTO_INCREMENT,
  `industry_code` varchar(255) NOT NULL,       -- 产业代码（非JSON，单值如 INB1354）
  `industry_name` varchar(255) NOT NULL,       -- 产业名称
  `id` varchar(255) NOT NULL,                  -- 资讯ID（UNIQUE）
  `title` varchar(255) NOT NULL,               -- 标题
  `publish_date` date NOT NULL,                -- 发布日期
  `abstract` text,                             -- 摘要
  `source` varchar(500) DEFAULT NULL,          -- 来源
  `is_deleted` smallint NOT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime DEFAULT NULL,
  `creater` varchar(100) DEFAULT NULL,
  `updater` varchar(100) DEFAULT NULL,
  `table_data_source` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`pk_id`),
  UNIQUE KEY `uk_dwd_industry_chain_news_info_id` (`id`)
);
```

---

## 2. DWD 目标表（`gkxlumenx_dwd`，当前仅 mock 数据）

| # | DWD 表 | 当前行数 | 说明 |
|---|--------|---------|------|
| 1 | `chain` | **8** | 产业链主表（mock：国标编码 C2711 等） |
| 2 | `chain_node` | **41** | 产业链环节/节点 |
| 3 | `chain_enterprise` | **120** | 产业链-企业关联 |
| 4 | `chain_news` | **200** | 产业动态资讯 |
| 5 | `chain_region_dist` | **288** | 区域分布统计 |
| 6 | `chain_investment` | **60** | 投融资明细 |
| 7 | `chain_enterprise_stat` | **209** | 企业参与统计 |

**物理表结构**：

```sql
-- chain
CREATE TABLE `chain` (
  `chain_id` varchar(16) NOT NULL,
  `chain_name` varchar(64) NOT NULL,
  `industry_code` varchar(16) DEFAULT NULL,   -- ⚠️ 当前为国标编码（C2711等），非INB编码
  `node_count` int DEFAULT NULL,
  `description` varchar(512) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`chain_id`)
);

-- chain_node
CREATE TABLE `chain_node` (
  `node_id` int NOT NULL,
  `chain_id` varchar(16) NOT NULL,
  `chain_name` varchar(64) DEFAULT NULL,
  `node_name` varchar(128) NOT NULL,
  `position` varchar(16) DEFAULT NULL,         -- 上游/中游/下游
  `seq_no` int DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`node_id`)
);

-- chain_enterprise
CREATE TABLE `chain_enterprise` (
  `enterprise_id` int NOT NULL,
  `enterprise_name` varchar(256) NOT NULL,
  `chain_id` varchar(16) NOT NULL,
  `chain_name` varchar(64) DEFAULT NULL,
  `city` varchar(64) DEFAULT NULL,
  `district` varchar(64) DEFAULT NULL,
  `reg_year` int DEFAULT NULL,
  `revenue` decimal(20,2) DEFAULT NULL,
  `rd_ratio` decimal(5,2) DEFAULT NULL,
  `patent_count` int DEFAULT NULL,
  `is_high_tech` smallint DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`enterprise_id`)
);

-- chain_news
CREATE TABLE `chain_news` (
  `news_id` int NOT NULL,
  `chain_id` varchar(16) NOT NULL,
  `chain_name` varchar(64) DEFAULT NULL,
  `enterprise_id` int DEFAULT NULL,
  `enterprise_name` varchar(256) DEFAULT NULL,
  `news_type` varchar(32) DEFAULT NULL,        -- 融资/并购/新品/政策
  `type_name` varchar(32) DEFAULT NULL,
  `title` varchar(1024) DEFAULT NULL,
  `summary` longtext,
  `views` int DEFAULT NULL,
  `is_hot` smallint DEFAULT NULL,
  `publish_time` datetime DEFAULT NULL,
  `data_year` int DEFAULT NULL,
  `data_month` varchar(10) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`news_id`)
);

-- chain_region_dist
CREATE TABLE `chain_region_dist` (
  `region_id` int NOT NULL,
  `chain_id` varchar(16) NOT NULL,
  `chain_name` varchar(64) DEFAULT NULL,
  `level` varchar(16) NOT NULL,                -- province/city/district
  `region_name` varchar(128) NOT NULL,
  `parent_region` varchar(128) DEFAULT NULL,
  `enterprise_count` int DEFAULT NULL,
  `institution_count` int DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`region_id`)
);

-- chain_investment
CREATE TABLE `chain_investment` (
  `investment_id` int NOT NULL,
  `chain_id` varchar(16) NOT NULL,
  `chain_name` varchar(64) DEFAULT NULL,
  `enterprise_id` int DEFAULT NULL,
  `enterprise_name` varchar(256) DEFAULT NULL,
  `round` varchar(32) DEFAULT NULL,
  `amount` decimal(20,2) DEFAULT NULL,
  `investor` varchar(256) DEFAULT NULL,
  `invest_date` datetime DEFAULT NULL,
  `data_year` int DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`investment_id`)
);

-- chain_enterprise_stat
CREATE TABLE `chain_enterprise_stat` (
  `enterprise_id` int NOT NULL,
  `chain_id` varchar(16) NOT NULL,
  `node_name` varchar(128) DEFAULT NULL,
  `role` varchar(32) DEFAULT NULL,
  `participation_depth` decimal(5,3) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL
);
```

---

## 3. 编码体系不兼容分析（关键问题）

**两套完全不兼容的编码体系：**

| 体系 | 库 | 来源 | 示例 |
|------|-----|------|------|
| **INB 编码** | `gkxlumenx_ods` | ODS 全部四表 | `INB1204`（集成电路）、`INB1309`（新材料） |
| **国标编码** | `gkxlumenx_dwd` | DWD `chain` mock 数据 | `C2711`（化学药品原料药制造）、`I6510`（软件开发） |

**影响范围**：

| DWD 表 | 关联键 | 编码体系 | 关系 |
|--------|--------|---------|------|
| `chain` | `chain_id` = 国标编码（C2711 等） | 国标 | **与 ODS 无法直接 JOIN** |
| `chain_node` | `chain_id` 外键 | 国标 | **同上** |
| `chain_enterprise` | `chain_id` 外键 | 国标 | **同上** |
| `chain_news` | `chain_id` 外键 | 国标 | **同上** |

**解决方案选项（🟡 需 PM/数据 Lead 确认）**：

| 方案 | 操作 | 影响面 |
|------|------|--------|
| A: DWD 改用 INB 编码 | `chain.chain_id` = INB1204/INB1303/INB1354/INB1309 | 重建全部 7 张 DWD 表数据 |
| B: 建立映射表 | 建 `dim_industry_code_map`（INB1204 → C2711, C2720...） | 需甲方确认映射准确性 |
| C: 双键并存 | DWD 同时保留 `chain_code`（INB）+ `gb_code`（国标） | 增加复杂度 |

---

## 4. 逐表字段映射详情

### 4.1 `chain` — 产业链主表

**ODS 来源**: `dwd_industry_chain_info`（level=0 去重聚合）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑 |
|---|---------|------|----------|---------|----------|
| 1 | chain_id | varchar(16) | ⚠️ | — | **需确认编码方案**（当前 mock 为国标，ODS 为 INB） |
| 2 | chain_name | varchar(64) | ✅ | `industry_name` WHERE level=0 | 4个产业大类名称 |
| 3 | industry_code | varchar(16) | ✅ | `industry_code` WHERE level=0 | INB1204/INB1303/INB1354/INB1309 |
| 4 | node_count | int | 🔧 | COUNT(industry_link_code) GROUP BY industry_code | 每个产业下的环节总数 |
| 5 | description | varchar(512) | ❌ | — | ODS 无 description 字段，需人工补录 |
| 6 | create_time | datetime | 🟦 | NOW() | 系统 |
| 7 | update_time | datetime | 🟦 | NOW() | 系统 |

**覆盖**: 5/7 = 71%（排除 🟦，含 ⚠️ 编码项）

### 4.2 `chain_node` — 产业链环节/节点

**ODS 来源**: `dwd_industry_chain_info`（全部 527 行，一行一节点）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑 |
|---|---------|------|----------|---------|----------|
| 1 | node_id | int | 🔧 | `pk_id` | 自增主键，直接映射 |
| 2 | chain_id | varchar(16) | ⚠️ | `industry_code` | **需编码转换** |
| 3 | chain_name | varchar(64) | ✅ | `industry_name` | 直接映射 |
| 4 | node_name | varchar(128) | ✅ | `industry_link_name` | 环节名称 |
| 5 | position | varchar(16) | ❌ | — | ODS 无上游/中游/下游标记（v2 预期的 `node_stage` 字段不存在） |
| 6 | seq_no | int | 🔧 | `pk_id` IN | 按同链同层排序 |
| 7~8 | create/update | 🟦 | NOW() | 系统 |

**⚠️ 关键缺口**：ODS 缺少以下节点属性字段：
- `node_stage`（上游/中游/下游）— **❌ 不存在**
- `node_type`（大类/业务/展示节点）— **❌ 不存在**
- `node_imp_level`（重要性）— **❌ 不存在**
- `downstream_link_code`（下游节点）— **❌ 不存在**
- `node_path`（节点路径）— **❌ 不存在**

### 4.3 `chain_enterprise` — 产业链-企业关联

**ODS 来源**: `dwd_org_industry_tags`（主源）+ `dwd_org_base_info`（补字段）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑 |
|---|---------|------|----------|---------|----------|
| 1 | enterprise_id | int | 🟦 | — | 序列生成 |
| 2 | enterprise_name | varchar(256) | ✅ | `company_name` | 直接映射 |
| 3 | chain_id | varchar(16) | ⚠️ | `industry_code` JSON拆行 | **需编码转换 + JSON 拆行** |
| 4 | chain_name | varchar(64) | ✅ | `industry_name` JSON拆行 | 并行拆行 |
| 5 | city | varchar(64) | 🔧 | `dwd_org_base_info.city` | JOIN ON credit_code==social_credit_code |
| 6 | district | varchar(64) | 🔧 | `dwd_org_base_info.district` | 同上 |
| 7 | reg_year | int | 🔧 | `dwd_org_base_info.incorporation_date` | 取年份 |
| 8 | revenue | decimal(20,2) | ❌ | — | ODS 无营收数据 |
| 9 | rd_ratio | decimal(5,2) | ❌ | — | ODS 无研发投入占比 |
| 10 | patent_count | int | 🔧 | `dwd_org_industry_chain_pat_dtl` | COUNT BY credit_code JOIN current_assign |
| 11 | is_high_tech | smallint | 🔧 | `dwd_org_innovation_carrier` | 是否有 carrier_type='高新技术企业' 记录 |
| 12~13 | create/update | 🟦 | NOW() | 系统 |

**处理逻辑（JSON 拆行）**：
- 一条 `dwd_org_industry_tags` 的 `industry_code = ["INB1309","INB1354"]` 需拆成 2 行 `chain_enterprise`
- 4,912 ODS 行 → 预计 ~5,700+ DWD 行（≥14% 企业跨产业）

**`dwd_org_base_info` JOIN 可行性**：

| base_info 字段 | 注释 | DWD 映射 |
|----------------|------|----------|
| city | 市 | → city |
| district | 区 | → district |
| incorporation_date | 成立日期 | → reg_year（取年份） |
| province / province_abbr | 省 | 可用于 chain_region_dist |
| social_credit_code | 统一社会信用代码 | JOIN KEY（与 credit_code 对应） |

### 4.4 `chain_news` — 产业动态资讯

**ODS 来源**: `dwd_industry_chain_news_info`

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑 |
|---|---------|------|----------|---------|----------|
| 1 | news_id | int | 🟦 | `pk_id` | 自增映射 |
| 2 | chain_id | varchar(16) | ⚠️ | `industry_code` | **需编码转换**（ODS 为 INB，DWD 当前为国标） |
| 3 | chain_name | varchar(64) | ✅ | `industry_name` | 直接映射 |
| 4 | enterprise_id | int | ❌ | — | ODS 新闻表无企业关联字段 |
| 5 | enterprise_name | varchar(256) | ❌ | — | 同上 |
| 6 | news_type | varchar(32) | ❌ | — | ODS 无分类字段（v2 预期 NLP 分类） |
| 7 | type_name | varchar(32) | ❌ | — | 同上 |
| 8 | title | varchar(1024) | ✅ | `title` | 直接映射（DWD 宽于 ODS 255） |
| 9 | summary | longtext | ✅ | `abstract` | 直接映射 |
| 10 | views | int | ❌ | — | ODS 无浏览量 |
| 11 | is_hot | smallint | ❌ | — | ODS 无热点标记 |
| 12 | publish_time | datetime | ✅ | `publish_date` | 直接映射 |
| 13 | data_year | int | 🔧 | YEAR(`publish_date`) | 派生 |
| 14 | data_month | varchar(10) | 🔧 | DATE_FORMAT(`publish_date`, '%Y-%m') | 派生 |
| 15~16 | create/update | 🟦 | NOW() | 系统 |

**覆盖**: 6/14 = 43%（排除 🟦）

### 4.5 `chain_region_dist` — 区域分布统计

**ODS 来源**: `dwd_org_industry_tags` + `dwd_org_base_info`（聚合统计）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑 |
|---|---------|------|----------|---------|----------|
| 1 | region_id | int | 🟦 | — | 序列生成 |
| 2 | chain_id | varchar(16) | ⚠️ | `industry_code` | **需编码转换** |
| 3 | chain_name | varchar(64) | ✅ | `industry_name` | |
| 4 | level | varchar(16) | 🔧 | — | 三张聚合表（province/city/district） |
| 5 | region_name | varchar(128) | 🔧 | `base_info.city` / `base_info.province` | JOIN 后 GROUP BY |
| 6 | parent_region | varchar(128) | 🔧 | `base_info.province`（当 level=city 时） | 层级关联 |
| 7 | enterprise_count | int | 🔧 | COUNT(DISTINCT credit_code) | 聚合 |
| 8 | institution_count | int | ❌ | — | ODS 无机构维度区分 |
| 9~10 | create/update | 🟦 | NOW() | 系统 |

### 4.6 `chain_investment` — 投融资明细

**ODS 来源**: ❌ `dwd_org_invest_info`（空）、`dwd_org_financing_info`（空）

| # | DWD字段 | 映射状态 | 说明 |
|---|---------|----------|------|
| 全部字段 | ❌ **无来源** | 两张投融资 ODS 表均为空表（0 行） |

此为**数据缺口**，Wave 1 阶段仅能保留 mock 数据或标记为空。

### 4.7 `chain_enterprise_stat` — 企业参与统计

**ODS 来源**: `dwd_org_industry_tags` + 算法加工

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑 |
|---|---------|------|----------|---------|----------|
| 1 | enterprise_id | int | 🟦 | — | 关联 chain_enterprise |
| 2 | chain_id | varchar(16) | ⚠️ | `industry_code` | **需编码转换** |
| 3 | node_name | varchar(128) | 🔧 | `industry_link_name` JSON拆行 | 企业参与的具体环节 |
| 4 | role | varchar(32) | 🔧 | — | 需算法判定上游/中游/下游角色 |
| 5 | participation_depth | decimal(5,3) | 🔧 | — | 需算法：参与环节数 / 总环节数 |
| 6~7 | create/update | 🟦 | NOW() | 系统 |

---

## 5. 映射覆盖率总览

| DWD 表 | 总字段 | ✅直接 | 🔧需计算 | ⚠️编码依赖 | ❌无来源 | 🟦系统 | 有效覆盖率* |
|--------|--------|--------|---------|-----------|---------|--------|------------|
| chain | 7 | 2 | 1 | 1 | 1 | 2 | 60% |
| chain_node | 8 | 2 | 1 | 1 | 1 | 2 | 50% |
| chain_enterprise | 13 | 2 | 4 | 1 | 2 | 2 | 55% |
| chain_news | 16 | 4 | 2 | 1 | 5 | 2 | 43% |
| chain_region_dist | 10 | 1 | 3 | 1 | 1 | 2 | 50% |
| chain_investment | 11 | 0 | 0 | 0 | 9 | 2 | **0%** |
| chain_enterprise_stat | 7 | 0 | 3 | 1 | 0 | 2 | 60% |
| **合计** | **72** | **11** | **14** | **6** | **19** | **14** | **47%** |

> *有效覆盖率 = (✅直接 + 🔧需计算) / (总字段 − 🟦系统 − ⚠️编码依赖) ≈ 25 / 52 = **48%**（排除编码待定 + 系统字段后）

---

## 6. 数据缺口与风险汇总

| 类型 | 编号 | 项 | 影响 DWD 表 | 严重度 | 建议 |
|------|------|-----|------------|--------|------|
| ⚠️ | GAP-01 | **编码体系不兼容**（INB vs 国标） | 全部 7 张表 | 🔴 阻断 | 先定编码方案再灌数 |
| ⚠️ | GAP-02 | `dwd_industry_chain_info` 缺少 `node_stage`/`node_type`/`node_imp_level`/`node_path` 等节点属性 | chain_node | 🟡 部分功能不可用 | `position` 暂 NULL；node_type 全标记为业务节点 |
| ❌ | GAP-03 | `dwd_org_invest_info` / `dwd_org_financing_info` 为空 | chain_investment | 🔴 完全缺失 | 需向供应方索要数据，或暂用 mock |
| ❌ | GAP-04 | ODS 新闻表无 `enterprise_id`/`news_type`/`views`/`is_hot` | chain_news | 🟡 部分字段不可用 | `enterprise_id` 暂 NULL；`news_type` 后续 NLP 补充 |
| ❌ | GAP-05 | ODS 无企业营收/研发投入数据 | chain_enterprise（revenue/rd_ratio） | 🟡 | 暂 mock 或从 `dwd_org_annual_financial_info` 补充（待确认该表是否有数据） |
| 🔧 | GAP-06 | JSON 数组拆行逻辑 | chain_enterprise/chain_enterprise_stat | 🟡 | 需 Python ETL 脚本 |
| 🔧 | GAP-07 | 企业→机构区分无来源 | chain_region_dist（institution_count） | 🟢 | 暂 0 |
| ❌ | GAP-08 | chain.description 无源 | chain | 🟢 | 可后续人工或 AI 补录 |

---

## 7. 与 v2 报告差异对比

| 差异项 | v2（基于要素库 5 表） | v3（基于 gkxlumenx_ods 实际） |
|--------|---------------------|---------------------------|
| 企业-链关联表 | `dwd_org_industry_chain_dtl`（独立字段，一行一企业一节点） | `dwd_org_industry_tags`（JSON 数组，需拆行） |
| 产品关联表 | `dwd_org_industry_chain_prod_dtl` | `dwd_org_industry_product_tags`（JSON 数组 product_name） |
| 节点属性丰富度 | 13 个直接映射字段（node_type/node_stage/node_path 等） | 仅 3 个（industry_code/industry_link_code/level） |
| 编码体系 | 一致的 chain_code | **不兼容**（INB vs 国标） |
| 投融资 | 预期有数据 | **空表** |
| 覆盖率 | 95.0% | **48%** |

---

## 8. 灌数推荐路径（分阶段）

### Phase 1：可立即灌数的表

| 优先级 | 表 | 前提条件 | 灌数方式 |
|--------|-----|---------|----------|
| P0 | `chain` | 定编码方案 | INSERT SELECT FROM `dwd_industry_chain_info` WHERE level=0 |
| P0 | `chain_node` | 定编码方案 | 全量 527 行直接映射（position 暂 NULL） |
| P0 | `chain_news` | 定编码方案 | 全量 5,000 行直接映射（enterprise_id/news_type 暂 NULL） |
| P1 | `chain_enterprise` | Python ETL（JSON 拆行 + JOIN base_info） | 4,912 → ~5,700 行 |
| P1 | `chain_enterprise_stat` | Python ETL + 后续算法 | 阶段性灌数 |

### Phase 2：需补数据或算法的表

| 表 | 需补内容 | 状态 |
|----|---------|------|
| `chain_region_dist` | city/district/province 聚合 | 待 ETL（有 base_info 可 JOIN） |
| `chain_investment` | 投融资数据 | **空表**，需供应方补数 |

### Phase 3：待后续算法产出

| 表 | 需要 | 算法 agent |
|----|------|-----------|
| ADS 全部 26 张表 | 先有 DWD 灌数完成 | algorithm-agent |

---

## 9. 综合结论

1. **ODS 4 张有数据表可支撑产业链 DWD 最小集**，但实际有效覆盖率仅 **48%**（远低于 v2 的 95%），主要原因是：
   - 节点属性字段大面积缺失（无 node_type/node_stage/node_imp_level 等）
   - 投融资 ODS 空表导致 `chain_investment` 完全无法灌数
   - 企业营收/研发数据缺失

2. **编码体系不兼容是首要阻塞项**：INB 编码（ODS）vs 国标编码（DWD mock），需 PM 先拍板编码方案。

3. **JSON 拆行是核心技术挑战**：`dwd_org_industry_tags` 的 `industry_code` 是 JSON 数组，需 Python ETL 拆成多行。

4. **投融资数据缺口**：`chain_investment` 完全无源，需与供应方沟通补数。

5. **`dwd_org_base_info`（10,996 行）是关键补充表**：可补 city/district/reg_year 字段。

---

*报告生成时间: 2026-07-24 ｜ ODS: gkxlumenx_ods 产业链 4 表 ｜ DWD: gkxlumenx_dwd 产业链 7 表 ｜ 作者: [human:李伟] + [agent:architect]*
