# 智能服务集群-科技专题服务算法库测试用例（技术成熟度分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 技术成熟度分析  
> **catalog**：`entry_id=chain.tech-maturity` · `catalog_page_id=chain.tech-maturity` · path `/chain/tech-maturity`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.tech-maturity`  
> **A 线对照**：无对应 Lxx（`_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `chain.tech-maturity`，原因：60 条无对应六级；覆盖矩阵见 `coverage-fp.md`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批8）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 技术成熟度 | chain.tech-maturity.main |
| 2 | 技术成熟度评分 | chain.tech-maturity.m_chain_tech_maturity_score |

两个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId`，不写备选，不按 field 拆条。

**chainId 取值**：`技术成熟度` 的 params.example 与 sampleRequest 均为 `INB170101`。`技术成熟度评分` 的 sampleRequest 为 `chain_id=INB1701`，params.example 为 `INB170101`，键名与取值不一致，主路径以 sampleRequest 为准（见附录 A）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01308**～**API-01311**，连续用满）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.tech-maturity`、组合 id。作废旧号 API-00399～00403，不复用 API-00001～00888。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01308 | 产业链分析 | 技术成熟度分析 | 主流程 | — | 技术成熟度分析 | 技术成熟度 | 技术成熟度在 chainId=INB170101 时返回文档中的成熟度评分、阶段与年度专利趋势 | 1、chainId 使用文档示例 INB170101 | 1.GET /innov/v1/industry/{chainId}/tech-maturity，path 取组合 TMA-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：tech_maturity_score（number，responseFields 技术成熟度评分，示例 70）、stage（string，sampleResponse 多出字段，示例 趋于成熟）；2、trend 为数组（responseFields 年度公开专利量），元素含 year（number）、patent_count（number）；示例第 1 条 year=2023、patent_count=86；示例第 2 条 year=2024、patent_count=102；示例第 3 条 year=2025、patent_count=118 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/tech-maturity | M_CHAIN_TECH_MATURITY_SCORE | INTEG | | | endpoint_id=chain.tech-maturity.main catalog_page_id=chain.tech-maturity 组合=TMA-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01309 | 产业链分析 | 技术成熟度分析 | 异常-入参-缺chainId | — | 技术成熟度分析 | 技术成熟度 | 技术成熟度不传 chainId | 1、path 不传 chainId | 1.GET /innov/v1/industry/{chainId}/tech-maturity，path 取组合 TMA-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 tech_maturity_score 或 trend 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/tech-maturity | | INTEG | | | endpoint_id=chain.tech-maturity.main catalog_page_id=chain.tech-maturity 组合=TMA-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01310 | 产业链分析 | 技术成熟度分析 | 主流程 | — | 技术成熟度分析 | 技术成熟度评分 | 技术成熟度评分按文档 sampleRequest 的 chain_id 计算并返回 metric_id 与 hint | 1、请求体使用文档 sampleRequest 的 chain_id=INB1701 | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute，请求体取组合 TMS-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_CHAIN_TECH_MATURITY_SCORE）、hint（string，sampleResponse 多出字段，示例 真实 compute 响应,以实际调用为准） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute | M_CHAIN_TECH_MATURITY_SCORE | INTEG | | | endpoint_id=chain.tech-maturity.m_chain_tech_maturity_score catalog_page_id=chain.tech-maturity 组合=TMS-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01311 | 产业链分析 | 技术成熟度分析 | 异常-入参-缺chainId | — | 技术成熟度分析 | 技术成熟度评分 | 技术成熟度评分不传 chainId | 1、请求体不传 chainId | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute，请求体取组合 TMS-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_TECH_MATURITY_SCORE 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute | | INTEG | | | endpoint_id=chain.tech-maturity.m_chain_tech_maturity_score catalog_page_id=chain.tech-maturity 组合=TMS-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TMA-01 | chain.tech-maturity.main | path chainId=INB170101 | 主路径（sampleRequest / params.example） |
| TMA-02 | chain.tech-maturity.main | 不传 path chainId（请求 `/innov/v1/industry//tech-maturity`，path 段为空） | 缺必填 chainId |
| TMS-01 | chain.tech-maturity.m_chain_tech_maturity_score | 请求体按 sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101，键名与取值均与 sampleRequest 不一致，本组合以 sampleRequest 为准） | 主路径（sampleRequest） |
| TMS-02 | chain.tech-maturity.m_chain_tech_maturity_score | 不传 chainId，请求体也不含 chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 技术成熟度 | chain.tech-maturity.main | GET | /innov/v1/industry/{chainId}/tech-maturity | chainId* | unavailable |
| 技术成熟度评分 | chain.tech-maturity.m_chain_tech_maturity_score | POST | /innov/v1/industry/chainan/metric/M_CHAIN_TECH_MATURITY_SCORE/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.tech-maturity.main | API-01308、01309 |
| chain.tech-maturity.m_chain_tech_maturity_score | API-01310、01311 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title（技术成熟度、技术成熟度评分）均在功能点列出现，且各有 1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条缺省反向；无其它参数，不写备选
- [x] unavailable（技术成熟度）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] 不按 field_key 拆用例；`coverage-fp.md` 已同步 API-01308～01311
- [x] 编号使用父控闭区间 API-01308～01311；本子任务不改 code-registry

**统计**：接口 **2**；用例 **4** 条（主流程 **2**、反向 **2**）；编号闭区间 **API-01308**～**API-01311**（父控 R2-批8 分配，连续用满）。
