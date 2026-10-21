# 智能服务集群-科技专题服务算法库测试用例（技术图谱 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.graph` · `catalog_page_id=innov.graph` · path `/innov/graph`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.graph`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 领域树）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 领域树 | innov.graph.domains | GET | /innov/v1/graph/domains | 无 | 1 |
| 2 | 领域子图 | innov.graph.subgraph | GET | /innov/v1/graph/subgraph | domainId*；limit? | 4 |
| 3 | 影响分排行 | innov.graph.rank | GET | /innov/v1/graph/influence/rank | domainId?；nodeType?；pageNum?；pageSize? | 9 |

三个 title 均为 catalog `status=running`。合计 **14** 条接口调用 + §6.1 清单 **2** 条 = **16** 条。无参 1 条主流程；有参为 1 条主流程（跟 `sampleRequest`）+ 每个可选参数与 sample 相反的传/不传 1 条 + 每个参数 1 条反向。必填反向只省略该参数。不交叉乘。

`领域子图` 的 `sampleRequest` 为 `domainId=D-AI`、`limit=60`。`影响分排行` 的 `sampleRequest` 为 `domainId=D-AI`、`pageNum=1`、`pageSize=20`，不传 `nodeType`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01115`～`01130`（闭区间 **16** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.graph`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01115 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 领域树 | 验证领域树功能，检查无参查询返回文档示例中的领域列表字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、无查询参数 | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「领域树」；4.保持请求参数为空，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 domainId（string，responseFields 领域 ID）、name（string，responseFields 领域名）；3、sampleResponse 还含 parentId（string）、level（number）、domainSource（string）；4、示例两行：domainId=D-AI、name=人工智能、parentId 空串、level=1、domainSource=seed；domainId=D-BIO、name=生物医药、parentId 空串、level=1、domainSource=seed | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/domains |  | INTEG |  |  | endpoint_id=innov.graph.domains catalog_page_id=innov.graph 场景=主流程 金样 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01116 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 领域子图 | 验证领域子图功能，检查填写 sampleRequest 所示参数 传 domainId=D-AI、limit=60 查询 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；limit=60 | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「领域子图」；4.填写 domainId=D-AI、limit=60，点击调用 | 1、返回面板 body 的 data 含 period（string，示例 2025Q1）、nodes（array，responseFields 节点）、edges（array，responseFields 边 src/dst）；2、nodes 元素含 nodeId（string）、nodeType（string）、name（string）、influenceScore（number）、rank（number）；3、示例两节点：nodeId=ORG-01、nodeType=org、name=鹏城实验室、influenceScore=88.2、rank=1；nodeId=SCH-01、nodeType=scholar、name=李研、influenceScore=76.4、rank=2；4、edges 元素含 src（string）、dst（string）、edgeType（string）、weight（number）；5、示例边 src=ORG-01、dst=SCH-01、edgeType=employ、weight=0.8 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/subgraph |  | INTEG |  |  | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=SUB-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01117 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 领域子图 | 验证领域子图功能，检查领域子图仅传 domainId、不传可选 limit（与 sampleRequest 相反） | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「领域子图」；4.不传 limit，填写 domainId=D-AI，点击调用 | 1、返回面板 body 的 data 仍含 period（string）、nodes（array）、edges（array）；2、nodes 元素仍含 nodeId、nodeType、name、influenceScore、rank；3、edges 元素仍含 src、dst、edgeType、weight；4、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/subgraph |  | INTEG |  |  | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=SUB-02 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01118 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 领域子图 | 验证领域子图功能，检查领域子图不传必填 domainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=60 保持合法 | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「领域子图」；4.不传 domainId，填写 limit=60，点击调用 | 1、返回面板 body 的 message 或 msg 指出 domainId 缺失；2、不返回含 nodes、edges 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/subgraph |  | INTEG |  |  | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=SUB-03 场景=异常-入参-缺domainId catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01119 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 领域子图 | 验证领域子图功能，检查领域子图 limit 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「领域子图」；4.填写 domainId=D-AI、limit=not-a-limit，点击调用 | 1、返回面板 body 的 message 或 msg 指出 limit 非法；2、不返回含 nodes、edges 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/subgraph |  | INTEG |  |  | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=SUB-04 场景=异常-入参-非法limit catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01120 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 影响分排行 | 验证影响分排行功能，检查填写 sampleRequest 所示参数 传 domainId=D-AI、pageNum=1、pageSize=20，不传 nodeType 查询 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageNum=1；pageSize=20；不传 nodeType | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「影响分排行」；4.不传 nodeType，填写 domainId=D-AI、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 含 total（number，示例 2）、period（string，示例 2025Q1）、list（array，responseFields 排行）；2、list 元素含 nodeId（string）、nodeType（string）、name（string）、influenceScore（number）、rankInDomain（number）；3、示例两行：nodeId=ORG-01、nodeType=org、name=鹏城实验室、influenceScore=88.2、rankInDomain=1；nodeId=SCH-01、nodeType=scholar、name=李研、influenceScore=76.4、rankInDomain=2 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG |  |  | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01121 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 影响分排行 | 验证影响分排行功能，检查影响分排行不传可选 domainId（与 sampleRequest 相反） | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum=1；pageSize=20；不传 nodeType | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「影响分排行」；4.不传 domainId、不传 nodeType，填写 pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 nodeId、nodeType、name、influenceScore、rankInDomain；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG |  |  | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-02 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01122 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 影响分排行 | 验证影响分排行功能，检查影响分排行传可选 nodeType=org（sampleRequest 未传该参数） | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；nodeType=org；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「影响分排行」；4.填写 domainId=D-AI、nodeType=org、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 nodeId、nodeType、name、influenceScore、rankInDomain；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG |  |  | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-03 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01123 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 影响分排行 | 验证影响分排行功能，检查影响分排行不传可选 pageNum（与 sampleRequest 相反） | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageSize=20；不传 nodeType | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「影响分排行」；4.不传 nodeType、不传 pageNum，填写 domainId=D-AI、pageSize=20，点击调用 | 1、返回面板 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 nodeId、nodeType、name、influenceScore、rankInDomain；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG |  |  | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-04 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01124 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 影响分排行 | 验证影响分排行功能，检查影响分排行不传可选 pageSize（与 sampleRequest 相反） | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageNum=1；不传 nodeType | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「影响分排行」；4.不传 nodeType、不传 pageSize，填写 domainId=D-AI、pageNum=1，点击调用 | 1、返回面板 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 nodeId、nodeType、name、influenceScore、rankInDomain；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG |  |  | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-05 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01125 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 影响分排行 | 验证影响分排行功能，检查影响分排行 domainId 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum=1；pageSize=20 保持合法 | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「影响分排行」；4.不传 nodeType，填写 domainId=__invalid__、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 domainId 非法；2、不返回含 list 排行的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank |  | INTEG |  |  | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-06 场景=异常-入参-非法domainId catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01126 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 影响分排行 | 验证影响分排行功能，检查影响分排行 nodeType 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「影响分排行」；4.填写 domainId=D-AI、nodeType=__invalid__、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 nodeType 非法；2、不返回含 list 排行的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank |  | INTEG |  |  | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-07 场景=异常-入参-非法nodeType catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01127 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 影响分排行 | 验证影响分排行功能，检查影响分排行 pageNum 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「影响分排行」；4.不传 nodeType，填写 domainId=D-AI、pageNum=not-a-page、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 pageNum 非法；2、不返回含 list 排行的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank |  | INTEG |  |  | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-08 场景=异常-入参-非法pageNum catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01128 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 影响分排行 | 验证影响分排行功能，检查影响分排行 pageSize 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、domainId=D-AI；pageNum=1 | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉选择「影响分排行」；4.不传 nodeType，填写 domainId=D-AI、pageNum=1、pageSize=not-a-size，点击调用 | 1、返回面板 body 的 message 或 msg 指出 pageSize 非法；2、不返回含 list 排行的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank |  | INTEG |  |  | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-09 场景=异常-入参-非法pageSize catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01129 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 接口信息 | 验证M2 创新点落图与赋分的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 3；2、下拉名称与 §0 各 title 一致（领域树、领域子图、影响分排行）；3、默认项概览 method=GET、path=/innov/v1/graph/domains；4、切换后概览对应影响分排行 GET /innov/v1/graph/influence/rank，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=innov.graph 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01130 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M2 创新点落图与赋分 | 算法测试 | 验证M2 创新点落图与赋分的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M2 创新点落图与赋分」；2.切换至「算法测试」tab；3.接口下拉切换到「领域子图」 | 1、算法测试 tab 下拉共 3 项，名称与接口信息 tab、catalog 一致；2、切换后调用区 method 为 GET、path 为 /innov/v1/graph/subgraph；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对接口下拉共 3 项且名称与 §0 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=innov.graph 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SUB-01 | innov.graph.subgraph | domainId=D-AI；limit=60 | 主路径全参（sampleRequest） |
| SUB-02 | innov.graph.subgraph | domainId=D-AI；不传 limit | 省略可选 limit（与 sample 相反） |
| SUB-03 | innov.graph.subgraph | 不传 domainId；limit=60 | 缺必填 domainId |
| SUB-04 | innov.graph.subgraph | domainId=D-AI；limit=not-a-limit | 只破坏 limit |
| RNK-01 | innov.graph.rank | domainId=D-AI；不传 nodeType；pageNum=1；pageSize=20 | 主路径（sampleRequest） |
| RNK-02 | innov.graph.rank | 不传 domainId；不传 nodeType；pageNum=1；pageSize=20 | 省略可选 domainId |
| RNK-03 | innov.graph.rank | domainId=D-AI；nodeType=org；pageNum=1；pageSize=20 | 传可选 nodeType（sample 未传） |
| RNK-04 | innov.graph.rank | domainId=D-AI；不传 nodeType；不传 pageNum；pageSize=20 | 省略可选 pageNum |
| RNK-05 | innov.graph.rank | domainId=D-AI；不传 nodeType；pageNum=1；不传 pageSize | 省略可选 pageSize |
| RNK-06 | innov.graph.rank | domainId=__invalid__；不传 nodeType；pageNum=1；pageSize=20 | 只破坏 domainId |
| RNK-07 | innov.graph.rank | domainId=D-AI；nodeType=__invalid__；pageNum=1；pageSize=20 | 只破坏 nodeType |
| RNK-08 | innov.graph.rank | domainId=D-AI；不传 nodeType；pageNum=not-a-page；pageSize=20 | 只破坏 pageNum |
| RNK-09 | innov.graph.rank | domainId=D-AI；不传 nodeType；pageNum=1；pageSize=not-a-size | 只破坏 pageSize |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 领域树 | innov.graph.domains | GET | /innov/v1/graph/domains | — | running |
| 领域子图 | innov.graph.subgraph | GET | /innov/v1/graph/subgraph | domainId*；limit? | running |
| 影响分排行 | innov.graph.rank | GET | /innov/v1/graph/influence/rank | domainId?；nodeType?；pageNum?；pageSize? | running |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.graph.domains | FUNC-01115 |
| innov.graph.subgraph | FUNC-01116、01117、01118、01119 |
| innov.graph.rank | FUNC-01120～01128 |
| （页面清单） | FUNC-01129、01130 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 3 个 title（领域树、领域子图、影响分排行）均在功能点列出现，且各有 1 条主流程
- [x] 主流程跟 sampleRequest：领域树无参；领域子图 domainId=D-AI、limit=60；影响分排行 domainId=D-AI、pageNum=1、pageSize=20、不传 nodeType
- [x] 可选参数与 sample 相反各 1 条：领域子图不传 limit；影响分排行不传 domainId、传 nodeType=org、不传 pageNum、不传 pageSize
- [x] 反向：领域子图省略 domainId、非法 limit 各 1 条；影响分排行 domainId、nodeType、pageNum、pageSize 各 1 条非法
- [x] 正向预期逐字段写出 sampleResponse（含 responseFields 未单列、但示例里出现的字段）；反向预期为 message 或 msg 指出该参数
- [x] 无登录 / Token / 401 / 424 / 只写 HTTP 4xx 的预期
- [x] A 线无对应 Lxx；未改 work
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 待挂需规 / 待挂需规
- [x] 三接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（01129、01130）
- [x] `coverage-fp.md` 已同步 FUNC-01115～01130

**统计**：合计 **16** 条（主流程 3、备选 5、反向 6、清单 2）；编号闭区间 **FUNC-01115**～**FUNC-01130**（R3 · innov.graph）。
