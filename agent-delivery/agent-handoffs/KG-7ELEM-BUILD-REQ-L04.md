# KG-7ELEM-BUILD-REQ-L04 · 七要素建图·必须三元组的建图动作与缺口

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 已认领，本叶不再次 task-claim。状态保持 `integration` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档。未用 YAGNI 删必须边 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 按当前 L03 的 24 条必须边逐条对照流水线，不用压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。沿用 L03 的 `KG-7ELEM-MUST-EDGES`，本叶不改图 |
| 图 diff | 无 |
| 会签态 | L03 图 frontmatter 为 `draft` |
| 说明 | 不新增、不删除必须边，所以不改图 |

## 问题清单

- 按当前 L03 的 24 条重对。编号已换，不沿用上一版 M 号。表内 M01–M24 与必须档一一对应。可选 0 条。
- 沿用 10：M15 `depends_on`，M16 政策 `cite`，M17 企业 `participates` 环节，M18 服务机构 `participates` 环节，M19 `research_coop`（双向，A29），M20 `talent_coop`（双向，A30），M21 `service_provide`，M22 企业 `cooperate`，M23 `supply`，M24 `parent_sub`。
- 离线补边 14：M01–M14。
- 服务机构 `participates` 服务机构未进表。L06 `SVC_RE_SVC_SVC` 不加回。
- 关系表名没写死的标了待确认。政策 `cite` 沿用 `POLICY_RE_CITE`，不并进技术 `cite`。
- 沿用只表示已有写图语句。触发不进页面请求。本叶不写接口。

## 修改内容

- 按当前 L03 覆盖 `工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-BUILD-REQ-L04-建图需求.md`。
- 未写接口，未改图空间，未配 GDF，未改 L03、L05，未改代码和 WBS。

## 测试结果

- 表中必须边 24 行，编号与当前 L03 必须档 M01–M24 一致，一条不漏、一条不多。
- 无「服务机构 participates 服务机构」行。
- 表名回指台账或 L06；没有写死的写待确认。未从存储设计抄表名。

## 遗留风险

- 沿用 10 条的现行入口仍是图谱接口。本叶要求离线触发，没有改调用代码。
- M19、M20 台账写实际写入未验证。
- M18 的 A26 表名未写。产业链机构端 `inst:` 与产业服务 A 档 `institution:` 前缀不一致。本叶不改 VID。
- 企业边若在存储设计里另有表名，留给 L05，本叶不抄。

## CI/CD（必填）

- 分支：`gkx-orchestration` `dev`
- commit：按本叶要求停在本地，未 commit / push
- pipeline URL / ID：无。`cicd: skip`
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无。文档叶，行数对照见上

## 可观测性（建议）

- OTEL_SERVICE_NAME：无服务改动
- traceId（dev 抽样）：无
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/工程过程/04-系统集成/07-图数据库集成/KG-7ELEM-BUILD-REQ-L04-建图需求.md`
- `agent-delivery/agent-handoffs/KG-7ELEM-BUILD-REQ-L04.md`

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 只写文档 | ✅ |
| 建图不进页面请求 | ✅ |
| 正式空间仍是 `demo_gkx_chain`，本叶不改 | ✅ |
| 不臆造表名、枚举、样本量 | ✅ |
| 不写接口、不配 GDF、不改代码 | ✅ |

## 成本

| 字段 | 值 |
|------|-----|
| model_used | grok-4.7 |
| actual_tokens | 40000（本叶粗估，无计量接口） |
| actual_cost | 1 |
| cost_warn | green |
