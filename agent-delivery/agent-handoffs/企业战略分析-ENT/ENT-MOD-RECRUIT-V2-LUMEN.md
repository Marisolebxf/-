# ENT-MOD-RECRUIT-V2-LUMEN · 引育推荐 V2 lumen 准生产实现

> 格式参考 `templates/handoff-template.md`；内容按本次实测与代码实写。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 说明 | S4 终止后续调整并入本任务；对齐 demo 功能/显示，真接口 `#102–#109` 不动 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 composable/store/API；未新加依赖；未用 YAGNI 跳过 D8/D9/D10 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 Headroom |

## 范围与实现

| DoD 项 | 结果 |
|--------|------|
| lumen-ui-topic 可演示并与产品/UX（demo）基线对齐 | ✅ 筛选/候选/结果/报告链路对齐 demo；招引·培育分袋隔离 |
| 会签单签字；lumen commit SHA + K8s/dev URL | ⏸ commit/SHA 已写入；会签与 K8s URL 待联调后补 |
| npm run build 通过 | ⏸ 本机以联调验证为主；CI 随 `origin/dev` push 触发 |

### 本轮实现要点

1. **条件筛选 / 候选台**：布局与条件真源对齐 demo；`RecruitReviewConfigPanel` 去权重滑块；候选企业产业/规模经对比篮缓存 + `#6 by-codes` 补全。
2. **招引 / 培育分袋**：`useRecruit` 按 mode 隔离条件、权重、任务与结果，互不串袋。
3. **结果与报告**：`#106` 资产读取（mock auth 不带 Bearer，避免 424）；失败回退 `#105.resultData`；`recruitResultMap` 兼容包络/snake_case；报告创建 `format: 'pdf'`；「查看 PDF」用报告任务 ID 调 `#106` 打开/下载。
4. **对比篮**：`entEnterpriseScales` 字典缓存；`compareBasket` 本地缓存 + `#91` 同步；修正 `source_route` / `source_summary`；去掉误调 `#14 compare`。
5. **任务栏轮询**：`SystemTaskFloat` 先探 `#108 running`；running 为空时不再调 `#103 list`。

## 问题清单

- 报告「查看 PDF」原先只关弹窗切 analysis_view，未走 `#106` → 已修。
- `#106` 曾因 mock Bearer 导致 424 → headers 与 `request.ts` 对齐。
- 任务栏空闲轮询仍打 list → running 为空跳过 list。

## 修改内容

- 引育工作台全链路 UI/编排对齐 demo + 真接口结果映射。
- 分析任务资产打开 API：`analysisTaskAssetOpen`（`#106`）。
- 全局任务浮层轮询减负。

## 测试结果

- 联调：推荐任务完成 → 结果展示；PDF 任务 success → `#106` 打开/下载。
- 自检：`recruitResultMap.selfcheck.mjs`（结果映射非平凡逻辑）。
- 任务栏：无 running 时网络面板不再出现 `analysis/tasks/list`。

## 遗留风险

- 会签签字与正式 K8s/dev URL 待 CI/部署后补登记。
- 评审模式关闭后需再扫一遍 DOM 无 `metric_id` / GAP 泄漏（沿用既有 review 门控）。
- PDF 弹窗拦截时回退下载，依赖浏览器策略。

## CI/CD（必填）

- 分支：`dev` → `origin/dev`
- commit：`a0e1393`（`lumen-ui-topic`）
- pipeline URL / ID：push 后由 GitLab CI 生成（待填）
- 部署 namespace / 镜像 tag：待 CI
- K8s rollout：待 CI
- dev 测试 URL / 命令与结果：本地 `npm run dev` 联调通过；路由 `/enterprise/recruit`

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用页面既有前端埋点
- traceId（dev 抽样）：无新增抽样
- Tempo / Loki：无

## 涉及文件

### 新增

- `src/api/enterprise/types/talentRecommendResult.ts`
- `src/components/enterprise/recruit/RecruitOutputTaskModal.vue`
- `src/components/enterprise/recruit/recruitResultMap.ts`
- `src/components/enterprise/recruit/recruitResultMap.selfcheck.mjs`
- `src/stores/entEnterpriseScales.ts`

### 主要修改

- `src/composables/useRecruit.ts`
- `src/views/enterprise/EnterpriseRecruit.vue`
- `src/components/enterprise/recruit/{CandidatePanel,RecruitFilterPanel,RecruitResultPanel,RecruitReviewConfigPanel,RecruitWorkbench}.vue`
- `src/stores/compareBasket.ts`
- `src/api/enterprise/analysisTask.ts`
- `src/components/system/SystemTaskFloat.vue`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 前端 → Java REST（不越层） | ✅ 仅 `#102–#109` / 企业 REST，未直连 Python |
| Nebula / 算法不在前端 | ✅ |
| D8 Arco + Design | ✅ 复用 Arco Vue + 既有 Section/评审组件 |
| D9 血缘 ⓘ / 角标 | ✅ 评审门控下 Metric/Trace 入口保留 |
| D10 交互 | ✅ 对齐 demo 状态机与弹窗/步骤 |
| 可观测 | ⏸ 无新增埋点；沿用既有 |
| demo→lumen 复刻 | ✅ 功能/显示对齐，未另起 UI 体系 |

## 提审说明

- 状态建议：`in_progress` → `integration`（AV-0：handoff + evidence）
- 下一步：联调确认关键字写入 note 后进 `pending_test`
