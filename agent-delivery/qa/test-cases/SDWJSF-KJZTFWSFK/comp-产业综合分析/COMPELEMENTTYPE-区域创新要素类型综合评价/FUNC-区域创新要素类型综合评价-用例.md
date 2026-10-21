# 智能服务集群-科技专题服务算法库测试用例（区域创新要素类型综合评价 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=comp.element-type` · `catalog_page_id=comp.element-type` · path `/industry-comp/element-type`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.element-type`  
> **A 线对照**：`fp-split-by-api-run/work/L56.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 ELEM-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 要素类型 | comp.element-type.main |

可选参数只有 `region`（区域编码，example `440300`，`required=false`）。`sampleRequest` 含 `region=440300`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`。反向恰好 1 条：`region=__invalid__`。catalog `status=unavailable`，备注注明未交付，仍按该接口 sampleResponse 编写。path 为 `GET /comp/v1/comp/element-type`，与同模块其它 `element-*` / `region-*` path 分开验收。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01055**～**FUNC-01059**，共 **5** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.element-type`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01055 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素类型综合评价模型 | 区域创新要素类型综合评价 | 要素类型 | 验证要素类型功能，检查填写 sampleRequest 所示参数 传 region=440300 后返回类型综合分与七维要素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300 | 1.侧栏进入「产业综合分析」→「区域创新要素类型综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「要素类型」；4.填写 region=440300，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：index（number，responseFields 类型综合分，示例 73.5）、cov（string，示例 6/7）、weak（number，示例 2）、rank（number，示例 4）；2、radar 为数组，元素含人才（number，示例 79）、企业（number，示例 84）、政策（number，示例 81）、服务机构（number，示例 70）、科研机构（number，示例 66）、资金（number，示例 73）、空间（number，示例 61）；3、bar_items 为数组，元素含 name（string）、value（number），示例企业 84、政策 81、人才 79、资金 73、服务 70、科研 66、空间 61；4、pie_items 为数组，元素含 name（string）、value（number），示例强 3、中 2、弱 2；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例企业/84/1/强/链主与专精特新密集、政策/81/2/强/工具箱完善、空间/61/7/弱/载体饱和度偏高 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-type | M_SYNTH_ELEM_TYPE_INDEX | INTEG |  |  | endpoint_id=comp.element-type.main catalog_page_id=comp.element-type 组合=ELEM-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01056 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素类型综合评价模型 | 区域创新要素类型综合评价 | 要素类型 | 验证要素类型功能，检查不传可选 region（与 sample 相反）时仍返回类型综合分与七维要素字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region | 1.侧栏进入「产业综合分析」→「区域创新要素类型综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「要素类型」；4.不传 region，点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：index（number，responseFields 类型综合分，示例 73.5）、cov（string，示例 6/7）、weak（number，示例 2）、rank（number，示例 4）；2、radar 为数组，元素含人才（number，示例 79）、企业（number，示例 84）、政策（number，示例 81）、服务机构（number，示例 70）、科研机构（number，示例 66）、资金（number，示例 73）、空间（number，示例 61）；3、bar_items 为数组，元素含 name（string）、value（number），示例企业 84、政策 81、人才 79、资金 73、服务 70、科研 66、空间 61；4、pie_items 为数组，元素含 name（string）、value（number），示例强 3、中 2、弱 2；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例企业/84/1/强/链主与专精特新密集、政策/81/2/强/工具箱完善、空间/61/7/弱/载体饱和度偏高 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-type | M_SYNTH_ELEM_TYPE_INDEX | INTEG |  |  | endpoint_id=comp.element-type.main catalog_page_id=comp.element-type 组合=ELEM-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01057 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素类型综合评价模型 | 区域创新要素类型综合评价 | 要素类型 | 验证要素类型功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、无其它查询参数 | 1.侧栏进入「产业综合分析」→「区域创新要素类型综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「要素类型」；4.填写 region=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-type |  | INTEG |  |  | endpoint_id=comp.element-type.main catalog_page_id=comp.element-type 组合=ELEM-03 场景=异常-入参-非法region catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01058 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素类型综合评价模型 | 区域创新要素类型综合评价 | 接口信息 | 验证区域创新要素类型综合评价的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域创新要素类型综合评价」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「要素类型」；3、核对概览区标题、method（GET）、path（/comp/v1/comp/element-type）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-type |  | INTEG |  |  | catalog_page_id=comp.element-type 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01059 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素类型综合评价模型 | 区域创新要素类型综合评价 | 算法测试 | 验证区域创新要素类型综合评价的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域创新要素类型综合评价」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /comp/v1/comp/element-type；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「要素类型」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /comp/v1/comp/element-type，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-type |  | INTEG |  |  | catalog_page_id=comp.element-type 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ELEM-01 | comp.element-type.main | region=440300 | 主路径（sampleRequest） |
| ELEM-02 | comp.element-type.main | 不传 region | 省略可选 region（与 sample 相反） |
| ELEM-03 | comp.element-type.main | region=__invalid__ | 只破坏 region |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 要素类型 | comp.element-type.main | GET | /comp/v1/comp/element-type | region? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.element-type.main | FUNC-01055、01056、01057 |
| （页面清单） | FUNC-01058、01059 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「要素类型」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-01055，组合 ELEM-01 金样）
- [x] 有参接口：sampleRequest 主流程 1 条；与 sample 相反不传 region 1 条备选；region 恰好 1 条非法反向
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 产业综合分析模型构建 / 区域创新要素类型综合评价模型（L56）
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-01055～01059；A 线 `work/L56.md` 未改

**统计**：接口 **1**；主流程 **1**；备选 **1**；反向 **1**；清单 **2**；合计 **5** 条；编号闭区间 **FUNC-01055**～**FUNC-01059**（父控 R3 返工 · comp.element-type 分配）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **FUNC-01055**～**FUNC-01059** |
| 接口向（不含清单） | **3** |
| 清单 | **2** |
| 主流程 | **1**（FUNC-01055 · ELEM-01 金样） |
| 备选-参数组合 | **1**（FUNC-01056） |
| 反向 | **1**（FUNC-01057） |
| catalog_page_id | `comp.element-type` |
| endpoint 数 | **1**（`comp.element-type.main`） |
| 已删 API 册 | `API-区域创新要素类型综合评价-用例.md`（API-01805～01807 作废，不复用） |
| 鉴权用例 | **0** |
