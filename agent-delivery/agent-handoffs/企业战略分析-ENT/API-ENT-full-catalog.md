# 企业维度 Java 门面总接口文档（76 端点）

- 时间：2026-07-20
- 作者：api-agent（监管：human:侯佳伟）
- 仓库：`lumen-svc-platform` / 模块：`gkxlumen-topic-enterprise`
- **字段结构真源**：Java DTO（`EnterpriseResponseDTOs` / `EnterpriseExtendedDTOs` / `Enterprise*Request`）
- **中文说明真源**：优先 Java javadoc；缺省时回填 Python  
  `demo-svc-topic-py/docs/API-接口文档.md` 字段表
- 关联：`API-ENT-contract-draft.md`、五单 handoff（`ENT-JAVA-*`）
- 范围：Python `gkx-search` **76** 个业务 POST（不含 `GET /healthz`）
- **前端入口说明**：接企业相关前端/联调任务时，以本文为接口真源；返回字段表与 JSON 示例按 Java typed DTO 完整展开。

## 1. 路由拼接规则

```text
gateway地址 / {EnableOpenApi value} / {Controller @RequestMapping} / {方法映射}
```

| 段 | 来源 | 当前值 |
| --- | --- | --- |
| gateway地址 | Swagger / 网关基址 | 例如 `http://127.0.0.1:9999` |
| OpenAPI 前缀 | `@EnableOpenApi("enterprise")` | `/enterprise` |
| Controller 前缀 | `@RequestMapping` | `/topic/v1` 或 `/topic/v1/...` |
| 方法路径 | `@PostMapping` | 如 `/search/query` |

示例：`POST gateway地址/enterprise/topic/v1/search/query` → Python `POST /internal/gkx-search/enterprises`。

## 2. 调用链

```text
前端 → gateway地址/enterprise/topic/v1/** → Controller → Service → RemoteEnterprisePythonClient → /internal/gkx-search/**
```

## 3. 76 端点总览

| # | 分组 | 网关路径（相对 `{GW}`） | Python 下游 | 请求对象 | 返回 data 类型 |
|---:|---|---|---|---|---|
| 1 | 检索 | `/topic/v1/search/query` | `/internal/gkx-search/enterprises` | `EnterpriseSearchRequest` | `SearchResponse` |
| 2 | 检索 | `/topic/v1/search/suggest` | `/internal/gkx-search/enterprises/suggest` | `EnterpriseSuggestRequest` | `List<SuggestItem>` |
| 3 | 检索 | `/topic/v1/search/advanced` | `/internal/gkx-search/enterprises/advanced` | `EnterpriseSearchRequest` | `SearchResponse` |
| 4 | 检索 | `/topic/v1/recommend` | `/internal/gkx-search/enterprises/recommend` | `EnterpriseRecommendRequest` | `RecommendResponse` |
| 5 | 检索辅助 | `/topic/v1/search/aggregations` | `/internal/gkx-search/enterprises/aggregations` | `EnterpriseAggregationRequest` | `AggregationResponse` |
| 6 | 检索辅助 | `/topic/v1/search/by-codes` | `/internal/gkx-search/enterprises/by-codes` | `EnterpriseByCodesRequest` | `SearchResponse` |
| 7 | 检索辅助 | `/topic/v1/search/hot` | `/internal/gkx-search/enterprises/hot` | `EnterpriseHotRequest` | `List<HotKeywordItem>` |
| 8 | 检索辅助 | `/topic/v1/search/smart` | `/internal/gkx-search/enterprises/smart` | `EnterpriseSmartSearchRequest` | `SearchResponse` |
| 9 | 元数据 | `/topic/v1/search/meta/filters` | `/internal/gkx-search/meta/filters` | `EnterpriseMetaRequest` | `FiltersResponse` |
| 10 | 元数据 | `/topic/v1/search/meta/regions` | `/internal/gkx-search/meta/regions` | `EnterpriseRegionRequest` | `RegionsResponse` |
| 11 | 元数据 | `/topic/v1/search/meta/company-types` | `/internal/gkx-search/meta/company-types` | `EnterpriseMetaRequest` | `OptionsResponse` |
| 12 | 元数据 | `/topic/v1/search/meta/enterprise-scales` | `/internal/gkx-search/meta/enterprise-scales` | `EnterpriseMetaRequest` | `OptionsResponse` |
| 13 | 元数据 | `/topic/v1/search/meta/tags` | `/internal/gkx-search/meta/tags` | `EnterpriseTagRequest` | `TagDictionaryResponse` |
| 14 | 对比篮 | `/topic/v1/compare-basket/compare` | `/internal/gkx-search/enterprises/compare` | `EnterpriseCompareRequest` | `CompareResponse` |
| 15 | 画像基础 | `/topic/v1/profile/panorama` | `/internal/gkx-search/profile` | `EnterpriseProfileRequest` | `PanoramaResponse` |
| 16 | 画像基础 | `/topic/v1/profile/card` | `/internal/gkx-search/profile/card` | `EnterpriseProfileRequest` | `CardResponse` |
| 17 | 画像基础 | `/topic/v1/profile/basic` | `/internal/gkx-search/profile/basic` | `EnterpriseProfileRequest` | `BasicResponse` |
| 18 | 画像基础 | `/topic/v1/profile/overview` | `/internal/gkx-search/profile/overview` | `EnterpriseProfileRequest` | `OverviewResponse` |
| 19 | 画像基础 | `/topic/v1/profile/news` | `/internal/gkx-search/profile/news` | `EnterpriseProfileRequest` | `NewsResponse` |
| 20 | 画像基础 | `/topic/v1/profile/risk/summary` | `/internal/gkx-search/profile/risk/summary` | `EnterpriseProfileRequest` | `RiskSummaryResponse` |
| 21 | 画像细分 | `/topic/v1/profile/finance` | `/internal/gkx-search/profile/finance` | `EnterpriseProfileRequest` | `FinanceHistoryResponse` |
| 22 | 画像细分 | `/topic/v1/profile/patent` | `/internal/gkx-search/profile/patent` | `EnterpriseProfileRequest` | `PatentPageResponse` |
| 23 | 画像细分 | `/topic/v1/profile/tags` | `/internal/gkx-search/profile/tags` | `EnterpriseProfileRequest` | `ProfileTagsResponse` |
| 24 | 画像细分 | `/topic/v1/profile/competitiveness` | `/internal/gkx-search/profile/competitiveness` | `EnterpriseProfileRequest` | `CompetitivenessResponse` |
| 25 | 画像细分 | `/topic/v1/profile/bids` | `/internal/gkx-search/profile/bids` | `EnterpriseProfileRequest` | `BidPageResponse` |
| 26 | 画像细分 | `/topic/v1/profile/executives` | `/internal/gkx-search/profile/executives` | `EnterpriseProfileRequest` | `ExecutiveListResponse` |
| 27 | 画像细分 | `/topic/v1/profile/innovation-carriers` | `/internal/gkx-search/profile/innovation-carriers` | `EnterpriseProfileRequest` | `InnovationCarrierListResponse` |
| 28 | 画像细分 | `/topic/v1/profile/qualifications` | `/internal/gkx-search/profile/qualifications` | `EnterpriseProfileRequest` | `QualificationResponse` |
| 29 | 画像细分 | `/topic/v1/profile/patent/history` | `/internal/gkx-search/profile/patent/history` | `EnterpriseProfileRequest` | `PatentHistoryResponse` |
| 30 | 画像细分 | `/topic/v1/profile/finance/latest` | `/internal/gkx-search/profile/finance/latest` | `EnterpriseProfileRequest` | `FinanceLatestResponse` |
| 31 | 画像细分 | `/topic/v1/profile/finance/trend` | `/internal/gkx-search/profile/finance/trend` | `EnterpriseProfileRequest` | `FinanceTrendResponse` |
| 32 | 画像细分 | `/topic/v1/profile/supply-chain` | `/internal/gkx-search/profile/supply-chain` | `EnterpriseProfileRequest` | `SupplyChainResponse` |
| 33 | 画像细分 | `/topic/v1/profile/invest` | `/internal/gkx-search/profile/invest` | `EnterpriseProfileRequest` | `InvestPageResponse` |
| 34 | 画像细分 | `/topic/v1/profile/shareholders` | `/internal/gkx-search/profile/shareholders` | `EnterpriseProfileRequest` | `ShareholderResponse` |
| 35 | 画像细分 | `/topic/v1/profile/financings` | `/internal/gkx-search/profile/financings` | `EnterpriseProfileRequest` | `FinancingPageResponse` |
| 36 | 画像细分 | `/topic/v1/profile/financings/summary` | `/internal/gkx-search/profile/financings/summary` | `EnterpriseProfileRequest` | `FinancingSummaryResponse` |
| 37 | 风险 | `/topic/v1/profile/risk/all` | `/internal/gkx-search/profile/risk/all` | `EnterpriseRiskAllRequest` | `RiskAllResponse` |
| 38 | 风险 | `/topic/v1/profile/risk/judicial-case` | `/internal/gkx-search/profile/risk/judicial-case` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 39 | 风险 | `/topic/v1/profile/risk/dishonest` | `/internal/gkx-search/profile/risk/dishonest` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 40 | 风险 | `/topic/v1/profile/risk/executed` | `/internal/gkx-search/profile/risk/executed` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 41 | 风险 | `/topic/v1/profile/risk/limit-high` | `/internal/gkx-search/profile/risk/limit-high` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 42 | 风险 | `/topic/v1/profile/risk/lawsuit` | `/internal/gkx-search/profile/risk/lawsuit` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 43 | 风险 | `/topic/v1/profile/risk/court-filed` | `/internal/gkx-search/profile/risk/court-filed` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 44 | 风险 | `/topic/v1/profile/risk/court-notice` | `/internal/gkx-search/profile/risk/court-notice` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 45 | 风险 | `/topic/v1/profile/risk/court-announcement` | `/internal/gkx-search/profile/risk/court-announcement` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 46 | 风险 | `/topic/v1/profile/risk/equity-freeze` | `/internal/gkx-search/profile/risk/equity-freeze` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 47 | 风险 | `/topic/v1/profile/risk/equity-pledge` | `/internal/gkx-search/profile/risk/equity-pledge` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 48 | 风险 | `/topic/v1/profile/risk/zhongben` | `/internal/gkx-search/profile/risk/zhongben` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 49 | 风险 | `/topic/v1/profile/risk/chattel-mortgage` | `/internal/gkx-search/profile/risk/chattel-mortgage` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 50 | 风险 | `/topic/v1/profile/risk/judicial-sale` | `/internal/gkx-search/profile/risk/judicial-sale` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 51 | 风险 | `/topic/v1/profile/risk/bankruptcy` | `/internal/gkx-search/profile/risk/bankruptcy` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 52 | 风险 | `/topic/v1/profile/risk/abnormal` | `/internal/gkx-search/profile/risk/abnormal` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 53 | 风险 | `/topic/v1/profile/risk/punishment` | `/internal/gkx-search/profile/risk/punishment` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 54 | 风险 | `/topic/v1/profile/risk/illegal` | `/internal/gkx-search/profile/risk/illegal` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 55 | 风险 | `/topic/v1/profile/risk/tax-punish` | `/internal/gkx-search/profile/risk/tax-punish` | `EnterpriseProfileRequest` | `RiskTypePageResponse` |
| 56 | 图谱 | `/topic/v1/profile/graph/subgraph` | `/internal/gkx-search/profile/graph/subgraph` | `EnterpriseGraphSubgraphRequest` | `GraphResponse` |
| 57 | 图谱 | `/topic/v1/profile/graph/expand` | `/internal/gkx-search/profile/graph/expand` | `EnterpriseGraphExpandRequest` | `GraphResponse` |
| 58 | 发展概况 | `/topic/v1/stats/overview/kpi` | `/internal/gkx-search/stats/overview/kpi` | `EnterpriseStatsRegionRequest` | `OverviewKpiResponse` |
| 59 | 发展概况 | `/topic/v1/stats/overview/industry-distribution` | `/internal/gkx-search/stats/overview/industry-distribution` | `EnterpriseStatsRegionRequest` | `IndustryDistResponse` |
| 60 | 发展概况 | `/topic/v1/stats/overview/trend` | `/internal/gkx-search/stats/overview/trend` | `EnterpriseStatsRegionRequest` | `TrendResponse` |
| 61 | 发展概况 | `/topic/v1/stats/overview/district-heat` | `/internal/gkx-search/stats/overview/district-heat` | `EnterpriseStatsRegionRequest` | `DistrictHeatResponse` |
| 62 | 发展概况 | `/topic/v1/stats/overview/industry-kpi` | `/internal/gkx-search/stats/overview/industry-kpi` | `EnterpriseMetaRequest` | `IndustryKpiResponse` |
| 63 | 发展概况 | `/topic/v1/stats/overview/industry-comparison` | `/internal/gkx-search/stats/overview/industry-comparison` | `EnterpriseMetaRequest` | `IndustryComparisonResponse` |
| 64 | 发展概况 | `/topic/v1/stats/overview/industry-trend` | `/internal/gkx-search/stats/overview/industry-trend` | `EnterpriseChainCodeRequest` | `IndustryTrendResponse` |
| 65 | 分布 | `/topic/v1/stats/distribution` | `/internal/gkx-search/stats/distribution` | `EnterpriseDistributionRequest` | `DistributionResponse` |
| 66 | 重点企业 | `/topic/v1/key-enterprise/kpi` | `/internal/gkx-search/key-enterprise/kpi` | `EnterpriseStatsRegionRequest` | `KeyEnterpriseKpiResponse` |
| 67 | 重点企业 | `/topic/v1/key-enterprise/chain-list` | `/internal/gkx-search/key-enterprise/chain-list` | `EnterpriseKeyChainListRequest` | `KeyChainListResponse` |
| 68 | 重点企业 | `/topic/v1/key-enterprise/chain-subject-stats` | `/internal/gkx-search/key-enterprise/chain-subject-stats` | `EnterpriseStatsRegionRequest` | `KeyChainSubjectStatsResponse` |
| 69 | 重点企业 | `/topic/v1/key-enterprise/qualification-summary` | `/internal/gkx-search/key-enterprise/qualification-summary` | `EnterpriseStatsRegionRequest` | `KeyQualificationSummaryResponse` |
| 70 | 重点企业 | `/topic/v1/key-enterprise/type-scale-stats` | `/internal/gkx-search/key-enterprise/type-scale-stats` | `EnterpriseTypeScaleRequest` | `KeyTypeScaleStatsResponse` |
| 71 | 明星企业 | `/topic/v1/star-enterprise/kpi` | `/internal/gkx-search/star-enterprise/kpi` | `EnterpriseStatsRegionRequest` | `StarEnterpriseKpiResponse` |
| 72 | 明星企业 | `/topic/v1/star-enterprise/list` | `/internal/gkx-search/star-enterprise/list` | `EnterpriseStarListRequest` | `StarEnterpriseListResponse` |
| 73 | 深圳企业 | `/topic/v1/shenzhen/kpi` | `/internal/gkx-search/shenzhen/kpi` | `EnterpriseMetaRequest` | `ShenzhenKpiResponse` |
| 74 | 深圳企业 | `/topic/v1/shenzhen/growth-trend` | `/internal/gkx-search/shenzhen/growth-trend` | `EnterpriseShenzhenTrendRequest` | `ShenzhenGrowthTrendResponse` |
| 75 | 深圳企业 | `/topic/v1/shenzhen/industry-distribution` | `/internal/gkx-search/shenzhen/industry-distribution` | `EnterpriseMetaRequest` | `ShenzhenIndustryDistResponse` |
| 76 | 深圳企业 | `/topic/v1/shenzhen/key-enterprise-list` | `/internal/gkx-search/shenzhen/key-enterprise-list` | `EnterpriseStarListRequest` | `ShenzhenKeyListResponse` |

## 4. 接口契约明细

> 返回字段表由 Java DTO **完整展开**。 中文说明：Java javadoc 优先，否则取自 Python `API-接口文档.md`。 JSON 示例含全部声明字段（值为示意）。嵌套类型见 §5。

#### 4.1 检索

##### 1. 企业复合检索

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/query`
- 服务内路径：`POST /topic/v1/search/query`
- Python 下游：`POST /internal/gkx-search/enterprises`
- 接口用途：企业复合检索。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseSearchRequest`
- 返回对象：`R<EnterpriseResponseDTOs.SearchResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `keyword` | `String` | 否 | 关键词检索文本。 对应 Python 接口中的 keyword 字段 |
| `filters` | `Map<String,Object>` | 否 | 扁平筛选条件集合。 对应 Python 接口中的 filters 字段 |
| `query_tree` | `Map<String,Object>` | 否 | 高级筛选查询树。 对应 Python 接口中的 query_tree 字段 |
| `sort_field` | `String` | 否 | 排序字段名。 对应 Python 接口中的 sort_field 字段 |
| `sort_order` | `String` | 否 | 排序方向。 允许值通常为 asc 或 desc，对应 Python 接口中的 sort_order 字段 |
| `page` | `Integer` | 否 | 当前查询页码 |
| `size` | `Integer` | 否 | 每页返回条数 |

请求 JSON 示例：

```json
{
  "keyword": "",
  "filters": {},
  "query_tree": {},
  "sort_field": "",
  "sort_order": "",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<SearchItem>` | 当前页企业列表 |
| `data.list[].org_id` | `String` | 企业唯一标识 |
| `data.list[].social_credit_code` | `String` | 统一社会信用代码 |
| `data.list[].name_cn` | `String` | 企业中文名称 |
| `data.list[].former_names` | `List<String>` | 曾用名列表 |
| `data.list[].lerep` | `String` | 法定代表人 |
| `data.list[].province` | `String` | 所在省份 |
| `data.list[].city` | `String` | 所在城市 |
| `data.list[].district` | `String` | 所在区县 |
| `data.list[].industry_class` | `String` | 行业分类编码 |
| `data.list[].industry_class_name` | `String` | 行业分类名称 |
| `data.list[].incorporation_year` | `Integer` | 成立年份 |
| `data.list[].incorporation_date` | `String` | 成立日期 |
| `data.list[].listing_status` | `String` | 上市状态 |
| `data.list[].registered_capital_value` | `BigDecimal` | 注册资本 |
| `data.list[].tags_flat` | `List<String>` | 标签编码平铺列表 |
| `data.list[].industry_chain_names_flat` | `List<String>` | 产业链名称平铺列表 |
| `data.list[].enterprise_scale` | `String` | 企业规模 |
| `data.list[].competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.list[].risk_level` | `String` | 风险等级 |
| `data.list[].operating_status` | `String` | 经营状态 |
| `data.list[].chain_position_text` | `String` | 产业链位置描述 |
| `data.list[].main_prod` | `String` | 主要产品 |
| `data.list[].logo_url` | `String` | 企业 Logo 地址 |
| `data.list[].company_type` | `String` | 企业类型 |
| `data.list[].region_id` | `String` | 区域编码 |
| `data.list[].tech_score` | `BigDecimal` | 技术力得分 |
| `data.list[].business_score` | `BigDecimal` | 商业力得分 |
| `data.list[].high_value_patent_count` | `Integer` | 高价值专利数量 |
| `data.list[].revenue_growth_rate` | `BigDecimal` | 营收增长率 |
| `data.list[].profit_margin` | `BigDecimal` | 利润率 |
| `data.list[].supply_chain_role` | `String` | 供应链角色 |
| `data.list[].core_tech_tags_flat` | `List<String>` | 核心技术标签编码列表 |
| `data.list[].statistics` | `List<Statistics>` | 统计指标列表 |
| `data.list[].statistics[].patent_total` | `Integer` | 专利总数 |
| `data.list[].statistics[].patent_valid` | `Integer` | 有效专利数量 |
| `data.list[].statistics[].patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `data.list[].statistics[].latest_revenue` | `BigDecimal` | 最新营收金额 |
| `data.list[].statistics[].financing_count` | `Integer` | 融资事件数量 |
| `data.list[].statistics[].bid_total` | `Integer` | 招投标数量 |
| `data.list[].statistics[].news_count` | `Integer` | 资讯数量 |
| `data.list[].statistics[].trademark_total` | `Integer` | 商标数量 |
| `data.list[].statistics[].software_copyright_total` | `Integer` | 软件著作权数量 |
| `data.list[].statistics[].rd_ratio` | `BigDecimal` | 研发投入占比 |
| `data.total` | `Long` | 命中企业总数 |
| `data.page` | `Integer` | 当前页码 |
| `data.size` | `Integer` | 每页返回条数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "social_credit_code": "",
        "name_cn": "",
        "former_names": [
          ""
        ],
        "lerep": "",
        "province": "",
        "city": "",
        "district": "",
        "industry_class": "",
        "industry_class_name": "",
        "incorporation_year": 2024,
        "incorporation_date": "2024-01-01",
        "listing_status": "",
        "registered_capital_value": 0.0,
        "tags_flat": [
          ""
        ],
        "industry_chain_names_flat": [
          ""
        ],
        "enterprise_scale": "",
        "competitiveness_score": 0.0,
        "risk_level": "低",
        "operating_status": "",
        "chain_position_text": "",
        "main_prod": "",
        "logo_url": "",
        "company_type": "",
        "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "tech_score": 0.0,
        "business_score": 0.0,
        "high_value_patent_count": 0,
        "revenue_growth_rate": 0.0,
        "profit_margin": 0.0,
        "supply_chain_role": "",
        "core_tech_tags_flat": [
          ""
        ],
        "statistics": [
          {
            "patent_total": 0,
            "patent_valid": 0,
            "patent_valid_count": 0,
            "latest_revenue": 0.0,
            "financing_count": 0,
            "bid_total": 0,
            "news_count": 0,
            "trademark_total": 0,
            "software_copyright_total": 0,
            "rd_ratio": 0.0
          }
        ]
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20
  },
  "ok": true
}
```

##### 2. 企业输入联想

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/suggest`
- 服务内路径：`POST /topic/v1/search/suggest`
- Python 下游：`POST /internal/gkx-search/enterprises/suggest`
- 接口用途：企业名称输入联想。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseSuggestRequest`
- 返回对象：`R<List<SuggestItem>>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `prefix` | `String` | 是 | 输入联想前缀字符串 |
| `size` | `Integer` | 否 | 期望返回的候选数量 |

请求 JSON 示例：

```json
{
  "prefix": "",
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data` | `List<SuggestItem>` | 联想候选数组（data 根即为数组） |
| `data[].org_id` | `String` | 企业唯一标识 |
| `data[].name_cn` | `String` | 企业中文名称 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": [
    {
      "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
      "name_cn": ""
    }
  ],
  "ok": true
}
```

##### 3. 企业高级筛选

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/advanced`
- 服务内路径：`POST /topic/v1/search/advanced`
- Python 下游：`POST /internal/gkx-search/enterprises/advanced`
- 接口用途：基于 query_tree 的高级筛选。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseSearchRequest`
- 返回对象：`R<EnterpriseResponseDTOs.SearchResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `keyword` | `String` | 否 | 关键词检索文本。 对应 Python 接口中的 keyword 字段 |
| `filters` | `Map<String,Object>` | 否 | 扁平筛选条件集合。 对应 Python 接口中的 filters 字段 |
| `query_tree` | `Map<String,Object>` | 否 | 高级筛选查询树。 对应 Python 接口中的 query_tree 字段 |
| `sort_field` | `String` | 否 | 排序字段名。 对应 Python 接口中的 sort_field 字段 |
| `sort_order` | `String` | 否 | 排序方向。 允许值通常为 asc 或 desc，对应 Python 接口中的 sort_order 字段 |
| `page` | `Integer` | 否 | 当前查询页码 |
| `size` | `Integer` | 否 | 每页返回条数 |

请求 JSON 示例：

```json
{
  "keyword": "",
  "filters": {},
  "query_tree": {},
  "sort_field": "",
  "sort_order": "",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<SearchItem>` | 当前页企业列表 |
| `data.list[].org_id` | `String` | 企业唯一标识 |
| `data.list[].social_credit_code` | `String` | 统一社会信用代码 |
| `data.list[].name_cn` | `String` | 企业中文名称 |
| `data.list[].former_names` | `List<String>` | 曾用名列表 |
| `data.list[].lerep` | `String` | 法定代表人 |
| `data.list[].province` | `String` | 所在省份 |
| `data.list[].city` | `String` | 所在城市 |
| `data.list[].district` | `String` | 所在区县 |
| `data.list[].industry_class` | `String` | 行业分类编码 |
| `data.list[].industry_class_name` | `String` | 行业分类名称 |
| `data.list[].incorporation_year` | `Integer` | 成立年份 |
| `data.list[].incorporation_date` | `String` | 成立日期 |
| `data.list[].listing_status` | `String` | 上市状态 |
| `data.list[].registered_capital_value` | `BigDecimal` | 注册资本 |
| `data.list[].tags_flat` | `List<String>` | 标签编码平铺列表 |
| `data.list[].industry_chain_names_flat` | `List<String>` | 产业链名称平铺列表 |
| `data.list[].enterprise_scale` | `String` | 企业规模 |
| `data.list[].competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.list[].risk_level` | `String` | 风险等级 |
| `data.list[].operating_status` | `String` | 经营状态 |
| `data.list[].chain_position_text` | `String` | 产业链位置描述 |
| `data.list[].main_prod` | `String` | 主要产品 |
| `data.list[].logo_url` | `String` | 企业 Logo 地址 |
| `data.list[].company_type` | `String` | 企业类型 |
| `data.list[].region_id` | `String` | 区域编码 |
| `data.list[].tech_score` | `BigDecimal` | 技术力得分 |
| `data.list[].business_score` | `BigDecimal` | 商业力得分 |
| `data.list[].high_value_patent_count` | `Integer` | 高价值专利数量 |
| `data.list[].revenue_growth_rate` | `BigDecimal` | 营收增长率 |
| `data.list[].profit_margin` | `BigDecimal` | 利润率 |
| `data.list[].supply_chain_role` | `String` | 供应链角色 |
| `data.list[].core_tech_tags_flat` | `List<String>` | 核心技术标签编码列表 |
| `data.list[].statistics` | `List<Statistics>` | 统计指标列表 |
| `data.list[].statistics[].patent_total` | `Integer` | 专利总数 |
| `data.list[].statistics[].patent_valid` | `Integer` | 有效专利数量 |
| `data.list[].statistics[].patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `data.list[].statistics[].latest_revenue` | `BigDecimal` | 最新营收金额 |
| `data.list[].statistics[].financing_count` | `Integer` | 融资事件数量 |
| `data.list[].statistics[].bid_total` | `Integer` | 招投标数量 |
| `data.list[].statistics[].news_count` | `Integer` | 资讯数量 |
| `data.list[].statistics[].trademark_total` | `Integer` | 商标数量 |
| `data.list[].statistics[].software_copyright_total` | `Integer` | 软件著作权数量 |
| `data.list[].statistics[].rd_ratio` | `BigDecimal` | 研发投入占比 |
| `data.total` | `Long` | 命中企业总数 |
| `data.page` | `Integer` | 当前页码 |
| `data.size` | `Integer` | 每页返回条数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "social_credit_code": "",
        "name_cn": "",
        "former_names": [
          ""
        ],
        "lerep": "",
        "province": "",
        "city": "",
        "district": "",
        "industry_class": "",
        "industry_class_name": "",
        "incorporation_year": 2024,
        "incorporation_date": "2024-01-01",
        "listing_status": "",
        "registered_capital_value": 0.0,
        "tags_flat": [
          ""
        ],
        "industry_chain_names_flat": [
          ""
        ],
        "enterprise_scale": "",
        "competitiveness_score": 0.0,
        "risk_level": "低",
        "operating_status": "",
        "chain_position_text": "",
        "main_prod": "",
        "logo_url": "",
        "company_type": "",
        "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "tech_score": 0.0,
        "business_score": 0.0,
        "high_value_patent_count": 0,
        "revenue_growth_rate": 0.0,
        "profit_margin": 0.0,
        "supply_chain_role": "",
        "core_tech_tags_flat": [
          ""
        ],
        "statistics": [
          {
            "patent_total": 0,
            "patent_valid": 0,
            "patent_valid_count": 0,
            "latest_revenue": 0.0,
            "financing_count": 0,
            "bid_total": 0,
            "news_count": 0,
            "trademark_total": 0,
            "software_copyright_total": 0,
            "rd_ratio": 0.0
          }
        ]
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20
  },
  "ok": true
}
```

##### 4. 推荐企业

- 接口路径：`POST gateway地址/enterprise/topic/v1/recommend`
- 服务内路径：`POST /topic/v1/recommend`
- Python 下游：`POST /internal/gkx-search/enterprises/recommend`
- 接口用途：推荐企业列表。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseRecommendRequest`
- 返回对象：`R<EnterpriseResponseDTOs.RecommendResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `count` | `Integer` | 否 | 期望返回的推荐企业数量。 <p> Python 侧默认值为 4；小于 1 时回落为 4，大于 10 时截断为 10 |

请求 JSON 示例：

```json
{
  "count": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<SearchItem>` | 推荐企业列表。 列表项结构与检索列表项 {@link SearchItem} 一致 |
| `data.items[].org_id` | `String` | 企业唯一标识 |
| `data.items[].social_credit_code` | `String` | 统一社会信用代码 |
| `data.items[].name_cn` | `String` | 企业中文名称 |
| `data.items[].former_names` | `List<String>` | 曾用名列表 |
| `data.items[].lerep` | `String` | 法定代表人 |
| `data.items[].province` | `String` | 所在省份 |
| `data.items[].city` | `String` | 所在城市 |
| `data.items[].district` | `String` | 所在区县 |
| `data.items[].industry_class` | `String` | 行业分类编码 |
| `data.items[].industry_class_name` | `String` | 行业分类名称 |
| `data.items[].incorporation_year` | `Integer` | 成立年份 |
| `data.items[].incorporation_date` | `String` | 成立日期 |
| `data.items[].listing_status` | `String` | 上市状态 |
| `data.items[].registered_capital_value` | `BigDecimal` | 注册资本 |
| `data.items[].tags_flat` | `List<String>` | 标签编码平铺列表 |
| `data.items[].industry_chain_names_flat` | `List<String>` | 产业链名称平铺列表 |
| `data.items[].enterprise_scale` | `String` | 企业规模 |
| `data.items[].competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.items[].risk_level` | `String` | 风险等级 |
| `data.items[].operating_status` | `String` | 经营状态 |
| `data.items[].chain_position_text` | `String` | 产业链位置描述 |
| `data.items[].main_prod` | `String` | 主要产品 |
| `data.items[].logo_url` | `String` | 企业 Logo 地址 |
| `data.items[].company_type` | `String` | 企业类型 |
| `data.items[].region_id` | `String` | 区域编码 |
| `data.items[].tech_score` | `BigDecimal` | 技术力得分 |
| `data.items[].business_score` | `BigDecimal` | 商业力得分 |
| `data.items[].high_value_patent_count` | `Integer` | 高价值专利数量 |
| `data.items[].revenue_growth_rate` | `BigDecimal` | 营收增长率 |
| `data.items[].profit_margin` | `BigDecimal` | 利润率 |
| `data.items[].supply_chain_role` | `String` | 供应链角色 |
| `data.items[].core_tech_tags_flat` | `List<String>` | 核心技术标签编码列表 |
| `data.items[].statistics` | `List<Statistics>` | 统计指标列表 |
| `data.items[].statistics[].patent_total` | `Integer` | 专利总数 |
| `data.items[].statistics[].patent_valid` | `Integer` | 有效专利数量 |
| `data.items[].statistics[].patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `data.items[].statistics[].latest_revenue` | `BigDecimal` | 最新营收金额 |
| `data.items[].statistics[].financing_count` | `Integer` | 融资事件数量 |
| `data.items[].statistics[].bid_total` | `Integer` | 招投标数量 |
| `data.items[].statistics[].news_count` | `Integer` | 资讯数量 |
| `data.items[].statistics[].trademark_total` | `Integer` | 商标数量 |
| `data.items[].statistics[].software_copyright_total` | `Integer` | 软件著作权数量 |
| `data.items[].statistics[].rd_ratio` | `BigDecimal` | 研发投入占比 |
| `data.total` | `Long` | 本次实际返回的推荐企业数量 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "social_credit_code": "",
        "name_cn": "",
        "former_names": [
          ""
        ],
        "lerep": "",
        "province": "",
        "city": "",
        "district": "",
        "industry_class": "",
        "industry_class_name": "",
        "incorporation_year": 2024,
        "incorporation_date": "2024-01-01",
        "listing_status": "",
        "registered_capital_value": 0.0,
        "tags_flat": [
          ""
        ],
        "industry_chain_names_flat": [
          ""
        ],
        "enterprise_scale": "",
        "competitiveness_score": 0.0,
        "risk_level": "低",
        "operating_status": "",
        "chain_position_text": "",
        "main_prod": "",
        "logo_url": "",
        "company_type": "",
        "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "tech_score": 0.0,
        "business_score": 0.0,
        "high_value_patent_count": 0,
        "revenue_growth_rate": 0.0,
        "profit_margin": 0.0,
        "supply_chain_role": "",
        "core_tech_tags_flat": [
          ""
        ],
        "statistics": [
          {
            "patent_total": 0,
            "patent_valid": 0,
            "patent_valid_count": 0,
            "latest_revenue": 0.0,
            "financing_count": 0,
            "bid_total": 0,
            "news_count": 0,
            "trademark_total": 0,
            "software_copyright_total": 0,
            "rd_ratio": 0.0
          }
        ]
      }
    ],
    "total": 0
  },
  "ok": true
}
```

#### 4.2 检索辅助

##### 5. facets 聚合

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/aggregations`
- 服务内路径：`POST /topic/v1/search/aggregations`
- Python 下游：`POST /internal/gkx-search/enterprises/aggregations`
- 接口用途：facets 聚合。
- Controller：`EnterpriseSearchAuxController`
- 请求对象：`EnterpriseAggregationRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.AggregationResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `field` | `String` | 是 | 聚合字段名。 可选：industry_class_name / province / city / listing_status / enterprise_scale / risk_level / tags_flat / industry_chain_names_flat / incorporation_year |

请求 JSON 示例：

```json
{
  "field": ""
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.field` | `String` | 聚合字段，见可选值 |
| `data.buckets` | `List<BucketItem>` | 聚合桶列表 |
| `data.buckets[].key` | `String` | 聚合键值 |
| `data.buckets[].doc_count` | `Long` | 文档数（企业数） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "field": "",
    "buckets": [
      {
        "key": "",
        "doc_count": 0
      }
    ]
  },
  "ok": true
}
```

##### 6. 按编码批量查询

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/by-codes`
- 服务内路径：`POST /topic/v1/search/by-codes`
- Python 下游：`POST /internal/gkx-search/enterprises/by-codes`
- 接口用途：按编码批量查企业。
- Controller：`EnterpriseSearchAuxController`
- 请求对象：`EnterpriseByCodesRequest`
- 返回对象：`R<EnterpriseResponseDTOs.SearchResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `codes` | `List<String>` | 是 | 统一社会信用代码列表 |

请求 JSON 示例：

```json
{
  "codes": [
    ""
  ]
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<SearchItem>` | 当前页企业列表 |
| `data.list[].org_id` | `String` | 企业唯一标识 |
| `data.list[].social_credit_code` | `String` | 统一社会信用代码 |
| `data.list[].name_cn` | `String` | 企业中文名称 |
| `data.list[].former_names` | `List<String>` | 曾用名列表 |
| `data.list[].lerep` | `String` | 法定代表人 |
| `data.list[].province` | `String` | 所在省份 |
| `data.list[].city` | `String` | 所在城市 |
| `data.list[].district` | `String` | 所在区县 |
| `data.list[].industry_class` | `String` | 行业分类编码 |
| `data.list[].industry_class_name` | `String` | 行业分类名称 |
| `data.list[].incorporation_year` | `Integer` | 成立年份 |
| `data.list[].incorporation_date` | `String` | 成立日期 |
| `data.list[].listing_status` | `String` | 上市状态 |
| `data.list[].registered_capital_value` | `BigDecimal` | 注册资本 |
| `data.list[].tags_flat` | `List<String>` | 标签编码平铺列表 |
| `data.list[].industry_chain_names_flat` | `List<String>` | 产业链名称平铺列表 |
| `data.list[].enterprise_scale` | `String` | 企业规模 |
| `data.list[].competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.list[].risk_level` | `String` | 风险等级 |
| `data.list[].operating_status` | `String` | 经营状态 |
| `data.list[].chain_position_text` | `String` | 产业链位置描述 |
| `data.list[].main_prod` | `String` | 主要产品 |
| `data.list[].logo_url` | `String` | 企业 Logo 地址 |
| `data.list[].company_type` | `String` | 企业类型 |
| `data.list[].region_id` | `String` | 区域编码 |
| `data.list[].tech_score` | `BigDecimal` | 技术力得分 |
| `data.list[].business_score` | `BigDecimal` | 商业力得分 |
| `data.list[].high_value_patent_count` | `Integer` | 高价值专利数量 |
| `data.list[].revenue_growth_rate` | `BigDecimal` | 营收增长率 |
| `data.list[].profit_margin` | `BigDecimal` | 利润率 |
| `data.list[].supply_chain_role` | `String` | 供应链角色 |
| `data.list[].core_tech_tags_flat` | `List<String>` | 核心技术标签编码列表 |
| `data.list[].statistics` | `List<Statistics>` | 统计指标列表 |
| `data.list[].statistics[].patent_total` | `Integer` | 专利总数 |
| `data.list[].statistics[].patent_valid` | `Integer` | 有效专利数量 |
| `data.list[].statistics[].patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `data.list[].statistics[].latest_revenue` | `BigDecimal` | 最新营收金额 |
| `data.list[].statistics[].financing_count` | `Integer` | 融资事件数量 |
| `data.list[].statistics[].bid_total` | `Integer` | 招投标数量 |
| `data.list[].statistics[].news_count` | `Integer` | 资讯数量 |
| `data.list[].statistics[].trademark_total` | `Integer` | 商标数量 |
| `data.list[].statistics[].software_copyright_total` | `Integer` | 软件著作权数量 |
| `data.list[].statistics[].rd_ratio` | `BigDecimal` | 研发投入占比 |
| `data.total` | `Long` | 命中企业总数 |
| `data.page` | `Integer` | 当前页码 |
| `data.size` | `Integer` | 每页返回条数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "social_credit_code": "",
        "name_cn": "",
        "former_names": [
          ""
        ],
        "lerep": "",
        "province": "",
        "city": "",
        "district": "",
        "industry_class": "",
        "industry_class_name": "",
        "incorporation_year": 2024,
        "incorporation_date": "2024-01-01",
        "listing_status": "",
        "registered_capital_value": 0.0,
        "tags_flat": [
          ""
        ],
        "industry_chain_names_flat": [
          ""
        ],
        "enterprise_scale": "",
        "competitiveness_score": 0.0,
        "risk_level": "低",
        "operating_status": "",
        "chain_position_text": "",
        "main_prod": "",
        "logo_url": "",
        "company_type": "",
        "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "tech_score": 0.0,
        "business_score": 0.0,
        "high_value_patent_count": 0,
        "revenue_growth_rate": 0.0,
        "profit_margin": 0.0,
        "supply_chain_role": "",
        "core_tech_tags_flat": [
          ""
        ],
        "statistics": [
          {
            "patent_total": 0,
            "patent_valid": 0,
            "patent_valid_count": 0,
            "latest_revenue": 0.0,
            "financing_count": 0,
            "bid_total": 0,
            "news_count": 0,
            "trademark_total": 0,
            "software_copyright_total": 0,
            "rd_ratio": 0.0
          }
        ]
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20
  },
  "ok": true
}
```

##### 7. 热门搜索词

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/hot`
- 服务内路径：`POST /topic/v1/search/hot`
- Python 下游：`POST /internal/gkx-search/enterprises/hot`
- 接口用途：热门搜索词。
- Controller：`EnterpriseSearchAuxController`
- 请求对象：`EnterpriseHotRequest`
- 返回对象：`R<List<HotKeywordItem>>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `size` | `Integer` | 否 | 返回条数；Python 默认 10，最大 20 |

请求 JSON 示例：

```json
{
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data` | `List<HotKeywordItem>` | 热词数组（data 根即为数组） |
| `data[].keyword` | `String` | 关键词（企业名/曾用名/经营范围/主要产品 + 统一社会信用代码精确/前缀匹配） |
| `data[].count` | `Long` | 返回数量，默认 4，最大 10 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": [
    {
      "keyword": "",
      "count": 0
    }
  ],
  "ok": true
}
```

##### 8. 智能搜索

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/smart`
- 服务内路径：`POST /topic/v1/search/smart`
- Python 下游：`POST /internal/gkx-search/enterprises/smart`
- 接口用途：多关键词智能搜索。
- Controller：`EnterpriseSearchAuxController`
- 请求对象：`EnterpriseSmartSearchRequest`
- 返回对象：`R<EnterpriseResponseDTOs.SearchResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `keywords` | `List<String>` | 否 | 关键词数组；多关键词按 AND 匹配 |
| `keyword` | `String` | 否 | 兼容旧版单关键词字符串 |
| `q` | `String` | 否 | 兼容查询别名 |
| `page` | `Integer` | 否 | 当前页码 |
| `size` | `Integer` | 否 | 每页条数 |
| `page_size` | `Integer` | 否 | 每页条数别名 |
| `sort_field` | `String` | 否 | 排序字段 |
| `sort_order` | `String` | 否 | 排序方向 |

请求 JSON 示例：

```json
{
  "keywords": [
    ""
  ],
  "keyword": "",
  "q": "",
  "page": 1,
  "size": 20,
  "page_size": 1,
  "sort_field": "",
  "sort_order": ""
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<SearchItem>` | 当前页企业列表 |
| `data.list[].org_id` | `String` | 企业唯一标识 |
| `data.list[].social_credit_code` | `String` | 统一社会信用代码 |
| `data.list[].name_cn` | `String` | 企业中文名称 |
| `data.list[].former_names` | `List<String>` | 曾用名列表 |
| `data.list[].lerep` | `String` | 法定代表人 |
| `data.list[].province` | `String` | 所在省份 |
| `data.list[].city` | `String` | 所在城市 |
| `data.list[].district` | `String` | 所在区县 |
| `data.list[].industry_class` | `String` | 行业分类编码 |
| `data.list[].industry_class_name` | `String` | 行业分类名称 |
| `data.list[].incorporation_year` | `Integer` | 成立年份 |
| `data.list[].incorporation_date` | `String` | 成立日期 |
| `data.list[].listing_status` | `String` | 上市状态 |
| `data.list[].registered_capital_value` | `BigDecimal` | 注册资本 |
| `data.list[].tags_flat` | `List<String>` | 标签编码平铺列表 |
| `data.list[].industry_chain_names_flat` | `List<String>` | 产业链名称平铺列表 |
| `data.list[].enterprise_scale` | `String` | 企业规模 |
| `data.list[].competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.list[].risk_level` | `String` | 风险等级 |
| `data.list[].operating_status` | `String` | 经营状态 |
| `data.list[].chain_position_text` | `String` | 产业链位置描述 |
| `data.list[].main_prod` | `String` | 主要产品 |
| `data.list[].logo_url` | `String` | 企业 Logo 地址 |
| `data.list[].company_type` | `String` | 企业类型 |
| `data.list[].region_id` | `String` | 区域编码 |
| `data.list[].tech_score` | `BigDecimal` | 技术力得分 |
| `data.list[].business_score` | `BigDecimal` | 商业力得分 |
| `data.list[].high_value_patent_count` | `Integer` | 高价值专利数量 |
| `data.list[].revenue_growth_rate` | `BigDecimal` | 营收增长率 |
| `data.list[].profit_margin` | `BigDecimal` | 利润率 |
| `data.list[].supply_chain_role` | `String` | 供应链角色 |
| `data.list[].core_tech_tags_flat` | `List<String>` | 核心技术标签编码列表 |
| `data.list[].statistics` | `List<Statistics>` | 统计指标列表 |
| `data.list[].statistics[].patent_total` | `Integer` | 专利总数 |
| `data.list[].statistics[].patent_valid` | `Integer` | 有效专利数量 |
| `data.list[].statistics[].patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `data.list[].statistics[].latest_revenue` | `BigDecimal` | 最新营收金额 |
| `data.list[].statistics[].financing_count` | `Integer` | 融资事件数量 |
| `data.list[].statistics[].bid_total` | `Integer` | 招投标数量 |
| `data.list[].statistics[].news_count` | `Integer` | 资讯数量 |
| `data.list[].statistics[].trademark_total` | `Integer` | 商标数量 |
| `data.list[].statistics[].software_copyright_total` | `Integer` | 软件著作权数量 |
| `data.list[].statistics[].rd_ratio` | `BigDecimal` | 研发投入占比 |
| `data.total` | `Long` | 命中企业总数 |
| `data.page` | `Integer` | 当前页码 |
| `data.size` | `Integer` | 每页返回条数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "social_credit_code": "",
        "name_cn": "",
        "former_names": [
          ""
        ],
        "lerep": "",
        "province": "",
        "city": "",
        "district": "",
        "industry_class": "",
        "industry_class_name": "",
        "incorporation_year": 2024,
        "incorporation_date": "2024-01-01",
        "listing_status": "",
        "registered_capital_value": 0.0,
        "tags_flat": [
          ""
        ],
        "industry_chain_names_flat": [
          ""
        ],
        "enterprise_scale": "",
        "competitiveness_score": 0.0,
        "risk_level": "低",
        "operating_status": "",
        "chain_position_text": "",
        "main_prod": "",
        "logo_url": "",
        "company_type": "",
        "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "tech_score": 0.0,
        "business_score": 0.0,
        "high_value_patent_count": 0,
        "revenue_growth_rate": 0.0,
        "profit_margin": 0.0,
        "supply_chain_role": "",
        "core_tech_tags_flat": [
          ""
        ],
        "statistics": [
          {
            "patent_total": 0,
            "patent_valid": 0,
            "patent_valid_count": 0,
            "latest_revenue": 0.0,
            "financing_count": 0,
            "bid_total": 0,
            "news_count": 0,
            "trademark_total": 0,
            "software_copyright_total": 0,
            "rd_ratio": 0.0
          }
        ]
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20
  },
  "ok": true
}
```

#### 4.3 元数据

##### 9. 筛选项字典

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/filters`
- 服务内路径：`POST /topic/v1/search/meta/filters`
- Python 下游：`POST /internal/gkx-search/meta/filters`
- 接口用途：筛选项字典。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseResponseDTOs.FiltersResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source` | `String` | 否 | 数据源：`nebula` / `mock` |

请求 JSON 示例：

```json
{
  "source": "mock"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.industries` | `List<String>` | 行业分类列表 |
| `data.provinces` | `List<String>` | 省份列表 |
| `data.cities` | `List<String>` | 城市列表 |
| `data.listing_statuses` | `List<String>` | 上市状态枚举列表 |
| `data.operating_statuses` | `List<String>` | 经营状态枚举列表 |
| `data.enterprise_scales` | `List<String>` | 企业规模枚举列表 |
| `data.risk_levels` | `List<String>` | 风险等级枚举列表 |
| `data.tags` | `List<String>` | 标签编码列表 |
| `data.industry_chains` | `List<String>` | 产业链名称列表 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "industries": [
      ""
    ],
    "provinces": [
      ""
    ],
    "cities": [
      ""
    ],
    "listing_statuses": [
      ""
    ],
    "operating_statuses": [
      ""
    ],
    "enterprise_scales": [
      ""
    ],
    "risk_levels": [
      ""
    ],
    "tags": [
      ""
    ],
    "industry_chains": [
      ""
    ]
  },
  "ok": true
}
```

##### 10. 地区字典

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/regions`
- 服务内路径：`POST /topic/v1/search/meta/regions`
- Python 下游：`POST /internal/gkx-search/meta/regions`
- 接口用途：地区字典。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseRegionRequest`
- 返回对象：`R<EnterpriseResponseDTOs.RegionsResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `parent_code` | `String` | 否 | 父级地区编码。 对应 Python 接口中的 parent_code 字段 |

请求 JSON 示例：

```json
{
  "parent_code": ""
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<RegionItem>` | 地区条目列表 |
| `data.items[].code` | `String` | 地区编码 |
| `data.items[].name` | `String` | 地区名称 |
| `data.items[].level` | `String` | 行政层级 |
| `data.items[].fulltitle` | `String` | 完整地区名称 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "code": "",
        "name": "",
        "level": "",
        "fulltitle": ""
      }
    ]
  },
  "ok": true
}
```

##### 11. 企业类型字典

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/company-types`
- 服务内路径：`POST /topic/v1/search/meta/company-types`
- Python 下游：`POST /internal/gkx-search/meta/company-types`
- 接口用途：企业类型字典。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseResponseDTOs.OptionsResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source` | `String` | 否 | 数据源：`nebula` / `mock` |

请求 JSON 示例：

```json
{
  "source": "mock"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<CodeNameItem>` | 枚举条目列表 |
| `data.items[].code` | `String` | 枚举编码 |
| `data.items[].name` | `String` | 枚举名称 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "code": "",
        "name": ""
      }
    ]
  },
  "ok": true
}
```

##### 12. 企业规模字典

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/enterprise-scales`
- 服务内路径：`POST /topic/v1/search/meta/enterprise-scales`
- Python 下游：`POST /internal/gkx-search/meta/enterprise-scales`
- 接口用途：企业规模字典。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseResponseDTOs.OptionsResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source` | `String` | 否 | 数据源：`nebula` / `mock` |

请求 JSON 示例：

```json
{
  "source": "mock"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<CodeNameItem>` | 枚举条目列表 |
| `data.items[].code` | `String` | 枚举编码 |
| `data.items[].name` | `String` | 枚举名称 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "code": "",
        "name": ""
      }
    ]
  },
  "ok": true
}
```

##### 13. 标签字典

- 接口路径：`POST gateway地址/enterprise/topic/v1/search/meta/tags`
- 服务内路径：`POST /topic/v1/search/meta/tags`
- Python 下游：`POST /internal/gkx-search/meta/tags`
- 接口用途：标签字典。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseTagRequest`
- 返回对象：`R<EnterpriseResponseDTOs.TagDictionaryResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `category` | `String` | 否 | 标签分类编码。 例如 qualification、honor 等业务分类 |

请求 JSON 示例：

```json
{
  "category": ""
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<TagItem>` | 标签字典条目列表 |
| `data.items[].tag_code` | `String` | 标签编码 |
| `data.items[].tag_value` | `String` | 标签展示值 |
| `data.items[].tag_name` | `String` | 标签名称 |
| `data.items[].tag_category` | `String` | 标签分类 |
| `data.items[].tag_level` | `String` | 标签层级。 对齐 DWD tag_dict.tag_level：national / province / city / district 等字符串；可为空 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "tag_code": "",
        "tag_value": "",
        "tag_name": "",
        "tag_category": "",
        "tag_level": ""
      }
    ]
  },
  "ok": true
}
```

#### 4.4 对比篮

##### 14. 企业对比

- 接口路径：`POST gateway地址/enterprise/topic/v1/compare-basket/compare`
- 服务内路径：`POST /topic/v1/compare-basket/compare`
- Python 下游：`POST /internal/gkx-search/enterprises/compare`
- 接口用途：多企业对比。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseCompareRequest`
- 返回对象：`R<EnterpriseResponseDTOs.CompareResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_ids` | `List<String>` | 是 | 参与对比的企业主键列表。 对应 Python 接口中的 org_ids 字段 |

请求 JSON 示例：

```json
{
  "org_ids": [
    ""
  ]
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<CompareItem>` | 参与对比的企业列表 |
| `data.items[].org_id` | `String` | 企业唯一标识 |
| `data.items[].social_credit_code` | `String` | 统一社会信用代码 |
| `data.items[].name_cn` | `String` | 企业中文名称 |
| `data.items[].lerep` | `String` | 法定代表人 |
| `data.items[].province` | `String` | 所在省份 |
| `data.items[].city` | `String` | 所在城市 |
| `data.items[].incorporation_year` | `Integer` | 成立年份 |
| `data.items[].incorporation_date` | `String` | 成立日期 |
| `data.items[].registered_capital_value` | `BigDecimal` | 注册资本 |
| `data.items[].capital_currency_code` | `String` | 资本币种或金额单位 |
| `data.items[].listing_status` | `String` | 上市状态 |
| `data.items[].stock_code` | `String` | 股票代码 |
| `data.items[].stock_type` | `String` | 股票类别 |
| `data.items[].listed_date` | `String` | 上市或挂牌日期 |
| `data.items[].industry_class` | `String` | 行业分类编码 |
| `data.items[].industry_class_name` | `String` | 行业分类名称 |
| `data.items[].main_activities` | `String` | 主营业务描述 |
| `data.items[].enterprise_scale` | `String` | 企业规模 |
| `data.items[].operating_status` | `String` | 经营状态 |
| `data.items[].competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.items[].chain_position_text` | `String` | 产业链位置描述 |
| `data.items[].risk_level` | `String` | 风险等级 |
| `data.items[].tags` | `List<TagItem>` | 标签明细列表 |
| `data.items[].tags[].tag_code` | `String` | 标签编码 |
| `data.items[].tags[].tag_value` | `String` | 标签展示值 |
| `data.items[].tags[].tag_name` | `String` | 标签名称 |
| `data.items[].tags[].tag_category` | `String` | 标签分类 |
| `data.items[].tags[].tag_level` | `String` | 标签层级。 对齐 DWD tag_dict.tag_level：national / province / city / district 等字符串；可为空 |
| `data.items[].tags_flat` | `List<String>` | 标签编码平铺列表 |
| `data.items[].industry_chain_names_flat` | `List<String>` | 产业链名称平铺列表 |
| `data.items[].financials` | `List<FinancialRecord>` | 财务历史列表 |
| `data.items[].financials[].year` | `Integer` | 财务年份 |
| `data.items[].financials[].main_business_revenue` | `BigDecimal` | 主营业务收入 |
| `data.items[].financials[].operating_revenue` | `BigDecimal` | 营业收入 |
| `data.items[].financials[].net_profit` | `BigDecimal` | 净利润 |
| `data.items[].financials[].rd_expense` | `BigDecimal` | 研发投入金额 |
| `data.items[].financials[].rd_ratio` | `BigDecimal` | 研发投入占比 |
| `data.items[].statistics` | `List<Statistics>` | 统计指标列表 |
| `data.items[].statistics[].patent_total` | `Integer` | 专利总数 |
| `data.items[].statistics[].patent_valid` | `Integer` | 有效专利数量 |
| `data.items[].statistics[].patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `data.items[].statistics[].latest_revenue` | `BigDecimal` | 最新营收金额 |
| `data.items[].statistics[].financing_count` | `Integer` | 融资事件数量 |
| `data.items[].statistics[].bid_total` | `Integer` | 招投标数量 |
| `data.items[].statistics[].news_count` | `Integer` | 资讯数量 |
| `data.items[].statistics[].trademark_total` | `Integer` | 商标数量 |
| `data.items[].statistics[].software_copyright_total` | `Integer` | 软件著作权数量 |
| `data.items[].statistics[].rd_ratio` | `BigDecimal` | 研发投入占比 |
| `data.total` | `Integer` | 对比企业总数 |
| `data.fields` | `List<String>` | 前端用于渲染对比表的字段清单 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "social_credit_code": "",
        "name_cn": "",
        "lerep": "",
        "province": "",
        "city": "",
        "incorporation_year": 2024,
        "incorporation_date": "2024-01-01",
        "registered_capital_value": 0.0,
        "capital_currency_code": "",
        "listing_status": "",
        "stock_code": "",
        "stock_type": "",
        "listed_date": "2024-01-01",
        "industry_class": "",
        "industry_class_name": "",
        "main_activities": "",
        "enterprise_scale": "",
        "operating_status": "",
        "competitiveness_score": 0.0,
        "chain_position_text": "",
        "risk_level": "低",
        "tags": [
          {
            "tag_code": "",
            "tag_value": "",
            "tag_name": "",
            "tag_category": "",
            "tag_level": ""
          }
        ],
        "tags_flat": [
          ""
        ],
        "industry_chain_names_flat": [
          ""
        ],
        "financials": [
          {
            "year": 2024,
            "main_business_revenue": 0.0,
            "operating_revenue": 0.0,
            "net_profit": 0.0,
            "rd_expense": 0.0,
            "rd_ratio": 0.0
          }
        ],
        "statistics": [
          {
            "patent_total": 0,
            "patent_valid": 0,
            "patent_valid_count": 0,
            "latest_revenue": 0.0,
            "financing_count": 0,
            "bid_total": 0,
            "news_count": 0,
            "trademark_total": 0,
            "software_copyright_total": 0,
            "rd_ratio": 0.0
          }
        ]
      }
    ],
    "total": 0,
    "fields": [
      ""
    ]
  },
  "ok": true
}
```

#### 4.5 画像基础

##### 15. 企业全景画像

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/panorama`
- 服务内路径：`POST /topic/v1/profile/panorama`
- Python 下游：`POST /internal/gkx-search/profile`
- 接口用途：企业全景画像。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.PanoramaResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.org_id` | `String` | 企业唯一标识 |
| `data.social_credit_code` | `String` | 统一社会信用代码 |
| `data.name_cn` | `String` | 企业中文名称 |
| `data.former_names` | `List<String>` | 曾用名列表 |
| `data.lerep` | `String` | 法定代表人 |
| `data.province` | `String` | 所在省份 |
| `data.city` | `String` | 所在城市 |
| `data.district` | `String` | 所在区县 |
| `data.address` | `String` | 企业注册地址或经营地址 |
| `data.addr_lng` | `BigDecimal` | 地址经度 |
| `data.addr_lat` | `BigDecimal` | 地址纬度 |
| `data.incorporation_year` | `Integer` | 成立年份 |
| `data.incorporation_date` | `String` | 成立日期 |
| `data.start_date` | `String` | 营业起始日期 |
| `data.end_date` | `String` | 营业截止日期 |
| `data.listing_status` | `String` | 上市状态 |
| `data.listing_date` | `String` | 上市日期 |
| `data.registered_capital_value` | `BigDecimal` | 注册资本数值 |
| `data.capital_currency_code` | `String` | 资本币种或金额单位 |
| `data.company_type` | `String` | 企业类型 |
| `data.paid_in_capital_value` | `BigDecimal` | 实缴资本数值 |
| `data.stock_code` | `String` | 股票代码 |
| `data.stock_noun` | `String` | 股票简称 |
| `data.stock_type` | `String` | 股票类别 |
| `data.listed_date` | `String` | 挂牌或上市时间 |
| `data.listed_status` | `String` | 挂牌或上市业务状态 |
| `data.industry_class` | `String` | 行业分类编码 |
| `data.industry_class_name` | `String` | 行业分类名称 |
| `data.main_activities` | `String` | 主营业务描述 |
| `data.main_prod` | `String` | 主要产品或服务 |
| `data.description` | `String` | 企业简介 |
| `data.tags` | `List<TagItem>` | 企业标签明细 |
| `data.tags[].tag_code` | `String` | 标签编码 |
| `data.tags[].tag_value` | `String` | 标签展示值 |
| `data.tags[].tag_name` | `String` | 标签名称 |
| `data.tags[].tag_category` | `String` | 标签分类 |
| `data.tags[].tag_level` | `String` | 标签层级。 对齐 DWD tag_dict.tag_level：national / province / city / district 等字符串；可为空 |
| `data.tags_flat` | `List<String>` | 标签编码平铺列表 |
| `data.industry_chains` | `List<IndustryChainItem>` | 产业链节点明细 |
| `data.industry_chains[].chain_name` | `String` | 产业链名称 |
| `data.industry_chains[].node_name` | `String` | 节点名称 |
| `data.industry_chains[].node_stage_name` | `String` | 节点阶段名称 |
| `data.industry_chain_names_flat` | `List<String>` | 产业链名称平铺列表 |
| `data.executives` | `List<ExecutiveItem>` | 高管列表 |
| `data.executives[].name` | `String` | 高管姓名 |
| `data.executives[].position` | `String` | 高管职务 |
| `data.financials` | `List<FinancialRecord>` | 财务历史记录列表 |
| `data.financials[].year` | `Integer` | 财务年份 |
| `data.financials[].main_business_revenue` | `BigDecimal` | 主营业务收入 |
| `data.financials[].operating_revenue` | `BigDecimal` | 营业收入 |
| `data.financials[].net_profit` | `BigDecimal` | 净利润 |
| `data.financials[].rd_expense` | `BigDecimal` | 研发投入金额 |
| `data.financials[].rd_ratio` | `BigDecimal` | 研发投入占比 |
| `data.financings` | `List<FinancingItem>` | 融资事件列表 |
| `data.financings[].event_id` | `String` | 融资事件标识 |
| `data.financings[].round_name` | `String` | 融资轮次名称 |
| `data.financings[].financing_date` | `String` | 融资日期 |
| `data.financings[].amount` | `BigDecimal` | 融资金额 |
| `data.financings[].currency_code` | `String` | 金额币种 |
| `data.financings[].valuation` | `BigDecimal` | 估值金额 |
| `data.financings[].lead_investor` | `String` | 领投方名称 |
| `data.financings[].investors` | `List<String>` | 投资方名称列表 |
| `data.innovation_carriers` | `List<InnovationCarrierItem>` | 创新载体列表 |
| `data.innovation_carriers[].carrier_type` | `String` | 载体类型 |
| `data.innovation_carriers[].carrier_level` | `String` | 载体等级 |
| `data.innovation_carriers[].carrier_name` | `String` | 载体名称 |
| `data.innovation_carriers[].create_year` | `Integer` | 创建年份 |
| `data.risk_flags` | `RiskFlags` | 风险标记汇总 |
| `data.risk_flags.abnormal_count` | `Integer` | 经营异常数量 |
| `data.risk_flags.shixin_count` | `Integer` | 失信被执行人数量 |
| `data.risk_flags.zhixing_count` | `Integer` | 被执行人数量 |
| `data.risk_flags.punishment_count` | `Integer` | 行政处罚数量 |
| `data.enterprise_scale` | `String` | 企业规模 |
| `data.operating_status` | `String` | 经营状态 |
| `data.competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.tech_score` | `BigDecimal` | 技术力得分 |
| `data.business_score` | `BigDecimal` | 商业力得分 |
| `data.chain_position_text` | `String` | 产业链位置描述 |
| `data.is_chain_leader` | `Boolean` | 是否为链主企业 |
| `data.risk_level` | `String` | 风险等级 |
| `data.website` | `String` | 企业官网地址 |
| `data.contact_phone` | `String` | 联系电话 |
| `data.contact_email` | `String` | 联系邮箱 |
| `data.business_scope` | `String` | 经营范围描述 |
| `data.logo_url` | `String` | 企业 Logo 地址 |
| `data.supply_chain_relations` | `List<SupplyChainRelationItem>` | 供应链关系列表 |
| `data.supply_chain_relations[].relation_type` | `String` | 关系类型 |
| `data.supply_chain_relations[].role` | `String` | 关系角色 |
| `data.supply_chain_relations[].target_org_id` | `String` | 关联企业主键 |
| `data.supply_chain_relations[].target_name` | `String` | 关联企业名称 |
| `data.supply_chain_relations[].supplier_name` | `String` | 供应商名称 |
| `data.supply_chain_relations[].customer_name` | `String` | 客户名称 |
| `data.statistics` | `List<Statistics>` | 统计指标列表 |
| `data.statistics[].patent_total` | `Integer` | 专利总数 |
| `data.statistics[].patent_valid` | `Integer` | 有效专利数量 |
| `data.statistics[].patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `data.statistics[].latest_revenue` | `BigDecimal` | 最新营收金额 |
| `data.statistics[].financing_count` | `Integer` | 融资事件数量 |
| `data.statistics[].bid_total` | `Integer` | 招投标数量 |
| `data.statistics[].news_count` | `Integer` | 资讯数量 |
| `data.statistics[].trademark_total` | `Integer` | 商标数量 |
| `data.statistics[].software_copyright_total` | `Integer` | 软件著作权数量 |
| `data.statistics[].rd_ratio` | `BigDecimal` | 研发投入占比 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
    "social_credit_code": "",
    "name_cn": "",
    "former_names": [
      ""
    ],
    "lerep": "",
    "province": "",
    "city": "",
    "district": "",
    "address": "",
    "addr_lng": 0.0,
    "addr_lat": 0.0,
    "incorporation_year": 2024,
    "incorporation_date": "2024-01-01",
    "start_date": "2024-01-01",
    "end_date": "2024-01-01",
    "listing_status": "",
    "listing_date": "2024-01-01",
    "registered_capital_value": 0.0,
    "capital_currency_code": "",
    "company_type": "",
    "paid_in_capital_value": 0.0,
    "stock_code": "",
    "stock_noun": "",
    "stock_type": "",
    "listed_date": "2024-01-01",
    "listed_status": "",
    "industry_class": "",
    "industry_class_name": "",
    "main_activities": "",
    "main_prod": "",
    "description": "",
    "tags": [
      {
        "tag_code": "",
        "tag_value": "",
        "tag_name": "",
        "tag_category": "",
        "tag_level": ""
      }
    ],
    "tags_flat": [
      ""
    ],
    "industry_chains": [
      {
        "chain_name": "",
        "node_name": "",
        "node_stage_name": ""
      }
    ],
    "industry_chain_names_flat": [
      ""
    ],
    "executives": [
      {
        "name": "",
        "position": ""
      }
    ],
    "financials": [
      {
        "year": 2024,
        "main_business_revenue": 0.0,
        "operating_revenue": 0.0,
        "net_profit": 0.0,
        "rd_expense": 0.0,
        "rd_ratio": 0.0
      }
    ],
    "financings": [
      {
        "event_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "round_name": "",
        "financing_date": "2024-01-01",
        "amount": 0.0,
        "currency_code": "",
        "valuation": 0.0,
        "lead_investor": "",
        "investors": [
          ""
        ]
      }
    ],
    "innovation_carriers": [
      {
        "carrier_type": "",
        "carrier_level": "",
        "carrier_name": "",
        "create_year": 2024
      }
    ],
    "risk_flags": {
      "abnormal_count": 0,
      "shixin_count": 0,
      "zhixing_count": 0,
      "punishment_count": 0
    },
    "enterprise_scale": "",
    "operating_status": "",
    "competitiveness_score": 0.0,
    "tech_score": 0.0,
    "business_score": 0.0,
    "chain_position_text": "",
    "is_chain_leader": true,
    "risk_level": "低",
    "website": "",
    "contact_phone": "",
    "contact_email": "",
    "business_scope": "",
    "logo_url": "",
    "supply_chain_relations": [
      {
        "relation_type": "",
        "role": "",
        "target_org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "target_name": "",
        "supplier_name": "",
        "customer_name": ""
      }
    ],
    "statistics": [
      {
        "patent_total": 0,
        "patent_valid": 0,
        "patent_valid_count": 0,
        "latest_revenue": 0.0,
        "financing_count": 0,
        "bid_total": 0,
        "news_count": 0,
        "trademark_total": 0,
        "software_copyright_total": 0,
        "rd_ratio": 0.0
      }
    ]
  },
  "ok": true
}
```

##### 16. 企业详情弹框

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/card`
- 服务内路径：`POST /topic/v1/profile/card`
- Python 下游：`POST /internal/gkx-search/profile/card`
- 接口用途：企业详情弹框。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.CardResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.header` | `CardHeader` | 卡片头部信息 |
| `data.header.name_cn` | `String` | 企业中文名称 |
| `data.header.logo_url` | `String` | 企业 Logo 地址 |
| `data.header.social_credit_code` | `String` | 统一社会信用代码 |
| `data.header.tags` | `List<TagItem>` | 标签列表 |
| `data.header.tags[].tag_code` | `String` | 标签编码 |
| `data.header.tags[].tag_value` | `String` | 标签展示值 |
| `data.header.tags[].tag_name` | `String` | 标签名称 |
| `data.header.tags[].tag_category` | `String` | 标签分类 |
| `data.header.tags[].tag_level` | `String` | 标签层级。 对齐 DWD tag_dict.tag_level：national / province / city / district 等字符串；可为空 |
| `data.metrics` | `CardMetrics` | 核心指标卡片 |
| `data.metrics.competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.metrics.registered_capital` | `String` | 已格式化的注册资本展示值 |
| `data.metrics.incorporation_date` | `String` | 成立日期 |
| `data.metrics.patent_count` | `Integer` | 专利数量 |
| `data.description` | `String` | 企业简介 |
| `data.business_info` | `CardBusinessInfo` | 工商基础信息块 |
| `data.business_info.lerep` | `String` | 法定代表人 |
| `data.business_info.registered_capital` | `String` | 已格式化的注册资本展示值 |
| `data.business_info.company_type` | `String` | 企业类型 |
| `data.business_info.operating_status` | `String` | 经营状态 |
| `data.business_info.incorporation_date` | `String` | 成立日期 |
| `data.business_info.industry_class_name` | `String` | 行业分类名称 |
| `data.business_info.registered_address` | `String` | 注册地址 |
| `data.business_info.main_activities` | `String` | 主营业务描述 |
| `data.business_info.former_names` | `List<String>` | 曾用名列表 |
| `data.industry_chains` | `List<IndustryChainItem>` | 产业链归属信息 |
| `data.industry_chains[].chain_name` | `String` | 产业链名称 |
| `data.industry_chains[].node_name` | `String` | 节点名称 |
| `data.industry_chains[].node_stage_name` | `String` | 节点阶段名称 |
| `data.qualifications` | `List<TagItem>` | 资质荣誉标签列表 |
| `data.qualifications[].tag_code` | `String` | 标签编码 |
| `data.qualifications[].tag_value` | `String` | 标签展示值 |
| `data.qualifications[].tag_name` | `String` | 标签名称 |
| `data.qualifications[].tag_category` | `String` | 标签分类 |
| `data.qualifications[].tag_level` | `String` | 标签层级。 对齐 DWD tag_dict.tag_level：national / province / city / district 等字符串；可为空 |
| `data.finance_latest` | `CardFinanceLatest` | 最新一期财务概况 |
| `data.finance_latest.year` | `Integer` | 财务年份 |
| `data.finance_latest.main_business_revenue` | `BigDecimal` | 主营业务收入 |
| `data.finance_latest.net_profit` | `BigDecimal` | 净利润 |
| `data.finance_latest.rd_expense` | `BigDecimal` | 研发投入金额 |
| `data.finance_latest.rd_ratio` | `BigDecimal` | 研发投入占比 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "header": {
      "name_cn": "",
      "logo_url": "",
      "social_credit_code": "",
      "tags": [
        {
          "tag_code": "",
          "tag_value": "",
          "tag_name": "",
          "tag_category": "",
          "tag_level": ""
        }
      ]
    },
    "metrics": {
      "competitiveness_score": 0.0,
      "registered_capital": "",
      "incorporation_date": "2024-01-01",
      "patent_count": 0
    },
    "description": "",
    "business_info": {
      "lerep": "",
      "registered_capital": "",
      "company_type": "",
      "operating_status": "",
      "incorporation_date": "2024-01-01",
      "industry_class_name": "",
      "registered_address": "",
      "main_activities": "",
      "former_names": [
        ""
      ]
    },
    "industry_chains": [
      {
        "chain_name": "",
        "node_name": "",
        "node_stage_name": ""
      }
    ],
    "qualifications": [
      {
        "tag_code": "",
        "tag_value": "",
        "tag_name": "",
        "tag_category": "",
        "tag_level": ""
      }
    ],
    "finance_latest": {
      "year": 2024,
      "main_business_revenue": 0.0,
      "net_profit": 0.0,
      "rd_expense": 0.0,
      "rd_ratio": 0.0
    }
  },
  "ok": true
}
```

##### 17. 工商概况详情

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/basic`
- 服务内路径：`POST /topic/v1/profile/basic`
- Python 下游：`POST /internal/gkx-search/profile/basic`
- 接口用途：工商概况详情。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.BasicResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.org_id` | `String` | 企业唯一标识 |
| `data.social_credit_code` | `String` | 统一社会信用代码 |
| `data.name_cn` | `String` | 企业中文名称 |
| `data.lerep` | `String` | 法定代表人 |
| `data.province` | `String` | 所在省份 |
| `data.city` | `String` | 所在城市 |
| `data.address` | `String` | 企业地址 |
| `data.addr_lng` | `BigDecimal` | 地址经度 |
| `data.addr_lat` | `BigDecimal` | 地址纬度 |
| `data.postal_code` | `String` | 邮政编码 |
| `data.incorporation_year` | `Integer` | 成立年份 |
| `data.incorporation_date` | `String` | 成立日期 |
| `data.start_date` | `String` | 经营起始日期 |
| `data.end_date` | `String` | 经营截止日期 |
| `data.listing_status` | `String` | 上市状态 |
| `data.listing_date` | `String` | 上市日期 |
| `data.registered_capital_value` | `BigDecimal` | 注册资本 |
| `data.capital_currency_code` | `String` | 币种或金额单位 |
| `data.registration_org` | `String` | 登记机关 |
| `data.stock_code` | `String` | 股票代码 |
| `data.stock_noun` | `String` | 股票简称 |
| `data.stock_type` | `String` | 股票类别 |
| `data.listed_date` | `String` | 挂牌日期 |
| `data.listed_status` | `String` | 挂牌状态 |
| `data.industry_class` | `String` | 行业分类编码 |
| `data.industry_class_name` | `String` | 行业分类名称 |
| `data.main_activities` | `String` | 主营业务 |
| `data.main_prod` | `String` | 主要产品 |
| `data.enterprise_scale` | `String` | 企业规模 |
| `data.operating_status` | `String` | 经营状态 |
| `data.website` | `String` | 官网地址 |
| `data.contact_phone` | `String` | 联系电话 |
| `data.contact_email` | `String` | 联系邮箱 |
| `data.business_scope` | `String` | 经营范围 |
| `data.description` | `String` | 企业简介 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
    "social_credit_code": "",
    "name_cn": "",
    "lerep": "",
    "province": "",
    "city": "",
    "address": "",
    "addr_lng": 0.0,
    "addr_lat": 0.0,
    "postal_code": "",
    "incorporation_year": 2024,
    "incorporation_date": "2024-01-01",
    "start_date": "2024-01-01",
    "end_date": "2024-01-01",
    "listing_status": "",
    "listing_date": "2024-01-01",
    "registered_capital_value": 0.0,
    "capital_currency_code": "",
    "registration_org": "",
    "stock_code": "",
    "stock_noun": "",
    "stock_type": "",
    "listed_date": "2024-01-01",
    "listed_status": "",
    "industry_class": "",
    "industry_class_name": "",
    "main_activities": "",
    "main_prod": "",
    "enterprise_scale": "",
    "operating_status": "",
    "website": "",
    "contact_phone": "",
    "contact_email": "",
    "business_scope": "",
    "description": ""
  },
  "ok": true
}
```

##### 18. 企业概况 KPI

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/overview`
- 服务内路径：`POST /topic/v1/profile/overview`
- Python 下游：`POST /internal/gkx-search/profile/overview`
- 接口用途：企业概况 KPI。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.OverviewResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.org_id` | `String` | 企业唯一标识 |
| `data.name_cn` | `String` | 企业中文名称 |
| `data.enterprise_scale` | `String` | 企业规模 |
| `data.operating_status` | `String` | 经营状态 |
| `data.risk_level` | `String` | 风险等级 |
| `data.competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.chain_position_text` | `String` | 产业链位置描述 |
| `data.incorporation_year` | `Integer` | 成立年份 |
| `data.listing_status` | `String` | 上市状态 |
| `data.tags` | `List<TagItem>` | 企业标签列表 |
| `data.tags[].tag_code` | `String` | 标签编码 |
| `data.tags[].tag_value` | `String` | 标签展示值 |
| `data.tags[].tag_name` | `String` | 标签名称 |
| `data.tags[].tag_category` | `String` | 标签分类 |
| `data.tags[].tag_level` | `String` | 标签层级。 对齐 DWD tag_dict.tag_level：national / province / city / district 等字符串；可为空 |
| `data.industry_chains` | `List<String>` | 企业所在产业链列表 |
| `data.risk_flags` | `RiskFlags` | 风险标记集合 |
| `data.risk_flags.abnormal_count` | `Integer` | 经营异常数量 |
| `data.risk_flags.shixin_count` | `Integer` | 失信被执行人数量 |
| `data.risk_flags.zhixing_count` | `Integer` | 被执行人数量 |
| `data.risk_flags.punishment_count` | `Integer` | 行政处罚数量 |
| `data.statistics` | `Statistics` | 关键统计指标 |
| `data.statistics.patent_total` | `Integer` | 专利总数 |
| `data.statistics.patent_valid` | `Integer` | 有效专利数量 |
| `data.statistics.patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `data.statistics.latest_revenue` | `BigDecimal` | 最新营收金额 |
| `data.statistics.financing_count` | `Integer` | 融资事件数量 |
| `data.statistics.bid_total` | `Integer` | 招投标数量 |
| `data.statistics.news_count` | `Integer` | 资讯数量 |
| `data.statistics.trademark_total` | `Integer` | 商标数量 |
| `data.statistics.software_copyright_total` | `Integer` | 软件著作权数量 |
| `data.statistics.rd_ratio` | `BigDecimal` | 研发投入占比 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
    "name_cn": "",
    "enterprise_scale": "",
    "operating_status": "",
    "risk_level": "低",
    "competitiveness_score": 0.0,
    "chain_position_text": "",
    "incorporation_year": 2024,
    "listing_status": "",
    "tags": [
      {
        "tag_code": "",
        "tag_value": "",
        "tag_name": "",
        "tag_category": "",
        "tag_level": ""
      }
    ],
    "industry_chains": [
      ""
    ],
    "risk_flags": {
      "abnormal_count": 0,
      "shixin_count": 0,
      "zhixing_count": 0,
      "punishment_count": 0
    },
    "statistics": {
      "patent_total": 0,
      "patent_valid": 0,
      "patent_valid_count": 0,
      "latest_revenue": 0.0,
      "financing_count": 0,
      "bid_total": 0,
      "news_count": 0,
      "trademark_total": 0,
      "software_copyright_total": 0,
      "rd_ratio": 0.0
    }
  },
  "ok": true
}
```

##### 19. 企业资讯

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/news`
- 服务内路径：`POST /topic/v1/profile/news`
- Python 下游：`POST /internal/gkx-search/profile/news`
- 接口用途：企业资讯。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.NewsResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<NewsItem>` | 当前页资讯列表 |
| `data.list[].news_id` | `String` | 资讯主键 |
| `data.list[].title` | `String` | 资讯标题 |
| `data.list[].summary` | `String` | 资讯摘要 |
| `data.list[].source` | `String` | 资讯来源 |
| `data.list[].date` | `String` | 资讯日期 |
| `data.list[].url` | `String` | 原文链接 |
| `data.list[].content_type` | `String` | 内容类型 |
| `data.total` | `Long` | 资讯总数 |
| `data.page` | `Integer` | 当前页码 |
| `data.size` | `Integer` | 每页条数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "news_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "title": "",
        "summary": "",
        "source": "mock",
        "date": "2024-01-01",
        "url": "",
        "content_type": ""
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20
  },
  "ok": true
}
```

##### 20. 风险汇总

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/summary`
- 服务内路径：`POST /topic/v1/profile/risk/summary`
- Python 下游：`POST /internal/gkx-search/profile/risk/summary`
- 接口用途：风险汇总。
- Controller：`EnterpriseOpenApiController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseResponseDTOs.RiskSummaryResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.risk_level` | `String` | 风险等级 |
| `data.risk_flags` | `RiskFlags` | 风险标记汇总 |
| `data.risk_flags.abnormal_count` | `Integer` | 经营异常数量 |
| `data.risk_flags.shixin_count` | `Integer` | 失信被执行人数量 |
| `data.risk_flags.zhixing_count` | `Integer` | 被执行人数量 |
| `data.risk_flags.punishment_count` | `Integer` | 行政处罚数量 |
| `data.competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `data.total_count` | `Integer` | 全量风险条目总数 |
| `data.type_counts` | `Map<String,Integer>` | 各风险类型数量映射 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "risk_level": "低",
    "risk_flags": {
      "abnormal_count": 0,
      "shixin_count": 0,
      "zhixing_count": 0,
      "punishment_count": 0
    },
    "competitiveness_score": 0.0,
    "total_count": 0,
    "type_counts": {
      "example_key": "example_value"
    }
  },
  "ok": true
}
```

#### 4.6 画像细分

##### 21. 财务历史

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/finance`
- 服务内路径：`POST /topic/v1/profile/finance`
- Python 下游：`POST /internal/gkx-search/profile/finance`
- 接口用途：企业财务历史。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.FinanceHistoryResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.financials` | `List<FinancialYearItem>` | 历年财务数据（按 `year` 倒序），字段同 §4.1 financials |
| `data.financials[].year` | `Integer` | 财务年份 |
| `data.financials[].total_assets` | `BigDecimal` | 总资产（万元） |
| `data.financials[].total_liabilities` | `BigDecimal` | 总负债（万元） |
| `data.financials[].operating_revenue` | `BigDecimal` | 营业收入（万元） |
| `data.financials[].main_business_revenue` | `BigDecimal` | 主营业务收入（万元） |
| `data.financials[].total_profit` | `BigDecimal` | 利润总额（万元） |
| `data.financials[].pure_profit` | `BigDecimal` | 净利润（万元） |
| `data.financials[].total_tax_paid` | `BigDecimal` | 纳税总额（万元） |
| `data.financials[].total_fixed_assets` | `BigDecimal` | 固定资产（万元） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "financials": [
      {
        "year": 2024,
        "total_assets": 0.0,
        "total_liabilities": 0.0,
        "operating_revenue": 0.0,
        "main_business_revenue": 0.0,
        "total_profit": 0.0,
        "pure_profit": 0.0,
        "total_tax_paid": 0.0,
        "total_fixed_assets": 0.0
      }
    ]
  },
  "ok": true
}
```

##### 22. 专利明细

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/patent`
- 服务内路径：`POST /topic/v1/profile/patent`
- Python 下游：`POST /internal/gkx-search/profile/patent`
- 接口用途：企业专利明细。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.PatentPageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<PatentDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].patent_id` | `String` | 专利 ID |
| `data.list[].publication_number` | `String` | 专利公布号 |
| `data.list[].title_zh` | `String` | 中文标题 |
| `data.list[].title_en` | `String` | 英文标题 |
| `data.list[].abstract_zh` | `String` | 中文摘要 |
| `data.list[].patent_type` | `String` | 申请类型（A=发明/U=实用/F=外观/W=PCT） |
| `data.list[].country` | `String` | 国家（如 `CN`） |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].filing_year` | `Integer` | 申请年份 |
| `data.list[].publication_date` | `String` | 公开日期 |
| `data.list[].publication_year` | `Integer` | 公开年份 |
| `data.list[].grant_date` | `String` | 授权日期（未授权为 `null`） |
| `data.list[].grant_year` | `Integer` | 授权年份（未授权为 `null`） |
| `data.list[].grant_number` | `String` | 授权号（未授权为 `null`） |
| `data.list[].ipc_main` | `String` | IPC 主分类号 |
| `data.list[].cpc_main` | `String` | CPC 主分类号 |
| `data.list[].inventor` | `String` | 发明人 |
| `data.list[].applicant_name` | `String` | 原始申请人名称 |
| `data.list[].assignee_name` | `String` | 当前专利权人名称 |
| `data.list[].legal_status` | `String` | 法律状态（有效/无效/审查中） |
| `data.list[].citation_count` | `Integer` | 引用专利数量 |
| `data.list[].cited_by_count` | `Integer` | 被引数量 |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "patent_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "publication_number": "",
        "title_zh": "",
        "title_en": "",
        "abstract_zh": "",
        "patent_type": "",
        "country": "",
        "filing_date": "2024-01-01",
        "filing_year": 2024,
        "publication_date": "2024-01-01",
        "publication_year": 2024,
        "grant_date": "2024-01-01",
        "grant_year": 2024,
        "grant_number": "",
        "ipc_main": "",
        "cpc_main": "",
        "inventor": "",
        "applicant_name": "",
        "assignee_name": "",
        "legal_status": "",
        "citation_count": 0,
        "cited_by_count": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20
  },
  "ok": true
}
```

##### 23. 业务标签

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/tags`
- 服务内路径：`POST /topic/v1/profile/tags`
- Python 下游：`POST /internal/gkx-search/profile/tags`
- 接口用途：企业业务标签。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.ProfileTagsResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.tags` | `List<TagItem>` | 标签编码列表（如 `high_tech`/`little_giant`） |
| `data.tags[].tag_code` | `String` | 标签编码 |
| `data.tags[].tag_value` | `String` | 标签展示值 |
| `data.tags[].tag_name` | `String` | 标签名称 |
| `data.tags[].tag_category` | `String` | 标签分类 |
| `data.tags[].tag_level` | `String` | 标签层级。 对齐 DWD tag_dict.tag_level：national / province / city / district 等字符串；可为空 |
| `data.tags_flat` | `List<String>` | 标签编码数组（如 `["high_tech","little_giant"]`） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "tags": [
      {
        "tag_code": "",
        "tag_value": "",
        "tag_name": "",
        "tag_category": "",
        "tag_level": ""
      }
    ],
    "tags_flat": [
      ""
    ]
  },
  "ok": true
}
```

##### 24. 竞争力得分

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/competitiveness`
- 服务内路径：`POST /topic/v1/profile/competitiveness`
- Python 下游：`POST /internal/gkx-search/profile/competitiveness`
- 接口用途：企业竞争力得分。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.CompetitivenessResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.competitiveness_score` | `BigDecimal` | 综合竞争力评分（0-100） |
| `data.statistics` | `List<Statistics>` | 统计汇总（nested，含 patent_valid/patent_total/latest_revenue 等） |
| `data.statistics[].patent_total` | `Integer` | 专利总数 |
| `data.statistics[].patent_valid` | `Integer` | 有效专利数量 |
| `data.statistics[].patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `data.statistics[].latest_revenue` | `BigDecimal` | 最新营收金额 |
| `data.statistics[].financing_count` | `Integer` | 融资事件数量 |
| `data.statistics[].bid_total` | `Integer` | 招投标数量 |
| `data.statistics[].news_count` | `Integer` | 资讯数量 |
| `data.statistics[].trademark_total` | `Integer` | 商标数量 |
| `data.statistics[].software_copyright_total` | `Integer` | 软件著作权数量 |
| `data.statistics[].rd_ratio` | `BigDecimal` | 研发投入占比 |
| `data.enterprise_scale` | `String` | 企业规模（`大型`/`中型`/`小型`/`微型`/`规上`） |
| `data.chain_position_text` | `String` | 产业链位置文本 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "competitiveness_score": 0.0,
    "statistics": [
      {
        "patent_total": 0,
        "patent_valid": 0,
        "patent_valid_count": 0,
        "latest_revenue": 0.0,
        "financing_count": 0,
        "bid_total": 0,
        "news_count": 0,
        "trademark_total": 0,
        "software_copyright_total": 0,
        "rd_ratio": 0.0
      }
    ],
    "enterprise_scale": "",
    "chain_position_text": ""
  },
  "ok": true
}
```

##### 25. 招投标

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/bids`
- 服务内路径：`POST /topic/v1/profile/bids`
- Python 下游：`POST /internal/gkx-search/profile/bids`
- 接口用途：企业招投标。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.BidPageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<BidItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].id` | `String` | 招投标记录 ID |
| `data.list[].role` | `String` | 企业角色（中标方/投标方/招标方） |
| `data.list[].announcement_title` | `String` | 公告标题 |
| `data.list[].counterparty_name` | `String` | 对方企业名称 |
| `data.list[].counterparty_code` | `String` | 对方信用代码 |
| `data.list[].announcement_date` | `String` | 公告日期（`yyyy-MM-dd`） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "id": "",
        "role": "",
        "announcement_title": "",
        "counterparty_name": "",
        "counterparty_code": "",
        "announcement_date": "2024-01-01"
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20
  },
  "ok": true
}
```

##### 26. 高管列表

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/executives`
- 服务内路径：`POST /topic/v1/profile/executives`
- Python 下游：`POST /internal/gkx-search/profile/executives`
- 接口用途：企业高管列表。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.ExecutiveListResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<ExecutiveItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].name` | `String` | 高管姓名 |
| `data.list[].position` | `String` | 高管职务 |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "name": "",
        "position": ""
      }
    ],
    "total": 0
  },
  "ok": true
}
```

##### 27. 创新载体

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/innovation-carriers`
- 服务内路径：`POST /topic/v1/profile/innovation-carriers`
- Python 下游：`POST /internal/gkx-search/profile/innovation-carriers`
- 接口用途：企业创新载体。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.InnovationCarrierListResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<InnovationCarrierItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].carrier_type` | `String` | 载体类型 |
| `data.list[].carrier_level` | `String` | 载体等级 |
| `data.list[].carrier_name` | `String` | 载体名称 |
| `data.list[].create_year` | `Integer` | 创建年份 |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `data.types` | `List<String>` | 载体类型列表 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "carrier_type": "",
        "carrier_level": "",
        "carrier_name": "",
        "create_year": 2024
      }
    ],
    "total": 0,
    "types": [
      ""
    ]
  },
  "ok": true
}
```

##### 28. 资质荣誉汇总

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/qualifications`
- 服务内路径：`POST /topic/v1/profile/qualifications`
- Python 下游：`POST /internal/gkx-search/profile/qualifications`
- 接口用途：企业资质荣誉汇总。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.QualificationResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.qualifications` | `List<QualificationItem>` | 合并资质列表 |
| `data.qualifications[].type` | `String` | 类型 tag/carrier/listing |
| `data.qualifications[].code` | `String` | 编码 |
| `data.qualifications[].value` | `String` | 值/级别 |
| `data.qualifications[].name` | `String` | 名称 |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `data.tags` | `List<TagItem>` | 标签编码列表（如 `high_tech`/`little_giant`） |
| `data.tags[].tag_code` | `String` | 标签编码 |
| `data.tags[].tag_value` | `String` | 标签展示值 |
| `data.tags[].tag_name` | `String` | 标签名称 |
| `data.tags[].tag_category` | `String` | 标签分类 |
| `data.tags[].tag_level` | `String` | 标签层级。 对齐 DWD tag_dict.tag_level：national / province / city / district 等字符串；可为空 |
| `data.tags_flat` | `List<String>` | 标签编码数组（如 `["high_tech","little_giant"]`） |
| `data.carriers` | `List<InnovationCarrierItem>` | 创新载体列表 |
| `data.carriers[].carrier_type` | `String` | 载体类型 |
| `data.carriers[].carrier_level` | `String` | 载体等级 |
| `data.carriers[].carrier_name` | `String` | 载体名称 |
| `data.carriers[].create_year` | `Integer` | 创建年份 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "qualifications": [
      {
        "type": "",
        "code": "",
        "value": "",
        "name": ""
      }
    ],
    "total": 0,
    "tags": [
      {
        "tag_code": "",
        "tag_value": "",
        "tag_name": "",
        "tag_category": "",
        "tag_level": ""
      }
    ],
    "tags_flat": [
      ""
    ],
    "carriers": [
      {
        "carrier_type": "",
        "carrier_level": "",
        "carrier_name": "",
        "create_year": 2024
      }
    ]
  },
  "ok": true
}
```

##### 29. 专利年度趋势

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/patent/history`
- 服务内路径：`POST /topic/v1/profile/patent/history`
- Python 下游：`POST /internal/gkx-search/profile/patent/history`
- 接口用途：企业专利年度趋势。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.PatentHistoryResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.history` | `List<PatentHistoryItem>` | 年度趋势列表（按年份正序） |
| `data.history[].year` | `Integer` | 年份 |
| `data.history[].apply_count` | `Integer` | 当年申请数 |
| `data.history[].grant_count` | `Integer` | 当年授权数 |
| `data.history[].valid_count` | `Integer` | 当年有效数 |
| `data.history[].invention_count` | `Integer` | 当年发明专利数 |
| `data.history[].citation_count` | `Integer` | 当年被引总次数 |
| `data.history[].latest_patent_date` | `String` | 当年最新申请日期 |
| `data.history[].latest_grant_date` | `String` | 当年最新授权日期 |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "history": [
      {
        "year": 2024,
        "apply_count": 0,
        "grant_count": 0,
        "valid_count": 0,
        "invention_count": 0,
        "citation_count": 0,
        "latest_patent_date": "2024-01-01",
        "latest_grant_date": "2024-01-01"
      }
    ],
    "total": 0
  },
  "ok": true
}
```

##### 30. 最新财务快照

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/finance/latest`
- 服务内路径：`POST /topic/v1/profile/finance/latest`
- Python 下游：`POST /internal/gkx-search/profile/finance/latest`
- 接口用途：企业最新财务快照。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.FinanceLatestResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.latest` | `FinancialYearItem` | 最新年份财务数据（字段同 §4.1 financials 元素） |
| `data.latest.year` | `Integer` | 财务年份 |
| `data.latest.total_assets` | `BigDecimal` | 总资产（万元） |
| `data.latest.total_liabilities` | `BigDecimal` | 总负债（万元） |
| `data.latest.operating_revenue` | `BigDecimal` | 营业收入（万元） |
| `data.latest.main_business_revenue` | `BigDecimal` | 主营业务收入（万元） |
| `data.latest.total_profit` | `BigDecimal` | 利润总额（万元） |
| `data.latest.pure_profit` | `BigDecimal` | 净利润（万元） |
| `data.latest.total_tax_paid` | `BigDecimal` | 纳税总额（万元） |
| `data.latest.total_fixed_assets` | `BigDecimal` | 固定资产（万元） |
| `data.year` | `Integer` | 最新年份 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "latest": {
      "year": 2024,
      "total_assets": 0.0,
      "total_liabilities": 0.0,
      "operating_revenue": 0.0,
      "main_business_revenue": 0.0,
      "total_profit": 0.0,
      "pure_profit": 0.0,
      "total_tax_paid": 0.0,
      "total_fixed_assets": 0.0
    },
    "year": 2024
  },
  "ok": true
}
```

##### 31. 财务趋势

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/finance/trend`
- 服务内路径：`POST /topic/v1/profile/finance/trend`
- Python 下游：`POST /internal/gkx-search/profile/finance/trend`
- 接口用途：企业财务趋势。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.FinanceTrendResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.series` | `List<FinancialYearItem>` | 趋势数据列表（按年份正序） |
| `data.series[].year` | `Integer` | 财务年份 |
| `data.series[].total_assets` | `BigDecimal` | 总资产（万元） |
| `data.series[].total_liabilities` | `BigDecimal` | 总负债（万元） |
| `data.series[].operating_revenue` | `BigDecimal` | 营业收入（万元） |
| `data.series[].main_business_revenue` | `BigDecimal` | 主营业务收入（万元） |
| `data.series[].total_profit` | `BigDecimal` | 利润总额（万元） |
| `data.series[].pure_profit` | `BigDecimal` | 净利润（万元） |
| `data.series[].total_tax_paid` | `BigDecimal` | 纳税总额（万元） |
| `data.series[].total_fixed_assets` | `BigDecimal` | 固定资产（万元） |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `data.years` | `List<Integer>` | 年份数组 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "series": [
      {
        "year": 2024,
        "total_assets": 0.0,
        "total_liabilities": 0.0,
        "operating_revenue": 0.0,
        "main_business_revenue": 0.0,
        "total_profit": 0.0,
        "pure_profit": 0.0,
        "total_tax_paid": 0.0,
        "total_fixed_assets": 0.0
      }
    ],
    "total": 0,
    "years": [
      2024
    ]
  },
  "ok": true
}
```

##### 32. 供应链关系

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/supply-chain`
- 服务内路径：`POST /topic/v1/profile/supply-chain`
- Python 下游：`POST /internal/gkx-search/profile/supply-chain`
- 接口用途：企业供应链关系。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.SupplyChainResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<ProfileSupplyChainItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].related_name` | `String` | 关联方企业名 |
| `data.list[].relation_type` | `String` | 关系类型（投资方/被投资方/招标方/中标方） |
| `data.list[].related_code` | `String` | 关联方信用代码 |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "related_name": "",
        "relation_type": "",
        "related_code": ""
      }
    ],
    "total": 0
  },
  "ok": true
}
```

##### 33. 对外投资

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/invest`
- 服务内路径：`POST /topic/v1/profile/invest`
- Python 下游：`POST /internal/gkx-search/profile/invest`
- 接口用途：企业对外投资。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.InvestPageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<InvestItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].inv_org_id` | `String` | 被投企业 id |
| `data.list[].inv_name` | `String` | 被投企业名称 |
| `data.list[].inv_external_id` | `String` | 被投企业信用代码 |
| `data.list[].investment_amount` | `BigDecimal` | 投资金额 |
| `data.list[].investment_ratio` | `BigDecimal` | 股权占比（%） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "inv_org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "inv_name": "",
        "inv_external_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "investment_amount": 0.0,
        "investment_ratio": 0.0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20
  },
  "ok": true
}
```

##### 34. 股东信息

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/shareholders`
- 服务内路径：`POST /topic/v1/profile/shareholders`
- Python 下游：`POST /internal/gkx-search/profile/shareholders`
- 接口用途：企业股东信息。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.ShareholderResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<ShareholderItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].shareholder_name` | `String` | 股东名称 |
| `data.list[].shareholder_type` | `String` | 股东类型（企业法人/自然人） |
| `data.list[].investment_ratio` | `BigDecimal` | 股权占比（%） |
| `data.list[].subscribed_capital` | `BigDecimal` | 认缴出资额（万元） |
| `data.list[].paid_in_capital` | `BigDecimal` | 实缴出资额（万元） |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `data.note` | `String` | 标注"DWD 无此表，暂返回 Mock 数据" |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "shareholder_name": "",
        "shareholder_type": "",
        "investment_ratio": 0.0,
        "subscribed_capital": 0.0,
        "paid_in_capital": 0.0
      }
    ],
    "total": 0,
    "note": ""
  },
  "ok": true
}
```

##### 35. 融资事件

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/financings`
- 服务内路径：`POST /topic/v1/profile/financings`
- Python 下游：`POST /internal/gkx-search/profile/financings`
- 接口用途：企业融资事件。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.FinancingPageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<FinancingEventItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].funding_round` | `String` | 融资轮次 |
| `data.list[].funding_amount` | `BigDecimal` | 融资金额 |
| `data.list[].funding_currency_code` | `String` | 币种 |
| `data.list[].post_valuation` | `BigDecimal` | 投后估值 |
| `data.list[].completion_date` | `String` | 完成日期 |
| `data.list[].investors_name` | `String` | 投资方名称 |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "funding_round": "",
        "funding_amount": 0.0,
        "funding_currency_code": "",
        "post_valuation": 0.0,
        "completion_date": "2024-01-01",
        "investors_name": ""
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20
  },
  "ok": true
}
```

##### 36. 融资统计

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/financings/summary`
- 服务内路径：`POST /topic/v1/profile/financings/summary`
- Python 下游：`POST /internal/gkx-search/profile/financings/summary`
- 接口用途：企业融资统计。
- Controller：`EnterpriseProfileDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.FinancingSummaryResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.total_rounds` | `Integer` | 融资总轮次 |
| `data.total_amount` | `BigDecimal` | 累计融资金额（CNY） |
| `data.total_amount_currency` | `String` | 币种（CNY） |
| `data.latest_valuation` | `BigDecimal` | 最新估值 |
| `data.latest_round` | `String` | 最新融资轮次 |
| `data.financing_count` | `Integer` | 统计表融资次数 |
| `data.financing_total_amount` | `BigDecimal` | 统计表累计金额 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "total_rounds": 0,
    "total_amount": 0.0,
    "total_amount_currency": "",
    "latest_valuation": 0.0,
    "latest_round": "",
    "financing_count": 0,
    "financing_total_amount": 0.0
  },
  "ok": true
}
```

#### 4.7 风险

##### 37. 全部风险分组

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/all`
- 服务内路径：`POST /topic/v1/profile/risk/all`
- Python 下游：`POST /internal/gkx-search/profile/risk/all`
- 接口用途：按类型分组返回风险。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseRiskAllRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskAllResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识 |
| `size` | `Integer` | 否 | 每类风险最新条数；默认 3，最大 10 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.groups` | `List<RiskGroupItem>` | 分组列表（按 node_stage） |
| `data.groups[].risk_type` | `String` | 风险类型编码 |
| `data.groups[].risk_name` | `String` | 风险类型中文名 |
| `data.groups[].risk_category` | `String` | 风险大类（judicial/risk/penalty） |
| `data.groups[].count` | `Integer` | 该类型风险数 |
| `data.groups[].latest_items` | `List<RiskDetailItem>` | 该组最新几条明细（请求 size） |
| `data.groups[].latest_items[].case_no` | `String` | 案号 |
| `data.groups[].latest_items[].case_title` | `String` | 案件标题 |
| `data.groups[].latest_items[].case_cause` | `String` | 案由 |
| `data.groups[].latest_items[].court_name` | `String` | 法院 |
| `data.groups[].latest_items[].filing_date` | `String` | 申请日期 |
| `data.groups[].latest_items[].publish_date` | `String` | 发布日期 |
| `data.groups[].latest_items[].judgment_date` | `String` | 判决日期 |
| `data.groups[].latest_items[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.groups[].latest_items[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `data.risk_level` | `String` | 风险等级（`低`/`中`/`高`） |
| `data.risk_flags` | `RiskFlags` | 风险标记聚合（abnormal_count/shixin_count/zhixing_count） |
| `data.risk_flags.abnormal_count` | `Integer` | 经营异常数量 |
| `data.risk_flags.shixin_count` | `Integer` | 失信被执行人数量 |
| `data.risk_flags.zhixing_count` | `Integer` | 被执行人数量 |
| `data.risk_flags.punishment_count` | `Integer` | 行政处罚数量 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "groups": [
      {
        "risk_type": "",
        "risk_name": "",
        "risk_category": "",
        "count": 0,
        "latest_items": [
          {
            "case_no": "",
            "case_title": "",
            "case_cause": "",
            "court_name": "",
            "filing_date": "2024-01-01",
            "publish_date": "2024-01-01",
            "judgment_date": "2024-01-01",
            "party_role": "",
            "is_history": 0
          }
        ]
      }
    ],
    "total": 0,
    "risk_level": "低",
    "risk_flags": {
      "abnormal_count": 0,
      "shixin_count": 0,
      "zhixing_count": 0,
      "punishment_count": 0
    }
  },
  "ok": true
}
```

##### 38. 风险明细 · 司法案件

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/judicial-case`
- 服务内路径：`POST /topic/v1/profile/risk/judicial-case`
- Python 下游：`POST /internal/gkx-search/profile/risk/judicial-case`
- 接口用途：司法案件分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 39. 风险明细 · 失信被执行人

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/dishonest`
- 服务内路径：`POST /topic/v1/profile/risk/dishonest`
- Python 下游：`POST /internal/gkx-search/profile/risk/dishonest`
- 接口用途：失信被执行人分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 40. 风险明细 · 被执行人

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/executed`
- 服务内路径：`POST /topic/v1/profile/risk/executed`
- Python 下游：`POST /internal/gkx-search/profile/risk/executed`
- 接口用途：被执行人分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 41. 风险明细 · 限制高消费

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/limit-high`
- 服务内路径：`POST /topic/v1/profile/risk/limit-high`
- Python 下游：`POST /internal/gkx-search/profile/risk/limit-high`
- 接口用途：限制高消费分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 42. 风险明细 · 裁判文书

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/lawsuit`
- 服务内路径：`POST /topic/v1/profile/risk/lawsuit`
- Python 下游：`POST /internal/gkx-search/profile/risk/lawsuit`
- 接口用途：裁判文书分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 43. 风险明细 · 法院立案

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/court-filed`
- 服务内路径：`POST /topic/v1/profile/risk/court-filed`
- Python 下游：`POST /internal/gkx-search/profile/risk/court-filed`
- 接口用途：法院立案分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 44. 风险明细 · 开庭公告

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/court-notice`
- 服务内路径：`POST /topic/v1/profile/risk/court-notice`
- Python 下游：`POST /internal/gkx-search/profile/risk/court-notice`
- 接口用途：开庭公告分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 45. 风险明细 · 法院公告

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/court-announcement`
- 服务内路径：`POST /topic/v1/profile/risk/court-announcement`
- Python 下游：`POST /internal/gkx-search/profile/risk/court-announcement`
- 接口用途：法院公告分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 46. 风险明细 · 股权冻结

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/equity-freeze`
- 服务内路径：`POST /topic/v1/profile/risk/equity-freeze`
- Python 下游：`POST /internal/gkx-search/profile/risk/equity-freeze`
- 接口用途：股权冻结分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 47. 风险明细 · 股权出质

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/equity-pledge`
- 服务内路径：`POST /topic/v1/profile/risk/equity-pledge`
- Python 下游：`POST /internal/gkx-search/profile/risk/equity-pledge`
- 接口用途：股权出质分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 48. 风险明细 · 终本案件

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/zhongben`
- 服务内路径：`POST /topic/v1/profile/risk/zhongben`
- Python 下游：`POST /internal/gkx-search/profile/risk/zhongben`
- 接口用途：终本案件分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 49. 风险明细 · 动产抵押

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/chattel-mortgage`
- 服务内路径：`POST /topic/v1/profile/risk/chattel-mortgage`
- Python 下游：`POST /internal/gkx-search/profile/risk/chattel-mortgage`
- 接口用途：动产抵押分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 50. 风险明细 · 司法拍卖

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/judicial-sale`
- 服务内路径：`POST /topic/v1/profile/risk/judicial-sale`
- Python 下游：`POST /internal/gkx-search/profile/risk/judicial-sale`
- 接口用途：司法拍卖分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 51. 风险明细 · 破产案件

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/bankruptcy`
- 服务内路径：`POST /topic/v1/profile/risk/bankruptcy`
- Python 下游：`POST /internal/gkx-search/profile/risk/bankruptcy`
- 接口用途：破产案件分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 52. 风险明细 · 经营异常

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/abnormal`
- 服务内路径：`POST /topic/v1/profile/risk/abnormal`
- Python 下游：`POST /internal/gkx-search/profile/risk/abnormal`
- 接口用途：经营异常分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 53. 风险明细 · 行政处罚

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/punishment`
- 服务内路径：`POST /topic/v1/profile/risk/punishment`
- Python 下游：`POST /internal/gkx-search/profile/risk/punishment`
- 接口用途：行政处罚分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 54. 风险明细 · 严重违法

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/illegal`
- 服务内路径：`POST /topic/v1/profile/risk/illegal`
- Python 下游：`POST /internal/gkx-search/profile/risk/illegal`
- 接口用途：严重违法分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

##### 55. 风险明细 · 税收违法

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/risk/tax-punish`
- 服务内路径：`POST /topic/v1/profile/risk/tax-punish`
- Python 下游：`POST /internal/gkx-search/profile/risk/tax-punish`
- 接口用途：税收违法分页明细。
- Controller：`EnterpriseRiskDetailController`
- 请求对象：`EnterpriseProfileRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.RiskTypePageResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识。 对应 Python 接口中的 org_id 字段 |
| `page` | `Integer` | 否 | 当前页码。 用于资讯等分页画像接口 |
| `size` | `Integer` | 否 | 每页条数。 用于资讯等分页画像接口 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "page": 1,
  "size": 20
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.list` | `List<RiskDetailItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.list[].case_no` | `String` | 案号 |
| `data.list[].case_title` | `String` | 案件标题 |
| `data.list[].case_cause` | `String` | 案由 |
| `data.list[].court_name` | `String` | 法院 |
| `data.list[].filing_date` | `String` | 申请日期 |
| `data.list[].publish_date` | `String` | 发布日期 |
| `data.list[].judgment_date` | `String` | 判决日期 |
| `data.list[].party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `data.list[].is_history` | `Integer` | 是否历史（0=当前/1=历史） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.size` | `Integer` | 每页条数，默认 20，最大 100（兼容 `page_size` 字段） |
| `data.risk_type` | `String` | 风险类型编码 |
| `data.risk_name` | `String` | 风险类型中文名 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "list": [
      {
        "case_no": "",
        "case_title": "",
        "case_cause": "",
        "court_name": "",
        "filing_date": "2024-01-01",
        "publish_date": "2024-01-01",
        "judgment_date": "2024-01-01",
        "party_role": "",
        "is_history": 0
      }
    ],
    "total": 0,
    "page": 1,
    "size": 20,
    "risk_type": "",
    "risk_name": ""
  },
  "ok": true
}
```

#### 4.8 图谱

##### 56. 企业关系子图

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/graph/subgraph`
- 服务内路径：`POST /topic/v1/profile/graph/subgraph`
- Python 下游：`POST /internal/gkx-search/profile/graph/subgraph`
- 接口用途：N 跳邻域子图。
- Controller：`EnterpriseGraphController`
- 请求对象：`EnterpriseGraphSubgraphRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.GraphResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `org_id` | `String` | 是 | 企业唯一标识 |
| `steps` | `Integer` | 否 | 拓展步数；默认 1，最大 3 |

请求 JSON 示例：

```json
{
  "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "steps": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.nodes` | `List<GraphNodeItem>` | 节点列表（含中心企业 + 邻居） |
| `data.nodes[].node_key` | `String` | 要拓展的节点 vid |
| `data.nodes[].node_type` | `String` | 环节类型（1=上游/2=中游/3=下游） |
| `data.nodes[].name` | `String` | 简称（如 `深圳市`） |
| `data.nodes[].weight` | `BigDecimal` | 权重/得分 |
| `data.nodes[].props` | `Map<String,Object>` | 节点扩展属性（类型相关，文档为自由 object） |
| `data.nodes[].tags` | `List<String>` | 标签编码列表（如 `high_tech`/`little_giant`） |
| `data.edges` | `List<GraphEdgeItem>` | 新旧节点之间的所有边（含新节点之间、新节点与已有节点之间的边） |
| `data.edges[].src_key` | `String` | 边起点节点键 |
| `data.edges[].dst_key` | `String` | 边终点节点键 |
| `data.edges[].relation_type` | `String` | 关系类型（投资方/被投资方/招标方/中标方） |
| `data.edges[].weight` | `BigDecimal` | 权重/得分 |
| `data.edges[].props` | `Map<String,Object>` | 边扩展属性 |
| `data.center` | `String` | 中心节点 vid |
| `data.target` | `String` | 被拓展的节点 vid |
| `data.steps` | `Integer` | 跳数，默认 1，最大 3 |
| `data.source` | `String` | 数据来源 nebula\|mock\|error |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "nodes": [
      {
        "node_key": "",
        "node_type": "",
        "name": "",
        "weight": 0.0,
        "props": {
          "example_key": "example_value"
        },
        "tags": [
          ""
        ]
      }
    ],
    "edges": [
      {
        "src_key": "",
        "dst_key": "",
        "relation_type": "",
        "weight": 0.0,
        "props": {
          "example_key": "example_value"
        }
      }
    ],
    "center": "",
    "target": "",
    "steps": 0,
    "source": "mock"
  },
  "ok": true
}
```

##### 57. 图谱节点拓展

- 接口路径：`POST gateway地址/enterprise/topic/v1/profile/graph/expand`
- 服务内路径：`POST /topic/v1/profile/graph/expand`
- Python 下游：`POST /internal/gkx-search/profile/graph/expand`
- 接口用途：节点拓展。
- Controller：`EnterpriseGraphController`
- 请求对象：`EnterpriseGraphExpandRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.GraphResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `node_key` | `String` | 是 | 待拓展节点标识 |
| `exclude_keys` | `List<String>` | 否 | 已展示节点标识列表，用于排除 |
| `steps` | `Integer` | 否 | 拓展步数；默认 1 |

请求 JSON 示例：

```json
{
  "node_key": "",
  "exclude_keys": [
    ""
  ],
  "steps": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.nodes` | `List<GraphNodeItem>` | 节点列表（含中心企业 + 邻居） |
| `data.nodes[].node_key` | `String` | 要拓展的节点 vid |
| `data.nodes[].node_type` | `String` | 环节类型（1=上游/2=中游/3=下游） |
| `data.nodes[].name` | `String` | 简称（如 `深圳市`） |
| `data.nodes[].weight` | `BigDecimal` | 权重/得分 |
| `data.nodes[].props` | `Map<String,Object>` | 节点扩展属性（类型相关，文档为自由 object） |
| `data.nodes[].tags` | `List<String>` | 标签编码列表（如 `high_tech`/`little_giant`） |
| `data.edges` | `List<GraphEdgeItem>` | 新旧节点之间的所有边（含新节点之间、新节点与已有节点之间的边） |
| `data.edges[].src_key` | `String` | 边起点节点键 |
| `data.edges[].dst_key` | `String` | 边终点节点键 |
| `data.edges[].relation_type` | `String` | 关系类型（投资方/被投资方/招标方/中标方） |
| `data.edges[].weight` | `BigDecimal` | 权重/得分 |
| `data.edges[].props` | `Map<String,Object>` | 边扩展属性 |
| `data.center` | `String` | 中心节点 vid |
| `data.target` | `String` | 被拓展的节点 vid |
| `data.steps` | `Integer` | 跳数，默认 1，最大 3 |
| `data.source` | `String` | 数据来源 nebula\|mock\|error |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "nodes": [
      {
        "node_key": "",
        "node_type": "",
        "name": "",
        "weight": 0.0,
        "props": {
          "example_key": "example_value"
        },
        "tags": [
          ""
        ]
      }
    ],
    "edges": [
      {
        "src_key": "",
        "dst_key": "",
        "relation_type": "",
        "weight": 0.0,
        "props": {
          "example_key": "example_value"
        }
      }
    ],
    "center": "",
    "target": "",
    "steps": 0,
    "source": "mock"
  },
  "ok": true
}
```

#### 4.9 发展概况

##### 58. 发展概况 · 概况 KPI

- 接口路径：`POST gateway地址/enterprise/topic/v1/stats/overview/kpi`
- 服务内路径：`POST /topic/v1/stats/overview/kpi`
- Python 下游：`POST /internal/gkx-search/stats/overview/kpi`
- 接口用途：概况 KPI。
- Controller：`EnterpriseStatsOverviewController`
- 请求对象：`EnterpriseStatsRegionRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.OverviewKpiResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `region_id` | `String` | 否 | 区域编码；概况类接口默认 440300 |
| `months` | `Integer` | 否 | 趋势月份数；仅 trend 接口使用，默认 12 |

请求 JSON 示例：

```json
{
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "months": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.region_id` | `String` | 国标行政区编码（v9.0 新增，如 440300） |
| `data.region_name` | `String` | 区县名称（如南山区） |
| `data.enterprise_total` | `Integer` | 深圳企业总数（DWD shenzhen_summary: stat_type='enterprise_total'） |
| `data.new_enterprise_count` | `Integer` | 新增企业数（最近一周成立） |
| `data.active_enterprise_count` | `Integer` | 活跃企业数（business_status=1） |
| `data.total_revenue` | `BigDecimal` | 产值规模（最新年度营收之和，万元） |
| `data.stat_date` | `String` | 统计日期（ETL 跑批日期） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
    "region_name": "",
    "enterprise_total": 0,
    "new_enterprise_count": 0,
    "active_enterprise_count": 0,
    "total_revenue": 0.0,
    "stat_date": "2024-01-01"
  },
  "ok": true
}
```

##### 59. 发展概况 · 产业分布

- 接口路径：`POST gateway地址/enterprise/topic/v1/stats/overview/industry-distribution`
- 服务内路径：`POST /topic/v1/stats/overview/industry-distribution`
- Python 下游：`POST /internal/gkx-search/stats/overview/industry-distribution`
- 接口用途：产业分布。
- Controller：`EnterpriseStatsOverviewController`
- 请求对象：`EnterpriseStatsRegionRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.IndustryDistResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `region_id` | `String` | 否 | 区域编码；概况类接口默认 440300 |
| `months` | `Integer` | 否 | 趋势月份数；仅 trend 接口使用，默认 12 |

请求 JSON 示例：

```json
{
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "months": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.region_id` | `String` | 国标行政区编码（v9.0 新增，如 440300） |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `data.items` | `List<ChainCountItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].chain_code` | `String` | 产业链编码 |
| `data.items[].chain_name` | `String` | 产业链名称 |
| `data.items[].enterprise_count` | `Integer` | 该产业链下深圳企业数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
    "total": 0,
    "items": [
      {
        "chain_code": "",
        "chain_name": "",
        "enterprise_count": 0
      }
    ]
  },
  "ok": true
}
```

##### 60. 发展概况 · 增长趋势

- 接口路径：`POST gateway地址/enterprise/topic/v1/stats/overview/trend`
- 服务内路径：`POST /topic/v1/stats/overview/trend`
- Python 下游：`POST /internal/gkx-search/stats/overview/trend`
- 接口用途：增长趋势。
- Controller：`EnterpriseStatsOverviewController`
- 请求对象：`EnterpriseStatsRegionRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.TrendResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `region_id` | `String` | 否 | 区域编码；概况类接口默认 440300 |
| `months` | `Integer` | 否 | 趋势月份数；仅 trend 接口使用，默认 12 |

请求 JSON 示例：

```json
{
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "months": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.region_id` | `String` | 国标行政区编码（v9.0 新增，如 440300） |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `data.items` | `List<GrowthTrendItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].year` | `Integer` | 年份 |
| `data.items[].month` | `Integer` | 月份（1-12） |
| `data.items[].new_enterprise_count` | `Integer` | 新增企业数（最近一周成立） |
| `data.items[].label` | `String` | 月份标签（如 `2026-06`） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
    "total": 0,
    "items": [
      {
        "year": 2024,
        "month": 0,
        "new_enterprise_count": 0,
        "label": ""
      }
    ]
  },
  "ok": true
}
```

##### 61. 发展概况 · 区域热力

- 接口路径：`POST gateway地址/enterprise/topic/v1/stats/overview/district-heat`
- 服务内路径：`POST /topic/v1/stats/overview/district-heat`
- Python 下游：`POST /internal/gkx-search/stats/overview/district-heat`
- 接口用途：区域热力。
- Controller：`EnterpriseStatsOverviewController`
- 请求对象：`EnterpriseStatsRegionRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.DistrictHeatResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `region_id` | `String` | 否 | 区域编码；概况类接口默认 440300 |
| `months` | `Integer` | 否 | 趋势月份数；仅 trend 接口使用，默认 12 |

请求 JSON 示例：

```json
{
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "months": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.region_id` | `String` | 国标行政区编码（v9.0 新增，如 440300） |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `data.items` | `List<DistrictHeatItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].region_id` | `String` | 国标行政区编码（v9.0 新增，如 440300） |
| `data.items[].region_name` | `String` | 区县名称（如南山区） |
| `data.items[].enterprise_total` | `Integer` | 深圳企业总数（DWD shenzhen_summary: stat_type='enterprise_total'） |
| `data.items[].heat_level` | `Integer` | 热度等级（1-5，5 最热） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
    "total": 0,
    "items": [
      {
        "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "region_name": "",
        "enterprise_total": 0,
        "heat_level": 0
      }
    ]
  },
  "ok": true
}
```

##### 62. 发展概况 · 八大产业 KPI

- 接口路径：`POST gateway地址/enterprise/topic/v1/stats/overview/industry-kpi`
- 服务内路径：`POST /topic/v1/stats/overview/industry-kpi`
- Python 下游：`POST /internal/gkx-search/stats/overview/industry-kpi`
- 接口用途：八大产业 KPI。
- Controller：`EnterpriseStatsOverviewController`
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.IndustryKpiResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source` | `String` | 否 | 数据源：`nebula` / `mock` |

请求 JSON 示例：

```json
{
  "source": "mock"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.enterprise_total` | `Integer` | 深圳企业总数（DWD shenzhen_summary: stat_type='enterprise_total'） |
| `data.research_staff_total` | `Integer` | 八大未来产业科研人数总数（去重） |
| `data.industry_coverage` | `Integer` | 覆盖产业数（八大未来产业已覆盖数） |
| `data.patent_total` | `Integer` | 专利总数 |
| `data.high_tech_count` | `Integer` | 高新技术企业数 |
| `data.stat_date` | `String` | 统计日期（ETL 跑批日期） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "enterprise_total": 0,
    "research_staff_total": 0,
    "industry_coverage": 0,
    "patent_total": 0,
    "high_tech_count": 0,
    "stat_date": "2024-01-01"
  },
  "ok": true
}
```

##### 63. 发展概况 · 八大产业对比

- 接口路径：`POST gateway地址/enterprise/topic/v1/stats/overview/industry-comparison`
- 服务内路径：`POST /topic/v1/stats/overview/industry-comparison`
- Python 下游：`POST /internal/gkx-search/stats/overview/industry-comparison`
- 接口用途：八大产业对比。
- Controller：`EnterpriseStatsOverviewController`
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.IndustryComparisonResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source` | `String` | 否 | 数据源：`nebula` / `mock` |

请求 JSON 示例：

```json
{
  "source": "mock"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `data.items` | `List<ChainCountItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].chain_code` | `String` | 产业链编码 |
| `data.items[].chain_name` | `String` | 产业链名称 |
| `data.items[].enterprise_count` | `Integer` | 该产业链下深圳企业数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "total": 0,
    "items": [
      {
        "chain_code": "",
        "chain_name": "",
        "enterprise_count": 0
      }
    ]
  },
  "ok": true
}
```

##### 64. 发展概况 · 产业历年趋势

- 接口路径：`POST gateway地址/enterprise/topic/v1/stats/overview/industry-trend`
- 服务内路径：`POST /topic/v1/stats/overview/industry-trend`
- Python 下游：`POST /internal/gkx-search/stats/overview/industry-trend`
- 接口用途：产业历年趋势。
- Controller：`EnterpriseStatsOverviewController`
- 请求对象：`EnterpriseChainCodeRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.IndustryTrendResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `chain_code` | `String` | 是 | 产业链编码，例如 IC001 |

请求 JSON 示例：

```json
{
  "chain_code": ""
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.chain_code` | `String` | 产业编码（如 `IC001`），不能为 `ALL` |
| `data.chain_name` | `String` | 产业链名称 |
| `data.items` | `List<YearCountItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].year` | `Integer` | 年份 |
| `data.items[].enterprise_count` | `Integer` | 该产业链下深圳企业数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "chain_code": "",
    "chain_name": "",
    "items": [
      {
        "year": 2024,
        "enterprise_count": 0
      }
    ]
  },
  "ok": true
}
```

#### 4.10 分布

##### 65. 企业地理分布

- 接口路径：`POST gateway地址/enterprise/topic/v1/stats/distribution`
- 服务内路径：`POST /topic/v1/stats/distribution`
- Python 下游：`POST /internal/gkx-search/stats/distribution`
- 接口用途：四维度分布。
- Controller：`EnterpriseDistributionController`
- 请求对象：`EnterpriseDistributionRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.DistributionResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `dimension` | `String` | 否 | 维度：global / national / regional / city |
| `region_type` | `String` | 否 | 区域类型：standard / city_cluster；仅 regional 有效 |
| `parent_region_id` | `String` | 否 | 父级区域编码 |

请求 JSON 示例：

```json
{
  "dimension": "",
  "region_type": "",
  "parent_region_id": "6bc50eca3435d4b53fb7bf661d058a47"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.dimension` | `String` | 维度：`global`(全球) / `national`(全国) / `regional`(地区) / `city`(深圳市)，默认 `national` |
| `data.region_type` | `String` | 区域类型：`standard`(行政区划) / `city_cluster`(城市群)，仅 `regional` 维度有效，默认 `standard` |
| `data.parent_region_id` | `String` | 上级地区码。`regional` 传省码(如 `440000`)展开地级市，`city` 传 `440300` 展开深圳区县。**`city` 维度不传时默认 `440300`（深圳市）** |
| `data.map_data` | `List<DistributionMapItem>` | 地区列表（按 enterprise_count 降序），前端地图热力图和列表共用 |
| `data.map_data[].region_id` | `String` | 地区码（ISO码 / 国标码 / CU码） |
| `data.map_data[].region_name` | `String` | 地区名称 |
| `data.map_data[].enterprise_count` | `Long` | 企业总数 |
| `data.map_data[].new_enterprise_count` | `Long` | 新增企业数（用于趋势箭头） |
| `data.map_data[].ratio` | `BigDecimal` | 占比百分比 |
| `data.kpi` | `DistributionKpi` | 分布 KPI 汇总 |
| `data.kpi.total_enterprise_count` | `Long` | 该维度企业总数 |
| `data.kpi.covered_regions` | `Integer` | 覆盖地区数 |
| `data.kpi.new_enterprise_count` | `Long` | 新增企业总数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "dimension": "",
    "region_type": "",
    "parent_region_id": "6bc50eca3435d4b53fb7bf661d058a47",
    "map_data": [
      {
        "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "region_name": "",
        "enterprise_count": 0,
        "new_enterprise_count": 0,
        "ratio": 0.0
      }
    ],
    "kpi": {
      "total_enterprise_count": 0,
      "covered_regions": 0,
      "new_enterprise_count": 0
    }
  },
  "ok": true
}
```

#### 4.11 重点企业

##### 66. 重点企业 KPI

- 接口路径：`POST gateway地址/enterprise/topic/v1/key-enterprise/kpi`
- 服务内路径：`POST /topic/v1/key-enterprise/kpi`
- Python 下游：`POST /internal/gkx-search/key-enterprise/kpi`
- 接口用途：重点企业 KPI。
- Controller：`EnterpriseKeyEnterpriseController`
- 请求对象：`EnterpriseStatsRegionRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.KeyEnterpriseKpiResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `region_id` | `String` | 否 | 区域编码；概况类接口默认 440300 |
| `months` | `Integer` | 否 | 趋势月份数；仅 trend 接口使用，默认 12 |

请求 JSON 示例：

```json
{
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "months": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.key_enterprise_total` | `Integer` | 深圳重点企业总数（DWD shenzhen_summary: stat_type='key_enterprise_total'） |
| `data.high_tech_total` | `Integer` | 国高企总数（ES count: tags_flat contains "high_tech"） |
| `data.covered_chain_nodes` | `Integer` | 覆盖产业链环节数（DWD stat_summary: stat_type='key_enterprise_node' 的 dim_code 去重数） |
| `data.covered_districts` | `Integer` | 覆盖行政区数（DWD stat_summary: stat_type='key_enterprise_district' 的行数） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "key_enterprise_total": 0,
    "high_tech_total": 0,
    "covered_chain_nodes": 0,
    "covered_districts": 0
  },
  "ok": true
}
```

##### 67. 重点企业链位分组列表

- 接口路径：`POST gateway地址/enterprise/topic/v1/key-enterprise/chain-list`
- 服务内路径：`POST /topic/v1/key-enterprise/chain-list`
- Python 下游：`POST /internal/gkx-search/key-enterprise/chain-list`
- 接口用途：链位分组列表。
- Controller：`EnterpriseKeyEnterpriseController`
- 请求对象：`EnterpriseKeyChainListRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.KeyChainListResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `chain_code` | `String` | 是 | 产业链编码 |
| `node_stage` | `Integer` | 否 | 节点阶段 1/2/3；为空返回全部阶段分组 |
| `page` | `Integer` | 否 | 当前页码 |
| `page_size` | `Integer` | 否 | 每页条数（Python 字段名 page_size） |

请求 JSON 示例：

```json
{
  "chain_code": "",
  "node_stage": 0,
  "page": 1,
  "page_size": 1
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.chain_code` | `String` | 产业编码（如 `IC001`），不能为 `ALL` |
| `data.chain_name` | `String` | 产业链名称 |
| `data.groups` | `List<KeyChainGroupItem>` | 分组列表（按 node_stage） |
| `data.groups[].node_stage` | `Integer` | 环节编码（1/2/3） |
| `data.groups[].node_stage_name` | `String` | 环节名称（上游/中游/下游） |
| `data.groups[].total` | `Integer` | 该环节重点企业总数 |
| `data.groups[].enterprises` | `List<FeaturedEnterpriseItem>` | 企业列表（分页后） |
| `data.groups[].enterprises[].org_id` | `String` | 企业 ID |
| `data.groups[].enterprises[].name_cn` | `String` | 企业名称 |
| `data.groups[].enterprises[].logo_url` | `String` | 企业 Logo |
| `data.groups[].enterprises[].tags` | `List<String>` | 标签编码数组 |
| `data.groups[].enterprises[].industry_chain_names` | `List<String>` | 产业链名称数组 |
| `data.groups[].enterprises[].node_name` | `String` | 环节节点名称 |
| `data.groups[].enterprises[].node_stage` | `Integer` | 环节编码（1/2/3） |
| `data.groups[].enterprises[].node_stage_name` | `String` | 环节名称（上游/中游/下游） |
| `data.groups[].enterprises[].competitiveness_score` | `BigDecimal` | 竞争力得分（无值时取 tech_score + business_score 均值） |
| `data.groups[].enterprises[].enterprise_scale` | `String` | 企业规模 |
| `data.groups[].enterprises[].company_type` | `String` | 企业类型 |
| `data.groups[].enterprises[].region_text` | `String` | 地区拼接（省-市-区） |
| `data.groups[].enterprises[].province` | `String` | 省 |
| `data.groups[].enterprises[].city` | `String` | 市 |
| `data.groups[].enterprises[].district` | `String` | 区县 |
| `data.groups[].enterprises[].registered_capital_value` | `BigDecimal` | 注册资本（万元） |
| `data.groups[].enterprises[].operating_status` | `String` | 经营状态 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "chain_code": "",
    "chain_name": "",
    "groups": [
      {
        "node_stage": 0,
        "node_stage_name": "",
        "total": 0,
        "enterprises": [
          {
            "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
            "name_cn": "",
            "logo_url": "",
            "tags": [
              ""
            ],
            "industry_chain_names": [
              ""
            ],
            "node_name": "",
            "node_stage": 0,
            "node_stage_name": "",
            "competitiveness_score": 0.0,
            "enterprise_scale": "",
            "company_type": "",
            "region_text": "",
            "province": "",
            "city": "",
            "district": "",
            "registered_capital_value": 0.0,
            "operating_status": ""
          }
        ]
      }
    ]
  },
  "ok": true
}
```

##### 68. 重点企业产业主体统计

- 接口路径：`POST gateway地址/enterprise/topic/v1/key-enterprise/chain-subject-stats`
- 服务内路径：`POST /topic/v1/key-enterprise/chain-subject-stats`
- Python 下游：`POST /internal/gkx-search/key-enterprise/chain-subject-stats`
- 接口用途：产业主体统计。
- Controller：`EnterpriseKeyEnterpriseController`
- 请求对象：`EnterpriseStatsRegionRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.KeyChainSubjectStatsResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `region_id` | `String` | 否 | 区域编码；概况类接口默认 440300 |
| `months` | `Integer` | 否 | 趋势月份数；仅 trend 接口使用，默认 12 |

请求 JSON 示例：

```json
{
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "months": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<KeyChainSubjectItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].chain_code` | `String` | 产业链编码 |
| `data.items[].chain_name` | `String` | 产业链名称 |
| `data.items[].enterprise_count` | `Integer` | 该产业链下深圳企业数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "chain_code": "",
        "chain_name": "",
        "enterprise_count": 0
      }
    ]
  },
  "ok": true
}
```

##### 69. 重点企业资质摘要

- 接口路径：`POST gateway地址/enterprise/topic/v1/key-enterprise/qualification-summary`
- 服务内路径：`POST /topic/v1/key-enterprise/qualification-summary`
- Python 下游：`POST /internal/gkx-search/key-enterprise/qualification-summary`
- 接口用途：资质摘要。
- Controller：`EnterpriseKeyEnterpriseController`
- 请求对象：`EnterpriseStatsRegionRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.KeyQualificationSummaryResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `region_id` | `String` | 否 | 区域编码；概况类接口默认 440300 |
| `months` | `Integer` | 否 | 趋势月份数；仅 trend 接口使用，默认 12 |

请求 JSON 示例：

```json
{
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "months": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<KeyQualificationStatItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].tag_code` | `String` | 资质编码（high_tech/little_giant/gazelle/unicorn） |
| `data.items[].tag_name` | `String` | 标签中文名（如 `高新技术企业`） |
| `data.items[].enterprise_count` | `Integer` | 该产业链下深圳企业数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "tag_code": "",
        "tag_name": "",
        "enterprise_count": 0
      }
    ]
  },
  "ok": true
}
```

##### 70. 类型×规模交叉统计

- 接口路径：`POST gateway地址/enterprise/topic/v1/key-enterprise/type-scale-stats`
- 服务内路径：`POST /topic/v1/key-enterprise/type-scale-stats`
- Python 下游：`POST /internal/gkx-search/key-enterprise/type-scale-stats`
- 接口用途：类型×规模矩阵。
- Controller：`EnterpriseKeyEnterpriseController`
- 请求对象：`EnterpriseTypeScaleRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.KeyTypeScaleStatsResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `region_level` | `String` | 是 | 区域层级：national / province / city |

请求 JSON 示例：

```json
{
  "region_level": ""
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.region_level` | `String` | 区域层级：national（全国）/ province（省级）/ city（市级） |
| `data.items` | `List<TypeScaleRowItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].company_type` | `String` | 企业类型（有限责任公司/股份有限公司/外商投资/国有企业/民营企业） |
| `data.items[].scales` | `List<TypeScaleCell>` | 规模列表 |
| `data.items[].scales[].enterprise_scale` | `String` | 规模（大型/中型/小型/微型） |
| `data.items[].scales[].enterprise_count` | `Integer` | 企业数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "region_level": "",
    "items": [
      {
        "company_type": "",
        "scales": [
          {
            "enterprise_scale": "",
            "enterprise_count": 0
          }
        ]
      }
    ]
  },
  "ok": true
}
```

#### 4.12 明星企业

##### 71. 明星企业 KPI

- 接口路径：`POST gateway地址/enterprise/topic/v1/star-enterprise/kpi`
- 服务内路径：`POST /topic/v1/star-enterprise/kpi`
- Python 下游：`POST /internal/gkx-search/star-enterprise/kpi`
- 接口用途：明星企业 KPI。
- Controller：`EnterpriseStarEnterpriseController`
- 请求对象：`EnterpriseStatsRegionRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.StarEnterpriseKpiResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `region_id` | `String` | 否 | 区域编码；概况类接口默认 440300 |
| `months` | `Integer` | 否 | 趋势月份数；仅 trend 接口使用，默认 12 |

请求 JSON 示例：

```json
{
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47",
  "months": 0
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.star_enterprise_total` | `Integer` | 明星企业总数（ES count: tags_flat contains "star_enterprise"） |
| `data.covered_chain_nodes` | `Integer` | 覆盖产业链环节数（DWD stat_summary: stat_type='key_enterprise_node' 的 dim_code 去重数） |
| `data.covered_districts` | `Integer` | 覆盖行政区数（DWD stat_summary: stat_type='key_enterprise_district' 的行数） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "star_enterprise_total": 0,
    "covered_chain_nodes": 0,
    "covered_districts": 0
  },
  "ok": true
}
```

##### 72. 明星企业列表

- 接口路径：`POST gateway地址/enterprise/topic/v1/star-enterprise/list`
- 服务内路径：`POST /topic/v1/star-enterprise/list`
- Python 下游：`POST /internal/gkx-search/star-enterprise/list`
- 接口用途：明星企业列表。
- Controller：`EnterpriseStarEnterpriseController`
- 请求对象：`EnterpriseStarListRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.StarEnterpriseListResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `page` | `Integer` | 否 | 当前页码 |
| `page_size` | `Integer` | 否 | 每页条数（Python 字段名 page_size） |
| `region_id` | `String` | 否 | 区域编码；为空表示全国 |

请求 JSON 示例：

```json
{
  "page": 1,
  "page_size": 1,
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.page_size` | `Integer` | 每页条数，默认 20，最大 100 |
| `data.items` | `List<FeaturedEnterpriseItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].org_id` | `String` | 企业 ID |
| `data.items[].name_cn` | `String` | 企业名称 |
| `data.items[].logo_url` | `String` | 企业 Logo |
| `data.items[].tags` | `List<String>` | 标签编码列表（含 star_enterprise） |
| `data.items[].industry_chain_names` | `List<String>` | 产业链名称列表 |
| `data.items[].node_name` | `String` | 环节名称（如 `集成电路设计`） |
| `data.items[].node_stage` | `Integer` | 产业链环节（1=上游/2=中游/3=下游），不传则返回全部 3 组 |
| `data.items[].node_stage_name` | `String` | 环节名称（上游/中游/下游） |
| `data.items[].competitiveness_score` | `BigDecimal` | 竞争力得分 |
| `data.items[].enterprise_scale` | `String` | 企业规模（大型/中型/小型/微型） |
| `data.items[].company_type` | `String` | 企业类型（有限责任公司/股份有限公司/外商投资/国有企业/民营企业） |
| `data.items[].region_text` | `String` | 地区文本（省-市-区拼接） |
| `data.items[].province` | `String` | 省 |
| `data.items[].city` | `String` | 市 |
| `data.items[].district` | `String` | 区县 |
| `data.items[].registered_capital_value` | `BigDecimal` | 注册资本（万元） |
| `data.items[].operating_status` | `String` | 经营状态 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "total": 0,
    "page": 1,
    "page_size": 1,
    "items": [
      {
        "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "name_cn": "",
        "logo_url": "",
        "tags": [
          ""
        ],
        "industry_chain_names": [
          ""
        ],
        "node_name": "",
        "node_stage": 0,
        "node_stage_name": "",
        "competitiveness_score": 0.0,
        "enterprise_scale": "",
        "company_type": "",
        "region_text": "",
        "province": "",
        "city": "",
        "district": "",
        "registered_capital_value": 0.0,
        "operating_status": ""
      }
    ]
  },
  "ok": true
}
```

#### 4.13 深圳企业

##### 73. 深圳企业 KPI

- 接口路径：`POST gateway地址/enterprise/topic/v1/shenzhen/kpi`
- 服务内路径：`POST /topic/v1/shenzhen/kpi`
- Python 下游：`POST /internal/gkx-search/shenzhen/kpi`
- 接口用途：深圳 KPI。
- Controller：`EnterpriseShenzhenController`
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.ShenzhenKpiResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source` | `String` | 否 | 数据源：`nebula` / `mock` |

请求 JSON 示例：

```json
{
  "source": "mock"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.enterprise_total` | `Integer` | 深圳企业总数（DWD shenzhen_summary: stat_type='enterprise_total'） |
| `data.key_enterprise_total` | `Integer` | 深圳重点企业总数（DWD shenzhen_summary: stat_type='key_enterprise_total'） |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "enterprise_total": 0,
    "key_enterprise_total": 0
  },
  "ok": true
}
```

##### 74. 深圳增长趋势

- 接口路径：`POST gateway地址/enterprise/topic/v1/shenzhen/growth-trend`
- 服务内路径：`POST /topic/v1/shenzhen/growth-trend`
- Python 下游：`POST /internal/gkx-search/shenzhen/growth-trend`
- 接口用途：历年累计增长。
- Controller：`EnterpriseShenzhenController`
- 请求对象：`EnterpriseShenzhenTrendRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.ShenzhenGrowthTrendResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `start_year` | `Integer` | 否 | 起始年份；默认 2015 |
| `end_year` | `Integer` | 否 | 结束年份；默认 2026 |

请求 JSON 示例：

```json
{
  "start_year": 2024,
  "end_year": 2024
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<CumulativeCountItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].year` | `Integer` | 年份 |
| `data.items[].cumulative_count` | `Integer` | 该年及之前成立的企业累计数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "year": 2024,
        "cumulative_count": 0
      }
    ]
  },
  "ok": true
}
```

##### 75. 深圳产业分布

- 接口路径：`POST gateway地址/enterprise/topic/v1/shenzhen/industry-distribution`
- 服务内路径：`POST /topic/v1/shenzhen/industry-distribution`
- Python 下游：`POST /internal/gkx-search/shenzhen/industry-distribution`
- 接口用途：深圳产业分布。
- Controller：`EnterpriseShenzhenController`
- 请求对象：`EnterpriseMetaRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.ShenzhenIndustryDistResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `source` | `String` | 否 | 数据源：`nebula` / `mock` |

请求 JSON 示例：

```json
{
  "source": "mock"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.items` | `List<ChainCountItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].chain_code` | `String` | 产业链编码 |
| `data.items[].chain_name` | `String` | 产业链名称 |
| `data.items[].enterprise_count` | `Integer` | 该产业链下深圳企业数 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "items": [
      {
        "chain_code": "",
        "chain_name": "",
        "enterprise_count": 0
      }
    ]
  },
  "ok": true
}
```

##### 76. 深圳重点企业列表

- 接口路径：`POST gateway地址/enterprise/topic/v1/shenzhen/key-enterprise-list`
- 服务内路径：`POST /topic/v1/shenzhen/key-enterprise-list`
- Python 下游：`POST /internal/gkx-search/shenzhen/key-enterprise-list`
- 接口用途：深圳重点企业列表。
- Controller：`EnterpriseShenzhenController`
- 请求对象：`EnterpriseStarListRequest`
- 返回对象：`R<EnterpriseExtendedDTOs.ShenzhenKeyListResponse>`

入参字段表：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `page` | `Integer` | 否 | 当前页码 |
| `page_size` | `Integer` | 否 | 每页条数（Python 字段名 page_size） |
| `region_id` | `String` | 否 | 区域编码；为空表示全国 |

请求 JSON 示例：

```json
{
  "page": 1,
  "page_size": 1,
  "region_id": "6bc50eca3435d4b53fb7bf661d058a47"
}
```

返回字段表（包络 + `data`，对齐 Java DTO；说明含 Python 回填）：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `Integer` | 统一响应码；成功通常为 `0` |
| `msg` | `String` | 统一响应消息；成功时可能为 `null` |
| `ok` | `Boolean` | 是否成功（Java `R` 包络字段） |
| `data.total` | `Long` | 各产业企业数合计（不去重，含重复） |
| `data.page` | `Integer` | 页码，从 1 开始 |
| `data.page_size` | `Integer` | 每页条数，默认 20，最大 100 |
| `data.items` | `List<FeaturedEnterpriseItem>` | 企业列表（字段同 §3.1 `_SEARCH_LIST_SOURCE`，与关键词检索完全一致） |
| `data.items[].org_id` | `String` | 企业 ID |
| `data.items[].name_cn` | `String` | 企业名称 |
| `data.items[].logo_url` | `String` | 企业 Logo |
| `data.items[].tags` | `List<String>` | 标签编码列表（含 star_enterprise） |
| `data.items[].industry_chain_names` | `List<String>` | 产业链名称列表 |
| `data.items[].node_name` | `String` | 环节名称（如 `集成电路设计`） |
| `data.items[].node_stage` | `Integer` | 产业链环节（1=上游/2=中游/3=下游），不传则返回全部 3 组 |
| `data.items[].node_stage_name` | `String` | 环节名称（上游/中游/下游） |
| `data.items[].competitiveness_score` | `BigDecimal` | 竞争力得分 |
| `data.items[].enterprise_scale` | `String` | 企业规模（大型/中型/小型/微型） |
| `data.items[].company_type` | `String` | 企业类型（有限责任公司/股份有限公司/外商投资/国有企业/民营企业） |
| `data.items[].region_text` | `String` | 地区文本（省-市-区拼接） |
| `data.items[].province` | `String` | 省 |
| `data.items[].city` | `String` | 市 |
| `data.items[].district` | `String` | 区县 |
| `data.items[].registered_capital_value` | `BigDecimal` | 注册资本（万元） |
| `data.items[].operating_status` | `String` | 经营状态 |

返回 JSON 示例（字段与上表对齐，值为示意）：

```json
{
  "code": 0,
  "msg": null,
  "data": {
    "total": 0,
    "page": 1,
    "page_size": 1,
    "items": [
      {
        "org_id": "6bc50eca3435d4b53fb7bf661d058a47",
        "name_cn": "",
        "logo_url": "",
        "tags": [
          ""
        ],
        "industry_chain_names": [
          ""
        ],
        "node_name": "",
        "node_stage": 0,
        "node_stage_name": "",
        "competitiveness_score": 0.0,
        "enterprise_scale": "",
        "company_type": "",
        "region_text": "",
        "province": "",
        "city": "",
        "district": "",
        "registered_capital_value": 0.0,
        "operating_status": ""
      }
    ]
  },
  "ok": true
}
```

## 5. 行级 / 嵌套类型附录（对齐 Java DTO + Python 中文说明）


### 5.1 `SearchItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `org_id` | `String` | 企业唯一标识 |
| `social_credit_code` | `String` | 统一社会信用代码 |
| `name_cn` | `String` | 企业中文名称 |
| `former_names` | `List<String>` | 曾用名列表 |
| `lerep` | `String` | 法定代表人 |
| `province` | `String` | 所在省份 |
| `city` | `String` | 所在城市 |
| `district` | `String` | 所在区县 |
| `industry_class` | `String` | 行业分类编码 |
| `industry_class_name` | `String` | 行业分类名称 |
| `incorporation_year` | `Integer` | 成立年份 |
| `incorporation_date` | `String` | 成立日期 |
| `listing_status` | `String` | 上市状态 |
| `registered_capital_value` | `BigDecimal` | 注册资本 |
| `tags_flat` | `List<String>` | 标签编码平铺列表 |
| `industry_chain_names_flat` | `List<String>` | 产业链名称平铺列表 |
| `enterprise_scale` | `String` | 企业规模 |
| `competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `risk_level` | `String` | 风险等级 |
| `operating_status` | `String` | 经营状态 |
| `chain_position_text` | `String` | 产业链位置描述 |
| `main_prod` | `String` | 主要产品 |
| `logo_url` | `String` | 企业 Logo 地址 |
| `company_type` | `String` | 企业类型 |
| `region_id` | `String` | 区域编码 |
| `tech_score` | `BigDecimal` | 技术力得分 |
| `business_score` | `BigDecimal` | 商业力得分 |
| `high_value_patent_count` | `Integer` | 高价值专利数量 |
| `revenue_growth_rate` | `BigDecimal` | 营收增长率 |
| `profit_margin` | `BigDecimal` | 利润率 |
| `supply_chain_role` | `String` | 供应链角色 |
| `core_tech_tags_flat` | `List<String>` | 核心技术标签编码列表 |
| `statistics` | `List<Statistics>` | 统计指标列表 |

### 5.2 `SuggestItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `org_id` | `String` | 企业唯一标识 |
| `name_cn` | `String` | 企业中文名称 |

### 5.3 `Statistics`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `patent_total` | `Integer` | 专利总数 |
| `patent_valid` | `Integer` | 有效专利数量 |
| `patent_valid_count` | `Integer` | 有效专利数量的兼容字段 |
| `latest_revenue` | `BigDecimal` | 最新营收金额 |
| `financing_count` | `Integer` | 融资事件数量 |
| `bid_total` | `Integer` | 招投标数量 |
| `news_count` | `Integer` | 资讯数量 |
| `trademark_total` | `Integer` | 商标数量 |
| `software_copyright_total` | `Integer` | 软件著作权数量 |
| `rd_ratio` | `BigDecimal` | 研发投入占比 |

### 5.4 `RiskFlags`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `abnormal_count` | `Integer` | 经营异常数量 |
| `shixin_count` | `Integer` | 失信被执行人数量 |
| `zhixing_count` | `Integer` | 被执行人数量 |
| `punishment_count` | `Integer` | 行政处罚数量 |

### 5.5 `TagItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `tag_code` | `String` | 标签编码 |
| `tag_value` | `String` | 标签展示值 |
| `tag_name` | `String` | 标签名称 |
| `tag_category` | `String` | 标签分类 |
| `tag_level` | `String` | 标签层级。 对齐 DWD tag_dict.tag_level：national / province / city / district 等字符串；可为空 |

### 5.6 `FinancialYearItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `year` | `Integer` | 财务年份 |
| `total_assets` | `BigDecimal` | 总资产（万元） |
| `total_liabilities` | `BigDecimal` | 总负债（万元） |
| `operating_revenue` | `BigDecimal` | 营业收入（万元） |
| `main_business_revenue` | `BigDecimal` | 主营业务收入（万元） |
| `total_profit` | `BigDecimal` | 利润总额（万元） |
| `pure_profit` | `BigDecimal` | 净利润（万元） |
| `total_tax_paid` | `BigDecimal` | 纳税总额（万元） |
| `total_fixed_assets` | `BigDecimal` | 固定资产（万元） |

### 5.7 `PatentDetailItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `patent_id` | `String` | 专利 ID |
| `publication_number` | `String` | 专利公布号 |
| `title_zh` | `String` | 中文标题 |
| `title_en` | `String` | 英文标题 |
| `abstract_zh` | `String` | 中文摘要 |
| `patent_type` | `String` | 申请类型（A=发明/U=实用/F=外观/W=PCT） |
| `country` | `String` | 国家（如 `CN`） |
| `filing_date` | `String` | 申请日期 |
| `filing_year` | `Integer` | 申请年份 |
| `publication_date` | `String` | 公开日期 |
| `publication_year` | `Integer` | 公开年份 |
| `grant_date` | `String` | 授权日期（未授权为 `null`） |
| `grant_year` | `Integer` | 授权年份（未授权为 `null`） |
| `grant_number` | `String` | 授权号（未授权为 `null`） |
| `ipc_main` | `String` | IPC 主分类号 |
| `cpc_main` | `String` | CPC 主分类号 |
| `inventor` | `String` | 发明人 |
| `applicant_name` | `String` | 原始申请人名称 |
| `assignee_name` | `String` | 当前专利权人名称 |
| `legal_status` | `String` | 法律状态（有效/无效/审查中） |
| `citation_count` | `Integer` | 引用专利数量 |
| `cited_by_count` | `Integer` | 被引数量 |

### 5.8 `BidItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 招投标记录 ID |
| `role` | `String` | 企业角色（中标方/投标方/招标方） |
| `announcement_title` | `String` | 公告标题 |
| `counterparty_name` | `String` | 对方企业名称 |
| `counterparty_code` | `String` | 对方信用代码 |
| `announcement_date` | `String` | 公告日期（`yyyy-MM-dd`） |

### 5.9 `RiskDetailItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `case_no` | `String` | 案号 |
| `case_title` | `String` | 案件标题 |
| `case_cause` | `String` | 案由 |
| `court_name` | `String` | 法院 |
| `filing_date` | `String` | 申请日期 |
| `publish_date` | `String` | 发布日期 |
| `judgment_date` | `String` | 判决日期 |
| `party_role` | `String` | 当事人角色（原告/被告/被执行人等） |
| `is_history` | `Integer` | 是否历史（0=当前/1=历史） |

### 5.10 `RiskGroupItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `risk_type` | `String` | 风险类型编码 |
| `risk_name` | `String` | 风险类型中文名 |
| `risk_category` | `String` | 风险大类（judicial/risk/penalty） |
| `count` | `Integer` | 返回数量，默认 4，最大 10 |
| `latest_items` | `List<RiskDetailItem>` | 该组最新几条明细（请求 size） |

### 5.11 `GraphNodeItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `node_key` | `String` | 要拓展的节点 vid |
| `node_type` | `String` | 环节类型（1=上游/2=中游/3=下游） |
| `name` | `String` | 简称（如 `深圳市`） |
| `weight` | `BigDecimal` | 权重/得分 |
| `props` | `Map<String,Object>` | 节点扩展属性（类型相关，文档为自由 object） |
| `tags` | `List<String>` | 标签编码列表（如 `high_tech`/`little_giant`） |

### 5.12 `GraphEdgeItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `src_key` | `String` | 边起点节点键 |
| `dst_key` | `String` | 边终点节点键 |
| `relation_type` | `String` | 关系类型（投资方/被投资方/招标方/中标方） |
| `weight` | `BigDecimal` | 权重/得分 |
| `props` | `Map<String,Object>` | 边扩展属性 |

### 5.13 `FeaturedEnterpriseItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `org_id` | `String` | 企业唯一标识（32 位 MD5） |
| `name_cn` | `String` | 企业名称 |
| `logo_url` | `String` | 企业 logo（v9.0 新增） |
| `tags` | `List<String>` | 标签编码列表（如 `high_tech`/`little_giant`） |
| `industry_chain_names` | `List<String>` | 产业链名称数组 |
| `node_name` | `String` | 环节名称（如 `集成电路设计`） |
| `node_stage` | `Integer` | 产业链环节（1=上游/2=中游/3=下游），不传则返回全部 3 组 |
| `node_stage_name` | `String` | 环节名称（上游/中游/下游） |
| `competitiveness_score` | `BigDecimal` | 综合竞争力评分（0-100） |
| `enterprise_scale` | `String` | 企业规模（`大型`/`中型`/`小型`/`微型`/`规上`） |
| `company_type` | `String` | 企业类型（有限责任公司/股份有限公司等） |
| `region_text` | `String` | 地区文本（省-市-区拼接） |
| `province` | `String` | 省份（如 `广东省`） |
| `city` | `String` | 深圳区界 GeoJSON |
| `district` | `String` | eq, neq, in（区县映射到 city） |
| `registered_capital_value` | `BigDecimal` | 注册资本（万元） |
| `operating_status` | `String` | 经营状态（在营/注销/迁出/吊销） |

### 5.14 `KeyChainGroupItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `node_stage` | `Integer` | 产业链环节（1=上游/2=中游/3=下游），不传则返回全部 3 组 |
| `node_stage_name` | `String` | 环节名称（上游/中游/下游） |
| `total` | `Integer` | 各产业企业数合计（不去重，含重复） |
| `enterprises` | `List<FeaturedEnterpriseItem>` | 企业列表（分页后） |

### 5.15 `TypeScaleRowItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `company_type` | `String` | 企业类型（有限责任公司/股份有限公司等） |
| `scales` | `List<TypeScaleCell>` | 规模列表 |

### 5.16 `TypeScaleCell`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `enterprise_scale` | `String` | 企业规模（`大型`/`中型`/`小型`/`微型`/`规上`） |
| `enterprise_count` | `Integer` | 该产业链下企业数 |

### 5.17 `DistributionMapItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `region_id` | `String` | 国标行政区编码（v9.0 新增，如 440300） |
| `region_name` | `String` | 区县名称（如南山区） |
| `enterprise_count` | `Long` | 该产业链下企业数 |
| `new_enterprise_count` | `Long` | 新增企业数（最近一周成立） |
| `ratio` | `BigDecimal` | 占比百分比 |

### 5.18 `DistributionKpi`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `total_enterprise_count` | `Long` | 该维度企业总数 |
| `covered_regions` | `Integer` | 覆盖地区数 |
| `new_enterprise_count` | `Long` | 新增企业数（最近一周成立） |

### 5.19 `ChainCountItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `chain_code` | `String` | 产业编码（如 `IC001`），不能为 `ALL` |
| `chain_name` | `String` | 产业链名称 |
| `enterprise_count` | `Integer` | 该产业链下企业数 |

### 5.20 `GrowthTrendItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `year` | `Integer` | 最新年份 |
| `month` | `Integer` | 月份（1-12） |
| `new_enterprise_count` | `Integer` | 新增企业数（最近一周成立） |
| `label` | `String` | 月份标签（如 `2026-06`） |

### 5.21 `DistrictHeatItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `region_id` | `String` | 国标行政区编码（v9.0 新增，如 440300） |
| `region_name` | `String` | 区县名称（如南山区） |
| `enterprise_total` | `Integer` | 深圳企业总数（DWD shenzhen_summary: stat_type='enterprise_total'） |
| `heat_level` | `Integer` | 热度等级（1-5，5 最热） |

### 5.22 `YearCountItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `year` | `Integer` | 最新年份 |
| `enterprise_count` | `Integer` | 该产业链下企业数 |

### 5.23 `CumulativeCountItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `year` | `Integer` | 最新年份 |
| `cumulative_count` | `Integer` | 该年及之前成立的企业累计数 |

### 5.24 `HotKeywordItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `keyword` | `String` | 关键词（企业名/曾用名/经营范围/主要产品 + 统一社会信用代码精确/前缀匹配） |
| `count` | `Long` | 返回数量，默认 4，最大 10 |

### 5.25 `BucketItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `key` | `String` | 聚合键值 |
| `doc_count` | `Long` | 文档数（企业数） |

### 5.26 `ExecutiveItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `name` | `String` | 高管姓名 |
| `position` | `String` | 高管职务 |

### 5.27 `InnovationCarrierItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `carrier_type` | `String` | 载体类型 |
| `carrier_level` | `String` | 载体等级 |
| `carrier_name` | `String` | 载体名称 |
| `create_year` | `Integer` | 创建年份 |

### 5.28 `QualificationItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `type` | `String` | 类型 tag/carrier/listing |
| `code` | `String` | `0` 表示成功；非 `0` 表示业务错误 |
| `value` | `String` | 值/级别 |
| `name` | `String` | 简称（如 `深圳市`） |

### 5.29 `InvestItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `inv_org_id` | `String` | 被投企业 id |
| `inv_name` | `String` | 被投企业名称 |
| `inv_external_id` | `String` | 被投企业信用代码 |
| `investment_amount` | `BigDecimal` | 投资金额 |
| `investment_ratio` | `BigDecimal` | 股权占比（%） |

### 5.30 `ShareholderItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `shareholder_name` | `String` | 股东名称 |
| `shareholder_type` | `String` | 股东类型（企业法人/自然人） |
| `investment_ratio` | `BigDecimal` | 股权占比（%） |
| `subscribed_capital` | `BigDecimal` | 认缴出资额（万元） |
| `paid_in_capital` | `BigDecimal` | 实缴出资额（万元） |

### 5.31 `FinancingEventItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `funding_round` | `String` | 融资轮次（天使轮/A轮/B轮/C轮/战略融资等） |
| `funding_amount` | `BigDecimal` | 融资金额（万元） |
| `funding_currency_code` | `String` | 币种 |
| `post_valuation` | `BigDecimal` | 投后估值（万元） |
| `completion_date` | `String` | 完成日期 |
| `investors_name` | `String` | 投资方名称（逗号分隔） |

### 5.32 `ProfileSupplyChainItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `related_name` | `String` | 关联方企业名 |
| `relation_type` | `String` | 关系类型（投资方/被投资方/招标方/中标方） |
| `related_code` | `String` | 关联方信用代码 |

### 5.33 `PatentHistoryItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `year` | `Integer` | 最新年份 |
| `apply_count` | `Integer` | 当年申请数 |
| `grant_count` | `Integer` | 当年授权数 |
| `valid_count` | `Integer` | 当年有效数 |
| `invention_count` | `Integer` | 当年发明专利数 |
| `citation_count` | `Integer` | 引用专利数量 |
| `latest_patent_date` | `String` | 当年最新申请日期 |
| `latest_grant_date` | `String` | 当年最新授权日期 |

### 5.34 `KeyChainSubjectItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `chain_code` | `String` | 产业编码（如 `IC001`），不能为 `ALL` |
| `chain_name` | `String` | 产业链名称 |
| `enterprise_count` | `Integer` | 该产业链下企业数 |

### 5.35 `KeyQualificationStatItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `tag_code` | `String` | tag_value 示例 |
| `tag_name` | `String` | 标签中文名（如 `高新技术企业`） |
| `enterprise_count` | `Integer` | 该产业链下企业数 |

### 5.36 `IndustryChainItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `chain_name` | `String` | 产业链名称 |
| `node_name` | `String` | 节点名称 |
| `node_stage_name` | `String` | 节点阶段名称 |

### 5.37 `NewsItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `news_id` | `String` | 资讯主键 |
| `title` | `String` | 资讯标题 |
| `summary` | `String` | 资讯摘要 |
| `source` | `String` | 资讯来源 |
| `date` | `String` | 资讯日期 |
| `url` | `String` | 原文链接 |
| `content_type` | `String` | 内容类型 |

### 5.38 `CompareItem`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `org_id` | `String` | 企业唯一标识 |
| `social_credit_code` | `String` | 统一社会信用代码 |
| `name_cn` | `String` | 企业中文名称 |
| `lerep` | `String` | 法定代表人 |
| `province` | `String` | 所在省份 |
| `city` | `String` | 所在城市 |
| `incorporation_year` | `Integer` | 成立年份 |
| `incorporation_date` | `String` | 成立日期 |
| `registered_capital_value` | `BigDecimal` | 注册资本 |
| `capital_currency_code` | `String` | 资本币种或金额单位 |
| `listing_status` | `String` | 上市状态 |
| `stock_code` | `String` | 股票代码 |
| `stock_type` | `String` | 股票类别 |
| `listed_date` | `String` | 上市或挂牌日期 |
| `industry_class` | `String` | 行业分类编码 |
| `industry_class_name` | `String` | 行业分类名称 |
| `main_activities` | `String` | 主营业务描述 |
| `enterprise_scale` | `String` | 企业规模 |
| `operating_status` | `String` | 经营状态 |
| `competitiveness_score` | `BigDecimal` | 综合竞争力得分 |
| `chain_position_text` | `String` | 产业链位置描述 |
| `risk_level` | `String` | 风险等级 |
| `tags` | `List<TagItem>` | 标签明细列表 |
| `tags_flat` | `List<String>` | 标签编码平铺列表 |
| `industry_chain_names_flat` | `List<String>` | 产业链名称平铺列表 |
| `financials` | `List<FinancialRecord>` | 财务历史列表 |
| `statistics` | `List<Statistics>` | 统计指标列表 |

## 6. 统一说明

1. 业务接口全部 `POST` + JSON Body；JSON 字段为 `snake_case`。
2. **字段是否存在**以 Java DTO 为准；**中文说明**优先 Java javadoc，缺省回填 Python `API-接口文档.md`。
3. 分页：画像/风险多用 `page`+`size`；重点/明星/深圳列表用 `page`+`page_size`。
4. 风险 18 类共用 `RiskDetailItem`；类型特有字段由 Jackson `ignoreUnknown` 忽略。
5. 图谱 `nodes[].props` / `edges[].props` 为开放 `Map`。
6. 不在范围：`GET /healthz`；`ENT-JAVA-SEARCH-BIZ`（Java 自建）。

## 7. 代码落点

| 层 | 路径 |
|---|---|
| Controllers | `…/controller/Enterprise*Controller.java` |
| Feign | `…/feign/RemoteEnterprisePythonClient.java` |
| 响应 DTO | `EnterpriseResponseDTOs.java`、`EnterpriseExtendedDTOs.java` |
| 请求 DTO | `Enterprise*Request.java` |
| Python 字段说明 | `demo-svc-topic-py/docs/API-接口文档.md` |

---

**维护**：结构变更改 Java DTO 后重同步本文；中文说明可从 Python 文档回填。
