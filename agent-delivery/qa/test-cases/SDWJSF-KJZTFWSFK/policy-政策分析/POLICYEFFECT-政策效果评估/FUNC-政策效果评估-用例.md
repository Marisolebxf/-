# 智能服务集群-科技专题服务算法库测试用例（政策效果评估 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=policy.effect` · `catalog_page_id=policy.effect` · path `#/policy/effect`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.effect`  
> **A 线对照**：`fp-split-by-api-run/work/L37.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批10）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 效果评估 | policy.effect.main | unavailable |

两个查询参数均可选：`scope_code`、`limit`。主流程对齐 sampleRequest：仅传 `limit=20`、不传 `scope_code`（params 说明 scope_code 示例为 440000，以 sampleRequest 为准）。catalog `status=unavailable`，仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00632**～**FUNC-00638**，共 **7** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.effect`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00632 | 算法工具库 | 科技专题服务算法库 | 政策效果评估模型 | 效果评估 | 政策效果评估 | 效果评估 | 验证效果评估功能，检查填写 sampleRequest 所示参数 仅传 limit=20、不传 scope_code 后返回效果字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20 | 1.侧栏进入「政策分析」→「政策效果评估」；2.切换至「算法测试」tab；3.接口下拉选择「效果评估」；4.不传 scope_code，填写 limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 scope_name（string）、scope_code（string）、effect_score（number，responseFields 效果评分）、impl_effect（number）；3、结构与 sampleResponse 一致，示例含深圳市/440300/effect_score 82.4/impl_effect 71.2，广东省/440000/79.1/68.6，北京市/110000/77.8/66 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect | M_POLICY_EFFECT_SCORE | INTEG |  |  | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00633 | 算法工具库 | 科技专题服务算法库 | 政策效果评估模型 | 效果评估 | 政策效果评估 | 效果评估 | 验证效果评估功能，检查补传可选 scope_code=440000 且 limit 保持 20 时仍返回效果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440000；limit=20 | 1.侧栏进入「政策分析」→「政策效果评估」；2.切换至「算法测试」tab；3.接口下拉选择「效果评估」；4.填写 scope_code=440000（params说明「如440000」）、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 scope_name（string）、scope_code（string）、effect_score（number，responseFields 效果评分）、impl_effect（number）；3、字段结构与 sampleResponse 一致（示例含深圳市 82.4/71.2、广东省 79.1/68.6、北京市 77.8/66） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect | M_POLICY_EFFECT_SCORE | INTEG |  |  | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00634 | 算法工具库 | 科技专题服务算法库 | 政策效果评估模型 | 效果评估 | 政策效果评估 | 效果评估 | 验证效果评估功能，检查仅传 scope_code=440000、不传可选 limit 时仍返回效果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440000 | 1.侧栏进入「政策分析」→「政策效果评估」；2.切换至「算法测试」tab；3.接口下拉选择「效果评估」；4.不传 limit，填写 scope_code=440000，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 scope_name（string）、scope_code（string）、effect_score（number，responseFields 效果评分）、impl_effect（number）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect | M_POLICY_EFFECT_SCORE | INTEG |  |  | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00635 | 算法工具库 | 科技专题服务算法库 | 政策效果评估模型 | 效果评估 | 政策效果评估 | 效果评估 | 验证效果评估功能，检查 scope_code 非法、limit 保持 20 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20 | 1.侧栏进入「政策分析」→「政策效果评估」；2.切换至「算法测试」tab；3.接口下拉选择「效果评估」；4.填写 scope_code=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scope_code 非法；2、不返回含 effect_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect |  | INTEG |  |  | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-04 场景=异常-入参-非法scope_code catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00636 | 算法工具库 | 科技专题服务算法库 | 政策效果评估模型 | 效果评估 | 政策效果评估 | 效果评估 | 验证效果评估功能，检查 limit 非法、不传 scope_code 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「政策效果评估」；2.切换至「算法测试」tab；3.接口下拉选择「效果评估」；4.不传 scope_code，填写 limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 effect_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect |  | INTEG |  |  | endpoint_id=policy.effect.main catalog_page_id=policy.effect 组合=EFF-05 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00637 | 算法工具库 | 科技专题服务算法库 | 政策效果评估模型 | 效果评估 | 政策效果评估 | 接口信息 | 验证政策效果评估的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「政策效果评估」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「效果评估」；3、核对概览区标题、method（GET）、path（/policy/v1/policy/analysis/effect）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect |  | INTEG |  |  | catalog_page_id=policy.effect 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00638 | 算法工具库 | 科技专题服务算法库 | 政策效果评估模型 | 效果评估 | 政策效果评估 | 算法测试 | 验证政策效果评估的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「政策效果评估」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /policy/v1/policy/analysis/effect；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「效果评估」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /policy/v1/policy/analysis/effect，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/effect |  | INTEG |  |  | catalog_page_id=policy.effect 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| EFF-01 | policy.effect.main | 不传 scope_code；limit=20 | 主路径（sampleRequest） |
| EFF-02 | policy.effect.main | scope_code=440000（params 说明「如 440000」）；limit=20 | 单独补传可选 scope_code |
| EFF-03 | policy.effect.main | scope_code=440000；不传 limit | 单独省略可选 limit |
| EFF-04 | policy.effect.main | scope_code=__invalid__；limit=20 | 只破坏 scope_code |
| EFF-05 | policy.effect.main | 不传 scope_code；limit=-1 | 只破坏 limit |

两参数同时都不传不单列：主流程已覆盖「不传 scope_code」，备选 EFF-03 已覆盖「不传 limit」。

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 效果评估 | policy.effect.main | GET | /policy/v1/policy/analysis/effect | scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.effect.main | FUNC-00632、00633、00634、00635、00636 |
| （页面清单） | FUNC-00637、00638 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「效果评估」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-00632）
- [x] 有参接口：sampleRequest 主路径 1 条（仅 limit=20）；单独补传 scope_code、单独省略 limit 各 1 条备选（00633、00634）；scope_code、limit 各 1 条非法反向（00635、00636）
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L37（政策效果评估模型 / 效果评估）填写
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00632～00638

**统计**：catalog endpoint **1**；title **1**；FUNC 用例 **7** 条；主流程 **1**、备选 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00632**～**FUNC-00638**（R3-批10 policy.effect）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **7** |
| 编号闭区间 | **FUNC-00632**～**FUNC-00638** |
| 接口向（不含清单） | **5** |
| 主流程 | **1** |
| 备选-参数组合 | **2** |
| 反向 | **2** |
| 清单 | **2** |
| 已删 API 册 | `API-政策效果评估-用例.md`（API-01426～01430 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
