# FE-TS-08A · 科技指数（M8）整页复刻 — 前端交付（联调中）

> 仓库：`repos/lumen-ui-science-pc`；路由 `/trend/tech-index`（`menu.ts` → `tech-index`，fullBleed）。
> 状态：**联调中**（mock 点测通过；`API-TS-M8` 冻结后 `USE_MOCK=false` 对接 Java）。
> demo 真源：`demo-ui-science/src/pages/tech-index/`（`index.jsx` + `mockData.js` + `style.css` + 10 组件 jsx）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | demo 单文件按 Tab/组件拆分 + mock 种子单文件冻结（确定性生成、派生链禁手写）；首屏同步种子对齐 demo 直接 import 语义；复用 PageTabFrame/IndustrySelect/SearchableCascadeFilter/MetricSpecHint；china GeoJSON 静态注册（不 fetch 外网）；无新 npm 包。 |

## 范围与实现（对照 DoD）

| DoD 项 | 实现 |
|---|---|
| 指标树：三级缩进 + 权重说明 + 赋权方法 + 版本历史 | `IndicatorTab.vue` = `IndicatorTreePanel`（搜索 + 权重标签）+ `IndicatorDetailPanel`（指标项/权重展示[设置方法/本指标赋权依据]/概述/计算方法/意义解读/下级指标六卡）+ `VersionComparePanel`（权重折线 + 版本明细表 + 变更历程 timeline）+ 权重指南 Modal（AHP+德尔菲四步骤 + 一级权重 + 说明） |
| 可视化：34 省地图 + 专家 H 指数 + 四维趋势 + 活跃度雷达 | `VisualizationTab.vue`：筛选条（IndustrySelect 级联 + 机构类型/地域/时间/指标维度）+ 视图 Radio（map/expert-ranking/trend/activity/comparison 五视图）+ 实时刷新开关（30s 扰动）+ 大屏导航 + 导出 Modal + 区域/专家详情 Drawer。`RegionMapPanel` = `registerMap('china', chinaGeoJson)` + visualMap 渐变 + 三统计卡 + 工具栏（放大/缩小/复位/全屏）；`ExpertRankingPanel` Top3 金银铜；`TrendPanel` 四维折线（可用月份 <3 切柱状月视图）；`ActivityRadarPanel` 热力图 + 活跃构成雷达 + 时间窗 slider；`ComparisonPanel` 机构多选（≤10）+ 雷达 + 明细表 + 单指标排行 |
| 排行榜：四榜 + 33 条详情 + 四维得分构成 | `RankingTab.vue`：榜单 Radio（综合/高校/企业/科研）+ 搜索 + 领域级联 + 成果/机构/地域/时间/排名范围/得分区间七筛选；`RankingTablePanel`（rank 徽章 + 各维度得分行内标签 + 加入对比/详情）；`RankingDetailDrawer`（基本信息三卡 + 排行依据[评价方法/数据来源/排行依据] + 四维雷达进度 + 排名历史反转 y 轴走势）；`CompareDrawer`（已加入对象 ≤5 + 推荐加入 + 综合差异 + 单对象画像/多对象雷达柱图 + 趋势变化 + 分析摘要 + 对象强弱项 + 保存方案 ≤5 + footer 清空/保存/导出）；导出 Modal（范围 filtered/all/compare × 内容 5 项） |
| 专家评议：20 人名单只读 | `PeerReviewTab.vue`：AI 辅助评议建议（Mock）banner + 只读说明 + 20 人 a-table（活跃度降序） |
| Mock + 接口双轨 | `mock/modules/techIndex.ts` 种子逐字冻结 demo `mockData.js`（指标树 L4–L341 / 权重设置 / 20 专家 / 区域 34 / 趋势 / 视图字典；`applyEvaluationModel` 派生 totalScore/weightContributions/rank，`buildHistory` 派生历史）；`api/situation/techIndex.ts` 单端点 `tsTechIndexDataset`（demo 单页一次取全；`API-TS-M8` 冻结拆 5 端点时仅改本层） |
| D9 / build / handoff | 可视化视图与详情数据来源说明读种子；权重指南含「演示口径（Mock）」说明；`pnpm type-check` / `pnpm build` 绿；本文件 |

### 类型契约（联调）

- `types/techIndex.ts`：`IndicatorNode` / `IndicatorWeightSetting` / `IndicatorVersionHistory` / `RegionIndexItem` / `ExpertItem` / `RankingRecord`（含 `weightContributions` / `compareSourceLabel`）/ `RankingData` / `TrendPoint` / `TechIndexDataset`
- 真实路径（过渡）：`GET /situation/v1/tech-index/dataset`（一次取全，对齐 demo 顶层 import 语义）
- 契约草案 `API-TS-M8.md` 为五端点；冻结后**仅改 api 层**拼装，页面零改动

## 验收证据

- `pnpm type-check`：**0 error**（2026-10-17 最新）
- `pnpm build`：**绿**（3552 modules）
- 自检：`node src/views/situation/tech-index/techIndex.test.mjs` → **55 项全绿**（demo 三测试文件基线摘选：指标树权重和=1 / totalScore=40·30·20·10 加权和 / 榜内降序 rank 连续 / 综合榜=领域榜拼接 / 区域榜有序不重名 / 版本史最新权重=树权重 / 禁 Math.random / 接线 / 文案口径）
- 浏览器冒烟（human:孔东 本机）：四 Tab 全渲染；「加入对比」→ 已加入态；对比抽屉单对象画像 ↔ 多对象维度对比切换；详情抽屉四区齐；专家表 20 行（DOM 验证）
- 2026-10-17 迭代修复（4 轮用户反馈）：按钮圆角 4px（`3200adc`）；按钮组 solid 样式 + Tag 色值修正 + 地图同步注册修复 + 4 Tab 滚动（`7569756`）；工具栏 radio 组 32px + 子视图 100% 宽（`48037fa`）；**综合对比机构选择回填丢失**（`af94c7c`，根因：共享 `SearchableCascadeFilter` 的 footer 走 `a-cascader #popup-render` 插槽而 Arco cascader 无此插槽（只消费 empty/label/prefix），footer 从未渲染 → 无确认入口 → 关闭即丢 pending；修复：tech-index 页内新增 `ComparisonCascadeSelect.vue`（path-mode + triggerProps.contentClass 锚点 + Teleport 注入 footer + 600ms 防误关，交互对齐 demo `popupRender`），共享组件零改动）；实测：勾选→确认→回填 tag→已选 n/10→统计条→雷达→明细表全链路绿；GI 页回归不受影响
- 已 push：`f2a5c94` / `3200adc` / `7569756` / `48037fa` / `af94c7c` → `origin/dev`

## 联调确认（AV-1）

- 前端 mock 环境（`USE_MOCK=true`）功能路径已通：**联调确认**
- 后端：`API-TS-M8` 仍为草案；Java 路径/DTO 冻结后切换 `USE_MOCK=false` 验证 dataset（或拆分五端点后的等价数据）
- 联调入口：`pnpm dev` → `/trend/tech-index`

## 偏离说明

- demo 顶层 Tab 第三个 label 为「科技成果综合排名」（demo `techIndexRankingLayout.test.mjs` 断言「排行榜」的基线在 demo 侧已过期红灯），lumen 按 demo 现行代码逐字复刻
- 排行榜文案口径沿用 demo 现行子集（「排名对比分析/排名结果导出/排名详情查看/科技成果综合排名」为 demo 原文案保留），demo 测试中的禁词全集因基线过期未全量继承（自检按 demo 实际代码校准）
- 综合榜 rank = 领域内位次（demo 2c 语义），非综合榜内序号

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 FE→Java→Python | ✅ api 仅网关路径 `/situation/v1/tech-index/*` |
| D12 | ✅ USE_MOCK=false 不执行 mock 注册逻辑 |
| D8 | ✅ Arco Table/Drawer/Modal/Radio/Select/Slider/Descriptions/Progress + Design token（主色 #165DFF、ti-* 样式类对齐 demo style.css） |
| D9 | ✅ 权重指南/详情数据来源读种子含演示口径说明；M8 契约冻结后挂 MetricSpecHint（metric_id 占位见遗留） |
| D10 | ✅ 抽屉/弹窗/表格/滑块/开关键盘可达；地图工具栏 aria-label |
| 可观测 | ✅ `ts-tech-index-track` CustomEvent + createTraceId（tab-change） |
| 无新依赖 | ✅ 零新 npm 包（GeoJSON 为仓内静态资产） |

## CI/CD

- 目标分支：`origin/dev`；已 push `f2a5c94`（等 GitLab CI 绿 → K8s dev）

## 涉及文件（M8）

`src/views/situation/tech-index/**`（index + 4 tabs + 11 components + models + styles + test）、`src/api/situation/techIndex.ts`、`src/mock/modules/techIndex.ts`、`src/types/techIndex.ts`、`src/assets/china.geo.json`；`src/mock/register.ts`、`src/router/menu.ts`

## 遗留风险

- `metric_id` 占位：M8 指标（指数分/专家 H 指数/排行得分等）待 `API-TS-M8` 冻结后对接 MetricSpecHint 八件套（对齐 M1–M7 做法）
- 实时刷新扰动为演示语义（30s ±delta），正式环境按契约移除或接 WebSocket
- 对比方案/已保存方案为会话态（demo 同款），持久化待产品定义
- 共享 `SearchableCascadeFilter`（GI）的 footer 插槽问题为**存量缺陷**（antd `popupRender` 在 Arco cascader 无等价物），影响所有多选消费方（bay/shenzhen/tracking/innovation-evaluation/GI 自身）。本次按用户要求只修 tech-index 页且不动共享组件；如需统一修复，建议另立 chore 单页页内组件化或升级共享组件（需全页面回归）
