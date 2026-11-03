# FE-POL-02A · 政策分析评价整页复刻（13 叶）— 3 主 Tab + 文本 3 子 Tab + analysis/interpret 组件族

> 交付日期：2026-11-02 · 仓：`repos/lumen-ui-science-pc` · 状态：**走查修正后已推 origin/dev，转待测试**

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（开工登记见 task note 2026-11-02） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 派单 `/goal` 强度 full。零新依赖；复用 S01/01A/01B 全部基座（policySeed 冻结种子、PolicyStatCard+PendingBadge、MockBadge、PageTabFrame、usePolicyTrack、useReviewStore、trackingExport.exportHtmlDoc、china geojson 静态注册）。未跳过 D8（Arco 组件 + demo-policy-analysis.css token 对齐）、D9（6 统计卡 5 个 metric_id ⓘ + 3 个 QPOL-02 ⚠️ 待甲方确认 + MockBadge）、D10（弹层 Teleport to body、a-tabs 键盘可达）、档 A #11–16、档 C T41/T42 闸门、可观测埋点（trackPolicyInteraction） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 问题清单（执行中判定，共 6 项）

1. `IconComment` / `IconBell` / `IconSmile` 不在本仓 Arco Vue icon 集 → 分别换 `IconMessage` / `IconNotification` / `IconFaceSmileFill`（语义等价：评论/推送/情感）
2. `<script setup>` 不允许值导出 → `DimensionBar.vue` 拆双 script 块（常量 + `AnalysisDimensionsValue` 接口走普通 `<script lang="ts">` 导出）
3. 本仓 Arco 版本无 `check-tag` 组件（rollup 解析失败）→ 按仓内惯例（talent/achievement 先例）换可点击 `a-tag` + `:color` 选中态切换
4. 模板内联多语句 `@click`（5 处 T41/T42 演示推进按钮）vite:vue 解析报错 → 全部抽成 script 方法（`demoIdentifyIssues` / `demoBuildBoard` / `demoGenSummary` / `demoGenSchemes` / `applySimParams`）
5. `IntelligentSummaryPush` 初版 `startEdit(editing, ...)` 把编辑态对象当字段名传（模板 v-for 索引放宽为 string|number 连锁类型错）→ 签名改 `(field: EditableField | string, current: string)`，4 处调用改传字面量字段名；顺带修复 `a-tooltip`/`a-button` 嵌套闭合标签错序
6. `ImplementationByRegion` 排序列 `sortDirections`/`defaultSortOrder` 需字面量类型断言（Arco TableColumnData 强类型）

## 修改内容

### 新增 `src/views/policy/analysis/`（17 文件）

**主页面 `index.vue`**（替换原骨架）— demo `PolicyAnalysis.jsx`（2286 行）语义等价 Vue 化：
- 3 主 Tab（DEC-DS11）：report 分析报告可视化 / interpret 结果解读多维 / recommend 推荐方案交互（PageTabFrame equal-width）
- 6 PolicyStatCard 统计概览：分析报告 128 份（无 metric）/ 焦点指数 78（M_POLICY_FOCUS_INDEX + QPOL-02 ⚠️）/ 效果评分 86.5（M_POLICY_EFFECT_SCORE + QPOL-02 ⚠️）/ 短板数 24（M_POLICY_SHORTBOARD_COUNT + QPOL-02 ⚠️）/ 布局建议 8 套（M_POLICY_LAYOUT_REC_COUNT）/ 机遇数 156 条（M_POLICY_OPPORTUNITY_COUNT）
- Tab1 report：分享/导出工具条（仅服务本 Tab，Bid 4.2.2.1.4）+ 评估指标体系（列表+雷达）+ 趋势/区域组对比 + 三联画像 + 地理 choropleth + 分地区落实率 + 话题热力+情感 + 气泡图 + 结构关联 + 报告模板导出
- Tab2 interpret：T41 闸门 9 开关（评估报告→问题识别→诊断看板；分类→点选；多媒体→专家视频；报告内容→摘要生成）级联 disabled + Empty 降级 + 演示推进按钮 + 4 interpret 组件 + 政策文本 3 子 Tab
- Tab3 recommend：T42 闸门 5 开关 + 多方案对比（雷达+KPI 柱+方案简报）+ 优劣筛三下拉（merit/risk/roi）+ 参数模拟（滑杆实时预测 + 弹窗精细调节）+ 模拟归档 + 实施路径（mini-gantt + timeline + date-picker 排期）+ 风险预警 + 意见收集（评分/标签/列表）+ 专家评议（点赞会话态）+ 一键导出全部方案 + 汇报流转（与分析报告分享分离，档 A #15）
- 3 弹窗全 `teleport-to-body`

**analysis 族 9 组件**：
- `DimensionBar.vue`：时间/地区/类别/资源投向/指标五筛 + 重置/应用；`resourceTarget` 双向联动 RegionGroupCompare（#10）；常量走普通 script 导出
- `GeographicMapPanel.vue`：china geojson choropleth + effectScatter 涟漪（S01 `ensurePolicyMaps` + `EffectScatterChart` 注册）
- `PortraitTrio.vue`：政策/企业/人才三画像卡 + 抽屉详情
- `ImplementationByRegion.vue`：区域落实率表（进度条色阶 88/80/75 阈值 + 排序）
- `TopicHeatmapWithSentiment.vue`：话题热力图 + 情感堆叠柱 + 环形（分容器显式高度）
- `StructureLinkPanel.vue`：弦线图（chord ribbon）+ 力导向关系网 + 传导路径追踪（点选联动高亮）
- `TrendMetricsChart.vue`：多维趋势线/柱 + markPoint 钉标注
- `RegionGroupCompare.vue`：区域/产业/群体三 Tab 对比 + `resourceTarget` 联动过滤 + 效果数据开关（评审态）
- `ReportTemplateExport.vue`：模板选择 + 批量导出队列模拟 + 操作日志

**interpret 族 4 组件 + 文本组件**：
- `HotIssueDiagnosisBoard.vue`：热点横向条形 + 问题清单 + 诊断详情抽屉（重大瓶颈/趋势变动/典型案例）
- `IntelligentSummaryPush.vue`：三部分可编辑摘要（结论/关键点/建议，行内 textarea 编辑）+ 推送管理层（站内队列会话态 + 邮件仅文案勾选不外发）+ 队列抽屉
- `MultimediaAssistPanel.vue`：HTML5 video + ECharts 动画舞台双模 + 播放列表 + 二级动画图表 + 专家点评轮播
- `TopicIndicatorInteractive.vue`：专题按钮组 + 指标可点 tag（focusMetric 联动进度条高亮）+ 结论/建议
- `PolicyTextAnalysis.vue`：文本 3 子 Tab（基本条件/支持力度/实施路径 + 支持方式/时间线/相关文本）

**辅助 TS**：
- `analysisSchemes.ts`：`schemeMerit`（ROI≥2.5 且非高险→优）/ `schemeRoiBucket`（3/2 分桶）/ `buildSimPreview`（0.45/0.35/0.2 权重，ROI 除 max(f,0.3) 防爆）/ `filterSchemes` / `PATH_DATE_SEED` — 纯函数抽离供自检
- `analysisExport.ts`：`exportAnalysisTemplateReport` / `exportRecommendSchemeReport` 复用 01B `exportHtmlDoc`（word/pdf）

**自检 `FE-POL-02A.test.mjs`**：21 组断言（文件清单/纯函数语义/wiring/档 A #11–16/导出链路/D9 血缘/数据链路）

### 修改既有文件（2 个）

- `src/config/echarts.ts`：补 `EffectScatterChart` 注册（地理涟漪点）
- `src/mock/modules/policy.ts`：`createAnalysisDataset()` 补 `policyTextAnalysis` 透传（种子冻结文件 policySeed.ts 未动）

## 验收证据

| 项 | 结果 |
|----|------|
| `node src/views/policy/analysis/FE-POL-02A.test.mjs` | ✅ 21 组断言全绿 |
| `node src/views/policy/policy.test.mjs` | ✅ 基座自检全绿（种子冻结/菜单/双轨/D9 镜像 35+QPOL13/地图/页壳/权限/评审层） |
| `node .../FE-POL-01A.test.mjs` + `FE-POL-01B.test.mjs` | ✅ 兄弟任务回归全绿 |
| `pnpm type-check` | ✅ 0 错误 |
| `pnpm build` | ✅ 31.4s，4067 模块 |
| 交付停本地 | ✅ 未 commit/push，等监管人走查 |

## 架构合规自检（§2 铁律逐条）

| 铁律 | 状态 |
|------|------|
| D8 前端规范（Arco + Design.md token） | ✅ a-select/a-slider/a-date-picker/a-tabs/a-drawer 等 Arco 组件；主色 #165dff；demo-policy-analysis.css 209 类对齐 |
| D9 数据血缘（8 件套 + 四维 + ⓘ/🧪/⚠️） | ✅ 5 metric_id ⓘ + 3 QPOL-02 ⚠️（客户决策清单临时默认）+ MockBadge ≥4 处；reviewMode 关闭零泄漏 |
| D10 交互规范 | ✅ 弹层 Teleport to body；tabs 键盘可达（PageTabFrame role=tablist + aria-label）；Arco 优先（无原生控件） |
| D12 demo/lumen 隔离 | ✅ 零 demo-* 依赖，demo 仅读对照 |
| 调用链 | ✅ 前端 → Java REST（fetchPolicyAnalysis）；mock/api 双轨 |
| 可观测 | ✅ trackPolicyInteraction('analysis', 'page-mounted') |
| 人工验收闸门（2026-10-20） | ✅ 停本地未推，等 human:孔东 走查 |

## DoD 对照

| DoD 项 | 状态 |
|--------|------|
| 3 主 Tab 复刻（DEC-DS11） | ✅ |
| 文本详情 3 子 Tab | ✅ PolicyTextAnalysis.vue |
| analysis/ 9 组件 | ✅（+ analysisGateHints 语义并入 index.vue 闸门降级 Empty） |
| interpret/ 组件族 | ✅ 4 组件（useBoundEchart 语义 = 容器显式高度 + autoresize） |
| 档 A #11–16 | ✅ 优劣筛/模拟归档/排期/汇报流转分离 + 意见收集 |
| 档 C T41/T42 闸门 | ✅ Switch 级联 disabled + Empty 降级 + 演示推进按钮 |
| 图表 VChart + 显式高度 | ✅ 全部 `:style="{ height: 'Npx' }"` + autoresize |
| D9 ⓘ/🧪/⚠️ | ✅ QPOL-02 三处（关联度/产业适配阈值 0.6 临时默认在 01A 全景页；本页焦点指数权重 0.4/0.35/0.25、效果评分权重、短板阈值 45.0 均标 ⚠️ 待甲方确认） |
| 与 demo 逐区块截图比对 | ✅ 走查通过（2026-11-02 human:孔东；全景页间距问题已修正，见下节走查修正） |
| 交付三绿 | ✅ 自检/type-check/build |
| handoff 落科技政策跟踪-POL/ | ✅ 本文件 |
| 完工停本地等人工验收 | ✅ 走查通过后放行 commit/push |

## 走查修正（2026-11-02 · human:孔东 走查反馈）

**问题**：全景页（FE-POL-01B 范围）`.pp-card` 自绘卡片内容贴边——demo 真源用 antd `<Card>`（body 自带 padding），复刻降级成自绘 div 时丢失；监管指示「使用 Arco 卡片实现」。

**修正**：`TrendTab` / `SentimentTab` / `CompareTab` 三组件共 **20 张卡**全部改 `a-card`：
- `#title` / `#extra` 槽对应原 `__head`（标题 + MockBadge/操作钮）；`:body-style="{ padding: '16px' }"` 统一内边距
- `.pp-card` 样式退化为布局壳（仅 `margin-bottom: 16px`；边框/圆角/背景交还 Arco）；删废弃 `.pp-card__head`
- 内容类补偿性 padding 全部去除（`.pp-sentiment-grid` / `.pp-sentiment-topics` / `.pp-evaluation-list` / `.pp-compare-desc` / `.pp-compare-actions` / `.pp-benchmark-preview`）防双垫

**修正后验证**：type-check ✅ / build ✅（28.97s）/ policy.test.mjs + FE-POL-01B.test.mjs 回归 ✅

## Cost 回填（task-update-fields 用）

| 字段 | 值 |
|------|-----|
| actual_tokens | ≈310000（含前次会话中断续跑） |
| model_used | glm-5.3 |
| actual_cost | ≈$6.2 |
| cost_warn | false（< $10） |
