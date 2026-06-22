# UI-DS-26-trial · ui-agent · DS-26 科技创新生态展示沙箱实现

## 执行时间

2026-06-22（ui-agent · 承接 UX 评审通过的 DS-26 试点）

## 任务

- 复刻 UX：`docs/ia/sandbox/innovation-ecosystem-2026-06-22/`（4 页 wireframe）
- 工作仓：`E:/gkx-lumen/repos/demo-ui-science`
- 栈：Arco Design + Leaflet + ECharts graph + D9 三件套

## 路由入口

| 页面 | Hash 路由 |
|------|-----------|
| 沙箱目录 | `#/sandbox` |
| P-01 总览 | `#/sandbox/innovation-ecosystem-2026-06-22` |
| P-02 载体地图 | `#/sandbox/innovation-ecosystem-2026-06-22/carriers` |
| P-03 人才态势 | `#/sandbox/innovation-ecosystem-2026-06-22/talents` |
| P-04 协作网络 | `#/sandbox/innovation-ecosystem-2026-06-22/collaboration` |

本地 dev：`npm run dev` → http://127.0.0.1:4176/#/sandbox/innovation-ecosystem-2026-06-22

## 产物路径

```
src/pages/sandbox/innovation-ecosystem-2026-06-22/
  _router.jsx, _layout.jsx, data.js, styles.css, WorkbenchShell.jsx
  index.jsx, carriers.jsx, talents.jsx, collaboration.jsx
  components/  (D9: MetricSpecCard, MockBadge, PendingBadge, DataLineageDrawer, LineageContext)
src/mocks/sandbox/innovation-ecosystem-2026-06-22/
  overview.json, metrics-catalog.json, carriers.json, talents.json, collaboration.json
```

注册：`SandboxRouter.jsx` + `sandbox/index.jsx`

## 完成清单

| # | 检查项 | 状态 |
|---|--------|------|
| 1 | 路由可访问 | ✅ |
| 2 | 覆盖 wireframe 4 页 | ✅ |
| 3 | 主菜单未改 | ✅（仅 SandboxRouter 注册） |
| 4 | Mock 贴近业务 | ✅ |
| 5 | 字段名对齐 ODS | ✅ carrier_name / scholar_id 等 |
| 6 | D9 ⓘ + MockBadge + ⚠️ | ✅ |
| 7 | 埋点 console.log | ✅ ic.* 事件 |
| 8 | npm run build 绿 | ✅ |
| 9 | 无同页 antd | ✅ 沙箱页纯 Arco |
| 10 | analysis-panel 保留 | ✅ WorkbenchShell |

## Design.md §14 自检（摘要）

- 浅蓝白工作台 ✅ | 六骨架 + 三段工作区 ✅ | 主色 #165DFF ✅
- Header 64px 由 layout context-bar 替代（沙箱模式）| 控件 ~32px ✅
- loading: Suspense Spin ✅ | empty: Empty ✅

## 已知限制

- 协作网络用 ECharts graph 代替 G6（减依赖复杂度；handoff 建议 Wave 1 可换 G6）
- 宏观 KPI / 人才分类 / 服务状态为 Mock + ⚠️（Q021/Q023/Q024/Q025）
- 未 push（main protected，同 UX 阶段）

## git

```
e409cc8 [sandbox] ui-agent 实现：DS-26 科技创新生态展示 Arco 沙箱 4 页 [agent:ui-agent]
```

（基于 UX commit `bf929e8`；本地 ahead 2 commits；main 受保护未 push）

## 下一步

- PM 有权限 push / MR
- frontend-agent 复刻到 lumen-ui-science-pc（经甲方汇报后）
- data-agent 补 DS-26-data-availability-matrix.md
