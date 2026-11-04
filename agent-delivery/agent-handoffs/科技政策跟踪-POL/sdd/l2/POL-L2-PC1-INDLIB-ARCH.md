# POL-L2-PC1-INDLIB-ARCH · 政策数据治理 · 规划指标库搭建

- 任务：`POL-L2-PC1-INDLIB-ARCH`
- 日期：2026-11-04
- 状态：起草完成，待四角色会签。会签未完成不挡签收
- 监管：`human:淮政玮`
- 认领：`agent:arch-agent`
- 强度：ponytail off（定义任务，不缩文档）
- 图：`POL-L2-PC1-INDLIB-ARCH-SEQ`（本叶新图，源文件无 frontmatter，记 `draft`）

本叶只定政策数据治理二级「规划指标库搭建」的实现架构和整体流程。SRS 序号 **605**。用户故事 `US-DS-POL-07`。不写 OpenAPI 字段、请求体、响应体、枚举。那是 `POL-L2-PC1-INDLIB-API`。

上游只引用，不改写：`政策数据治理.md` 605、说明书第 2 节 PC-1 与第 11.2 节、`sdd/调用链与边界.md`、`sdd/契约输入清单.md` 的 `governance/indicator-library`、`sdd/指标与501.md` 治理节、`survey/PC.md` PC-1。不新造 `metric_id`，不改 D4。

签收标准（`human:淮政玮`，说明书第 11 节）：可实现才签收。真算、真查或真模型做不到时，只接受新建表、把 mock 写入表、接口读表。不允许接口直接返回 mock。本叶按第 11.2 节「治理 · 指标库 605」写迁移之后的架构：**建 `gapfill_policy_indicator_lib`，mock 行写入表，接口只读表**。

## 1. 范围

605 是治理页的规划指标库区块。需规要的是「梳理政策核心指标维度，搭建标准化政策指标库，涵盖扶持力度、适用范围、实施时效、申请条件等关键指标，为政策拆解、对比分析提供统一指标口径与数据支撑」。

政策域 35 条注册指标（`M_POLICY_*`）没有一个覆盖这四个维度作为「指标库条目」——它们的口径是发布量、分布、力度指数、效果评分等展示页统计。605 要的是另一个东西：**按政策拆解/对比视角组织的指标条目库**，每个条目说明某政策在扶持力度、适用范围、实施时效、申请条件上的口径与值。这个库没有生产系统，按签收标准建 gapfill 表灌 mock。

前缀 `/display/v1/policy/`，资源只有一条：`GET /display/v1/policy/governance/indicator-library`。

| 需规要点 | 本叶流程 |
|---|---|
| 梳理核心指标维度 | 维度就是需规点名的四个：扶持力度、适用范围、实施时效、申请条件。不扩充维度清单 |
| 搭建标准化指标库 | 建表 + 灌行 + 只读接口。库条目 = 表行 |
| 统一指标口径 | 每行带口径说明。不挂政策域注册指标（见 §2 迁移分析） |
| 为政策拆解、对比提供支撑 | 本叶只建库与读面。拆解页（607/608）与对比页（610）消费方式不在本叶，不为其改挂资源 |

## 2. 客观事实与迁移分析

任务 note 要求：算法中台已有的沿用，没有的把合理部分迁到 lumen 链路。

| 现有实现 | 与 605 的关系 | 本叶裁定 |
|---|---|---|
| `M_POLICY_BASE_100_1`（STAT，D4=mock） | 口径是发布量/分布，`page_ids` 只有专题 E7 | 不是指标库条目。调研已判本叶不挂，契约清单也点名治理不挂这条 |
| `M_POLICY_INTENSITY_SCORE` / `M_POLICY_SUPPORT_STRENGTH` | 力度评分/支持力度，挂全景与详情对比 | 不是「申请条件、实施时效」这类库条目。不借用来填库 |
| GDF `policy_support` 列（全是字面 `'null'`） | 源上就没有结构化要素，回包第 24 条已确认 | 不能作库条目数据源。C2 只能切条或走模型，这是第 6 项已确认的预期 |
| demo 原型政策治理页本地数组 | 演示指标条目在页面内存 | 不迁数据，只迁区块信息结构 |
| 门户扶持十条（`ALGO-LIB-POL-PORTAL-*`） | 门户政策扶持的计算条目 | 不是本页任务（跨项边界），不做展示页条目 |

四个维度的现状：扶持力度在 DWD 源上无结构化值（`policy_support` 字面 null）；适用范围、实施时效、申请条件同样没有落库结构。**整个库无真源**，与 604 的「半真半 mock」不同，605 全部行都是 mock。

## 3. 实现架构

浏览器只打 `/display/v1/policy/**`。不改打 `/topic/v1/policy`，不打开算法中台页面，不打 `/v1/policy/**`。

治理页契约只有三条资源。本二级只用 `governance/indicator-library` 这一条。另两条由 602/603 与 604 的稿件定，本叶不实现、不改挂。

| 需规要点 | 资源 | 迁移后的读法 |
|---|---|---|
| 指标库读面 | `GET /display/v1/policy/governance/indicator-library` | `gkxlumen-element` 只读 `gkxlumenx_gapfill.gapfill_policy_indicator_lib` |

```mermaid
flowchart LR
  fe["治理页 · 规划指标库 605"]
  gw["gkxlumen-gateway"]
  bff["gkxlumen-display"]
  el["gkxlumen-element"]
  gap["gkxlumenx_gapfill.gapfill_policy_indicator_lib"]
  fe --> gw --> bff --> el --> gap
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| `data-agent` 按 `POL-L2-PC1-INDLIB-GAPFILL-L01` 灌 mock 行 | `gkxlumen-element` 只读，经 `gkxlumen-display` 原样返回 | 用户打开治理页指标库区块，或按维度/政策浏览条目 | 无行则区块空，不造 0；失败不清空治理页其他区块 | 不进 `gkxlumen-topic-async-service`。不调用任何 `polan` 函数。不写 ODS、DWD、ADS。不把 demo 本地数组当接口 |

`gkxlumen-display` 不直连库，不直连 Python，不写算法，不写 nGQL。`E-E7-POLICY-M1-L06` 不是本页路径。

这条资源不进异步任务管道。治理页三条资源各自独立，本叶不改另两条的读法。

trace 沿既有展示链走。display 往 element 带 traceId。本叶不新设计观测点。

## 4. 整体流程

1. `data-agent` 灌数：按四个维度 × 若干政策写指标条目行，写入 gapfill 表。
2. 用户打开治理页指标库区块。前端调 `indicator-library`。display 委托 element 只读 gapfill 表。
3. 用户按维度或政策浏览条目。仍走同一条资源，按条件拣行。条件对不上则空。
4. 任何失败不清空治理页其他区块。

## 5. 数据来源：一张 gapfill 表

表只建在 `gkxlumenx_gapfill`，表名 `gapfill_policy_indicator_lib`。不进 ODS、DWD、ADS，不写供应方库。字段级 DDL 由 `POL-L2-PC1-INDLIB-DATA` 定；灌数由 `POL-L2-PC1-INDLIB-GAPFILL-L01` 执行，本叶不执行。

| 维度（需规点名） | 条目行要含 | 真源 |
|---|---|---|
| 扶持力度 | 口径说明 + 条目值/档位 | 无（`policy_support` 字面 null，无算法可算）——mock |
| 适用范围 | 口径说明 + 适用地域/对象描述 | 无——mock |
| 实施时效 | 口径说明 + 时效区间描述 | 无——mock |
| 申请条件 | 口径说明 + 条件要素描述 | 无——mock |

与 604 不同，605 **不掺真实行**：四个维度在源上都没有结构化值，没有可取的真实锚点。全部行标 mock（`fill_method=manual`、`gap_item` 写序号与叶子名），UI 带 🧪 MockBadge。每行都带 `metric_id`（留空，说明书明令「不新造 `metric_id`」）、`gap_item`、`fill_method`、`gapfill_batch_id`、`generated_at`。D4 保持 mock。

### 5.1 输入条件

条件只来自需规原文。下表是用户会做的操作，不是参数名，也不是响应字段。参数名留给 `POL-L2-PC1-INDLIB-API`。

| 用户操作 | 必选 | 落到哪次读取 |
|---|---|---|
| 打开治理页指标库区块 | 无 | 读库概览（条目数、维度分布）。无行则空 |
| 按维度浏览条目 | 否，不选则读全部 | 按维度拣行。维度枚举只有需规点名的四个，接口单不得另造维度 |
| 按政策查该政策条目 | 否 | 按政策拣行。该政策无行则空 |

### 5.2 与政策域注册指标的关系

| | 605 指标库条目 | `M_POLICY_*` 注册指标 |
|---|---|---|
| 对象 | 单政策 × 四维度的口径与值描述 | 全域统计（总量、分布、指数、评分） |
| 目的 | 政策拆解、对比的统一口径支撑 | 展示页统计卡、图表 |
| 注册 | 不注册 `metric_id` | 已在 metric-registry，D4=mock |

注册指标不是库条目的数据源，库条目也不反挂注册指标。两套并存，互不顶替。

## 6. 点名排除

| 资源或序号 | 不纳入本二级的原因 |
|---|---|
| `M_POLICY_BASE_100_1` | 口径是发布量/分布，调研与契约清单都点名治理页不挂 |
| `M_POLICY_INTENSITY_SCORE`、`M_POLICY_SUPPORT_STRENGTH` | 力度评分指标，不是库条目。借用即改挂，禁止 |
| `governance/results`、`governance/lineage-index` | 602/603 与 604 的资源 |
| 门户扶持十条 | 门户的任务，跨项边界。不做成展示条目 |
| `policy_support` 列抬升 | 源上字面 null，回包第 24 条已确认是预期。不做要素抬升 |
| 政策拆解（607/608）与对比（610）页对库的调用方式 | 拆解、对比各有自己的资源。本叶不定义消费契约 |
| 第 7 项读图 | 605 不涉及图 |

## 7. 明确不做

- 不写 OpenAPI 字段表、请求体、响应体、枚举。
- 不新造 `metric_id`。不改 D4。不改模型注册表。
- 浏览器不改打专题 URL。不把 `E-E7-POLICY-M1-L06` 写成展示路径。
- 不重开 GDF，不写 nGQL，不加 ODS、DWD、ADS 表。本叶只加第 5 节这一张 `gapfill_` 表。
- 不在本叶改 Python 或 Java。
- 不改 `FE-POL-04A`，不新建前端单。
- 不改说明书、调研分册，不改 WBS 里的四单拆分。
- 不允许接口函数直接返回 mock。行都在表里，接口只读表。
- 不会签。不把本单标 done。

## 8. 签收条件：可实现

605 的链路现在就能照着做：建表 → 灌四维条目行 → element 只读 → display 委托。写成「等指标体系评审完再建库」，或者接口直接返回写死的条目，本单不可签收。

| 需规要点 | 可实现的做法 | 现在就能用的依据 |
|---|---|---|
| 梳理指标维度 | 维度闭集 = 需规点名的四个 | 需规原文点名，不扩充不缩减 |
| 搭建标准化指标库 | 建表灌行，接口读表 | 签收标准的唯一许可路径（表+mock+读表） |
| 统一口径支撑拆解对比 | 每行带口径说明，供拣行 | 表行即条目，无需新算法 |

迁移边界：demo 本地数组不迁数据；门户扶持十条留在门户；注册指标留在注册表。展示不打 `/internal/*`。

## 9. 表与要灌的 mock

| 表 | 要灌的 mock | 不灌 |
|---|---|---|
| `gapfill_policy_indicator_lib` | 四个维度（扶持力度、适用范围、实施时效、申请条件）× 若干政策的条目行，每行含口径说明与条目值 | 注册指标的值（不借 `M_POLICY_*`）；`policy_support` 抬升；门户扶持条目；编造的注册 `metric_id` |

行要能按 §5.1 的条件拣出来。灌数单执行人是 `data-agent`，监管 `human:淮政玮`，状态 backlog，依赖本架构和 `POL-L2-PC1-INDLIB-DATA`。查询请求不灌数。
