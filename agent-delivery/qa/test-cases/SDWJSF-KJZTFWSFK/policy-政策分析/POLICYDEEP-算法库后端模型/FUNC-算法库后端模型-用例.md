# 智能服务集群-科技专题服务算法库测试用例（算法库后端模型 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=policy.deep` · `catalog_page_id=policy.deep` · path `#/policy/deep`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.deep`  
> **A 线对照**：**无对应 Lxx**（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.deep`，原因：不扩六级；不改 `work/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批13）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 后端模型 | policy.deep.models | unavailable |

两个查询参数均可选：`scope_code`、`limit`。主流程对齐 `sampleRequest`：同时传 `scope_code=440300`、`limit=50`。备选与 sample 相反：不传 `scope_code`（保留 `limit=50`）、不传 `limit`（保留 `scope_code=440300`）。反向各 1 条非法，不把省略写成反向。catalog `status=unavailable`，仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00739**～**FUNC-00745**，共 **7** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.deep`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00739 | 算法工具库 | 科技专题服务算法库 | 算法库后端模型 | 后端模型 | 算法库后端模型 | 后端模型 | 验证后端模型功能，检查填写 sampleRequest 所示参数 传 scope_code=440300、limit=50 时返回六大模型索引字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440300；limit=50 | 1.侧栏进入「政策分析」→「算法库后端模型」；2.切换至「算法测试」tab；3.接口下拉选择「后端模型」；4.填写 scope_code=440300、limit=50，点击调用 | 1、返回面板 body 含 rows（array，responseFields 后端模型索引）；2、rows 元素含 model（string）、model_name（string）、metric_id（string）、index（number）；3、与 sampleResponse 逐字段一致：model=focus、model_name=政策焦点识别模型、metric_id=M_POLICY_DEEP_166_1、index=82.6；model=intensity、model_name=政策力度评估模型、metric_id=M_POLICY_DEEP_167_1、index=78.4；model=effect、model_name=政策效果评估模型、metric_id=M_POLICY_DEEP_168_1、index=75.1；model=gap、model_name=政策短板识别模型、metric_id=M_POLICY_DEEP_169_1、index=3；model=opportunity、model_name=政策机遇识别模型、metric_id=M_POLICY_DEEP_170_1、index=9；model=layout、model_name=政策布局推荐模型、metric_id=M_POLICY_DEEP_171_1、index=6 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_DEEP_166_1 | INTEG |  | FUNC-00739 | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00740 | 算法工具库 | 科技专题服务算法库 | 算法库后端模型 | 后端模型 | 算法库后端模型 | 后端模型 | 验证后端模型功能，检查不传可选 scope_code、limit 保持文档示例 50 时仍返回模型索引字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 scope_code；limit=50 | 1.侧栏进入「政策分析」→「算法库后端模型」；2.切换至「算法测试」tab；3.接口下拉选择「后端模型」；4.不传 scope_code，填写 limit=50，点击调用 | 1、返回面板 body 含 rows（array）；2、元素仍含 model（string）、model_name（string）、metric_id（string）、index（number）；3、字段与 sampleResponse 逐字段同类，示例值（focus/政策焦点识别模型/M_POLICY_DEEP_166_1/82.6，intensity/政策力度评估模型/M_POLICY_DEEP_167_1/78.4，effect/政策效果评估模型/M_POLICY_DEEP_168_1/75.1，gap/政策短板识别模型/M_POLICY_DEEP_169_1/3，opportunity/政策机遇识别模型/M_POLICY_DEEP_170_1/9，layout/政策布局推荐模型/M_POLICY_DEEP_171_1/6）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_DEEP_166_1 | INTEG |  | FUNC-00740 | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00741 | 算法工具库 | 科技专题服务算法库 | 算法库后端模型 | 后端模型 | 算法库后端模型 | 后端模型 | 验证后端模型功能，检查不传可选 limit、scope_code 保持文档示例 440300 时仍返回模型索引字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440300；不传 limit | 1.侧栏进入「政策分析」→「算法库后端模型」；2.切换至「算法测试」tab；3.接口下拉选择「后端模型」；4.不传 limit，填写 scope_code=440300，点击调用 | 1、返回面板 body 含 rows（array）；2、元素仍含 model（string）、model_name（string）、metric_id（string）、index（number）；3、字段与 sampleResponse 逐字段同类，示例值（focus/政策焦点识别模型/M_POLICY_DEEP_166_1/82.6，intensity/政策力度评估模型/M_POLICY_DEEP_167_1/78.4，effect/政策效果评估模型/M_POLICY_DEEP_168_1/75.1，gap/政策短板识别模型/M_POLICY_DEEP_169_1/3，opportunity/政策机遇识别模型/M_POLICY_DEEP_170_1/9，layout/政策布局推荐模型/M_POLICY_DEEP_171_1/6）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_DEEP_166_1 | INTEG |  | FUNC-00741 | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00742 | 算法工具库 | 科技专题服务算法库 | 算法库后端模型 | 后端模型 | 算法库后端模型 | 后端模型 | 验证后端模型功能，检查 scope_code 非法、limit 保持文档合法值 50 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=50 | 1.侧栏进入「政策分析」→「算法库后端模型」；2.切换至「算法测试」tab；3.接口下拉选择「后端模型」；4.填写 scope_code=__invalid__、limit=50，点击调用 | 1、返回面板的 message 或 msg 指出 scope_code 非法；2、不返回含 model、model_name、metric_id、index 的成功业务 rows | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus |  | INTEG |  | FUNC-00742 | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-04 场景=异常-入参-非法scope_code catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00743 | 算法工具库 | 科技专题服务算法库 | 算法库后端模型 | 后端模型 | 算法库后端模型 | 后端模型 | 验证后端模型功能，检查 limit 非法、scope_code 保持文档示例 440300 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440300 | 1.侧栏进入「政策分析」→「算法库后端模型」；2.切换至「算法测试」tab；3.接口下拉选择「后端模型」；4.填写 scope_code=440300、limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 model、model_name、metric_id、index 的成功业务 rows | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus |  | INTEG |  | FUNC-00743 | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=MOD-05 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00744 | 算法工具库 | 科技专题服务算法库 | 算法库后端模型 | 后端模型 | 算法库后端模型 | 接口信息 | 验证算法库后端模型的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「算法库后端模型」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「后端模型」；3、核对概览区标题、method（GET）、path（/policy/v1/policy/analysis/focus）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus |  | INTEG |  | FUNC-00744 | catalog_page_id=policy.deep 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00745 | 算法工具库 | 科技专题服务算法库 | 算法库后端模型 | 后端模型 | 算法库后端模型 | 算法测试 | 验证算法库后端模型的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「算法库后端模型」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /policy/v1/policy/analysis/focus；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「后端模型」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /policy/v1/policy/analysis/focus，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus |  | INTEG |  | FUNC-00745 | catalog_page_id=policy.deep 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MOD-01 | policy.deep.models | scope_code=440300；limit=50 | 主路径（sampleRequest） |
| MOD-02 | policy.deep.models | 不传 scope_code；limit=50 | 与 sample 相反：省略可选 scope_code |
| MOD-03 | policy.deep.models | scope_code=440300；不传 limit | 与 sample 相反：省略可选 limit |
| MOD-04 | policy.deep.models | scope_code=__invalid__；limit=50 | 只破坏 scope_code |
| MOD-05 | policy.deep.models | scope_code=440300；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 后端模型 | policy.deep.models | GET | /policy/v1/policy/analysis/focus | scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.deep.models | FUNC-00739、00740、00741、00742、00743 |
| （页面清单） | FUNC-00744、00745 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「后端模型」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-00739）
- [x] 有参接口：sampleRequest 主流程 1 条；省略 scope_code 1 条、省略 limit 1 条；每个可选参数 1 条非法反向（00742、00743）
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 五级/六级按 catalog 页（算法库后端模型 / 后端模型）填写；A 线无 Lxx
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00739～00745

**统计**：catalog endpoint **1**；title **1**；FUNC 用例 **7** 条；主流程 **1**、备选 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00739**～**FUNC-00745**（R3-批13 policy.deep）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **7** |
| 编号闭区间 | **FUNC-00739**～**FUNC-00745** |
| 接口向（不含清单） | **5** |
| 主流程 | **1** |
| 备选-参数组合 | **2** |
| 反向 | **2** |
| 清单 | **2** |
| 已删 API 册 | `API-算法库后端模型-用例.md`（API-01513～01517 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
