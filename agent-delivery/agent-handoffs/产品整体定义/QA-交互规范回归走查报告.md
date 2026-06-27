# QA · 交互规范回归走查报告

- **任务**：E-PROD-UXUE-ALIGN-L01（已上线/已完成前端页面 × 《UX-UE 通用交互组件规范》一次性回归走查）
- **性质**：只读审计 —— 仅读前端代码 + 产出本报告，**未改任何业务代码**（整改另开 task）
- **走查人**：qa-agent
- **走查日期**：2026-06-23（**第 2 轮复核**，依赖 E-PROD-UXUE-COMP-L02 视觉规范已产出）
- **cicd**：skip_design_only（无代码改动，无需流水线）

## 0. 走查基准与说明

| 基准 | 状态 | 说明 |
|---|---|---|
| `产品整体定义/UX-UE 通用交互组件规范.md` | ✅ 存在，以它为准 | 主基准；重点用 §3.4 验收用例、§19 走查清单、§15 状态矩阵、§16 键盘总则、§17 无障碍 |
| `产品整体定义/UI-通用交互组件视觉规范.md` | ✅ 存在（v1.0，E-PROD-UXUE-COMP-L02） | **第 2 轮起纳入**；视觉 token / 图例右下角 / 控件高度等对照；交互语义仍以 UX 规范为准（D10 分层） |
| `agent-delivery/Design.md` | ✅ 存在 | 视觉 token 真源（主色 #165DFF、控件 32px 等） |

> 走查方法：先用 glob/grep/dir 定位实际路由与 pages 目录（不假设路径），再逐页对照六大维度（状态覆盖 / 键盘可达 / 上下文保留 / Arco 一致性 / 焦点恢复 / 非颜色依赖）抽检。本报告对**代表性页面 + 跨页复用内核**做核对，同类页（如 entan ≈ policy、其余分析页 ≈ EnterpriseOverview）按内核结论归纳。

### 0.1 与第 1 轮（2026-06-23 初检）差异

| 项 | 第 1 轮 | 第 2 轮 |
|---|---|---|
| UI 视觉规范 | ❌ 未找到，Design.md 兜底 | ✅ 已产出，纳入基准 |
| 业务代码整改 | — | **无**（G-01~G-19 代码证据与初检一致，差距未收敛） |
| 建议整改 task | §4 口头建议 | **已登记 task-registry**（FIX-A11Y-* / FIX-EVENTMAP-* / DECIDE-SYSTEMTEST-STACK / POLISH-UXUE-P2） |
| 结论 | P0=0，P1=5 类、P2=13 类 | **不变**（复核确认） |

## 1. 走查范围定位结果

| 范围项 | 计划目标 | 实际定位 | 栈 / UI 库 | 定位状态 |
|---|---|---|---|---|
| POLICY-PROTO（专题前端） | demo-ui-topic pages/policy、policy-portal | `src/app/pages/policy/*`、`pages/policy-portal/*` + `policyShared.tsx` | React + **Arco** + ECharts | ✅ |
| POLICY-PROTO（算法台） | demo-ui-system-test /policy、/entan | `src/views/policy/index.vue`+components、`src/views/entan/index.vue`+components | Vue3 + **Element Plus**（PIGX） | ✅ |
| E-INNOV EventMap | lumen-ui-science-pc EventMap | `src/views/innov/index.vue`、`components/EventMap.vue`、`CityIndex.vue` | Vue3 + **Arco Vue** + Leaflet | ✅ |
| E-PERM-L03a | demo-ui-topic 企业维度 + 权限内核 | `pages/enterprise/*`、`pages/development/*`、`perms/PermGate.tsx`、`perms/LockedButton.tsx`、`components/Layout.tsx` | React + **Arco** | ✅ |
| E-PLATFORM-P0-L07 首页 | lumen-pc + demo-ui-topic 首页 | lumen：`views/HomeView.vue`；demo-ui-topic：`/` → 重定向 `/enterprise/overview`（`routes.tsx:125`）；门户概况 `development/DevelopmentOverview.tsx` | Arco | ⚠️ 部分（见下） |

**需 coordinator 补指针 / 澄清的点**（与初检相同，仍未裁决）：

1. **demo-ui-topic 无独立"平台首页占位"**：路由 `/` 直接 `Navigate → /enterprise/overview`。`pages/Overview.tsx`（纯 Tailwind + lucide-react、硬编码数字、**完全不用 Arco**）**未挂任何路由**，属遗留/孤儿组件 → 本报告不计为线上页，建议清理。若 E-PLATFORM-P0-L07 指的是某个真实占位首页，请补指针。
2. **demo-ui-system-test 整仓基于 Element Plus（PIGX 平台）**，非 Arco；定位应为"算法效果展示/内测台"而非甲方 Arco 展示前端 —— 是否纳入 Arco 一致性收敛范围需 PM/架构师确认（见 G-09，task **DECIDE-SYSTEMTEST-STACK**）。

## 2. 总体结论

- **基本达标**（栈合规、状态/键盘/上下文主体到位，仅次要项）：
  - lumen-ui-science-pc **EventMap.vue / innov / HomeView**（Arco Vue，状态覆盖、等价表格替代、loading/empty 较完整）
  - demo-ui-topic **policy / policy-portal / enterprise** 系列分析页（Arco 栈、PermGate 锁态、metricId ⓘ、Mock/Pending 角标、Drawer 分区结构良好）
- **需优先整改**（跨页复用内核的无障碍缺口，一处修则全局收益）：
  - **`MetricSpecCard`(ⓘ) / `HelpPopover`(?)** —— 键盘 / 触屏不可达（hover-only + 不可聚焦 `span`）
  - **`LockedButton`（PermGate 降级态）** —— 键盘 / 读屏不可感知锁态原因
- **栈级偏离待裁决**：demo-ui-system-test 全量 Element Plus（非 Arco）
- **视觉规范新增对照**：EventMap 基础图例位于地图下方常规流（`EventMap.vue:53-57`），与 UI 视觉规范 § 地图图例「容器右下角浮层」及 UX §9.2 不一致（G-11~G-12，P2）

**一句话结论**：四个范围内 Arco 前端页面交互骨架基本达标，无阻断级缺陷；**第 2 轮复核确认差距未收敛**，最突出的仍是 **ⓘ/? 说明气泡与权限锁态按钮两个高复用内核键盘/读屏不可达**，应优先按内核统一整改。

- **P0（阻断）数量：0**
- P1（重要）：5 类；P2（次要）：13 类（详见 §3、§4）

## 3. 差距清单（页面 × 检查项 × 现状 × 严重度 × 整改建议）

> 代码证据经第 2 轮 grep/读文件复核；与初检一致处标注「复核 ✅」。

### 3.1 跨页复用内核（影响面最大，优先级最高）

| 编号 | 页面/组件 | 检查项 | 现状 | 严重度 | 整改建议 |
|---|---|---|---|---|---|
| G-01 | `common/MetricSpecCard.tsx`（ⓘ，全 policy/enterprise 统计卡复用） | 键盘可达 / 聚焦状态（§16/§17/§3.4） | `Popover trigger="hover"`（L83），触发元素为 `<span>`（L88-94，无 `tabIndex`、非按钮）→ 键盘与触屏用户**无法打开**指标"8 件套"说明卡 | **P1** | 触发元素改为可聚焦（`<button>` 或 `tabIndex=0`+`role="button"`）；Popover `trigger={['hover','click','focus']}`；保留现有 `aria-label` |
| G-01b | `common/HelpPopover.tsx`（?，policy 图表口径说明） | 同 G-01 | 同构：`trigger="hover"`（L66）+ 不可聚焦 `<span>`（L67-73） | **P1** | 与 G-01 同一套改法；可与 FIX-A11Y-INFO-POPOVER 一并修 |
| G-02 | `perms/LockedButton.tsx`（PermGate 降级态） | 键盘可达 + 非颜色依赖 + 焦点（§14/§17） | 锁态用 `<span onClickCapture>`（L50-64），**不可聚焦**；`Tooltip` 仅 hover；`IconLock` 无可访问名；无 `aria-disabled` | **P1** | 锁态容器可聚焦并补 `aria-disabled`/`aria-describedby`；Tooltip 支持 focus 触发；IconLock 补 `aria-label="未授权"` |
| G-03 | `components/Layout.tsx` 左侧导航 | 当前项 current 状态 / 菜单键盘（§4.1） | 当前项仅 `.active` class（L193），**无 `aria-current="page"`**；菜单组有 `aria-expanded`（L287 ✅）；**无方向键导航** | **P2** | 当前项加 `aria-current="page"`；按 §4.1 补方向键（Tab 等价路径已在） |
| G-04 | `enterprise/analysisShared.tsx` ContextBar | 筛选一致/联动可解释（§19/§3.4） | Wave0 图表/指标为静态 mock，**筛选变化不联动任何数据**（无 loading/无结果反馈）→ 筛选呈"装饰态" | **P1** | Wave0 至少给筛选变化可见反馈（toast/skeleton）；Wave1 接真数据时打通联动 |
| G-05 | `analysisShared.tsx` AnalysisShell | 上下文保留（§3.4） | 每页各自维护内部 ctx，跨页仅靠 URL `enterprise_code` 透传；离开再回筛选回默认值 | **P2** | demo 阶段可接受；正式期建议全局筛选上提到路由/状态层 |

### 3.2 POLICY-PROTO · demo-ui-topic（Arco）

| 编号 | 页面 | 检查项 | 现状 | 严重度 | 整改建议 |
|---|---|---|---|---|---|
| G-06 | `policy-portal/PolicyPortalOverview.tsx` | 一级 Tab 联动可解释 | 级别 Tab 切换仅更新 4 个 MetricCard（L136-144）；环形/条形/时序图 `useMemo([])` **不随 tab 变化**（L38-104） | **P2** | 图表/表格数据按 `tab` 派生，或标题注明"分布图为全口径" |
| G-07 | `policy/policyShared.tsx` PolicyDetailDrawer | 抽屉 footer 固定（§12.3） | `footer={null}`（L185）；收藏/分享/原文操作置于 body 顶部（L197-216） | **P2** | 主操作迁入固定 footer，body 仅承载内容 |
| G-08 | `policy-portal/PolicyPortalOverview.tsx` 明细表 | 表格行交互/状态（§11.2/§11.3） | `onRow={() => ({ onClick: () => {} })}`（L166）空实现；无 loading/empty/error 接线 | **P2** | 整行 hover 提示可点击或移除空 onRow；Wave1 补状态态 |
| G-08b | `policy/PolicyOverview.tsx` 时间轴 | 非颜色依赖/可访问名（§17） | 节点为原生 `<button>`（L152，键盘可达 ✅），但无 `aria-label`；等级 Tag 有颜色+文字（非颜色 ✅） | **P2** | 时间轴节点补 `aria-label`（政策名+级别+日期） |

### 3.3 POLICY-PROTO · demo-ui-system-test（Element Plus / PIGX）

| 编号 | 页面 | 检查项 | 现状 | 严重度 | 整改建议 |
|---|---|---|---|---|---|
| G-09 | `views/policy/index.vue`、`views/entan/index.vue` | Arco 一致性（D8/§19） | 全量 **Element Plus**（`el-tabs`/`el-button`/`ElMessage`/`ElMessageBox`） | **P1（栈级，需裁决）** | task **DECIDE-SYSTEMTEST-STACK**：豁免登记或迁 Arco；**不建议 QA 单方定级** |
| G-10 | 同上 | 上下文保留（§3.4） | 灌数完成 `window.location.reload()`（policy/index.vue:109）重置全部上下文 | **P2** | admin 灌数动作可接受；如需保留可改局部刷新 |

> 正向：灌数流程 `ElMessageBox` 二次确认 + `loading` + 轮询 + 成功/失败 `Message`，异步任务反馈（§13/§15）完善。

### 3.4 E-INNOV · lumen-ui-science-pc EventMap（Arco Vue + Leaflet）

| 编号 | 页面 | 检查项 | 现状 | 严重度 | 整改建议 |
|---|---|---|---|---|---|
| G-11 | `EventMap.vue` | 热力强度分级图例（§9.2 / UI 规范地图章） | 热力开启后**无热力强度分级图例**（仅 L53-57 基础类型图例） | **P2** | 开启热力时叠加强度分级图例（低→高） |
| G-12 | `EventMap.vue` | 图例位置 / 全屏（§9.2 / UI 规范） | 图例在地图下方常规流（`.legend { margin-top: 6px }`），非容器右下角浮层 | **P2** | 图例改为容器内右下角浮层；全屏态保留图例 |
| G-13 | `EventMap.vue` | 热力无数据态（§9.4） | `heatPts` 为空时静默空白（L241-247），无提示 | **P2** | 空热力数据时保留视野与基础图例并提示 |
| G-14 | `EventMap.vue` | 详情抽屉错误态/焦点（§3.4/§15.2） | 详情失败 → `drawer.value = false`（L306）直接关闭 | **P2** | 抽屉保持打开，body 展示错误+重试 |
| G-15 | `EventMap.vue` | 非颜色依赖（§2.2） | 地图 `circleMarker` 类型仅以颜色编码；tooltip/列表/Tag 有文字 → 部分达标 | **P2** | 可接受；严格模式可对类型加形状标记 |

> 正向：右侧等价事件表格（§9.5 ✅）、`a-spin`/`a-empty`/`a-pagination`、moveend 300ms 防抖、热力开关仅刷新热力层（§9.3 ✅）。

### 3.5 E-PERM-L03a · demo-ui-topic 企业维度（Arco）

| 编号 | 页面 | 检查项 | 现状 | 严重度 | 整改建议 |
|---|---|---|---|---|---|
| G-16 | `enterprise/EnterpriseOverview.tsx` TopN 列表 | 非颜色依赖/选中态 | 命中行仅以 `var(--sci-primary-soft)` 背景（L180）区分，无文字/图标标记 | **P2** | 当前行补"当前"标签或左侧主色条+可访问名 |
| G-17 | `enterprise/EnterpriseOverview.tsx` 全国分布 | 联动可解释（§8.2） | ECharts 柱不可点击，下钻靠按钮组（键盘等价 ✅） | **P2** | 可接受；可选补 `onChartPointClick` |
| — | 权限锁态 | 见 G-02 | 继承跨切面 P1 | P1 | 同 G-02 |

> 正向：PermGate 非阻断锁态（§14 ✅）、省份下钻按钮键盘可达、metricId+PendingBadge（D9 ✅）。

### 3.6 E-PLATFORM-P0-L07 · 首页占位

| 编号 | 页面 | 检查项 | 现状 | 严重度 | 整改建议 |
|---|---|---|---|---|---|
| G-18 | lumen `views/HomeView.vue` | 数据血缘/状态（D9/§15.2） | `a-statistic` 业务指标无 ⓘ/8 件套；无 empty/error 态 | **P2** | 转正式首页时补 metricId ⓘ 与空/错态 |
| G-19 | demo-ui-topic `pages/Overview.tsx` | Arco 一致性 / 路由 | 纯 Tailwind + lucide-react、**未挂路由**（孤儿组件） | **P2（清理项）** | 确认无引用后删除；线上首页 = `/enterprise/overview`（Arco ✅） |

> 正向：lumen HomeView Arco 栈、observability 按钮有 `loading`、`a-alert` 反馈完善。

## 4. 整改 task 清单（已登记 task-registry）

**P0（阻断级）= 0 项**。

以下 **P1 内核整改** 与 **P2 批量 polish** 已在 `task-registry.yaml` 登记（depends_on: E-PROD-UXUE-ALIGN-L01）：

| task id | 范围 | agent | 关联差距 | 预估 |
|---|---|---|---|---|
| **FIX-A11Y-INFO-POPOVER** | `demo-ui-topic/.../MetricSpecCard.tsx`、`HelpPopover.tsx` | frontend-agent | G-01、G-01b | S |
| **FIX-A11Y-PERM-LOCK** | `demo-ui-topic/.../LockedButton.tsx`；连带 `Layout.tsx` `aria-current` | frontend-agent | G-02、G-03 | S/M |
| **FIX-EVENTMAP-HEAT-LEGEND** | `lumen-ui-science-pc/.../EventMap.vue` | frontend-agent | G-11~G-14 | M |
| **DECIDE-SYSTEMTEST-STACK** | demo-ui-system-test Arco 豁免/收敛决策 | architect-agent + PM | G-09 | 决策 |
| **POLISH-UXUE-P2** | G-06~G-08b、G-16~G-19 等 P2 批量 | frontend-agent | 见 §3 P2 项 | M |

## 5. §19 设计走查清单逐项对照（汇总）

| §19 检查项 | 总体判定 | 主要缺口 |
|---|---|---|
| 组件归类 | ✅ | policyShared/analysisShared 分层清晰 |
| 状态完整性 | ⚠️ | mock 页多未接线 loading/empty/error（G-08/G-13/G-14/G-18） |
| 键盘可达 | ❌→需修 | ⓘ/? 与锁态按钮不可达（G-01/G-01b/G-02）；导航无方向键（G-03） |
| 筛选一致 | ⚠️ | ContextBar 未联动（G-04）；Portal Tab 不联动图表（G-06） |
| 联动可解释 | ✅/⚠️ | 下钻多有按钮等价路径；部分图形点击联动缺（G-06/G-17） |
| 权限明确 | ✅/⚠️ | PermGate 非阻断锁态到位；锁态原因 AT 不可达（G-02） |
| 导出可信 | ⚠️ | demo 导出为 Message.info 占位 |
| 异常可恢复 | ⚠️ | EventMap 详情失败直接关闭（G-14） |
| 空态可行动 | ⚠️ | 热力空态缺提示（G-13） |
| 抽屉宽度合理 | ✅ | policy 720 / EventMap 44% 合理 |
| 遮罩策略明确 | ✅ | 非模态 Drawer 用于详情 |
| 无障碍达标 | ❌→需修 | 焦点/可访问名缺口集中在 G-01/G-01b/G-02/G-03 |
| Arco 一致性 | ⚠️ | Arco 页达标；system-test Element Plus（G-09）；Overview.tsx 孤儿（G-19） |

## 6. DoD 自检

1. **逐页按 §3.4 + §19 抽检完成** —— ✅（第 2 轮全量复核代表页 + 内核组件；UI 视觉规范纳入对照）
2. **产出差距清单表** —— ✅（§3，G-01~G-19 + G-01b）
3. **P0 项单列整改 task + P1 内核 task 登记** —— ✅（§4 → task-registry）
4. **总体结论** —— ✅（§2；与初检一致，差距未收敛）

---
*本报告为只读审计产物（第 2 轮复核）。未进行任何 git commit / push，未修改任何业务代码。*
