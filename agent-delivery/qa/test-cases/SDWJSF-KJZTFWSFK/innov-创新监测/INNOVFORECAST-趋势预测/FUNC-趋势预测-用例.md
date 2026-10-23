# 智能服务集群-科技专题服务算法库测试用例（趋势预测 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.forecast` · `catalog_page_id=innov.forecast` · path `/innov/forecast`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.forecast`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 DOM-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 领域趋势预测 | innov.forecast.domain | GET | /innov/v1/forecast/domain/{domainId} | domainId* | 2 |
| 2 | 创新点贡献度 | innov.forecast.contributions | GET | /innov/v1/forecast/contributions | domainId*；pageNum?；pageSize? | 6 |
| 3 | 主题突变 | innov.forecast.bursts | GET | /innov/v1/forecast/bursts | domainId? | 3 |

三个 title 均为 catalog `status=running`。合计 **11** 条接口调用 + §6.1 清单 **2** 条 = **13** 条。`领域趋势预测` 仅必填 path `domainId`；主流程跟 `sampleRequest`（`domainId=D-AI`）；必填反向为不传 `domainId`。`创新点贡献度` 主流程跟 sample（`domainId=D-AI`、`pageNum=1`、`pageSize=10`）；与 sample 相反为不传 `pageNum`、不传 `pageSize`；省略必填 `domainId` 与 `pageNum`、`pageSize` 各 1 条非法。`主题突变` 主流程传 `domainId=D-AI`；与 sample 相反为不传 `domainId`；`domainId` 另 1 条非法。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01151**～**FUNC-01163**，共 **13** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.forecast`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01151 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 领域趋势预测 | 验证领域趋势预测功能，检查填写 pathdomainId=D-AI 传 path domainId=D-AI 后返回历史与预测字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「领域趋势预测」；4.填写 pathdomainId=D-AI，点击调用 | 1、返回面板 body 的 data 含 forecastMode（string，示例 trend）、history（array，responseFields 历史年度）、predictions（array，responseFields 预测点）；2、history 元素含 statYear（number）、value（number）；3、sampleResponse 四行：statYear=2021、value=1200；statYear=2022、value=1480；statYear=2023、value=1760；statYear=2024、value=2010；4、predictions 元素含 predictPeriod（string）、predictValue（number）、ciLower（number）、ciUpper（number）；5、sampleResponse 两行：predictPeriod=2025、predictValue=2280、ciLower=2100、ciUpper=2460；predictPeriod=2026、predictValue=2510、ciLower=2280、ciUpper=2740 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/domain/{domainId} | M_INNOV_FORECAST_OUTPUT | INTEG |  | FUNC-01151 | endpoint_id=innov.forecast.domain catalog_page_id=innov.forecast 组合=DOM-01 场景=主流程 catalog_status=running 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01152 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 领域趋势预测 | 验证领域趋势预测功能，检查不传必填 domainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 domainId | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「领域趋势预测」；4.不传 domainId，点击调用 | 1、返回面板 body 的 message 或 msg 指出 domainId 缺失或非法；2、不返回含 history、predictions 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/domain/{domainId} |  | INTEG |  | FUNC-01152 | endpoint_id=innov.forecast.domain catalog_page_id=innov.forecast 组合=DOM-02 场景=异常-入参-缺domainId catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01153 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 创新点贡献度 | 验证创新点贡献度功能，检查填写 domainId=D-AI、pageNum=1、pageSize=10调用后返回贡献度排行 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageNum=1；pageSize=10 | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「创新点贡献度」；4.填写 domainId=D-AI、pageNum=1、pageSize=10，点击调用 | 1、返回面板 body 的 data 含 total（number，示例 2）、list（array，responseFields 贡献度排行）；2、list 元素含 targetId（string）、title（string）、eventType（string）、contribution（number）、predictValue（number）；3、sampleResponse 两行：targetId=EVT-001、title=深圳大模型开源发布会、eventType=breakthrough、contribution=0.186、predictValue=420；targetId=EVT-002、title=北京量子计算联合实验室揭牌、eventType=cooperation、contribution=0.124、predictValue=280 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions |  | INTEG |  | FUNC-01153 | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01154 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 创新点贡献度 | 验证创新点贡献度功能，检查不传 pageNum 后仍返回与 sampleResponse 同类结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageSize=10；不传 pageNum | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「创新点贡献度」；4.不传 pageNum，填写 domainId=D-AI、pageSize=10，点击调用 | 1、返回面板 body 的 data 仍含 total（number）、list（array）；2、list 元素仍含 targetId、title、eventType、contribution、predictValue；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions |  | INTEG |  | FUNC-01154 | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-02 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01155 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 创新点贡献度 | 验证创新点贡献度功能，检查不传 pageSize 后仍返回与 sampleResponse 同类结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageNum=1；不传 pageSize | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「创新点贡献度」；4.不传 pageSize，填写 domainId=D-AI、pageNum=1，点击调用 | 1、返回面板 body 的 data 仍含 total（number）、list（array）；2、list 元素仍含 targetId、title、eventType、contribution、predictValue；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions |  | INTEG |  | FUNC-01155 | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-03 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01156 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 创新点贡献度 | 验证创新点贡献度功能，检查不传必填 domainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum=1；pageSize=10；不传 domainId | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「创新点贡献度」；4.不传 domainId，填写 pageNum=1、pageSize=10，点击调用 | 1、返回面板 body 的 message 或 msg 指出 domainId 缺失或非法；2、不返回含 list 贡献度排行的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions |  | INTEG |  | FUNC-01156 | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-04 场景=异常-入参-缺domainId catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01157 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 创新点贡献度 | 验证创新点贡献度功能，检查 pageNum 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageSize=10；pageNum 取非法值 | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「创新点贡献度」；4.填写 domainId=D-AI、pageNum=not-a-page、pageSize=10，点击调用 | 1、返回面板 body 的 message 或 msg 指出 pageNum 非法；2、不返回含 list 贡献度排行的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions |  | INTEG |  | FUNC-01157 | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-05 场景=异常-入参-非法pageNum catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01158 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 创新点贡献度 | 验证创新点贡献度功能，检查 pageSize 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageNum=1；pageSize 取非法值 | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「创新点贡献度」；4.填写 domainId=D-AI、pageNum=1、pageSize=not-a-size，点击调用 | 1、返回面板 body 的 message 或 msg 指出 pageSize 非法；2、不返回含 list 贡献度排行的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions |  | INTEG |  | FUNC-01158 | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-06 场景=异常-入参-非法pageSize catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01159 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 主题突变 | 验证主题突变功能，检查填写 domainId=D-AI 传 domainId=D-AI 后返回主题突变数组 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「主题突变」；4.填写 domainId=D-AI，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 topicName（string，responseFields 主题）、burstScore（number，responseFields 强度）；3、sampleResponse 还含 domainId（string）、burstStart（string）；4、示例两行：topicName=多模态大模型、domainId=D-AI、burstStart=2023-06、burstScore=18.4；topicName=端侧推理芯片、domainId=D-AI、burstStart=2024-02、burstScore=14.1 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/bursts |  | INTEG |  | FUNC-01159 | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BUR-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01160 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 主题突变 | 验证主题突变功能，检查不传 domainId 后仍返回与 sampleResponse 同类结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 domainId | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「主题突变」；4.不传 domainId，点击调用 | 1、返回面板 body 的 data 仍为数组；2、元素仍含 topicName（string）、burstScore（number）、domainId（string）、burstStart（string）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/bursts |  | INTEG |  | FUNC-01160 | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BUR-02 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01161 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 主题突变 | 验证主题突变功能，检查 domainId 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId 取非法值 | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉选择「主题突变」；4.填写 domainId=__invalid__，点击调用 | 1、返回面板 body 的 message 或 msg 指出 domainId 非法；2、不返回含 topicName、burstScore 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/bursts |  | INTEG |  | FUNC-01161 | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BUR-03 场景=异常-入参-非法domainId catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01162 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 接口信息 | 验证M5 创新影响预测的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 3；2、下拉名称与 §0 各 title 一致（领域趋势预测、创新点贡献度、主题突变）；3、默认项概览 method=GET、path=/innov/v1/forecast/domain/{domainId}；4、切换后概览对应创新点贡献度 GET /innov/v1/forecast/contributions，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01162 | catalog_page_id=innov.forecast 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01163 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M5 创新影响预测 | 算法测试 | 验证M5 创新影响预测的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M5 创新影响预测」；2.切换至「算法测试」tab；3.接口下拉切换到「主题突变」 | 1、算法测试 tab 下拉共 3 项，名称与接口信息 tab、catalog 一致；2、切换后调用区 method 为 GET、path 为 /innov/v1/forecast/bursts；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对接口下拉共 3 项且名称与 §0 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01163 | catalog_page_id=innov.forecast 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| DOM-01 | innov.forecast.domain | path domainId=D-AI | 主路径（sampleRequest） |
| DOM-02 | innov.forecast.domain | 不传 domainId | 缺必填 domainId |
| CON-01 | innov.forecast.contributions | domainId=D-AI；pageNum=1；pageSize=10 | 主路径全参（sampleRequest） |
| CON-02 | innov.forecast.contributions | domainId=D-AI；不传 pageNum；pageSize=10 | 省略可选 pageNum（与 sample 相反） |
| CON-03 | innov.forecast.contributions | domainId=D-AI；pageNum=1；不传 pageSize | 省略可选 pageSize（与 sample 相反） |
| CON-04 | innov.forecast.contributions | 不传 domainId；pageNum=1；pageSize=10 | 缺必填 domainId |
| CON-05 | innov.forecast.contributions | domainId=D-AI；pageNum=not-a-page；pageSize=10 | 只破坏 pageNum |
| CON-06 | innov.forecast.contributions | domainId=D-AI；pageNum=1；pageSize=not-a-size | 只破坏 pageSize |
| BUR-01 | innov.forecast.bursts | domainId=D-AI | 主路径（sampleRequest） |
| BUR-02 | innov.forecast.bursts | 不传 domainId | 省略可选 domainId（与 sample 相反） |
| BUR-03 | innov.forecast.bursts | domainId=__invalid__ | 只破坏 domainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 领域趋势预测 | innov.forecast.domain | GET | /innov/v1/forecast/domain/{domainId} | domainId* | running |
| 创新点贡献度 | innov.forecast.contributions | GET | /innov/v1/forecast/contributions | domainId*；pageNum?；pageSize? | running |
| 主题突变 | innov.forecast.bursts | GET | /innov/v1/forecast/bursts | domainId? | running |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.forecast.domain | FUNC-01151、01152 |
| innov.forecast.contributions | FUNC-01153～01158 |
| innov.forecast.bursts | FUNC-01159～01161 |
| （页面清单） | FUNC-01162、01163 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 3 个 title（领域趋势预测、创新点贡献度、主题突变）均在功能点列出现，且各有 1 条主流程
- [x] 主流程跟 sampleRequest：领域 domainId=D-AI；贡献度 domainId=D-AI、pageNum=1、pageSize=10；主题突变 domainId=D-AI
- [x] 备选：贡献度省略 pageNum、省略 pageSize；主题突变省略 domainId
- [x] 反向：领域省略 domainId；贡献度省略 domainId、非法 pageNum、非法 pageSize；主题突变非法 domainId
- [x] 正向预期逐字段写出 sampleResponse；反向预期为 message 或 msg 指出该参数
- [x] 无登录 / Token / 401 / 424
- [x] A 线无对应 Lxx；未改 work
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 待挂需规 / 待挂需规
- [x] 三接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（01162、01163）
- [x] `coverage-fp.md` 已同步 FUNC-01151～01163；旧 API-01883～01893 作废

**统计**：合计 **13** 条（主流程 3、备选 3、反向 5、清单 2）；编号闭区间 **FUNC-01151**～**FUNC-01163**（R3 · innov.forecast）。金样 **FUNC-01151**（DOM-01）。
