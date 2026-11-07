# TS-L2-DS02-ENTITY-DEMO-ACCEPT-LOOP

- 验收单：`TS-L2-DS02-ENTITY-DEMO-ACCEPT-LOOP`
- 用例：`agent-delivery/工程过程/04-系统集成/05-展示系统集成/合规演示用例/TS-L2-DS02-ENTITY-合规演示用例.md`
- 监管：`human:淮政玮`

## 运行 2026-11-07

- 用例：同上
- 库：只读对照用例取数基线；本轮未再 SSH 探库（见 GRAPH 同日 handoff）
- 探测：同 GRAPH，HTTP 200
- 样本满足：否
- 停止：继续（DATA 子任务 ready；QUERY 挂图谱 QUERY 单）

### 可演行对照

| 行 | 结果 | 现况 |
|---|---|---|
| 22 选点后 Top5 | 通过 | listRecords=61；专利20/论文13/人8/机构20 |
| 23 换点 | 通过 | 第二次 listRecords=29；论文前三 W2981451354、W3174384278、W3214589207 |
| 24 基本属性 | 部分 | W2093980670 type/nodeIds 有；influence=null（期望 16.4） |
| 25 按类型 | 通过 | 论文13、机构20（truncated.institution） |
| 27 按影响力 | 未通过 | influence 全 null，无法按影响力排序核对 |

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| ads_technology_panorama_score.{id}.overlay | QUERY | influence=null | W2093980670=16.4 | 与图谱同键 | `TS-L2-DS02-GRAPH-DEMO-FIX-R20261107-QUERY` |
| nebula.demo_gkx_chain.tech_has_*.{属性} 等 | DATA | 无强度/中文名/年份 | 覆盖不到四行 | 挂 L02 不开工 | `TS-L2-DS02-ENTITY-DEMO-FIX-R20261107-DATA` |

前端 `TS-L2-DS02-FE-ENTITY-FIX-L01` 在 LOOP 外，本轮不判页面。
