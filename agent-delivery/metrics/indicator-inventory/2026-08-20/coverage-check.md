# 产业链九维 / 企业五类与 seed 对照

## 1. 产业链基础指标（序号 95，九维）

| 一级 | 已有 seed 引用 | 补抽项 | 补抽条数 |
|---|---|---|---|
| 产业市场规模 | `M_CHAIN_MARKET_SIZE`、`M_CHAIN_MARKET_GROWTH` | 无 | 0 |
| 产业企业规模 | `M_CHAIN_ENTERPRISE_NEW_COUNT` | 企业规模增长率 | 1 |
| 产业机构规模 | `M_CHAIN_INSTITUTION_COUNT` | 机构规模增长率 | 1 |
| 产业投融资规模 | `M_CHAIN_INVEST_TOTAL`、`M_CHAIN_INVEST_COUNT` | 投融资规模增长率 | 1 |
| 全球产业区域分布 | `M_CHAIN_GLOBAL_REGION_COUNT` | 全球分布增长率 | 1 |
| 全国产业分布 | `M_CHAIN_NATIONAL_REGION_COUNT` | 全国分布增长率 | 1 |
| 产业动态资讯 | `M_CHAIN_NEWS_COUNT`、`M_CHAIN_HOT_NEWS_COUNT` | 热点指标平均值 | 1 |
| 深圳产业要素 | `M_CHAIN_SZ_ENTERPRISE_COUNT`、`M_CHAIN_SZ_INSTITUTION_COUNT` | 投融资/人才/科技创新要素数量 | 1 |
| 深圳产业分布 | `M_CHAIN_SZ_REGION_COUNT`、`M_CHAIN_SZ_ENTERPRISE_COUNT + M_CHAIN_SZ_INSTITUTION_COUNT` | 深圳产业分布增长率 | 1 |
| **合计** | 14 个引用 | | **8** |

说明：深圳产业分布“企业/机构总数”由两个已有 seed 合成，不作为补抽。

## 2. 企业基础指标（序号 97，五类）

| 一级 | 已有 seed 引用 | 补抽/部分项 | 补抽条数 |
|---|---|---|---|
| 重点企业提取 | `M_ENT_INNOVATIVE_COUNT`（部分）、`M_ENT_PATENT_TOTAL` | 重点企业技术交易额 | 1 |
| 企业类型分布 | `M_ENT_TYPE_COUNT`、`M_ENT_TYPE_RATIO` | 企业类型增长率 | 1 |
| 企业领域分布 | `M_ENT_DOMAIN_COVERAGE_COUNT`、`M_ENT_DOMAIN_COVERAGE_BREADTH`、`M_ENT_DOMAIN_COVERAGE_DEPTH` | 企业领域增长率 | 1 |
| 企业重点资讯 | 无直接 seed | 企业融资规模、并购/战略合作/新品发布指标 | 2 |
| 新增企业数量 | `M_ENT_NEW_COUNT_Y` | 新增企业数量增长率 | 1 |
| **合计** | 8 个引用 | | **6** |

## 3. 结论

- 产业链九维、企业五类均已完整进入 `inventory.yaml`；
- 已有 seed 的叶子标了 `seed_ref`，缺的叶子标 `补抽`；
- 未使用 `CHAIN-SZ` demo 种子冒充九维基础指标已齐全；
- 本任务只盘点缺口，不修改 seed。
