# 智能服务集群-科技专题服务算法库测试用例（区域产业指数 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 区域产业指数  
> **catalog**：`entry_id=chain.region` · `catalog_page_id=chain.region` · path `/chain/region`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.region`  
> **A 线对照**：`fp-split-by-api-run/work/L23.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批6）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 区域指数 | chain.region.main |
| 2 | 竞争力评价 | chain.region.competitiveness |
| 3 | 区域产业指数模型 | chain.region.m_chain_deep_126_1 |

三个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId`，不写备选，不按 field 拆条。

**chainId 取值**：`区域指数`、`竞争力评价` 的 params.example 与 sampleRequest 均为 `INB170101`。`区域产业指数模型` 的 sampleRequest 为 `chain_id=INB1701`，params.example 为 `INB170101`，键名与取值不一致，主路径以 sampleRequest 为准（见附录 A）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01274**～**API-01279**，连续用满）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.region`、组合 id。作废旧号 API-00360～00373，不复用 API-00001～00888。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01274 | 产业链分析 | 区域产业指数 | 主流程 | — | 区域产业指数 | 区域指数 | 区域指数在 chainId=INB170101 时返回文档中的区域指数字段 | 1、chainId 使用文档示例 INB170101 | 1.GET /innov/v1/industry/{chainId}/region-index，path 取组合 RIX-01 | 1、返回 body 的 data 为数组，与 sampleResponse 同形；2、元素含 province（string）、region_index（number，responseFields 产业指数）、enterprise_count（number）、rank_in_chain（number）；3、sampleResponse 示例三条：深圳 province=深圳、region_index=91、enterprise_count=486、rank_in_chain=1；上海 89/430/2；北京 87/380/3 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | M_CHAIN_REGION_INDEX | INTEG | | | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=RIX-01 金样 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01275 | 产业链分析 | 区域产业指数 | 异常-入参-缺chainId | — | 区域产业指数 | 区域指数 | 区域指数不传 chainId | 1、path 不传 chainId | 1.GET /innov/v1/industry/{chainId}/region-index，path 取组合 RIX-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 region_index 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | | INTEG | | | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=RIX-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01276 | 产业链分析 | 区域产业指数 | 主流程 | — | 区域产业指数 | 竞争力评价 | 竞争力评价在 chainId=INB170101 时返回文档中的竞争力指数字段 | 1、chainId 使用文档示例 INB170101 | 1.GET /innov/v1/industry/{chainId}/competitiveness，path 取组合 CMP-01 | 1、返回 body 的 data 为数组，与 sampleResponse 同形；2、元素含 province（string）、competitiveness_index（number，responseFields 竞争力指数）；3、sampleResponse 示例三条：深圳 province=深圳、competitiveness_index=94；上海 88；北京 84 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | M_CHAIN_COMPETITIVENESS_INDEX | INTEG | | | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=CMP-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01277 | 产业链分析 | 区域产业指数 | 异常-入参-缺chainId | — | 区域产业指数 | 竞争力评价 | 竞争力评价不传 chainId | 1、path 不传 chainId | 1.GET /innov/v1/industry/{chainId}/competitiveness，path 取组合 CMP-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 competitiveness_index 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | | INTEG | | | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=CMP-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01278 | 产业链分析 | 区域产业指数 | 主流程 | — | 区域产业指数 | 区域产业指数模型 | 区域产业指数模型按文档 sampleRequest 的 chain_id 计算并返回 metric_id 与 hint | 1、请求体使用文档 sampleRequest 的 chain_id=INB1701 | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_126_1/compute，请求体取组合 RGM-01 | 1、返回 body 为对象，含 metric_id（string，responseFields 指标 ID，sampleResponse 示例 M_CHAIN_DEEP_126_1）、hint（string，sampleResponse 示例 真实 compute 响应,以实际调用为准） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_126_1/compute | M_CHAIN_DEEP_126_1 | INTEG | | | endpoint_id=chain.region.m_chain_deep_126_1 catalog_page_id=chain.region 组合=RGM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01279 | 产业链分析 | 区域产业指数 | 异常-入参-缺chainId | — | 区域产业指数 | 区域产业指数模型 | 区域产业指数模型不传 chainId | 1、请求体不传 chainId | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_126_1/compute，请求体取组合 RGM-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_126_1 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_126_1/compute | | INTEG | | | endpoint_id=chain.region.m_chain_deep_126_1 catalog_page_id=chain.region 组合=RGM-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RIX-01 | chain.region.main | path chainId=INB170101 | 主路径（sampleRequest / params.example） |
| RIX-02 | chain.region.main | 不传 path chainId（请求 `/innov/v1/industry//region-index`，path 段为空） | 缺必填 chainId |
| CMP-01 | chain.region.competitiveness | path chainId=INB170101 | 主路径（sampleRequest / params.example） |
| CMP-02 | chain.region.competitiveness | 不传 path chainId（请求 `/innov/v1/industry//competitiveness`，path 段为空） | 缺必填 chainId |
| RGM-01 | chain.region.m_chain_deep_126_1 | 请求体按 sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101，键名与取值均与 sampleRequest 不一致，本组合以 sampleRequest 为准） | 主路径（sampleRequest） |
| RGM-02 | chain.region.m_chain_deep_126_1 | 不传 chainId，请求体也不含 chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 区域指数 | chain.region.main | GET | /innov/v1/industry/{chainId}/region-index | chainId* | unavailable |
| 竞争力评价 | chain.region.competitiveness | GET | /innov/v1/industry/{chainId}/competitiveness | chainId* | unavailable |
| 区域产业指数模型 | chain.region.m_chain_deep_126_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_126_1/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.region.main | API-01274、01275 |
| chain.region.competitiveness | API-01276、01277 |
| chain.region.m_chain_deep_126_1 | API-01278、01279 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 3 个 title（区域指数、竞争力评价、区域产业指数模型）均在功能点列出现，且各有 1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条缺省反向；无其它参数，不写备选
- [x] unavailable（区域指数、竞争力评价）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] 不按 L23 field_key 拆用例；`coverage-fp.md` 已同步 API-01274～01279
- [x] 编号使用父控闭区间 API-01274～01279；本子任务不改 code-registry

**统计**：接口 **3**；用例 **6** 条（主流程 **3**、反向 **3**）；编号闭区间 **API-01274**～**API-01279**（父控 R2-批6 分配，连续用满）。
