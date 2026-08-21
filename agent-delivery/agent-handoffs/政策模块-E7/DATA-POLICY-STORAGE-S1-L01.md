# DATA-POLICY-STORAGE-S1-L01 · 政策维存储设计 S1

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本叶只改编排仓 Markdown） |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW`；CHAIN 增量 `CHAIN-STORAGE-FLOW` 附录 B |
| 图 diff | 新增政策→`demo_gkx_chain` 实线投影；`gkx_policy` 改为虚线 as-built；禁止 DROP 底图 / 写 `gkx_chain` |
| 会签态 | `POLICY-STORAGE-FLOW` = **approved**（`human:淮政玮` · 2026-08-21）；`CHAIN-STORAGE-FLOW` 主图仍 **approved**（李伟 · 产业链拓扑，不翻签）；附录 B 由淮政玮放行 |

## 问题清单

- `tech`/`talent` 本波不上图（OPEN-POLICY-GRAPH-01），不挡 B。
- 细表 `stores/` 仍 draft。

## 修改内容

- 新建 `storage/POLICY/`（README / 00-context / 01-data-flow）。
- `storage/README.md`、`diagram-as-contract.md` L2 映射认 POLICY 流图。
- CHAIN `01-data-flow.md` 附录 B + OPEN-CHAIN-POLICY-01；**不翻签**主图。
- `graph-engine.md`：`gkx_policy` 禁止新写入。
- 旧 `政策域数据库设计(v1)` 文首过期回链。
- **未改** `demo-algo-*` 代码。

## 测试结果

- 文档对照：决策 #7 / `nebula_schema` Tag 列表 / 2026-08-21 Tempo ADS-only 事实。
- 无 CI（定义叶）。

## 遗留风险

- B 叶施工范围已钉：`CREATE TAG policy` + 四边；`tech`/`talent` 不上图。
- CHAIN 主图仍李伟 2026-08-13 签；本管线不要求其复签政策增量。

## CI/CD（必填）

- 分支：`gkx-orchestration` `origin/dev`（未要求本会话 commit）
- commit：待监管人提交
- pipeline / K8s：N/A（设计叶）

## 可观测性（建议）

- 现网抽样：`e0901e8c7fea95c6a2aebca48017840c`、`605f71cdf6b60ae01bbfa19e584e1301`（仅 MySQL ADS）

## 涉及文件

- `agent-delivery/data/data-design/storage/POLICY/*`
- `agent-delivery/data/data-design/storage/README.md`
- `agent-delivery/data/data-design/storage/CHAIN/01-data-flow.md`
- `agent-delivery/data/data-design/storage/CHAIN/README.md`
- `agent-delivery/data/data-design/政策/政策域数据库设计(v1).md`
- `agent-delivery/graph-engine.md`
- `agent-delivery/diagram-as-contract.md`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 写图仍归 polan（B 叶） |
| 调用链 / D12 | ✅ 产品链虚线；本叶不改 lumen |
| Nebula / 禁 Neo4j | ✅ 一张 G |
| Java 不写 nGQL | ✅ |
| Demo 库 | ✅ `demo_*` / `demo_gkx_chain` |
| 禁第二张 G | ✅ `gkx_policy` 虚线 |

## cost（待会话结束回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | 待填 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 待填 |
| cost_warn | green |
