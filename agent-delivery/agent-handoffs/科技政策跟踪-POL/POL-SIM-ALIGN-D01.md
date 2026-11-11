# POL-SIM-ALIGN-D01 · 政策效果推演整页对齐原型

- 时间：2026-11-10
- 仓库：`lumen-ui-science-pc`（只改此仓；未提交、未推送 `gkx-orchestration`）
- 分支：`dev`
- commit：`ae03b25c2299a111557005631f19bb1a7e4dc712`
- push：`origin HEAD:dev` 已成功（`6f6fe85..ae03b25`）
- 复刻自：`demo-ui-science` `src/pages/policy-tracking/simulation/`（只读对照，未 merge）
- 监管：`human:淮政玮`
- 强度：完工即推

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 本叶按总控 §5.1 开工。按派单不调用 task-claim / task-update-status / task-create，注册表状态未改。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用仓内 Arco、`RegionalSpatialMapChart`、`simulationLive` 与原型种子图表工厂。未新造地图、未把互斥布局叠在同一节点。未跳过 D8/D9 评审门控与 Mock 开关。 |

## 范围清单

政策效果推演整页（`src/views/policy/simulation/**`）。

效果预估五子页：

- 未出台：参数、仿真结果、多次模拟对比
- 新出台：政策摘要（引用解析）、短中长期效果、时间变化趋势、产业发展影响、空间分布特征
- 区域：三维地图·省域热力+城市柱高、热力图·指标矩阵、模拟参数、模拟结果预测
- 多维度效果评估：四维雷达、分项柱、维度说明
- 利益攸关方：四项识别、意见列表

科技政策推演六子页：

- 文本解析、重点可视化、影响范围、关联分析、实施路径、解读报告

`USE_MOCK=true` 仍走原型种子。`USE_MOCK=false` 只渲染接口行。未改全景、评价、专题仓、Java、Python。

## 修改内容

- 新出台真轨从「政策摘要 / 效果与分布」两张总卡拆回原型五块。短中长期、时间趋势、产业影响、空间分布各留标题。
- 未出台仿真结果改回经济效益 / 社会影响 / 创新促进三格；逐年趋势只有「2026年120、2027年146」这种整段才画折线。
- 区域页保留工作区已有的 `spatialItemsToCities` / 单列热力图。对不上城市坐标时仍留「三维地图」「热力图」标题：地图卡展示原文，热力图空态。未选区域、没有对得上的行两句空态未改。请求体在政策类型留空时仍只有 `kind` + `region_name`，不带 `target_industry`。
- 利益攸关方四项识别在真轨保留四个标题，结论空态「没有识别结论」；意见正文仍来自接口。
- 推演六子页真轨补回原型块：解析用描述列表；重点柱图无得分则空；影响范围拆成受益对象、覆盖面、分区域、影响区域、影响行业、空间分布、时间变化；关联网络与协同效应两块空态且不请求；路径保留历史评估图空态 + 实施流程时间轴；解读报告按接口段落做章节勾选，不下载文件。
- 页头四张统计卡的 86.5 / 78 / 7 / 3 只在 `USE_MOCK=true` 出现。真轨四张标题 + 「没有接口得分」。
- 折线工厂 `plainLineOption` 不写置信度。

## 复刻验收

### V1–V7

| # | 结果 | 说明 |
|---|------|------|
| V1 | ✅ | 页在政策跟踪壳内，本页不另铺灰底；样式仍引 `demo-policy-simulation.css` |
| V2 | ✅ | 本页不是检索 Hub，无独立白卡片搜框 |
| V3 | ✅ | 卡片标题与正文横向书写，参数与结果分列 |
| V4 | ✅ | 真轨 / 种子用 `v-if` / `v-else` 互斥，不把两套 layout 叠在同一节点 |
| V5 | ✅ | `.ps-sub-pane` 保留 `min-width: 0`，只加在需要截断的栅格子项 |
| V6 | ✅ | 无行、未选条件走既有空态文案；有行则进对应卡片 |
| V7 | ✅ | 无 `industry-search-result-card` |

### R1–R5

| # | 结果 | 说明 |
|---|------|------|
| R1 | ✅ | 五子页 + 六子页原型块都有标题和结构 |
| R2 | ✅ | 未选、无行、有句子、有可解析分数四种展示分开；失败仍落成无行空态（沿用原接线，不新造加载条） |
| R3 | ✅ | Arco + 本页既有 `ps-*` / demo 仿真样式，未另起一套灰白皮肤 |
| R4 | ✅ | 评审只走 `useReviewStore` 与 `@/components/lineage/MockBadge`。闸门文案在 `reviewMode` 下。未自造 ⓘ。真轨页头无统计数字，故无 metric 挂点；种子态页头仍是 `PolicyStatCard`（`M_POLICY_EFFECT_SCORE`、`M_POLICY_IMPLEMENTATION_EFFECT`、`M_POLICY_LAYOUT_REC_COUNT`） |
| R5 | ✅ | 开：`USE_MOCK` + `@/mock/modules/policySeed`。关：不引用种子填数；句子展示原文；解析失败留标题和空态 |

## 自检

| 命令 | 结果 |
|------|------|
| `node src/views/policy/simulation/simulationLive.test.mjs` | 通过（含广州市42 等四市柱、单列热力、区域请求不带 target_industry、年份序列与句子互斥） |
| `node src/views/policy/simulation/FE-POL-03A.test.mjs` | 通过，42 项 |
| `pnpm type-check`（`vue-tsc --build`） | 通过，exit 0。本叶引入的 `VChart` option `null` 已改为 `undefined`。无与本叶无关的既有类型红 |

## 测试结果

- 未在浏览器点选线上页。真轨数字是否出现以接口行能否被 `yearPoints` / `namedScorePoints` / `spatialItemsToCities` 解析为准，自检覆盖了种子句与「广州市42、深圳市38、佛山市21、东莞市16」。

## 遗留风险

- 推演失败与「没有对得上的行」仍是同一种空态。
- ~~影响范围没有覆盖率列，覆盖面块在真轨保持空态。~~ **废止（2026-11-12 需规分句闭合卡1=C）**：已加 `coverage_rate` / `eligible_count` / `covered_count` / `penetration_score`，真轨出覆盖面与渗透 KPI。
- 政策关联没有读口，两块保持空态。
- 注册表未回写（本叶禁止 task-update）。cost 四字段未写入 task-registry。

## CI/CD（必填）

- 分支：`dev`
- commit：`ae03b25c2299a111557005631f19bb1a7e4dc712`
- pipeline URL / ID：push 已触发，本叶未等流水线
- 部署 namespace / 镜像 tag：未在本叶核对
- K8s rollout：未核对
- dev 测试 URL / 命令与结果：见上表三条本地自检

## 涉及文件

- `src/views/policy/simulation/index.vue`
- `src/views/policy/simulation/estimate/EstimateWorkbench.vue`
- `src/views/policy/simulation/interpret/InterpretWorkbench.vue`
- `src/views/policy/simulation/sharedCharts.ts`
- `src/views/policy/simulation/simulationLive.mjs`
- `src/views/policy/simulation/simulationLive.test.mjs`
