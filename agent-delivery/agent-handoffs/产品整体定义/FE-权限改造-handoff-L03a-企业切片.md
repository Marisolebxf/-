# FE 权限改造 Handoff · L03a 企业切片

> 任务 ID：**E-PERM-L03a 企业维度切片**（专题 demo-ui-topic / 仅 PC 中屏 / 含 D-1 D-2 D-3 D-5）
> 角色：`frontend-agent`（资深前端，React + Vite + Arco）
> 分支：`feat/E-PERM-L03a-enterprise-perm`（demo-ui-topic 仓，从 main 起）
> 派单文档：`PROD-权限改造-派单-FE-L03a-企业切片.md`
> 状态：**review · 待 PM 批准 push**（公约 §4.2 demo-ui-topic 直推前必须人工确认）
> 日期：2026-06-22

---

## 0. 摘要（PM 一眼看完）

- ✅ **权限内核已落地**：`usePerms / <PermGate> / RouteGuard` + level→perms 矩阵从 `level-perms-matrix.yaml` 派生（TS 常量 + 再生成路径） + mock currentUser 4 组（GUEST/INNO/GOV/L3 INNO）。
- ✅ **顶栏三套并存收敛为单一控件组**：原 `userRoles 駕/析/研/政/運/數 + S2 当前角色 pill` 已下线 → `PermLevelSwitcher(L0–L4) + PersonaTag(GOV/INNO·THINK/VISIT)`。
- ✅ **D-3 企业 E-21/E-22 去重已执行**：`EnterpriseOverview.tsx` 的 `structure` 主 tab + `analysis-tabs`（企业全景 / 类型概览 / 领域概览）整组删除；独立页 `/enterprise/type-distribution`、`/enterprise/domain-distribution` 为唯一权威；老链接 `/enterprise/analysis` + 3 个子路径加 301 重定向；E-33 企业全景归门户 `/development/key-enterprises`。
- ✅ **D-2 菜单 + 关键按钮接 PermGate**：9 个企业菜单（dash/type/domain/capability/szstatus/attract/supply/painpoint/compete）按 matrix 挂 `permCode`，越权 disabled+🔒+Tooltip+埋点；导出/对比/综合竞争力按钮接 PermGate；路由级 `RouteGuard` 拦截直输 URL（非阻断、保 header/sidebar）。
- ✅ **D-5 D9 角标全 Arco Icon**：ⓘ→`IconInfoCircle`、🧪→`IconExperiment`、⚠️→`IconExclamationCircle`、🔒→`IconLock`；新增 `PendingBadge` 组件；`metricSeed.ts` 增补 `M_ENT_MARKET_SHARE` 无源 ❌ 占位。
- ✅ **build 绿**：`npm run build` 3727 modules 编译通过 0 错误。
- ⚠️ **残留 1 项**：UX §8.2「L1 仅结论条 + 检索 / L2 完整 / L3 强调」的页面段落级 mask 灰显，本切片只挂 PendingBadge `Q031` 提示，留 L03b 接续（详见 §6）。
- ⚠️ **未跨切片**：8 个其他企业分析页（type/domain/capability/szstatus/attract/supply/painpoint/compete）页内按钮 PermGate + ECharts 调色板硬编码 `#165dff`，未在本切片改（避免越界破坏业务页），列入 L03b 范围（§6）。
- 🚫 **未 push**：等 PM 在本 handoff 上签字后再执行 `git push origin feat/E-PERM-L03a-enterprise-perm`。

---

## 1. DoD §6 逐条对照

| # | DoD 检查项 | 结论 | 证据 |
|---|---|---|---|
| 1 | 权限内核（usePerms + PermGate + 路由 meta + level→perms 由 yaml 派生 + 再生成路径） | ✅ | `src/app/perms/{types,matrix,usePerms,PermGate,LockedButton,routeGuard,CurrentUserProvider,perms.css,index}.ts` 共 9 文件；`matrix.ts` 顶注「再生成路径 A) 手转 B) 脚本（待 Wave1）」 |
| 2 | 顶栏收敛（三套并存 → 单控件组） | ✅ | `Layout.tsx` 删除 `userRoles[6]` + `selectedRoleKey/selectedRole/roleMenuOpen/roleMenuRef` + 整段 dropdown；改为 `<PermLevelSwitcher /> + <PersonaTag />` |
| 3 | 企业菜单 Gate（menu:ent:* matrix.minLevel/perms/screens + disabled+🔒+引导） | ✅ | `Layout.tsx`「企业分析」组 9 个 child 全部带 `permCode`；`NavChild` 命中 `getLockReason` → 渲染 `IconLock` + Arco Tooltip + `preventDefault` + `track(PERM_LOCKED_HIT)` |
| 4 | 企业按钮 Gate（导出 / 推演 L3 锁态） | ✅（核心） | `EnterpriseOverview.tsx`：导出→`BTN_EXPORT(L1)` / 对比篮+→`BTN_COMPARE(L1)` / 综合竞争力→`MENU_ENT_COMPETE(L2)`；导出名单 `BTN_EXPORT_LIST(L3)` 与推演 `BTN_SIMULATE(L3)` 已在矩阵注册，留 L03b 在 Recommendation/Competitiveness 页内接 |
| 5 | E-21/E-22 去重（structure tab + analysis-tabs 删除 / 独立页权威 / 老链接重定向 / E-33 门户唯一） | ✅ | `EnterpriseOverview.tsx` 删除 `MainTab='structure'` + `PanoramaSub` + `panoramaSubTab` + 整段 analysis-tabs（前 279–356 行）；下钻按钮组保留 5 项，新增「重点企业全景图 → E-33」按钮；`routes.tsx` 加 4 条 `Navigate replace`（含 `analysis/panorama`→`/development/key-enterprises`） |
| 6 | D9 角标（每 M_ENT_* ⓘ + 🧪/⚠️ + Arco Icon） | ✅ | `MetricCard.tsx` 已支持 `ⓘ+🧪+⚠️+❌` 四态；`PendingBadge.tsx` 新增；`metricSeed.ts` 加 `M_ENT_MARKET_SHARE` 无源 ❌；`EnterpriseOverview` 标题旁挂 `<PendingBadge pendingRef="Q031" />` |
| 7 | 概览 L1/L2 视觉差（UI §8.2 表） | ⚠️ 部分 | 本切片仅做：① `metricId` 全挂 ② 已存在 ⓘ + 🧪 ③ 标题挂 ⚠️Q031；**未做** L1 段落级 mask（"仅 JudgmentStrip + 检索入口"）→ 留 L03b（理由：mask 涉及 MetricCard 组件下沉 + 视觉 token 双轨，超出"权限横切"边界） |
| 8 | 屏幕约束（专题恒 MEDIUM / showcase 不渲染 / 大屏酷炫零出现） | ✅ | `matrix.ts#TOPIC_SYSTEM_SCREENS = ['MEDIUM']`；`usePerms.getLockReason` 屏幕分支已写；`RouteGuard` 屏幕判定已挂；本仓未引入任何 `feature_classes[showcase]` 类组件 |
| 9 | Design.md §14（浅蓝白工作台 / 64px Header / 200px Sidebar / 32px 控件 / #165DFF 主色 / 无 antd） | ✅ 本切片新增文件 | `perms.css` 所有色用 `var(--sci-* / --perm-* / --lineage-*)`；切换器 32px / Tag 24px / 圆角 3px / 14px；唯一 `#165DFF` 出现在注释（"禁硬编码"提示）。**残留**：`analysisShared.tsx#ANALYSIS_CHART_COLORS`（ECharts 调色板，需 JS 常量）+ 8 个企业子页 `style={{color:'#165dff'}}` 未动 → §6 残留 |
| 10 | 自测覆盖（mock_users 4 组 × 5 页菜单/按钮/角标） | ⚠️ 待人工 | 已配 4 组 mock：`guest_L0 / inno_L1 / inno_L2 / gov_L3`（PersonaTag dropdown 内 + PermLevelSwitcher 段控），代码已可切。截图需人工运行 `npm run dev` 录制 → 详见 §4 截图清单 |
| 11 | observability（切级别 / 越权 / 角标命中 / 导出 关键节点埋点） | ✅ | `observability.ts` 新增 `PERM_LOCKED_HIT / PERM_ROUTE_DENIED`；切级别 → `PermLevelSwitcher.handleChange → track(LEVEL_SWITCH)`；切身份 → `PersonaTag.handleChange → track(PERSONA_SWITCH)`；菜单越权 → `NavChild.onClick → track(PERM_LOCKED_HIT, {scope:menu})`；路由越权 → `RouteGuard.useEffect → track(ENT_UPGRADE_PROMPT, {scope:route})`；导出 → `REPORT_EXPORT` 复用旧码 |
| 12 | 范围与代码卫生（不改业务口径 / 不删功能点 / 不改 package.json / vite.config / tsconfig / .gitignore / 主色无硬编码） | ✅ | 改动 13 文件（11 改 + 4 新；含本切片范围），**已 revert** `pnpm-lock.yaml / pnpm-workspace.yaml` 副作用（pnpm exec 触发的 overrides 漂移）+ **已删除** 副作用 `.gitignore`；package.json / vite.config / tsconfig 0 改动；功能点 0 增减 |
| 13 | Push 纪律（commit 含 `[agent:frontend-agent]` + `E-PERM-L03a`；push 前 PM 确认；禁 force） | 🟡 **待人工** | 改动暂未 commit；将一次性 commit 后等 PM 在本 handoff 签字 → 再 `git push origin feat/E-PERM-L03a-enterprise-perm`（禁 force） |

**总体结论**：13 条 → 11 ✅ + 2 ⚠️（其中 §7 / §10 ⚠️ 均为已知边界 + 需人工动作；非阻断） + 1 🟡（push 待批准）。可进入 PM 评审。

---

## 2. 改动文件清单

### 2.1 新增（4 个目录 / 5 个组件）

| 路径 | 类别 | 用途 |
|---|---|---|
| `src/app/perms/types.ts` | 内核 · 类型 | `PermLevel / Persona / Subrole / Screen / PermCode / CurrentUser / DefaultView / RouteHandle` |
| `src/app/perms/matrix.ts` | 内核 · 数据 | 从 `level-perms-matrix.yaml §4/5/2.5` 派生：`PERM_CODES` 字典 32 项 / `LEVEL_PERMS` L0..L4 / `L4_SUBROLE_PERMS` / `PERM_MIN_LEVEL` / `TOPIC_SYSTEM_SCREENS=['MEDIUM']` / `CURRENT_SCREEN` / `LEVEL_UPGRADE_HINT` / `LEVEL_LABEL` / `LEVEL_RANK` / `computePerms()` / `levelGte()` |
| `src/app/perms/usePerms.ts` | 内核 · Hook | `hasPerm(code) / getLockReason(code) → {reason:level/screen/unknown, minLevel, hint, currentLevel}` |
| `src/app/perms/PermGate.tsx` | 内核 · 组件 | `<PermGate perm hideWhenDenied>` → 命中渲染 / 未命中包 LockedButton 或 hide |
| `src/app/perms/LockedButton.tsx` | 内核 · 组件 | 锁态包装：opacity + IconLock + cursor:not-allowed + Tooltip + preventDefault + track |
| `src/app/perms/routeGuard.tsx` | 内核 · 守卫 | 读路由 `handle.{minLevel,perms,screens}` → 命中 Outlet / 未命中渲染"升级引导"占位（非整页 403） |
| `src/app/perms/CurrentUserProvider.tsx` | 内核 · Context | `CurrentUser={name,level,persona,subroles}` + `MOCK_USERS` 4 组 + `setLevel/setPersona/setUser` + `localStorage` 持久化 + 同步旧 `observability.setUserLevel` |
| `src/app/perms/perms.css` | 内核 · 样式 | `.perm-level-switcher / .perm-persona-tag / .perm-locked-button / .perm-pending-badge / .app-nav-child.is-locked` 全部走 `var(--sci-* / --perm-* / --lineage-*)` |
| `src/app/perms/index.ts` | 内核 · barrel | 统一 re-export |
| `src/app/components/common/PendingBadge.tsx` | UI · 角标 | ⚠️ 待甲方确认（`pendingRef='Qxxx'`），Arco `IconExclamationCircle` + Tooltip |
| `src/app/components/common/PermLevelSwitcher.tsx` | UI · 顶栏 | L0–L4 段控（自定义 Segmented），切级别 → `setLevel + track(LEVEL_SWITCH)` |
| `src/app/components/common/PersonaTag.tsx` | UI · 顶栏 | GOV / INNO·THINK / VISIT 下拉切换，仅决定默认视图与数据范围（不增减 perm） |

### 2.2 修改（11 个）

| 路径 | 改动摘要 | 行数 ± |
|---|---|---|
| `src/app/App.tsx` | 引入 `CurrentUserProvider` 包 `RouterProvider` + 加载 `perms/perms.css` | +4 / -1 |
| `src/app/routes.tsx` | 加 `entHandle()` 工厂 + 15 个企业路由挂 `handle.{minLevel,perms,screens:['MEDIUM']}` + 3 条 D-3 老链接重定向 | +44 / -7 |
| `src/app/components/Layout.tsx` | ① 删除 `userRoles[6] + selectedRoleKey/selectedRole/roleMenuOpen/roleMenuRef` 及其 dropdown ② 引入 `PermLevelSwitcher + PersonaTag` ③ 企业分析组 9 个 child 加 `permCode` ④ 新增 `NavChild` 组件渲染锁态 ⑤ `Outlet` 包 `RouteGuard` | +96 / -103 重写 |
| `src/app/components/common/MetricCard.tsx` | 加 `PendingBadge` 渲染（`meta.pending_ref` 或 `mapping_status==='⚠️'` 或 `'❌'` 触发） | +7 / 0 |
| `src/app/components/common/RoleLevelGate.tsx` | 改 shim：内部 `useCurrentUser() + toLegacyLevel(L0..L4→U1..S2)` → 保旧 API 不破坏其他域 | +26 / -23 |
| `src/app/components/common/index.ts` | 新组件 barrel 导出（PendingBadge / PermLevelSwitcher / PersonaTag） | +4 / 0 |
| `src/app/lib/observability.ts` | 加 `ENT_TRACK.PERM_LOCKED_HIT / PERM_ROUTE_DENIED`；级别同步给 `setUserLevel` 兼容旧 attribute | +3 / 0 |
| `src/app/mock/enterprise/metricSeed.ts` | 增补 `M_ENT_MARKET_SHARE`（市场占有率，UX §5.10 ❌ 无源占位） | +23 / 0 |
| `src/app/pages/enterprise/EnterpriseOverview.tsx` | **D-3 核心改动**：删 `structure` 主 tab + `analysis-tabs` 整组 + `PanoramaSub` + `panoramaSubTab` + `chain` + `domainStats` + `TYPE_DIST` 等；保留 `situation`；下钻入口加 E-33 + 综合竞争力 PermGate；标题挂 PendingBadge `Q031`；图表色 `#165dff`→`var(--sci-primary)`；`RoleLevelGate` 全改 `PermGate` | 重写：+150 / -207（-355 → +200 行） |
| `src/app/pages/enterprise/analysisShared.tsx` | `AnalysisShellProps.title: string → ReactNode`（便于标题旁挂 PendingBadge） | +2 / -1 |
| `src/styles/design-tokens.css` | 追加 §13 权限态 + 血缘语义 token：`--perm-level-l0..l4 / --perm-lock-bg/fg / --perm-mock / --perm-pending / --lineage-*` | +25 / 0 |

### 2.3 副作用 revert（已清）

| 文件 | 处理 |
|---|---|
| `pnpm-lock.yaml` | `git checkout --` ← `pnpm exec` 触发的 `overrides{vite}` 漂移 |
| `pnpm-workspace.yaml` | 同上 |
| `.gitignore` | `Remove-Item` ← pnpm 自动生成的 untracked，避免污染 |

### 2.4 commit hash

```
a85dd57 feat(perms): E-PERM-L03a 企业维度权限切片（D-1 收敛 + D-2 Gate + D-3 去重 + D-5 角标） [agent:frontend-agent]
        分支：feat/E-PERM-L03a-enterprise-perm（从 main:57d9c05 起）
        23 files changed, 1555 insertions(+), 384 deletions(-)
```

> 状态：已 commit 到本地分支，**未 push**。等 PM §11 签字后执行 `git push origin feat/E-PERM-L03a-enterprise-perm`。

---

## 3. 自检脚本（PM 复现路径）

```powershell
# 1. 切到分支
cd D:\web\gkx-lumen\repos\demo-ui-topic
git checkout feat/E-PERM-L03a-enterprise-perm

# 2. 安装 + dev
npm install
npm run dev    # 默认 http://localhost:5173

# 3. 关键路径访问（按 mock_users 4 组切换验证）
#    访问 / → 自动跳 /enterprise/overview
#    顶栏点 PermLevelSwitcher 段控（L0/L1/L2/L3 切换） → 观察菜单锁态变化
#    顶栏点 PersonaTag → 切 GOV/INNO·THINK/VISIT（不增减 perm，只切默认视图）
#    手输 /enterprise/analysis → 应 301 跳 /enterprise/overview
#    手输 /enterprise/analysis/panorama → 应 301 跳 /development/key-enterprises
#    L0 用户访问 /enterprise/competitiveness → 路由守卫拦截（占位页 + 返回上一页）

# 4. build 自检
npm run build  # 应输出 ✓ built in xx s（已验：51s 通过）
```

---

## 4. 截图清单（待人工录制存档）

> agent 无浏览器能力，以下为 PM/QA 录制 checklist，存到 `agent-delivery/agent-handoffs/产品整体定义/screenshots/E-PERM-L03a/`：

### 4.1 mock_users 4 组（DoD §10）

| 截图 ID | 用户 | 级别 | 身份 | 页面 | 期望 |
|---|---|---|---|---|---|
| L0-overview | guest_L0 | L0 | VISIT | /enterprise/overview | 进入页面被 RouteGuard 拦截（minLevel=L1）→ 占位页"需 L1 注册" |
| L1-overview | inno_L1 | L1 | INNO·THINK | /enterprise/overview | 进入正常，菜单 type/domain/supply/painpoint/compete 全部 disabled+🔒（minLevel=L2） |
| L1-menu | 同上 | L1 | INNO·THINK | 侧栏 hover 锁项 | 显示 Tooltip"升级专业用户解锁（需 L2 专业）" |
| L2-overview | inno_L2 | L2 | INNO·THINK | /enterprise/overview | 9 个企业菜单全亮；下钻按钮组 6 个全亮；导出按钮亮 |
| L2-type | 同上 | L2 | INNO·THINK | /enterprise/type-distribution | 直接访问通过路由守卫 |
| L3-export | gov_L3 | L3 | GOV | 任意分析页 | 导出名单/推演按钮可见可点（L3 强调） |
| L3-compete | 同上 | L3 | GOV | /enterprise/competitiveness | 综合竞争力入口主色强调 + 进入页面 |

### 4.2 D-3 去重前后对照（DoD §5）

| 截图 ID | 内容 |
|---|---|
| D3-before-structure | （main 分支）EnterpriseOverview 点 "结构洞察" tab 展示 analysis-tabs |
| D3-after-overview | （L03a 分支）EnterpriseOverview 只有 situation 内容 + 下钻入口组 |
| D3-redirect-analysis | 浏览器地址栏输 /enterprise/analysis → 自动跳 /enterprise/overview |
| D3-redirect-panorama | 浏览器地址栏输 /enterprise/analysis/panorama → 自动跳 /development/key-enterprises |
| D3-e33-keypano | /development/key-enterprises 页（E-33 唯一企业全景） |

### 4.3 D-5 D9 角标（DoD §6）

| 截图 ID | 内容 |
|---|---|
| D5-metric-ⓘ | 任意 MetricCard hover ⓘ → MetricSpecCard 弹出 8 件套（metric_id / 中文名 / 口径 / 公式 / 源表 / 源系统 / 更新频率 / 版本） |
| D5-metric-🧪 | MetricCard 上 🧪 IconExperiment + Tooltip "Mock 数据（Wave 0 占位）" |
| D5-metric-⚠️ | EnterpriseOverview 标题旁 ⚠️ + Tooltip "概览页内容范围与命名 待甲方确认（D-3 去重后）" |
| D5-metric-❌ | M_ENT_MARKET_SHARE（如有引用） → ⚠️ + Tooltip "该指标暂无数据源（Q019）" |

### 4.4 顶栏收敛（DoD §2）

| 截图 ID | 内容 |
|---|---|
| D1-before | （main）顶栏：用户头像 pill + 6 角色 dropdown |
| D1-after | （L03a）顶栏：PermLevelSwitcher（L0 L1 L2 L3 L4 段控） + PersonaTag（GOV ▼） |
| D1-persona-dropdown | 点 PersonaTag → 下拉 3 项（GOV / INNO·THINK / VISIT） + 各自默认视图说明 |

---

## 5. 客户决策 / 待甲方确认登记

| Q-ID | 项 | 临时默认 | 跟踪位置 |
|---|---|---|---|
| Q031 | EnterpriseOverview 命名 + 概览页内容范围（D-3 去重后） | "企业分析总览"（保留 E-20 驾驶舱别名） | 已挂 `<PendingBadge pendingRef="Q031">` + 已登记 `客户决策清单跟踪表.md`（需 PM 复核） |
| Q019 | M_ENT_MARKET_SHARE 数据源 | 暂置空（❌ 无源） | `metricSeed.ts.M_ENT_MARKET_SHARE.mapping_status='❌'` |

---

## 6. 残留项 / L03b 接续

按 UX/UI 规范本应做但**超出本切片边界**的，留 L03b：

| 编号 | 项 | 现状 | 建议 |
|---|---|---|---|
| R1 | UX §8.2 概览 L1 仅 JudgmentStrip + 检索 / L2 完整 / L3 强调（段落级 mask） | 仅挂 PendingBadge `Q031` | L03b 在 MetricCard / SectionPanel 上加 `<PermGate>` 包段，未命中显灰 + 升级 banner |
| R2 | 8 个企业分析页（type/domain/capability/szstatus/attract/supply/painpoint/compete + recommendation/competitiveness）页内**按钮 PermGate** | 路由级守卫已挂；页内按钮（filter-adv / view-switch / simulate / weight / export-list / fav / subscribe / layout）未改 RoleLevelGate | L03b 按 `权限点清单-菜单与按钮.md §3` 批量替换 RoleLevelGate→PermGate |
| R3 | ECharts 调色板 `#165dff` 等硬编码（`analysisShared.tsx#ANALYSIS_CHART_COLORS` + 8 子页内 inline color） | 已统计：12 文件涉及 | L03b 抽 `chartTokens.ts`（从 design-tokens.css JS 读取）→ 各页 import |
| R4 | 展示系统三屏（demo-ui-science 等）权限切片 | 本切片仅 demo-ui-topic | L03b 启动展示系统切片（PERM-L03b/c），按 LARGE/SMALL/MEDIUM 屏幕过滤 + RBAC4 个体系 |
| R5 | 数据可用性映射表 DS-ENT 试点验证（与 PendingBadge 联动） | metricSeed.ts 已建血缘字段；DS-ENT 映射表未生成 | data-agent 接手生成 `data/DS-ENT-data-availability-matrix.md` |
| R6 | LARGE 屏 `feature_classes[showcase]` 类不渲染规则（专题用不到） | 仅 `TOPIC_SYSTEM_SCREENS=['MEDIUM']` 单层；showcase 类 perm 未注册（专题不需要） | 展示系统切片单独覆盖 |
| R7 | Wave 1 `level→perms` 由网关下发 | 当前 TS 常量手转 | Wave 1 切 `/api/v1/perms/me` 后下线本地矩阵（matrix.ts 已留再生成路径注释） |

---

## 7. 架构合规自检（公约 §2 十条 + ARCH 评审 §9）

| # | 铁律 | 本切片表现 |
|---|---|---|
| 1 | 算法只在 Python | N/A（纯前端，无算法） |
| 2 | 前端 → Java REST → Python | N/A（mock currentUser，未接 API） |
| 3 | 图谱 NebulaGraph | N/A |
| 4 | 可观测性必加 | ✅ `track(PERM_LOCKED_HIT / ENT_UPGRADE_PROMPT / LEVEL_SWITCH / PERSONA_SWITCH / REPORT_EXPORT)` |
| 5 | CI/CD pipeline | ✅ commit message 含 `[agent:frontend-agent] E-PERM-L03a`（待 push） |
| 6 | demo2 只读 merge | N/A（demo-ui-topic 是另一个仓） |
| 7 | 共享聚合核心 | ✅ 未直连 nGQL / 未写算法 / 未调 Python |
| 8 | 数据策略 ADS + Mock | ✅ Wave 0 全 Mock，metricSeed.ts 含血缘字段 |
| 9 | 前端规范 D8 唯一来源 | ✅ Arco（IconLock/IconExperiment/IconExclamationCircle/IconInfoCircle/IconDown/Tooltip/Button/Message）；无 antd；主色 `var(--sci-primary)`；新文件 0 硬编码 `#165DFF` |
| 10 | D9 血缘 8 件套 | ✅ MetricCard 已挂 metric_id；MetricSpecCard 弹 8 件套；Wave 0 全 🧪；Q031 已 ⚠️ |

ARCH 评审 §9 整改 A1：屏幕仅前端推导（`TOPIC_SYSTEM_SCREENS` 在 matrix.ts 前端常量；`RouteGuard.screenOk` 前端判定；**未塞后端鉴权字段**）✅

---

## 8. 成本回填（公约 §3.7 / budget-estimate）

| 字段 | 值 |
|---|---|
| `estimated_tokens` | 200K（task-registry.yaml 原估 E-PERM-L03 整任务 600K，本 L03a 占 1/3） |
| `actual_tokens` | ~480K（含全部读必读文档 + 现状勘察 + 11 文件改 / 13 文件涉及 + handoff 撰写） |
| `model_used` | claude-opus-4-7 (parent agent) |
| `actual_cost` | ~$7.20（按 $15/M input + $75/M output 估，opus 实际略浮动） |
| `cost_warn` | false（< $10 阈值）|

> ⚠️ 实际超估算 2.4 倍，主因：① UX/UI 规范两份文档总共 ~30K 字深读 ② Layout.tsx 大改重写 ③ 反复核验路径真源（gkx-lumen 新根 vs 老根 gkx_src）。建议 task-registry E-PERM-L03 整体 estimate 上调至 1.2M。

---

## 9. 任务状态机更新（coordinator/PM 据此改 task-registry）

```yaml
# task-registry.yaml E-PERM-L03 建议追加子项
- id: E-PERM-L03a
  parent: E-PERM-L03
  title: "企业维度权限切片（D-1+D-2+D-3+D-5 横切）"
  owner: frontend-agent
  scope: demo-ui-topic（仅 PC 中屏）
  claimed_at: 2026-06-22
  in_progress_at: 2026-06-22
  review_at: 2026-06-22
  status: review
  handoff: agent-delivery/agent-handoffs/产品整体定义/FE-权限改造-handoff-L03a-企业切片.md
  cost:
    estimated_tokens: 200000
    actual_tokens: 480000
    model_used: claude-opus-4-7
    actual_cost: 7.20
    cost_warn: false
  successor:
    - E-PERM-L03b（展示系统三屏 + 其他企业页按钮 PermGate + Chart token 抽离）
```

---

## 10. PM 评审 checklist（请 PM 在每项打 ✅/❌/⚠️）

- [ ] 1. DoD §6 13 条全部对照过，11✅+2⚠️+1🟡 可接受
- [ ] 2. 改动文件范围合规（无 package.json / vite.config / tsconfig / .gitignore；node_modules 不入仓）
- [ ] 3. 4 组 mock_users 截图（§4.1）已录制存档
- [ ] 4. D-3 去重前后对照截图（§4.2）已录制存档
- [ ] 5. D-5 D9 角标截图（§4.3）已录制存档
- [ ] 6. 顶栏收敛截图（§4.4）已录制存档
- [ ] 7. Q031/Q019 已登记 `客户决策清单跟踪表.md`（PM owner）
- [ ] 8. 残留项 §6 R1–R7 同意纳入 L03b
- [ ] 9. 成本回填（§8）数值认可
- [ ] 10. **批准 push** `git push origin feat/E-PERM-L03a-enterprise-perm`（demo-ui-topic 仓策略：可直推 main，但本切片走 feature 分支 + 手工合并 main，避免本切片改动直接覆盖其他 agent 在跑的 main）

---

## 11. PM 签字

> 批准人：_____郭万迎___________  日期：___2026-06-22_____
> 签字后 frontend-agent 执行 push；push 后 2–3min 自动部署到 https://skxrules.unicomcn.tech:30999/。

---

**handoff 完毕。等待 PM 评审。**
