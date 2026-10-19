# 智能服务集群-科技专题服务算法库测试用例（政策基础指标 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：基础指标 / 政策基础指标  
> **catalog**：`entry_id=policy.basic` · `catalog_page_id=policy.basic` · path `/policy/basic`  
> **A 线对照**：`fp-split-by-api-run/work/L03.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批9）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 指标总览 | policy.basic.metrics |
| 2 | 政策基础指标（全维度） | policy.basic.indicators |
| 3 | 政策级别指标 | policy.basic.indicators-level |
| 4 | 政策类型指标 | policy.basic.indicators-type |
| 5 | 政策时序指标 | policy.basic.indicators-timeseries |
| 6 | 全国政策分布 | policy.basic.indicators-national |
| 7 | 深圳政策分布 | policy.basic.indicators-sz |

**kind 试调取值**：全维度文档示例 `all`；级别 `level`；类型 `type`；时序 `timeseries`；全国 `national`；深圳 `sz`。六个有参接口的 `kind` 均为可选；省略属于备选，非法值单独作反向。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01314**～**API-01332**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.basic`、组合 id（如有）。本页 7 个接口 `status=unavailable`，仍按 catalog 返回体编写。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01314 | 基础指标 | 政策基础指标 | 主流程 | — | 政策基础指标 | 指标总览 | 指标总览无参查询返回文档示例中的 headline 头部 KPI 字段 | 1、无业务前置 | 1.GET /policy/v1/policy/metrics（无查询参数） | 1、返回 body 的 data 为对象；2、含 headline（object，responseFields 头部 KPI）；3、headline 含 M_POLICY_TOTAL_COUNT（number）、M_POLICY_VALIDITY_RATE（number）、M_POLICY_NATIONAL_PROVINCES（number）、M_POLICY_PEAK_YEAR_PUBLISH（number）、M_POLICY_GRAPH_NODES（number）、M_POLICY_GRAPH_EDGES（number）；4、结构与 sampleResponse 一致（示例 M_POLICY_TOTAL_COUNT=1280、M_POLICY_VALIDITY_RATE=86.4、M_POLICY_NATIONAL_PROVINCES=31、M_POLICY_PEAK_YEAR_PUBLISH=246、M_POLICY_GRAPH_NODES=420、M_POLICY_GRAPH_EDGES=980） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/metrics | M_POLICY_TOTAL_COUNT | INTEG | | | endpoint_id=policy.basic.metrics catalog_page_id=policy.basic 组合=— 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01315 | 基础指标 | 政策基础指标 | 主流程 | — | 政策基础指标 | 政策基础指标（全维度） | 政策基础指标（全维度）按文档 sampleRequest kind=all 查询 | 1、kind 使用文档示例 all | 1.GET /policy/v1/policy/indicators，查询参数取组合 ALL-01 | 1、返回 body 的 data 为对象；2、含 level、type、timeseries、national、sz（均为 array；responseFields A1 级别分布 / A2 类型分布 / A3 发布时序 / A4 全国分布 / A5 深圳分布）；3、level 元素含 level（string）、level_name（string）、policy_count（number）、validity_rate（number）；4、type 元素含 policy_type（string）、policy_count（number）；5、timeseries 元素含 period_key（string）、publish_count（number）、growth_rate（number）、continuity_rate（number）；6、national 元素含 province_name（string）、policy_count（number）；7、sz 元素含 district_name（string）、policy_count（number）；8、结构与 sampleResponse 一致（示例 level 1/2/3/4、level_name 国家级/省级/市级/区县级、policy_count 与 validity_rate 成对出现；policy_type 产业政策/人才政策/企业扶持/科技创新；period_key 2023/2024/2025 及 publish_count、growth_rate、continuity_rate；province_name 广东/北京/上海/浙江/江苏；district_name 南山/福田/宝安/龙岗） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG | | | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 组合=ALL-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01316 | 基础指标 | 政策基础指标 | 备选-参数组合 | 省略 kind | 政策基础指标 | 政策基础指标（全维度） | 政策基础指标（全维度）不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /policy/v1/policy/indicators，查询参数取组合 ALL-02 | 1、返回 body 的 data 为对象；2、仍含 level、type、timeseries、national、sz（array）；3、level 元素仍含 level（string）、level_name（string）、policy_count（number）、validity_rate（number）；4、type 元素仍含 policy_type（string）、policy_count（number）；5、timeseries 元素仍含 period_key（string）、publish_count（number）、growth_rate（number）、continuity_rate（number）；6、national 元素仍含 province_name（string）、policy_count（number）；7、sz 元素仍含 district_name（string）、policy_count（number）；8、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG | | | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 组合=ALL-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01317 | 基础指标 | 政策基础指标 | 异常-入参-非法kind | — | 政策基础指标 | 政策基础指标（全维度） | 政策基础指标（全维度）kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /policy/v1/policy/indicators，查询参数取组合 ALL-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 level、type、timeseries、national、sz 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | | INTEG | | | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 组合=ALL-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01318 | 基础指标 | 政策基础指标 | 主流程 | — | 政策基础指标 | 政策级别指标 | 政策级别指标按文档 sampleRequest kind=level 查询 | 1、kind 使用文档示例 level | 1.GET /policy/v1/policy/indicators，查询参数取组合 LVL-01 | 1、返回 body 的 data 为对象；2、含 level（array，responseFields A1 级别分布）；3、元素含 level（string）、level_name（string）、policy_count（number）、validity_rate（number）；4、结构与 sampleResponse 一致（示例 level 1/2/3/4、level_name 国家级/省级/市级/区县级、policy_count 186/412/498/184、validity_rate 91.2/87.4/84.1/79.6） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG | | | endpoint_id=policy.basic.indicators-level catalog_page_id=policy.basic 组合=LVL-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01319 | 基础指标 | 政策基础指标 | 备选-参数组合 | 省略 kind | 政策基础指标 | 政策级别指标 | 政策级别指标不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /policy/v1/policy/indicators，查询参数取组合 LVL-02 | 1、返回 body 的 data 为对象；2、仍含 level（array）；3、元素仍含 level（string）、level_name（string）、policy_count（number）、validity_rate（number）；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG | | | endpoint_id=policy.basic.indicators-level catalog_page_id=policy.basic 组合=LVL-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01320 | 基础指标 | 政策基础指标 | 异常-入参-非法kind | — | 政策基础指标 | 政策级别指标 | 政策级别指标 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /policy/v1/policy/indicators，查询参数取组合 LVL-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 level、level_name、policy_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | | INTEG | | | endpoint_id=policy.basic.indicators-level catalog_page_id=policy.basic 组合=LVL-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01321 | 基础指标 | 政策基础指标 | 主流程 | — | 政策基础指标 | 政策类型指标 | 政策类型指标按文档 sampleRequest kind=type 查询 | 1、kind 使用文档示例 type | 1.GET /policy/v1/policy/indicators，查询参数取组合 TYP-01 | 1、返回 body 的 data 为对象；2、含 type（array，responseFields A2 类型分布）；3、元素含 policy_type（string）、policy_count（number）；4、结构与 sampleResponse 一致（示例 policy_type 产业政策/人才政策/企业扶持/科技创新、policy_count 320/210/268/196） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_TYPE_DIST | INTEG | | | endpoint_id=policy.basic.indicators-type catalog_page_id=policy.basic 组合=TYP-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01322 | 基础指标 | 政策基础指标 | 备选-参数组合 | 省略 kind | 政策基础指标 | 政策类型指标 | 政策类型指标不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /policy/v1/policy/indicators，查询参数取组合 TYP-02 | 1、返回 body 的 data 为对象；2、仍含 type（array）；3、元素仍含 policy_type（string）、policy_count（number）；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_TYPE_DIST | INTEG | | | endpoint_id=policy.basic.indicators-type catalog_page_id=policy.basic 组合=TYP-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01323 | 基础指标 | 政策基础指标 | 异常-入参-非法kind | — | 政策基础指标 | 政策类型指标 | 政策类型指标 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /policy/v1/policy/indicators，查询参数取组合 TYP-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 policy_type、policy_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | | INTEG | | | endpoint_id=policy.basic.indicators-type catalog_page_id=policy.basic 组合=TYP-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01324 | 基础指标 | 政策基础指标 | 主流程 | — | 政策基础指标 | 政策时序指标 | 政策时序指标按文档 sampleRequest kind=timeseries 查询 | 1、kind 使用文档示例 timeseries | 1.GET /policy/v1/policy/indicators，查询参数取组合 TS-01 | 1、返回 body 的 data 为对象；2、含 timeseries（array，responseFields A3 发布时序）；3、元素含 period_key（string）、publish_count（number）、growth_rate（number）、continuity_rate（number）；4、结构与 sampleResponse 一致（示例 period_key 2023/2024/2025、publish_count 198/226/246、growth_rate 6.4/14.1/8.8、continuity_rate 88/91/93） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_TIMESERIES | INTEG | | | endpoint_id=policy.basic.indicators-timeseries catalog_page_id=policy.basic 组合=TS-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01325 | 基础指标 | 政策基础指标 | 备选-参数组合 | 省略 kind | 政策基础指标 | 政策时序指标 | 政策时序指标不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /policy/v1/policy/indicators，查询参数取组合 TS-02 | 1、返回 body 的 data 为对象；2、仍含 timeseries（array）；3、元素仍含 period_key（string）、publish_count（number）、growth_rate（number）、continuity_rate（number）；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_TIMESERIES | INTEG | | | endpoint_id=policy.basic.indicators-timeseries catalog_page_id=policy.basic 组合=TS-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01326 | 基础指标 | 政策基础指标 | 异常-入参-非法kind | — | 政策基础指标 | 政策时序指标 | 政策时序指标 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /policy/v1/policy/indicators，查询参数取组合 TS-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 period_key、publish_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | | INTEG | | | endpoint_id=policy.basic.indicators-timeseries catalog_page_id=policy.basic 组合=TS-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01327 | 基础指标 | 政策基础指标 | 主流程 | — | 政策基础指标 | 全国政策分布 | 全国政策分布按文档 sampleRequest kind=national 查询 | 1、kind 使用文档示例 national | 1.GET /policy/v1/policy/indicators，查询参数取组合 NAT-01 | 1、返回 body 的 data 为对象；2、含 national（array，responseFields A4 全国分布）；3、元素含 province_name（string）、policy_count（number）；4、结构与 sampleResponse 一致（示例 province_name 广东/北京/上海/浙江/江苏、policy_count 148/112/96/88/84） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_NATIONAL_DIST | INTEG | | | endpoint_id=policy.basic.indicators-national catalog_page_id=policy.basic 组合=NAT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01328 | 基础指标 | 政策基础指标 | 备选-参数组合 | 省略 kind | 政策基础指标 | 全国政策分布 | 全国政策分布不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /policy/v1/policy/indicators，查询参数取组合 NAT-02 | 1、返回 body 的 data 为对象；2、仍含 national（array）；3、元素仍含 province_name（string）、policy_count（number）；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_NATIONAL_DIST | INTEG | | | endpoint_id=policy.basic.indicators-national catalog_page_id=policy.basic 组合=NAT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01329 | 基础指标 | 政策基础指标 | 异常-入参-非法kind | — | 政策基础指标 | 全国政策分布 | 全国政策分布 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /policy/v1/policy/indicators，查询参数取组合 NAT-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 province_name、policy_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | | INTEG | | | endpoint_id=policy.basic.indicators-national catalog_page_id=policy.basic 组合=NAT-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01330 | 基础指标 | 政策基础指标 | 主流程 | — | 政策基础指标 | 深圳政策分布 | 深圳政策分布按文档 sampleRequest kind=sz 查询 | 1、kind 使用文档示例 sz | 1.GET /policy/v1/policy/indicators，查询参数取组合 SZ-01 | 1、返回 body 的 data 为对象；2、含 sz（array，responseFields A5 深圳分布）；3、元素含 district_name（string）、policy_count（number）；4、结构与 sampleResponse 一致（示例 district_name 南山/福田/宝安/龙岗、policy_count 42/31/24/21） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_SZ_DIST | INTEG | | | endpoint_id=policy.basic.indicators-sz catalog_page_id=policy.basic 组合=SZ-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01331 | 基础指标 | 政策基础指标 | 备选-参数组合 | 省略 kind | 政策基础指标 | 深圳政策分布 | 深圳政策分布不传可选 kind（与 sampleRequest 相反） | 1、不传 kind | 1.GET /policy/v1/policy/indicators，查询参数取组合 SZ-02 | 1、返回 body 的 data 为对象；2、仍含 sz（array）；3、元素仍含 district_name（string）、policy_count（number）；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_SZ_DIST | INTEG | | | endpoint_id=policy.basic.indicators-sz catalog_page_id=policy.basic 组合=SZ-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01332 | 基础指标 | 政策基础指标 | 异常-入参-非法kind | — | 政策基础指标 | 深圳政策分布 | 深圳政策分布 kind 非法 | 1、kind 取文档枚举外的值 | 1.GET /policy/v1/policy/indicators，查询参数取组合 SZ-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 district_name、policy_count 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | | INTEG | | | endpoint_id=policy.basic.indicators-sz catalog_page_id=policy.basic 组合=SZ-03 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ALL-01 | policy.basic.indicators | kind=all | 主路径（sampleRequest） |
| ALL-02 | policy.basic.indicators | 不传 kind | 省略可选 kind（与 sample 相反） |
| ALL-03 | policy.basic.indicators | kind=__invalid__ | 非法 kind |
| LVL-01 | policy.basic.indicators-level | kind=level | 主路径（sampleRequest） |
| LVL-02 | policy.basic.indicators-level | 不传 kind | 省略可选 kind（与 sample 相反） |
| LVL-03 | policy.basic.indicators-level | kind=__invalid__ | 非法 kind |
| TYP-01 | policy.basic.indicators-type | kind=type | 主路径（sampleRequest） |
| TYP-02 | policy.basic.indicators-type | 不传 kind | 省略可选 kind（与 sample 相反） |
| TYP-03 | policy.basic.indicators-type | kind=__invalid__ | 非法 kind |
| TS-01 | policy.basic.indicators-timeseries | kind=timeseries | 主路径（sampleRequest） |
| TS-02 | policy.basic.indicators-timeseries | 不传 kind | 省略可选 kind（与 sample 相反） |
| TS-03 | policy.basic.indicators-timeseries | kind=__invalid__ | 非法 kind |
| NAT-01 | policy.basic.indicators-national | kind=national | 主路径（sampleRequest） |
| NAT-02 | policy.basic.indicators-national | 不传 kind | 省略可选 kind（与 sample 相反） |
| NAT-03 | policy.basic.indicators-national | kind=__invalid__ | 非法 kind |
| SZ-01 | policy.basic.indicators-sz | kind=sz | 主路径（sampleRequest） |
| SZ-02 | policy.basic.indicators-sz | 不传 kind | 省略可选 kind（与 sample 相反） |
| SZ-03 | policy.basic.indicators-sz | kind=__invalid__ | 非法 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 指标总览 | policy.basic.metrics | GET | /policy/v1/policy/metrics | — | unavailable |
| 政策基础指标（全维度） | policy.basic.indicators | GET | /policy/v1/policy/indicators | kind? | unavailable |
| 政策级别指标 | policy.basic.indicators-level | GET | /policy/v1/policy/indicators | kind? | unavailable |
| 政策类型指标 | policy.basic.indicators-type | GET | /policy/v1/policy/indicators | kind? | unavailable |
| 政策时序指标 | policy.basic.indicators-timeseries | GET | /policy/v1/policy/indicators | kind? | unavailable |
| 全国政策分布 | policy.basic.indicators-national | GET | /policy/v1/policy/indicators | kind? | unavailable |
| 深圳政策分布 | policy.basic.indicators-sz | GET | /policy/v1/policy/indicators | kind? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.basic.metrics | API-01314 |
| policy.basic.indicators | API-01315、01316、01317 |
| policy.basic.indicators-level | API-01318、01319、01320 |
| policy.basic.indicators-type | API-01321、01322、01323 |
| policy.basic.indicators-timeseries | API-01324、01325、01326 |
| policy.basic.indicators-national | API-01327、01328、01329 |
| policy.basic.indicators-sz | API-01330、01331、01332 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 7 个 title 均在功能点列出现且各有 ≥1 条主流程（功能项=主流程）
- [x] 无参接口 1 条主流程、0 条反向；仅可选 kind 的接口各 3 条（sampleRequest 主流程 + 省略 kind 备选 + 非法 kind 反向）
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] `coverage-fp.md` 已同步 API-01314～01332

**统计**：用例 **19** 条（主流程 **7**、备选 **6**、反向 **6**）；编号闭区间 **API-01314**～**API-01332**（父控 R2-批9 分配）。
