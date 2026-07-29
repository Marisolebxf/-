# 产业链 DWD 灌数表清单（7 张）

> 数据源: `gkxlumenx_ods` / 目标库: `gkxlumenx_dwd`
> 生成时间: 2026-07-28 ｜ 作者: [human:李伟]

| 符号 | 含义 |
|------|------|
| ✅ | ODS 有值，直接映射 |
| 🔧 | ODS 有值，需跨表 JOIN 或 ETL 加工 |
| ⚠️ | 编码阻塞（INB vs 国标），需先定编码方案 |
| ❌ | ODS 无来源 |

---

## 1. chain — 产业链主表（当前 8 行 mock）

| # | 字段 | 中文含义 | 类型 | 必填 | 主键 | 状态 | 来源 ODS |
|---|------|---------|------|------|------|------|----------|
| 1 | `chain_id` | 产业链编码 | varchar(16) | 是 | ✅ PK | ⚠️ | 需定编码方案（ODS:INB vs DWD:国标） |
| 2 | `chain_name` | 产业链名称 | varchar(64) | 是 | | ✅ | `dwd_industry_chain_info.industry_name`（WHERE level=0） |
| 3 | `industry_code` | 产业代码 | varchar(16) | | | ✅ | `dwd_industry_chain_info.industry_code`（WHERE level=0） |
| 4 | `node_count` | 环节节点数 | int | | | ✅ | `dwd_industry_chain_info.industry_link_code`（GROUP BY industry_code COUNT） |
| 5 | `description` | 产业链描述 | varchar(512) | | | ❌ | —（无来源） |
| 6 | `create_time` | 创建时间 | datetime | | | 🟦 | 系统填 NOW() |
| 7 | `update_time` | 更新时间 | datetime | | | 🟦 | 系统填 NOW() |

---

## 2. chain_node — 产业链节点表（当前 41 行 mock）

| # | 字段 | 中文含义 | 类型 | 必填 | 主键 | 状态 | 来源 ODS |
|---|------|---------|------|------|------|------|----------|
| 1 | `node_id` | 节点ID | int | 是 | ✅ PK | ✅ | `dwd_industry_chain_info.pk_id` |
| 2 | `chain_id` | 产业链编码 | varchar(16) | 是 | | ⚠️ | `dwd_industry_chain_info.industry_code`（需编码转换） |
| 3 | `chain_name` | 产业链名称 | varchar(64) | | | ✅ | `dwd_industry_chain_info.industry_name` |
| 4 | `node_name` | 环节名称 | varchar(128) | 是 | | ✅ | `dwd_industry_chain_info.industry_link_name` |
| 5 | `position` | 环节位置（上游/中游/下游） | varchar(16) | | | ❌ | —（ODS 无 node_stage 字段） |
| 6 | `seq_no` | 排序号 | int | | | 🔧 | `dwd_industry_chain_info.industry_code` + `dwd_industry_chain_info.level`（ROW_NUMBER 分组排序） |
| 7 | `create_time` | 创建时间 | datetime | | | 🟦 | 系统填 NOW() |
| 8 | `update_time` | 更新时间 | datetime | | | 🟦 | 系统填 NOW() |

---

## 3. chain_enterprise — 产业链-企业关联表（当前 120 行 mock）

| # | 字段 | 中文含义 | 类型 | 必填 | 主键 | 状态 | 来源 ODS |
|---|------|---------|------|------|------|------|----------|
| 1 | `enterprise_id` | 企业ID | int | 是 | ✅ PK | 🟦 | 系统自增 |
| 2 | `enterprise_name` | 企业名称 | varchar(256) | 是 | | ✅ | `dwd_org_industry_tags.company_name` |
| 3 | `chain_id` | 产业链编码 | varchar(16) | 是 | | ⚠️ | `dwd_org_industry_tags.industry_code`（JSON 拆行 + 编码转换） |
| 4 | `chain_name` | 产业链名称 | varchar(64) | | | ✅ | `dwd_org_industry_tags.industry_name`（JSON 拆行） |
| 5 | `city` | 所在城市 | varchar(64) | | | 🔧 | `dwd_org_base_info.city`（JOIN ON credit_code = social_credit_code） |
| 6 | `district` | 所在区县 | varchar(64) | | | 🔧 | `dwd_org_base_info.district`（同上） |
| 7 | `reg_year` | 成立年份 | int | | | 🔧 | `dwd_org_base_info.incorporation_date`（YEAR() 提取，同上 JOIN） |
| 8 | `revenue` | 营业收入（万元） | decimal(20,2) | | | ❌ | —（无来源） |
| 9 | `rd_ratio` | 研发投入占比（%） | decimal(5,2) | | | ❌ | —（无来源） |
| 10 | `patent_count` | 专利数量 | int | | | 🔧 | `dwd_org_industry_chain_pat_dtl.chain_code`（JOIN credit_code，COUNT 聚合） |
| 11 | `is_high_tech` | 是否高新技术企业 | smallint | | | 🔧 | `dwd_org_innovation_carrier.carrier_type`（JOIN social_credit_code，判断含"高新技术企业"） |
| 12 | `create_time` | 创建时间 | datetime | | | 🟦 | 系统填 NOW() |
| 13 | `update_time` | 更新时间 | datetime | | | 🟦 | 系统填 NOW() |

---

## 4. chain_news — 产业动态资讯表（当前 200 行 mock）

| # | 字段 | 中文含义 | 类型 | 必填 | 主键 | 状态 | 来源 ODS |
|---|------|---------|------|------|------|------|----------|
| 1 | `news_id` | 资讯ID | int | 是 | ✅ PK | ✅ | `dwd_industry_chain_news_info.pk_id` |
| 2 | `chain_id` | 产业链编码 | varchar(16) | 是 | | ⚠️ | `dwd_industry_chain_news_info.industry_code`（需编码转换） |
| 3 | `chain_name` | 产业链名称 | varchar(64) | | | ✅ | `dwd_industry_chain_news_info.industry_name` |
| 4 | `enterprise_id` | 关联企业ID | int | | | ❌ | —（ODS 新闻表不关联企业） |
| 5 | `enterprise_name` | 关联企业名称 | varchar(256) | | | ❌ | —（同上） |
| 6 | `news_type` | 资讯类型（融资/并购/新品/政策） | varchar(32) | | | ❌ | —（无分类字段，后续需 NLP 算法补） |
| 7 | `type_name` | 类型名称 | varchar(32) | | | ❌ | —（同上） |
| 8 | `title` | 资讯标题 | varchar(1024) | | | ✅ | `dwd_industry_chain_news_info.title` |
| 9 | `summary` | 资讯摘要 | longtext | | | ✅ | `dwd_industry_chain_news_info.abstract` |
| 10 | `views` | 浏览量 | int | | | ❌ | —（无来源） |
| 11 | `is_hot` | 是否热点 | smallint | | | ❌ | —（无来源，后续算法阈值判定） |
| 12 | `publish_time` | 发布时间 | datetime | | | ✅ | `dwd_industry_chain_news_info.publish_date` |
| 13 | `data_year` | 数据年份 | int | | | 🔧 | `dwd_industry_chain_news_info.publish_date`（YEAR() 提取） |
| 14 | `data_month` | 数据月份 | varchar(10) | | | 🔧 | `dwd_industry_chain_news_info.publish_date`（DATE_FORMAT('%Y-%m') 提取） |
| 15 | `create_time` | 创建时间 | datetime | | | 🟦 | 系统填 NOW() |
| 16 | `update_time` | 更新时间 | datetime | | | 🟦 | 系统填 NOW() |

---

## 5. chain_region_dist — 产业链区域分布统计表（当前 288 行 mock）

| # | 字段 | 中文含义 | 类型 | 必填 | 主键 | 状态 | 来源 ODS |
|---|------|---------|------|------|------|------|----------|
| 1 | `region_id` | 区域记录ID | int | 是 | ✅ PK | 🟦 | 系统自增 |
| 2 | `chain_id` | 产业链编码 | varchar(16) | 是 | | ⚠️ | `dwd_org_industry_tags.industry_code`（JSON 拆行 + 编码转换） |
| 3 | `chain_name` | 产业链名称 | varchar(64) | | | ✅ | `dwd_org_industry_tags.industry_name`（JSON 拆行后映射） |
| 4 | `level` | 区域层级（省/市/区） | varchar(16) | 是 | | 🔧 | 三张聚合产物（province / city / district） |
| 5 | `region_name` | 区域名称 | varchar(128) | 是 | | 🔧 | `dwd_org_base_info.province` / `dwd_org_base_info.city` / `dwd_org_base_info.district`（JOIN 后 GROUP BY） |
| 6 | `parent_region` | 上级区域 | varchar(128) | | | 🔧 | `dwd_org_base_info.province`（当 level=city 时，取 province） |
| 7 | `enterprise_count` | 企业数量 | int | | | 🔧 | `dwd_org_industry_tags.credit_code` + `dwd_org_base_info.*`（COUNT DISTINCT GROUP BY region） |
| 8 | `institution_count` | 机构数量 | int | | | ❌ | —（无来源） |
| 9 | `create_time` | 创建时间 | datetime | | | 🟦 | 系统填 NOW() |
| 10 | `update_time` | 更新时间 | datetime | | | 🟦 | 系统填 NOW() |

---

## 6. chain_investment — 产业链投融资明细表（当前 60 行 mock）

| # | 字段 | 中文含义 | 类型 | 必填 | 主键 | 状态 | 来源 ODS |
|---|------|---------|------|------|------|------|----------|
| 1 | `investment_id` | 投融资记录ID | int | 是 | ✅ PK | ❌ | —（`dwd_org_invest_info` 0 行，`dwd_org_financing_info` 0 行） |
| 2 | `chain_id` | 产业链编码 | varchar(16) | 是 | | ❌ | —（同上） |
| 3 | `chain_name` | 产业链名称 | varchar(64) | | | ❌ | —（同上） |
| 4 | `enterprise_id` | 企业ID | int | | | ❌ | —（同上） |
| 5 | `enterprise_name` | 企业名称 | varchar(256) | | | ❌ | —（同上） |
| 6 | `round` | 融资轮次 | varchar(32) | | | ❌ | —（同上） |
| 7 | `amount` | 融资金额（万元） | decimal(20,2) | | | ❌ | —（同上） |
| 8 | `investor` | 投资方 | varchar(256) | | | ❌ | —（同上） |
| 9 | `invest_date` | 投资日期 | datetime | | | ❌ | —（同上） |
| 10 | `data_year` | 数据年份 | int | | | ❌ | —（同上） |
| 11 | `create_time` | 创建时间 | datetime | | | 🟦 | 系统填 NOW() |
| 12 | `update_time` | 更新时间 | datetime | | | 🟦 | 系统填 NOW() |

> ⚠️ ODS 的 `dwd_org_invest_info`（0 行）和 `dwd_org_financing_info`（0 行）均为空表，**此表完全无法灌数**。

---

## 7. chain_enterprise_stat — 企业参与统计表（当前 209 行 mock）

| # | 字段 | 中文含义 | 类型 | 必填 | 主键 | 状态 | 来源 ODS |
|---|------|---------|------|------|------|------|----------|
| 1 | `enterprise_id` | 企业ID | int | 是 | | 🟦 | 关联 `gkxlumenx_dwd.chain_enterprise.enterprise_id` |
| 2 | `chain_id` | 产业链编码 | varchar(16) | 是 | | ⚠️ | `dwd_org_industry_tags.industry_code`（JSON 拆行 + 编码转换） |
| 3 | `node_name` | 参与环节名称 | varchar(128) | | | ✅ | `dwd_org_industry_tags.industry_link_name`（JSON 拆行） |
| 4 | `role` | 角色（上游/中游/下游） | varchar(32) | | | ❌ | —（无来源，需算法判定） |
| 5 | `participation_depth` | 参与深度 | decimal(5,3) | | | 🔧 | `dwd_org_industry_tags.industry_link_code`（算法：参与环节数 / 该链总环节数） |
| 6 | `create_time` | 创建时间 | datetime | | | 🟦 | 系统填 NOW() |
| 7 | `update_time` | 更新时间 | datetime | | | 🟦 | 系统填 NOW() |

---

## 汇总

| DWD 表 | 当前行数 | 字段数 | 涉及 ODS 源表 | 可灌性 |
|--------|---------|--------|-------------|--------|
| `chain` | 8 | 7 | `dwd_industry_chain_info` | ✅ 定编码后直接灌 |
| `chain_node` | 41 | 8 | `dwd_industry_chain_info` | ✅ 定编码后直接灌 |
| `chain_enterprise` | 120 | 13 | `dwd_org_industry_tags` + `dwd_org_base_info` + `dwd_org_industry_chain_pat_dtl` + `dwd_org_innovation_carrier` | 🔧 需 ETL 加工 |
| `chain_news` | 200 | 16 | `dwd_industry_chain_news_info` | ✅ 定编码后直接灌 |
| `chain_region_dist` | 288 | 10 | `dwd_org_industry_tags` + `dwd_org_base_info` | 🔧 需 ETL 聚合 |
| `chain_investment` | 60 | 12 | ❌ 无（`dwd_org_invest_info` / `dwd_org_financing_info` 空表） | ❌ 不可灌 |
| `chain_enterprise_stat` | 209 | 7 | `dwd_org_industry_tags` + 算法 | 🔧 需算法 |

**7 张表共 73 字段，来源涉及 6 张 ODS 表**：`dwd_industry_chain_info`、`dwd_org_industry_tags`、`dwd_industry_chain_news_info`、`dwd_org_base_info`、`dwd_org_industry_chain_pat_dtl`、`dwd_org_innovation_carrier`。

---

*文档生成时间: 2026-07-28 ｜ 作者: [human:李伟]*
