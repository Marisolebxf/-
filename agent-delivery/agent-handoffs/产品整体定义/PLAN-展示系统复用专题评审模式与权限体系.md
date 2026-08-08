# 展示系统复用专题「评审模式 + 权限体系」实施计划

> **状态**：draft · 待 PM/架构师确认后派单  
> **日期**：2026-08-08（修订：补齐权限/评审文档真源表）  
> **Owner 建议**：frontend-agent · 监管 human:孔东（权限）/ human:高颖（政策试点评审投影）  
> **关联任务**：`E-PERM-L03b`（backlog，含 demo-ui-science 三屏权限切片）；建议拆竖切子任务挂其上或并行  
> **试点模块**：DS10-12 科技政策跟踪（`demo-ui-science`）

---

## 0. 目标与非目标

### 目标

在**科技信息展示系统**落地两套**正交**能力（各自有产品定义文档，不以专题代码为需求真源）：

1. **内部评审模式**：顶栏用户菜单开关 + 评审层自闸；关评审后评审辅助信息 **DOM 零泄漏**；不改变业务权限。  
2. **权限体系**：统一身份下 **Level（L0–L4）× Persona × Screen**；`PermGate` / `LockedButton` 非阻断降级；菜单/按钮与 `level-perms-matrix.yaml` 对齐。

展示侧相对专题的增量：**三屏 Gate**（LARGE / MEDIUM / SMALL）与 `feature_classes`（display / interact / deep / personal / manage / showcase）。

### 0.1 试点范围锁定（2026-08-08 确认）

**控制入口**：右上角用户切换  
- 现状图1：`App.jsx` `Header` + `data.js` `userRoles`（驾/析/研/政/营/治）  
- 目标图2：专题同款（Persona 列表 + 内部评审模式 Switch + 高级演示 Level）

**先只做「科技政策跟踪」**（右上角是全站壳，不能物理上只存在于政策模块，故按下列收敛）：

| 层 | 试点行为 |
| --- | --- |
| 顶栏 UI | **进入科技政策跟踪任一子页时**显示图2；离开政策模块仍显示图1，避免其它六大模块演示被打断 |
| 状态 | 图2 → `persona/level/reviewMode`（`ds_*` localStorage）；图1 → 原 `selectedRoleKey` |
| 权限锁态 | **仅** `menu:ds:policy` + ds10/11/12（及核增四页）接 PermGate |
| 评审投影 | **仅** `policy-tracking/*` 角标走 `ReviewOnly` |
| 旧角色消费 | `GlobalSituation` 等仍吃 `selectedUserRole`；政策页不再依赖旧 `policy` key |

备选（默认不采用）：全站顶栏永远图2，但非政策模块忽略 `reviewMode`/Level——换皮面更大。

#### 权限 + 评审开关铁律（2026-08-08 再确认）

**权限变动、评审开关显隐 —— 都先只影响政策模块，不整系统修改。**

| 允许 | 禁止（本迭代） |
| --- | --- |
| 侧栏「科技政策跟踪」组内菜单按 Level/Screen 锁态或裁剪 | 改写其它六大模块菜单的可见/锁态逻辑 |
| 政策 7 子页内按钮/表单（如推演参数）接 `PermGate` | 给态势/人才/图谱等页批量挂 `PermGate` |
| **仅政策页**读 `reviewMode`：角标/追溯/`ReviewOnly` 随开关显隐 | 其它模块页面挂 `ReviewOnly` 或随全局开关隐藏业务旁注 |
| 进政策时顶栏出图2（含评审 Switch）；开关状态可持久化到 `ds_review_mode` | 非政策页显示评审 Switch，或因开关改变非政策页 DOM |
| 政策页读 `persona/level` | 让 `GlobalSituation` 等旧页改为依赖新 Level 矩阵 |
| matrix 先只注册并校验 `menu:ds:policy` + ds10/11/12（+核增） | 一次性导入并启用全量 `menu:ds:*` 三屏切片 |
| 进政策时顶栏出图2（UI 壳） | 删除或全局替换 `userRoles` / 旧 `selectedRoleKey` 消费链 |

**评审开关验收（政策限定）**：

- 在政策子页：关评审 → 政策页无 `ⓘ/🧪/⚠️`、无追溯/评审容器（DOM 零泄漏）；业务图表与筛选仍在。  
- 离开政策模块：顶栏回图1（无评审 Switch）；其它模块页面外观与开关状态无关、零变化。

其它模块继续走现有 `userRoles`（图1）与原有导出/角色策略，互不影响。

### 非目标（本计划不做）

- 不替甲方拍板业务口径（QPOL / Q020–Q031 等仍 🟡）。  
- 不把专题 E7 `/policy/*` 路由或对比篮合同搬进展示。  
- 不在本阶段全面重写展示全站为 Arco（试点可「壳层 Arco 组件 + 页面 AntD 兼容」）。  
- 不在本阶段接生产 SSO / PigX perms（Wave0 mock；接口同构留给 V2）。  
- 不把 `lumen-ui-science-pc`（Vue 模板）当作 Wave0 主战场。  
- 不以专题 demo 实现反向定义产品规则；代码冲突时回写文档或登记 gap。  
- **不整系统改权限/评审**：本迭代权限锁态与评审开关显隐均仅限科技政策跟踪；其它模块零行为变化（顶栏在非政策页保持图1、无评审 Switch）。

---

## 0.5 文档真源（必读 · 禁止另造规则）

> 路径均相对 `agent-delivery/agent-handoffs/产品整体定义/`（除非另行注明）。  
> **执行顺序**：先读本节文档 → 再对照专题实现 → 最后改 `demo-ui-science`。  
> **专题代码 = 参考实现，不是需求权威。**

### A. 内部评审模式（跨模块辅助能力 · 非 bid 叶子）

| 优先级 | 文档 | 用途 |
| --- | --- | --- |
| P0 | `内部评审模式/评审模式-产品流程与状态定义.md` | 流程、三类内容边界、关闭后零泄漏、与权限正交 |
| P0 | `内部评审模式/USM-内部评审模式.md` | US-REV-01~03；全局开关挂用户菜单；业务模块必须挂评审层 |
| P0 | `内部评审模式/IA-内部评审模式.md` | 开关 / 页面级容器 / IconFile / 角标 / 全局抽屉分层 |
| P0 | `内部评审模式/Wireframe-内部评审模式.md` | Frame：默认态 / 关闭态 / 局部追溯 / 抽屉 |
| P0 | `内部评审模式/TRACE-REVIEW-内部评审模式.yaml` | 治理追溯；`review_visibility` 机器字段 |
| P1 | `../../data-lineage-policy.md` §2.3 / §5 | ⓘ / 🧪 / ⚠️ 触发与组件语义（评审模式只控显隐） |
| P1 | 业务模块自有包（试点：`DS10-12-科技政策跟踪/` UX-SPEC §9 + Wireframe `review_trace_contract`） | **只登记本页文案与落位**，不得另造显隐规则 |

**状态备注**：评审模式定义包仍为「产品定义初稿」；Wave0 可先落开关 + 模块内联角标/追溯，全局抽屉与模块复核状态若未齐则登记 `stage_block` / gap，不得伪造「已通过」正式会签语义。

### B. 权限体系（全系统 · 含展示三屏）

| 优先级 | 文档 | 用途 |
| --- | --- | --- |
| P0 | `全系统角色权限体系设计.md` | **主设计稿**；L0–L4 × Persona；展示+专题；**取代并扩展**展示单系统前序稿 |
| P0 | `level-perms-matrix.yaml` | **机器真源**：级别累加、screen、`feature_classes`、`menu:ds:*` / `btn:*` |
| P0 | `权限点清单-菜单与按钮.md` | 菜单/按钮 perm code 实现级清单 |
| P0 | `ARCH-权限体系-评审.md` | D6 合规、Wave0 mock / Wave1 网关同构、屏幕仅前端推导（整改 A1） |
| P1 | `UX-权限交互规范-企业维度.md` | 非阻断降级、`PermGate`/`LockedButton`、与评审角标交互原则（企业切片起，交互可复用） |
| P1 | `UI-权限视觉规范-企业维度.md` | 锁态视觉 token（`--perm-lock-*` 等） |
| P2 | `科技信息展示系统-角色权限体系.md` | **前序展示单系统稿**；场景/角色叙事可参考，**冲突时以全系统设计稿为准** |
| P2 | `PROD-权限体系-handoff.md` / `PROD-权限改造-派单-*.md` / `FE-权限改造-handoff-L03a-企业切片.md` / `PM-决策-E-PERM-L03a-签字单.md` | 派单、切片证据、签字闸门；**不创造新业务口径** |
| P2 | `PROD-原型核对-权限规划对照.md` | 原型与规划对照（历史核对） |

**判定式（摘自设计稿 / ARCH / matrix，实现必须遵守）**：

```text
最终可用 = Level(L0–L4 累加命中 minLevel)
         ∧ Screen(feature_classes[class][screen] ≠ false；菜单另看 screens)
         ∧ 密级/L4 子角色命中
Persona  = 仅默认视图 + 数据范围（不增减 perm，L4 子角色除外）
评审模式 = 仅评审辅助信息显隐（不进入上式）
```

**展示系统特有（matrix 已写）**：

- `system_screen_scope.display_system = [LARGE, MEDIUM, SMALL]`  
- 政策试点叶子示例：`menu:ds:ds10` L0 三屏；`ds11` L1 三屏；`ds12` L2 **仅 MEDIUM**（deep）

### C. 参考实现（非真源）

| 仓 / 路径 | 用途 |
| --- | --- |
| `repos/demo-ui-topic/src/app/perms/*` | PermGate / matrix / CurrentUserProvider 参考 |
| `repos/demo-ui-topic/src/app/components/common/{ReviewOnly,MockBadge,PendingBadge,MetricSpecCard,PersonaLevelSwitcher,ReviewTrace}.tsx` | 评审壳与角标参考 |
| 专题 E7 `policy-portal` ReviewMount | 业务页挂载样板（路由/合同不可照搬） |

冲突处理：文档 ↔ 专题代码不一致 → **停手登记 gap**，回写定义或经 PM/架构师批准后再改实现；禁止用代码静默覆盖文档。

---

## 1. 现状差距（一句话）

| 能力 | 文档要求 | 专题 `demo-ui-topic` | 展示 `demo-ui-science` |
| --- | --- | --- | --- |
| 评审开关 | 用户菜单；内部默认开 | 已有 | **无**（政策角标常驻） |
| 评审门控 | 关闭 DOM 零泄漏 | `ReviewOnly` | **无** |
| D9 / 追溯 | 仅评审态；语义见 data-lineage | Arco 共享组件 | 本地 AntD 拷贝 |
| 权限内核 | L0–L4 × matrix | `usePerms` / `PermGate` | **无** |
| 三屏 | 展示必有；专题仅 MEDIUM | 恒 MEDIUM | 矩阵已写、**FE 未接** |
| 正式仓 | D6 网关同构 | 规划对齐 demo | Vue `v-permission` 壳 |

---

## 2. 架构原则

```text
顶栏: Persona/Level 切换  +  评审模式 Switch（二者正交）
        │
        v
CurrentUserProvider
  - reviewMode ----------> ReviewOnly / 角标自闸（显示层）
  - level+persona+screen -> usePerms / PermGate（权限层）
        │
        v
页面业务宿主 + Wireframe review_mounts
```

1. **评审 ⊥ 权限**：关评审不升/降业务权限；改 Level 不自动开评审。  
2. **接口同构**：展示仓组件 API 与专题保持同名同语义（便于后续抽包或双向同步）。  
3. **先壳后页**：未挂全局 Provider + 顶栏开关前，禁止宣称「评审模式已复用」。  
4. **Wave0 mock**：用户/矩阵本地；`localStorage` 键建议 `ds_mock_user` / `ds_review_mode`（与专题 `ent_*` 隔离，避免两仓同域串态）。  
5. **三屏为展示增量**：`CURRENT_SCREEN` 可切换（演示）；`ds12` 等仅 MEDIUM 的叶子在 LARGE/SMALL 上锁态或隐藏（按矩阵 + UX-SPEC）。  
6. **挂点等式**：`defined == coverage == rendered_review_mounts`；`business_mode` 下评审节点 count = 0。

### 复用策略（选型）

| 方案 | 做法 | 建议 |
| --- | --- | --- |
| A. 仓内拷贝对齐 | 把 perms/review 目录拷入 `demo-ui-science/src/app/`，改 storage key + screen | **Wave0 采用**（最快、与 L03b 一致） |
| B. 抽 monorepo 包 | `@gkxlumen/review-perms` | V2 再议；现无 workspace 包 |
| C. 运行时跨仓引用 | 禁止 | 破坏仓边界 |

**视觉**：新壳层组件用 **Arco**（权威栈）；试点页宿主可暂留 AntD，角标替换为 Arco 评审组件，避免再扩 emoji Tag。

---

## 3. 分期与任务分解

### Phase 0 · 决策闸门（0.5d · 人）

- [ ] **D0** 开工前确认 §0.5 两套文档已读：评审模式五件套 + 权限（全系统设计 / matrix / ARCH）；与 `科技信息展示系统-角色权限体系.md` 冲突处以全系统设计为准。  
- [ ] **D1** 确认本计划挂靠 `E-PERM-L03b` 还是新建 `DS-REVIEW-PERM-L01` 竖切（推荐：L03b 下拆叶子，政策试点先做）。  
- [ ] **D2** 确认 storage key 隔离（`ds_*`）与默认 `reviewMode`（对齐评审模式定义：**内部默认 true**；业务验收须显式关）。  
- [ ] **D3** 确认三屏演示入口：顶栏 Screen 切换 vs 仅 URL/环境（建议顶栏；screen 仅前端推导，见 ARCH A1）。  
- [ ] **D4** `E-PERM-L03a` 签字单 §D3 R4（展示三屏）是否已放行；未放行则本计划只做**评审壳 + 政策页投影**，权限三屏标 `stage_block`。

### Phase 1 · 壳层复用（demo-ui-science · 2–3d）

**Files（建议新建）**

- `src/app/perms/{types,matrix,usePerms,PermGate,LockedButton,routeGuard,CurrentUserProvider}.tsx`  
- `src/app/components/common/{ReviewOnly,MockBadge,PendingBadge,MetricSpecCard,ReviewTrace,PersonaLevelSwitcher}.tsx`  
- 改：壳层 Layout / Header（`App.jsx` 或等价）挂 Provider + 顶栏开关  

**Steps**

- [ ] 以 §0.5-B 判定式 + `level-perms-matrix.yaml` 生成展示侧 `matrix.ts`（勿只抄专题 MEDIUM 常量）。  
- [ ] 对照 §0.5-A 与专题参考实现接入 `reviewMode`；开关落在**用户菜单**（USM），关闭后页面无残留入口。  
- [ ] `CURRENT_SCREEN` 可切换（默认 MEDIUM）；先挂 `menu:ds:policy` + `ds10/11/12`（核增 PC 无独立 code 则父码 + deep 锁，缺口回写清单）。  
- [ ] 顶栏：Persona/Level（演示覆盖须标「权限边界演示」）+ 评审 Switch + Screen。  
- [ ] 冒烟：关评审后无评审 DOM；无权限 → `LockedButton` 非整页 403；L0+LARGE 下 `ds12` 不可用。

**DoD**

- 任意空白页可演示：开关评审、切换 L0/L2、切换 LARGE/MEDIUM。  
- handoff 附截图/简短证据。

### Phase 2 · 政策试点 DS10-12（2–3d）

**Files**

- 删/替：`src/pages/policy-tracking/components/{MockBadge,PendingBadge,MetricSpecTrigger}.jsx` → 改用共享组件  
- 改：`PolicyPanorama|Analysis|Simulation|PcPages.jsx`  
- 增：`PolicyReviewMount.tsx`（mount_id ↔ 共享组件映射，对照 UX-SPEC §9 / Wireframe `review_trace_contract`）  
- 增：`mocks/policy-gap-catalog`（Pending 文案，对齐专题 gap catalog 形态）  
- 更新：`交付覆盖/DS10-12-科技政策跟踪/` coverage + evidence  

**Steps**

- [ ] 所有 KPI/角标外包 `ReviewOnly`；业务态零泄漏验收。  
- [ ] 补需求追溯条（分轨说明可挂 `ReviewTrace`）。  
- [ ] 权限竖切：  
  - `ds10` L0 可见  
  - `ds11` 需 L1（菜单锁态）  
  - `ds12` 需 L2 且仅 MEDIUM；LARGE/SMALL 禁用或隐藏  
  - 推演表单：无权限 → 只读结果（UX-SPEC）  
- [ ] 核增 PC 页：深度操作对齐 `deep` feature_class（L2+/MEDIUM）。  
- [ ] 跑 composite-label checker；更新 validation-report。

**DoD**

- J-DS-PC / 三主屏在「开评审 + L2 + MEDIUM」可完整演示。  
- 「关评审 + L0 + LARGE」：无评审 DOM；推演入口锁/隐；全景可浏览。

### Phase 3 · 推广模板（1–2d · 文档+样板）

- [ ] 写 `展示系统-评审与权限接入指南.md`（怎么给新模块加 ReviewMount / PermGate）。  
- [ ] 从政策试点抽「最小挂载清单」模板，供态势/人才等模块复制。  
- [ ] 与 `E-PERM-L03b` 其余范围（topic 残留、R1–R3）排期对齐，避免双开冲突。

### Phase 4 · V2 lumen（后续 · 不阻塞 Wave0）

- [ ] 明确 `lumen-ui-science-pc` 是否跟专题一样「以 demo 为真源」重做 React+Arco；若维持 Vue，则只做接口同构适配层。  
- [ ] perms 源切网关/SSO；metric catalog 切 `gkxlumen-metrics`。  
- [ ] 评审偏好是否升账户级（产品未决则继续 localStorage）。

---

## 4. 建议任务拆单（registry）

| 建议 ID | 标题 | 依赖 | 仓 |
| --- | --- | --- | --- |
| `DS-REVIEW-PERM-L00` | 展示壳层：评审模式 + Perm 内核拷贝对齐（含三屏状态） | L03a 放行或 D4 豁免评审-only | demo-ui-science |
| `DS-REVIEW-PERM-L01` | DS10-12 评审投影 + 角标替换 + 零泄漏验收 | L00 | demo-ui-science |
| `DS-REVIEW-PERM-L02` | DS10-12 权限/三屏竖切（矩阵 ds10/11/12） | L00；对齐 E-PERM-L03b R4 | demo-ui-science |
| `E-PERM-L03b` | 保持母单；L00–L02 完成后回填 R4 证据 | L03a §D3 | science + topic |

> 建单须走 MCP `task-create` + PM 确认；本文件不直接改 registry。

---

## 5. 验收清单（跨 Phase）

| # | 检查项 | 通过标准 |
| --- | --- | --- |
| 1 | 评审开关 | 顶栏可切换；刷新后 localStorage 保持 |
| 2 | 零泄漏 | `reviewMode=false` 时无 `data-review-mount-id` / 无 MetricSpec 触发器 |
| 3 | 正交性 | 关评审后锁态菜单/按钮仍按 Level 显示 |
| 4 | D9 | 开评审时 KPI 有 ⓘ + 🧪；QPOL 有 ⚠️ |
| 5 | 权限降级 | 无权限 → LockedButton + 原因 Tooltip，非整页 403 |
| 6 | 三屏 | MEDIUM 最全；LARGE 推演不可用；SMALL 按矩阵裁剪 |
| 7 | 分轨 | 政策页仍声明展示/专题分轨，不写 E7 篮 |
| 8 | 文档 | coverage / handoff / validation-report 已更新 |

---

## 6. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| AntD 页嵌 Arco 角标样式漂移 | 角标独立样式作用域；对照 Design.md §7.4；不强制本迭代整页 Arco |
| 与 E-PERM-L03b 双开 | 计划挂靠 L03b；政策竖切先做，其余域后铺 |
| 默认开评审导致业务态误验 | 验收用例强制「关评审」一组 |
| 矩阵缺核增 PC perm 码 | 先挂父级 `menu:ds:policy` + 页内 deep 锁；缺口回写 matrix（人批） |
| lumen Vue 分叉 | Wave0 只认 demo-ui-science；V2 单独决策 |

---

## 7. 建议立即决策（只需选一项）

**本迭代范围选哪条？**

1. **评审壳 + DS10-12 投影**（不依赖 L03b 签字；权限三屏后置）  
2. **评审壳 + 权限/三屏 + DS10-12 全竖切**（需 L03a §D3 / L03b 放行）  
3. **仅出本计划，先开会对齐 D1–D4 再派单**

确认后即可按 Phase 1 开工或走 `task-create` 拆单。
