# 智能服务集群-科技专题服务算法库测试用例（深圳机遇分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 深圳机遇分析  
> **catalog**：`entry_id=chain.sz-opportunity` · `catalog_page_id=chain.sz-opportunity` · path `/chain/sz-opportunity`  
> **A 线对照**：`fp-split-by-api-run/work/L25.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批7）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 深圳机遇分析 | chain.sz-opportunity.main |
| 2 | 深圳机遇分析模型 | chain.sz-opportunity.m_chain_deep_128_1 |
| 3 | 深圳产业机遇数 | chain.sz-opportunity.m_chain_sz_opportunity_count |
| 4 | 深圳产业机遇评分 | chain.sz-opportunity.m_chain_sz_opportunity_score |

四个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId`，不写备选，不按 field 拆条。

**chainId 取值**：`深圳机遇分析` 的 params.example 与 sampleRequest 均为 `INB170101`。三个 POST 的 params.example 为 `INB170101`，sampleRequest 为空对象，主路径以 params.example 为准（见附录 A）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01288**～**API-01295**，连续用满）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.sz-opportunity`、组合 id。作废旧号 API-00384～00388，不复用 API-00001～00888。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01288 | 产业链分析 | 深圳机遇分析 | 主流程 | — | 深圳机遇分析 | 深圳机遇分析 | 深圳机遇分析在 chainId=INB170101 时返回文档中的全景、优势、问题与机遇字段 | 1、chainId 使用文档示例 INB170101 | 1.GET /innov/v1/industry/{chainId}/shenzhen，path 取组合 SZO-01 | 1、返回 body 为对象，与 sampleResponse 同层含 panorama、advantage、problem、opportunity；2、panorama.enterprise_count（number，responseFields 深圳企业数，示例 486）、panorama.node_count（number，示例 6）、panorama.nodes（array，responseFields 深圳环节节点）；3、panorama.nodes 元素含 node_name（string）、position（string）、enterprise_count（number），示例：芯片设计/中游/96，终端应用/下游/88，封装测试/中游/72；4、panorama.edges 为数组，元素含 src（string）、dst（string），示例：芯片设计→封装测试，封装测试→终端应用；5、panorama.district_dist 为数组，元素含 district（string）、enterprise_count（number），示例：南山区/168，龙岗区/96，福田区/84；6、advantage 含 sz_enterprise_count（number，示例 486）、sz_share（number，示例 18.6）、sz_rank（number，示例 1）、growth_rate（number，示例 15.2）、advantage_index（number，示例 92）、rank_overall（number，示例 1）、share_score（number，示例 88）、rank_score（number，示例 96）、growth_score（number，示例 90）；7、advantage.advantages 为 string 数组，示例「企业集聚与链主带动形成可持续优势」「应用场景与终端牵引相对领先」；8、problem 含 problem_count（number，示例 2）、tech_score（number，示例 52）、talent_score（number，示例 58）、market_score（number，示例 71）、capital_score（number，示例 66）、policy_score（number，示例 74）；9、problem.problems 为数组，元素含 name（string）、severity（string）、score（number），示例：关键设备/严重/52，半导体材料/严重/58；10、opportunity 含 opportunity_index（number，示例 87）、cycle_stage（string，示例 成长期后段）、trend_score（number，示例 90）、policy_score（number，示例 88）、market_score（number，示例 84）、rank_overall（number，示例 1） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/shenzhen | | INTEG | | | endpoint_id=chain.sz-opportunity.main catalog_page_id=chain.sz-opportunity 组合=SZO-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01289 | 产业链分析 | 深圳机遇分析 | 异常-入参-缺chainId | — | 深圳机遇分析 | 深圳机遇分析 | 深圳机遇分析不传 chainId | 1、path 不传 chainId | 1.GET /innov/v1/industry/{chainId}/shenzhen，path 取组合 SZO-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 panorama.enterprise_count 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/shenzhen | | INTEG | | | endpoint_id=chain.sz-opportunity.main catalog_page_id=chain.sz-opportunity 组合=SZO-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01290 | 产业链分析 | 深圳机遇分析 | 主流程 | — | 深圳机遇分析 | 深圳机遇分析模型 | 深圳机遇分析模型在 chainId=INB170101 时返回 metric_id、hint 与 responseFields | 1、chainId 使用文档示例 INB170101 | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute，请求体取组合 SZM-01 | 1、返回 body 为对象；2、sampleResponse 含 metric_id（string，示例 M_CHAIN_DEEP_128_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 另列 panorama.enterprise_count（number，深圳企业数）、panorama.nodes（array，深圳环节节点），成功体中应出现这些字段 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute | M_CHAIN_DEEP_128_1 | INTEG | | | endpoint_id=chain.sz-opportunity.m_chain_deep_128_1 catalog_page_id=chain.sz-opportunity 组合=SZM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01291 | 产业链分析 | 深圳机遇分析 | 异常-入参-缺chainId | — | 深圳机遇分析 | 深圳机遇分析模型 | 深圳机遇分析模型不传 chainId | 1、请求体不传 chainId | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute，请求体取组合 SZM-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_128_1 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute | | INTEG | | | endpoint_id=chain.sz-opportunity.m_chain_deep_128_1 catalog_page_id=chain.sz-opportunity 组合=SZM-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01292 | 产业链分析 | 深圳机遇分析 | 主流程 | — | 深圳机遇分析 | 深圳产业机遇数 | 深圳产业机遇数在 chainId=INB170101 时返回 metric_id、hint 与 responseFields | 1、chainId 使用文档示例 INB170101 | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_COUNT/compute，请求体取组合 SZC-01 | 1、返回 body 为对象；2、sampleResponse 含 metric_id（string，示例 M_CHAIN_SZ_OPPORTUNITY_COUNT）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 另列 panorama.enterprise_count（number，深圳企业数）、panorama.nodes（array，深圳环节节点），成功体中应出现这些字段 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_COUNT/compute | M_CHAIN_SZ_OPPORTUNITY_COUNT | INTEG | | | endpoint_id=chain.sz-opportunity.m_chain_sz_opportunity_count catalog_page_id=chain.sz-opportunity 组合=SZC-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01293 | 产业链分析 | 深圳机遇分析 | 异常-入参-缺chainId | — | 深圳机遇分析 | 深圳产业机遇数 | 深圳产业机遇数不传 chainId | 1、请求体不传 chainId | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_COUNT/compute，请求体取组合 SZC-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_SZ_OPPORTUNITY_COUNT 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_COUNT/compute | | INTEG | | | endpoint_id=chain.sz-opportunity.m_chain_sz_opportunity_count catalog_page_id=chain.sz-opportunity 组合=SZC-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01294 | 产业链分析 | 深圳机遇分析 | 主流程 | — | 深圳机遇分析 | 深圳产业机遇评分 | 深圳产业机遇评分在 chainId=INB170101 时返回 metric_id、hint 与 responseFields | 1、chainId 使用文档示例 INB170101 | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute，请求体取组合 SZS-01 | 1、返回 body 为对象；2、sampleResponse 含 metric_id（string，示例 M_CHAIN_SZ_OPPORTUNITY_SCORE）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 另列 panorama.enterprise_count（number，深圳企业数）、panorama.nodes（array，深圳环节节点），成功体中应出现这些字段 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute | M_CHAIN_SZ_OPPORTUNITY_SCORE | INTEG | | | endpoint_id=chain.sz-opportunity.m_chain_sz_opportunity_score catalog_page_id=chain.sz-opportunity 组合=SZS-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01295 | 产业链分析 | 深圳机遇分析 | 异常-入参-缺chainId | — | 深圳机遇分析 | 深圳产业机遇评分 | 深圳产业机遇评分不传 chainId | 1、请求体不传 chainId | 1.POST /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute，请求体取组合 SZS-02 | 1、返回 body 的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_SZ_OPPORTUNITY_SCORE 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute | | INTEG | | | endpoint_id=chain.sz-opportunity.m_chain_sz_opportunity_score catalog_page_id=chain.sz-opportunity 组合=SZS-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SZO-01 | chain.sz-opportunity.main | path chainId=INB170101 | 主路径（sampleRequest / params.example） |
| SZO-02 | chain.sz-opportunity.main | 不传 path chainId（请求 `/innov/v1/industry//shenzhen`，path 段为空） | 缺必填 chainId |
| SZM-01 | chain.sz-opportunity.m_chain_deep_128_1 | 请求体 chainId=INB170101（params.example；sampleRequest 为空对象，不作为主路径） | 主路径（必填 example） |
| SZM-02 | chain.sz-opportunity.m_chain_deep_128_1 | 不传 chainId，请求体为空 | 缺必填 chainId |
| SZC-01 | chain.sz-opportunity.m_chain_sz_opportunity_count | 请求体 chainId=INB170101（params.example；sampleRequest 为空对象，不作为主路径） | 主路径（必填 example） |
| SZC-02 | chain.sz-opportunity.m_chain_sz_opportunity_count | 不传 chainId，请求体为空 | 缺必填 chainId |
| SZS-01 | chain.sz-opportunity.m_chain_sz_opportunity_score | 请求体 chainId=INB170101（params.example；sampleRequest 为空对象，不作为主路径） | 主路径（必填 example） |
| SZS-02 | chain.sz-opportunity.m_chain_sz_opportunity_score | 不传 chainId，请求体为空 | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 深圳机遇分析 | chain.sz-opportunity.main | GET | /innov/v1/industry/{chainId}/shenzhen | chainId* | unavailable |
| 深圳机遇分析模型 | chain.sz-opportunity.m_chain_deep_128_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute | chainId* | available |
| 深圳产业机遇数 | chain.sz-opportunity.m_chain_sz_opportunity_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_COUNT/compute | chainId* | available |
| 深圳产业机遇评分 | chain.sz-opportunity.m_chain_sz_opportunity_score | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.sz-opportunity.main | API-01288、01289 |
| chain.sz-opportunity.m_chain_deep_128_1 | API-01290、01291 |
| chain.sz-opportunity.m_chain_sz_opportunity_count | API-01292、01293 |
| chain.sz-opportunity.m_chain_sz_opportunity_score | API-01294、01295 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 4 个 title（深圳机遇分析、深圳机遇分析模型、深圳产业机遇数、深圳产业机遇评分）均在功能点列出现，且各有 1 条主流程（功能项=主流程）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条缺省反向；无其它参数，不写备选
- [x] unavailable（深圳机遇分析）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] 不按 L25 field_key 拆用例；`coverage-fp.md` 已同步 API-01288～01295
- [x] 编号使用父控闭区间 API-01288～01295；本子任务不改 code-registry

**统计**：接口 **4**；用例 **8** 条（主流程 **4**、反向 **4**）；编号闭区间 **API-01288**～**API-01295**（父控 R2-批7 分配，连续用满）。
