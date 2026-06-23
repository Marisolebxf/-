# CHAIN-wireframe — 产业链分析页面线框

> **要素**：产业链（CHAIN / E2）
> **scope_ref**：bid `§1.1.1.2.4.2.2`（8 子功能）
> **参照**：ENT-wireframe.md（企业域 9 页线框）
> **作者**：ux-agent
> **日期**：2026-06-23
> **D9 合规**：所有统计字段含 metric_id，来源引用真实 ODS 表

---

## 通用骨架说明

所有分析层页面遵循 Design.md 三段工作台：

- **左图层面板**（152–184px）：筛选器、图层控制、分类导航
- **中央主视图**（自适应）：图谱 / 图表 / 地图为主视图
- **右分析面板**（440–608px）：结论卡片、趋势分析、下钻明细

顶部：TopicFilterBar（产业选择 + 时间窗口 + 区域范围 + 关键词）
组件基座：Arco Design + ECharts + AntV G6 + Leaflet

---

## CP0 产业链分析概述（全局驾驶舱）

**路由**：`/industry/overview`
**bid 映射**：全局驾驶舱，9 维度基础指标一览
**算法依赖**：基础指标×9 维度（产业市场规模/企业规模/机构规模/投融资规模/全球区域分布/全国产业分布/产业动态资讯/深圳产业要素/深圳产业分布）

### 骨架

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TopicFilterBar [产业▼] [时间窗口▼] [区域▼] [🔍关键词]                   │
├────────┬──────────────────────────────────┬─────────────────────────────┤
│ 左图层  │ 中央主视图                        │ 右分析面板                   │
│        │                                  │                             │
│ 产业快捷 │ ┌──────────────────────────────┐│ ┌─ judgment-strip ────────┐│
│ 导航    │ │ 9 KPI MetricCards 网格        ││ │ 当前产业: 集成电路      ││
│        │ │ 3×3 布局                       ││ │ 规模↑ 企业↑ 投融资↓     ││
│ □ 市场规模│ │ 每卡: 数值 + ⓘ + 🧪          ││ │ 建议: 关注瓶颈堵点→     ││
│ □ 企业规模│ └──────────────────────────────┘│ └─────────────────────────┘│
│ □ 机构规模│                                  │                             │
│ □ 投融资  │ ┌──────────────────────────────┐│ ┌─ 热点资讯 ─────────────┐│
│ □ 区域分布│ │ 产业规模趋势 ECharts 折线图   ││ │ 🔥 AI芯片需求激增      ││
│ □ 全国分布│ │ + 企业/机构规模柱状图         ││ │ 📰 产业链重构政策发布   ││
│ □ 动态资讯│ └──────────────────────────────┘│ │ 📊 投融资季度报告       ││
│ □ 深圳要素│                                  │ └─────────────────────────┘│
│ □ 深圳分布│ ┌──────────────────────────────┐│                             │
│        │ │ 深圳产业要素 ECharts 雷达图     ││ ┌─ 快速下钻 ─────────────┐│
│        │ │ + 全国产业分布地图 Leaflet      ││ │ → 全景图谱 CP1         ││
│        │ └──────────────────────────────┘│ │ → 周期分析 CP2         ││
│        │                                  │ │ → 区域评价 CP3         ││
│        │                                  │ └─────────────────────────┘│
├────────┴──────────────────────────────────┴─────────────────────────────┤
│ PrimaryWorkbenchTabs: [概述] [全景图谱] [周期阶段] [区域评价] [关键环节]  │
│                       [瓶颈堵点] [深圳分析]                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### §4.2 五段优先级

| 段 | 内容 |
|----|------|
| ①关注什么 | 9 维度基础指标全貌 |
| ②为什么 | 产业全景态势感知，发现异常维度 |
| ③重点对象 | 规模最大/增长最快/下滑最严重的产业 |
| ④趋势/异常 | 规模趋势折线 + 同比环比异常标注 |
| ⑤下钻明细 | 跳转 CP1~CP6 各分析页 |

### 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
|------|------|------|------|------|----------|
| 产业市场规模 | float 亿 | 聚合 | ✅ | 1,250.6 亿 | `M_CHAIN_MARKET_SIZE` |
| 市场规模同比增长率 | float% | 聚合 | ✅ | 8.3% | `M_CHAIN_MARKET_YOY_GROWTH` |
| 产业企业规模 | int | 聚合 | ✅ | 3,452 | `M_CHAIN_ENTERPRISE_COUNT` |
| 企业新增数 | int | 聚合 | ✅ | 186 | `M_CHAIN_ENTERPRISE_NEW_COUNT_Y` |
| 产业机构规模 | int | 聚合 | ✅ | 128 | `M_CHAIN_ORG_COUNT` |
| 机构新增数 | int | 聚合 | ✅ | 12 | `M_CHAIN_ORG_NEW_COUNT_Y` |
| 产业投融资规模 | float 亿 | 聚合 | ✅ | 89.5 亿 | `M_CHAIN_FINANCING_SIZE` |
| 投融资同比增长率 | float% | 聚合 | ✅ | -3.2% | `M_CHAIN_FINANCING_YOY_GROWTH` |
| 全球产业区域分布 | map | 聚合 | ✅ | — | `M_CHAIN_GLOBAL_REGION_DISTRIBUTION` |
| 全国产业分布 | map | 聚合 | ✅ | — | `M_CHAIN_NATIONAL_DISTRIBUTION` |
| 产业动态资讯数 | int | 聚合 | ✅ | 67 | `M_CHAIN_NEWS_COUNT` |
| 热点资讯 TOP5 | list | 明细 | ✅ | ["AI芯片需求激增",...] | — |
| 深圳产业要素指数🔧 | float | 聚合 | ✅ | 72.5 | `M_CHAIN_SZ_ELEMENT_INDEX` |
| 深圳产业分布覆盖率 | float% | 聚合 | ✅ | 68.2% | `M_CHAIN_SZ_COVERAGE_RATE` |

### 本页 metric_id 清单

| metric_id | 中文名 | 状态 | source_tables |
|-----------|--------|------|--------------|
| `M_CHAIN_MARKET_SIZE` | 产业市场规模 | ⚠️ | `dwd_industry_chain_info` + 外部市场数据 |
| `M_CHAIN_MARKET_YOY_GROWTH` | 市场规模同比增长率 | ⚠️ | 计算字段 |
| `M_CHAIN_ENTERPRISE_COUNT` | 产业企业规模 | ✅ | `dwd_org_industry_chain_dtl` COUNT |
| `M_CHAIN_ENTERPRISE_NEW_COUNT_Y` | 企业新增数 | ✅ | `dwd_org_industry_chain_dtl` 年度新增 |
| `M_CHAIN_ORG_COUNT` | 产业机构规模 | ✅ | `dwd_org_industry_chain_dtl` 关联机构 |
| `M_CHAIN_ORG_NEW_COUNT_Y` | 机构新增数 | ✅ | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_FINANCING_SIZE` | 产业投融资规模 | ⚠️ | 外部投融资数据 |
| `M_CHAIN_FINANCING_YOY_GROWTH` | 投融资同比增长率 | ⚠️ | 计算字段 |
| `M_CHAIN_GLOBAL_REGION_DISTRIBUTION` | 全球产业区域分布 | ⚠️ | `dwd_industry_chain_info` 关联地理 |
| `M_CHAIN_NATIONAL_DISTRIBUTION` | 全国产业分布 | ✅ | `dwd_org_industry_chain_dtl` 区域聚合 |
| `M_CHAIN_NEWS_COUNT` | 产业动态资讯数 | ✅ | `dwd_industry_chain_news_info` COUNT |
| `M_CHAIN_SZ_ELEMENT_INDEX` | 深圳产业要素指数 | 🔧 | `dwd_org_industry_chain_dtl` 深圳聚合 |
| `M_CHAIN_SZ_COVERAGE_RATE` | 深圳产业分布覆盖率 | ✅ | `dwd_org_industry_chain_dtl` + `dwd_industry_chain_info` |

---

## CP1 产业链全景图谱

**路由**：`/industry/panorama`
**bid 映射**：§1.1.1.2.4.2.2.1 产业链全景图谱（结构可视化 + 节点下钻 + 动态演进）
**算法依赖**：产业链全景模型 + 深圳产业链模型

### 骨架

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TopicFilterBar [产业▼] [时间窗口▼] [区域▼] [🔍关键词]                   │
├────────┬──────────────────────────────────┬─────────────────────────────┤
│ 左图层  │ 中央主视图                        │ 右分析面板                   │
│        │                                  │                             │
│ 图层控制 │ ┌──────────────────────────────┐│ ┌─ judgment-strip ────────┐│
│        │ │                                ││ │ 集成电路产业链共 X 环节  ││
│ □ 上游  │ │  AntV G6 全景图谱              ││ │ 上游X 中游X 下游X       ││
│ □ 中游  │ │  节点: 环节名称                 ││ │ 关键环节: X 个           ││
│ □ 下游  │ │  连线: 上下游关系               ││ │ 瓶颈环节: X 个 →CP5     ││
│ □ 关键环节│ │  颜色: 节点类型/重要性           ││ └─────────────────────────┘│
│ □ 瓶颈环节│ │  尺寸: 企业数量/评分             ││                             │
│        │ │  标注: node_imp_level ★           ││ ┌─ 选中节点详情 ─────────┐│
│ 视图模式 │ │                                ││ │ 节点: 芯片设计          ││
│ ○ 全景  │ └──────────────────────────────┘│ │ 类型: 业务节点           ││
│ ○ 深圳筛选│                                  │ │ 环节: 中游              ││
│        │                                  │ │ 企业数: 42              ││
│ 演进模式 │ ┌──────────────────────────────┐│ │ 专利数: 156             ││
│ [时间轴] │ │ 时间轴演进 ECharts             ││ │ 重要性: ★★★☆☆         ││
│ ← 2020  │ │ 产业重大事件标注                ││ │ [查看关联企业→]         ││
│   2021  │ └──────────────────────────────┘│ │ [查看关联专利→]         ││
│   2022  │                                  │ └─────────────────────────┘│
│   →2026 │                                  │                             │
├────────┴──────────────────────────────────┴─────────────────────────────┤
│ PrimaryWorkbenchTabs: [概述] [全景图谱●] [周期阶段] [区域评价] [关键环节]  │
│                       [瓶颈堵点] [深圳分析]                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### §4.2 五段优先级

| 段 | 内容 |
|----|------|
| ①关注什么 | 产业链完整结构，上下游关系 |
| ②为什么 | 识别链条断点与缺失环节 |
| ③重点对象 | 关键环节（高附加值/高壁垒）、瓶颈环节 |
| ④趋势/异常 | 演进时间轴，新加入/退出的节点 |
| ⑤下钻明细 | 点击节点→产业链画像/关联企业/专利 |

### 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
|------|------|------|------|------|----------|
| 产业链名称 | string | 明细 | ✅ | 集成电路 | — |
| 产业链环节总数 | int | 聚合 | ✅ | 38 | `M_CHAIN_NODE_TOTAL_COUNT` |
| 上游环节数 | int | 聚合 | ✅ | 12 | `M_CHAIN_UPSTREAM_COUNT` |
| 中游环节数 | int | 聚合 | ✅ | 16 | `M_CHAIN_MIDSTREAM_COUNT` |
| 下游环节数 | int | 聚合 | ✅ | 10 | `M_CHAIN_DOWNSTREAM_COUNT` |
| 关键环节占比🔧 | float% | 聚合 | ✅ | 15.8% | `M_CHAIN_KEY_NODE_RATIO` |
| 关联企业总数 | int | 聚合 | ✅ | 1,245 | `M_CHAIN_RELATED_ENTERPRISE_COUNT` |
| 关联专利总数 | int | 聚合 | ✅ | 3,678 | `M_CHAIN_RELATED_PATENT_COUNT` |
| 节点名称 | string | 明细 | ✅ | 芯片设计 | — |
| 节点类型 | enum | 明细 | ✅ | 业务节点 | — |
| 节点重要性等级 | int | 明细 | ✅ | 2 | `M_CHAIN_NODE_IMP_LEVEL` |
| 节点环节(上/中/下游) | enum | 明细 | ✅ | 中游 | — |
| 节点关联企业数 | int | 聚合 | ✅ | 42 | `M_CHAIN_NODE_ENTERPRISE_COUNT` |
| 节点关联专利数 | int | 聚合 | ✅ | 156 | `M_CHAIN_NODE_PATENT_COUNT` |
| 产业链完整度🔧 | float% | 聚合 | ✅ | 72.5% | `M_CHAIN_COMPLETENESS` |
| 深圳产业链覆盖度 | float% | 聚合 | ✅ | 68.2% | `M_CHAIN_SZ_COVERAGE_RATE` |

### 本页 metric_id 清单

| metric_id | 中文名 | 状态 | source_tables |
|-----------|--------|------|--------------|
| `M_CHAIN_NODE_TOTAL_COUNT` | 产业链环节总数 | ✅ | `dwd_industry_chain_info` COUNT |
| `M_CHAIN_UPSTREAM_COUNT` | 上游环节数 | ✅ | `dwd_industry_chain_info` node_stage=1 |
| `M_CHAIN_MIDSTREAM_COUNT` | 中游环节数 | ✅ | `dwd_industry_chain_info` node_stage=2 |
| `M_CHAIN_DOWNSTREAM_COUNT` | 下游环节数 | ✅ | `dwd_industry_chain_info` node_stage=3 |
| `M_CHAIN_KEY_NODE_RATIO` | 关键环节占比 | 🔧 | `dwd_industry_chain_info` node_imp_level 计算 |
| `M_CHAIN_RELATED_ENTERPRISE_COUNT` | 关联企业总数 | ✅ | `dwd_org_industry_chain_dtl` COUNT(DISTINCT) |
| `M_CHAIN_RELATED_PATENT_COUNT` | 关联专利总数 | ✅ | `dwd_org_industry_chain_pat_dtl` COUNT(DISTINCT) |
| `M_CHAIN_NODE_IMP_LEVEL` | 节点重要性等级 | ✅ | `dwd_industry_chain_info.node_imp_level` |
| `M_CHAIN_NODE_ENTERPRISE_COUNT` | 节点关联企业数 | ✅ | `dwd_org_industry_chain_dtl` 按节点聚合 |
| `M_CHAIN_NODE_PATENT_COUNT` | 节点关联专利数 | ✅ | `dwd_org_industry_chain_pat_dtl` 按节点聚合 |
| `M_CHAIN_COMPLETENESS` | 产业链完整度 | 🔧 | `dwd_industry_chain_info` + `dwd_org_industry_chain_dtl` |
| `M_CHAIN_SZ_COVERAGE_RATE` | 深圳产业链覆盖度 | ✅ | `dwd_org_industry_chain_dtl` 深圳筛选 |

---

## CP2 产业周期与阶段

**路由**：`/industry/cycle`
**bid 映射**：§1.1.1.2.4.2.2.2 产业周期分析 + 产业阶段分析
**算法依赖**：产业周期分析模型 + 产业阶段分析模型 + 产业发展路线历程模型

### 骨架

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TopicFilterBar [产业▼] [时间窗口▼] [区域▼] [🔍关键词]                   │
├────────┬──────────────────────────────────┬─────────────────────────────┤
│ 左图层  │ 中央主视图                        │ 右分析面板                   │
│        │                                  │                             │
│ 周期阶段 │ ┌──────────────────────────────┐│ ┌─ judgment-strip ────────┐│
│ 导航    │ │  产业生命周期曲线               ││ │ 集成电路处于【成长期】   ││
│        │ │  ECharts 面积图               ││ │ 增长率>15% 持续3年      ││
│ □ 起始期│ │  X轴:时间 Y轴:规模/增长率      ││ │ 建议: 关注产能扩张风险  ││
│ □ 成长期│ │  标注当前阶段位置               ││ └─────────────────────────┘│
│ □ 成熟期│ └──────────────────────────────┘│                             │
│ □ 衰退期│                                  │ ┌─ 周期判定依据 ─────────┐│
│        │ ┌──────────────────────────────┐│ │ 市场规模: 1250亿 ↑     ││
│ 对标产业│ │  产业阶段仪表盘                ││ │ 增长率: 15.2% ↑        ││
│ □ 5G   │ │  雷达图: 多指标阶段判定        ││ │ 利润率: 8.6% →         ││
│ □ AI   │ │  + 阶段仪表盘 ECharts gauge   ││ │ 创新活跃度: 高 ↑        ││
│ □ 新能源│ └──────────────────────────────┘│ │ [周期模型参数配置→]     ││
│        │                                  │ └─────────────────────────┘│
│ 路线历程│ ┌──────────────────────────────┐│                             │
│ [时间轴] │ │  发展路线历程 ECharts 时间轴   ││ ┌─ 趋势预测 ─────────────┐│
│        │ │  重大事件标记 + 驱动因素        ││ │ 预计2027进入成熟期      ││
│        │ │  + 拐点预测虚线                ││ │ 关键驱动: AI芯片需求    ││
│        │ └──────────────────────────────┘│ │ 潜在拐点: 技术替代风险  ││
│        │                                  │ └─────────────────────────┘│
├────────┴──────────────────────────────────┴─────────────────────────────┤
│ PrimaryWorkbenchTabs: [概述] [全景图谱] [周期阶段●] [区域评价] [关键环节]  │
│ SecondaryTabs: [周期分析] [阶段判定] [路线历程]                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### §4.2 五段优先级

| 段 | 内容 |
|----|------|
| ①关注什么 | 产业当前所处周期阶段 |
| ②为什么 | 判断投资节奏与政策窗口期 |
| ③重点对象 | 处于拐点附近的产业，增长/衰退异常产业 |
| ④趋势/异常 | 周期趋势预测，拐点预警 |
| ⑤下钻明细 | 查看历史重大事件 → 路线历程详情 |

### 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
|------|------|------|------|------|----------|
| 产业名称 | string | 明细 | ✅ | 集成电路 | — |
| 当前周期阶段🔧 | enum | 聚合 | ✅ | 成长期 | `M_CHAIN_CYCLE_STAGE` |
| 市场规模 | float 亿 | 聚合 | ✅ | 1,250.6 | `M_CHAIN_MARKET_SIZE` |
| 增长率 | float% | 聚合 | ✅ | 15.2% | `M_CHAIN_GROWTH_RATE` |
| 利润率⚠️ | float% | 聚合 | ✅ | 8.6% | `M_CHAIN_PROFIT_MARGIN` |
| 创新活跃度🔧 | float | 聚合 | ✅ | 0.82 | `M_CHAIN_INNOVATION_ACTIVITY` |
| 产业成熟度指数🔧 | float | 聚合 | ✅ | 0.65 | `M_CHAIN_MATURITY_INDEX` |
| 预测下一拐点年份🔧 | int | 聚合 | ✅ | 2027 | `M_CHAIN_INFLECTION_YEAR` |
| 发展路线重大事件数 | int | 聚合 | ✅ | 23 | `M_CHAIN_MILESTONE_EVENT_COUNT` |
| 周期模型置信度🔧 | float% | 聚合 | ✅ | 78.5% | `M_CHAIN_CYCLE_CONFIDENCE` |
| 对标产业周期对比 | list | 聚合 | ✅ | [{name:"5G",stage:"成熟期"}] | `M_CHAIN_CYCLE_BENCHMARK` |

### 本页 metric_id 清单

| metric_id | 中文名 | 状态 | source_tables |
|-----------|--------|------|--------------|
| `M_CHAIN_CYCLE_STAGE` | 当前周期阶段 | 🔧 | 产业周期分析模型输出 |
| `M_CHAIN_MARKET_SIZE` | 市场规模 | ⚠️ | 外部市场数据 |
| `M_CHAIN_GROWTH_RATE` | 增长率 | ⚠️ | 计算字段 |
| `M_CHAIN_PROFIT_MARGIN` | 利润率 | ⚠️ | 外部财报数据 |
| `M_CHAIN_INNOVATION_ACTIVITY` | 创新活跃度 | 🔧 | `dwd_org_industry_chain_pat_dtl` + 模型 |
| `M_CHAIN_MATURITY_INDEX` | 产业成熟度指数 | 🔧 | 多维度综合计算 |
| `M_CHAIN_INFLECTION_YEAR` | 预测拐点年份 | 🔧 | 周期趋势模拟预测模型 |
| `M_CHAIN_MILESTONE_EVENT_COUNT` | 重大事件数 | ✅ | `dwd_industry_chain_news_info` |
| `M_CHAIN_CYCLE_CONFIDENCE` | 周期模型置信度 | 🔧 | 模型输出 |
| `M_CHAIN_CYCLE_BENCHMARK` | 对标产业周期对比 | 🔧 | 多产业周期模型输出 |

---

## CP3 区域产业指数评价

**路由**：`/industry/regional-evaluation`
**bid 映射**：§1.1.1.2.4.2.2.3 区域产业指数评价 + §1.1.1.2.4.2.2.8 区域产业竞争力评价
**算法依赖**：区域产业指数模型

### 骨架

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TopicFilterBar [产业▼] [时间窗口▼] [区域▼] [🔍关键词]                   │
├────────┬──────────────────────────────────┬─────────────────────────────┤
│ 左图层  │ 中央主视图                        │ 右分析面板                   │
│        │                                  │                             │
│ 评价维度 │ ┌──────────────────────────────┐│ ┌─ judgment-strip ────────┐│
│ □ 企业能力│ │  区域产业指数热力图             ││ │ 深圳集成电路指数 72.5    ││
│ □ 学术生态│ │  Leaflet 地图 + 热力层         ││ │ 排名: 全国第3           ││
│ □ 配套生态│ │  + 气泡大小=指数值             ││ │ 优势: 企业能力↑         ││
│        │ └──────────────────────────────┘│ │ 短板: 配套生态↓          ││
│ 指标配置 │                                  │ └─────────────────────────┘│
│ [权重滑块]│ ┌──────────────────────────────┐│                             │
│ 企业能力  │ │  多区域对比柱状图               ││ ┌─ 指标体系配置 ─────────┐│
│ ──●──── │ │  ECharts 横向柱状              ││ │ 三大维度:               ││
│ 学术生态  │ │  X轴:指数 Y轴:区域              ││ │ ☑ 企业能力 w=0.4       ││
│ ────●── │ │  颜色:三维度堆叠                ││ │ ☑ 学术生态 w=0.3       ││
│ 配套生态  │ └──────────────────────────────┘│ │ ☑ 配套生态 w=0.3       ││
│ ──●──── │                                  │ │ [重置] [应用]           ││
│        │ ┌──────────────────────────────┐│ └─────────────────────────┘│
│ 对比区域 │ │  竞争力雷达图                   ││                             │
│ ☑ 深圳  │ │  ECharts 雷达                  ││ ┌─ 竞争力排名 ──────────┐│
│ ☑ 北京  │ │  多区域叠加对比                 ││ │ 1. 北京 85.2           ││
│ ☑ 上海  │ └──────────────────────────────┘│ │ 2. 上海 78.6           ││
│ ☑ 苏州  │                                  │ │ 3. 深圳 72.5           ││
│ ☑ 广州  │                                  │ │ ...                    ││
│        │                                  │ └─────────────────────────┘│
├────────┴──────────────────────────────────┴─────────────────────────────┤
│ PrimaryWorkbenchTabs: [概述] [全景图谱] [周期阶段] [区域评价●] [关键环节]  │
│ SecondaryTabs: [区域指数] [竞争力评价]                                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### §4.2 五段优先级

| 段 | 内容 |
|----|------|
| ①关注什么 | 各区域产业指数与竞争力排名 |
| ②为什么 | 识别区域优势与短板，支撑政策制定 |
| ③重点对象 | 指数最高/最低区域，排名跃升/下降区域 |
| ④趋势/异常 | 指数时序变化，异常波动 |
| ⑤下钻明细 | 选区域→CP6 深圳分析 / 查看区域内企业 |

### 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
|------|------|------|------|------|----------|
| 区域名称 | string | 明细 | ✅ | 深圳 | — |
| 区域产业综合指数🔧 | float | 聚合 | ✅ | 72.5 | `M_CHAIN_REGIONAL_INDEX` |
| 企业能力竞争力🔧 | float | 聚合 | ✅ | 0.78 | `M_CHAIN_REGIONAL_ENTERPRISE_POWER` |
| 学术生态竞争力🔧 | float | 聚合 | ✅ | 0.65 | `M_CHAIN_REGIONAL_ACADEMIC_ECO` |
| 配套生态竞争力🔧 | float | 聚合 | ✅ | 0.71 | `M_CHAIN_REGIONAL_SUPPORT_ECO` |
| 综合竞争力排名🔧 | int | 聚合 | ✅ | 3 | `M_CHAIN_COMPETITIVENESS_RANK` |
| 竞争力指数🔧 | float | 聚合 | ✅ | 72.5 | `M_CHAIN_COMPETITIVENESS_SCORE` |
| 短板维度 | string | 聚合 | ✅ | 配套生态 | `M_CHAIN_SHORTBOARD_DIM` |
| 指数时序变化 | list | 聚合 | ✅ | [{year:2024,val:68.3}] | `M_CHAIN_REGIONAL_INDEX_TREND` |

### 本页 metric_id 清单

| metric_id | 中文名 | 状态 | source_tables |
|-----------|--------|------|--------------|
| `M_CHAIN_REGIONAL_INDEX` | 区域产业综合指数 | 🔧 | 区域产业指数模型 |
| `M_CHAIN_REGIONAL_ENTERPRISE_POWER` | 企业能力竞争力 | 🔧 | `dwd_org_industry_chain_dtl` 聚合 |
| `M_CHAIN_REGIONAL_ACADEMIC_ECO` | 学术生态竞争力 | 🔧 | `dwd_org_industry_chain_pat_dtl` + 机构数据 |
| `M_CHAIN_REGIONAL_SUPPORT_ECO` | 配套生态竞争力 | 🔧 | 多维度综合 |
| `M_CHAIN_COMPETITIVENESS_RANK` | 综合竞争力排名 | 🔧 | 模型输出排名 |
| `M_CHAIN_COMPETITIVENESS_SCORE` | 竞争力指数 | 🔧 | 多维度加权 |
| `M_CHAIN_SHORTBOARD_DIM` | 短板维度 | 🔧 | 三维度对比 |
| `M_CHAIN_REGIONAL_INDEX_TREND` | 指数时序变化 | 🔧 | 历年指数时序 |

---

## CP4 产业关键环节识别

**路由**：`/industry/key-nodes`
**bid 映射**：§1.1.1.2.4.2.2.4 产业关键环节识别
**算法依赖**：产业链关键环节识别模型

### 骨架

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TopicFilterBar [产业▼] [时间窗口▼] [区域▼] [🔍关键词]                   │
├────────┬──────────────────────────────────┬─────────────────────────────┤
│ 左图层  │ 中央主视图                        │ 右分析面板                   │
│        │                                  │                             │
│ 环节层级 │ ┌──────────────────────────────┐│ ┌─ judgment-strip ────────┐│
│        │ │  全链路环节结构化拆解            ││ │ 集成电路关键环节 X 个    ││
│ □ 研发  │ │  横向流程图                    ││ │ 最高端化: 光刻机(92.5)  ││
│ □ 设计  │ │  上游→中游→下游               ││ │ 建议优先布局: 光刻设备   ││
│ □ 制造  │ │  节点: 环节名称                ││ └─────────────────────────┘│
│ □ 销售  │ │  颜色: 高端化指数梯度色        ││                             │
│ □ 服务  │ │  标注: ★关键环节              ││ ┌─ 选中环节分析 ─────────┐│
│        │ │  尺寸: 附加值/技术壁垒          ││ │ 环节: 光刻机            ││
│ 筛选    │ └──────────────────────────────┘│ │ 高端化指数: 92.5 🔧      ││
│ □ 仅关键│                                  │ │ 技术壁垒: 高             ││
│ □ 仅瓶颈│ ┌──────────────────────────────┐│ │ 附加值: 极高             ││
│        │ │  关键环节高端化指数排名          ││ │ 市场集中度: 高           ││
│        │ │  ECharts 横向柱状              ││ │ 代表企业: ASML, ...     ││
│        │ │  + 竞争格局/代表企业           ││ │ 技术趋势: EUV→High-NA   ││
│        │ └──────────────────────────────┘│ │ [查看关联企业→]          ││
│        │                                  │ │ [查看技术趋势→]          ││
│        │                                  │ └─────────────────────────┘│
├────────┴──────────────────────────────────┴─────────────────────────────┤
│ PrimaryWorkbenchTabs: [概述] [全景图谱] [周期阶段] [区域评价] [关键环节●]  │
│ SecondaryTabs: [环节结构] [关键环节分析]                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### §4.2 五段优先级

| 段 | 内容 |
|----|------|
| ①关注什么 | 产业链中高价值关键环节 |
| ②为什么 | 聚焦资源投入核心环节，优化产业链布局 |
| ③重点对象 | 高端化指数 TOP5 环节，技术壁垒最高环节 |
| ④趋势/异常 | 关键环节技术替代趋势，价值变动 |
| ⑤下钻明细 | 选环节→查看代表企业/专利/技术趋势 |

### 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
|------|------|------|------|------|----------|
| 环节名称 | string | 明细 | ✅ | 光刻机 | — |
| 环节层级 | enum | 明细 | ✅ | 中游 | — |
| 高端化指数🔧 | float | 聚合 | ✅ | 92.5 | `M_CHAIN_HIGHEND_INDEX` |
| 技术壁垒等级🔧 | enum | 聚合 | ✅ | 高 | `M_CHAIN_TECH_BARRIER_LEVEL` |
| 附加值率⚠️ | float% | 聚合 | ✅ | 45.2% | `M_CHAIN_VALUE_ADDED_RATE` |
| 市场集中度⚠️ | float | 聚合 | ✅ | 0.85 | `M_CHAIN_MARKET_CONCENTRATION` |
| 关键环节标识🔧 | bool | 聚合 | ✅ | true | `M_CHAIN_IS_KEY_NODE` |
| 代表企业 | list | 明细 | ✅ | ["ASML","上海微电子"] | — |
| 专利数量 | int | 聚合 | ✅ | 234 | `M_CHAIN_NODE_PATENT_COUNT` |
| 技术趋势 | string | 明细 | ✅ | EUV→High-NA | — |

### 本页 metric_id 清单

| metric_id | 中文名 | 状态 | source_tables |
|-----------|--------|------|--------------|
| `M_CHAIN_HIGHEND_INDEX` | 高端化指数 | 🔧 | 关键环节识别模型 |
| `M_CHAIN_TECH_BARRIER_LEVEL` | 技术壁垒等级 | 🔧 | 模型输出 |
| `M_CHAIN_VALUE_ADDED_RATE` | 附加值率 | ⚠️ | 外部财务数据 |
| `M_CHAIN_MARKET_CONCENTRATION` | 市场集中度 | ⚠️ | 外部市场数据 |
| `M_CHAIN_IS_KEY_NODE` | 关键环节标识 | 🔧 | 模型输出 |
| `M_CHAIN_NODE_PATENT_COUNT` | 专利数量 | ✅ | `dwd_org_industry_chain_pat_dtl` |

---

## CP5 产业瓶颈堵点识别

**路由**：`/industry/problem-diagnosis`
**bid 映射**：§1.1.1.2.4.2.2.5 产业瓶颈堵点识别
**算法依赖**：产业瓶颈堵点识别模型

### 骨架

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TopicFilterBar [产业▼] [时间窗口▼] [区域▼] [🔍关键词]                   │
├────────┬──────────────────────────────────┬─────────────────────────────┤
│ 左图层  │ 中央主视图                        │ 右分析面板                   │
│        │                                  │                             │
│ 瓶颈维度 │ ┌──────────────────────────────┐│ ┌─ judgment-strip ────────┐│
│ □ 技术  │ │  多维瓶颈健康度矩阵             ││ │ 集成电路瓶颈 X 个       ││
│ □ 人才  │ │  ECharts 热力图                ││ │ 最严重: 光刻设备(技术)  ││
│ □ 市场  │ │  X轴:环节 Y轴:维度             ││ │ 建议: 加速国产替代路径  ││
│ □ 资金  │ │  颜色: 健康度评分(红=差)       ││ └─────────────────────────┘│
│ □ 政策  │ └──────────────────────────────┘│                             │
│        │                                  │ ┌─ 瓶颈详情 ─────────────┐│
│ 严重度  │ ┌──────────────────────────────┐│ │ 环节: 光刻设备          ││
│ □ 高   │ │  瓶颈环节时序趋势              ││ │ 瓶颈类型: 技术          ││
│ □ 中   │ │  ECharts 折线图               ││ │ 严重度: 高              ││
│ □ 低   │ │  多维度趋势叠加                ││ │ 成因: 核心技术被垄断    ││
│        │ │  + 瓶颈标记线                  ││ │ 影响: 产业链上游受限    ││
│        │ └──────────────────────────────┘│ │ 建议: 加速国产替代      ││
│        │                                  │ │ [查看归因报告→]         ││
│        │ ┌──────────────────────────────┐│ └─────────────────────────┘│
│        │ │  瓶颈归因与建议                ││                             │
│        │ │  ECharts 桑基图               ││ ┌─ 改进建议 ─────────────┐│
│        │ │  瓶颈→原因→建议               ││ │ 1. 加速国产替代          ││
│        │ └──────────────────────────────┘│ │ 2. 引进海外人才          ││
│        │                                  │ │ 3. 设立专项基金          ││
│        │                                  │ └─────────────────────────┘│
├────────┴──────────────────────────────────┴─────────────────────────────┤
│ PrimaryWorkbenchTabs: [概述] [全景图谱] [周期阶段] [区域评价] [关键环节]  │
│                       [瓶颈堵点●] [深圳分析]                               │
│ SecondaryTabs: [健康度矩阵] [瓶颈识别] [归因建议]                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### §4.2 五段优先级

| 段 | 内容 |
|----|------|
| ①关注什么 | 产业链各环节瓶颈堵点 |
| ②为什么 | 精准定位"卡脖子"环节，制定靶向方案 |
| ③重点对象 | 高严重度瓶颈环节，多维度同时薄弱环节 |
| ④趋势/异常 | 瓶颈恶化/改善趋势，新增瓶颈预警 |
| ⑤下钻明细 | 选瓶颈→归因分析→改进建议→CP6 深圳短板 |

### 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
|------|------|------|------|------|----------|
| 环节名称 | string | 明细 | ✅ | 光刻设备 | — |
| 瓶颈维度 | enum | 聚合 | ✅ | 技术 | `M_CHAIN_BOTTLENECK_DIM` |
| 健康度评分🔧 | float | 聚合 | ✅ | 32.5 | `M_CHAIN_HEALTH_SCORE` |
| 瓶颈严重度🔧 | enum | 聚合 | ✅ | 高 | `M_CHAIN_BOTTLENECK_SEVERITY` |
| 瓶颈成因 | string | 明细 | ✅ | 核心技术被海外垄断 | — |
| 影响范围🔧 | string | 明细 | ✅ | 产业链上游受限 | `M_CHAIN_BOTTLENECK_IMPACT` |
| 技术成熟度⚠️ | float | 聚合 | ✅ | 0.35 | `M_CHAIN_TECH_MATURITY` |
| 人才供给量⚠️ | float | 聚合 | ✅ | 0.42 | `M_CHAIN_TALENT_SUPPLY` |
| 融资事件数 | int | 聚合 | ✅ | 3 | `M_CHAIN_FINANCING_EVENT_COUNT` |
| 政策覆盖率🔧 | float% | 聚合 | ✅ | 25.0% | `M_CHAIN_POLICY_COVERAGE` |
| 改进建议 | list | 明细 | ✅ | ["加速国产替代",...] | — |
| 瓶颈趋势 | list | 聚合 | ✅ | [{year:2024,score:32.5}] | `M_CHAIN_BOTTLENECK_TREND` |

### 本页 metric_id 清单

| metric_id | 中文名 | 状态 | source_tables |
|-----------|--------|------|--------------|
| `M_CHAIN_BOTTLENECK_DIM` | 瓶颈维度 | 🔧 | 模型输出 |
| `M_CHAIN_HEALTH_SCORE` | 健康度评分 | 🔧 | 瓶颈堵点识别模型 |
| `M_CHAIN_BOTTLENECK_SEVERITY` | 瓶颈严重度 | 🔧 | 模型输出 |
| `M_CHAIN_BOTTLENECK_IMPACT` | 影响范围 | 🔧 | 模型输出 |
| `M_CHAIN_TECH_MATURITY` | 技术成熟度 | ⚠️ | 外部技术评估数据 |
| `M_CHAIN_TALENT_SUPPLY` | 人才供给量 | ⚠️ | 外部人才数据 |
| `M_CHAIN_FINANCING_EVENT_COUNT` | 融资事件数 | ⚠️ | 外部投融资数据 |
| `M_CHAIN_POLICY_COVERAGE` | 政策覆盖率 | 🔧 | 政策数据关联计算 |
| `M_CHAIN_BOTTLENECK_TREND` | 瓶颈趋势 | 🔧 | 时序计算 |

---

## CP6 深圳产业分析对比

**路由**：`/industry/shenzhen-analysis`
**bid 映射**：§1.1.1.2.4.2.2.6 深圳产业情况分析对比 + §1.1.1.2.4.2.2.7 深圳产业发展分析
**算法依赖**：深圳产业优势识别模型 + 深圳问题识别模型 + 深圳机遇分析模型 + 重点布局产业推荐模型

### 骨架

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TopicFilterBar [产业▼] [时间窗口▼] [区域▼] [🔍关键词]                   │
├────────┬──────────────────────────────────┬─────────────────────────────┤
│ 左图层  │ 中央主视图                        │ 右分析面板                   │
│        │                                  │                             │
│ 分析维度 │ ┌──────────────────────────────┐│ ┌─ judgment-strip ────────┐│
│ □ 优势  │ │  深圳产业多维度对标             ││ │ 深圳集成电路:           ││
│ □ 问题  │ │  ECharts 雷达图叠加            ││ │ 优势: 产业规模↑ 创新活跃││
│ □ 机遇  │ │  深圳 vs 北京 vs 上海 vs 苏州  ││ │ 短板: 配套生态↓         ││
│ □ 推荐  │ │  多维度: 规模/创新/配套/...    ││ │ 建议: 强化配套服务      ││
│        │ └──────────────────────────────┘│ └─────────────────────────┘│
│ 对标城市 │                                  │                             │
│ ☑ 北京  │ ┌──────────────────────────────┐│ ┌─ 深圳优势 ─────────────┐│
│ ☑ 上海  │ │  深圳产业发展阶段判断           ││ │ 产业规模: 全国第2      ││
│ ☑ 苏州  │ │  生命周期曲线 + 深圳标注       ││ │ 创新活跃度: 全国第1    ││
│ ☑ 广州  │ │  + 潜力评估仪表盘              ││ │ 投融资: 全国第3        ││
│        │ └──────────────────────────────┘│ └─────────────────────────┘│
│        │                                  │                             │
│ 发展分析 │ ┌──────────────────────────────┐│ ┌─ 发展建议 ─────────────┐│
│ Tab    │ │  智能建议与发展路径              ││ │ 🔧 1. 加速光刻设备国产 ││
│        │ │  ECharts 路径图/桑基图         ││ │ 🔧 2. 引进EDA工具人才  ││
│        │ │  优势→机遇→策略→布局           ││ │ 🔧 3. 布局先进封装     ││
│        │ └──────────────────────────────┘│ │ [生成发展报告→]         ││
│        │                                  │ └─────────────────────────┘│
│        │ ┌──────────────────────────────┐│                             │
│        │ │  重点布局产业推荐              ││ ┌─ 推荐产业 ─────────────┐│
│        │ │  ECharts 气泡图               ││ │ 🔧 1. 先进封装(92.5)   ││
│        │ │  X轴:推荐指数 Y轴:增长率      ││ │ 🔧 2. 汽车芯片(87.3)   ││
│        │ │  气泡:产业规模                ││ │ 🔧 3. AI芯片(85.1)     ││
│        │ └──────────────────────────────┘│ └─────────────────────────┘│
├────────┴──────────────────────────────────┴─────────────────────────────┤
│ PrimaryWorkbenchTabs: [概述] [全景图谱] [周期阶段] [区域评价] [关键环节]  │
│                       [瓶颈堵点] [深圳分析●]                               │
│ SecondaryTabs: [多维对标] [发展分析] [机遇推荐]                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### §4.2 五段优先级

| 段 | 内容 |
|----|------|
| ①关注什么 | 深圳产业的相对优势与短板 |
| ②为什么 | 客观定位深圳产业能级，支撑差异化战略 |
| ③重点对象 | 深圳优势领域、严重短板领域、高潜力领域 |
| ④趋势/异常 | 深圳位次变化、新兴机遇、恶化风险 |
| ⑤下钻明细 | 选优势→企业列表 / 选短板→CP5 归因 / 选推荐→布局策略 |

### 字段表

| 名称 | 类型 | 来源 | 必填 | 示例 | metric_id |
|------|------|------|------|------|----------|
| 产业名称 | string | 明细 | ✅ | 集成电路 | — |
| 深圳产业规模排名 | int | 聚合 | ✅ | 2 | `M_CHAIN_SZ_SCALE_RANK` |
| 深圳产业优势评分🔧 | float | 聚合 | ✅ | 82.5 | `M_CHAIN_SZ_ADVANTAGE_SCORE` |
| 深圳创新活跃度🔧 | float | 聚合 | ✅ | 0.91 | `M_CHAIN_SZ_INNOVATION_SCORE` |
| 深圳产业链完整度🔧 | float% | 聚合 | ✅ | 68.2% | `M_CHAIN_SZ_COMPLETENESS` |
| 深圳配套生态评分🔧 | float | 聚合 | ✅ | 0.55 | `M_CHAIN_SZ_SUPPORT_SCORE` |
| 深圳问题识别结果🔧 | list | 聚合 | ✅ | ["配套生态薄弱"] | `M_CHAIN_SZ_PROBLEM_LIST` |
| 发展阶段判断🔧 | enum | 聚合 | ✅ | 成长后期 | `M_CHAIN_SZ_DEV_STAGE` |
| 产业化潜力🔧 | float | 聚合 | ✅ | 0.78 | `M_CHAIN_SZ_POTENTIAL` |
| 智能建议列表🔧 | list | 明细 | ✅ | ["加速国产替代"] | — |
| 发展路径方案🔧 | list | 明细 | ✅ | [{phase:"短期",action:"..."}] | — |
| 机遇推荐指数🔧 | float | 聚合 | ✅ | 85.1 | `M_CHAIN_OPPORTUNITY_INDEX` |
| 重点布局推荐排名🔧 | int | 聚合 | ✅ | 3 | `M_CHAIN_LAYOUT_RECOMMEND_RANK` |
| 重点布局产业🔧 | string | 明细 | ✅ | AI芯片 | `M_CHAIN_LAYOUT_INDUSTRY` |

### 本页 metric_id 清单

| metric_id | 中文名 | 状态 | source_tables |
|-----------|--------|------|--------------|
| `M_CHAIN_SZ_SCALE_RANK` | 深圳产业规模排名 | ✅ | `dwd_org_industry_chain_dtl` 深圳聚合 |
| `M_CHAIN_SZ_ADVANTAGE_SCORE` | 深圳产业优势评分 | 🔧 | 深圳产业优势识别模型 |
| `M_CHAIN_SZ_INNOVATION_SCORE` | 深圳创新活跃度 | 🔧 | `dwd_org_industry_chain_pat_dtl` + 模型 |
| `M_CHAIN_SZ_COMPLETENESS` | 深圳产业链完整度 | 🔧 | `dwd_industry_chain_info` + `dwd_org_industry_chain_dtl` |
| `M_CHAIN_SZ_SUPPORT_SCORE` | 深圳配套生态评分 | 🔧 | 多维度综合 |
| `M_CHAIN_SZ_PROBLEM_LIST` | 深圳问题识别结果 | 🔧 | 深圳问题识别模型 |
| `M_CHAIN_SZ_DEV_STAGE` | 发展阶段判断 | 🔧 | 产业阶段分析模型 |
| `M_CHAIN_SZ_POTENTIAL` | 产业化潜力 | 🔧 | 深圳机遇分析模型 |
| `M_CHAIN_OPPORTUNITY_INDEX` | 机遇推荐指数 | 🔧 | 深圳机遇分析模型 |
| `M_CHAIN_LAYOUT_RECOMMEND_RANK` | 重点布局推荐排名 | 🔧 | 重点布局产业推荐模型 |
| `M_CHAIN_LAYOUT_INDUSTRY` | 重点布局产业 | 🔧 | 重点布局产业推荐模型 |

---

## 全模块 metric_id 汇总

> 全部前缀 `M_CHAIN_`；🔧 = 待算法实现，⚠️ = 待甲方确认数据来源，✅ = 可直查 ODS，❌ = 无来源

| metric_id | 中文名 | 状态 | 所在页面 | source_tables |
|-----------|--------|------|---------|--------------|
| `M_CHAIN_MARKET_SIZE` | 产业市场规模 | ⚠️ | CP0 | 外部市场数据 |
| `M_CHAIN_MARKET_YOY_GROWTH` | 市场规模同比增长率 | ⚠️ | CP0 | 计算字段 |
| `M_CHAIN_ENTERPRISE_COUNT` | 产业企业规模 | ✅ | CP0 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_ENTERPRISE_NEW_COUNT_Y` | 企业新增数 | ✅ | CP0 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_ORG_COUNT` | 产业机构规模 | ✅ | CP0 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_ORG_NEW_COUNT_Y` | 机构新增数 | ✅ | CP0 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_FINANCING_SIZE` | 产业投融资规模 | ⚠️ | CP0 | 外部投融资数据 |
| `M_CHAIN_FINANCING_YOY_GROWTH` | 投融资同比增长率 | ⚠️ | CP0 | 计算字段 |
| `M_CHAIN_GLOBAL_REGION_DISTRIBUTION` | 全球产业区域分布 | ⚠️ | CP0 | 地理关联 |
| `M_CHAIN_NATIONAL_DISTRIBUTION` | 全国产业分布 | ✅ | CP0 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_NEWS_COUNT` | 产业动态资讯数 | ✅ | CP0 | `dwd_industry_chain_news_info` |
| `M_CHAIN_SZ_ELEMENT_INDEX` | 深圳产业要素指数 | 🔧 | CP0 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_SZ_COVERAGE_RATE` | 深圳产业分布覆盖率 | ✅ | CP0,CP1 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_NODE_TOTAL_COUNT` | 产业链环节总数 | ✅ | CP1 | `dwd_industry_chain_info` |
| `M_CHAIN_UPSTREAM_COUNT` | 上游环节数 | ✅ | CP1 | `dwd_industry_chain_info` |
| `M_CHAIN_MIDSTREAM_COUNT` | 中游环节数 | ✅ | CP1 | `dwd_industry_chain_info` |
| `M_CHAIN_DOWNSTREAM_COUNT` | 下游环节数 | ✅ | CP1 | `dwd_industry_chain_info` |
| `M_CHAIN_KEY_NODE_RATIO` | 关键环节占比 | 🔧 | CP1 | `dwd_industry_chain_info` |
| `M_CHAIN_RELATED_ENTERPRISE_COUNT` | 关联企业总数 | ✅ | CP1 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_RELATED_PATENT_COUNT` | 关联专利总数 | ✅ | CP1 | `dwd_org_industry_chain_pat_dtl` |
| `M_CHAIN_NODE_IMP_LEVEL` | 节点重要性等级 | ✅ | CP1 | `dwd_industry_chain_info.node_imp_level` |
| `M_CHAIN_NODE_ENTERPRISE_COUNT` | 节点关联企业数 | ✅ | CP1 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_NODE_PATENT_COUNT` | 节点关联专利数 | ✅ | CP1,CP4 | `dwd_org_industry_chain_pat_dtl` |
| `M_CHAIN_COMPLETENESS` | 产业链完整度 | 🔧 | CP1 | 多表综合 |
| `M_CHAIN_CYCLE_STAGE` | 当前周期阶段 | 🔧 | CP2 | 产业周期分析模型 |
| `M_CHAIN_GROWTH_RATE` | 增长率 | ⚠️ | CP2 | 计算字段 |
| `M_CHAIN_PROFIT_MARGIN` | 利润率 | ⚠️ | CP2 | 外部财报数据 |
| `M_CHAIN_INNOVATION_ACTIVITY` | 创新活跃度 | 🔧 | CP2 | `dwd_org_industry_chain_pat_dtl` |
| `M_CHAIN_MATURITY_INDEX` | 产业成熟度指数 | 🔧 | CP2 | 多维度综合 |
| `M_CHAIN_INFLECTION_YEAR` | 预测拐点年份 | 🔧 | CP2 | 周期趋势模型 |
| `M_CHAIN_MILESTONE_EVENT_COUNT` | 重大事件数 | ✅ | CP2 | `dwd_industry_chain_news_info` |
| `M_CHAIN_CYCLE_CONFIDENCE` | 周期模型置信度 | 🔧 | CP2 | 模型输出 |
| `M_CHAIN_CYCLE_BENCHMARK` | 对标产业周期对比 | 🔧 | CP2 | 多产业模型 |
| `M_CHAIN_REGIONAL_INDEX` | 区域产业综合指数 | 🔧 | CP3 | 区域产业指数模型 |
| `M_CHAIN_REGIONAL_ENTERPRISE_POWER` | 企业能力竞争力 | 🔧 | CP3 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_REGIONAL_ACADEMIC_ECO` | 学术生态竞争力 | 🔧 | CP3 | `dwd_org_industry_chain_pat_dtl` |
| `M_CHAIN_REGIONAL_SUPPORT_ECO` | 配套生态竞争力 | 🔧 | CP3 | 多维度综合 |
| `M_CHAIN_COMPETITIVENESS_RANK` | 综合竞争力排名 | 🔧 | CP3 | 模型排名 |
| `M_CHAIN_COMPETITIVENESS_SCORE` | 竞争力指数 | 🔧 | CP3 | 多维度加权 |
| `M_CHAIN_SHORTBOARD_DIM` | 短板维度 | 🔧 | CP3 | 模型输出 |
| `M_CHAIN_REGIONAL_INDEX_TREND` | 指数时序变化 | 🔧 | CP3 | 历年指数 |
| `M_CHAIN_HIGHEND_INDEX` | 高端化指数 | 🔧 | CP4 | 关键环节识别模型 |
| `M_CHAIN_TECH_BARRIER_LEVEL` | 技术壁垒等级 | 🔧 | CP4 | 模型输出 |
| `M_CHAIN_VALUE_ADDED_RATE` | 附加值率 | ⚠️ | CP4 | 外部财务数据 |
| `M_CHAIN_MARKET_CONCENTRATION` | 市场集中度 | ⚠️ | CP4 | 外部市场数据 |
| `M_CHAIN_IS_KEY_NODE` | 关键环节标识 | 🔧 | CP4 | 模型输出 |
| `M_CHAIN_BOTTLENECK_DIM` | 瓶颈维度 | 🔧 | CP5 | 模型输出 |
| `M_CHAIN_HEALTH_SCORE` | 健康度评分 | 🔧 | CP5 | 瓶颈识别模型 |
| `M_CHAIN_BOTTLENECK_SEVERITY` | 瓶颈严重度 | 🔧 | CP5 | 模型输出 |
| `M_CHAIN_BOTTLENECK_IMPACT` | 影响范围 | 🔧 | CP5 | 模型输出 |
| `M_CHAIN_TECH_MATURITY` | 技术成熟度 | ⚠️ | CP5 | 外部技术评估 |
| `M_CHAIN_TALENT_SUPPLY` | 人才供给量 | ⚠️ | CP5 | 外部人才数据 |
| `M_CHAIN_FINANCING_EVENT_COUNT` | 融资事件数 | ⚠️ | CP5 | 外部投融资数据 |
| `M_CHAIN_POLICY_COVERAGE` | 政策覆盖率 | 🔧 | CP5 | 政策数据关联 |
| `M_CHAIN_BOTTLENECK_TREND` | 瓶颈趋势 | 🔧 | CP5 | 时序计算 |
| `M_CHAIN_SZ_SCALE_RANK` | 深圳产业规模排名 | ✅ | CP6 | `dwd_org_industry_chain_dtl` |
| `M_CHAIN_SZ_ADVANTAGE_SCORE` | 深圳产业优势评分 | 🔧 | CP6 | 深圳优势识别模型 |
| `M_CHAIN_SZ_INNOVATION_SCORE` | 深圳创新活跃度 | 🔧 | CP6 | `dwd_org_industry_chain_pat_dtl` |
| `M_CHAIN_SZ_COMPLETENESS` | 深圳产业链完整度 | 🔧 | CP6 | 多表综合 |
| `M_CHAIN_SZ_SUPPORT_SCORE` | 深圳配套生态评分 | 🔧 | CP6 | 多维度综合 |
| `M_CHAIN_SZ_PROBLEM_LIST` | 深圳问题识别结果 | 🔧 | CP6 | 深圳问题识别模型 |
| `M_CHAIN_SZ_DEV_STAGE` | 发展阶段判断 | 🔧 | CP6 | 产业阶段分析模型 |
| `M_CHAIN_SZ_POTENTIAL` | 产业化潜力 | 🔧 | CP6 | 深圳机遇分析模型 |
| `M_CHAIN_OPPORTUNITY_INDEX` | 机遇推荐指数 | 🔧 | CP6 | 深圳机遇分析模型 |
| `M_CHAIN_LAYOUT_RECOMMEND_RANK` | 重点布局推荐排名 | 🔧 | CP6 | 重点布局推荐模型 |
| `M_CHAIN_LAYOUT_INDUSTRY` | 重点布局产业 | 🔧 | CP6 | 重点布局推荐模型 |

**统计**: 共 62 个 metric_id（✅ 可直查 14 个 / 🔧 待算法 33 个 / ⚠️ 待确认来源 15 个）
