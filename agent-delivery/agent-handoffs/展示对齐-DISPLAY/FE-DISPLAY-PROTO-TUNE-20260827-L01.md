# FE-DISPLAY-PROTO-TUNE-20260827-L01 · UI handoff（Wave 1）

> 任务 ID: FE-DISPLAY-PROTO-TUNE-20260827-L01  
> Epic: E-DISPLAY-ALIGN  
> 执行 Agent: `agent:ui-agent`  
> 监管人: `human:孙英哲`  
> 认领类型: `coordinator_dispatch`  
> 日期: 2026-08-27  
> 阶段: **Wave 1 A 包已落地（策略 A 原地）**  
> ponytail: full

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:ui-agent` |
| supervised_by | `human:孙英哲` |
| claim_type | `coordinator_dispatch` |
| lock | 4h |
| 说明 | registry 无 ID 时经 `task-mcp-cli` 补建后认领。本会话 Cursor 未挂载 `task-registry` MCP，走官方 CLI。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D8/D9/D10；D9 页内拷贝政策 AntD 触发器，不改 `src/components`；未接真 NLP/真源流。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本会话动态工具仅 `cursor` 命名空间。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（本叶不改调用链 / 存储流） |
| 图 diff | 无 |
| 会签态 | N/A |

## 1. 范围与实现

PM 确认 **按 A 包开工**。只改 `demo-ui-science`，策略 A 原地，无 `*New` 菜单。

| 项 | 实现 |
|----|------|
| #499 | `SpaceTimeEvolutionPage` 在总览与工作台之间接入 `hotspotAlerts`（AntD Alert+List）；导出 CSV/JSON/TXT 含预警段；标注「演示口径，非真源阈值」 |
| D9 | `soft-science/components/lineage/`：AntD `MockBadge` + `MetricSpecTrigger` + catalog。D1=`draft` / D4=`mock` / `algorithm_type=UNKNOWN`，不改绿。挂 JudgmentOverview / KpiDeck / 时空 KPI / 全球创新实时 KPI `label` |
| #15 | 全域态势重要性胶囊旁：「等级为演示口径，非真源实时」 |
| #60/#72 | 实时说明改为「演示刷新非真源流」 |
| #3 自动复位 | **跳过**（按钮+ESC/Ctrl+R 已在） |
| 禁改 | `src/components`、`pageRouting.js`、政策跟踪、技术点详情抽屉、KG 400–454、人才 NLP |

## 2. 偏离说明

| 项 | 说明 |
|---|---|
| 全域态势 KPI 未铺满 D9 | A 包原文想铺「可见统计数字」；施工卡与 App.jsx 体量约束只允许 #15 一句标注，未对全域态势 KPI 做 D9 全铺 |
| 截图 | 本机无 Cursor 浏览器工具；以 `npx vite build` 绿 + 源码断言代替。30999 待 `origin/dev` CI 后由监管人点验 |
| 人才 #260 等标注 | 施工卡白名单未列人才页，未扩写 |

## 3. 产物清单

| 产物 | 路径 |
|------|------|
| 缺口表 | `agent-delivery/agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-PROTO-TUNE-20260827-缺口清单.md` |
| 本 handoff | `agent-delivery/agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-PROTO-TUNE-20260827-L01.md` |
| 代码 | `${GKX_ROOT}/repos/demo-ui-science`（见 §10） |

入口：https://skxrules.unicomcn.tech:30999 （跟踪 `origin/dev`）

- `#/topic/科技时空演进展示` — 热点预警 + KPI ⓘ
- `#/topic/软科学成果展示` — 判断总览 KPI ⓘ / Mock
- `#/topic/全球创新监测` — 实时数据更新 Tab，演示刷新文案 + KPI lineage
- `#/topic/科技全域态势` — 重要性分级演示标注

## 4. 测试结果

- `npx vite build`：**通过**（约 1m26s；既有 ThemeWindow duplicate-key 警告，非本叶引入）
- `node --test src/pages/global-innovation/tabs/realtimeModel.test.mjs`：6/6 通过（含「演示刷新非真源流」）
- catalog 自检：14 条指标均为 D1 draft / D4 mock / UNKNOWN
- 本地 `vite preview :4176` 主包 `index-CeitX5NG.js` 含：`热点预警` / `演示口径，非真源阈值` / `等级为演示口径` / `演示刷新非真源流` / `M_STE_EVENT_COUNT` / `查看指标`
- 时空页测试已加「热点预警」与 `M_STE_EVENT_COUNT` ⓘ 断言（仓内无 vitest 脚本，未跑 RTL）
- 复验（源码仍在，未重写）：#15 筛选+标注、#17/#39 撤销重做、#281 批量导入、#478 导出记录、#479 报表配置
- **30999**：已发布 `/assets/index-DhAczV1K.js`，包内含 `热点预警` / `演示口径，非真源阈值` / `等级为演示口径` / `演示刷新非真源流` / `M_STE_EVENT_COUNT`。无浏览器工具，截图未附，请监管人点 §3 四条路由补图

## 10. touched_files 白名单

未改 `src/components`、`pageRouting.js`、`data.js`、政策跟踪、技术点详情抽屉。

### demo-ui-science

- `src/pages/achievement-preview/modules/soft-science/components/lineage/MetricLineageMarks.jsx`
- `src/pages/achievement-preview/modules/soft-science/components/lineage/displayMetricsCatalog.json`
- `src/pages/achievement-preview/modules/soft-science/components/lineage/lineage.css`
- `src/pages/achievement-preview/modules/soft-science/components/SoftScienceJudgmentOverview.jsx`
- `src/pages/achievement-preview/modules/soft-science/components/SoftScienceKpiDeck.jsx`
- `src/pages/achievement-preview/modules/soft-science/utils/softScienceHomepageDerivations.js`
- `src/pages/achievement-preview/modules/space-time-evolution/components/SpaceTimeEvolutionPage.jsx`
- `src/pages/achievement-preview/modules/space-time-evolution/spaceTimeEvolution.css`
- `src/pages/achievement-preview/modules/space-time-evolution/components/__tests__/SpaceTimeEvolutionPage.test.jsx`
- `src/pages/global-innovation/tabs/InnovationRealtime.jsx`
- `src/pages/global-innovation/tabs/realtimeModel.js`
- `src/pages/global-innovation/tabs/realtimeModel.test.mjs`
- `src/pages/global-innovation/style.css`
- `src/App.jsx`（仅 #15 一句标注）

### gkx-orchestration

- `agent-delivery/agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-PROTO-TUNE-20260827-缺口清单.md`
- `agent-delivery/agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-PROTO-TUNE-20260827-L01.md`

## 5. Design.md §14 自检（A 包页）

### 检查 8 条

| # | 项 | Wave 1 |
|---|-----|--------|
| 1 | 浅蓝白工作台，非深色大屏 | ✅ 未改壳；预警用 AntD Alert warning，无霓虹 |
| 2 | Header / 侧栏 / 主视图 / 右侧分析 | ✅ 时空预警插在总览与工作台之间，未删右栏 |
| 3 | 选中态 `#165DFF` / `#E8F3FF` | ✅ ⓘ 用 `var(--blue)` |
| 4 | 控件接近 Arco 节奏 32px | ✅ 未改顶栏/筛选高度 |
| 5 | 地图工具栏/图例克制 | ✅ 未改地图工具条 |
| 6 | 筛选单控件 ≤400px | ✅ 未新增超宽筛选 |
| 7 | 24 栅格 / 展开 200 / 收起 64 | ✅ 未改骨架 |
| 8 | loading / empty / error | ✅ 预警空列表不渲染；评审关闭零泄漏 |

### 验收 6 条

| # | 项 | Wave 1 |
|---|-----|--------|
| 1 | 一眼是分析工作台 | ✅ 未改成卡片仪表盘 |
| 2 | Header ≈64px、侧栏 ≈200px | ✅ 未改壳 |
| 3 | 控件高 ≈32px、筛选 gap 16/24、单控件 ≤400px | ✅ |
| 4 | 主色 `#165DFF`、底 `#D8E7FC` | ✅ 无新硬编码霓虹色 |
| 5 | 中央主视图 > 右侧分析；有分析分组 | ✅ 未删面板 |
| 6 | 可视化内核 vs 外围 | ✅ 预警是 AntD 外围；地图/图未混画 |

## 6. D10 §19 / §3.4

- 预警条有区域名 `热点预警`、演示口径说明、列表可读
- KPI ⓘ 可点；关评审 `ReviewOnly` 不渲染 `metric_id`
- #3 手势复位仍不实现（已有按钮+ESC/Ctrl+R）

## 7. 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ |
| 2 调用链前端→Java→Python | ✅ 未接真 API、未直连 Python |
| 3 Nebula | ✅ |
| 4 可观测 | N/A 本叶不改公共 `observability.ts` |
| 5 CI | push `origin/dev` 后跟仓 Pipeline |
| 6 demo 不 merge lumen | ✅ |
| 7 方案 A | ✅ Mock only |
| 8 ADS/Mock | ✅ catalog 标明 pending_ads / Mock |
| 9 D8 Design.md | ✅ §14 已打 |
| 10 D9 | ✅ ⓘ + MockBadge；D1 draft D4 mock；未手写改绿 |
| 11 D10 | ✅ |
| 12 D12 | ✅ 只改 demo-ui-science |

## 8. 遗留风险

- 30999 已含 A 包文案；交互截图请监管人补
- 全域态势 KPI 未铺 D9，若 PM 坚持 A 包原文第 2 条需另开叶
- 同页 GI 实时 Tab 引入 AntD lineage（该页原为 lucide/custom，未引入 Arco）

## 9. CI/CD（必填）

- 分支：`demo-ui-science` `origin/dev`；编排仓 handoff 另提交
- commit：见 git log（`[agent:ui-agent]`）
- pipeline URL / ID：push 后补
- 部署 namespace / 镜像 tag：静态站 30999 跟踪 dev
- K8s rollout：静态站
- dev 测试 URL：https://skxrules.unicomcn.tech:30999

## 11. 下一步

监管人在 30999 点验三页 + 全域态势标注；coordinator AV-0 收 handoff。B/C 包不改。
