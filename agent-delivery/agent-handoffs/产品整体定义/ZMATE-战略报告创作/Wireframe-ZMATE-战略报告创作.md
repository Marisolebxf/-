# Wireframe-ZMATE-战略报告创作.md

> **模块**：ZMATE 战略报告创作（Zmate 战略咨询报告创作工作台原型）  
> **对应 IA**：`IA-ZMATE-战略报告创作.md`  
> **对应 USM / TRACE**：`USM-ZMATE-战略报告创作.md` / `TRACE-ZMATE-战略报告创作.yaml`  
> **阶段**：门 1 PDR 输入 · `ZMATE-RPT-WF-L01`  
> **体验 Owner**：待业务确认（门 1 前指定）  
> **监管人**：`human:淮政玮`  
> **交互基线**：`UX-UE 通用交互组件规范.md`（§19 走查）  
> **视觉**：Design.md 线框级引用 — 控件高 **32px**、主色 **`#165DFF`**、页面底 **`#D8E7FC`**；**本单不画高保真**  
> **版本**：v0.1.0 · 2026-11-16  
> **本阶段边界**：纯前端 Demo 样机（`demo-ui-topic`）；路由对齐建设方案 §9.2；旧 L01–L08 脚手架默认废稿、按本 WF 重做  
> **ponytail**：`off`（定义任务）

## 0. 术语合同（全页强制）

| 正式名 | 落点 Frame | 禁止混称 |
| --- | --- | --- |
| **专题切片** `ThematicSlice` / `slice_id` | F-ZMATE-SLICE | 勿叫「卷宗」 |
| **研判卡** `ScopeCard` | F-ZMATE-CLARIFY / F-ZMATE-SLICE | — |
| **辩论知识卷宗** Debate Dossier | F-ZMATE-DEBATE | 勿叫专题切片 / 研判卡 |
| **合规 Judge** | F-ZMATE-JUDGE | ≠ 战略胜负裁判 |
| **对抗审查**（V3 降级） | 报告区抽屉壳 | ≠ 研究阶段 Judge |

---

## 1. 页面 / Frame 清单

| Frame | 路由 | 目的 | USM |
| --- | --- | --- | --- |
| F-ZMATE-SHELL 创作壳 | `/zmate-strategy-demo` | 项目轨 + Query + 类型 + 专家/Skill → 创建任务 | US-01/02/11 |
| F-ZMATE-HUB Graph Hub | `/zmate-strategy-demo/run/:runId` | **只**展示阶段/解锁/报告区宿主；禁止静默全链 | US-05 |
| F-ZMATE-CLARIFY 澄清人闸 | `…/clarify` | 澄清卡逐步确认；确认前禁 autoRun | US-03/04 |
| F-ZMATE-PLANNER Planner | `…/planner` | 任务树 / 组件开关摘要（不露思维链） | US-05 |
| F-ZMATE-DEBATE 辩论∥卷宗 | `…/debate` | 人控辩论 + 辩论知识卷宗 | US-06 |
| F-ZMATE-SLICE 切片∥研判卡 | `…/slice` | 研判卡 + 方面 + 指标四态 | US-04/07 |
| F-ZMATE-SEEKER 域 Seeker | `…/seeker` | 取数摘要 → 证据包 | US-08 |
| F-ZMATE-WRITER Writer/Assembler | `…/writer` | 四层十组件装配 + 溯源角标 | US-09 |
| F-ZMATE-JUDGE 合规 Judge | `…/judge` | Default-FAIL；≠ 胜负裁判 | US-10 |
| F-ZMATE-TASK-REDIR 旧链兼容 | `/zmate-strategy-demo/task/:id` | 重定向至 Hub，停在未完成阶段 | US-11 |
| （层）内部评审模式 | 壳层全局开关 · 非独立路由 | 仅本页特有差异，见 §12 | US-12 |

**统一分屏壳（Hub 与各 Agent 站共用）**：

```text
┌─ 中屏 medium_1440_1920 · 页底 #D8E7FC ─────────────────────────────┐
│ 顶栏：返回创作壳 · run 摘要 · 阶段 Chip · [内部评审开关=壳层用户面板] │
├─ 左：阶段导航（32px 行高）─┬─ 中：本站工作区 ─┬─ 右：报告阅读宿主 ─┤
│ 澄清 / Planner / …         │ 当前站内容       │ 等待确认 / 占位 /   │
│ 人闸未过 → 后续站锁定      │                  │ 终稿只读            │
└────────────────────────────┴──────────────────┴─────────────────────┘
```

**禁止**：单页一键 autoRun 假进度跑完全链；安装 Skill 静默当本次使用；生成中右侧渲染未完成正文。

---

## 2. 全局状态清单（HITL / Graph）

> 各站状态机落在本表语义上；具体控件态另见各 Frame。

| 状态 ID | 中文 | 表现（全局） | 用户下一步 | 禁止 |
| --- | --- | --- | --- | --- |
| `empty` | 空 | 无 run / 项目轨无任务 / 站内无制品；引导文案 + 主 CTA | 创建任务 / 完成人闸 / 选切片 | 用 fixture 伪造成功报告 |
| `locked` | 锁定 | 目标站灰显；Tooltip 写清解锁条件（人闸/制品） | 回到前置站完成条件 | 点击强行进入并跳过人闸 |
| `awaiting_gate` | 人闸等待 | 本站可编辑；右侧「等待需求确认」或「等待结束辩论」等；后续站锁定 | 显式确认/结束/批准 | autoRun；右侧出正文 |
| `running` | 进行中 | 本站骨架/阶段条（**禁止虚构 %**）；右侧占位「生成中不出正文」 | 等待；可取消（Demo 示意） | 提前渲染终稿；假 live 绿 |
| `failed` | 失败 | 错误条 + 重试；制品不伪造成功 | 重试或带着 `known_gaps` 回看 | 静默改绿 D1–D4 |
| `compliance_fail` | 合规 FAIL | Judge 结果区 Default-FAIL + 原因清单 + 回环提示 | 补 id / 回澄清或切片 / 接受缺口交付 | 把 FAIL 文案写成「辩论败方」 |

### 2.1 Hub 阶段解锁合同（线框级）

| 当前站完成条件 | 解锁 |
| --- | --- |
| 创建任务 | Hub + Clarify（其余锁定） |
| 澄清「确认需求」+ 研判卡可见 | Planner |
| Planner 完成（计划摘要可见） | **辩论 ∥ 切片**（并行均可进） |
| 切片批准（或 V1 显式跳过辩论路径） | Seeker |
| 取数齐备或显式 `known_gaps`；若启用辩论须「结束辩论」或显式跳过 | Writer |
| Writer 装配完成（有结构草稿） | Judge |
| Judge PASS 或带着 known_gaps 交付 | 右侧终稿只读入口 |

**V1 最短路径 A**：澄清确认 → 研判卡 → Planner 示意 →（跳过完整辩论，Hub 标记缺口）→ Writer 占位 → Judge 最小规则 → 报告可读。  
**Demo 路径 B**：必须能分站点进辩论与切片，禁止「一点即跑完」。

---

## 3. F-ZMATE-SHELL 创作壳

### 3.1 线框图

```text
┌─ /zmate-strategy-demo 页底 #D8E7FC ─────────────────────────────────┐
│ 左：项目轨（两级）          │ 右：创作主区                           │
│  📁 文件夹                  │ Query（多行 · 自然语言命题）            │
│   └ 报告任务 · 状态 Chip    │ 报告类型 [Select 32px]                 │
│  [新建文件夹]               │ 专家入口网格（卡 · 进入示意）           │
│                             │ Skill 区：                              │
│                             │  · 已安装 [Chip]（只读清单）            │
│                             │  · 本次使用 [Checkbox]（与安装分离）    │
│                             │              [创建报告任务 · primary]   │
└─────────────────────────────┴───────────────────────────────────────┘
```

### 3.2 字段与规则

| 区块 | 控件 | 规则 | 禁止 |
| --- | --- | --- | --- |
| 项目轨 | 树 / 列表 32px | 两级：文件夹 → 报告任务；点任务进 Hub 恢复 | 当二级强制菜单删改仓内专题菜单 |
| Query | `a-textarea` | 必填才可创建；不清空项目轨 | 承诺 LLM 已理解未澄清 |
| 报告类型 | `a-select` 高 32px | 必选 | — |
| Skill 已安装 | Chip | **≠** 本次使用 | 装了即静默写入本报告 |
| Skill 本次使用 | Checkbox | 取消后时间线不得静默调用 | 与安装态混成一枚 Chip |
| 创建任务 | `a-button` primary `#165DFF` | 成功 → Hub（`runId`） | 单页假跑完全链 |

### 3.3 状态

| 状态 | 表现 | 下一步 |
| --- | --- | --- |
| empty | 项目轨空 + Query 空；主 CTA 引导 | 输入并创建 |
| running | 创建中按钮 loading | 等待进 Hub |
| failed | 错误条 + 重试 | 修正后重试 |

### 3.4 交互

| 触发 | 行为 | 不应发生 |
| --- | --- | --- |
| 创建成功 | 路由 `/run/:runId`；阶段=澄清 | Hub 内静默跑 Planner…Judge |
| 打开既有任务 | → Hub，停在未完成阶段 | 跳过已锁定人闸 |
| 取消本次 Skill | 配置快照无该 Skill | 仍出现在后续时间线调用 |

---

## 4. F-ZMATE-HUB Graph Hub

### 4.1 线框图

```text
┌─ /run/:runId ───────────────────────────────────────────────────────┐
│ 顶：任务标题 · Query 摘要 · 报告类型                                  │
├─ 左阶段导航 ──────────────┬─ 中：本阶段摘要卡 ─┬─ 右报告宿主 ────────┤
│ ○ 澄清   [当前/完成/锁]   │ 当前站职责一句话   │ 等待需求确认 /      │
│ ○ Planner                 │ 下一站解锁条件     │ 生成中占位 /        │
│ ○ 辩论 ∥ 切片（并行）     │ [进入当前站]       │ 终稿只读入口        │
│ ○ Seeker                  │                    │                     │
│ ○ Writer                  │ **无**「一键跑完」 │                     │
│ ○ Judge                   │                    │                     │
└───────────────────────────┴────────────────────┴─────────────────────┘
```

### 4.2 规则

| 项 | 合同 |
| --- | --- |
| Hub 职责 | **只**展示进度、制品交接摘要、解锁条件 |
| 进入站 | 仅解锁站可点；锁定站 Tooltip 写条件 |
| 并行 | Planner 完成后辩论与切片同级可进 |
| 报告区 | 未确认 →「等待需求确认」；生成中 → 占位；完成后只读入口 |
| 禁止 | Hub 内静默执行全链；假进度条假装跑完 |

### 4.3 状态映射

| Hub 表现 | 全局状态 |
| --- | --- |
| 无 run | empty |
| 后续站灰 | locked |
| 澄清未确认 | awaiting_gate |
| 某站执行中 | running |
| 站失败条 | failed |
| Judge FAIL 摘要 | compliance_fail |

---

## 5. F-ZMATE-CLARIFY 澄清人闸

### 5.1 线框图

```text
┌─ …/clarify ─────────────────────────────────────────────────────────┐
│ 左导航（澄清=当前）│ 中：澄清卡逐步确认              │ 右：等待需求确认 │
│                    │ 对象 / 行业 / 范围 / 时间       │ （无正文）       │
│                    │ 受众 / 深度 / 决策要点 …        │                 │
│                    │ 候选研判卡列表 → 绑定/生成      │                 │
│                    │ [上一步] [确认需求 · primary]   │                 │
└────────────────────┴────────────────────────────────┴─────────────────┘
```

### 5.2 规则

| 项 | 合同 |
| --- | --- |
| 人闸 | 「确认需求」前：`awaiting_gate`；禁 autoRun；右侧固定等待文案 |
| 确认后 | 绑定/生成至少一张研判卡（Demo Mock 可）；暴露 `slice_id` |
| 制品 | brief + 候选/绑定 `slice_id` |
| 不可做 | 直接写终稿；未确认进 Planner 长跑 |

### 5.3 状态

| 状态 | 表现 |
| --- | --- |
| awaiting_gate | 卡可编辑；确认按钮可用；后续锁；右等待 |
| running | 绑定研判卡中骨架 |
| empty | 无候选卡 → 引导「生成研判卡」 |
| failed | 绑定失败 + 重试 |

---

## 6. F-ZMATE-PLANNER Planner

### 6.1 线框图

```text
┌─ …/planner ─────────────────────────────────────────────────────────┐
│ 任务树（章节/组件开关摘要）│ 切片选择摘要 │ 右：仍可等待/占位         │
│ [组件开关 Chip · 只读示意] │             │ 不露思维链 / CoT         │
│ 完成后解锁：辩论 ∥ 切片    │             │                         │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 规则

| 项 | 合同 |
| --- | --- |
| 可见 | 任务树、组件开关摘要、切片选择 |
| 禁止 | 把 metric-registry 当规划主入口；露思维链 |
| 完成后 | Hub 同时解锁 `/debate` 与 `/slice` |

### 6.3 状态

| 状态 | 表现 |
| --- | --- |
| locked | 澄清未确认 |
| running | 计划生成骨架 |
| empty | 计划空 → 重跑 Planner |
| failed | 错误 + 重试 |

---

## 7. F-ZMATE-DEBATE 辩论 ∥ 辩论知识卷宗

### 7.1 线框图

```text
┌─ …/debate ──────────────────────────────────────────────────────────┐
│ 顶提示：本站对象 = 辩论知识卷宗（≠ 专题切片/研判卡）· 无战略胜负裁判 │
│ 中左：正方 / 反方论点流 │ 中右：卷宗三层（结论 / 推理 / 信源）       │
│ [新一轮] [引导轮] [结束辩论]                                         │
│ 结束后：卷宗只读；人闸解除（若启用辩论）                              │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 规则

| 项 | 合同 |
| --- | --- |
| 人控 | 新一轮 / 引导轮 / 结束；非自动辩完 |
| 卷宗 | 三层可读写 → 结束后只读 |
| 并行 | 与切片站互不冒充制品 |
| V1 | 可跳过完整辩论，但须 Hub 可点验本站入口 |
| 禁止 | 「胜负 / 采信方」文案；把卷宗写成切片 |

### 7.3 状态

| 状态 | 表现 |
| --- | --- |
| locked | Planner 未完成 |
| awaiting_gate | 启用辩论且未结束 → Writer 锁定 |
| running | 一轮生成中骨架 |
| empty | 尚无论点 → 引导「新一轮」 |
| failed | 轮次失败 + 重试 |

---

## 8. F-ZMATE-SLICE 切片 ∥ 研判卡

### 8.1 线框图

```text
┌─ …/slice ───────────────────────────────────────────────────────────┐
│ 顶提示：本站对象 = 专题切片 / 研判卡（≠ 辩论知识卷宗）               │
│ 研判卡卡面 · slice_id │ 方面域摘要 │ 指标需求四态表                  │
│ 四态：可用 / 待建 / 待真接 / 待外网补数 · Mock 角标（评审开时）      │
│ [批准切片指标] → 解锁 Seeker                                         │
└─────────────────────────────────────────────────────────────────────┘
```

### 8.2 规则

| 项 | 合同 |
| --- | --- |
| 四态诚实 | 不得「已对齐 live」假绿 |
| Mock | 评审模式可见 🧪；业务态可保留数值但不改绿 D4 |
| 禁止 | 把切片叫卷宗；假 live |
| 并行 | 与辩论站独立 |

### 8.3 状态

| 状态 | 表现 |
| --- | --- |
| locked | Planner 未完成 |
| empty | 无研判卡 → 回澄清绑定 |
| awaiting_gate | 未批准 → Seeker 锁 |
| running | 四态刷新骨架 |
| failed | 加载失败 + 重试 |

---

## 9. F-ZMATE-SEEKER 域 Seeker

### 9.1 线框图

```text
┌─ …/seeker ──────────────────────────────────────────────────────────┐
│ 域列表：展示态势 / 产业链 / 政策 / 企业 …（Demo 可串行模拟并行）     │
│ 取数摘要卡 → 写入证据包清单                                           │
│ known_gaps 显式列出                                                  │
│ 齐备或显式缺口后 → 可进 Writer（仍受辩论结束条件约束）                │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.2 规则

| 项 | 合同 |
| --- | --- |
| 输入 | 已批准切片指标 |
| 输出 | 证据包摘要 + `known_gaps` |
| 禁止 | 写手直连多库；擅自扩切片外指标 |

### 9.3 状态

| 状态 | 表现 |
| --- | --- |
| locked | 切片未批准 |
| running | 域取数中 |
| empty | 证据包空 + 缺口说明 |
| failed | 域失败条 + 重试 / 记入缺口 |

---

## 10. F-ZMATE-WRITER Writer / Assembler

### 10.1 线框图

```text
┌─ …/writer ──────────────────────────────────────────────────────────┐
│ 准入条：辩论条件 · 取数条件（未满足 = locked 说明）                   │
│ 四层十组件装配大纲（可勾选/只读示意）                                 │
│ 章节草稿宿主；关键结论旁溯源角标占位（原文 / 口径 / 推断）            │
│ 生成中：右侧报告宿主 = 占位「不出未完成正文」                         │
│ 完成后：右侧可打开结构草稿（仍须 Judge）                              │
└─────────────────────────────────────────────────────────────────────┘
```

### 10.2 规则

| 项 | 合同 |
| --- | --- |
| 装配 | 按组件，非黑盒长文 |
| 溯源 | 数字可回 `slice_id` / `metric_id` 或 `known_gaps` |
| 生成中 | 右侧**不**渲染未完成正文 |
| 禁止 | 发明无 id 数字；绕过切片直查指标库当入口 |

### 10.3 状态

| 状态 | 表现 |
| --- | --- |
| locked | 辩论未结束（若启用）或取数未齐且无显式缺口 |
| running | 装配中；右占位 |
| empty | 无章节结构 → 引导重跑 |
| failed | 装配失败 + 重试 |

---

## 11. F-ZMATE-JUDGE 合规 Judge

### 11.1 线框图

```text
┌─ …/judge ───────────────────────────────────────────────────────────┐
│ 顶标注：合规 Judge · Default-FAIL · ≠ 战略胜负裁判                    │
│ 规则清单：缺 metric_id / 假 live / 绕过人闸 / …                      │
│ 结果：PASS | FAIL（compliance_fail）                                 │
│ FAIL：原因 + known_gaps + 回环（回澄清/切片/Writer）                  │
│ PASS：右侧终稿只读 + 基础溯源                                        │
│ （V3）对抗审查 = 报告旁抽屉壳 + 静态清单，非本站裁判                  │
└─────────────────────────────────────────────────────────────────────┘
```

### 11.2 规则

| 项 | 合同 |
| --- | --- |
| Default-FAIL | 缺 id / 假 live / 绕过人闸 → FAIL |
| 职责 | 合规闸；**不**改正文；**不**当辩论裁判 |
| 禁止 | 静默改 D1–D4；FAIL 文案写成胜负 |

### 11.3 状态

| 状态 | 表现 |
| --- | --- |
| locked | Writer 未产出结构草稿 |
| running | 质检中 |
| compliance_fail | FAIL 面板 + 回环 |
| failed | 质检服务失败（≠ 合规 FAIL）+ 重试 |
| empty | 无规则结果 → 重跑 Judge |

---

## 12. 内部评审模式 · 页特有差异（仅本模块）

> **入口**：右上角用户/角色面板 → 全局「内部评审模式」。  
> **本 WF 只记页特有差异**；通用自闸 / 关闭零泄漏 / 角标并存序等不复制。

| 挂载点 | 页特有内容（开启可见） |
| --- | --- |
| 创作壳 / Hub | 建设方案 §3 三轴、§9.2 路由对照；阶段契约；非目标提示；菜单仅增量 |
| 澄清 / 辩论 / 切片 | **术语对照卡**（卷宗 vs 切片/研判卡）；人闸 / 禁 autoRun 验收句 |
| 切片 · 指标需求 | 四态 + Mock / `known_gaps`；禁止假 live 说明 |
| Judge | Default-FAIL 规则清单；「≠ 战略胜负裁判」 |
| 报告阅读 | `slice_id` / `metric_id` 溯源评审挂载；HV-11 组件结构示意 |

关闭后：上述字样与评审角标自闸隐藏；业务 Query、报告正文、任务状态、阶段导航保留，且无 `metric_id` / `GAP-*` / 条款字样泄漏。

### 12.1 review mounts（摘要）

```yaml
  - mount_id: ZMATE-SHELL-HUB-TRACE
    frame_id: F-ZMATE-SHELL / F-ZMATE-HUB
    marker_type: requirement_trace
    required_payload: [source_location, stage_contract, non_goals]
    review_mode: present
    business_mode: absent
  - mount_id: ZMATE-TERM-DOSSIER-VS-SLICE
    frame_id: F-ZMATE-CLARIFY / F-ZMATE-DEBATE / F-ZMATE-SLICE
    marker_type: terminology_card
    required_payload: [dossier_def, slice_def, forbidden_aliases]
    review_mode: present
    business_mode: absent
  - mount_id: ZMATE-SLICE-FOUR-STATE
    frame_id: F-ZMATE-SLICE
    marker_type: mock_badge + gap_hint
    required_payload: [four_state, known_gaps, no_fake_live]
    review_mode: present
    business_mode: absent
  - mount_id: ZMATE-JUDGE-DEFAULT-FAIL
    frame_id: F-ZMATE-JUDGE
    marker_type: compliance_rules
    required_payload: [default_fail_rules, not_strategy_referee]
    review_mode: present
    business_mode: absent
  - mount_id: ZMATE-REPORT-TRACE
    frame_id: 报告阅读宿主
    marker_type: lineage_mount
    required_payload: [slice_id, metric_id_or_gap, hv11_structure]
    review_mode: present
    business_mode: absent
```

---

## 13. 主路径线框 walkthrough

### 13.1 路径 A · V1 最短

```text
SHELL 创建 → HUB → CLARIFY 确认 + 研判卡
  → PLANNER 示意 →（跳过完整辩论，标记缺口）
  → WRITER 占位装配 → JUDGE 最小规则 → 右报告可读
```

### 13.2 路径 B · Demo 完整可点验

```text
同 A 至 PLANNER
  → DEBATE ∥ SLICE（分站进入，禁止一点跑完）
  → SEEKER → WRITER（条件满足）→ JUDGE → 终稿
```

### 13.3 路径 C · 项目轨恢复

```text
SHELL 项目轨 → HUB（未完成阶段）→ 继续人闸 / 分站；不跳过人闸
```

---

## 14. D10 §19 走查对照（本模块）

| 检查项 | 本 WF 落点 |
| --- | --- |
| 组件归类 | 壳/导航/Chip/人闸按钮=通用；澄清卡/卷宗/研判卡/Judge 规则=业务 |
| 状态完整性 | §2 六态 + 各 Frame 状态表；控件悬停/聚焦/禁用走 Arco 默认 |
| 键盘可达 | 主路径：Tab 进 Query/类型/创建；人闸「确认需求」可聚焦激活；阶段导航可键盘激活已解锁项 |
| 筛选一致 | 本台无全局分析筛选条；项目轨过滤与 Hub 阶段 Chip 上下文一致 |
| 联动可解释 | 点阶段 → 进对应站；报告区随人闸/生成态变化；可返回 Hub |
| 权限明确 | Demo 角色切换示意；导出正式权限门 1 后；不可进锁定站有 Tooltip 原因 |
| 导出可信 | 本阶段不承接正式导出对齐 ENT-EXPORT（OPEN-ZMATE-EXPORT-01） |
| 异常可恢复 | failed / compliance_fail 均有重试或回环 |
| 空态可行动 | 各站 empty 有下一步 CTA |
| 抽屉宽度 | 对抗审查降级抽屉参考 30vw / min 480 / max 640 |
| 遮罩策略 | Hub/分站非模态分屏；确认类用模态（确认需求可页内主按钮，无需强模态） |
| 无障碍 | 等待/锁定/FAIL 有文本，不只靠色；卷宗只读态有说明 |
| Arco 一致性 | Select/Button/Checkbox/Chip/树 优先 Arco；禁页私有控件风格 |

---

## 15. 与 IA / USM 差异说明

| 项 | 说明 |
| --- | --- |
| 路由 / 阶段序 | 与 IA §3 / §3.3 一致，无新增二级菜单 |
| 六态命名 | WF 落地为 `empty/locked/awaiting_gate/running/failed/compliance_fail`，语义对齐 USM 异常表 |
| 高保真 | 不画；仅 Design token 引用 |
| 旧 FE 脚手架 | 默认废稿，按本 Frame 重做（OPEN-ZMATE-DEMO-01） |

---

## 16. Wireframe 自检

- [x] 覆盖：创作壳、Hub、澄清人闸、Planner、辩论∥切片、Seeker、Writer、Judge  
- [x] 状态清单：空 / 锁定 / 人闸等待 / 进行中 / 失败 / 合规 FAIL  
- [x] 术语：辩论知识卷宗 ≠ 专题切片；Judge ≠ 胜负裁判  
- [x] 禁止单页跑完全链；Hub 只展示进度  
- [x] 内部评审模式仅页特有差异  
- [x] D10 §19 走查对照表  
- [x] Design 线框级引用（32px / `#165DFF` / `#D8E7FC`）  
- [x] 未改前端代码  
