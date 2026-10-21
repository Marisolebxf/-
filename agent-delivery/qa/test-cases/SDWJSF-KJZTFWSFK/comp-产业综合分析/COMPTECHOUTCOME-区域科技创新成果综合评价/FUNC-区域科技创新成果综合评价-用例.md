# 智能服务集群-科技专题服务算法库测试用例（区域科技创新成果综合评价 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=comp.tech-outcome` · `catalog_page_id=comp.tech-outcome` · path `#/industry-comp/tech-outcome`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.tech-outcome`  
> **A 线对照**：`fp-split-by-api-run/work/L51.md`（覆盖矩阵用，禁止 field 一行一用例；未改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 科技成果评价 | comp.tech-outcome.main | unavailable |
| 2 | 区域科技创新成果综合评价模型 | comp.tech-outcome.m_synth_182_1 | available |

两个接口的可选参数均为 `region`（区域编码，example `440300`）、`year`（年份，example `2025`）。`sampleRequest` 均含 `region=440300`、`year=2025`。主流程对齐 sampleRequest；备选与 sample 相反：不传 `region`（`year` 保持 2025）、不传 `year`（`region` 保持 440300）。每个参数恰好 1 条非法反向（`region=__invalid__` 或 `year=-1`），另一参数保持文档合法值。`科技成果评价` 的 catalog `status=unavailable`，仍按该接口文档返回体编写，备注注明未交付。path `GET /comp/v1/comp/region-tech-outcome` 为本页独占，与同模块其它 `region-*-outcome` 分开验收。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01007**～**FUNC-01018**，共 **12** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.tech-outcome`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01007 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 科技成果评价 | 验证科技成果评价功能，检查填写 region=440300、year=2025调用后返回与 sampleResponse 一致的指数与图表字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；year=2025 | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「科技成果评价」；4.填写 region=440300、year=2025，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：index（number，responseFields 科技成果指数，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +6.0%）、adv（number，示例 1）；2、radar 为数组，元素含基础科学（number，示例 62）、应用科技（number，示例 71）、科研机构（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例基础科学 33、应用科技 34、科研机构 33；5、rows 为数组（responseFields 区域明细），元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳/92/1/领先/综合优势突出、北京/90/2/领先/科研密度高、上海/88/3/领先/产业化强、杭州/79/4/跟进/数字经济拉动 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome | M_SYNTH_182_1 | INTEG |  |  | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01008 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 科技成果评价 | 验证科技成果评价功能，检查不传可选 region、year=2025 不传 region 后仍返回与 sampleResponse 同类的业务字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region；year=2025 | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「科技成果评价」；4.不传 region，填写 year=2025，点击调用（不传 region），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：index（number，科技成果指数，示例 66.3）、rank（number，示例 2）、yoy（string，示例 +6.0%）、adv（number，示例 1）；2、radar、bar_items、pie_items、rows 结构与主流程一致，rows 元素仍含 name、score、rank、tag、note | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome | M_SYNTH_182_1 | INTEG |  |  | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01009 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 科技成果评价 | 验证科技成果评价功能，检查 region=440300、不传可选 year 不传 year 后仍返回与 sampleResponse 同类的业务字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；不传 year | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「科技成果评价」；4.不传 year，填写 region=440300，点击调用（不传 year），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：index（number，科技成果指数，示例 66.3）、rank、yoy、adv 类型与主流程一致；2、radar、bar_items、pie_items、rows 结构与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome | M_SYNTH_182_1 | INTEG |  |  | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01010 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 科技成果评价 | 验证科技成果评价功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region 取非法值；year=2025 保持合法 | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「科技成果评价」；4.填写 region=__invalid__、year=2025，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome |  | INTEG |  |  | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-04 场景=异常-入参-非法region catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01011 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 科技成果评价 | 验证科技成果评价功能，检查 year 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、year 取非法值；region=440300 保持合法 | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「科技成果评价」；4.填写 region=440300、year=-1，点击调用 | 1、返回面板的 message 或 msg 指出 year 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-tech-outcome |  | INTEG |  |  | endpoint_id=comp.tech-outcome.main catalog_page_id=comp.tech-outcome 组合=TEC-05 场景=异常-入参-非法year catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01012 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 验证区域科技创新成果综合评价模型功能，检查填写 region=440300、year=2025调用后返回 metric_id、hint 与 responseFields 声明字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；year=2025 | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域科技创新成果综合评价模型」；4.填写 region=440300、year=2025，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_SYNTH_182_1）、hint（string，示例「真实 compute 响应,以实际调用为准」）；2、responseFields 另声明 index（number，科技成果指数）、rows（array，区域明细），sampleResponse 未给出这两字段的示例值，返回中应含 index、rows 且类型与声明一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | M_SYNTH_182_1 | INTEG |  |  | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01013 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 验证区域科技创新成果综合评价模型功能，检查不传可选 region、year=2025 不传 region 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region；year=2025 | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域科技创新成果综合评价模型」；4.不传 region，填写 year=2025，点击调用（不传 region），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_182_1）、hint（string）；2、responseFields 声明的 index（number）、rows（array）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | M_SYNTH_182_1 | INTEG |  |  | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01014 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 验证区域科技创新成果综合评价模型功能，检查 region=440300、不传可选 year 不传 year 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；不传 year | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域科技创新成果综合评价模型」；4.不传 year，填写 region=440300，点击调用（不传 year），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id、hint；2、index、rows 仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | M_SYNTH_182_1 | INTEG |  |  | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-03 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01015 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 验证区域科技创新成果综合评价模型功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region 取非法值；year=2025 保持合法 | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域科技创新成果综合评价模型」；4.填写 region=__invalid__、year=2025，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 metric_id 或 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute |  | INTEG |  |  | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-04 场景=异常-入参-非法region catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01016 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 区域科技创新成果综合评价模型 | 验证区域科技创新成果综合评价模型功能，检查 year 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、year 取非法值；region=440300 保持合法 | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域科技创新成果综合评价模型」；4.填写 region=440300、year=-1，点击调用 | 1、返回面板的 message 或 msg 指出 year 非法；2、不返回含 metric_id 或 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute |  | INTEG |  |  | endpoint_id=comp.tech-outcome.m_synth_182_1 catalog_page_id=comp.tech-outcome 组合=SYN-05 场景=异常-入参-非法year catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01017 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 接口信息 | 验证区域科技创新成果综合评价的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（科技成果评价、区域科技创新成果综合评价模型）；3、默认项概览 method=GET、path=/comp/v1/comp/region-tech-outcome；4、切换后概览对应区域科技创新成果综合评价模型 POST /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=comp.tech-outcome 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01018 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域科技创新成果综合评价模型 | 区域科技创新成果综合评价 | 算法测试 | 验证区域科技创新成果综合评价的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域科技创新成果综合评价」；2.切换到「算法测试」tab；3.下拉切换到「区域科技创新成果综合评价模型」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「区域科技创新成果综合评价模型」；3、调用区 method 为 POST、path 为 /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=comp.tech-outcome 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TEC-01 | comp.tech-outcome.main | region=440300；year=2025 | 主路径（sampleRequest） |
| TEC-02 | comp.tech-outcome.main | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| TEC-03 | comp.tech-outcome.main | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| TEC-04 | comp.tech-outcome.main | region=__invalid__；year=2025 | 只破坏 region |
| TEC-05 | comp.tech-outcome.main | region=440300；year=-1 | 只破坏 year |
| SYN-01 | comp.tech-outcome.m_synth_182_1 | region=440300；year=2025 | 主路径（sampleRequest，请求体） |
| SYN-02 | comp.tech-outcome.m_synth_182_1 | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| SYN-03 | comp.tech-outcome.m_synth_182_1 | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| SYN-04 | comp.tech-outcome.m_synth_182_1 | region=__invalid__；year=2025 | 只破坏 region |
| SYN-05 | comp.tech-outcome.m_synth_182_1 | region=440300；year=-1 | 只破坏 year |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 科技成果评价 | comp.tech-outcome.main | GET | /comp/v1/comp/region-tech-outcome | region?；year? | unavailable |
| 区域科技创新成果综合评价模型 | comp.tech-outcome.m_synth_182_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | region?；year? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.tech-outcome.main | FUNC-01007、01008、01009、01010、01011 |
| comp.tech-outcome.m_synth_182_1 | FUNC-01012、01013、01014、01015、01016 |
| （页面清单） | FUNC-01017、01018 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-01007、01012）
- [x] 每个接口：sampleRequest 主流程 + 省略 region、省略 year 备选 + region、year 各 1 条非法反向
- [x] 正向预期按 sampleResponse / responseFields；反向预期写 message 或 msg 指出该参数非法
- [x] unavailable（科技成果评价）仍按文档写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L51：产业综合分析模型构建 / 区域科技创新成果综合评价模型
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-01007～01018
- [x] 金样：FUNC-01007（科技成果评价主流程）

**统计**：catalog endpoint **2**；FUNC 用例 **12** 条；主流程 **2**、备选 **4**、反向 **4**、清单 **2**；编号闭区间 **FUNC-01007**～**FUNC-01018**。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **12** |
| 编号闭区间 | **FUNC-01007**～**FUNC-01018** |
| 接口向（不含清单） | **10** |
| 主流程 | **2** |
| 备选-参数组合 | **4** |
| 反向 | **4** |
| 清单 | **2** |
| 已删 API 册 | `API-区域科技创新成果综合评价-用例.md`（API-01767～01776 作废，不复用） |
| 鉴权用例 | **0** |
