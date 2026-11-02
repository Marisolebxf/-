# KG-7ELEM-LOAD-PATH-L02 · 七要素上图路径·企业

> 定义文档。只回答企业端点与本叶分到的必须边。未改业务仓，未执行 nGQL，未连图库。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权开跑 L02。本叶停在 integration，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档。三问都保留，没有用删代码的方式省略缺项或未实现。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶要求对照已打开的源码和已签收正文，不用压缩摘要代替读代码。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本叶不改图。必须边图仍是已签收 L03 的 `KG-7ELEM-MUST-EDGES`。 |
| 图 diff | 无。 |
| 会签态 | 不改源图。L03 正文 frontmatter 仍为 `draft`（本叶不翻签）。 |
| 说明 | 未改 storage，未改已签收建图正文。 |

## 问题清单

- 问 1：我方 6 条，燕大 3 条。我方同名同向能写的是企业点、`supply`、`parent_sub`；产业链仓另有 `participates`（源表不是企业表）。`cooperate`、`service_provide` 会写，方向对不上 M22、M21。
- 问 2：我方 5 条，燕大 4 条。缺的是双向合作的落法、对端稳定 ID、企业表到 `participates` 的同名边、政策适用表、服务提供的方向。
- 问 3：2 条。名称唯一对齐：我方未实现，燕大 `ExactOrganizationResolver` 已实现且不写合作边。政策正文抽取适用关系：两边都未实现。
- 待确认 5 条：双向边的物理形态、环节 ID 是否同一套、`antitypic` 与 `org_id`、燕大境内母子表名、服务机构 VID 前缀。
- 燕大有代码、我方 demo 没有同名实现：3 条。`SUBSIDIARY_OF` 写图、`BELONGS_TO_NODE` 写图、`ExactOrganizationResolver`。向量索引不写边，不计入这 3 条。`invest` 不计入。
- `lumen-algo-py` 不作为入口。正式仓没有本叶写图，不写成我方未实现。

## 修改内容

- 新增 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L02-企业.md`。
- 新增问 3 示例 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L02/unique_name_to_org_id.py`。文件内自检未执行（任务要求不执行）。示例不是已实现。
- 我方入口：`repos/demo-algo-ent-analysis` 的 `entan/graph/ops.py`、`entan/graph/nebula_loader.py`、`api/entan_graph_routes.py`；`repos/demo-algo-science` 的 `chainan/graph/nebula_schema.py`、`nebula_project.py`、`graph_ops.py`。science 只声明企业 Tag，不 `INSERT` 企业点；`graph_ops._hang` 在点已存在时写 `participates`。
- 燕大入口均在 `yanda/tech-kg-api`：`organization_entity_etl.py`、`organization_relation_etl.py`、`organization_graph_etl.py`（只转调实体装载）、`industry_chain_etl/load_industry_chain_graph.py`。

## 测试结果

- 文档与代码路径人工对照。未跑示例，未连 Nebula，未连 Doris。
- `scripts/run_all.py`（企业 demo 仓）未检索到对 `ops` / `nebula_loader` 的引用。

## 遗留风险

- 菜单入口不传 `dry_run` 时默认只预览。把默认调用说成已经写进图会失真。
- L06（未签收）写过企业 space 改动未发布。工作区源码字面量已是 `demo_gkx_chain`。源码字面量不是集群发布证据。
- 代码 `SELECT` 的列未连库核对是否都在现表上。
- 同一对关系我方与燕大边名不同。汇总叶不要收成第三套名字。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`（文档未 commit）
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无。定义文档，不发布。

## 可观测性（建议）

- OTEL_SERVICE_NAME：不涉及新服务。企业写图代码里已有 span 名 `ent.graph.write`，本叶未改。
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L02-企业.md`
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L02/unique_name_to_org_id.py`
- `agent-delivery/agent-handoffs/KG-7ELEM-LOAD-PATH-L02.md`

## 架构合规

| 项 | 结果 |
|---|---|
| 调用链：本叶不改代码；写图仍在 Python | ✅ |
| Java 不做 NLP / 向量 / 模型推理 | ✅ |
| 不选燕大 space 作生产 | ✅ |
| 不新增、不删除必须边 | ✅ |
| 企业—科研机构、企业—技术、企业—人才不建 | ✅ |
| `technology` 不计入七要素技术 | ✅ |
| 未改已签收建图正文、storage、L06、业务仓 | ✅ |
| D12：未把 lumen 指到 demo | ✅ |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000（粗估，无计量回执） |
| model_used | grok-4.7 |
| actual_cost | 1.5（美元，粗估） |
| cost_warn | green |
