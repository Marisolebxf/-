# KG-7ELEM-SCHEMA-DDL-L01 · 七要素建图·图数据库初始化脚本

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | lock 24h。本叶不改 claimed_by |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档。未用强度行删必须端点或必须边 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 脚本按已签收必须边逐条落成语句，不用压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。不改 `KG-7ELEM-MUST-EDGES` |
| 图 diff | 无 |
| 会签态 | 该图仍是 `draft` |
| 说明 | 脚本不授权改现网空间 |

## 问题清单

- 2026-10-30 第二次返工。上一版把关系名加了后缀，又给没写类型的列补了 `weight` / `props`，文件还包着 Markdown 围栏。
- 本版边名与总单关系列一致，每个名字只 CREATE 一次。同一条 CREATE 上方的注释列出全部端点对和方向。无向、双向写明「写入时两个方向各一条」。Nebula 没有无向边语法，也没有按端点拆 CREATE 的语法。
- Tag：企业 `enterprise`，产业链环节 `segment`，科研机构 `research`（无属性），技术 `paper` / `patent` / `project`（无属性），人才 `person`（无属性），服务机构 `institution`（只含已写明类型的列），政策 `policy`。现网 Tag `institution` 留给服务机构，不建成科研机构。`technology` 不建。
- 未执行。未连接 `10.50.75.136:9669`。
- 2026-10-30 复验结论：达到。15 条 CREATE EDGE 覆盖 M01–M24，无阻断项。任务仍停在 integration。

## 修改内容

- 再写 `工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-SCHEMA-DDL-L01-图数据库初始化脚本.md`。去掉围栏。边名改回总单关系列。未写明类型的列不再补。
- 未改 L01–L05，未改 storage，未改代码，未改图空间。

## 测试结果

- 未在环境执行。
- CREATE TAG 9。CREATE EDGE 15，对应 15 个关系名。注释覆盖必须三元组 24 对。不建的 13 对没有出现。
- 脚本从 `CREATE SPACE` 起，没有 Markdown 围栏，没有任务号、路径、章节号或其他文档名。
- `cite`、`supply`、`parent_sub`、`depends_on` 只带已写明类型的列。`cooperate`、`belong`、`participate`、`author_of`、`publish`、`policy_relate`、`policy_apply_to`、`participates`、`research_coop`、`talent_coop`、`service_provide` 无属性。
- 空间 `demo_gkx_chain`，`FIXED_STRING(80)`。`IF NOT EXISTS`。无 `DROP`。

## 遗留风险

- 同名不同端点在 Nebula 里只能是一条边。`cite` 同时承载技术引用和政策引用，`cooperate` 同时承载四对端点。现网企业到科研机构、企业到人才的同名边也能插进 `research_coop`、`talent_coop`。
- 科研机构、论文、专利、项目、人才没有已写明的属性，CREATE 不带列。现网点若写在 Tag `talent` 上，对不上 `person`。
- `:sleep 20` 是 nebula-console 指令。空间已存在时等待无害。

## CI/CD

- 分支：`gkx-orchestration` `dev`
- commit：脚本与 handoff 停在本地
- pipeline：无。`cicd: skip`
- 部署 / rollout / URL：无

## 可观测性

- 无服务改动

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-SCHEMA-DDL-L01-图数据库初始化脚本.md`
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/派单说明-KG-7ELEM-SCHEMA-DDL-L01.md`
- `agent-delivery/agent-handoffs/KG-7ELEM-SCHEMA-DDL-L01.md`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 只写文档 | ✅ |
| 不执行、不改 Nebula space | ✅ |
| 不臆造已有类型以外的列 | ✅ 未写明类型的 Tag 和 Edge 不带列 |
| D12 | ✅ 未把 demo 服务写进 lumen |
| 调用链 | ✅ 未改 |

## 成本

| 字段 | 值 |
|------|-----|
| model_used | grok-4.7 |
| actual_tokens | 20000（本叶粗估，无计量接口） |
| actual_cost | 0.5 |
| cost_warn | green |

ponytail: N/A（定义/文档）
