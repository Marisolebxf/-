# 小屏 AI 出效果备忘

> **定位**：两系统共用的出效果提示词 + 改动范围（C5 观感上限，非 P0）。规范真源：`agent-delivery/Design-mobile.md` v1.1。  
> **C1–C7**：见 `Design-mobile.md` 文首。不下发红线仍用 Design-mobile §10。  
> **唯一真源**：本文。两仓不留副本。  
> Owner：`human:孔东`。适用范围：`lumen-ui-science-mobile`（展示）+ `lumen-ui-topic-mobile`（专题）。试点样例见文末，不是范围。

## 0. 观感上限（C5，全局）

1. 指标卡 **一行两列**
2. PC 用 ECharts 的块，小屏也用 ECharts（禁止 G6）
3. 地区 / 要素支持 **地图视图 / 列表视图**
4. 地图工具条复刻 PC：放大 / 缩小 / 复位 / 全屏 + 热力开关 + 图例
5. 数字与名单对齐 demo 预览样例（页内常量，标「预览样例」，不走 `USE_MOCK`）
6. 详情用 **全屏抽屉**（半屏抽屉仅次要点选）
7. 分块多用 **底部 Tab**，少用 `van-tabs` / 分段按钮；不叠两套
8. 壳上 **返回顶部**

## 1. 页骨架（全局）

| 层 | 做法 |
|---|---|
| 常驻 | 一句结论（有则放）；不把 PC 三栏压进来 |
| 分块 | 底 Tab 切内容；Tab 名按该页信息架构，不套固定四字 |
| 数字 | `StatCard` 两列；`metric-id` 只挂已登记指标 |
| 图 | PC 有图才上 `VChart`；禁止 G6 / 图谱建模 |
| 地 | `UnifiedLeafletMap` + `MapChrome`；可切列表 |
| 详 | `ProfileDrawer`；点地图/名单只开抽屉 |
| 布局 class | `page-workspace` + `stat-grid` + `page-tabs` + `map-stage` |

## 2. 可复用提示词

贴进后续 BATCH / 专题叶时原样用。把「范围」换成该叶 `/goal` 页清单，不要改下面约束。

```text
强度：ponytail lite。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
必读：agent-delivery/Design-mobile.md v1.1 + agent-delivery/小屏AI出效果备忘.md。
小屏 = 中屏核心裁剪：滑入侧栏 + 页内底部 Tab，详情全屏抽屉，地图工具条复刻 PC。
只复用 StatCard / ListCard / QuickFilter / ProfileDrawer / UnifiedLeafletMap / MapChrome / PageTabs / BackToTop / SectionTitle / VChart。
C1：壳/Icon/D9 用 Arco，页内控件用 Vant 4。Tabbar 只做页内分块，禁止一级菜单。路由 history。
PC 有图的块用 echarts；禁止 G6 / 图谱。
MetricMarker 经 StatCard 的 metric-id；镜像没有 id 就不要传。
页内常量注释「预览样例，非 USE_MOCK fixture」。
布局：page-workspace + 2 列 stat-grid + page-tabs + map-stage。
展示只写 lumen-ui-science-mobile 。
专题只写 lumen-ui-topic-mobile ，禁止写 lumen-ui-topic。
范围：本叶 /goal 列出的页。未列入的菜单保持 PlaceholderView。
```

## 3. 改哪些 / 不改哪些（两系统）

按仓改 `src/**`，不按某个子目录锁死。展示叶不碰专题仓，专题叶不碰展示仓。

### 改（出效果可动）

- 目标仓 `src/**`：结论、文案、Tab 名与默认、预览样例、KPI 挂载
- 底 Tab / 地图·列表双视图 / MapChrome / 抽屉 Tab / PC 有图则 ECharts
- 已登记 `metric_id` 才传；没有就走红问号，不伪造 8 件套
- 分析工作区若上小屏：切条件不自动 `create`，须「开始分析」（I2-12）
- 路由：只把本叶 path 从 `PlaceholderView` 换成真页

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

## 4. 试点样例（不是范围）

`FE-SMALL-AI-SPIKE-L01` 已落地的两页，只说明「上限长什么样」。后续叶按模块在 `src/views/{模块}/` 加页，Tab / KPI / 图按该页 IA，不要抄本表名字。

| 系统 | 样板页 | 仓 | 文件 | 路由 |
|---|---|---|---|---|
| 展示 | 科技全域态势 | `lumen-ui-science-mobile` | `src/views/trend/TechOverallSituationView.vue` | `/trend/tech-overall-situation` |
| 专题 | 企业总览 | `lumen-ui-topic-mobile` | `src/views/enterprise/EnterpriseOverviewView.vue` | `/enterprise-center/overview` |

当时页内切法（仅对照）：态势 = 地图 / 要素 / 事件 / 分析；企业 = 概况 / 分布 / 重点 / 深圳。
