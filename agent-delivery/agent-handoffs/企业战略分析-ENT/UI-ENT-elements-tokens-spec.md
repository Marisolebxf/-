# UI Handoff：企业要素 设计 Tokens + 组件视觉规格（ui-agent）

- 时间：2026-06-19
- 角色：ui-agent（视觉设计 + 前端样式工程）
- 仓库：`topic_demo`（原型仓，独立 git）
- 分支：`feat/ent-elements-build`
- 推送状态：**未 push**（按派单纪律，topic_demo push 由人工评审后触发）
- 派单依据：企业要素前端重做 —— 维持现状技术栈、视觉严格对齐 D8（`Design.md`）
- 上位设计：`ENT-search-design.md` §10 / `ENT-element-master-design.md`
- 权威规范：`agent-delivery/Design.md`（D8）+ `data-lineage-policy.md`（D9）

---

## 1. 产物清单（新增 3 + 改 1）

| 文件 | 动作 | 说明 |
|------|------|------|
| `topic_demo/src/styles/design-tokens.css` | **新增** | D8 权威设计 token 单一真源：基础色/状态色/方向色/10 类要素色（+浅底）/14 色图表序列+蓝梯度+奖牌色/SearchScaffold 要素色板/字号 7 级/圆角/描边阴影/间距/控件与骨架尺寸/z-index/动效。仅 `:root` 变量，无副作用 |
| `topic_demo/src/styles/README-tokens.md` | **新增** | tokens 使用说明：与 `theme.css` 关系、Tailwind v4 三种消费方式（任意值类 / 内联 style / 图表读变量，**无需改构建配置**）、关键 token 速查、要素色板表、红线 |
| `topic_demo/docs/ia/enterprise/ENT-ui-spec.md` | **新增** | 关键组件视觉皮肤规格（library-agnostic）：SearchHub / 高级筛选条件构建器 / 结果工具条+企业卡片+表格 / 统一企业画像（抽屉720+整页）/ 通用组件（ContextBar·MetricCard·MetricSpecCard·MockBadge·StatusTag·空态·分页）/ 角色分级视觉（受限·脱敏·引导·锁标）/ 基础控件皮肤 / 图表配色 / 浮层 / metric_id 清单 / §14 自检 |
| `topic_demo/src/styles/index.css` | **改（加 1 行）** | 在最前追加 `@import './design-tokens.css';`，使 token 为基础层先加载。非构建配置文件 |

> 要素色板（派单交付物 3）：见 `design-tokens.css` §5 与 `README-tokens.md` §4——
> 企业 `#16C7C7` / 科研机构 `#4DD164` / 服务机构 `#F779B6` / 人才 `#4180FD`（均复用 D8 固定要素色）；
> 政策 `#BA8DE5`（D8 无固定政策色，按图表序列 chart-13 补位，已在文档显式标注，见 §4 偏离说明）。

---

## 2. 是否动了构建配置 / tailwind.config

| 项 | 结论 |
|----|------|
| `package.json` | ❌ 未改 |
| `vite.config.ts` | ❌ 未改 |
| `.gitignore` | ❌ 未改 |
| **`tailwind.config.*`** | ❌ **不存在**（本仓 Tailwind v4，主题以 `@theme inline` 写在 `src/styles/theme.css`）；**未改 `theme.css` 的 `@theme`**。利用 Tailwind v4「任意值类」直接读 CSS 变量（如 `bg-[var(--sci-primary)]`），**无需把色板写进 `@theme`**，故零构建配置改动 |
| `src/styles/index.css` | ✅ 仅新增 1 行 `@import`（样式入口，非构建配置） |
| `scripts/check-design-contract.mjs` | ❌ 未改；已本地运行 `node scripts/check-design-contract.mjs` → **Design contract checks passed** |

**tokens 关键值**：主色 `--sci-primary:#165DFF`、hover `#4080FF`、选中浅蓝 `#E8F3FF`、页面底 `--sci-bg-page:#D8E7FC`、正文 `--sci-fs-body:14px`、关键数值 `--sci-fs-metric:30px`、控件高 `--sci-control-h:32px`、输入/按钮圆角 `4px/3px`、卡片/面板圆角 `8px/12px`、弹层阴影 `0 4px 10px rgba(0,0,0,.1)`、抽屉宽 `--sci-drawer-w:720px`。

---

## 3. 偏离说明（重要）

### 3.1 ⚠️ 栈口径差异：「不引入 Arco」与仓现状/契约冲突（需 PM/架构师裁决）

- 派单口径：「技术栈维持现状 = React+Vite+Tailwind+recharts+lucide，**不引入 Arco**」。
- 仓**实际现状**：`topic_demo` **已含 Arco Design**——`package.json` 依赖 `@arco-design/web-react`；
  `src/app/App.tsx` 用 Arco `ConfigProvider` 包裹并 import `arco.css`；多数企业页用 Arco `Button/Select/Tabs`；
  且 `scripts/check-design-contract.mjs` **强制 Arco**（断言 package.json/App.tsx/Layout.tsx 必须有 Arco）。
- 团队公约 D8（§2.9）亦规定「新页面权威栈 = Arco」。
- 结论：「不引入 Arco」与仓现状、设计契约、团队公约**三者冲突**（公约 §6：用户指令不得违反铁律，须人类裁决）。
- **本 ui-agent 处理**：①不替决策拍板；②交付物（tokens + 视觉规格）**与组件库无关**，无论维持 Arco 还是
  改纯 Tailwind 均适用——token 既可覆盖 Arco 组件主题，也可用 Tailwind 任意值类直接表达；
  ③**未改 `package.json`/`vite.config`/`design:check`**，不制造既成事实；④已在 `ENT-ui-spec.md` §0 与 §12
  显式标注差异与两条落地路径，留给 PM/架构师裁决。
- **请 PM/架构师裁决**：企业要素前端是「维持 Arco（与契约一致，推荐）」还是「改纯 Tailwind（需双签 + 同步改 design:check）」。

### 3.2 政策要素色补位

D8 §4.3 仅固定 10 类要素色，**无「政策」固定色**（且已取消「资讯」色）。SearchScaffold 需要政策要素色，
按 `ui.mdc` 第 5 条指引「按 chart 序列补位并在 handoff 说明」，取图表序列 chart-13 `#BA8DE5`（柔紫，
与论文紫 `#A872E2` 区分）。已在 tokens 与文档显式标注。如甲方/UE 另有政策标准色，替换 `--sci-elem-policy` 即可。

### 3.3 与 `theme.css` 既有 `--sci-*` 的关系

`theme.css` 已镜像一份 `--sci-*` 子集（供 Tailwind `@theme` 与 Element `--el-*` 兼容）。
`design-tokens.css` 是**完整真源**（补齐间距/字号/控件高/要素色板/图表序列/层级），重复变量**值完全一致**，
无冲突；新页面统一引用 `design-tokens.css`。未来可考虑让 `theme.css` 反向引用本文件以彻底单源（本期未做，避免改动既有契约校验项）。

---

## 4. D8 §14 合规自检（14 条）

**§14 检查 8 条**（文档/token 层面）
1. ✅ 浅蓝白工作台、无深色大屏（红线明示 + 底色 token 锁定）
2. ✅ 规格保留容器/主视图/右侧分析（§4/§8）
3. ✅ 选中态统一 `--sci-primary` / `--sci-primary-soft`
4. ✅ 按钮/输入/分页/标签 32px 节奏 + Arco 风格语义（§7）
5. ✅ 工具栏/图例/筛选尺寸克制（h32/icon16）
6. ✅ 8 态全覆盖（默认/hover/active/disabled/loading/empty/error/半选，§0）
7. ✅ 图表色遵循 §4.3 要素色 + 图表序列（tokens §3/§4，spec §9）
8. ✅ 无霓虹/紫蓝发光/营销 hero/emoji 表达状态（红线）

**§14 验收 6 条**
1. ⏳ 首屏工作台观感 —— frontend 实现后截图核验
2. ⏳ Header ≈64px —— 复用骨架时核验（token 已锁 `--sci-header-h:64px`）
3. ⏳ 侧栏 ≈200px —— 同上（`--sci-sidebar-w:200px`）
4. ✅ 控件/分页/工具条 ≈32px（规格已约束）
5. ✅ 主色 `#165DFF`（token 锁定）
6. ⚠️ 「无 antd/.ant-」：本规格不引 AntD；Arco 去留以 §3.1 裁决为准

## 5. 架构合规自检（公约 §2 十条）

1. ✅ 算法只在 Python —— N/A（纯样式 token+文档）
2. ✅ 调用链 —— N/A
3. ✅ NebulaGraph —— N/A
4. ✅ 可观测性 —— N/A（本期无页面逻辑）
5. ✅ CI/CD —— 设计/样式类，未触发部署；design:check 本地绿
6. ✅ demo2 只读 merge —— N/A（在 topic_demo）
7. ✅ 共享聚合核心 —— N/A
8. ✅ 数据策略（ADS 先行 + Mock）—— spec 已贯彻 D9 ⓘ/🧪/⚠️ 三件套
9. ✅ 前端规范唯一来源 D8 —— token/spec 严格对齐 Design.md §4/§5/§6/§7/§13；§3.1 已标注 Arco 栈口径差异待裁决
10. ✅ 数据血缘 D9 —— spec 含 MetricSpecCard/MockBadge/⚠️ 规格 + 本页 metric_id 清单

---

## 6. 给 frontend-agent 的实现提示

1. 引用 token：优先 Tailwind 任意值类 `bg-[var(--sci-primary)]`，动态色用内联 `style`，图表用 `getComputedStyle` 读变量（见 `README-tokens.md` §2）。
2. 卡片范式：白底 86% + 1px `--sci-border` + 圆角 8 + `shadow-none`；hover 才上轻阴影。
3. 每个统计数字旁必带 ⓘ(MetricSpecCard) + Wave 0 必带 🧪(MockBadge)；口径未定项 ⚠️ 并登记 `客户决策清单跟踪表.md`（K-O30/Q010/K-O23）。
4. SearchScaffold 壳组件要素无关，要素差异全进配置（含要素色取 `--sci-elem-*`）。
5. **动工前确认 §3.1 栈口径裁决**（维持 Arco / 改纯 Tailwind）。

---

## 7. cost 字段（budget-estimate.md）

| 字段 | 值 |
|------|----|
| actual_tokens | ~95k（读 Design.md/2 份企业设计/data-lineage + 现有样式盘点 + 3 产物撰写） |
| model_used | Claude Opus 4.8 |
| actual_cost | ~$3.2（估算，单任务 < $10 阈值，无需复盘） |
| cost_warn | none |

---

## 8. 下一步

1. UI/UE + 架构师评审 tokens + ENT-ui-spec；**裁决 §3.1 Arco 栈口径**。
2. frontend-agent 据 spec 实现 SearchScaffold 壳 + 企业 config（Wave 0：SearchHub+卡片列表+抽屉画像）。
3. 政策标准色（§3.2）如甲方有定，回填 `--sci-elem-policy`。

---

**handoff 结束**
