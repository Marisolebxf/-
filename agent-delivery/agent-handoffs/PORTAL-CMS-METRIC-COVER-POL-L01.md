# PORTAL-CMS-METRIC-COVER-POL-L01 · 门户指标覆盖核对·政策扶持

> 定义核对。未改 `PORTAL-CMS-政策扶持.md`，未改种子，未改就绪度矩阵，未写业务仓代码。未 commit，未 push。状态送到 `ready_to_sign` 后，签收操作人是 `human:淮政玮`。本 handoff 不写签收已完成，note 不附会签类确认词。完成日期要求：2026-11-05（WBS-03-04；本叶交付的是核对结论）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 开工时 `status=ready`。已 `task-claim`，再转入 `in_progress`。任务类型 `definition`。完成路径停在 `ready_to_sign`，不改为 `done` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义核对。派单强度为 full，但本单不写代码。未用 YAGNI 删缺项行，未改契约 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 契约、WBS-03-04、`data-lineage-policy.md` §2 / §2.3 / §7.3，以及下列指标 8 件套，均按原文阅读。未用压缩摘要代替精读 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无 |
| 图 diff | 本单不改图 |
| 会签态 | 不自填。契约文件头仍是草案 |
| 说明 | 定义核对，没有架构图或存储流图要改 |

## 范围与实现

只核对政策扶持契约里的指标行，对照现行 metric-registry（2026-10-23，`metric-get` / `metric-query`）。不新编口径。

对照原文：

- `agent-delivery/agent-handoffs/平台基建-PLATFORM/产物/PORTAL-CMS-政策扶持.md` §1.1–§1.4、§1.6（§1.5 时间线是 record，不在本单十条里）
- `agent-delivery/工程过程/04-系统集成/03-专题系统集成/WBS.md`「WBS-03-04 政策扶持」
- `agent-delivery/bid-reference/智慧服务门户系统-要素相关.md` §1.1.1.1.1.1.2（契约招标锚点，只用来核对区块语义，不新写口径）
- `agent-delivery/data-lineage-policy.md` §2、§2.1、§2.3、§7.3

D9 用法：8 件套只取 `kit`。`found.matrix=false` 且 `readiness.d1_def_status` 为空时，只说明种子里有这个 ID，**不写成 D1 已对齐**。`extras.is_mock` 是种子标记，不是 D4。`lifecycle_stage=unspecified` 且 `lifecycle_stage_inferred=true` 的，不写成 8 件套已齐。

政策域列表查询 35 条，全部 `found.matrix=false`。另查「发布密度」0 条；「政策排名」0 条；`M_POLICY_CITY` 0 条；「密度」无政策域 ID。

## 问题清单

- QPOL-02 仍是 🟡（力度 / 机遇等权重与阈值待甲方）。本单不拍板，不升绿，不改临时权重。
- 下列十条在契约里已经记为缺口。核对后仍然是缺口，没有可以改挂的现成 `metric_id`。
- 省级、城市力度排名没有单独排名 ID。排序依据只核对 `M_POLICY_INTENSITY_SCORE`。不用 `M_POLICY_INTENSITY_INDEX` 替换。

## 十条缺项

结论只有「缺口」。相近 ID 都不能顶替。每条相近 ID 都是种子有、矩阵无、D1 为空。

### 1. stats · 全国政策数量及连续性 — 缺口

招标语义：展示全国相关产业的政策数量及连续性。

| 相近 ID | 身份（8 件套摘要） | 不能顶替的原因 |
|---------|-------------------|----------------|
| `M_POLICY_TOTAL_COUNT` | 政策总数。`STAT`。`COUNT(DISTINCT policy_id)`。快照去重总数，可按层级/地区/时间筛选。`version=0.1.0` | 只有数量，没有连续性。对象是政策库全量，不是「相关产业」的全国数量加连续性 |
| `M_POLICY_TIMESERIES` | 政策时序指标。`STAT`。发布量按期计数；增长率/连续性 `pending_algorithm`。`formula_status=pending_algorithm` | 连续性还不能算。也没有按全国、按产业切开 |
| `M_POLICY_OPPORTUNITY_COUNT` | 政策机遇数。`STAT`。口径 `pending_data_lead(QPOL-02)`，公式 `pending_algorithm` | 计的是过阈值的机遇条数，不是政策数量。本单不拍板 QPOL-02 |

### 2. stats · 省级政策数量及连续性 — 缺口

招标语义：各省对于相关产业的政策数量对比，以及发布连续性对比。

| 相近 ID | 身份（8 件套摘要） | 不能顶替的原因 |
|---------|-------------------|----------------|
| `M_POLICY_LEVEL_DIST` | 政策级别分布。`STAT`。按国家级/省级/市级/区县级 `COUNT(DISTINCT policy_id)` 与占比 | 这是文件的行政级别，不是各省之间的数量对比，也没有连续性 |
| `M_POLICY_TOTAL_COUNT` | 同上，快照总数 | 筛出一个数，不是省与省的对比，没有连续性 |
| `M_POLICY_TIMESERIES` | 同上，全库时序 | 不按省分组。连续性 `pending_algorithm` |

### 3. stats · 市级政策数量及连续性 — 缺口

招标语义：全国重点城市对相关产业政策的数量对比及连续性对比。相近 ID 与第 2 行相同。

| 相近 ID | 不能顶替的原因 |
|---------|----------------|
| `M_POLICY_LEVEL_DIST` | 「市级」只是行政级别里的一档合计，不是重点城市之间的对比，没有连续性 |
| `M_POLICY_TOTAL_COUNT` | 快照总数，不是城市对比，没有连续性 |
| `M_POLICY_TIMESERIES` | 不按城市分组。连续性 `pending_algorithm` |

`metric-query` `M_POLICY_CITY` 为 0 条。没有城市数量对比 ID，没有城市连续性 ID。

### 4. map · 全国发布密度 — 缺口

招标语义：地图展示全国各地的产业政策发布密度。没有发布密度 ID。

`M_POLICY_NATIONAL_DIST`（全国政策分布，`STAT`）的公式是按省 `COUNT(DISTINCT policy_id)` 与占比。计数和占比没有面积或人口这类分母，不是发布密度。不能改挂。

「密度」命中的是企业密度、服务网络密度等，域不是政策，不能拿来顶政策发布密度。

### 5. map · 省发布密度 — 缺口

没有发布密度 ID。`M_POLICY_NATIONAL_DIST` 仍是省级计数与占比，不是某一省内部的发布密度。`M_POLICY_LEVEL_DIST` 是行政级别分布，不是省地图密度。

### 6. map · 市发布密度 — 缺口

没有发布密度 ID。没有市级分布 ID，也没有市级密度 ID。第 4、5 行的相近 ID 同样不能顶替。

### 7. coverage · 产业链节点上的政策覆盖 — 缺口

招标语义：结合产业链全景图，展示各节点的相关政策覆盖情况。契约写明覆盖数不进 CMS。

`M_POLICY_INDUSTRY_COVERAGE`（政策产业覆盖度，`STAT`，`version=0.1.0`）的定义是「已覆盖节点数 / 产业链全节点数」。公式为 `pending_algorithm`，`formula_status=pending_algorithm`，`srs_refs` 为空。它是一条还不能算的覆盖率，不是各节点上的覆盖情况。不能改挂。矩阵未覆盖，D1 为空，不写成已对齐。

### 8. shenzhen · 深圳政策数量及趋势 — 缺口

招标语义：深圳相关产业发布的政策数量及趋势。

| 相近 ID | 不能顶替的原因 |
|---------|----------------|
| `M_POLICY_SZ_DIST` | 深圳政策分布。公式是 `region` 命中深圳后按区计数。定义散文写了增长趋势，公式里没有逐期。也没有「相关产业」过滤。不能当作全市数量及趋势 |
| `M_POLICY_TIMESERIES` | 全库时序，不限定深圳，不限定产业。增长率/连续性 `pending_algorithm` |
| `M_POLICY_TOTAL_COUNT` | 可按地区筛选的快照总数，不是趋势 |

### 9. shenzhen · 深圳各区发布情况 — 缺口

招标语义：地图或图表呈现深圳各区的政策发布情况。

`M_POLICY_SZ_DIST` 最接近：按福田/南山/宝安/龙岗等区去重计数与占比，`version=0.1.0`，需求来源是展示系统政策全景（05 分册 seq 100），不是本门户行的已挂 ID。不能顶替，原因有三条：

1. 公式是存量计数和占比，不是各区发布情况；定义里的增长趋势没有进公式。
2. 招标写的是深圳相关产业政策。该 ID 只用 `region LIKE '%深圳%'`，没有产业范围。
3. 矩阵未覆盖，D1 为空。种子里有一条区县分布，不等于这行已经有可对齐的取数 ID。

`M_CHAIN_SZ_POLICY`（深圳政策维度）也不顶替：`found.seed=false`，8 件套各项为空，`algorithm_type=UNKNOWN`（推断）。矩阵侧 D1 写成 `aligned`，与规约「UNKNOWN 不得标 D1=aligned」以及「种子缺失不得脑补」不一致。本单不改矩阵，也不把它当成已对齐。`M_POLICY_SZ_DIST` 的需求来源已写明禁止用它顶替深圳分布。

### 10. shenzhen · 深圳产业链节点覆盖 — 缺口

招标语义：结合深圳产业链全景图，展示深圳产业链节点的政策覆盖情况。

`M_POLICY_INDUSTRY_COVERAGE` 是全库节点覆盖率，公式 `pending_algorithm`，没有深圳范围，也不是各节点覆盖情况。不能改挂。

## 力度排名

只核对 `M_POLICY_INTENSITY_SCORE`。省级、城市都没有单独排名 ID。`metric-query`「政策排名」为 0 条。

| 项 | 核对结果 |
|----|----------|
| 契约取数 | 省级排名、城市排名的排序依据都是这条评分。城市排名是按城市聚合该评分。CMS 不填名次、不填分数 |
| 8 件套 | 中文名「政策力度评分」。定义：选定产业或技术领域内，单条有效政策，效果/覆盖/成本三维，0–100。公式：三维分母不同，同年截面 min-max 后等权×100。`algorithm_type=MODEL`。源表 `dwd_policy_base`、`dwd_industry_chain_info`。源系统 `Mock @ batch=mock_20260623`。`update_freq=weekly`。`version=1` |
| 接入 | `found.seed=true`，`found.matrix=false`，D1 为空，`lifecycle_stage=unspecified`（推断）。**不是已对齐**。`extras.is_mock=true` 不是 D4。`pending_ref=QPOL-02`，本单不拍板 |
| 不改挂 | `M_POLICY_INTENSITY_INDEX` 是按城市综合的力度指数，对象是城市，分母含该市有效政策条数。它不是单条政策评分，不能替换 SCORE，也不能充当省级排名 ID 或城市排名 ID。它同样矩阵未覆盖、D1 为空，并挂 QPOL-02 |
| 不改挂 | `M_POLICY_SUPPORT_STRENGTH`（支持力度，`COMPUTE`）公式 `pending_algorithm`，挂 QPOL-02。不是排名 ID |

## 修改内容

- 新增本 handoff。
- 未改契约、WBS、种子、矩阵、客户决策清单、业务仓。

## 测试结果

- 十条都有结论，结论都是缺口，并写了相近 ID 不能顶替的原因。
- 排名只核对 `M_POLICY_INTENSITY_SCORE`；写明没有省级排名 ID、城市排名 ID；写明不用 `M_POLICY_INTENSITY_INDEX`。
- `M_POLICY_OPPORTUNITY_COUNT` 不顶替数量。
- 查询工具只有 `metric-get` / `metric-query`。未读 `metrics/registry` 的 seed 与矩阵 YAML。

## 遗留风险

- QPOL-02 仍待甲方。力度评分、力度指数、机遇数、支持力度都挂着它。页面在它闭合前不能把这些数当成已定口径。
- 十条缺口若要有数，需另开定义（新 ID 或证明某现有 ID 的对象与招标句相同）。本单不新编口径。
- `M_CHAIN_SZ_POLICY` 矩阵 D1=`aligned` 与空 8 件套、`UNKNOWN`、种子缺失并存。留给 data-agent，本单不改。
- WBS-03-04b 依赖本叶。本叶未签收前，指标页仍应按缺口做空态，不要用相近 ID 填数。

## CI/CD（必填）

- 分支：`gkx-orchestration` 的 `dev`（本地工作区，未推送）
- commit：无。本单要求停在本地
- pipeline URL / ID：无。定义核对不跑业务 CI
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无运行时。验收是契约与 MCP 对照

## 可观测性（建议）

- 无服务变更。不新增 `OTEL_SERVICE_NAME`，无 traceId。

## 涉及文件

- `agent-delivery/agent-handoffs/PORTAL-CMS-METRIC-COVER-POL-L01.md`（本文件，新增）

## 架构合规自检

| 项 | 结果 |
|----|------|
| 算法只在 Python | 未写算法，未改 Java |
| 调用链 | 未改接口 |
| 图谱只走 Nebula | 未涉及 |
| 可观测 | 无服务变更 |
| CI/CD | 定义文档，无业务流水线 |
| demo 不 merge 进 lumen | 未 merge，未改 lumen 仓 |
| D8 / D10 | 未改页面与交互 |
| D9 | 只读 8 件套与 D1–D4。矩阵未覆盖的一律不写已对齐。未改种子、未改就绪度 |
| D12 | 未调用、未修改 `demo-*` 服务 |
| D14 | 未涉及对象存储 |
| 业务口径 | 未拍板 QPOL-02，未新编口径，未改契约 |
| 决策不外包 | 缺口与「不能顶替」只复述已注册身份和招标原句，没有替甲方定阈值或权重 |

## DoD 对照

1. 十条（全国/省/市数量与连续性、三条发布密度、产业链节点覆盖、深圳数量及趋势、深圳各区、深圳节点覆盖）都有结论，结论都是缺口。
2. 力度排名只核对 `M_POLICY_INTENSITY_SCORE`。没有单独的省级排名 ID、城市排名 ID。机遇数不顶替数量。
3. 本 handoff 已落盘。`ponytail` 为 `N/A`。evidence 指向本文件。状态改为 `ready_to_sign`。note 不附会签类确认词。不改为 `done`。

## 成本

| 字段 | 值 |
|------|-----|
| model_used | `grok-4.7` |
| actual_tokens | `48000`（无 Console 分离值；按本单阅读与本文体量估算 in+out） |
| actual_cost | `0.29` 美元 |
| cost_warn | `green` |
| 计算公式 | Grok 4.7 不在 `budget-estimate.md` §1.2 价表。本单是定义核对，按 B 档 $3 / $15 每百万 token，algorithm 比例 75/25：`48000×0.75×3/1e6 + 48000×0.25×15/1e6 = 0.288`，记 `0.29`。低于 $5 |
