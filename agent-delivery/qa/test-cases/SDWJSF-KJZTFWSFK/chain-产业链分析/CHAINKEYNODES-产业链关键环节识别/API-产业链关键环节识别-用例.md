# 智能服务集群-科技专题服务算法库测试用例（产业链关键环节识别 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 产业链关键环节识别  
> **catalog**：`entry_id=chain.keynodes` · `catalog_page_id=chain.keynodes` · path `/chain/keynodes`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.keynodes`  
> **A 线对照**：`fp-split-by-api-run/work/L21.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批6）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 关键环节 | chain.keynodes.main |
| 2 | 产业链关键环节识别模型 | chain.keynodes.m_chain_deep_124_1 |

两个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId`，不写备选，不按 field 拆条。

**chainId 取值**：`关键环节` 的 params.example 与 sampleRequest 均为 `INB170101`。`产业链关键环节识别模型` 的 sampleRequest 为 `chain_id=INB1701`，params.example 为 `INB170101`，键名与取值不一致，主路径以 sampleRequest 为准（见附录 A）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01266**～**API-01269**，连续用满）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.keynodes`、组合 id。作废旧号 API-00350～00359，不复用 API-00001～00888。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01266 | 产业链分析 | 产业链关键环节识别 | 主流程 | — | 产业链关键环节识别 | 关键环节 | 关键环节在 chainId=INB170101 时返回文档中的关键环节字段 | 1、chainId 使用文档示例 INB170101 | 1.GET /innov/v1/industry/{chainId}/key-nodes，path 取组合 KND-01 | 1、返回 body 与 sampleResponse 同形为数组（若有信封则 data 为该数组）；2、元素逐字段含 node_name（string）、position（string）、high_end_index（number，responseFields 高端化指数）、value_added_score（number）、tech_barrier_score（number）、market_concentration_score（number）、is_key_node（boolean）；3、sampleResponse 示例三条为 芯片设计/上游/86.2/81/88/72/true、整机制造/中游/74.5/68/61/54/true、渠道运营/下游/58.1/49/36/41/false；4、元素内无更深嵌套对象 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/key-nodes | | INTEG | | | endpoint_id=chain.keynodes.main catalog_page_id=chain.keynodes 组合=KND-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01267 | 产业链分析 | 产业链关键环节识别 | 异常-入参-缺chainId | — | 产业链关键环节识别 | 关键环节 | 关键环节不传 chainId | 1、path 不传 chainId | 1.GET /innov/v1/industry/{chainId}/key-nodes，path 取组合 KND-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 high_end_index 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/key-nodes | | INTEG | | | endpoint_id=chain.keynodes.main catalog_page_id=chain.keynodes 组合=KND-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01268 | 产业链分析 | 产业链关键环节识别 | 主流程 | — | 产业链关键环节识别 | 产业链关键环节识别模型 | 产业链关键环节识别模型按文档 sampleRequest 的 chain_id 计算并返回 metric_id 与 hint | 1、请求体使用文档 sampleRequest 的 chain_id=INB1701 | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_124_1/compute，请求体取组合 KNM-01 | 1、返回 body 为对象，含 metric_id（string，responseFields 指标 ID，sampleResponse 示例 M_CHAIN_DEEP_124_1）、hint（string，sampleResponse 示例 真实 compute 响应,以实际调用为准）；2、sampleResponse 无嵌套对象 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_124_1/compute | M_CHAIN_DEEP_124_1 | INTEG | | | endpoint_id=chain.keynodes.m_chain_deep_124_1 catalog_page_id=chain.keynodes 组合=KNM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01269 | 产业链分析 | 产业链关键环节识别 | 异常-入参-缺chainId | — | 产业链关键环节识别 | 产业链关键环节识别模型 | 产业链关键环节识别模型不传 chainId | 1、请求体不传 chainId | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_124_1/compute，请求体取组合 KNM-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_124_1 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_124_1/compute | | INTEG | | | endpoint_id=chain.keynodes.m_chain_deep_124_1 catalog_page_id=chain.keynodes 组合=KNM-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| KND-01 | chain.keynodes.main | path chainId=INB170101 | 主路径（sampleRequest / params.example） |
| KND-02 | chain.keynodes.main | 不传 path chainId（请求 `/innov/v1/industry//key-nodes`，path 段为空） | 缺必填 chainId |
| KNM-01 | chain.keynodes.m_chain_deep_124_1 | 请求体按 sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101，键名与取值均与 sampleRequest 不一致，本组合以 sampleRequest 为准） | 主路径（sampleRequest） |
| KNM-02 | chain.keynodes.m_chain_deep_124_1 | 不传 chainId，请求体也不含 chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 关键环节 | chain.keynodes.main | GET | /innov/v1/industry/{chainId}/key-nodes | chainId* | unavailable |
| 产业链关键环节识别模型 | chain.keynodes.m_chain_deep_124_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_124_1/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.keynodes.main | API-01266、01267 |
| chain.keynodes.m_chain_deep_124_1 | API-01268、01269 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title（关键环节、产业链关键环节识别模型）均在功能点列出现，且各有 1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条缺省反向；无其它参数，不写备选
- [x] unavailable（关键环节）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] 不按 L21 field_key 拆用例；`coverage-fp.md` 已同步 API-01266～01269
- [x] 编号使用父控闭区间 API-01266～01269；本子任务不改 code-registry

**统计**：接口 **2**；用例 **4** 条（主流程 **2**、反向 **2**）；编号闭区间 **API-01266**～**API-01269**（父控 R2-批6 分配，连续用满）。
