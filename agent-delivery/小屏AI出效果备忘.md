# 小屏 AI 出效果备忘

> **定位**：两系统共用的出效果提示词 + 改动范围（C5 **能力上限**，非 P0）。规范真源：`agent-delivery/Design-mobile.md` v1.1.2。  
> **C1–C7**：见 `Design-mobile.md` 文首。不下发红线仍用 Design-mobile §10。  
> **唯一真源**：本文。两仓不留副本。  
> Owner：`human:孔东`。适用范围：`lumen-ui-science-mobile`（展示）+ `lumen-ui-topic-mobile`（专题）。试点样例见文末，**不是模板**。  
> **2026-08-27 纠偏**：上限 ≠ 每页必装。`FE-DISPLAY-SMALL-BATCH-A` 第一版把本文 §0–§2 抄成统一「指标 + 地图 + 底 Tab」套版，禁止再犯。

## 0. 观感上限（C5，有该能力才上）

下列是**单页能力天花板**，不是每页 DOM 清单。本页信息架构没有的块，**不要塞**。

| 能力 | 何时上 | 上限（上了才守） |
|---|---|---|
| 指标卡 | 本页确有统计数字 | `StatCard` **一行两列**；`metric-id` 只挂已登记指标 |
| 图 | PC 该块用了 ECharts | 小屏也用 ECharts（`VChart`）；**禁止 G6** / 图谱建模 |
| 地图 | 本页有地区 / 要素等地理主舞台 | `UnifiedLeafletMap` + `MapChrome`；可切列表视图 |
| 地图工具条 | 仅当地图存在 | 放大 / 缩小 / 复位 / 全屏 + 热力开关 + 图例；**z-index 低于侧栏 Menu** |
| 底 Tab | 同菜单页分块 **多**（≥4 且互斥） | `PageTabs`（Vant Tabbar，不改路由）；少块用 `van-tabs` / 分段 / **单页滚动**；不叠两套 |
| 详情 | 点地图 / 名单 / 卡片 | **全屏抽屉**（半屏仅次要点选）；点选不跳 PC |
| 样例 | 数字与名单 | 页内常量，标「预览样例」，不走 `USE_MOCK` |
| 返回顶部 | 壳上 | `BackToTop`，不要每页再做一套 |

## 0.1 禁止套版（BATCH-A 教训）

- **一页一 vue**。禁止 `TrendBatchAView` 这类「一份配置驱动多路由」模板。
- 禁止把 SPIKE「地图 / 要素 / 事件 / 分析」四 Tab 或 `page-workspace + stat-grid + page-tabs + map-stage` 四件套抄到无此功能的页。
- 不需要指标的页不要 `StatCard` / `stat-grid`；不需要地图的页不要 `map-stage`；不需要 Tabbar 的页不要 `PageTabs`。
- 按该页功能做移动端最优解：同一屏内按 IA **堆叠**，不要为了「像样板页」而三分段。

## 1. 页骨架（壳全局，页内按需）

| 层 | 全局还是按页 | 做法 |
|---|---|---|
| App 壳 | **全局** | 顶栏 + 滑入侧栏；不把 PC 三栏压进来；不要改 `src/shell/` |
| 页根 | 建议 | `page-workspace` 作滚动容器即可 |
| 常驻 | 按页 | 一句结论（**有则放**） |
| 分块 / 数字 / 图 / 地 | **按页** | 见 §0；有才用 `stat-grid` / `page-tabs` / `map-stage` |
| 详 | 按页 | `ProfileDrawer`；点地图/名单只开抽屉 |
| 抽屉按钮 | 全局交互 | 头上 `关闭`（IconClose）+ 底栏 `关闭`。**返回与关闭同义时只留关闭**，不要两个都关抽屉 |

地图控件（工具条 / 热力开关 / 图例）层级必须低于壳侧栏，禁止盖住 Menu。

## 2. 可复用提示词

仓 / 栈 / 红线原样贴。**布局不要原样贴**：把「范围」换成该叶 `/goal` 页清单后，必须按每页 IA 选用 §0 能力，禁止统一骨架。

```text
强度：ponytail lite。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
必读：agent-delivery/Design-mobile.md v1.1.2 + agent-delivery/小屏AI出效果备忘.md。
小屏 = 中屏核心裁剪：滑入侧栏。页内按该页 IA 堆叠；分块多才用底 Tab，少则不用。
详情全屏抽屉（返回与关闭同义则只留关闭）。有地图才上 MapChrome，工具条不得盖住侧栏。
只复用已有组件（StatCard / ListCard / QuickFilter / ProfileDrawer / UnifiedLeafletMap / MapChrome / PageTabs / BackToTop / SectionTitle / VChart），但按页选用，禁止多页一个配置模板。
C1：壳/Icon/D9 用 Arco，页内控件用 Vant 4。Tabbar 只做页内分块，禁止一级菜单。路由 history。
PC 有图的块用 echarts；禁止 G6 / 图谱。无统计不塞 KPI，无地理不塞地图。
MetricMarker 经 StatCard 的 metric-id；镜像没有 id 就不要传。
页内常量注释「预览样例，非 USE_MOCK fixture」。
一页一 vue。布局 class 按需：页根 page-workspace；有 KPI 才 stat-grid；有底 Tab 才 page-tabs；有地图才 map-stage。
展示只写 lumen-ui-science-mobile 。
专题只写 lumen-ui-topic-mobile ，禁止写 lumen-ui-topic。
范围：本叶 /goal 列出的页。未列入的菜单保持 PlaceholderView。
```

## 3. 改哪些 / 不改哪些（两系统）

按仓改 `src/**`，不按某个子目录锁死。展示叶不碰专题仓，专题叶不碰展示仓。

### 改（出效果可动）

- 目标仓 `src/**`：按页结论、文案、预览样例、该页确有的 KPI / 图 / 地图
- 分块多才底 Tab；有地图才地图·列表双视图 + MapChrome；PC 有图则 ECharts
- 已登记 `metric_id` 才传；没有就走红问号，不伪造 8 件套
- 分析工作区若上小屏：切条件不自动 `create`，须「开始分析」（I2-12）
- 路由：只把本叶 path 从 `PlaceholderView` 换成**该页自己的** vue

### 缓（默认留给 PC 或后叶）

- 卡片模板库、拖拽排序、隐藏/恢复、卡片编辑
- 知识图谱、路径比较/播放、G6
- 横向对比、对比篮、聚类、影响力、权重/推演
- 趋势预测、异常监测、导出、关注收藏、PermGate
- 地域×时间×领域级联全套、搜索历史
- 点省/点地区进 PC 分析真页；与 PC 查询/评估工作区对齐

### 不改 / 禁止

- `src/shell/`、`src/config/breakpoints.ts` 的 `PHONE_MAX_PX=767`
- `@/review`；禁止手改 `readiness.generated.ts`
- `observability.ts` 请求头（`X-Trace-Id` / `traceparent`）
- 未列入本叶 `/goal` 的空壳路由
- 搬 demo 整页；互斥 `display` 叠 PC 工作台
- 直连 Python / demo 网关；往 `lumen-ui-topic` 写小屏
- `USE_MOCK=false` 时用 `@/mock` 或 Demo fixture 填数
- 点地图/名单跳 PC 真页（只开抽屉）
- 多页共用一个配置驱动 vue；无功能强加 KPI / 地图 / 底 Tab

## 4. 试点样例（不是范围、不是套版）

`FE-SMALL-AI-SPIKE-L01` 已落地的两页，只说明「**地图型总览**上限长什么样」。后续叶按模块在 `src/views/{模块}/` **各写各页**，Tab / KPI / 图 / 地图按该页 IA，不要抄本表名字，也不要抄本表骨架。

| 系统 | 样板页 | 仓 | 文件 | 路由 |
|---|---|---|---|---|
| 展示 | 科技全域态势 | `lumen-ui-science-mobile` | `src/views/trend/TechOverallSituationView.vue` | `/trend/tech-overall-situation` |
| 专题 | 企业总览 | `lumen-ui-topic-mobile` | `src/views/enterprise/EnterpriseOverviewView.vue` | `/enterprise-center/overview` |

当时页内切法（仅对照这两页）：态势 = 地图 / 要素 / 事件 / 分析；企业 = 概况 / 分布 / 重点 / 深圳。

## 5. 监管人纠偏原文（2026-08-26 `human:孔东`）

BATCH-A 当晚后半夜三条，已吸收进 §0 / §1 / §2。后续叶直接守本文，不必再贴聊天。

1. **按页布局**：所有功能高度雷同、布局一模一样不行。不需要指标和地图的页面不要强加，不需要 Tabbar 的可以不用，根据页面功能按移动端实现最优解；重新分析各页，优化布局、丰富该页功能。
2. **地图叠层**：地图工具条 / 热力开关 / 图例层级太高、盖住侧栏 Menu 时，必须压到壳导航之下。
3. **抽屉按钮**：返回与关闭作用一样时，弹窗只保留关闭。
