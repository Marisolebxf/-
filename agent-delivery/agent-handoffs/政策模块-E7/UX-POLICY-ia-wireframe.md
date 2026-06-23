# Handoff · POLICY-PROTO-L02（UX：政策维度 IA + 用户流 + 低保真线框）

> 角色：ux-agent · Epic：E-POLICY-PROTOTYPE · 任务：POLICY-PROTO-L02
> 产物性质：结构化 Markdown + mermaid（不写代码、不画高保真）
> 范围：专题·政策分析（`/policy/*`，3 页）+ 门户·政策扶持（`/policy-portal/*`，6 页），共 9 页；**明确排除** DS-10/11/12 前端
> 本次例外：按派单约定跳过人工评审 gate，直接产出文档

---

## 1. 产物清单（demo-ui-topic 仓 `docs/ia/policy/`）

| 文件 | 内容 | DoD |
|------|------|-----|
| `README.md` | 索引 / 导览 / 阅读顺序 / 关键决策 / 待评审开放项 | ✅ |
| `POL-IA.md` | 两层站点图（mermaid）+ 9 页清单 + 路由 + 每页 §4.2 五段优先级 + IA 骨架 | ✅ |
| `POL-wireframe.md` | 9 页 ASCII 低保真 + 交互注解 + **6 列字段表（字段/控件类型/数据来源/交互/校验/metric_id）** + 每页 metric_id 清单 + 待评审 | ✅ |
| `POL-userflow.md` | 门户/分析主路径 + 7 条异常路径 + 角色矩阵（U1/U2/S1/S2）+ 21 埋点（携 user_level） | ✅ |
| `POL-gap-analysis.md` | 现有 3 页 vs bid 9 页覆盖矩阵 + 组件映射 + 缺口优先级 + 角色 Gap | ✅ |
| `POL-functional-design.md` | 逐页功能点 + 数据依赖总表 + polan 算法关联（L01/L02/L03）+ 口径映射 | ✅ |

---

## 2. 页面清单（9 页 · P-XX · 路由 · 优先级）

| # | 页面 | 路由 | P-XX | bid 章节 | 优先级 |
|---|------|------|------|---------|--------|
| A1 | 政策时序分析 | `/policy/overview` | P-70 | §1.1.1.2.4.2.6.1 | P0 |
| A2 | 区域政策对比 | `/policy/analysis` | P-72 | §1.1.1.2.4.2.6.2 | P0 |
| A3 | 深圳政策现状·三维框架 | `/policy/recommendation` | P-73 | §1.1.1.2.4.2.6.3 | P0 |
| B1 | 政策概况统计 | `/policy-portal/overview` | P-17 | §1.1.1.1.1.1.2.1 | P0 |
| B2 | 政策地图 | `/policy-portal/map` | P-18 | §1.1.1.1.1.1.2.2 | P1 |
| B3 | 政策产业覆盖 | `/policy-portal/industry-coverage` | P-19 | §1.1.1.1.1.1.2.3 | P1 |
| B4 | 政策力度排名 | `/policy-portal/intensity-rank` | P-20 | §1.1.1.1.1.1.2.4 | P1 |
| B5 | 最新政策动态 | `/policy-portal/latest` | P-21 | §1.1.1.1.1.1.2.5 | P0 |
| B6 | 深圳政策对比 | `/policy-portal/shenzhen` | P-22 | §1.1.1.1.1.1.2.6 | P0 |

> 专题 3 页：对齐现有原型 `src/app/pages/policy/{PolicyOverview,PolicyAnalysis,PolicyRecommendation}.tsx`（保留改造）。门户 6 页：全新路由（`pages/policy-portal/*` 尚未创建），由 ui-agent 评审后登记 `routes.tsx`。

---

## 3. §7 通用组件清单（本次 9 页用到，给 ui-agent）

PageShell · TopicSidebar · ContextBar · ModuleHeader · MetricCard · DataCard · SearchableCascadeFilter · FilterBar · StatusTag · Tag · DetailDrawer · DataTable · ChartPanel · MapPanel · GraphCanvas · Timeline · EvidenceList · SectionPanel · PrimaryWorkbenchTabs · SecondaryAnalysisTabs · MetricSpecCard(ⓘ) · MockBadge(🧪)（共 22 个）。

---

## 4. Arco 控件映射建议（D8/D9 → @arco-design/web-react）

| 抽象组件 | Arco / 图引擎控件 | 备注 |
|---------|------------------|------|
| PageShell | `Layout` + 自封装容器 | 底色 #D8E7FC |
| TopicSidebar | `Menu`（可折叠） | 宽 200px |
| ContextBar | 自封装 + `Select` / `Cascader` / `DatePicker` / `Button` | 控件高 32px |
| MetricCard | `Card` + `Statistic` + 自封装 ⓘ/🧪/⚠️ 角标 | 升降方向色 |
| DataCard | `Card` / `List` | 政策卡片 |
| SearchableCascadeFilter | `Cascader` + `Select(mode=multiple)` + `Input.Search` | 带搜索/重置/确认/已选摘要 |
| FilterBar | `Form` + `Grid` + 上述控件 | label 在上 14px |
| StatusTag / Tag | `Tag` | 浅底深字同族边框（§7.4） |
| DetailDrawer | `Drawer`（720px）+ 整页同构 | 政策详情画像 |
| DataTable | `Table`（排序/分页/导出） | — |
| ChartPanel | `Card` + **ECharts**（echarts-for-react） | ⚠️ 禁 recharts（D8 栈） |
| MapPanel | **Leaflet** | 三级行政区划下钻 |
| GraphCanvas | **AntV G6** | 关系走 NebulaGraph |
| Timeline | `Timeline` / ECharts 自定义 | A1/B5/B6 |
| EvidenceList | `List` / `Timeline` | 结论/策略卡 |
| SectionPanel | `Card` / `Collapse` | 去营销渐变 |
| PrimaryWorkbenchTabs | `Tabs`（下划线激活，去胶囊背景，§7.3） | 主视图切换保留筛选 |
| SecondaryAnalysisTabs | `Tabs`（轻量面片） | 右侧研判内切视图 |
| MetricSpecCard(ⓘ) | `Popover` / `Trigger` | D9 8 件套展示 |
| MockBadge(🧪) | `Badge` / `Tag` | Wave 0 Mock 标识 |

> 主色固定 `#165DFF`，选中态 `#165DFF`/`#E8F3FF`，圆角 2-4px；新页依赖必须含 `@arco-design/web-react`（D8 §14 验收）。

---

## 5. 架构合规自检（对照公约 §2 十条）

| # | 铁律 | 合规 | 说明 |
|---|------|------|------|
| 1 | 算法只在 Python | ✅ | polan 政策算法全集在 Python（L01/L02/L03），UX 文档明确前端不写算法 |
| 2 | 调用链 前端→Java→Python | ✅ | 9 页只调 Java REST 消费 ADS 聚合结果，不越层 |
| 3 | 图谱用 NebulaGraph | ✅ | B3/A2/A3 关联走 `gkx_policy`，前端仅 G6 渲染 |
| 4 | 可观测性必加 | ✅ | userflow §4 给 21 埋点（携 user_level），移交前端落 `observability.ts` |
| 5 | CI/CD push→绿→dev | ⏸ | 文档阶段，前端开工后由 frontend-agent 走流水线 |
| 6 | demo2 只读 merge | ✅ | 本产物为 demo-ui-topic docs，不涉及 demo2→lumen 合并 |
| 7 | 共享聚合核心（方案 A） | ✅ | 专题+门户共享 polan + Java 聚合核心，Java 只读 ADS |
| 8 | ADS 先行 + Mock | ✅ | Wave 0 全 Mock + 🧪，字段表 source_tables 预留真实 ODS/DWD |
| 9 | 前端规范 D8 | ✅ | 新页 Arco + ECharts + G6 + Leaflet（#165DFF）；handoff 含 Arco 映射 + §14 检查清单对照 |
| 10 | 数据血缘 D9 | ✅ | 字段表 metric_id 列引用 cfg_metric-POLICY-seed.yaml（M_POLICY_* 19 条）；统计数字旁 ⓘ/🧪/⚠️ |

> 全部 ✅/⏸，无 ❌。

### Design.md §14 检查清单对照（移交 ui-agent 验收用）
- ✅ 浅蓝白工作台（底色 #D8E7FC），非深色大屏。
- ✅ 保留 Header(64px) / Sidebar(200px) / 主内容 / 中央主视图 / 右侧研判。
- ✅ 选中态统一 #165DFF / #E8F3FF；控件高 32px / 小按钮 24px。
- ✅ 中央主视图面积 > 右侧研判面板；右侧含 SecondaryAnalysisTabs。
- ✅ 要求 loading/empty/disabled/error 状态（userflow 异常 C/E/F 覆盖）。
- ⚠️ 提醒 ui-agent：现有 3 页用 recharts，lumen 复刻须迁 ECharts；新依赖须含 @arco-design/web-react。

---

## 6. 阻塞与风险

- **无阻断项**。本任务按例外约定跳过人工签收/评审 gate，直接产出文档。
- **风险 R1（口径未定）**：QPOL-01/02/03 + 🟡-05/07 共 5 类业务口径待甲方确认，UX 已在 wireframe/字段表以临时默认值标 ⚠️ 推进（力度权重 补贴40%+税收25%+数量20%+周期15%、三维等权、匹配阈值 0.6 等）。上线前须升 🟢 否则 A2/A3/B1/B4 统计数字返工。**请 PM 推动甲方确认并更新客户决策清单跟踪表。**
- **风险 R2（数据缺口）**：A3 落地实效性/政策效果的执行监测、宏观经济、社会发展数据 ❌ **无 ODS 来源，待采购**；`dwd.industry_chain` 跨域产业链维表、NebulaGraph `gkx_policy` 需 data/algorithm-agent 确认就位。Wave 0 以 Mock 🧪 填充。
- **风险 R3（算法全集 vs 前端弱消费）**：文本解析/摘要、匹配推送（P-38）、效果推演仿真（P-58~P-62）算法全集实现但本次 9 页无独立页/弱消费，需 data/algorithm-agent 确保其 metric/model 仍登记 cfg_metric/cfg_model_registry，供 Wave1 血缘核验与 Wave2/DS-10/11/12 复用。
- **风险 R4（范围混淆）**：DS-10/11/12（展示系统）与 `/policy-portal` 同含"政策地图/全景/对比"近义词，IA/gap 已反复强调本次只做 9 页前端，ui/frontend handoff 须延续，避免误扩范围触发 ±10% 铁律。
- **风险 R5（技术栈偏离）**：现有政策 3 页为 Tailwind+recharts+自绘，与 D8 权威栈（Arco+ECharts+G6+Leaflet）系统性偏离；topic 原型沙箱可保留，门户 6 新页建议直接按 D8 权威栈起步。

### UX 新增登记开放项（请 coordinator/PM 同步客户决策清单跟踪表）
- **K-POL01**：用户级别划分与权限矩阵（U1/U2/S1/S2 判定与提权规则）。
- **K-POL02**：公众可导出范围与配额、收藏/分享登录态、画像脱敏字段范围。
- **🆕 cfg_metric 补登建议**（给 data-agent）：B2「区域政策密度」、B5「近 N 天新发数（滚动窗口）」建议补登独立 metric_id（当前以 NATIONAL_DIST/TIMESERIES 派生）。

---

## 7. 后续依赖与接力

- **ui-agent**：据 POL-wireframe 区块 + Arco 映射做高保真/页面实现，先 P0 6 页（A1/A2/A3/B1/B5/B6）。
- **algorithm-agent**：实现 cfg_metric 标 🔧/pending_algorithm 的 12 条 formula（力度/效果/焦点/短板/机遇/布局/三维/时序/覆盖/有效/连续/关联）。
- **data-agent**：确认 `dwd.industry_chain`、`dim_region`(深圳区县)、NebulaGraph `gkx_policy` 就位；补登 🆕 两个派生 metric。
- **PM**：推动甲方确认 QPOL-01~03 / 🟡-05/07 / K-POL01/02，更新客户决策清单跟踪表。
- **frontend-agent**：lumen 复刻时 recharts→ECharts、自绘图→G6、地图→Leaflet，落 observability.ts 21 埋点。

> 本 handoff 即 POLICY-PROTO-L02 的交付证据。维护：ux-agent 起草，业务口径变更须 PM + 甲方确认。
