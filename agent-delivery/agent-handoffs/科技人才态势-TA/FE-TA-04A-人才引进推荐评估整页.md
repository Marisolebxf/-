# FE-TA-04A · 人才引进推荐评估 — 整页复刻

- **任务**：FE-TA-04A（Epic：E-FE-TALENT）
- **执行**：agent:frontend-agent（监管 human:淮政玮）
- **日期**：2026-10-21
- **状态**：实现完成，停本地工作区待人工验收（AGENTS.md 闸门：验收通过前不 commit/push）
- **ponytail**：full

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| registry | FE-TA-04A → in_progress（完工后按闸门停本地，待人工验收再推进状态） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过任何护栏项：搜索状态机真生效、规格条、4 Tab 全量、3 报告导出走专用打印页、D9 A15 挂点 + 六条无源指标红问号不伪闭合、handoff 全交付；纯函数模型全部冻结移植不重写。 |

## 修改内容

### 1. 页面层（`src/views/talent/recommend/`）

| 文件 | demo 真源 | 说明 |
|---|---|---|
| `index.vue`（基座壳填充为整页） | `TalentRecommendPage.jsx`（~260 行） | 筛选行（产业级联 `IndustrySelect` + 评估目标 `a-select` + 当前评估对象可搜索 `a-select allow-search` 搜索真生效）+ 已应用摘要条（`:key="appliedSummary.revision"` 数据签名规避 dev slot props 失效）+ `RecommendSpecBar` 规格条（L5 规格 + 评估目标 Tab 联动）+ `PageTabFrame` 4 Tab + 跨页 `talentId` 定位（initialTalentId 语义） |
| `components/ContributionTab.vue` | `ContributionTab.jsx`（739 行） | 学科贡献度分析：三栏（可视化层级雷达+概览/学者/成果三层视图 / 多维数据联动力导向图+跨学科协同路径 / 指标缩放+热力+智能分析与推荐）；图元点击下钻联动（专家/学科/成果/合作者四类节点）+ 自动深度分析（高潜力 Top1 切换）+ 贡献匹配报告弹窗入口 |
| `components/DifficultyTab.vue` | `DifficultyTab.jsx`（165 行） | 学者引进难度预测：难度仪表盘 + 六因子量化（DEMO_RULE_HINTS ⓘ 演示规则提示，005/006/007 红问号）+ 过往合作表 + 合作网络力导向图 + 策略预警（selectAlertStrategies 复用 S01 冻结件）+ CSV 导出（BOM） |
| `components/CostTab.vue` | `CostTab.jsx`（653 行） | 引进成本预测：成本结构条+饼 / 三方案预设（稳健/科研倾斜/薪酬竞争）+ 五滑杆模拟 / 方案对比表 / 历史趋势双线（投入+效果）+ 市场薪酬趋势 / 智能预警 a-alert 族 / 行业对比条 + 对比结论弹窗；CSV + PDF 导出。真机期 DN-A15-COST 无源：mock 态照 demo 渲染 + 红问号 + 「成本采集来源未拍板」title，不外推金额 |
| `components/ReportTab.vue` | `ReportTab.jsx`（~400 行） | 人才尽调报告与推荐：定制维度勾选 a-checkbox-group + 筛选行（学科方向/匹配方式[评估目标联动 TARGET_TO_ORG_NEED]/匹配度阈值/关键词）+ 推荐卡网格（data-talent-rec 锚点、维度进度、风险标签、动态更新时间戳）+ 对比抽屉 + 并行尽调队列弹窗（batchQueue 依次审阅）+ 动态跟踪刷新 |
| `components/DueDiligenceReport.vue` | `DueDiligenceReport.jsx`（296 行） | 尽调报告弹窗：多源画像（NLP 融合采集计数）+ AI 评分雷达 + 成果/履历/合作网络/风险四段 + a-rate 评级 + PDF 导出（雷达 getDataURL 快照） |
| `components/ContributionMatchReport.vue` | `ContributionMatchReport.jsx`（192 行） | 贡献匹配报告弹窗：潜力/匹配/风险三卡 + 贡献雷达 + 分维度进度 + 分析摘要（buildContributionMatchAnalysis 合成）+ PDF 导出 |
| `components/TalentComparePanel.vue` | `TalentComparePanel.jsx`（~350 行） | 对比面板：协同度评分 + 学科覆盖缺口 + 角色互补（AI 分/风险）+ 两两协同潜力表（pairSynergy）+ 团队分析报告弹窗 + 并行生成尽调入口 |
| `recommend-overrides.css` | `talent-recommend.css` `.ant-*` 族 | Arco 等价替换层：mini select/input 高度 24px、slider 收敛、alert/table 字号、滚动条；自含 `tl-metric-missing-mark` 红问号样式（防样式裸奔，复刻经验 §2.2） |

### 2. 纯函数模型（冻结移植，`src/views/talent/models/`）

| 模型 | demo 真源 | 函数/常量 |
|---|---|---|
| `talentRecommendSearch.ts` | `talentRecommendSearch.js` | `TARGET_TO_ORG_NEED` / `filterTalentsForRecommend` / `findTalentByKeyword`（精确→前缀→单位→兜底分级）/ `buildRecommendSearchOptions`（30 条截断）/ `resolveRecommendSearch`（keyword 优先→talentId→首位，demo 冻结次序） |
| `talentRecommendSpec.ts` | `talentRecommendSpec.js` | `TALENT_RECOMMEND_BID_DESC`（需规原文）/ `TALENT_RECOMMEND_L5`（四 Tab × 25 叶 L6 清单）/ `EVALUATE_TARGET_TAB`（team→report、industry→cost 等 demo 冻结映射）/ `getRecommendL5` |
| `dueDiligenceReportExport.ts` | `dueDiligenceReportExport.js` | `esc` / `printReportHtml`（blob URL + 新窗口 + load/600ms 双触发 print，不 window.print 整页）/ `DIM_LABELS` / `buildDueDiligenceReportHtml`（六段组装）/ `exportDueDiligencePdf` |
| `contributionMatchReportExport.ts` | `contributionMatchReportExport.js` | `buildContributionMatchAnalysis`（潜力分=均值+趋势×1.8+增益×0.08、匹配度 0.55/0.3/0.08/对齐合成、风险四项研判、决策建议分档）/ `buildContributionMatchReportHtml` / `exportContributionMatchPdf` |
| `costTabExport.ts` | `CostTab.jsx` 导出段 | `buildCostExportCsv`（BOM）/ `downloadCsv` / `exportCostReportPdf`（成本报告打印页） |
| `recommendMetrics.ts` | `SCI-INT-A15.yaml` | D9 挂点常量：3 metric_id + 6 无源指标 + 5 missing 卡 |
| `libCompat.ts` | `@/lib/industryCluster`（03A 未交付） | `fieldScopeShare` 桥接 + `UNMAPPED_CLUSTER_MESSAGE_FALLBACK` 兜底（03A 交付 resolveScope 后可去重） |

### 3. Arco 替换清单（antd → Arco Design Vue）

| antd | Arco | 备注 |
|---|---|---|
| Select（showSearch） | `a-select allow-search + filter-option` | 当前评估对象搜索真生效（filterTalentOption 桥接） |
| Segmented | `a-radio-group type="button"` | 可视化层级/预测视图/方案预设 |
| Slider（range） | `a-slider range` | 指标缩放分值区间（antd range 属性等价，非独立组件） |
| Table | `a-table size="small"`（row-key 静态字段名） | 过往合作表 / 方案对比表 |
| Modal | `a-modal`（#footer 插槽，`:title` 绑定模板串） | 尽调/贡献匹配/成本结论/团队分析/批量队列 |
| Checkbox.Group | `a-checkbox-group :options` | 报告定制维度 |
| Rate | `a-rate` | 尽调推荐等级 |
| Alert | `a-alert :type :title` | 成本智能预警族 |
| Progress | `a-progress size="small" :format` | 因子状态/维度进度/对比条 |
| Drawer | `a-drawer` | 推荐卡对比抽屉 |
| message | `Message.info/success/warning` | 联动提示 |

### 4. D9 数据血缘挂点（A15 卡，excel 308–332 / seq 305–329）

**已挂 3 指标（MetricSpecHint ⓘ，8 件套口径文本进 `recommendMetrics.ts`）**：

| metric_id | 挂点 |
|---|---|
| `M_TALENT_DEEP_164_1` 招入推荐匹配度 | 贡献 Tab 评估条 / ReportTab 推荐列表标题（1402/1403/1419/1421 匹配+AI 评分族） |
| `M_TALENT_DEEP_160_1` 人才关系链 | 贡献 Tab 合作切面（1407 过往合作回溯 / 1408 合作网络） |
| `M_TALENT_GRAPH_110_1` 人才实体识别 | ReportTab 推荐卡数据源行（1418 专家画像智能生成 NLP 融合采集） |

**六条无源指标（红问号 `?` + title 注明「无数据源（IP-10，owner 待定）」，不伪闭合）**：

| cardId | 挂点 |
|---|---|
| `...RECRUIT_005` 沟通障碍智能检测 | 难度 Tab communication 因子 |
| `...RECRUIT_006` 文化融合风险评估 | 难度 Tab culture 因子 |
| `...RECRUIT_007` 国际流动壁垒分析 | 难度 Tab mobility 因子 |
| `...RECRUIT_010` 引进阻力量化评分 | 难度 Tab 面板标题 + 策略预警（禁用 164 推荐分顶替） |
| `...RECRUIT_013` 引进成本模型 | 成本 Tab 标题 + 模拟区（DN-A15-COST：319–325 采集族未拍板，mock 金额不外推） |
| `...RECRUIT_025` 团队组合与协同分析 | 对比面板协同度（禁用 160 关系边密度顶替） |

**5 张 metric_missing 卡（红问号，语义锚定）**：INT-A-X-1401（指标缩放/热力）、1408（科研活跃度）、1410（策略建议）、1422（动态跟踪）、1423（尽调风险三段）。

- MockBadge：`USE_MOCK` 门控（基座语义，本页统计区无 01A 式 KPI 卡）。
- ⚠️ 成本族 DN-A15-COST 未拍板：真机期空态不出费用数字；mock 态照 demo 演示。

### 5. demo 逐区块对照表

| # | demo 区块（TalentRecommendPage 结构序） | lumen 落点 | 状态 |
|---|---|---|---|
| 1 | 筛选行（产业/评估目标/当前评估对象搜索） | index.vue tl-filter-bar | ✅ |
| 2 | 已应用摘要条 + 重新选择 | appliedSummary :key=revision | ✅ |
| 3 | 规格说明条（需规文案 + L5） | RecommendSpecBar（getRecommendL5） | ✅ |
| 4 | 评估目标切换 → 默认 Tab 联动 | EVALUATE_TARGET_TAB watch | ✅ |
| 5 | 4 Tab（贡献度/难度/成本/尽调报告） | PageTabFrame 四子组件 | ✅ |
| 6 | 贡献 Tab 三层视图（概览/学者/成果） | ContributionTab viewMode | ✅ |
| 7 | 贡献力导向图 + 跨学科路径 + 四类节点下钻 | graphOption + onGraphClick | ✅ |
| 8 | 指标缩放（radio + range + bar）+ 热力（zoom 模式） | metricBarOption/heatmapOption | ✅ |
| 9 | 自动深度分析（高潜力 Top1）+ 匹配报告弹窗 | runAutoDeep/openReport | ✅ |
| 10 | 难度仪表盘 + 六因子 + ⓘ 规则提示 | gaugeOption + DEMO_RULE_HINTS | ✅ |
| 11 | 过往合作表 + 合作网络图 | COOP_COLUMNS + networkOption | ✅ |
| 12 | 策略预警（红/黄过滤）+ CSV 导出 | selectAlertStrategies + exportReport | ✅ |
| 13 | 成本结构（bar + pie + 短名映射） | costBarOption/pieOption | ✅ |
| 14 | 三方案预设 + 五滑杆模拟 + 复位 | SCHEME_PRESETS + watch 复位 | ✅ |
| 15 | 方案对比表（A/B/C/模拟 + 差异着色） | schemeTable #diff 插槽 | ✅ |
| 16 | 历史趋势（投入+效果双轴）+ 市场薪酬 | trendOption/marketTrendOption | ✅ |
| 17 | 智能预警（行业/历史/案例/薪酬跳升四规则） | alerts computed | ✅ |
| 18 | 行业对比条 + 生成对比结论弹窗 | compareBars + buildCompareConclusion | ✅ |
| 19 | 成本 CSV + PDF 导出 | buildCostExportCsv/exportCostReportPdf | ✅ |
| 20 | 尽调报告维度勾选 + 筛选行 | enabledDims + orgNeed/matchFilter/searchKw | ✅ |
| 21 | 推荐卡网格（匹配度/维度进度/风险/更新戳/对比勾选） | data-talent-rec 卡 | ✅ |
| 22 | 推荐卡对比抽屉 + 打开尽调 | TalentComparePanel drawer | ✅ |
| 23 | 并行尽调队列（≥2 勾选，依次审阅） | startBatchReports/batchQueue | ✅ |
| 24 | 动态跟踪与更新（refreshTick） | runDynamicRefresh | ✅ |
| 25 | 尽调弹窗（多源画像/雷达/风险/评级）+ PDF | DueDiligenceReport | ✅ |
| 26 | 贡献匹配弹窗（三卡/雷达/进度）+ PDF | ContributionMatchReport | ✅ |
| 27 | 对比面板（协同/覆盖/互补/两两）+ 团队报告 | TalentComparePanel + 团队分析 modal | ✅ |
| 28 | 跨页带 talentId 定位（画像页跳转） | initialTalentId + 搜索解析 | ✅ |

### 6. 需规对照（SCI-INT-A15 seq 305–329 摘要）

| seq 段 | 需求项 | 落点 |
|---|---|---|
| 305–307 | 全领域学者多维分析总纲 + 筛选搜索 | 筛选行 + talentRecommendSearch |
| 308–310 | 学科贡献度分析（可视化/联动/智能推荐） | ContributionTab 三栏 |
| 311–318 | 难度预测（适应性/沟通/文化/流动/回溯/活跃/评分/策略） | DifficultyTab 六因子+策略 |
| 319–325 | 成本预测（采集/模型/分布/模拟/趋势/预警/导出） | CostTab（DN-A15-COST 红问号） |
| 326–329 | 尽调报告与推荐（画像/评分/报告/推荐/跟踪/风险/团队） | ReportTab + 三弹窗 |

## 测试结果（三绿）

- `pnpm type-check`（vue-tsc --build）：exit 0（0 错误）
- `node src/views/talent/talent.test.mjs`：`ok`（第 11 节 FE-TA-04A 共 45+ 断言：组件/模型/接线/状态机锚点/导出管线/D9/Arco 替换层）
- `pnpm build`：✓ built in 22.58s

## 走查修正记录

1. `a-range-slider`（antd range 语义误独立成组件）→ `a-slider range`（build 期 Rollup 解析失败暴露，修复后过）。
2. `title=`...`` 模板串未绑定（SFC 解析失败）→ `:title` 绑定。
3. `defineProps` 默认值引用本地常量（hoist 限制）→ 内联展开。
4. `noUncheckedIndexedAccess` 严格索引引发的类型门错误 ~50 处：常量字面量化（去 `Record<string, T>` 注解）、`?? null`/`as unknown as` 收窄、Arco `row-key` 静态字段名化、`scroll x: true`→数字（antd 布尔语义 Arco 不收）；均为类型层修正，运行语义与 demo 冻结一致。

## 遗留风险

1. `printReportHtml` 公共管线由本单先落于 `dueDiligenceReportExport.ts`（demo 挂 profileReportExport.js 属 03A）；03A 交付后可去重合并（头注释已标）。
2. `libCompat.ts` 的 `fieldScopeShare` 为 03A `@/lib/industryCluster` 未交付期的桥接；03A 合入后切换 import 并删除兜底。
3. 成本族真机期（DN-A15-COST 拍板前）：mock 态照 demo 渲染，红问号 + title 注明不外推；BE 接口就绪后按 I1-08 数据路径矩阵接线。
4. `USE_MOCK=false` 空数据防御：各 Tab 对空数组 `?? 1`/`|| []` 兜底（demo 同款）。
5. talent.test.mjs 与 FE-TA-03A 并行会话共享：第 12 节（画像页断言）由 03A 会话维护，本单仅追加第 11 节；两边均已收敛（全量 ok）。

## CI/CD（必填）

- 分支：dev（改动停本地工作区，未 commit/push —— AGENTS.md 人工验收闸门）
- commit：无（待验收后 `[agent:frontend-agent]` 提交）
- pipeline：未触发
- dev 测试 URL：待推送部署后补充

## 可观测性（建议）

- 事件：`ta-talent-track`（page-mounted + 关键交互），traceId 经 `createTraceId`（useTalentTrack 复用基座）
- OTEL_SERVICE_NAME：lumen-ui-science-pc（仓默认）

## 涉及文件

- `src/views/talent/recommend/index.vue`（基座壳 → 整页复刻）
- `src/views/talent/recommend/components/ContributionTab.vue`（新增）
- `src/views/talent/recommend/components/DifficultyTab.vue`（新增）
- `src/views/talent/recommend/components/CostTab.vue`（新增）
- `src/views/talent/recommend/components/ReportTab.vue`（新增）
- `src/views/talent/recommend/components/DueDiligenceReport.vue`（新增）
- `src/views/talent/recommend/components/ContributionMatchReport.vue`（新增）
- `src/views/talent/recommend/components/TalentComparePanel.vue`（新增）
- `src/views/talent/recommend/recommend-overrides.css`（新增）
- `src/views/talent/models/talentRecommendSearch.ts`（新增）
- `src/views/talent/models/talentRecommendSpec.ts`（新增）
- `src/views/talent/models/dueDiligenceReportExport.ts`（新增）
- `src/views/talent/models/contributionMatchReportExport.ts`（新增）
- `src/views/talent/models/costTabExport.ts`（新增）
- `src/views/talent/models/recommendMetrics.ts`（新增）
- `src/views/talent/libCompat.ts`（新增）
- `src/views/talent/talent.test.mjs`（第 11 节追加）
- `src/config/echarts.ts`（GaugeChart/RadarChart/GraphChart 按需注册，01A 后既有项复用）
