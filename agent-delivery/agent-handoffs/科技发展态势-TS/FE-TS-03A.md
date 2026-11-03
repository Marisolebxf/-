# FE-TS-03A · 技术发展跟踪（M3）整页复刻 — 前端交付（联调中）

> 仓库：`repos/lumen-ui-science-pc`；路由 `/trend/tech-development-tracking`（menu.ts 注册，fullBleed 布局）。
> 状态：mock 数据环境人工点测通过，**进入联调**（`API-TS-M3` + BE-TS-CONTRACT 契约冻结后切 `USE_MOCK=false`）。

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
| 说明 | 三阶段状态机（setup/running/result）对齐 demo App.jsx TechnologyDevelopmentTracking；meta+dataset 双接口 defineApi 双轨；派生逻辑集中在 `trackingModel.ts`；复用 StepIndicator/SearchableCascadeFilter/TiandituMap/InsightDetailDrawer/VChart；未用 YAGNI 跳过可观测（M1 拦截器）。D9 统计 ⓘ/🧪 待注册表接入后补全（见遗留风险）。 |

## 范围与实现（对照 DoD）

| DoD 项 | 实现 |
|---|---|
| 结果：综合分 + 阶段判定 + 4 期历史矩阵下钻 | `components/ResultDashboard.vue`（综合热度指数 hero + 发展阶段/趋势 KPI；多视图工作台热力/地图/气泡/关系图；**评估结果追踪**：4 期 × 4 方法并排矩阵 + 阶段对比 + 方法对比；演示历史切换） |
| 参数：5 套模板权重/阈值/启用维度展示 | mock `technologyEvaluationParameterTemplates`（5 套系统模板）+ `ParameterTemplateDialog.vue` / `SetupStage.vue` 参数网格 + 导入导出/优化/保存模板弹窗 |
| 方法：4 评估方法详解 + 案例 | `MethodDetailDialog.vue` + `MethodComparisonDialog.vue` + `MethodKnowledgeDrawer.vue`（知识库案例/最佳实践） |
| 评估工作流（demo 整页） | `index.vue` 三阶段；`SetupStage.vue` / `RunningStage.vue`（冻结口径 + 进度/成功失败演示） |
| Mock 种子冻结自 demo；接口四类用途 | `mock/modules/tracking.ts` + `api/situation/tracking.ts`（`fetchTrackingMeta` / `fetchTrackingDataset` → `/situation/v1/tracking/*`） |
| pnpm build 绿 | ✅ 见验收证据 |

### 类型契约（联调对接清单）

- `types/tracking.ts`：`TrackingMetaResult`（阶段/模板/方法/知识库/历史矩阵/地图字典）+ `TrackingDataset` + 参数模板/方法类型
- `api/situation/tracking.ts`：
  - `GET /situation/v1/tracking/meta` → `TrackingMetaResult`
  - `GET /situation/v1/tracking/dataset?fieldValues&regionKeys&startYear&endYear&keyword` → `TrackingDataset`
- 契约冻结后仅改 api 层 `real`，页面/models 零改动

## 验收证据

- `pnpm type-check`（vue-tsc --build）：**0 error**
- `pnpm build`：**绿（~38s，2026-10-15）**
- 人工点测（监管人 human:孔东，2026-10-15，dev `:3000` `/trend/tech-development-tracking`）：
  - setup：范围筛选、参数配置、方法勾选、模板/导入导出/优化建议/知识库弹窗
  - running：进度阶段与成功/失败演示切换
  - result：KPI、多视图图表、详情侧栏、历史矩阵与方法/阶段对比、报告导出入口
  - UI：评估设置说明区 `.tracking-evaluation-setup-note` 上下间距调整（避免与步骤条挤压）

## 偏离说明

- hero KPI 文案与 demo 一致为「综合热度指数」，四方法得分主要在「评估结果追踪」矩阵/方法对比区展示（非 hero 四卡）；与 demo 冻结一致
- 历史记录区保留「演示用历史状态切换」（demo 同语义；真实环境由后端历史评估记录驱动）

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java→Python | ✅ api 层真实路径 `/situation/v1/tracking/*` |
| D12 不调 demo-* | ✅ USE_MOCK=false 走网关，无 demo 服务 |
| D8 Design token | ✅ `demo-tech-tracking.css` 整块抽取 + Arco/VChart |
| D9 血缘 | ⚠️ 结果 KPI 尚未挂 MetricSpecCard / MockBadge；联调前按矩阵补 TS-M3 metric_id |
| D10 交互规范 | ✅ 步骤条/弹窗/抽屉/键盘 tablist 对齐 demo |
| 可观测 | ✅ X-Trace-Id/traceparent（M1 拦截器） |
| 无新依赖 | ✅ 零新增 npm 包 |

## CI/CD（必填）

- 分支：`dev`
- dev 测试：`pnpm dev` → `/trend/tech-development-tracking`（USE_MOCK=true）

## 涉及文件

**新增**：`src/views/situation/tracking/`（index + components + models + styles）、`src/api/situation/tracking.ts`、`src/mock/modules/tracking.ts`、`src/types/tracking.ts`  
**修改**：`src/mock/register.ts`、`src/router/menu.ts`、`src/config/echarts.ts`、`src/components/drawer/InsightDetailDrawer.vue`、`src/components/drawer/detailModel.ts`（详情抽屉扩展支持跟踪页下钻）

## 遗留风险

- `metric_id`（TS-M3-*）待 metric-registry 正式挂接后替换占位 —— **2026-11-03 进展**：本页数字在指标库**没有已签收指标**（DS-03 模块 `M_TECH_*` 是另一套、`is_mock=true`、算法服务未上线，挂上去即错挂），故按 D9 §2 先落 **D1 missing 红问号 + 治理引用**（`DS-03-METRIC-OPEN-L01` / `Q-MO-DS03-01…06`），不显伪 8 件套；详见 `docs/tracking-真评估接入设计.md` §11。
- BE-TS-CONTRACT-01 / `API-TS-M3` 未冻前，`USE_MOCK=false` 仅做冒烟 —— **2026-11-03 进展**：已切 `USE_MOCK=false` 跑真实数据并完成联调（meta/dataset 经 display 网关取久新只读通道），本条关闭。
- 联调确认：mock 验收通过，**联调闸门待 Java 契约冻结** —— **2026-11-03 更正**：联调已完成，闸门解除；本轮追加工作另立三单 `SITUATION-TS-TRACKING-EVAL-L01`（真评估接入）/ `-REPORT-L01`（报告生成与复用）/ `-PERSIST-L01`（范围挂载 + 落库回读 + D9 缺口角标）。
- ⚠️ 人工验收闸门（2026-10-20 裁定）：上述改动全部停本地工作区，**未 commit / 未 push**，等 `human:孔东` / `human:唐绍祖` 走查通过后推送。

## 2026-11-03 第二批（用户点名四项）

| 项 | 结果 |
|---|---|
| 产业领域接通 | 复用科技全域态势真源 `subfield_topic_map`（innov `/industry-subfields`）：display `resolveSubfieldIds` 反查 → `subfield_ids`；同时修掉 `meta.fieldScope` 写死空串导致默认领域被覆盖、领域永不生效。实测 `CL-SEI-01 → 39 个子学科`，口径回传「技术领域：已生效…」 |
| 结果页榜单表 | `ResultDashboard` 新增技术评估榜单（Top-20，10 行预览可展开），消费 `dataset.records`，只排序格式化不重算 |
| 报告上限 + 清理 | 最近列表 5 条上限；`POST /report-remove` 逻辑删除（`status=deleted` 留痕）+ 删本地产物；前端两段式确认（「清理」→「确认清理」），不套嵌套 Modal |
| 领域提示 | 二态化，由反查结果驱动：「已映射 N 个久新子学科，参与取数」/「未关联，本次不参与」 |

补充踩坑（供 review 参考）：Arco 静态 `Modal.confirm` 在 `ReportExportDialog` 里 `onOk` 不触发（请求根本没发出，后端日志无记录）→ 已改为按钮两段式确认，功能正常（DB `active 5 / deleted 2`）。

**mock 归属**：本页 mock 已按 `mock-ledger.md`「技术发展跟踪登记（2026-11-03）」逐行登记 ——
① 前端演示轨 `src/mock/modules/tracking.ts`（`trackingMocks` + `trackingEvaluationMocks`，`fe-ts-03a-v1`，种子冻结自 demo）；
② **后端零 mock 种子**（`TrackingController` 无 `MockProvider`、域服务 resources 无种子 SQL）；
③ 报告/模板类 6 个 API 演示轨**无 mock 注册**，`USE_MOCK=true` 时显式抛 `Missing API mock registration`（诚实失败，不造伪报告）。
