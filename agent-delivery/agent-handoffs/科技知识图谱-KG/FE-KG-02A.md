# FE-KG-02A · 指标展示 — 整页复刻（告警条+KPI+3 Tab 十五叶）

> demo 真源：`repos/demo-ui-science/src/pages/tech-knowledge-graph/IndicatorDisplay.jsx`(165) + `BlacklistTriggerPanel.jsx`(16KB) + `FusionIndicatorsPanel.jsx`(15KB) + `OptimizeDecisionPanel.jsx`(17KB) + `fusionMetrics.js`/`decisionModel.js` + 3 selfcheck

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（4h 锁，2026-11-05 10:49 起） |
| 说明 | 认领时依赖 FE-KG-S01 为 `integration`（与 FE-KG-01A 认领时同款情形：基座三绿+浏览器验证过，mock/api/样式可用）；开工前核对 01A handoff 踩坑记录（4 轮走查沉淀） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D8 token / D9 ⓘ🧪 / 可观测埋点 / 架构铁律。算法层按规划 D1「照 demo 前端演示 + 🧪」，demo 源随机函数改确定性 LCG（见修改内容 1） |

## FE-KG-01A 踩坑对照（本单开工依据）

开工前通读 01A handoff 4 轮走查记录，本单预先规避：

1. **PageTabFrame 保留判定**：01A 被去掉的是「单占位页签无切换语义」；本页 demo WorkbenchTabs 是真 3 Tab → **保留 PageTabFrame**（selfcheck §7 同口径）
2. **禁 Math.random/Date.now**：demo `decisionModel.js` 用 `Math.random()`/`Date.now()` 生成训练扰动与 id → 本单移植为 `_dmSeed` 确定性 LCG + `_trainSeq` 会话序号 + 冻结演示时间戳（种子 2026-05-20 语境），自检断言 models 文件零字面量
3. **图标显式 import + 正确图标名**：Arco 图标库无 `IconAudit`/`IconAlert`/`IconLineChart`/`IconMerge`（type-check 必红）→ 先查 `@arco-design/web-vue/es/icon/index.js` 实际导出再写（本单映射：IconRecord/IconExclamation/IconBarChart/IconApps）
4. **卡头/Tab 去装饰图标**：01A 第 4 轮走查要求卡头标题纯文字 → 本单卡头均不挂装饰图标（~~Tab 前置图标保留~~ → 2026-11-05 第 2 轮走查升级：Tab 标题同样去图标，见文末走查记录）
5. **a-progress 0-1**：antd 0-100 → Arco percent 需 /100 换算，自检断言禁止直接用 0-100 值
6. **横向滚动条**：洞察卡位移教训 → 本单布局用 grid/flex 定宽，目检 `bodyScrollX=false`
7. **全局滚动条**：S01 基座 main.css 已有 4px 细蓝条全局规则，本页继承不另写

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 问题清单

- 无阻塞。metric 正名沿用 S01/01A 盘点口径（见 D9 节）

## 修改内容

**仓：`repos/lumen-ui-science-pc`（dev，完工停本地工作区等孔东人工验收，未 commit/push）**

1. **算法层移植**（`src/views/knowledge-graph/models/`）：
   - `fusionMetrics.ts`：`normalizeMetricValue`/`recomputeFusionValue`/`applyScenarioWeights`/`normalizeWeights`/`checkConsistency`/`scoreEvalObjects`/`buildCorrelationMatrix`，demo 语义逐行冻结 + TS 化（interface FusionIndicator/CorrelationPair/ConsistencyIssue/FusionEvalObject）
   - `decisionModel.ts`：`bumpDynamicMetrics`/`runAutoTrain`/`applyFeedbackLoop`/`summarizeRiskDetection` + `demoNowDate(DemoNowDateTime)` 演示时间戳；**demo 源随机函数 → `_dmSeed` 确定性 LCG、时间戳 id → `_trainSeq` 会话序号、new Date → 冻结日期**（铁律禁随机，同输入同输出，演示语义不变）
2. **黑名单触发面板**（`components/KgBlacklistPanel.vue`）：§408 监测指标卡 ×4（阈值着色）→ §410 触发记录表（风险等级 Tag/异常度/规则/自动入黑/关联节点 Badge/状态/详情）+ 选中行联动 + 右侧风险链条 a-timeline（首节点红）+ 自动入黑/联动通知统计 +「模拟规则入黑+联动」按钮（写操作会话级演示态 D3：600ms 后追加库/通知/审计三件）→ 内嵌 4 子 Tab：§409 专家规则库 / 黑名单库 / §411 通知联动（选中事件高亮+计数）/ §412 审计日志 Timeline（自动入黑红/解除绿）
3. **融合统计指标面板**（`components/KgFusionPanel.vue`）：§413 指标整合表（三源值着色+融合值 Progress+趋势 Tag）+ 场景预设 a-select（4 预设冻结）+ 来源筛选 → §414 权重配置（三源 a-slider + 指标权重 a-slider + 合计校验红字 + 归一化）→ 底部 4 子 Tab：§415 相关性（ECharts heatmap 5×5 + visualMap 色带 + Top6 相关对 + 范围 a-slider）/ §416 一致性检验（a-alert 三色）/ §417 综合评分（权重实时重算+等级 Tag）/ 趋势双轴折线
4. **优化决策模型面板**（`components/KgDecisionPanel.vue`）：§418 头部操作条（自适应 a-switch + 接入数据 + 自动训练）+ 动态指标卡 ×4（↗ delta）→ 左列模型优化历程 a-timeline + §419 专家规则联合 a-list → 右列 §420 性能四 Progress（准确率/召回率/F1/延迟）+ 算法切换 a-select（4 算法）+ 训练折线 + 重训/调权按钮 → 底部 3 子 Tab：训练历史表 / §421 风险预警（统计四格+风险表 Progress 红档）/ §422 反馈闭环（a-rate + 应用反馈优化）
5. **整页**（`indicators/index.vue`，重写 S01 页壳）：
   - PageTabFrame 真 3 Tab（demo WorkbenchTabs 三 key：blacklist/indicators/optimization，Tab 前置图标）
   - #header：KgPageHeader + 告警条 ×3（demo 冻结文案）+ KPI 四卡（demo 冻结值，ⓘ 占位 metric_id ×4 + 🧪 评审态）
   - 黑名单详情抽屉：InsightDetailDrawer map-object 三段（图谱监测指标/规则判别/自动拦截与联动）+ metricCards（风险评分/异常度/关联节点）
   - 双轨 fetch（mock 种子 → contractPending 网关占位）
6. **类型**（`models/kgTypes.ts`）：补指标页契约类型（BlacklistTrigger/BlacklistGraphMetric/BlacklistExpertRule/BlacklistLibraryEntry/BlacklistNotification/BlacklistAuditLog/FusionScenarioPreset）
7. **自检**（`indicators/FE-KG-02A.test.mjs`）：demo 三份 selfcheck（fusionMetrics/decisionModel/blacklistTrigger）断言语义摘选移植 + 02A 接线组（三面板挂接/PageTabFrame 保留判定/KPI ⓘ/告警冻结文案/抽屉三段/Arco 全替换/a-progress 0-1/图标显式 import 逐文件校验/禁随机时间）；`node --experimental-strip-types` 直跑 models+seed

## 测试结果（三绿 + 浏览器目检）

- `pnpm type-check`（vue-tsc --build）：**0 错**
- `node src/views/knowledge-graph/indicators/FE-KG-02A.test.mjs`：**5 组全绿**
- `node src/views/knowledge-graph/kg.selfcheck.mjs`（S01 基座防回归）：**全绿（9 组）**
- `node src/views/knowledge-graph/analysis/FE-KG-01A.test.mjs`（01A 防回归）：**全绿（5 组）**
- `pnpm build`：**绿**（30.4s，无本页相关告警；KnowledgeGraphCanvas 大 chunk 为 echarts 全量注册存量）
- 浏览器目检（dev :3000 `/graph/graph-indicators`，admin 已登录态）：
  - 标题「指标展示」；3 Tab 文案齐（黑名单触发/融合统计指标和模型特征/优化决策模型）
  - KPI 4 卡 = 3个/5项/92.8%/156件（demo 冻结值）；ⓘ ×4（占位 M_KG_IND_*）；评审态 `lumen-review-mode=1` 下 🧪「演示数据」Tag ×4
  - 告警条 ×3；黑名单 Tab：监测指标卡 ×4 + 触发表（详情按钮 ×5）+ 4 子 Tab
  - 融合 Tab：a-slider ×9（三源 3 + 指标 5 + 范围 1）、heatmap canvas、表格 13 行
  - 决策 Tab：动态指标卡 ×4、a-switch ×1、Timeline、训练折线 canvas、3 子 Tab（模型自动迭代/风险识别优化/决策反馈闭环）
  - 详情抽屉打开：三段（图谱监测指标/规则判别/自动拦截与联动）+ metricCards 渲染正常，关闭正常
  - `bodyScrollX=false`（无横向滚动条）
  - 截图：`page-2026-11-05T03-03-11-406Z.png`（黑名单 Tab）/ `page-2026-11-05T03-04-02-884Z.png`（决策 Tab）/ `page-2026-11-05T03-04-53-348Z.png`（详情抽屉）（本机 Temp cursor/screenshots/）

## D9 数据血缘（按 data-lineage-policy §2.3 执行契约）

- KPI 四卡 ⓘ：KgKpiCard `metricId` 占位（`M_KG_IND_ACTIVE_ALERTS` / `M_KG_IND_FUSION_COUNT` / `M_KG_IND_MODEL_ACC` / `M_KG_IND_HANDLED_EVENTS`，**均占位未入 metric-registry，待 data-agent 正名**；对齐方向见 types/knowledgeGraph.ts 注释——活跃告警语义近邻 `M_SCIUI_KGANALY_043`）
- 融合面板头 MetricSpecHint：`M_KG_IND_FUSION_COUNT`（同上占位）
- 🧪 MockBadge：KPI 卡自带（评审层门控，默认关闭零泄漏）；融合面板头 + 决策模型头各 1（评审态显示）
- 不伪闭合：训练/入黑/反馈等写操作均为会话级演示态（D3），Message 明示演示语义；算法层为前端规则模拟（规划 D1 拍板「演示 + 🧪」）

## 架构合规自检（公约 §2 逐条）

- ✅ 调用链：前端不直连图谱服务/不感知 nGQL；数据经 api/knowledgeGraph.ts 双轨（mock/网关占位 contractPending）
- ✅ D8：Arco 全替换（Table/Tag/Badge count/Timeline/Statistic→小卡/Select/Slider/Switch/Rate/List/Alert/Tabs/Progress 0-1/Message）；token 走 CHART_BASE + 主色 #165dff；卡头与 Tab 标题纯文字无装饰图标（01A 第 4 轮 + 02A 第 2 轮走查口径）
- ✅ D12：零 demo 仓依赖；mock 种子 S01 已冻结（selfcheck §2 逐行校验仍绿）
- ✅ 图谱铁律：heatmap/line 走 echarts.ts 注册（HeatmapChart/VisualMapComponent 在册），未引新链路
- ✅ 可观测：trackKgInteraction 埋点（page-mounted/simulate-auto-block/blacklist-detail-open/fusion-scenario-apply/fusion-weights-normalize/decision-ingest-data/decision-auto-train/decision-apply-feedback）
- ✅ 互斥 display 不叠同一节点（三 Tab 面板 v-if 切换；selfcheck 断言）

## 遗留风险

- metric_id 占位正名（`M_KG_IND_*` 4 条 + KbFusion 面板 1 条复用）待 data-agent 入 registry（与 S01 `M_KG_SVC_*`、01A `M_KG_ANALY_*` 同批）
- decisionModel 确定性 LCG 与 demo 随机函数数值不同源——demo 侧 selfcheck 只断言语义（≥基线/状态位），本单自检同语义全绿；真算接入后由 BE-KG-CONTRACT-01 换数据源
- 融合面板「指标权重」slider max=50（demo 同款 0–0.5 权重域），合计≠100% 时红字提示（demo 同语义），归一化按钮兜底
- 训练时间戳用冻结演示日期（2026-05-20 语境）——真机联调时若走 BE 时间轴需对齐（契约单登记）

## CI/CD

- 分支：`dev`（lumen-ui-science-pc）——**未 commit/push**（孔东监管限定 2026-11-04：supervised_by human:孔东 的任务完工停本地工作区等人工确认，AGENTS.md 仓级裁定优先于「完工即推」）
- 待孔东验收放行后：commit（`[agent:frontend-agent]` 标注）+ push `origin/dev` 触发 CI

## 2026-11-05 孔东走查调整（第 1 轮，任务仍处 integration 停本地）

- **表格状态列颜色 Tag 修复**：走查发现黑名单面板表格状态列（启用/拦截中/已送达等）显示纯文本。根因 = 写了 `<template #xxx>` 列插槽但 column 定义漏 `slotName` 声明——Arco 表格只有声明 `slotName` 的列才走插槽渲染，否则按 `dataIndex` 纯文本输出。**一次修三面板 8 张表**（触发表 riskScore/autoBlockedLabel/relatedNodes/statusLabel、专家规则 enabledLabel、黑名单库 sourceLabel/statusLabel、通知 statusLabel、融合整合表 name/graphValue/ruleValue/modelValue/fusionValue/trend、评分表 type/score/level、训练历史 statusLabel、风险表 type/score/signals/status）
- **防回归断言**：FE-KG-02A.test.mjs 新增「列插槽（`<template #xxx="{ record }">`）必须在 column 声明 slotName」静态校验（只匹配带 `{ record }` 解构的表格列插槽，不误伤 #title/#extra 卡头插槽）
- 验证：三绿复跑全过（type-check 0 错 / 02A 自检含新断言 / kg.selfcheck 9 组 / build 31.6s 绿）；CDP 复验 Tag/Badge/Progress 全生效：黑名单 Tab `.arco-tag` 0→**42**、`.arco-badge` 0→**5**，融合表 Tag **22** + Progress **11**，风险表 Tag **20** + Progress **4**；截图 `page-2026-11-05T03-14-48-158Z.png`（风险预警 Tab 红档 Tag + Progress 条确认）
- **此坑沉淀**（复刻新通用规则）：Arco `a-table` 列要自定义渲染（Tag/Progress/着色）时，column 必须声明 `slotName` 且模板插槽名一致；只写插槽不声明 = 静默退化纯文本（不报错、type-check 也不拦）。建议追加到 `TS-demo-lumen复刻经验清单.md` §1（本 handoff 已记录，待 doc-agent 汇编时收录）

## 2026-11-05 孔东走查调整（第 2 轮，任务仍处 integration 停本地）

- **tabs/card 标题去图标**：走查指认顶部 Tab（黑名单触发）、融合子 Tab（综合评分）、卡头（权重配置）三处样例，要求 Tab/卡头标题全部纯文字。本单开工时按 01A 第 4 轮口径只清了卡头、保留了 Tab 前置图标——本轮口径升级为 **Tab 标题同样不挂图标**（含 PageTabFrame 顶部 Tab + 三面板全部内嵌子 Tab）
- **改动**：`index.vue` TABS 数组去 `icon` 字段及 icon import；`KgBlacklistPanel.vue` 4 子 Tab（IconSafe/IconApps/IconLink/IconRecord）；`KgFusionPanel.vue` 卡头 IconSettings + 2 子 Tab（IconCheckCircle/IconTrophy）；`KgDecisionPanel.vue` 卡头 IconExperiment + 2 子 Tab（IconExclamation/IconMessage）；各自清理未用 import。**按钮内图标保留**（归一化 IconSync、训练 IconThunderbolt 等，非标题类）
- 验证：三绿复跑全过（02A 自检 / type-check / build 29.4s）；CDP 全量断言 `hasSvg:false` —— 顶部 3 Tab、黑名单 4 子 Tab、融合 4 子 Tab、决策 3 子 Tab、决策面板 4 卡头、权重配置卡头；截图 `page-2026-11-05T03-21-35-309Z.png`（决策 Tab）+ `page-2026-11-05T03-22-00-100Z.png`（融合 Tab）
- **经验沉淀**：Tab/卡头标题统一纯文字，demo 源带的前置装饰图标不复刻（01A 第 4 轮卡头口径 + 02A 第 2 轮 Tab 口径合并）；下次复刻开工即按此口径免走查返工

## 签收与推送（2026-11-05）

- **人工走查放行**：human:孔东 2026-11-05 11:26 走查通过，明示「可以 commit、push dev」
- 前端仓提交：`lumen-ui-science-pc@dev` `14afb54`（8 文件，+2539/-20；只含 FE-KG-02A 产物，`.env.development` 本地改动非本任务产物未纳入）
- CI 将按公约触发 K8s dev rollout

## 涉及文件

- `src/views/knowledge-graph/indicators/index.vue`（重写，S01 页壳 → 整页）
- `src/views/knowledge-graph/indicators/FE-KG-02A.test.mjs`（新增）
- `src/views/knowledge-graph/components/KgBlacklistPanel.vue`（新增）
- `src/views/knowledge-graph/components/KgFusionPanel.vue`（新增）
- `src/views/knowledge-graph/components/KgDecisionPanel.vue`（新增）
- `src/views/knowledge-graph/models/fusionMetrics.ts`（新增）
- `src/views/knowledge-graph/models/decisionModel.ts`（新增）
- `src/views/knowledge-graph/models/kgTypes.ts`（补指标页类型）

---

- actual_tokens ≈ 150k（读 demo 真源 4 件 + 01A 踩坑 handoff + 基座核对 + 实现 + 三绿 + CDP 目检）
- model_used：glm-5.3（Cursor agent 会话）
- actual_cost ≈ $2.1；cost_warn：否
