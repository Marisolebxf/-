# 智能服务集群-科技专题服务算法库测试用例（深圳创新监测 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.sz-monitoring` · `catalog_page_id=innov.sz-monitoring` · path `/innov/sz-monitoring`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.sz-monitoring`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 深圳创新监测指标清单 | innov.sz-monitoring.metrics | GET | /innov/v1/innov/metrics | module? | 3 |
| 2 | 深圳创新载体创新价值排名 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | module? | 3 |
| 3 | 创新价值排名 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | module? | 3 |
| 4 | 深圳科技发展指标对比 | innov.sz-monitoring.m_innov_city_compare_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | module? | 3 |
| 5 | 深圳科技竞争力 | innov.sz-monitoring.m_innov_city_compete_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | module? | 3 |
| 6 | 深圳创新能力指数 | innov.sz-monitoring.m_innov_city_index_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | module? | 3 |
| 7 | 深圳城市科技发展排名 | innov.sz-monitoring.m_innov_city_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | module? | 3 |
| 8 | 深圳与对标城市趋势 | innov.sz-monitoring.m_innov_city_trend_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | module? | 3 |

8 个 title 按 catalog `endpoints` 顺序各 3 条，合计 **24** 条接口调用。每个接口只有可选 `module`：1 条主流程（跟 `sampleRequest`，`module=sz-monitoring`）+ 1 条与 sample 相反的不传 `module` + 1 条非法 `module=__invalid__`。GET 的 `module` 为查询参数；POST 的 `module` 为请求体。另加 §6.1 页面清单 **2** 条，本册共 **26** 条。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01400`～`01425`（闭区间 **26** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.sz-monitoring`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01400 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳创新监测指标清单 | 验证深圳创新监测指标清单功能，检查填写 sampleRequest 所示参数 传 module=sz-monitoring 后返回 metrics 与 total 及元素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=sz-monitoring | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳创新监测指标清单」；4.填写 module=sz-monitoring，点击调用 | 1、返回面板 body 的 data 含 metrics（array，responseFields 指标元数据清单）、total（number，responseFields 指标数，sampleResponse 示例 7）；2、metrics 元素含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；3、sampleResponse 七行：metric_id=M_INNOV_CARRIER_VALUE_RANK_SZ、name=深圳创新载体创新价值排名、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_DS_06_CARRIER_003、name=创新价值排名、algorithm_type=MODEL、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_CITY_COMPARE_SZ、name=深圳科技发展指标对比、algorithm_type=MIXED、formula_status=mock、pending_ref=Q-MO-DS06-01；metric_id=M_INNOV_CITY_COMPETE_SZ、name=深圳科技竞争力、algorithm_type=MIXED、formula_status=mock、pending_ref=Q-MO-DS06-03；metric_id=M_INNOV_CITY_INDEX_SZ、name=深圳创新能力指数、algorithm_type=MIXED、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_CITY_RANK_SZ、name=深圳城市科技发展排名、algorithm_type=MIXED、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED；metric_id=M_INNOV_CITY_TREND_SZ、name=深圳与对标城市趋势、algorithm_type=MIXED、formula_status=mock、pending_ref=GAP-ALGO-TYPE-UNSIGNED | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  | FUNC-01400 | endpoint_id=innov.sz-monitoring.metrics catalog_page_id=innov.sz-monitoring 组合=MET-01 catalog_status=running 场景=主流程 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01401 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳创新监测指标清单 | 验证深圳创新监测指标清单功能，检查不传可选 module（与 sampleRequest 相反）后仍返回指标清单结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳创新监测指标清单」；4.不传 module，点击调用 | 1、返回面板 body 的 data 仍含 metrics（array）、total（number）；2、metrics 元素仍含 metric_id（string）、name（string）、algorithm_type（string）、formula_status（string）、pending_ref（string）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  | FUNC-01401 | endpoint_id=innov.sz-monitoring.metrics catalog_page_id=innov.sz-monitoring 组合=MET-02 catalog_status=running 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01402 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳创新监测指标清单 | 验证深圳创新监测指标清单功能，检查 module 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳创新监测指标清单」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metrics、total 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metrics |  | INTEG |  | FUNC-01402 | endpoint_id=innov.sz-monitoring.metrics catalog_page_id=innov.sz-monitoring 组合=MET-03 catalog_status=running 场景=异常-入参-非法module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01403 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳创新载体创新价值排名 | 验证深圳创新载体创新价值排名功能，检查填写 sampleRequest 所示参数 传 module=sz-monitoring 后返回 metric_id 与 hint 及 responseFields 声明的 metrics、total | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=sz-monitoring | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳创新载体创新价值排名」；4.填写 module=sz-monitoring，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CARRIER_VALUE_RANK_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | M_INNOV_CARRIER_VALUE_RANK_SZ | INTEG |  | FUNC-01403 | endpoint_id=innov.sz-monitoring.m_innov_carrier_value_rank_sz catalog_page_id=innov.sz-monitoring 组合=CVR-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01404 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳创新载体创新价值排名 | 验证深圳创新载体创新价值排名功能，检查不传可选 module（与 sampleRequest 相反）后仍返回与 sampleResponse 同类的 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳创新载体创新价值排名」；4.不传 module，点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CARRIER_VALUE_RANK_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | M_INNOV_CARRIER_VALUE_RANK_SZ | INTEG |  | FUNC-01404 | endpoint_id=innov.sz-monitoring.m_innov_carrier_value_rank_sz catalog_page_id=innov.sz-monitoring 组合=CVR-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01405 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳创新载体创新价值排名 | 验证深圳创新载体创新价值排名功能，检查 module 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳创新载体创新价值排名」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute |  | INTEG |  | FUNC-01405 | endpoint_id=innov.sz-monitoring.m_innov_carrier_value_rank_sz catalog_page_id=innov.sz-monitoring 组合=CVR-03 场景=异常-入参-非法module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01406 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 创新价值排名 | 验证创新价值排名功能，检查填写 sampleRequest 所示参数 传 module=sz-monitoring 后返回 metric_id 与 hint 及 responseFields 声明的 metrics、total | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=sz-monitoring | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「创新价值排名」；4.填写 module=sz-monitoring，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_DS_06_CARRIER_003）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | M_INNOV_DS_06_CARRIER_003 | INTEG |  | FUNC-01406 | endpoint_id=innov.sz-monitoring.m_innov_ds_06_carrier_003 catalog_page_id=innov.sz-monitoring 组合=C03-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01407 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 创新价值排名 | 验证创新价值排名功能，检查不传可选 module（与 sampleRequest 相反）后仍返回与 sampleResponse 同类的 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「创新价值排名」；4.不传 module，点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_DS_06_CARRIER_003）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | M_INNOV_DS_06_CARRIER_003 | INTEG |  | FUNC-01407 | endpoint_id=innov.sz-monitoring.m_innov_ds_06_carrier_003 catalog_page_id=innov.sz-monitoring 组合=C03-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01408 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 创新价值排名 | 验证创新价值排名功能，检查 module 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「创新价值排名」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute |  | INTEG |  | FUNC-01408 | endpoint_id=innov.sz-monitoring.m_innov_ds_06_carrier_003 catalog_page_id=innov.sz-monitoring 组合=C03-03 场景=异常-入参-非法module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01409 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳科技发展指标对比 | 验证深圳科技发展指标对比功能，检查填写 sampleRequest 所示参数 传 module=sz-monitoring 后返回 metric_id 与 hint 及 responseFields 声明的 metrics、total | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=sz-monitoring | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳科技发展指标对比」；4.填写 module=sz-monitoring，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_COMPARE_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | M_INNOV_CITY_COMPARE_SZ | INTEG |  | FUNC-01409 | endpoint_id=innov.sz-monitoring.m_innov_city_compare_sz catalog_page_id=innov.sz-monitoring 组合=CMP-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01410 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳科技发展指标对比 | 验证深圳科技发展指标对比功能，检查不传可选 module（与 sampleRequest 相反）后仍返回与 sampleResponse 同类的 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳科技发展指标对比」；4.不传 module，点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_COMPARE_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | M_INNOV_CITY_COMPARE_SZ | INTEG |  | FUNC-01410 | endpoint_id=innov.sz-monitoring.m_innov_city_compare_sz catalog_page_id=innov.sz-monitoring 组合=CMP-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01411 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳科技发展指标对比 | 验证深圳科技发展指标对比功能，检查 module 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳科技发展指标对比」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute |  | INTEG |  | FUNC-01411 | endpoint_id=innov.sz-monitoring.m_innov_city_compare_sz catalog_page_id=innov.sz-monitoring 组合=CMP-03 场景=异常-入参-非法module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01412 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳科技竞争力 | 验证深圳科技竞争力功能，检查填写 sampleRequest 所示参数 传 module=sz-monitoring 后返回 metric_id 与 hint 及 responseFields 声明的 metrics、total | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=sz-monitoring | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳科技竞争力」；4.填写 module=sz-monitoring，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_COMPETE_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | M_INNOV_CITY_COMPETE_SZ | INTEG |  | FUNC-01412 | endpoint_id=innov.sz-monitoring.m_innov_city_compete_sz catalog_page_id=innov.sz-monitoring 组合=CPT-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01413 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳科技竞争力 | 验证深圳科技竞争力功能，检查不传可选 module（与 sampleRequest 相反）后仍返回与 sampleResponse 同类的 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳科技竞争力」；4.不传 module，点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_COMPETE_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | M_INNOV_CITY_COMPETE_SZ | INTEG |  | FUNC-01413 | endpoint_id=innov.sz-monitoring.m_innov_city_compete_sz catalog_page_id=innov.sz-monitoring 组合=CPT-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01414 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳科技竞争力 | 验证深圳科技竞争力功能，检查 module 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳科技竞争力」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute |  | INTEG |  | FUNC-01414 | endpoint_id=innov.sz-monitoring.m_innov_city_compete_sz catalog_page_id=innov.sz-monitoring 组合=CPT-03 场景=异常-入参-非法module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01415 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳创新能力指数 | 验证深圳创新能力指数功能，检查填写 sampleRequest 所示参数 传 module=sz-monitoring 后返回 metric_id 与 hint 及 responseFields 声明的 metrics、total | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=sz-monitoring | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳创新能力指数」；4.填写 module=sz-monitoring，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_INDEX_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | M_INNOV_CITY_INDEX_SZ | INTEG |  | FUNC-01415 | endpoint_id=innov.sz-monitoring.m_innov_city_index_sz catalog_page_id=innov.sz-monitoring 组合=IDX-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01416 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳创新能力指数 | 验证深圳创新能力指数功能，检查不传可选 module（与 sampleRequest 相反）后仍返回与 sampleResponse 同类的 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳创新能力指数」；4.不传 module，点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_INDEX_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | M_INNOV_CITY_INDEX_SZ | INTEG |  | FUNC-01416 | endpoint_id=innov.sz-monitoring.m_innov_city_index_sz catalog_page_id=innov.sz-monitoring 组合=IDX-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01417 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳创新能力指数 | 验证深圳创新能力指数功能，检查 module 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳创新能力指数」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute |  | INTEG |  | FUNC-01417 | endpoint_id=innov.sz-monitoring.m_innov_city_index_sz catalog_page_id=innov.sz-monitoring 组合=IDX-03 场景=异常-入参-非法module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01418 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳城市科技发展排名 | 验证深圳城市科技发展排名功能，检查填写 sampleRequest 所示参数 传 module=sz-monitoring 后返回 metric_id 与 hint 及 responseFields 声明的 metrics、total | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=sz-monitoring | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳城市科技发展排名」；4.填写 module=sz-monitoring，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_RANK_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | M_INNOV_CITY_RANK_SZ | INTEG |  | FUNC-01418 | endpoint_id=innov.sz-monitoring.m_innov_city_rank_sz catalog_page_id=innov.sz-monitoring 组合=RNK-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01419 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳城市科技发展排名 | 验证深圳城市科技发展排名功能，检查不传可选 module（与 sampleRequest 相反）后仍返回与 sampleResponse 同类的 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳城市科技发展排名」；4.不传 module，点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_RANK_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | M_INNOV_CITY_RANK_SZ | INTEG |  | FUNC-01419 | endpoint_id=innov.sz-monitoring.m_innov_city_rank_sz catalog_page_id=innov.sz-monitoring 组合=RNK-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01420 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳城市科技发展排名 | 验证深圳城市科技发展排名功能，检查 module 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳城市科技发展排名」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute |  | INTEG |  | FUNC-01420 | endpoint_id=innov.sz-monitoring.m_innov_city_rank_sz catalog_page_id=innov.sz-monitoring 组合=RNK-03 场景=异常-入参-非法module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01421 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳与对标城市趋势 | 验证深圳与对标城市趋势功能，检查填写 sampleRequest 所示参数 传 module=sz-monitoring 后返回 metric_id 与 hint 及 responseFields 声明的 metrics、total | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=sz-monitoring | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳与对标城市趋势」；4.填写 module=sz-monitoring，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_INNOV_CITY_TREND_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 metrics（array，指标元数据清单）、total（number，指标数），sampleResponse 未给出这两字段的示例值，返回中应含 metrics、total 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | M_INNOV_CITY_TREND_SZ | INTEG |  | FUNC-01421 | endpoint_id=innov.sz-monitoring.m_innov_city_trend_sz catalog_page_id=innov.sz-monitoring 组合=TRD-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01422 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳与对标城市趋势 | 验证深圳与对标城市趋势功能，检查不传可选 module（与 sampleRequest 相反）后仍返回与 sampleResponse 同类的 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 module | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳与对标城市趋势」；4.不传 module，点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_INNOV_CITY_TREND_SZ）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 声明的 metrics（array，指标元数据清单）、total（number，指标数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | M_INNOV_CITY_TREND_SZ | INTEG |  | FUNC-01422 | endpoint_id=innov.sz-monitoring.m_innov_city_trend_sz catalog_page_id=innov.sz-monitoring 组合=TRD-02 场景=备选-参数组合 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01423 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 深圳与对标城市趋势 | 验证深圳与对标城市趋势功能，检查 module 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、module=__invalid__ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉选择「深圳与对标城市趋势」；4.填写 module=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 module 非法；2、不返回含 metric_id、hint 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute |  | INTEG |  | FUNC-01423 | endpoint_id=innov.sz-monitoring.m_innov_city_trend_sz catalog_page_id=innov.sz-monitoring 组合=TRD-03 场景=异常-入参-非法module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01424 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 接口信息 | 验证深圳创新监测的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 8；2、下拉名称与 §0 各 title 一致（深圳创新监测指标清单、深圳创新载体创新价值排名、创新价值排名、深圳科技发展指标对比、深圳科技竞争力、深圳创新能力指数、深圳城市科技发展排名、深圳与对标城市趋势）；3、默认项概览 method=GET、path=/innov/v1/innov/metrics；4、切换后概览对应深圳与对标城市趋势 POST /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01424 | catalog_page_id=innov.sz-monitoring 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01425 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 深圳创新监测 | 算法测试 | 验证深圳创新监测的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「深圳创新监测」；2.切换至「算法测试」tab；3.接口下拉切换到「创新价值排名」 | 1、算法测试 tab 下拉共 8 项，名称与接口信息 tab、catalog 一致；2、切换后调用区 method 为 POST、path 为 /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对接口下拉共 8 项且名称与 §0 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01425 | catalog_page_id=innov.sz-monitoring 场景=算法测试-清单 |
---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MET-01 | innov.sz-monitoring.metrics | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| MET-02 | innov.sz-monitoring.metrics | 不传 module | 与 sampleRequest 相反：省略可选 module |
| MET-03 | innov.sz-monitoring.metrics | module=__invalid__ | 只破坏 module 这一个参数 |
| CVR-01 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| CVR-02 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| CVR-03 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| C03-01 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| C03-02 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | 不传 module | 与 sampleRequest 相反：省略可选 module |
| C03-03 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | module=__invalid__ | 只破坏 module 这一个参数 |
| CMP-01 | innov.sz-monitoring.m_innov_city_compare_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| CMP-02 | innov.sz-monitoring.m_innov_city_compare_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| CMP-03 | innov.sz-monitoring.m_innov_city_compare_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| CPT-01 | innov.sz-monitoring.m_innov_city_compete_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| CPT-02 | innov.sz-monitoring.m_innov_city_compete_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| CPT-03 | innov.sz-monitoring.m_innov_city_compete_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| IDX-01 | innov.sz-monitoring.m_innov_city_index_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| IDX-02 | innov.sz-monitoring.m_innov_city_index_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| IDX-03 | innov.sz-monitoring.m_innov_city_index_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| RNK-01 | innov.sz-monitoring.m_innov_city_rank_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| RNK-02 | innov.sz-monitoring.m_innov_city_rank_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| RNK-03 | innov.sz-monitoring.m_innov_city_rank_sz | module=__invalid__ | 只破坏 module 这一个参数 |
| TRD-01 | innov.sz-monitoring.m_innov_city_trend_sz | module=sz-monitoring（sampleRequest） | 主路径（sampleRequest 传 module） |
| TRD-02 | innov.sz-monitoring.m_innov_city_trend_sz | 不传 module | 与 sampleRequest 相反：省略可选 module |
| TRD-03 | innov.sz-monitoring.m_innov_city_trend_sz | module=__invalid__ | 只破坏 module 这一个参数 |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 深圳创新监测指标清单 | innov.sz-monitoring.metrics | GET | /innov/v1/innov/metrics | module? | running |
| 深圳创新载体创新价值排名 | innov.sz-monitoring.m_innov_carrier_value_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CARRIER_VALUE_RANK_SZ/compute | module? | available |
| 创新价值排名 | innov.sz-monitoring.m_innov_ds_06_carrier_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_06_CARRIER_003/compute | module? | available |
| 深圳科技发展指标对比 | innov.sz-monitoring.m_innov_city_compare_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPARE_SZ/compute | module? | available |
| 深圳科技竞争力 | innov.sz-monitoring.m_innov_city_compete_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_COMPETE_SZ/compute | module? | available |
| 深圳创新能力指数 | innov.sz-monitoring.m_innov_city_index_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_INDEX_SZ/compute | module? | available |
| 深圳城市科技发展排名 | innov.sz-monitoring.m_innov_city_rank_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_RANK_SZ/compute | module? | available |
| 深圳与对标城市趋势 | innov.sz-monitoring.m_innov_city_trend_sz | POST | /innov/v1/innov/metric/M_INNOV_CITY_TREND_SZ/compute | module? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.sz-monitoring.metrics | FUNC-01400、01401、01402 |
| innov.sz-monitoring.m_innov_carrier_value_rank_sz | FUNC-01403、01404、01405 |
| innov.sz-monitoring.m_innov_ds_06_carrier_003 | FUNC-01406、01407、01408 |
| innov.sz-monitoring.m_innov_city_compare_sz | FUNC-01409、01410、01411 |
| innov.sz-monitoring.m_innov_city_compete_sz | FUNC-01412、01413、01414 |
| innov.sz-monitoring.m_innov_city_index_sz | FUNC-01415、01416、01417 |
| innov.sz-monitoring.m_innov_city_rank_sz | FUNC-01418、01419、01420 |
| innov.sz-monitoring.m_innov_city_trend_sz | FUNC-01421、01422、01423 |
| （页面清单） | FUNC-01424、01425 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 8 个 title 均在功能点列出现且各有 1 条 `场景=主流程`（FUNC-01400、01403、01406、01409、01412、01415、01418、01421）
- [x] 每个接口恰好 3 条：sampleRequest 主流程 + 与 sample 相反的不传 module + 非法 module
- [x] 正向预期逐字段写 sampleResponse；反向预期为 message 或 msg 指出 module 非法
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 无对应 Lxx：功能项/子功能项写待挂需规
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 八接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（01424、01425）
- [x] `coverage-fp.md` 已同步 FUNC-01400～01425

**统计**：catalog endpoint **8**；title **8**；FUNC 用例 **26** 条；主流程 **8**、备选 **8**、反向 **8**、清单 **2**；编号闭区间 **FUNC-01400**～**FUNC-01425**（R3 · innov.sz-monitoring）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **26** |
| 编号闭区间 | **FUNC-01400**～**FUNC-01425** |
| 接口向（不含清单） | **24** |
| 主流程 | **8** |
| 备选-参数组合 | **8** |
| 反向 | **8** |
| 清单 | **2** |
| 已删 API 册 | `API-深圳创新监测-用例.md`（API-02118～02141 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
