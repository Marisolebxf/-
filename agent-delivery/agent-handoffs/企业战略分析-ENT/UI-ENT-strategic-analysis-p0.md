# UI Handoff：企业分析 P0 拆页 + 竞争力去重（ui-agent）

- 时间：2026-06-18
- 角色：ui-agent（UI/前端实现臂）
- 仓库：`topic_demo`（原型沙箱仓）
- 分支：`main`
- Commit：`bc16e5a`　message：`[sandbox] ui-agent：企业分析 P0 拆页+竞争力去重 [agent:ui-agent]`
- 推送状态：**未 push**（按派单纪律，topic_demo push 由人工评审后触发）
- 实现依据：ux-agent 产物 `topic_demo/docs/ia/enterprise/`（ENT-IA / ENT-wireframe / ENT-gap-analysis）

---

## 1. 改动文件清单（5 个）

| 文件 | 动作 | 说明 |
|------|------|------|
| `src/app/pages/enterprise/EnterpriseTypeDistribution.tsx` | 新增 | P0-1 重点企业类型分析（路由 `/enterprise/type-distribution`，导出 `EnterpriseTypeDistribution`） |
| `src/app/pages/enterprise/EnterpriseDomainDistribution.tsx` | 新增 | P0-2 重点企业领域分布分析（路由 `/enterprise/domain-distribution`，导出 `EnterpriseDomainDistribution`） |
| `src/app/pages/enterprise/EnterpriseStatusAnalysis.tsx` | 改 | P0-3 移除「综合竞争力分析」Tab 及其全部状态/数据/自定义指标弹窗，仅保留「现状分析」（.3.5），改为单视图无 Tab |
| `src/app/components/Layout.tsx` | 改 | P0-3 `enterpriseItems` 新增「企业竞争力分析」→ `/enterprise/competitiveness`；同时挂入两个新页（类型/领域）做侧边栏入口 |
| `src/app/routes.tsx` | 改 | 企业路由块新增 `type-distribution`、`domain-distribution` 两条 + import 两个新页面组件 |

---

## 2. 3 个 P0 完成情况

### P0-1 重点企业类型分析（bid §1.1.1.2.4.2.3.1 / E-21）✅
- 从 `EnterpriseOverview`「重点企业概况」Tab 的「企业类型分布分析」子区抽取/改造为独立页。
- 按 wireframe P1 补齐区块：ContextBar（产业级联 + 时间窗 + 导出/刷新/保存口径）、SearchableCascadeFilter（产业级联 + 企业类型多选「外企/高企/小微/上市」+ 搜索/重置/确认/已选摘要）、MapPanel（沿用现有 `imports/image.png` 地图占位 + 图例 + 数量/占比/集聚指数 二级研判 Tab）、ChartPanel（企业类型结构 区域×类型 堆叠柱）、DataTable（区域企业清单：区域/数量/各类型占比/密度/集聚指数 + 导出）。
- KPI ×4（匹配企业总数/外企占比/高企占比/上市占比）旁带 ⓘ（title=metric_id+口径）+ 🧪 MockBadge；口径未定项带 ⚠️ 角标（K-O2/K-O4）。

### P0-2 重点企业领域分布分析（bid §1.1.1.2.4.2.3.2 / E-22）✅
- 从 Overview「领域分布分析」子区抽取为独立页。
- 按 wireframe P2 布局：ContextBar、FilterBar（企业搜索多选 + 领域层级 + 时间窗）、MetricCard ×3（覆盖领域数/多元化指数/核心领域深度）、ChartPanel（企业×领域覆盖深度对比柱）、DataTable（企业领域覆盖明细）、DetailDrawer（企业领域映射证据：业务/产品/技术标签）。
- KPI 旁带 ⓘ + 🧪 + ⚠️（K-O5 覆盖广度/深度口径待算法 lead+甲方确认）；含 empty 状态（未选企业时）。

### P0-3 竞争力去重 ✅
- `Layout.tsx` `enterpriseItems` 新增「企业竞争力分析」→ `/enterprise/competitiveness`（图标 Trophy），使既有 `CompetitivenessAnalysis.tsx`（.3.10）成为竞争力唯一侧边栏入口。
- `EnterpriseStatusAnalysis.tsx` 删除「综合竞争力分析」Tab：移除 `activeTab`/Tab 导航/竞争力数据常量/指标配置状态/自定义指标弹窗/`IndicatorItem` 依赖，页面只保留「现状分析」内容并整体重排为单视图。现状分析渲染未受影响（区域对比/产业链环节/完整度/趋势/高效经营占比等图表全部保留）。

---

## 3. 与 wireframe / gap 的对照

| gap 项 | 状态 | 实现位置 |
|--------|------|---------|
| P0-1 .3.1 拆独立页 | ✅ | EnterpriseTypeDistribution.tsx，对齐 wireframe P1 区块/字段表 |
| P0-2 .3.2 拆独立页 | ✅ | EnterpriseDomainDistribution.tsx，对齐 wireframe P2 区块/字段表 |
| P0-3 竞争力去重 | ✅ | Layout 挂载 competitiveness + StatusAnalysis 移除竞争力 Tab |
| metric_id 占位 | ✅ | 各 KPI 用 ⓘ tooltip 暴露 metric_id + 口径（如 `M_ENT_TYPE_MATCH_COUNT` 等） |

---

## 4. 遗留项 / 已知限制

1. **MetricSpecCard / DataLineageDrawer / MockBadge 完整组件**：本次仅做轻量占位（ⓘ 用原生 `title` tooltip、🧪 用小徽标、⚠️ 用 icon+title）。D9 规定的完整 MetricSpecCard 弹卡/血缘抽屉留待 frontend-agent 复刻到 lumen 时按 `data-lineage-policy.md §5` 实现。
2. **技术栈仍为 topic_demo 原样**（React + Tailwind + recharts + lucide-react），未迁 Arco/ECharts/Leaflet/G6——按派单硬约束（D8 对已有原型仓兼容保留），Arco 迁移属 lumen 复刻范畴，不在本任务。
3. **GIS 三级地理下钻**（国/省/市）沿用现有静态地图占位（`imports/image.png`），Leaflet 行政区划真实下钻待 lumen 阶段（wireframe P1 已标 ⚠️ 需人工评审；K-O4 区划精度待甲方）。
4. **业务口径 ⚠️ 项**：企业类型判定规则（K-O2）、区划精度（K-O4）、领域覆盖广度/深度口径（K-O5）均已在 UI 上保留 ⚠️ 角标 + tooltip，未替甲方拍板；对应项已登记于 `客户决策清单跟踪表.md`（由 ux-agent 登记，本次校对一致）。
5. **Overview 整页未重构**（P1-1 不在本任务范围）：Overview 仍保留「企业类型分布分析/领域分布分析」两个子区（未删除原子区，避免破坏 Overview 整页）；新独立页与 Overview 子区暂并存，待 P1-1 重构 Overview 为纯战略概述时再清理。
6. **Mock 字段名**：新页 Mock 以 ODS/DWD 字段口径注释占位（如 `dwd.enterprise.headquarters_city`），具体 JSON 数据文件未落地（沿用页面内联 Mock，与现有 enterprise 页面一致）。

---

## 5. §2 架构铁律自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ N/A（前端无算法，派生指标标 🔧 待 algorithm-agent） |
| 2 | 调用链 前端→Java→Python | ✅ N/A（原型仅 Mock，未接 API） |
| 3 | 图谱 NebulaGraph 禁 Neo4j | ✅ N/A（本任务无图谱页） |
| 4 | 可观测性必加 | 🟡 原型沙箱，关键交互用 `console.log` 埋点占位（查询/导出/下钻/确认）；`observability.ts` 待 lumen 复刻 |
| 5 | CI/CD push→绿→rollout | 🟡 设计/原型类；本次未 push，待人工评审 |
| 6 | demo2 只读 merge 铁律 | ✅ 仅改 topic_demo 原型仓，未 merge 进 lumen |
| 7 | 共享聚合核心（方案A） | ✅ N/A（原型层） |
| 8 | 数据策略 ADS 先行 + Mock | ✅ Mock 数据驱动，字段按 ODS/DWD 口径注释 |
| 9 | 前端规范唯一来源（D8） | 🟡 **按派单豁免**：topic_demo 原型仓保持原栈（Tailwind+recharts），不迁 Arco；Arco 规范在 lumen 复刻时执行 |
| 10 | 数据血缘铁律（D9） | 🟡 轻量占位（ⓘ/🧪/⚠️ 均在位），完整 MetricSpecCard 留 lumen |

> 说明：第 9/10 条的 🟡 系派单明确豁免（topic_demo 原型兼容保留），非违规；完整 Arco + D9 三件套属 frontend-agent 复刻 lumen 范围。

---

## 6. 成本回填（budget-estimate.md 口径）

- `actual_tokens`：≈ 175k（含 5 份设计文档 + 大文件 Overview/StatusAnalysis 研读 + 2 新页生成 + StatusAnalysis 重写）
- `model_used`：Claude Opus 4.8
- `actual_cost`：≈ $4.0（估）
- `cost_warn`：否（< $10 阈值）

---

## 7. 验收建议（交 qa / UI-UE 评审）

- `npm run dev` 后访问 `/enterprise/type-distribution`、`/enterprise/domain-distribution`、`/enterprise/competitiveness` 三条路由可达，侧边栏「企业分析」分组新增 3 项。
- 确认 `/enterprise/status-analysis` 仅剩「现状分析」单视图，无「综合竞争力分析」Tab，且现状图表全部正常渲染。
- 下一步：UI/UE 评审 → 人工 push topic_demo（触发 https://skxrules.unicomcn.tech:30999/ 自动部署）→ 后续 frontend-agent 复刻到 lumen（迁 Arco/ECharts/Leaflet + 完整 D9 三件套）。
