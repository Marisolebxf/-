# 飞书多维表格（Bitable）集成指南 · Phase 0 人类看板

> **为何用 Bitable**：飞书项目需企业申请；Bitable **开箱可用**，10–30 分钟可上线 Kanban。  
> **真源**：`task-registry.yaml`（Agent） · **人类看板**：多维表格看板视图  
> **配置**：`feishu-bitable.yaml` · **脚本**：`scripts/sync-feishu-bitable.ps1`  
> **迁移**：飞书项目审批通过后见 `feishu-project-integration.md`

---

## 1. 架构

```text
task-registry.yaml  ──sync──►  飞书多维表格（看板视图）
       ▲
       └── Agent / Git 真源不变；人只打开 Bitable，不读 MD
```

| 谁 | 看什么 |
|----|--------|
| Agent / coordinator | YAML + MD |
| PM / lead / 全员站会 | **飞书多维表格**（手机/PC） |

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
| Handoff | 文本/链接 | evidence 路径 |

**「状态」单选选项**（与 Kanban 列一致）：

`Backlog` · `Ready` · `已认领` · `进行中` · `评审中` · `已完成` · `阻塞`

4. 新建视图 → **看板** → 分组依据 = **状态**
5. 可选：筛选视图 `Sprint = 2026-W28`

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

```powershell
cd E:\gkx-lumen\gkx-orchestration

# 刷新 Kanban 状态
.\scripts\sync-task-ready-status.ps1

# 预览
.\scripts\sync-feishu-bitable.ps1 -DryRun -SprintId 2026-W28

# 写入 Bitable
.\scripts\sync-feishu-bitable.ps1 -DryRun:$false -SprintId 2026-W28
```

| 时机 | 操作 |
|------|------|
| Planning 后 | sync ready + bitable 全量 Sprint |
| 每日站会前 | 同上 |
| registry 改 status 后 | coordinator 跑 sync |

---

## 4. 人在 Bitable 怎么用

| 可以做 | 不要做 |
|--------|--------|
| 看板看进度、@同事 | 在 Bitable **改 Task ID** |
| 站会口头认领，由 lead 改 registry | 只拖状态不回写 YAML（Phase 1 前） |
| 筛选 Sprint / Epic | 在 Bitable 新增任务代替 registry |

**Phase 1**：Bitable 自动化 → Webhook 回写 registry（可选，后续做）。

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
