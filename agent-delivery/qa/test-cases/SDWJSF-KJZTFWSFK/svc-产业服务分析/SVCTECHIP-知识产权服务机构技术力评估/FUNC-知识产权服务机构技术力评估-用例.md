# 智能服务集群-科技专题服务算法库测试用例（知识产权服务机构技术力评估 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=svc.tech-ip` · `catalog_page_id=svc.tech-ip` · path `#/industry-service/tech-ip`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/svc.json` · 页 `svc.tech-ip`  
> **A 线对照**：`fp-split-by-api-run/work/L44.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批14；金样 chain.basic）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 知识产权技术力 | svc.tech-ip.models | unavailable |
| 2 | 知识产权服务机构技术力评价模型 | svc.tech-ip.m_svc_deep_175_1 | available |

两个接口均仅有可选 `kind`。主流程对齐各自 `sampleRequest`：`kind=tech`。省略 `kind` 为备选；`kind=__invalid__` 作反向。`知识产权技术力` 的 catalog `status=unavailable`，仍按该接口文档返回体编写。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00892**～**FUNC-00899**，共 **8** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.tech-ip`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00892 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 知识产权服务机构技术力评价模型 | 知识产权服务机构技术力评估 | 知识产权技术力 | 验证知识产权技术力功能，检查填写 kind=tech调用后返回技术力名单字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 使用文档 sampleRequest 的 tech | 1.侧栏进入「产业服务分析」→「知识产权服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「知识产权技术力」；4.填写 kind=tech，点击调用 | 1、返回面板 body 为对象；2、tech 为 array（responseFields 技术力名单）；3、元素含 org_id（string）、service_type（string）、score（number）；4、ext 为 object，含 name（string）、rank_no（number）；5、dimension_scores 为 object，含 patents、rdInvestment、experts、cases、standards（均为 number）；6、sampleResponse 一条：org_id=svc:ip_sz、service_type=IP、score=84.2、name=知产服务中心、rank_no=1、patents=91、rdInvestment=70、experts=80、cases=76、standards=72 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG |  | FUNC-00892 | endpoint_id=svc.tech-ip.models catalog_page_id=svc.tech-ip 组合=IPM-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00893 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 知识产权服务机构技术力评价模型 | 知识产权服务机构技术力评估 | 知识产权技术力 | 验证知识产权技术力功能，检查不传 kind 后仍返回技术力名单结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「知识产权服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「知识产权技术力」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 为对象；2、tech 仍为 array（responseFields 技术力名单）；3、元素仍含 org_id（string）、service_type（string）、score（number）；4、ext 仍为 object，含 name（string）、rank_no（number）；5、dimension_scores 仍为 object，含 patents、rdInvestment、experts、cases、standards（均为 number）；6、结构与 sampleResponse 同类，示例仍为 org_id=svc:ip_sz、service_type=IP、score=84.2、name=知产服务中心、rank_no=1、patents=91、rdInvestment=70、experts=80、cases=76、standards=72 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG |  | FUNC-00893 | endpoint_id=svc.tech-ip.models catalog_page_id=svc.tech-ip 组合=IPM-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00894 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 知识产权服务机构技术力评价模型 | 知识产权服务机构技术力评估 | 知识产权技术力 | 验证知识产权技术力功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「知识产权服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「知识产权技术力」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 score 的成功 tech 业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models |  | INTEG |  | FUNC-00894 | endpoint_id=svc.tech-ip.models catalog_page_id=svc.tech-ip 组合=IPM-03 场景=异常-入参-非法kind catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00895 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 知识产权服务机构技术力评价模型 | 知识产权服务机构技术力评估 | 知识产权服务机构技术力评价模型 | 验证知识产权服务机构技术力评价模型功能，检查填写 kind=tech调用后返回 metric_id 与 hint | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 使用 sampleRequest 取值 tech | 1.侧栏进入「产业服务分析」→「知识产权服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「知识产权服务机构技术力评价模型」；4.填写 kind=tech，点击调用 | 1、返回面板 body 与 sampleResponse 同层含 metric_id（string，示例 M_SVC_DEEP_175_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 另列 tech（array，技术力名单），sampleResponse 未给 tech 元素示例值，返回中应出现 responseFields 所列 tech | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_175_1/compute | M_SVC_DEEP_175_1 | INTEG |  | FUNC-00895 | endpoint_id=svc.tech-ip.m_svc_deep_175_1 catalog_page_id=svc.tech-ip 组合=D175-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00896 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 知识产权服务机构技术力评价模型 | 知识产权服务机构技术力评估 | 知识产权服务机构技术力评价模型 | 验证知识产权服务机构技术力评价模型功能，检查不传 kind 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「知识产权服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「知识产权服务机构技术力评价模型」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 仍含 metric_id（string，示例 M_SVC_DEEP_175_1）、hint（string）；2、responseFields 的 tech 为 array（技术力名单）；3、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_175_1/compute | M_SVC_DEEP_175_1 | INTEG |  | FUNC-00896 | endpoint_id=svc.tech-ip.m_svc_deep_175_1 catalog_page_id=svc.tech-ip 组合=D175-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00897 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 知识产权服务机构技术力评价模型 | 知识产权服务机构技术力评估 | 知识产权服务机构技术力评价模型 | 验证知识产权服务机构技术力评价模型功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「知识产权服务机构技术力评估」；2.切换至「算法测试」tab；3.接口下拉选择「知识产权服务机构技术力评价模型」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_175_1 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_175_1/compute |  | INTEG |  | FUNC-00897 | endpoint_id=svc.tech-ip.m_svc_deep_175_1 catalog_page_id=svc.tech-ip 组合=D175-03 场景=异常-入参-非法kind catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00898 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 知识产权服务机构技术力评价模型 | 知识产权服务机构技术力评估 | 接口信息 | 验证知识产权服务机构技术力评估的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「知识产权服务机构技术力评估」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（知识产权技术力、知识产权服务机构技术力评价模型）；3、默认项概览 method=GET、path=/entan/v1/svc/models；4、切换后概览对应知识产权服务机构技术力评价模型 POST /entan/v1/svc-metric/metric/M_SVC_DEEP_175_1/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00898 | catalog_page_id=svc.tech-ip 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00899 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 知识产权服务机构技术力评价模型 | 知识产权服务机构技术力评估 | 算法测试 | 验证知识产权服务机构技术力评估的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「知识产权服务机构技术力评估」；2.切换到「算法测试」tab；3.下拉切换到「知识产权服务机构技术力评价模型」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「知识产权服务机构技术力评价模型」；3、调用区 method 为 POST、path 为 /entan/v1/svc-metric/metric/M_SVC_DEEP_175_1/compute；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00899 | catalog_page_id=svc.tech-ip 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| IPM-01 | svc.tech-ip.models | kind=tech | 主路径（sampleRequest） |
| IPM-02 | svc.tech-ip.models | 不传 kind | 省略可选 kind |
| IPM-03 | svc.tech-ip.models | kind=__invalid__ | 只破坏 kind |
| D175-01 | svc.tech-ip.m_svc_deep_175_1 | kind=tech | 主路径（sampleRequest） |
| D175-02 | svc.tech-ip.m_svc_deep_175_1 | 不传 kind | 省略可选 kind |
| D175-03 | svc.tech-ip.m_svc_deep_175_1 | kind=__invalid__ | 只破坏 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 知识产权技术力 | svc.tech-ip.models | GET | /entan/v1/svc/models | kind? | unavailable |
| 知识产权服务机构技术力评价模型 | svc.tech-ip.m_svc_deep_175_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_175_1/compute | kind? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.tech-ip.models | FUNC-00892、00893、00894 |
| svc.tech-ip.m_svc_deep_175_1 | FUNC-00895、00896、00897 |
| （页面清单） | FUNC-00898、00899 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-00892、00895）
- [x] 仅可选 kind 的接口各 3 条（sampleRequest 主流程 + 省略 kind 备选 + 非法 kind 反向）
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L44（产业服务深度分析模型构建 / 知识产权服务机构技术力评价模型）
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 多接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00892～00899

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **8** 条；主流程 **2**、备选 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-00892**～**FUNC-00899**（R3-批14 svc.tech-ip）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **8** |
| 编号闭区间 | **FUNC-00892**～**FUNC-00899** |
| 接口向（不含清单） | **6** |
| 主流程 | **2** |
| 备选-参数组合 | **2** |
| 反向 | **2** |
| 清单 | **2** |
| 已删 API 册 | `API-知识产权服务机构技术力评估-用例.md`（API-01674～01679 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
