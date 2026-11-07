# TS-L2-DS02-PATH-DEMO-ACCEPT-LOOP

- 验收单：`TS-L2-DS02-PATH-DEMO-ACCEPT-LOOP`
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS02-PATH-合规演示用例.md`
- 监管：`human:淮政玮`

## 运行 2026-11-07

- 用例：同上
- 库：只读对照用例取数基线；本轮未再 SSH 探库
- 探测：同 GRAPH，HTTP 200
- 样本满足：否
- 停止：继续（DATA ready；QUERY 挂图谱 QUERY 单）

### 可演行对照

| 行 | 结果 | 现况 |
|---|---|---|
| 28 节点序列 | 通过 | keyPathOptions=2：tep_8392b7f8…(3步)、tep_6cddc27a…(2步) |
| 29 关键节点标记 | 部分 | role/strength 有；centrality=null（期望 41.292） |
| 30 步序与端点 | 通过 | 依赖 28 的 stageIds/nodes |
| 32 路径比较 | 通过 | 依赖 28 两条路径 |
| 33 动态演示 | 通过 | 依赖 28 步序 |

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| ads_technology_panorama_score.{id}.overlay | QUERY | centrality=null | 41.292 | 与图谱同键 | `TS-L2-DS02-GRAPH-DEMO-FIX-R20261107-QUERY` |
| ads_technology_panorama_score.{path_id}.path_priority 等 | DATA | path_priority 0 行；summary/类型/年份空 | 覆盖不到三行 | 灌数脚本+挂 L02 不开工 | `TS-L2-DS02-PATH-DEMO-FIX-R20261107-DATA` |
