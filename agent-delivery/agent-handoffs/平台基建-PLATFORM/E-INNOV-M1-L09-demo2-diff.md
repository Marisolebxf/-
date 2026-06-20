# E-INNOV-M1-L09 · demo2「全球创新实时数据」 vs lumen EventMap 交互对照

## 任务信息

| 字段 | 值 |
|------|-----|
| task-id | E-INNOV-M1-L09 |
| agent | frontend-agent |
| repo | gkx-orchestration（handoff）+ 只读对照 demo-ui-science / lumen-ui-science-pc |
| depends_on | E-INNOV-M1-L08 |
| cicd | skip（设计类，无 CI） |

## 对照范围说明

| 侧 | 路由 / Tab 文案 | 代码真源 | 交互范式 |
|----|-----------------|----------|----------|
| **demo2** | 全球创新监测 → Tab「全球创新实时数据」 | `demo-ui-science/src/pages/global-innovation/tabs/InnovationRealtime.jsx` | 实时 KPI + 知识图谱 + 趋势/领域图；**无地理事件地图** |
| **lumen** | `/innov` · `topicTitle: 全球创新实时数据` → M1「科创事件地图」 | `lumen-ui-science-pc/src/views/innov/components/EventMap.vue` | Leaflet 事件地图 + 侧栏列表 + 详情抽屉 |

**命名对齐但范式不同**：lumen 路由 `meta.topicTitle` 与 demo2 Tab 同名，但 lumen 首 Tab 实现的是「科创事件地图」，与 demo2 该 Tab 的「知识图谱实时流」并非同一组件。

**demo2 事件地图近邻参考**（同仓、非「全球创新实时数据」Tab，供地图/列表维度对照）：

- `demo-ui-science/src/App.jsx` → `GlobalEventSection`（科技全域态势 · 工作台 Tab「科创事件」）
- 父级筛选：`FilterBar`（地域级联、时间粒度、学科领域、事件类型、关键词等）

下文 **§1–§3** 主列 demo2「全球创新实时数据」Tab；地图/列表相关行附加 **demo2 科创事件（GlobalEventSection）** 列，便于与 lumen EventMap 对齐。

---

## 1. 筛选维度对照

| 维度 | demo2「全球创新实时数据」 | demo2 科创事件（GlobalEventSection） | lumen EventMap | 对齐状态 | backlog |
|------|---------------------------|--------------------------------------|----------------|----------|---------|
| 时间范围 | ❌ 无显式筛选（趋势图固定 18 月窗口） | ✅ 年范围 + 粒度（日/周/月/季/年）+ 当前时间片 | ✅ `a-range-picker`（`startTime`/`endTime`） | 🟡 粒度不一致 | **BL-M1-01** 时间粒度（日/周/月/季/年）与当前年片 |
| 地域 / 区域 | ❌ | ✅ 级联「地域范围」 | ❌ 仅地图 bbox 隐式范围 | 🔴 lumen 缺 | **BL-M1-02** 地域级联筛选（独立于 bbox） |
| 学科 / 技术领域 | 🟡 领域分布饼图 hover/点击高亮（非列表筛选） | ✅ `FieldFilter` 多选 | ❌ | 🔴 lumen 缺 | **BL-M1-03** 技术领域筛选 |
| 事件类型 | ❌ | ✅ 多选：科技热点、科技舆情（2 类） | ✅ 多选：12 类（`/dict/event-types`） | ✅ lumen 更完整 | — |
| 重要性 | ❌ | 🟡 逻辑存在（高/中/低），工作台侧当前固定 `all` | ✅ 1/2/3 级多选 | 🟡 demo2 Tab 无 | — |
| 关键词 | ❌ | ✅ 带历史/分类候选的关键词检索 | ✅ `keyword` 输入 | ✅ | — |
| 图谱实体类型 | ✅ 聚焦：机构 / 专家 / 成果 / 全部 | ❌ | ❌ | 🔴 lumen 缺 | **BL-M1-04** 知识图谱实体聚焦（M2 落图？） |
| 实时 KPI 口径 | ✅ 专利/论文/投资/机构四指标 + 30s 刷新 | ❌ | ❌ | 🔴 lumen 缺 | **BL-M1-05** 实时 KPI 条 + 刷新频率说明 |
| 科创要素 | ❌ | ❌（要素在另一工作台 Tab） | ❌ | — | — |
| 关系类型 | ❌ | ❌ | ❌ | — | — |
| 导出 | ❌ | ✅ 工作台 FilterBar 导出 | ❌ | 🔴 lumen 缺 | **BL-M1-06** 当前筛选结果导出 |

---

## 2. 地图操作对照

| 操作 | demo2「全球创新实时数据」 | demo2 科创事件（GlobalEventSection） | lumen EventMap | 对齐状态 | backlog |
|------|---------------------------|--------------------------------------|----------------|----------|---------|
| 底图 / 引擎 | ❌ 无地理地图 | ✅ `SharedRegionMap`（共享地图组件） | ✅ Leaflet + 高德瓦片 | 🟡 引擎不同 | — |
| 平移 / 缩放 | 🟡 知识图谱：拖拽节点、滚轮缩放 | ✅ 地图默认交互 | ✅ 拖拽、滚轮缩放 | ✅ | — |
| 视野联动数据 | ❌ | 🟡 视口聚焦键刷新，无 bbox API | ✅ `moveend` 防抖 300ms → `bbox` 查询 geo/heatmap | ✅ lumen 更强 | — |
| 热力图层 | ❌ | ✅ 开关（混合/纯点位） | ✅ `a-switch` 热力图 / 点位 | ✅ | — |
| 点位样式 | 🟡 KG 节点按实体类型 | ✅ 按事件类型色 + 重要性层级 | ✅ `circleMarker`：类型色、重要性半径 | ✅ | — |
| 点位 hover | 🟡 KG 节点选中 | ✅ 区域标注 | ✅ `bindTooltip` 类型+标题 | ✅ | — |
| 点位 click | ✅ 节点详情侧栏 | ✅ → 事件详情抽屉 | ✅ → 详情抽屉 + 关联分析 API | ✅ | — |
| 地图 / 列表视图切换 | ❌ | ✅ 全屏「地图视图」↔「列表视图」 | ❌ 左右分栏固定布局 | 🔴 lumen 缺 | **BL-M1-07** 地图/列表全屏视图切换 |
| 地图工具栏 | ❌ | ✅ 放大/缩小/重置/全屏（`MAP_TOOLBAR_ACTIONS`） | ❌ | 🔴 lumen 缺 | **BL-M1-08** 地图工具栏（缩放/重置/全屏） |
| 列表「在地图中查看」 | ❌ | ✅ 定位并高亮地图点位 | ❌ | 🔴 lumen 缺 | **BL-M1-09** 列表行定位地图并高亮 |
| 图例 | ❌ | ✅ 事件类型 + 热度等级 | ✅ 事件类型色块（字典驱动） | 🟡 lumen 无热度图例 | **BL-M1-10** 重要性/热度图例说明 |
| 空态 | 🟡 KG 无节点提示 | ✅ 「当前范围暂无科创事件点位」 | ✅ `a-empty` | ✅ | — |
| 框选区域 | ❌ | ❌ | ❌ | — | （创新成果 Tab 有框选，非本 Tab） |

---

## 3. 列表字段对照

### 3.1 主列表

| 列 / 字段 | demo2「全球创新实时数据」 | demo2 科创事件列表视图 | lumen EventMap 侧栏表 | 对齐状态 | backlog |
|-----------|---------------------------|------------------------|----------------------|----------|---------|
| 事件标题 | ❌ 无列表 | ✅ `text`（可带当前地域前缀） | ✅ `title` | ✅ | — |
| 事件类型 | ❌ | ✅ 类型徽章 + 色 | ❌ 列表无类型列（详情有） | 🔴 lumen 缺 | **BL-M1-11** 列表增加「类型」列 |
| 重要性 | ❌ | ✅ 高/中/低 文案 | ✅ `importanceLevel` 标签（1–3） | 🟡 分级体系不同 | — |
| 重要性评分 | ❌ | ❌ | ✅ `importanceScore` | ➕ lumen 独有 | — |
| 时间 | ❌ | ✅ `date` + 周期标签（随粒度） | ✅ `eventTime`（仅日期 `slice(0,10)`） | 🟡 lumen 无周期副文案 | **BL-M1-12** 时间列展示粒度/周期 |
| 操作列 | ❌ | ✅ 「查看」「在地图中查看」 | ❌ 整行点击进详情 | 🔴 lumen 缺 | **BL-M1-09**（同上） |
| 列排序 | ❌ | ✅ 标题/类型/重要性/时间可排序 | ❌ | 🔴 lumen 缺 | **BL-M1-13** 列表列头排序 |
| 分页 | ❌ | ✅ 7 条/页 + 页码跳转 | ✅ 20 条/页 + `show-total` | 🟡 页大小不同 | — |

### 3.2 详情 / 侧栏（非表格列表）

| 区块 | demo2「全球创新实时数据」 | demo2 科创事件 | lumen EventMap 抽屉 |
|------|---------------------------|----------------|---------------------|
| 选中节点详情 | ✅ 影响力指数、领域、实时状态、描述 | ✅ `InsightDetailDrawer` | ✅ Descriptions：类型、时间、等级、评分 |
| 评分明细 | ❌ | 🟡 依详情抽屉内容 | ✅ `importanceDetail` 分项表 |
| 关联分析 | 🟡 「进入科学技术全景分析」跳转 | 🟡 工作台详情动作 | ✅ `relations` 关联表 |
| 图谱统计 | ✅ 可见节点 / 机构 / 成果计数 | ❌ | ❌ | **BL-M1-14** 实时流统计摘要（若保留 KG 范式） |
| 趋势图 | ✅ 专利/论文/投资 实测+预测 | ❌ | ❌ | **BL-M1-15** 创新趋势分析图（M5？） |
| 领域分布 | ✅ 饼图 + Top5 + 其他明细 | ❌ | ❌ | **BL-M1-16** 领域分布图 |

---

## 4. lumen 已覆盖、demo2「全球创新实时数据」Tab 未覆盖

| 能力 | lumen | demo2 Tab |
|------|-------|-----------|
| REST `/innov/v1/events` list/geo/heatmap | ✅ | ❌（Mock 本地） |
| 12 类事件类型字典 + 图例色 | ✅ | ❌ |
| 重要性数值评分 + 可解释分项 | ✅ | ❌ |
| bbox 驱动地图数据刷新 | ✅ | ❌ |
| 关联实体 API 表 | ✅ | ❌ |

---

## 5. Backlog 汇总（lumen 暂缺 → 记入 M1+）

| ID | 优先级 | 项 | 建议归属 |
|----|--------|-----|----------|
| BL-M1-01 | P2 | 时间粒度（日/周/月/季/年）与当前时间片 | EventMap 或 M5 |
| BL-M1-02 | P1 | 地域级联筛选（独立于 bbox） | EventMap |
| BL-M1-03 | P1 | 技术领域筛选 | EventMap + API |
| BL-M1-04 | P2 | 知识图谱实体聚焦（机构/专家/成果） | M2 GraphInfluence |
| BL-M1-05 | P1 | 实时 KPI 四指标 + 30s 刷新说明 | 新 Tab 或页头 |
| BL-M1-06 | P2 | 筛选结果导出 | EventMap |
| BL-M1-07 | P2 | 地图/列表全屏视图切换 | EventMap UX |
| BL-M1-08 | P2 | 地图工具栏（缩放/重置/全屏） | EventMap |
| BL-M1-09 | P1 | 列表「在地图中查看」+ 高亮 | EventMap |
| BL-M1-10 | P3 | 重要性/热度图例 | EventMap |
| BL-M1-11 | P2 | 列表「类型」列 | EventMap |
| BL-M1-12 | P3 | 时间列周期副文案 | EventMap |
| BL-M1-13 | P2 | 列表列头排序 | EventMap |
| BL-M1-14 | P2 | 图谱可见节点统计 | M2 |
| BL-M1-15 | P2 | 创新趋势预测图 | M5 ForecastView |
| BL-M1-16 | P2 | 领域分布图 | EventMap 或 M5 |

**产品决策待 PM**：lumen `/innov` 是否应合并 demo2 两套范式（事件地图 + 实时 KPI/知识图谱），或拆分为多 Tab（当前已有 M1–M5 五个 Tab 骨架）。

---

## 6. 代码索引

| 文件 | 说明 |
|------|------|
| `demo-ui-science/src/pages/global-innovation/tabs/InnovationRealtime.jsx` | demo2「全球创新实时数据」 |
| `demo-ui-science/src/pages/global-innovation/tabs/realtimeModel.js` | 实时状态、领域分布、趋势模型 |
| `demo-ui-science/src/App.jsx` `GlobalEventSection` | demo2 科创事件地图+列表 |
| `demo-ui-science/src/App.jsx` `FilterBar` | 工作台级筛选条 |
| `lumen-ui-science-pc/src/views/innov/components/EventMap.vue` | lumen M1 |
| `lumen-ui-science-pc/src/router/routes.ts` | `topicTitle: 全球创新实时数据` |
| `lumen-ui-science-pc/src/types/innov-event.ts` | 列表/Geo/详情类型 |

---

## 7. 架构合规自检

| 铁律 | 状态 |
|------|------|
| demo2 只读、禁止 merge 进 lumen | ✅ 本文档只读对照，无 demo2 代码变更 |
| 前端 → Java `/innov/v1` | ✅ lumen EventMap 已接（L08） |
| Design.md §14 | 🟡 本任务为对照清单，UI 补齐项见 backlog |
| 数据血缘 ⓘ / MockBadge | 🟡 demo2 KPI/图谱为 Mock；lumen 事件指标 ⓘ 待 M2+ 验收 |

---

## 8. cost 回填

| estimated_tokens | actual_tokens | model_used | actual_cost | cost_warn |
|------------------|---------------|------------|-------------|-----------|
| 150_000 | TBD | claude-sonnet-4.5 | TBD | green |

## 9. 建议下一任务

- **L10** coordinator + qa：基于本 backlog 与 L08 补验清单做 M1 里程碑签收（30891 EventMap E2E）
