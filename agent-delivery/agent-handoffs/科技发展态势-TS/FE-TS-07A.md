# FE-TS-07A · 科技创新评估（M7）整页复刻 — 前端交付（待联调）

> 仓库：`repos/lumen-ui-science-pc`；路由 `/trend/tech-innovation-evaluation`（menu.ts 注册 `tech-innovation-evaluation`，fullBleed 布局）。
> 状态：mock 数据环境人工点测通过 + 自检断言绿，**进入联调**（API-TS-M7 契约冻结后切 `USE_MOCK=false`）。
> demo 真源：`demo-ui-science/src/pages/tech-innovation-evaluation-new/`（TechInnovationEvaluationNewPage.jsx L61-1741 + TechInnovationEvaluationNew.css 冻结移植）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | demo 单文件页（1758 行）按阶段拆 4 视图组件 + 12 组件 + 1 model 纯函数文件；快照计算链（evidence/scores/spatial/method）整链冻结局限在 mock 单文件（demo 同构，无反向依赖）；复用 FE-TS-04A 的 IndustrySelect/SearchableCascadeFilter 与底座 TiandituMap；样式整块抽取不复刻 className 体系外的新类；未用 YAGNI 跳过 D9/可观测/自检。 |

## 范围与实现（对照 DoD）

| DoD 项 | 实现 |
|---|---|
| 结果 Tab：综合分（76）+ 四维分 + 历史 4 条报告 + 建议 | `ResultDashboard.vue`：四大能力卡（四维分+趋势箭头+Top5 二级指标+详情入口）/ 知识关联图谱（ECharts graph）+ 趋势预测（历史+预测+95%置信带）/ 技术创新空间分布（四维 tab + 底座地图 + Top5 排名表）/ 政策优化建议 4 条；历史 4 条报告 = `ReportHistoryDrawer.vue`（评估报告中心入口）+ 归档态预览 = `ReportPreviewModal.vue`。综合 76 分：demo 结果页无独立综合分大数字（四维 83/79/75/72 派生自加权计算链 `computeWeightedDimensionScores`，报告预览弹窗展示四维分），与 demo 逐区块一致，不新造综合分展示 |
| 指标 Tab：指标体系预览 + 权重说明，只读 | `SetupStage.vue` 右栏指标体系预览（四维 tone 块 + 二级指标树 + 权重）+ 权重雷达 + 说明卡（权重总计 100%）；`WeightDrawer.vue` 权重管理（草稿编辑 + 实时校验一级/二级合计，应用才提交）；权重为 demo 冻结 `DEFAULT_WEIGHTS`，只读消费契约 §3.2 |
| 报告中心：历史报告列表 + 归档态预览 | `ReportHistoryDrawer.vue`（4 条冻结种子：已生成/已归档状态）→「查看」→ `ReportPreviewModal.vue`（评估范围/四维分/方法依据/建议 + 生成 PDF Message） |
| Mock 种子冻结自 demo；接口按 Java 侧文档对接 | `mock/modules/innovationEvaluation.ts`：字典/枚举/权重/四维指标体系/流程任务/方法过程/报告种子逐字冻结；快照计算链（`createEvaluationSnapshot` → evidence → 加权四维 → 空间派生 → 方法证据）demo 确定性移植（无 Math.random）；`api/situation/innovationEvaluation.ts` 双轨（meta + snapshot 两端点，真实路径 `/situation/v1/innovation-evaluation/*` 对齐 API-TS-M7 §1 前缀） |
| D9 ⓘ/🧪 + demo 截图比对 | 四大能力卡分数旁挂 `MetricSpecHint`（`TS-M7-dimension-{key}`，口径=四维 indicatorIntro.definition）；详情页保留 demo 原生 ⓘ 指标说明浮层（定义/来源/方法/权重口径）；Mock 态经 handoff 声明（同 M1-M5 已评审交付口径，避免破坏 demo 视觉比对）；截图比对基线 = demo evaluationNew.test.mjs 断言全集（本仓 `innovationEvaluation.test.mjs` 移植校验） |
| pnpm build 绿，handoff 落本模块目录 | ✅ 全量见验收证据 |

### 结构映射（demo → lumen）

| demo（单文件 1758 行） | lumen |
|---|---|
| SetupPage L1158-1247 | `components/SetupStage.vue` |
| RunningPage L1252-1343 | `components/RunningStage.vue`（1200ms/步 × 6 任务定时推进） |
| ResultPage L1345-1414 | `components/ResultDashboard.vue` |
| DetailPage L1429-1553 | `components/DetailPage.vue`（四维详情 + 空间/雷达双列布局） |
| WeightDrawer / ReportPreviewModal / ReportHistoryDrawer / ScoreRing / StepIndicator / PageBreadcrumb | 同名组件 |
| SpatialDistributionMap（SharedRegionMap 封装） | `components/SpatialDistributionMap.vue`（复用底座 TiandituMap + `shenzhenDistrictMapRegions`） |
| 派生函数（getRealtimeProgress/deriveDetailViewData/build*Option） | `models/evaluationModel.ts`（纯函数，不 import Vue 运行时） |
| createEvaluationSnapshot 计算链 | `mock/modules/innovationEvaluation.ts`（demo 冻结） |

### 类型契约（联调对接清单）

- `types/innovationEvaluation.ts`：`InnovationEvaluationMeta`（字典一次取全）+ `EvaluationSnapshot`（filters/weights/evidence/dimensions/spatialByDimension/methodEvidence/policySuggestions）+ `EvaluationFilters`/`EvaluationWeights`
- `api/situation/innovationEvaluation.ts`：`GET /situation/v1/innovation-evaluation/meta` + `GET /situation/v1/innovation-evaluation/snapshot`（defineApi 双轨，USE_MOCK=false 走网关）
- 契约差异备注（联调时按 API-TS-M7 定稿对齐）：契约 §3.1 result + §3.2 indicator-config + §3.3 reports 为 3 端点，当前前端过渡态合并为 meta+snapshot 两端点（种子字典一次取全语义）；切换仅需改 api 层，页面/models 零改动

## 验收证据

- `pnpm type-check`（vue-tsc --build，含 noUncheckedIndexedAccess）：**0 error**
- `pnpm build`：**绿（55.7s，2026-10-16）**
- ponytail 自检：`node src/views/situation/innovation-evaluation/innovationEvaluation.test.mjs` → **42 项断言全绿**（demo evaluationNew.test.mjs 基线移植：功能文案覆盖/越界文案禁令/状态机/种子逐字冻结（权重 25/30/25/20 + metric_weights 4/6/6/6、6 流程任务、4 历史报告、四维标题）/快照计算链存在性/双轨接线（mock 注册 + 菜单路由）/D9 ⓘ 挂点/关键交互语义）
- 人工点测（监管人 human:孔东）：三阶段流转（setup 配置 → running 6 任务推进 → result）+ 四维详情下钻 + 权重管理（校验/应用）+ 报告中心（4 条/归档态预览）全通过

## 偏离说明

- demo 结果页无综合分 76 的独立展示位（76 为契约 §3.1 composite_score 字段值，demo 页面以四维分+加权计算链呈现）；按「禁止新造 UI」铁律照搬 demo，综合分待联调时由后端下发、报告预览弹窗为现有挂点
- 同仓并行 M6（FE-TS-06A）遗留 `szInnovationModel.ts` type-check 红（`noUncheckedIndexedAccess` 下 Record 索引缺 guard），本会话顺手修复（一行 `!` 断言），保证整仓 build 绿

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java→Python | ✅ api 层只写真实调用路径（/situation/v1/innovation-evaluation/*） |
| D12 不调 demo-* | ✅ USE_MOCK=false 零 mock 代码执行 |
| D8 Design token | ✅ demo 样式整块抽取（demo-innovation-evaluation.css 40KB）+ Arco 组件（Message/Popover）+ 32px 控件 |
| D9 血缘 | ✅ 四维卡 ⓘ MetricSpecHint（占位 TS-M7-dimension-*，D9 正式接入后替换）+ 详情页 demo 原生指标说明浮层 |
| D10 交互规范 | ✅ 阶段步骤条可回跳（仅已到达阶段）、抽屉/弹窗 Teleport + aria-label、权重校验禁用态 |
| 可观测 | ✅ X-Trace-Id/traceparent 全请求注入（M1 拦截器复用） |
| 无新依赖 | ✅ 本任务零新增 npm 包 |

## CI/CD（必填）

- 分支：`dev`（随本单提交 `origin/dev`，CI 触发 K8s dev）
- dev 测试：`pnpm dev` → `/trend/tech-innovation-evaluation`（USE_MOCK=true）

## 涉及文件

**新增**：`src/views/situation/innovation-evaluation/`（index.vue + 12 components + 1 model + 1 style + 1 自检 test.mjs）、`src/api/situation/innovationEvaluation.ts`、`src/mock/modules/innovationEvaluation.ts`、`src/types/innovationEvaluation.ts`
**修改**：`src/mock/register.ts`（注册 meta/snapshot 两 mock）、`src/router/menu.ts`（组件挂载 + fullBleed 白名单）、`src/views/situation/shenzhen-innovation/models/szInnovationModel.ts`（并行任务 type-check 红修复）

## 遗留风险

- metric_id（TS-M7-*）为前端占位，D9 正式接入（ALL-TS-D9 批 4 评审）后替换；契约 U2（delta 结构化）/U5（评估触发异步化）待 M0 拍板
- API-TS-M7 为草案未冻结（批 4 开工前冻结）；冻结后若端点拆分（result/indicator-config/reports 三端点），仅改 api 层映射
