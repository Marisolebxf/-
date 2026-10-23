# 智能服务集群-科技专题服务算法库测试用例（企业技术力评估 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业技术力评估  
> **catalog**：`entry_id=entan.tech` · `catalog_page_id=entan.tech` · path `#/entan/tech`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **A 线对照**：`fp-split-by-api-run/work/L31.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批3；金样 CHAINBASIC）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 企业技术力得分（企业集合） | entan.tech.rank |
| 2 | 技术力详情 | entan.tech.detail |
| 3 | 模型权重 | entan.tech.weights |
| 4 | 评估报告 | entan.tech.report |
| 5 | 技术影响力评估 | entan.tech.rank.m_ent_ds_07_industry_potential_005 |

**试调取值**（catalog `sampleRequest`）：`enterprise_codes` 为 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`；`orgId` 为 `0218337e44ca794fee9850cf1627b03b`；`model` 为 `tech_power`。

本页 JSON 共 **5** 个 endpoint。每个接口仅 1 个必填参数、无可选参数：1 条主流程 + 1 条反向。`entan.tech.rank` / `detail` / `weights` / `report` 的 catalog `status=unavailable`，仍按文档请求与返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00131**～**FUNC-00142**，共 **12** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.tech`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00131 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 企业技术力得分（企业集合） | 验证企业技术力得分（企业集合）功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回技术力指数及五维得分等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes 使用文档 sampleRequest 四条标识 | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「企业技术力得分（企业集合）」；4.填写 enterprise_codes=[0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299]，点击调用 | 1、返回面板含 metric_id（string）、metric_name_zh（string）、data_source（string）、confidence（string）；2、value 为 object，其中 enterprises 为 array（responseFields 企业技术力得分明细）；3、元素含 org_id（string）、enterprise_name（string）、tech_power_index（number）、talent_score（number）、innovation_score（number）、transfer_score（number）、cooperation_score（number）、investment_score（number）；4、calc_process 含 definition（string）、formula（string）、source_tables（string 数组）、model_version（string）；5、与 sampleResponse 一致（示例 metric_id=M_ENT_TECH_POWER_SCORE，metric_name_zh=企业技术力得分，data_source=real，confidence=high，formula=五维加权，model_version=entan-v1.0） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | M_ENT_TECH_POWER_SCORE | INTEG |  | FUNC-00131 | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=RANK-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00132 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 企业技术力得分（企业集合） | 验证企业技术力得分（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「企业技术力得分（企业集合）」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含 tech_power_index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute |  | INTEG |  | FUNC-00132 | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=RANK-02 catalog_status=unavailable 场景=异常-入参-缺enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00133 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 技术力详情 | 验证技术力详情功能，检查填写 chainId=INB1701 orgId 查询后返回五维得分与年度趋势字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、orgId=0218337e44ca794fee9850cf1627b03b | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「技术力详情」；4.填写 orgId=0218337e44ca794fee9850cf1627b03b，点击调用 | 1、返回面板含 org_id（string）、enterprise_name（string）、talent_score（number，responseFields 人才得分）、innovation_score（number）、transfer_score（number）、cooperation_score（number）、investment_score（number）；2、trend 为 array（responseFields 年度趋势），元素含 year（number）、value（number）；3、与 sampleResponse 一致（示例 org_id=0218337e44ca794fee9850cf1627b03b，trend 含 year 2023/2024/2025） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/tech-power/{orgId} | M_ENT_TECH_POWER_SCORE | INTEG |  | FUNC-00133 | endpoint_id=entan.tech.detail catalog_page_id=entan.tech 组合=DTL-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00134 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 技术力详情 | 验证技术力详情功能，检查不传 orgId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「技术力详情」；4.不传 orgId，点击调用（不传 orgId），点击调用 | 1、返回面板的 message 或 msg 说明 orgId 缺失或非法；2、不返回含 talent_score 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/tech-power/{orgId} |  | INTEG |  | FUNC-00134 | endpoint_id=entan.tech.detail catalog_page_id=entan.tech 组合=DTL-02 catalog_status=unavailable 场景=异常-入参-缺orgId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00135 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 模型权重 | 验证模型权重功能，检查填写 chainId=INB1701 model 查询后返回权重配置字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、model=tech_power | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「模型权重」；4.填写 model=tech_power，点击调用 | 1、返回面板为 array；2、元素含 name_zh（string）、weight（number，responseFields 权重）、description（string）；3、与 sampleResponse 一致（示例 name_zh=技术创新，weight=0.28，description=专利与论文） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | M_ENT_TECH_POWER_SCORE | INTEG |  | FUNC-00135 | endpoint_id=entan.tech.weights catalog_page_id=entan.tech 组合=WGT-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00136 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 模型权重 | 验证模型权重功能，检查不传 model 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「模型权重」；4.不传 model，点击调用（不传 model），点击调用 | 1、返回面板的 message 或 msg 说明 model 缺失或非法；2、不返回含 weight 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights |  | INTEG |  | FUNC-00136 | endpoint_id=entan.tech.weights catalog_page_id=entan.tech 组合=WGT-02 catalog_status=unavailable 场景=异常-入参-缺model |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00137 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 评估报告 | 验证评估报告功能，检查填写 chainId=INB1701 orgId 查询后返回 Markdown 报告正文 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、orgId=0218337e44ca794fee9850cf1627b03b | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「评估报告」；4.填写 orgId=0218337e44ca794fee9850cf1627b03b，点击调用 | 1、返回面板含 markdown（string，responseFields 报告正文）；2、与 sampleResponse 一致（示例 markdown 为「# 技术力评估报告」） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | M_ENT_TECH_POWER_SCORE | INTEG |  | FUNC-00137 | endpoint_id=entan.tech.report catalog_page_id=entan.tech 组合=RPT-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00138 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 评估报告 | 验证评估报告功能，检查不传 orgId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「评估报告」；4.不传 orgId，点击调用（不传 orgId），点击调用 | 1、返回面板的 message 或 msg 说明 orgId 缺失或非法；2、不返回含 markdown 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report |  | INTEG |  | FUNC-00138 | endpoint_id=entan.tech.report catalog_page_id=entan.tech 组合=RPT-02 catalog_status=unavailable 场景=异常-入参-缺orgId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00139 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 技术影响力评估 | 验证技术影响力评估功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回 metric_id 与 hint 等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes 使用文档 sampleRequest 四条标识 | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「技术影响力评估」；4.填写 enterprise_codes=[0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299]，点击调用 | 1、返回面板含 metric_id（string）、hint（string）；2、responseFields 另声明 enterprises（array，企业技术力得分明细），sampleResponse 未展开元素字段，成功结果应含 enterprises 或可识别的计算结果体；3、示例来自 sampleResponse：metric_id=M_ENT_DS_07_INDUSTRY_POTENTIAL_005，hint=compute 响应,以实际调用为准 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute | M_ENT_DS_07_INDUSTRY_POTENTIAL_005 | INTEG |  | FUNC-00139 | endpoint_id=entan.tech.rank.m_ent_ds_07_industry_potential_005 catalog_page_id=entan.tech 组合=INF-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00140 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 技术影响力评估 | 验证技术影响力评估功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「技术影响力评估」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含 metric_id 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute |  | INTEG |  | FUNC-00140 | endpoint_id=entan.tech.rank.m_ent_ds_07_industry_potential_005 catalog_page_id=entan.tech 组合=INF-02 场景=异常-入参-缺enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00141 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 接口信息 | 验证企业技术力评估的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业技术力评估」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 5；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应企业技术力得分（企业集合） POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute；4、切换后概览对应技术力详情 GET /entan/v1/tech-power/{orgId}，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00141 | catalog_page_id=entan.tech 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00142 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业技术力评估模型 | 企业技术力评估 | 算法测试 | 验证企业技术力评估的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业技术力评估」；2.切换到「算法测试」tab；3.下拉切换到「评估报告」 | 1、算法测试 tab 下拉共 5 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「评估报告」；3、调用区 method 为 GET、path 为 /entan/v1/enterprises/{orgId}/report；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00142 | catalog_page_id=entan.tech 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RANK-01 | entan.tech.rank | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| RANK-02 | entan.tech.rank | 不传 enterprise_codes | 缺必填 enterprise_codes |
| DTL-01 | entan.tech.detail | orgId=0218337e44ca794fee9850cf1627b03b | 主路径（sampleRequest） |
| DTL-02 | entan.tech.detail | 不传 orgId | 缺必填 orgId |
| WGT-01 | entan.tech.weights | model=tech_power | 主路径（sampleRequest） |
| WGT-02 | entan.tech.weights | 不传 model | 缺必填 model |
| RPT-01 | entan.tech.report | orgId=0218337e44ca794fee9850cf1627b03b | 主路径（sampleRequest） |
| RPT-02 | entan.tech.report | 不传 orgId | 缺必填 orgId |
| INF-01 | entan.tech.rank.m_ent_ds_07_industry_potential_005 | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| INF-02 | entan.tech.rank.m_ent_ds_07_industry_potential_005 | 不传 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 企业技术力得分（企业集合） | entan.tech.rank | POST | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | enterprise_codes* | unavailable |
| 技术力详情 | entan.tech.detail | GET | /entan/v1/tech-power/{orgId} | orgId* | unavailable |
| 模型权重 | entan.tech.weights | GET | /entan/v1/eval/weights | model* | unavailable |
| 评估报告 | entan.tech.report | GET | /entan/v1/enterprises/{orgId}/report | orgId* | unavailable |
| 技术影响力评估 | entan.tech.rank.m_ent_ds_07_industry_potential_005 | POST | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_005/compute | enterprise_codes* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.tech.rank | FUNC-00131、00132 |
| entan.tech.detail | FUNC-00133、00134 |
| entan.tech.weights | FUNC-00135、00136 |
| entan.tech.report | FUNC-00137、00138 |
| entan.tech.rank.m_ent_ds_07_industry_potential_005 | FUNC-00139、00140 |
| （页面清单） | FUNC-00141、00142 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 5 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 有参接口：文档示例正向 + 每参数恰好 1 条反向（本页均为单必填、无可选，无备选-参数组合）
- [x] unavailable（得分集合、详情、权重、报告）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 企业深度分析模型构建 / 企业技术力评估模型
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 页面清单用例 2 条：页头 5 个接口；切换后概览/调用区刷新
- [x] `coverage-fp.md` 已同步 FUNC-00131～00142

**统计**：接口 **5**；主流程 **5**；反向 **5**；清单 **2**；合计 **12** 条；编号闭区间 **FUNC-00131**～**FUNC-00142**（父控 R3-批3 分配，连续无跳号）。
