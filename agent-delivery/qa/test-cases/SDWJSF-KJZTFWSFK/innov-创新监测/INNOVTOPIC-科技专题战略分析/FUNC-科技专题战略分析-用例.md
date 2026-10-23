# 智能服务集群-科技专题服务算法库测试用例（科技专题战略分析 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.topic-strategy` · `catalog_page_id=innov.topic-strategy` · path `/innov/topic-strategy`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.topic-strategy`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 MET-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 科技专题战略分析指标清单 | innov.topic-strategy.metrics | GET | /innov/v1/innov/metrics | module? | 3 |
| 2 | 影响力评价与应用反馈 | innov.topic-strategy.m_innov_ds_25_softsci_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | module? | 3 |
| 3 | 协同绩效与影响力智能评估 | innov.topic-strategy.m_innov_ds_26_eco_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | module? | 3 |
| 4 | 热点区域自动识别与预警 | innov.topic-strategy.m_innov_ds_27_spatio_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | module? | 3 |

4 个 title 按 catalog `endpoints` 顺序各 3 条，合计 **12** 条接口调用。每个接口只有可选 `module`：1 条主流程（跟 `sampleRequest`，`module=topic-strategy`）+ 1 条与 sample 相反的不传 `module` + 1 条非法 `module=__invalid__`。GET 的 `module` 为查询参数；POST 的 `module` 为请求体。另加 §6.1 页面清单 **2** 条，本册共 **14** 条。

`科技专题战略分析指标清单` 为 catalog `status=running`；其余 3 个 POST compute 为 `available`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01479`～`01492`（闭区间 **14** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.topic-strategy`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01479 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 科技专题战略分析指标清单 | 验证科技专题战略分析指标清单功能，检查填写 module=topic-strategy（sampleRequest） 传 module=topic-strategy 后返回 metrics 清单与 total 及元素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=topic-strategy | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「科技专题战略分析指标清单」；4.填写 module=topic-strategy，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 同层逐字段：metrics（array，responseFields 指标元数据清单）、total（number，responseFields 指标数，示例 3）；2、metrics 元素含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；3、sampleResponse 三行：metric_id=M_INNOV_DS_25_SOFTSCI_012、name=影响力评价与应用反馈、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_DS_26_ECO_012、name=协同绩效与影响力智能评估、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_DS_27_SPATIO_003、name=热点区域自动识别与预警、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  | FUNC-01479 | endpoint_id=innov.topic-strategy.metrics catalog_page_id=innov.topic-strategy 组合=MET-01 catalog_status=running 场景=主流程 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01480 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 科技专题战略分析指标清单 | 验证科技专题战略分析指标清单功能，检查不传可选 module 不传 module 后仍返回与 sampleResponse 同类结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「科技专题战略分析指标清单」；4.不传 module，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 逐字段同类：metrics（array，responseFields 指标元数据清单）、total（number，responseFields 指标数，示例 3）；2、metrics 元素仍含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；3、字段结构与主流程及 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  | FUNC-01480 | endpoint_id=innov.topic-strategy.metrics catalog_page_id=innov.topic-strategy 组合=MET-02 catalog_status=running 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01481 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 科技专题战略分析指标清单 | 验证科技专题战略分析指标清单功能，检查 module 非法填写 module=__invalid__ 后返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「科技专题战略分析指标清单」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metrics 与 total 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  | FUNC-01481 | endpoint_id=innov.topic-strategy.metrics catalog_page_id=innov.topic-strategy 组合=MET-03 catalog_status=running 场景=异常-入参-非法module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01482 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 影响力评价与应用反馈 | 验证影响力评价与应用反馈功能，检查填写 module=topic-strategy（sampleRequest） 传 module=topic-strategy 后返回 metric_id、hint 及 metrics、total 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=topic-strategy | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「影响力评价与应用反馈」；4.填写 module=topic-strategy，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_25_SOFTSCI_012）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | M_INNOV_DS_25_SOFTSCI_012 | INTEG |  | FUNC-01482 | endpoint_id=innov.topic-strategy.m_innov_ds_25_softsci_012 catalog_page_id=innov.topic-strategy 组合=S25-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01483 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 影响力评价与应用反馈 | 验证影响力评价与应用反馈功能，检查不传可选 module 不传 module 后仍返回与 sampleResponse 同类结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「影响力评价与应用反馈」；4.不传 module，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_25_SOFTSCI_012）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | M_INNOV_DS_25_SOFTSCI_012 | INTEG |  | FUNC-01483 | endpoint_id=innov.topic-strategy.m_innov_ds_25_softsci_012 catalog_page_id=innov.topic-strategy 组合=S25-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01484 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 影响力评价与应用反馈 | 验证影响力评价与应用反馈功能，检查 module 非法填写 module=__invalid__ 后返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「影响力评价与应用反馈」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id 为 M_INNOV_DS_25_SOFTSCI_012 且含 hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute |  | INTEG |  | FUNC-01484 | endpoint_id=innov.topic-strategy.m_innov_ds_25_softsci_012 catalog_page_id=innov.topic-strategy 组合=S25-03 场景=异常-入参-非法module catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01485 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 协同绩效与影响力智能评估 | 验证协同绩效与影响力智能评估功能，检查填写 module=topic-strategy（sampleRequest） 传 module=topic-strategy 后返回 metric_id、hint 及 metrics、total 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=topic-strategy | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「协同绩效与影响力智能评估」；4.填写 module=topic-strategy，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_26_ECO_012）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | M_INNOV_DS_26_ECO_012 | INTEG |  | FUNC-01485 | endpoint_id=innov.topic-strategy.m_innov_ds_26_eco_012 catalog_page_id=innov.topic-strategy 组合=E26-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01486 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 协同绩效与影响力智能评估 | 验证协同绩效与影响力智能评估功能，检查不传可选 module 不传 module 后仍返回与 sampleResponse 同类结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「协同绩效与影响力智能评估」；4.不传 module，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_26_ECO_012）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | M_INNOV_DS_26_ECO_012 | INTEG |  | FUNC-01486 | endpoint_id=innov.topic-strategy.m_innov_ds_26_eco_012 catalog_page_id=innov.topic-strategy 组合=E26-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01487 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 协同绩效与影响力智能评估 | 验证协同绩效与影响力智能评估功能，检查 module 非法填写 module=__invalid__ 后返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「协同绩效与影响力智能评估」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id 为 M_INNOV_DS_26_ECO_012 且含 hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute |  | INTEG |  | FUNC-01487 | endpoint_id=innov.topic-strategy.m_innov_ds_26_eco_012 catalog_page_id=innov.topic-strategy 组合=E26-03 场景=异常-入参-非法module catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01488 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 热点区域自动识别与预警 | 验证热点区域自动识别与预警功能，检查填写 module=topic-strategy（sampleRequest） 传 module=topic-strategy 后返回 metric_id、hint 及 metrics、total 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=topic-strategy | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「热点区域自动识别与预警」；4.填写 module=topic-strategy，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_27_SPATIO_003）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | M_INNOV_DS_27_SPATIO_003 | INTEG |  | FUNC-01488 | endpoint_id=innov.topic-strategy.m_innov_ds_27_spatio_003 catalog_page_id=innov.topic-strategy 组合=P27-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01489 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 热点区域自动识别与预警 | 验证热点区域自动识别与预警功能，检查不传可选 module 不传 module 后仍返回与 sampleResponse 同类结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「热点区域自动识别与预警」；4.不传 module，点击调用 | 1、返回面板 body 的 data 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_27_SPATIO_003）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | M_INNOV_DS_27_SPATIO_003 | INTEG |  | FUNC-01489 | endpoint_id=innov.topic-strategy.m_innov_ds_27_spatio_003 catalog_page_id=innov.topic-strategy 组合=P27-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01490 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 热点区域自动识别与预警 | 验证热点区域自动识别与预警功能，检查 module 非法填写 module=__invalid__ 后返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉选择「热点区域自动识别与预警」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id 为 M_INNOV_DS_27_SPATIO_003 且含 hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute |  | INTEG |  | FUNC-01490 | endpoint_id=innov.topic-strategy.m_innov_ds_27_spatio_003 catalog_page_id=innov.topic-strategy 组合=P27-03 场景=异常-入参-非法module catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01491 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 接口信息 | 验证科技专题战略分析的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 4；2、下拉名称与 §0 各 title 一致（科技专题战略分析指标清单、影响力评价与应用反馈、协同绩效与影响力智能评估、热点区域自动识别与预警）；3、默认项概览 method=GET、path=/innov/v1/innov/metrics；4、切换后概览对应热点区域自动识别与预警 POST /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01491 | catalog_page_id=innov.topic-strategy 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01492 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 科技专题战略分析 | 算法测试 | 验证科技专题战略分析的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「科技专题战略分析」；2.切换至「算法测试」tab；3.接口下拉切换到「协同绩效与影响力智能评估」 | 1、算法测试 tab 下拉共 4 项，名称与接口信息 tab、catalog 一致；2、切换后调用区 method 为 POST、path 为 /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对接口下拉共 4 项且名称与 §0 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01492 | catalog_page_id=innov.topic-strategy 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MET-01 | innov.topic-strategy.metrics | module=topic-strategy（sampleRequest） | 主路径（sampleRequest 传 module） |
| MET-02 | innov.topic-strategy.metrics | 不传 module | 与 sample 相反：省略可选 module |
| MET-03 | innov.topic-strategy.metrics | module=__invalid__ | 只破坏 module 这一个参数 |
| S25-01 | innov.topic-strategy.m_innov_ds_25_softsci_012 | module=topic-strategy（sampleRequest） | 主路径（sampleRequest 传 module） |
| S25-02 | innov.topic-strategy.m_innov_ds_25_softsci_012 | 不传 module | 与 sample 相反：省略可选 module |
| S25-03 | innov.topic-strategy.m_innov_ds_25_softsci_012 | module=__invalid__ | 只破坏 module 这一个参数 |
| E26-01 | innov.topic-strategy.m_innov_ds_26_eco_012 | module=topic-strategy（sampleRequest） | 主路径（sampleRequest 传 module） |
| E26-02 | innov.topic-strategy.m_innov_ds_26_eco_012 | 不传 module | 与 sample 相反：省略可选 module |
| E26-03 | innov.topic-strategy.m_innov_ds_26_eco_012 | module=__invalid__ | 只破坏 module 这一个参数 |
| P27-01 | innov.topic-strategy.m_innov_ds_27_spatio_003 | module=topic-strategy（sampleRequest） | 主路径（sampleRequest 传 module） |
| P27-02 | innov.topic-strategy.m_innov_ds_27_spatio_003 | 不传 module | 与 sample 相反：省略可选 module |
| P27-03 | innov.topic-strategy.m_innov_ds_27_spatio_003 | module=__invalid__ | 只破坏 module 这一个参数 |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 科技专题战略分析指标清单 | innov.topic-strategy.metrics | GET | /innov/v1/innov/metrics | module? | running |
| 影响力评价与应用反馈 | innov.topic-strategy.m_innov_ds_25_softsci_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_25_SOFTSCI_012/compute | module? | available |
| 协同绩效与影响力智能评估 | innov.topic-strategy.m_innov_ds_26_eco_012 | POST | /innov/v1/innov/metric/M_INNOV_DS_26_ECO_012/compute | module? | available |
| 热点区域自动识别与预警 | innov.topic-strategy.m_innov_ds_27_spatio_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_27_SPATIO_003/compute | module? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.topic-strategy.metrics | FUNC-01479、01480、01481 |
| innov.topic-strategy.m_innov_ds_25_softsci_012 | FUNC-01482、01483、01484 |
| innov.topic-strategy.m_innov_ds_26_eco_012 | FUNC-01485、01486、01487 |
| innov.topic-strategy.m_innov_ds_27_spatio_003 | FUNC-01488、01489、01490 |
| （页面清单） | FUNC-01491、01492 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 4 个 title 均在功能点列出现且各有 1 条 `场景=主流程`（FUNC-01479、01482、01485、01488）
- [x] 每个接口恰好 3 条：sampleRequest 主流程 + 与 sample 相反的不传 module + 非法 module
- [x] 正向预期逐字段写 sampleResponse；反向预期为 message 或 msg 指出 module 非法
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 无对应 Lxx：功能项/子功能项写待挂需规
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 四接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（01491、01492）
- [x] `coverage-fp.md` 已同步 FUNC-01479～01492

**统计**：catalog endpoint **4**；title **4**；FUNC 用例 **14** 条；主流程 **4**、备选 **4**、反向 **4**、清单 **2**；编号闭区间 **FUNC-01479**～**FUNC-01492**（R3 · innov.topic-strategy）。作废第二轮 API **02193**～**02204** 不复用。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **14** |
| 编号闭区间 | **FUNC-01479**～**FUNC-01492** |
| 接口向（不含清单） | **12** |
| 主流程 | **4** |
| 备选-参数组合 | **4** |
| 反向 | **4** |
| 清单 | **2** |
| 下一可用 FUNC 号（父控签收后） | **01493** |
