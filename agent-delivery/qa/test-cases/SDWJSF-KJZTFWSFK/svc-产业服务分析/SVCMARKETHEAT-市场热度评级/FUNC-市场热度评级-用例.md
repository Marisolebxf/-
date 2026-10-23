# 智能服务集群-科技专题服务算法库测试用例（市场热度评级 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=svc.market-heat` · `catalog_page_id=svc.market-heat` · path `#/industry-service/market-heat`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/svc.json` · 页 `svc.market-heat`  
> **A 线对照**：**无对应 Lxx**（`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `svc.market-heat`，原因：不扩六级；不改 `work/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批15）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 市场热度 | svc.market-heat.main | unavailable |
| 2 | 市场热度评级 | svc.market-heat.m_svc_org_market_heat | available |

两个接口均仅有可选 `industry`。主流程对齐各自 `sampleRequest`：`industry=人工智能`。省略 `industry` 为备选；`industry=__invalid__` 作反向。`市场热度` 的 catalog `status=unavailable`，仍按该接口文档返回体编写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00948**～**FUNC-00955**，共 **8** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.market-heat`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00948 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 市场热度评级 | 市场热度 | 验证市场热度功能，检查填写 industry=人工智能调用后返回热度与序列字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、industry=人工智能 | 1.侧栏进入「产业服务分析」→「市场热度评级」；2.切换至「算法测试」tab；3.接口下拉选择「市场热度」；4.填写 industry=人工智能，点击调用 | 1、返回面板 body 含 market_heat_level（string，responseFields 市场热度等级，sampleResponse 示例「高」）；2、trend_slope（number，sampleResponse 示例 0.18）；3、volatility（number，sampleResponse 示例 0.24）；4、series 为数组（responseFields 新增机构时间序列）；5、series 元素含 year（number，示例 2022、2023、2024）与 new_org_count（number，示例 24、31、40）；6、结构与 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/market-heat | M_SVC_ORG_MARKET_HEAT | INTEG |  | FUNC-00948 | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00949 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 市场热度评级 | 市场热度 | 验证市场热度功能，检查不传 industry 后仍返回热度与序列结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 industry | 1.侧栏进入「产业服务分析」→「市场热度评级」；2.切换至「算法测试」tab；3.接口下拉选择「市场热度」；4.不传 industry，点击调用（不传 industry），点击调用 | 1、返回面板 body 仍含 market_heat_level（string）、trend_slope（number）、volatility（number）；2、series 仍为数组，元素含 year（number）、new_org_count（number）；3、responseFields 所列 market_heat_level、series 仍应出现；4、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/market-heat | M_SVC_ORG_MARKET_HEAT | INTEG |  | FUNC-00949 | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00950 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 市场热度评级 | 市场热度 | 验证市场热度功能，检查 industry 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、industry 取文档示例外的值 | 1.侧栏进入「产业服务分析」→「市场热度评级」；2.切换至「算法测试」tab；3.接口下拉选择「市场热度」；4.填写 industry=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 industry 非法；2、不返回含 market_heat_level 或 series 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/market-heat |  | INTEG |  | FUNC-00950 | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-03 场景=异常-入参-非法industry catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00951 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 市场热度评级 | 市场热度评级 | 验证市场热度评级功能，检查填写 industry=人工智能调用后返回 metric_id 与 responseFields 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、industry=人工智能 | 1.侧栏进入「产业服务分析」→「市场热度评级」；2.切换至「算法测试」tab；3.接口下拉选择「市场热度评级」；4.填写 industry=人工智能，点击调用 | 1、返回面板 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_ORG_MARKET_HEAT）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 market_heat_level（string，市场热度等级）、series（array，新增机构时间序列），返回中应有这些字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute | M_SVC_ORG_MARKET_HEAT | INTEG |  | FUNC-00951 | endpoint_id=svc.market-heat.m_svc_org_market_heat catalog_page_id=svc.market-heat 组合=MHR-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00952 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 市场热度评级 | 市场热度评级 | 验证市场热度评级功能，检查不传 industry 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 industry | 1.侧栏进入「产业服务分析」→「市场热度评级」；2.切换至「算法测试」tab；3.接口下拉选择「市场热度评级」；4.不传 industry，点击调用（不传 industry），点击调用 | 1、返回面板 body 仍含 metric_id（string）、hint（string）；2、responseFields 所列 market_heat_level（string，市场热度等级）、series（array，新增机构时间序列）仍应出现；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute | M_SVC_ORG_MARKET_HEAT | INTEG |  | FUNC-00952 | endpoint_id=svc.market-heat.m_svc_org_market_heat catalog_page_id=svc.market-heat 组合=MHR-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00953 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 市场热度评级 | 市场热度评级 | 验证市场热度评级功能，检查 industry 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、industry 取文档示例外的值 | 1.侧栏进入「产业服务分析」→「市场热度评级」；2.切换至「算法测试」tab；3.接口下拉选择「市场热度评级」；4.填写 industry=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 industry 非法；2、不返回含 metric_id 为 M_SVC_ORG_MARKET_HEAT 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute |  | INTEG |  | FUNC-00953 | endpoint_id=svc.market-heat.m_svc_org_market_heat catalog_page_id=svc.market-heat 组合=MHR-03 场景=异常-入参-非法industry catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00954 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 市场热度评级 | 接口信息 | 验证市场热度评级的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「市场热度评级」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（市场热度、市场热度评级）；3、默认项概览 method=GET、path=/entan/v1/svc/market-heat；4、切换后概览对应市场热度评级 POST /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00954 | catalog_page_id=svc.market-heat 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00955 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 市场热度评级 | 算法测试 | 验证市场热度评级的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「市场热度评级」；2.切换到「算法测试」tab；3.下拉切换到「市场热度评级」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「市场热度评级」；3、调用区 method 为 POST、path 为 /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00955 | catalog_page_id=svc.market-heat 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MH-01 | svc.market-heat.main | industry=人工智能 | 主路径（sampleRequest） |
| MH-02 | svc.market-heat.main | 不传 industry | 省略可选 industry |
| MH-03 | svc.market-heat.main | industry=__invalid__ | 只破坏 industry |
| MHR-01 | svc.market-heat.m_svc_org_market_heat | industry=人工智能 | 主路径（sampleRequest） |
| MHR-02 | svc.market-heat.m_svc_org_market_heat | 不传 industry | 省略可选 industry |
| MHR-03 | svc.market-heat.m_svc_org_market_heat | industry=__invalid__ | 只破坏 industry |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 市场热度 | svc.market-heat.main | GET | /entan/v1/svc/market-heat | industry? | unavailable |
| 市场热度评级 | svc.market-heat.m_svc_org_market_heat | POST | /entan/v1/svc-metric/metric/M_SVC_ORG_MARKET_HEAT/compute | industry? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.market-heat.main | FUNC-00948、00949、00950 |
| svc.market-heat.m_svc_org_market_heat | FUNC-00951、00952、00953 |
| （页面清单） | FUNC-00954、00955 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-00948、00951）
- [x] 仅可选 industry 的接口各 3 条（sampleRequest 主流程 + 省略 industry 备选 + 非法 industry 反向）
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 无对应 Lxx：五级/六级均写「待挂需规」（catalog_skip）
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 多接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00948～00955

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **8** 条；主流程 **2**、备选 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00948**～**FUNC-00955**（R3-批15 svc.market-heat）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **8** |
| 编号闭区间 | **FUNC-00948**～**FUNC-00955** |
| 接口向（不含清单） | **6** |
| 主流程 | **2** |
| 备选-参数组合 | **2** |
| 反向 | **2** |
| 清单 | **2** |
| 已删 API 册 | `API-市场热度评级-用例.md`（API-01716～01721 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
