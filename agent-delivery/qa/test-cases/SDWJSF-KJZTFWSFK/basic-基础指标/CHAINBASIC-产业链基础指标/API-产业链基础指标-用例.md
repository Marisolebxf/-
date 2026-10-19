# 智能服务集群-科技专题服务算法库测试用例（产业链基础指标 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：基础指标 / 产业链基础指标  
> **catalog**：`entry_id=chain.basic` · `catalog_page_id=chain.basic` · path `/chain/basic`  
> **A 线对照**：`fp-split-by-api-run/work/L01.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批1）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 产业链列表 | chain.basic.list |
| 2 | A1 产业市场规模 | chain.basic.market-stats |
| 3 | A2 产业企业规模 | chain.basic.enterprise-stats |
| 4 | A3 产业机构规模 | chain.basic.institution-stats |
| 5 | A4 产业投融资规模 | chain.basic.investment-stats |
| 6 | A5 全球产业区域分布 | chain.basic.global-dist |
| 7 | A6 全国产业分布 | chain.basic.national-dist |
| 8 | A7 产业动态资讯 | chain.basic.news-stats |
| 9 | A8 深圳产业要素 | chain.basic.sz-elements |
| 10 | A9 深圳产业分布 | chain.basic.sz-dist |

**chainId 试调取值**：文档示例 `INB1701`（`GET /innov/v1/industry/list` 首条 `chain_id` 可替换，其余组合表引用该值）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-00889**～**API-00911**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.basic`、组合 id（如有）。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00889 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | 产业链列表 | 产业链列表无参查询返回文档示例中的列表字段结构 | 1、无业务前置 | 1.GET /innov/v1/industry/list（无查询参数） | 1、返回 body 的 data 为数组；2、元素含 chain_id（string）、chain_name（string）；3、sampleResponse 示例还含 cluster_name、map_status、description（string），非空元素中应出现这些字段 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/list | M_CHAIN_TOTAL_COUNT | INTEG | | | endpoint_id=chain.basic.list catalog_page_id=chain.basic 组合=— 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00890 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | A1 产业市场规模 | A1 产业市场规模按文档示例 chainId、statYear 查询 | 1、chainId 使用文档示例 INB1701 | 1.GET /innov/v1/industry/market-stats，查询参数取组合 MKT-01 | 1、返回 body 的 data 为数组；2、元素含 stat_year（number）、total_revenue（number，responseFields 总营收(万)）、growth_rate（number）；3、结构与 sampleResponse 一致（示例 stat_year 2023/2024/2025 及对应 total_revenue、growth_rate） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats | M_CHAIN_MARKET_SIZE | INTEG | | | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00891 | 基础指标 | 产业链基础指标 | 备选-参数组合 | 省略 statYear | 产业链基础指标 | A1 产业市场规模 | A1 产业市场规模仅传 chainId、不传可选 statYear | 1、chainId=INB1701 | 1.GET /innov/v1/industry/market-stats，查询参数取组合 MKT-04 | 1、返回 body 的 data 为数组；2、元素仍含 stat_year、total_revenue、growth_rate（number），结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats | M_CHAIN_MARKET_SIZE | INTEG | | | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00892 | 基础指标 | 产业链基础指标 | 异常-入参-缺chainId | — | 产业链基础指标 | A1 产业市场规模 | A1 产业市场规模不传 chainId | 1、其余参数保持合法 | 1.GET /innov/v1/industry/market-stats，查询参数取组合 MKT-02 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 total_revenue 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats | | INTEG | | | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00893 | 基础指标 | 产业链基础指标 | 异常-入参-非法statYear | — | 产业链基础指标 | A1 产业市场规模 | A1 产业市场规模 statYear 非法 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/market-stats，查询参数取组合 MKT-05 | 1、返回 body 的 message 或 msg 说明 statYear 非法或无法解析；2、不返回含可信 total_revenue 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats | | INTEG | | | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00894 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | A2 产业企业规模 | A2 产业企业规模按文档 sampleRequest 仅 chainId 查询 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/enterprise-stats，查询参数取组合 ENT-01 | 1、返回 body 的 data 为数组；2、元素含 stat_year（number）、enterprise_count（number，responseFields 企业数）、growth_rate（number）；3、与 sampleResponse 结构一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats | M_CHAIN_ENTERPRISE_COUNT | INTEG | | | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00895 | 基础指标 | 产业链基础指标 | 备选-参数组合 | 省略 statYear | 产业链基础指标 | A2 产业企业规模 | A2 产业企业规模传 chainId 与 statYear=2025 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/enterprise-stats，查询参数取组合 ENT-04 | 1、返回 body 的 data 为数组；2、元素含 stat_year、enterprise_count、growth_rate（number），结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats | M_CHAIN_ENTERPRISE_COUNT | INTEG | | | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00896 | 基础指标 | 产业链基础指标 | 异常-入参-缺chainId | — | 产业链基础指标 | A2 产业企业规模 | A2 产业企业规模不传 chainId | 1、statYear=2025（可选，保持合法） | 1.GET /innov/v1/industry/enterprise-stats，查询参数取组合 ENT-02 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 enterprise_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats | | INTEG | | | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00897 | 基础指标 | 产业链基础指标 | 异常-入参-非法statYear | — | 产业链基础指标 | A2 产业企业规模 | A2 产业企业规模 statYear 非法 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/enterprise-stats，查询参数取组合 ENT-05 | 1、返回 body 的 message 或 msg 说明 statYear 非法或无法解析；2、不返回含可信 enterprise_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats | | INTEG | | | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00898 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | A3 产业机构规模 | A3 产业机构规模按文档 chainId 查询返回机构规模字段 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/institution-stats，查询参数取组合 INS-01 | 1、返回 body 的 data 为数组；2、元素含 stat_year（number）、institution_count（number，responseFields 机构数）、growth_rate（number）；3、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/institution-stats | | INTEG | | | endpoint_id=chain.basic.institution-stats catalog_page_id=chain.basic 组合=INS-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00899 | 基础指标 | 产业链基础指标 | 异常-入参-缺chainId | — | 产业链基础指标 | A3 产业机构规模 | A3 产业机构规模不传 chainId | 1、无 | 1.GET /innov/v1/industry/institution-stats，查询参数取组合 INS-02 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 institution_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/institution-stats | | INTEG | | | endpoint_id=chain.basic.institution-stats catalog_page_id=chain.basic 组合=INS-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00900 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | A4 产业投融资规模 | A4 产业投融资规模按文档 chainId 查询 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/investment-stats，查询参数取组合 INV-01 | 1、返回 body 的 data 为数组；2、元素含 stat_year（number）、total_amount（number，responseFields 投融资金额(万)）、amount_growth_rate（number）；3、与 sampleResponse 结构一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/investment-stats | | INTEG | | | endpoint_id=chain.basic.investment-stats catalog_page_id=chain.basic 组合=INV-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00901 | 基础指标 | 产业链基础指标 | 异常-入参-缺chainId | — | 产业链基础指标 | A4 产业投融资规模 | A4 产业投融资规模不传 chainId | 1、无 | 1.GET /innov/v1/industry/investment-stats，查询参数取组合 INV-02 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 total_amount 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/investment-stats | | INTEG | | | endpoint_id=chain.basic.investment-stats catalog_page_id=chain.basic 组合=INV-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00902 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | A5 全球产业区域分布 | A5 全球产业区域分布按文档 chainId 查询 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/global-dist，查询参数取组合 GLO-01 | 1、返回 body 的 data 为数组；2、元素含 country（string，responseFields 国家/地区）、enterprise_count（number）、institution_count（number）；3、与 sampleResponse 结构一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/global-dist | | INTEG | | | endpoint_id=chain.basic.global-dist catalog_page_id=chain.basic 组合=GLO-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00903 | 基础指标 | 产业链基础指标 | 异常-入参-缺chainId | — | 产业链基础指标 | A5 全球产业区域分布 | A5 全球产业区域分布不传 chainId | 1、无 | 1.GET /innov/v1/industry/global-dist，查询参数取组合 GLO-02 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 country 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/global-dist | | INTEG | | | endpoint_id=chain.basic.global-dist catalog_page_id=chain.basic 组合=GLO-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00904 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | A6 全国产业分布 | A6 全国产业分布按文档 chainId 查询 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/national-dist，查询参数取组合 NAT-01 | 1、返回 body 的 data 为数组；2、元素含 province（string，responseFields 省份）、enterprise_count（number）；3、与 sampleResponse 结构一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/national-dist | | INTEG | | | endpoint_id=chain.basic.national-dist catalog_page_id=chain.basic 组合=NAT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00905 | 基础指标 | 产业链基础指标 | 异常-入参-缺chainId | — | 产业链基础指标 | A6 全国产业分布 | A6 全国产业分布不传 chainId | 1、无 | 1.GET /innov/v1/industry/national-dist，查询参数取组合 NAT-02 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 province 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/national-dist | | INTEG | | | endpoint_id=chain.basic.national-dist catalog_page_id=chain.basic 组合=NAT-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00906 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | A7 产业动态资讯 | A7 产业动态资讯按文档 chainId 查询 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/news-stats，查询参数取组合 NEW-01 | 1、返回 body 的 data 为数组；2、元素含 stat_month（string）、news_count（number，responseFields 资讯数）、hot_count（number）；3、与 sampleResponse 结构一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/news-stats | | INTEG | | | endpoint_id=chain.basic.news-stats catalog_page_id=chain.basic 组合=NEW-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00907 | 基础指标 | 产业链基础指标 | 异常-入参-缺chainId | — | 产业链基础指标 | A7 产业动态资讯 | A7 产业动态资讯不传 chainId | 1、无 | 1.GET /innov/v1/industry/news-stats，查询参数取组合 NEW-02 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 news_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/news-stats | | INTEG | | | endpoint_id=chain.basic.news-stats catalog_page_id=chain.basic 组合=NEW-02 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00908 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | A8 深圳产业要素 | A8 深圳产业要素按文档 chainId 查询 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/sz-elements，查询参数取组合 SZE-01 | 1、返回 body 的 data 为数组（或等价载荷）；2、元素含 enterprise_count、institution_count（number，responseFields 深圳企业数/机构数）；3、sampleResponse 还含 talent_count、total_revenue（number），非空载荷中应出现 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-elements | M_CHAIN_SZ_ENTERPRISE_COUNT | INTEG | | | endpoint_id=chain.basic.sz-elements catalog_page_id=chain.basic 组合=SZE-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00909 | 基础指标 | 产业链基础指标 | 异常-入参-缺chainId | — | 产业链基础指标 | A8 深圳产业要素 | A8 深圳产业要素不传 chainId | 1、无 | 1.GET /innov/v1/industry/sz-elements，查询参数取组合 SZE-02 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 enterprise_count/institution_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-elements | | INTEG | | | endpoint_id=chain.basic.sz-elements catalog_page_id=chain.basic 组合=SZE-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00910 | 基础指标 | 产业链基础指标 | 主流程 | — | 产业链基础指标 | A9 深圳产业分布 | A9 深圳产业分布按文档 chainId 查询 | 1、chainId=INB1701 | 1.GET /innov/v1/industry/sz-dist，查询参数取组合 SZD-01 | 1、返回 body 的 data 为数组；2、元素含 district（string，responseFields 行政区）、enterprise_count（number）；3、与 sampleResponse 结构一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-dist | M_CHAIN_SZ_ENTERPRISE_COUNT | INTEG | | | endpoint_id=chain.basic.sz-dist catalog_page_id=chain.basic 组合=SZD-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00911 | 基础指标 | 产业链基础指标 | 异常-入参-缺chainId | — | 产业链基础指标 | A9 深圳产业分布 | A9 深圳产业分布不传 chainId | 1、无 | 1.GET /innov/v1/industry/sz-dist，查询参数取组合 SZD-02 | 1、返回 body 的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 district 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-dist | | INTEG | | | endpoint_id=chain.basic.sz-dist catalog_page_id=chain.basic 组合=SZD-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MKT-01 | chain.basic.market-stats | chainId=INB1701；statYear=2025 | 主路径全参（sampleRequest） |
| MKT-02 | chain.basic.market-stats | 不传 chainId；statYear=2025 | 缺必填 chainId |
| MKT-04 | chain.basic.market-stats | chainId=INB1701；不传 statYear | 省略可选 statYear |
| MKT-05 | chain.basic.market-stats | chainId=INB1701；statYear=not-a-year | 非法 statYear |
| ENT-01 | chain.basic.enterprise-stats | chainId=INB1701 | 主路径（sampleRequest） |
| ENT-02 | chain.basic.enterprise-stats | 不传 chainId；statYear=2025 | 缺必填 chainId |
| ENT-04 | chain.basic.enterprise-stats | chainId=INB1701；statYear=2025 | 含可选 statYear |
| ENT-05 | chain.basic.enterprise-stats | chainId=INB1701；statYear=0 | 非法 statYear |
| INS-01 | chain.basic.institution-stats | chainId=INB1701 | 主路径 |
| INS-02 | chain.basic.institution-stats | 不传 chainId | 缺必填 chainId |
| INV-01 | chain.basic.investment-stats | chainId=INB1701 | 主路径 |
| INV-02 | chain.basic.investment-stats | 不传 chainId | 缺必填 chainId |
| GLO-01 | chain.basic.global-dist | chainId=INB1701 | 主路径 |
| GLO-02 | chain.basic.global-dist | 不传 chainId | 缺必填 chainId |
| NAT-01 | chain.basic.national-dist | chainId=INB1701 | 主路径 |
| NAT-02 | chain.basic.national-dist | 不传 chainId | 缺必填 chainId |
| NEW-01 | chain.basic.news-stats | chainId=INB1701 | 主路径 |
| NEW-02 | chain.basic.news-stats | 不传 chainId | 缺必填 chainId |
| SZE-01 | chain.basic.sz-elements | chainId=INB1701 | 主路径 |
| SZE-02 | chain.basic.sz-elements | 不传 chainId | 缺必填 chainId |
| SZD-01 | chain.basic.sz-dist | chainId=INB1701 | 主路径 |
| SZD-02 | chain.basic.sz-dist | 不传 chainId | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 产业链列表 | chain.basic.list | GET | /innov/v1/industry/list | — | available |
| A1 产业市场规模 | chain.basic.market-stats | GET | /innov/v1/industry/market-stats | chainId*；statYear? | available |
| A2 产业企业规模 | chain.basic.enterprise-stats | GET | /innov/v1/industry/enterprise-stats | chainId*；statYear? | available |
| A3 产业机构规模 | chain.basic.institution-stats | GET | /innov/v1/industry/institution-stats | chainId* | unavailable |
| A4 产业投融资规模 | chain.basic.investment-stats | GET | /innov/v1/industry/investment-stats | chainId* | available |
| A5 全球产业区域分布 | chain.basic.global-dist | GET | /innov/v1/industry/global-dist | chainId* | unavailable |
| A6 全国产业分布 | chain.basic.national-dist | GET | /innov/v1/industry/national-dist | chainId* | available |
| A7 产业动态资讯 | chain.basic.news-stats | GET | /innov/v1/industry/news-stats | chainId* | unavailable |
| A8 深圳产业要素 | chain.basic.sz-elements | GET | /innov/v1/industry/sz-elements | chainId* | available |
| A9 深圳产业分布 | chain.basic.sz-dist | GET | /innov/v1/industry/sz-dist | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.basic.list | API-00889 |
| chain.basic.market-stats | API-00890、00891、00892、00893 |
| chain.basic.enterprise-stats | API-00894、00895、00896、00897 |
| chain.basic.institution-stats | API-00898、00899 |
| chain.basic.investment-stats | API-00900、00901 |
| chain.basic.global-dist | API-00902、00903 |
| chain.basic.national-dist | API-00904、00905 |
| chain.basic.news-stats | API-00906、00907 |
| chain.basic.sz-elements | API-00908、00909 |
| chain.basic.sz-dist | API-00910、00911 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 10 个 title 均在功能点列出现且各有 ≥1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向 + 可选参数组合（A1/A2 statYear）+ 每参数 1 条反向
- [x] unavailable（A3/A5/A7）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] `coverage-fp.md` 已同步 API-00889～00911

**统计**：用例 **23** 条；编号闭区间 **API-00889**～**API-00911**（父控 R2-批1 分配）。
