# TS-L2-DS02-ENTITY-ARCH · 科学技术全景 · 展示技术点关联实体 · 二级架构

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 监管人会话派单。本会话不改 task-registry，未经 MCP 认领 |
| 说明 | 只写文档。不写代码、不改库、不 commit。不标 done |

## Ponytail

ponytail: off（定义任务）

不缩文档。未用 YAGNI 跳过调用链、D12、D18、空态与上限。

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-ENTITY-ARCH-SEQ`、`TS-L2-DS02-ENTITY-ARCH-DATA` |
| 图 diff | 新增两张。语义与 `TS-L2-DS02-ARCH-SEQ` / `-DATA` 一致，只把实体一路单独画出：页 → 网关 → `gkxlumen-display` → `/internal/tech-graph/read` → `demo_gkx_chain`；影响力按编号只读分数表 |
| 会签态 | 源文件无 frontmatter，记 `draft`。待四角色会签 |
| 说明 | 图在 `sdd/l2/TS-L2-DS02-ENTITY-ARCH.md` 第 2、3 节 |

## 范围与实现

对照需规「科学技术全景」二级「展示技术点关联实体」序号 22–27，说明书 §2.2。按已实现的代码写 as-built：调用链、数据流、边界、空态与失败态、上限、现状。说明书已定的判定（22–25、27 真读，26 为 501，影响力读分数表、D4 mock）不重开。

## 偏离

文档本身无偏离。as-built 与说明书有五处不一致，登记在分册第 8 节，修复归原实现单：

1. 选中点字段名断：前端 `selectedNodeId` → Java 转发 `techPointId` → Python 只认 `technology_node_id` / `technologyNodeId`。选中点到不了 Python。
2. 前端 live 实体区不读 `listRecords`，从 `nodes` + `relations` 推，后端有实体也不显示。
3. 22 按强度取前 5：实体边不取属性，无强度，按名称排。
4. 24 条数：`relationCount` 恒 1，不是邻居个数。
5. Java 不透传 Python 分类型截断标记。

## 产物清单

- `sdd/l2/TS-L2-DS02-ENTITY-ARCH.md`
- 本 handoff

## 验收证据

- 分册已落盘，含两张 Mermaid、边界、空态 / 失败态表、上限表、现状表、差异表。
- 代码只读核对：`lumen-algo-py` `tech_graph_read.py`（HEAD `07ffa9f`）；`lumen-svc-platform` `SituationPanoramaService.java`、`TechGraphReadAdapter.java`、`JdbcPanoramaScores.java`、`SituationPanoramaController.java`；`lumen-ui-science-pc` `liveGraph.ts`、`index.vue`、`GraphAnalysisPanel.vue`、`entityRanking.ts`。
- 定义单，无业务 CI，无 PR。未 commit。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ Java 只装配与只读 SELECT，不算强度、影响力 |
| 2 调用链 | ✅ 页 → 网关 `/display/**` → `gkxlumen-display` → `/internal/tech-graph/read`，不越层 |
| 3 图谱 Nebula | ✅ 只读 `demo_gkx_chain`，非此空间 422 / 502 |
| 4 可观测 | ✅ 沿用 display Java Agent、Python 进程内中间件、前端 `request` trace 头，本叶不新加 |
| 5 CI/CD | ✅ 定义文档，`cicd: skip` 类，不触发部署 |
| 6 demo 只读 | ✅ 不 merge demo，不引用 demo 代码 |
| 7 共享聚合核心 | ✅ 前端只调 Java；Java 不写 nGQL，只读 ADS |
| 8 数据策略 | ✅ 实体真读图；影响力读 ADS mock 行 |
| 9 D8 前端规范 | ✅ 不改页面。另记：实体筛选用原生 `<select>`，与 Arco 优先不一致，非本二级决策 |
| 10 D9 血缘 | ✅ 影响力挂 `M_TECH_ENTITY_INFLUENCE` + ⓘ + MockBadge；不新造 id |
| 11 D10 交互 | ✅ 空态文案沿现页，不改交互 |
| 12 D12 | ✅ Feign `lumen-platform-algo-py`，不调 `demo-*`，不经 `gkxlumen-graph` |
| 13 D14 对象存储 | ✅ 不涉及 |
| 14 D16 缺项 | ✅ 不用 `gapfill_` 表 |
| 15 D17 合规算法 | ✅ 不改锁定算法 |
| 16 D18 | ✅ 影响力只读新建 ADS 表 mock 行，接口不写死，D4 mock |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 40000（估算） |
| model_used | claude-opus |
| actual_cost | 1.08 |
| cost_warn | green |

按 architect 80/20、C 档 `$15/$75`：`40000×0.8×15/1e6 + 40000×0.2×75/1e6 = 1.08`。无控制台分项。

## 遗留风险

- 差异第 1、2 条不修，L02 落边后实体区仍空。
- 图上尚无技术点连实体的边；人物影响力 0 行。
- 线上镜像、K8s rollout 未核，页面未在浏览器点过。

## CI/CD

- 分支：`gkx-orchestration` `dev`（未提交，等监管人确认）
- pipeline：编排仓无业务 CI
- K8s rollout：无

## 涉及文件

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-ENTITY-ARCH.md`
- `agent-delivery/agent-handoffs/科学技术全景-DS02/TS-L2-DS02-ENTITY-ARCH.md`
