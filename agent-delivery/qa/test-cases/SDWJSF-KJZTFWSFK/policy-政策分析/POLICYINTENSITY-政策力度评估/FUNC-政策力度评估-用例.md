# 智能服务集群-科技专题服务算法库测试用例（政策力度评估 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=policy.intensity` · `catalog_page_id=policy.intensity` · path `#/policy/intensity`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.intensity`  
> **A 线对照**：`fp-split-by-api-run/work/L36.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批10）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 力度评估 | policy.intensity.main | unavailable |

三个查询参数均可选：`scope_type`、`scope_code`、`limit`。主流程取 `sampleRequest`：`scope_type=province`、`limit=20`，不传 `scope_code`。备选各动一个参数，与 sample 相反：不传 `scope_type`、传入 `scope_code=440000`（参数说明示例）、不传 `limit`。反向各 1 条非法，不把省略写成反向。catalog `status=unavailable`，仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00623**～**FUNC-00631**，共 **9** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.intensity`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00623 | 算法工具库 | 科技专题服务算法库 | 政策力度评估模型 | 力度评估 | 政策力度评估 | 力度评估 | 验证力度评估功能，检查填写 sampleRequest 所示参数 传 scope_type=province、limit=20、不传 scope_code 后返回力度字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_type=province；limit=20；不传 scope_code | 1.侧栏进入「政策分析」→「政策力度评估」；2.切换至「算法测试」tab；3.接口下拉选择「力度评估」；4.不传 scope_code，填写 scope_type=province、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 rank_no（number）、scope_type（string）、scope_code（string）、scope_name（string）、intensity_index（number，responseFields 力度指数）、industry_coverage（number）；3、与 sampleResponse 逐字段一致，示例第1条 rank_no=1、scope_type=policy、scope_code=POL_IC_EU、scope_name=欧盟芯片法案配套实施细则、intensity_index=91.2、industry_coverage=72.5，第2条 rank_no=2、scope_type=policy、scope_code=POL_SZ_IC、scope_name=深圳市加快集成电路产业发展若干措施、intensity_index=88.6、industry_coverage=69.8，第3条 rank_no=3、scope_type=province、scope_code=440000、scope_name=广东省、intensity_index=87.3、industry_coverage=76.2 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | M_POLICY_INTENSITY_INDEX | INTEG |  |  | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00624 | 算法工具库 | 科技专题服务算法库 | 政策力度评估模型 | 力度评估 | 政策力度评估 | 力度评估 | 验证力度评估功能，检查不传可选 scope_type、limit 保持 sample 的 20、不传 scope_code 时仍返回力度字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 scope_code | 1.侧栏进入「政策分析」→「政策力度评估」；2.切换至「算法测试」tab；3.接口下拉选择「力度评估」；4.不传 scope_type、不传 scope_code，填写 limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 rank_no（number）、scope_type（string）、scope_code（string）、scope_name（string）、intensity_index（number）、industry_coverage（number）；3、结构与 sampleResponse 同类，示例值（如 intensity_index=91.2、industry_coverage=72.5）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | M_POLICY_INTENSITY_INDEX | INTEG |  |  | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00625 | 算法工具库 | 科技专题服务算法库 | 政策力度评估模型 | 力度评估 | 政策力度评估 | 力度评估 | 验证力度评估功能，检查传入可选 scope_code=440000、scope_type 与 limit 保持 sample 时仍返回力度字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_type=province；scope_code=440000；limit=20 | 1.侧栏进入「政策分析」→「政策力度评估」；2.切换至「算法测试」tab；3.接口下拉选择「力度评估」；4.填写 scope_type=province、scope_code=440000、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 rank_no（number）、scope_type（string）、scope_code（string）、scope_name（string）、intensity_index（number）、industry_coverage（number）；3、结构与 sampleResponse 同类，示例值（如 intensity_index=91.2、industry_coverage=72.5）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | M_POLICY_INTENSITY_INDEX | INTEG |  |  | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00626 | 算法工具库 | 科技专题服务算法库 | 政策力度评估模型 | 力度评估 | 政策力度评估 | 力度评估 | 验证力度评估功能，检查不传可选 limit、scope_type 保持 sample 的 province、不传 scope_code 时仍返回力度字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_type=province；不传 scope_code | 1.侧栏进入「政策分析」→「政策力度评估」；2.切换至「算法测试」tab；3.接口下拉选择「力度评估」；4.不传 scope_code、不传 limit，填写 scope_type=province，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 rank_no（number）、scope_type（string）、scope_code（string）、scope_name（string）、intensity_index（number）、industry_coverage（number）；3、结构与 sampleResponse 同类，示例值（如 intensity_index=91.2、industry_coverage=72.5）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | M_POLICY_INTENSITY_INDEX | INTEG |  |  | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-04 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00627 | 算法工具库 | 科技专题服务算法库 | 政策力度评估模型 | 力度评估 | 政策力度评估 | 力度评估 | 验证力度评估功能，检查 scope_type 非法、其余参数保持 sample 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 scope_code | 1.侧栏进入「政策分析」→「政策力度评估」；2.切换至「算法测试」tab；3.接口下拉选择「力度评估」；4.不传 scope_code，填写 scope_type=__invalid__（不在province、policy、空）、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scope_type 非法；2、不返回含 intensity_index 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity |  | INTEG |  |  | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-05 场景=异常-入参-非法scope_type catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00628 | 算法工具库 | 科技专题服务算法库 | 政策力度评估模型 | 力度评估 | 政策力度评估 | 力度评估 | 验证力度评估功能，检查 scope_code 非法、其余参数保持 sample 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_type=province；limit=20 | 1.侧栏进入「政策分析」→「政策力度评估」；2.切换至「算法测试」tab；3.接口下拉选择「力度评估」；4.填写 scope_type=province、scope_code=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scope_code 非法；2、不返回含 intensity_index 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity |  | INTEG |  |  | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-06 场景=异常-入参-非法scope_code catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00629 | 算法工具库 | 科技专题服务算法库 | 政策力度评估模型 | 力度评估 | 政策力度评估 | 力度评估 | 验证力度评估功能，检查 limit 非法、其余参数保持 sample 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_type=province；不传 scope_code | 1.侧栏进入「政策分析」→「政策力度评估」；2.切换至「算法测试」tab；3.接口下拉选择「力度评估」；4.不传 scope_code，填写 scope_type=province、limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 intensity_index 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity |  | INTEG |  |  | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-07 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00630 | 算法工具库 | 科技专题服务算法库 | 政策力度评估模型 | 力度评估 | 政策力度评估 | 接口信息 | 验证政策力度评估的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「政策力度评估」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「力度评估」；3、核对概览区标题、method（GET）、path（/policy/v1/policy/analysis/intensity）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity |  | INTEG |  |  | catalog_page_id=policy.intensity 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00631 | 算法工具库 | 科技专题服务算法库 | 政策力度评估模型 | 力度评估 | 政策力度评估 | 算法测试 | 验证政策力度评估的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「政策力度评估」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /policy/v1/policy/analysis/intensity；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「力度评估」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /policy/v1/policy/analysis/intensity，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity |  | INTEG |  |  | catalog_page_id=policy.intensity 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| INT-01 | policy.intensity.main | scope_type=province；不传 scope_code；limit=20 | 主路径（sampleRequest） |
| INT-02 | policy.intensity.main | 不传 scope_type；不传 scope_code；limit=20 | 省略可选 scope_type（sample 含 scope_type） |
| INT-03 | policy.intensity.main | scope_type=province；scope_code=440000；limit=20 | 传入可选 scope_code（sample 不含 scope_code；440000 取参数说明示例） |
| INT-04 | policy.intensity.main | scope_type=province；不传 scope_code；不传 limit | 省略可选 limit（sample 含 limit） |
| INT-05 | policy.intensity.main | scope_type=__invalid__（不在 province、policy、空）；不传 scope_code；limit=20 | 只破坏 scope_type |
| INT-06 | policy.intensity.main | scope_type=province；scope_code=__invalid__；limit=20 | 只破坏 scope_code |
| INT-07 | policy.intensity.main | scope_type=province；不传 scope_code；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 力度评估 | policy.intensity.main | GET | /policy/v1/policy/analysis/intensity | scope_type?；scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.intensity.main | FUNC-00623、00624、00625、00626、00627、00628、00629 |
| （页面清单） | FUNC-00630、00631 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「力度评估」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-00623）
- [x] 有参接口：sample 主路径 1 条主流程；每个可选参数单独省略或相反传参 1 条备选（00624～00626）；每个可选参数 1 条非法反向（00627～00629）
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L36（政策力度评估模型 / 力度评估）填写
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00623～00631

**统计**：catalog endpoint **1**；title **1**；FUNC 用例 **9** 条；主流程 **1**、备选 **3**、反向 **3**、清单 **2**；编号闭区间 **FUNC-00623**～**FUNC-00631**（R3-批10 policy.intensity）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **9** |
| 编号闭区间 | **FUNC-00623**～**FUNC-00631** |
| 接口向（不含清单） | **7** |
| 主流程 | **1** |
| 备选-参数组合 | **3** |
| 反向 | **3** |
| 清单 | **2** |
| 已删 API 册 | `API-政策力度评估-用例.md`（API-01419～01425 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
