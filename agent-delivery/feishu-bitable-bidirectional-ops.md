# 飞书多维表格 ↔ task-registry 双向同步 · 操作手册

> **读者**：PM、lead、coordinator、站会主持人  
> **配置真源**：`feishu-bitable.yaml` · **开通指南**：`feishu-bitable-integration.md`  
> **看板**：[GKX 智树任务看板](https://hcnci7146fwq.feishu.cn/base/JI94bBxwsaIzyMsMBrYcPJscnDc?table=tblb65lPULz31h9U)  
> **2026-07-28**：飞书改为**纯看板**（`inbound.enabled=false`）。下表「Inbound」默认关闭；改任务请改 registry / `update-task-status`。

---

## 1. 两个方向（必记）

| 方向 | 脚本 | 数据流 | 何时跑 |
|------|------|--------|--------|
| **Inbound（入站）** | `sync-feishu-bitable-inbound.ps1` | 飞书 → registry | **已默认关闭**；仅逃生阀 `-AllowInbound` / 临时改 yaml |
| **Outbound（出站）** | `sync-feishu-bitable.ps1` / `board-task-status --watch-outbound` | registry → 飞书 | Agent/coordinator **改 registry** 之后；K8s/投影机定时兜底 |

**推荐（纯看板）**：

```powershell
cd F:\gkx-lumen\gkx-orchestration
# 出站投影（registry → 飞书，含状态/认领）
.\scripts\board-sync-watch.ps1
# 或
node scripts/lib/board-task-status.mjs --watch-outbound
```

内部顺序（默认）：

1. ~~inbound~~（跳过：`feishu-bitable.yaml#inbound.enabled=false`）  
2. `sync-task-ready-status`（可选）  
3. outbound **全量**投影看板字段（registry 真源盖飞书展示）  

Webhook 仍接受 `action=dispatch_confirm|reject` / `gap_proposal_*`（派单门控，不是看板字段同步）。  
记录变更类 webhook（拖状态）会 **skipped**，不写 registry。

---

## 2. 前置条件（每次同步前自检）

- [ ] 本地 `gkx-orchestration/.env` 已配置 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`（**勿提交 Git**）
- [ ] `feishu-bitable.yaml` 中 `app_token`、`table_id` 已填
- [ ] 飞书应用对表格有 **可编辑 / 文档应用** 权限
- [ ] PowerShell 可执行脚本（`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` 已设一次即可）
- [ ] 工作目录：`${GKX_ROOT}\gkx-orchestration`

---

## 3. 标准操作流程（DryRun → 正式 → 验收）

### 3.1 预览（必做）

```powershell
cd F:\gkx-lumen\gkx-orchestration

# 方式 A：双向一次预览（推荐）
.\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun -SprintId 2026-W28

# 方式 B：分步预览
.\scripts\sync-feishu-bitable-inbound.ps1 -DryRun
.\scripts\sync-feishu-bitable.ps1 -DryRun -SprintId 2026-W28
```

**看什么**：

| 输出 | 含义 |
|------|------|
| `[DRY] UPDATE registry \| TASK-ID \| status=..., claimed_by=...` | Inbound 将回写 registry |
| `[DRY] CREATE/UPDATE \| TASK-ID` | Outbound 将写入/更新 Bitable 行 |
| `[QUEUE] ...` | Bitable 新行进入 `bitable-inbound-proposals.yaml`，**不进 registry** |
| `[SKIP] ...` | 跳过（Task ID 无效或不在 registry） |
| `Done. registry_updates=N` | Inbound 将改 N 条 registry |

### 3.2 正式执行

```powershell
# 当前 Sprint 站会（常用）
.\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun:$false -SprintId 2026-W28

# 全量（Planning 后 / 首次铺底）
.\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun:$false
```

### 3.3 验收

```powershell
# 1. 看 registry  diff
git diff agent-delivery/task-registry.yaml

# 2. 打开飞书看板，核对 Task ID / 状态 / 认领 / 功能模块
# 3. 若有 inbound 改动，由 PM/lead 评审后 commit
git add agent-delivery/task-registry.yaml
git commit -m "chore(registry): sync from Feishu Bitable inbound [human:姓名]"
git push
```

---

## 4. 场景手册

### 场景 A · 站会认领（已验证示例）

**人工操作（飞书）**：

1. 找到任务，例如 `ENT-REQ-CONFIRM-01`
2. 看板拖到 **已认领**
3. **认领** 列选人员；**监管人** 列填姓名或 `@姓名`
4. 可选：**Sprint** 列填 `2026-W28`

**同步命令**：

```powershell
cd F:\gkx-lumen\gkx-orchestration
.\scripts\sync-feishu-bitable-inbound.ps1 -DryRun
# 确认出现：ENT-REQ-CONFIRM-01 | status=claimed, claimed_by=human:高颖
.\scripts\sync-feishu-bitable-inbound.ps1 -DryRun:$false
git diff agent-delivery/task-registry.yaml
```

**registry 预期**：

```yaml
status: claimed
claimed_by: human:高颖
feishu_bitable_record_id: rec...
```

### 场景 B · Coordinator 只改了 registry（Agent 派单）

**无需 inbound**；`board-sync-watch` / 带 `-FeishuAuthoritative` 的双向 sync 会 **自动把 `supervised_by` 投影到飞书「监管人」列**（registry 真源）。

若需同时投影状态/认领/Sprint，跑 **不带** `-FeishuAuthoritative` 的全量 outbound：

```powershell
.\scripts\sync-task-ready-status.ps1
.\scripts\sync-feishu-bitable.ps1 -DryRun:$false -SprintId 2026-W28
```

### 场景 C · 站会前后完整闭环（推荐节奏）

| 时点 | 操作 |
|------|------|
| 站会前 5 分钟 | 人在 Bitable 更新状态/认领 |
| 站会开始 | `-DryRun` 预览 → 站会上念变更 |
| 站会结束 | `-DryRun:$false` 双向 sync → `git commit` registry |
| 日间 Agent 改 registry | 仅 outbound |

### 场景 D · Bitable 新增一行

- **不会**自动写入 `task-registry.yaml`
- Inbound 写入 **`bitable-inbound-proposals.yaml`**
- PM 审阅后手工在 registry 新增 task，再 outbound

---

## 5. 字段同步边界

> **真源分工（2026-07-21）**：`supervised_by`（监管人）= **registry → 飞书**；`claimed_by`（认领）= **飞书 → registry**。详见 `feishu-bitable.yaml#field_authority`。

### 5.1 Inbound 会回写 registry 的字段

| Bitable 列 | registry 字段 | 说明 |
|------------|---------------|------|
| 状态 | `status` | 7 项中文/英文与 `status_map` 一致 |
| 认领 | `claimed_by` | User 人员列 → `human:姓名`（**飞书真源**） |
| Sprint | `sprint_id` | 如 `2026-W28` |
| 优先级 | `priority` | 如 `P0` / `P1` / `P2`（单选选项名与 Bitable 一致） |
| 标题 | `title` | 可选 |
| （系统） | `feishu_bitable_record_id` | 首次绑定 Bitable 行 |

> **监管人**不在 inbound 范围：coordinator 在 registry 维护 `supervised_by`，由 outbound 写入飞书；在 Bitable 手改「监管人」**不会**回写 YAML，下次 outbound 会被 registry 覆盖。

### 5.2 人员字段（registry ↔ Bitable）

| Bitable 列 | 类型 | registry 字段 | 真源 | outbound（FeishuAuthoritative） |
|------------|------|---------------|------|-----------------------------------|
| **认领** | User 人员 | `claimed_by` | **飞书** | **不写出站**（inbound 回写 registry） |
| **监管人** | 文本 | `supervised_by` | **registry** | **始终**写 `@姓名` |

> 2026-07-12：已删除「监管人 (人员 )」列；监管人仅保留文本列。

**首次 / 新成员**：从看板已有 @人员 采集 open_id：

```powershell
.\scripts\feishu-bitable-harvest-person-ids.ps1
# 写入 agent-delivery/feishu-user-map.yaml（已采集：郭万迎、孔东、高颖）
```

若 outbound 出现 `[WARN] no feishu_open_id`，先让人在 Bitable 手动 @ 一次，再跑 harvest。

### 5.3 仅 Outbound 投影（不要在 Bitable 手改）

`Agent`、`Epic`、`功能模块`、`Token估算`、`Handoff` — 下次 outbound 会覆盖 Bitable。

**Handoff**：outbound 将 registry `evidence`（或缺省时的 `agent-handoffs/...` 路径）转为 GitLab blob 可点击链接，例如：

`https://gitlab.htmisoft.net/gkx-lumen/gkx-orchestration/-/blob/dev/agent-delivery/agent-handoffs/....md?ref_type=heads`

配置见 `feishu-bitable.yaml#handoff_link`。

`priority` 已支持 **Inbound 回写**；若 registry 无 `priority` 字段，outbound 不会清空 Bitable 已有值（未写入该列）。

### 5.4 禁止在 Bitable 修改

**Task ID**（主键；改了会导致 duplicate 或 sync 找不到）

---

## 6. 状态对照表

| registry `status` | Bitable「状态」 |
|-------------------|-----------------|
| backlog | Backlog |
| ready | Ready |
| claimed | 已认领 |
| in_progress | 进行中 |
| review | 评审中 |
| done | 已完成 |
| blocked | 阻塞 |

---

## 7. 命令速查

```powershell
cd F:\gkx-lumen\gkx-orchestration

# ★ 双向（站会常用）
.\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun -SprintId 2026-W28
.\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun:$false -SprintId 2026-W28

# 仅入站
.\scripts\sync-feishu-bitable-inbound.ps1 -DryRun
.\scripts\sync-feishu-bitable-inbound.ps1 -DryRun:$false

# 仅出站
.\scripts\sync-task-ready-status.ps1
.\scripts\sync-feishu-bitable.ps1 -DryRun:$false -SprintId 2026-W28
.\scripts\sync-feishu-bitable.ps1 -DryRun:$false          # 全量

# 列名/权限/人员 open_id 排查
.\scripts\feishu-bitable-discover.ps1 -AppToken "JI94bBxwsaIzyMsMBrYcPJscnDc" -TableId "tblb65lPULz31h9U"
.\scripts\feishu-bitable-harvest-person-ids.ps1
```

---

## 8. 故障排查

| 现象 | 处理 |
|------|------|
| `禁止运行脚本` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `1254043` / 无权限 | 表格 **添加文档应用**，权限可管理/可编辑 |
| `FieldNameNotFound` | `discover` 核对列名与 yaml `field_names`；缺列在 Bitable 补列 |
| Inbound 只更新 `feishu_bitable_record_id` | 正常；状态/认领未改或与 registry 已一致 |
| `claimed_by=human:@姓名` | 已自动去 `@`；确认 registry 为 `human:姓名` |
| 非法状态跳转 WARN | 默认仍写入；要更严改 yaml `validate_transitions: strict` |
| 重复 Bitable 行 | Task ID 去重后 outbound；保证每 Task ID 唯一 |

---

## 9. 与 Git / Agent 的纪律

1. **registry 变更必须 commit + push**，Agent/coordinator 才能读到最新状态  
2. **不要**只在 Bitable 改完不跑 inbound — Phase 1 为 **pull**，非实时  
3. **新任务**必须 PM 批准进 registry，禁止 silent 加活（见 `scrum-sprint.yaml`）  
4. commit message 建议：`chore(registry): bitable inbound sync [human:姓名]`

---

## 10. 相关文件

| 文件 | 作用 |
|------|------|
| `agent-delivery/feishu-bitable.yaml` | 列名、状态映射、inbound 策略 |
| `agent-delivery/task-registry.yaml` | 机器真源 |
| `agent-delivery/bitable-inbound-proposals.yaml` | 新任务提案队列 |
| `agent-delivery/scrum-sprint.yaml` | 当前 Sprint ID |
| `scripts/sync-feishu-bitable-bidirectional.ps1` | 双向一键脚本 |

---

**维护**：PM + coordinator · 列名/状态变更时同步改 `feishu-bitable.yaml`。
