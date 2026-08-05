# IA-SYNTH-REGION｜信息架构

> 版本 v1.0-r3，与 USM/Wireframe/UX-SPEC/TRACE 同步。

## 1. 导航落位

```
专题服务系统（demo-ui-topic 左侧导航）
└── 综合智能分析
    ├── 区域创新活力分析   /intelligence/vitality        F-SYN-01
    ├── 区域创新要素分析   /intelligence/elements        F-SYN-02
    └── 区域创新协同分析   /intelligence/collaboration   F-SYN-03
```

三页共享"区域上下文"（目标区域 / 对比范围 / 时间窗），构成"看整体 → 析要素 → 促协同"顺链闭环；页内提供顺链下钻入口，导航亦可直达任一页。

## 2. Frame 清单

| Frame | 名称 | 路由 / 载体 | 主要区块 | 对应故事 |
| --- | --- | --- | --- | --- |
| `F-SYN-01` | 活力总览页 | `/intelligence/vitality` | 上下文条 · 指数总览卡 · 分项得分 · 排名榜 · 指数趋势 · 指标体系分层 · 核心结论 · 下钻入口 | US-01/02/03 |
| `F-SYN-02` | 要素分析页 | `/intelligence/elements` | 上下文条 · 要素全景卡组 · 要素评价雷达 · 影响关联区 · 核心结论 · 下钻入口 | US-01/04/05 |
| `F-SYN-03` | 协同分析页 | `/intelligence/collaboration` | 上下文条 · 图谱筛选条 · 关系图谱 + 网络统计侧栏 · 协同度区 · 集群/孤立区 · 效果评估区 | US-01/06/07 |
| `F-SYN-04` | 要素详情抽屉 | F-SYN-02 内 Drawer（URL `element`） | 四维得分 · 构成明细 · 代表主体样例 | US-04 |
| `F-SYN-05` | 主体详情抽屉 | F-SYN-03 内 Drawer（人才/高校节点） | 基本信息 · 合作关系摘要 · 跨模块边界说明 | US-06 |

## 3. 数据对象

| 对象 | 关键字段 | 说明 |
| --- | --- | --- |
| Region | id / name / level(city|district) / inComparePool | 区域字典；区级 `inComparePool=false`（无横向排名） |
| IndicatorDimension | id / name / weight / indicators[] | 一级维度（4 个），权重合计 100 |
| Indicator | id / name / caliber / weight / valuesByRegion / scoresByRegion | 二级指标（12 个）；无数据区域缺省 |
| ElementCategory | id(enterprise|institution|talent|capital) / scaleByRegion / evalByRegion{scale,quality,structure,activity} / breakdown / sampleEntities | 四类要素 |
| ElementContribution | elementId / percent / pathText | 贡献度与影响路径（演示态） |
| CollabNode | id / name / kind(enterprise|institution|talent|svcOrg) / industry / crossRef{entCode?|svcOrgId?} | 图谱节点；企业/服务机构节点带跨模块真实 ID |
| CollabLink | source / target / relType(专利|项目|人才流动) / weight | 图谱边 |
| CollabCluster | id / name / memberIds / score / summary | 高效集群（演示态判定） |
| SynthState | region / compareScope / window / expandedDims / element / graphFilters / selectedNode / selectedCluster | store 状态（`topic-synth-workbench`） |

## 4. 指标目录（M_SYNTH_*，D9）

| metric_id | 中文名 | D1 | 挂载点 |
| --- | --- | --- | --- |
| `M_SYNTH_VITALITY_INDEX` | 区域创新活力综合指数 | missing（Q-SYNTH-01） | F-SYN-01 指数卡 / 排名榜 / 趋势 |
| `M_SYNTH_INDICATOR_SCORE` | 活力分项指标得分 | draft（Q-SYNTH-01） | F-SYN-01 指标体系 / 分项条形 |
| `M_SYNTH_ELEMENT_SCALE` | 创新要素规模统计 | aligned | F-SYN-02 要素全景卡 / F-SYN-04 |
| `M_SYNTH_ELEMENT_SCORE` | 创新要素评价得分 | missing（Q-SYNTH-02） | F-SYN-02 雷达 / F-SYN-04 |
| `M_SYNTH_ELEMENT_CONTRIB` | 要素创新贡献度 | missing（Q-SYNTH-02） | F-SYN-02 影响关联 |
| `M_SYNTH_COLLAB_DENSITY` | 协同网络连接密度 | draft（Q-SYNTH-03） | F-SYN-03 网络统计 |
| `M_SYNTH_COLLAB_CENTRALITY` | 主体网络中心性 | draft（Q-SYNTH-03） | F-SYN-03 中心性列表 |
| `M_SYNTH_COLLAB_INDEX` | 区域创新协同指数 | missing（Q-SYNTH-03） | F-SYN-03 协同度卡 / 集群分 |
| `M_SYNTH_COLLAB_OUTPUT_CORR` | 协同-产出相关系数 | missing（Q-SYNTH-03） | F-SYN-03 效果评估 |

就绪度四维：全部 D4 mock（🧪）；D2 partial（`dws_synth_*` ADS 表仅规划）；D3 见 TRACE `#metric_registration`。

## 5. 状态与 URL

| 状态 | 持久化 | URL 参数 | 页面 |
| --- | --- | --- | --- |
| 目标区域 | ✅ `topic-synth-workbench` | `region` | 三页共享 |
| 对比范围 | ✅ | — | 三页共享 |
| 时间窗 | ✅ | `window` | 三页共享 |
| 指标体系展开维度 | ✅ | — | F-SYN-01 |
| 要素抽屉 | — | `element` | F-SYN-02 |
| 图谱产业筛选 / 主体类型 | ✅ | `industry` | F-SYN-03 |
| 图谱选中节点 | — | `node` | F-SYN-03 |

URL 参数优先级 > localStorage > 默认值；非法参数按 USM 异常表回落并清除。

## 6. 跨模块出入口

| 方向 | 入口 | 目标 | 契约 |
| --- | --- | --- | --- |
| 出 | 图谱企业节点 | `/enterprise-center/profile/:code` | CT-SYN-01 |
| 出 | 图谱服务机构节点 | `/service/institution-judgment?org=` | CT-SYN-02 |
| 出 | 生成分析报告 / 协同效率报告 | 系统报告面 | CT-SYN-03 |
| 入 | 导航直达 / URL 分享（region/window/element/industry/node） | 三页任意状态 | — |
