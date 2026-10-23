# 智能服务集群-科技专题服务算法库测试用例（条件保障力 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=policy.guard` · `catalog_page_id=policy.guard` · path `#/policy/guard`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.guard`  
> **A 线对照**：**无对应 Lxx**（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.guard`，原因：不扩六级；不改 `work/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批12）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 保障力 | policy.guard.main | unavailable |

两个查询参数均可选：`scope_code`、`limit`。主流程对齐 `sampleRequest`：只传 `limit=20`，不传 `scope_code`。`scope_code` 的合法补传值取参数说明中的省/市编码示例 `440000`。catalog `status=unavailable`，仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00732**～**FUNC-00738**，共 **7** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.guard`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00732 | 算法工具库 | 科技专题服务算法库 | 条件保障力模型 | 保障力 | 条件保障力 | 保障力 | 验证保障力功能，检查填写 sampleRequest 所示参数 只传 limit=20、不传 scope_code 时返回保障力字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 scope_code | 1.侧栏进入「政策分析」→「条件保障力」；2.切换至「算法测试」tab；3.接口下拉选择「保障力」；4.不传 scope_code，填写 limit=20，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：model_id（string，示例 guard）、count（number，示例 1）；2、rows 为数组（responseFields 组合分行）；3、rows 元素含 scope_name（string，示例 广东省）、effect_score（number，示例 68.1）、metric_id（string，示例 M_POLICY_DS_07_POLICY_GUARD_008） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | M_POLICY_DS_07_POLICY_GUARD_008 | INTEG |  | FUNC-00732 | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00733 | 算法工具库 | 科技专题服务算法库 | 条件保障力模型 | 保障力 | 条件保障力 | 保障力 | 验证保障力功能，检查补传可选 scope_code=440000、limit 保持文档示例 20 时仍返回保障力字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440000；limit=20 | 1.侧栏进入「政策分析」→「条件保障力」；2.切换至「算法测试」tab；3.接口下拉选择「保障力」；4.填写 scope_code=440000、limit=20，点击调用 | 1、返回面板 body 为对象；2、仍含 model_id（string，示例 guard）、count（number，示例 1）；3、rows 为数组（responseFields 组合分行），元素含 scope_name（string，示例 广东省）、effect_score（number，示例 68.1）、metric_id（string，示例 M_POLICY_DS_07_POLICY_GUARD_008），与 sampleResponse 逐字段同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | M_POLICY_DS_07_POLICY_GUARD_008 | INTEG |  | FUNC-00733 | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00734 | 算法工具库 | 科技专题服务算法库 | 条件保障力模型 | 保障力 | 条件保障力 | 保障力 | 验证保障力功能，检查不传可选 limit、scope_code 保持主路径不传时仍返回保障力字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 scope_code；不传 limit | 1.侧栏进入「政策分析」→「条件保障力」；2.切换至「算法测试」tab；3.接口下拉选择「保障力」；4.不传 scope_code、不传 limit，点击调用 | 1、返回面板 body 为对象；2、仍含 model_id（string，示例 guard）、count（number，示例 1）；3、rows 为数组（responseFields 组合分行），元素含 scope_name（string，示例 广东省）、effect_score（number，示例 68.1）、metric_id（string，示例 M_POLICY_DS_07_POLICY_GUARD_008），与 sampleResponse 逐字段同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | M_POLICY_DS_07_POLICY_GUARD_008 | INTEG |  | FUNC-00734 | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00735 | 算法工具库 | 科技专题服务算法库 | 条件保障力模型 | 保障力 | 条件保障力 | 保障力 | 验证保障力功能，检查 scope_code 非法、limit 保持文档合法值 20 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20 | 1.侧栏进入「政策分析」→「条件保障力」；2.切换至「算法测试」tab；3.接口下拉选择「保障力」；4.填写 scope_code=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scope_code 非法；2、不返回含 effect_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard |  | INTEG |  | FUNC-00735 | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-04 场景=异常-入参-非法scope_code catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00736 | 算法工具库 | 科技专题服务算法库 | 条件保障力模型 | 保障力 | 条件保障力 | 保障力 | 验证保障力功能，检查 limit 非法、scope_code 保持主路径不传时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 scope_code | 1.侧栏进入「政策分析」→「条件保障力」；2.切换至「算法测试」tab；3.接口下拉选择「保障力」；4.不传 scope_code，填写 limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 effect_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard |  | INTEG |  | FUNC-00736 | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GRD-05 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00737 | 算法工具库 | 科技专题服务算法库 | 条件保障力模型 | 保障力 | 条件保障力 | 接口信息 | 验证条件保障力的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「条件保障力」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「保障力」；3、核对概览区标题、method（GET）、path（/policy/v1/policy/analysis/guard）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard |  | INTEG |  | FUNC-00737 | catalog_page_id=policy.guard 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00738 | 算法工具库 | 科技专题服务算法库 | 条件保障力模型 | 保障力 | 条件保障力 | 算法测试 | 验证条件保障力的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「条件保障力」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /policy/v1/policy/analysis/guard；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「保障力」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /policy/v1/policy/analysis/guard，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard |  | INTEG |  | FUNC-00738 | catalog_page_id=policy.guard 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GRD-01 | policy.guard.main | 不传 scope_code；limit=20 | 主路径（sampleRequest） |
| GRD-02 | policy.guard.main | scope_code=440000；limit=20 | 只补传可选 scope_code（说明示例 440000） |
| GRD-03 | policy.guard.main | 不传 scope_code；不传 limit | 只省略可选 limit |
| GRD-04 | policy.guard.main | scope_code=__invalid__；limit=20 | 只破坏 scope_code |
| GRD-05 | policy.guard.main | 不传 scope_code；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 保障力 | policy.guard.main | GET | /policy/v1/policy/analysis/guard | scope_code?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.guard.main | FUNC-00732、00733、00734、00735、00736 |
| （页面清单） | FUNC-00737、00738 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「保障力」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-00732）
- [x] 有参接口：sampleRequest 主流程 1 条；scope_code 补传 1 条、limit 省略 1 条；每个可选参数 1 条非法反向（00735、00736）
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 五级/六级按 catalog 页（条件保障力模型 / 保障力）填写；A 线无 Lxx
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00732～00738

**统计**：catalog endpoint **1**；title **1**；FUNC 用例 **7** 条；主流程 **1**、备选 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00732**～**FUNC-00738**（R3-批12 policy.guard）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **7** |
| 编号闭区间 | **FUNC-00732**～**FUNC-00738** |
| 接口向（不含清单） | **5** |
| 主流程 | **1** |
| 备选-参数组合 | **2** |
| 反向 | **2** |
| 清单 | **2** |
| 已删 API 册 | `API-条件保障力-用例.md`（API-01508～01512 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
