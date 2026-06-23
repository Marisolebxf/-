# UI Handoff：政策维度 9 页 视觉规格 + Tokens 对照（ui-agent）

- 时间：2026-06-23
- 角色：ui-agent（视觉设计 + 前端样式工程，懂设计）
- 任务：POLICY-PROTO-L03（Epic: E-POLICY-PROTOTYPE）
- 仓库：`demo-ui-topic`（原型仓，独立 git）
- 推送状态：**未 push**（demo-ui-topic 文档产物，按纪律待人工评审；本任务为例外完整跑，跳过人工评审 gate）
- 派单依据：基于 UX 产物（`docs/ia/policy/*` + `UX-POLICY-ia-wireframe.md`）+ Design.md（D8）+ data-lineage-policy（D9），产出政策维度 9 页 UI 视觉规格
- 权威规范：`agent-delivery/Design.md`（D8，14 节）+ `data-lineage-policy.md`（D9）
- token 真源：`demo-ui-topic/src/styles/design-tokens.css`（已含政策要素色，本次无需新增）

---

## 1. 产物清单

| 文件 | 动作 | 说明 |
|------|------|------|
| `demo-ui-topic/docs/ia/policy/POL-ui-spec.md` | **新增** | 政策 9 页视觉规格：六骨架+三段工作区 / 通用组件 Arco 映射皮肤（22 个）/ ECharts 图表类型与配色序列 / Leaflet 政策地图 / AntV G6 产业覆盖图谱 / MetricCard+ⓘ MetricSpecCard+🧪 MockBadge+⚠️ 待确认角标 / token 引用清单 / 政策要素色确认 / §14 自检 |
| `agent-delivery/agent-handoffs/政策模块-E7/UI-POLICY-tokens-spec.md` | **新增** | 本 handoff（§14 检查清单 14 条对照表 + token 引用清单 + 待评审开放项 + 架构合规自检 + 阻塞与风险 + cost）|

> **未改任何代码/配置**：`package.json` / `vite.config.ts` / `.gitignore` / `tailwind`(无) / `routes.tsx` / `design-tokens.css` **均未改动**（政策要素色 `--sci-elem-policy:#BA8DE5` 在企业维度 POLICY-PROTO 既有任务中已落 design-tokens.css §5，本次复用、不重复新增）。ui-agent 不写页面代码（属 frontend-agent），不替决策拍板。

---

## 2. 栈口径（与 ENT 维度差异，已锁定）

| 项 | 本次政策维度 | 说明 |
|----|------------|------|
| 组件库 | **Arco Design**（`@arco-design/web-react` + icon） | 派单口径明确"新页面权威栈=Arco，禁 antd"，与 D8 §2.9 + UX handoff §4 一致 |
| 图表 | **ECharts** | 禁 recharts（D8 栈）；现有专题 3 页 recharts 须迁移 |
| 地图 | **Leaflet** | B2/B6 政策地图三级下钻 |
| 图谱 | **AntV G6** | B3/B6 产业覆盖，关系走 NebulaGraph |
| 落地方式 | Arco 组件 + `design-tokens.css` 项目级 token 覆盖 | 不做 library-agnostic 折中（区别于 ENT-ui-spec 的栈口径待裁决） |

> 因此本规格**未沿用 ENT-ui-spec 的「不引入 Arco / 改纯 Tailwind」争议**——政策维度栈口径无歧义，直接 Arco。

---

## 3. Design.md §14 检查清单 14 条对照表

> §14 = 检查清单 8 条（生成前自检）+ 验收标准 6 条 = 14 条。

| # | §14 条目 | 类别 | 状态 | 证据（POL-ui-spec 章节） |
|---|---------|------|------|------------------------|
| 1 | 仍是浅蓝白科技工作台，非深色大屏 | 检查 | ✅ | §0 红线 + `--sci-bg-page:#D8E7FC` 锁定 |
| 2 | 保留 Header/左导航/主内容容器/中央主视图/右侧分析 | 检查 | ✅ | §1.1 六骨架 + §1.3 三段工作区（右侧研判不可删） |
| 3 | 选中态统一 `#165DFF` 或 `#E8F3FF` | 检查 | ✅ | §0 + §1.2 + §2.12（`--sci-primary`/`--sci-primary-soft`） |
| 4 | 表单/按钮/分页/标签接近 Arco 节奏 | 检查 | ✅ | §2.14 控件 h32 + §2.13 分页 + §2.6 Tag |
| 5 | 地图工具栏/图例/筛选尺寸克制 | 检查 | ✅ | §4 工具条 h32/小24/图标16；§2.1 ContextBar h32 |
| 6 | 覆盖 loading/empty/disabled/error 状态 | 检查 | ✅ | §0 通用交互 8 态（Skeleton/Empty/Alert）|
| 7 | 图表色遵循要素色/图表色序列 | 检查 | ✅ | §3 配色全取 `--sci-chart-*` / `--sci-seq-blue-*`；§7 政策要素色 |
| 8 | 避免霓虹/紫蓝发光/营销 hero/emoji/无意义占位 | 检查 | ✅ | §0 红线明示 |
| 9 | 首屏一眼是地图/图谱分析工作台，非卡片仪表盘 | 验收 | ⏳ | 规格定调三段工作区（A1/A2/A3/B2/B3）；frontend 实现后截图核验 |
| 10 | Header 高度 ≈64px | 验收 | ⏳ | token 锁 `--sci-header-h:64px`（§1.1）；实现后核验 |
| 11 | 左侧展开导航 ≈200px | 验收 | ⏳ | token 锁 `--sci-sidebar-w:200px`（§1.1/§1.2）；实现后核验 |
| 12 | 表单/按钮/分页/工具栏高度 ≈32px | 验收 | ✅ | §2.14/§2.1/§4（规格已约束 h32） |
| 13 | 主色取样 ≈`#165DFF`、底色 ≈`#D8E7FC` | 验收 | ✅ | token 锁定（§0/§8） |
| 14 | 普通卡片无强阴影；中央主视图 > 右侧分析面板；右侧含 tabs/分组；依赖含 `@arco-design/web-react`，无 antd | 验收 | ✅/⏳ | 卡片 `shadow:none`（§2.2）；面积约束（§1.1）；SecondaryAnalysisTabs（§2.12）；栈=Arco 禁 antd（§2 本 handoff）。面积比例 frontend 实现后截图核验 |

> 检查 8 条全 ✅；验收 6 条中 4 条 token/规格已锁定，2 条（首屏观感、Header/Sidebar 实测、面积比例）待 frontend-agent 实现后截图核验。

---

## 4. token 引用清单（禁硬编码，全部来自 design-tokens.css）

| 类别 | token |
|------|-------|
| 底色/面/边框 | `--sci-bg-page` `--sci-surface-main/-muted/-solid/-soft/-hover` `--sci-border(-strong/-white)` `--sci-map-border` |
| 文字 | `--sci-text-1/2/3` `--sci-text-placeholder` `--sci-text-number` |
| 主色 | `--sci-primary(-hover/-soft/-border)` |
| 状态/方向 | `--sci-success/warning/danger/link(-soft)`；`--sci-trend-up`(升红)/`-down`(降绿)/`-flat`(平灰) |
| 政策要素色 | `--sci-elem-policy:#BA8DE5`（+`-soft`），见 §6 |
| 图表 | `--sci-chart-1…14`；连续量 `--sci-seq-blue-1…6`；奖牌 `--sci-rank-gold/silver/bronze` |
| 字体 | `--sci-fs-*` `--sci-lh-*` `--sci-fw-*` `--sci-font-cn/-num` |
| 圆角/描边/阴影/间距 | `--sci-radius-*` `--sci-stroke` `--sci-shadow-none/popover/float/soft` `--sci-space-1…8` |
| 控件/骨架 | `--sci-control-h(-sm/-lg)` `--sci-input-h` `--sci-tag-h` `--sci-switch-*` `--sci-checkbox` `--sci-radio` `--sci-icon` `--sci-header-h` `--sci-sidebar-w(-collapsed)` `--sci-content-margin` `--sci-analysis-w` `--sci-layer-panel-w` `--sci-drawer-w` |
| 层级/动效 | `--sci-z-*` `--sci-ease` `--sci-dur-*` |
| 权限/血缘 | `--perm-level-l0…l4` `--perm-lock-*` `--perm-upgrade` `--perm-pending(-soft)` `--perm-mock(-soft)` `--lineage-card-bg` `--lineage-info-fg` |

> Arco 主题层覆盖（如需）按 D8 §13 `primary-6:#165DFF` 等，取值与上表 token 一致，不另起色值。

---

## 5. 待 UI/UE 评审开放项

| 编号 | 开放项 | 当前处理 | 待定方 |
|------|--------|---------|--------|
| O-UI-01 | 政策要素正式标准色 | 沿用 `#BA8DE5`（chart-13 补位），标 🟡 | UI/UE |
| O-UI-02 | 门户 6 新页路由登记 `routes.tsx`（`/policy-portal/*`） | 规格已定，ui-agent 不改代码，待评审后 frontend-agent 登记 | UI/架构师 |
| O-UI-03 | B2 三级行政区划下钻精度与降级阈值 | P1 复杂则降级平面分级图 | 甲方（与企业 K-O4 同源）|
| O-UI-04 | 角色分级视觉（受限/脱敏/导出水印配额）范围 | 复用 ENT-ui-spec §6 角色态规格 | 甲方（K-POL01/02）|
| O-UI-05 | 现有专题 3 页 recharts→ECharts、自绘→Leaflet/G6 迁移 | 规格已按 ECharts/Leaflet/G6 定调 | frontend/架构师 |

---

## 6. 政策要素色确认（`--sci-elem-policy`）

- **现值**：`#BA8DE5`（图表序列 `--sci-chart-13` 补位，柔紫，与论文紫 `#A872E2` 区分）；浅底 `--sci-elem-policy-soft = rgba(186,141,229,0.12)`。
- **由来**：D8 §4.3 仅固定 10 类要素色、**无"政策"固定色**；按 `ui.mdc` 第 5 条"按 chart 序列补位并 handoff 说明"取值，已在 `design-tokens.css` §5 显式标注。
- **用途**：仅政策"要素类别"标识（类型/领域 Tag 低饱和底、图例色点、混合图谱政策节点）；**不用于主色/按钮/装饰**；政策级别/状态/方向仍走蓝梯度/状态色/方向色。
- **状态**：🟡 沿用并**标注待 UI/UE 确认**；若甲方/UE 有正式色，仅替换 `--sci-elem-policy` 一处即全局生效。

---

## 7. 架构合规自检（公约 §2 十条）

| # | 铁律 | 合规 | 说明 |
|---|------|------|------|
| 1 | 算法只在 Python | ✅ | 纯样式 token + 视觉规格，无算法 |
| 2 | 调用链 前端→Java→Python | ✅ | 规格不越层；图表/地图/图谱仅渲染 Java 聚合结果 |
| 3 | 图谱用 NebulaGraph | ✅ | B3/B6 G6 渲染 `gkx_policy`，不直连 nGQL |
| 4 | 可观测性必加 | ⏸ | 埋点由 frontend-agent 落 `observability.ts`（userflow 21 项）|
| 5 | CI/CD push→绿→dev | ⏸ | 文档阶段未触发部署 |
| 6 | demo2 只读 merge | ✅ | 产物在 demo-ui-topic docs，不涉合并 |
| 7 | 共享聚合核心（方案 A） | ✅ | 专题+门户共享 polan + Java 聚合核心 |
| 8 | ADS 先行 + Mock | ✅ | 规格贯彻 D9 ⓘ/🧪/⚠️，Wave 0 全 Mock |
| 9 | 前端规范唯一来源 D8 | ✅ | Arco+ECharts+G6+Leaflet（#165DFF）；token 引 design-tokens.css；含 §14 对照 |
| 10 | 数据血缘 D9 | ✅ | 每统计数字 ⓘ+🧪，口径未定 ⚠️；引 cfg_metric-POLICY-seed.yaml（19 条） |

> 全部 ✅/⏸，无 ❌。

---

## 8. 阻塞与风险

- **无阻断项**。本任务按例外约定跳过人工评审 gate，直接产出规格文档。
- **R1（口径未定，承接 UX R1）**：QPOL-01/02/03 + 🟡-04/05/07 共 6 类业务口径（政策类型分类、密度/支持强度/三维/力度权重、产业适配匹配规则、连续性定义、国内外合并、力度临时权重）未定。规格已用 ⚠️ 角标承接，**ui-agent 不替甲方拍板**（公约 §3.8）；请 PM 推动甲方确认并更新 `客户决策清单跟踪表.md`，否则 A1/A2/A3/B1/B4 统计数字返工。
- **R2（数据缺口，承接 UX R2）**：A3 落地实效性/政策效果执行监测、宏观/社会数据 ❌ 无 ODS 来源待采购；`dwd.industry_chain`、`dim_region`(深圳区县)、NebulaGraph `gkx_policy` 需 data/algorithm-agent 确认就位。Wave 0 以 Mock 🧪 填充。
- **R3（栈迁移）**：现有政策专题 3 页为 Tailwind+recharts 自绘，与 D8 权威栈（Arco+ECharts+G6+Leaflet）系统性偏离。门户 6 新页建议直接按 D8 权威栈起步；专题 3 页 lumen 复刻时迁移（O-UI-05）。
- **R4（范围混淆）**：DS-10/11/12（展示系统科技政策跟踪）与 `/policy-portal` 含近义词（政策地图/全景/对比），本规格仅覆盖 9 页前端，frontend-agent 须延续，避免误扩触发 ±10% 铁律。
- **R5（复杂交互需人工评审）**：B2 Leaflet 三级下钻、B3/B6 G6 产业链图谱、A2 NLP 条款溯源为复杂能力，规格已标"需人工评审、不简化静态图"；P1 地图可降级平面分级图（不降为静态图片）。

---

## 9. cost 字段（budget-estimate.md）

| 字段 | 值 |
|------|----|
| actual_tokens | ~70k（读 Design.md 14 节 + POL-IA/wireframe + UX/ENT handoff + design-tokens.css + ENT-ui-spec 模板 + 2 产物撰写） |
| model_used | Claude Opus 4.8 |
| actual_cost | ~$2.4（估算，单任务 < $10 阈值，无需复盘） |
| cost_warn | none |

---

## 10. 下一步与接力

1. **UI/UE + 架构师评审** POL-ui-spec；确认政策要素色（O-UI-01）、门户路由登记授权（O-UI-02）、角色态范围（O-UI-04）。
2. **frontend-agent**：据 POL-ui-spec + POL-wireframe 实现 P0 6 页（A1/A2/A3/B1/B5/B6）优先；Wave 0 Mock + ⓘ/🧪/⚠️；落 observability.ts 21 埋点；recharts→ECharts、自绘→Leaflet/G6。
3. **algorithm-agent**：实现 cfg_metric 标 🔧 的 12 条 formula。
4. **data-agent**：确认 `dwd.industry_chain`/`dim_region`(深圳)/NebulaGraph `gkx_policy` 就位；补登 B2「区域政策密度」、B5「近 N 天新发数」独立 metric。
5. **PM**：推动甲方确认 QPOL-01~03 / 🟡-04/05/07 / K-POL01/02，更新客户决策清单跟踪表。

> 本 handoff 即 POLICY-PROTO-L03 的交付证据。维护：ui-agent 起草，业务口径变更须 PM + 甲方确认。

---

**handoff 结束**
