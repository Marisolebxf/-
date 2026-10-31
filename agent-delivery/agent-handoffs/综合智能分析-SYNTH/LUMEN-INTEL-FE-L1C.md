# LUMEN-INTEL-FE-L1C — 三叶共享件（IntelMetricMount/MissingDefBadge 复用/SynthContextBar/menu 指向）

- 任务：LUMEN-INTEL-FE-L1C（E8-综合智能分析 / implementation / P0 / lumen-ui-topic）
- 强度：ponytail full
- 状态：in_progress → 待走查
- commit：lumen-ui-topic dev `4c87b38`（已推 dev）
- 监管人：human:孔东
- 背景：三叶页面任务（VIT/ELEM/COLLAB）worktree 并行的前置微单，消除共享文件冲突

## 1. 范围与实现（对照 DoD）

### DoD-1 IntelMetricMount.vue
`views/intelligence/components/IntelMetricMount.vue`：
- 组合 `MetricSpecCard`（ⓘ/D1-missing 红问号 + draft pending_ref 文案）+ **draft 右上橙点**（6px #FF7D00，demo 同款）+ `ReviewMetricBadges`（结构/⚠️/🧪/⟳ 总装）
- 评审自闸复用 `ReviewMetricBadges` 内部 `isReviewFeatureEnabled() && reviewMode`，组件不重复实现门控；关闭评审 DOM 零渲染
- `batchHint` prop：Mock source 覆盖为「跑批预计算」（demo batchHint 同款）
- **MissingDefBadge 不新建**：lumen `MetricSpecCard.isUnregistered` 路径已覆盖 demo MissingDefBadge 全部语义（红问号 + 治理引用 + 不显伪 8 件套）——ponytail 复用而非复制

### DoD-2 SynthContextBar.vue
`views/intelligence/components/SynthContextBar.vue`：
- 目标区域(160px)/对比范围(180px)/时间窗(140px) 三联 a-select（demo 同尺寸）
- 系统默认/已改条件 Tag + 非默认时「恢复默认」按钮
- `useSynthCtx` 接线（URL 真源 + localStorage `topic-synth-workbench` 持久化 + 无关 query 参数保留）
- `actions` slot：右侧动作区（指标与方法说明/分析记录/开始分析由各叶工作台填）
- `change` 事件：条件变更通知父页（清 taskId/mode 由父页按 demo patchCtx 语义处理）

### DoD-3 menu 占位收口
`IntelWorkbenchPlaceholder.vue` + `menu.ts` 三叶 `component` 指向：
- 三叶菜单从 DevelopingView 切到占位页（含共享条件栏可用预览 + 三单标注）
- VIT/ELEM/COLLAB 各自替换 `component` 指向为终页，menu.ts 冲突面收敛为各自 1 行

### DoD-4 自检
`intelL1c.selfcheck.mjs`：共享件结构断言 + 评审自闸（无 v-if="true"）+ menu 三处指向 + intel seed fallback 通

## 2. 产物清单

| 文件 | 类型 |
|---|---|
| `src/views/intelligence/components/IntelMetricMount.vue` | A |
| `src/views/intelligence/components/SynthContextBar.vue` | A |
| `src/views/intelligence/IntelWorkbenchPlaceholder.vue` | A |
| `src/router/menu.ts` | M（三叶 +component） |
| `src/mock/intel/intelL1c.selfcheck.mjs` | A |

## 3. 验收证据

- `pnpm type-check` ✅ / `eslint src/views/intelligence` ✅ / `intelL1c.selfcheck.mjs` ✅
- 已推 origin/dev `6a60ef6..4c87b38`（CI 触发）

## 4. 架构合规

- ✅ D8：Arco select/tag/button + sci token 变量，无新 UI 体系
- ✅ D9：角标只读消费 seed（getIntelMetricMeta/getSynthMetricReadiness L1 已挂全局 fallback），无前端改绿
- ✅ D10：select 键盘可达（Arco 原生）
- ✅ 评审零泄漏：ReviewMetricBadges 自闸 + REVIEW_FEATURE.enabled 单点清理

## 5. 三单并行指引（VIT/ELEM/COLLAB）

1. worktree 分支 `intel/fe-vit|elem|collab` rebase 到 `origin/dev`（含 4c87b38）
2. 各自替换 menu.ts 中本叶 `component: () => import('@/views/intelligence/IntelWorkbenchPlaceholder.vue')` → 终页（只动自己那行，无交叉）
3. 共享件从 `@/views/intelligence/components/` 导入；角标/条件栏禁止内联重写
4. 过程页/记录面板复用 L1B 桥（`useSynthTaskBridge`）+ `SynthAnalysisRecordsPanel`

## 6. cost 回填

- actual_tokens: ~35k / model_used: glm-5.3 / actual_cost: ~$0.5 / cost_warn: false

ponytail: full
