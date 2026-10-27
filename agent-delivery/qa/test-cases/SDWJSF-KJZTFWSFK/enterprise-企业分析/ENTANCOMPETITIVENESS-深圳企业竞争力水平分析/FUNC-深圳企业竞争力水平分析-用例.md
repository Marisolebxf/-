# 智能服务集群-科技专题服务算法库测试用例（深圳企业竞争力水平分析 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=entan.competitiveness` · `catalog_page_id=entan.competitiveness` · path `#/entan/competitiveness`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **A 线对照**：`fp-split-by-api-run/work/L27.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批2）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | path | status |
|---|------------------------|-------------|--------|------|--------|
| 1 | 深圳企业竞争力水平分析（企业集合） | entan.competitiveness.score | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | unavailable |
| 2 | 深圳企业竞争力排名（企业集合） | entan.competitiveness.ranking | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | unavailable |
| 3 | 多城市企业群对标值 | entan.competitiveness.score.m_ent_city_compare_topic | POST | /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute | available |

**enterprise_codes 试调取值**：catalog `sampleRequest` 四元组：`0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（附录组合表引用，执行期可替换为环境有效 org_id）。`responseFields` 声明顶层 `enterprises`（array）；得分/排名样例明细位于 `value.enterprises`，正向预期同时覆盖嵌套结构与契约字段。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00100**～**FUNC-00107**，共 **8** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.competitiveness`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00100 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 深圳企业竞争力水平分析模型 | 深圳企业竞争力水平分析 | 深圳企业竞争力水平分析（企业集合） | 验证深圳企业竞争力水平分析（企业集合）功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回综合竞争力得分契约字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes 使用 §0 文档四元组（可替换） | 1.侧栏进入「企业分析」→「深圳企业竞争力水平分析」；2.接口下拉选择「深圳企业竞争力水平分析（企业集合）」；3.填写 enterprise_codes=§0四元组（catalogsampleRequest，可替换），点击调用 | 1、返回面板含 string 型 metric_id、metric_name_zh；2、含 object 型 value，且 value.enterprises 为 array；3、若 enterprises 非空则元素含 string 型 org_id、enterprise_name，number 型 total_score，object 型 dimensions（含 innovation、operation、growth）；4、sampleResponse 示例还含 data_source（string）、confidence（string）、calc_process（object）；5、契约 responseFields 要求的 enterprises（array）在载荷中可定位 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | M_ENT_COMPETITIVENESS_SCORE | INTEG |  | FUNC-00100 | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00101 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 深圳企业竞争力水平分析模型 | 深圳企业竞争力水平分析 | 深圳企业竞争力水平分析（企业集合） | 验证深圳企业竞争力水平分析（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「深圳企业竞争力水平分析」；2.接口下拉选择「深圳企业竞争力水平分析（企业集合）」；3.填写 不填 enterprise_codes（请求区不含该参数），点击调用 | 1、返回面板的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含 sampleResponse 形态 total_score 与 dimensions 的成功得分结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute |  | INTEG |  | FUNC-00101 | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-02 场景=异常-入参-缺enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00102 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 深圳企业竞争力水平分析模型 | 深圳企业竞争力水平分析 | 深圳企业竞争力排名（企业集合） | 验证深圳企业竞争力排名（企业集合）功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回排名结果集契约字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes 使用 §0 文档四元组（可替换） | 1.侧栏进入「企业分析」→「深圳企业竞争力水平分析」；2.接口下拉选择「深圳企业竞争力排名（企业集合）」；3.填写 enterprise_codes 同 SCR-01，点击调用 | 1、返回面板含 string 型 metric_id、metric_name_zh；2、含 object 型 value，且 value.enterprises 为 array；3、若 enterprises 非空则元素含 org_id、enterprise_name、total_score、dimensions（innovation、operation、growth）；4、sampleResponse 示例还含 data_source、confidence、calc_process；5、enterprises 数组承载排名明细（排序语义以接口文档为准） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | M_ENT_COMPETITIVENESS_SCORE | INTEG |  | FUNC-00102 | endpoint_id=entan.competitiveness.ranking catalog_page_id=entan.competitiveness 组合=RNK-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00103 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 深圳企业竞争力水平分析模型 | 深圳企业竞争力水平分析 | 深圳企业竞争力排名（企业集合） | 验证深圳企业竞争力排名（企业集合）功能，检查 enterprise_codes 含明显非法编码时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「深圳企业竞争力水平分析」；2.接口下拉选择「深圳企业竞争力排名（企业集合）」；3.填写 enterprise_codes=`__invalid_org__`，点击调用 | 1、返回面板的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含可信排序 enterprises 与 total_score 的成功排名结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute |  | INTEG |  | FUNC-00103 | endpoint_id=entan.competitiveness.ranking catalog_page_id=entan.competitiveness 组合=RNK-02 场景=异常-入参-非法enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00104 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 深圳企业竞争力水平分析模型 | 深圳企业竞争力水平分析 | 多城市企业群对标值 | 验证多城市企业群对标值功能，检查填写 enterprise_codes=0218337e44ca794fee9850cf1627b03b 等四元组后返回 metric_id、hint 与 enterprises 等 compute 契约字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes 使用 §0 文档四元组（可替换） | 1.侧栏进入「企业分析」→「深圳企业竞争力水平分析」；2.接口下拉选择「多城市企业群对标值」；3.填写 enterprise_codes=0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299，点击调用 | 1、返回面板含 string 型 metric_id（sampleResponse 示例为 M_ENT_CITY_COMPARE_TOPIC）；2、含 string 型 hint（示例为 compute 响应,以实际调用为准）；3、契约 responseFields 要求的 enterprises（array）在载荷中可定位；4、以实际调用为准时 hint 文案可变，但 metric_id 与 enterprises 字段形态须符合文档 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute | M_ENT_CITY_COMPARE_TOPIC | INTEG |  | FUNC-00104 | endpoint_id=entan.competitiveness.score.m_ent_city_compare_topic catalog_page_id=entan.competitiveness 组合=CTY-01 场景=主流程 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00105 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 深圳企业竞争力水平分析模型 | 深圳企业竞争力水平分析 | 多城市企业群对标值 | 验证多城市企业群对标值功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「深圳企业竞争力水平分析」；2.接口下拉选择「多城市企业群对标值」；3.填写 不填 enterprise_codes，点击调用 | 1、返回面板的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含 metric_id 与 enterprises 的成功 compute 结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute |  | INTEG |  | FUNC-00105 | endpoint_id=entan.competitiveness.score.m_ent_city_compare_topic catalog_page_id=entan.competitiveness 组合=CTY-02 场景=异常-入参-缺enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00106 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 深圳企业竞争力水平分析模型 | 深圳企业竞争力水平分析 | 接口信息 | 验证深圳企业竞争力水平分析的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「深圳企业竞争力水平分析」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 3；2、下拉名称与 §0 各 title 一致；3、默认项概览 method 为 POST、path 为 /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute；4、切换后概览对应深圳企业竞争力排名（企业集合），path 仍为 /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00106 | catalog_page_id=entan.competitiveness 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00107 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 深圳企业竞争力水平分析模型 | 深圳企业竞争力水平分析 | 算法测试 | 验证深圳企业竞争力水平分析的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「深圳企业竞争力水平分析」；2.切换到「算法测试」tab；3.下拉切换到「多城市企业群对标值」 | 1、算法测试 tab 下拉共 3 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「多城市企业群对标值」；3、调用区 method 为 POST、path 为 /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00107 | catalog_page_id=entan.competitiveness 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SCR-01 | entan.competitiveness.score | enterprise_codes=§0 四元组（catalog sampleRequest，可替换） | 主路径全参 |
| SCR-02 | entan.competitiveness.score | 不填 enterprise_codes（请求区不含该参数） | 缺必填 |
| RNK-01 | entan.competitiveness.ranking | enterprise_codes 同 SCR-01 | 主路径全参 |
| RNK-02 | entan.competitiveness.ranking | enterprise_codes=`__invalid_org__` | 只破坏 enterprise_codes |
| CTY-01 | entan.competitiveness.score.m_ent_city_compare_topic | enterprise_codes 同 SCR-01 | 主路径全参 |
| CTY-02 | entan.competitiveness.score.m_ent_city_compare_topic | 不填 enterprise_codes | 缺必填 |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 深圳企业竞争力水平分析（企业集合） | entan.competitiveness.score | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | enterprise_codes* | unavailable |
| 深圳企业竞争力排名（企业集合） | entan.competitiveness.ranking | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | enterprise_codes* | unavailable |
| 多城市企业群对标值 | entan.competitiveness.score.m_ent_city_compare_topic | POST | /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute | enterprise_codes* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.competitiveness.score | FUNC-00100、00101 |
| entan.competitiveness.ranking | FUNC-00102、00103 |
| entan.competitiveness.score.m_ent_city_compare_topic | FUNC-00104、00105 |
| （页面清单） | FUNC-00106、00107 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 3 个 catalog title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 有参接口每参数 1 条反向（enterprise_codes：00101、00103、00105）
- [x] unavailable（得分/排名）仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 企业深度分析模型构建 / 深圳企业竞争力水平分析模型
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件；0 条鉴权/401 用例
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00100～00107

**统计**：接口 **3**；主流程 **3**；反向 **3**；清单 **2**；合计 **8** 条；编号闭区间 **FUNC-00100**～**FUNC-00107**（父控 R3-批2 分配）。
