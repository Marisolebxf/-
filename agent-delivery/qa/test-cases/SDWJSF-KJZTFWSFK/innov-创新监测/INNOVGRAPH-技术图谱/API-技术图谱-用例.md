# 智能服务集群-科技专题服务算法库测试用例（技术图谱 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 技术图谱  
> **catalog**：`entry_id=innov.graph` · `catalog_page_id=innov.graph` · path `/innov/graph`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.graph`  
> **A 线对照**：无对应 Lxx。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（创新监测不在本轮 60 六级）。不改 `work/`  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批19）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 领域树 | innov.graph.domains |
| 2 | 领域子图 | innov.graph.subgraph |
| 3 | 影响分排行 | innov.graph.rank |

**参数口径**：领域树无参，仅 1 条主流程。领域子图必填 `domainId`、可选 `limit`；主流程对齐 `sampleRequest`（`domainId=D-AI`、`limit=60`）；与 sample 相反为不传 `limit`；必填反向为省略 `domainId`；`limit` 另 1 条非法。影响分排行四个参数均可选；主流程对齐 `sampleRequest`（`domainId=D-AI`、`pageNum=1`、`pageSize=20`，不传 `nodeType`）；与 sample 相反为不传 `domainId`、传 `nodeType=org`、不传 `pageNum`、不传 `pageSize`；每个参数另 1 条非法。三接口 catalog `status=running`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01853**～**API-01866**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.graph`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01853 | 创新监测 | 技术图谱 | 主流程 | — | 技术图谱 | 领域树 | 领域树无参查询返回文档示例中的领域列表字段 | 1、无业务前置 | 1.GET /innov/v1/graph/domains（无查询参数） | 1、返回 body 的 data 为数组；2、元素含 domainId（string，responseFields 领域 ID）、name（string，responseFields 领域名）；3、sampleResponse 还含 parentId（string）、level（number）、domainSource（string）；4、示例两行：domainId=D-AI、name=人工智能、parentId 空串、level=1、domainSource=seed；domainId=D-BIO、name=生物医药、parentId 空串、level=1、domainSource=seed | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/domains | | INTEG | | | endpoint_id=innov.graph.domains catalog_page_id=innov.graph 组合=— 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01854 | 创新监测 | 技术图谱 | 主流程 | — | 技术图谱 | 领域子图 | 领域子图按文档 sampleRequest domainId=D-AI、limit=60 查询 | 1、domainId 使用文档示例 D-AI；limit=60 | 1.GET /innov/v1/graph/subgraph，查询参数取组合 SUB-01 | 1、返回 body 的 data 含 period（string，示例 2025Q1）、nodes（array，responseFields 节点）、edges（array，responseFields 边 src/dst）；2、nodes 元素含 nodeId（string）、nodeType（string）、name（string）、influenceScore（number）、rank（number）；3、示例两节点：nodeId=ORG-01、nodeType=org、name=鹏城实验室、influenceScore=88.2、rank=1；nodeId=SCH-01、nodeType=scholar、name=李研、influenceScore=76.4、rank=2；4、edges 元素含 src（string）、dst（string）、edgeType（string）、weight（number）；5、示例边 src=ORG-01、dst=SCH-01、edgeType=employ、weight=0.8 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/subgraph | | INTEG | | | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=SUB-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01855 | 创新监测 | 技术图谱 | 备选-参数组合 | 省略 limit | 技术图谱 | 领域子图 | 领域子图仅传 domainId、不传可选 limit（与 sampleRequest 相反） | 1、domainId=D-AI | 1.GET /innov/v1/graph/subgraph，查询参数取组合 SUB-02 | 1、返回 body 的 data 仍含 period（string）、nodes（array）、edges（array）；2、nodes 元素仍含 nodeId、nodeType、name、influenceScore、rank；3、edges 元素仍含 src、dst、edgeType、weight；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/subgraph | | INTEG | | | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=SUB-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01856 | 创新监测 | 技术图谱 | 异常-入参-缺domainId | — | 技术图谱 | 领域子图 | 领域子图不传必填 domainId | 1、limit=60 保持合法 | 1.GET /innov/v1/graph/subgraph，查询参数取组合 SUB-03 | 1、返回 body 的 message 或 msg 指出 domainId 缺失；2、不返回含 nodes、edges 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/subgraph | | INTEG | | | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=SUB-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01857 | 创新监测 | 技术图谱 | 异常-入参-非法limit | — | 技术图谱 | 领域子图 | 领域子图 limit 非法 | 1、domainId=D-AI | 1.GET /innov/v1/graph/subgraph，查询参数取组合 SUB-04 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 nodes、edges 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/subgraph | | INTEG | | | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=SUB-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01858 | 创新监测 | 技术图谱 | 主流程 | — | 技术图谱 | 影响分排行 | 影响分排行按文档 sampleRequest domainId=D-AI、pageNum=1、pageSize=20 查询 | 1、domainId 使用文档示例 D-AI；pageNum=1；pageSize=20；不传 nodeType | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 RNK-01 | 1、返回 body 的 data 含 total（number，示例 2）、period（string，示例 2025Q1）、list（array，responseFields 排行）；2、list 元素含 nodeId（string）、nodeType（string）、name（string）、influenceScore（number）、rankInDomain（number）；3、示例两行：nodeId=ORG-01、nodeType=org、name=鹏城实验室、influenceScore=88.2、rankInDomain=1；nodeId=SCH-01、nodeType=scholar、name=李研、influenceScore=76.4、rankInDomain=2 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01859 | 创新监测 | 技术图谱 | 备选-参数组合 | 省略 domainId | 技术图谱 | 影响分排行 | 影响分排行不传可选 domainId（与 sampleRequest 相反） | 1、pageNum=1；pageSize=20；不传 nodeType | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 RNK-02 | 1、返回 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 nodeId、nodeType、name、influenceScore、rankInDomain；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01860 | 创新监测 | 技术图谱 | 备选-参数组合 | 传 nodeType | 技术图谱 | 影响分排行 | 影响分排行传可选 nodeType=org（sampleRequest 未传该参数） | 1、domainId=D-AI；nodeType=org；pageNum=1；pageSize=20 | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 RNK-03 | 1、返回 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 nodeId、nodeType、name、influenceScore、rankInDomain；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01861 | 创新监测 | 技术图谱 | 备选-参数组合 | 省略 pageNum | 技术图谱 | 影响分排行 | 影响分排行不传可选 pageNum（与 sampleRequest 相反） | 1、domainId=D-AI；pageSize=20；不传 nodeType | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 RNK-04 | 1、返回 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 nodeId、nodeType、name、influenceScore、rankInDomain；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01862 | 创新监测 | 技术图谱 | 备选-参数组合 | 省略 pageSize | 技术图谱 | 影响分排行 | 影响分排行不传可选 pageSize（与 sampleRequest 相反） | 1、domainId=D-AI；pageNum=1；不传 nodeType | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 RNK-05 | 1、返回 body 的 data 仍含 total（number）、period（string）、list（array）；2、list 元素仍含 nodeId、nodeType、name、influenceScore、rankInDomain；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | M_INNOV_NODE_INFLUENCE | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01863 | 创新监测 | 技术图谱 | 异常-入参-非法domainId | — | 技术图谱 | 影响分排行 | 影响分排行 domainId 非法 | 1、pageNum=1；pageSize=20 保持合法 | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 RNK-06 | 1、返回 body 的 message 或 msg 指出 domainId 非法；2、不返回含 list 排行的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-06 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01864 | 创新监测 | 技术图谱 | 异常-入参-非法nodeType | — | 技术图谱 | 影响分排行 | 影响分排行 nodeType 非法 | 1、domainId=D-AI；pageNum=1；pageSize=20 | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 RNK-07 | 1、返回 body 的 message 或 msg 指出 nodeType 非法；2、不返回含 list 排行的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-07 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01865 | 创新监测 | 技术图谱 | 异常-入参-非法pageNum | — | 技术图谱 | 影响分排行 | 影响分排行 pageNum 非法 | 1、domainId=D-AI；pageSize=20 | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 RNK-08 | 1、返回 body 的 message 或 msg 指出 pageNum 非法；2、不返回含 list 排行的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-08 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01866 | 创新监测 | 技术图谱 | 异常-入参-非法pageSize | — | 技术图谱 | 影响分排行 | 影响分排行 pageSize 非法 | 1、domainId=D-AI；pageNum=1 | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 RNK-09 | 1、返回 body 的 message 或 msg 指出 pageSize 非法；2、不返回含 list 排行的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=RNK-09 |

---

## 附录 A · 入参组合

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
| innov.graph.domains | API-01853 |
| innov.graph.subgraph | API-01854、01855、01856、01857 |
| innov.graph.rank | API-01858、01859、01860、01861、01862、01863、01864、01865、01866 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 3 个 title 均在功能点列出现，且各有 1 条主流程（01853 领域树、01854 领域子图、01858 影响分排行）
- [x] 无参领域树仅 1 条主流程；领域子图 1 主流程 + 省略 limit 1 条 + 省略 domainId 1 条 + 非法 limit 1 条；影响分排行 1 主流程 + 4 条与 sample 相反的可选参数 + 4 条非法反向
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数缺失或非法
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01853～01866；A 线写无对应 Lxx
- [ ] `code-registry.yaml` 由父控回写（本子任务未改 registry）

**统计**：用例 **14** 条；主流程 **3**、备选 **5**、反向 **6**；编号闭区间 **API-01853**～**API-01866**（父控 R2-批19 分配）。
