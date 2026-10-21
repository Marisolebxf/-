# 服务关系链 · 功能点覆盖（svc.relation / L42）

> catalog `svc.relation` · path `#/industry-service/relation`  
> A 线真源：`fp-split-by-api-run/work/L42.md`  
> B 线用例：`FUNC-服务关系链-用例.md`（第三轮 **FUNC-00870**～**FUNC-00883**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| svc.relation.models | GET | /entan/v1/svc/models | FUNC-00870～00872 | unavailable |
| svc.relation.graph | GET | /entan/v1/svc/graph | FUNC-00873～00875 | unavailable |
| svc.relation.m_svc_graph_influence | POST | /entan/v1/svc-metric/metric/M_SVC_GRAPH_INFLUENCE/compute | FUNC-00876～00878 | available |
| svc.relation.m_svc_deep_173_1 | POST | /entan/v1/svc-metric/metric/M_SVC_DEEP_173_1/compute | FUNC-00879～00881 | available |
| （页面清单） | — | — | FUNC-00882、00883 | — |

---

## 功能点 → 用例矩阵（挂 L42.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L42 \| svc.relation.models \| kind \| 算法输入-kind模型类型 | catalog kind | FUNC-00870、00871、00872 | 已覆盖 | 主路径 kind=relation + 省略 kind + 非法 kind=__invalid__ |
| L42 \| svc.relation.models \| relation_summary.density \| 算法输出-relation_summary.density关系密度 | catalog relation_summary.density | FUNC-00870、00871 | 已覆盖 | 主流程断言 density（number，示例 0.042）及 ext.node_count、ext.link_count；备选同结构 |
| L42 \| svc.relation.models \| relation_top \| 算法输出-relation_top关键机构列表 | catalog relation_top | FUNC-00870、00871 | 已覆盖 | 主流程断言 relation_top 元素 org_id、ext.name、centrality；备选同结构 |
| L42 \| svc.relation.models \| _empty \| 关系链模型无数据空态 | 契约空结果 | — | 未覆盖 | sampleResponse 为非空 relation_summary/relation_top，无稳定空结果构造条件，不单开空态用例 |
| L42 \| svc.relation.models \| _fail \| 关系链模型查询失败 | 契约错误态 | FUNC-00872 | 部分覆盖 | 仅非法 kind 反向，预期 message 或 msg 指出 kind 非法 |
| L42 \| svc.relation.graph \| limit \| 算法输入-limit节点上限 | catalog limit | FUNC-00873、00874、00875 | 已覆盖 | 主路径 limit=40 + 省略 limit + 非法 limit=-1 |
| L42 \| svc.relation.graph \| nodes \| 算法输出-nodes网络节点 | catalog nodes | FUNC-00873、00874 | 已覆盖 | 主流程断言 nodes 元素 id、name、weight；备选同结构 |
| L42 \| svc.relation.graph \| edges \| 算法输出-edges关系边 | catalog edges | FUNC-00873、00874 | 已覆盖 | 主流程断言 edges 元素 source、target、mapped_from、relation；备选同结构 |
| L42 \| svc.relation.graph \| _empty \| 关系链图谱无数据空态 | 契约空结果 | — | 未覆盖 | sampleResponse 为非空 nodes/edges，无稳定空图构造条件，不单开空态用例 |
| L42 \| svc.relation.graph \| _fail \| 关系链图谱查询失败 | 契约错误态 | FUNC-00875 | 部分覆盖 | 仅非法 limit 反向，预期 message 或 msg 指出 limit 非法 |

---

## req_only 行（无 endpoint 挂接）

L42.md 中 `etl_clean_standardize`、`strength_layer_density_indicators`、`stability_closeness_compute`、`risk_coop_optimization_semantic`、`structure_analysis_report`、`key_org_match_scheme`、`org_type_industry_time_scope`、`report_chart_risk_trend_outputs`、`auto_monitor_dynamic_refresh`、`api_sdk_regulatory_platform` 共 10 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

---

## B 线独有（A 线未列 endpoint）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| svc.relation.m_svc_graph_influence | FUNC-00876～00878 | 无对应功能点 | L42 未列该 compute endpoint；用例仍按 catalog 编写 |
| svc.relation.m_svc_deep_173_1 | FUNC-00879～00881 | 无对应功能点 | L42 未列该 compute endpoint；用例仍按 catalog 编写 |

sampleResponse 中 density 的 ext、relation_top 成员，以及 nodes/edges 成员已写入对应正向预期；A 线只列顶层 field_key，不按子成员拆行。
