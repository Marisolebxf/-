# LUMEN-INTEL-FE-COLLAB — 协同分析三页复刻（图谱/关联散点/集群/策略）

- 任务：LUMEN-INTEL-FE-COLLAB（E8-综合智能分析 / implementation / P0 / lumen-ui-topic）
- 强度：ponytail full
- 状态：in_progress → **停本地待人工走查**（2026-10-20 闸门：严禁自动 push）
- commit：worktree `worktrees/lumen-ui-topic--intel-collab` 分支 `intel/fe-collab` `4586be4`（未推）
- 监管人：human:孔东
- 源：demo `RegionalInnovationCollaboration.tsx` + `CollabAnalysisTaskPage.tsx` + `CollabReportPage.tsx` + `CollabMethodDrawer.tsx`

## 1. 范围与实现（对照 DoD）

### DoD-1 协同工作台（CollabWorkbenchView.vue，menu:topic:intel:collab → 终页）
- **四结果态**：`instant`（默认三元组+跑批秒开，`getCollabBatchSnapshot`）/ `result_task`（#105 任务快照，`getCollabTaskResult`）/ `dirty`（已改条件）/ `no_batch`（默认但无跑批）——判定对齐 demo showTaskResult/showInstant 语义，URL `view=result|config` + `task_id` 驱动
- **协同指数仪表盘**（ECharts gauge #165DFF）+ vs均值/同比 + 「演示态合成；正式权重与历史校准未闭合」诚实文案
- **网络完整度 / 中心度 / 密度卡**（三指标 ×100 显示，全部 IntelMetricMount 挂载）
- **合作关系输入构成**：三数字卡（联合专利/合作项目/人才流动）+ 横向条形图
- **创新主体关系图谱**（ECharts graph force layout）：主体类型×5 / 关系类型×3 Checkbox 过滤、中心主体 TOP 点击高亮（节点描边+关联边 #165DFF）、**子图统计**（节点/边/完整度/中心度/密度，与全网指标区分标注）、孤立主体表**点击高亮**联动
- **集群表**（score=null 显 note 诚实态「集群分挂 Q-SYNTH-C-02，演示态不伪造权威分」）+ 孤立主体/低连接表
- **横向对比表**：点击其他区域切 `region` 并进 `view=config`（不自动起任务，E.3）；**纵向四线趋势**（协同指数/完整度×100/中心度×100/密度×100）
- **关联散点三分支**：`ok`（系数+散点）/ `insufficient`（样本<3 门槛 3 警示，不出系数不画图）/ `none`（无演示序列警示）；文案「演示关联散点；正式方法待甲方确认（Q-SYNTH-C-03）。禁止因果表述」
- **策略建议表**：审核态 Tag（已审核 green / 待审核 orangered）+「策略不自动发布；正式优化路径待 Q-SYNTH-C-04」+ methodDigest 链
- 三叶互跳（活力/要素带 ctx query）；「开始分析」走 `startOrResumeSynthAnalysis` 四决策（E.4 单飞/E.5 当天复用）；切回工作台 `resolveSynthWorkbenchRestore` 恢复
- Tab：协同分析 / 分析记录（`SynthAnalysisRecordsPanel`，#103 按叶过滤）
- 埋点：仓内 observability 惯例为 request 层 traceparent（`utils/request.ts`）+ 无独立 track 库 → 交互埋点以 data 属性 + 评审层覆盖，未另造埋点框架（对齐总纲 §1.1「仓内 observability 埋点方案对齐现有 views 惯例」，现有 views 无 track() 调用）

### DoD-2 关联散点（Pearson 诚实态）
- `COLLAB_CORR_SERIES` **从 `@/mock/intel/collabMock` 取**（L1 已随迁，本叶零新增 mock 数据）；pearson/门槛 3/两态警示逻辑在 mock 层（L1 已交付，selfcheck 断言 12 个年份点齐全）
- UI 三分支逐字对齐 demo 文案；禁因果表述

### DoD-3 过程页（CollabAnalysisTaskPage.vue）
- 双卡片（SectionPanel）：任务卡（ID/类型/对象冻结三段/已用秒）+ 过程卡（**协同五阶段** a-steps vertical）
- 数据 = #104/#105 poll（1.5s `useIntelTaskPageHydrate`，`collabTaskPageShared.ts` 导出，VIT/ELEM 可复用）；EVENTS 空显「不编造协同阶段」空态
- **完成停 wait_view 不自动跳**（「查看分析结果」回工作台 `view=result`）；排队**可撤回**（#107 cancel）；失败「按此配置新建分析 / 重新尝试」

### DoD-4 报告页（CollabReportPage.vue）
- 七段式 `SystemReportReader`（demo buildCollabReport 逐段复刻）；template `synth-collaboration-report-v1`
- 结果来源：任务快照（taskId query → #104）优先，回退默认跑批；context 从任务冻结参数还原
- PDF 导出：`renderIndustryAnalysisReportPdf` + `downloadReportBlob`（STSong-Light 中文 PDF，仓内既有）
- limitations 四条诚实态：Mock 声明 / 权重未闭合+关联非因果（Q-SYNTH-C-03）/ 集群分不补零 / 评审环境限定

### 方法抽屉（CollabMethodDrawer.vue）
§10.10 七步骤（每步 IntelMetricMount）+ 临时演示公式表 + 「⚠️ 禁止将「密度×强度」冒充正式合成。正式图类型、分母、边权、权重与校准见 Q-SYNTH-C-01 / C-02」+ 关系输入三 Tag

### menu.ts（本叶 3 行）
`intel-collaboration` 工作台 component → CollabWorkbenchView；task/report 两隐路由 +component。**VIT/ELEM 占位不动**（diff 3+/1-，无越界）。

## 2. 产物清单

| 文件 | 类型 | 说明 |
|---|---|---|
| `src/views/intelligence/collaboration/CollabWorkbenchView.vue` | A | 工作台（~800 行） |
| `src/views/intelligence/collaboration/CollabAnalysisTaskPage.vue` | A | 过程页 |
| `src/views/intelligence/collaboration/CollabReportPage.vue` | A | 报告页 |
| `src/views/intelligence/collaboration/CollabMethodDrawer.vue` | A | 方法抽屉 |
| `src/views/intelligence/collaboration/collabTaskPageShared.ts` | A | 过程页 hydrate（VIT/ELEM 复用） |
| `src/views/intelligence/collaboration/collab.selfcheck.mjs` | A | 本叶自检 |
| `src/router/menu.ts` | M | 仅本叶 component 3 行 |
| `src/mock/intel/intelL1c.selfcheck.mjs` | M | 占位断言 3→>=2（COLLAB 落地演进） |

## 3. 验收证据

- `npm run type-check`（vue-tsc）✅ 0 error
- `npx eslint src/views/intelligence/collaboration/**` ✅ 0 error（menu.ts 存量 `serviceShellPage` 未用为 L1C 遗留，非本叶引入，未动）
- `npm run build-only`（vite）✅ built in 20.77s
- selfcheck 全绿：`collab.selfcheck` + `intel.selfcheck`(L1) + `intelL1b.selfcheck` + `intelL1c.selfcheck`
- 评审零泄漏断言：template 文案无裸露 `M_SYNTH_*`（角标全走 IntelMetricMount → @/review 组件自闸）

## 4. 架构合规自检

- ✅ D8：Arco Design Vue（select/tag/table/steps/drawer/tabs/checkbox/alert/descriptions）+ VChart + sci token 变量；主色 #165DFF；无新 UI 体系
- ✅ D9：每个统计数字旁 IntelMetricMount（ⓘ/红问号 D1-missing/Pending/Mock 组合，@/review 门控自闸）；就绪度只读消费 `synthReadinessSeed`（经全局 fallback）；Q-SYNTH-C-01~04 逐字保留；未在前端改绿
- ✅ D10：Arco 原生键盘可达；表行点击有 cursor + 文字提示
- ✅ D12：只调 `gkxlumen` 任务中心 #102–#109（Java REST 白名单 L1B 已扩），无 demo 服务直连
- ✅ Mock 开关：mock 全走 L1 `registerApiMock`（synthCollabBatch/analysisTask*），本叶未注册新 mock、`USE_MOCK=false` 不生效面
- ✅ 附录 E：E.3 切条件只进 config 不自动 create；E.4 同条件 running 单飞（bridge）；E.5 当天成功直接开结果 + 切回恢复
- ✅ 代码已推 `lumen-ui-topic` `origin/dev`（走查修正 `233b382`，合入 `76b0eea`）；任务状态 integration

## 5. 偏离说明

1. **报告触发**：demo 用 `data-system-report-trigger` 数据属性契约 + SystemTaskLayer 拦截；lumen 侧该契约无对应物（全仓 grep 0 命中）。本叶实现为：按钮直接创建 `region_innovation_collaboration_report` 产物任务（#102，mock 立即 success + 回写父任务 report_generated）→ 跳报告页。报告关联键 `snapshot:{taskId}` 与 L1B `isIntelRelatedReport` 兼容，记录面板「查看报告」可用。
2. **过程页五阶段来源**：demo 用 collabTasks localStorage 总线 900ms tick；lumen 对应物 = 任务中心 events 节点（`INTEL_NODE_NAMES` = COLLAB_TASK_STAGES 文案真源，L1B 已接）。空 events 不编阶段（svc 同款诚实空态）。
3. **intelL1c.selfcheck 修改**：占位断言 `equal 3` → `ok >= 2`（COLLAB 落地的预期演进；VIT/ELEM 落地时同样演进，AV 单收口）。

## 6. 待走查重点（建议）

- 工作台四结果态切换（默认 instant / 改条件 config / 任务 result / 恢复默认）
- 图谱过滤+高亮+子图统计联动；孤立表/中心 TOP 点击高亮
- 散点三分支：深圳 3y（ok）/ 上海 1y（insufficient，2 点）/ 南山区（none）
- 过程页：开始分析 → 五阶段 → wait_view → 查看结果；排队撤回
- 报告：生成 → 七段式 → PDF 导出中文正常
- 评审模式开：ⓘ 角标 + draft 橙点 + MissingDef 红问号（M_SYNTH_COLLAB_INDEX/OUTPUT_CORR）；关：DOM 零泄漏

## 7. cost 回填

- actual_tokens: ~150k / model_used: glm-5.3 / actual_cost: ~$2.1 / cost_warn: false

## 8. 走查修正（2026-10-27，已推 origin/dev）

commit `233b382`（合入 `76b0eea`）`lumen-ui-topic` `dev`。浏览器走查后修：

- 卡片无描边：Uno `preflight: false` 时 `.border` 只写线宽，补 `border-style`
- 筛选改不回去：切条件改用事件里的新上下文写回 URL，不再用旧 query 覆盖
- 过程页步骤已完成但顶栏/底栏仍「进行中」：mock 详情同引用赋值不触发响应式，hydrate 改为浅克隆
- Arco Vue Alert 无 `content` 属性，文案改走默认插槽
- 非默认条件「查看结果」空白：解开 showTaskResult 与拉任务的环，结果地址带上任务冻结的区域/对比/时间窗

状态：进入联调（integration）。

ponytail: full
