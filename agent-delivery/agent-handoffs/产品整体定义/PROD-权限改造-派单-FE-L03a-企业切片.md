# 权限改造 · FE-L03a 企业维度切片 · 派单话术

> **状态**：🟢 可启动（上游 L00 ✅ done / L01·L02 企业切片 ✅ 已交付，commit 未 push 但产物在编排资产内可读）
> **作者**：调度者 + AI（基于 `PROD-权限改造-派单-5角色.md` §派单话术 3 切片化适配）
> **创建**：2026-06-22
> **任务 ID（建议挂载）**：`E-PERM-L03a`（task-registry 现有 `E-PERM-L03` 切片为 a 企业维度 + b 展示三屏）

## 0. 为什么要切片？

| 上游任务 | 标称状态 | 实际产物 | 缺口 |
|---|---|---|---|
| E-PERM-L00 架构评审 | ✅ done | `ARCH-权限体系-评审.md` | 完整 |
| E-PERM-L01 UX 交互规范 | 🟡 in_progress | `UX-权限交互规范-企业维度.md`（commit 62bd342，未 push） | **仅企业维度切片**，展示系统三屏未做 |
| E-PERM-L02 UI 视觉规范 | 🟡 in_progress | `UI-权限视觉规范-企业维度.md`（commit 4c2a914，未 push） | 同上，仅企业维度切片 |

UX/UI 已经把"**企业维度**"完整切出来交付，且 D-3 去重决策（方案 B 独立页权威）已做出。FE 没有理由等三屏部分，可立即启动 **L03a 企业维度切片**：仅改 `demo-ui-topic` 仓，落实 D-3 去重 + 权限内核 + D9 角标。展示系统 `demo-ui-science` 三屏改造留给后续 **L03b**。

## 1. 切片范围（与全量 L03 的差异）

| 项 | 全量 L03（原版话术 3） | 本切片 L03a |
|---|---|---|
| 涉及仓 | `demo-ui-science` + `demo-ui-topic` | **仅 `demo-ui-topic`** |
| D-1 角色收敛 | 两仓全做 | 仅 `demo-ui-topic` |
| D-2 级别×屏幕 Gate | 展示三屏 + 专题中屏 | **仅专题中屏**（`system_screen_scope.topic_system=[MEDIUM]`），不实现三屏过滤 |
| D-3 企业 E-21/E-22 去重 | ✅ | ✅（核心交付） |
| D-5 D9 血缘角标 | 两仓全做 | 仅 `demo-ui-topic` 企业域 |
| Push 纪律 | science 可推 main / topic 待 PM | **仅 topic 一仓，push 前必须 PM 确认** |

## 2. 上游产物索引（agent 必读，目录均为 `agent-delivery/agent-handoffs/产品整体定义/`）

- `ARCH-权限体系-评审.md` §9 给 FE 的架构约束清单（matrix 派生、非阻断 Gate、Wave0 脱敏标 🧪、demo→lumen 走 PR）
- `UX-权限交互规范-企业维度.md` §1.5 概览去重布局 / §2.2 切换器 / §3.3 降级态 / §4 角标 / §5 字段表（含 metric_id）/ §6 待评审 Q031·Q032 / **§7.3 FE 接力建议**
- `UI-权限视觉规范-企业维度.md` §1 token / §2 切换器 / §3 身份徽标 / §4 降级 / §5 角标 / §6 菜单锁态 / §7 权重只读 / §8 概览去重布局 / §9 §14 对照 / **§10.2 组件名/className/token 表**
- `level-perms-matrix.yaml`：levels / personas / l4_subroles / screen_types / `system_screen_scope` / `feature_classes` / mock_users / demo_mapping / permissions[]
- `权限点清单-菜单与按钮.md`（菜单/按钮权限点真源）
- `data-lineage-policy.md` §5（MetricSpecCard / DataLineageDrawer / MockBadge）
- `Design.md`（D8 全文，§4 色彩 / §7 组件 / §13 实现映射 / §14 检查清单）
- 仓内：`demo-ui-topic/AGENTS.md`、`demo-ui-topic/CLAUDE.md`（实际技术栈与 observability）

## 3. ====== 派单话术：FE L03a 企业维度切片 ======（复制到新 Cursor 会话）

```
/goal frontend-agent

## 身份
你是 frontend-agent —— 资深前端工程师（React + Vite + Arco）。本切片只做 demo-ui-topic 仓 · 仅 PC 中屏（专题恒 MEDIUM，不实现三屏过滤）。严守团队公约（00-team-constitution.mdc）+ Design.md（D8）+ data-lineage-policy.md（D9）+ ARCH 评审 §9 架构约束。不改业务口径、不动数据真值、不重设计企业业务页本身。

## 任务（E-PERM-L03a 企业维度切片，对接 UX/UI 企业切片）
落实 D-1（角色收敛）/ D-2（级别 Gate）/ D-3（E-21/E-22 去重，核心）/ D-5（D9 角标），改造范围：仅 demo-ui-topic / 仅企业要素相关页面与全局壳。

### 3.1 权限内核（demo-ui-topic 全仓共用，企业切片优先用）
- 从 level-perms-matrix.yaml 派生 level→perms 映射（生成 TS 常量；脚本或一次性手转都行，但必须有"再生成"路径，不准散落硬编码）。
- 实现 usePerms() Hook + <PermGate perm="..." /> 组件：命中渲染、未命中按 UI §4 降级（disabled+🔒+Tooltip+升级/登录/申请引导），并埋点 user_level + perm_code（用仓内 observability）。
- 路由守卫：路由 meta { minLevel, perms, screens:[MEDIUM] }，按当前 currentUser.level + 固定 screen=MEDIUM 过滤。
- 屏幕规则：专题 system_screen_scope.topic_system=[MEDIUM]，本仓恒 MEDIUM；feature_classes[showcase]=false 在专题不渲染（不用做大屏酷炫态）。
- mock currentUser={level,persona,subroles}：Wave0 本地，对照 yaml mock_users + demo_mapping，把现状三套（顶栏 userRoles 驾/析/研/政/运/数 + 页面 U/S 级别 + 当前角色 S2）收敛掉。

### 3.2 D-1 角色收敛 + 顶栏控件（按 UX §2.2 + UI §2/§3）
- 顶栏改为「PermLevelSwitcher（级别切换器 L0–L4）+ PersonaTag（身份徽标 GOV / INNO·THINK / VISIT）」，移除/收敛现状三套控件。
- 切换器视觉：Segmented（Arco），高 32px，配色阶 L0 灰 / L1-L2 主色阶 / L3 强调 / L4 管理色，token 用 UI §1.2 --perm-level-l0..l4。
- 身份徽标：Tag + Dropdown，GOV 默认 dashboard / INNO·THINK 默认 workbench / VISIT 默认 readonly（仅决定默认视图与数据范围，不增减 perm）。

### 3.3 D-2 级别×屏幕 Gate（落到企业域菜单 + 按钮）
- 菜单：menu:ent:type / menu:ent:domain / menu:ent:supply / menu:ent:painpoint / menu:ent:compete 等按 matrix.permissions[] 挂 meta.minLevel + meta.perms + meta.screens:[MEDIUM]。
- 按钮：按 权限点清单-菜单与按钮.md §2.1/§3 接 <PermGate code="btn:..." />；如 btn:common:export-list（导出名单）需 L3 + 审计、btn:common:simulate（断链推演）需 L3 等。
- 越权一律非阻断（disabled+🔒+引导按钮），不整页 403。

### 3.4 D-3 企业 E-21/E-22 去重（UX §1 推荐方案 B：独立页权威，核心改动）
现状（只读核对 demo-ui-topic）：
- ① 概览页 menu:ent:dash /enterprise/overview（activeTab=situation）= 态势总览（保留）
- ② 概览页 activeTab=structure 二级 analysis-tabs（企业全景 / 类型分布概览 / 领域分布概览）= 与 ③ 重叠（删除）
- ③ 独立页 menu:ent:type /enterprise/type-distribution（E-21）+ menu:ent:domain /enterprise/domain-distribution（E-22）= 唯一权威（保留）

落地（按 UX §1.5 + UI §8）：
1. 删除 EnterpriseOverview.tsx 的 structure tab + analysis-tabs 整组（包含"企业全景 / 类型概览 / 领域概览"三个子 tab 内容）。
2. 保留"决策链下钻入口"按钮组：[→ 类型分析 P1/E-21] [→ 领域分布 P2/E-22] [→ 深圳现状 P5/E-25] [→ 引育推荐 P6] [→ 综合竞争力 P10/E-30(L3 强调)]。
3. 路由保留 /enterprise/analysis → /enterprise/overview 的 301/重定向，避免老链接 404。
4. "企业全景"归门户 E-33（menu:ent:keypano，/development/key-enterprises），不在分析层重复。
5. 概览 L1 / L2 视觉差异按 UI §8.2 实现：L1 仅 JudgmentStrip 结论条 + 检索入口；MetricCard / 趋势图 / 全国分布 / TopN / 视图切换 等按目标页 minLevel 显示锁态（Q031 临时默认，加 ⚠️"待甲方确认"角标）。

### 3.5 D-5 D9 血缘角标（按 UI §5 + data-lineage-policy.md §5）
- 每统计数字（M_ENT_*）旁 ⓘ → MetricSpecCard（读 metricSeed.ts；Wave1 切 /metrics/v1/catalog）。**不准删 ⓘ**。
- Mock 数据 🧪 MockBadge（按 metricSeed.ts.is_mock）。
- 口径未定 ⚠️ PendingBadge（按 metricSeed.ts.pending_ref，对应 Q010~Q032）。
- 角标 emoji 仅作语义锚点，FE 实际渲染必须用 Arco Icon（D8 §12.3 + UI §4.5）：
  - ⓘ → IconInfoCircle
  - 🧪 → IconExperiment
  - ⚠️ → IconExclamationCircle
  - 🔒 → IconLock
- 全量 metric_id 见 UX §5.10（共 29 个，含 1 个 ❌ 无源 M_ENT_MARKET_SHARE，做 ❌ 占位即可）。

### 3.6 组件命名 + token（严格按 UI §10.2 接力表）
PermLevelSwitcher / PersonaTag / PermGate / LockedButton / MaskedField / WeightReadonly / MetricInfoIcon / MockBadge / PendingBadge / MetricSpecCard / DataLineageDrawer / SidebarMenu(.is-locked) / EnterpriseOverviewDash —— className 走 .perm-* / .sci-* / .arco-*，颜色全部走 §1 CSS 变量（--sci-primary / --perm-level-l0..l4 / --perm-lock-* / --perm-mock / --perm-pending / --lineage-* 等），**禁页面内硬编码主色 #165DFF**。

## 4. 仓库（cwd）
- ${GKX_ROOT}/repos/demo-ui-topic（专题系统 / 企业 / 仅 PC + E-21/22 去重）
- 工作根从 gkx-orchestration/.env GKX_ROOT 解析（00-path-resolution.mdc）

## 5. 硬约束（违反必拒）
1. 不改业务口径 / 不删功能点 / 不新增功能点（权限是横切，不计 58 点 ±10%）。
2. 不改 package.json / vite.config / tsconfig / .gitignore（除非任务必需且 PM 批）。
3. Gate 用 React Hook/组件，禁 Vue 指令。
4. level→perms 必须由 yaml 派生，禁手抄硬编码散落各文件。
5. 屏幕维度仅前端推导（ARCH §6.1.3 + 整改 A1），禁塞后端鉴权。专题恒 MEDIUM，不渲染 showcase 类。
6. 大屏酷炫态严禁出现（D8 §0 + ARCH §6.1.3）。
7. 所有 emoji 角标实际渲染必须用 Arco Icon（D8 §12.3）；非 Arco 组件库禁用（禁 antd 类名 .ant- / .vendor-antd）。
8. 顶栏三套并存现状（驾析研政运数 + U/S 级别 + S2 当前角色）必须收敛为「级别切换器 + 身份徽标」单一控件组。
9. ⓘ 角标禁删；Wave0 数据带 🧪；Q020~Q032 未决加 ⚠️。
10. demo→lumen 走 PR 非直搬（本切片不动 lumen-ui-topic）。
11. **commit 必须含 [agent:frontend-agent] + 任务 ID（E-PERM-L03a）**；**push 前必须取得 PM 确认**（demo-ui-topic 仓策略，公约 §4.2）。

## 6. DoD（自检表）
| # | 检查项 | 通过条件 |
|---|---|---|
| 1 | 权限内核 | usePerms + <PermGate> + 路由 meta 落地；level→perms 由 matrix yaml 派生（含再生成路径） |
| 2 | 顶栏收敛 | 三套并存消除；PermLevelSwitcher + PersonaTag 单控件组上线 |
| 3 | 企业菜单 Gate | menu:ent:* 按 matrix 挂 meta.minLevel/perms/screens；越权 disabled+🔒+引导 |
| 4 | 企业按钮 Gate | 权限点清单覆盖按钮接 <PermGate>；导出/推演 L3 锁态正确 |
| 5 | E-21/E-22 去重 | 概览 structure tab + analysis-tabs 删除；独立页权威；老链接重定向 OK；门户 E-33 一处 |
| 6 | D9 角标 | 每 M_ENT_* 接 ⓘ + 🧪/⚠️（按 metricSeed.ts）；emoji 全替为 Arco Icon |
| 7 | 概览 L1/L2 视觉差 | JudgmentStrip / MetricCard / TopN / 视图切换 等按 UI §8.2 表格落实；L1 ⚠️ 角标 |
| 8 | 屏幕约束 | 全仓 screens:[MEDIUM]；showcase 类不渲染；大屏酷炫零出现 |
| 9 | Design.md §14 | 14 条逐条对照（参考 UI §9）：浅蓝白工作台 / 64px Header / 200px Sidebar / 32px 控件 / #165DFF 主色 / 无 antd |
| 10 | 自测覆盖 | mock_users 切 L0/L1/L2/L3/L4 + GOV/INNO/VISIT，菜单按钮按矩阵增减正确 + 截图存档 |
| 11 | observability | 切级别 / 越权 / 角标命中 / 导出配额 等关键节点埋点（user_level、perm_code、target_page） |
| 12 | 范围与代码卫生 | 不改业务口径 / 不删功能点 / 不改配置文件 / 主色无硬编码 |
| 13 | Push 纪律 | commit 含 [agent:frontend-agent] + E-PERM-L03a；**push 前 PM 确认**；禁 force |

## 7. Handoff（必交付）
- 写到：agent-delivery/agent-handoffs/产品整体定义/FE-权限改造-handoff-L03a-企业切片.md
- 内容：
  1. DoD §6 逐条对照 ✅/❌
  2. 改动文件清单（含路径 + commit hash 摘要）
  3. 截图：mock_users 至少 4 组（L0 GUEST / L1 INNO / L2 INNO / L3 GOV）×（概览页 + 类型分析 + 领域分布 + 供应链 + 综合竞争力）的菜单/按钮/角标态
  4. E-21/E-22 去重前后对照截图（structure tab 删除验证 + 独立页保留 + 老链接重定向）
  5. ⓘ MetricSpecCard 弹出截图（带 8 件套：metric_id / 中文名 / 口径 / 公式 / 源表 / 源系统 / 更新频率 / 版本）
  6. 残留项 / 待 L03b 接续的事项（展示系统三屏部分，不在本切片）
  7. 成本回填：estimated_tokens / actual_tokens / model_used / actual_cost / cost_warn（公约 §3.7）
  8. 任务状态机更新：claimed_at → in_progress → review（task-registry.yaml E-PERM-L03 状态由 coordinator/PM 据此调整或追加 L03a 子项）

## 8. 起步动作
1. 读：00-team-constitution.mdc / 00-path-resolution.mdc / Design.md / data-lineage-policy.md / ARCH-权限体系-评审.md §9 / UX-权限交互规范-企业维度.md（重点 §1.5 §2.2 §3.3 §4 §7.3）/ UI-权限视觉规范-企业维度.md（重点 §1 §2 §4 §5 §8 §10.2）/ level-perms-matrix.yaml / 权限点清单-菜单与按钮.md / demo-ui-topic/AGENTS.md
2. 现状只读核对：EnterpriseOverview.tsx + routes.tsx + 现有顶栏组件 + metricSeed.ts，列出待删/待改文件清单（先列再动）
3. 建分支：feat/E-PERM-L03a-enterprise-perm（从 main 起，参照公约 §4.2 demo-ui-topic 策略）
4. 按 §3 顺序实施 → §6 DoD 自检 → §7 handoff → 等 PM 给 push 许可

## 9. 中文产出，开始执行。

## ====== 派单话术结束 ======
```

## 4. 与原版 §派单话术 3 的关系

- 本切片话术**不替换**原版 `PROD-权限改造-派单-5角色.md` §派单话术 3。
- 待 UX/UI 完成展示系统三屏（D-1/D-2/D-5 在 demo-ui-science 上的实施）后，可基于原版话术派 **L03b**：仅做 `demo-ui-science` 三屏 Gate + 角色收敛 + 角标，跳过 L03a 已完成的内核逻辑（usePerms/PermGate/路由 meta 可直接复用模式）。

## 5. PM 确认与状态更新建议

- **task-registry.yaml** 现 `E-PERM-L03` status=pending；建议 PM 启动时：
  - 在 `E-PERM-L03` `note` 增补 `"切片为 L03a（企业，本任务）+ L03b（展示三屏，待 L01/L02 三屏补齐）"`
  - 或新增子任务 `E-PERM-L03a` / `E-PERM-L03b`，依赖关系：L03a 仅依赖 L01/L02 的企业切片产物；L03b 依赖 L01/L02 全量交付。
- 接力守门：FE 完成 §6 DoD 自检 + §7 handoff 后，PM/coordinator 验收 + push 许可 → 任务 done → coordinator-agent 同步 task-registry。

---

**本派单话术状态**：🟢 可立即复制到 Cursor 新会话启动 frontend-agent。
