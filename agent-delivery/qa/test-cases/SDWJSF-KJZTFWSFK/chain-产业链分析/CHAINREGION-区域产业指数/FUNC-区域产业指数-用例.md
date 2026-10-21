# 智能服务集群-科技专题服务算法库测试用例（区域产业指数 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.region` · `catalog_page_id=chain.region` · path `#/chain/region`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.region`  
> **A 线对照**：`fp-split-by-api-run/work/L23.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批7）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 区域指数 | chain.region.main | unavailable |
| 2 | 竞争力评价 | chain.region.competitiveness | unavailable |
| 3 | 区域产业指数模型 | chain.region.m_chain_deep_126_1 | available |

三个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId`，不写备选，不按 field 拆条。

**chainId 取值**：`区域指数`、`竞争力评价` 的 params.example 与 sampleRequest 均为 `INB170101`。`区域产业指数模型` 的 sampleRequest 为 `chain_id=INB1701`，params.example 为 `INB170101`，键名与取值不一致，主路径以 sampleRequest 为准（见附录 A）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00473**～**FUNC-00480**，共 **8** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.region`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00473 | 算法工具库 | 科技专题服务算法库 | 区域产业指数模型 | 区域指数 | 区域产业指数 | 区域指数 | 验证区域指数功能，检查 chainId=INB170101 时返回面板中的区域指数字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「区域产业指数」；2.切换至「算法测试」tab；3.接口下拉选择「区域指数」；4.填写 chainId=INB170101，点击调用 | 1、返回面板 body 与 sampleResponse 同形为数组（若有信封则 data 为该数组）；2、元素含 province（string）、region_index（number，responseFields 产业指数）、enterprise_count（number）、rank_in_chain（number）；3、sampleResponse 示例三条：深圳 province=深圳、region_index=91、enterprise_count=486、rank_in_chain=1；上海 89/430/2；北京 87/380/3 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | M_CHAIN_REGION_INDEX | INTEG |  |  | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=RIX-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00474 | 算法工具库 | 科技专题服务算法库 | 区域产业指数模型 | 区域指数 | 区域产业指数 | 区域指数 | 验证区域指数功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「区域产业指数」；2.切换至「算法测试」tab；3.接口下拉选择「区域指数」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 region_index 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index |  | INTEG |  |  | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=RIX-02 场景=异常-入参-缺chainId catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00475 | 算法工具库 | 科技专题服务算法库 | 区域产业指数模型 | 竞争力评价 | 区域产业指数 | 竞争力评价 | 验证竞争力评价功能，检查 chainId=INB170101 时返回面板中的竞争力指数字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「区域产业指数」；2.切换至「算法测试」tab；3.接口下拉选择「竞争力评价」；4.填写 chainId=INB170101，点击调用 | 1、返回面板 body 与 sampleResponse 同形为数组（若有信封则 data 为该数组）；2、元素含 province（string）、competitiveness_index（number，responseFields 竞争力指数）；3、sampleResponse 示例三条：深圳 province=深圳、competitiveness_index=94；上海 88；北京 84 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | M_CHAIN_COMPETITIVENESS_INDEX | INTEG |  |  | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=CMP-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00476 | 算法工具库 | 科技专题服务算法库 | 区域产业指数模型 | 竞争力评价 | 区域产业指数 | 竞争力评价 | 验证竞争力评价功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「区域产业指数」；2.切换至「算法测试」tab；3.接口下拉选择「竞争力评价」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 competitiveness_index 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness |  | INTEG |  |  | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=CMP-02 场景=异常-入参-缺chainId catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00477 | 算法工具库 | 科技专题服务算法库 | 区域产业指数模型 | 区域产业指数模型 | 区域产业指数 | 区域产业指数模型 | 验证区域产业指数模型功能，检查填写 sampleRequest 所示参数 传 chain_id=INB1701 后返回 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「区域产业指数」；2.切换至「算法测试」tab；3.接口下拉选择「区域产业指数模型」；4.填写 请求体按sampleRequest：chain_id=INB1701（params.name=chainId，example=INB170101，键名与取值均与sampleRequest不一致，本组合以sampleRequest为准），点击调用 | 1、返回面板 body 为对象，含 metric_id（string，responseFields 指标 ID，sampleResponse 示例 M_CHAIN_DEEP_126_1）、hint（string，sampleResponse 示例 真实 compute 响应,以实际调用为准）；2、sampleResponse 无更深嵌套对象 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_126_1/compute | M_CHAIN_DEEP_126_1 | INTEG |  |  | endpoint_id=chain.region.m_chain_deep_126_1 catalog_page_id=chain.region 组合=RGM-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00478 | 算法工具库 | 科技专题服务算法库 | 区域产业指数模型 | 区域产业指数模型 | 区域产业指数 | 区域产业指数模型 | 验证区域产业指数模型功能，检查不传 chainId/chain_id 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「区域产业指数」；2.切换至「算法测试」tab；3.接口下拉选择「区域产业指数模型」；4.不传 chainId，请求体也不含 chain_id，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_126_1 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_126_1/compute |  | INTEG |  |  | endpoint_id=chain.region.m_chain_deep_126_1 catalog_page_id=chain.region 组合=RGM-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00479 | 算法工具库 | 科技专题服务算法库 | 区域产业指数模型 | 区域指数 | 区域产业指数 | 接口信息 | 验证区域产业指数的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「区域产业指数」；2.停留在「接口信息」tab；3.接口下拉切换到「竞争力评价」 | 1、页头数量、下拉项数均为 3；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应区域指数 GET /innov/v1/industry/{chainId}/region-index；4、切换后概览对应竞争力评价 GET /innov/v1/industry/{chainId}/competitiveness，参数表与示例区已刷新；1、确认页头接口数量为 3；2、查看默认选中接口的概览 title、method、path 与 §0 清单第一项一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.region 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00480 | 算法工具库 | 科技专题服务算法库 | 区域产业指数模型 | 区域指数 | 区域产业指数 | 算法测试 | 验证区域产业指数的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「区域产业指数」；2.切换到「算法测试」tab；3.下拉切换到「区域产业指数模型」 | 1、算法测试 tab 下拉共 3 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「区域产业指数模型」；3、调用区 method 为 POST、path 为 /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_126_1/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.region 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RIX-01 | chain.region.main | chainId=INB170101 | 主路径（sampleRequest / params.example） |
| RIX-02 | chain.region.main | 不传 chainId | 缺必填 chainId |
| CMP-01 | chain.region.competitiveness | chainId=INB170101 | 主路径（sampleRequest / params.example） |
| CMP-02 | chain.region.competitiveness | 不传 chainId | 缺必填 chainId |
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
| chain.region.main | FUNC-00473、00474 |
| chain.region.competitiveness | FUNC-00475、00476 |
| chain.region.m_chain_deep_126_1 | FUNC-00477、00478 |
| （页面清单） | FUNC-00479、00480 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 3 个 title（区域指数、竞争力评价、区域产业指数模型）均在功能点列出现，且各有 1 条主流程（场景=主流程）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条缺省反向；无其它参数，不写备选
- [x] unavailable（区域指数、竞争力评价）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤为联调台侧栏进页 + 算法测试调用，无 GET/POST 步骤
- [x] 五级/六级按 L23（区域产业指数模型 / 区域指数·竞争力评价·区域产业指数模型）填写
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（3 接口页含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00473～00480

**统计**：catalog endpoint **3**；title **3**；FUNC 用例 **8** 条；主流程 **3**、反向 **3**、清单 **2**；编号闭区间 **FUNC-00473**～**FUNC-00480**（R3-批7 chain.region）。
