# Wireframe-ZHIKU-STRATEGY-REPORT｜战略咨询报告与成果

> **版本**：v1.0-rework-r5（AI 起草，待人确认）
> **视觉基线**：Design.md；交互基线：UX-UE 通用交互组件规范.md；字段表第 6 列 metric_id/序号（D9）

## F-SP-01 研究报告

```
┌ Tab 研究报告 ────────────────────────────────────────┐
│ [研究报告总数 ⓘ🧪]        [关键词🔍][行业▾][清空] [上传报告]│
│ 行: 标题 | 行业Tag | v2 | 质量分86🧪 | 08-03 | 状态   │
│     [详情][编辑][新版本][归档][删除][导出]            │
│ 研报库分组（已归档）: 标题 | 归档时间 | [回链原报告]   │
│ 详情抽屉: 摘要🧪/关键词🧪/标签🧪/目录/全文/溯源附录/版本│
│ 上传弹窗: 文件*(演示) 标题* 行业*  → 解析中→已就绪     │
└──────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | metric_id / 序号 |
| --- | --- | --- | --- | --- | --- |
| 统计 | 研究报告总数 | MetricCard | store.research.length | ⓘ 弹卡 | `ZHIKU-SP-RESEARCH-TOTAL` / 50 |
| 筛选 | 关键词/行业 | input+select | ui.researchFilter | 叠加实时、持久化、Empty+清空 | 50 |
| 列表 | 标题/行业/版本/质量分/状态 | a-table | store.filteredResearch | 解析中禁操作（骨架） | 50 |
| 操作 | 编辑/新版本/归档/删除/导出 | a-button 组 | actions | 删除引用拦截并列引用方 | 50 |
| 详情 | 摘要/关键词/标签/质检 | a-drawer | report | 🧪 规则式演示标注 | 50 |
| 版本 | 版本历史 | a-timeline | report.versions | 旧版可回看摘要 | 50 |
| 上传 | 文件/标题/行业 | a-modal | uploadReport | 校验拦截；2s 🧪 解析流转 | 50 |

## F-SP-02 洞察月刊

```
┌ Tab 洞察月刊 ────────────────────────────────────────┐
│ [洞察报告总数 ⓘ🧪]   订阅方向: [半导体●][AI○]…  推送记录(2)│
│ 期次卡: 2026-Q3 半导体产业洞察 [订阅中Tag]            │
│ 详情: 概念/趋势折线/热点Tag/地区排行/洞察专题🧪 [导出▾]│
└──────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | metric_id / 序号 |
| --- | --- | --- | --- | --- | --- |
| 统计 | 洞察报告总数 | MetricCard | store.insights.length | ⓘ 弹卡 | `ZHIKU-SP-INSIGHT-TOTAL` / 51 |
| 订阅 | 方向开关 | a-switch | store.subscriptions | 幂等；订阅→🧪 推送记录追加 | 51 |
| 推送 | 推送记录 | a-list | store.pushLog | Empty 引导订阅 | 51 |
| 详情 | 概念/趋势/热点/排行/专题 | 区块+VChart | issue | 专题带 🧪 自动生成标注 | 51 |
| 导出 | PDF/图片 | a-dropdown | exportIssue | demo 文本导出+🧪 | 51 |

## F-SP-03 热点分析

```
┌ Tab 热点分析  [产业|技术|资本]（分段，持久化）─────────┐
│ 榜单: #1 半导体设备国产化  指数 87？ ↑12%             │
│ 详情抽屉: 四源构成条形🧪(学术/专利/投融资/舆情)        │
│           近6期趋势折线   [关联月刊: 2026-Q3 →]       │
└──────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | metric_id / 序号 |
| --- | --- | --- | --- | --- | --- |
| 切换 | 三方向 | a-radio-group(button) | ui.hotspotDirection | 持久化；空方向局部 Empty | 52 |
| 榜单 | 排名/名称/指数/环比 | a-table | store.hotspotsOf | 指数旁红问号（D1 missing GAP） | `ZHIKU-SP-HOTSPOT-INDEX` / 52 |
| 详情 | 四源构成/趋势/回链 | a-drawer + VChart | hotspot | 回链跳 F-SP-02 期次；缺期置灰 | 52 |

## F-SP-04 战略报告生成

```
┌ Tab 战略报告生成 ────────────────────────────────────┐
│ 底料勾选: [研究报告☑︎列表][洞察月刊☑︎列表][专家意见☑︎预置]│
│ 推荐区🧪(按行业规则)   脱敏开关🧪   模板: 战略咨询报告  │
│ 要点预览: · RR-001 量子计算…(研究报告)                │
│ [生成报告 →]（未选禁用+tooltip）                       │
│ 生成历史: 08-04 底料3份 已脱敏 [打开任务→]/已失效      │
└──────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | metric_id / 序号 |
| --- | --- | --- | --- | --- | --- |
| 底料 | 三类勾选 | a-checkbox-group ×3 | research/insights/expertOpinions | 勾选驱动要点预览 | 53 |
| 推荐 | 推荐底料 | a-tag 列表 | 规则匹配 | 🧪 标注，点击即勾选 | 53 |
| 预览 | 大纲要点 | a-list | 派生 | 每底料一条+来源标注 | 53 |
| 生成 | 生成报告 | a-button(primary) | writingStore.createTask | 未选禁用；确认后跳写作（CT-SP-01） | 53 |
| 历史 | 生成记录 | a-list | store.generations | 任务回链；失效底料标注 | 53 |

## F-SP-05 战略咨询成果（strategy/case-show；案例广场 writing/cases 共享案例区）

```
┌ 战略咨询成果 ────────────────────────────────────────┐
│ [总成果数ⓘ🧪][总投资额ⓘ🧪][平均ROIⓘ🧪←点击筛选][满意度ⓘ🧪]│
│ 已发布报告区（来自报告创作链路，Empty 引导）           │
│ 行业过滤 [全部|AI|半导体…]   (ROI 突出筛选态 Banner)   │
│ 案例卡 → 详情弹窗: 背景/做法/成效/投资与回报           │
└──────────────────────────────────────────────────────┘
```

| 区块 | 字段 | 控件 | 数据源 | 交互 | metric_id / 序号 |
| --- | --- | --- | --- | --- | --- |
| 统计 | 总成果数 | MetricCard | caseStore.cases.length | ⓘ | `ZHIKU-SP-CASE-TOTAL` / 54 |
| 统计 | 总投资额 | MetricCard(亿元) | sum(investment) | ⓘ🧪 | `ZHIKU-SP-CASE-INVEST-TOTAL` / 54 |
| 统计 | 平均投资回报率 | MetricCard(%)可点击 | avg(roi) | 点击切换 ROI 突出筛选 | `ZHIKU-SP-CASE-ROI-AVG` / 54 |
| 统计 | 客户满意度 | MetricCard(%) | avg(satisfaction) | ⓘ🧪 | `ZHIKU-SP-CASE-SATISFACTION` / 54 |
| 发布区 | 已发布报告 | a-list | writingStore.published | 回链任务；Empty 引导 | `ZHIKU-SP-ACHIEVEMENT-PUBLISHED` / 54+CT |
| 案例 | 行业过滤/卡片 | radio+card | caseStore.filtered | ROI 筛选叠加；详情弹窗四区块 | 54 |
