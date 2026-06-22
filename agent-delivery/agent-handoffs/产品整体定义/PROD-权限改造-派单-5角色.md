# 权限体系落地改造 · 派单（5 角色：架构师 / UX / UI / Frontend / PM）

> **状态**：🟡 待 PM 启动（当前 `coordinator_halt` 生效，2026-06-20 用户停所有任务）
> **作者**：产品经理（人主导，AI 辅助）
> **创建**：2026-06-22
> **调度登记**：Epic `E-PERM-M1`（`task-registry.yaml` + `dispatch-queue.yaml`），5 任务 `E-PERM-L00~L04`
> **缘起**：`PROD-原型核对-权限规划对照.md` 实地核对发现 5 项差异 D-1~D-5，需 架构师评审 → UX→UI→Frontend 接力改造，PM 全程跟踪，把权限规划落到两个原型。
> **接力链**：架构师评审(L00) → UX 交互(L01) → UI 视觉(L02) → FE 实现(L03)；PM 跟踪(L04) 全程并行。
> **基线文档（三角色共同必读，均在本目录 `agent-delivery/agent-handoffs/产品整体定义/`）**：
> - `全系统角色权限体系设计.md`（级别 L0–L4 × 身份 + 屏幕 §8.5）
> - `权限点清单-菜单与按钮.md`（菜单/按钮/屏幕 feature_class）
> - `level-perms-matrix.yaml`（机器可读：level→perms / screens / 密级 / demo 映射）
> - `PROD-原型核对-权限规划对照.md`（差异 D-1~D-5）
> - `agent-delivery/Design.md`（D8 UI 权威）、`agent-delivery/data-lineage-policy.md`（D9 血缘）
> **两个原型仓**：
> - 展示系统 `demo-ui-science`（多屏；main 直推允许）→ https://skxrules.unicomcn.tech:30999/
> - 专题系统 `demo-ui-topic`（仅 PC；含企业）→ https://skxdemo.unicomcn.tech:30999/

## 差异 → 角色分工总览

| 差异 | 说明 | 架构师 | UX | UI | FE | PM |
|---|---|:--:|:--:|:--:|:--:|:--:|
| D-1 | 角色三套并存，未收敛 L0–L4 | 鉴权/SSO 方案 | ✅设计 | ✅视觉 | ✅实现 | 跟踪 |
| D-2 | 级别×屏幕 Gate 未落地 | 权限服务/网关 | ✅交互 | ✅锁态视觉 | ✅实现 | 跟踪 |
| D-3 | 企业 E-21/E-22 重复 | — | ✅IA 决策 | — | ✅实现 | 跟踪 |
| D-4 | DS-30 已拆 5 页 | — | 已同步 | — | 无需改 | — |
| D-5 | D9 血缘角标缺失 | 元数据下发 | ✅交互 | ✅角标/卡 | ✅接入 | 跟踪 |
| 全局 | 口径 Q020~Q030 待甲方 | 评审影响 | 标 ⚠️ | — | mock | ✅推进甲方 |

**接力顺序**：架构师评审(L00) → UX(L01) → UI(L02) → FE(L03)；PM(L04) 全程并行跟踪 + 推甲方口径。

## 调度任务映射（`task-registry.yaml` Epic E-PERM-M1）

| 任务 | 角色 | 依赖 | 仓 | 产物 |
|---|---|---|---|---|
| E-PERM-L00 | architect-agent | — | orchestration | 架构评审意见（D6/SSO/统一权限服务实现路径） |
| E-PERM-L01 | ux-agent | L00 | orchestration docs | UX-权限交互规范.md |
| E-PERM-L02 | ui-agent | L01 | orchestration docs | UI-权限视觉规范.md |
| E-PERM-L03 | frontend-agent | L02 | demo-ui-science + demo-ui-topic | FE-权限改造-handoff.md + 代码 |
| E-PERM-L04 | pm / coordinator | 全程并行 | orchestration | 进度跟踪 + Q020~Q030 甲方推进 |

---

## ====== 派单话术 0：架构师 ======（复制到新 Cursor 会话）

/goal architect-agent

## 身份
你是 **architect-agent** —— 资深架构师，负责 Epic 开工评审与架构基线合规。**不写业务代码**；产出评审意见 + 实现路径，对齐 `architecture-baseline.md`（重点 D6：鉴权/SSO/权限经网关统一）。

## 任务（E-PERM-L00，先于 UX/UI/FE）
评审"全系统权限体系"设计，回答"**如何实现**"，给下游 UX/UI/FE 与未来 lumen 正式仓一个可落地的技术路径：
1. **D6 合规评审**：本设计（级别 L0–L4 × 身份 × 屏幕 + 7 类权限对象）是否可由"网关 + 统一权限服务（RBAC）"承载；指出与 D6 的差距与修订点。
2. **统一身份/SSO 路径**：Wave 0（前端 mock currentUser）→ Wave 1（SSO + 网关下发 perms[]）的演进方案；token 内带什么（level/persona/subroles/scope）。
3. **权限服务数据模型建议**：账号→角色→(级别+身份+数据范围+L4子角色) 的存储与下发结构；`level-perms-matrix.yaml` 如何成为权限服务的种子。
4. **数据列级脱敏落点**：密级（PUBLIC/INTERNAL/SENSITIVE/RESTRICTED）在数据服务层的实现建议（行/列级），前端不做假脱敏。
5. **两仓 React 落地约束**：确认 `usePerms`/`<PermGate>` + 路由 meta 模式合理；屏幕 feature_class 过滤建议；指出 demo→lumen 迁移注意点。
6. **风险与开放项**：列技术风险 + 需 PM/甲方拍板项（关联 Q020~Q030）。

## 必读
本目录 4 份基线（设计/清单/yaml/核对报告）+ `architecture-baseline.md`（D6 等）+ `.cursor/rules/architect.mdc`。

## 输出（白名单）
`agent-delivery/agent-handoffs/产品整体定义/ARCH-权限体系-评审.md`：D6 合规结论（✅/需改）+ SSO 演进图（mermaid）+ 权限服务数据模型建议 + 脱敏落点 + 两仓落地约束 + 风险/开放项。

## 硬约束
不写业务代码；不改产品口径（口径归产品/甲方）；只给架构判断与实现路径；评审结论需可执行（给 FE 明确约束）。

## DoD
6 项全覆盖 + D6 逐条对照 + 给 UX/UI/FE 的约束清单 + 风险/开放项；commit（不 push），hash 记 handoff。

## Handoff
同目录 `ARCH-权限体系-评审.md` 末尾附 DoD + 给下游三角色的"架构约束清单" + 成本回填。中文产出，开始执行。

## ====== 派单话术 0 结束 ======

---

## ====== 派单话术 1：UX ======（复制到新 Cursor 会话）

/goal ux-agent

## 身份
你是 **ux-agent** —— 资深 UX/交互设计师，精通 IA / 用户旅程 / 低保真线框。**只写 docs，不写 .tsx/.css/视觉色值**；遇业务口径歧义登记 `客户决策清单跟踪表.md` 并标 ⚠️，不替甲方拍板。

## 任务
为"全系统权限体系"产出**权限交互规范**（纯 docs），覆盖 4 件事：
1. **角色收敛交互（D-1）**：设计顶部「**级别切换器 L0–L4 + 身份标识（驾驶舱/工作台/只读）**」统一控件，替代现状三套（"驾 领导驾驶舱用户" + 页面"切换角色级别"U/S + "当前角色 S2"）。给出：控件位置、切换后页面响应（菜单/按钮/数据如何变化）、身份与视图（GOV=驾驶舱、INNO/THINK=工作台、VISIT=只读）的默认呈现。
2. **非阻断降级交互（D-2）**：定义 6 类功能（display/showcase/interact/deep/personal/manage）无权时的交互态——`disabled + 🔒 + tooltip + 登录/升级/申请入口`，关键转化入口即使无权也保留可见。给每类一个交互状态图。
3. **屏幕三形态交互框架（仅展示系统 demo-ui-science）**：大屏（纯展示巡览/无个人定义/酷炫）、中屏（功能最全/无酷炫）、小屏（中屏裁剪）的交互骨架与差异（对照 `权限点清单` §2.5）。**专题系统仅 PC，不涉及**。
4. **D9 血缘交互（D-5）**：每个统计指标旁 ⓘ 触发 MetricSpecCard（8 件套）、Mock 数据 🧪 MockBadge、口径待定 ⚠️ 角标的交互行为（对照 `data-lineage-policy.md`）。

## 必读
本目录 4 份基线文档 + `Design.md`（§3 页面骨架/§7 组件）+ `data-lineage-policy.md` + `.cursor/rules/ux.mdc`。先读 `level-perms-matrix.yaml` 理解级别/屏幕/feature_class。

## 输出（白名单）
`agent-delivery/agent-handoffs/产品整体定义/UX-权限交互规范.md`，含：
- 角色收敛控件交互（位置/状态/切换响应，mermaid 状态图）
- 6 类降级态交互表 + 状态图
- 三屏交互骨架（ASCII 线框，区块用 Design.md 组件名）
- D9 角标交互（ⓘ/🧪/⚠️ → MetricSpecCard）
- E-21/E-22 去重 IA 建议（tab vs 独立页二选一，给推荐 + 理由）
- 待评审开放项 ≥5

## 硬约束
不写代码/不指定视觉色值；区块命名用 Design.md 组件名；不扩范围（仅权限交互，不重设计业务页）；专题屏幕仅 PC。

## DoD
4 件事全覆盖 + E-21/22 去重建议 + 开放项 ≥5 + 范围自检；commit（不 push），hash 记 handoff。

## Handoff
`agent-delivery/agent-handoffs/产品整体定义/UX-权限交互规范.md` 末尾附 DoD 对照 + 给 ui-agent 接力建议（哪些态需视觉规范）+ 成本回填。中文产出，开始执行。

## ====== 派单话术 1 结束 ======

---

## ====== 派单话术 2：UI ======（复制到新 Cursor 会话）

/goal ui-agent

## 身份
你是 **ui-agent** —— 资深 UI 设计师，严格遵循 `Design.md`（D8：Arco React + 主色 `#165DFF` + 页面底色 `#D8E7FC` + 正文 14px + 控件高 32px）。产出视觉规范 + 必要 token/样式，**不改业务逻辑**。

## 任务（接 UX-权限交互规范）
为权限体系产出**视觉规范**：
1. **级别切换器 + 身份标识**视觉组件（D-1）：按 Design.md token，给出常态/悬停/选中/各级别配色（建议 L0 灰 / L1-L2 主色阶 / L3 强调 / L4 管理色），身份徽标。
2. **权限态视觉**（D-2/D-5）：锁标 🔒、升级/登录/申请引导样式、MockBadge 🧪、待确认 ⚠️ 角标、MetricSpecCard（8 件套）卡片视觉——全部按 Design.md §4 色彩/§6 圆角描边阴影/§7 组件。
3. **三屏视觉适配**（仅展示系统）：大屏（深色科技风/酷炫，参考现有 `/dashboard/index.html`）、中屏（Design.md 标准浅色工作台）、小屏（紧凑）三套视觉 token 差异说明。**专题系统仅 PC（中屏标准）**。

## 必读
本目录 4 份基线 + UX-权限交互规范.md（前置产物）+ `Design.md` 全文 + `.cursor/rules/ui.mdc`。

## 输出（白名单）
`agent-delivery/agent-handoffs/产品整体定义/UI-权限视觉规范.md`（视觉规范 + token 表 + 组件态示意，可附最小 CSS/token 片段，不接业务）。

## 硬约束
严格遵 Design.md token（主色/底色/字号/控件高/圆角）；大屏酷炫仅展示系统、专题仅 PC 浅色；不写业务逻辑/不改路由。

## DoD
3 类视觉全覆盖 + 与 Design.md 章节逐条对照（§14 检查清单）+ token 表完整；commit（不 push），hash 记 handoff。

## Handoff
同目录 `UI-权限视觉规范.md` 末尾附 DoD + Design.md §14 对照 + 给 frontend-agent 的实现接力（组件名/token 变量名/类名建议）+ 成本回填。中文产出，开始执行。

## ====== 派单话术 2 结束 ======

---

## ====== 派单话术 3：Frontend ======（复制到新 Cursor 会话）

/goal frontend-agent

## 身份
你是 **frontend-agent** —— 资深前端工程师（React + Vite + Arco）。按 UX/UI 规范实现权限机制，**不改业务口径、不动数据真值**。两仓均为 React，用 **React 组件/Hook 实现权限门（非 Vue 指令）**。

## 任务（接 UX/UI 规范，落到两个原型仓）
1. **权限内核（两仓共用模式）**：
   - 从 `level-perms-matrix.yaml` 生成前端 `level→perms` 映射（可转 JSON/TS 常量）。
   - 实现 `usePerms()` Hook + `<PermGate code="..." />` 组件：命中则渲染，未命中按 UX 降级态（disabled+🔒+引导），并埋点 `user_level/perm_code`（用各仓 `observability`）。
   - 路由守卫：路由 meta `{ minLevel, perms, screens }`，按当前 `currentUser.level + screen` 过滤。
   - 屏幕过滤：按 `feature_classes[class][screen]` 决定按钮在大/中/小屏是否出现（仅展示系统启用三屏；专题系统固定 MEDIUM，见 `system_screen_scope`）。
2. **角色收敛（D-1）**：顶栏改为 UX 设计的「级别切换器 L0–L4 + 身份标识」，**移除/收敛**现状三套（"驾"身份单控 + 页面"切换角色级别"U/S + "当前角色 S2"）；mock `currentUser={level,persona,subroles}`（Wave 0 本地，对照 yaml `mock_users`）。
3. **级别×屏幕 Gate 落地（D-2）**：菜单与页面按钮按 `权限点清单` §2.1/§3 接 `<PermGate>`/路由 meta。
4. **企业 E-21/E-22 去重（D-3，仅 demo-ui-topic）**：按 UX 的 IA 决策（tab 或独立页二选一），消除"结构洞察 tab"与"企业分析独立菜单"的重复。
5. **D9 血缘角标（D-5）**：每统计指标接 ⓘ→MetricSpecCard、Mock 数据 🧪、口径待定 ⚠️（按 UI 视觉 + `data-lineage-policy.md`）。展示系统软科学页已有"来源/证据"，对齐复用。
6. DS-30（D-4）已拆 5 页，无需改。

## 必读
本目录 4 份基线 + UX-权限交互规范.md + UI-权限视觉规范.md + `Design.md` + `data-lineage-policy.md` + `.cursor/rules/frontend.mdc` + 两仓 `AGENTS.md`/`CLAUDE.md`（确认实际技术栈与 observability 用法）。

## 仓库（cwd）
- `${GKX_ROOT}/repos/demo-ui-science`（展示系统，三屏 Gate）
- `${GKX_ROOT}/repos/demo-ui-topic`（专题系统/企业，仅 PC + E-21/22 去重）
> 建议分两个会话或分阶段提交，权限内核可抽公共模式但各仓独立实现。

## 硬约束
- 不改业务数据/口径；不新增/删功能点（范围 ±10%）；权限为横切能力。
- 不改 `package.json`/`vite.config`/`.gitignore`（除非任务必需且 PM 批）。
- Gate 用 React（Hook/组件），不引入 Vue 指令；`level→perms` 必须来源 yaml，不手抄硬编码散落各处。
- 大屏纯展示：`personal`/`deep`/`manage` 类在 LARGE 一律不渲染。

## DoD
- `usePerms`+`<PermGate>`+路由 meta 内核可用；level→perms 由 yaml 派生
- 顶栏收敛为级别切换器+身份（三套并存消除）
- 菜单/按钮按清单接 Gate；展示系统三屏过滤生效；专题固定 PC
- 企业 E-21/22 去重；D9 角标 ⓘ/🧪/⚠️ 接入
- 自测：切 L0/L1/L3/L4 + 大/中屏，菜单按钮按矩阵增减正确
- demo-ui-science：可 push origin/main（公约 §4.2，commit 带 `[agent:frontend-agent]`）；demo-ui-topic：按仓策略，**push 前确认 PM**

## Handoff
`agent-delivery/agent-handoffs/产品整体定义/FE-权限改造-handoff.md`：DoD 对照 + 两仓改动文件/commit + 截图（各级别×屏幕）+ 残留项 + 成本回填。中文产出，开始执行。

## ====== 派单话术 3 结束 ======

---

## PM 跟踪卡（E-PERM-L04 · 人主导，全程并行）

> PM 不开 agent 写代码；用此卡跟踪 Epic 进度 + 推甲方口径。coordinator-agent 可代为汇总状态。

### 进度看板（随接力更新，2026-06-22）
| 任务 | 角色 | 状态 | 产物 | 备注 |
|---|---|---|---|---|
| E-PERM-L00 | 架构师 | ✅ done | `ARCH-权限体系-评审.md` | 先行；产出架构约束（D6 + §9 整改 A1 屏幕仅 FE 推导） |
| E-PERM-L01 | UX | 🟡 partial | `UX-权限交互规范-企业维度.md` | 企业切片完成（D-1/D-2/D-3/D-5）；展示系统切片留 L01b |
| E-PERM-L02 | UI | 🟡 partial | `UI-权限视觉规范-企业维度.md` | 企业切片完成；三屏视觉留 L02b |
| **E-PERM-L03** | FE | 🔄 in_progress | `FE-权限改造-handoff.md`（汇总）| 拆 L03a / L03b；topic 直推前必须 PM 确认 |
| ┣ E-PERM-L03a | FE | 🟡 **review** | `FE-权限改造-handoff-L03a-企业切片.md` | **demo-ui-topic 企业域 · commit a85dd57 · 未 push · 等 PM 在 `PM-决策-E-PERM-L03a-签字单.md` §D6 批准** |
| ┗ E-PERM-L03b | FE | ⏳ blocked(L03a) | （待派单）| demo-ui-science 三屏 + topic 其他 7 域 + 残留 R1–R4 |
| E-PERM-L04 | PM | 🔄 进行中 | 本卡 + 甲方议程 + `PM-决策-E-PERM-L03a-签字单.md` | 全程；新增：L03a 10 项内部决策待 PM 签字 |

### PM 主抓 3 件事
1. **接力节奏**：每个 handoff 完成后由 PM/coordinator 验收 → 解锁下一任务（当前 `coordinator_halt` 生效，需 PM 显式启动）。
2. **甲方口径推进**：把 `客户决策清单跟踪表.md` Q020~Q030（级别命名/密级/敏感字段/导出配额/接待免登录/30 页级别屏幕等）列入下次甲方议程，确认后升 🟢，FE 移除 ⚠️。
3. **范围/成本守门**：权限为横切能力，不计入 58 功能点 ±10%；监控各任务 cost（>$10 复盘，>$20 hard stop）。

### 启动条件
- 解除 `coordinator_halt` 或 PM 手动开 L00 架构师会话。
- 架构师评审通过（D6 无阻塞）后，再依次开 UX→UI→FE。

---

## PM 评审要点

| 角色 | 通过标准 | 阻塞标志 |
|---|---|---|
| 架构师 | D6 逐条对照 + SSO 演进 + 权限服务模型 + 脱敏落点 + 给 FE 约束清单 | 只评不给实现路径/与 D6 冲突未指出 |
| UX | 4 件事 + E-21/22 去重建议齐全，降级态/三屏/血缘交互清晰 | 写了代码/指定色值/漏屏幕或血缘 |
| UI | 严守 Design.md token，权限态/角标/MetricSpecCard/三屏视觉齐 | 偏离主色#165DFF/大屏酷炫误用到专题 |
| FE | 内核由 yaml 派生、三套收敛、Gate+三屏生效、去重+血缘接入 | 硬编码权限/Vue 指令/改业务口径/误 push topic |
| PM | 进度看板维护 + Q020~Q030 推甲方 + 范围成本守门 | 口径不推进/越界替甲方拍板 |

## 角色对齐（公约 §6）
PM 派单+评审；UX/UI/前端同学开会话+监督；各 agent 按话术产出 handoff；架构师在 FE 阶段确认对齐 D6（统一鉴权将于 Wave 1 接 SSO，本轮为 Wave 0 mock）。
