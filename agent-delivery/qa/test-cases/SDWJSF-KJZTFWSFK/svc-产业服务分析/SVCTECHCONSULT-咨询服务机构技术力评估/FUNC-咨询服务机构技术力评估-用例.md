# 智能服务集群-科技专题服务算法库测试用例（咨询服务机构技术力评估 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=svc.tech-consult` · `catalog_page_id=svc.tech-consult` · path `#/industry-service/tech-consult`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/svc.json` · 页 `svc.tech-consult`  
> **A 线对照**：`fp-split-by-api-run/work/L47.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批15）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 咨询服务技术力 | svc.tech-consult.models | unavailable |
| 2 | 咨询服务机构技术力评价模型 | svc.tech-consult.m_svc_deep_178_1 | available |

两个接口均仅有可选 `kind`。主流程对齐各自 `sampleRequest`：`kind=tech`。省略 `kind` 为备选；`kind=__invalid__` 作反向。`咨询服务技术力` 的 catalog `status=unavailable`，仍按该接口文档返回体编写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00916**～**FUNC-00923**，共 **8** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.tech-consult`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00916 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 咨询服务机构技术力评价模型 | 咨询服务机构技术力评估 | 咨询服务技术力 | 验证咨询服务技术力功能，检查填写 kind=tech调用后返回技术力名单字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=tech | 1.侧栏进入「产业服务分析」→「咨询服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「咨询服务技术力」；4.填写 kind=tech，点击调用 | 1、返回面板 body 顶层含 tech（array，responseFields 技术力名单）；2、元素含 org_id（string，示例 svc:cs_ns）、service_type（string，示例 CONSULT）、score（number，示例 75.0）；3、ext 含 name（string，示例 南山产业咨询所）、rank_no（number，示例 1）；4、dimension_scores 含 patents（number，示例 46）、rdInvestment（number，示例 58）、experts（number，示例 83）、cases（number，示例 79）、standards（number，示例 51）；5、结构与 sampleResponse 一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG |  | FUNC-00916 | endpoint_id=svc.tech-consult.models catalog_page_id=svc.tech-consult 组合=TCON-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00917 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 咨询服务机构技术力评价模型 | 咨询服务机构技术力评估 | 咨询服务技术力 | 验证咨询服务技术力功能，检查不传 kind 后仍返回技术力名单结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「咨询服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「咨询服务技术力」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 顶层仍含 tech（array，responseFields 技术力名单）；2、元素仍含 org_id（string）、service_type（string）、score（number）；3、ext 仍含 name（string）、rank_no（number）；4、dimension_scores 仍含 patents、rdInvestment、experts、cases、standards（number）；5、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG |  | FUNC-00917 | endpoint_id=svc.tech-consult.models catalog_page_id=svc.tech-consult 组合=TCON-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00918 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 咨询服务机构技术力评价模型 | 咨询服务机构技术力评估 | 咨询服务技术力 | 验证咨询服务技术力功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「咨询服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「咨询服务技术力」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 tech 技术力名单数组的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models |  | INTEG |  | FUNC-00918 | endpoint_id=svc.tech-consult.models catalog_page_id=svc.tech-consult 组合=TCON-03 场景=异常-入参-非法kind catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00919 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 咨询服务机构技术力评价模型 | 咨询服务机构技术力评估 | 咨询服务机构技术力评价模型 | 验证咨询服务机构技术力评价模型功能，检查填写 kind=tech调用后返回 metric_id 与 tech 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=tech | 1.侧栏进入「产业服务分析」→「咨询服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「咨询服务机构技术力评价模型」；4.填写 kind=tech，点击调用 | 1、返回面板 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_DEEP_178_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明 tech 为 array（技术力名单）；3、sampleResponse 未给出 tech 示例元素，返回中应出现 responseFields 所列 tech | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_178_1/compute | M_SVC_DEEP_178_1 | INTEG |  | FUNC-00919 | endpoint_id=svc.tech-consult.m_svc_deep_178_1 catalog_page_id=svc.tech-consult 组合=D178-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00920 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 咨询服务机构技术力评价模型 | 咨询服务机构技术力评估 | 咨询服务机构技术力评价模型 | 验证咨询服务机构技术力评价模型功能，检查不传 kind 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「咨询服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「咨询服务机构技术力评价模型」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 仍含 metric_id（string）、hint（string）；2、responseFields 所列 tech（array，技术力名单）仍应出现；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_178_1/compute | M_SVC_DEEP_178_1 | INTEG |  | FUNC-00920 | endpoint_id=svc.tech-consult.m_svc_deep_178_1 catalog_page_id=svc.tech-consult 组合=D178-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00921 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 咨询服务机构技术力评价模型 | 咨询服务机构技术力评估 | 咨询服务机构技术力评价模型 | 验证咨询服务机构技术力评价模型功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「咨询服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「咨询服务机构技术力评价模型」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_178_1 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_178_1/compute |  | INTEG |  | FUNC-00921 | endpoint_id=svc.tech-consult.m_svc_deep_178_1 catalog_page_id=svc.tech-consult 组合=D178-03 场景=异常-入参-非法kind catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00922 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 咨询服务机构技术力评价模型 | 咨询服务机构技术力评估 | 接口信息 | 验证咨询服务机构技术力评估的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「咨询服务机构技术力评估」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（咨询服务技术力、咨询服务机构技术力评价模型）；3、默认项概览 method=GET、path=/entan/v1/svc/models；4、切换后概览对应咨询服务机构技术力评价模型 POST /entan/v1/svc-metric/metric/M_SVC_DEEP_178_1/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00922 | catalog_page_id=svc.tech-consult 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00923 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 咨询服务机构技术力评价模型 | 咨询服务机构技术力评估 | 算法测试 | 验证咨询服务机构技术力评估的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「咨询服务机构技术力评估」；2.切换到「算法测试」tab；3.下拉切换到「咨询服务机构技术力评价模型」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「咨询服务机构技术力评价模型」；3、调用区 method 为 POST、path 为 /entan/v1/svc-metric/metric/M_SVC_DEEP_178_1/compute；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00923 | catalog_page_id=svc.tech-consult 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TCON-01 | svc.tech-consult.models | kind=tech | 主路径（sampleRequest） |
| TCON-02 | svc.tech-consult.models | 不传 kind | 省略可选 kind |
| TCON-03 | svc.tech-consult.models | kind=__invalid__ | 只破坏 kind |
| D178-01 | svc.tech-consult.m_svc_deep_178_1 | kind=tech | 主路径（sampleRequest） |
| D178-02 | svc.tech-consult.m_svc_deep_178_1 | 不传 kind | 省略可选 kind |
| D178-03 | svc.tech-consult.m_svc_deep_178_1 | kind=__invalid__ | 只破坏 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 咨询服务技术力 | svc.tech-consult.models | GET | /entan/v1/svc/models | kind? | unavailable |
| 咨询服务机构技术力评价模型 | svc.tech-consult.m_svc_deep_178_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_178_1/compute | kind? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.tech-consult.models | FUNC-00916、00917、00918 |
| svc.tech-consult.m_svc_deep_178_1 | FUNC-00919、00920、00921 |
| （页面清单） | FUNC-00922、00923 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-00916、00919）
- [x] 仅可选 kind 的接口各 3 条（sampleRequest 主流程 + 省略 kind 备选 + 非法 kind 反向）
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L47（产业服务深度分析模型构建 / 咨询服务机构技术力评价模型）
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 多接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00916～00923

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **8** 条；主流程 **2**、备选 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00916**～**FUNC-00923**（R3-批15 svc.tech-consult）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **8** |
| 编号闭区间 | **FUNC-00916**～**FUNC-00923** |
| 接口向（不含清单） | **6** |
| 主流程 | **2** |
| 备选-参数组合 | **2** |
| 反向 | **2** |
| 清单 | **2** |
| 已删 API 册 | `API-咨询服务机构技术力评估-用例.md`（API-01692～01697 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
