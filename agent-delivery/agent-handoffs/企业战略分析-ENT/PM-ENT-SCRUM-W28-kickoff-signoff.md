# PM-ENT-SCRUM-W28-kickoff · 企业维度 Sprint 启动会签收

> **Sprint ID**：`2026-W28`
> **会议日期**：2026-07-07（Planning）；书面补录：2026-07-13
> **主持**：郭万迎
> **Sprint Owner**：高颖（`human:高颖`）
> **参会**：郭万迎、高颖、徐滕强、孔东、侯佳伟（可选）、coordinator
> **容器真源**：[`scrum-sprint.yaml`](../../scrum-sprint.yaml) · [`sprints/2026-W28.md`](../../sprints/2026-W28.md)
> **详表**：[`ent-scrum-pdr-backlog.md`](../../sprints/ent-scrum-pdr-backlog.md)
> **Task ID**：`ENT-SCRUM-W28-KICKOFF`

---

## 1. Sprint Goal（会上宣读 · 与 scrum-sprint.yaml 一致）

门 1 已通过的三模块（**搜索 / 对比篮 / 企业详情**）完成 **V1 高保真会签**；**徐滕强**牵头功能实现架构设计；补录 PDR 纪要与客户决策清单；**V1 完成后**启动 **V2 lumen 准生产**（孔东团队 · `lumen-ui-science-topic` dev）。

**周期**：2026-07-07 ~ 2026-07-20（双周 · ISO 周 W27–W28）

---

## 2. Committed（本 Sprint 承诺）

| 优先级 | Task ID | 标题 | Agent | supervised_by | 启动会时状态 | 2026-07-13 实况 |
|--------|---------|------|-------|---------------|--------------|-----------------|
| P0 | ENT-MOD-SEARCH-V1-HIFI | 企业查询 V1 高保真 | ui-agent | 高颖 | ready | **in_progress** |
| P0 | ENT-MOD-COMPARE-V1-HIFI | 对比篮 V1 高保真 | ui-agent | 高颖 | ready | **in_progress** |
| P0 | ENT-MOD-PROFILE-V1-HIFI | 企业详情 V1 高保真 | ui-agent | 高颖 | ready | ready |
| P0 | ENT-ARCH-IMPL-DESIGN | 企业功能实现架构设计 | architect-agent | 徐滕强 | ready | **in_progress** |
| P1 | ENT-PDR-MINUTES-TRIO | 补录三门 PDR 纪要 | coordinator-agent | 郭万迎 | ready | **claimed**（纪要已落盘；TRACE 待补） |

**门 1 已通过（不计入 Committed 执行，已 done）**：`ENT-MOD-SEARCH-PDR-G1`、`ENT-MOD-COMPARE-PDR-G1`、`ENT-MOD-PROFILE-PDR-G1`

---

## 3. Stretch（有余力）

| Task ID | 标题 | supervised_by | 说明 |
|---------|------|---------------|------|
| ENT-MOD-SEARCH-V2-DEMO | 搜索 V2 lumen 准生产 | 孔东 | V1 通过后；已提前 in_progress |
| ENT-MOD-COMPARE-V2-DEMO | 对比篮 V2 | 孔东 | backlog |
| ENT-MOD-PROFILE-V2-DEMO | 画像 V2 | 孔东 | backlog |
| ENT-ARCH-API-CONTRACT | OpenAPI 契约草案 | 侯佳伟 | 依赖 ARCH；backlog |
| ENT-ALGO-DEMO-L01 | 算法全集 + /entan 对齐 /policy | 唐绍祖 | 2026-07-13 调度加活；claimed |
| CHAIN-MOD-PDR-G1 等 | 产业链 PDR 占位 | — | 非企业专班主路径 |

---

## 4. 明确不做（本 Sprint）

| 项 | 说明 |
|----|------|
| OVERVIEW / KEYENT / EVAL / RISK / RECRUIT / EXPORT / OPS | 待门 1 PDR；不进 W28 committed |
| 企业总览等 7 模块 USM | 高颖完成五件套后再排门 1 |
| Silent 加活 | 新 task 须 PM 写入 sprint backlog 或 swap（`scrum-sprint.yaml` 铁律） |

---

## 5. 仪式日历

| 仪式 | 时间 | 参与 |
|------|------|------|
| **Sprint Planning** | 2026-07-07（一）90min | 郭万迎 + 高颖 + 孔东 + coordinator |
| **Daily Standup** | 每工作日 09:30 · 15min | 企业专班 + leads |
| **Sprint Review** | 2026-07-20 前 | 汇总 `done` task + demo 链接 |
| **V2 lumen 会签** | W28 第 2 周 | 高颖 + 孔东团队 |
| **Retro** | 2026-07-18（五）60min | 全员 |

---

## 6. 风险与依赖

| # | 风险 | 升级 | 清单 / 纪要 |
|---|------|------|-------------|
| R1 | `TRACE-ENT-*.yaml` 三份未落盘 | 高颖 + coordinator | PDR-01/03 🟡 |
| R2 | 会议定稿 vs 规格差异（列表/导出/高筛） | 郭万迎 | Q033~Q037、客户决策清单 §2.6 |
| R3 | V2 不得先于 V1 过门 2（规程 §11） | 孔东 + 高颖 | DECIDE-FE-V2-LUMEN-DIRECT |
| R4 | 7 模块待 PDR 阻塞总览等 FE 任务 | 郭万迎 + 高颖 | `ent-scrum-pdr-backlog.md` §2 |

---

## 7. Planning 检查清单（启动会当场确认）

- [x] `scrum-sprint.yaml#2026-W28.status` → **`active`**（2026-07-13 补录）
- [x] Committed 五项 `sprint_id` + `supervised_by` 已写入 `task-registry.yaml`
- [ ] 飞书看板 W28 列与 registry 对齐（coordinator outbound sync）
- [x] 站会三问纳入 Daily（见 `ent-scrum-pdr-backlog.md` §6）
- [ ] `sync-task-ready-status.ps1` 每日站会前执行（持续）
- [ ] TRACE 三份落盘 → `ENT-PDR-MINUTES-TRIO` 闭合

---

## 8. 站会三问（企业专班）

1. **门 1 三模块**：V1 进度？V2 何时开？ARCH 契约有无阻塞？
2. **待 PDR 模块**：哪几个 USM/TRACE 能在 Sprint N+1 上门 1？
3. **飞书看板**：committed task 是否已 sync？认领是否填 `supervised_by` 真名？

---

## 9. 签字

| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| 合规 Owner / 主持 | 郭万迎 | | |
| Sprint Owner / 体验 | 高颖 | | |
| 架构 | 徐滕强 | | |
| 前端 V2 | 孔东 | | |
| coordinator | coordinator-agent | | 2026-07-13 |
