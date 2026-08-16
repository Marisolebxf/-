# 飞书项目集成指南（GKX 智树 · Scrum/看板）

> **状态：⏸ 暂缓** — 飞书项目需企业申请；当前 Phase 0 请用 **[feishu-bitable-integration.md](feishu-bitable-integration.md)**。  
> 审批通过后按本文档迁移，并改 `task-registry#scrum_policy.human_board` → `feishu_project`。

> **读者**：PM、coordinator、DevOps  
> **真源**：`task-registry.yaml`（Agent / Git）  
> **人类看板**：飞书项目（Scrum 迭代 + 看板视图）  
> **配置**：[`feishu-project.yaml`](./feishu-project.yaml) · **脚本**：`scripts/sync-feishu-project.ps1`

---

## 1. 架构

```text
task-registry.yaml  ──sync──►  飞书项目工作项（人读、站会、@人）
       ▲                              │
       └──────── webhook（Phase 2）────┘
              状态/负责人回写（PM 规则）
```

| 层 | 载体 | 谁用 |
|----|------|------|
| 机器真源 | YAML + Git | Agent、coordinator、CI |
| 人类 Scrum | 飞书项目迭代 + 看板 | PM、lead、全员 |
| Agent 文档 | MD handoff | Agent（不必同步到飞书正文） |

---

## 2. 一次性开通（约 2–4 小时）

### 2.1 飞书项目空间

1. 打开 [飞书项目](https://project.feishu.cn)，创建空间（建议名：**GKX 智树交付**）
2. 启用 **敏捷 / Scrum** 模板（迭代 + 看板 + 甘特）
3. 创建当前迭代：**2026-W28**（与 `scrum-sprint.yaml` 对齐）
4. 双击空间名称 → 复制 **project_key**（或 simple_name）

### 2.2 开放平台插件

1. 飞书项目 → **开发者后台** → 创建**插件**
2. 记录 **Plugin ID**、**Plugin Secret**
3. 申请 OpenAPI 权限（工作项读写、搜索、状态变更）
4. 将插件**安装到**上一步的空间
5. 左下角双击头像 → 复制 **user_key**

### 2.3 自定义字段（防重复同步）

在空间的工作项类型（建议 Story/Task）中新增字段：

| 字段名 | 别名 alias | 类型 | 用途 |
|--------|------------|------|------|
| GKX Task ID | `gkx_task_id` | 文本 | 存 `E-E7-POLICY-M1-L01` 等，upsert 主键 |

可选字段（人类可读）：

| 字段名 | 类型 | 映射 registry |
|--------|------|---------------|
| Agent | 单选/文本 | `agent` |
| 监管人 | 文本 | `supervised_by` |
| Sprint | 文本 | `sprint_id` |
| Epic | 文本 | `epic` |

### 2.4 状态与 Kanban 列

在飞书项目工作流中配置状态，与 `task_state_machine` 对齐：

| registry status | 飞书状态（示例） |
|-----------------|------------------|
| backlog | Backlog |
| ready | Ready |
| claimed | 已认领 |
| in_progress | 进行中 |
| review | 评审中 |
| done | 已完成 |
| blocked | 阻塞 |

将 `state_key` 填入 `feishu-project.yaml#status_map`（discover 脚本或工作项配置中查看）。

### 2.5 本地凭证（`.env`，不入 git）

```env
FEISHU_PROJECT_PLUGIN_ID=MII_xxxxxxxx
FEISHU_PROJECT_PLUGIN_SECRET=xxxxxxxx
FEISHU_PROJECT_USER_KEY=7568516887894324252
```

模板见 `gkx-orchestration/.env.example`。

---

## 3. 配置与探测

### 3.1 填写 `feishu-project.yaml`

```yaml
project:
  project_key: "your_project_key"
  work_item_type_key: "story"
sync:
  enabled: false          # 首次 DryRun 通过后改 true
  external_id:
    feishu_field_key: "field_xxxx"   # gkx_task_id 的 field_key
```

### 3.2 运行 discover

```powershell
cd F:\gkx-lumen\gkx-orchestration
.\scripts\feishu-project-discover.ps1 -ProjectKey "your_project_key" -WorkItemTypeKey story
```

输出工作项类型列表 + 字段 `field_key`，回填 yaml。

---

## 4. 同步节奏（coordinator 操作）

| 时机 | 命令 |
|------|------|
| Planning 后 | `.\scripts\sync-task-ready-status.ps1` 然后 `.\scripts\sync-feishu-project.ps1 -DryRun -SprintId 2026-W28` |
| 确认无误 | `.\scripts\sync-feishu-project.ps1 -DryRun:$false -SprintId 2026-W28` |
| 每日站会前 | `sync-task-ready-status.ps1` → `sync-feishu-project.ps1 -DryRun:$false` |
| registry 大改后 | 同上 |

**首次务必 `-DryRun`**，确认 CREATE/UPDATE 列表后再写飞书。

---

## 5. 人在飞书怎么用

| 动作 | 在哪里 | 是否回写 YAML |
|------|--------|---------------|
| 看 Sprint 看板 | 飞书项目 → 迭代 2026-W28 → 看板 | — |
| @监管人 | 工作项负责人字段 | Phase 2 webhook |
| 拖状态 | 看板列 | Phase 2（PM 规则） |
| 改 scope/DoD | **不要**在飞书改 | 只改 registry |

站会：**只打开飞书项目**，不必读 `sprints/*.md`。

---

## 6. Phase 2 · Webhook 回写（可选）

飞书项目 → 插件 → **监听事件** → 回调 URL（内网或 GitLab CI 服务）：

| 事件 | 用途 |
|------|------|
| WorkitemStatusEvent (3001) | 拖看板 → 更新 registry `status` |
| WorkitemPersonAssignedEvent | 更新 `supervised_by` |

策略见 `feishu-project.yaml#webhook`：**冲突以 task-registry 为准**，飞书变更需映射且可 PM 审批。

实现路径（择一）：

- **n8n** + [飞书项目节点](https://github.com/luka-n8n-nodes/n8n-nodes-feishu-project) → 调脚本改 YAML → Git commit
- 自建 `feishu-webhook-handler`（Go/Node）→ 同上
- GitLab CI：`push task-registry` 仍为出方向主触发，webhook 仅入方向

---

## 7. 字段对照速查

| task-registry | 飞书工作项 |
|---------------|-----------|
| `id` | `gkx_task_id` + 标题前缀 |
| `title` | 名称 |
| `status` | 状态 / 看板列 |
| `supervised_by` | 负责人（需映射飞书用户） |
| `sprint_id` | 迭代 |
| `agent` | 自定义字段 |
| `feishu_work_item_id` | 飞书工作项 ID（registry 回写，加速 update） |

---

## 8. 故障排查

| 现象 | 处理 |
|------|------|
| plugin_token 失败 | 检查 Plugin ID/Secret；插件是否安装到空间 |
| 403 / 无权限 | 开发者后台给插件加 API 权限并重新安装 |
| 搜不到已有项 | 确认 `gkx_task_id` field_key 填对 |
| 重复创建工作项 | 先补 `feishu_work_item_id` 或 `gkx_task_id` 字段 |
| 状态拖不动 | `status_map.state_key` 与空间工作流不一致，重跑 discover |

错误码：[飞书项目 OpenAPI FAQ](https://www.feishu.cn/content/60bl79n2)

---

## 9. 相关文件

| 文件 | 作用 |
|------|------|
| `feishu-project.yaml` | 映射与开关 |
| `scrum-sprint.yaml` | Sprint 与飞书迭代对齐 |
| [`../task-claiming-guide.md`](../task-claiming-guide.md) | 认领字段名词 |
| `scripts/sync-feishu-project.ps1` | YAML → 飞书 upsert |
| `scripts/feishu-project-discover.ps1` | 探测 field_key |

---

**维护**：Sprint retro 时核对状态映射；空间工作流变更后更新 `feishu-project.yaml`。
