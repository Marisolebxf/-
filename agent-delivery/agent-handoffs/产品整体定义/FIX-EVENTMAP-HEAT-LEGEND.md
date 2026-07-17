# FIX-EVENTMAP-HEAT-LEGEND · EventMap 热力图例与错误态

> 对照 `templates/handoff-template.md` · epic `E-PROD-UXUE-FIX` · QA G-11~G-14  
> 状态：`review`（待 coordinator 验收）

## 任务认领

| 字段 | 值 |
|---|---|
| task-id | FIX-EVENTMAP-HEAT-LEGEND |
| epic | E-PROD-UXUE-FIX |
| repo | lumen-ui-science-pc |
| claimed_by | agent:frontend-agent |
| supervised_by | human:孙英哲 |
| claim_type | pull |
| claimed_at | 2026-07-17T12:42:00+08:00 |

## 范围与实现（对照 DoD + G-11~G-14）

仅改 `lumen-ui-science-pc/src/views/innov/components/EventMap.vue`（最小 diff，未改 package.json / vite / demo）。

| 项 | 状态 | 说明 |
|---|---|---|
| G-11 热力强度图例 | ✅ | `heatmapOn` 时叠 `.heatmap-legend`（低→高色条）；关闭热力时 `v-if` 隐藏 |
| G-12 图例右下角浮层 | ✅ | `.map-container` > `.map-canvas`；图例经 `Teleport` 挂入 Leaflet 容器内 `absolute` 右下（仍在地图容器子树） |
| G-13 热力空态 | ✅ | `heatPts` 为空设 `heatEmpty`；`v-show`「暂无热力数据」；保留视野与基础图例 |
| G-14 详情 error+retry | ✅ | catch 不再 `drawer.value = false`；`detailError` + `a-result` +「重试」 |

## 产物清单

- `lumen-ui-science-pc/src/views/innov/components/EventMap.vue`
- 本 handoff：`agent-delivery/agent-handoffs/产品整体定义/FIX-EVENTMAP-HEAT-LEGEND.md`

## Design.md §14（与本改动相关条目）

| # | 检查项 | 状态 |
|---|---|---|
| 1 | 浅蓝白科技工作台，非深色大屏 | ✅ 未改全局主题；地图浅色底图 |
| 2 | 地图基础图例固定右下角；热力图例仅随热力开 | ✅ `.map-legend` 在 `.map-container` 内 absolute；热力条 `v-if="heatmapOn"` |
| 3 | 表单/按钮接近 Arco 节奏（控件约 32px） | ✅ 仍用 `a-*` size=small / 既有 toolbar |
| 4 | 有 loading / empty / error 状态 | ✅ map/list/detail spin；热力空态；详情 error+retry |
| 5 | 图表/地图由可视化内核承载，Arco 做外围 | ✅ Leaflet + leaflet.heat；图例/抽屉用 Arco |
| 6 | 禁 antd / 依赖 Arco | ✅ `@arco-design/web-vue`（本仓 Vue 栈；未引 antd） |
| 7 | 避免霓虹/紫蓝发光/无意义占位 | ✅ 图例白底轻阴影，热力条蓝系 |

未触及本改动：Header/侧栏栅格、右侧分析面板 tabs、全站断点等 — N/A。

## 测试结果

- `pnpm run build`：✅（pnpm **10.12.1**；`vue-tsc --build` + `vite build` 通过；关键输出：`✓ built in 17.33s`）
- 说明：本仓 `pnpm-workspace.yaml` 含 `allowBuilds`，需 pnpm 10+；本机 PATH 无 `pnpm` 时用完整路径调用 `pnpm10.exe`（见历史验证命令）

## CI/CD

| 字段 | 值 |
|---|---|
| 分支 | `feat/FIX-EVENTMAP-HEAT-LEGEND`（已 push，跟踪 `origin/feat/FIX-EVENTMAP-HEAT-LEGEND`） |
| commit | `8dfce163772b06a524809889c3aa11d18a4a864d`（短：`8dfce16`；含 map-container + Teleport/z-index=850；起自 `eebedbf`） |
| 建 MR | https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-pc/-/merge_requests/new?merge_request%5Bsource_branch%5D=feat%2FFIX-EVENTMAP-HEAT-LEGEND |
| pipeline URL | https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-pc/-/pipelines?ref=feat%2FFIX-EVENTMAP-HEAT-LEGEND |
| commit 页（CI 状态） | https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-science-pc/-/commit/8dfce163772b06a524809889c3aa11d18a4a864d |

> 说明：本环境无 GitLab API token，无法解析具体 pipeline `#iid`；上表为分支筛选入口。若已有单个 pipeline，可将 URL 替换为 `.../-/pipelines/<iid>`。

## 架构合规

| 项 | 状态 |
|---|---|
| 前端只调 Java（`@/api/innov` → `/api/innov/v1`） | ✅ |
| 禁 antd | ✅ |
| observability / request Message+traceId 保留 | ✅ |
| 未改 demo-ui-science | ✅ |
| 算法不进前端 | ✅ N/A |

## 开放项

1. `team-roster.yaml` 尚无 `human:孙英哲`，建议 PM 补登。
2. 建/合 MR 后，可将 pipeline URL 替换为具体 `.../-/pipelines/<iid>`；当前已填分支 pipelines 筛选链接。
3. 全屏态图例：浮层已在 Leaflet 容器内；若后续加全屏需复测。
4. **z-index（已处理）**：图例/空态 `z-index: 850`（`< .leaflet-control 1000`），`pointer-events: none`；经 Teleport 挂入 `map.getContainer()`，右下角未来工具条可点穿/压在浮层之上。
5. 待 coordinator 验收后将 registry `review` → `done`。

## cost（必填）

| 字段 | 值 |
|---|---|
| model_used | cursor-grok-4.5 |
| actual_tokens | 80000 |
| actual_cost | 3.0 |
| cost_warn | green |
