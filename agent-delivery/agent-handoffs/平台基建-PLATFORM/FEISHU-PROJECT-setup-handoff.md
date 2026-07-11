# FEISHU-PROJECT · 飞书项目开通会话 handoff（模板）

> **状态**：进行中 / 已完成  
> **教练会话**：用户 + feishu-setup-coach agent  
> **关联**：`feishu-project-integration.md` · `feishu-project.yaml`

## 进度

| 阶段 | 状态 | 备注 |
|------|------|------|
| A 空间+Scrum | ⬜ | |
| B 开放平台插件 | ⬜ | |
| C 自定义字段 | ⬜ | |
| D 工作流状态 | ⬜ | |
| E 本地 sync | ⬜ | |

## 配置回填（不含 Secret）

```yaml
# feishu-project.yaml 已填项
project_key: ""
work_item_type_key: ""
gkx_task_id_field_key: ""
feishu_sprint_id: ""
```

## 验收

- [ ] discover.ps1 成功
- [ ] sync -DryRun 通过
- [ ] sync 写入后飞书看板可见 2026-W28 任务
- [ ] scrum-sprint.yaml status → active

## 遗留 / 阻塞

- 

---

**完成时**：由 PM 在 `scrum-sprint.yaml` 激活 Sprint，coordinator 接管日常 sync。
