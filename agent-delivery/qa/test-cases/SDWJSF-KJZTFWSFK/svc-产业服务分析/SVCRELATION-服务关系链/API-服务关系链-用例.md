# 智能服务集群-科技专题服务算法库测试用例（服务关系链 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 服务关系链  
> **catalog**：`entry_id=svc.relation` · `catalog_page_id=svc.relation` · path `/industry-service/relation`  
> **A 线对照**：`fp-split-by-api-run/work/L42.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `svc.json` 页 `svc.relation`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批13）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 关系链模型 | svc.relation.models |
| 2 | 关系链图谱 | svc.relation.graph |
| 3 | 生态影响力评分 | svc.relation.m_svc_graph_influence |
| 4 | 服务关系链模型 | svc.relation.m_svc_deep_173_1 |

四个接口各只有 1 个可选参数。`sampleRequest` 均传入该参数：关系链模型与两个 compute 为 `kind=relation`，关系链图谱为 `limit=40`。备选与 sample 相反，不传该参数；反向各 1 条，只把该参数改为非法值。`服务关系链模型` 的 `params.example` 与 options 为 `tech`，主路径仍取 `sampleRequest` 的 `relation`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01656**～**API-01667**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.relation`、组合 id。旧号 API-000589～000598 作废，不复用。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01656 | 产业服务分析 | 服务关系链 | 主流程 | — | 服务关系链 | 关系链模型 | 关系链模型按文档 sampleRequest 传 kind=relation 时返回关系密度与中心性名单 | 1、kind 使用文档 sampleRequest 的 relation | 1.GET /entan/v1/svc/models，查询参数取组合 MOD-01 | 1、返回 body 为对象；2、relation_summary.density 为 number（responseFields 关系密度，示例 0.042）；3、relation_summary.ext.node_count 为 number（示例 18）、relation_summary.ext.link_count 为 number（示例 27）；4、relation_top 为 array（responseFields 中心性名单）；5、元素含 org_id（string）、ext.name（string）、centrality（number）；6、sampleResponse 三条：org_id=svc:ns_fin、name=南山科技金融站、centrality=0.86；org_id=svc:ip_sz、name=知产服务中心、centrality=0.71；org_id=svc:hr_ft、name=福田人才服务港、centrality=0.58 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_RELATION_DENSITY | INTEG | | | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01657 | 产业服务分析 | 服务关系链 | 备选-参数组合 | 省略 kind | 服务关系链 | 关系链模型 | 关系链模型不传可选 kind | 1、不传 kind | 1.GET /entan/v1/svc/models，查询参数取组合 MOD-02 | 1、返回 body 为对象；2、relation_summary.density 仍为 number（responseFields 关系密度）；3、relation_summary.ext 仍含 node_count（number）、link_count（number）；4、relation_top 仍为 array，元素仍含 org_id（string）、ext.name（string）、centrality（number）；5、结构与 sampleResponse 同类，示例仍为 density=0.042、node_count=18、link_count=27，以及 svc:ns_fin/南山科技金融站/0.86、svc:ip_sz/知产服务中心/0.71、svc:hr_ft/福田人才服务港/0.58 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_RELATION_DENSITY | INTEG | | | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01658 | 产业服务分析 | 服务关系链 | 异常-入参-非法kind | — | 服务关系链 | 关系链模型 | 关系链模型传入非法 kind | 1、kind=__invalid__ | 1.GET /entan/v1/svc/models，查询参数取组合 MOD-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 density 的成功 relation_summary | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01659 | 产业服务分析 | 服务关系链 | 主流程 | — | 服务关系链 | 关系链图谱 | 关系链图谱按文档 sampleRequest 传 limit=40 时返回节点与边 | 1、limit 使用文档 sampleRequest 的 40 | 1.GET /entan/v1/svc/graph，查询参数取组合 GRF-01 | 1、返回 body 为对象；2、nodes 为 array（responseFields 节点）；3、元素含 id（string）、name（string）、weight（number）；4、sampleResponse 三条：id=svc:ns_fin、name=南山科技金融站、weight=1.4；id=svc:ip_sz、name=知产服务中心、weight=1.1；id=svc:hr_ft、name=福田人才服务港、weight=0.9；5、edges 为 array（responseFields 边）；6、元素含 source（string）、target（string）、mapped_from（string）、relation（string）；7、示例 source=svc:ns_fin、target=svc:ip_sz、mapped_from=cooperation、relation=合作 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph | | INTEG | | | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-01 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01660 | 产业服务分析 | 服务关系链 | 备选-参数组合 | 省略 limit | 服务关系链 | 关系链图谱 | 关系链图谱不传可选 limit | 1、不传 limit | 1.GET /entan/v1/svc/graph，查询参数取组合 GRF-02 | 1、返回 body 为对象；2、nodes 仍为 array（responseFields 节点），元素仍含 id（string）、name（string）、weight（number）；3、edges 仍为 array（responseFields 边），元素仍含 source（string）、target（string）、mapped_from（string）、relation（string）；4、结构与 sampleResponse 同类，示例仍为 svc:ns_fin/南山科技金融站/1.4、svc:ip_sz/知产服务中心/1.1、svc:hr_ft/福田人才服务港/0.9，以及 source=svc:ns_fin、target=svc:ip_sz、mapped_from=cooperation、relation=合作 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph | | INTEG | | | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01661 | 产业服务分析 | 服务关系链 | 异常-入参-非法limit | — | 服务关系链 | 关系链图谱 | 关系链图谱传入非法 limit | 1、limit=-1 | 1.GET /entan/v1/svc/graph，查询参数取组合 GRF-03 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 nodes、edges 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph | | INTEG | | | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01662 | 产业服务分析 | 服务关系链 | 主流程 | — | 服务关系链 | 生态影响力评分 | 生态影响力评分按文档 sampleRequest 传 kind=relation 时返回评分字段 | 1、请求体 kind 使用文档 sampleRequest 的 relation | 1.POST /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute，请求体取组合 INF-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_SVC_GRAPH_INFLUENCE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 另列 relation_summary.density（number，关系密度）、relation_top（array，中心性名单），sampleResponse 未给这两字段的示例值 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute | M_SVC_GRAPH_INFLUENCE | INTEG | | | endpoint_id=svc.relation.m_svc_graph_influence catalog_page_id=svc.relation 组合=INF-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01663 | 产业服务分析 | 服务关系链 | 备选-参数组合 | 省略 kind | 服务关系链 | 生态影响力评分 | 生态影响力评分不传可选 kind | 1、请求体不传 kind | 1.POST /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute，请求体取组合 INF-02 | 1、返回 body 为对象；2、仍含 metric_id（string，示例 M_SVC_GRAPH_INFLUENCE）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 relation_summary.density 为 number（关系密度）、relation_top 为 array（中心性名单） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute | M_SVC_GRAPH_INFLUENCE | INTEG | | | endpoint_id=svc.relation.m_svc_graph_influence catalog_page_id=svc.relation 组合=INF-02 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01664 | 产业服务分析 | 服务关系链 | 异常-入参-非法kind | — | 服务关系链 | 生态影响力评分 | 生态影响力评分传入非法 kind | 1、请求体 kind=__invalid__ | 1.POST /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute，请求体取组合 INF-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_GRAPH_INFLUENCE 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute | | INTEG | | | endpoint_id=svc.relation.m_svc_graph_influence catalog_page_id=svc.relation 组合=INF-03 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01665 | 产业服务分析 | 服务关系链 | 主流程 | — | 服务关系链 | 服务关系链模型 | 服务关系链模型按文档 sampleRequest 传 kind=relation 时返回模型字段 | 1、请求体 kind 使用文档 sampleRequest 的 relation | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute，请求体取组合 D173-01 | 1、返回 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_SVC_DEEP_173_1）、hint（string，sampleResponse 多出字段，示例 真实 compute 响应,以实际调用为准） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute | M_SVC_DEEP_173_1 | INTEG | | | endpoint_id=svc.relation.m_svc_deep_173_1 catalog_page_id=svc.relation 组合=D173-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01666 | 产业服务分析 | 服务关系链 | 备选-参数组合 | 省略 kind | 服务关系链 | 服务关系链模型 | 服务关系链模型不传可选 kind | 1、请求体不传 kind | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute，请求体取组合 D173-02 | 1、返回 body 为对象；2、仍含 metric_id（string，示例 M_SVC_DEEP_173_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 metric_id 为 string（指标 ID） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute | M_SVC_DEEP_173_1 | INTEG | | | endpoint_id=svc.relation.m_svc_deep_173_1 catalog_page_id=svc.relation 组合=D173-02 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01667 | 产业服务分析 | 服务关系链 | 异常-入参-非法kind | — | 服务关系链 | 服务关系链模型 | 服务关系链模型传入非法 kind | 1、请求体 kind=__invalid__ | 1.POST /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute，请求体取组合 D173-03 | 1、返回 body 的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_173_1 的成功结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute | | INTEG | | | endpoint_id=svc.relation.m_svc_deep_173_1 catalog_page_id=svc.relation 组合=D173-03 catalog_status=available |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MOD-01 | svc.relation.models | kind=relation | 主路径（sampleRequest） |
| MOD-02 | svc.relation.models | 不传 kind | 省略可选 kind |
| MOD-03 | svc.relation.models | kind=__invalid__ | 只破坏 kind |
| GRF-01 | svc.relation.graph | limit=40 | 主路径（sampleRequest） |
| GRF-02 | svc.relation.graph | 不传 limit | 省略可选 limit |
| GRF-03 | svc.relation.graph | limit=-1 | 只破坏 limit |
| INF-01 | svc.relation.m_svc_graph_influence | kind=relation | 主路径（sampleRequest） |
| INF-02 | svc.relation.m_svc_graph_influence | 不传 kind | 省略可选 kind |
| INF-03 | svc.relation.m_svc_graph_influence | kind=__invalid__ | 只破坏 kind |
| D173-01 | svc.relation.m_svc_deep_173_1 | kind=relation | 主路径（sampleRequest；params.example 与 options 为 tech，主路径仍取 sample） |
| D173-02 | svc.relation.m_svc_deep_173_1 | 不传 kind | 省略可选 kind |
| D173-03 | svc.relation.m_svc_deep_173_1 | kind=__invalid__ | 只破坏 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 关系链模型 | svc.relation.models | GET | /entan/v1/svc/models | kind? | unavailable |
| 关系链图谱 | svc.relation.graph | GET | /entan/v1/svc/graph | limit? | unavailable |
| 生态影响力评分 | svc.relation.m_svc_graph_influence | POST | /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute | kind? | available |
| 服务关系链模型 | svc.relation.m_svc_deep_173_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute | kind? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.relation.models | API-01656、01657、01658 |
| svc.relation.graph | API-01659、01660、01661 |
| svc.relation.m_svc_graph_influence | API-01662、01663、01664 |
| svc.relation.m_svc_deep_173_1 | API-01665、01666、01667 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 4 个 title 均在功能点列出现，且各有 1 条主流程（API-01656、01659、01662、01665）
- [x] 有参接口：sampleRequest 主流程 1 条；可选参数与 sample 相反（不传）各 1 条；每个参数恰好 1 条非法反向
- [x] unavailable（关系链模型、关系链图谱）仍按 catalog 返回体写主流程，备注注明未交付
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数非法
- [x] 无登录 / Token / 401 / 424
- [x] `coverage-fp.md` 已同步 API-01656～01667

**统计**：接口 **4**；用例 **12** 条（主流程 4、备选 4、反向 4）；编号闭区间 **API-01656**～**API-01667**（父控 R2-批13 分配，连续用满）。
