# 飞书多维表格（Bitable）集成指南 · Phase 0 人类看板

> **为何用 Bitable**：飞书项目需企业申请；Bitable **开箱可用**，10–30 分钟可上线 Kanban。  
> **真源**：`task-registry.yaml`（Agent） · **人类看板**：多维表格看板视图  
> **配置**：`feishu-bitable.yaml` · **脚本**：`scripts/sync-feishu-bitable*.ps1`  
> **双向同步操作手册（站会必读）**：`feishu-bitable-bidirectional-ops.md`
> **迁移**：飞书项目审批通过后见 `feishu-project-integration.md`

---

## 1. 架构

```text
Phase 0（已实现）:
  task-registry.yaml  ──outbound──►  飞书多维表格

Phase 1（pull 双向）:
  飞书多维表格  ──inbound──►  task-registry.yaml  ──outbound──►  飞书多维表格
       │                              ▲
       └── 人工拖状态/改认领 ──┘
       （监管人由 registry outbound 投影，不在 inbound）
```

| 谁 | 看什么 |
|----|--------|
| Agent / coordinator | YAML + Git（真源） |
| PM / lead / 全员站会 | **飞书多维表格**（改状态后跑 inbound） |

**真源铁律**：`task-registry.yaml` 仍是 Agent 派单真源；Bitable 可回写 **允许字段**（见 `feishu-bitable.yaml#inbound`）。**新增任务**默认进入 `bitable-inbound-proposals.yaml` 队列，由 PM 审阅后并入 registry。

---

## 2. 一次性开通（约 30–60 分钟）

### 2.1 建表（在飞书里操作）

1. 飞书 → **云文档** → 新建 **多维表格**
2. 命名：**GKX 智树任务看板**
3. 建列（列名必须与 `feishu-bitable.yaml#field_names` 一致）：

| 列名 | 类型 | 说明 |
|------|------|------|
| Task ID | 文本 | 主键，如 `E-E7-POLICY-M1-L01` |
| 标题 | 文本 | task title |
| 状态 | **单选** | 选项见下表 |
| Agent | 文本 | |
| Epic | 文本 | |
| Sprint | 文本 | 如 2026-W28 |
| 监管人 | 文本 | 真名 |
| 认领 | 文本 | |
| Token估算 | 数字 | 可选 |
| 优先级 | 单选 | P0/P1/P2… 可选 |
| Handoff | 文本 | outbound 写入 **GitLab blob URL**（见 `handoff_link`） |
| 备注 | 文本 | registry `note`（多行） |
| 验收标准 | 文本 | registry `definition_of_done`（列表拼成多行 `- …`） |
| 贡献分 | 数字 | registry `effort_points`（1/2/3/5/8/13） |
| 难度 | 文本 | registry `difficulty`（S/M/L/XL） |
| **交付阶段** | **单选（推荐）或文本** | registry `delivery_phase`：`定义` / `实现` / `横切` |

> 若表中尚无「备注 / 验收标准 / 贡献分 / 难度 / 交付阶段」，outbound sync 会尝试 **自动建列**（贡献分为数字列，其余为文本；「交付阶段」建议在飞书里改成**单选**并设三选项，便于筛视图）。

**「状态」单选选项**（与 Kanban 列一致）：

`Backlog` · `Ready` · `已认领` · `进行中` · `评审中` · `已完成` · `阻塞`

**「交付阶段」选项**（与 `delivery_phase_map` 一致）：

`定义` · `实现` · `横切`

4. 新建视图 → **看板** → 分组依据 = **状态**
5. 可选：筛选视图 `Sprint = 2026-W28`
6. **定义/实现分流视图（推荐）**：见 §2.1.1

### 2.1.1 定义 / 实现分组视图（2026-07-21）

一张表、多视图；规程真源分别为 `产品定义评审规程.md` 与 `产品实现规程.md`。

| 视图名（建议） | 类型 | 筛选 / 分组 |
|----------------|------|-------------|
| **定义看板** | 看板 | 筛选 `交付阶段 = 定义`；分组 = **状态** |
| **实现看板** | 看板 | 筛选 `交付阶段 = 实现`；分组 = **状态**；可再筛当前 Sprint |
| **模块总览** | 表格 | 分组 = **功能模块** → **交付阶段** |

- registry 字段：`delivery_phase: definition | implementation | crosscut`
- 缺省时 sync / `scripts/backfill-delivery-phase.mjs` 按 `feishu-bitable.yaml#delivery_phase_classify` 推断
- Planning：未标阶段且无法推断的 task，coordinator 补写后再进 committed

### 2.2 获取 app_token / table_id

- 打开多维表格，URL 形如：  
  `https://xxx.feishu.cn/base/**AppToken**?table=**TableId**&view=...`
- 或：表格右上角「…」→ 高级设置 / API 说明

### 2.3 飞书开放平台自建应用

1. 打开 https://open.feishu.cn/app → **创建企业自建应用**
2. 权限（至少）：
   - `bitable:app` — 查看、编辑多维表格
   - 或细分：`base:record:read` / `base:record:write`
3. **发布**应用（版本管理 → 申请发布，或开发态仅管理员可用）
4. **重要**：打开该多维表格 → 分享 → 把 **应用机器人** 加为 **可编辑** 协作者
5. 凭证 → 复制 **App ID**、**App Secret** → 写入本地 `.env`

```env
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxx
```

### 2.4 填写 `feishu-bitable.yaml`

```yaml
bitable:
  app_token: "你的AppToken"
  table_id: "tblxxxxxxxx"
sync:
  enabled: false    # DryRun 通过后改 true
```

---

## 3. 同步命令

> **站会/日常双向同步**：见 **[feishu-bitable-bidirectional-ops.md](./feishu-bitable-bidirectional-ops.md)**（DryRun → 正式 → 验收完整流程）。

```powershell
cd F:\gkx-lumen\gkx-orchestration

# 刷新 Kanban 状态（registry 内）
.\scripts\sync-task-ready-status.ps1

# --- Outbound：registry → Bitable ---
.\scripts\sync-feishu-bitable.ps1 -DryRun -SprintId 2026-W28
.\scripts\sync-feishu-bitable.ps1 -DryRun:$false -SprintId 2026-W28

# --- Inbound：Bitable → registry（Phase 1）---
.\scripts\sync-feishu-bitable-inbound.ps1 -DryRun
.\scripts\sync-feishu-bitable-inbound.ps1 -DryRun:$false

# --- 双向（推荐：先 inbound 再 outbound）---
.\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun
.\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun:$false -SprintId 2026-W28
```

| 时机 | 操作 |
|------|------|
| 站会前（人改过 Bitable） | **bidirectional** 或 inbound → outbound |
| Planning 后 | outbound 全量 Sprint |
| registry 改 status 后 | outbound |
| Bitable 新增行 | inbound → 审阅 `bitable-inbound-proposals.yaml` |

---

## 4. 人在 Bitable 怎么用

| 可以做 | 不要做 |
|--------|--------|
| 看板看进度、@同事 | 在 Bitable **改 Task ID** |
| 拖状态 / 改认领 / Sprint / **优先级** → 跑 **inbound** 回写 registry | 改 **Agent / Epic / Token**（不会回写；下次 outbound 覆盖） |
| 筛选 Sprint / Epic / 功能模块 | 指望 **新增行自动进 registry**（默认仅进提案队列） |
| 站会口头认领后，在 Bitable 填「认领」再 inbound | 在 Bitable 手改「监管人」指望回写 YAML（**监管人以 registry 为准**） |
| coordinator 在 registry 填 `supervised_by` → watch/outbound 自动投影飞书 | 只拖状态不回写 YAML |

**Phase 2（方案 B · 已落地 Handler）**：飞书 Bitable 自动化 Webhook → 单条 inbound → scan → pending → confirm。运维见 [`feishu-bitable-webhook-handler.md`](feishu-bitable-webhook-handler.md) · 设计 [`RFC/RFC-003-feishu-bitable-webhook.md`](RFC/RFC-003-feishu-bitable-webhook.md)。

---

## 5. 探测脚本

```powershell
.\scripts\feishu-bitable-discover.ps1 -AppToken "xxx" -TableId "tblxxx"
```

列出表字段，核对列名与 yaml 一致。

---

## 6. 与 Scrum 对齐

- Sprint 容器仍在 `scrum-sprint.yaml`
- Bitable 用 **Sprint 列** + 筛选视图代替飞书「迭代」
- `2026-W28` committed 任务 sync 时可加筛选 `-SprintId 2026-W28`

---

## 7. 迁回飞书项目（将来）

飞书项目开通后：

1. 跑 `sync-feishu-project.ps1` 替代 bitable sync  
2. `task-registry#scrum_policy.human_board` 改为 `feishu_project`  
3. Bitable 表归档只读  

---

## 8. 故障排查

| 现象 | 处理 |
|------|------|
| 1254043 等无权限 | 应用加入表格协作者；检查 bitable 权限 |
| 状态写不进去 | Bitable「状态」选项文字与 status_map 不一致 |
| 重复行 | Task ID 列保证唯一；先删重复再 sync |
| token 失败 | App ID/Secret 或应用未发布 |

---

**维护**：列名变更时同步改 `feishu-bitable.yaml#field_names`。
