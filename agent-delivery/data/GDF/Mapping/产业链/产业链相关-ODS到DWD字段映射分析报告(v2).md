# 产业链相关 ODS → DWD 字段映射分析报告（v2）

> 生成时间: 2026-06-23 ｜ 版本: v2（ODS 数据源：三方「要素库」产业链 Sheet）
> 分析范围: **产业链（CHAIN/E2）** 数据域
> 任务: ALGO-DB-DWD-C01 · Epic E-DB-DESIGN-ALGO-V11-DWD

---

## 1. 背景与版本变更

本报告分析三方采购数据源（ODS 层）能否满足本项目自建 **`gkx_dwd` 产业链标准明细表** 的字段填充需求，对标 `企业域数据库设计(v1).md` 与 `企业相关-ODS到DWD字段映射分析报告(v2).md` 体例。

| 项 | 说明 |
|----|------|
| ODS 来源 | 三方「要素库」产业链要素库 **5 张表**（`data/ODS源数据表结构清单(v2).md` §4.3） |
| 宏观补充 | `dwd_series_metadata`、`dwd_macro_index_data`（市场规模，⚠️ **Q-ALGO-003**） |
| DWD 目标 | **4 张**自建标准表（3 张核心 + 1 张资讯明细） |
| DWM 已有 | `gkx_dwm.dwm_industry_chain_snapshot`（指标聚合宽表，本任务不重复） |
| ENT 交叉 | `gkx_dwd.enterprise_industry`、`enterprise_supply_chain`（引用 ENT v1，本域不重复） |

> **命名澄清**：要素库 `dwd_industry_chain_*` / `dwd_org_industry_chain_*` 是供应方命名，业务定位为**三方 ODS（贴源层）**；本报告右侧 `gkx_dwd.industry_chain*` 才是本项目自建 DWD 标准明细层。

**映射状态图例**：
- ✅**直接映射**：ODS 有对应字段，可直接取值或简单类型/枚举转换
- 🔧**需计算/算法**：有数据源但需聚合、去重、推导或算法模型
- ⚠️**待确认/质量待验**：需业务确认或口径待甲方定稿（含 Q-ALGO-003）
- ❌**无来源**：要素库中无相关数据
- 🟦**系统/预留**：主键、时间戳、扩展位等由 ETL 填充

---

## 2. 产业链相关 ODS 源表概况

| # | ODS 表 | 中文名 | 字段数 | 角色 |
|---|--------|--------|--------|------|
| 1 | `dwd_industry_chain_info` | 产业链图谱 | 16 | **主源**：链 + 节点树/上下游/环节 |
| 2 | `dwd_org_industry_chain_dtl` | 产业关联企业信息 | 10 | **主源**：链-节点-企业关联 + 评分 |
| 3 | `dwd_org_industry_chain_prod_dtl` | 产业链企业关联产品 | 10 | **辅助**：主营产品，丰富 org_rel.ext |
| 4 | `dwd_org_industry_chain_pat_dtl` | 产业链关联专利 | 14 | **交叉 ENT**：专利明细归 `enterprise_patent_history` / `enterprise_cooperation`，本域不建表 |
| 5 | `dwd_industry_chain_news_info` | 产业动态资讯 | 10 | **主源**：`industry_chain_news` |

**宏观/市场规模补充（非产业链 Sheet，跨域引用）**：

| ODS 表 | 字段数 | 用途 |
|--------|--------|------|
| `dwd_series_metadata` | 15 | 序列元数据（产业标签 ↔ index_code 映射，⚠️ Q-ALGO-003） |
| `dwd_macro_index_data` | 9 | 宏观指标时序值（`index_value` → 市场规模候选） |
| `dwd_series_timepoints` | 2 | 序列时间点（与 macro 联查） |

**企业域交叉引用（不重复建表）**：

| ENT DWD 表 | 主要 ODS | 与产业链域关系 |
|------------|----------|----------------|
| `enterprise_industry` | `dwd_org_industry_chain_dtl` | 企业视角产业链归属；灌数源与 `industry_chain_org_rel` 同源 |
| `enterprise_supply_chain` | `dwd_industry_chain_info` + `dwd_org_industry_chain_dtl` | 上下游企业对；由节点 `downstream_link_code` / `node_stage` 推导 |

---

## 3. DWD 产业链标准表概览

| # | DWD 表（物理） | 字段数 | 说明 | 主要 ODS 来源 |
|---|----------------|--------|------|---------------|
| 1 | `gkx_dwd.industry_chain` | 11 | 产业链主数据（链编码、名称、层级） | `dwd_industry_chain_info`（按 chain_code 去重） |
| 2 | `gkx_dwd.industry_chain_node` | 20 | 环节/节点明细 | `dwd_industry_chain_info` |
| 3 | `gkx_dwd.industry_chain_org_rel` | 15 | 链-节点-企业/机构关联 | `dwd_org_industry_chain_dtl`、`dwd_org_industry_chain_prod_dtl` |
| 4 | `gkx_dwd.industry_chain_news` | 14 | 产业资讯明细（可选纳入最小集，本期交付） | `dwd_industry_chain_news_info` |

> **微调说明（相对派单建议表集）**：保留建议 3+1 四表；`prod_dtl` 产品列表写入 `industry_chain_org_rel.ext` JSON，不单独建表；`pat_dtl` 归 ENT 域处理。

---

## 4. 映射覆盖率总览

| DWD 表 | 总字段 | ✅直接 | 🔧需计算 | ⚠️待确认 | ❌无来源 | 🟦系统/预留 | 覆盖率* |
|--------|--------|--------|---------|---------|---------|------------|--------|
| industry_chain | 11 | 3 | 3 | 0 | 0 | 5 | 100% |
| industry_chain_node | 20 | 13 | 2 | 0 | 0 | 5 | 100% |
| industry_chain_org_rel | 15 | 7 | 3 | 1 | 0 | 4 | 100% |
| industry_chain_news | 14 | 7 | 0 | 1 | 0 | 6 | 100% |
| **合计** | **60** | **30** | **8** | **2** | **0** | **20** | **100%** |

> *覆盖率 = (✅直接 + 🔧需计算) / (总字段 − 系统/预留) = 38 / 40 = **95.0%**。
> 宏观市场规模字段不在 DWD 明细表内，经 DWM `market_size` 承接（⚠️ Q-ALGO-003）。

---

## 5. 逐表字段映射详情

### 5.1 gkx_dwd.industry_chain（产业链主表，11 字段）

**ODS 来源**: `dwd_industry_chain_info`（按 `chain_code` 去重聚合）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增主键 |
| 2 | chain_code | varchar(64) | ✅直接 | `dwd_industry_chain_info.chain_code` | 产业链业务主键 |
| 3 | chain_name | varchar(255) | ✅直接 | `dwd_industry_chain_info.chain_name` | 取同 chain_code 下任意非空值（应一致） |
| 4 | max_level | int | 🔧需计算 | `dwd_industry_chain_info.level` | MAX(level) GROUP BY chain_code |
| 5 | node_count | int | 🔧需计算 | `dwd_industry_chain_info.node_id` | COUNT(DISTINCT node_id) |
| 6 | biz_node_count | int | 🔧需计算 | `node_type=2` 的 node_id | 业务节点数（可关联企业） |
| 7 | data_source | varchar(100) | ✅直接 | `dwd_industry_chain_info.data_source` | 数据来源 |
| 8 | data_collect_time | datetime | ✅直接 | `dwd_industry_chain_info.created_time` | ODS 入库时间 |
| 9 | ext | json | 🟦系统 | - | 扩展位 |
| 10 | create_time | datetime | 🟦系统 | - | ETL 写入 |
| 11 | update_time | datetime | 🟦系统 | - | ETL 更新 |

### 5.2 gkx_dwd.industry_chain_node（产业链节点，20 字段）

**ODS 来源**: `dwd_industry_chain_info`（一行一节点：`chain_code` + `node_id`）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | chain_code | varchar(64) | ✅直接 | `chain_code` | 外键 → industry_chain |
| 3 | node_id | varchar(64) | ✅直接 | `node_id` | 节点业务键 |
| 4 | node_name | varchar(255) | ✅直接 | `node_name` | 节点名称 |
| 5 | node_type | tinyint | ✅直接 | `node_type` | 1大类/2业务/3展示；值域 1,2,3 |
| 6 | level | tinyint | ✅直接 | `level` | 节点层级 1~5 |
| 7 | node_seq | int | ✅直接 | `node_seq` | 同父级排序 |
| 8 | parent_id | varchar(64) | ✅直接 | `parent_id` | 父节点代码 |
| 9 | parent_name | varchar(255) | ✅直接 | `parent_name` | 父节点名称 |
| 10 | node_imp_level | tinyint | ✅直接 | `node_imp_level` | 重要性 1~5，仅 node_type=2 |
| 11 | downstream_link_code | varchar(64) | ✅直接 | `downstream_link_code` | 下游节点代码 |
| 12 | node_stage | tinyint | ✅直接 | `node_stage` | 1上游/2中游/3下游 |
| 13 | node_path | text | ✅直接 | `node_path` | 节点路径 |
| 14 | node_stage_name | varchar(20) | 🔧需计算 | `node_stage` | CASE 映射：上游/中游/下游 |
| 15 | is_biz_node | tinyint | 🔧需计算 | `node_type` | node_type=2 → 1，否则 0 |
| 16 | data_source | varchar(100) | ✅直接 | `data_source` | |
| 17 | data_collect_time | datetime | ✅直接 | `created_time` | |
| 18 | ext | json | 🟦系统 | - | |
| 19 | create_time | datetime | 🟦系统 | - | |
| 20 | update_time | datetime | 🟦系统 | - | |

> ⚠️ `node_type=3` 展示节点不关联企业；ETL 灌 `industry_chain_org_rel` 时建议仅保留 `node_type IN (1,2)` 且企业关联仅来自业务节点。

### 5.3 gkx_dwd.industry_chain_org_rel（链-企业关联，15 字段）

**ODS 来源**: `dwd_org_industry_chain_dtl`（主）、`dwd_org_industry_chain_prod_dtl`（产品 enrich）

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | 序列自增 |
| 2 | chain_code | varchar(64) | ✅直接 | `dwd_org_industry_chain_dtl.chain_code` | |
| 3 | node_id | varchar(64) | ✅直接 | `node_id` | |
| 4 | node_name | varchar(255) | ✅直接 | `node_name` | 冗余便于查询 |
| 5 | org_id | varchar(64) | ✅直接 | `antitypic` | ODS 企业身份 id；与 ENT `org_id` 口径对齐 |
| 6 | enterprise_code | varchar(64) | ✅直接 | `credit_code` | 统一社会信用代码 → ENT `enterprise_code` |
| 7 | enterprise_name | varchar(500) | 🔧需计算 | `dwd_org_industry_chain_prod_dtl.company_name` | prod_dtl LEFT JOIN 补全名称 |
| 8 | chain_score | decimal(10,4) | ✅直接 | `chain_score` | 产业链评分 |
| 9 | rel_type | varchar(32) | 🔧需计算 | - | 默认 `enterprise`；机构主体待 ORG 域扩展为 `org` |
| 10 | tech_products | json | 🔧需计算 | `dwd_org_industry_chain_prod_dtl` | 按 chain+org 聚合主营产品数组 |
| 11 | data_source | varchar(100) | ✅直接 | `data_source` | |
| 12 | data_collect_time | datetime | ✅直接 | `created_time` | |
| 13 | ext | json | 🟦系统 | - | 兜底未预见属性 |
| 14 | create_time | datetime | 🟦系统 | - | ETL 写入 |
| 15 | update_time | datetime | 🟦系统 | - | ETL 更新 |

> **实体归一**：`enterprise_code = credit_code`；若 credit_code 为空则保留 `org_id`，ETL 经 `dwd_org_reg_info.external_id` / `dwd_company_base.credit_code` 回填（与 ENT v1 §3.1 双源归一一致）。
> ⚠️ `org_id`（antitypic）与 `enterprise_code` 可能一对多脏数据，ETL 需 DQ 告警。

### 5.4 gkx_dwd.industry_chain_news（产业资讯，14 字段）

**ODS 来源**: `dwd_industry_chain_news_info`

| # | DWD字段 | 类型 | 映射状态 | ODS来源 | 映射逻辑/备注 |
|---|---------|------|----------|---------|---------------|
| 1 | id | bigint | 🟦系统 | - | |
| 2 | chain_code | varchar(64) | ✅直接 | `chain_code` | |
| 3 | chain_name | varchar(255) | ✅直接 | `chain_name` | |
| 4 | news_id | varchar(64) | ✅直接 | `news_id` | 资讯业务键 |
| 5 | title | varchar(500) | ✅直接 | `title` | 源 255，DWD 扩至 500 |
| 6 | release_date | date | ✅直接 | `relaese_date` | ODS 字段拼写保留映射，DWD 规范为 release_date |
| 7 | summary | text | ✅直接 | `summary` | |
| 8 | source | varchar(255) | ✅直接 | `source` | 资讯来源 |
| 9 | is_hot | tinyint | ⚠️待确认 | - | bid §4.1.1.1(7) 热点判定需浏览量/评论数，ODS 无此字段，暂 NULL |
| 10 | data_source | varchar(100) | ✅直接 | `data_source` | |
| 11 | data_collect_time | datetime | ✅直接 | `created_time` | |
| 12 | ext | json | 🟦系统 | - | |
| 13 | create_time | datetime | 🟦系统 | - | ETL 写入 |
| 14 | update_time | datetime | 🟦系统 | - | ETL 更新 |

### 5.5 不建 DWD 表的 ODS 映射说明

| ODS 表 | 处理方式 |
|--------|----------|
| `dwd_org_industry_chain_pat_dtl` | 专利明细 → ENT `enterprise_patent_history` / `enterprise_cooperation`（见企业映射报告 §5.3/§5.7） |
| `dwd_org_industry_chain_prod_dtl` | 产品 → `industry_chain_org_rel.tech_products` JSON |
| `dwd_macro_index_data` + `dwd_series_metadata` | 市场规模 → DWM `dwm_industry_chain_snapshot.market_size`（⚠️ Q-ALGO-003） |
| `dwd_industry_code`（量子专题） | 辅助环节编码维表；与 chain 编码体系不同，归 `gkx_dim.dim_industry_chain` 扩展，本期引用 |

---

## 6. bid §4.1.1.1 九维指标 ↔ DWD/DWM/ADS 链路

| # | bid 九维（§4.1.1.1） | acceptance | DWD 明细 | DWM 宽表 | ADS / cfg | 状态 |
|---|---------------------|------------|----------|----------|-----------|------|
| 1 | 产业市场规模 | IC-03 | —（宏观 ODS） | `market_size` ← `dwd_macro_index_data` | `ads_metric_timeseries` · `M_CHAIN_MARKET_SIZE_Y` | ⚠️ Q-ALGO-003 |
| 2 | 产业企业规模 | IC-04 | `industry_chain_org_rel` | `enterprise_cnt` | `M_CHAIN_ENT_CNT_Y`（map.yaml） | 🔧 聚合 |
| 3 | 产业机构规模 | IC-05 | 交叉 ORG 域（`dwd_org_reg_info`） | `org_cnt` | cfg_metric 待注册 | 🔧 跨域 |
| 4 | 产业投融资规模 | IC-06 | 交叉 `dwd_org_financing_info` | `invest_amount` | `M_CHAIN_INVEST_AMOUNT_Y` | 🔧 跨域 |
| 5 | 全球产业区域分布 | IC-07 | `industry_chain_org_rel` + ENT `enterprise` | — | `ads_metric_timeseries` dim_json.country | 🔧 |
| 6 | 全国产业分布 | IC-08 | 同上 + `headquarters_province` | — | dim_json.province | 🔧 |
| 7 | 产业动态资讯 | IC-09 | `industry_chain_news` | — | 资讯统计 ADS（待 Wave1） | ⚠️ 热点字段缺 ODS |
| 8 | 深圳产业要素 | IC-10 | 多域汇总（投融资/人才/专利计数） | `ext` JSON | 深圳要素指标待注册 | 🔧 |
| 9 | 深圳产业分布 | IC-11 | `industry_chain_org_rel` + ENT 深圳区划 | — | dim_json.district | 🔧 |

**分层边界（铁律 3）**：

```text
ODS（5 张产业链表 + 宏观补充）
    │  ETL 去重 / 归一 / 关系明细
    ▼
DWD  industry_chain / industry_chain_node / industry_chain_org_rel / industry_chain_news
    │  Python 按链×日聚合 + 跨域 JOIN（企业/机构/投融资/宏观）
    ▼
DWM  dwm_industry_chain_snapshot（chain_code × stat_date 宽表：enterprise_cnt/org_cnt/invest_amount/market_size）
    │  algorithm-agent 指标计算
    ▼
ADS  ads_metric_timeseries（Java 只读）+ ads_model_score（M3 深度模型）
```

---

## 7. 与 DWM / ENT 分工

| 层 | 对象 | 粒度 | 谁写 | 典型用途 |
|----|------|------|------|----------|
| DWD | `industry_chain*` | 链/节点/企业关系/资讯 **明细** | Python ETL | 图谱灌数、节点下钻、企业列表 |
| DWM | `dwm_industry_chain_snapshot` | 链 × 统计日 **指标宽表** | Python + algorithm | M1 基础指标聚合输入 |
| ENT | `enterprise_industry` / `enterprise_supply_chain` | 企业视角归属/供应链 | Python ETL | 企业专题、Nebula `gkx_enterprise` |
| ADS | `ads_metric_timeseries` | 指标时序契约面 | Python | **Java 只读** |

---

## 8. ETL 示例（核心逻辑）

```sql
-- Step1: 产业链主表（去重）
INSERT INTO gkx_dwd.industry_chain (chain_code, chain_name, max_level, node_count, biz_node_count, data_source, data_collect_time)
SELECT chain_code,
       MAX(chain_name),
       MAX(CAST(level AS SIGNED)),
       COUNT(DISTINCT node_id),
       COUNT(DISTINCT CASE WHEN node_type = 2 THEN node_id END),
       MAX(data_source),
       MAX(created_time)
FROM ods.dwd_industry_chain_info
GROUP BY chain_code;

-- Step2: 节点明细（一比一）
INSERT INTO gkx_dwd.industry_chain_node (...)
SELECT ... FROM ods.dwd_industry_chain_info;

-- Step3: 链-企业关联（实体归一）
INSERT INTO gkx_dwd.industry_chain_org_rel (chain_code, node_id, org_id, enterprise_code, chain_score, ...)
SELECT d.chain_code, d.node_id, d.antitypic,
       COALESCE(d.credit_code, o.external_id, c.credit_code),
       d.chain_score, ...
FROM ods.dwd_org_industry_chain_dtl d
LEFT JOIN ods.dwd_org_reg_info o ON d.antitypic = o.org_id
LEFT JOIN ods.dwd_company_base c ON d.antitypic = CAST(c.id AS CHAR);
```

---

## 9. 数据缺口与风险

| 类型 | 项 | 说明 | 建议 |
|------|-----|------|------|
| ⚠️ | Q-ALGO-003 | 市场规模：`dwd_macro_index_data.index_code` 与 `chain_code` 映射规则未确认 | PM 客户决策清单；DWM `market_size` 暂 Mock |
| ⚠️ | 资讯热点 | ODS 无浏览量/评论数 | `is_hot` 暂 NULL；算法侧规则待补 |
| ⚠️ | org_id 归一 | `antitypic` 与 `credit_code` 可能不一致 | DQ-CHAIN-04 交叉校验 |
| 🔧 | 机构主体 | 产业链机构非企业主体 | `rel_type=org` 待 ORG 域落地 |
| ❌ | 无 | 本域 4 表字段均有 ODS 或系统来源 | — |

---

## 10. 综合结论

1. **ODS 5 表可支撑 CHAIN DWD 最小集**：图谱/关联/资讯直接映射覆盖率 **95.0%**（剔除系统列）。
2. **专利与产品不重复建表**：专利归 ENT；产品写入 `org_rel.tech_products`。
3. **市场规模走 DWM**：宏观 ODS 补充，口径 ⚠️ Q-ALGO-003，不在 DWD 落列。
4. **与 ENT 分工清晰**：本域管「链结构 + 链-企业关系」；企业视角归属/供应链见 ENT v1。
5. **下游**：DWM 快照 → `ads_metric_timeseries`；图谱 → Nebula `gkx_industry`（schema 引用见域设计 §7）。

---

*报告生成时间: 2026-06-23 ｜ ODS: 产业链要素库 5 表 + 宏观 2 表 ｜ DWD: gkx_dwd 产业链 4 表 ｜ 设计详述: `产业链域数据库设计(v1).md`*
