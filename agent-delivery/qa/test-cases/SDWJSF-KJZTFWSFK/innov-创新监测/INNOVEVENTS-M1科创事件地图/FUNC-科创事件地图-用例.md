# 智能服务集群-科技专题服务算法库测试用例（M1 科创事件地图 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=innov.events` · `catalog_page_id=innov.events` · path `/innov/events`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.events`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 LST-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | 参数 | 条数 |
|---|------------------------|-------------|--------|------|------|------|
| 1 | 事件列表 | innov.events.list | GET | /innov/v1/events | startTime? endTime? eventTypes? importanceLevels? keyword? pageNum? pageSize? | 15 |
| 2 | 地图点位 | innov.events.geo | GET | /innov/v1/events | mode* | 2 |
| 3 | 热力聚合 | innov.events.heatmap | GET | /innov/v1/events/heatmap | startTime? endTime? | 5 |
| 4 | 事件详情 | innov.events.detail | GET | /innov/v1/events/{eventId} | eventId* | 2 |
| 5 | 关联分析 | innov.events.relations | GET | /innov/v1/events/{eventId}/relations | eventId* | 2 |
| 6 | 事件类型字典 | innov.events.types | GET | /innov/v1/dict/event-types | 无 | 1 |

六个 title 均为 catalog `status=running`。合计 **27** 条接口调用 + §6.1 清单 **2** 条 = **29** 条。无参 1 条主流程；有参为 1 条主流程（跟 `sampleRequest`）+ 每个可选参数与 sample 相反的传/不传 1 条 + 每个参数 1 条反向。必填反向只省略该参数。不交叉乘。

`事件列表` 与 `地图点位` 同 path `GET /innov/v1/events`，用例都留在本页，备注写 `endpoint_id` 区分。列表 sample 不传 `mode`；点位 sample 为 `mode=geo`。

`事件列表` 的 `sampleRequest` 只传 `pageNum=1`、`pageSize=20`。`startTime`、`endTime` 的合法补传取各自 params.example。`eventTypes`、`importanceLevels`、`keyword` 的 params.example 为空：`eventTypes` 补传取同接口 sampleResponse 的 `eventType=breakthrough`；`importanceLevels` 补传取说明中的 `1`；`keyword` 补传取 sampleResponse 标题中的「大模型」。

`热力聚合` 的 `sampleRequest` 为 `{}`，两个 params.example 也为空。合法补传借用同页事件列表的时间 example：`2024-01-01 00:00:00`、`2025-12-31 23:59:59`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01086`～`01114`（闭区间 **29** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.events`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01086 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查填写 sampleRequest 所示参数 传 pageNum=1、pageSize=20，不传 startTime、endTime、eventTypes、importanceLevels、keyword 后返回 total 与 list 及元素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum=1、pageSize=20 取自 sampleRequest | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传 startTime、endTime、eventTypes、importanceLevels、keyword，填写 pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 为对象；2、total（number，responseFields 总数，示例 3）；3、list（array，responseFields 事件列表）；4、list 元素含 eventId（string）、title（string）、importanceLevel（number）、importanceScore（number）、eventTime（string）、eventType（string）、cityCode（string）；5、sampleResponse 示例：EVT-001/深圳大模型开源发布会/1/92/2025-03-12 10:00:00/breakthrough/440300，EVT-002/北京量子计算联合实验室揭牌/2/81/2025-02-20 09:30:00/cooperation/110000，EVT-003/上海生物医药产业政策出台/3/64/2024-11-08 14:00:00/policy/310000 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events | M_INNOV_EVENT_COUNT | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-01 场景=主流程 金样 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01087 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表补传可选 startTime，pageNum、pageSize 保持 sampleRequest | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、startTime 使用 params.example；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传 endTime、eventTypes、importanceLevels、keyword，填写 startTime=2024-01-0100:00:00、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 为对象；2、total（number，responseFields 总数，示例 3）；3、list（array，responseFields 事件列表）；4、list 元素含 eventId（string）、title（string）、importanceLevel（number）、importanceScore（number）、eventTime（string）、eventType（string）、cityCode（string）；5、sampleResponse 示例：EVT-001/深圳大模型开源发布会/1/92/2025-03-12 10:00:00/breakthrough/440300，EVT-002/北京量子计算联合实验室揭牌/2/81/2025-02-20 09:30:00/cooperation/110000，EVT-003/上海生物医药产业政策出台/3/64/2024-11-08 14:00:00/policy/310000 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events | M_INNOV_EVENT_COUNT | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-02 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01088 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表补传可选 endTime，pageNum、pageSize 保持 sampleRequest | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、endTime 使用 params.example；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传 startTime、eventTypes、importanceLevels、keyword，填写 endTime=2025-12-3123:59:59、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 为对象；2、total（number，responseFields 总数，示例 3）；3、list（array，responseFields 事件列表）；4、list 元素含 eventId（string）、title（string）、importanceLevel（number）、importanceScore（number）、eventTime（string）、eventType（string）、cityCode（string）；5、sampleResponse 示例：EVT-001/深圳大模型开源发布会/1/92/2025-03-12 10:00:00/breakthrough/440300，EVT-002/北京量子计算联合实验室揭牌/2/81/2025-02-20 09:30:00/cooperation/110000，EVT-003/上海生物医药产业政策出台/3/64/2024-11-08 14:00:00/policy/310000 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events | M_INNOV_EVENT_COUNT | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-03 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01089 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表补传可选 eventTypes=breakthrough，pageNum、pageSize 保持 sampleRequest | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、eventTypes 取 sampleResponse 的 eventType；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传 startTime、endTime、importanceLevels、keyword，填写 eventTypes=breakthrough、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 为对象；2、total（number，responseFields 总数，示例 3）；3、list（array，responseFields 事件列表）；4、list 元素含 eventId（string）、title（string）、importanceLevel（number）、importanceScore（number）、eventTime（string）、eventType（string）、cityCode（string）；5、sampleResponse 示例：EVT-001/深圳大模型开源发布会/1/92/2025-03-12 10:00:00/breakthrough/440300，EVT-002/北京量子计算联合实验室揭牌/2/81/2025-02-20 09:30:00/cooperation/110000，EVT-003/上海生物医药产业政策出台/3/64/2024-11-08 14:00:00/policy/310000 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events | M_INNOV_EVENT_COUNT | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-04 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01090 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表补传可选 importanceLevels=1，pageNum、pageSize 保持 sampleRequest | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、importanceLevels 取说明中的 1；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传 startTime、endTime、eventTypes、keyword，填写 importanceLevels=1、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 为对象；2、total（number，responseFields 总数，示例 3）；3、list（array，responseFields 事件列表）；4、list 元素含 eventId（string）、title（string）、importanceLevel（number）、importanceScore（number）、eventTime（string）、eventType（string）、cityCode（string）；5、sampleResponse 示例：EVT-001/深圳大模型开源发布会/1/92/2025-03-12 10:00:00/breakthrough/440300，EVT-002/北京量子计算联合实验室揭牌/2/81/2025-02-20 09:30:00/cooperation/110000，EVT-003/上海生物医药产业政策出台/3/64/2024-11-08 14:00:00/policy/310000 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events | M_INNOV_EVENT_COUNT | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-05 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01091 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表补传可选 keyword=大模型，pageNum、pageSize 保持 sampleRequest | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、keyword 取 sample 标题中的大模型；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传 startTime、endTime、eventTypes、importanceLevels，填写 keyword=大模型、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 data 为对象；2、total（number，responseFields 总数，示例 3）；3、list（array，responseFields 事件列表）；4、list 元素含 eventId（string）、title（string）、importanceLevel（number）、importanceScore（number）、eventTime（string）、eventType（string）、cityCode（string）；5、sampleResponse 示例：EVT-001/深圳大模型开源发布会/1/92/2025-03-12 10:00:00/breakthrough/440300，EVT-002/北京量子计算联合实验室揭牌/2/81/2025-02-20 09:30:00/cooperation/110000，EVT-003/上海生物医药产业政策出台/3/64/2024-11-08 14:00:00/policy/310000 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events | M_INNOV_EVENT_COUNT | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-06 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01092 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表不传可选 pageNum（与 sample 相反），pageSize 保持 20 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 pageNum；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传 pageNum、不传 startTime、endTime、eventTypes、importanceLevels、keyword，填写 pageSize=20，点击调用 | 1、返回面板 body 的 data 为对象；2、total（number，responseFields 总数，示例 3）；3、list（array，responseFields 事件列表）；4、list 元素含 eventId（string）、title（string）、importanceLevel（number）、importanceScore（number）、eventTime（string）、eventType（string）、cityCode（string）；5、sampleResponse 示例：EVT-001/深圳大模型开源发布会/1/92/2025-03-12 10:00:00/breakthrough/440300，EVT-002/北京量子计算联合实验室揭牌/2/81/2025-02-20 09:30:00/cooperation/110000，EVT-003/上海生物医药产业政策出台/3/64/2024-11-08 14:00:00/policy/310000 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events | M_INNOV_EVENT_COUNT | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-07 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01093 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表不传可选 pageSize（与 sample 相反），pageNum 保持 1 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum=1；不传 pageSize | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传 pageSize、不传 startTime、endTime、eventTypes、importanceLevels、keyword，填写 pageNum=1，点击调用 | 1、返回面板 body 的 data 为对象；2、total（number，responseFields 总数，示例 3）；3、list（array，responseFields 事件列表）；4、list 元素含 eventId（string）、title（string）、importanceLevel（number）、importanceScore（number）、eventTime（string）、eventType（string）、cityCode（string）；5、sampleResponse 示例：EVT-001/深圳大模型开源发布会/1/92/2025-03-12 10:00:00/breakthrough/440300，EVT-002/北京量子计算联合实验室揭牌/2/81/2025-02-20 09:30:00/cooperation/110000，EVT-003/上海生物医药产业政策出台/3/64/2024-11-08 14:00:00/policy/310000 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events | M_INNOV_EVENT_COUNT | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-08 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01094 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表 startTime 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、startTime 取非法值；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传其余可选参数，填写 startTime=not-a-date、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 startTime 非法；2、不返回含 total 与 list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events |  | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-09 场景=异常-入参-非法startTime catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01095 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表 endTime 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、endTime 取非法值；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传其余可选参数，填写 endTime=not-a-date、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 endTime 非法；2、不返回含 total 与 list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events |  | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-10 场景=异常-入参-非法endTime catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01096 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表 eventTypes 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、eventTypes 取非法值；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传其余可选参数，填写 eventTypes=__invalid__、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 eventTypes 非法；2、不返回含 total 与 list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events |  | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-11 场景=异常-入参-非法eventTypes catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01097 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表 importanceLevels 超出 1/2/3时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、importanceLevels 取非法值；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传其余可选参数，填写 importanceLevels=4、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 importanceLevels 非法；2、不返回含 total 与 list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events |  | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-12 场景=异常-入参-非法importanceLevels catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01098 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表 keyword 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、keyword 取非法值；pageNum=1；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传其余可选参数，填写 keyword=__invalid__、pageNum=1、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 keyword 非法；2、不返回含 total 与 list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events |  | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-13 场景=异常-入参-非法keyword catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01099 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表 pageNum 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum 取非法值；pageSize=20 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传其余可选参数，填写 pageNum=-1、pageSize=20，点击调用 | 1、返回面板 body 的 message 或 msg 指出 pageNum 非法；2、不返回含 total 与 list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events |  | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-14 场景=异常-入参-非法pageNum catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01100 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件列表 | 验证事件列表功能，检查事件列表 pageSize 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、pageNum=1；pageSize 取非法值 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件列表」；4.不传其余可选参数，填写 pageNum=1、pageSize=0，点击调用 | 1、返回面板 body 的 message 或 msg 指出 pageSize 非法；2、不返回含 total 与 list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events |  | INTEG |  |  | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=LST-15 场景=异常-入参-非法pageSize catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01101 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 地图点位 | 验证地图点位功能，检查地图点位按 sampleRequest 传 mode=geo | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、mode 使用 sampleRequest 的 geo | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「地图点位」；4.填写 mode=geo，点击调用 | 1、返回面板 body 的 data 为对象；2、type（string，responseFields GeoJSON 类型，示例 FeatureCollection）；3、features（array，responseFields 点位 Feature）；4、features 元素含 type（string，示例 Feature）、geometry.type（string，示例 Point）、geometry.coordinates（number 数组，示例 113.94 与 22.54、116.4 与 39.9）、properties.eventId（string）、properties.title（string）、properties.importanceLevel（number）、properties.importanceScore（number）、properties.eventType（string）；5、sampleResponse 两点：EVT-001/深圳大模型开源发布会/importanceLevel=1/importanceScore=92/eventType=breakthrough；EVT-002/北京量子计算联合实验室揭牌/2/81/cooperation | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events |  | INTEG |  |  | endpoint_id=innov.events.geo catalog_page_id=innov.events 组合=GEO-01 场景=主流程 同 path 与事件列表 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01102 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 地图点位 | 验证地图点位功能，检查地图点位不传必填 mode时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 mode | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「地图点位」；4.不传 mode（请求 GET /innov/v1/events，无查询参数），点击调用 | 1、返回面板 body 的 message 或 msg 指出 mode 缺失或非法；2、不返回含 type 为 FeatureCollection 且含 features 的成功点位结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events |  | INTEG |  |  | endpoint_id=innov.events.geo catalog_page_id=innov.events 组合=GEO-02 场景=异常-入参-缺mode 同 path 与事件列表 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01103 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 热力聚合 | 验证热力聚合功能，检查热力聚合按 sampleRequest 不传 startTime、endTime | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、sampleRequest 为空，不传时间参数 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「热力聚合」；4.不传 startTime、不传 endTime，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 lng（number，responseFields 经度）、lat（number，responseFields 纬度）、weight（number，responseFields 权重，说明为 importance_score）；3、sampleResponse 三点：lng=113.94、lat=22.54、weight=92；lng=116.4、lat=39.9、weight=81；lng=121.47、lat=31.23、weight=64 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events/heatmap |  | INTEG |  |  | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=HM-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01104 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 热力聚合 | 验证热力聚合功能，检查热力聚合补传可选 startTime（与 sample 相反），不传 endTime | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、startTime 借用同页列表时间 example；不传 endTime | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「热力聚合」；4.不传 endTime，填写 startTime=2024-01-0100:00:00，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 lng（number，responseFields 经度）、lat（number，responseFields 纬度）、weight（number，responseFields 权重，说明为 importance_score）；3、sampleResponse 三点：lng=113.94、lat=22.54、weight=92；lng=116.4、lat=39.9、weight=81；lng=121.47、lat=31.23、weight=64 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events/heatmap |  | INTEG |  |  | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=HM-02 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01105 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 热力聚合 | 验证热力聚合功能，检查热力聚合补传可选 endTime（与 sample 相反），不传 startTime | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、endTime 借用同页列表时间 example；不传 startTime | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「热力聚合」；4.不传 startTime，填写 endTime=2025-12-3123:59:59，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 lng（number，responseFields 经度）、lat（number，responseFields 纬度）、weight（number，responseFields 权重，说明为 importance_score）；3、sampleResponse 三点：lng=113.94、lat=22.54、weight=92；lng=116.4、lat=39.9、weight=81；lng=121.47、lat=31.23、weight=64 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events/heatmap |  | INTEG |  |  | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=HM-03 场景=备选-参数组合 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01106 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 热力聚合 | 验证热力聚合功能，检查热力聚合 startTime 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、startTime 取非法值 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「热力聚合」；4.不传 endTime，填写 startTime=not-a-date，点击调用 | 1、返回面板 body 的 message 或 msg 指出 startTime 非法；2、不返回含 lng、lat、weight 的成功热力数组 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events/heatmap |  | INTEG |  |  | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=HM-04 场景=异常-入参-非法startTime catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01107 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 热力聚合 | 验证热力聚合功能，检查热力聚合 endTime 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、endTime 取非法值 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「热力聚合」；4.不传 startTime，填写 endTime=not-a-date，点击调用 | 1、返回面板 body 的 message 或 msg 指出 endTime 非法；2、不返回含 lng、lat、weight 的成功热力数组 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events/heatmap |  | INTEG |  |  | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=HM-05 场景=异常-入参-非法endTime catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01108 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件详情 | 验证事件详情功能，检查事件详情按 sampleRequest 传 path eventId=EVT-001 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、eventId=EVT-001 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件详情」；4.填写 patheventId=EVT-001，点击调用 | 1、返回面板 body 的 data 为对象；2、eventId（string，responseFields 事件 ID，示例 EVT-001）；3、importanceDetail（array，responseFields 评分分项）；4、sampleResponse 同层还含 title（string，示例 深圳大模型开源发布会）、eventType（string，示例 breakthrough）、eventTime（string，示例 2025-03-12 10:00:00）、importanceLevel（number，示例 1）、importanceScore（number，示例 92）、summary（string，示例 深圳发布开源大模型并开放权重。）；5、importanceDetail 元素含 k（string）、v（number），示例 影响力/40、新颖性/32、传播/20 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events/{eventId} |  | INTEG |  |  | endpoint_id=innov.events.detail catalog_page_id=innov.events 组合=DET-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01109 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件详情 | 验证事件详情功能，检查事件详情不传必填 eventId时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 eventId | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件详情」；4.不传 path eventId（请求 `/innov/v1/events/`，path 段为空），点击调用 | 1、返回面板 body 的 message 或 msg 指出 eventId 缺失或非法；2、不返回含 eventId 与 importanceDetail 的成功详情 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events/{eventId} |  | INTEG |  |  | endpoint_id=innov.events.detail catalog_page_id=innov.events 组合=DET-02 场景=异常-入参-缺eventId catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01110 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 关联分析 | 验证关联分析功能，检查关联分析按 sampleRequest 传 path eventId=EVT-001 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、eventId=EVT-001 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「关联分析」；4.填写 patheventId=EVT-001，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 relType（string，responseFields 关系类型）、relName（string，responseFields 对象）；3、sampleResponse 还含 relId（string）、relDesc（string）、score（number）；4、示例：org/ORG-SZ-01/鹏城实验室/主办机构/0.91；domain/D-AI/人工智能/所属领域/0.88 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events/{eventId}/relations |  | INTEG |  |  | endpoint_id=innov.events.relations catalog_page_id=innov.events 组合=REL-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01111 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 关联分析 | 验证关联分析功能，检查关联分析不传必填 eventId时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 eventId | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「关联分析」；4.不传 path eventId（请求 `/innov/v1/events//relations`，path 段为空），点击调用 | 1、返回面板 body 的 message 或 msg 指出 eventId 缺失或非法；2、不返回含 relType 与 relName 的成功关联数组 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/events/{eventId}/relations |  | INTEG |  |  | endpoint_id=innov.events.relations catalog_page_id=innov.events 组合=REL-02 场景=异常-入参-缺eventId catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01112 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 事件类型字典 | 验证事件类型字典功能，检查事件类型字典无参查询返回文档示例中的类型字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、无查询参数 | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉选择「事件类型字典」；4.保持请求参数为空，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 eventType（string，responseFields 类型编码）、nameZh（string，responseFields 中文名）；3、sampleResponse 还含 color（string）；4、示例：breakthrough/突破/#e76f51；cooperation/合作/#2a9d8f；policy/政策/#165DFF | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/dict/event-types |  | INTEG |  |  | endpoint_id=innov.events.types catalog_page_id=innov.events 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01113 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 接口信息 | 验证M1 科创事件地图的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 6；2、下拉名称与 §0 各 title 一致（事件列表、地图点位、热力聚合、事件详情、关联分析、事件类型字典）；3、默认项概览 method=GET、path=/innov/v1/events；4、切换后概览对应地图点位 GET /innov/v1/events，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=innov.events 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01114 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | M1 科创事件地图 | 算法测试 | 验证M1 科创事件地图的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「创新监测算法库」→「M1 科创事件地图」；2.切换至「算法测试」tab；3.接口下拉切换到「热力聚合」 | 1、算法测试 tab 下拉共 6 项，名称与接口信息 tab、catalog 一致；2、切换后调用区 method 为 GET、path 为 /innov/v1/events/heatmap；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对接口下拉共 6 项且名称与 §0 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=innov.events 场景=算法测试-清单 |

---


## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| LST-01 | innov.events.list | pageNum=1；pageSize=20；不传 startTime、endTime、eventTypes、importanceLevels、keyword | 主路径（sampleRequest） |
| LST-02 | innov.events.list | startTime=2024-01-01 00:00:00；pageNum=1；pageSize=20；不传 endTime、eventTypes、importanceLevels、keyword | 单独补传 startTime（sample 不传） |
| LST-03 | innov.events.list | endTime=2025-12-31 23:59:59；pageNum=1；pageSize=20；不传 startTime、eventTypes、importanceLevels、keyword | 单独补传 endTime（sample 不传） |
| LST-04 | innov.events.list | eventTypes=breakthrough；pageNum=1；pageSize=20；不传 startTime、endTime、importanceLevels、keyword | 单独补传 eventTypes（example 为空，值取 sampleResponse.eventType） |
| LST-05 | innov.events.list | importanceLevels=1；pageNum=1；pageSize=20；不传 startTime、endTime、eventTypes、keyword | 单独补传 importanceLevels（说明为 1/2/3，example 为空） |
| LST-06 | innov.events.list | keyword=大模型；pageNum=1；pageSize=20；不传 startTime、endTime、eventTypes、importanceLevels | 单独补传 keyword（example 为空，值取 sample 标题） |
| LST-07 | innov.events.list | 不传 pageNum；pageSize=20；不传 startTime、endTime、eventTypes、importanceLevels、keyword | 单独省略 pageNum（sample 传 pageNum=1） |
| LST-08 | innov.events.list | pageNum=1；不传 pageSize；不传 startTime、endTime、eventTypes、importanceLevels、keyword | 单独省略 pageSize（sample 传 pageSize=20） |
| LST-09 | innov.events.list | startTime=not-a-date；pageNum=1；pageSize=20；不传其余可选参数 | 只破坏 startTime |
| LST-10 | innov.events.list | endTime=not-a-date；pageNum=1；pageSize=20；不传其余可选参数 | 只破坏 endTime |
| LST-11 | innov.events.list | eventTypes=__invalid__；pageNum=1；pageSize=20；不传其余可选参数 | 只破坏 eventTypes |
| LST-12 | innov.events.list | importanceLevels=4；pageNum=1；pageSize=20；不传其余可选参数 | 只破坏 importanceLevels（超出 1/2/3） |
| LST-13 | innov.events.list | keyword=__invalid__；pageNum=1；pageSize=20；不传其余可选参数 | 只破坏 keyword |
| LST-14 | innov.events.list | pageNum=-1；pageSize=20；不传其余可选参数 | 只破坏 pageNum |
| LST-15 | innov.events.list | pageNum=1；pageSize=0；不传其余可选参数 | 只破坏 pageSize |
| GEO-01 | innov.events.geo | mode=geo | 主路径（sampleRequest） |
| GEO-02 | innov.events.geo | 不传 mode（请求 GET /innov/v1/events，无查询参数） | 缺必填 mode |
| HM-01 | innov.events.heatmap | 不传 startTime；不传 endTime | 主路径（sampleRequest 为 {}） |
| HM-02 | innov.events.heatmap | startTime=2024-01-01 00:00:00；不传 endTime | 单独补传 startTime（本接口 example 为空，值取同页列表 example） |
| HM-03 | innov.events.heatmap | endTime=2025-12-31 23:59:59；不传 startTime | 单独补传 endTime（本接口 example 为空，值取同页列表 example） |
| HM-04 | innov.events.heatmap | startTime=not-a-date；不传 endTime | 只破坏 startTime |
| HM-05 | innov.events.heatmap | endTime=not-a-date；不传 startTime | 只破坏 endTime |
| DET-01 | innov.events.detail | path eventId=EVT-001 | 主路径（sampleRequest） |
| DET-02 | innov.events.detail | 不传 path eventId（请求 `/innov/v1/events/`，path 段为空） | 缺必填 eventId |
| REL-01 | innov.events.relations | path eventId=EVT-001 | 主路径（sampleRequest） |
| REL-02 | innov.events.relations | 不传 path eventId（请求 `/innov/v1/events//relations`，path 段为空） | 缺必填 eventId |

事件类型字典无查询参数，不设组合 id。

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 事件列表 | innov.events.list | GET | /innov/v1/events | startTime?；endTime?；eventTypes?；importanceLevels?；keyword?；pageNum?；pageSize? | running |
| 地图点位 | innov.events.geo | GET | /innov/v1/events | mode* | running |
| 热力聚合 | innov.events.heatmap | GET | /innov/v1/events/heatmap | startTime?；endTime? | running |
| 事件详情 | innov.events.detail | GET | /innov/v1/events/{eventId} | eventId* | running |
| 关联分析 | innov.events.relations | GET | /innov/v1/events/{eventId}/relations | eventId* | running |
| 事件类型字典 | innov.events.types | GET | /innov/v1/dict/event-types | — | running |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.events.list | FUNC-01086～01100 |
| innov.events.geo | FUNC-01101、01102 |
| innov.events.heatmap | FUNC-01103～01107 |
| innov.events.detail | FUNC-01108、01109 |
| innov.events.relations | FUNC-01110、01111 |
| innov.events.types | FUNC-01112 |
| （页面清单） | FUNC-01113、01114 |


---

## 3. 覆盖自检（第三轮口径）

- [x] 6 个 title（事件列表、地图点位、热力聚合、事件详情、关联分析、事件类型字典）均在功能点列出现，且各有 1 条主流程
- [x] 主流程跟 sampleRequest：列表 pageNum=1、pageSize=20；点位 mode=geo；热力不传时间；详情与关联 eventId=EVT-001；字典无参
- [x] 可选参数与 sample 相反各 1 条，不交叉：列表补传 5 个 sample 未传参数、省略 pageNum 与 pageSize；热力分别补传 startTime、endTime
- [x] 反向：列表 7 个参数各 1 条非法；热力 startTime、endTime 各 1 条非法；必填 mode、详情 eventId、关联 eventId 各 1 条省略
- [x] 正向预期逐字段写出 sampleResponse（含 responseFields 未单列、但示例里出现的字段）；反向预期为 message 或 msg 指出该参数
- [x] 同 path 的列表与点位留在本页，备注写 endpoint_id
- [x] 无登录 / Token / 401 / 424 / 只写 HTTP 4xx 的预期
- [x] A 线无对应 Lxx；未改 work
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 待挂需规 / 待挂需规
- [x] 六接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（01113、01114）
- [x] `coverage-fp.md` 已同步 FUNC-01086～01114

**统计**：合计 **29** 条（主流程 6、备选 9、反向 12、清单 2）；编号闭区间 **FUNC-01086**～**FUNC-01114**（R3 · innov.events）。
