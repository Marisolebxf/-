# LUMEN-SVC-FE-ANALYSIS-VISUAL-L01 · 分析三键 + 生态 + 招引视觉复刻（R+W）

> 日期：2026-08-18  
> Task：`LUMEN-SVC-FE-ANALYSIS-VISUAL-L01`  
> 总控 / 派单：`DEMO-SVC-ABCD-长任务总控.md` · `DEMO-SVC-FE-D-视觉复刻补单.md` · `DEMO-SVC-FE-D-总派单.md`  
> 对照：`templates/fe-replica-visual-dod.md` · `demo-ui-topic` ServiceOrgAnalysis / ServiceChainEcosystem / ServiceRecommend  
> 上游：`LUMEN-SVC-FE-PORTAL-VISUAL-L01`（integration · `404a607`，本叶未改 portal）  
> 有数叶：`LUMEN-SVC-FE-ANALYSIS-FULL-L01`（金路径绿 ≠ 本叶完成）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短 diff 对齐 Demo 区块；补报告阅读器/G6/实包图表；未用 YAGNI 跳过 D8/D9/D10/W1–W3；不贴 JSX；不 new 地图 |

## /goal 区块清单（对照 Demo）

### A. institution-judgment 三键（`ServiceOrgAnalysisPage`）

| workspace | Demo 区块 | 本叶完成度 |
|-----------|-----------|------------|
| field | 双 Tab · 上下文条（领域+对比篮）· KPI 条 · 过程壳 · 覆盖热力/矩阵切换 · 核心结论三格 · 记录 | ✅；热力用实包类型柱图诚实表达（无机构×领域矩阵维） |
| trend | 上下文 · KPI · 过程壳 · 趋势窗切换 · 折线/表 · 热度研判 · 记录 | ✅；折线仅实包序列 |
| capability | 上下文 · 评价模型维权 · 过程壳 · 排名/雷达 · 记录 | ✅；雷达无 dim_scores 诚实骨架 |

### B. chain-analysis 生态（`ServiceChainAnalysisPage`）

| workspace | Demo 区块 | 本叶完成度 |
|-----------|-----------|------------|
| chain | 上下文 · 过程壳 · 地铁轨道图 · 瓶颈堵点 · 短板清单 · 配置态同构壳 · 记录 | ✅；配置态铺齐地铁骨架 |
| graph | 上下文 · 关系/节点过滤 · 过程壳 · **G6** 关系图 · 记录 | ✅；有 nodes/edges 才画；ADS 无快照诚实空 |
| shenzhen | 评价框架 · 对比指标 · 过程壳 · 区分布图/表 · 机构样本 · 记录 | ✅；城市对比柱无数不伪造 |

### C. institution-decision 招引（`ServiceRecommendPage`）

| workspace | Demo 区块 | 本叶完成度 |
|-----------|-----------|------------|
| attract | 固定权重模型 · 生成名单 · 过程壳 · rank-row 名单 · 报告入口 · 记录 | ✅ |
| cultivate | 类型/环节筛选 · 固定权重 · 过程壳 · rank-row+培育建议 · 报告入口 · 记录 | ✅ |

## 复刻五维验收（R1–R5）

| # | 项 | 结果 |
|---|-----|------|
| R1 布局 | 三键+生态三键+招引两键 Demo 区块均有结构；一节点一套 layout | ✅ |
| R2 交互 | config / processing / result / report / records；空篮门控；wait_view 显式查看 | ✅ |
| R3 样式 | `--sci-bg-page`、svc-* token、rank-badge 色阶、地铁/结论/热度面板 | ✅ |
| R4 评审 | 只挂 `@/review`（`TraceInfoIcon` / `ReviewMetricBadges`）；关评审零泄漏 | ✅ mount：`SVC-ORG-*` / `SVC-ECO-*` / `SVC-RECOMMEND-*` / `SVC-REC-*` |
| R5 Mock | 开：既有 `registerApiMock`；关：只渲染 Java 实包，禁止 fixture 填数 | ✅ |

## 工作区 W1–W3

| # | 项 | 结果 |
|---|-----|------|
| W1 | 配置区 / 过程壳 / 结果板 / 记录 Tab | ✅（三工作区均齐） |
| W2 | 关系图用本仓 G6（`ServiceEcoGraph`），不用 ECharts 冒充 | ✅ |
| W3 | 报告入口挂已有 `SystemReportReader`（`SvcAnalysisReportHost`） | ✅ |

检索皮肤 V1–V7：本叶非查询 Hub → V2 N/A；V1/V3–V7 适用处 ✅。

## 偏离说明

- 领域覆盖正式热力=机构×领域；Java `org_coverage` 仅类型计数 → 柱图 + 表诚实表达，不造矩阵假点
- 技术力雷达需 `dim_scores`；实包无 → 雷达骨架 + 排名/得分柱图
- 图谱 ADS 无快照表 → G6 组件已挂，无数诚实空（algo 已约定）
- 深圳「城市横向对比」无数 → 对比格骨架，不画假柱
- **未改**门户视觉叶文件

## 产物清单

| 产物 | 路径 |
|------|------|
| 报告宿主 | `src/components/service-center/SvcAnalysisReportHost.vue` |
| G6 图谱 | `src/components/service-center/ServiceEcoGraph.vue` |
| 图表工具 | `src/utils/svcAnalysisCharts.ts` |
| Job | `useSvcAnalysisJob.ts`（`report` view + `openReport`） |
| 三页 | `ServiceOrgAnalysisPage` / `ServiceChainAnalysisPage` / `ServiceRecommendPage` |
| 自检 | `svcWorkspaceVisual.selfcheck.mjs` · `svcAnalysisCharts.selfcheck.mjs` |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-ANALYSIS-VISUAL-L01.md` |

## 验收证据

- [x] `node src/utils/svcWorkspaceVisual.selfcheck.mjs` → OK
- [x] `node src/utils/svcAnalysisCharts.selfcheck.mjs` → OK
- [x] `npm run type-check` → 绿
- [x] commit + push `origin/dev`（见 CI 段）
- [ ] 外网截图人审（非下一叶闸门）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 调用链 | 前端→Java analysisTask / svc | ✅ |
| D8 | Design / Arco / `--sci-*` | ✅ |
| D9 | ReviewMetricBadges；不自造 ⓘ | ✅ |
| D10 | 过程/结果/报告状态机 | ✅ |
| D12 | 不调 demo-* | ✅ |
| 复刻五维 | R1–R5 + W1–W3 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~14 万 |
| actual_cost | 估 <$6 |
| cost_warn | false |

## CI/CD

- 分支：`dev`
- commit：`db6ef55`
- pipeline：push 后 GitLab `lumen-ui-topic` tracking `origin/dev`

## 联调确认

联调通过：分析三键 + 生态 + 招引视觉区块按 Demo 清单铺齐；报告走 `SystemReportReader`；图谱走 G6；`USE_MOCK=false` 诚实空或实包。门户视觉叶区块未破坏。
