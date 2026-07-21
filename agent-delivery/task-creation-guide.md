# 任务创建指南（task-registry 入库）

> **读者**：PM、架构师、产品 Owner、各 team Lead、coordinator  
> **版本**：v1.0 · 2026-07-21  
> **维护**：PM（郭万迎）+ coordinator  
> **机器真源**：`task-registry.yaml` · `bitable-inbound-proposals.yaml`（提案队列）  
> **关联**：`task-claiming-guide.md`（认领与状态）· `自动派单与确认规约.md`（unlock/confirm）· `产品定义评审规程.md` §9.1 · `产品实现规程.md` §8

---

## 1. 一句话

> **建单 = 在 `task-registry.yaml` 登记一条可派工 leaf；解锁 = 把已有 leaf 从 backlog 变 ready；认领 = 执行人承诺负责进度。** 三者不可混用。

---

## 2. 三角关系（必记）

```text
┌─────────────┐     scan + confirm      ┌─────────────┐     飞书/CLI 认领      ┌─────────────┐
│  ① 建单      │ ──► 已有 backlog leaf   │  ② 解锁      │ ──► ready leaf       │  ③ 认领      │
│  写入 registry│     （不新建 id）        │  backlog→ready│                      │  ready→claimed│
└─────────────┘                         └─────────────┘                      └─────────────┘
     PM/架构师                               PM/监管人 confirm                      执行人 + 监管人
```

| 动作 | 改什么 | 谁做 | 自动化 |
|------|--------|------|--------|
| **建单** | 新增或补全 `task-registry` leaf | PM、架构师（经授权 Lead） | ❌ 不自动写入 registry |
| **解锁** | 已有 leaf：`backlog` → `ready` + 派单包 | PM / 监管人 `confirm` | ✅ scan 自动提议 pending |
| **认领** | `ready` → `claimed` + `claimed_by` / `supervised_by` | 执行人 / Lead | 飞书 inbound 或 CLI |

**常见误解**：

- ❌ 「PACK done 后系统自动创建 UX 任务」→ 错。UX 须**事先入库**；done 后只是 **confirm 解锁**。
- ❌ 「飞书新建一行 = 正式 task」→ 错。默认进 **`bitable-inbound-proposals.yaml`**，PM 审阅后手工并入 registry。
- ❌ 「confirm = 建单」→ 错。confirm 只改状态、出派单包，**不新增 Task ID**。

---

## 3. 谁可以创建任务？

| 角色 | 可否新建 registry leaf | 典型场景 | 不应做的事 |
|------|------------------------|----------|------------|
| **PM（郭万迎）** | ✅ 主责 | Epic 首开、Sprint Planning、门 I1 工程拆单、proposals 采纳 | 绕过 DG 把实现轨标 ready |
| **项目负责人（淮政玮）** | ✅ 定义轨拍板相关 | PACK/DG 结论、范围变更登记 | 代替 PM 日常拆 Sprint |
| **架构师（徐滕强 / 李伟）** | ✅ 经 PM 对齐 | ARCH-IMPL、API 契约 leaf、跨模块依赖 | 超 architecture 铁律的 leaf |
| **产品 Owner / 体验 Owner** | ⚠️ 提案为主 | 定义轨 PACK 前置讨论；走 PM 入库 | 自行 push registry 不经 PM |
| **前端 / 后端 / 算法 Lead** | ⚠️ 缺口提案 | Retro 补单、Convoy 串行链；写 proposals 或找 PM | 擅自新建 Epic 级 leaf |
| **普通开发** | ❌ 默认不建 | 飞书认领已有 ready task | 手改 `task-registry.yaml` |
| **coordinator-agent** | ⚠️ 起草 YAML | 辅助 PM 生成 leaf 片段；**须人审 + commit** | 自动 merge 进 registry |

> **铁律**：范围超出 bid-reference ±10% 的新 leaf，须淮政玮 + 郭万迎书面登记；业务口径未定须标 🟡（见 `客户决策清单跟踪表.md`）。

---

## 4. 三条入库路径

### 4.1 路径 A · 规划拆单（主路径）

**适用**：Epic 首开、模块定义链、门 3 后工程链。

1. PM / 架构师对照规程模板列出 leaf 清单  
   - **定义轨**：`产品定义评审规程.md` §9.1.1（PACK → METRIC-OPEN ∥ UX → … → DG-G3）  
   - **实现轨**：`产品实现规程.md` §8.1（DG-G3 后 ARCH / API / FE-WIRE / QA…）
2. 复制 `templates/task-leaf-template.yaml`，按模块改 `id` / `depends_on` / `agent` / `delivery_phase`
3. 写入 `task-registry.yaml`（`status: backlog`，**不要**直接标 `ready`）
4. `git commit` → outbound 投影飞书（或等 watch 同步）
5. 依赖满足后走 **scan → confirm** 解锁（定义轨 / 实现轨均须 confirm）

### 4.2 路径 B · 飞书新增行（提案路径）

**适用**：站会口头提出新活、临时记录想法。

1. 人在飞书 Bitable **新增一行**（可先填标题；Task ID 勿乱改）
2. 跑 inbound → 行进入 **`bitable-inbound-proposals.yaml`**
3. PM 审阅：采纳 / 驳回 / 合并到已有 leaf
4. 采纳时：在 registry **手工新增**正式 leaf（规范 Task ID），再 outbound
5. **不会**自动进 registry（见 `feishu-bitable-integration.md` §1）

### 4.3 路径 C · 缺口 / Retro 补单

**适用**：QA 整改、handoff 建议、联调发现遗漏。

1. 提出人在 Retro 或 handoff 写清：**建议 Task ID、依赖、agent、理由**
2. PM 判断是否 in-scope → 走路径 A 入库，或写入 proposals 待 Planning
3. 禁止开发自行 push 未评审 leaf

---

## 5. 交付阶段（`delivery_phase`）怎么选？

| 值 | 含义 | 对应规程 | 典型后缀 / 场景 |
|----|------|----------|-----------------|
| `definition` | 产品定义阶段 | `产品定义评审规程.md` | `*-PACK-L01`、`*-UX-L01`、`*-V1-HIFI`、`*-PDR-G1*`、`*-DG-G3` |
| `implementation` | DG 后工程实现 | `产品实现规程.md` | `*-API-*`、`*-FE-WIRE*`、`*-JAVA-*`、联调 / 硬化 leaf |
| `crosscut` | 平台 / 编排横切 | 架构 + PM 约定 | feishu-sync、权限 Epic、编排脚本 |

**规则**：

- 门 3 **之前**：工程类 leaf 应为 `backlog` + `definition` 或暂不建；**禁止** implementation 标 `ready`
- 门 3 **之后**：工程 leaf 标 `delivery_phase: implementation`；unlock 走 `impl-gate3-unlock` + confirm
- 飞书「交付阶段」列由 registry **outbound 投影**，勿指望 inbound 回写

---

## 6. Task ID 命名与字段清单

### 6.1 命名建议

```text
{Epic前缀}-{模块}-{类型}-{序号}
例：ENT-MOD-SEARCH-PACK-L01
    ENT-MOD-SEARCH-UX-L01
    ENT-JAVA-SEARCH-BIZ
```

- 模块 slug 与 `dispatch-rules.yaml` / 产品包目录一致  
- 同模块 leaf 共用 `parent`（如 `ENT-MOD-SEARCH-PDR-G1-RECLOSE`）便于追溯  
- **禁止**与已有 id 重复；**禁止**在 Bitable 手改 Task ID 主键

### 6.2 新建 leaf 最低必填

| 字段 | 说明 |
|------|------|
| `id` | 全局唯一 |
| `title` | 中文标题，站会可读 |
| `epic` | 所属 Epic id |
| `agent` | 执行 agent 角色 |
| `repo` / `repos` | 主工作仓 |
| `depends_on` | 直接依赖 task id 列表 |
| `status` | 新建一律 `backlog`（勿直接 `ready`） |
| `delivery_phase` | `definition` / `implementation` / `crosscut` |
| `priority` | P0 / P1 / P2 |
| `definition_of_done` | 可验收条目列表 |
| `estimated_tokens` | 派单前估算（可选 effort_points / difficulty） |

### 6.3 定义轨建议附加

- `product_gates` / `visual_gates`（见 `产品定义评审规程.md` §9.1 示例）
- `cicd: skip_design_only`（纯文档 leaf）
- `evidence` 路径占位（完成后回填）

### 6.4 实现轨建议附加

- `depends_on` 含同模块 `*-DG-G3` 或架构契约 leaf
- `supervised_by` 在 confirm 前可由 coordinator 按 `dispatch-rules.yaml#agent_supervisors` 回填
- 联调类 leaf 注明 Convoy（见 `dispatch-queue.yaml`）

完整字段说明见 `task-registry.yaml` 头部 `fields` / `delivery_phase_policy` / `contribution_policy`。

---

## 7. 按角色的快速 checklist

### PM

- [ ] 新 leaf 是否 in-scope（±10%）？
- [ ] `delivery_phase` 与门 3 状态一致？
- [ ] `depends_on` 无环、上游已存在？
- [ ] 定义轨 / 实现轨 unlock 是否留待 **confirm**（勿手改 ready 绕过）？
- [ ] Sprint 内 leaf 是否写入 `sprint_id`（Planning 时）？
- [ ] proposals 队列是否每周清空审阅？

### 架构师

- [ ] Java / Python / 前端边界符合 architecture-baseline？
- [ ] API leaf 是否只描述契约与门面，不含算法实现？
- [ ] 跨 Epic 依赖是否写入 `depends_on` + note？

### 产品 / 体验 Owner

- [ ] 定义轨 leaf 证据路径与 USM/IA/Wireframe 目录一致？
- [ ] 未决业务口径是否登记 `客户决策清单跟踪表.md` 🟡？

### 开发 Lead / 工程师

- [ ] 需要新 task 时是否先找 PM / 写 proposals？
- [ ] 只认领 **ready** 任务；用飞书改认领 + inbound？
- [ ] Agent 执行时 `supervised_by` 填开 Cursor 的真人真名？

---

## 8. 与自动派单的衔接

```text
registry 已有 leaf (backlog)
        │
        ▼ 上游 done
   coordinator scan ──► pending-dispatch.yaml（解锁提议，非建单）
        │
        ▼ PM confirm
   backlog → ready + 派单包.md
        │
        ▼ 执行人认领
   claimed → in_progress → … → done
```

- **scan / confirm 详情**：`自动派单与确认规约.md`  
- **认领 / 状态机**：`task-claiming-guide.md`  
- **规则真源**：`dispatch-rules.yaml`

---

## 9. 用 Cursor 辅助起草（不代替 PM 拍板）

**PM — 按定义轨模板生成草案（不直接改 registry）**

```text
请在 gkx-orchestration 对照 产品定义评审规程 §9.1.1，
为模块 ENT-MOD-COMPARE 列出应有 definition leaf 清单，
并输出可粘贴的 YAML 片段（status 一律 backlog）。
不要直接修改 task-registry.yaml。
```

**PM — 门 I1 工程拆单草案**

```text
模块 ENT-MOD-SEARCH 已通过 DG-G3。
请按 产品实现规程 §8.1 生成 implementation leaf YAML 草案，
depends_on 含 ENT-MOD-SEARCH-DG-G3，delivery_phase: implementation。
输出供 PM 审阅，不要 commit。
```

**架构师 — API 契约 leaf**

```text
为 ENT 企业查询模块新增 API 契约 leaf，
agent: api-agent，repo: lumen-svc-platform，
depends_on 与 产品实现规程 §8.1 一致。仅输出 YAML 块。
```

---

## 10. 常见反模式

| 反模式 | 后果 | 正确做法 |
|--------|------|----------|
| PACK done 才发现没建 UX leaf | confirm 无 target，下游永远不解锁 | Epic 规划时按 §9.1 一次性入库 |
| DG 后直接标 implementation `ready` | 跳过 confirm 审计、无派单包 | backlog + 等 impl-gate3-unlock confirm |
| 开发手改 registry 标 ready | 缺派单包 / 飞书与 YAML 冲突 | `update-task-status` + confirm 流程 |
| 飞书新增行当正式 task | duplicate / sync 失败 | 审阅 proposals 后赋正式 Task ID |
| 混用 `pending` 与 `backlog` | 状态机漂移 | 新 task 只用 `backlog`；跑 ready-engine 迁移 |

---

## 11. 相关文档索引

| 文档 | 用途 |
|------|------|
| `templates/task-leaf-template.yaml` | 复制即用的 leaf 片段 |
| `产品定义评审规程.md` §9.1 | 定义轨依赖模板 |
| `产品实现规程.md` §8 | 实现轨拆单模板 |
| `task-claiming-guide.md` | 认领与 execution 状态机 |
| `自动派单与确认规约.md` | scan / confirm / 飞书三列 |
| `feishu-bitable-bidirectional-ops.md` §4.D | 飞书新增行 proposals |
| `bitable-inbound-proposals.yaml` | 飞书新增行待 PM 审阅队列 |
| `registry-gap-proposals.yaml` | **缺口建单建议**队列（Phase 1 脚本写入） |
| `registry-gap-templates.yaml` | 定义/实现轨缺口检测模板 |
| `sprints/ent-scrum-pdr-backlog.md` | 企业维度拆单样例 |

---

## 13. 缺口建单建议（Phase 1 · 已实现）

> **原则**：脚本只**建议**，PM 审阅后手工并入 `task-registry.yaml`；**绝不**自动 merge。

### 13.1 检测什么？

| 类型 | 说明 |
|------|------|
| `missing_definition_leaf` | 已有 `PACK-L01`，缺 §9.1 链上必填 leaf（METRIC-OPEN / UX / V1…） |
| `unlock_target_missing` | 上游已 `done`，但 `dispatch-rules` 期望的 unlock 目标不存在 |
| `missing_implementation_leaf` | 已登记 `DG-G3`，缺 §8 推荐 implementation leaf |
| `broken_dependency` | `depends_on` 指向 registry 中不存在的 id |

模板真源：`registry-gap-templates.yaml`

### 13.2 命令

```powershell
cd gkx-orchestration

# 扫描缺口（stdout）
node scripts/suggest-registry-tasks.mjs scan
node scripts/suggest-registry-tasks.mjs scan --module ENT-MOD-RISK --phase definition

# 写入建议队列（供 PM 审阅）
node scripts/suggest-registry-tasks.mjs write --module ENT-MOD-RISK

# 列出待审建议
node scripts/suggest-registry-tasks.mjs list

# 输出可粘贴 YAML（不写入 proposals 文件）
node scripts/suggest-registry-tasks.mjs yaml --module ENT-MOD-RISK

# coordinator 别名
node scripts/coordinator-dispatch.mjs suggest-gaps --module ENT-MOD-RISK
```

### 13.3 PM 采纳流程

```text
1. scan / write → registry-gap-proposals.yaml（status: proposed）
2. PM 审阅 reason + suggested_yaml
3. 复制 YAML 并入 task-registry.yaml（或按模板手改）
4. git commit → outbound 投影飞书
5. 将 proposal 标 accepted / rejected（手工编辑 proposals 文件，Phase 2 可加 CLI）
6. 依赖满足后走 scan → confirm 解锁（不是建单）
```

### 13.4 与 unlock / proposals 的区别

| 队列 | 作用 |
|------|------|
| `pending-dispatch.yaml` | 已有 leaf **解锁**提议（confirm） |
| `bitable-inbound-proposals.yaml` | 飞书**新增行**提案 |
| `registry-gap-proposals.yaml` | **缺 leaf / 坏依赖** 建单建议 |

---

## 14. Phase 2 · accept/reject + scan 摘要 + 飞书投影（已实现）

### 14.1 accept / reject（审计字段）

```powershell
# 审阅后标记（不自动 merge registry）
node scripts/suggest-registry-tasks.mjs accept \
  --ids gap-ENT-MOD-RISK-METRIC-OPEN-L01-mru4ho8s \
  --approved-by human:郭万迎 \
  --note "已复制 YAML 并入 registry"

node scripts/suggest-registry-tasks.mjs reject \
  --ids gap-ENT-MOD-RISK-UX-L01-mru4ho8s \
  --approved-by human:郭万迎 \
  --note "与现有 UX 任务合并"

# 批量
node scripts/suggest-registry-tasks.mjs accept --all --approved-by human:郭万迎
```

写入 `registry-gap-proposals.yaml` 的审计字段：

| 字段 | 说明 |
|------|------|
| `reviewed_by` | PM/监管人（与 confirm 同 roster 校验） |
| `reviewed_at` | ISO 时间戳 |
| `review_note` | 可选说明 |
| `registry_merged` | accept 时若 registry 已有同 id 则为 true |
| `registry_task_id` | 合并后的正式 Task ID |

> **accept 仍不自动写入 task-registry** — PM 须手工 merge YAML 后 commit；若 registry 已含同 id，accept 会自动标 `registry_merged: true`。

### 14.2 scan 结束 gap 摘要

`scan` 与 `coordinator-dispatch.mjs scan` 结束时自动输出 **registry gap summary**（scan 缺口数 + proposed 队列数）。

```powershell
node scripts/suggest-registry-tasks.mjs scan --module ENT-MOD-RISK
node scripts/coordinator-dispatch.mjs scan --cause-task ENT-MOD-RISK-PACK-L01
```

### 14.3 飞书「待审建单」投影

`feishu-bitable.yaml#dispatch_gate_map` 新增：

| key | Bitable 显示 |
|-----|-------------|
| `gap_proposed` | 待审建单 |
| `gap_accepted` | 建单已采纳 |
| `gap_rejected` | 建单已驳回 |

```powershell
# write 后投影（或单独跑）
node scripts/suggest-registry-tasks.mjs write --module ENT-MOD-RISK --project-feishu
node scripts/suggest-registry-tasks.mjs project-feishu --status proposed [--dry-run]
```

投影行为：为 **尚未入库** 的 `suggested_task_id` 在 Bitable **CREATE/UPDATE** 一行；`派单门控=待审建单`，`解锁说明=[kind] reason`；`feishu_record_id` 回写 proposals。

accept/reject 后自动更新对应行的门控为「建单已采纳/已驳回」。

### 14.4 完整 PM 闭环（RISK 样例）

```text
1. write --module ENT-MOD-RISK [--project-feishu]
2. 飞书/Bitable 看待审建单行 + list --status proposed
3. 复制 suggested_yaml → task-registry.yaml → commit
4. accept --ids ... --approved-by human:郭万迎
5. PACK done 后 scan → confirm 解锁（不是建单）
```
