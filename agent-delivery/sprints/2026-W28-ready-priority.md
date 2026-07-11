# Ready 队列 · Planning 认领优先级表

> **生成**：2026-07-11 · **Sprint**：2026-W28  
> **数据源**：`task-registry.yaml`（`status=ready` × 10）+ `scrum-sprint.yaml` + Convoy/WIP 规则  
> **用途**：Sprint Planning 现场认领；认领前须写 `claimed_by` + `supervised_by`

---

## 1. 总览

| 指标 | 值 |
|------|-----|
| Ready 任务数 | **10** |
| 已入 Sprint committed | **2**（L01、L02） |
| 已在执行（非 ready） | ORCH-L01 `in_progress`；E-PERM-L03/L03a 占用 `demo-ui-topic` |
| Ready 估算 token 合计 | **~1.90M**（若全做） |
| Sprint committed 估算 | **~1.20M**（L01 400k + L02 800k） |

---

## 2. 认领优先级（P0 → P4）

| 优先级 | Task ID | 标题（简） | Agent | 仓库 | Sprint | Token | 解锁下游 |
|:------:|---------|-----------|-------|------|:------:|------:|----------|
| **P0** | `E-E7-POLICY-M1-L01` | E7 政策 5 指标 ETL + ADS | data-agent | innov-algo-science | ✅ W28 | 400k | **L03 → L04 → L05…**（政策链核心） |
| **P0** | `E-E7-POLICY-M1-L02` | E7 政策图谱 NER/RE + Nebula | algorithm-agent | demo-algo-ent-analysis | ✅ W28 | 800k | **L04 API** 图谱侧；与 L01 **可并行** |
| **P1** | `E-PROD-UXUE-COMP-L03` | Design.md 栅格体系轻量评审 | coordinator-agent | agent-delivery | — | 40k | 关闭 Design 评审环；无仓冲突 |
| **P1** | `DECIDE-SYSTEMTEST-STACK` | system-test 是否迁 Arco（决策） | architect-agent | agent-delivery | — | 30k | 解除 QA **G-09**；人拍板为主 |
| **P2** | `ENT-REQ-CONFIRM-01` | 企业原型需求确认会 | coordinator-agent | agent-delivery | — | 80k | **解锁 ENT-UE-IA-L01~L08** 整链 |
| **P2** | `E-PERM-L04` | 权限 PM 进度 + Q020~Q030 | coordinator-agent | agent-delivery | — | 60k | 与 E-PERM-L03 并行；**PM 人主导** |
| **P3** | `FIX-EVENTMAP-HEAT-LEGEND` | EventMap 热力图例/空态 | frontend-agent | lumen-ui-science-pc | — | 200k | QA **G-11~G-14**；**独立仓可并行** |
| **P3** | `FE-ENT-OVERVIEW-DRILLDOWN-ACTIONS` | 企业总览下钻/卡片动作 FE | frontend-agent | demo-ui-topic | — | 90k | ENT 总览验收；见 Convoy ⚠️ |
| **P4** | `FIX-A11Y-INFO-POPOVER` | ⓘ Popover 键盘/触屏 | frontend-agent | demo-ui-topic | — | 80k | QA **G-01**；Convoy 串行 |
| **P4** | `FIX-A11Y-PERM-LOCK` | LockedButton/Nav a11y | frontend-agent | demo-ui-topic | — | 120k | QA **G-02/03**；排在 FIX-A11Y-INFO 后 |

---

## 3. Convoy / 并行建议

```text
Lane A（Sprint 主战场 · 可立即并行）
  ├─ E-E7-POLICY-M1-L01   → innov-algo-science      （data lead 监管）
  └─ E-E7-POLICY-M1-L02   → demo-algo-ent-analysis  （algorithm lead 监管）

Lane B（编排 · 已在跑）
  └─ E-PLATFORM-ORCH-L01  → in_progress

Lane C（协调/决策 · 低冲突）
  ├─ E-PROD-UXUE-COMP-L03
  ├─ DECIDE-SYSTEMTEST-STACK  （需 PM+架构师 30min 决策会）
  ├─ E-PERM-L04               （PM 人主导）
  └─ ENT-REQ-CONFIRM-01       （PM 排 90min 评审会，coordinator 收 handoff）

Lane D（独立前端仓 · 可与 Lane A 并行）
  └─ FIX-EVENTMAP-HEAT-LEGEND → lumen-ui-science-pc

Lane E（demo-ui-topic · ⚠️ 串行 Convoy）
  当前占用：E-PERM-L03 in_progress · E-PERM-L03a review（等 PM 批准 push）
  建议顺序：
    1. FE-ENT-OVERVIEW-DRILLDOWN-ACTIONS
    2. FIX-A11Y-INFO-POPOVER
    3. FIX-A11Y-PERM-LOCK
  → 同一 frontend lead 监管，WIP=1
```

---

## 4. Planning 建议认领方案（示例）

> 现场把「负责人」改成真名，写入 `task-registry.supervised_by`。

| 顺序 | Task | 建议监管人 | claim_type | 说明 |
|:----:|------|-----------|------------|------|
| 1 | E-E7-POLICY-M1-L01 | 数据 lead | pull | Sprint **必做**；优先开工 |
| 2 | E-E7-POLICY-M1-L02 | 算法 lead | pull | 与 L01 **同时**认领 |
| 3 | E-PROD-UXUE-COMP-L03 | coordinator 操作者 | pull | 40k，1 会话可关 |
| 4 | DECIDE-SYSTEMTEST-STACK | 架构师 | pull | 先开 30min 决策会再关 task |
| 5 | FIX-EVENTMAP-HEAT-LEGEND | 前端 lead（展示） | pull | 不与 topic 仓冲突 |
| 6 | ENT-REQ-CONFIRM-01 | PM + coordinator | coordinator_dispatch | **人排会**；非纯 Agent |
| 7 | E-PERM-L04 | PM | pull | 全程并行跟踪 |
| 8–10 | FE-ENT / FIX-A11Y×2 | 前端 lead（专题） | pull | **等 L03a PM 签字后**或 swap 进 Sprint |

**不建议本 Sprint 全收 10 项**：token ~1.9M + WIP 易超 4；**P0+P1+Lane D** 为稳妥包。

---

## 5. 认领后立即写入 registry 的字段

```yaml
status: claimed          # 开代码后 → in_progress
sprint_id: "2026-W28"    # 仅 Sprint 承诺项；其余 Planning 时 PM 决定是否 swap 入 Sprint
claimed_by: agent:{role} # 或 human:{真名}
supervised_by: human:{真名}
claim_type: pull         # 或 coordinator_dispatch
claimed_at: "2026-07-14T09:30:00+08:00"
lock_until: "2026-07-14T13:30:00+08:00"
```

---

## 6. 不在 Ready 但 Planning 需知晓

| Task | 状态 | 说明 |
|------|------|------|
| E-PLATFORM-ORCH-L01 | in_progress | Sprint committed，填 `supervised_by` 真名 |
| E-PERM-L03 / L03a | in_progress / review | 占 demo-ui-topic；阻塞 Lane E 并行 |
| E-E7-POLICY-M1-L03 | backlog | **L01 done 后**跑 sync 脚本 → 变 ready（stretch） |

---

## 7. Planning 现场 checklist

- [ ] PM 激活 Sprint：`scrum-sprint.yaml` → `status: active`
- [ ] P0 两项认领并填真名
- [ ] 确认是否 swap P1/P3 进 `committed_task_ids`（超出则 swap 出去）
- [ ] Lane E 是否等 E-PERM-L03a PM 签字 —— PM 拍板
- [ ] 跑 `.\scripts\sync-task-ready-status.ps1`
- [ ] 更新 [`2026-W28.md`](2026-W28.md) burndown

---

**维护**：coordinator · 每次 sync 脚本后或 Ready 数量变化时重生成本节。
