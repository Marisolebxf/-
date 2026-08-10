# SYNTH-MOD-COLLAB-V1-HIFI · handoff

## 认领信息

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:ui-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | pull（会签后已 claimed → 开工改 agent 认领） |
| status | `in_progress` → 待转 `pending_test` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |

## 范围与实现

- **仓**：`demo-ui-topic` · `/intelligence/collaboration` + `/intelligence/collaboration/tasks/:taskId`
- **对齐**：Pack1 五件套 + 派单包（完整度/中心度/密度/协同指数 · 指标·方法·结果显性 · 默认秒开 · 协同五阶段）
- **共享上下文**：`src/app/intelligence/synthCtx.ts`（`topic-synth-workbench`，默认深圳×全国重点城市×最近3年）
- **未做**：METRIC-OPEN 正式闭合、真实 Java 任务总线、PDR-G1、F-COLLAB-04 完整主体详情 Drawer（仅 `node=` 高亮）、活力页改造

## 产物清单

| 路径 | 说明 |
| --- | --- |
| `src/app/pages/intelligence/RegionalInnovationCollaboration.tsx` | F-COLLAB-01 工作台（重写） |
| `src/app/intelligence/CollabAnalysisTaskPage.tsx` | F-COLLAB-02 过程页 |
| `src/app/intelligence/CollabMethodDrawer.tsx` | F-COLLAB-03 方法抽屉 |
| `src/app/intelligence/collabMock.ts` | 跑批/任务 Mock 结果 |
| `src/app/intelligence/collabMetricSeed.ts` | M_SYNTH_COLLAB_* |
| `src/app/intelligence/collabTasks.ts` | 本叶 mock 任务总线（`region_innovation_collaboration`） |
| `src/app/intelligence/collab.selfcheck.mjs` | 默认值/五阶段自检 |
| `src/app/routes.tsx` | 增加 `collaboration/tasks/:taskId` |

## 验收证据

- 默认三元组秒开结果面（不进过程页）；改条件后「开始分析」进 F-COLLAB-02 协同五阶段（无产业链四力/活力四维/要素四模型文案）
- 结果面同页：协同指数、完整度、中心度/密度、关系输入、图谱边表+子图统计、集群/孤立、对比/趋势、效果评估诚实空态、优势不足与待审核策略
- 方法抽屉明确禁止「密度×强度」权威化；INDEX / OUTPUT_CORR 为 D1 missing 红问号
- `node src/app/intelligence/collab.selfcheck.mjs` → ok
- `npm run build` → **通过**（built in ~65s）

## 仓状态备注

- 工作区曾处于 **ELEMENT V1-HIFI rebase in progress**（`dev` onto `e07eb30`）；冲突文件已 `git add` 标为解决，**未执行** `rebase --continue` / 本单 commit / push（待监管人确认，避免误提交 ELEMENT 补丁）
- 本单代码已落盘；push `origin/main` 需先结束 rebase 或按仓策略切到可推送分支

## 架构合规自检

| # | 铁律 | 结论 |
|---|------|------|
| 1–2 | 算法/调用链 | ✅ 前端仅 Mock/展示；不直连 Python |
| 4 | 可观测 | ✅ `track('synth_collab_*')` |
| 6 | demo 仓 | ✅ 只改 `demo-ui-topic` |
| 9–11 | D8/D9/D10 | ✅ Arco + 角标 + 过程双卡/无百分比 |

## Cost 四字段

| 字段 | 值 |
|------|-----|
| actual_tokens | ~240000（估） |
| model_used | Cursor Grok 4.5 |
| actual_cost | ~$3.2（估） |
| cost_warn | green |

## 下一步

1. 监管人确认后：结束 ELEMENT rebase → commit COLLAB → push（demo 仓约定分支）
2. 浏览器走查默认秒开 / 改条件过程 / 方法抽屉
3. QA 领取 `pending_test`
4. METRIC-OPEN 闭合后回刷角标文案
