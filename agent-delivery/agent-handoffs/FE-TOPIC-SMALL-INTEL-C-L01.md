# FE-TOPIC-SMALL-INTEL-C-L01 · 要素/协同工作台小屏落地 · handoff

- **状态**：integration（联调确认中）
- **执行**：[agent:frontend-agent] · 监管：human:孔东
- **仓**：`lumen-ui-topic-mobile` · commit `f064125`（dev，已推送 `4c90848..f064125`）
- **PC 真源**：`lumen-ui-topic` ElementsWorkbenchView / CollabWorkbenchView
- **日期**：2026-11-17

## 1. 范围与实现（对照 PC）

| PC 能力 | 小屏实现 | 文件 |
|---|---|---|
| 要素五透镜（综合/类型/层次/领域/全景136） | `van-tabs` 五透镜，全景缺数 reason 披露（禁编数） | `IntelElementsView.vue` |
| 要素三指数 + 四维过渡打分 + 贡献路径 | 三指数卡 + 过渡打分（pending_registration 声明）+ 非因果归因说明（Q-SYNTH-E-02） | 同上 |
| 协同四 KPI（指数/完整度/中心度/密度） | null 容忍渲染（缺数显 `—`） | `IntelCollabView.vue` |
| 协同图谱（kind 过滤 + 节点选中） | G6 v5 force 布局 + kind chips 过滤叠加 + tap 选中底部信息条 | `IntelCollabGraph.vue` + `IntelCollabView.vue` |
| 中心度 Top / 孤立主体 / 横向排名 / 四线趋势 | ListCard 竖排 + ECharts 四线趋势 | `IntelCollabView.vue` |
| 关联散点（协同→联合专利） | 样本 < 3 不出系数、不下有效关联结论（Q-SYNTH-C-03）；仅描述关联非因果 | 同上 |
| clusters / strategies LLM 降级 | clusters 恒空 + `clustersReason`（cluster_rule_unclosed）披露；策略 LLM 不可用话术 + 须人工审核 | 同上 |
| 路由专属化 | `/intelligence/elements`、`/intelligence/collaboration` 由过渡期复用活力页改为专属视图 | `src/router/index.ts` |

## 2. 复用与零重复

- 四结果态（instant/task/config/no_batch）复用批次 B 的 `useIntelResultSource` + `ChainAnalysisShell`（I2-12 闸门）。
- 类型与 Mock 种子复用批次 A 的 `intelMockSeed.ts` / `intelMockData.ts`，未新增数据面。
- 图谱事件/降载模式与仓内 `PolicyPortalChainGraph` / `ChainPanoramaGraph` 同款（animation:false、token 防竞态、ResizeObserver）。

## 3. 偏离说明

- 小屏无悬浮面板：节点选中改为底部信息条（移动交互习惯）；kinds 过滤叠加显示（PC 为侧栏多选）。
- 关联散点 N<3 时不渲染图只出文案（PC 同语义，展示形态从表格改文案行）。

## 4. 验收证据

- 质量门：`npm run type-check` ✅ / `npm test` 85/85 ✅ / `npm run build` ✅（chunk 警告为仓既有，非本批次引入）
- 产物清单：`IntelElementsView.vue`（~600 行）、`IntelCollabView.vue`（~450 行）、`IntelCollabGraph.vue`（~170 行）、路由映射
- 联调确认：Mock 默认三元组（深圳×全国重点城市×最近3年）秒开；非默认组合 no_batch 引导发起分析（USE_MOCK=true 本地验证语义）

## 5. 架构合规自检（§2 铁律）

- ✅ 调用链：前端 → Java REST（synthBatch / analysisTask），未越层
- ✅ D9：每个统计数字有 metric-id（M_SYNTH_ELEM_* / M_SYNTH_COLLAB_*），null 不补 0；Mock 态 🧪 角标（review 层 StatCard 内建）
- ✅ D12：未引 demo-* 任何代码/服务；对照 PC 只读重写
- ✅ I2-12 / 附录 E：切条件不自动 create；闸门走 Shell；复用/重跑语义与 PC 同
- ✅ USE_MOCK=false 时 fixture 零参与（mock 面仅 main.ts 动态加载）
- ✅ 诚实性：clusters/strategies/全景缺数全部 reason 披露，不编数

## 6. cost 回填

- actual_tokens: ~150k · model_used: glm-5.3 · actual_cost: ~$0.9 · cost_warn: false

ponytail: full（复用既有组件/composable 优先，无新依赖，无新抽象）
