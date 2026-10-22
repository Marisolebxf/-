# FE-ACH-02A · 科技创新生态展示 — 整页复刻交付

> 任务：FE-ACH-02A（科技创新生态展示 a/b/c 三页签整页复刻）
> 工作区：~~worktrees/lumen-ui-science-pc--ach02-innovation-eco~~（已并 dev 清理，见 §7）
> 状态：**联调中（integration）** — 2026-10-21 用户验收通过，转联调
> ponytail: full

## 1. 范围与实现（DoD 对照）

| DoD（派单包 §3） | 实现 |
|---|---|
| Tab a 载体地图与增量分析 | ✅ 三级层级（大湾区/深圳/行政区）视口飞行、点位/热力/增量三模式、类型 Checkbox 筛选（28→22 联动验证）、季度 Bar（markPoint 峰值橙标）/年度 Bar+同比 Line、分区对比表+联动 Bar、类型结构 Pie、载体详情 Drawer（Descriptions 10 项+资料下载演示 Message） |
| Tab b 人才态势分析 | ✅ 人才点位/聚集热力、类别 Pie、年度流入 Bar、学科 Bar、岗位层次 Bar、技术领域雷达（vs 全国基准）、典型案例 Timeline、人才详情 Drawer（明细表行点击同开） |
| Tab c 载体人才协作关系 | ✅ 四图层 Checkbox（载体/热力/热点/连线，取消载体点位 28 circle→0 验证）+ Polyline 虚线网络、协作网络 ECharts graph（force/roam/emphasis adjacency）、项目进展表+详情 Drawer（动态推送 Timeline）、影响力雷达、联合产出四卡（M_IE_* metricId+lineage 直读 demo 冻结文案） |
| 地图复用 | ✅ 新建 `EcoMapStage.vue`（demo EcoMap.jsx 语义复刻：flyTo 0.6s / invalidateSize 150ms / leaflet.heat 静态 import / circleMarker / dashArray 4-4 虚线 / isolation:isolate）；**未动 `TiandituMap`**（其 props 只有 L.marker/divIcon 体系，无 circleMarker/热力半径渐变/polyline 语义，demo EcoMap 是独立 stage 体系——按复刻经验 §2.4「不预设用不到的抽象」，新组件而非改公共件） |
| Arco 替换 | ✅ radio-group(type=button)/checkbox-group/table/descriptions/drawer/timeline/progress(0-1 ÷100)/tag/Message/icon 全 Arco；无原生 select/input |
| D9 全挂 | ✅ 5 KPI ⓘ（种子 KPI_META metricId+lineage）+ 14 图表卡 MetricSpecHint + 🧪 全挂（MockBadge） |
| 三绿 | ✅ type-check 0 错 / `innovation-ecosystem.test.mjs`（新）+ `achievement.test.mjs` 全绿 / `pnpm build` 绿（28.3s） |

## 2. 产物清单

- `src/views/achievement/innovation-ecosystem/index.vue`（重写：S01 基壳 → 整页 3 页签 + 3 Drawer，~1250 行）
- `src/views/achievement/innovation-ecosystem/EcoMapStage.vue`（新，地图舞台）
- `src/views/achievement/innovation-ecosystem/MapLegend.vue`（新，页内第 2 处出现即封装：3 页签共用）
- `src/views/achievement/innovation-ecosystem/innovation-ecosystem.css`（新，demo 内联样式冻结 class 化；grid 5-12-7 / 8-8-8×2+13-11 / 14-10×2）
- `src/views/achievement/innovation-ecosystem/innovation-ecosystem.test.mjs`（新，最小自检 30+ 断言）
- 环境补链（worktrees 目录，非仓内）：`worktrees/demo-ui-science` junction → `repos/demo-ui-science`（与 node_modules junction 同性质；自检读 demo 真源用，**不改 demo 仓**）

未动（闸门遵守）：`_shared/`、`menu.ts`、`api/`、`types/`、种子、`TiandituMap`、其他 ach01/03/04/05 worktree 与主工作区。

## 3. 与 demo 逐区块对照（走查证据，1600×900 视口）

| 区块 | demo | lumen | 结论 |
|---|---|---|---|
| KPI 行 5 卡 | 283/46(+17.9%)/1258/96/312 | 283/46(+17.9%)/1258/96/312 + 全 ⓘ🧪 | ✅ |
| Tab a 三栏 | 筛选(5)+地图(12)+图表(7) | 同比例 grid，地图 560px/28 点位 | ✅ |
| 层级×模式×类型联动 | 大湾区点位默认 | 行政区→10 气泡+模式禁用+提示；热力→canvas 热力层；增量→橙点高亮图例切换；去实验室 28→22 | ✅ |
| Tab b 布局 | 8-8-8 / 8-8-8 / 13-11 | 同；地图 420px、图例 4 类+橙高亮、匹配表 Progress 0-1、明细 22 行分页 8 | ✅ |
| Tab c 布局 | 14-10 / 14-10 | 同；graph canvas 820×472 实绘、绩效四卡 312/486/96/58、项目表 8 行、连线虚线橙 | ✅ |
| 载体 Drawer | Descriptions 10 项 + 4 Tag + 资料下载 Message | 同（松山湖双创社区实测）+ 🧪 | ✅ |
| 项目 Drawer | 6 项 + 动态推送 Timeline3 + 推送 Tag | 同（P01 实测）| ✅ |

截图：ach02-tab-a-wide / ach02-tab-b / ach02-tab-c / ach02-carrier-drawer / ach02-project-drawer（Cursor screenshots 目录）。

## 4. 偏离说明

1. **worktree 路径**：用户指令写 `ach02-soft-science`，实际按派单包真源 `ach02-innovation-eco`（soft-science 是 ach01）。
2. **EcoMapStage 而非 TiandituMap**：派单包说「地图复用 TiandituMap（热力 props 已支持）」，但 TiandituMap 无 circleMarker 半径/描边/热力渐变参数/polyline props，demo EcoMap 是 CircleMarker+heatLayer+Polyline 独立体系；为不改公共件（其他页正在消费）新建页内 stage，语义逐条对齐 demo。已在 handoff 登记，如走查要求可后续合并进 TiandituMap。
3. **demo 空类名 `ien-tab-content`**：demo css 无此规则定义（仅类名占位），lumen 保留类名不新增规则。
4. **c 页签人才点位点击开载体 Drawer 的 index 语义**：demo 叠加图 carriers 点击开载体详情、hotspots 无点击；lumen 按构造顺序前 N=carriers 判定，行为等价。

## 5. 架构合规自检（公约 §2）

- ✅ 调用链：前端只经 `fetchInnovationEcosystemDataset`（defineApi 双轨，USE_MOCK=true 走冻结种子）
- ✅ D8：React→Vue 复刻同视觉 token（#165DFF/#D8E7FC/卡片圆角 8/阴影），Arco Vue 全量替换
- ✅ D9：ⓘ（MetricSpecHint）+ 🧪（MockBadge）全挂；M_IE_* 直读种子；USE_MOCK=false 表格 a-empty「等待网关契约」零 fixture
- ✅ D10：Tabs=PageTabFrame（role=tablist 键盘可达）、控件 32px 体系（radio/checkbox small 型对齐 demo）
- ✅ D12：零 demo import/merge；种子逐行冻结（achievement.test.mjs 断言仍绿）
- ✅ 可观测：trackAchievementInteraction（page-mounted/tab-change/carrier-download-demo/export）

## 5.5 走查修正（2026-10-21 用户 DOM 反馈）

1. 标题去（New）：`title="科技创新生态展示"`（index.vue）
2. 年度新增载体「同比 17.9%」tag 移入数值行（`46 个` 之后）：KpiTile 加 `value-extra` 槽——与 ach01 同日走查修正同槽位合并（冲突解决：两侧同实现，保留注释版）
3. 页根上下滚动：`.ach-page` 加 `height:100% / min-height:0 / overflow-x:hidden / overflow-y:auto / overscroll-behavior:contain`（fullBleed 下 content-shell--flush 为 overflow:hidden，页根自管滚动，对齐 tracking 页先例）

验证：vue-tsc 0 错 / 两 test.mjs 全绿 / 浏览器实测三处生效。

## 6. cost

- actual_tokens: ~0.55M（glm-5.3）
- model_used: glm-5.3
- actual_cost: ~$1.4
- cost_warn: false

## 7. 转联调记录（2026-10-21）

- 用户验收通过 → `task-update-status integration`
- worktree 分支 `feat/ach02-innovation-eco` 提交 `978b56e`（复刻成果 + 走查修正，7 files +1724/-61）
- 并入主仓 dev：merge commit `9881287`（唯一冲突 KpiTile value-extra 槽两侧同实现，保留注释版）；合并后三绿复验（vue-tsc / 两 test.mjs）
- 清理：worktree 目录已 remove、临时分支已删（dev 快照 `9881287`）
- push `origin/dev` `ef62ac6..9881287` → CI → K8s dev rollout
- 5233 端口走查 dev server 已停
