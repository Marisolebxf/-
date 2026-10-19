# 智能服务集群-科技专题服务算法库测试用例（产业全要素图谱 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：图谱 / 产业全要素图谱 API  
> **catalog**：`entry_id=comp.graph` · `catalog_page_id=comp.graph` · path `/industry-comp/graph`  
> **A 线对照**：`fp-split-by-api-run/work/L13.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：联调台 `http://111.198.38.90:50897/`（接口文档真源 `comp.json` 页 `comp.graph`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第二轮 R2-批16）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | D 浏览 COMP_GRAPH_BROWSE | comp.graph.browse |
| 2 | 实体检索 COMP_ENTITY_SEARCH | comp.graph.entities |
| 3 | 关系查询 COMP_REL_QUERY | comp.graph.relations |
| 4 | 可视化 COMP_GRAPH_VIZ | comp.graph.viz |
| 5 | 语义相似 COMP_SEMANTIC_SIM | comp.graph.similar |
| 6 | 网络指标 COMP_NETWORK_METRIC | comp.graph.metrics |

**条数**：每个接口 1 条主流程（对齐 `sampleRequest`）+ 每个可选参数相对 sample 相反的传/不传 1 条 + 每个参数 1 条反向。必填反向=省略该参数；可选反向=非法值。不交叉乘可选组合。

**取值说明**：浏览 center 用文档示例 `ent:ORG00000002`。关系查询 `sampleRequest` 含 `limit=20`，但 `params` 无 `limit`，主流程及同接口其余组合保留该值，不为 `limit` 另开传/不传或反向。`dst`、`rel` 的 catalog example 为空串且 sample 未传，备选传入同接口 `sampleResponse` 中的 `dst=chain:IC`、`rel=industry_belong`。网络指标 sample 未传 center，备选传入同接口 `sampleResponse.centrality` 的 `ent:ORG00000002`。本页 6 个接口 catalog `status=available`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`（本轮 **API-01731**～**API-01766**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.graph`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01731 | 图谱 | 产业全要素图谱 API | 主流程 | — | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | D 浏览 COMP_GRAPH_BROWSE 按文档 sampleRequest 的 center、hops、limit 查询 | 1、center、hops、limit 使用文档 sampleRequest | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-01 | 1、返回 body 含 op_id（string，示例 COMP_GRAPH_BROWSE）、space（string，示例 demo_gkx_chain，responseFields 恒 demo_gkx_chain）、source（string，示例 pg）；2、written_nodes、written_edges 为 array（示例均为空数组）；3、nodes 为 array（responseFields 节点），元素含 node_key（string，示例 ent:ORG00000002）、name（string，示例 示例企业）、node_type（string，示例 enterprise）、weight（number，示例 1）；4、edges 为 array（responseFields 边，示例空数组）；5、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01732 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 center | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | D 浏览 COMP_GRAPH_BROWSE 不传可选 center（与 sampleRequest 相反） | 1、不传 center；hops、limit 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-02 | 1、返回 body 仍含 op_id（string）、space（string）、source（string）；2、written_nodes、written_edges 仍为 array；3、nodes 仍为 array，元素仍含 node_key、name、node_type（string）与 weight（number）；4、edges 仍为 array；5、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01733 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 hops | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | D 浏览 COMP_GRAPH_BROWSE 不传可选 hops（与 sampleRequest 相反） | 1、不传 hops；center、limit 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-03 | 1、返回 body 仍含 op_id（string）、space（string）、source（string）；2、written_nodes、written_edges 仍为 array；3、nodes 仍为 array，元素仍含 node_key、name、node_type（string）与 weight（number）；4、edges 仍为 array；5、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01734 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 limit | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | D 浏览 COMP_GRAPH_BROWSE 不传可选 limit（与 sampleRequest 相反） | 1、不传 limit；center、hops 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-04 | 1、返回 body 仍含 op_id（string）、space（string）、source（string）；2、written_nodes、written_edges 仍为 array；3、nodes 仍为 array，元素仍含 node_key、name、node_type（string）与 weight（number）；4、edges 仍为 array；5、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01735 | 图谱 | 产业全要素图谱 API | 异常-入参-非法center | — | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | D 浏览 COMP_GRAPH_BROWSE 的 center 非法 | 1、center 取非法值；hops、limit 保持合法 | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-05 | 1、返回 body 的 message 或 msg 指出 center 非法；2、不返回含 nodes 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph | | INTEG | | | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01736 | 图谱 | 产业全要素图谱 API | 异常-入参-非法hops | — | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | D 浏览 COMP_GRAPH_BROWSE 的 hops 非法 | 1、hops 取非法值；center、limit 保持合法 | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-06 | 1、返回 body 的 message 或 msg 指出 hops 非法；2、不返回含 nodes 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph | | INTEG | | | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-06 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01737 | 图谱 | 产业全要素图谱 API | 异常-入参-非法limit | — | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | D 浏览 COMP_GRAPH_BROWSE 的 limit 非法 | 1、limit 取非法值；center、hops 保持合法 | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-07 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 nodes 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph | | INTEG | | | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-07 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01738 | 图谱 | 产业全要素图谱 API | 主流程 | — | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索 COMP_ENTITY_SEARCH 按文档 sampleRequest 的 q、sort、size 查询 | 1、q、sort、size 使用文档 sampleRequest | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-01 | 1、返回 body 含 op_id（string，示例 COMP_ENTITY_SEARCH）、space（string，示例 demo_gkx_chain）、source（string，示例 pg）；2、written_nodes、written_edges 为 array（示例空数组）；3、items 为 array（responseFields 已有点），元素含 vid（string，示例 ent:ORG00000002）、type（string，示例 enterprise）、name（string，示例 量子示例）、weight（number，示例 1）；4、total 为 number（示例 1）；5、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01739 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 sort | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索 COMP_ENTITY_SEARCH 不传可选 sort（与 sampleRequest 相反） | 1、不传 sort；q、size 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-02 | 1、返回 body 仍含 op_id（string）、space（string）、source（string）；2、written_nodes、written_edges 仍为 array；3、items 仍为 array，元素仍含 vid、type、name（string）与 weight（number）；4、total 仍为 number；5、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01740 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 size | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索 COMP_ENTITY_SEARCH 不传可选 size（与 sampleRequest 相反） | 1、不传 size；q、sort 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-03 | 1、返回 body 仍含 op_id（string）、space（string）、source（string）；2、written_nodes、written_edges 仍为 array；3、items 仍为 array，元素仍含 vid、type、name（string）与 weight（number）；4、total 仍为 number；5、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01741 | 图谱 | 产业全要素图谱 API | 异常-入参-缺q | — | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索 COMP_ENTITY_SEARCH 不传必填 q | 1、不传 q；sort、size 保持合法 | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-04 | 1、返回 body 的 message 或 msg 指出 q 缺失；2、不返回含 items 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities | | INTEG | | | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01742 | 图谱 | 产业全要素图谱 API | 异常-入参-非法sort | — | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索 COMP_ENTITY_SEARCH 的 sort 非法 | 1、sort 取枚举外的值；q、size 保持合法 | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-05 | 1、返回 body 的 message 或 msg 指出 sort 非法；2、不返回含 items 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities | | INTEG | | | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01743 | 图谱 | 产业全要素图谱 API | 异常-入参-非法size | — | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索 COMP_ENTITY_SEARCH 的 size 非法 | 1、size 取非法值；q、sort 保持合法 | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-06 | 1、返回 body 的 message 或 msg 指出 size 非法；2、不返回含 items 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities | | INTEG | | | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-06 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01744 | 图谱 | 产业全要素图谱 API | 主流程 | — | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 COMP_REL_QUERY 按文档 sampleRequest 的 src、direction、limit 查询 | 1、src、direction、limit 使用文档 sampleRequest | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-01 | 1、返回 body 含 op_id（string，示例 COMP_REL_QUERY）、space（string，示例 demo_gkx_chain）；2、written_nodes、written_edges 为 array（示例空数组）；3、edges 为 array（responseFields 已有边），元素含 src（string，示例 ent:ORG00000002）、rel（string，示例 industry_belong）、dst（string，示例 chain:IC）、weight（number，示例 1）；4、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01745 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 传入 dst | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 COMP_REL_QUERY 传入可选 dst（sampleRequest 未传） | 1、传入 dst；src、direction、limit 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-02 | 1、返回 body 仍含 op_id（string）、space（string）；2、written_nodes、written_edges 仍为 array；3、edges 仍为 array，元素仍含 src、rel、dst（string）与 weight（number）；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01746 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 传入 rel | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 COMP_REL_QUERY 传入可选 rel（sampleRequest 未传） | 1、传入 rel；src、direction、limit 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-03 | 1、返回 body 仍含 op_id（string）、space（string）；2、written_nodes、written_edges 仍为 array；3、edges 仍为 array，元素仍含 src、rel、dst（string）与 weight（number）；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01747 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 direction | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 COMP_REL_QUERY 不传可选 direction（与 sampleRequest 相反） | 1、不传 direction；src、limit 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-04 | 1、返回 body 仍含 op_id（string）、space（string）；2、written_nodes、written_edges 仍为 array；3、edges 仍为 array，元素仍含 src、rel、dst（string）与 weight（number）；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01748 | 图谱 | 产业全要素图谱 API | 异常-入参-缺src | — | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 COMP_REL_QUERY 不传必填 src | 1、不传 src；direction、limit 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-05 | 1、返回 body 的 message 或 msg 指出 src 缺失；2、不返回含 edges 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations | | INTEG | | | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01749 | 图谱 | 产业全要素图谱 API | 异常-入参-非法dst | — | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 COMP_REL_QUERY 的 dst 非法 | 1、dst 取非法值；src、direction、limit 保持合法 | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-06 | 1、返回 body 的 message 或 msg 指出 dst 非法；2、不返回含 edges 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations | | INTEG | | | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-06 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01750 | 图谱 | 产业全要素图谱 API | 异常-入参-非法rel | — | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 COMP_REL_QUERY 的 rel 非法 | 1、rel 取非法值；src、direction、limit 保持合法 | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-07 | 1、返回 body 的 message 或 msg 指出 rel 非法；2、不返回含 edges 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations | | INTEG | | | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-07 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01751 | 图谱 | 产业全要素图谱 API | 异常-入参-非法direction | — | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 COMP_REL_QUERY 的 direction 非法 | 1、direction 取枚举外的值；src、limit 保持合法 | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-08 | 1、返回 body 的 message 或 msg 指出 direction 非法；2、不返回含 edges 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations | | INTEG | | | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-08 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01752 | 图谱 | 产业全要素图谱 API | 主流程 | — | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 可视化 COMP_GRAPH_VIZ 按文档 sampleRequest 的 layout、limit 查询 | 1、layout、limit 使用文档 sampleRequest | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-01 | 1、返回 body 含 op_id（string，示例 COMP_GRAPH_VIZ）、space（string，示例 demo_gkx_chain）；2、written_nodes、written_edges 为 array（示例空数组）；3、nodes 为 array（responseFields 图节点），元素含 node_key（string，示例 ent:ORG00000002）、name（string，示例 示例）、node_type（string，示例 enterprise）；4、edges 为 array（示例空数组）；5、tags 为 array，元素含 name（string，示例 enterprise）、count（number，示例 1）；6、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01753 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 layout | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 可视化 COMP_GRAPH_VIZ 不传可选 layout（与 sampleRequest 相反） | 1、不传 layout；limit 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-02 | 1、返回 body 仍含 op_id（string）、space（string）；2、written_nodes、written_edges 仍为 array；3、nodes 仍为 array，元素仍含 node_key、name、node_type（string）；4、edges 仍为 array；5、tags 仍为 array，元素仍含 name（string）、count（number）；6、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01754 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 limit | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 可视化 COMP_GRAPH_VIZ 不传可选 limit（与 sampleRequest 相反） | 1、不传 limit；layout 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-03 | 1、返回 body 仍含 op_id（string）、space（string）；2、written_nodes、written_edges 仍为 array；3、nodes 仍为 array，元素仍含 node_key、name、node_type（string）；4、edges 仍为 array；5、tags 仍为 array，元素仍含 name（string）、count（number）；6、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01755 | 图谱 | 产业全要素图谱 API | 异常-入参-非法layout | — | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 可视化 COMP_GRAPH_VIZ 的 layout 非法 | 1、layout 取枚举外的值；limit 保持合法 | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-04 | 1、返回 body 的 message 或 msg 指出 layout 非法；2、不返回含 nodes 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz | | INTEG | | | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01756 | 图谱 | 产业全要素图谱 API | 异常-入参-非法limit | — | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 可视化 COMP_GRAPH_VIZ 的 limit 非法 | 1、limit 取非法值；layout 保持合法 | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 nodes 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz | | INTEG | | | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01757 | 图谱 | 产业全要素图谱 API | 主流程 | — | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似 COMP_SEMANTIC_SIM 按文档 sampleRequest 的 a、b、mode 计算 | 1、a、b、mode 使用文档 sampleRequest | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-01 | 1、返回 body 含 op_id（string，示例 COMP_SEMANTIC_SIM）、space（string，示例 demo_gkx_chain）、score（number，responseFields 0–1，示例 0.5）、source（string，示例 rule）、model_version（string，示例 comp_query_v1）、llm_fallback（boolean，示例 false）；2、written_nodes、written_edges 为 array（示例空数组）；3、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01758 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 mode | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似 COMP_SEMANTIC_SIM 不传可选 mode（与 sampleRequest 相反） | 1、不传 mode；a、b 保持 sampleRequest | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-02 | 1、返回 body 仍含 op_id（string）、space（string）、score（number）、source（string）、model_version（string）、llm_fallback（boolean）；2、written_nodes、written_edges 仍为 array；3、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01759 | 图谱 | 产业全要素图谱 API | 异常-入参-缺a | — | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似 COMP_SEMANTIC_SIM 不传必填 a | 1、不传 a；b、mode 保持 sampleRequest | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-03 | 1、返回 body 的 message 或 msg 指出 a 缺失；2、不返回含 score 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar | | INTEG | | | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01760 | 图谱 | 产业全要素图谱 API | 异常-入参-缺b | — | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似 COMP_SEMANTIC_SIM 不传必填 b | 1、不传 b；a、mode 保持 sampleRequest | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-04 | 1、返回 body 的 message 或 msg 指出 b 缺失；2、不返回含 score 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar | | INTEG | | | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01761 | 图谱 | 产业全要素图谱 API | 异常-入参-非法mode | — | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似 COMP_SEMANTIC_SIM 的 mode 非法 | 1、mode 取枚举外的值；a、b 保持合法 | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-05 | 1、返回 body 的 message 或 msg 指出 mode 非法；2、不返回含 score 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar | | INTEG | | | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01762 | 图谱 | 产业全要素图谱 API | 主流程 | — | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标 COMP_NETWORK_METRIC 按文档 sampleRequest 仅传 limit 查询 | 1、limit 使用文档 sampleRequest；不传 center | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-01 | 1、返回 body 含 op_id（string，示例 COMP_NETWORK_METRIC）、space（string，示例 demo_gkx_chain）、density（number，responseFields 密度，示例 0）、node_count（number，示例 1）、edge_count（number，示例 0）；2、centrality 为 array，元素含 vid（string，示例 ent:ORG00000002）、degree（number，示例 0）；3、written_nodes、written_edges 为 array（示例空数组）；4、结构与 sampleResponse 一致 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01763 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 传入 center | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标 COMP_NETWORK_METRIC 传入可选 center（sampleRequest 未传） | 1、传入 center；limit 保持 sampleRequest | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-02 | 1、返回 body 仍含 op_id（string）、space（string）、density（number）、node_count（number）、edge_count（number）；2、centrality 仍为 array，元素仍含 vid（string）、degree（number）；3、written_nodes、written_edges 仍为 array；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01764 | 图谱 | 产业全要素图谱 API | 备选-参数组合 | 省略 limit | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标 COMP_NETWORK_METRIC 不传可选 limit（与 sampleRequest 相反） | 1、不传 center、不传 limit | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-03 | 1、返回 body 仍含 op_id（string）、space（string）、density（number）、node_count（number）、edge_count（number）；2、centrality 仍为 array，元素仍含 vid（string）、degree（number）；3、written_nodes、written_edges 仍为 array；4、结构与 sampleResponse 同类 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics | M_COMP_GRAPH_116_1 | INTEG | | | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01765 | 图谱 | 产业全要素图谱 API | 异常-入参-非法center | — | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标 COMP_NETWORK_METRIC 的 center 非法 | 1、center 取非法值；limit 保持合法 | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-04 | 1、返回 body 的 message 或 msg 指出 center 非法；2、不返回含 density 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics | | INTEG | | | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-01766 | 图谱 | 产业全要素图谱 API | 异常-入参-非法limit | — | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标 COMP_NETWORK_METRIC 的 limit 非法 | 1、limit 取非法值；不传 center | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-05 | 1、返回 body 的 message 或 msg 指出 limit 非法；2、不返回含 density 的成功业务结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics | | INTEG | | | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-05 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| BRW-01 | comp.graph.browse | center=ent:ORG00000002；hops=1；limit=40 | 主路径全参（sampleRequest） |
| BRW-02 | comp.graph.browse | 不传 center；hops=1；limit=40 | 省略可选 center |
| BRW-03 | comp.graph.browse | center=ent:ORG00000002；不传 hops；limit=40 | 省略可选 hops |
| BRW-04 | comp.graph.browse | center=ent:ORG00000002；hops=1；不传 limit | 省略可选 limit |
| BRW-05 | comp.graph.browse | center=__invalid__；hops=1；limit=40 | 只破坏 center |
| BRW-06 | comp.graph.browse | center=ent:ORG00000002；hops=-1；limit=40 | 只破坏 hops |
| BRW-07 | comp.graph.browse | center=ent:ORG00000002；hops=1；limit=-1 | 只破坏 limit |
| ENT-01 | comp.graph.entities | q=量子；sort=name；size=20 | 主路径全参（sampleRequest） |
| ENT-02 | comp.graph.entities | q=量子；不传 sort；size=20 | 省略可选 sort |
| ENT-03 | comp.graph.entities | q=量子；sort=name；不传 size | 省略可选 size |
| ENT-04 | comp.graph.entities | 不传 q；sort=name；size=20 | 缺必填 q |
| ENT-05 | comp.graph.entities | q=量子；sort=__invalid__；size=20 | 只破坏 sort |
| ENT-06 | comp.graph.entities | q=量子；sort=name；size=-1 | 只破坏 size |
| REL-01 | comp.graph.relations | src=ent:ORG00000002；direction=both；limit=20 | 主路径（sampleRequest；limit 不在 params） |
| REL-02 | comp.graph.relations | src=ent:ORG00000002；dst=chain:IC；direction=both；limit=20 | 传入可选 dst（sample 未传） |
| REL-03 | comp.graph.relations | src=ent:ORG00000002；rel=industry_belong；direction=both；limit=20 | 传入可选 rel（sample 未传） |
| REL-04 | comp.graph.relations | src=ent:ORG00000002；不传 direction；limit=20 | 省略可选 direction |
| REL-05 | comp.graph.relations | 不传 src；direction=both；limit=20 | 缺必填 src |
| REL-06 | comp.graph.relations | src=ent:ORG00000002；dst=__invalid__；direction=both；limit=20 | 只破坏 dst |
| REL-07 | comp.graph.relations | src=ent:ORG00000002；rel=__invalid__；direction=both；limit=20 | 只破坏 rel |
| REL-08 | comp.graph.relations | src=ent:ORG00000002；direction=__invalid__；limit=20 | 只破坏 direction |
| VIZ-01 | comp.graph.viz | layout=graph；limit=40 | 主路径全参（sampleRequest） |
| VIZ-02 | comp.graph.viz | 不传 layout；limit=40 | 省略可选 layout |
| VIZ-03 | comp.graph.viz | layout=graph；不传 limit | 省略可选 limit |
| VIZ-04 | comp.graph.viz | layout=__invalid__；limit=40 | 只破坏 layout |
| VIZ-05 | comp.graph.viz | layout=graph；limit=-1 | 只破坏 limit |
| SIM-01 | comp.graph.similar | a=量子；b=量子计算；mode=rule | 主路径全参（sampleRequest） |
| SIM-02 | comp.graph.similar | a=量子；b=量子计算；不传 mode | 省略可选 mode |
| SIM-03 | comp.graph.similar | 不传 a；b=量子计算；mode=rule | 缺必填 a |
| SIM-04 | comp.graph.similar | a=量子；不传 b；mode=rule | 缺必填 b |
| SIM-05 | comp.graph.similar | a=量子；b=量子计算；mode=__invalid__ | 只破坏 mode |
| MET-01 | comp.graph.metrics | 不传 center；limit=40 | 主路径（sampleRequest） |
| MET-02 | comp.graph.metrics | center=ent:ORG00000002；limit=40 | 传入可选 center（sample 未传） |
| MET-03 | comp.graph.metrics | 不传 center；不传 limit | 省略可选 limit |
| MET-04 | comp.graph.metrics | center=__invalid__；limit=40 | 只破坏 center |
| MET-05 | comp.graph.metrics | 不传 center；limit=-1 | 只破坏 limit |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| D 浏览 COMP_GRAPH_BROWSE | comp.graph.browse | GET | /industry-comp/v1/comp/graph | center?；hops?；limit? | available |
| 实体检索 COMP_ENTITY_SEARCH | comp.graph.entities | GET | /industry-comp/v1/comp/graph/entities | q*；sort?；size? | available |
| 关系查询 COMP_REL_QUERY | comp.graph.relations | GET | /industry-comp/v1/comp/graph/relations | src*；dst?；rel?；direction? | available |
| 可视化 COMP_GRAPH_VIZ | comp.graph.viz | GET | /industry-comp/v1/comp/graph/viz | layout?；limit? | available |
| 语义相似 COMP_SEMANTIC_SIM | comp.graph.similar | POST | /industry-comp/v1/comp/graph/similar | a*；b*；mode? | available |
| 网络指标 COMP_NETWORK_METRIC | comp.graph.metrics | GET | /industry-comp/v1/comp/graph/metrics | center?；limit? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.graph.browse | API-01731、01732、01733、01734、01735、01736、01737 |
| comp.graph.entities | API-01738、01739、01740、01741、01742、01743 |
| comp.graph.relations | API-01744、01745、01746、01747、01748、01749、01750、01751 |
| comp.graph.viz | API-01752、01753、01754、01755、01756 |
| comp.graph.similar | API-01757、01758、01759、01760、01761 |
| comp.graph.metrics | API-01762、01763、01764、01765、01766 |

---

## 3. 覆盖自检（第二轮口径）

- [x] 6 个 title 均在功能点列出现，且各有 1 条主流程（01731、01738、01744、01752、01757、01762）
- [x] 有参接口：sampleRequest 主流程 + 每个可选参数与 sample 相反的传/不传 + 每参数 1 条反向（必填省略、可选非法）
- [x] 正向预期逐字段写 sampleResponse；反向预期写 message 或 msg 指出该参数缺失或非法
- [x] 无鉴权类用例
- [x] `coverage-fp.md` 已同步 API-01731～01766；未改 A 线 work

**统计**：接口 **6**；用例 **36** 条（主流程 6、备选 13、反向 17）；编号闭区间 **API-01731**～**API-01766**（父控 R2-批16 分配，连续用满）。
