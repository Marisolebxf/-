# 智能服务集群-科技专题服务算法库测试用例（区域产业创新政策综合评价 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=comp.policy-outcome` · `catalog_page_id=comp.policy-outcome` · path `#/industry-comp/policy-outcome`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.policy-outcome`  
> **A 线对照**：`fp-split-by-api-run/work/L54.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；双 endpoint 结构对齐 comp.tech-outcome；金样主流程）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 政策成果评价 | comp.policy-outcome.main | GET | unavailable |
| 2 | 区域产业创新政策综合评价模型 | comp.policy-outcome.m_synth_185_1 | POST | available |

两个接口的可选参数都是 `region`（区域编码，example `440300`）、`year`（年份，example `2025`）。`sampleRequest` 均含 `region=440300`、`year=2025`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`（`year` 保持 2025）、不传 `year`（`region` 保持 440300）。每个参数恰好 1 条非法反向（`region=__invalid__` 或 `year=-1`），另一参数保持文档合法值。`政策成果评价` 的 catalog `status=unavailable`，备注注明未交付，仍按该接口 sampleResponse 编写。

`GET /comp/v1/comp/region-policy-outcome` 只挂 title「政策成果评价」。`POST /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute` 只挂 title「区域产业创新政策综合评价模型」。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01038**～**FUNC-01049**，共 **12** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.policy-outcome`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01038 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 政策成果评价 | 验证政策成果评价功能，检查填写 region=440300、year=2025调用后返回与 sampleResponse 同层字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；year=2025 | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「政策成果评价」；4.填写 region=440300、year=2025，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：index（number，政策指数，示例 66.3）、rank（number，示例 4）、yoy（string，示例 +8.0%）、adv（number，示例 1）；2、radar 为数组，元素含政策供给（number，示例 62）、政策力度（number，示例 71）、政策效果（number，示例 66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例政策供给 33、政策力度 34、政策效果 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例深圳 92/1/领先/综合优势突出、北京 90/2/领先/科研密度高、上海 88/3/领先/产业化强、杭州 79/4/跟进/数字经济拉动 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-policy-outcome | M_SYNTH_185_1 | INTEG |  | FUNC-01038 | endpoint_id=comp.policy-outcome.main catalog_page_id=comp.policy-outcome 组合=POL-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01039 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 政策成果评价 | 验证政策成果评价功能，检查不传 region 后仍返回与 sampleResponse 同类字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region；year=2025 | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「政策成果评价」；4.不传 region，填写 year=2025，点击调用（不传 region），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：index（number，政策指数，示例 66.3）、rank（number，示例 4）、yoy（string，示例 +8.0%）、adv（number，示例 1）；2、radar 为数组，元素含政策供给、政策力度、政策效果（number，示例 62、71、66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例政策供给 33、政策力度 34、政策效果 33；5、rows 为数组，元素含 name、score、rank、tag、note，示例深圳 92/1/领先/综合优势突出、北京 90/2/领先/科研密度高、上海 88/3/领先/产业化强、杭州 79/4/跟进/数字经济拉动 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-policy-outcome | M_SYNTH_185_1 | INTEG |  | FUNC-01039 | endpoint_id=comp.policy-outcome.main catalog_page_id=comp.policy-outcome 组合=POL-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01040 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 政策成果评价 | 验证政策成果评价功能，检查不传 year 后仍返回与 sampleResponse 同类字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；不传 year | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「政策成果评价」；4.不传 year，填写 region=440300，点击调用（不传 year），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：index（number，政策指数，示例 66.3）、rank（number，示例 4）、yoy（string，示例 +8.0%）、adv（number，示例 1）；2、radar 为数组，元素含政策供给、政策力度、政策效果（number，示例 62、71、66）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 92、北京 90、上海 88、杭州 79、广州 76、苏州 74；4、pie_items 为数组，元素含 name（string）、value（number），示例政策供给 33、政策力度 34、政策效果 33；5、rows 为数组，元素含 name、score、rank、tag、note，示例深圳 92/1/领先/综合优势突出、北京 90/2/领先/科研密度高、上海 88/3/领先/产业化强、杭州 79/4/跟进/数字经济拉动 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-policy-outcome | M_SYNTH_185_1 | INTEG |  | FUNC-01040 | endpoint_id=comp.policy-outcome.main catalog_page_id=comp.policy-outcome 组合=POL-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01041 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 政策成果评价 | 验证政策成果评价功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region 取非法值；year=2025 保持合法 | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「政策成果评价」；4.填写 region=__invalid__、year=2025，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-policy-outcome |  | INTEG |  | FUNC-01041 | endpoint_id=comp.policy-outcome.main catalog_page_id=comp.policy-outcome 组合=POL-04 场景=异常-入参-非法region catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01042 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 政策成果评价 | 验证政策成果评价功能，检查 year 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、year 取非法值；region=440300 保持合法 | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「政策成果评价」；4.填写 region=440300、year=-1，点击调用 | 1、返回面板的 message 或 msg 指出 year 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/region-policy-outcome |  | INTEG |  | FUNC-01042 | endpoint_id=comp.policy-outcome.main catalog_page_id=comp.policy-outcome 组合=POL-05 场景=异常-入参-非法year catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01043 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 区域产业创新政策综合评价模型 | 验证区域产业创新政策综合评价模型功能，检查填写 region=440300、year=2025调用后返回 metric_id、hint 与 index 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；year=2025 | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域产业创新政策综合评价模型」；4.填写 region=440300、year=2025，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_SYNTH_185_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 index（number，政策指数），返回中应有该字段；3、结构与 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute | M_SYNTH_185_1 | INTEG |  | FUNC-01043 | endpoint_id=comp.policy-outcome.m_synth_185_1 catalog_page_id=comp.policy-outcome 组合=M185-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01044 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 区域产业创新政策综合评价模型 | 验证区域产业创新政策综合评价模型功能，检查不传 region 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region；year=2025 | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域产业创新政策综合评价模型」；4.不传 region，填写 year=2025，点击调用（不传 region），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_185_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 所列 index（number，政策指数）仍应出现 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute | M_SYNTH_185_1 | INTEG |  | FUNC-01044 | endpoint_id=comp.policy-outcome.m_synth_185_1 catalog_page_id=comp.policy-outcome 组合=M185-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01045 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 区域产业创新政策综合评价模型 | 验证区域产业创新政策综合评价模型功能，检查不传 year 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300；不传 year | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域产业创新政策综合评价模型」；4.不传 year，填写 region=440300，点击调用（不传 year），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_185_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 所列 index（number，政策指数）仍应出现 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute | M_SYNTH_185_1 | INTEG |  | FUNC-01045 | endpoint_id=comp.policy-outcome.m_synth_185_1 catalog_page_id=comp.policy-outcome 组合=M185-03 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01046 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 区域产业创新政策综合评价模型 | 验证区域产业创新政策综合评价模型功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region 取非法值；year=2025 保持合法 | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域产业创新政策综合评价模型」；4.填写 region=__invalid__、year=2025，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute |  | INTEG |  | FUNC-01046 | endpoint_id=comp.policy-outcome.m_synth_185_1 catalog_page_id=comp.policy-outcome 组合=M185-04 场景=异常-入参-非法region catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01047 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 区域产业创新政策综合评价模型 | 验证区域产业创新政策综合评价模型功能，检查 year 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、year 取非法值；region=440300 保持合法 | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换至「算法测试」tab；3.接口下拉选择「区域产业创新政策综合评价模型」；4.填写 region=440300、year=-1，点击调用 | 1、返回面板的 message 或 msg 指出 year 非法；2、不返回含 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute |  | INTEG |  | FUNC-01047 | endpoint_id=comp.policy-outcome.m_synth_185_1 catalog_page_id=comp.policy-outcome 组合=M185-05 场景=异常-入参-非法year catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01048 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 接口信息 | 验证区域产业创新政策综合评价的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（政策成果评价、区域产业创新政策综合评价模型）；3、默认项概览 method=GET、path=/comp/v1/comp/region-policy-outcome；4、切换后概览对应区域产业创新政策综合评价模型 POST /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01048 | catalog_page_id=comp.policy-outcome 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01049 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域产业创新政策综合评价模型 | 区域产业创新政策综合评价 | 算法测试 | 验证区域产业创新政策综合评价的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域产业创新政策综合评价」；2.切换到「算法测试」tab；3.下拉切换到「区域产业创新政策综合评价模型」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「区域产业创新政策综合评价模型」；3、调用区 method 为 POST、path 为 /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01049 | catalog_page_id=comp.policy-outcome 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| POL-01 | comp.policy-outcome.main | region=440300；year=2025 | 主路径（sampleRequest） |
| POL-02 | comp.policy-outcome.main | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| POL-03 | comp.policy-outcome.main | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| POL-04 | comp.policy-outcome.main | region=__invalid__；year=2025 | 只破坏 region |
| POL-05 | comp.policy-outcome.main | region=440300；year=-1 | 只破坏 year |
| M185-01 | comp.policy-outcome.m_synth_185_1 | region=440300；year=2025 | 主路径（sampleRequest，请求体） |
| M185-02 | comp.policy-outcome.m_synth_185_1 | 不传 region；year=2025 | 省略可选 region（与 sample 相反） |
| M185-03 | comp.policy-outcome.m_synth_185_1 | region=440300；不传 year | 省略可选 year（与 sample 相反） |
| M185-04 | comp.policy-outcome.m_synth_185_1 | region=__invalid__；year=2025 | 只破坏 region |
| M185-05 | comp.policy-outcome.m_synth_185_1 | region=440300；year=-1 | 只破坏 year |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 政策成果评价 | comp.policy-outcome.main | GET | /comp/v1/comp/region-policy-outcome | region?；year? | unavailable |
| 区域产业创新政策综合评价模型 | comp.policy-outcome.m_synth_185_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_185_1/compute | region?；year? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.policy-outcome.main | FUNC-01038、01039、01040、01041、01042 |
| comp.policy-outcome.m_synth_185_1 | FUNC-01043、01044、01045、01046、01047 |
| （页面清单） | FUNC-01048、01049 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-01038 政策成果评价、FUNC-01043 区域产业创新政策综合评价模型）
- [x] 各接口：sampleRequest 主流程 1 条 + 与 sample 相反的不传 region、不传 year 各 1 条备选 + region、year 各 1 条非法反向，各恰好 5 条
- [x] unavailable（政策成果评价）仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L54：`产业综合分析模型构建` / `区域产业创新政策综合评价模型`
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 双接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-01038～01049

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **12** 条；主流程 **2**、备选 **4**、反向 **4**、清单 **2**；编号闭区间 **FUNC-01038**～**FUNC-01049**（R3 返工 · comp.policy-outcome）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **12** |
| 编号闭区间 | **FUNC-01038**～**FUNC-01049** |
| 接口向（不含清单） | **10** |
| 清单 | **2** |
| 主流程 | **2**（FUNC-01038、FUNC-01043） |
| 备选-参数组合 | **4**（01039、01040、01044、01045） |
| 反向 | **4**（01041、01042、01046、01047） |
| catalog_page_id | `comp.policy-outcome` |
| endpoint 数 | **2** |
| 已删 API 册 | `API-区域产业创新政策综合评价-用例.md`（API-01792～01801 作废，不复用） |
| 鉴权用例 | **0** |
