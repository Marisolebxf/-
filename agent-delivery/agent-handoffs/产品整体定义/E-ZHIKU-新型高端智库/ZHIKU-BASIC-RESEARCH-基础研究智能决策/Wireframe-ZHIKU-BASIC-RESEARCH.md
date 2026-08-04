# Wireframe-ZHIKU-BASIC-RESEARCH｜基础研究智能决策·线框与字段表

> **版本**：v1.0-rework-r2（AI 起草，待人确认）；收编并升级 S5 Wireframe v0.6 P67-P72 字段表
> **视觉规范**：Design.md（Arco 主题、主色 #165DFF、控件高 32px）；交互规范：UX-UE 通用交互组件规范
> **字段表第 6 列**：关联 metric_id / 功能序号（D9 铁律）

## F-BR-01 问题清单（P67 升级）

```
┌ PageShell「基础研究问题清单与趋势」 覆盖 82-84 ────────────────┐
│ [Tab] 问题清单 | 问题发展趋势 | 竞争格局报告   ← URL ?tab=      │
│ ┌统计卡┐ ┌统计卡┐                                              │
│ │问题总数 ⓘ🧪│ │我的订阅数│                                     │
│ ┌ 权威来源目录（可点选过滤）───────────────────────────────┐   │
│ │ [基金指南] [院士建议] [政策文件] [研讨纪要]              │   │
│ ┌ 问题清单  [关键词搜索][状态筛选][清空筛选] [智能识别🧪] ─┐   │
│ │ 表格：问题描述|领域|来源|识别时间|状态|订阅|操作          │   │
│ │  新识别行带「新识别🧪」标签；识别中行有[在线发布][移除]   │   │
│ ┌ 我的订阅 ────────────────────────────────────────────────┐   │
│ │ 订阅问题卡片 ×N（点击→查看趋势）/ Empty 引导              │   │
└──────────────────────────────────────────────────────────────┘
```

| # | 元素 | 类型 | 数据源 | 交互 | 关联 |
| --- | --- | --- | --- | --- | --- |
| 1 | 问题总数统计卡 | MetricCard | store.publishedCount | ⓘ 弹 MetricSpecCard | `ZHIKU-BR-ISSUE-TOTAL`／82 |
| 2 | 我的订阅数统计卡 | MetricCard（无 id，派生计数） | store.subscribedIssueIds.length | — | 82 |
| 3 | 权威来源目录 | Tag 组 | ISSUE_SOURCES | 点选切换过滤（再点取消） | 82 |
| 4 | 关键词搜索 | a-input-search | store.issueKeyword | 输入即过滤，持久化 | 82 |
| 5 | 状态筛选 | a-select | published/identifying | 叠加过滤 | 82 |
| 6 | 清空筛选 | a-button | — | 重置 3/4/5 | 82 |
| 7 | 智能识别按钮 | a-button loading | store.runIdentify() | 延时后新问题置顶入库；池尽提示空态 | 82 |
| 8 | 清单表格 | a-table | store.filteredIssues | 行内订阅/退订、在线发布、移除（限新识别未发布）、查看趋势 | 82 |
| 9 | 我的订阅区 | 卡片列表/Empty | store.subscribedIssues | 点击→trend Tab 下钻 | 82 |
| 10 | 诚实性标注 | 文本 | 固定 | — | 82（🧪 识别为演示态） |

## F-BR-02 问题发展趋势（P68 升级）

```
│ [问题选择器 v-model=issue] ← URL ?issue=                        │
│ ┌ 来源回溯条：来源目录标签 + 识别时间 + 状态 ┐                  │
│ ┌ 发展轨迹图（近5年折线，Empty=新识别无数据）┐                  │
│ ┌统计卡×3┐ 增长速度 ⓘ🧪 | 研究热度 | 潜力评估                   │
│ ┌ 动态监控预警 ┐ 未处理（[标记已处理]）/ 已处理（灰）分组       │
│ ┌ 智能推荐 ┐ 相关问题（点击切换 issue）| 相关文献（点击开抽屉） │
│ [Drawer] 文献摘要（标题/来源/摘要/🧪标注）                       │
```

| # | 元素 | 类型 | 数据源 | 交互 | 关联 |
| --- | --- | --- | --- | --- | --- |
| 1 | 问题选择器 | a-select | store.issues | 切换同步 URL ?issue= | 83 |
| 2 | 来源回溯条 | 描述行 | activeIssue.source/identifiedAt | — | 83 |
| 3 | 发展轨迹图 | VChart line | ISSUE_TREND_BY_ID | 无数据→EmptyState | 83 |
| 4 | 增长速度卡 | MetricCard | ISSUE_SCORE_BY_ID | ⓘ 弹卡（演示态） | `ZHIKU-BR-ISSUE-HEAT-SCORE`／83 |
| 5 | 研究热度/潜力卡 | MetricCard×2 | 同上 | — | 83 |
| 6 | 预警列表 | 分组列表 | store.alertsFor(issue) | [标记已处理] 持久化 | 83 |
| 7 | 智能推荐 | 列表 | ISSUE_RECOMMENDATIONS | 相关问题→切 issue；文献→抽屉 | 83 |
| 8 | 文献摘要抽屉 | a-drawer | 推荐项 mock 摘要 | 关闭返回 | 83 |
| 9 | 诚实性标注 | 文本 | 固定 | — | 83（演示态打分） |

## F-BR-03 竞争格局报告（P69 升级）

```
│ [Tab] 国际 | 国家 | 深圳市   ← 持久化                            │
│ ┌统计卡×4┐ 研究热度 ？(红) | 前沿引领性 | 投资力度 | 主体总量    │
│ ┌ 区域对比 [柱状图|雷达图] ┐  ┌ 趋势追踪（三线逐年）┐            │
│ [生成竞争格局报告] → Modal 确认 → writing 预填任务 + 跳转        │
│ 诚实性标注：指数权重算法待定（Q-ZHIKU-04）                       │
```

| # | 元素 | 类型 | 数据源 | 交互 | 关联 |
| --- | --- | --- | --- | --- | --- |
| 1 | 层次 Tab | a-tabs | COMPETITION_TIERS | 切换持久化 | 84 |
| 2 | 综合指数统计卡 | MetricCard（D1 missing 红问号） | COMPETITION_STAT_BY_TIER | 点开显 GAP 引用 | `ZHIKU-BR-COMPETITION-INDEX`／84 |
| 3 | 其余三统计卡 | MetricCard | 同上 | — | 84 |
| 4 | 区域对比图 | VChart bar/radar | 三层次四维 | 图型切换 | 84 |
| 5 | 趋势追踪图 | VChart line×3 | COMPETITION_TREND | — | 84 |
| 6 | 生成报告按钮 | a-button primary | — | Modal 确认→createTask 预填→`/writing/create?step=outline&task=` | 84（跨叶子） |
| 7 | 诚实性标注 | 文本 | 固定 | — | 84（Q-ZHIKU-04） |

## F-BR-04 深圳市部署清单（P70 升级）

```
┌ PageShell「深圳市基础研究部署清单」 覆盖 85 ─────────────────┐
│ ┌统计卡┐┌统计卡┐ 清单总数 ⓘ🧪 | 高优先级条目数                │
│ [领域▾][优先级▾][进展状态▾][清空筛选]  ← 持久化               │
│ ┌ 地图（TalentMapView，点位=筛选后清单）│ ┌ 清单表格 ┐        │
│ │  点位点击→表格行高亮+详情侧条        │ │ 行点击→地图高亮 │  │
│ │  选中点位放大/描边                    │ │ 选中行底色      │  │
│ ┌ 详情侧条：领域/机构/优先级/状态/更新时间 ┐                   │
│ ┌ 趋势分析（清单规模+高优先级逐年）┐                           │
│ ┌ 热点问题识别：问题标签 ×N →跳 issues?tab=trend&issue= ┐      │
└──────────────────────────────────────────────────────────────┘
```

| # | 元素 | 类型 | 数据源 | 交互 | 关联 |
| --- | --- | --- | --- | --- | --- |
| 1 | 清单总数卡 | MetricCard | DEPLOY_LIST | ⓘ 弹卡 | `ZHIKU-BR-DEPLOY-TOTAL`／85 |
| 2 | 高优先级数卡 | MetricCard（派生） | 筛选前数据 | — | 85 |
| 3 | 三维筛选条 | a-select×3 + 清空 | store.deployFilters | 叠加过滤持久化 | 85 |
| 4 | 地图 | TalentMapView | deployToMapPoints(filtered) | select-point→选中联动 | 85 |
| 5 | 清单表格 | a-table row-class | store.filteredDeployList | 行点击→setSelectedDeploy | 85 |
| 6 | 详情侧条 | a-descriptions | selectedDeploy | — | 85 |
| 7 | 趋势分析图 | VChart line | DEPLOY_TREND | — | 85 |
| 8 | 热点问题标签 | a-tag 组 | 领域关联 issues | 点击→issues 页 trend 下钻 | 85 |
| 9 | 空态 | EmptyState | 筛选无结果 | 清空筛选按钮 | 85 |
| 10 | 诚实性标注 | 文本 | 固定 | — | 85（Mock 静态集合） |

## F-BR-05 组织实施分析（P71 升级）

```
│ ┌统计卡×6┐ 综合得分 ⓘ🧪 + 五维单项                              │
│ ┌ 五维雷达 ┐  ┌ 深圳现有科研资源清单表 ┐                        │
│ ┌ 引进/创新资源需求预测（实线+虚线🧪）┐                          │
│ ┌ 资源配置建议（四类 Tag）  [纳入跟踪/移除跟踪] ┐                │
│ ┌ 我的跟踪清单（计数 + 可移除 / Empty 引导）┐                    │
```

| # | 元素 | 类型 | 数据源 | 交互 | 关联 |
| --- | --- | --- | --- | --- | --- |
| 1 | 综合得分卡 | MetricCard | ORG_CAPABILITY_DIMS 均值 | ⓘ 弹卡（等权重演示态） | `ZHIKU-BR-ORG-CAPABILITY-SCORE`／86 |
| 2 | 五维单项卡 | MetricCard×5 | 同上 | — | 86 |
| 3 | 五维雷达 | VChart radar | 同上 | — | 86 |
| 4 | 资源清单表 | a-table | ORG_RESOURCE_LIST | — | 86 |
| 5 | 需求预测图 | VChart line 实/虚 | RESOURCE_FORECAST | — | 86（虚线演示态） |
| 6 | 建议列表 | a-list + Tag | RESOURCE_SUGGESTIONS | [纳入跟踪/移除跟踪] 幂等持久化 | 86 |
| 7 | 跟踪清单 | 卡片/Empty | store.adoptedSuggestions | 移除 | 86 |
| 8 | 诚实性标注 | 文本×2 | 固定 | — | 86（预测/建议演示态） |

## F-BR-06 成果评估（P72 升级）

```
│ [Alert 告警条] 四维算法定义卡未落地（Q-ZHIKU-04）演示态          │
│ [成果选择器 ▾]  ← 持久化                                        │
│ ┌统计卡×5┐ 综合得分 ？(红) + 应用性/理论/创新/影响力             │
│ ┌ 四维雷达 ┐  ┌ 可视化评估报告（文本）[生成评估报告] ┐           │
│ ┌ 分析视图 [对比分析|趋势分析] ┐ ← 子视图切换持久化              │
│ │ 对比=多成果柱图 / 趋势=历年平均分曲线                          │
```

| # | 元素 | 类型 | 数据源 | 交互 | 关联 |
| --- | --- | --- | --- | --- | --- |
| 1 | 告警条 | a-alert warning | 固定 | — | 87（Q-ZHIKU-04） |
| 2 | 成果选择器 | a-select | EVAL_RESULTS | 切换持久化 | 87 |
| 3 | 综合得分卡 | MetricCard（D1 missing 红问号） | evalTotalScore | 点开显 GAP 引用 | `ZHIKU-BR-EVAL-SCORE`／87 |
| 4 | 四维单项卡 | MetricCard×4 | dims | — | 87 |
| 5 | 四维雷达 | VChart radar | dims | — | 87 |
| 6 | 评估报告文本 | 段落 | 模板文案 | — | 87 |
| 7 | 生成评估报告 | a-button | — | Modal 确认→createTask 预填→跳转 | 87（跨叶子） |
| 8 | 子视图切换 | a-radio-group | store.evalView | 切换持久化 | 87 |
| 9 | 对比柱图/趋势线图 | VChart | EVAL_RESULTS / EVAL_TREND | 随子视图切换 | 87 |

## 最小服务响应字段（正式态对照）

- issues：`id,title,field,source,identifiedAt,status,subscribed,isNew`
- trend：`issueId,points[{year,value}],score{growthRate,heatScore,potentialScore}`
- competition：`tier,researchHeat,frontierLead,investment,subjectTotal,trend[]`
- deploy：`id,field,priority,institution,status,updatedAt,lng,lat,value`
- org：`dims[{dim,score}],resources[],forecast[],suggestions[]`
- eval：`id,name,field,dims{applicability,theoretical,innovation,influence},trend[]`

## ReviewMode 挂钩与 metric_id 清单

- 评审模式开：所有 MetricCard 显示 ⓘ/红问号 + 就绪度角标（🧪 MockBadge 全量、两项 missing 红问号）；关：DOM 零泄漏（无 metric_id/GAP-*/Q0xx 字样）。
- 本 Frame 集 metric_id 全集（6）：`ZHIKU-BR-ISSUE-TOTAL`、`ZHIKU-BR-ISSUE-HEAT-SCORE`、`ZHIKU-BR-COMPETITION-INDEX`、`ZHIKU-BR-DEPLOY-TOTAL`、`ZHIKU-BR-ORG-CAPABILITY-SCORE`、`ZHIKU-BR-EVAL-SCORE`。
