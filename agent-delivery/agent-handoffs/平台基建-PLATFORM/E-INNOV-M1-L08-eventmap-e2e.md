# E-INNOV-M1-L08 · EventMap 联调真实 API

## 任务信息

| 字段 | 值 |
|------|-----|
| task-id | E-INNOV-M1-L08 |
| agent | frontend-agent |
| repo | lumen-ui-science-pc |
| branch | feat/E-INNOV-M1-L08 |
| depends_on | E-INNOV-M1-L05, E-INNOV-M1-L07 |
| PM waiver | v2 — 30891 浏览器验收 **DEFERRED → L10** |

## 范围与实现

### 替换 mock → 真实 `/innov/v1/*`

| 能力 | API | 实现要点 |
|------|-----|----------|
| 事件列表 + 分页 | `GET /events?mode=list` | `fetchEvents` 显式 `mode=list`；Arco Table + Pagination |
| 地图点位 | `GET /events?mode=geo` | 随地图视野传 `bbox=minLng,minLat,maxLng,maxLat`；GeoJSON → Leaflet circleMarker |
| 热力图 | `GET /events/heatmap` | 同筛选 + bbox；`leaflet.heat` 渲染 |
| 事件详情 | `GET /events/{eventId}` | 抽屉 Descriptions + 评分明细 |
| 关联分析 | `GET /events/{eventId}/relations` | 抽屉 Table |
| 图例字典 | `GET /dict/event-types` | 工具栏类型筛选 + 图例色块 |

### 代码变更

| 文件 | 变更 |
|------|------|
| `src/views/innov/components/EventMap.vue` | bbox 联动、moveend 防抖刷新、loading/empty、错误静默（Message 由 request 拦截器负责） |
| `src/api/innov/index.ts` | M1 端点泛型 + `mode=list` 默认 |
| `src/types/innov-event.ts` | **新增** EventPageResult / GeoFeatureCollection / HeatmapPoint 等类型 |

### 与 L07 差异

- L07 已迁入 Arco 版 EventMap 并调用 `@/api/innov`，但**未传 bbox**（契约 §1.1 geo 必传）、**未区分 mode=list**、无 loading/empty 态
- L08 补齐契约对齐与 UX 状态，响应解包沿用 lumen `request.ts`（直接取 `data`，非 demo 的 `res.data`）

## Design.md §14 检查清单

| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1–5 | Arco 工作台 / 控件节奏 | ✅ | 继承 L07 |
| 6 | loading/empty/error | ✅ | a-spin + a-empty；API 错 Message+traceId |
| 7–16 | 色/布局/地图工具栏 | ✅ | 无变更 |

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| 前端 → Java REST `/api/innov/v1` | ✅ |
| 算法越层 / NebulaGraph | N/A |
| observability.ts + traceId | ✅ request 拦截器 |
| demo2 只读参考 | ✅ |

## 测试证据

### 本地 build

```
npm run build  →  exit 0（2026-06-20）
vue-tsc --build  →  0 errors
```

### 浏览器 E2E（30891）

| 项 | 状态 | 说明 |
|----|------|------|
| http://192.168.88.50:30891/innov EventMap 有数据 | 🟡 **DEFERRED L10** | PM waiver v2 |
| 热力开关 / 分页 / 详情抽屉 / 无 console 报错 | 🟡 **DEFERRED L10** | 待 L10 qa + coordinator 补验 |

### L10 补验清单

1. 打开 `/innov` → M1 Tab 默认展示
2. 地图加载 GeoJSON 点位，拖拽/缩放后 bbox 刷新
3. 切换热力图开关，热力层可见
4. 筛选（时间/类型/等级/关键词）列表与地图同步
5. 点击列表行或地图点 → 详情抽屉 + 关联分析
6. 故意断 API → Message 含 traceId，无未捕获 Promise  rejection

## 产物清单

- 代码：`gkx-lumen/lumen-ui-science-pc` @ `feat/E-INNOV-M1-L08`
- 类型：`src/types/innov-event.ts`
- handoff：本文件

## 阻塞项 / 风险

| # | 项 | 严重度 |
|---|-----|--------|
| 1 | `gkx-innov` 未就绪时页面空态（非 mock 兜底） | 🟡 |
| 2 | 30891 内网可达性 | 🟡 L10 |

## cost 回填

| estimated_tokens | actual_tokens | model_used | actual_cost | cost_warn |
|------------------|---------------|------------|-------------|-----------|
| 300_000 | TBD | claude-sonnet-4.5 | TBD | green |

## 建议下一任务

- **L09** frontend-agent：demo2「全球创新实时数据」与 lumen EventMap 交互对照清单
