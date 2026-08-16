# 飞书多维表格开通 · 分步清单

| 步 | 动作 | 完成标志 |
|----|------|----------|
| 1 | 飞书 → 云文档 → 新建多维表格「GKX 智树任务看板」 | 表已创建 |
| 2 | 建列：Task ID、标题、状态(单选)、Agent、Epic、Sprint、监管人、认领、Token估算、Handoff | 11 列齐全 |
| 3 | 状态列添加 7 个选项：Backlog/Ready/已认领/进行中/评审中/已完成/阻塞 | 单选可填 |
| 4 | 新建 **看板视图**，分组 = 状态 | 可拖拽 |
| 5 | 从 URL 复制 app_token、table_id | 两串 ID |
| 6 | open.feishu.cn 建自建应用，开 bitable 权限，发布 | 有 App ID/Secret |
| 7 | 表格分享 → 添加 **应用** 为可编辑协作者 | API 可写 |
| 8 | 本地 `.env` 填 FEISHU_APP_ID/SECRET | discover 不报错 |
| 9 | 填 `feishu-bitable.yaml`，跑 sync -DryRun | 列出 CREATE |
| 10 | sync -DryRun:$false，看板出现任务 | 人类看板可用 |

**教练 Prompt**：`feishu-bitable-setup-coach-prompt.md`
