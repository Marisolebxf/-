# FE-ACH-04A · 大型科学仪器共享 — 整页复刻交付

> 任务：FE-ACH-04A（大型科学仪器共享 a/b/c 三页签整页复刻）
> 工作区：`worktrees/lumen-ui-science-pc--ach04-instrument`（分支 feat/ach04-instrument，基点 1834a50）
> 状态：**已合并 dev 并推送（ef62ac6），临时分支 feat/ach04-instrument 已删除**（2026-10-21 走查 2 项修正见 §7，合并记录见 §8）
> ponytail: full

## 1. 范围与实现（DoD 对照）

| DoD（派单包 §3） | 实现 |
|---|---|
| Tab a 仪器盘点 | ✅ KPI 卡 5 枚（demo 真实口径数值，metricId 直读种子 KPIS）、类别 Checkbox 筛选 + 状态/区域联动、`InstrumentMap` 三态着色（在用/闲置/维修 divIcon 徽标）+ `leaflet.markercluster` 聚合 + `fitBounds`、32 台仪器滚动列表（点击开 Drawer）、状态分布 Bar / 类别密度 Bar / 使用频率 Line 三图 |
| Tab b 预约服务 | ✅ 服务网点地图（可预约 Tag）、14 项服务清单（类型/共享类型/预计周期/频率，点击开 Modal）、服务类型 Pie / 共享类型 Bar 两图、12 条订单排期表（`ORDER_STATUS_META` 着色 Tag、`a-switch` 订阅提醒会话态、预约与评价交互按 demo 演示态 Message 提示不落库） |
| Tab c 服务机构 | ✅ 机构分类地图（`ORG_TYPE_META` 着色 divIcon + 聚合）、14 家机构列表（`a-progress` 开放率 percent÷100、`a-rate` 共享能力评分、批量导出按钮）、机构类型 Pie / 开放率 Bar / 活跃状态列表三区、服务能力明细表（关键词过滤） |
| 报告生成 TS 等价 | ✅ `orgAnalysisReport.ts`（模块目录内）：`flattenInstitutionRows` / `buildOrgAnalysisReport` / `downloadOrgAnalysisReport`（CSV UTF-8 BOM `\ufeff`）/ `exportOrgReports`，语义逐条对齐 demo `orgAnalysisReport.js`，零 demo import |
| 地图复用 | ✅ `InstrumentMap.vue` 包装 `TiandituMap`：`mapRef.getMap()` 取原生 map → `L.markerClusterGroup` 生命周期管理（watch 数据重建）→ 自定义 divIcon 徽标 → tooltip/click 事件 → 图例条 + 空态 |
| Arco 替换 | ✅ descriptions/drawer/modal/tabs/tag/progress(0-1 ÷100)/switch/table/rate/checkbox-group/icon 全 Arco；无原生 select/input |
| D9 全挂 | ✅ 5 KPI ⓘ（`MetricSpecHint`，种子 KPI_META metricId+lineage）+ 图表卡 ⓘ + 🧪（`MockBadge`）全挂 |
| 三绿 | ✅ `pnpm type-check` 0 错（TS2614/TS2769 已修：具名导出走 ts 模块、`valueYAxis` 显式返回类型）/ `instrument-sharing.test.mjs`（12 断言）+ `achievement.test.mjs` 全绿 / `pnpm build` 绿（25.96s） |

## 2. 产物清单

- `src/views/achievement/instrument-sharing/index.vue`（S01 基壳 → 整页：页头 profile 副标题 + 导出按钮、5 KPI 卡、3 页签容器、仪器 Drawer / 服务 Modal / 机构 Modal，263 行）
- `src/views/achievement/instrument-sharing/InstrumentListTab.vue`（新，Tab a 整页，266 行）
- `src/views/achievement/instrument-sharing/BookingServiceTab.vue`（新，Tab b 整页，224 行）
- `src/views/achievement/instrument-sharing/OrganizationTab.vue`（新，Tab c 整页，273 行）
- `src/views/achievement/instrument-sharing/InstrumentMap.vue`（新，地图舞台：TiandituMap 包装 + markercluster，172 行）
- `src/views/achievement/instrument-sharing/orgAnalysisReport.ts`（新，报告生成 TS 等价，104 行）
- `src/views/achievement/instrument-sharing/instrument-sharing.css`（新，布局 grid/滚动列表/Tag 尺寸归一/图表显式高度 `.isn-chart--300` `.isn-chart--260`，219 行）
- `src/views/achievement/instrument-sharing/instrument-sharing.test.mjs`（新，最小自检 12 断言，116 行）
- `.walkthrough/`（走查截图 6 张，未入 git）

未动（闸门遵守）：`_shared/`、`menu.ts`、`api/`、`types/`、种子（`achievementInstrumentSeed.ts` 冻结零改动）、`TiandituMap` 公共件、其他 ach01/02/03/05 worktree 与主工作区。

依赖补充（主仓根执行，worktree junction 共享）：`leaflet.markercluster` + `@types/leaflet.markercluster`（demo 同款聚合库，属「已有依赖选型」而非新栈）。

## 3. 与 demo 逐区块对照（走查证据，localhost:3214）

| 区块 | demo | lumen | 结论 |
|---|---|---|---|
| KPI 行 5 卡 | 入网 9,262 台套等真实口径 | 同数值 + 全 ⓘ🧪 | ✅ |
| Tab a 三区 | 筛选(5)/地图+列表(12)/图表(7) | 同 grid 比例；32 点位三态徽标聚合 | ✅ |
| 类别筛选联动 | 勾选过滤点位+列表 | Checkbox-group 联动（含全选/清空） | ✅ |
| Tab b 布局 | 服务地图+清单 / 两图 / 订单表 | 同；地图可预约 Tag、订单 12 行状态 Tag 着色 | ✅ |
| 订阅提醒开关 | switch 演示态 | `a-switch` 会话态切换实测 | ✅ |
| Tab c 布局 | 机构地图(14)/列表+导出/三统计区/明细表 | 同；Progress 0-1 实测、Rate 只读评分 | ✅ |
| 仪器 Drawer | 型号/分类/厂商/载体/价格/购买日期/产地/原值/地址/功能/指标/使用要求 13 项 | 同（Descriptions + 🧪） | ✅ |
| 服务 Modal | 周期/类型/共享类型/说明/范围/样品要求/联系人/单位/图片占位 | 同（高通量基因测序实测） | ✅ |
| 机构 Modal | 优势资源/历史评价/能力评分 + 导出报告 | 同（中科院深圳先进院实测）+ CSV 下载 | ✅ |

截图（worktree `.walkthrough/`）：`fe-ach-04a-tab-a-instruments.png` / `fe-ach-04a-tab-b-booking.png` / `fe-ach-04a-tab-b-switch.png` / `fe-ach-04a-tab-b-service-modal.png` / `fe-ach-04a-tab-c-org.png` / `fe-ach-04a-tab-c-org-modal.png`。

## 4. 偏离说明

1. **worktree 路径**：用户指令写 `ach04-soft-science`，实际按派单包真源 `ach04-instrument`（soft-science 是 ach01 的 worktree 名）。
2. **依赖安装位置**：worktree 内 node_modules 是主仓 junction，`pnpm add leaflet.markercluster` 须在主仓根执行——包落在主仓 `package.json`，worktree 经 junction 消费；与本单「已有依赖」口径一致（demo 同库）。
3. **订单表订阅提醒**：demo 为本地 state 演示，lumen 同步为会话态（刷新还原），不替 BE 拍板落库。

## 5. 架构合规自检（公约 §2）

- ✅ 调用链：前端只经 `fetchInstrumentSharingDataset`（defineApi 双轨，USE_MOCK=true 走冻结种子）
- ✅ D8：React→Vue 复刻同视觉 token（#165DFF/#D8E7FC/卡片圆角 8/阴影），Arco Vue 全量替换
- ✅ D9：ⓘ（MetricSpecHint）+ 🧪（MockBadge）全挂；metricId 直读种子 KPIS；USE_MOCK=false 时零 fixture
- ✅ D10：Tabs 键盘可达、控件 32px 体系、弹层 Teleport body
- ✅ D12：零 demo import/merge；报告生成器是 TS 重写非复制
- ✅ 可观测：trackAchievementInteraction（page-mounted / tab-change / export / 详情打开）
- ✅ 图表显式高度（`.isn-chart--300/260`）防 init 0 高死锁
- ✅ 未 commit/push（人工验收闸门 2026-10-20）

## 6. cost

- actual_tokens: ~0.62M（glm-5.3，两段会话累计）
- model_used: glm-5.3
- actual_cost: ~$1.5
- cost_warn: false

## 7. 走查修正记录（2026-10-21 监管人走查反馈）

| # | 走查问题 | 根因 | 修正 |
|---|---|---|---|
| 1 | 页面无上下滚动（整页高 2426px 但滚不动） | `instrument-sharing` 是 fullBleed 路由，框架层 `.content-shell--flush { overflow: hidden }` + `.layout-page { overflow: hidden }`，超出视口内容无处滚动 | `index.vue` 页壳外包 `.isn-scroll-shell`（`height: calc(100dvh - 68px); overflow-y: auto`），规则放本页 css——不动 `_shared/` 公共件（派单包 §4 闸门） |
| 2 | Tab a 首行「仪器类别筛选」卡布局内容不对（筛选卡满宽 1296px，三栏变三行堆叠） | `InstrumentListTab.vue` 类名笔误：模板写 `isn-row--cols-5-13_6`（连字符）vs CSS 定义 `isn-row--cols-5_13_6`（下划线），grid 规则未命中 | 模板类名改 `isn-row--cols-5_13_6`，恢复 demo 5:13:6 三栏（实测 260/676/312px） |

修正后验证：type-check 0 错 / 双自检全绿 / build 24.17s；浏览器实测滚动壳 `overflow-y:auto`（scrollHeight 1251 > clientHeight 856，可滚）+ 三栏 grid 恢复 + 截图 `fe-ach-04a-fix-tab-a-top.png` 归档。内容本身与 demo 一致（12 类别 + 状态统计 18/9/5=32 台套），未改数据。

## 8. 合并记录（2026-10-21 用户授权）

1. 主仓未提交的 `package.json`+`pnpm-lock.yaml`（本单依赖补充）先提交 dev：`26ef506`
2. worktree 提交本单 8 文件：`bd3ec68`
3. `--no-ff` 合并 `feat/ach04-instrument` → dev（ort 策略，零冲突，dev 头原为 FE-ACH-05A ach05，文件零交集）
4. 合并后主仓三绿复验：type-check 0 错 / 双自检 ✓ / build 23.23s
5. 推送 `origin/dev`：`4ff9874..ef62ac6`
6. 清理：停 3214 dev server → worktree `ach04-instrument` 移除 → 分支 `feat/ach04-instrument` 删除（截图证据先归档至编排仓 `agent-handoffs/科技成果展示-ACH/assets-fe-ach-04a/`，7 张）
