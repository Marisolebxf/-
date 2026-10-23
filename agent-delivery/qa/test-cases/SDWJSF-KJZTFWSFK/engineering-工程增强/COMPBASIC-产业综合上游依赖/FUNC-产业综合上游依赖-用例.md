# 智能服务集群-科技专题服务算法库测试用例（产业综合上游依赖 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=comp.basic` · `catalog_page_id=comp.basic` · path `/industry-comp/basic`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.basic`  
> **A 线对照**：无对应 Lxx（工程增强，非 60 六级；`_l6-to-catalog-map.yaml` catalog_skip `comp.basic`；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 上游依赖与综合研判 | comp.basic.upstream |

可选参数 1 个：`region`（区域编码，example `440300`）。`sampleRequest` 含 `region=440300`。备选与 sample 相反：不传 `region`。反向恰好 1 条非法 `region`，不把省略写成反向。catalog `status=unavailable`，仍按文档请求与返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00964**～**FUNC-00968**，共 **5** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.basic`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00964 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 产业综合上游依赖 | 上游依赖与综合研判 | 验证上游依赖与综合研判功能，检查填写 sampleRequest 所示参数 传 region=440300 后返回 KPI 与上游七维字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300 | 1.侧栏进入「工程增强」→「产业综合上游依赖」；2.切换至「算法测试」tab；3.接口下拉选择「上游依赖与综合研判」；4.填写 region=440300，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：kpis 为 object（responseFields 活力/要素/协同演示指数），含 vitality（number，示例 76.4）、element（number，示例 71.5）、synergy（number，示例 68.5）；2、upstream 为数组（responseFields 上游七维依赖），元素含 dimension（string）、name（string）、bidSection（string）、menuLabel（string）、ready（boolean）、ready_label（string）；sampleResponse 七条为产业链/产业链基础指标输出/§4.1.1/产业链分析算法库 · 基础指标/true/可消费，技术链/技术基础指标输出/§4.1.2/未挂载算法库/false/待接入，企业/企业基础指标输出/§4.1.3/企业分析算法库 · 基础指标/true/可消费，人才/人才基础指标输出/§4.1.4/未挂载算法库/false/待接入，科研机构/科研机构基础指标输出/§4.1.5/未挂载算法库/false/待接入，政策/政策基础指标输出/§4.1.6/政策分析算法库 · 基础指标/true/可消费，服务机构/服务机构基础指标输出/§4.1.7/产业服务算法库 · 基础指标/true/可消费；3、bar_items 为数组（sampleResponse 多出字段），元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组（sampleResponse 多出字段），元素含 name（string）、value（number），示例活力 40、要素 32、协同 28 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | M_SYNTH_VIT_INDEX | INTEG |  | FUNC-00964 | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=UPD-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00965 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 产业综合上游依赖 | 上游依赖与综合研判 | 验证上游依赖与综合研判功能，检查不传可选 region（与 sample 相反）时仍返回 KPI 与上游七维字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region | 1.侧栏进入「工程增强」→「产业综合上游依赖」；2.切换至「算法测试」tab；3.接口下拉选择「上游依赖与综合研判」；4.不传 region，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 逐字段同类：kpis 为 object，含 vitality（number，示例 76.4）、element（number，示例 71.5）、synergy（number，示例 68.5）；2、upstream 为数组，元素含 dimension、name、bidSection、menuLabel（string）、ready（boolean）、ready_label（string），七条示例与主流程相同（产业链至服务机构，§4.1.1～§4.1.7）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例活力 40、要素 32、协同 28 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | M_SYNTH_VIT_INDEX | INTEG |  | FUNC-00965 | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=UPD-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00966 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 产业综合上游依赖 | 上游依赖与综合研判 | 验证上游依赖与综合研判功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、无其它查询参数 | 1.侧栏进入「工程增强」→「产业综合上游依赖」；2.切换至「算法测试」tab；3.接口下拉选择「上游依赖与综合研判」；4.填写 region=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 kpis.vitality 或 upstream 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps |  | INTEG |  | FUNC-00966 | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=UPD-03 场景=异常-入参-非法region catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00967 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 产业综合上游依赖 | 接口信息 | 验证产业综合上游依赖的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「产业综合上游依赖」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「上游依赖与综合研判」；3、核对概览区标题、method（GET）、path（/comp/v1/comp/upstream-deps）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps |  | INTEG |  | FUNC-00967 | catalog_page_id=comp.basic 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00968 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 产业综合上游依赖 | 算法测试 | 验证产业综合上游依赖的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「产业综合上游依赖」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /comp/v1/comp/upstream-deps；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「上游依赖与综合研判」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /comp/v1/comp/upstream-deps，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps |  | INTEG |  | FUNC-00968 | catalog_page_id=comp.basic 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| UPD-01 | comp.basic.upstream | region=440300 | 主路径（sampleRequest） |
| UPD-02 | comp.basic.upstream | 不传 region | 省略可选 region（与 sample 相反） |
| UPD-03 | comp.basic.upstream | region=__invalid__ | 只破坏 region |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 上游依赖与综合研判 | comp.basic.upstream | GET | /comp/v1/comp/upstream-deps | region? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.basic.upstream | FUNC-00964、00965、00966 |
| （页面清单） | FUNC-00967、00968 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「上游依赖与综合研判」在功能点列出现且有 ≥1 条 `场景=主流程`
- [x] 有参接口：sampleRequest 主流程 1 条；与 sample 相反不传 region 1 条备选；region 恰好 1 条非法反向
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 待挂需规 / 待挂需规（catalog_skip 工程增强）
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00964～00968

**统计**：接口 **1**；主流程 **1**；备选 **1**；反向 **1**；清单 **2**；合计 **5** 条；编号闭区间 **FUNC-00964**～**FUNC-00968**（父控 R3 返工 · comp.basic 分配）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **FUNC-00964**～**FUNC-00968** |
| 接口向（不含清单） | **3** |
| 清单 | **2** |
| 主流程 | **1**（FUNC-00964） |
| 备选-参数组合 | **1**（FUNC-00965） |
| 反向 | **1**（FUNC-00966） |
| catalog_page_id | `comp.basic` |
| endpoint 数 | **1**（`comp.basic.upstream`） |
| 已删 API 册 | `API-产业综合上游依赖-用例.md`（API-01728～01730 作废，不复用） |
| 鉴权用例 | **0** |
