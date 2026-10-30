# KG-7ELEM-BUILD-REQ-L05 · 七要素建图·完整 schema 与存储设计缺项

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工前已是 in_progress，本叶不再 task-claim。lock 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档。未用强度行删必须边或删缺项 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | schema 按 L03 必须边与 storage 原文逐条写，不用压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。沿用 L03 的 `KG-7ELEM-MUST-EDGES`，本叶不改图 |
| 图 diff | 无 |
| 会签态 | L03 图仍是 `draft` |
| 说明 | 不新增边，所以不改图 |

## 问题清单

- 按最新 L03 重对：必须 Edge 24（M01–M24），可选 0。不沿用旧编号。
- 存储设计已有 8（Tag 4，Edge 4：M15、M16、M23、M24）。缺 Tag 0。缺 Edge 6。缺属性 2。无对应存储域 17（Tag 3，Edge 14）。
- M16 政策 `cite` 政策：存储设计已有。M19 `research_coop`、M20 `talent_coop`：无对应存储域。ENT 同名边是企业→科研机构、企业→人才，且是有向，不是双向。
- 服务机构之间的 `participates` 未加回。
- 人才、科研机构、论文/专利/项目没有 `pipeline-to-nebula`。ENT 的 `technology` 未当成技术。
- POLICY 无目录 `stores/nebula/`，有单文件 `stores/nebula.md`。COMP 无 `stores/nebula`。COMP 只读查询未算进建图 schema。

## 修改内容

- 新增 `工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-BUILD-REQ-L05-建图schema与存储设计缺项.md`。
- 未改 storage 原文，未改 L03，未改代码，未改图空间。未重做 `SYSINT-SCHEME-07-L07`。

## 测试结果

- 必须边行数 = 最新 L03 必须表 M01–M24，共 24。可选 0。没有服务机构 `participates` 服务机构。
- 端点 Tag 行数 = 7。
- 缺项类只有：存储设计已有、缺 Tag、缺 Edge、缺属性、无对应存储域。
- 同名但起终点或方向不同的边没有标成已有。VID 和属性没有写出存储文件与 L06 前缀以外的名字。

## 遗留风险

- `enterprise`、`institution` 的属性集合在两份存储里对不上，建图时不能自行并成一套。
- 服务机构 VID 现网 `institution:` 与目标 `inst:` 都写了，存储设计没有收成一条。
- M19、M20 与 ENT 的同名边端点和方向都不同。企业到科研机构、企业到人才没有补进 schema。M22 企业 `cooperate` 在 L03 是双向，存储是有向，不算已有。

## CI/CD

- 分支：`gkx-orchestration` `dev`
- commit：产物按厚包停在本地，本叶不 commit / push
- pipeline：无。`cicd: skip`
- 部署 / rollout / URL：无

## 可观测性

- 无服务改动

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-BUILD-REQ-L05-建图schema与存储设计缺项.md`
- `agent-delivery/agent-handoffs/KG-7ELEM-BUILD-REQ-L05.md`

## 架构合规

| 铁律 | 结果 |
|---|---|
| 只写文档 | ✅ |
| 调用链 / 不改 Nebula space | ✅ 未改 |
| 不臆造 VID、属性、表名 | ✅ |
| D12 | ✅ 未把 demo 服务写进 lumen |
| 不重做 L07 代码差异 | ✅ |

## 成本

| 字段 | 值 |
|------|-----|
| model_used | grok-4.7 |
| actual_tokens | 50000（本叶粗估，无计量接口） |
| actual_cost | 1 |
| cost_warn | green |

ponytail: N/A（定义/文档）
