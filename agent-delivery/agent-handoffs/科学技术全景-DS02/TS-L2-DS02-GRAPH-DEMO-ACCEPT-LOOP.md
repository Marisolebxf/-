# TS-L2-DS02-GRAPH-DEMO-ACCEPT-LOOP

- 验收单：`TS-L2-DS02-GRAPH-DEMO-ACCEPT-LOOP`
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS02-GRAPH-合规演示用例.md`
- 监管：`human:淮政玮`

## 运行 2026-11-07

- 用例：同上
- 库：只读对照既有用例取数基线（Nebula `demo_gkx_chain`、ADS `ads_technology_panorama_score`）。本轮跳板机两次未列出 Running 的 `lumen-platform-algo-py` pod，未再开第三轮 SSH；网关侧已实测。
- 探测：`POST .../display/v1/situation/panorama/graph` body `{}` → HTTP 200（token 有效，映射存在）
- 样本满足：否
- 停止：继续（已建缺口子任务，等人说「可以派了」）

### 可演行对照

| 行 | 结果 | 现况 |
|---|---|---|
| 18 节点 | 通过 | nodes=200，首个 `tcn_000f21ac…`，truncated.nodes=true |
| 18 连线 | 未通过 | selected → relations=2（期望 65），rto=3 |
| 19 展开高亮 | 未通过 | 依赖 18 连线 |
| 20 模糊 | 未通过 | keyword=人工智能 → nodes=0，emptyReason=GRAPH_EMPTY（期望 190） |
| 20 精确 | 未通过 | 全名搜索 → nodes=0 |
| 21 名称与属性 | 部分 | name/role/strength 有；centrality=null（期望 41.292） |

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| display.graph.keyword | QUERY | GRAPH_EMPTY / 0 | ≈190 含 tcn_fceeb0c7… | 查 Java→Python keyword 透传 | `TS-L2-DS02-GRAPH-DEMO-FIX-R20261107-QUERY` |
| display.graph.relations.afterFilter | QUERY | 2 条 HIGH | 65 / 三种类型 | 查 lowEvidence×nodeCap | 同上 |
| ads_technology_panorama_score.{id}.overlay | QUERY | centrality=null | 41.292 | 查 PanoramaScores | 同上 |
| nebula.demo_gkx_chain.tech_point.*.description\|development_status | DATA | 无字段 | 描述与发展状态 | 覆盖不到；挂 L02 不去开工 | `TS-L2-DS02-GRAPH-DEMO-FIX-R20261107-DATA` |

SEL-FIX 选中点参数名已签收 `done`；本轮 QUERY 不含该键。
