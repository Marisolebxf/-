# LUMEN-TOPIC-FE-SHARED-CHROME-L01 · 工作区公共骨架

> 格式参考 `templates/handoff-template.md`。本叶只抽 Tab / 页头 / 对象确认；字典筛选见 `LUMEN-TOPIC-FE-SHARED-FORM-L01`（backlog，依赖本叶）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | 用户 2026-08-20 明确授权建单 + 认领 + 开工 + 收口 commit/push。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D8/D10 class 与键盘可达。不重包 Arco Button/Table/Modal/Drawer。过程壳未做（规划 P1，留给后续叶）。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂 Headroom。 |

## 范围与实现

仓：`lumen-ui-topic`。抽三件公共骨架并接到已落地企业 / 产业链页。

| 组件 | 路径 | 用法 |
|------|------|------|
| `WorkbenchTabs` | `src/components/common/WorkbenchTabs.vue` | 一级 Tab：`global-workbench-tabs` + `role=tablist` + 左右方向键 |
| `AnalysisPageHeader` | `src/components/common/AnalysisPageHeader.vue` | `plain` 分析页 h1；`panel` 即原 WorkbenchPageHeader |
| `AnalysisObjectContext` | `src/components/common/AnalysisObjectContext.vue` | 对象预览 / 超限 / 返回对比篮 / 管理抽屉 |
| 预览口径 | `analysisObjectPreview.ts` | ≤5 全展示，>5 预览前 3 家 |

接线：企业评估 / 风险 / 引育 / 深圳现状 / 重点分析页头；产业诊断·区域·深圳·维护页头；`IndustryWorkspaceTabs` 改为通用 Tab + 评审插槽；评估/风险对象确认改为薄封装；画像 Tab、培育结果 Tab 同样改走 `WorkbenchTabs`。

CSS：`analysis-rounded-tabs` / `analysis-rounded-radio` / `sci-button-group` 写入 `search-workspace.css`（Design.md §7.3）。区域评价模式 Radio、风险洞察若干 Radio、重点分析地图/列表按钮已挂 class。

对比篮对象类型 Tab 仍手写（含 `aria-controls` 与自定义 keydown），本叶未强改，避免打散系统篮无障碍。

## 偏离说明

- `AnalysisProcessShell` 未抽：评估 / 风险 / 产业 / 引育过程页仍各用现壳。规划 P1，不塞进本叶。
- `sci-button-group` / `analysis-rounded-radio` 在 demo 仓无完整 CSS 真源（仅 class 引用）；按 Design.md §7.3 写入 lumen。
- **对比篮「服务机构」Tab 本叶不恢复。** 用户 2026-08-20 确认暂不处理。缺因是 `DEMO-SVC-ABORT-L01`（`4f923e3`）随服务机构页一并拆掉 `ServiceOrgCompareBasketPanel`；不是本叶骨架改动造成。重开须新 DAG / 新任务 ID。

## 产物清单

- 公共件：`WorkbenchTabs` / `AnalysisPageHeader` / `AnalysisObjectContext` / `analysisObjectPreview.ts`
- 自检：`scripts/check-shared-chrome.mjs`
- 本 handoff
- 代码仓 commit：`lumen-ui-topic` `b551267`（`origin/dev`）

## 验收证据

- `node scripts/check-shared-chrome.mjs` → `check-shared-chrome: ok`
- `npm run type-check`（`vue-tsc --build`）绿
- CI：push `origin/dev` 后由 GitLab pipeline 接续（本机未等 K8s rollout）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ 未改算法 |
| 2 调用链 前端→Java | ✅ 未新增直连 |
| 3 Nebula | ✅ 未改图谱 |
| 4 可观测 | ✅ 未删既有埋点；本叶无新请求 |
| 5 CI | ⏳ push `origin/dev` 后由 GitLab 接续 |
| 6 demo2 不 merge lumen | ✅ |
| 7 共享聚合 | ✅ |
| 8 数据策略 | ✅ 未改 Mock 填数 |
| 9 D8 Design | ✅ Tab class / 不包 Arco 皮肤 |
| 10 D9 | ✅ 未改血缘组件进口径 |
| 11 D10 | ✅ 一级 Tab 键盘 + role=tablist |
| 12 D12 | ✅ 只动 lumen-ui-topic |

## 测试结果

- 预览函数自检绿（`scripts/check-shared-chrome.mjs`）
- `vue-tsc --build` 绿
- 未做 Playwright e2e（tech_task 骨架，无新路由）

## 遗留风险

- 对比篮对象类型 Tab 未迁到 `WorkbenchTabs`；后续 FORM 叶不要重复造 Tab。
- 对比篮服务机构 Tab / 面板按用户决定本叶不恢复；SVC 新链开工后再单独立叶。
- 过程壳四套平行仍在，政策模块开工前建议单独立叶。
- `task-registry.yaml` 仅经 MCP 回填，本 handoff 仓 commit **不**夹带 registry 手改。

## CI/CD

- 分支：`lumen-ui-topic` `dev` → `origin/dev`
- commit：`b551267ef5ba6b37c9712dadde19367fd95fae53`
- pipeline / K8s：push 后由 GitLab 触发；本机未等 rollout
- 编排仓：本 handoff 同步 push `gkx-orchestration` `origin/dev`

## 可观测性

- 本叶无新 HTTP；沿用现有 `request.ts` / `X-Trace-Id`
- OTEL / Tempo：N/A

## 涉及文件

- `src/components/common/WorkbenchTabs.vue`
- `src/components/common/AnalysisPageHeader.vue`
- `src/components/common/AnalysisObjectContext.vue`
- `src/components/common/WorkbenchPageHeader.vue`
- `src/components/common/analysisObjectPreview.ts`
- `src/components/common/index.ts`
- `src/components/industry-center/IndustryWorkspaceTabs.vue`
- `src/components/enterprise/evaluation/EvalObjectContext.vue`
- `src/components/enterprise/risk/RiskObjectContext.vue`
- `src/views/enterprise/EnterpriseEvaluation.vue` / `EnterpriseRisk.vue` / `EnterpriseRecruit.vue` / `EnterpriseSzStatus.vue` / `EnterpriseKeyAnalysis.vue`
- `src/views/industry-center/IndustryDiagnosisPage.vue` / `IndustryRegionalPage.vue` / `IndustryShenzhenPage.vue` / `IndustryMaintenancePage.vue`
- `src/components/search/ElementProfile.vue`
- `src/components/enterprise/recruit/RecruitResultPanel.vue`
- `src/components/enterprise/keyAnalysis/TypeRegionPanel.vue`
- `src/components/enterprise/risk/PainPointsPanel.vue` / `SupplyChainInsightPanel.vue` / `SupplyChainNodeList.vue`
- `src/assets/search-workspace.css` / `src/assets/layout/diagnosis-shell.css`
- `scripts/check-shared-chrome.mjs`

## 成本

- actual_tokens: 220000（会话估算：规划对照 + 实现 + 收口；source: session_estimate）
- model_used: cursor-grok-4.6
- actual_cost: 1.28
- cost_warn: green
