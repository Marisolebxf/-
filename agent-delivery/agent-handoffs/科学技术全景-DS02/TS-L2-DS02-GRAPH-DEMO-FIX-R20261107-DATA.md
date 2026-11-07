# TS-L2-DS02-GRAPH-DEMO-FIX-R20261107-DATA · DS02 图谱 LOOP · 覆盖不到（描述/发展状态）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（LOOP 2026-11-07 首轮 DATA，已 claimed / in_progress） |
| 说明 | 本单不开工 `SYSINT-TECHGRAPH-02-L02` / `L03`。不改前端，不改过滤口径，不把 D4 mock 改绿。不改 `task-registry.yaml`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只做缺口核对与 handoff；未用 YAGNI 跳过图 schema 实测与 L02 去重挂接。 |

## 结论

**blocked（挂 L02 核对后仍无源可补）**。缺口键无法在本 DATA 单内灌齐；未静默改用例期望。

## 缺口键与实测

| 缺口键 | 实测（2026-11-07，跳板 `10.50.69.111` → `zhipu-tts`/`lumen-platform-algo-py`） |
|--------|----------------------------------------------------------------------------------|
| `nebula.demo_gkx_chain.tech_point.{technology_node_id}.description` | `DESCRIBE TAG tech_point` **无** `description` 列 |
| `nebula.demo_gkx_chain.tech_point.{technology_node_id}.development_status` | 同上，**无** `development_status` 列 |

现有列仅：`technology_node_id`、`name_zh`、`name_en`、`community_role`、`weighted_degree`、`community_id`、`graph_release_id`、`data_version`。与 `_TAGS["tech_point"]`（`lumen-algo-py` `tech_graph.py`）及 `TS-L2-DS02-GRAPH-DATA` as-built「序号 21 对应行空」一致。

读图 `tech_graph_read.py` 也不投影这两项；侧栏无法编描述/发展状态属数据源缺列，不是前端过滤。

## 与 SYSINT-TECHGRAPH-02-L02 去重

| 项 | 值 |
|----|-----|
| L02 状态 | `backlog`（依赖 L01；本单**未认领、未开工**） |
| L02 范围 | 边上图 + 边/路径/实体只读列表；写 `tech_rel` / `tech_has_*` / `tech_path_step` |
| 是否覆盖本缺口键 | **否**。本键是 `tech_point` Tag 属性扩列/灌值，不在现行 L02 派单说明内 |

**挂接**：验收/下一轮仍登记 hung-on `SYSINT-TECHGRAPH-02-L02` 作去重锚点；真正补列需另开「Tag 扩属性 + 入图」类单（或扩 L02 范围，须人拍板），**本 DATA 不代开**。

## 用例回写建议（勿静默改期望）

对象：`合规演示用例/TS-L2-DS02-GRAPH-合规演示用例.md` 行 **21 技术点详情 · 描述与发展状态**（现「覆盖不到」）。

建议文案（供产品/验收人确认后改用例，本单不直接改）：

> 图空间 `demo_gkx_chain` Tag `tech_point` 无 `description`、`development_status` 属性（2026-11-07 DESCRIBE 已核）；`SYSINT-TECHGRAPH-02-L02` 现行范围不写入这两项。本行改为 **设计无资源 / 无源**，待 Tag 扩列与入图任务落地后再改回可演期望；在此之前不把侧栏空描述当作 DATA 灌数失败。

## 修改内容

- 无业务仓代码改动；无图写；无 ADS 写。
- 仅本 handoff。

## 测试结果

- SSH 1 次意图：kubectl + `DESCRIBE TAG tech_point`（经 algo-py pod）。成功。
- 未跑 SCORE 灌数（本单缺口非 `path_priority` / centrality）。

## 遗留风险 / DoD 开项

1. DoD「补齐描述与发展状态」——**开**：无列可写，挂扩 schema 决策 + hung-on L02 去重说明。
2. DoD「核对 L02」——**闭**：已核对，L02 不覆盖同键。
3. 前端 / D4 ——未动。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`（仅 handoff）
- commit：见本轮 push
- 业务仓 / K8s rollout：无

## 架构合规自检

1. 算法只在 Python：未写算法。✅  
2. 调用链未改。✅  
3. Nebula 只读 DESCRIBE。✅  
4. 未开工 L02/L03。✅  
5. D4 mock 未改绿。✅  
6. D12：未调 demo 服务。✅  

## Cost 回填（建议）

- actual_tokens: ~8000（本叶估）
- model_used: claude-sonnet-4.5（会话路由模型；按登记枚举回填）
- actual_cost: 0.04
- cost_warn: green

## 人下一步

1. 确认是否接受「21 → 设计无资源」用例回写。  
2. 若要坚持演示描述/发展状态：另派 Tag 扩列 + 灌值（并明确是否扩 L02）。  
3. 本 DATA 单可在 AV 时标 blocked 或 needs-revision，勿标 done 直至用例或扩列闭合。
