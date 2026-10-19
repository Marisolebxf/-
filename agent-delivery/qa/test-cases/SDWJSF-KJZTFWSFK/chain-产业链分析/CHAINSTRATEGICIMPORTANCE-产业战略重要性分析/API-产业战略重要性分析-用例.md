# 智能服务集群-科技专题服务算法库测试用例（产业战略重要性分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 产业战略重要性分析  
> **catalog**：`entry_id=chain.strategic-importance` · `catalog_page_id=chain.strategic-importance` · path `/chain/strategic-importance`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.strategic-importance`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip`：`chain.strategic-importance`，60 条无对应六级）。不改 `work/`。  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批8）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 战略重要性 | chain.strategic-importance.main |

本页只有 1 个 title。必填 path 参数 `chainId`，无其它参数。写 1 条主流程 + 1 条缺 `chainId`，不写备选，不按 field 拆条。

**chainId 取值**：params.example 与 sampleRequest 均为 `INB170101`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01312**～**API-01313**，连续用满）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.strategic-importance`、组合 id。作废旧号 API-000404～000408，不复用 API-00001～00888。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01312 | 产业链分析 | 产业战略重要性分析 | 主流程 | — | 产业战略重要性分析 | 战略重要性 | 战略重要性在 chainId=INB170101 时返回文档中的环节战略重要性字段 | 1、chainId 使用文档示例 INB170101 | 1.GET /innov/v1/industry/{chainId}/strategic-importance，path 取组合 STI-01 | 1、返回 body 为对象，与 sampleResponse 同层含 rows（array，responseFields 环节战略重要性）；2、rows 元素含 node_name（string）、position（string）、importance_score（number）；3、sampleResponse 示例三条：芯片设计 position=上游 importance_score=88.4；整机制造/中游/79.1；终端应用/下游/71.6 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/strategic-importance | M_CHAIN_STRATEGIC_IMPORTANCE | INTEG | | | endpoint_id=chain.strategic-importance.main catalog_page_id=chain.strategic-importance 组合=STI-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01313 | 产业链分析 | 产业战略重要性分析 | 异常-入参-缺chainId | — | 产业战略重要性分析 | 战略重要性 | 战略重要性不传 chainId | 1、path 不传 chainId | 1.GET /innov/v1/industry/{chainId}/strategic-importance，path 取组合 STI-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 rows 或 importance_score 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/strategic-importance | | INTEG | | | endpoint_id=chain.strategic-importance.main catalog_page_id=chain.strategic-importance 组合=STI-02 catalog_status=unavailable 文档标记未交付 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| STI-01 | chain.strategic-importance.main | path chainId=INB170101 | 主路径（sampleRequest / params.example） |
| STI-02 | chain.strategic-importance.main | 不传 path chainId（请求 `/innov/v1/industry//strategic-importance`，path 段为空） | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 战略重要性 | chain.strategic-importance.main | GET | /innov/v1/industry/{chainId}/strategic-importance | chainId* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.strategic-importance.main | API-01312、01313 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 1 个 title（战略重要性）在功能点列出现，且有 1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向 1 条；必填 chainId 1 条缺省反向；无其它参数，不写备选
- [x] unavailable 仍按 catalog sampleResponse（含嵌套 node_name、position、importance_score）与 responseFields（rows）写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] A 线无对应 Lxx，不按 field_key 拆用例；`coverage-fp.md` 已同步 API-01312～01313
- [x] 编号使用父控闭区间 API-01312～01313；本子任务不改 code-registry

**统计**：接口 **1**；用例 **2** 条（主流程 **1**、反向 **1**）；编号闭区间 **API-01312**～**API-01313**（父控 R2-批8 分配，连续用满）。
