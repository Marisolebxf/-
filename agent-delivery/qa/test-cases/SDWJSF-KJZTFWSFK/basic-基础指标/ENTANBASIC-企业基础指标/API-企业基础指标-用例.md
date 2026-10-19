# 智能服务集群-科技专题服务算法库测试用例（企业基础指标 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：基础指标 / 企业基础指标  
> **catalog**：`entry_id=entan.basic` · `catalog_page_id=entan.basic` · path `/entan/basic`  
> **A 线对照**：`fp-split-by-api-run/work/L02.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（下拉框 title 原文）

| # | title | endpoint_id | METHOD | path | status |
|---|--------|-------------|--------|------|--------|
| 1 | 筛选项 | entan.basic.filters | GET | /entan/v1/meta/filters | unavailable |
| 2 | 重点企业 | entan.basic.key-enterprises | GET | /entan/v1/key-enterprises | unavailable |
| 3 | 企业类型分布 | entan.basic.type-distribution | GET | /entan/v1/type-distribution | unavailable |
| 4 | 领域分布 | entan.basic.domain-distribution | GET | /entan/v1/domain-distribution | unavailable |
| 5 | 历年新增企业 | entan.basic.new-enterprises | GET | /entan/v1/new-enterprises | unavailable |
| 6 | 重点资讯统计 | entan.news.stats | GET | /entan/v1/news/stats | unavailable |
| 7 | 重点资讯明细 | entan.news.list | GET | /entan/v1/news | unavailable |

本页 7 个接口在 catalog 均为 `status=unavailable`；用例仍按各接口 `sampleRequest` / `sampleResponse` / `responseFields` 编写返回 body 预期，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-00912**～**API-00942**，共 31 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.basic`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00912 | 基础指标 | 企业基础指标 | 主流程 | 金样 | 企业基础指标 | 筛选项 | 筛选项无参请求返回文档中的四维筛选项字段 | 1、企业基础指标页筛选项数据可查询 | 1.GET /entan/v1/meta/filters（无查询参数） | 1、返回 body 的 data 为对象；2、含 industries（array）、cities（array）、domains（array）、years（array）；3、文档 sampleResponse 示例 industries 含「人工智能」、cities 含「深圳市」、domains 含「人工智能」「商业航天」、years 含 2024 与 2025（示例值说明形态，不断言固定计数） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/meta/filters | | INTEG | | | endpoint_id=entan.basic.filters catalog_page_id=entan.basic 组合=— 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00913 | 基础指标 | 企业基础指标 | 主流程 | 文档示例 | 企业基础指标 | 重点企业 | 重点企业按 catalog sampleRequest 全参查询返回重点企业清单字段 | 1、重点企业指标数据可查询 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-01 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number）；3、文档 sampleResponse 示例还含 headquarters_city、enterprise_scale、industry、patent_grant_count、tech_transaction_amount | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | M_ENT_TOTAL_COUNT | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00914 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传industry | 企业基础指标 | 重点企业 | 重点企业不传 industry 时仍返回文档清单字段结构 | 1、重点企业指标数据可查询 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-02 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number）；3、结构与 sampleResponse 一致，可为空数组 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00915 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传city | 企业基础指标 | 重点企业 | 重点企业不传 city 时仍返回文档清单字段结构 | 1、重点企业指标数据可查询 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-03 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00916 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传scale | 企业基础指标 | 重点企业 | 重点企业不传 scale 时仍返回文档清单字段结构 | 1、重点企业指标数据可查询 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-04 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00917 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传limit | 企业基础指标 | 重点企业 | 重点企业不传 limit 时仍返回文档清单字段结构 | 1、重点企业指标数据可查询 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-05 | 1、返回 body 的 data 为数组；2、元素含 enterprise_name（string）、key_score（number） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00918 | 基础指标 | 企业基础指标 | 异常-入参-非法industry | 重点企业 | 企业基础指标 | 重点企业 | 重点企业 industry 非法时返回该参数错误说明 | 1、重点企业接口可调用 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-06 | 1、返回 body 的 message 或 msg 说明 industry 缺失或非法；2、不返回含可信 key_score 的成功重点企业列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-06 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00919 | 基础指标 | 企业基础指标 | 异常-入参-非法city | 重点企业 | 企业基础指标 | 重点企业 | 重点企业 city 非法时返回该参数错误说明 | 1、重点企业接口可调用 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-07 | 1、返回 body 的 message 或 msg 说明 city 缺失或非法；2、不返回含可信 key_score 的成功重点企业列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-07 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00920 | 基础指标 | 企业基础指标 | 异常-入参-非法scale | 重点企业 | 企业基础指标 | 重点企业 | 重点企业 scale 非法时返回该参数错误说明 | 1、重点企业接口可调用 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-08 | 1、返回 body 的 message 或 msg 说明 scale 缺失或非法；2、不返回含可信 key_score 的成功重点企业列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-08 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00921 | 基础指标 | 企业基础指标 | 异常-入参-非法limit | 重点企业 | 企业基础指标 | 重点企业 | 重点企业 limit 非法时返回该参数错误说明 | 1、重点企业接口可调用 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-09 | 1、返回 body 的 message 或 msg 说明 limit 缺失或非法；2、不返回含可信 key_score 的成功重点企业列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-09 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00922 | 基础指标 | 企业基础指标 | 主流程 | 文档示例 | 企业基础指标 | 企业类型分布 | 企业类型分布在 year=2025 时返回 rows 类型分布 | 1、类型分布指标数据可查询 | 1.GET /entan/v1/type-distribution，查询参数取组合 TYP-01 | 1、返回 body 的 data 为对象；2、含 rows（array）；3、rows 元素含 type_name（string）、enterprise_count（number）；4、文档 sampleResponse 含 year=2025 及示例类型行 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/type-distribution | | INTEG | | | endpoint_id=entan.basic.type-distribution catalog_page_id=entan.basic 组合=TYP-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00923 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传year | 企业基础指标 | 企业类型分布 | 企业类型分布不传 year 时仍返回 rows 结构 | 1、类型分布指标数据可查询 | 1.GET /entan/v1/type-distribution，查询参数取组合 TYP-02 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 type_name、enterprise_count 字段 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/type-distribution | | INTEG | | | endpoint_id=entan.basic.type-distribution catalog_page_id=entan.basic 组合=TYP-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00924 | 基础指标 | 企业基础指标 | 异常-入参-非法year | 类型分布 | 企业基础指标 | 企业类型分布 | 企业类型分布 year 非法时返回该参数错误说明 | 1、类型分布接口可调用 | 1.GET /entan/v1/type-distribution，查询参数取组合 TYP-03 | 1、返回 body 的 message 或 msg 说明 year 缺失或非法；2、不返回含可信 rows.enterprise_count 的成功统计 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/type-distribution | | INTEG | | | endpoint_id=entan.basic.type-distribution catalog_page_id=entan.basic 组合=TYP-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00925 | 基础指标 | 企业基础指标 | 主流程 | 文档示例 | 企业基础指标 | 领域分布 | 领域分布在 year=2025 时返回 rows 领域分布与增长率 | 1、领域分布指标数据可查询 | 1.GET /entan/v1/domain-distribution，查询参数取组合 DOM-01 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 domain（string）、enterprise_count（number）、growth_rate（number）；3、文档 sampleResponse 示例 domain=「人工智能」 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/domain-distribution | | INTEG | | | endpoint_id=entan.basic.domain-distribution catalog_page_id=entan.basic 组合=DOM-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00926 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传year | 企业基础指标 | 领域分布 | 领域分布不传 year 时仍返回 rows 结构 | 1、领域分布指标数据可查询 | 1.GET /entan/v1/domain-distribution，查询参数取组合 DOM-02 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 domain、enterprise_count、growth_rate | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/domain-distribution | | INTEG | | | endpoint_id=entan.basic.domain-distribution catalog_page_id=entan.basic 组合=DOM-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00927 | 基础指标 | 企业基础指标 | 异常-入参-非法year | 领域分布 | 企业基础指标 | 领域分布 | 领域分布 year 非法时返回该参数错误说明 | 1、领域分布接口可调用 | 1.GET /entan/v1/domain-distribution，查询参数取组合 DOM-03 | 1、返回 body 的 message 或 msg 说明 year 缺失或非法；2、不返回含可信 growth_rate 的成功统计 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/domain-distribution | | INTEG | | | endpoint_id=entan.basic.domain-distribution catalog_page_id=entan.basic 组合=DOM-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00928 | 基础指标 | 企业基础指标 | 主流程 | 文档示例 | 企业基础指标 | 历年新增企业 | 历年新增企业在 domain=ALL 时返回 rows 新增趋势 | 1、新增企业指标数据可查询 | 1.GET /entan/v1/new-enterprises，查询参数取组合 NEW-01 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 stat_year（number）、new_count（number）、cumulative_count（number）；3、文档 sampleResponse 含 2023、2024 示例行 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/new-enterprises | M_ENT_NEW_COUNT_Y | INTEG | | | endpoint_id=entan.basic.new-enterprises catalog_page_id=entan.basic 组合=NEW-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00929 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传domain | 企业基础指标 | 历年新增企业 | 历年新增企业不传 domain 时仍返回 rows 结构 | 1、新增企业指标数据可查询 | 1.GET /entan/v1/new-enterprises，查询参数取组合 NEW-02 | 1、返回 body 的 data 含 rows（array）；2、rows 元素含 stat_year、new_count、cumulative_count | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/new-enterprises | | INTEG | | | endpoint_id=entan.basic.new-enterprises catalog_page_id=entan.basic 组合=NEW-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00930 | 基础指标 | 企业基础指标 | 异常-入参-非法domain | 新增企业 | 企业基础指标 | 历年新增企业 | 历年新增企业 domain 非法时返回该参数错误说明 | 1、新增企业接口可调用 | 1.GET /entan/v1/new-enterprises，查询参数取组合 NEW-03 | 1、返回 body 的 message 或 msg 说明 domain 缺失或非法；2、不返回含可信 new_count 的成功趋势 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/new-enterprises | | INTEG | | | endpoint_id=entan.basic.new-enterprises catalog_page_id=entan.basic 组合=NEW-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00931 | 基础指标 | 企业基础指标 | 主流程 | 全部类型 | 企业基础指标 | 重点资讯统计 | 重点资讯统计 news_type 为空（全部）时返回月度统计字段 | 1、资讯统计指标数据可查询 | 1.GET /entan/v1/news/stats，查询参数取组合 NST-01 | 1、返回 body 的 data 为数组；2、元素含 stat_month（string）、news_type（string）、type_name（string）、news_count（number）、total_amount（number）、growth_rate（number）；3、文档 sampleResponse 含 financing、product 等示例行 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news/stats | M_ENT_NEWS_STAT | INTEG | | | endpoint_id=entan.news.stats catalog_page_id=entan.basic 组合=NST-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00932 | 基础指标 | 企业基础指标 | 备选-参数组合 | 融资类型 | 企业基础指标 | 重点资讯统计 | 重点资讯统计 news_type=financing 时返回融资类统计字段 | 1、资讯统计指标数据可查询 | 1.GET /entan/v1/news/stats，查询参数取组合 NST-02 | 1、返回 body 的 data 为数组；2、元素含 stat_month、news_type、type_name、news_count、total_amount、growth_rate；3、news_type 为 financing 或 type_name 为「融资」 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news/stats | | INTEG | | | endpoint_id=entan.news.stats catalog_page_id=entan.basic 组合=NST-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00933 | 基础指标 | 企业基础指标 | 异常-入参-非法news_type | 资讯统计 | 企业基础指标 | 重点资讯统计 | 重点资讯统计 news_type 非法时返回该参数错误说明 | 1、资讯统计接口可调用 | 1.GET /entan/v1/news/stats，查询参数取组合 NST-03 | 1、返回 body 的 message 或 msg 说明 news_type 缺失或非法；2、不返回含可信 news_count 的成功统计 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news/stats | | INTEG | | | endpoint_id=entan.news.stats catalog_page_id=entan.basic 组合=NST-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00934 | 基础指标 | 企业基础指标 | 主流程 | 文档示例 | 企业基础指标 | 重点资讯明细 | 重点资讯明细按 sampleRequest 分页参数返回 list 与分页元数据 | 1、资讯明细数据可查询 | 1.GET /entan/v1/news，查询参数取组合 NLST-01 | 1、返回 body 的 data 为对象；2、含 list（array）、total（number）、page（number）、size（number）；3、list 元素含 enterprise_name、news_type、title、amount、finance_round、counterparty、region、publish_time（见 sampleResponse） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | M_ENT_NEWS_DETAIL | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00935 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传news_type | 企业基础指标 | 重点资讯明细 | 重点资讯明细不传 news_type 时仍返回 list 分页结构 | 1、资讯明细数据可查询 | 1.GET /entan/v1/news，查询参数取组合 NLST-02 | 1、返回 body 的 data 含 list（array）、total、page、size | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00936 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传keyword | 企业基础指标 | 重点资讯明细 | 重点资讯明细不传 keyword 时仍返回 list 分页结构 | 1、资讯明细数据可查询 | 1.GET /entan/v1/news，查询参数取组合 NLST-03 | 1、返回 body 的 data 含 list（array）、total、page、size | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00937 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传page | 企业基础指标 | 重点资讯明细 | 重点资讯明细不传 page 时仍返回 list 分页结构 | 1、资讯明细数据可查询 | 1.GET /entan/v1/news，查询参数取组合 NLST-04 | 1、返回 body 的 data 含 list（array）、total、page、size | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00938 | 基础指标 | 企业基础指标 | 备选-参数组合 | 不传size | 企业基础指标 | 重点资讯明细 | 重点资讯明细不传 size 时仍返回 list 分页结构 | 1、资讯明细数据可查询 | 1.GET /entan/v1/news，查询参数取组合 NLST-05 | 1、返回 body 的 data 含 list（array）、total、page、size | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00939 | 基础指标 | 企业基础指标 | 异常-入参-非法news_type | 资讯明细 | 企业基础指标 | 重点资讯明细 | 重点资讯明细 news_type 非法时返回该参数错误说明 | 1、资讯明细接口可调用 | 1.GET /entan/v1/news，查询参数取组合 NLST-06 | 1、返回 body 的 message 或 msg 说明 news_type 缺失或非法；2、不返回含可信 list 的成功分页 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-06 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00940 | 基础指标 | 企业基础指标 | 异常-入参-非法keyword | 资讯明细 | 企业基础指标 | 重点资讯明细 | 重点资讯明细 keyword 超长非法时返回该参数错误说明 | 1、资讯明细接口可调用 | 1.GET /entan/v1/news，查询参数取组合 NLST-07 | 1、返回 body 的 message 或 msg 说明 keyword 非法；2、不返回含可信 list 的成功分页 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-07 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00941 | 基础指标 | 企业基础指标 | 异常-入参-非法page | 资讯明细 | 企业基础指标 | 重点资讯明细 | 重点资讯明细 page 非法类型时返回该参数错误说明 | 1、资讯明细接口可调用 | 1.GET /entan/v1/news，查询参数取组合 NLST-08 | 1、返回 body 的 message 或 msg 说明 page 缺失或非法；2、不返回含可信 list 的成功分页 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-08 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00942 | 基础指标 | 企业基础指标 | 异常-入参-非法size | 资讯明细 | 企业基础指标 | 重点资讯明细 | 重点资讯明细 size 非法时返回该参数错误说明 | 1、资讯明细接口可调用 | 1.GET /entan/v1/news，查询参数取组合 NLST-09 | 1、返回 body 的 message 或 msg 说明 size 缺失或非法；2、不返回含可信 list 的成功分页 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-09 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| KEY-01 | entan.basic.key-enterprises | industry=；city=；scale=；limit=150（catalog sampleRequest） | 主路径全参 |
| KEY-02 | entan.basic.key-enterprises | 不传 industry；city=深圳市；scale=大；limit=150 | 省略 industry |
| KEY-03 | entan.basic.key-enterprises | industry=人工智能；不传 city；scale=大；limit=150 | 省略 city |
| KEY-04 | entan.basic.key-enterprises | industry=人工智能；city=深圳市；不传 scale；limit=150 | 省略 scale |
| KEY-05 | entan.basic.key-enterprises | industry=人工智能；city=深圳市；scale=大；不传 limit | 省略 limit |
| KEY-06 | entan.basic.key-enterprises | industry=__invalid__；city=深圳市；scale=大；limit=150 | 只破坏 industry |
| KEY-07 | entan.basic.key-enterprises | industry=人工智能；city=__invalid__；scale=大；limit=150 | 只破坏 city |
| KEY-08 | entan.basic.key-enterprises | industry=人工智能；city=深圳市；scale=__invalid__；limit=150 | 只破坏 scale |
| KEY-09 | entan.basic.key-enterprises | industry=人工智能；city=深圳市；scale=大；limit=-1 | 只破坏 limit |
| TYP-01 | entan.basic.type-distribution | year=2025 | 主路径 |
| TYP-02 | entan.basic.type-distribution | 不传 year | 省略 year |
| TYP-03 | entan.basic.type-distribution | year=__invalid__ | 非法 year |
| DOM-01 | entan.basic.domain-distribution | year=2025 | 主路径 |
| DOM-02 | entan.basic.domain-distribution | 不传 year | 省略 year |
| DOM-03 | entan.basic.domain-distribution | year=__invalid__ | 非法 year |
| NEW-01 | entan.basic.new-enterprises | domain=ALL | 主路径 |
| NEW-02 | entan.basic.new-enterprises | 不传 domain | 省略 domain |
| NEW-03 | entan.basic.new-enterprises | domain=__invalid__ | 非法 domain |
| NST-01 | entan.news.stats | news_type=（空，catalog sampleRequest） | 全部类型 |
| NST-02 | entan.news.stats | news_type=financing | 文档选项合法值 |
| NST-03 | entan.news.stats | news_type=__invalid__ | 非法 news_type |
| NLST-01 | entan.news.list | news_type=；keyword=；page=1；size=15（catalog sampleRequest） | 主路径全参 |
| NLST-02 | entan.news.list | 不传 news_type；keyword=；page=1；size=15 | 省略 news_type |
| NLST-03 | entan.news.list | news_type=financing；不传 keyword；page=1；size=15 | 省略 keyword |
| NLST-04 | entan.news.list | news_type=financing；keyword=；不传 page；size=15 | 省略 page |
| NLST-05 | entan.news.list | news_type=financing；keyword=；page=1；不传 size | 省略 size |
| NLST-06 | entan.news.list | news_type=__invalid__；page=1；size=15 | 只破坏 news_type |
| NLST-07 | entan.news.list | news_type=financing；keyword=（重复字符超 512）；page=1；size=15 | 只破坏 keyword |
| NLST-08 | entan.news.list | news_type=financing；page=abc；size=15 | 只破坏 page |
| NLST-09 | entan.news.list | news_type=financing；page=1；size=-1 | 只破坏 size |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | title | METHOD | path | status | params |
|-------------|-------|--------|------|--------|--------|
| entan.basic.filters | 筛选项 | GET | /entan/v1/meta/filters | unavailable | — |
| entan.basic.key-enterprises | 重点企业 | GET | /entan/v1/key-enterprises | unavailable | industry、city、scale、limit（均可选） |
| entan.basic.type-distribution | 企业类型分布 | GET | /entan/v1/type-distribution | unavailable | year |
| entan.basic.domain-distribution | 领域分布 | GET | /entan/v1/domain-distribution | unavailable | year |
| entan.basic.new-enterprises | 历年新增企业 | GET | /entan/v1/new-enterprises | unavailable | domain |
| entan.news.stats | 重点资讯统计 | GET | /entan/v1/news/stats | unavailable | news_type |
| entan.news.list | 重点资讯明细 | GET | /entan/v1/news | unavailable | news_type、keyword、page、size |

---

## 2. endpoint → 用例简表

| endpoint_id | title | 用例编号 |
|-------------|-------|----------|
| entan.basic.filters | 筛选项 | API-00912 |
| entan.basic.key-enterprises | 重点企业 | API-00913～00921 |
| entan.basic.type-distribution | 企业类型分布 | API-00922～00924 |
| entan.basic.domain-distribution | 领域分布 | API-00925～00927 |
| entan.basic.new-enterprises | 历年新增企业 | API-00928～00930 |
| entan.news.stats | 重点资讯统计 | API-00931～00933 |
| entan.news.list | 重点资讯明细 | API-00934～00942 |

---

## 3. §I 交卷自检计数

| 检查项 | 计数 / 结论 |
|--------|-------------|
| 本页 title 数 | **7**（§0 清单） |
| 功能点列可搜到的 title | **7** / 7 |
| 每 title 至少 1 条主流程 | **7** / 7（00912、00913、00922、00925、00928、00931、00934） |
| 用例总数 | **31**（API-00912～00942） |
| 鉴权 / Token / 401 / 424 用例 | **0** |
| 契约-不可用 / 异常-鉴权 功能项 | **0** |
| 正向用例（主流程+备选） | **19** |
| 反向用例（异常-入参） | **12**（重点企业 4 + 类型 1 + 领域 1 + 新增 1 + 资讯统计 1 + 资讯明细 4） |
| 有参接口每参数反向 | industry/city/scale/limit/year×2/domain/news_type×2/keyword/page/size = **12**，与反向用例数一致 |
| unavailable 接口主流程按文档 body | **7** / 7 |
| `coverage-fp.md` | 已同步 L02 矩阵 |
