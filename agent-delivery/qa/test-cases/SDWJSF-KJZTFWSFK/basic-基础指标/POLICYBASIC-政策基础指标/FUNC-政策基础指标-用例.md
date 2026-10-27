# 智能服务集群-科技专题服务算法库测试用例（政策基础指标 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：基础指标 / 政策基础指标  
> **catalog**：`entry_id=policy.basic` · `catalog_page_id=policy.basic` · path `#/policy/basic`  
> **A 线对照**：`fp-split-by-api-run/work/L03.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 + §长任务返工 + §S1（第三轮 R3-批1）  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

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

**kind 文档取值**：全维度 `all`；级别 `level`；类型 `type`；时序 `timeseries`；全国 `national`；深圳 `sz`。六个有参接口的 `kind` 均为可选。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00059**～**FUNC-00079**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.basic`、组合 id（如有）。本页 7 个接口 `status=unavailable`，仍按 catalog 返回体编写。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00059 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 指标总览 | 验证指标总览功能，检查无参调用后返回面板含文档示例 headline 头部 KPI 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「指标总览」；4.不填查询参数，点击调用 | 1、返回面板 body 的 data 为对象；2、含 headline（object，responseFields 头部 KPI）；3、headline 含 M_POLICY_TOTAL_COUNT（number）、M_POLICY_VALIDITY_RATE（number）、M_POLICY_NATIONAL_PROVINCES（number）、M_POLICY_PEAK_YEAR_PUBLISH（number）、M_POLICY_GRAPH_NODES（number）、M_POLICY_GRAPH_EDGES（number）；4、结构与 sampleResponse 一致（示例 M_POLICY_TOTAL_COUNT=1280、M_POLICY_VALIDITY_RATE=86.4、M_POLICY_NATIONAL_PROVINCES=31、M_POLICY_PEAK_YEAR_PUBLISH=246、M_POLICY_GRAPH_NODES=420、M_POLICY_GRAPH_EDGES=980） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/metrics | M_POLICY_TOTAL_COUNT | INTEG |  | FUNC-00059 | endpoint_id=policy.basic.metrics catalog_page_id=policy.basic 场景=主流程 组合=— catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00060 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策基础指标（全维度） | 验证政策基础指标（全维度）功能，检查填写 chainId=INB1701 kind=all 查询后返回五维指标块字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=all | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策基础指标（全维度）」；4.填写 kind=all，点击调用 | 1、返回面板 body 的 data 为对象；2、含 level、type、timeseries、national、sz（均为 array；responseFields A1～A5）；3、level 元素含 level（string）、level_name（string）、policy_count（number）、validity_rate（number）；4、type 元素含 policy_type（string）、policy_count（number）；5、timeseries 元素含 period_key（string）、publish_count（number）、growth_rate（number）、continuity_rate（number）；6、national 元素含 province_name（string）、policy_count（number）；7、sz 元素含 district_name（string）、policy_count（number）；8、结构与 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG |  | FUNC-00060 | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 场景=主流程 组合=ALL-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00061 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策基础指标（全维度） | 验证政策基础指标（全维度）功能，检查不传可选 kind 时仍返回五维指标块 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策基础指标（全维度）」；4.不传 kind，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 level、type、timeseries、national、sz（array）；3、level 元素仍含 level（string）、level_name（string）、policy_count（number）、validity_rate（number）；4、type 元素仍含 policy_type（string）、policy_count（number）；5、timeseries 元素仍含 period_key（string）、publish_count（number）、growth_rate（number）、continuity_rate（number）；6、national 元素仍含 province_name（string）、policy_count（number）；7、sz 元素仍含 district_name（string）、policy_count（number）；8、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG |  | FUNC-00061 | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 场景=备选-参数组合 组合=ALL-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00062 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策基础指标（全维度） | 验证政策基础指标（全维度）功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策基础指标（全维度）」；4.填写 kind=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 kind 非法；2、不返回含 level、type、timeseries、national、sz 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators |  | INTEG |  | FUNC-00062 | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 场景=异常-入参-非法kind 组合=ALL-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00063 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策级别指标 | 验证政策级别指标功能，检查填写 chainId=INB1701 kind=level 查询后返回 level 级别分布字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=level | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策级别指标」；4.填写 kind=level，点击调用 | 1、返回面板 body 的 data 为对象；2、含 level（array，responseFields A1 级别分布）；3、元素含 level（string）、level_name（string）、policy_count（number）、validity_rate（number）；4、结构与 sampleResponse 一致（示例 level 1/2/3/4、level_name 国家级/省级/市级/区县级、policy_count 186/412/498/184、validity_rate 91.2/87.4/84.1/79.6） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG |  | FUNC-00063 | endpoint_id=policy.basic.indicators-level catalog_page_id=policy.basic 场景=主流程 组合=LVL-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00064 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策级别指标 | 验证政策级别指标功能，检查不传可选 kind 时仍返回 level 数组 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策级别指标」；4.不传 kind，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 level（array）；3、元素仍含 level（string）、level_name（string）、policy_count（number）、validity_rate（number）；4、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG |  | FUNC-00064 | endpoint_id=policy.basic.indicators-level catalog_page_id=policy.basic 场景=备选-参数组合 组合=LVL-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00065 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策级别指标 | 验证政策级别指标功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策级别指标」；4.填写 kind=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 kind 非法；2、不返回含 level、level_name、policy_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators |  | INTEG |  | FUNC-00065 | endpoint_id=policy.basic.indicators-level catalog_page_id=policy.basic 场景=异常-入参-非法kind 组合=LVL-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00066 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策类型指标 | 验证政策类型指标功能，检查填写 chainId=INB1701 kind=type 查询后返回 type 类型分布字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=type | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策类型指标」；4.填写 kind=type，点击调用 | 1、返回面板 body 的 data 为对象；2、含 type（array，responseFields A2 类型分布）；3、元素含 policy_type（string）、policy_count（number）；4、结构与 sampleResponse 一致（示例 policy_type 产业政策/人才政策/企业扶持/科技创新、policy_count 320/210/268/196） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_TYPE_DIST | INTEG |  | FUNC-00066 | endpoint_id=policy.basic.indicators-type catalog_page_id=policy.basic 场景=主流程 组合=TYP-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00067 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策类型指标 | 验证政策类型指标功能，检查不传可选 kind 时仍返回 type 数组 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策类型指标」；4.不传 kind，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 type（array）；3、元素仍含 policy_type（string）、policy_count（number）；4、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_TYPE_DIST | INTEG |  | FUNC-00067 | endpoint_id=policy.basic.indicators-type catalog_page_id=policy.basic 场景=备选-参数组合 组合=TYP-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00068 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策类型指标 | 验证政策类型指标功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策类型指标」；4.填写 kind=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 kind 非法；2、不返回含 policy_type、policy_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators |  | INTEG |  | FUNC-00068 | endpoint_id=policy.basic.indicators-type catalog_page_id=policy.basic 场景=异常-入参-非法kind 组合=TYP-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00069 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策时序指标 | 验证政策时序指标功能，检查填写 kind=timeseries 查询后返回 timeseries 发布时序字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=timeseries | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策时序指标」；4.填写 kind=timeseries，点击调用 | 1、返回面板 body 的 data 为对象；2、含 timeseries（array，responseFields A3 发布时序）；3、元素含 period_key（string）、publish_count（number）、growth_rate（number）、continuity_rate（number）；4、结构与 sampleResponse 一致（示例 period_key 2023/2024/2025、publish_count 198/226/246、growth_rate 6.4/14.1/8.8、continuity_rate 88/91/93） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_TIMESERIES | INTEG |  | FUNC-00069 | endpoint_id=policy.basic.indicators-timeseries catalog_page_id=policy.basic 场景=主流程 组合=TS-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00070 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策时序指标 | 验证政策时序指标功能，检查不传可选 kind 时仍返回 timeseries 数组 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策时序指标」；4.不传 kind，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 timeseries（array）；3、元素仍含 period_key（string）、publish_count（number）、growth_rate（number）、continuity_rate（number）；4、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_TIMESERIES | INTEG |  | FUNC-00070 | endpoint_id=policy.basic.indicators-timeseries catalog_page_id=policy.basic 场景=备选-参数组合 组合=TS-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00071 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 政策时序指标 | 验证政策时序指标功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「政策时序指标」；4.填写 kind=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 kind 非法；2、不返回含 period_key、publish_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators |  | INTEG |  | FUNC-00071 | endpoint_id=policy.basic.indicators-timeseries catalog_page_id=policy.basic 场景=异常-入参-非法kind 组合=TS-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00072 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 全国政策分布 | 验证全国政策分布功能，检查填写 kind=national 后返回 national 全国分布字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=national | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「全国政策分布」；4.填写 kind=national，点击调用 | 1、返回面板 body 的 data 为对象；2、含 national（array，responseFields A4 全国分布）；3、元素含 province_name（string）、policy_count（number）；4、结构与 sampleResponse 一致（示例 province_name 广东/北京/上海/浙江/江苏、policy_count 148/112/96/88/84） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_NATIONAL_DIST | INTEG |  | FUNC-00072 | endpoint_id=policy.basic.indicators-national catalog_page_id=policy.basic 场景=主流程 组合=NAT-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00073 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 全国政策分布 | 验证全国政策分布功能，检查不传可选 kind 时仍返回 national 数组 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「全国政策分布」；4.不传 kind，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 national（array）；3、元素仍含 province_name（string）、policy_count（number）；4、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_NATIONAL_DIST | INTEG |  | FUNC-00073 | endpoint_id=policy.basic.indicators-national catalog_page_id=policy.basic 场景=备选-参数组合 组合=NAT-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00074 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 全国政策分布 | 验证全国政策分布功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「全国政策分布」；4.填写 kind=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 kind 非法；2、不返回含 province_name、policy_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators |  | INTEG |  | FUNC-00074 | endpoint_id=policy.basic.indicators-national catalog_page_id=policy.basic 场景=异常-入参-非法kind 组合=NAT-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00075 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 深圳政策分布 | 验证深圳政策分布功能，检查填写 kind=sz 查询后返回 sz 深圳分布字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=sz | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「深圳政策分布」；4.填写 kind=sz，点击调用 | 1、返回面板 body 的 data 为对象；2、含 sz（array，responseFields A5 深圳分布）；3、元素含 district_name（string）、policy_count（number）；4、结构与 sampleResponse 一致（示例 district_name 南山/福田/宝安/龙岗、policy_count 42/31/24/21） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_SZ_DIST | INTEG |  | FUNC-00075 | endpoint_id=policy.basic.indicators-sz catalog_page_id=policy.basic 场景=主流程 组合=SZ-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00076 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 深圳政策分布 | 验证深圳政策分布功能，检查不传可选 kind 时仍返回 sz 数组 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「深圳政策分布」；4.不传 kind，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 sz（array）；3、元素仍含 district_name（string）、policy_count（number）；4、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_SZ_DIST | INTEG |  | FUNC-00076 | endpoint_id=policy.basic.indicators-sz catalog_page_id=policy.basic 场景=备选-参数组合 组合=SZ-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00077 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 深圳政策分布 | 验证深圳政策分布功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.接口下拉选择「深圳政策分布」；4.填写 kind=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 kind 非法；2、不返回含 district_name、policy_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators |  | INTEG |  | FUNC-00077 | endpoint_id=policy.basic.indicators-sz catalog_page_id=policy.basic 场景=异常-入参-非法kind 组合=SZ-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00078 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 接口信息 | 验证政策基础指标的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「政策基础指标」；2.记录默认选中项的概览标题、method、path 与附录 B 对应行一致；3.接口下拉切换至「政策基础指标（全维度）」 | 1、页头接口数量=7；2、下拉项数=7，名称依次为指标总览、政策基础指标（全维度）、政策级别指标、政策类型指标、政策时序指标、全国政策分布、深圳政策分布；3、切换前默认项概览 method、path 与所选接口附录 B 一致；4、切换后概览与附录 B 中 policy.basic.indicators 行一致，参数表与示例区已刷新；1、确认位于「接口信息」页签；2、核对页头显示 7 个接口、下拉共 7 项且名称与 §0 一致；3、核对概览标题、method（GET）、path（/policy/v1/policy/indicators）已更新，参数表与示例区有内容刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00078 | catalog_page_id=policy.basic 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00079 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 政策基础指标模型构建 | 政策基础指标 | 算法测试 | 验证政策基础指标的算法测试功能，检查接口下拉与调用区 method、path 在切换后正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「政策基础指标」；2.切换至「算法测试」页签；3.记录当前选中项在调用区展示的 method、path；4.接口下拉切换至「全国政策分布」 | 1、算法测试页签下拉项数=7，名称与接口信息 tab、catalog 一致；2、切换前调用区 method、path 与当前接口附录 B 一致；3、切换至全国政策分布后，调用区 method=GET、path=/policy/v1/policy/indicators，请求区已刷新；1、核对下拉 7 项且名称与 §0、catalog 一致；2、核对下拉名称、调用区 method（GET）、path（/policy/v1/policy/indicators）及请求参数区已刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00079 | catalog_page_id=policy.basic 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

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
| policy.basic.metrics | FUNC-00059 |
| policy.basic.indicators | FUNC-00060、00061、00062 |
| policy.basic.indicators-level | FUNC-00063、00064、00065 |
| policy.basic.indicators-type | FUNC-00066、00067、00068 |
| policy.basic.indicators-timeseries | FUNC-00069、00070、00071 |
| policy.basic.indicators-national | FUNC-00072、00073、00074 |
| policy.basic.indicators-sz | FUNC-00075、00076、00077 |
| （页面清单） | FUNC-00078、00079 |

---

## 3. §I 交卷自检（第三轮）

| 检查项 | 结果 |
|--------|------|
| 对象：7 个 title 均在功能点列出现，且各有 ≥1 条 `场景=主流程` | 通过（00059、00060、00063、00066、00069、00072、00075） |
| 步骤：均为 algovwz 侧栏/下拉/填参/调用；含 GET/POST 步骤 | 0 条 GET/POST |
| 模块列：算法工具库 / 科技专题服务算法库 / 基础指标分析模型 / 政策基础指标模型构建 | 通过 |
| 测试内容：每条含「验证」与「检查」 | 21/21 |
| 鉴权：登录/Token/401/424 独立用例 | 0 条；登录仅前置条件 |
| 正向：有参接口 sample + 省略 kind；预期含 sampleResponse 字段 | 通过 |
| 反向：每有参接口 kind 恰好 1 条非法 | 6 条（00062、00065、00068、00071、00074、00077） |
| unavailable：仍按文档写主流程，备注注明未交付 | 通过 |
| 清单：`场景=接口信息-清单`、`场景=算法测试-清单` 各 1 条 | 00078、00079 |
| 编号：闭区间 FUNC-00059～00079，无 API 号 | 通过 |

**统计**：用例 **21** 条（主流程 **7**、备选 **6**、反向 **6**、清单 **2**）；编号 **FUNC-00059**～**FUNC-00079**。
