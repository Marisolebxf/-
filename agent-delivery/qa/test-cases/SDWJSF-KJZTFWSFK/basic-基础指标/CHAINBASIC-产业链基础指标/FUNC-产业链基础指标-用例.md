# 智能服务集群-科技专题服务算法库测试用例（产业链基础指标 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.basic` · `catalog_page_id=chain.basic` · path `#/chain/basic`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **A 线对照**：`fp-split-by-api-run/work/L01.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批1 金样）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 产业链列表 | chain.basic.list |
| 2 | 产业市场规模 | chain.basic.market-stats |
| 3 | 产业企业规模 | chain.basic.enterprise-stats |
| 4 | 产业机构规模 | chain.basic.institution-stats |
| 5 | 产业投融资规模 | chain.basic.investment-stats |
| 6 | 全球产业区域分布 | chain.basic.global-dist |
| 7 | 全国产业分布 | chain.basic.national-dist |
| 8 | 产业动态资讯 | chain.basic.news-stats |
| 9 | 深圳产业要素 | chain.basic.sz-elements |
| 10 | 深圳产业分布 | chain.basic.sz-dist |

**chainId 试调取值**：文档示例 `INB1701`（`产业链列表` 首条 `chain_id` 可替换，附录组合表引用该值）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00001**～**FUNC-00025**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.basic`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00001 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业链列表 | 验证产业链列表功能，检查无参调用后返回面板含文档示例列表字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业链列表」；3.不填查询参数，点击调用 | 1、返回面板中 data 为数组；2、元素含 chain_id（string）、chain_name（string）；3、sampleResponse 示例还含 cluster_name、map_status、description（string），非空元素中应出现这些字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/list | M_CHAIN_TOTAL_COUNT | INTEG |  |  | endpoint_id=chain.basic.list catalog_page_id=chain.basic 组合=— 场景=主流程 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00002 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业市场规模 | 验证产业市场规模功能，检查填写 chainId=INB1701、statYear=2025 查询后返回总营收等规模字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业市场规模」；3.填写 chainId=INB1701、statYear=2025，点击调用 | 1、返回面板中 data 为数组；2、元素含 stat_year（number）、total_revenue（number，responseFields 总营收(万)）、growth_rate（number）；3、结构与 sampleResponse 一致（示例 stat_year 2023/2024/2025 及对应 total_revenue、growth_rate） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats | M_CHAIN_MARKET_SIZE | INTEG |  |  | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00003 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业市场规模 | 验证产业市场规模功能，检查仅传 chainId、不传可选 statYear 时仍返回规模字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业市场规模」；3.不传 statYear，填写 chainId=INB1701，点击调用 | 1、返回面板中 data 为数组；2、元素仍含 stat_year、total_revenue、growth_rate（number），结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats | M_CHAIN_MARKET_SIZE | INTEG |  |  | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-04 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00004 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业市场规模 | 验证产业市场规模功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业市场规模」；3.不传 chainId，填写 statYear=2025，点击调用 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 total_revenue 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats |  | INTEG |  |  | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-02 场景=异常-入参-缺chainId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00005 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业市场规模 | 验证产业市场规模功能，检查 statYear 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业市场规模」；3.填写 chainId=INB1701、statYear=not-a-year，点击调用 | 1、返回面板的 message 或 msg 说明 statYear 非法或无法解析；2、不返回含可信 total_revenue 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats |  | INTEG |  |  | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-05 场景=异常-入参-非法statYear |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00006 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业企业规模 | 验证产业企业规模功能，检查填写 sampleRequest 所示参数 仅 chainId 查询后返回企业数等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业企业规模」；3.填写 chainId=INB1701，点击调用 | 1、返回面板中 data 为数组；2、元素含 stat_year（number）、enterprise_count（number，responseFields 企业数）、growth_rate（number）；3、与 sampleResponse 结构一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats | M_CHAIN_ENTERPRISE_COUNT | INTEG |  |  | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00007 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业企业规模 | 验证产业企业规模功能，检查传 chainId 与 statYear=2025 时返回企业规模字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业企业规模」；3.填写 chainId=INB1701、statYear=2025，点击调用 | 1、返回面板中 data 为数组；2、元素含 stat_year、enterprise_count、growth_rate（number），结构与 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats | M_CHAIN_ENTERPRISE_COUNT | INTEG |  |  | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-04 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00008 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业企业规模 | 验证产业企业规模功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业企业规模」；3.不传 chainId，填写 statYear=2025，点击调用 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 enterprise_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats |  | INTEG |  |  | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-02 场景=异常-入参-缺chainId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00009 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业企业规模 | 验证产业企业规模功能，检查 statYear 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业企业规模」；3.填写 chainId=INB1701、statYear=0，点击调用 | 1、返回面板的 message 或 msg 说明 statYear 非法或无法解析；2、不返回含可信 enterprise_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats |  | INTEG |  |  | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-05 场景=异常-入参-非法statYear |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00010 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业机构规模 | 验证产业机构规模功能，检查填写 chainId=INB1701 查询后返回机构规模字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业机构规模」；3.填写 chainId=INB1701，点击调用 | 1、返回面板中 data 为数组；2、元素含 stat_year（number）、institution_count（number，responseFields 机构数）、growth_rate（number）；3、结构与 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/institution-stats |  | INTEG |  |  | endpoint_id=chain.basic.institution-stats catalog_page_id=chain.basic 组合=INS-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00011 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业机构规模 | 验证产业机构规模功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业机构规模」；3.不传 chainId，点击调用 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 institution_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/institution-stats |  | INTEG |  |  | endpoint_id=chain.basic.institution-stats catalog_page_id=chain.basic 组合=INS-02 场景=异常-入参-缺chainId catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00012 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业投融资规模 | 验证产业投融资规模功能，检查填写 chainId=INB1701 查询后返回投融资金额等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业投融资规模」；3.填写 chainId=INB1701，点击调用 | 1、返回面板中 data 为数组；2、元素含 stat_year（number）、total_amount（number，responseFields 投融资金额(万)）、amount_growth_rate（number）；3、与 sampleResponse 结构一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/investment-stats |  | INTEG |  |  | endpoint_id=chain.basic.investment-stats catalog_page_id=chain.basic 组合=INV-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00013 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业投融资规模 | 验证产业投融资规模功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业投融资规模」；3.不传 chainId，点击调用 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 total_amount 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/investment-stats |  | INTEG |  |  | endpoint_id=chain.basic.investment-stats catalog_page_id=chain.basic 组合=INV-02 场景=异常-入参-缺chainId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00014 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 全球产业区域分布 | 验证全球产业区域分布功能，检查填写 chainId=INB1701 查询后返回国家地区与企业机构数字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「全球产业区域分布」；3.填写 chainId=INB1701，点击调用 | 1、返回面板中 data 为数组；2、元素含 country（string，responseFields 国家/地区）、enterprise_count（number）、institution_count（number）；3、与 sampleResponse 结构一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/global-dist |  | INTEG |  |  | endpoint_id=chain.basic.global-dist catalog_page_id=chain.basic 组合=GLO-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00015 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 全球产业区域分布 | 验证全球产业区域分布功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「全球产业区域分布」；3.不传 chainId，点击调用 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 country 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/global-dist |  | INTEG |  |  | endpoint_id=chain.basic.global-dist catalog_page_id=chain.basic 组合=GLO-02 场景=异常-入参-缺chainId catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00016 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 全国产业分布 | 验证全国产业分布功能，检查填写 chainId=INB1701 查询后返回省份与企业数字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「全国产业分布」；3.填写 chainId=INB1701，点击调用 | 1、返回面板中 data 为数组；2、元素含 province（string，responseFields 省份）、enterprise_count（number）；3、与 sampleResponse 结构一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/national-dist |  | INTEG |  |  | endpoint_id=chain.basic.national-dist catalog_page_id=chain.basic 组合=NAT-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00017 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 全国产业分布 | 验证全国产业分布功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「全国产业分布」；3.不传 chainId，点击调用 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 province 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/national-dist |  | INTEG |  |  | endpoint_id=chain.basic.national-dist catalog_page_id=chain.basic 组合=NAT-02 场景=异常-入参-缺chainId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00018 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业动态资讯 | 验证产业动态资讯功能，检查填写 chainId=INB1701 查询后返回资讯数与热点数等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业动态资讯」；3.填写 chainId=INB1701，点击调用 | 1、返回面板中 data 为数组；2、元素含 stat_month（string）、news_count（number，responseFields 资讯数）、hot_count（number）；3、与 sampleResponse 结构一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/news-stats |  | INTEG |  |  | endpoint_id=chain.basic.news-stats catalog_page_id=chain.basic 组合=NEW-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00019 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 产业动态资讯 | 验证产业动态资讯功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「产业动态资讯」；3.不传 chainId，点击调用 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 news_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/news-stats |  | INTEG |  |  | endpoint_id=chain.basic.news-stats catalog_page_id=chain.basic 组合=NEW-02 场景=异常-入参-缺chainId catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00020 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 深圳产业要素 | 验证深圳产业要素功能，检查填写 chainId=INB1701 查询后返回深圳企业数、机构数等要素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「深圳产业要素」；3.填写 chainId=INB1701，点击调用 | 1、返回面板中 data 为数组（或等价载荷）；2、元素含 enterprise_count、institution_count（number，responseFields 深圳企业数/机构数）；3、sampleResponse 还含 talent_count、total_revenue（number），非空载荷中应出现 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-elements | M_CHAIN_SZ_ENTERPRISE_COUNT | INTEG |  |  | endpoint_id=chain.basic.sz-elements catalog_page_id=chain.basic 组合=SZE-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00021 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 深圳产业要素 | 验证深圳产业要素功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「深圳产业要素」；3.不传 chainId，点击调用 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 enterprise_count/institution_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-elements |  | INTEG |  |  | endpoint_id=chain.basic.sz-elements catalog_page_id=chain.basic 组合=SZE-02 场景=异常-入参-缺chainId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00022 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 深圳产业分布 | 验证深圳产业分布功能，检查填写 chainId=INB1701 查询后返回行政区与企业数字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB1701 | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「深圳产业分布」；3.填写 chainId=INB1701，点击调用 | 1、返回面板中 data 为数组；2、元素含 district（string，responseFields 行政区）、enterprise_count（number）；3、与 sampleResponse 结构一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-dist | M_CHAIN_SZ_ENTERPRISE_COUNT | INTEG |  |  | endpoint_id=chain.basic.sz-dist catalog_page_id=chain.basic 组合=SZD-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00023 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 深圳产业分布 | 验证深圳产业分布功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.接口下拉选择「深圳产业分布」；3.不传 chainId，点击调用 | 1、返回面板的 message 或 msg 说明 chainId 缺失或非法；2、不返回含 district 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-dist |  | INTEG |  |  | endpoint_id=chain.basic.sz-dist catalog_page_id=chain.basic 组合=SZD-02 场景=异常-入参-缺chainId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00024 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 接口信息 | 验证产业链基础指标的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 10；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应产业链列表 GET /innov/v1/industry/list；4、切换后概览对应产业市场规模 GET /innov/v1/industry/market-stats，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.basic 场景=接口信息-清单 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00025 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 产业链基础指标模型构建 | 产业链基础指标 | 算法测试 | 验证产业链基础指标的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「产业链基础指标」；2.切换到「算法测试」tab；3.下拉切换到「产业投融资规模」 | 1、算法测试 tab 下拉共 10 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「产业投融资规模」；3、调用区 method 为 GET、path 为 /innov/v1/industry/investment-stats；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.basic 场景=算法测试-清单 金样 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

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
| 产业市场规模 | chain.basic.market-stats | GET | /innov/v1/industry/market-stats | chainId*；statYear? | available |
| 产业企业规模 | chain.basic.enterprise-stats | GET | /innov/v1/industry/enterprise-stats | chainId*；statYear? | available |
| 产业机构规模 | chain.basic.institution-stats | GET | /innov/v1/industry/institution-stats | chainId* | unavailable |
| 产业投融资规模 | chain.basic.investment-stats | GET | /innov/v1/industry/investment-stats | chainId* | available |
| 全球产业区域分布 | chain.basic.global-dist | GET | /innov/v1/industry/global-dist | chainId* | unavailable |
| 全国产业分布 | chain.basic.national-dist | GET | /innov/v1/industry/national-dist | chainId* | available |
| 产业动态资讯 | chain.basic.news-stats | GET | /innov/v1/industry/news-stats | chainId* | unavailable |
| 深圳产业要素 | chain.basic.sz-elements | GET | /innov/v1/industry/sz-elements | chainId* | available |
| 深圳产业分布 | chain.basic.sz-dist | GET | /innov/v1/industry/sz-dist | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.basic.list | FUNC-00001 |
| chain.basic.market-stats | FUNC-00002、00003、00004、00005 |
| chain.basic.enterprise-stats | FUNC-00006、00007、00008、00009 |
| chain.basic.institution-stats | FUNC-00010、00011 |
| chain.basic.investment-stats | FUNC-00012、00013 |
| chain.basic.global-dist | FUNC-00014、00015 |
| chain.basic.national-dist | FUNC-00016、00017 |
| chain.basic.news-stats | FUNC-00018、00019 |
| chain.basic.sz-elements | FUNC-00020、00021 |
| chain.basic.sz-dist | FUNC-00022、00023 |
| （页面清单） | FUNC-00024、00025 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 10 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 有参接口：文档示例正向 + 可选参数组合（产业市场规模/产业企业规模 statYear）+ 每参数 1 条反向
- [x] unavailable（产业机构规模/全球产业区域分布/产业动态资讯）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 基础指标分析模型 / 产业链基础指标模型构建
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00001～00025

**统计**：接口 **10**；主流程 **10**；备选 **2**；反向 **11**；清单 **2**；合计 **25** 条；编号闭区间 **FUNC-00001**～**FUNC-00025**（父控 R3-批1 分配）。
