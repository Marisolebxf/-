# 智能服务集群-科技专题服务算法库测试用例（区域创新要素层次综合评价 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=comp.element-layer` · `catalog_page_id=comp.element-layer` · path `/industry-comp/element-layer`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.element-layer`  
> **A 线对照**：`fp-split-by-api-run/work/L57.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 ELY-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 要素层次 | comp.element-layer.main |

可选参数只有 `region`（区域编码，example `440300`，`required=false`）。`sampleRequest` 含 `region=440300`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`。反向恰好 1 条：`region=__invalid__`。catalog `status=unavailable`，备注注明未交付，仍按该接口 sampleResponse 编写。path 为 `GET /comp/v1/comp/element-layer`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01060**～**FUNC-01064**，共 **5** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.element-layer`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01060 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素层次综合评价模型 | 区域创新要素层次综合评价 | 要素层次 | 验证要素层次功能，检查填写 sampleRequest 所示参数 传 region=440300 后返回层次综合分与三层要素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300 | 1.侧栏进入「产业综合分析」→「区域创新要素层次综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「要素层次」；4.填写 region=440300，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：index（number，responseFields 层次综合分，示例 69.8）、balance（number，示例 0.72）、hit（string，示例 2/3）、rank（number，示例 5）；2、radar 为数组，元素含基础层（number，示例 74）、支撑层（number，示例 68）、应用层（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例基础层 74、支撑层 68、应用层 66；4、pie_items 为数组，元素含 name（string）、value（number），示例基础层 34、支撑层 33、应用层 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例基础层 score 74 rank 1 tag 达标 note 人才/科研底座较稳、支撑层 score 68 rank 2 tag 临界 note 资金/政策支撑一般、应用层 score 66 rank 3 tag 临界 note 转化落地待加强 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-layer | M_SYNTH_ELEM_LEVEL_INDEX | INTEG |  | FUNC-01060 | endpoint_id=comp.element-layer.main catalog_page_id=comp.element-layer 组合=ELY-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01061 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素层次综合评价模型 | 区域创新要素层次综合评价 | 要素层次 | 验证要素层次功能，检查不传可选 region（与 sample 相反）时仍返回层次综合分与三层要素字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region | 1.侧栏进入「产业综合分析」→「区域创新要素层次综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「要素层次」；4.不传 region，点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：index（number，responseFields 层次综合分，示例 69.8）、balance（number，示例 0.72）、hit（string，示例 2/3）、rank（number，示例 5）；2、radar 为数组，元素含基础层（number，示例 74）、支撑层（number，示例 68）、应用层（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例基础层 74、支撑层 68、应用层 66；4、pie_items 为数组，元素含 name（string）、value（number），示例基础层 34、支撑层 33、应用层 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例基础层 score 74 rank 1 tag 达标 note 人才/科研底座较稳、支撑层 score 68 rank 2 tag 临界 note 资金/政策支撑一般、应用层 score 66 rank 3 tag 临界 note 转化落地待加强 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-layer | M_SYNTH_ELEM_LEVEL_INDEX | INTEG |  | FUNC-01061 | endpoint_id=comp.element-layer.main catalog_page_id=comp.element-layer 组合=ELY-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01062 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素层次综合评价模型 | 区域创新要素层次综合评价 | 要素层次 | 验证要素层次功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、无其它查询参数 | 1.侧栏进入「产业综合分析」→「区域创新要素层次综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「要素层次」；4.填写 region=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-layer |  | INTEG |  | FUNC-01062 | endpoint_id=comp.element-layer.main catalog_page_id=comp.element-layer 组合=ELY-03 场景=异常-入参-非法region catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01063 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素层次综合评价模型 | 区域创新要素层次综合评价 | 接口信息 | 验证区域创新要素层次综合评价的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域创新要素层次综合评价」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「要素层次」；3、核对概览区标题、method（GET）、path（/comp/v1/comp/element-layer）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-layer |  | INTEG |  | FUNC-01063 | catalog_page_id=comp.element-layer 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01064 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素层次综合评价模型 | 区域创新要素层次综合评价 | 算法测试 | 验证区域创新要素层次综合评价的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域创新要素层次综合评价」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /comp/v1/comp/element-layer；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「要素层次」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /comp/v1/comp/element-layer，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-layer |  | INTEG |  | FUNC-01064 | catalog_page_id=comp.element-layer 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ELY-01 | comp.element-layer.main | region=440300 | 主路径（sampleRequest） |
| ELY-02 | comp.element-layer.main | 不传 region | 省略可选 region（与 sample 相反） |
| ELY-03 | comp.element-layer.main | region=__invalid__ | 只破坏 region |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 要素层次 | comp.element-layer.main | GET | /comp/v1/comp/element-layer | region? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.element-layer.main | FUNC-01060、01061、01062 |
| （页面清单） | FUNC-01063、01064 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「要素层次」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-01060，组合 ELY-01 金样）
- [x] sampleRequest 主流程 1 条；与 sample 相反不传 region 1 条备选；region 恰好 1 条非法反向
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 产业综合分析模型构建 / 区域创新要素层次综合评价模型（L57）
- [x] 单接口页清单用例 2 条
- [x] `coverage-fp.md` 已同步 FUNC-01060～01064

**统计**：合计 **5** 条；编号闭区间 **FUNC-01060**～**FUNC-01064**（R3-批18 · comp.element-layer）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **FUNC-01060**～**FUNC-01064** |
| 已删 API 册 | `API-区域创新要素层次综合评价-用例.md`（API-01808～01810 作废） |
