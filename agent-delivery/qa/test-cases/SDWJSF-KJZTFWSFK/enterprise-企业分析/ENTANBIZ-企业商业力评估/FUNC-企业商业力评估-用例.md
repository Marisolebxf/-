# 智能服务集群-科技专题服务算法库测试用例（企业商业力评估 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业商业力评估  
> **catalog**：`entry_id=entan.biz` · `catalog_page_id=entan.biz` · path `#/entan/biz`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **A 线对照**：`fp-split-by-api-run/work/L32.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批3；金样 CHAINBASIC）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 企业商业力得分（企业集合） | entan.biz.rank |
| 2 | 商业力详情 | entan.biz.detail |
| 3 | 模型权重 | entan.biz.weights |
| 4 | 评估报告 | entan.biz.report |

**试调取值**（catalog `sampleRequest` / `example`）：`enterprise_codes` 四元组 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`；`orgId` 为 `0218337e44ca794fee9850cf1627b03b`；`model` 为 `biz_power`。四接口 `status=unavailable`，仍按文档请求与 sampleResponse 编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00143**～**FUNC-00152**，共 **10** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.biz`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00143 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 企业商业力得分（企业集合） | 验证企业商业力得分（企业集合）功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回商业力得分明细字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「企业商业力评估」；2.接口下拉选择「企业商业力得分（企业集合）」；3.填写 enterprise_codes=[0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299]，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 示例 M_ENT_BUSINESS_POWER_SCORE）、metric_name_zh（string，示例企业商业力得分）；2、value 为 object，value.enterprises 为 array（responseFields 企业商业力得分明细）；3、元素含 org_id（string）、enterprise_name（string）、biz_power_index（number）、market_score（number）、product_score（number）、brand_score（number）、cooperation_score（number）、chain_coverage_score（number）、chain_keynode_score（number）；4、含 data_source（string）、confidence（string）；5、calc_process 为 object，含 definition（string）、formula（string）、source_tables（array）、model_version（string） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | M_ENT_BUSINESS_POWER_SCORE | INTEG |  |  | endpoint_id=entan.biz.rank catalog_page_id=entan.biz 组合=RNK-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00144 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 企业商业力得分（企业集合） | 验证企业商业力得分（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业商业力评估」；2.接口下拉选择「企业商业力得分（企业集合）」；3.填写 清空 enterprise_codes 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 biz_power_index 与 enterprises 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute |  | INTEG |  |  | endpoint_id=entan.biz.rank catalog_page_id=entan.biz 组合=RNK-02 场景=异常-入参-缺enterprise_codes catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00145 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 商业力详情 | 验证商业力详情功能，检查填写 chainId=INB1701 orgId 查询后返回六维得分与趋势字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、orgId=0218337e44ca794fee9850cf1627b03b | 1.侧栏进入「企业分析」→「企业商业力评估」；2.接口下拉选择「商业力详情」；3.填写 orgId=0218337e44ca794fee9850cf1627b03b，点击调用 | 1、返回面板含 market_score（number，responseFields 市场得分）、product_score（number）、brand_score（number）、cooperation_score（number）、chain_coverage_score（number）、chain_keynode_score（number）；2、trend 为 array，元素含 year（number）、value（number）；3、与 sampleResponse 一致（示例 market_score=90、product_score=88、brand_score=82、cooperation_score=79、chain_coverage_score=84、chain_keynode_score=76、year=2024、value=86） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/biz-power/{orgId} | M_ENT_BUSINESS_POWER_SCORE | INTEG |  |  | endpoint_id=entan.biz.detail catalog_page_id=entan.biz 组合=DTL-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00146 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 商业力详情 | 验证商业力详情功能，检查不传 orgId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业商业力评估」；2.接口下拉选择「商业力详情」；3.填写 清空 orgId 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 orgId；2、不返回含 market_score 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/biz-power/{orgId} |  | INTEG |  |  | endpoint_id=entan.biz.detail catalog_page_id=entan.biz 组合=DTL-02 场景=异常-入参-缺orgId catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00147 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 模型权重 | 验证模型权重功能，检查填写 chainId=INB1701 model=biz_power 查询后返回权重表字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、model=biz_power | 1.侧栏进入「企业分析」→「企业商业力评估」；2.接口下拉选择「模型权重」；3.填写 model=biz_power，点击调用 | 1、返回面板中 data 为数组（sampleResponse 即为数组形态）；2、元素含 name_zh（string）、weight（number，responseFields 权重）、description（string）；3、与 sampleResponse 一致（示例 name_zh=市场、weight=0.22、description=市场份额） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | M_ENT_BUSINESS_POWER_SCORE | INTEG |  |  | endpoint_id=entan.biz.weights catalog_page_id=entan.biz 组合=WGT-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00148 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 模型权重 | 验证模型权重功能，检查不传 model 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业商业力评估」；2.接口下拉选择「模型权重」；3.填写 清空 model 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 model；2、不返回含 weight 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights |  | INTEG |  |  | endpoint_id=entan.biz.weights catalog_page_id=entan.biz 组合=WGT-02 场景=异常-入参-缺model catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00149 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 评估报告 | 验证评估报告功能，检查填写 chainId=INB1701 orgId 查询后返回报告正文字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、orgId=0218337e44ca794fee9850cf1627b03b | 1.侧栏进入「企业分析」→「企业商业力评估」；2.接口下拉选择「评估报告」；3.填写 orgId=0218337e44ca794fee9850cf1627b03b，点击调用 | 1、返回面板含 markdown（string，responseFields 报告正文）；2、与 sampleResponse 一致（示例 markdown 为商业力评估报告标题文本） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | M_ENT_BUSINESS_POWER_SCORE | INTEG |  |  | endpoint_id=entan.biz.report catalog_page_id=entan.biz 组合=RPT-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00150 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 评估报告 | 验证评估报告功能，检查不传 orgId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业商业力评估」；2.接口下拉选择「评估报告」；3.填写 清空 orgId 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 orgId；2、不返回含 markdown 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report |  | INTEG |  |  | endpoint_id=entan.biz.report catalog_page_id=entan.biz 组合=RPT-02 场景=异常-入参-缺orgId catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00151 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 接口信息 | 验证企业商业力评估的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业商业力评估」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 4；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应企业商业力得分 POST /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute；4、切换后概览对应商业力详情 GET /entan/v1/biz-power/{orgId}，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=entan.biz 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00152 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业商业力评估模型 | 企业商业力评估 | 算法测试 | 验证企业商业力评估的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业商业力评估」；2.切换到「算法测试」tab；3.下拉切换到「模型权重」 | 1、算法测试 tab 下拉共 4 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「模型权重」；3、调用区 method 为 GET、path 为 /entan/v1/eval/weights；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=entan.biz 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RNK-01 | entan.biz.rank | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| RNK-02 | entan.biz.rank | 清空 enterprise_codes 入参 | 缺必填 enterprise_codes |
| DTL-01 | entan.biz.detail | orgId=0218337e44ca794fee9850cf1627b03b | 主路径（sampleRequest） |
| DTL-02 | entan.biz.detail | 清空 orgId 入参 | 缺必填 orgId |
| WGT-01 | entan.biz.weights | model=biz_power | 主路径（sampleRequest） |
| WGT-02 | entan.biz.weights | 清空 model 入参 | 缺必填 model |
| RPT-01 | entan.biz.report | orgId=0218337e44ca794fee9850cf1627b03b | 主路径（sampleRequest） |
| RPT-02 | entan.biz.report | 清空 orgId 入参 | 缺必填 orgId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 企业商业力得分（企业集合） | entan.biz.rank | POST | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | enterprise_codes* | unavailable |
| 商业力详情 | entan.biz.detail | GET | /entan/v1/biz-power/{orgId} | orgId* | unavailable |
| 模型权重 | entan.biz.weights | GET | /entan/v1/eval/weights | model* | unavailable |
| 评估报告 | entan.biz.report | GET | /entan/v1/enterprises/{orgId}/report | orgId* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.biz.rank | FUNC-00143、00144 |
| entan.biz.detail | FUNC-00145、00146 |
| entan.biz.weights | FUNC-00147、00148 |
| entan.biz.report | FUNC-00149、00150 |
| （页面清单） | FUNC-00151、00152 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 4 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 有参接口：文档示例全参正向；每接口必填参数恰好 1 条反向；无可选参数，无备选-参数组合
- [x] unavailable 四接口仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 企业深度分析模型构建 / 企业商业力评估模型
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00143～00152

**统计**：接口 **4**；主流程 **4**；反向 **4**；清单 **2**；合计 **10** 条；编号闭区间 **FUNC-00143**～**FUNC-00152**（父控 R3-批3 · entan.biz 分配）。
