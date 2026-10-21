# 智能服务集群-科技专题服务算法库测试用例（重点布局产业推荐 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.layout` · `catalog_page_id=chain.layout` · path `#/chain/layout`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.layout`  
> **A 线对照**：`fp-split-by-api-run/work/L26.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批8）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 重点布局产业推荐 | chain.hotspot.recommendation | unavailable |
| 2 | 重点布局产业推荐模型 | chain.layout.m_chain_deep_129_1 | available |

两个 title 均只有必填 `chainId`。各 1 条主流程 + 1 条缺 `chainId`，不写备选，不按 field 拆条。

**chainId 取值**：`重点布局产业推荐` 的 params.example 与 sampleRequest 均为 `INB170101`（描述另写 INB1701 无推荐，本册不单开空态用例）。`重点布局产业推荐模型` 的 sampleRequest 为 `{}`，无 `chain_id` 键；主路径取 params.example `INB170101`，请求体键名用 params.name `chainId`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00515**～**FUNC-00520**，共 **6** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.layout`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00515 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 重点布局产业推荐模型 | 重点布局产业推荐 | 重点布局产业推荐 | 验证重点布局产业推荐功能，检查 chainId=INB170101 时返回面板中的推荐级别、推荐指数与维度得分 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「重点布局产业推荐」；2.切换至「算法测试」tab；3.接口下拉选择「重点布局产业推荐」；4.填写 chainId=INB170101，点击调用 | 1、返回面板 body 为对象，无嵌套数组；与 sampleResponse 同层逐字段一致：recommend_level（string，responseFields 推荐级别，示例 优先布局）、recommend_index（number，responseFields 推荐指数，示例 84.2）、advantage_score（number，sampleResponse 多出字段，示例 78）、opportunity_score（number，sampleResponse 多出字段，示例 81）、policy_match_score（number，sampleResponse 多出字段，示例 88）、rank_overall（number，sampleResponse 多出字段，示例 2） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/recommendation | M_CHAIN_LAYOUT_PRIORITY_SCORE | INTEG |  |  | endpoint_id=chain.hotspot.recommendation catalog_page_id=chain.layout 组合=LAY-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00516 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 重点布局产业推荐模型 | 重点布局产业推荐 | 重点布局产业推荐 | 验证重点布局产业推荐功能，检查不传 chainId 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「重点布局产业推荐」；2.切换至「算法测试」tab；3.接口下拉选择「重点布局产业推荐」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 recommend_level 或 recommend_index 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/recommendation |  | INTEG |  |  | endpoint_id=chain.hotspot.recommendation catalog_page_id=chain.layout 组合=LAY-02 场景=异常-入参-缺chainId catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00517 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 重点布局产业推荐模型 | 重点布局产业推荐 | 重点布局产业推荐模型 | 验证重点布局产业推荐模型功能，检查 chainId=INB170101 时返回 metric_id、hint，且 responseFields 含推荐级别与推荐指数 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「重点布局产业推荐」；2.切换至「算法测试」tab；3.接口下拉选择「重点布局产业推荐模型」；4.填写 请求体chainId=INB170101（sampleRequest为{}，无chain_id、params.name=chainId，example=INB170101），点击调用 | 1、返回面板 body 为对象，无嵌套数组；与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_CHAIN_DEEP_129_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 同层另列 recommend_level（string，推荐级别）、recommend_index（number，推荐指数），sampleResponse 未给这两字段的示例值 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute | M_CHAIN_DEEP_129_1 | INTEG |  |  | endpoint_id=chain.layout.m_chain_deep_129_1 catalog_page_id=chain.layout 组合=LYM-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00518 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 重点布局产业推荐模型 | 重点布局产业推荐 | 重点布局产业推荐模型 | 验证重点布局产业推荐模型功能，检查不传 chainId 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「重点布局产业推荐」；2.切换至「算法测试」tab；3.接口下拉选择「重点布局产业推荐模型」；4.不传 chainId，请求体也不含 chain_id，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 metric_id 为 M_CHAIN_DEEP_129_1 或 recommend_level 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute |  | INTEG |  |  | endpoint_id=chain.layout.m_chain_deep_129_1 catalog_page_id=chain.layout 组合=LYM-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00519 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 重点布局产业推荐模型 | 重点布局产业推荐 | 接口信息 | 验证重点布局产业推荐的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「重点布局产业推荐」；2.停留在「接口信息」tab；3.接口下拉切换到「重点布局产业推荐模型」 | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应重点布局产业推荐 GET /innov/v1/industry/{chainId}/recommendation；4、切换后概览对应重点布局产业推荐模型 POST /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute，参数表与示例区已刷新；1、确认页头接口数量为 2；2、查看默认选中接口的概览 title、method、path 与 §0 清单第一项一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.layout 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00520 | 算法工具库 | 科技专题服务算法库 | 产业链深度分析模型构建 | 重点布局产业推荐模型 | 重点布局产业推荐 | 算法测试 | 验证重点布局产业推荐的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「重点布局产业推荐」；2.切换到「算法测试」tab；3.下拉切换到「重点布局产业推荐模型」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「重点布局产业推荐模型」；3、调用区 method 为 POST、path 为 /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_129_1/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.layout 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| LAY-01 | chain.hotspot.recommendation | chainId=INB170101 | 主路径（sampleRequest 与 params.example 一致） |
| LAY-02 | chain.hotspot.recommendation | 不传 chainId | 缺必填 chainId |
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
| chain.hotspot.recommendation | FUNC-00515、00516 |
| chain.layout.m_chain_deep_129_1 | FUNC-00517、00518 |
| （页面清单） | FUNC-00519、00520 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title（重点布局产业推荐、重点布局产业推荐模型）均在功能点列出现，且各有 1 条 `场景=主流程`（FUNC-00515、00517）
- [x] 有参接口：文档示例正向各 1 条；必填 chainId 各 1 条反向；无可选参数，无备选-参数组合
- [x] unavailable（重点布局产业推荐）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 五级/六级按 L26（产业链深度分析模型构建 / 重点布局产业推荐模型）填写
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（2 接口页含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00515～00520

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **6** 条；主流程 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00515**～**FUNC-00520**（R3-批8 chain.layout）。
