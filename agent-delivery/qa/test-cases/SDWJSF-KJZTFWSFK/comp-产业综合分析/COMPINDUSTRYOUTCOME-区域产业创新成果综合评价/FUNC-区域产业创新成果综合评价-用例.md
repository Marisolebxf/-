# 智能服务集群-科技专题服务算法库测试用例（区域产业创新成果综合评价 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=comp.industry-outcome` · `catalog_page_id=comp.industry-outcome` · path `/industry-comp/industry-outcome`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.industry-outcome`  
> **A 线对照**：`fp-split-by-api-run/work/L52.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；金样主流程 RIO-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 产业成果评价 | comp.industry-outcome.main |

可选参数 2 个：`region`（区域编码，example `440300`）、`year`（年份，example `2025`），catalog 均为 `required=false`。`sampleRequest` 同时传 `region=440300`、`year=2025`。备选 2 条与 sample 相反：不传 `region`（`year` 保持 2025）、不传 `year`（`region` 保持 440300）。反向恰好 2 条：只非法 `region`、只非法 `year`。path 为 `GET /comp/v1/comp/region-industry-outcome`。catalog `status=unavailable`，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01019**～**FUNC-01025**，共 **7** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.industry-outcome`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01019 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新成果综合评价模型 | 区域产业创新成果综合评价 | 产业成果评价 | 验证产业成果评价功能，检查填写 sampleRequest 所示参数 传 region=440300、year=2025 后返回产业成果字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；year=2025 | 1.侧栏进入「产业综合分析」→「区域产业创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「产业成果评价」；4.填写 region=440300、year=2025，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：index（number，responseFields 产业成果指数，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +5.0%）、adv（number，示例 1）；2、radar 为数组，元素含产品服务（number，示例 62）、企业创新（number，示例 71）、服务机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例产品服务 33、企业创新 34、服务机构 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome | M_SYNTH_183_1 | INTEG |  |  | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01020 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新成果综合评价模型 | 区域产业创新成果综合评价 | 产业成果评价 | 验证产业成果评价功能，检查不传可选 region、year 保持 2025（与 sample 相反）时仍返回产业成果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region；year=2025 | 1.侧栏进入「产业综合分析」→「区域产业创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「产业成果评价」；4.不传 region，填写 year=2025，点击调用 | 1、返回面板 body 仍与 sampleResponse 同层：index（number，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +5.0%）、adv（number，示例 1）；2、radar 为数组，元素含产品服务（number，示例 62）、企业创新（number，示例 71）、服务机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例产品服务 33、企业创新 34、服务机构 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome | M_SYNTH_183_1 | INTEG |  |  | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01021 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新成果综合评价模型 | 区域产业创新成果综合评价 | 产业成果评价 | 验证产业成果评价功能，检查不传可选 year、region 保持 440300（与 sample 相反）时仍返回产业成果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；不传 year | 1.侧栏进入「产业综合分析」→「区域产业创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「产业成果评价」；4.不传 year，填写 region=440300，点击调用 | 1、返回面板 body 仍与 sampleResponse 同层：index（number，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +5.0%）、adv（number，示例 1）；2、radar 为数组，元素含产品服务（number，示例 62）、企业创新（number，示例 71）、服务机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例产品服务 33、企业创新 34、服务机构 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome | M_SYNTH_183_1 | INTEG |  |  | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01022 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新成果综合评价模型 | 区域产业创新成果综合评价 | 产业成果评价 | 验证产业成果评价功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、year=2025 | 1.侧栏进入「产业综合分析」→「区域产业创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「产业成果评价」；4.填写 region=__invalid__、year=2025，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome |  | INTEG |  |  | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-04 场景=异常-入参-非法region catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01023 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新成果综合评价模型 | 区域产业创新成果综合评价 | 产业成果评价 | 验证产业成果评价功能，检查 year 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300 | 1.侧栏进入「产业综合分析」→「区域产业创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「产业成果评价」；4.填写 region=440300、year=0，点击调用 | 1、返回面板的 message 或 msg 指出 year 非法；2、不返回含 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome |  | INTEG |  |  | endpoint_id=comp.industry-outcome.main catalog_page_id=comp.industry-outcome 组合=RIO-05 场景=异常-入参-非法year catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01024 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新成果综合评价模型 | 区域产业创新成果综合评价 | 接口信息 | 验证区域产业创新成果综合评价的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域产业创新成果综合评价」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=GET、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「产业成果评价」；3、核对概览区标题、method（GET）、path（/comp/v1/comp/region-industry-outcome）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome |  | INTEG |  |  | catalog_page_id=comp.industry-outcome 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01025 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新成果综合评价模型 | 区域产业创新成果综合评价 | 算法测试 | 验证区域产业创新成果综合评价的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域产业创新成果综合评价」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 GET、path 为 /comp/v1/comp/region-industry-outcome；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「产业成果评价」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 GET /comp/v1/comp/region-industry-outcome，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-industry-outcome |  | INTEG |  |  | catalog_page_id=comp.industry-outcome 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RIO-01 | comp.industry-outcome.main | region=440300；year=2025 | 主路径全参（sampleRequest） |
| RIO-02 | comp.industry-outcome.main | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| RIO-03 | comp.industry-outcome.main | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| RIO-04 | comp.industry-outcome.main | region=__invalid__；year=2025 | 只破坏 region |
| RIO-05 | comp.industry-outcome.main | region=440300；year=0 | 只破坏 year |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 产业成果评价 | comp.industry-outcome.main | GET | /comp/v1/comp/region-industry-outcome | region?；year? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.industry-outcome.main | FUNC-01019、01020、01021、01022、01023 |
| （页面清单） | FUNC-01024、01025 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「产业成果评价」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-01019，组合 RIO-01 金样）
- [x] 有参接口：sampleRequest 主流程 1 条；与 sample 相反不传 region、不传 year 各 1 条备选；region、year 各恰好 1 条非法反向
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 产业综合分析模型构建 / 区域产业创新成果综合评价模型（L52）
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-01019～01025；A 线 `work/L52.md` 未改

**统计**：接口 **1**；主流程 **1**；备选 **2**；反向 **2**；清单 **2**；合计 **7** 条；编号闭区间 **FUNC-01019**～**FUNC-01025**（父控 R3 返工 · comp.industry-outcome 分配）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **7** |
| 编号闭区间 | **FUNC-01019**～**FUNC-01025** |
| 接口向（不含清单） | **5** |
| 清单 | **2** |
| 主流程 | **1**（FUNC-01019 · RIO-01 金样） |
| 备选-参数组合 | **2**（FUNC-01020、01021） |
| 反向 | **2**（FUNC-01022、01023） |
| catalog_page_id | `comp.industry-outcome` |
| endpoint 数 | **1**（`comp.industry-outcome.main`） |
| 已删 API 册 | `API-区域产业创新成果综合评价-用例.md`（API-01777～01781 作废，不复用） |
| 鉴权用例 | **0** |
