# 智能服务集群-科技专题服务算法库测试用例（政策匹配推送 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=policy.match` · `catalog_page_id=policy.match` · path `#/policy/match`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.match`  
> **A 线对照**：**无对应 Lxx**（`_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `policy.match`，原因：不扩六级；不改 `work/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批12）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 政策匹配 | policy.match.main | unavailable |
| 2 | 政策匹配推送 | policy.match.m_policy_match | available |

两个接口的可选参数相同：`subject_id`、`subject_type`、`limit`。`sampleRequest` 均为 `subject_type=enterprise`、`limit=20`，不含 `subject_id`。主流程对齐该 sample；备选各 1 条与 sample 相反（传入 `subject_id=E0001`、省略 `subject_type`、省略 `limit`）。反向各 1 条非法，不把省略写成反向。`政策匹配` 为 unavailable，仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00693**～**FUNC-00708**，共 **16** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.match`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00693 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配 | 验证政策匹配功能，检查填写 sampleRequest 所示参数 传 subject_type=enterprise、limit=20、不传 subject_id 时返回匹配字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、subject_type=enterprise；limit=20；不传 subject_id（对齐 sampleRequest） | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id，填写 subject_type=enterprise、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素含 rank_no（number）、subject_name（string）、policy_title（string）、match_score（number，responseFields 匹配分）、metric_id（string）；3、与 sampleResponse 逐字段一致，示例 rank_no=1、subject_name=示例企业、policy_title=示例政策、match_score=75、metric_id=M_POLICY_MATCH | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG |  |  | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00694 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配 | 验证政策匹配功能，检查传入可选 subject_id=E0001，subject_type 与 limit 保持 sampleRequest 时仍返回匹配字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、subject_id=E0001；subject_type=enterprise；limit=20 | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.填写 subject_id=E0001、subject_type=enterprise、limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 rank_no（number）、subject_name（string）、policy_title（string）、match_score（number，responseFields 匹配分）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（如 rank_no=1、subject_name=示例企业、policy_title=示例政策、match_score=75、metric_id=M_POLICY_MATCH）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG |  |  | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00695 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配 | 验证政策匹配功能，检查不传可选 subject_type，limit 保持 sample 的 20、不传 subject_id 时仍返回匹配字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 subject_id；不传 subject_type；limit=20 | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id、不传 subject_type，填写 limit=20，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 rank_no（number）、subject_name（string）、policy_title（string）、match_score（number，responseFields 匹配分）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（如 match_score=75、subject_name=示例企业、policy_title=示例政策）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG |  |  | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00696 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配 | 验证政策匹配功能，检查不传可选 limit，subject_type 保持 sample 的 enterprise、不传 subject_id 时仍返回匹配字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 subject_id；subject_type=enterprise；不传 limit | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id、不传 limit，填写 subject_type=enterprise，点击调用 | 1、返回面板 body 的 data 为数组；2、元素仍含 rank_no（number）、subject_name（string）、policy_title（string）、match_score（number，responseFields 匹配分）、metric_id（string）；3、字段与 sampleResponse 逐字段同类，示例值（如 match_score=75、rank_no=1、metric_id=M_POLICY_MATCH）说明形态 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG |  |  | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-04 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00697 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配 | 验证政策匹配功能，检查 subject_id 非法，subject_type 与 limit 保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、subject_type=enterprise；limit=20 | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.填写 subject_id=__invalid__、subject_type=enterprise、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 subject_id 非法；2、不返回含 match_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  |  | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-05 场景=异常-入参-非法subject_id catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00698 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配 | 验证政策匹配功能，检查 subject_type 枚举外非法、limit 保持合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 subject_id；limit=20 | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id，填写 subject_type=__invalid__（不在空、enterprise、user）、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 subject_type 非法；2、不返回含 match_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  |  | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-06 场景=异常-入参-非法subject_type catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00699 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配 | 验证政策匹配功能，检查 limit 非法、subject_type 保持文档合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 subject_id；subject_type=enterprise | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配」；4.不传 subject_id，填写 subject_type=enterprise、limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 match_score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match |  | INTEG |  |  | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MAT-07 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00700 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配推送 | 验证政策匹配推送功能，检查填写 sampleRequest 所示参数 提交 subject_type=enterprise、limit=20、不传 subject_id 后返回计算字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、请求体 subject_type=enterprise；limit=20；不传 subject_id（对齐 sampleRequest） | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配推送」；4.不传 subject_id，填写 subject_type=enterprise、limit=20，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_POLICY_MATCH）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 另含 match_score（number，匹配分） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | M_POLICY_MATCH | INTEG |  |  | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00701 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配推送 | 验证政策匹配推送功能，检查传入可选 subject_id=E0001，subject_type 与 limit 保持 sampleRequest 时仍返回计算字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、请求体 subject_id=E0001；subject_type=enterprise；limit=20 | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配推送」；4.填写 subject_id=E0001、subject_type=enterprise、limit=20，点击调用 | 1、返回面板 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_MATCH）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 match_score 为 number（匹配分） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | M_POLICY_MATCH | INTEG |  |  | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00702 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配推送 | 验证政策匹配推送功能，检查不传可选 subject_type，limit 保持 sample 的 20、不传 subject_id 时仍返回计算字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 subject_id；不传 subject_type；limit=20 | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配推送」；4.不传 subject_id、不传 subject_type，填写 limit=20，点击调用 | 1、返回面板 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_MATCH）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 match_score 为 number（匹配分） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | M_POLICY_MATCH | INTEG |  |  | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-03 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00703 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配推送 | 验证政策匹配推送功能，检查不传可选 limit，subject_type 保持 sample 的 enterprise、不传 subject_id 时仍返回计算字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 subject_id；subject_type=enterprise；不传 limit | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配推送」；4.不传 subject_id、不传 limit，填写 subject_type=enterprise，点击调用 | 1、返回面板 body 为对象；2、仍含 metric_id（string，示例 M_POLICY_MATCH）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 match_score 为 number（匹配分） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute | M_POLICY_MATCH | INTEG |  |  | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-04 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00704 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配推送 | 验证政策匹配推送功能，检查 subject_id 非法，subject_type 与 limit 保持文档合法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、请求体 subject_type=enterprise；limit=20 | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配推送」；4.填写 subject_id=__invalid__、subject_type=enterprise、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 subject_id 非法；2、不返回含 metric_id 或 match_score 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute |  | INTEG |  |  | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-05 场景=异常-入参-非法subject_id catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00705 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配推送 | 验证政策匹配推送功能，检查 subject_type 枚举外非法、limit 保持合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 subject_id；limit=20 | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配推送」；4.不传 subject_id，填写 subject_type=__invalid__（不在空、enterprise、user）、limit=20，点击调用 | 1、返回面板的 message 或 msg 指出 subject_type 非法；2、不返回含 metric_id 或 match_score 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute |  | INTEG |  |  | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-06 场景=异常-入参-非法subject_type catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00706 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 政策匹配推送 | 验证政策匹配推送功能，检查 limit 非法、subject_type 保持文档合法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 subject_id；subject_type=enterprise | 1.侧栏进入「政策分析」→「匹配推送」；2.切换至「算法测试」tab；3.接口下拉选择「政策匹配推送」；4.不传 subject_id，填写 subject_type=enterprise、limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 metric_id 或 match_score 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/polan/metric/M_POLICY_MATCH/compute |  | INTEG |  |  | endpoint_id=policy.match.m_policy_match catalog_page_id=policy.match 组合=PSH-07 场景=异常-入参-非法limit catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00707 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 接口信息 | 验证匹配推送的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「匹配推送」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（政策匹配、政策匹配推送）；3、默认项概览 method=GET、path=/policy/v1/policy/match；4、切换后概览对应政策匹配推送 POST /policy/v1/polan/metric/M_POLICY_MATCH/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=policy.match 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00708 | 算法工具库 | 科技专题服务算法库 | 主体政策匹配推送 | 匹配推送 | 匹配推送 | 算法测试 | 验证匹配推送的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「匹配推送」；2.切换到「算法测试」tab；3.下拉切换到「政策匹配推送」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「政策匹配推送」；3、调用区 method 为 POST、path 为 /policy/v1/polan/metric/M_POLICY_MATCH/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=policy.match 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MAT-01 | policy.match.main | subject_type=enterprise；不传 subject_id；limit=20 | 主路径（sampleRequest） |
| MAT-02 | policy.match.main | subject_id=E0001；subject_type=enterprise；limit=20 | 与 sample 相反：传入可选 subject_id |
| MAT-03 | policy.match.main | 不传 subject_id；不传 subject_type；limit=20 | 与 sample 相反：省略可选 subject_type |
| MAT-04 | policy.match.main | 不传 subject_id；subject_type=enterprise；不传 limit | 与 sample 相反：省略可选 limit |
| MAT-05 | policy.match.main | subject_id=__invalid__；subject_type=enterprise；limit=20 | 只破坏 subject_id |
| MAT-06 | policy.match.main | 不传 subject_id；subject_type=__invalid__（不在空、enterprise、user）；limit=20 | 只破坏 subject_type |
| MAT-07 | policy.match.main | 不传 subject_id；subject_type=enterprise；limit=-1 | 只破坏 limit |
| PSH-01 | policy.match.m_policy_match | subject_type=enterprise；不传 subject_id；limit=20 | 主路径（sampleRequest） |
| PSH-02 | policy.match.m_policy_match | subject_id=E0001；subject_type=enterprise；limit=20 | 与 sample 相反：传入可选 subject_id |
| PSH-03 | policy.match.m_policy_match | 不传 subject_id；不传 subject_type；limit=20 | 与 sample 相反：省略可选 subject_type |
| PSH-04 | policy.match.m_policy_match | 不传 subject_id；subject_type=enterprise；不传 limit | 与 sample 相反：省略可选 limit |
| PSH-05 | policy.match.m_policy_match | subject_id=__invalid__；subject_type=enterprise；limit=20 | 只破坏 subject_id |
| PSH-06 | policy.match.m_policy_match | 不传 subject_id；subject_type=__invalid__（不在空、enterprise、user）；limit=20 | 只破坏 subject_type |
| PSH-07 | policy.match.m_policy_match | 不传 subject_id；subject_type=enterprise；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 政策匹配 | policy.match.main | GET | /policy/v1/policy/match | subject_id?；subject_type?；limit? | unavailable |
| 政策匹配推送 | policy.match.m_policy_match | POST | /policy/v1/polan/metric/M_POLICY_MATCH/compute | subject_id?；subject_type?；limit? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.match.main | FUNC-00693、00694、00695、00696、00697、00698、00699 |
| policy.match.m_policy_match | FUNC-00700、00701、00702、00703、00704、00705、00706 |
| （页面清单） | FUNC-00707、00708 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title「政策匹配」「政策匹配推送」均在功能点列出现，且各有 1 条 `场景=主流程`（FUNC-00693、FUNC-00700）
- [x] 每个接口：sample 主流程 1 条；与 sample 相反的传/不传各 1 条备选（传入 subject_id、省略 subject_type、省略 limit）；每个参数 1 条非法反向
- [x] unavailable（政策匹配）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 双接口页清单用例 2 条：预期写明下拉共 2 项且可切换；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00693～00708
- [x] A 线写无对应 Lxx（catalog_skip）

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **16** 条；主流程 **2**、备选 **6**、反向 **6**、清单 **2**；编号闭区间 **FUNC-00693**～**FUNC-00708**（R3-批12 policy.match）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **16** |
| 编号闭区间 | **FUNC-00693**～**FUNC-00708** |
| 接口向（不含清单） | **14** |
| 主流程 | **2** |
| 备选-参数组合 | **6** |
| 反向 | **6** |
| 清单 | **2** |
| 已删 API 册 | `API-政策匹配推送-用例.md`（API-01475～01488 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
