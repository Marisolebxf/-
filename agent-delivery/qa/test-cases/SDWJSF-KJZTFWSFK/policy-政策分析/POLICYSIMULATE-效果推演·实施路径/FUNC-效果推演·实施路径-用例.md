# 智能服务集群-科技专题服务算法库测试用例（效果推演 · 实施路径 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=policy.simulate` · `catalog_page_id=policy.simulate` · path `#/policy/simulate`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.simulate`  
> **A 线对照**：**无对应 Lxx**（`_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.simulate`，原因：不扩六级；不改 `work/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批12）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 效果推演 | policy.simulate.main | unavailable |
| 2 | 政策效果推演 | policy.simulate.m_policy_simulate | available |

两个接口的可选参数相同：`scope_code`、`scenario_id`、`limit`。`sampleRequest` 均为 `limit=20`，不含 `scope_code`、`scenario_id`。主流程对齐该 sample；备选各动一个参数，与 sample 相反：传入 `scope_code=440000`（参数说明「如 440000」，亦为 sampleResponse 示例）、传入 `scenario_id=sc_support_up_20`（枚举非空项，亦为 sampleResponse 示例）、不传 `limit`。反向各 1 条非法，不把省略写成反向。GET 走查询参数；POST 走 JSON 请求体。`效果推演` 为 unavailable，仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00709**～**FUNC-00724**，共 **16** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.simulate`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00709 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 效果推演 | 验证效果推演功能，检查填写 sampleRequest 所示参数 传 limit=20、不传 scope_code 与 scenario_id 后返回推演字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 scope_code；不传 scenario_id（对齐 sampleRequest） | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scope_code、不传 scenario_id，填写 limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 scope_code（string）、scenario_id（string）、baseline_value（number）、simulated_value（number，responseFields 推演值）、metric_id（string）；3、与 sampleResponse 逐字段一致，示例第1条 scope_code=440000、scenario_id=sc_support_up_20、baseline_value=70、simulated_value=78.4、metric_id=M_POLICY_SIMULATE | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG |  |  | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00710 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 效果推演 | 验证效果推演功能，检查传入可选 scope_code=440000、limit 保持 sample 的 20、不传 scenario_id 时仍返回推演字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scope_code=440000；limit=20；不传 scenario_id | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scenario_id，填写 scope_code=440000、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 scope_code（string）、scenario_id（string）、baseline_value（number）、simulated_value（number，responseFields 推演值）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（scope_code=440000、scenario_id=sc_support_up_20、baseline_value=70、simulated_value=78.4、metric_id=M_POLICY_SIMULATE）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG |  |  | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00711 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 效果推演 | 验证效果推演功能，检查传入可选 scenario_id=sc_support_up_20、limit 保持 sample 的 20、不传 scope_code 时仍返回推演字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、scenario_id=sc_support_up_20；limit=20；不传 scope_code | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scope_code，填写 scenario_id=sc_support_up_20、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 scope_code（string）、scenario_id（string）、baseline_value（number）、simulated_value（number，responseFields 推演值）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（scope_code=440000、scenario_id=sc_support_up_20、baseline_value=70、simulated_value=78.4、metric_id=M_POLICY_SIMULATE）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG |  |  | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00712 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 效果推演 | 验证效果推演功能，检查不传可选 limit、亦不传 scope_code 与 scenario_id 时仍返回推演字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 scope_code；不传 scenario_id；不传 limit | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scope_code、不传 scenario_id、不传 limit，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 scope_code（string）、scenario_id（string）、baseline_value（number）、simulated_value（number，responseFields 推演值）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（baseline_value=70、simulated_value=78.4、metric_id=M_POLICY_SIMULATE）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_DS_11_POLICY_EVAL_015 | INTEG |  |  | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-04 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00713 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 效果推演 | 验证效果推演功能，检查 scope_code 非法、limit 保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 scenario_id | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scenario_id，填写 scope_code=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scope_code 非法；2、不返回含 simulated_value 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate |  | INTEG |  |  | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-05 场景=异常-入参-非法scope_code catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00714 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 效果推演 | 验证效果推演功能，检查 scenario_id 非法、limit 保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=20；不传 scope_code | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scope_code，填写 scenario_id=__invalid__（不在空、sc_support_up_20、sc_support_up_40、sc_coverage_expand）、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scenario_id 非法；2、不返回含 simulated_value 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate |  | INTEG |  |  | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-06 场景=异常-入参-非法scenario_id catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00715 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 效果推演 | 验证效果推演功能，检查 limit 非法、scope_code 与 scenario_id 保持 sample 不传时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 scope_code；不传 scenario_id | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「效果推演」；4.不传 scope_code、不传 scenario_id，填写 limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 simulated_value 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate |  | INTEG |  |  | endpoint_id=policy.simulate.main catalog_page_id=policy.simulate 组合=SIM-07 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00716 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 政策效果推演 | 验证政策效果推演功能，检查填写 sampleRequest 所示参数 提交 limit=20、不传 scope_code 与 scenario_id 后返回推演字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、请求体 limit=20；不传 scope_code；不传 scenario_id（对齐 sampleRequest） | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「政策效果推演」；4.不传 scope_code、不传 scenario_id，填写 limit=20，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_SIMULATE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 另含 simulated_value（number，推演值） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | M_POLICY_SIMULATE | INTEG |  |  | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00717 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 政策效果推演 | 验证政策效果推演功能，检查传入可选 scope_code=440000、limit 保持 sample 的 20、不传 scenario_id 时仍返回推演字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、请求体 scope_code=440000；limit=20；不传 scenario_id | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「政策效果推演」；4.不传 scenario_id，填写 scope_code=440000、limit=20，点击调用 | 1、返回面板 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_SIMULATE）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 simulated_value 为 number（推演值） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | M_POLICY_SIMULATE | INTEG |  |  | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00718 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 政策效果推演 | 验证政策效果推演功能，检查传入可选 scenario_id=sc_support_up_20、limit 保持 sample 的 20、不传 scope_code 时仍返回推演字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、请求体 scenario_id=sc_support_up_20；limit=20；不传 scope_code | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「政策效果推演」；4.不传 scope_code，填写 scenario_id=sc_support_up_20、limit=20，点击调用 | 1、返回面板 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_SIMULATE）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 simulated_value 为 number（推演值） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | M_POLICY_SIMULATE | INTEG |  |  | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-03 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00719 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 政策效果推演 | 验证政策效果推演功能，检查不传可选 limit、亦不传 scope_code 与 scenario_id 时仍返回推演字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 scope_code；不传 scenario_id；不传 limit | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「政策效果推演」；4.不传 scope_code、不传 scenario_id、不传 limit，点击调用 | 1、返回面板 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_SIMULATE）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 simulated_value 为 number（推演值） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | M_POLICY_SIMULATE | INTEG |  |  | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-04 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00720 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 政策效果推演 | 验证政策效果推演功能，检查 scope_code 非法、limit 保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、请求体 limit=20；不传 scenario_id | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「政策效果推演」；4.不传 scenario_id，填写 scope_code=__invalid__、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scope_code 非法；2、不返回含 metric_id 或 simulated_value 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute |  | INTEG |  |  | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-05 场景=异常-入参-非法scope_code catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00721 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 政策效果推演 | 验证政策效果推演功能，检查 scenario_id 非法、limit 保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、请求体 limit=20；不传 scope_code | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「政策效果推演」；4.不传 scope_code，填写 scenario_id=__invalid__（不在空、sc_support_up_20、sc_support_up_40、sc_coverage_expand）、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 scenario_id 非法；2、不返回含 metric_id 或 simulated_value 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute |  | INTEG |  |  | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-06 场景=异常-入参-非法scenario_id catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00722 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 政策效果推演 | 验证政策效果推演功能，检查 limit 非法、scope_code 与 scenario_id 保持 sample 不传时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 scope_code；不传 scenario_id | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换至「算法测试」tab；3.接口下拉选择「政策效果推演」；4.不传 scope_code、不传 scenario_id，填写 limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 metric_id 或 simulated_value 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute |  | INTEG |  |  | endpoint_id=policy.simulate.m_policy_simulate catalog_page_id=policy.simulate 组合=CMP-07 场景=异常-入参-非法limit catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00723 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 接口信息 | 验证效果推演 · 实施路径的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（效果推演、政策效果推演）；3、默认项概览 method=GET、path=/policy/v1/policy/simulate；4、切换后概览对应政策效果推演 POST /policy/v1/polan/metric/M_POLICY_SIMULATE/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=policy.simulate 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00724 | 算法工具库 | 科技专题服务算法库 | 政策效果推演与实施路径 | 效果推演 · 实施路径 | 效果推演 · 实施路径 | 算法测试 | 验证效果推演 · 实施路径的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「效果推演 · 实施路径」；2.切换到「算法测试」tab；3.下拉切换到「政策效果推演」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「政策效果推演」；3、调用区 method 为 POST、path 为 /policy/v1/polan/metric/M_POLICY_SIMULATE/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=policy.simulate 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SIM-01 | policy.simulate.main | 不传 scope_code；不传 scenario_id；limit=20 | 主路径（sampleRequest）；查询参数 |
| SIM-02 | policy.simulate.main | scope_code=440000；不传 scenario_id；limit=20 | 传入可选 scope_code（sample 不含 scope_code；440000 取参数说明示例） |
| SIM-03 | policy.simulate.main | 不传 scope_code；scenario_id=sc_support_up_20；limit=20 | 传入可选 scenario_id（sample 不含 scenario_id；枚举非空项） |
| SIM-04 | policy.simulate.main | 不传 scope_code；不传 scenario_id；不传 limit | 省略可选 limit（sample 含 limit） |
| SIM-05 | policy.simulate.main | scope_code=__invalid__；不传 scenario_id；limit=20 | 只破坏 scope_code |
| SIM-06 | policy.simulate.main | 不传 scope_code；scenario_id=__invalid__（不在空、sc_support_up_20、sc_support_up_40、sc_coverage_expand）；limit=20 | 只破坏 scenario_id |
| SIM-07 | policy.simulate.main | 不传 scope_code；不传 scenario_id；limit=-1 | 只破坏 limit |
| CMP-01 | policy.simulate.m_policy_simulate | 不传 scope_code；不传 scenario_id；limit=20 | 主路径（sampleRequest）；JSON 请求体 |
| CMP-02 | policy.simulate.m_policy_simulate | scope_code=440000；不传 scenario_id；limit=20 | 传入可选 scope_code（sample 不含 scope_code；440000 取参数说明示例） |
| CMP-03 | policy.simulate.m_policy_simulate | 不传 scope_code；scenario_id=sc_support_up_20；limit=20 | 传入可选 scenario_id（sample 不含 scenario_id；枚举非空项） |
| CMP-04 | policy.simulate.m_policy_simulate | 不传 scope_code；不传 scenario_id；不传 limit | 省略可选 limit（sample 含 limit） |
| CMP-05 | policy.simulate.m_policy_simulate | scope_code=__invalid__；不传 scenario_id；limit=20 | 只破坏 scope_code |
| CMP-06 | policy.simulate.m_policy_simulate | 不传 scope_code；scenario_id=__invalid__（不在空、sc_support_up_20、sc_support_up_40、sc_coverage_expand）；limit=20 | 只破坏 scenario_id |
| CMP-07 | policy.simulate.m_policy_simulate | 不传 scope_code；不传 scenario_id；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 效果推演 | policy.simulate.main | GET | /policy/v1/policy/simulate | scope_code?；scenario_id?；limit? | unavailable |
| 政策效果推演 | policy.simulate.m_policy_simulate | POST | /policy/v1/polan/metric/M_POLICY_SIMULATE/compute | scope_code?；scenario_id?；limit? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.simulate.main | FUNC-00709、00710、00711、00712、00713、00714、00715 |
| policy.simulate.m_policy_simulate | FUNC-00716、00717、00718、00719、00720、00721、00722 |
| （页面清单） | FUNC-00723、00724 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title「效果推演」「政策效果推演」均在功能点列出现，且各有 1 条 `场景=主流程`（FUNC-00709、FUNC-00716）
- [x] 每个接口：sample 主流程 1 条；与 sample 相反的传/不传各 1 条备选（传入 scope_code、传入 scenario_id、省略 limit）；每个参数 1 条非法反向
- [x] unavailable（效果推演）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 双接口页清单用例 2 条：预期写明下拉共 2 项且可切换；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00709～00724
- [x] A 线写无对应 Lxx（catalog_skip）

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **16** 条；主流程 **2**、备选 **6**、反向 **6**、清单 **2**；编号闭区间 **FUNC-00709**～**FUNC-00724**（R3-批12 policy.simulate）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **16** |
| 编号闭区间 | **FUNC-00709**～**FUNC-00724** |
| 接口向（不含清单） | **14** |
| 主流程 | **2** |
| 备选-参数组合 | **6** |
| 反向 | **6** |
| 清单 | **2** |
| 已删 API 册 | `API-效果推演·实施路径-用例.md`（API-01489～01502 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
