# 企业评估 / 风险洞察 / 引育推荐 — V2 lumen 准生产实现设计规格

- 日期：2026-07-29
- 作者：human:孔东（前端 Lead）
- 关联任务：ENT-MOD-EVAL-V2-LUMEN、ENT-MOD-RISK-V2-LUMEN、ENT-MOD-RECRUIT-V2-LUMEN
- 目标仓：`lumen-ui-topic`（Vue 3 + Vite + Arco Design Vue + Pinia + Vue Router）
- 参考仓：`demo-ui-topic`（仅参考信息架构、交互流程、视觉；不复制 React/前端算分/localStorage 任务系统）
- 接口真源：`agent-handoffs/企业战略分析-ENT/API-ENT-full-catalog.md` #102~109、#113~121
- 必读基线：`agent-delivery/Design.md`、`agent-delivery/data-lineage-policy.md`、`agent-delivery/architecture-baseline.md`（D8/D9）

## 1. 范围与目标

在 `lumen-ui-topic` 实现企业评估、风险洞察、引育推荐三个模块页，与 V1 冻结基线 / demo-ui-topic 布局与字段对齐，可演示、可联调，保留评审模式与 Mock 双轨。

### 1.1 不做

- 不复制 demo 的 React 组件、Arco React import 结构
- 不在前端做业务算分、权重计算、排名排序（后端职责）
- 不建 localStorage 任务/模板/候选持久化（走 Java REST）
- 不建客户端 PDF 拼装
- 不碰 `package.json` / `vite.config.ts` / `tsconfig.json` 等配置文件

## 2. 架构边界

### 2.1 工程真源

`lumen-ui-topic` 框架为准：Vue 3.5 + TypeScript + Vite 7 + `@arco-design/web-vue` ^2.58 + Pinia 3 + Vue Router 5 + UnoCSS + Less + `--sci-*` token + ECharts + Leaflet。observability 走现有 `src/utils/observability.ts` + `request.ts` trace 深链。

### 2.2 数据流（统一）

```
Vue 页面 → composable → typed API → defineApi → 真实 Java REST / registerApiMock
```

- 真实请求：`defineApi({ real })` → `/api` 代理 → Java gateway
- Mock：`USE_MOCK=true` 时 `registerApiMock(id, fn)` 命中
- 页面禁止直接 import `@/mock`；正式页字段库走 `@/fixtures`
- 评审模式：`@/review` 的 `reviewMode` 控制 `MetricSpecCard`/`MockBadge`/`TraceInfoIcon`/`RoleLevelGate`；非评审隐藏

### 2.3 同仓并行边界（touched_files 独占）

| 任务 | 独占目录 | 共享文件（孔东统一维护） |
|------|----------|--------------------------|
| ENT-MOD-RISK-V2-LUMEN | `src/views/enterprise/EnterpriseRisk.vue` + `src/components/enterprise/risk/**` + `src/composables/useEnterpriseRisk.ts` + `src/config/enterpriseRisk.ts` + `src/mock/enterprise/riskInsight.ts` | `src/router/menu.ts`、`src/config/compareBasketDispatch.ts`、`src/config/enterpriseBreadcrumb.ts`、`src/composables/useCompareBasketDispatchContext.ts`、`src/mock/enterprise/searchBizApi.ts`、`src/mock/register.ts` |
| ENT-MOD-EVAL-V2-LUMEN | `src/views/enterprise/EnterpriseEvaluation.vue` + `src/components/enterprise/evaluation/**` + `src/composables/useEvalTask.ts` + `src/config/enterpriseEvaluation.ts` | 同上（由 RISK 任务统一接线） |
| ENT-MOD-RECRUIT-V2-LUMEN | `src/views/enterprise/EnterpriseRecruit.vue` + `src/components/enterprise/recruit/**` | 同上（由 RISK 任务统一接线） |

高冲突文件（`menu.ts`、`mock/register.ts`、`compareBasketDispatch.ts`）统一由孔东维护，曹丽影不修改。

## 3. 分工（3:1）

### 3.1 孔东（75%，3 份工作包）

| # | 工作包 | 说明 |
|---|--------|------|
| 1 | S1 共享底座 + 三模块 API/Mock/类型/composable 全量 | 路由注册 + 对比篮上下文 + dispatch 路径对齐 + mock/register 合并 + 评估 API/类型/Mock（#102~109、#113~121）+ 风险 API/Mock + 引育 API/类型/Mock/composable |
| 2 | S2 风险洞察全量 | 供应链图谱 + 痛难点诊断 + 四态/历史/画像联动 |
| 3 | S3 企业评估全量 | 配置页 + 过程/结果/历史页 |

### 3.2 曹丽影（25%，1 份工作包）

| # | 工作包 | 说明 |
|---|--------|------|
| 4 | S4 引育推荐全量 | 页面组装 + 工作台 + 候选工作台 + 详情 Drawer |

曹丽影只消费孔东 S1 提供的 `useRecruit.ts` typed composable/ViewModel，不接触 API/Mock 注册、路由菜单配置。验收直接使用三个主任务 DoD，不单设集成验收子任务。

## 4. 接口设计

### 4.1 企业评估（#102~109、#113~121）

| 分组 | 接口 | 用途 |
|------|------|------|
| 配置 | #113 行业、#114 指标树、#115 数据预检、#117~121 模板 CRUD | 配置页数据源 |
| 任务 | #102 创建、#104 详情、#107 取消、#108 运行中、#109 SSE | 任务生命周期 |
| 结果 | #105 资产指针、#106 下载资产、#116 双企对比 | 结果页 |
| 历史 | #103 分页列表 | 历史页 |

### 4.2 #106 特殊处理（用户口径）

`#106` 是报告/结果下载接口，**不 mock 数据**。Mock 模式下前端只展示下载过程的动态模拟（进度态 → 完成态），不构造结果 JSON 字段。真实模式下走 `defineApi({ real })` 下载。

### 4.3 Mock 规则（通用）

- 同一 `taskId` 在 #102/103/104/105/109 间字段自洽
- `targetParams.enterpriseCodes` 与 #115 输入一致
- 状态仅 `running/success/failed/cancelled`（无 pending）
- `#113 is_preview`、`#115 data_source=mock` 原样保留
- 模板接口保持 snake_case；任务接口保持 camelCase/兼容字段
- 不发明 `dimension_diff`/`dimensions`/`enterprises[]` 内部评分字段
- 不发明预检阈值

### 4.4 风险/引育

- 优先复用目标仓现有 `risk.ts`、`recommend.ts`、`compare.ts`
- 孔东提供稳定 typed composable；曹丽影只消费页面 ViewModel

## 5. 组件结构

> **工程纪律：禁止上帝文件。** demo-ui-topic 是原型参照，只复刻其交互/业务逻辑/样式/功能，不复制其文件结构。demo 原型存在大量上帝文件（`EnterpriseRecommendation.tsx` 1651 行、`EnterpriseEvaluationPage.tsx` 1050 行、`EnterpriseRiskInsightPage.tsx` 339 行），在 lumen-ui-topic 落地时必须按职责拆分。单 `.vue`/`.ts` 文件默认 ≤300 行；超过须在 handoff 说明理由；超过 500 行视为缺陷必须拆分。拆分原则：页面壳（路由+Tab+视图切换）独立、每个面板/工作台/Drawer 独立组件、业务逻辑全部提到 composable、纯展示子块再下沉一层。

### 5.1 共享

- `WorkbenchPageHeader` + `SectionPanel`：工作台页头/分区
- `useCompareBasketDispatchContext`：解析 `route.query`（`enterprise_org_ids[]`、`return_context_id`、`source`、`analysis_type`）+ 返回对比篮
- `@/review`：`MetricSpecCard`、`MockBadge`、`TraceInfoIcon`、`RoleLevelGate`

### 5.2 企业评估（孔东，`src/views/enterprise/EnterpriseEvaluation.vue` + `src/components/enterprise/evaluation/**` + `src/composables/useEvalTask.ts`）

- `EnterpriseEvaluation.vue`：路由壳 + 四视图切换（configuration/processing/result/history）
- `EvalConfigPanel.vue`：对象区 + 指标权重 + 模板 + 预检
- `EvalProcessingSteps.vue`：六阶段进度（#109 SSE）
- `EvalResultWorkspace.vue`：排名/雷达/对比/可信度
- `EvalHistoryTable.vue`：任务历史
- `useEvalTask.ts`：任务状态机 composable

### 5.3 风险洞察（孔东）

- `EnterpriseRisk.vue`：壳 + Tab（供应链/痛难点/最近分析）
- `SupplyChainInsightPanel.vue`：ECharts force graph、节点展开、关键/风险节点侧栏
- `PainPointsPanel.vue`：四维诊断、共性问题 Top5、严重度 Tag、受影响企业 Drawer
- `useEnterpriseRisk.ts`：状态机 composable

### 5.4 引育推荐（曹丽影，`src/views/enterprise/EnterpriseRecruit.vue` + `src/components/enterprise/recruit/**`）

- `EnterpriseRecruit.vue`：壳 + 双层 Tab（招引/培育 × 筛选/候选）
- `RecruitWorkbench.vue`：筛选条件/权重/结果排名/区域分布
- `CandidatePanel.vue`：候选工作台
- `RecruitDetailDrawer.vue`：维度证据/核心优势/风险信用/政策方向
- `useRecruit.ts`：状态机 composable（由孔东提供接口，曹丽影消费；位于 `src/composables/useRecruit.ts`）

## 6. 状态覆盖

### 6.1 四视图（统一）

configuration → processing → result → history

### 6.2 结果态

success / empty / partial / error / permission

### 6.3 评审模式

reviewMode 控制 TraceInfoIcon / MetricSpecCard / MockBadge；非评审隐藏。

### 6.4 引育额外

- 招引/培育切换
- 筛选推荐/候选工作台切换
- analysisState：initial/loading/success/empty/partial/error/permission

## 7. 异常处理

- API 错误统一走 `request.ts` 拦截；页面按状态映射到 error/permission 态
- 任务失败：`status=failed` + `errorMsg`；SSE 断线走 #108 重连
- 预检不通过：`ready=false`，展示 `missing_codes` 和 `overall_confidence`
- 归属/权限失败：映射到 permission 态
- #106 下载失败：展示错误态，不回退到 mock 数据

## 8. 测试与验收

- `npm run build` + `npm run type-check` 绿
- `npm run lint` 通过
- 对比篮 → 模块页 → 返回对比篮闭环
- `USE_MOCK=true/false` 双路径可演示
- K8s dev URL 可访问（NodePort 30892）
- 评审模式指标卡/MockBadge 可见
- 每个统计数字配 `metricId` + 评审态 `MetricSpecCard`
- Mock 指标带 🧪 MockBadge
- 会签单签字 + lumen commit SHA + K8s/dev URL

## 9. 开放项

| 项 | 说明 | 处理 |
|----|------|------|
| #106 结果 JSON 嵌套结构 | catalog 未展开 enterprises[]/summary | 不 mock 数据；下载动态模拟；真实结构待 Java/Python DTO 核对后补 |
| #113 items[] schema | 完整字段未定义 | mock 用 catalog 示例字段，不扩展 |
| #114 dimensions/groups | 嵌套结构未展开 | mock 返回 1 层占位，不填指标 key |
| #115 per_enterprise[] | 元素结构未定义 | mock 不填充，标 🟡 |
| #116 dimension_diff[] | 元素结构未定义 | mock 返回空或 2-3 条占位，不定义维度 key |
| 评估模板 industry vs industry_code | 命名 🟡 | 保持 catalog 原样，不擅自改名 |
| 预检阈值 | catalog 未定义 | mock 不做业务判断，标 🟡 |
