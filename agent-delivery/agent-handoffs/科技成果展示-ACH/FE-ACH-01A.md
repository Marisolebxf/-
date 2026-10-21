# FE-ACH-01A · 软科学成果展示 — 整页复刻

- **任务**：FE-ACH-01A（Epic：E-FE-ACHIEVEMENT）
- **执行**：agent:frontend-agent（监管 human:孔东）
- **日期**：2026-10-21
- **状态**：联调中（integration）；走查通过，监管人授权 commit → merge → push origin/dev，临时分支已清理
- **ponytail**：full
- **worktree**：已清理（分支 `feat/ach01-soft-science` 基点 1834a50，commit 7496254，经 merge 8ec5d94 并入 dev 并推送）

## 1. 范围与实现（对照派单 DoD §3 逐项）

| DoD | 落点 | 说明 |
|---|---|---|
| 1 组合筛选 | `soft-science/index.vue` 左栏 | 年度 `a-slider range` / 单位类型+课题主题 `a-checkbox-group` / 成果标签 `a-tag checkable` / 省市区 `a-cascader`（`path-mode`+`check-strictly` 等价 demo `changeOnSelect`+`expand-trigger="hover"`）/ 方案 localStorage（`soft-science-new-filter-schemes`，存/复用/删/重置，上限 8 条同 demo） |
| 2 五级地图 | `components/SoftScienceMapSection.vue` + `softScienceMapNodes.ts` | country→province→city→district→unit 逐级下钻（`handleDrill` demo 冻结语义，city 级取 `node.items[0].district \|\| node.label`）；热力层（`heatOn` 开关 + `buildHeatPoints` 冻结强度算法）；视口 `buildMapView` 每级中心/zoom（TiandituMap 内部 safeSetView/flyTo）；**列表悬停↔节点高亮**（`getNodeKeyForTopic` p:/c:/t:/d:/u: 前缀约定，hover 置于卡片 → `highlightKey` → divIcon 红 `#F53F3F` 12px/加 zIndexOffset）；复用 `TiandituMap`（props 传 marker/heat/视口，零页内 leaflet init）；瓦片复原 `.ss-map-frame .leaflet-tile { max-width: none }`；demo CircleMarker 半径语义 → divIcon 直径（尺寸/透明度/描边对齐） |
| 3 智能检索列表 | `index.vue` 中栏下卡 | 7 种排序（SORT_OPTIONS 冻结）；难题类型优选多选（命中紫标「优选」+整组置顶，组内按当前排序键）；热词/新兴主题 tag 点击回填关键词；课题详情 `a-modal` + `a-descriptions`（demo 字段逐行，含贡献度/代表成果）；「查看完整详情」跳 detail Tab |
| 4 底部 5 Tab | `components/SoftScience{Detail,Stats,Interaction,Export,Progress}Tab.vue` | 成果详情与案例（课题切换 select、附件/归档按钮、攻关历程 timeline、三案例卡、影响力评分+采纳率+反馈列表）/ 多维统计（年度 slider+marks、5 图表：年度线/类型饼(点击联动)/成果演化三线/单位+区域 Top8 横条(点击联动定位)/机构饼+速览、批量导出 modal Excel/CSV/PDF 真实下载）/ 互动传播（评论流+点赞+专家答疑、评论入库知识库 modal localStorage、关注/收藏/推送开关、多渠道分享、互动趋势图）/ 导出报告（4 格式快捷导出、模板 radio、审计表格、角色字段配置）/ 进展监控（步骤条、阶段归档、阶段评分提交、阶段分布图、滞后预警 alert、全周期历史 timeline 检索） |
| 5 Arco 全替 | 全组件 | demo 原生控件零残留；已知坑按经验清单 §1 根因修法（`#option` 用 `:options`/`a-option`、图标显式 import、label 不包裹 select） |
| 6 图表 | `softScienceCharts.ts` | 容器显式高度（`.ss-chart--trend/panel/rank/mini`）防 init 0 高死锁；echarts.ts 已含所需类型零新增注册 |
| 7 D9 | 全组件 | KPI 5 枚经 `AchievementKpiTile`（内部 ⓘ+🧪）；地图/统计/互动卡直接挂 `MetricSpecHint`+`MockBadge`；metricId 沿用 demo 冻结值（M_SS_TOPIC_TOTAL 等 15+ 枚） |
| 8 写操作 | 各 Tab | 筛选方案/评论知识库/详情归档/关注收藏均 localStorage 会话演示态，不替 BE 拍板 |
| 9 自检 | `soft-science/softScience.test.mjs` | ①文件存在性 ②冻结语义锚点（localStorage key/handleDrill/7 排序键/5 Tab 标题）③纯逻辑内联复算（getContribution 含预算封顶、filterPanelTopics 三段区划、applyMapFocus 分级比对、nodeKey 前缀、province 聚合、优选置顶组内贡献度降序）④D9 锚点；三绿见 §3 |

## 2. 文件结构（本单新建/修改）

```
src/views/achievement/soft-science/
├── index.vue                      # 整页组装（KPI 行/左筛选/中地图+检索/底部 5 Tab/详情 Modal）
├── soft-science.css               # demo 内联样式 → class 化（.ss-* 前缀自含）
├── softScienceLogic.ts            # 筛选/排序/贡献度/关键词/nodeKey 纯逻辑（列表+地图+自检三处消费，抽层）
├── softScienceMapNodes.ts         # 五级节点聚合/视口/热力点（MapSection+自检两处消费）
├── softScienceCharts.ts           # 8 类图表 option 组装（token 复用 chartOptions baseTooltip）
├── softScienceExport.ts           # 贡献度报表 sheets/XLS/CSV/PDF 打印（demo 冻结算法）
├── softScience.test.mjs           # 最小自检
└── components/
    ├── SoftScienceMapSection.vue      # a：五级地图+趋势图+区域对比
    ├── SoftScienceDetailTab.vue       # c：详情与案例
    ├── SoftScienceStatsTab.vue        # d：多维统计
    ├── SoftScienceInteractionTab.vue  # e：互动传播
    ├── SoftScienceExportTab.vue       # f：导出报告
    └── SoftScienceProgressTab.vue     # g：进展监控
```

## 3. 验收证据（三绿）

- `pnpm type-check`（vue-tsc --build）：**exit 0**（0 errors）
- `node src/views/achievement/soft-science/softScience.test.mjs`：**all assertions passed ✓**（含样式接线防回归断言）
- `node src/views/achievement/achievement.test.mjs`（S01 基座自检，回归）：**all assertions passed ✓**
- `pnpm build`：**✓ built in 25.13s**（`achievement-*.js` 进产物；共享样式 `ach-kpi-tile__value{font-size:24px}` 已验证在 styles chunk）
- dev 走查：`http://localhost:5211/results/soft-science-achievements`（worktree dev server，2026-10-21 晚起）

## 4. 架构合规自检（公约 §2）

- ✅ 调用链：消费 S01 `fetchSoftScienceDataset` 双轨 API；real 路径占位不变
- ✅ D8 Design：主色 `#165DFF`/底 `#D8E7FC`/正文 14px/控件 32px/圆角 4-8/阴影 `0 1px 4px rgba(22,93,255,0.08)` 冻结 demo；全 Arco 组件
- ✅ D9 血缘：每个统计数字旁 ⓘ（MetricSpecHint）+ 🧪（MockBadge）并存排列「数字→ⓘ→🧪」；metricId 沿用 demo 冻结值；评审门控组件经 `reviewMode` 全局开关自闸
- ✅ D10 交互：Arco 组件原生键盘/焦点语义保留；tablist aria-label
- ✅ D12 隔离：零 import demo-*；逻辑为 demo 语义移植非代码复制
- ✅ 可观测：`trackAchievementInteraction`（page-mounted/export 埋点，traceId）
- ✅ 复刻三防：`USE_MOCK=false` 空数据显 a-empty（零 fixture 填数）；种子零改动；写操作不替 BE 拍板

## 5. 偏离说明（含公共件扩展登记）

1. **`_shared/AchievementSectionCard.vue` 加 `#title` slot（回落 title prop）**：demo 的 title prop 接收 ReactNode（含 ⓘ/🧪/图标），S01 版只有 string prop，本页及子组件需富标题——在公共件加 slot 为**根因修法**（否则 6+ 处标题富内容被静默丢弃）。纯向后兼容增量，S01 存量消费（纯 string title）行为不变。
2. **`components/workbench/PageTabFrame.vue` tab 定义加可选 `icon?: Component`**：demo BottomTabs 五个 tab label 均带图标，Arco `a-tab-pane` 经 `#title` slot 渲染图标+文字。不传 icon 时与原版渲染完全一致（其他 10+ 消费方零影响）。
3. **检索按钮无「检索」文字**：Arco Vue `a-input-search` 的 `search-button` 为 boolean（React 版可传字符串），Vue 版只能图标按钮——组件能力差异，语义一致。
4. **demo BottomTabs `topics={filtered.length ? filtered : TOPICS}` 回退**：整页 topics 经同一 computed 传递，语义保留。

### 5.1 走查修正（2026-10-21 晚，dev 5211 实测）

- **P0 样式裸奔修复**：整页重写时 `index.vue` 丢了 `import '../_shared/styles.css'`，页壳底色/KPI 瓦片（24px 值、12px 16px padding）/SectionCard 阴影全部失效（tile 实测 46px → 应 118px）。已补 import 并产物验证（`ach-kpi-tile__value{font-size:24px}` 进 styles chunk）；自检新增防回归断言（import 丢失必红）。
- **整页纵向滚动**：fullBleed 壳 `.content-shell--flush` 为 `overflow:hidden`，软科学整页（KPI+筛选+地图+列表+5 Tab）超出视口被裁死。根因修法在共用页壳 `.ach-page` 加 `height:100%; overflow-y:auto`（demo 语义即整页滚动；短页内容不满时无滚动条，行为不变）。
- **样式 token 对照扫描**：`scripts/style-diff-ach01.mjs`（一次性走查工具，不进构建）扫 demo 3 主文件 383 个内联 token，91% 直接命中 CSS；未命中项人工复核全部为「组件内联样式已实现」（width 320/280/720、Rate 11px、#FF7D00 新兴主题等）或数值单位书写差异，无视觉缺口。
- 浏览器 CDP 与并行验收会话抢标签：改用源码级对照 + dev server HTTP 探测（`/src/views/achievement/_shared/styles.css` 200）验证。

## 6. 遗留风险

- 评审走查建议覆盖：五级下钻（含 district「未分区」分支）、cascader 三段筛选与地图联动、列表悬停高亮、优选+7 排序组合、批量导出 CSV/PDF 真实落盘、知识库 localStorage 持久化
- metricId 仍为 demo 冻结占位值，待 metric-registry 正式登记后正名（同 S01 §6）

## 7. 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## 8. CI/CD

- commit：`7496254`（feat 分支）→ merge `8ec5d94`（--no-ff 入 dev；冲突 `_shared/styles.css` `.ach-page` 滚动规则两侧同语义，保留 dev 版完整规则）
- push：`origin/dev` `9881287..8ec5d94`（2026-10-21），pipeline 由 push 触发
- worktree `lumen-ui-science-pc--ach01-soft-science` 与分支 `feat/ach01-soft-science` 已删除（已合入，安全清理）

## 9. 涉及文件

- 新建：`src/views/achievement/soft-science/**`（12 文件，见 §2）
- 修改：`src/views/achievement/_shared/AchievementSectionCard.vue`（#title slot，§5.1）
- 修改：`src/components/workbench/PageTabFrame.vue`（可选 icon，§5.2）
- 未动：menu.ts / api / types / mock 种子（派单 §4 红线遵守）
