# KG-7ELEM-LOAD-PATH-L05 · 服务机构上图路径

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务调研叶。只写本叶路径文档和本 handoff。不停在 done |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档。三问都保留，没有用 YAGNI 删类 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶要求读代码和已签收必须边，不用 compress 代替 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本叶不改图 |
| 图 diff | 无 |
| 会签态 | 不填。SVC etl / graph-svc 源文件 frontmatter 仍是 draft |
| 说明 | 不改 `KG-7ELEM-MUST-EDGES`，不改 `SVC-GRAPH-TRIPLE` |

## 问题清单

- 三问条数：第 1 问 1，第 2 问 2，第 3 问 2。
- 待确认条数：5。
- 燕大有代码、我方没有：0。
- `lumen-algo-py` 没有服务机构写图入口。入口在 `demo-algo-ent-analysis` 与 `demo-algo-science`。
- 未签收 `SYSINT-SCHEME-07-L03`、`SYSINT-SCHEME-07-L06` 只作索引。已实现以代码为准。L03 把入口写成 lumen vendor，不采纳。

## 修改内容

- 新增 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L05-服务机构.md`。
- 新增第 3 问示例 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L05/q3_link_core.py`。标明未实现，未执行。
- 服务机构互相 `participates` 未补。科研机构未写入。
- 未改已签收建图正文、初始化脚本、storage、`SYSINT-SCHEME-07-L06`、业务仓。未 commit。

## 测试结果

- 文档对照已签收 L03 的 M18、M21，以及 demo 仓 `svc_routes.py`、`svcgraph.py`、`svcgraph_ops.py`、`demo-algo-science/chainan`。
- 燕大对照 `yanda/tech-kg-api`（2026-10-30 13:19 工作区）：无服务机构 Tag，无 `service_provide`。`BELONGS_TO_NODE` 是企业归属，不计入。
- 示例脚本未执行。

## 遗留风险

- VID `institution:` 与 `inst:` 未收口（已签收 L05）。链上 C 档只 FETCH `inst:`。
- 两条必须边的关系行要先加工。本叶未建表、未灌数。
- 未签收台账与代码路径不一致处，以代码为准。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`（本地未提交）
- commit：无
- pipeline URL / ID：无。定义文档，无业务发布
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：未连图库，未跑示例

## 可观测性（建议）

- OTEL_SERVICE_NAME：无。本叶不改服务
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L05-服务机构.md`
- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L05/q3_link_core.py`
- `agent-delivery/agent-handoffs/KG-7ELEM-LOAD-PATH-L05.md`

## 成本（粗估）

| 字段 | 值 |
|------|-----|
| actual_tokens | 150000 |
| model_used | `grok-4.7` |
| actual_cost | 0.63 |
| cost_warn | `green` |
| 说明 | 价表无 grok。按 budget-estimate §1.2 B 档 $3/$15、输入 90% 粗算：150000×0.9×3/1e6 + 150000×0.1×15/1e6 = 0.63。低于 $5 |
