# 智能服务集群-科技专题服务算法库测试用例（深圳机遇识别 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.sz-opportunity` · `catalog_page_id=chain.sz-opportunity` · path `#/chain/sz-opportunity`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.sz-opportunity`  
> **A 线对照**：`fp-split-by-api-run/work/L25.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批8）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 深圳机遇分析 | chain.sz-opportunity.main | unavailable |
| 2 | 深圳机遇分析模型 | chain.sz-opportunity.m_chain_deep_128_1 | available |
| 3 | 深圳产业机遇数 | chain.sz-opportunity.m_chain_sz_opportunity_count | available |
| 4 | 深圳产业机遇评分 | chain.sz-opportunity.m_chain_sz_opportunity_score | available |

四个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId` 反向，不写备选，不按 field 拆条。

**chainId 取值**：`深圳机遇分析` 的 params.example 与 sampleRequest 均为 `INB170101`。三个 POST 的 params.example 为 `INB170101`，sampleRequest 为空对象，主路径以 params.example 为准（见附录 A）。

同 path 的 `chain.shenzhen.main`、`chain.sz-problem.main` 与本页 GET 共用 `/innov/v1/industry/{chainId}/shenzhen`。本册只按 `catalog_page_id=chain.sz-opportunity` 写预期，不混用其它页。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00493**～**FUNC-00502**，共 **10** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.sz-opportunity`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00493 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 深圳机遇分析 | 验证深圳机遇分析功能，检查 chainId=INB170101 时返回面板中的 panorama、advantage、problem、opportunity 字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.切换至「算法测试」tab；3.接口下拉选择「深圳机遇分析」；4.填写 chainId=INB170101，点击调用 | 1、返回面板 body 为对象，顶层含 panorama、advantage、problem、opportunity，与 sampleResponse 同层逐字段一致；2、panorama.enterprise_count（number，responseFields 深圳企业数，示例 486）、panorama.node_count（number，示例 6）；3、panorama.nodes（array，responseFields 深圳环节节点），元素含 node_name（string）、position（string）、enterprise_count（number），示例：芯片设计/中游/96、终端应用/下游/88、封装测试/中游/72；4、panorama.edges 为数组，元素含 src（string）、dst（string），示例：芯片设计→封装测试、封装测试→终端应用；5、panorama.district_dist 为数组，元素含 district（string）、enterprise_count（number），示例：南山区/168、龙岗区/96、福田区/84；6、advantage 含 sz_enterprise_count（number，示例 486）、sz_share（number，示例 18.6）、sz_rank（number，示例 1）、growth_rate（number，示例 15.2）、advantage_index（number，示例 92）、rank_overall（number，示例 1）、share_score（number，示例 88）、rank_score（number，示例 96）、growth_score（number，示例 90）；advantages 为 string 数组，示例「企业集聚与链主带动形成可持续优势」「应用场景与终端牵引相对领先」；7、problem 含 problem_count（number，示例 2）、tech_score（number，示例 52）、talent_score（number，示例 58）、market_score（number，示例 71）、capital_score（number，示例 66）、policy_score（number，示例 74）；problems 为数组，元素含 name（string）、severity（string）、score（number），示例：关键设备/严重/52、半导体材料/严重/58；8、opportunity 含 opportunity_index（number，示例 87）、cycle_stage（string，示例 成长期后段）、trend_score（number，示例 90）、policy_score（number，示例 88）、market_score（number，示例 84）、rank_overall（number，示例 1） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/shenzhen |  | INTEG |  | FUNC-00493 | endpoint_id=chain.sz-opportunity.main catalog_page_id=chain.sz-opportunity 组合=SZO-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00494 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 深圳机遇分析 | 验证深圳机遇分析功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.切换至「算法测试」tab；3.接口下拉选择「深圳机遇分析」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 panorama.enterprise_count 或 opportunity.opportunity_index 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/shenzhen |  | INTEG |  | FUNC-00494 | endpoint_id=chain.sz-opportunity.main catalog_page_id=chain.sz-opportunity 组合=SZO-02 场景=异常-入参-缺chainId catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00495 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 深圳机遇分析模型 | 验证深圳机遇分析模型功能，检查 chainId=INB170101 时返回 metric_id、hint 与 responseFields 对应字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.切换至「算法测试」tab；3.接口下拉选择「深圳机遇分析模型」；4.填写 请求体chainId=INB170101（params.example、sampleRequest 为空对象，不作为主路径），点击调用 | 1、返回面板 body 为对象；2、含 metric_id（string，示例 M_CHAIN_DEEP_128_1）、hint（string，sampleResponse 示例 真实 compute 响应,以实际调用为准）；3、responseFields 另列 panorama.enterprise_count（number，深圳企业数）、panorama.nodes（array，深圳环节节点），成功体中应出现这些字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute | M_CHAIN_DEEP_128_1 | INTEG |  | FUNC-00495 | endpoint_id=chain.sz-opportunity.m_chain_deep_128_1 catalog_page_id=chain.sz-opportunity 组合=SZM-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00496 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 深圳机遇分析模型 | 验证深圳机遇分析模型功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.切换至「算法测试」tab；3.接口下拉选择「深圳机遇分析模型」；4.不传 chainId，请求体为空，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_128_1 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute |  | INTEG |  | FUNC-00496 | endpoint_id=chain.sz-opportunity.m_chain_deep_128_1 catalog_page_id=chain.sz-opportunity 组合=SZM-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00497 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 深圳产业机遇数 | 验证深圳产业机遇数功能，检查 chainId=INB170101 时返回 metric_id、hint 与 responseFields 对应字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.切换至「算法测试」tab；3.接口下拉选择「深圳产业机遇数」；4.填写 请求体chainId=INB170101（params.example、sampleRequest 为空对象，不作为主路径），点击调用 | 1、返回面板 body 为对象；2、含 metric_id（string，示例 M_CHAIN_SZ_OPPORTUNITY_COUNT）、hint（string，sampleResponse 示例 真实 compute 响应,以实际调用为准）；3、responseFields 另列 panorama.enterprise_count（number，深圳企业数）、panorama.nodes（array，深圳环节节点），成功体中应出现这些字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_COUNT/compute | M_CHAIN_SZ_OPPORTUNITY_COUNT | INTEG |  | FUNC-00497 | endpoint_id=chain.sz-opportunity.m_chain_sz_opportunity_count catalog_page_id=chain.sz-opportunity 组合=SZC-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00498 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 深圳产业机遇数 | 验证深圳产业机遇数功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.切换至「算法测试」tab；3.接口下拉选择「深圳产业机遇数」；4.不传 chainId，请求体为空，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_SZ_OPPORTUNITY_COUNT 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_COUNT/compute |  | INTEG |  | FUNC-00498 | endpoint_id=chain.sz-opportunity.m_chain_sz_opportunity_count catalog_page_id=chain.sz-opportunity 组合=SZC-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00499 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 深圳产业机遇评分 | 验证深圳产业机遇评分功能，检查 chainId=INB170101 时返回 metric_id、hint 与 responseFields 对应字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.切换至「算法测试」tab；3.接口下拉选择「深圳产业机遇评分」；4.填写 请求体chainId=INB170101（params.example、sampleRequest 为空对象，不作为主路径），点击调用 | 1、返回面板 body 为对象；2、含 metric_id（string，示例 M_CHAIN_SZ_OPPORTUNITY_SCORE）、hint（string，sampleResponse 示例 真实 compute 响应,以实际调用为准）；3、responseFields 另列 panorama.enterprise_count（number，深圳企业数）、panorama.nodes（array，深圳环节节点），成功体中应出现这些字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute | M_CHAIN_SZ_OPPORTUNITY_SCORE | INTEG |  | FUNC-00499 | endpoint_id=chain.sz-opportunity.m_chain_sz_opportunity_score catalog_page_id=chain.sz-opportunity 组合=SZS-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00500 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 深圳产业机遇评分 | 验证深圳产业机遇评分功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.切换至「算法测试」tab；3.接口下拉选择「深圳产业机遇评分」；4.不传 chainId，请求体为空，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_SZ_OPPORTUNITY_SCORE 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute |  | INTEG |  | FUNC-00500 | endpoint_id=chain.sz-opportunity.m_chain_sz_opportunity_score catalog_page_id=chain.sz-opportunity 组合=SZS-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00501 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 接口信息 | 验证深圳机遇分析的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.停留在「接口信息」tab；3.接口下拉切换到「深圳机遇分析模型」 | 1、页头数量、下拉项数均为 4；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应深圳机遇分析 GET /innov/v1/industry/{chainId}/shenzhen；4、切换后概览对应深圳机遇分析模型 POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_128_1/compute，参数表与示例区已刷新；1、确认页头接口数量为 4；2、查看默认选中接口的概览 title、method、path 与 §0 清单第一项一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00501 | catalog_page_id=chain.sz-opportunity 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00502 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 深圳机遇分析模型 | 深圳机遇分析 | 算法测试 | 验证深圳机遇分析的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「深圳机遇分析」；2.切换到「算法测试」tab；3.下拉切换到「深圳产业机遇评分」 | 1、算法测试 tab 下拉共 4 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「深圳产业机遇评分」；3、调用区 method 为 POST、path 为 /innov/v1/industry/chainan/metric/M_CHAIN_SZ_OPPORTUNITY_SCORE/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00502 | catalog_page_id=chain.sz-opportunity 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SZO-01 | chain.sz-opportunity.main | chainId=INB170101 | 主路径（sampleRequest / params.example） |
| SZO-02 | chain.sz-opportunity.main | 不传 chainId | 缺必填 chainId |
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
| chain.sz-opportunity.main | FUNC-00493、00494 |
| chain.sz-opportunity.m_chain_deep_128_1 | FUNC-00495、00496 |
| chain.sz-opportunity.m_chain_sz_opportunity_count | FUNC-00497、00498 |
| chain.sz-opportunity.m_chain_sz_opportunity_score | FUNC-00499、00500 |
| （页面清单） | FUNC-00501、00502 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 4 个 title（深圳机遇分析、深圳机遇分析模型、深圳产业机遇数、深圳产业机遇评分）均在功能点列出现，且各有 1 条主流程（场景=主流程）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条缺省反向；无其它参数，不写备选
- [x] unavailable（深圳机遇分析）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤为联调台侧栏进页 + 算法测试调用，无 GET/POST 步骤
- [x] 五级/六级按 L25（产业链深度分析模型构建 / 深圳机遇分析模型）填写
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（4 接口页含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00493～00502

**统计**：catalog endpoint **4**；title **4**；FUNC 用例 **10** 条；主流程 **4**、反向 **4**、清单 **2**；编号闭区间 **FUNC-00493**～**FUNC-00502**（R3-批8 chain.sz-opportunity）。
