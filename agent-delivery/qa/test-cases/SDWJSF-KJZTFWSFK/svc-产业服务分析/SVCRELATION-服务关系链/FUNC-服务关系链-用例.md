# 智能服务集群-科技专题服务算法库测试用例（服务关系链 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=svc.relation` · `catalog_page_id=svc.relation` · path `#/industry-service/relation`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/svc.json` · 页 `svc.relation`  
> **A 线对照**：`fp-split-by-api-run/work/L42.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批14）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 关系链模型 | svc.relation.models | unavailable |
| 2 | 关系链图谱 | svc.relation.graph | unavailable |
| 3 | 生态影响力评分 | svc.relation.m_svc_graph_influence | available |
| 4 | 服务关系链模型 | svc.relation.m_svc_deep_173_1 | available |

四个接口各只有 1 个可选参数。`sampleRequest` 均传入该参数：关系链模型与两个 compute 为 `kind=relation`，关系链图谱为 `limit=40`。备选与 sample 相反，不传该参数；反向各 1 条，只把该参数改为非法值。`服务关系链模型` 的 `params.example` 与 options 为 `tech`，主路径仍取 `sampleRequest` 的 `relation`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00870**～**FUNC-00883**，共 **14** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.relation`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00870 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 关系链模型 | 验证关系链模型功能，检查填写 kind=relation调用后返回关系密度与中心性名单 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 使用文档 sampleRequest 的 relation | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「关系链模型」；4.填写 kind=relation，点击调用 | 1、返回面板 body 为对象；2、relation_summary.density 为 number（responseFields 关系密度，示例 0.042）；3、relation_summary.ext.node_count 为 number（示例 18）、relation_summary.ext.link_count 为 number（示例 27）；4、relation_top 为 array（responseFields 中心性名单）；5、元素含 org_id（string）、ext.name（string）、centrality（number）；6、sampleResponse 三条：org_id=svc:ns_fin、name=南山科技金融站、centrality=0.86；org_id=svc:ip_sz、name=知产服务中心、centrality=0.71；org_id=svc:hr_ft、name=福田人才服务港、centrality=0.58 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_RELATION_DENSITY | INTEG |  | FUNC-00870 | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00871 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 关系链模型 | 验证关系链模型功能，检查不传 kind 后仍返回关系密度与中心性名单结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「关系链模型」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 为对象；2、relation_summary.density 仍为 number（responseFields 关系密度）；3、relation_summary.ext 仍含 node_count（number）、link_count（number）；4、relation_top 仍为 array，元素仍含 org_id（string）、ext.name（string）、centrality（number）；5、结构与 sampleResponse 同类，示例仍为 density=0.042、node_count=18、link_count=27，以及 svc:ns_fin/南山科技金融站/0.86、svc:ip_sz/知产服务中心/0.71、svc:hr_ft/福田人才服务港/0.58 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_RELATION_DENSITY | INTEG |  | FUNC-00871 | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00872 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 关系链模型 | 验证关系链模型功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「关系链模型」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 density 的成功 relation_summary | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/models |  | INTEG |  | FUNC-00872 | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-03 场景=异常-入参-非法kind catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00873 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 关系链图谱 | 验证关系链图谱功能，检查填写 limit=40调用后返回节点与边 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit 使用文档 sampleRequest 的 40 | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「关系链图谱」；4.填写 limit=40，点击调用 | 1、返回面板 body 为对象；2、nodes 为 array（responseFields 节点）；3、元素含 id（string）、name（string）、weight（number）；4、sampleResponse 三条：id=svc:ns_fin、name=南山科技金融站、weight=1.4；id=svc:ip_sz、name=知产服务中心、weight=1.1；id=svc:hr_ft、name=福田人才服务港、weight=0.9；5、edges 为 array（responseFields 边）；6、元素含 source（string）、target（string）、mapped_from（string）、relation（string）；7、示例 source=svc:ns_fin、target=svc:ip_sz、mapped_from=cooperation、relation=合作 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph |  | INTEG |  | FUNC-00873 | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00874 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 关系链图谱 | 验证关系链图谱功能，检查不传 limit 后仍返回节点与边结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 limit | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「关系链图谱」；4.不传 limit，点击调用（不传 limit），点击调用 | 1、返回面板 body 为对象；2、nodes 仍为 array（responseFields 节点），元素仍含 id（string）、name（string）、weight（number）；3、edges 仍为 array（responseFields 边），元素仍含 source（string）、target（string）、mapped_from（string）、relation（string）；4、结构与 sampleResponse 同类，示例仍为 svc:ns_fin/南山科技金融站/1.4、svc:ip_sz/知产服务中心/1.1、svc:hr_ft/福田人才服务港/0.9，以及 source=svc:ns_fin、target=svc:ip_sz、mapped_from=cooperation、relation=合作 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph |  | INTEG |  | FUNC-00874 | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00875 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 关系链图谱 | 验证关系链图谱功能，检查 limit 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、limit=-1 | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「关系链图谱」；4.填写 limit=-1，点击调用 | 1、返回面板的 message 或 msg 指出 limit 非法；2、不返回含 nodes、edges 的成功结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph |  | INTEG |  | FUNC-00875 | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-03 场景=异常-入参-非法limit catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00876 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 生态影响力评分 | 验证生态影响力评分功能，检查填写 kind=relation调用后返回评分字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 使用文档 sampleRequest 的 relation | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「生态影响力评分」；4.填写 kind=relation，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，示例 M_SVC_GRAPH_INFLUENCE）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 另列 relation_summary.density（number，关系密度）、relation_top（array，中心性名单），sampleResponse 未给这两字段的示例值 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute | M_SVC_GRAPH_INFLUENCE | INTEG |  | FUNC-00876 | endpoint_id=svc.relation.m_svc_graph_influence catalog_page_id=svc.relation 组合=INF-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00877 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 生态影响力评分 | 验证生态影响力评分功能，检查不传 kind 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「生态影响力评分」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 为对象；2、仍含 metric_id（string，示例 M_SVC_GRAPH_INFLUENCE）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 relation_summary.density 为 number（关系密度）、relation_top 为 array（中心性名单） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute | M_SVC_GRAPH_INFLUENCE | INTEG |  | FUNC-00877 | endpoint_id=svc.relation.m_svc_graph_influence catalog_page_id=svc.relation 组合=INF-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00878 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 生态影响力评分 | 验证生态影响力评分功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「生态影响力评分」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_GRAPH_INFLUENCE 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute |  | INTEG |  | FUNC-00878 | endpoint_id=svc.relation.m_svc_graph_influence catalog_page_id=svc.relation 组合=INF-03 场景=异常-入参-非法kind catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00879 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 服务关系链模型 | 验证服务关系链模型功能，检查填写 kind=relation调用后返回模型字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 使用文档 sampleRequest 的 relation | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「服务关系链模型」；4.填写 kind=relation，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_SVC_DEEP_173_1）、hint（string，sampleResponse 多出字段，示例 真实 compute 响应,以实际调用为准） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute | M_SVC_DEEP_173_1 | INTEG |  | FUNC-00879 | endpoint_id=svc.relation.m_svc_deep_173_1 catalog_page_id=svc.relation 组合=D173-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00880 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 服务关系链模型 | 验证服务关系链模型功能，检查不传 kind 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「服务关系链模型」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板 body 为对象；2、仍含 metric_id（string，示例 M_SVC_DEEP_173_1）、hint（string，示例 真实 compute 响应,以实际调用为准）；3、responseFields 的 metric_id 为 string（指标 ID） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute | M_SVC_DEEP_173_1 | INTEG |  | FUNC-00880 | endpoint_id=svc.relation.m_svc_deep_173_1 catalog_page_id=svc.relation 组合=D173-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00881 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 服务关系链模型 | 验证服务关系链模型功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换至「算法测试」tab；3.接口下拉选择「服务关系链模型」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 metric_id 为 M_SVC_DEEP_173_1 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute |  | INTEG |  | FUNC-00881 | endpoint_id=svc.relation.m_svc_deep_173_1 catalog_page_id=svc.relation 组合=D173-03 场景=异常-入参-非法kind catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00882 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 接口信息 | 验证服务关系链的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「服务关系链」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 4；2、下拉名称与 §0 各 title 一致（关系链模型、关系链图谱、生态影响力评分、服务关系链模型）；3、默认项概览 method=GET、path=/entan/v1/svc/models；4、切换后概览对应关系链图谱 GET /entan/v1/svc/graph、生态影响力评分 POST /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00882 | catalog_page_id=svc.relation 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00883 | 算法工具库 | 科技专题服务算法库 | 产业服务深度分析模型构建 | 服务关系链模型 | 服务关系链 | 算法测试 | 验证服务关系链的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业服务分析」→「服务关系链」；2.切换到「算法测试」tab；3.下拉切换到「关系链图谱」 | 1、算法测试 tab 下拉共 4 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「关系链图谱」；3、调用区 method 为 GET、path 为 /entan/v1/svc/graph；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-00883 | catalog_page_id=svc.relation 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

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
| svc.relation.models | FUNC-00870、00871、00872 |
| svc.relation.graph | FUNC-00873、00874、00875 |
| svc.relation.m_svc_graph_influence | FUNC-00876、00877、00878 |
| svc.relation.m_svc_deep_173_1 | FUNC-00879、00880、00881 |
| （页面清单） | FUNC-00882、00883 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 4 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-00870、00873、00876、00879）
- [x] 有参接口：sampleRequest 主流程 1 条；可选参数与 sample 相反（不传）各 1 条；每个参数恰好 1 条非法反向
- [x] unavailable（关系链模型、关系链图谱）仍按 catalog 返回体写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L42（产业服务深度分析模型构建 / 服务关系链模型）
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件；功能点无 A1/A2 后缀
- [x] 多接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-00870～00883

**统计**：catalog endpoint **4**；title **4**；FUNC 用例 **14** 条；主流程 **4**、备选 **4**、反向 **4**、清单 **2**；编号闭区间 **FUNC-00870**～**FUNC-00883**（R3-批14 svc.relation）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **14** |
| 编号闭区间 | **FUNC-00870**～**FUNC-00883** |
| 接口向（不含清单） | **12** |
| 主流程 | **4** |
| 备选-参数组合 | **4** |
| 反向 | **4** |
| 清单 | **2** |
| 已删 API 册 | `API-服务关系链-用例.md`（API-01656～01667 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
