# 智能服务集群-科技专题服务算法库测试用例（趋势预测 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 趋势预测  
> **catalog**：`entry_id=innov.forecast` · `catalog_page_id=innov.forecast` · path `/innov/forecast`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.forecast`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（创新监测不在本轮 60 六级）。不改 `work/`  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批20）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 领域趋势预测 | innov.forecast.domain |
| 2 | 创新点贡献度 | innov.forecast.contributions |
| 3 | 主题突变 | innov.forecast.bursts |

**参数口径**：领域趋势预测仅必填 path `domainId`；主流程对齐 `sampleRequest`（`domainId=D-AI`）；必填反向为省略该 path 段。创新点贡献度必填 `domainId`、可选 `pageNum`、`pageSize`；主流程对齐 `sampleRequest`（`domainId=D-AI`、`pageNum=1`、`pageSize=10`）；与 sample 相反为不传 `pageNum`、不传 `pageSize`；必填反向为省略 `domainId`；`pageNum`、`pageSize` 各 1 条非法。主题突变仅可选 `domainId`；主流程对齐 `sampleRequest`（`domainId=D-AI`）；与 sample 相反为不传 `domainId`；`domainId` 另 1 条非法。三接口 catalog `status=running`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01883**～**API-01893**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.forecast`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01883 | 创新监测 | 趋势预测 | 主流程 | — | 趋势预测 | 领域趋势预测 | 领域趋势预测按文档 sampleRequest path domainId=D-AI 查询 | 1、path domainId 使用文档示例 D-AI | 1.GET /innov/v1/forecast/domain/{domainId}，path 取组合 DOM-01 | 1、返回 body 的 data 含 forecastMode（string，示例 trend）、history（array，responseFields 历史年度）、predictions（array，responseFields 预测点）；2、history 元素含 statYear（number）、value（number）；3、sampleResponse 四行：statYear=2021、value=1200；statYear=2022、value=1480；statYear=2023、value=1760；statYear=2024、value=2010；4、predictions 元素含 predictPeriod（string）、predictValue（number）、ciLower（number）、ciUpper（number）；5、sampleResponse 两行：predictPeriod=2025、predictValue=2280、ciLower=2100、ciUpper=2460；predictPeriod=2026、predictValue=2510、ciLower=2280、ciUpper=2740 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/domain/{domainId} | M_INNOV_FORECAST_OUTPUT | INTEG | | | endpoint_id=innov.forecast.domain catalog_page_id=innov.forecast 组合=DOM-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01884 | 创新监测 | 趋势预测 | 异常-入参-缺domainId | — | 趋势预测 | 领域趋势预测 | 领域趋势预测省略必填 path 段 domainId | 1、无其它业务前置 | 1.GET /innov/v1/forecast/domain，省略 path 段，组合 DOM-02 | 1、返回 body 的 message 或 msg 指出 domainId 缺失；2、不返回含 history、predictions 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/domain/{domainId} | | INTEG | | | endpoint_id=innov.forecast.domain catalog_page_id=innov.forecast 组合=DOM-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01885 | 创新监测 | 趋势预测 | 主流程 | — | 趋势预测 | 创新点贡献度 | 创新点贡献度按文档 sampleRequest domainId=D-AI、pageNum=1、pageSize=10 查询 | 1、domainId 使用文档示例 D-AI；pageNum=1；pageSize=10 | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CON-01 | 1、返回 body 的 data 含 total（number，示例 2）、list（array，responseFields 贡献度排行）；2、list 元素含 targetId（string）、title（string）、eventType（string）、contribution（number）、predictValue（number）；3、sampleResponse 两行：targetId=EVT-001、title=深圳大模型开源发布会、eventType=breakthrough、contribution=0.186、predictValue=420；targetId=EVT-002、title=北京量子计算联合实验室揭牌、eventType=cooperation、contribution=0.124、predictValue=280 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01886 | 创新监测 | 趋势预测 | 备选-参数组合 | 省略 pageNum | 趋势预测 | 创新点贡献度 | 创新点贡献度不传可选 pageNum（与 sampleRequest 相反） | 1、domainId=D-AI；pageSize=10 | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CON-02 | 1、返回 body 的 data 仍含 total（number）、list（array）；2、list 元素仍含 targetId、title、eventType、contribution、predictValue；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01887 | 创新监测 | 趋势预测 | 备选-参数组合 | 省略 pageSize | 趋势预测 | 创新点贡献度 | 创新点贡献度不传可选 pageSize（与 sampleRequest 相反） | 1、domainId=D-AI；pageNum=1 | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CON-03 | 1、返回 body 的 data 仍含 total（number）、list（array）；2、list 元素仍含 targetId、title、eventType、contribution、predictValue；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01888 | 创新监测 | 趋势预测 | 异常-入参-缺domainId | — | 趋势预测 | 创新点贡献度 | 创新点贡献度不传必填 domainId | 1、pageNum=1；pageSize=10 保持合法 | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CON-04 | 1、返回 body 的 message 或 msg 指出 domainId 缺失；2、不返回含 list 贡献度排行的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01889 | 创新监测 | 趋势预测 | 异常-入参-非法pageNum | — | 趋势预测 | 创新点贡献度 | 创新点贡献度 pageNum 非法 | 1、domainId=D-AI；pageSize=10 | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CON-05 | 1、返回 body 的 message 或 msg 指出 pageNum 非法；2、不返回含 list 贡献度排行的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01890 | 创新监测 | 趋势预测 | 异常-入参-非法pageSize | — | 趋势预测 | 创新点贡献度 | 创新点贡献度 pageSize 非法 | 1、domainId=D-AI；pageNum=1 | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CON-06 | 1、返回 body 的 message 或 msg 指出 pageSize 非法；2、不返回含 list 贡献度排行的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CON-06 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01891 | 创新监测 | 趋势预测 | 主流程 | — | 趋势预测 | 主题突变 | 主题突变按文档 sampleRequest domainId=D-AI 查询 | 1、domainId 使用文档示例 D-AI | 1.GET /innov/v1/forecast/bursts，查询参数取组合 BUR-01 | 1、返回 body 的 data 为数组；2、元素含 topicName（string，responseFields 主题）、burstScore（number，responseFields 强度）；3、sampleResponse 还含 domainId（string）、burstStart（string）；4、示例两行：topicName=多模态大模型、domainId=D-AI、burstStart=2023-06、burstScore=18.4；topicName=端侧推理芯片、domainId=D-AI、burstStart=2024-02、burstScore=14.1 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/bursts | | INTEG | | | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BUR-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01892 | 创新监测 | 趋势预测 | 备选-参数组合 | 省略 domainId | 趋势预测 | 主题突变 | 主题突变不传可选 domainId（与 sampleRequest 相反） | 1、无查询参数 | 1.GET /innov/v1/forecast/bursts，查询参数取组合 BUR-02 | 1、返回 body 的 data 仍为数组；2、元素仍含 topicName（string）、burstScore（number）、domainId（string）、burstStart（string）；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/bursts | | INTEG | | | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BUR-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01893 | 创新监测 | 趋势预测 | 异常-入参-非法domainId | — | 趋势预测 | 主题突变 | 主题突变 domainId 非法 | 1、无其它合法查询参数 | 1.GET /innov/v1/forecast/bursts，查询参数取组合 BUR-03 | 1、返回 body 的 message 或 msg 指出 domainId 非法；2、不返回含 topicName、burstScore 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/forecast/bursts | | INTEG | | | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BUR-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| DOM-01 | innov.forecast.domain | path domainId=D-AI | 主路径（sampleRequest） |
| DOM-02 | innov.forecast.domain | 省略 path 段 domainId | 缺必填 domainId |
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
| innov.forecast.domain | API-01883、01884 |
| innov.forecast.contributions | API-01885、01886、01887、01888、01889、01890 |
| innov.forecast.bursts | API-01891、01892、01893 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 3 个 title 均在功能点列出现，且各有 1 条主流程（01883 领域趋势预测、01885 创新点贡献度、01891 主题突变）
- [x] 领域趋势预测 1 主流程 + 省略 domainId 1 条；创新点贡献度 1 主流程 + 省略 pageNum、省略 pageSize 各 1 条 + 省略 domainId、非法 pageNum、非法 pageSize 各 1 条；主题突变 1 主流程 + 省略 domainId 1 条 + 非法 domainId 1 条
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数缺失或非法
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01883～01893；A 线写无对应 Lxx
- [ ] `code-registry.yaml` 由父控回写（本子任务未改 registry）

**统计**：用例 **11** 条；主流程 **3**、备选 **3**、反向 **5**；编号闭区间 **API-01883**～**API-01893**（父控 R2-批20 分配）。
