# 智能服务集群-科技专题服务算法库测试用例（产业周期分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 产业周期分析  
> **catalog**：`entry_id=chain.cycle` · `catalog_page_id=chain.cycle` · path `/chain/cycle`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.cycle`  
> **A 线对照**：`fp-split-by-api-run/work/L19.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批5）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 产业周期分析 | chain.cycle.main |
| 2 | 产业周期分析模型 | chain.cycle.m_chain_deep_122_1 |

两个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId`，不写备选，不按 field 拆条。

**chainId 取值**：`产业周期分析` 的 params.example 与 sampleRequest 均为 `INB1701`。`产业周期分析模型` 的 sampleRequest 为 `chain_id=INB1701`，params.example 为 `INB170101`，键名与取值不一致，主路径以 sampleRequest 为准（见附录 A）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01258**～**API-01261**，连续用满）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.cycle`、组合 id。作废旧号 API-00055～00058，不复用 API-00001～00888。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01258 | 产业链分析 | 产业周期分析 | 主流程 | — | 产业周期分析 | 产业周期分析 | 产业周期分析在 chainId=INB1701 时返回文档中的周期与阶段字段 | 1、chainId 使用文档示例 INB1701 | 1.GET /innov/v1/industry/{chainId}/cycle，path 取组合 CYC-01 | 1、返回 body 为对象，与 sampleResponse 同层含 cycle（object）、stage（object）；2、cycle.cycle_stage（string，responseFields 周期阶段，示例 成长期）、cycle.growth_rate（number，示例 14.9）、cycle.investment_trend（string，示例 up）、cycle.enterprise_trend（string，示例 up）、cycle.trend（array）；3、trend 元素含 year（number）、revenue（number）、growth_rate（number），示例三条为 2023/12800/8.2、2024/14640/14.4、2025/16820/14.9；4、stage.cycle_stage（string，示例 成长期）、stage.sub_stage（string，responseFields 细分阶段，示例 加速扩张）、stage.high_tech_ratio（number，示例 46.2）、stage.investment_intensity（number，示例 7.8）、stage.growth_rate（number，示例 14.9） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/cycle | M_CHAIN_CYCLE_STAGE | INTEG | | | endpoint_id=chain.cycle.main catalog_page_id=chain.cycle 组合=CYC-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01259 | 产业链分析 | 产业周期分析 | 异常-入参-缺chainId | — | 产业周期分析 | 产业周期分析 | 产业周期分析不传 chainId | 1、path 不传 chainId | 1.GET /innov/v1/industry/{chainId}/cycle，path 取组合 CYC-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 cycle.cycle_stage 或 stage.sub_stage 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/cycle | | INTEG | | | endpoint_id=chain.cycle.main catalog_page_id=chain.cycle 组合=CYC-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01260 | 产业链分析 | 产业周期分析 | 主流程 | — | 产业周期分析 | 产业周期分析模型 | 产业周期分析模型按文档 sampleRequest 的 chain_id 计算并返回 metric_id 与 hint | 1、请求体使用文档 sampleRequest 的 chain_id=INB1701 | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_122_1/compute，请求体取组合 CYM-01 | 1、返回 body 为对象，含 metric_id（string，responseFields 指标 ID，sampleResponse 示例 M_CHAIN_DEEP_122_1）、hint（string，sampleResponse 示例 真实 compute 响应,以实际调用为准） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_122_1/compute | M_CHAIN_DEEP_122_1 | INTEG | | | endpoint_id=chain.cycle.m_chain_deep_122_1 catalog_page_id=chain.cycle 组合=CYM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01261 | 产业链分析 | 产业周期分析 | 异常-入参-缺chainId | — | 产业周期分析 | 产业周期分析模型 | 产业周期分析模型不传 chainId | 1、请求体不传 chainId | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_122_1/compute，请求体取组合 CYM-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_122_1 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_122_1/compute | | INTEG | | | endpoint_id=chain.cycle.m_chain_deep_122_1 catalog_page_id=chain.cycle 组合=CYM-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| CYC-01 | chain.cycle.main | path chainId=INB1701 | 主路径（sampleRequest / params.example） |
| CYC-02 | chain.cycle.main | 不传 path chainId（请求 `/innov/v1/industry//cycle`，path 段为空） | 缺必填 chainId |
| CYM-01 | chain.cycle.m_chain_deep_122_1 | 请求体按 sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101，键名与取值均与 sampleRequest 不一致，本组合以 sampleRequest 为准） | 主路径（sampleRequest） |
| CYM-02 | chain.cycle.m_chain_deep_122_1 | 不传 chainId，请求体也不含 chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 产业周期分析 | chain.cycle.main | GET | /innov/v1/industry/{chainId}/cycle | chainId* | unavailable |
| 产业周期分析模型 | chain.cycle.m_chain_deep_122_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_122_1/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.cycle.main | API-01258、01259 |
| chain.cycle.m_chain_deep_122_1 | API-01260、01261 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title（产业周期分析、产业周期分析模型）均在功能点列出现，且各有 1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条缺省反向；无其它参数，不写备选
- [x] unavailable（产业周期分析）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] 不按 L19 field_key 拆用例；`coverage-fp.md` 已同步 API-01258～01261
- [x] 编号使用父控闭区间 API-01258～01261；本子任务不改 code-registry

**统计**：接口 **2**；用例 **4** 条（主流程 **2**、反向 **2**）；编号闭区间 **API-01258**～**API-01261**（父控 R2-批5 分配，连续用满）。
