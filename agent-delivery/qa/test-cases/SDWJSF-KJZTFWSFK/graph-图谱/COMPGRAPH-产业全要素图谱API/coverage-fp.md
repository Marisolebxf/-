# 产业全要素图谱 API · 功能点覆盖（comp.graph / L13）

> catalog `comp.graph` · path `#/industry-comp/graph`  
> A 线真源：`fp-split-by-api-run/work/L13.md`（只读，未改）  
> B 线用例：`FUNC-产业全要素图谱API-用例.md`（第三轮 **FUNC-00969**～**01006**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.graph.browse | GET | /industry-comp/v1/comp/graph | FUNC-00969～00975 | available |
| comp.graph.entities | GET | /industry-comp/v1/comp/graph/entities | FUNC-00976～FUNC-00981 | available |
| comp.graph.relations | GET | /industry-comp/v1/comp/graph/relations | FUNC-00982～FUNC-00989 | available |
| comp.graph.viz | GET | /industry-comp/v1/comp/graph/viz | FUNC-00990～FUNC-00994 | available |
| comp.graph.similar | POST | /industry-comp/v1/comp/graph/similar | FUNC-00995～FUNC-00999 | available |
| comp.graph.metrics | GET | /industry-comp/v1/comp/graph/metrics | FUNC-01000～FUNC-01004 | available |

---

## 功能点 → 用例矩阵（挂 L13.md）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L13 \| comp.graph.browse \| center \| 算法输入-center稳定 VID | catalog center | FUNC-00969、00970、00973 | 已覆盖 | 主路径传入 + 省略可选 center + 非法 center=__invalid__ |
| L13 \| comp.graph.browse \| hops \| 算法输入-hops邻域跳数 | catalog hops | FUNC-00969、00971、00974 | 已覆盖 | 主路径 hops=1 + 省略 + 非法 hops=-1 |
| L13 \| comp.graph.browse \| limit \| 算法输入-limit节点上限 | catalog limit | FUNC-00969、00972、00975 | 已覆盖 | 主路径 limit=40 + 省略 + 非法 limit=-1 |
| L13 \| comp.graph.browse \| nodes \| 算法输出-nodes节点 | catalog nodes | FUNC-00969 | 已覆盖 | 主流程逐字段断言 nodes 及元素字段；备选 FUNC-00970～FUNC-00972 同结构 |
| L13 \| comp.graph.browse \| edges \| 算法输出-edges边 | catalog edges | FUNC-00969 | 已覆盖 | 主流程断言 edges（array）；备选同结构 |
| L13 \| comp.graph.browse \| space \| 算法输出-space恒 demo_gkx_chain | catalog space | FUNC-00969 | 已覆盖 | 主流程断言 space（string，示例 demo_gkx_chain） |
| L13 \| comp.graph.browse \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L13 \| comp.graph.browse \| _fail \| 调用失败 | 契约错误态 | FUNC-00973、FUNC-00974、FUNC-00975 | 已覆盖 | 三参数各 1 条反向，预期 message 或 msg |
| L13 \| comp.graph.entities \| q \| 算法输入-q关键词或 VID | catalog q | FUNC-00976、FUNC-00979 | 已覆盖 | 主路径 q=量子 + 省略必填 q；备选 FUNC-00977、FUNC-00978 仍传合法 q |
| L13 \| comp.graph.entities \| sort \| 算法输入-sortname/-name/weight/-weight/vid/-vid | catalog sort | FUNC-00976、FUNC-00977、FUNC-00980 | 已覆盖 | 主路径 sort=name + 省略 + 非法 sort=__invalid__ |
| L13 \| comp.graph.entities \| size \| 算法输入-size页大小 | catalog size | FUNC-00976、FUNC-00978、FUNC-00981 | 已覆盖 | 主路径 size=20 + 省略 + 非法 size=-1 |
| L13 \| comp.graph.entities \| items \| 算法输出-items已有点 | catalog items | FUNC-00976 | 已覆盖 | 主流程逐字段断言 items 及 vid、type、name、weight；备选 FUNC-00977、FUNC-00978 同结构 |
| L13 \| comp.graph.entities \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L13 \| comp.graph.entities \| _fail \| 调用失败 | 契约错误态 | FUNC-00979、FUNC-00980、FUNC-00981 | 已覆盖 | 缺 q、非法 sort、非法 size，预期 message 或 msg |
| L13 \| comp.graph.relations \| src \| 算法输入-src源稳定 VID | catalog src | FUNC-00982、FUNC-00986 | 已覆盖 | 主路径 src=ent:ORG00000002 + 省略必填 src |
| L13 \| comp.graph.relations \| dst \| 算法输入-dst对端 VID | catalog dst | FUNC-00983、FUNC-00987 | 已覆盖 | sample 未传，备选传入 dst=chain:IC；反向 dst=__invalid__ |
| L13 \| comp.graph.relations \| rel \| 算法输入-rel已上图边类型 | catalog rel | FUNC-00984、FUNC-00988 | 已覆盖 | sample 未传，备选传入 rel=industry_belong；反向 rel=__invalid__ |
| L13 \| comp.graph.relations \| direction \| 算法输入-directionboth/out/in | catalog direction | FUNC-00982、FUNC-00985、FUNC-00989 | 已覆盖 | 主路径 direction=both + 省略 + 非法 direction=__invalid__ |
| L13 \| comp.graph.relations \| edges \| 算法输出-edges已有边 | catalog edges | FUNC-00982 | 已覆盖 | 主流程逐字段断言 edges 及 src、rel、dst、weight；备选 FUNC-00983～FUNC-00985 同结构 |
| L13 \| comp.graph.relations \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L13 \| comp.graph.relations \| _fail \| 调用失败 | 契约错误态 | FUNC-00986、FUNC-00987、FUNC-00988、FUNC-00989 | 已覆盖 | 缺 src 与非法 dst、rel、direction，预期 message 或 msg |
| L13 \| comp.graph.viz \| layout \| 算法输入-layoutgraph/wordcloud | catalog layout | FUNC-00990、FUNC-00991、FUNC-00993 | 已覆盖 | 主路径 layout=graph + 省略 + 非法 layout=__invalid__ |
| L13 \| comp.graph.viz \| limit \| 算法输入-limit上限 | catalog limit | FUNC-00990、FUNC-00992、FUNC-00994 | 已覆盖 | 主路径 limit=40 + 省略 + 非法 limit=-1 |
| L13 \| comp.graph.viz \| nodes \| 算法输出-nodes图节点 | catalog nodes | FUNC-00990 | 已覆盖 | 主流程逐字段断言 nodes；备选 FUNC-00991、FUNC-00992 同结构 |
| L13 \| comp.graph.viz \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L13 \| comp.graph.viz \| _fail \| 调用失败 | 契约错误态 | FUNC-00993、FUNC-00994 | 已覆盖 | 非法 layout、非法 limit，预期 message 或 msg |
| L13 \| comp.graph.similar \| a \| 算法输入-a名称或 VID | catalog a | FUNC-00995、FUNC-00997 | 已覆盖 | 主路径 a=量子 + 省略必填 a |
| L13 \| comp.graph.similar \| b \| 算法输入-b名称或 VID | catalog b | FUNC-00995、FUNC-00998 | 已覆盖 | 主路径 b=量子计算 + 省略必填 b |
| L13 \| comp.graph.similar \| mode \| 算法输入-moderule/llm | catalog mode | FUNC-00995、FUNC-00996、FUNC-00999 | 已覆盖 | 主路径 mode=rule + 省略 + 非法 mode=__invalid__ |
| L13 \| comp.graph.similar \| score \| 算法输出-score0–1 | catalog score | FUNC-00995 | 已覆盖 | 主流程断言 score（number）；备选 FUNC-00996 同结构 |
| L13 \| comp.graph.similar \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L13 \| comp.graph.similar \| _fail \| 调用失败 | 契约错误态 | FUNC-00997、FUNC-00998、FUNC-00999 | 已覆盖 | 缺 a、缺 b、非法 mode，预期 message 或 msg |
| L13 \| comp.graph.metrics \| center \| 算法输入-center中心 VID | catalog center | FUNC-01000、FUNC-01001、FUNC-01003 | 已覆盖 | 主路径按 sample 不传 center + 备选传入 + 非法 center=__invalid__ |
| L13 \| comp.graph.metrics \| limit \| 算法输入-limit子图上限 | catalog limit | FUNC-01000、FUNC-01002、FUNC-01004 | 已覆盖 | 主路径 limit=40 + 省略 + 非法 limit=-1 |
| L13 \| comp.graph.metrics \| density \| 算法输出-density密度 | catalog density | FUNC-01000 | 已覆盖 | 主流程断言 density（number）；备选 FUNC-01001、FUNC-01002 同结构 |
| L13 \| comp.graph.metrics \| _empty \| 查询无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L13 \| comp.graph.metrics \| _fail \| 调用失败 | 契约错误态 | FUNC-01003、FUNC-01004 | 已覆盖 | 非法 center、非法 limit，预期 message 或 msg |

---

## req_only 行（无 endpoint 挂接）

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L13 \| （页级） \| ext_integration_semantic \| 外部系统集成调用 | 需规应用场景 | — | 无对应功能点 | req_only，catalog 无单独集成字段，不单开 FUNC 用例 |
| L13 \| （页级） \| knowledge_expand_semantic \| 知识扩充应用场景 | 需规应用场景 | — | 无对应功能点 | req_only，本页以 COMP_* 查询承载，不单开 FUNC 用例 |

sampleResponse 中另有、A 线未单列的 field 已写入对应主流程正向预期：浏览的 `op_id`、`source`、`written_nodes`、`written_edges` 及 nodes 元素 `node_key`、`name`、`node_type`、`weight`；实体检索的 `op_id`、`source`、`written_*`、`total` 及 items 元素字段；关系查询的 `op_id`、`written_*` 及 edges 元素字段；可视化的 `op_id`、`written_*`、`edges`、`tags`；语义相似的 `op_id`、`source`、`model_version`、`llm_fallback`、`written_*`；网络指标的 `op_id`、`node_count`、`edge_count`、`centrality`、`written_*`。

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 31（入参、出参、`_fail`） |
| 未覆盖 | 6（各接口 `_empty`） |
| 无对应功能点 | 2（req_only） |
| L13 矩阵行 | 39 |
| API 用例 | 36（FUNC-00969～FUNC-01004，连续用满） |
