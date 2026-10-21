# 智能服务集群-科技专题服务算法库测试用例（风险评分 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=entan.risk` · `catalog_page_id=entan.risk` · path `#/entan/risk`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.risk`  
> **A 线对照**：无对应 Lxx（工程增强，非 60 六级；`_l6-to-catalog-map.yaml` catalog_skip `entan.risk`；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批4；金样 CHAINBASIC）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 风险评分 | entan.risk.list |

`level`、`limit` 均为可选。主路径取 `sampleRequest`：`level` 空串（选项「全部」）、`limit`=200。catalog `status=unavailable`，仍按文档请求与返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00309**～**FUNC-00315**，共 **7** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.risk`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00309 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险评分 | 风险评分 | 验证风险评分功能，检查填写 sampleRequest 所示参数 传 level 空串、limit=200 后返回风险列表字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「风险评分」；2.切换至「算法测试」tab；3.接口下拉选择「风险评分」；4.填写 level=""（sampleRequest空串，选项全部）、limit=200，点击调用 | 1、返回面板含 rows（array，responseFields 风险列表）；2、元素含 enterprise_name（string）、risk_score（number）、risk_level（string）、shixin_count（number）、abnormal_count（number）、punish_count（number）；3、与 sampleResponse 一致：南山智造有限公司 enterprise_name、risk_score=68、risk_level=高、shixin_count=1、abnormal_count=2、punish_count=3；深湾算法有限公司 risk_score=41、risk_level=中、shixin_count=0、abnormal_count=1、punish_count=1；云启智元科技股份有限公司 risk_score=18、risk_level=低、shixin_count=0、abnormal_count=0、punish_count=0 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk |  | INTEG |  |  | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00310 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险评分 | 风险评分 | 验证风险评分功能，检查省略可选 level、仅传 limit=200 时仍返回风险列表字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「风险评分」；2.切换至「算法测试」tab；3.接口下拉选择「风险评分」；4.不传 level，填写 limit=200，点击调用 | 1、返回面板含 rows（array，responseFields 风险列表）；2、元素仍含 enterprise_name（string）、risk_score（number）、risk_level（string）、shixin_count（number）、abnormal_count（number）、punish_count（number）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk |  | INTEG |  |  | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00311 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险评分 | 风险评分 | 验证风险评分功能，检查传 level 空串、省略可选 limit 时仍返回风险列表字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「风险评分」；2.切换至「算法测试」tab；3.接口下拉选择「风险评分」；4.不传 limit，填写 level=""，点击调用 | 1、返回面板含 rows（array，responseFields 风险列表）；2、元素仍含 enterprise_name（string）、risk_score（number）、risk_level（string）、shixin_count（number）、abnormal_count（number）、punish_count（number）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk |  | INTEG |  |  | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00312 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险评分 | 风险评分 | 验证风险评分功能，检查 level 取枚举外非法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「风险评分」；2.切换至「算法测试」tab；3.接口下拉选择「风险评分」；4.填写 level=__invalid_level__、limit=200，点击调用 | 1、返回面板的 message 或 msg 指出 level 非法；2、不返回含 risk_score、risk_level 的成功业务 rows | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk |  | INTEG |  |  | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-04 场景=异常-入参-非法level catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00313 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险评分 | 风险评分 | 验证风险评分功能，检查 limit 取非整数非法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「风险评分」；2.切换至「算法测试」tab；3.接口下拉选择「风险评分」；4.填写 level=""、limit=not_a_number，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 risk_score 的成功业务 rows | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk |  | INTEG |  |  | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-05 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00314 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险评分 | 接口信息 | 验证风险评分的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「风险评分」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「风险评分」；3、核对概览区标题、method（GET）、path（/entan/v1/risk）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk |  | INTEG |  |  | catalog_page_id=entan.risk 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00315 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 风险评分 | 算法测试 | 验证风险评分的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「风险评分」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /entan/v1/risk；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「风险评分」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /entan/v1/risk，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk |  | INTEG |  |  | catalog_page_id=entan.risk 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RISK-01 | entan.risk.list | level=""（sampleRequest 空串，选项全部）；limit=200 | 主路径全参（sampleRequest） |
| RISK-02 | entan.risk.list | 不传 level；limit=200 | 省略可选 level |
| RISK-03 | entan.risk.list | level=""；不传 limit | 省略可选 limit |
| RISK-04 | entan.risk.list | level=__invalid_level__；limit=200 | 只破坏 level |
| RISK-05 | entan.risk.list | level=""；limit=not_a_number | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 风险评分 | entan.risk.list | GET | /entan/v1/risk | level?；limit? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.risk.list | FUNC-00309、00310、00311、00312、00313 |
| （页面清单） | FUNC-00314、00315 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「风险评分」在功能点列出现且有 ≥1 条 `场景=主流程`
- [x] 有参接口：sampleRequest 全参 1 条主流程；省略 level、省略 limit 各 1 条备选；level、limit 各 1 条非法反向
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 待挂需规 / 待挂需规（catalog_skip 工程增强）
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00309～00315

**统计**：接口 **1**；主流程 **1**；备选 **2**；反向 **2**；清单 **2**；合计 **7** 条；编号闭区间 **FUNC-00309**～**FUNC-00315**（父控 R3-批4 分配）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **7** |
| 编号闭区间 | **FUNC-00309**～**FUNC-00315** |
| 接口向（不含清单） | **5** |
| 主流程 | **1** |
| 备选-参数组合 | **2** |
| 反向 | **2** |
| 清单 | **2** |
| 已删 API 册 | `API-风险评分-用例.md`（API-01134～01138 作废，不复用） |
| 鉴权用例 | **0** |
