# 智能服务集群-科技专题服务算法库测试用例（企业发展痛难点识别 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=entan.pain-points` · `catalog_page_id=entan.pain-points` · path `#/entan/pain-points`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **A 线对照**：`fp-split-by-api-run/work/L29.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批2）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 企业发展痛难点反映企业数（企业集合） | entan.pain-points.count |
| 2 | 企业发展痛难点严重度（企业集合） | entan.pain-points.severity |
| 3 | 痛难点改进差距 | entan.pain-points.count.m_ent_painpoint_gap |
| 4 | 发展痛难点诊断 | entan.pain-points.count.m_ent_painpoint_topic |

**enterprise_codes 试调取值**：文档 `sampleRequest` 四元组 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（执行期可替换为环境有效企业标识，附录组合表引用该组）。

本页 4 个接口均只有必填 `enterprise_codes`，无可选参数。每接口 1 条主流程（sampleRequest 全参）+ 1 条反向（缺 `enterprise_codes`）。`count` / `severity` 的 catalog `status=unavailable`，仍按文档返回体写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00117**～**FUNC-00126**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.pain-points`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00117 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 企业发展痛难点反映企业数（企业集合） | 验证企业发展痛难点反映企业数（企业集合）功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回反映企业数与维度卡片字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.接口下拉选择「企业发展痛难点反映企业数（企业集合）」；3.填写 enterprise_codes=[0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299]，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 样例 M_ENT_PAINPOINT_COUNT）、metric_name_zh（string，样例痛难点反映企业数）；2、value 为 object，含 value.count（number，样例 12）；3、value.dimension_cards 为 array；4、dimension_cards 元素含 dimension（string）、issue_count（number）、priority（string）、affected_enterprise_count（number）；5、另含 data_source（string）、confidence（string）；6、calc_process 为 object，含 definition（string）、formula（string）、source_tables（array）、model_version（string） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | M_ENT_PAINPOINT_COUNT | INTEG |  | FUNC-00117 | endpoint_id=entan.pain-points.count catalog_page_id=entan.pain-points 组合=CNT-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00118 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 企业发展痛难点反映企业数（企业集合） | 验证企业发展痛难点反映企业数（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.接口下拉选择「企业发展痛难点反映企业数（企业集合）」；3.填写 清空 enterprise_codes 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 value.count 与 dimension_cards 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute |  | INTEG |  | FUNC-00118 | endpoint_id=entan.pain-points.count catalog_page_id=entan.pain-points 组合=CNT-02 场景=异常-入参-缺enterprise_codes catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00119 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 企业发展痛难点严重度（企业集合） | 验证企业发展痛难点严重度（企业集合）功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回严重度与维度卡片字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.接口下拉选择「企业发展痛难点严重度（企业集合）」；3.填写 enterprise_codes 同 CNT-01，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 样例 M_ENT_PAINPOINT_SEVERITY）、metric_name_zh（string，样例痛难点严重度）；2、value 含 value.severity（object，样例键为技术、人才、资金、供应链，值为严重度文案）；3、value.dimension_cards 为 array；4、dimension_cards 元素含 dimension（string）、issue_count（number）、priority（string）、affected_enterprise_count（number）；5、另含 data_source（string）、confidence（string）；6、calc_process 为 object，含 definition、formula、source_tables、model_version | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | M_ENT_PAINPOINT_SEVERITY | INTEG |  | FUNC-00119 | endpoint_id=entan.pain-points.severity catalog_page_id=entan.pain-points 组合=SEV-01 场景=主流程 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00120 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 企业发展痛难点严重度（企业集合） | 验证企业发展痛难点严重度（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.接口下拉选择「企业发展痛难点严重度（企业集合）」；3.填写 清空 enterprise_codes 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 value.severity 与 dimension_cards 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute |  | INTEG |  | FUNC-00120 | endpoint_id=entan.pain-points.severity catalog_page_id=entan.pain-points 组合=SEV-02 场景=异常-入参-缺enterprise_codes catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00121 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 痛难点改进差距 | 验证痛难点改进差距功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回 metric_id 与 dimension_cards 可定位 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.接口下拉选择「痛难点改进差距」；3.填写 enterprise_codes 同 CNT-01，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 样例 M_ENT_PAINPOINT_GAP）；2、含 hint（string，样例为 compute 响应说明，以实际调用为准）；3、responseFields 声明的 dimension_cards（array）在返回体中可定位；样例未给出数组元素子字段，不断言未列出的嵌套值 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | M_ENT_PAINPOINT_GAP | INTEG |  | FUNC-00121 | endpoint_id=entan.pain-points.count.m_ent_painpoint_gap catalog_page_id=entan.pain-points 组合=GAP-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00122 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 痛难点改进差距 | 验证痛难点改进差距功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.接口下拉选择「痛难点改进差距」；3.填写 清空 enterprise_codes 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 metric_id 与 dimension_cards 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute |  | INTEG |  | FUNC-00122 | endpoint_id=entan.pain-points.count.m_ent_painpoint_gap catalog_page_id=entan.pain-points 组合=GAP-02 场景=异常-入参-缺enterprise_codes catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00123 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 发展痛难点诊断 | 验证发展痛难点诊断功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回 metric_id 与 dimension_cards 可定位 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.接口下拉选择「发展痛难点诊断」；3.填写 enterprise_codes 同 CNT-01，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 样例 M_ENT_PAINPOINT_TOPIC）；2、含 hint（string，样例为 compute 响应说明，以实际调用为准）；3、responseFields 声明的 dimension_cards（array）在返回体中可定位；样例未给出数组元素子字段，不断言未列出的嵌套值 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_TOPIC/compute | M_ENT_PAINPOINT_TOPIC | INTEG |  | FUNC-00123 | endpoint_id=entan.pain-points.count.m_ent_painpoint_topic catalog_page_id=entan.pain-points 组合=TPC-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00124 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 发展痛难点诊断 | 验证发展痛难点诊断功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.接口下拉选择「发展痛难点诊断」；3.填写 清空 enterprise_codes 入参，点击调用 | 1、返回面板的 message 或 msg 说明缺少 enterprise_codes；2、不返回含 metric_id 与 dimension_cards 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_TOPIC/compute |  | INTEG |  | FUNC-00124 | endpoint_id=entan.pain-points.count.m_ent_painpoint_topic catalog_page_id=entan.pain-points 组合=TPC-02 场景=异常-入参-缺enterprise_codes catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00125 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 接口信息 | 验证企业发展痛难点识别的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 4；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应企业发展痛难点反映企业数 POST /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute；4、切换后概览对应严重度 POST /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00125 | catalog_page_id=entan.pain-points 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00126 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业发展痛难点识别模型 | 企业发展痛难点识别 | 算法测试 | 验证企业发展痛难点识别的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业发展痛难点识别」；2.切换到「算法测试」tab；3.下拉切换到「痛难点改进差距」 | 1、算法测试 tab 下拉共 4 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「痛难点改进差距」；3、调用区 method 为 POST、path 为 /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00126 | catalog_page_id=entan.pain-points 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| CNT-01 | entan.pain-points.count | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| CNT-02 | entan.pain-points.count | 清空 enterprise_codes 入参 | 缺必填 enterprise_codes |
| SEV-01 | entan.pain-points.severity | enterprise_codes 同 CNT-01 | 主路径全参（sampleRequest） |
| SEV-02 | entan.pain-points.severity | 清空 enterprise_codes 入参 | 缺必填 enterprise_codes |
| GAP-01 | entan.pain-points.count.m_ent_painpoint_gap | enterprise_codes 同 CNT-01 | 主路径全参（sampleRequest） |
| GAP-02 | entan.pain-points.count.m_ent_painpoint_gap | 清空 enterprise_codes 入参 | 缺必填 enterprise_codes |
| TPC-01 | entan.pain-points.count.m_ent_painpoint_topic | enterprise_codes 同 CNT-01 | 主路径全参（sampleRequest） |
| TPC-02 | entan.pain-points.count.m_ent_painpoint_topic | 清空 enterprise_codes 入参 | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 企业发展痛难点反映企业数（企业集合） | entan.pain-points.count | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | enterprise_codes* | unavailable |
| 企业发展痛难点严重度（企业集合） | entan.pain-points.severity | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | enterprise_codes* | unavailable |
| 痛难点改进差距 | entan.pain-points.count.m_ent_painpoint_gap | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_GAP/compute | enterprise_codes* | available |
| 发展痛难点诊断 | entan.pain-points.count.m_ent_painpoint_topic | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_TOPIC/compute | enterprise_codes* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.pain-points.count | FUNC-00117、00118 |
| entan.pain-points.severity | FUNC-00119、00120 |
| entan.pain-points.count.m_ent_painpoint_gap | FUNC-00121、00122 |
| entan.pain-points.count.m_ent_painpoint_topic | FUNC-00123、00124 |
| （页面清单） | FUNC-00125、00126 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 4 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 有参接口：文档示例全参正向；每参数恰好 1 条反向（缺 enterprise_codes）；无可选参数，无备选-参数组合
- [x] unavailable（反映企业数、严重度）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 企业深度分析模型构建 / 企业发展痛难点识别模型
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00117～00126

**统计**：接口 **4**；主流程 **4**；反向 **4**；清单 **2**；合计 **10** 条；编号闭区间 **FUNC-00117**～**FUNC-00126**（父控 R3-批2 分配）。
