# 智能服务集群-科技专题服务算法库测试用例（重点布局产业推荐 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 重点布局产业推荐  
> **catalog**：`entry_id=chain.layout` · `catalog_page_id=chain.layout` · path `/chain/layout`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.layout`  
> **A 线对照**：`fp-split-by-api-run/work/L26.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（本册不登录、不试调）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批8）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 重点布局产业推荐 | chain.hotspot.recommendation |
| 2 | 重点布局产业推荐模型 | chain.layout.m_chain_deep_129_1 |

两个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId`，不写备选，不按 field 拆条。

**chainId 取值**：`重点布局产业推荐` 的 params.example 与 sampleRequest 均为 `INB170101`（描述另写 INB1701 无推荐，本册不单开空态用例）。`重点布局产业推荐模型` 的 sampleRequest 为 `{}`，无 `chain_id` 键；主路径取 params.example `INB170101`，请求体键名用 params.name `chainId`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01304**～**API-01307**，连续用满）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.layout`、组合 id。作废旧号不复用 API-00001～00888。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01304 | 产业链分析 | 重点布局产业推荐 | 主流程 | — | 重点布局产业推荐 | 重点布局产业推荐 | 重点布局产业推荐在 chainId=INB170101 时返回文档中的推荐级别、推荐指数与维度得分 | 1、chainId 使用文档示例 INB170101 | 1.GET /innov/v1/industry/{chainId}/recommendation，path 取组合 LAY-01 | 1、返回 body 为对象，无嵌套数组；与 sampleResponse 同层逐字段一致：recommend_level（string，responseFields 推荐级别，示例 优先布局）、recommend_index（number，responseFields 推荐指数，示例 84.2）、advantage_score（number，sampleResponse 多出字段，示例 78）、opportunity_score（number，sampleResponse 多出字段，示例 81）、policy_match_score（number，sampleResponse 多出字段，示例 88）、rank_overall（number，sampleResponse 多出字段，示例 2） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/recommendation | M_CHAIN_LAYOUT_PRIORITY_SCORE | INTEG | | | endpoint_id=chain.hotspot.recommendation catalog_page_id=chain.layout 组合=LAY-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01305 | 产业链分析 | 重点布局产业推荐 | 异常-入参-缺chainId | — | 重点布局产业推荐 | 重点布局产业推荐 | 重点布局产业推荐不传 chainId | 1、path 不传 chainId | 1.GET /innov/v1/industry/{chainId}/recommendation，path 取组合 LAY-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 recommend_level 或 recommend_index 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/recommendation | | INTEG | | | endpoint_id=chain.hotspot.recommendation catalog_page_id=chain.layout 组合=LAY-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01306 | 产业链分析 | 重点布局产业推荐 | 主流程 | — | 重点布局产业推荐 | 重点布局产业推荐模型 | 重点布局产业推荐模型在 chainId=INB170101 时返回 metric_id、hint 及推荐级别、推荐指数 | 1、chainId 使用 params.example INB170101（sampleRequest 为空） | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute，请求体取组合 LYM-01 | 1、返回 body 为对象，无嵌套数组；与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_CHAIN_DEEP_129_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 同层另列 recommend_level（string，推荐级别）、recommend_index（number，推荐指数），sampleResponse 未给这两字段的示例值 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute | M_CHAIN_DEEP_129_1 | INTEG | | | endpoint_id=chain.layout.m_chain_deep_129_1 catalog_page_id=chain.layout 组合=LYM-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01307 | 产业链分析 | 重点布局产业推荐 | 异常-入参-缺chainId | — | 重点布局产业推荐 | 重点布局产业推荐模型 | 重点布局产业推荐模型不传 chainId | 1、请求体不传 chainId | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute，请求体取组合 LYM-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_129_1 或 recommend_level 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute | | INTEG | | | endpoint_id=chain.layout.m_chain_deep_129_1 catalog_page_id=chain.layout 组合=LYM-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| LAY-01 | chain.hotspot.recommendation | path chainId=INB170101 | 主路径（sampleRequest 与 params.example 一致） |
| LAY-02 | chain.hotspot.recommendation | 不传 path chainId（请求 `/innov/v1/industry//recommendation`，path 段为空） | 缺必填 chainId |
| LYM-01 | chain.layout.m_chain_deep_129_1 | 请求体 chainId=INB170101（sampleRequest 为 {}，无 chain_id；params.name=chainId，example=INB170101） | 主路径（params.example） |
| LYM-02 | chain.layout.m_chain_deep_129_1 | 不传 chainId，请求体也不含 chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 重点布局产业推荐 | chain.hotspot.recommendation | GET | /innov/v1/industry/{chainId}/recommendation | chainId* | unavailable |
| 重点布局产业推荐模型 | chain.layout.m_chain_deep_129_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.hotspot.recommendation | API-01304、01305 |
| chain.layout.m_chain_deep_129_1 | API-01306、01307 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title（重点布局产业推荐、重点布局产业推荐模型）均在功能点列出现，且各有 1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条缺省反向；无其它参数，不写备选
- [x] unavailable（重点布局产业推荐）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] 不按 L26 field_key 拆用例；`coverage-fp.md` 已同步 API-01304～01307
- [x] 编号使用父控闭区间 API-01304～01307；本子任务不改 code-registry

**统计**：接口 **2**；用例 **4** 条（主流程 **2**、反向 **2**）；编号闭区间 **API-01304**～**API-01307**（父控 R2-批8 分配，连续用满）。
