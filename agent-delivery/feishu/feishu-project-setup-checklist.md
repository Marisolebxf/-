# 飞书项目开通 · 分步清单（教练 Agent 逐步引用）

> **教练 Prompt**：`feishu-project-setup-coach-prompt.md`  
> **预计总时长**：2–4 小时（可分多次会话）

---

## 阶段 A · 空间与 Scrum（30–45 min）

| 步 | 动作 | 完成标志 | 产出 |
|----|------|----------|------|
| A1 | 打开 https://project.feishu.cn ，创建空间「GKX 智树交付」 | 能进入空间首页 | 空间已存在 |
| A2 | 选择 **敏捷 / Scrum** 模板（或空间设置中启用迭代+看板） | 左侧有「迭代」「看板」 | 模板就绪 |
| A3 | 新建迭代：**2026-W28**，日期 2026-07-14 ~ 2026-07-27 | 迭代列表可见 | 与 scrum-sprint.yaml 一致 |
| A4 | **双击空间名称**复制 project_key | 得到一串 key 或 simple_name | → 回填 yaml `project.project_key` |
| A5 | 创建看板视图（按状态分列） | 能拖拽卡片 | 人类站会视图 |

---

## 阶段 B · 开放平台插件（45–60 min）

| 步 | 动作 | 完成标志 | 产出 |
|----|------|----------|------|
| B1 | 飞书项目 → **开发者后台**（或开放平台）→ 创建插件 | 有 Plugin ID | Plugin 记录 |
| B2 | 复制 **Plugin Secret**（仅本地保存） | 已写入 `.env` 本地 | 不入 git、不发聊天 |
| B3 | 插件 → **权限管理** → 勾选工作项读/写/搜索/状态变更 | 权限列表已保存 | API 可调 |
| B4 | 插件 → **安装到空间** → 选 A1 的空间 | 空间内可见已安装插件 | 安装成功 |
| B5 | 空间左下角 **双击个人头像** → 复制 user_key | 得到数字 user_key | → `.env` FEISHU_PROJECT_USER_KEY |

**Plan B**：若无开发者后台入口 → 联系企业管理员开通「飞书项目开放平台」或使用企业 IT 代建插件。

---

## 阶段 C · 工作项字段（30 min）

| 步 | 动作 | 完成标志 | 产出 |
|----|------|----------|------|
| C1 | 空间 → **工作项配置** → 选 Story/Task 类型 | 进入字段列表 | — |
| C2 | 新增文本字段 **GKX Task ID**，alias `gkx_task_id` | 创建成功 | upsert 主键 |
| C3 | （可选）新增：Agent、监管人、Sprint、Epic 文本字段 | 字段可见 | 人类可读 |
| C4 | 运行 discover 脚本获取 `field_key` | 终端输出 field_key | → yaml `sync.external_id.feishu_field_key` |

```powershell
cd F:\gkx-lumen\gkx-orchestration
# .env 已填凭证后：
.\scripts\feishu-project-discover.ps1 -ProjectKey "<你的project_key>" -WorkItemTypeKey story
```

---

## 阶段 D · 工作流 / 状态（30–45 min）

| 步 | 动作 | 完成标志 | registry 对应 |
|----|------|----------|---------------|
| D1 | 工作项配置 → **工作流/状态** | 状态列表可编辑 | — |
| D2 | 确保存在（或新建）以下状态 | 7 态齐全 | 见下表 |
| D3 | 看板列绑定状态 | 拖卡片可改状态 | Kanban |
| D4 | 记录每个状态的 **state_key** | 填入 feishu-project.yaml#status_map | 脚本 Phase2 用 |

| registry status | 建议飞书状态名 |
|-----------------|----------------|
| backlog | Backlog |
| ready | Ready |
| claimed | 已认领 |
| in_progress | 进行中 |
| review | 评审中 |
| done | 已完成 |
| blocked | 阻塞 |

---

## 阶段 E · 本地配置与首次同步（30 min）

| 步 | 动作 | 完成标志 |
|----|------|----------|
| E1 | 编辑 `gkx-orchestration/.env` 三项 FEISHU_PROJECT_* | discover 不报错 |
| E2 | 编辑 `feishu-project.yaml`：project_key、feishu_field_key | yaml 完整 |
| E3 | `sync-feishu-project.ps1 -DryRun -SprintId 2026-W28` | 列出 CREATE/UPDATE |
| E4 | `-DryRun:$false` 写入飞书 | 看板出现 Sprint 任务 |
| E5 | `scrum-sprint.yaml` → status: active | Sprint 正式开工 |

---

## 配置回填表（教练会话结束时填写）

| 项 | 值 |
|----|-----|
| 空间名称 | |
| project_key | |
| work_item_type_key | |
| gkx_task_id field_key | |
| 飞书迭代 2026-W28 ID | |
| DryRun 通过时间 | |
| 首次 sync 任务数 | |

---

## 常见问题速查

| 问题 | 处理 |
|------|------|
| 找不到开发者后台 | 企业版权限；找管理员 |
| 插件装不上空间 | 确认插件发布状态 + 空间管理员 |
| discover 401/403 | 权限未开或插件未安装 |
| 看板无卡片 | 先 DryRun:$false；检查 sprint_id 过滤 |
