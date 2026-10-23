# 智能服务集群-科技专题服务算法库测试用例（产业战略重要性分析 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.strategic-importance` · `catalog_page_id=chain.strategic-importance` · path `#/chain/strategic-importance`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.strategic-importance`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip`：`chain.strategic-importance`，60 条无对应六级；不改 `work/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批9）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 战略重要性 | chain.strategic-importance.main | unavailable |

本页仅 1 个 title。必填 path 参数 `chainId`，无其它参数。写 1 条主流程 + 1 条缺 `chainId` 反向，不写备选，不按 field 拆条。

**chainId 取值**：params.example 与 sampleRequest 均为 `INB170101`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00527**～**FUNC-00530**，共 **4** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.strategic-importance`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00527 | 算法工具库 | 科技专题服务算法库 | 产业链关键环节识别模型 | 战略重要性 | 产业战略重要性分析 | 战略重要性 | 验证战略重要性功能，检查 chainId=INB170101 时返回面板中的环节战略重要性 rows 及行内字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB170101 | 1.侧栏进入「产业链分析」→「产业战略重要性分析」；2.切换至「算法测试」tab；3.接口下拉选择「战略重要性」；4.填写 chainId=INB170101，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层含 rows（array，responseFields 环节战略重要性）；2、rows 元素含 node_name（string）、position（string）、importance_score（number）；3、sampleResponse 示例三条：芯片设计 position=上游 importance_score=88.4；整机制造 position=中游 importance_score=79.1；终端应用 position=下游 importance_score=71.6 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/strategic-importance | M_CHAIN_STRATEGIC_IMPORTANCE | INTEG |  | FUNC-00527 | endpoint_id=chain.strategic-importance.main catalog_page_id=chain.strategic-importance 组合=STI-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00528 | 算法工具库 | 科技专题服务算法库 | 产业链关键环节识别模型 | 战略重要性 | 产业战略重要性分析 | 战略重要性 | 验证战略重要性功能，检查不传 chainId 时返回面板指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业战略重要性分析」；2.切换至「算法测试」tab；3.接口下拉选择「战略重要性」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出缺少 chainId；2、不返回含 rows 或 importance_score 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/strategic-importance |  | INTEG |  | FUNC-00528 | endpoint_id=chain.strategic-importance.main catalog_page_id=chain.strategic-importance 组合=STI-02 场景=异常-入参-缺chainId catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00529 | 算法工具库 | 科技专题服务算法库 | 产业链关键环节识别模型 | 战略重要性 | 产业战略重要性分析 | 接口信息 | 验证产业战略重要性分析的接口信息功能，检查接口数量、名称和 method/path 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业战略重要性分析」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「战略重要性」；3、核对概览区 title、method（GET）、path（/innov/v1/industry/{chainId}/strategic-importance）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/strategic-importance |  | INTEG |  | FUNC-00529 | catalog_page_id=chain.strategic-importance 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00530 | 算法工具库 | 科技专题服务算法库 | 产业链关键环节识别模型 | 战略重要性 | 产业战略重要性分析 | 算法测试 | 验证产业战略重要性分析的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业链分析」→「产业战略重要性分析」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /innov/v1/industry/{chainId}/strategic-importance；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「战略重要性」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /innov/v1/industry/{chainId}/strategic-importance，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/strategic-importance |  | INTEG |  | FUNC-00530 | catalog_page_id=chain.strategic-importance 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| STI-01 | chain.strategic-importance.main | chainId=INB170101 | 主路径（sampleRequest / params.example） |
| STI-02 | chain.strategic-importance.main | 不传 chainId | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 战略重要性 | chain.strategic-importance.main | GET | /innov/v1/industry/{chainId}/strategic-importance | chainId* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.strategic-importance.main | FUNC-00527、00528 |
| （页面清单） | FUNC-00529、00530 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「战略重要性」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-00527）
- [x] 有参接口：文档示例正向 1 条主流程；必填 chainId 恰好 1 条反向；无可选参数，无备选组合
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 五级/六级：产业链关键环节识别模型 / 战略重要性（A 线无 Lxx，与 L21 req_only 战略语义对齐，不按 field 拆条）
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [ ] `coverage-fp.md` 待父控同步 FUNC-00527～00530（本子任务仅交付 FUNC 册）

**统计**：catalog endpoint **1**；主流程 **1**；反向 **1**；清单 **2**；合计 **4** 条；编号闭区间 **FUNC-00527**～**FUNC-00530**（R3-批9 · chain.strategic-importance）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **4** |
| 编号闭区间 | **FUNC-00527**～**FUNC-00530** |
| 接口向（不含清单） | **2** |
| 清单 | **2** |
| 对照 API 册 | `API-产业战略重要性分析-用例.md`（API-01312～01313 仍有效；本页无新增 API 号） |
