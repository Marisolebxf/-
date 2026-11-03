# E-E7-POLICY-M1-L11 · 专题政策门面 · 政策订阅与外发 · 架构设计

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| 状态 | `in_progress`。本单不改 task-registry，不标 done |
| ponytail | `off` |
| 说明 | 架构设计，不写代码。未用 YAGNI 跳过调用链、订阅关系落库和「没有记录就返回空」。未 commit，未 push。 |

ponytail: off

## 任务认领

任务开工时已是 `claimed_by=agent:arch-agent`、`supervised_by=human:淮政玮`、`status=in_progress`。本会话不重复认领，不认领 `E-E7-POLICY-M1-L12`、`E-E7-POLICY-M1-L13`。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `E-E7-POLICY-M1-L11-SEQ` |
| 图 diff | 浏览器仍只打 `GET /display/v1/policy/panorama/subscriptions`。display 到 `gkxlumen-topic-policy` 的委托是虚线：入口尚未接通。关系写 `gkxlumenx_topic_policy`。筛选读已入库 `policy_base_info`。到点执行记录交 `gkxlumen-topic-async-service` |
| 会签态 | `draft`。图源无 frontmatter。本单不写会签通过 |
| 说明 | 图在 `sdd/l2/E-E7-POLICY-M1-L11.md` 第 3 节 |

## 调用链

动向页 → `gkxlumen-gateway` → `gkxlumen-display` 的 `GET /display/v1/policy/panorama/subscriptions`。

接通之后，display 把保存、修改、取消、读取和外发全部委托给 `gkxlumen-topic-policy`。展示服务不保存关系，不跑定时，不发信，不发短信。浏览器不改打 `/topic/v1/policy`。这不把 `E-E7-POLICY-M1-L06` 改成展示联调单。

门面到点用已有检索筛已经入库的政策：`gkxlumen-topic-policy` → Python `/internal/policy` → `gkxlumenx_dwd.policy_base_info`。不新开抓取。到点外发的执行记录交给 `gkxlumen-topic-async-service`。Java 不生成推送文案，不调用未注册模型。外发内容来自已入库政策的已有字段。

**入口尚未接通。** 只读 `PolicyFacadeController`：现网门面有检索、正文、指标、分布，没有订阅入口。全仓没有 `subscriptions`。未提交的排序、收藏、导出不计入本入口。

## 关系落在哪里

订阅关系落在门面自己的库 `gkxlumenx_topic_policy`。不进 ODS、DWD、ADS，不进 `gkxlumenx_gapfill`，不用态势模块的用户行为表。

关系保存：鉴权用户、政策类别、行业领域、发布部门、地区、频率（日/周/月）、通道（系统通知、邮件、短信）、是否仍有效、上次外发对到的入库位置。用户可修改、取消。没有记录就返回空，不灌假记录。本单不写建表 SQL。

这不是序号 201 的收藏，也不是序号 212 的企业匹配。

入口接上且该用户没有订阅时，返回空列表。外发通道还没有时，推送记录为空列表，不把本叶改判成外发已上线。

## 范围

架构正文：`sdd/l2/E-E7-POLICY-M1-L11.md`。

`L12` 实现、`L13` 测试仍是后续单，监管都是 `human:淮政玮`。本单不实现。

## 偏离

无。入口未接通按第 7.1 节如实写，不改成已委托。

## 产物清单

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/sdd/l2/E-E7-POLICY-M1-L11.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/E-E7-POLICY-M1-L11.md`

未改 Java，未改 task-registry，未 commit，未 push。

## 验收证据

对照 `POL-L2-DS10-TREND-ARCH` 第 7.1 节与说明书第 11 节。只读门面控制器，确认没有订阅映射。无运行测试，无 pipeline。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python | ✅ 本单不调用模型。Java 不生成推送文案 |
| 调用链 | ✅ 浏览器只打 `/display/v1/policy/panorama/subscriptions`。委托在服务内部，且尚未接通 |
| 图谱 | ✅ 不读图，不写 nGQL |
| 可观测 | ✅ 沿既有 Java 链，本单不新设计观测点 |
| CI/CD | ✅ 设计文档。未 commit，未 push，无 rollout |
| D12 | ✅ 不调用 demo 服务 |
| D9 | ✅ 不新造 `metric_id`，不改 D4，不把空推送列表改判成外发已上线 |
| D16 / 说明书第 11 节 | ✅ 订阅条件不灌假记录，不建 `gapfill_` 订阅表 |
| D18 | ✅ 关系可落门面库，筛选读已入库行，无记录返回空。不在接口里写死 mock |

## Cost

| 字段 | 值 |
|---|---|
| actual_tokens | 12000 |
| model_used | grok-4.7 |
| actual_cost | 0.06 |
| cost_warn | green |

无控制台分项。按本单 `estimated_tokens` 12000、architect 80/20、B 档 `$3/$15` 估算：`12000×0.80×3/1e6 + 12000×0.20×15/1e6 = 0.065`，记 `0.06`。未回写 task-registry。

## 修改内容

- 新增 `sdd/l2/E-E7-POLICY-M1-L11.md`
- 新增本 handoff

2026-11-03 human:淮政玮 签收本架构。入口仍未接通，不灌假订阅。
