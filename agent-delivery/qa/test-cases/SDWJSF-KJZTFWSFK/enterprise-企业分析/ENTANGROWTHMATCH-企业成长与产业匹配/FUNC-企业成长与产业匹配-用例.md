# 智能服务集群-科技专题服务算法库测试用例（企业成长与产业匹配 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=entan.growth-match` · `catalog_page_id=entan.growth-match` · path `#/entan/growth-match`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.growth-match`  
> **A 线对照**：无对应 Lxx（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `entan.growth-match`，原因「不扩六级」；不改 `work/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批5；金样 CHAINBASIC）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 成长潜力（企业集合） | entan.growth-match.potential |
| 2 | 产业匹配度（企业集合） | entan.growth-match.match |
| 3 | M_ENT_AGGLOMERATION_INDEX | entan.growth-match.potential.m_ent_agglomeration_index |
| 4 | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | entan.growth-match.potential.m_ent_ds_07_industry_potential_006 |

**enterprise_codes 试调取值**：文档 `sampleRequest` 四元组 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（可替换为环境有效企业标识）。本页 4 个接口均仅 1 个必填参数 `enterprise_codes`，无可选参数。`entan.growth-match.potential` / `match` 的 catalog `status=unavailable`，仍按文档请求与返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00332**～**FUNC-00341**，共 **10** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.growth-match`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00332 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | 成长潜力（企业集合） | 验证成长潜力（企业集合）功能，检查填写 enterprise_codes 查询后返回成长潜力得分及三维维度等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes 使用文档 sampleRequest 四元组 | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.切换至「算法测试」tab；3.接口下拉选择「成长潜力（企业集合）」；4.填写 enterprise_codes=[0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299]，点击调用 | 1、返回面板含 metric_id（string，示例 M_ENT_GROWTH_POTENTIAL）、metric_name_zh（string，示例成长潜力）；2、value 为 object，内含 value（number，示例 72.5）、dimensions（object：market_expand number 示例 68.0、profit_growth number 示例 74.0、asset_accumulate number 示例 76.0）、hint（string，示例 mock 阶段数据，三维等权重与行业均值比较（Q015 待补））；3、data_source（string，示例 mock）、confidence（string，示例 medium）；4、calc_process 为 object，含 definition（string，示例成长潜力）、formula（string，示例市场扩张/利润增长/资产积累三维等权）、source_tables（string 数组，示例含成长潜力缺口表）、model_version（string，示例 entan-v1.0）；5、responseFields 声明 value 为 number（成长潜力得分），与 sampleResponse 结构一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | M_ENT_GROWTH_POTENTIAL | INTEG |  | FUNC-00332 | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=POT-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00333 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | 成长潜力（企业集合） | 验证成长潜力（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.切换至「算法测试」tab；3.接口下拉选择「成长潜力（企业集合）」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 metric_id 为 M_ENT_GROWTH_POTENTIAL 且带 value 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute |  | INTEG |  | FUNC-00333 | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=POT-02 catalog_status=unavailable 场景=异常-入参-缺enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00334 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | 产业匹配度（企业集合） | 验证产业匹配度（企业集合）功能，检查填写 enterprise_codes 查询后返回产业匹配度及上游度等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes 使用文档 sampleRequest 四元组 | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.切换至「算法测试」tab；3.接口下拉选择「产业匹配度（企业集合）」；4.填写 enterprise_codes 同 POT-01 四元组，点击调用 | 1、返回面板含 metric_id（string，示例 M_ENT_INDUSTRY_MATCH_SCORE）、metric_name_zh（string，示例产业匹配度）；2、value 为 object，内含 value（number，示例 0.82）、upstream_degree（number，示例 2.4）、centroid_degree（number，示例 0.71）、chain_relevance（number，示例 1.15）、hint（string，示例 mock 阶段数据，依赖投入产出表上游度/质心度（Q015 待补））；3、data_source（string，示例 mock）、confidence（string，示例 medium）；4、calc_process 为 object，含 definition（string，示例产业匹配度）、formula（string，示例上游度/质心度/产业链相关性）、source_tables（string 数组，示例含投入产出表）、model_version（string，示例 entan-v1.0）；5、responseFields 声明 value 为 number（产业匹配度），与 sampleResponse 结构一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | M_ENT_INDUSTRY_MATCH_SCORE | INTEG |  | FUNC-00334 | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=MAT-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00335 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | 产业匹配度（企业集合） | 验证产业匹配度（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.切换至「算法测试」tab；3.接口下拉选择「产业匹配度（企业集合）」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 metric_id 为 M_ENT_INDUSTRY_MATCH_SCORE 且带 value 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute |  | INTEG |  | FUNC-00335 | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=MAT-02 catalog_status=unavailable 场景=异常-入参-缺enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00336 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | M_ENT_AGGLOMERATION_INDEX | 验证 M_ENT_AGGLOMERATION_INDEX 功能，检查填写 enterprise_codes 查询后返回 metric_id 与 hint 等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes 使用文档 sampleRequest 四元组 | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.切换至「算法测试」tab；3.接口下拉选择「M_ENT_AGGLOMERATION_INDEX」；4.填写 enterprise_codes 同 POT-01 四元组，点击调用 | 1、返回面板含 metric_id（string，示例 M_ENT_AGGLOMERATION_INDEX）、hint（string，示例 compute 响应,以实际调用为准）；2、responseFields 声明 value 为 number（成长潜力得分），sampleResponse 未给出 value 示例值，成功结果应出现 value 或可识别的计算结果体 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute | M_ENT_AGGLOMERATION_INDEX | INTEG |  | FUNC-00336 | endpoint_id=entan.growth-match.potential.m_ent_agglomeration_index catalog_page_id=entan.growth-match 组合=AGG-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00337 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | M_ENT_AGGLOMERATION_INDEX | 验证 M_ENT_AGGLOMERATION_INDEX 功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.切换至「算法测试」tab；3.接口下拉选择「M_ENT_AGGLOMERATION_INDEX」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 metric_id 为 M_ENT_AGGLOMERATION_INDEX 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute |  | INTEG |  | FUNC-00337 | endpoint_id=entan.growth-match.potential.m_ent_agglomeration_index catalog_page_id=entan.growth-match 组合=AGG-02 场景=异常-入参-缺enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00338 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | 验证 M_ENT_DS_07_INDUSTRY_POTENTIAL_006 功能，检查填写 enterprise_codes 查询后返回 metric_id 与 hint 等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes 使用文档 sampleRequest 四元组 | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.切换至「算法测试」tab；3.接口下拉选择「M_ENT_DS_07_INDUSTRY_POTENTIAL_006」；4.填写 enterprise_codes 同 POT-01 四元组，点击调用 | 1、返回面板含 metric_id（string，示例 M_ENT_DS_07_INDUSTRY_POTENTIAL_006）、hint（string，示例 compute 响应,以实际调用为准）；2、responseFields 声明 value 为 number（成长潜力得分），sampleResponse 未给出 value 示例值，成功结果应出现 value 或可识别的计算结果体 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | INTEG |  | FUNC-00338 | endpoint_id=entan.growth-match.potential.m_ent_ds_07_industry_potential_006 catalog_page_id=entan.growth-match 组合=IND-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00339 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | 验证 M_ENT_DS_07_INDUSTRY_POTENTIAL_006 功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.切换至「算法测试」tab；3.接口下拉选择「M_ENT_DS_07_INDUSTRY_POTENTIAL_006」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 metric_id 为 M_ENT_DS_07_INDUSTRY_POTENTIAL_006 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute |  | INTEG |  | FUNC-00339 | endpoint_id=entan.growth-match.potential.m_ent_ds_07_industry_potential_006 catalog_page_id=entan.growth-match 组合=IND-02 场景=异常-入参-缺enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00340 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | 接口信息 | 验证企业成长与产业匹配的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 4；2、下拉名称与 §0 各 title 一致；3、默认项概览 method=POST、path 为 /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute；4、切换后概览对应产业匹配度 POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00340 | catalog_page_id=entan.growth-match 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00341 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业成长与产业匹配模型 | 企业成长与产业匹配 | 算法测试 | 验证企业成长与产业匹配的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业成长与产业匹配」；2.切换到「算法测试」tab；3.下拉切换到「M_ENT_AGGLOMERATION_INDEX」 | 1、算法测试 tab 下拉共 4 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「M_ENT_AGGLOMERATION_INDEX」；3、调用区 method 为 POST、path 为 /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00341 | catalog_page_id=entan.growth-match 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| POT-01 | entan.growth-match.potential | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| POT-02 | entan.growth-match.potential | 不传 enterprise_codes | 缺必填 enterprise_codes |
| MAT-01 | entan.growth-match.match | enterprise_codes 同 POT-01 四元组 | 主路径全参（sampleRequest） |
| MAT-02 | entan.growth-match.match | 不传 enterprise_codes | 缺必填 enterprise_codes |
| AGG-01 | entan.growth-match.potential.m_ent_agglomeration_index | enterprise_codes 同 POT-01 四元组 | 主路径全参（sampleRequest） |
| AGG-02 | entan.growth-match.potential.m_ent_agglomeration_index | 不传 enterprise_codes | 缺必填 enterprise_codes |
| IND-01 | entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | enterprise_codes 同 POT-01 四元组 | 主路径全参（sampleRequest） |
| IND-02 | entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | 不传 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 成长潜力（企业集合） | entan.growth-match.potential | POST | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | enterprise_codes* | unavailable |
| 产业匹配度（企业集合） | entan.growth-match.match | POST | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | enterprise_codes* | unavailable |
| M_ENT_AGGLOMERATION_INDEX | entan.growth-match.potential.m_ent_agglomeration_index | POST | /entan/v1/entan/metric/M_ENT_AGGLOMERATION_INDEX/compute | enterprise_codes* | available |
| M_ENT_DS_07_INDUSTRY_POTENTIAL_006 | entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | POST | /entan/v1/entan/metric/M_ENT_DS_07_INDUSTRY_POTENTIAL_006/compute | enterprise_codes* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.growth-match.potential | FUNC-00332、00333 |
| entan.growth-match.match | FUNC-00334、00335 |
| entan.growth-match.potential.m_ent_agglomeration_index | FUNC-00336、00337 |
| entan.growth-match.potential.m_ent_ds_07_industry_potential_006 | FUNC-00338、00339 |
| （页面清单） | FUNC-00340、00341 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 4 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 有参接口：文档示例全参正向；每接口必填 `enterprise_codes` 恰好 1 条反向；无可选参数，无备选-参数组合
- [x] unavailable（成长潜力、产业匹配度）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 企业深度分析模型构建 / 企业成长与产业匹配模型
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 页面清单用例 2 条：页头 4 个接口；切换后概览/调用区刷新
- [x] `coverage-fp.md` 已同步 FUNC-00332～00341

**统计**：接口 **4**；主流程 **4**；反向 **4**；清单 **2**；合计 **10** 条；编号闭区间 **FUNC-00332**～**FUNC-00341**（父控 R3-批5 · entan.growth-match 分配）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **10** |
| 编号闭区间 | **FUNC-00332**～**FUNC-00341** |
| 接口向（不含清单） | **8** |
| 主流程 | **4** |
| 反向 | **4** |
| 清单 | **2** |
| 已删 API 册 | `API-企业成长与产业匹配-用例.md`（API-01149～01156 作废，不复用） |
| 鉴权用例 | **0** |
