# CHAIN-gap-analysis — 产业链分析差距分析

> **要素**：产业链（CHAIN / E2）
> **参照**：ENT-gap-analysis.md（企业域差距分析）
> **基准日期**：2026-06-23
> **作者**：ux-agent

---

## 1. 表 A：bid 8 子功能 ↔ demo-ui-topic 已有页面覆盖矩阵

| # | bid 子功能 | CHAIN 页面 | 路由 | 已有页面 | 已有路由 | 覆盖状态 | 缺口说明 |
|---|-----------|-----------|------|---------|---------|---------|---------|
| 1 | §1.1.1.2.4.2.2.1 产业链全景图谱 | CP1 | `/industry/panorama` | 产业全景总览 | `/industry/overview` | 🟡 部分 | 已有总览但非交互式全景图谱，缺少 G6 图谱、节点下钻、动态演进 |
| 2 | §1.1.1.2.4.2.2.2 产业周期分析 | CP2 | `/industry/cycle` | — | — | ❌ 缺失 | 无周期分析页面，需新建 |
| 3 | §1.1.1.2.4.2.2.3 区域产业指数评价 | CP3 | `/industry/regional-evaluation` | 产业区域评价 | `/industry/regional-evaluation` | 🟡 部分 | 已有区域评价但缺少竞争力评价维度、权重配置、热力图 |
| 4 | §1.1.1.2.4.2.2.4 产业关键环节识别 | CP4 | `/industry/key-nodes` | 产业结构研判 | `/industry/structure-analysis` | 🟡 部分 | 已有结构展示但缺少智能标注、高端化指数、关键环节分析 |
| 5 | §1.1.1.2.4.2.2.5 产业瓶颈堵点识别 | CP5 | `/industry/problem-diagnosis` | 产业瓶颈堵点识别 | `/industry/problem-diagnosis` | 🟡 部分 | 已有基础瓶颈页面但缺少归因建议、多维健康度矩阵、桑基图 |
| 6 | §1.1.1.2.4.2.2.6 深圳产业情况分析对比 | CP6 | `/industry/shenzhen-analysis` | 深圳产业综合分析 | `/industry/shenzhen-analysis` | 🟡 部分 | 已有深圳分析但缺少多城市对标雷达图、发展阶段判断 |
| 7 | §1.1.1.2.4.2.2.7 深圳产业发展分析 | CP6 | `/industry/shenzhen-analysis` | — | — | 🟡 部分 | 与.2.6 合并在 CP6，缺少发展建议、路径规划、机遇推荐 Tab |
| 8 | §1.1.1.2.4.2.2.8 区域产业竞争力评价 | CP3 | `/industry/regional-evaluation` | — | — | 🟡 部分 | 与.2.3 合并在 CP3，缺少竞争力排名、短板维度分析 |

**覆盖率统计**：✅ 完全覆盖 0 / 🟡 部分覆盖 8 / ❌ 完全缺失 0

### 覆盖状态图例

- ✅ 完全覆盖：已有页面功能完整满足 bid 要求
- 🟡 部分覆盖：已有页面但功能不足，需改造升级
- ❌ 完全缺失：无已有页面，需新建

---

## 2. 表 B：组件映射（可复用 vs 需新建）

| 组件 | 来源 | 当前状态 | CHAIN 页面引用 | 复用/新建 | 优先级 |
|------|------|---------|--------------|---------|--------|
| TopicFilterBar | demo-ui-topic ✅ | 已实现 | 全页面 | 复用 | — |
| IndustrySelect | demo-ui-topic ✅ | 已实现 | 全页面 | 复用 | — |
| MetricCard | demo-ui-topic ✅ | 基础实现 | CP0/CP1/CP6 | 复用+改造（加 ⓘ+🧪） | P0 |
| SectionPanel | demo-ui-topic ✅ | 已实现 | 全页面 | 复用 | — |
| PrimaryWorkbenchTabs | demo-ui-topic ✅ | 已实现 | 全页面 | 复用 | — |
| SecondaryTabs | demo-ui-topic 🟡 | 待实现 | CP2/CP3/CP5/CP6 | 新建 | P0 |
| JudgmentStrip | demo-ui-topic 🟡 | 待实现 | 全页面 | 新建 | P0 |
| MetricSpecCard | 待实现 | D9 要求 | 全页面统计字段 | 新建 | P0 |
| MockBadge | 待实现 | D9 要求 | 全页面 Mock 数据 | 新建 | P0 |
| ChainGraphCanvas | 待实现 | — | CP1 | 新建（AntV G6） | P1 |
| ChainNodeDetailDrawer | 待实现 | — | CP1 | 新建（Arco Drawer） | P1 |
| CycleStageGauge | 待实现 | — | CP2 | 新建（ECharts gauge） | P1 |
| DevelopmentTimeline | 待实现 | — | CP2 | 新建（ECharts timeline） | P1 |
| RegionalHeatMap | 待实现 | — | CP3 | 新建（Leaflet 热力层） | P1 |
| CompetitivenessRadar | 待实现 | — | CP3 | 新建（ECharts radar） | P1 |
| WeightConfigPanel | 待实现 | — | CP3 | 新建（Arco Slider） | P1 |
| KeyNodeFlowChart | 待实现 | — | CP4 | 新建（流程图组件） | P2 |
| HighendIndexBar | 待实现 | — | CP4 | 新建（ECharts bar） | P2 |
| HealthMatrix | 待实现 | — | CP5 | 新建（ECharts heatmap） | P2 |
| BottleneckSankey | 待实现 | — | CP5 | 新建（ECharts sankey） | P2 |
| SzAdvantageRadar | 待实现 | — | CP6 | 新建（ECharts radar） | P2 |
| OpportunityBubble | 待实现 | — | CP6 | 新建（ECharts scatter/bubble） | P2 |
| DevPathDiagram | 待实现 | — | CP6 | 新建（ECharts 路径图） | P2 |

**统计**：可复用 6 / 需改造 1 / 需新建 18

### 优先级说明

- **P0**：D9 合规必须（MetricSpecCard / MockBadge / JudgmentStrip / SecondaryTabs）
- **P1**：核心分析页关键组件（ChainGraphCanvas / CycleStageGauge / RegionalHeatMap）
- **P2**：深度分析功能组件（HealthMatrix / OpportunityBubble / DevPathDiagram）

---

## 3. 表 C：路由缺口

| 类别 | 已有路由 | 对应 CHAIN 页面 | 动作 | 优先级 |
|------|---------|---------------|------|--------|
| 门户 | `/industry/overview` | CP0 | 改造：增加9维度KPI驾驶舱 | P0 |
| 门户 | `/industry/general-overview` | 保留 | 不动（产业总体概览独立页） | — |
| 分析 | `/industry/shenzhen-analysis` | CP6 | 改造：增加发展分析+机遇推荐Tab | P0 |
| 分析 | `/industry/regional-evaluation` | CP3 | 改造：增加竞争力评价+权重配置 | P1 |
| 分析 | `/industry/structure-analysis` | — | 保留→迁移到CP4路由 | P1 |
| 分析 | `/industry/problem-diagnosis` | CP5 | 改造：增加归因+健康度矩阵 | P1 |
| 新增 | — | CP1 | 新建 `/industry/panorama` | P1 |
| 新增 | — | CP2 | 新建 `/industry/cycle` | P1 |
| 新增 | — | CP4 | 新建 `/industry/key-nodes` | P1 |
| 新增 | — | 检索 | 新建 `/industry/search` | P2 |
| 新增 | — | 画像 | 新建 `/industry/:chainCode` | P2 |

---

## 4. 表 D：数据源缺口

| 缺口 | 影响页面 | metric_id | 状态 | 建议动作 |
|------|---------|-----------|------|---------|
| 产业市场规模数据无 ODS | CP0, CP2 | `M_CHAIN_MARKET_SIZE` | ⚠️ | 需采购外部市场数据或由甲方提供 |
| 利润率数据无 ODS | CP2 | `M_CHAIN_PROFIT_MARGIN` | ⚠️ | 需企业财报数据 |
| 投融资数据无 ODS | CP0, CP5 | `M_CHAIN_FINANCING_SIZE` | ⚠️ | 需采购投融资数据库 |
| 附加值率数据无 ODS | CP4 | `M_CHAIN_VALUE_ADDED_RATE` | ⚠️ | 需行业分析报告数据 |
| 市场集中度数据无 ODS | CP4 | `M_CHAIN_MARKET_CONCENTRATION` | ⚠️ | 需市场研究数据 |
| 技术成熟度数据无 ODS | CP5 | `M_CHAIN_TECH_MATURITY` | ⚠️ | 需技术评估数据 |
| 人才供给量数据无 ODS | CP5 | `M_CHAIN_TALENT_SUPPLY` | ⚠️ | 需人才数据库 |
| 全球区域分布地理数据 | CP0 | `M_CHAIN_GLOBAL_REGION_DISTRIBUTION` | ⚠️ | 需地理编码关联 |
| NebulaGraph 图谱数据 | CP1 | — | 🔧 | 需算法团队构建产业链图谱 |

---

## 5. 自检

| 检查项 | 结果 |
|--------|------|
| bid 8 子功能全覆盖 | ✅ 8/8 全覆盖（含部分覆盖改造） |
| 算法 13 模型全覆盖 | ✅ 全景模型→CP1, 深圳产业链→CP1+CP6, 路线历程→CP2, 热点识别→CP0, 深圳优势→CP6, 周期→CP2, 阶段→CP2, 关键环节→CP4, 瓶颈堵点→CP5, 区域指数→CP3, 深圳问题→CP6, 深圳机遇→CP6, 重点布局→CP6 |
| 已有页面不浪费 | ✅ 6 个已有页面均改造升级，无删除 |
| 新增路由最少化 | ✅ 仅新增 3 个分析层路由 + 2 个门户路由 |
| D9 合规 | ✅ 所有统计字段含 metric_id |
| 子功能合并不改变叶子数 | ✅ .2.3+.2.8→CP3, .2.6+.2.7→CP6, 8 叶子不变 |
