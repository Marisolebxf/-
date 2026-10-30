# KG-7ELEM-LOAD-PATH-L01 · 七要素上图路径方案

> 定义文档。只汇总 L02–L06 已写结论。未改五张子单，未改示例脚本，未改业务仓，未执行 nGQL，未连图库，未连久新库。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务汇总叶。五张调研叶已有 handoff。本叶停在 integration，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档。三问都保留，没有用删条目的方式把未实现写成已实现。 |

ponytail: N/A（定义/文档）

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶要求对照五份正文，不用压缩摘要代替阅读。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无。本叶不改图。必须边图仍是已签收 L03 的 `KG-7ELEM-MUST-EDGES`。 |
| 图 diff | 无。不增删必须边。 |
| 会签态 | 不改源图。子单写明 L03 正文 frontmatter 为 `draft`，本叶不翻签。 |
| 说明 | 未改已签收建图正文、初始化脚本、storage、派单说明、`SYSINT-SCHEME-07-L06`。 |

## 问题清单

- 第 1 问 13 条。第 2 问 17 条。第 3 问 8 条。
- 我方已实现 10 条：企业点、M23 `supply`、M24 `parent_sub`、环节 `segment`、M15 白名单 `depends_on`、M17 产业链仓 `participates`、政策点、M16 约定格式 `cite`、M16 的 `mode=llm` `cite_pids`、服务机构点。
- 待确认 25 条。叶相加 27，两处同一问题合成后减 2。
- 燕大有代码、我方没有：12 条。叶相加 13，`BELONGS_TO_NODE` 重复 1 次，汇总计 1。
- 久新现库能对上、我方没有写图：2 条（M06 专利→论文，M09 人才→专利）。L06 待确认 6 条不计入。我方第 1 问在科研/人才/技术域是 0 条。
- 子单冲突 4 处：燕大 `BELONGS_TO_NODE` 重复计数；服务机构 VID 是否新开待确认；L03 正文消费行编号 A26 两处不一致；`nebula_project.py` 是否写 `participates`。另有归位 3 处（M21 收到问 2，M17 企业表路径收到问 1，M18 方向按 L05 所写代码 src/dst）。未改子单。
- 未实现保持未实现。`technology` 不计入。服务机构互相 `participates` 不补。企业—科研机构、企业—技术、企业—人才不建。
- 我方入口只写 `demo-algo-science`、`demo-algo-ent-analysis`。未把 `lumen-algo-py` 补成入口。未选燕大 space 作生产。久新 `ads_*` 未写成我方 ADS。

## 修改内容

- 新增 `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L01-上图路径方案.md`。
- 新增本 handoff。
- 未改 L02–L06 正文、示例脚本、已签收建图正文、初始化脚本、storage、派单说明、`SYSINT-SCHEME-07-L06`、业务仓。
- 未执行 nGQL，未连图库，未连久新库。产物未写账号、主机、端口、连接串。

## 测试结果

- 对照五份正文与五份 handoff 做了计数差额。数字以正文计数节为准。
- 未跑示例脚本，未连 Nebula，未连 Doris。

## 遗留风险

- 四条冲突未在子单里收口。后续若改入口或改计数，先改子单再改本汇总，避免汇总单独变成第三套说法。
- L03 正文两处消费行编号不一致，本叶没有替它删掉或补上 A26。
- 我方已实现 10 条里，M15 只覆盖白名单行，M16 规则路径只覆盖约定格式，M17 只覆盖产业链仓菜单路径。正式 `parent_child`、自由文本以外的向量补边、企业表上的 `industry_belong` 仍是未实现。
- 成本是粗估，无 Console 回执。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`（文档未 commit）
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无。定义文档，不发布。

## 可观测性（建议）

- OTEL_SERVICE_NAME：无。本叶不改服务
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-LOAD-PATH-L01-上图路径方案.md`
- `agent-delivery/agent-handoffs/KG-7ELEM-LOAD-PATH-L01.md`

## 架构合规

| 项 | 结果 |
|---|---|
| 调用链：本叶不改代码；写图入口仍按子单记在 Python demo 仓 | ✅ |
| Java 不做 NLP / 向量 / 模型推理 | ✅ |
| 不选燕大 space 作生产 | ✅ |
| 不新增、不删除必须边 | ✅ |
| 企业—科研机构、企业—技术、企业—人才不建 | ✅ |
| 服务机构互相 `participates` 不补 | ✅ |
| `technology` 不计入七要素技术 | ✅ |
| 久新 `ads_*` 不写成我方 ADS | ✅ |
| 未改已签收建图正文、storage、L06 派单说明、业务仓、五张子单 | ✅ |
| D12：未把 lumen 指到 demo，未把 `lumen-algo-py` 补成入口 | ✅ |

## 成本

| 字段 | 值 |
|------|-----|
| actual_tokens | 180000（粗估，无计量回执） |
| model_used | grok-4.7 |
| actual_cost | 0.76（美元，粗估） |
| cost_warn | green |

价表无 grok-4.7。按预算说明 B 档（输入 3 美元/百万、输出 15 美元/百万）和读多写少 90/10 套算：180000×0.9×3/1e6 + 180000×0.1×15/1e6 = 0.756，取 0.76。低于 $5。
