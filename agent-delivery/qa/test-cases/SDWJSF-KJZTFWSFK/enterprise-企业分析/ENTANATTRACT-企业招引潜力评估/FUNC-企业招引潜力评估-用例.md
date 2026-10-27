# 智能服务集群-科技专题服务算法库测试用例（企业招引潜力评估 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=entan.attract` · `catalog_page_id=entan.attract` · path `#/entan/attract`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **A 线对照**：`fp-split-by-api-run/work/L33.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批3）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 招引企业推荐指数（企业集合） | entan.attract.recommend | unavailable |
| 2 | 政策匹配度 | entan.attract.recommend.m_ent_policy_match_score | available |

**enterprise_codes 试调取值**：文档 `sampleRequest` 四元组 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（执行期可替换为环境有效企业标识，附录组合表引用该组）。

本页 2 个接口均只有必填 `enterprise_codes`，无可选参数。每接口 1 条主流程（sampleRequest 全参）+ 1 条反向（缺 `enterprise_codes`）。`recommend` 的 catalog `status=unavailable`，仍按文档返回体写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00153**～**FUNC-00158**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.attract`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00153 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 招引企业综合推荐模型 | 招引企业综合推荐 | 招引企业推荐指数（企业集合） | 验证招引企业推荐指数（企业集合）功能，检查填写 enterprise_codes 查询后返回招引推荐排名与权重等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「招引企业综合推荐」；2.接口下拉选择「招引企业推荐指数（企业集合）」；3.填写 enterprise_codes=[0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299]，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 示例 M_ENT_ATTRACTION_INDEX）、metric_name_zh（string，示例招引推荐指数）、data_source（string，示例 real）、confidence（string，示例 high）；2、value 为 object，value.result 含 sub_type（string，示例 attraction）、candidate_count（number，示例 2）；3、value.result.weights 含 technology_match（number，示例 40）、growth（number，示例 35）、regional_fit（number，示例 25）；4、value.result.rankings 为 array（responseFields 名 rankings，招引推荐清单），元素含 enterprise_code（string）、enterprise_name（string）、rank（number）、industry_domain（string）、geographic_source（string）、target_traits（string 数组）、recommendation_score（number）；5、calc_process 为 object，含 definition（string，示例招引推荐指数）、formula（string，示例技术匹配/成长性/区域适配加权）、source_tables（array）、model_version（string，示例 entan-v1.0） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | M_ENT_ATTRACTION_INDEX | INTEG |  | FUNC-00153 | endpoint_id=entan.attract.recommend catalog_page_id=entan.attract 组合=ATR-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00154 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 招引企业综合推荐模型 | 招引企业综合推荐 | 招引企业推荐指数（企业集合） | 验证招引企业推荐指数（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「招引企业综合推荐」；2.接口下拉选择「招引企业推荐指数（企业集合）」；3.填写 清空 enterprise_codes 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 recommendation_score 与 rankings 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute |  | INTEG |  | FUNC-00154 | endpoint_id=entan.attract.recommend catalog_page_id=entan.attract 组合=ATR-02 场景=异常-入参-缺enterprise_codes catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00155 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 招引企业综合推荐模型 | 招引企业综合推荐 | 政策匹配度 | 验证政策匹配度功能，检查填写 enterprise_codes 查询后返回 metric_id、hint 与 rankings 可定位 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「招引企业综合推荐」；2.接口下拉选择「政策匹配度」；3.填写 enterprise_codes 同 ATR-01，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 示例 M_ENT_POLICY_MATCH_SCORE）；2、含 hint（string，样例为 compute 响应说明，以实际调用为准）；3、responseFields 声明的 rankings（array，招引推荐清单）在返回体中可定位；样例未展开元素子字段，不断言未列出的嵌套值 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute | M_ENT_POLICY_MATCH_SCORE | INTEG |  | FUNC-00155 | endpoint_id=entan.attract.recommend.m_ent_policy_match_score catalog_page_id=entan.attract 组合=POL-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00156 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 招引企业综合推荐模型 | 招引企业综合推荐 | 政策匹配度 | 验证政策匹配度功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「招引企业综合推荐」；2.接口下拉选择「政策匹配度」；3.填写 清空 enterprise_codes 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 metric_id 与 rankings 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute |  | INTEG |  | FUNC-00156 | endpoint_id=entan.attract.recommend.m_ent_policy_match_score catalog_page_id=entan.attract 组合=POL-02 场景=异常-入参-缺enterprise_codes catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00157 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 招引企业综合推荐模型 | 招引企业综合推荐 | 接口信息 | 验证招引企业综合推荐的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「招引企业综合推荐」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应招引企业推荐指数 POST /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute；4、切换后概览对应政策匹配度 POST /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00157 | catalog_page_id=entan.attract 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00158 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 招引企业综合推荐模型 | 招引企业综合推荐 | 算法测试 | 验证招引企业综合推荐的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「招引企业综合推荐」；2.切换到「算法测试」tab；3.下拉切换到「政策匹配度」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「政策匹配度」；3、调用区 method 为 POST、path 为 /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00158 | catalog_page_id=entan.attract 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ATR-01 | entan.attract.recommend | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| ATR-02 | entan.attract.recommend | 清空 enterprise_codes 入参 | 缺必填 enterprise_codes |
| POL-01 | entan.attract.recommend.m_ent_policy_match_score | enterprise_codes 同 ATR-01 | 主路径全参（sampleRequest） |
| POL-02 | entan.attract.recommend.m_ent_policy_match_score | 清空 enterprise_codes 入参 | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 招引企业推荐指数（企业集合） | entan.attract.recommend | POST | /entan/v1/entan/metric/M_ENT_ATTRACTION_INDEX/compute | enterprise_codes* | unavailable |
| 政策匹配度 | entan.attract.recommend.m_ent_policy_match_score | POST | /entan/v1/entan/metric/M_ENT_POLICY_MATCH_SCORE/compute | enterprise_codes* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.attract.recommend | FUNC-00153、00154 |
| entan.attract.recommend.m_ent_policy_match_score | FUNC-00155、00156 |
| （页面清单） | FUNC-00157、00158 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 有参接口：文档示例全参正向；每参数恰好 1 条反向（缺 enterprise_codes）；无可选参数，无备选-参数组合
- [x] unavailable（招引企业推荐指数）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 POST/GET 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 企业深度分析模型构建 / 招引企业综合推荐模型
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00153～00158

**统计**：接口 **2**；主流程 **2**；反向 **2**；清单 **2**；合计 **6** 条；编号闭区间 **FUNC-00153**～**FUNC-00158**（父控 R3-批3 分配）。
