# 小屏 AI 出效果备忘

> **定位**：出效果提示词 + 样板上限（非 P0）。规范真源：`agent-delivery/Design-mobile.md` v1.1。  
> **C1–C7 定义表**：见 `Design-mobile.md` 文首。本备忘是 **C5 观感上限**（不是不下发红线）。  
> **仓内副本**：`repos/lumen-ui-science-mobile/docs/小屏AI出效果备忘.md`。  
> Owner：`human:孔东`。样板页：展示「科技全域态势」（专题「企业总览」在 `lumen-ui-topic-mobile`）。

## 0. 本轮人改方向（2026-08-25，C5 确认为观感上限）

1. 指标卡 **一行两列**
2. PC 用 ECharts 的块，小屏也用 ECharts（禁止 G6）
3. 地区 / 要素支持 **地图视图 / 列表视图**
4. 地图工具条复刻 PC：放大 / 缩小 / 复位 / 全屏 + 热力开关 + 图例
5. 数字与名单对齐 demo 预览样例（页内常量，标「预览样例」，不走 `USE_MOCK`）
6. 详情用 **全屏抽屉**
7. **底部 Tab** 切开内容
8. 壳上 **返回顶部**

仍不做：对比篮、导出、PermGate、图谱/G6、路径比较、卡片编辑、点省进 PC 分析真页。

## 1. 两页信息架构

| 页 | 仓（目标） | 常驻 | 底部 Tab |
|---|---|---|---|
| 科技全域态势 | science-mobile | 结论条 | 地图 · 要素 · 事件 · 分析 |
| 企业总览 | topic-mobile | 结论条 | 概况 · 分布 · 重点 · 深圳 |

## 2. 可复用提示词

```text
强度：ponytail lite。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。
必读：agent-delivery/Design-mobile.md v1.1。
小屏 = 中屏核心裁剪：滑入侧栏 + 页内底部 Tab，详情全屏抽屉，地图工具条复刻 PC。
只复用 StatCard / ListCard / QuickFilter / ProfileDrawer / UnifiedLeafletMap / MapChrome / PageTabs / VChart。
C1：壳/Icon/D9 用 Arco，页内控件用 Vant 4。Tabbar 只做页内分块，禁止一级菜单。路由 history。
PC 有图的块用 echarts；禁止 G6 / 图谱。
MetricMarker 经 StatCard 的 metric-id；镜像没有 id 就不要传。
页内常量注释「预览样例，非 USE_MOCK fixture」。
布局：page-workspace + 2 列 stat-grid + page-tabs + map-stage。
专题页只写 lumen-ui-topic-mobile，禁止写 lumen-ui-topic。
```

## 3. 改哪些 / 不改哪些

改：页头结论、卡片文案、Tab 默认、样例点位。丽影只改 topic-mobile。

不改：`src/shell/` 断点数字、评审层、`observability.ts`、其余空壳路由。

## 4. 路径

| 系统 | 页 | 文件 | 仓 |
|---|---|---|---|
| 展示 | 科技全域态势 | `src/views/trend/TechOverallSituationView.vue` | science-mobile |
| 专题 | 企业总览 | `src/views/topic/enterprise/EnterpriseOverviewView.vue` | topic-mobile |
