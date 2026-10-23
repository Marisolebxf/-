# 智能服务集群-科技专题服务算法库测试用例（政策焦点识别 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=policy.focus` · `catalog_page_id=policy.focus` · path `#/policy/focus`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.focus`  
> **A 线对照**：`fp-split-by-api-run/work/L35.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批9）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 焦点识别 | policy.focus.main | unavailable |

三个查询参数均可选：`policy_id`、`region_code`、`limit`。主流程取全参：`policy_id`、`region_code` 对齐 sampleResponse 首条 `POL_SZ_IC` / `440300`，`limit` 对齐 sampleRequest 的 `20`（params.example 为 100，以 sampleRequest 为准）。catalog `status=unavailable`，仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00602**～**FUNC-00610**，共 **9** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.focus`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00602 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 政策焦点识别 | 焦点识别 | 验证焦点识别功能，检查填写 chainId=INB1701 policy_id、region_code、limit 全参查询后返回焦点字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、policy_id=POL_SZ_IC；region_code=440300；limit=20 | 1.侧栏进入「政策分析」→「政策焦点识别」；2.切换至「算法测试」tab；3.接口下拉选择「焦点识别」；4.填写 policy_id=POL_SZ_IC、region_code=440300、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 policy_id（string）、region_code（string）、focus_score（number，responseFields 焦点指数）、relation_degree（number）、opportunity_cnt（number）；3、元素含 ext 对象及其中 title（string）；4、结构与 sampleResponse 一致，示例含 POL_SZ_IC、region_code=440300、focus_score=88.6、relation_degree=0.72、opportunity_cnt=6、ext.title=深圳市加快集成电路产业发展若干措施，以及 POL_GD_AI（440000、84.1、0.66、5、广东省推动人工智能产业发展行动方案）、POL_BJ_BIO（110000、81.3、0.61、4、北京市生物医药产业促进办法） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_FOCUS_INDEX | INTEG |  | FUNC-00602 | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00603 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 政策焦点识别 | 焦点识别 | 验证焦点识别功能，检查不传可选 policy_id、region_code 与 limit 保持文档合法值时仍返回焦点字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region_code=440300；limit=20 | 1.侧栏进入「政策分析」→「政策焦点识别」；2.切换至「算法测试」tab；3.接口下拉选择「焦点识别」；4.不传 policy_id，填写 region_code=440300、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 policy_id（string）、region_code（string）、focus_score（number）、relation_degree（number）、opportunity_cnt（number）及 ext.title（string）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_FOCUS_INDEX | INTEG |  | FUNC-00603 | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00604 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 政策焦点识别 | 焦点识别 | 验证焦点识别功能，检查不传可选 region_code、policy_id 与 limit 保持文档合法值时仍返回焦点字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、policy_id=POL_SZ_IC；limit=20 | 1.侧栏进入「政策分析」→「政策焦点识别」；2.切换至「算法测试」tab；3.接口下拉选择「焦点识别」；4.不传 region_code，填写 policy_id=POL_SZ_IC、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 policy_id（string）、region_code（string）、focus_score（number）、relation_degree（number）、opportunity_cnt（number）及 ext.title（string）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_FOCUS_INDEX | INTEG |  | FUNC-00604 | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00605 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 政策焦点识别 | 焦点识别 | 验证焦点识别功能，检查不传可选 limit、policy_id 与 region_code 保持文档合法值时仍返回焦点字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、policy_id=POL_SZ_IC；region_code=440300 | 1.侧栏进入「政策分析」→「政策焦点识别」；2.切换至「算法测试」tab；3.接口下拉选择「焦点识别」；4.不传 limit，填写 policy_id=POL_SZ_IC、region_code=440300，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 policy_id（string）、region_code（string）、focus_score（number）、relation_degree（number）、opportunity_cnt（number）及 ext.title（string）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus | M_POLICY_FOCUS_INDEX | INTEG |  | FUNC-00605 | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-04 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00606 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 政策焦点识别 | 焦点识别 | 验证焦点识别功能，检查 policy_id 非法、其余参数保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region_code=440300；limit=20 | 1.侧栏进入「政策分析」→「政策焦点识别」；2.切换至「算法测试」tab；3.接口下拉选择「焦点识别」；4.填写 policy_id=__invalid__、region_code=440300、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 policy_id 非法；2、不返回含 focus_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus |  | INTEG |  | FUNC-00606 | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-05 场景=异常-入参-非法policy_id catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00607 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 政策焦点识别 | 焦点识别 | 验证焦点识别功能，检查 region_code 非法、其余参数保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、policy_id=POL_SZ_IC；limit=20 | 1.侧栏进入「政策分析」→「政策焦点识别」；2.切换至「算法测试」tab；3.接口下拉选择「焦点识别」；4.填写 policy_id=POL_SZ_IC、region_code=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 region_code 非法；2、不返回含 focus_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus |  | INTEG |  | FUNC-00607 | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-06 场景=异常-入参-非法region_code catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00608 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 政策焦点识别 | 焦点识别 | 验证焦点识别功能，检查 limit 非法、其余参数保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、policy_id=POL_SZ_IC；region_code=440300 | 1.侧栏进入「政策分析」→「政策焦点识别」；2.切换至「算法测试」tab；3.接口下拉选择「焦点识别」；4.填写 policy_id=POL_SZ_IC、region_code=440300、limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 focus_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus |  | INTEG |  | FUNC-00608 | endpoint_id=policy.focus.main catalog_page_id=policy.focus 组合=FOC-07 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00609 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 政策焦点识别 | 接口信息 | 验证政策焦点识别的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「政策焦点识别」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「焦点识别」；3、核对概览区标题、method（GET）、path（/policy/v1/policy/analysis/focus）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus |  | INTEG |  | FUNC-00609 | catalog_page_id=policy.focus 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00610 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 政策焦点识别 | 算法测试 | 验证政策焦点识别的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「政策焦点识别」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /policy/v1/policy/analysis/focus；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「焦点识别」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /policy/v1/policy/analysis/focus，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus |  | INTEG |  | FUNC-00610 | catalog_page_id=policy.focus 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| FOC-01 | policy.focus.main | policy_id=POL_SZ_IC；region_code=440300；limit=20 | 主路径全参（sampleResponse 首条标识 + sampleRequest.limit） |
| FOC-02 | policy.focus.main | 不传 policy_id；region_code=440300；limit=20 | 省略可选 policy_id |
| FOC-03 | policy.focus.main | policy_id=POL_SZ_IC；不传 region_code；limit=20 | 省略可选 region_code |
| FOC-04 | policy.focus.main | policy_id=POL_SZ_IC；region_code=440300；不传 limit | 省略可选 limit |
| FOC-05 | policy.focus.main | policy_id=__invalid__；region_code=440300；limit=20 | 只破坏 policy_id |
| FOC-06 | policy.focus.main | policy_id=POL_SZ_IC；region_code=__invalid__；limit=20 | 只破坏 region_code |
| FOC-07 | policy.focus.main | policy_id=POL_SZ_IC；region_code=440300；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 焦点识别 | policy.focus.main | GET | /policy/v1/policy/analysis/focus | policy_id?；region_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.focus.main | FUNC-00602、00603、00604、00605、00606、00607、00608 |
| （页面清单） | FUNC-00609、00610 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「焦点识别」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-00602）
- [x] 有参接口：sample 全参 1 条主流程；每个可选参数单独省略 1 条备选（00603～00605）；每个可选参数 1 条非法反向（00606～00608）
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L35（政策焦点识别模型 / 焦点识别）填写
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00602～00610

**统计**：catalog endpoint **1**；title **1**；FUNC 用例 **9** 条；主流程 **1**、备选 **3**、反向 **3**、清单 **2**；编号闭区间 **FUNC-00602**～**FUNC-00610**（R3-批9 policy.focus）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **9** |
| 编号闭区间 | **FUNC-00602**～**FUNC-00610** |
| 接口向（不含清单） | **7** |
| 主流程 | **1** |
| 备选-参数组合 | **3** |
| 反向 | **3** |
| 清单 | **2** |
| 已删 API 册 | `API-政策焦点识别-用例.md`（API-01402～01408 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
