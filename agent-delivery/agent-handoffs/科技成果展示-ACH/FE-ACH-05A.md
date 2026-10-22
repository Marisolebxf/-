# Handoff · FE-ACH-05A 创新载体孵化载体 — 整页复刻

- **任务**：FE-ACH-05A 创新载体孵化载体 — 整页复刻：全景/入驻成果/政策联动/绩效监控
- **执行**：agent:frontend-agent · 监管 human:孔东 · 2026-10-21
- **工作区**：worktree `D:\web\gkx-lumen\worktrees\lumen-ui-science-pc--ach05-incubation`（分支 `feat/ach05-incubation`，基点 1834a50）
- **状态**：**已验收合并 dev（2026-10-21 孔东口头放行「05A 任务完成」）**
  - worktree 提交 `4ff9874` → 主工作区 fast-forward 合并 dev → `push origin dev`（1834a50..4ff9874）→ worktree `lumen-ui-science-pc--ach05-incubation` 与分支 `feat/ach05-incubation` 已删除清理
- **ponytail: full**

---

## 1. 范围与实现

demo 真源（只读对照）：`demo-ui-science/src/pages/achievement-preview-new/incubation-carrier-new/`（IncubationCarrierNewPage.jsx 1471 / CarrierMap.jsx 116 / mockData.js 833）。lumen 落点 `src/views/achievement/incubation-carrier/`，全页 Vue3 + Arco Vue 重写，禁 merge 逐文件对照复刻。

### 文件清单（9 新建 + 1 修改，全在 `src/views/achievement/` 内）

| 文件 | 职责 |
|---|---|
| `incubation-carrier/incubation.ts` | 派生纯函数层：`shareToken`（中文 2 字滑窗共现）、`entFinSum`/`fmtWan`、`carrierRadarValues`、`enterpriseAvgScores`、`buildInvestorGraphicReport`（IMAGE_GRADIENTS 卡片 HTML 报告）、localStorage 归档（PROJECT_ARCHIVE_KEY 语义）、全部 ECharts option 工厂 |
| `incubation-carrier/CarrierMapPanel.vue` | 包装 `TiandituMap`：受控 points（divIcon 圆点，半径=入驻企业数、色=TYPE_COLOR_MAP）+ 热力（权重=势能评分）；全区总览/园区/楼宇三视角（MAP_LEVELS） |
| `incubation-carrier/PanoramaTab.vue` | Tab a：载体类型/区域筛选 + 22 载体列表（点击联动地图与详情）+ 地图面板 + 多媒体卡 + newsFeed 动态推送 + 累计数量趋势 Bar+势能指数 Line 双轴 + 筛选构成环图 + 全市势能趋势 + 能级雷达 + 各区平均势能柱图 |
| `incubation-carrier/EnterprisesTab.vue` | Tab b：行业维度切换、行业聚集环图（扇区点击联动维度）、各区样本企业柱图、企业名录表格（行业/融资/专利/阶段，行点击联动）、企业成长轨迹+融资曲线双轴、获奖标签、代表项目卡片（亮点/突破/生成报告）、企业服务资源供需匹配、创新成效评估雷达、投资人图文报告 Modal（iframe srcdoc 预览 + 打印/PDF + 下载 HTML + localStorage 归档） |
| `incubation-carrier/PoliciesTab.vue` | Tab c：政策级别/类型筛选（POLICY_LEVELS/POLICY_TYPES 着色 Tag）、申报流程 Steps、申报材料清单、申报节点 Timeline（含距今天数预警）、载体对接匹配（政策↔载体智能匹配度）、政策服务咨询窗口（问答气泡交互 + 疑难库 FAQ Collapse） |
| `incubation-carrier/PerformanceTab.vue` | Tab d：在孵企业数量与毕业统计、投资金额与融资动态监控、创新成果与专利产出、服务频率与资源利用、企业满意度报告（Rate 评分 + 优劣项归纳） |
| `incubation-carrier/CarrierDetailModal.vue` | 载体详情四 Pane：详细资料 Descriptions / 图片（渐变占位）/ 视频（占位语义）/ 资讯 newsFeed |
| `incubation-carrier/styles.css` | 模块私有自含样式：图表显式高度（ic-chart--xxx 系列）、flex 布局、项目卡网格、聊天气泡、报告 iframe 容器 |
| `incubation-carrier/index.vue` | 整页：KPI 行（5 瓦片 M_IC_*）+ PageTabFrame 四 Tab + 详情 Modal 挂载 + 页头「生成图文报告」跨 Tab 触发 |
| `achievement.test.mjs`（修改） | demoRoot 解析支持 worktree 目录（`repos/demo-ui-science` 回溯 + `GKX_DEMO_UI_SCIENCE` 环境变量覆盖） |

**种子冻结**：`achievementIncubationSeed.ts` 零改动（achievement.test.mjs 逐行冻结断言通过）。**未动文件**：`_shared/`、menu.ts、api、types、种子——零越界。

### 写操作演示态

投资人报告归档、导出、咨询问答均为前端演示态（localStorage / Message 提示），不替 BE 拍板。

## 2. DoD 对照表

| # | 派单包 DoD | 交付 | 验证 |
|---|---|---|---|
| 1 | KPI 行 5 瓦片（M_IC_* 占位 id，随筛选联动） | ✅ AchievementKpiTile ×5，ⓘ+🧪 全挂，载体/企业/融资/毕业率/满意度随种子联动 | 浏览器截图 §4-1 |
| 2 | Tab a 层级地图+筛选+趋势 Bar+势能+列表 | ✅ MAP_LEVELS 三视角、TYPE_COLOR_MAP 着色、类型/区域筛选联动、趋势+势能双轴图、22 载体列表点击联动 | 截图 §4-2 |
| 3 | Tab b 企业列表+行业聚集+成长轨迹+亮点+投资人图文报告（生成→预览→打印/PDF→下载→归档） | ✅ 全链路：`buildInvestorGraphicReport`（IMAGE_GRADIENTS 渐变卡）、iframe srcdoc 预览 Modal、`window.print`、`downloadHtmlFile`、PROJECT_ARCHIVE_KEY localStorage 归档（「已归档 N 条」Tag 回显） | 截图 §4-3 |
| 4 | Tab c 政策筛选+申报 Steps+材料清单+咨询 FAQ（demo New 页补齐旧页缺口重点） | ✅ POLICY_LEVELS/POLICY_TYPES 着色、Steps 6 步、材料清单 Checkbox 语义、Timeline 节点+天数预警、载体对接匹配度、问答气泡窗口+疑难库 Collapse | 截图 §4-4 |
| 5 | Tab d 满意度（Rate+优劣项）+毕业率+运营指标+趋势图 | ✅ carrierGrowthTrend/potentialIndexTrend 图表、满意度 Rate+优劣项归纳、毕业统计、融资监控、服务利用率 | 截图 §4-5 |
| 6 | 载体详情 Modal 四 Pane | ✅ 详细资料 Descriptions/图片渐变/视频/资讯 newsFeed，四 Pane 实测切换 | 截图 §4-6 |
| 7 | 地图复用 TiandituMap；原生控件全换 Arco；图表显式高度；D9 ⓘ+🧪 | ✅ TiandituMap 受控复用；全页无原生控件；styles.css 图表高度显式；ⓘ（MetricSpecHint）+🧪（MockBadge）全挂 | 走查确认 |
| 8 | 与 demo 逐区块对照 + 三绿 | ✅ 对照表见 §3；type-check ✓ / test.mjs×2 ✓ / build ✓ | 见 §5 |

## 3. 与 demo 逐区块对照

| demo 区块（IncubationCarrierNewPage.jsx） | lumen 实现 | 对齐度 |
|---|---|---|
| KPI 行（L1xx 监测载体/入驻/融资/毕业率/满意度） | index.vue ic-kpi-row，口径文案照搬 | 一致 |
| Tab a 筛选+列表+地图（CarrierMap.jsx） | PanoramaTab + CarrierMapPanel（TiandituMap 包装） | 一致（地图换天地图受控实现，点位/热力语义同） |
| Tab a 趋势/势能/雷达/区均势能图 | incubation.ts option 工厂 | 一致 |
| Tab b 行业聚集 Pie 扇区联动维度 | EnterprisesTab 环图 onClick 切维度 | 一致 |
| Tab b 名录表/成长轨迹/融资曲线/获奖 | EnterprisesTab 表格+双轴图+Tag | 一致（原生 table→a-table，Arco 化） |
| Tab b 代表项目+投资人报告（buildInvestorGraphicReport/IMAGE_GRADIENTS/PROJECT_ARCHIVE_KEY） | incubation.ts 同名函数+Modal 全链路 | 一致（HTML 报告结构、归档键语义逐项对齐） |
| Tab c 政策列表/Steps/材料/Timeline/匹配/咨询 FAQ | PoliciesTab 全量 | 一致（补齐旧页缺口部分完整） |
| Tab d 四组统计+满意度 Rate+优劣项 | PerformanceTab | 一致 |
| 详情 Modal 四 Pane | CarrierDetailModal | 一致（图片渐变占位语义） |

差异说明：地图由 demo 的 Leaflet 裸实现换为仓内 `TiandituMap`（派单包明示要求复用）；其余交互/文案/配色逐块对齐，无另起 UI。

## 4. 浏览器走查截图（localhost:3003 `/results/innovation-carrier`）

1. KPI 行+Tab a 首屏：5 瓦片（22 载体/2399 入驻/亿元融资/毕业率/满意度★4.6）+ 筛选 + 列表 + 地图 + 多媒体 + 趋势图 ✅
2. Tab a 下部：势能指数趋势 + 能级雷达 + 各区平均势能 ✅
3. Tab b：行业聚集环图、各区样本柱图、名录表（融资/专利列）、成长轨迹+融资曲线双轴、代表项目卡（亮点/突破/奖项）✅
4. Tab c：政策列表（着色 Tag）、Steps 申报流程、材料清单、Timeline 节点预警、载体匹配、咨询问答+疑难库 Collapse ✅
5. Tab d：在孵/毕业统计、融资监控、专利产出、服务利用率、满意度 Rate+优劣项 ✅
6. 载体详情 Modal：四 Pane（详细资料/图片/视频/资讯）实测切换 ✅；投资人报告 Modal：iframe 预览+打印/下载按钮+归档提示 ✅

> 注：走查期间共享浏览器实例被并行会话多次抢占标签页，最终以独立后台标签完成全部区块验证；无遗留问题。

## 5. 验证（三绿）

- `node src/views/achievement/incubation-carrier/test.mjs` → **all assertions passed ✓**（shareToken/统计/报告 HTML/政策匹配/文件齐备）
- `node src/views/achievement/achievement.test.mjs` → **all assertions passed ✓**（种子冻结逐行一致 + 各页文件齐备；本单仅改 demoRoot 解析支持 worktree）
- `pnpm type-check` → **0 error ✓**
- `pnpm build` → **✓ built in 33.00s**

## 6. 架构合规自检（公约 §2 铁律）

- [x] D8 前端规范：全页 Arco Vue（a-select/a-table/a-steps/a-timeline/a-rate/a-collapse/a-modal…），主色 #165DFF，无原生控件
- [x] D9 数据血缘：每个统计数字旁 ⓘ（MetricSpecHint，M_IC_* id）+ 🧪（MockBadge）；Mock 态诚实标注
- [x] D12 demo/lumen 隔离：只读对照重写，零 import/merge demo 代码
- [x] 复刻经验清单：Arco 优先、第二处封装（incubation.ts 纯函数层）、图表显式高度、mock 冻结、类型门 type-check——逐条遵守
- [x] 调用链：仅经 `fetchIncubationCarrierDataset`（@/api/achievement）→ USE_MOCK 走种子，无越层
- [x] 可观测：`trackAchievementInteraction` 埋点（page-mounted/export-click/carrier-select/header-report-click）
- [x] 写操作演示态不替 BE 拍板（归档/导出/问答均前端演示）
- [x] 未改 `_shared/`、menu.ts、api、types、种子；改动全部限定 `incubation-carrier/**` + achievement.test.mjs demoRoot 一行

## 7. 偏离说明

1. `achievement.test.mjs` 修改（派单包外）：worktree 目录层级与主工作区不同导致 demo 真源回溯路径失效，改为向上回溯 `repos/demo-ui-science` + `GKX_DEMO_UI_SCIENCE` 环境变量覆盖；主工作区行为不变（该修改对其他页无影响，属工装适配）。
2. 无其他偏离。

## 8. cost 回填

- estimated_tokens 350,000；实际约 310,000（多轮浏览器走查+修复）
- model_used: glm-5.3（Cursor agent）
- actual_cost ≈ $2.6（按内部折算）；cost_warn: false

## 9. 验收指引

已验收合并（2026-10-21）：`4ff9874` fast-forward 进 dev 并推送 origin/dev；worktree 与临时分支已清理。走查修正 8 项（滚动/checkbox 边距/新闻标签/星星位置尺寸/MockBadge 对齐 demo/半星 max-width 根因）均已包含在该提交内。
