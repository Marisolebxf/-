# FE-POLICY-topic-pages —— 政策专题分析三页（POLICY-PROTO-L05）

- 角色：frontend-agent（Convoy worker，与门户层同仓同文件集归一执行）
- 仓：`demo-ui-topic`（React + Vite）  分支：`feat/policy-elements-build`（未直推 main）
- 任务：POLICY-PROTO-L05 专题分析三页（扩写 `src/app/pages/policy/`）
- 状态：✅ 已完成，`npm run build` 绿
- 日期：2026-06-23  ·  commit 标记：`[agent:frontend]`

---

## 1. 路由表

| 页面 | 路由 | 组件文件 | 导航入口（Layout）|
|---|---|---|---|
| A1 政策时序分析 | `/policy/overview` | `pages/policy/PolicyOverview.tsx` | 「政策」→ 政策时序分析 |
| A2 区域政策对比 | `/policy/analysis` | `pages/policy/PolicyAnalysis.tsx` | 「政策」→ 区域政策对比 |
| A3 深圳政策现状·三维框架 | `/policy/recommendation` | `pages/policy/PolicyRecommendation.tsx` | 「政策」→ 深圳政策现状分析 |

> 现有 3 路由原已注册，本次为**扩写而非新增路由**（recharts/Tailwind 原型 → Arco + ECharts 权威栈）。

---

## 2. 组件清单（新增 / 复用）

### 新增共享骨架 `pages/policy/policyShared.tsx`
- `PolicyMetricCard`：指标卡（数字 + 名称 + ⓘ MetricSpecCard + 🧪 MockBadge + ⚠️ PendingBadge + 方向徽标，升红/降绿/平灰）
- `usePolicyDetailDrawer`：政策画像抽屉（DR-04，原文跳转/收藏/分享 + 支持强度构成）
- `SecondaryAnalysisTabs`：右侧研判内切视图（line tabs，含埋点）
- `POLICY_COLORS` / `LEVEL_COLOR`：ECharts 取色常量（镜像 design-tokens.css 等值 hex，canvas 不能解析 CSS 变量）
- `POLICY_TRACK`：政策域埋点常量（统一 `policy_` 前缀）
- 复用基础层：`AnalysisShell` / `SectionPanel`（enterprise/analysisShared）、`MetricSpecCard` / `MockBadge` / `PendingBadge` / `StatusTag`、`EChart`、`ContextBar`、`track`

### 各页组件
| 页 | 关键组件 / 图表 |
|---|---|
| A1 | MetricCard×4（总数/密度/增长率/有效占比）· 密度趋势折线(窗口期标注) · 支持强度堆叠(资金/税收/土地/人才) · 政策关键节点时间轴(点选→画像) · 关键洞察 |
| A2 | 对比配置(区域多选≥2 + 评价维度勾选) · MetricCard×3 · 区域对比矩阵(领先浅蓝/落后浅警示, 单元点选→条款溯源) · SecondaryAnalysisTabs(雷达/热力/差异结论) |
| A3 | 三维框架配置(权重滑杆, **总权重=100% 校验拦截**) · MetricCard×3(短板维 warning 分色) · gauge 综合得分 · **三维雷达(支持力度/产业适配性/落地实效性 + 短板阈值虚线)** · 短板成因下钻(Collapse) · 优化策略卡 |

> A3「**支持力度 / 产业适配性 / 落地实效性雷达**」按派单要求落地（ECharts radar，深圳主蓝高亮 + 橙色短板阈值虚线）。

---

## 3. metric_id 映射（每统计数字旁 ⓘ + Wave0 🧪 + 待定 ⚠️）

| 页 | 指标卡 | metric_id | 备注 |
|---|---|---|---|
| A1 | 政策总数 | `M_POLICY_TOTAL_COUNT` | 600（ADS 对齐）|
| A1 | 政策密度指数 / 年度增长率 | `M_POLICY_TIMESERIES` | 密度 ⚠️ QPOL-02 |
| A1 | 有效政策占比 | `M_POLICY_VALIDITY_RATE` | 80.83% |
| A2 | 深圳综合得分 / 相对位次 | `M_POLICY_SUPPORT_STRENGTH` | composite ⚠️ QPOL-02 |
| A3 | 支持力度 | `M_POLICY_SUPPORT_STRENGTH` | 85（达标）|
| A3 | 产业适配性 | `M_POLICY_INDUSTRY_FIT` | 72（短板，QPOL-03 匹配规则待定）|
| A3 | 落地实效性 | `M_POLICY_IMPLEMENTATION_EFFECT` | 68（短板，❌ 无 ODS 来源/待采购）|

> 8 件套元数据来源：`mock/policy/policyMetricSeed.ts`（前端本地副本，对齐 `cfg_metric-POLICY-seed.yaml`）。`is_mock=true` → 🧪；`mapping_status='⚠️'` 或有 `pending_ref` → ⚠️。

---

## 4. Mock 数据（结构对齐 polan ADS）

- 文件：`src/app/mock/policy/policyData.ts`、`policyMetricSeed.ts`
- 量级对齐 `ALGO-POLICY-fullset.md` 实跑：总数 600 / 级别 56·137·266·114·27 / 时效 80.83% / 2022→2023 +67.24% / 全国 Top5 广东75·江苏55·北京55·浙江41·上海40 / 力度榜 广东115.0
- ADS 表对照：`ads_policy_level_dist` / `ads_policy_type_dist` / `ads_policy_timeseries` / `ads_policy_national_dist` / `ads_policy_metric_timeseries`
- Wave 1 起改读 Java 聚合 `/v1/policy/{indicators,metrics,analysis/intensity,graph,simulate}`，**前端结构不变**

---

## 5. Design.md §14 检查清单 + 验收 6 条对照

| 项 | 结论 | 说明 |
|---|---|---|
| 技术栈 React+Vite+Arco+ECharts | ✅ | 新代码仅引 `@arco-design/web-react` + icon；图表 ECharts；**无 antd** |
| 主色 #165DFF / 页面底色 | ✅ | DOM 用 `var(--sci-primary)` / `var(--sci-bg-page)`；ECharts 用等值 hex 常量 |
| 方向色 升红降绿 | ✅ | `trendUp #f53f3f` / `trendDown #00b42a` / `flat #86909c` |
| 政策要素色 | ✅ | `var(--sci-elem-policy)` 用于关键词 Tag / 国际级别 |
| token 不硬编码 | ✅ | DOM 全量 `var(--sci-*)`；ECharts 取色为 token 镜像 hex（canvas 限制，已注释说明）|
| 正文 14px / 控件 32px | ✅ | Arco 默认 + token fs/lh |
| D9 ⓘ/🧪/⚠️ | ✅ | 每统计数字旁 MetricSpecCard；Wave0 全 MockBadge；待定口径 PendingBadge |
| 结论先行 | ✅ | 每页 AnalysisShell 顶部 JudgmentStrip 一句话结论 |

---

## 6. 架构合规自检（00-team-constitution §2 十条）

1. 算法只在 Python ✅（前端纯展示，无算法）
2. 调用链不越层 ✅（仅 mock，无直连 nGQL/后端）
3. 图谱 NebulaGraph ✅（本层未用图谱）
4. 可观测性 ✅（统一 `track()` + `POLICY_TRACK`）
5. CI/CD ✅（待 push 触发 pipeline）
6. demo2 只读 merge ✅（独立仓 demo-ui-topic，未动 lumen）
7. 共享聚合核心 ✅（前端只调 Java/未来；当前 mock）
8. 数据策略 ADS 先行 + Mock ✅
9. 前端规范唯一来源 D8 ✅
10. 数据血缘 D9 ✅（8 件套 + 🧪/⚠️）

---

## 7. 构建结果

- `npm run build`：**✅ 成功**（vite v6.3.5，4790 modules，built in ~57s，exit 0）
- ESLint / TS：新文件 ReadLints **0 error**
- 注：仓未单独装 `typescript`，无独立 `tsc`；以 vite build 通过为类型/编译自检

---

## 8. 阻塞与风险

- ⚠️ **QPOL-02 力度/密度/综合得分口径未定**：现按团队临时默认值 Mock，UI 已挂 ⚠️ PendingBadge，待甲方确认（登记于客户决策清单跟踪表）
- ⚠️ **QPOL-03 政策-产业匹配规则待甲方**：A3 产业适配性短板成因已标注
- ❌ **落地实效性无 ODS 来源（待采购）**：A3 以 Mock 代理 + 文案明示「待采购」
- ⚠️ **QPOL-01 政策类型临时取 topic_type**：类型分布已注释
- 评审 gate：本次按派单为例外，**跳过人工评审**直接落地；上线前仍需 UX/UI/PM 人工评审
