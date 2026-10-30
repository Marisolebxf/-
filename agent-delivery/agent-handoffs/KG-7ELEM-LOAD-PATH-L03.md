# KG-7ELEM-LOAD-PATH-L03 · 七要素上图路径·产业链

> 定义文档。只回答产业链环节、`depends_on`、企业或服务机构 `participates` 到环节。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权。本叶停在 integration，不标 done |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档。三问都保留 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 本叶不改图。对照 `KG-7ELEM-MUST-EDGES` |
| 图 diff | 无。不增删必须边 |
| 会签态 | 源文件 `KG-7ELEM-BUILD-REQ-L03` frontmatter 为 `draft` |
| 说明 | 本叶不改已签收建图正文 |

## 问题清单

- 第 1 问 4 条。环节 Tag、白名单 `depends_on`、企业 `participates` 到环节能从关系库走我方 demo 写图。燕大对应的是 `IndustryNode`，不是同一套边名。
- 第 2 问 3 条。正式加工的 `parent_child` 上不了 `depends_on`；服务机构行没有洗进实体关系表；燕大 `downstream_link_code` 有无值未连库。
- 第 3 问 1 条。正文抽上下游：我方和燕大都未实现。示例脚本不能当已实现。
- 待确认 6 条。燕大有代码、我方没有 3 条：`CHILD_OF`、`BELONGS_TO_NODE`、`DOWNSTREAM_OF`。
- 企业端归 L02，服务机构端归 L05。`lumen-algo-py` 没有 `/v1/chain/graph` 与 `/internal/chain/graph`。

## 修改内容

- 新增 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L03-产业链.md`
- 新增 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L03/upstream_from_text.py`（第 3 问示例，未实现）
- 未改业务仓、storage、已签收建图正文、`SYSINT-SCHEME-07-L06`

## 测试结果

- 未执行 nGQL，未连图库，未连 Doris，未跑示例脚本。
- 写图入口打开过 `repos/demo-algo-science` 的 `api/main.py`、`chainan/graph/nebula_schema.py`、`graph_ops.py`、`nebula_project.py`。
- 企业/服务参与边打开过 `repos/demo-algo-ent-analysis` 的 `api/svc_routes.py`、`entan/svcgraph_ops.py`。企业→环节的 `participates` 不在该仓。
- 燕大对照打开过 `yanda/tech-kg-api` 的产业实体与 `CHILD_OF` / `DOWNSTREAM_OF` / `BELONGS_TO_NODE` 抽取脚本。

## 遗留风险

- 未连库，白名单行和服务机构行是否已有数据未知。
- `parent_child` 与 `depends_on` 的语义没有并成一条。
- 燕大三条边不能当成生产放行。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`（未 commit）
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无。定义文档

## 可观测性（建议）

- OTEL_SERVICE_NAME：无
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L03-产业链.md`
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L03/upstream_from_text.py`
- `agent-delivery/agent-handoffs/KG-7ELEM-LOAD-PATH-L03.md`

## 成本（粗估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000 |
| model_used | grok-4.7 |
| actual_cost | 2 |
| cost_warn | green |
