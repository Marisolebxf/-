# 智能服务集群-科技专题服务算法库测试用例（金融服务机构技术力评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 金融服务机构技术力评估  
> **catalog**：`entry_id=svc.tech-finance` · `catalog_page_id=svc.tech-finance` · path `/industry-service/tech-finance`  
> **A 线对照**：`fp-split-by-api-run/work/L43.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `svc.json` 页 `svc.tech-finance`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批14）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 金融服务技术力 | svc.tech-finance.models |
| 2 | 金融服务机构技术力评价模型 | svc.tech-finance.m_svc_deep_174_1 |

两个接口各只有 1 个可选参数 `kind`。`sampleRequest` 与 `params.example` 均为 `kind=tech`，主路径取该值。备选与 sample 相反，不传 `kind`；反向各 1 条，只把 `kind` 改为 `__invalid__`。`GET /entan/v1/svc/models` 与其它服务机构模型页同 path，本页以 `kind=tech` 与页 title 区分。catalog `resultFilter` 按 `tech[].service_type=FINANCE` 过滤展示，不是请求参数，不另造入参用例。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01668**～**API-01673**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.tech-finance`、组合 id。旧号 API-000599～000603 作废，不复用。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01668 | 产业服务分析 | 金融服务机构技术力评估 | 主流程 | — | 金融服务机构技术力评估 | 金融服务技术力 | 金融服务技术力按文档 sampleRequest 传 kind=tech 时返回技术力名单字段 | 1、kind 使用文档 sampleRequest 的 tech | 1.GET /entan/v1/svc/models，查询参数取组合 TFM-01 | 1、返回 body 为对象；2、tech 为 array（responseFields 技术力名单）；3、元素含 org_id（string）、service_type（string）、score（number）；4、ext 为对象，含 name（string）、rank_no（number）；5、dimension_scores 为对象，含 patents、rdInvestment、experts、cases、standards（均为 number）；6、sampleResponse 两条：org_id=svc:ns_fin、service_type=FINANCE、score=86.4、name=南山科技金融站、rank_no=1、patents=78、rdInvestment=82、experts=74、cases=88、standards=61；org_id=svc:ba_fin、service_type=FINANCE、score=79.1、name=宝安科技金融中心、rank_no=2、patents=70、rdInvestment=76、experts=68、cases=80、standards=55 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG | | | endpoint_id=svc.tech-finance.models catalog_page_id=svc.tech-finance 组合=TFM-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01669 | 产业服务分析 | 金融服务机构技术力评估 | 备选-参数组合 | 省略 kind | 金融服务机构技术力评估 | 金融服务技术力 | 金融服务技术力不传可选 kind | 1、不传 kind | 1.GET /entan/v1/svc/models，查询参数取组合 TFM-02 | 1、返回 body 为对象；2、tech 仍为 array（responseFields 技术力名单）；3、元素仍含 org_id（string）、service_type（string）、score（number）；4、ext 仍含 name（string）、rank_no（number）；5、dimension_scores 仍含 patents、rdInvestment、experts、cases、standards（均为 number）；6、结构与 sampleResponse 同类，示例仍为 svc:ns_fin/FINANCE/86.4/南山科技金融站/rank_no=1/78/82/74/88/61，以及 svc:ba_fin/FINANCE/79.1/宝安科技金融中心/rank_no=2/70/76/68/80/55 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_ORG_TECH_SCORE | INTEG | | | endpoint_id=svc.tech-finance.models catalog_page_id=svc.tech-finance 组合=TFM-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01670 | 产业服务分析 | 金融服务机构技术力评估 | 异常-入参-非法kind | — | 金融服务机构技术力评估 | 金融服务技术力 | 金融服务技术力传入非法 kind | 1、kind=__invalid__ | 1.GET /entan/v1/svc/models，查询参数取组合 TFM-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 tech 技术力名单及 org_id、score 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.tech-finance.models catalog_page_id=svc.tech-finance 组合=TFM-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01671 | 产业服务分析 | 金融服务机构技术力评估 | 主流程 | — | 金融服务机构技术力评估 | 金融服务机构技术力评价模型 | 金融服务机构技术力评价模型按文档 sampleRequest 传 kind=tech 时返回模型字段 | 1、请求体 kind 使用文档 sampleRequest 的 tech | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_174_1/compute，请求体取组合 D174-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_SVC_DEEP_174_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 另列 tech（array，技术力名单），sampleResponse 未给出 tech 元素示例 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_174_1/compute | M_SVC_DEEP_174_1 | INTEG | | | endpoint_id=svc.tech-finance.m_svc_deep_174_1 catalog_page_id=svc.tech-finance 组合=D174-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01672 | 产业服务分析 | 金融服务机构技术力评估 | 备选-参数组合 | 省略 kind | 金融服务机构技术力评估 | 金融服务机构技术力评价模型 | 金融服务机构技术力评价模型不传可选 kind | 1、请求体不传 kind | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_174_1/compute，请求体取组合 D174-02 | 1、返回 body 为对象；2、仍含 metric_id（string，示例 M_SVC_DEEP_174_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 tech 仍为 array（技术力名单） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_174_1/compute | M_SVC_DEEP_174_1 | INTEG | | | endpoint_id=svc.tech-finance.m_svc_deep_174_1 catalog_page_id=svc.tech-finance 组合=D174-02 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01673 | 产业服务分析 | 金融服务机构技术力评估 | 异常-入参-非法kind | — | 金融服务机构技术力评估 | 金融服务机构技术力评价模型 | 金融服务机构技术力评价模型传入非法 kind | 1、请求体 kind=__invalid__ | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_174_1/compute，请求体取组合 D174-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_174_1 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_174_1/compute | | INTEG | | | endpoint_id=svc.tech-finance.m_svc_deep_174_1 catalog_page_id=svc.tech-finance 组合=D174-03 catalog_status=available |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TFM-01 | svc.tech-finance.models | kind=tech | 主路径（sampleRequest；与 params.example 一致） |
| TFM-02 | svc.tech-finance.models | 不传 kind | 省略可选 kind |
| TFM-03 | svc.tech-finance.models | kind=__invalid__ | 只破坏 kind |
| D174-01 | svc.tech-finance.m_svc_deep_174_1 | kind=tech | 主路径（sampleRequest；与 params.example 一致） |
| D174-02 | svc.tech-finance.m_svc_deep_174_1 | 不传 kind | 省略可选 kind |
| D174-03 | svc.tech-finance.m_svc_deep_174_1 | kind=__invalid__ | 只破坏 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 金融服务技术力 | svc.tech-finance.models | GET | /entan/v1/svc/models | kind? | unavailable |
| 金融服务机构技术力评价模型 | svc.tech-finance.m_svc_deep_174_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_174_1/compute | kind? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.tech-finance.models | API-01668、01669、01670 |
| svc.tech-finance.m_svc_deep_174_1 | API-01671、01672、01673 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 2 个 title 均在功能点列出现，且各有 1 条主流程（API-01668、01671）
- [x] 有参接口：sampleRequest 主流程 1 条；可选参数与 sample 相反（不传 kind）各 1 条；每个参数恰好 1 条非法反向
- [x] unavailable（金融服务技术力）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数非法
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01668～01673

**统计**：接口 **2**；用例 **6** 条（主流程 2、备选 2、反向 2）；编号闭区间 **API-01668**～**API-01673**（父控 R2-批14 分配，连续用满）。
