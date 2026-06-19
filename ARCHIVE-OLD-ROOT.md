# 老根 archive 指引（M6 切换日启用）

> **本文档当前状态**：占位，待 RFC-002 §8 M6 触发后由 coordinator-agent 填充实际日期与操作记录。
> **不要在 M6 之前修改本文档内容**，仅团队管理者 / coordinator 在 M6 当日填写。

---

## 1. 元信息（M6 当日填写）

| 字段 | 值 |
|------|---|
| M6 触发日期 | （待填）|
| M6 触发原因 | RFC-002 §8.3 T1-T4 全部满足 |
| 老根路径 | `E:/gkx_src` |
| 老 GitLab group | `https://gitlab.htmisoft.net/SZCGKX` |
| 新根路径 | `E:/gkx-lumen` |
| 新 GitLab group | `https://gitlab.htmisoft.net/gkx-lumen` |
| 团队管理者签发人 | （待填）|

---

## 2. M6 切换日动作 checklist（按顺序执行）

### 2.1 老根 GitLab archive
- [ ] `SZCGKX/gkx-orchestration` 设为 Archived
- [ ] `SZCGKX/demo2` 设为 Archived
- [ ] `SZCGKX/ent-analysis-demo` 设为 Archived
- [ ] `SZCGKX/gkx_dataease` 设为 Archived
- [ ] `SZCGKX/gkx_demo_python` 设为 Archived
- [ ] `SZCGKX/gkx_demo_ui` 设为 Archived
- [ ] `SZCGKX/gkx_lumen_backend` 设为 Archived
- [ ] `SZCGKX/gkx_lumen_fronted_mobile` 设为 Archived
- [ ] `SZCGKX/gkx_lumen_fronted_pc` 设为 Archived
- [ ] `SZCGKX/gkx_service_demo` 设为 Archived
- [ ] `SZCGKX/gkx_ui_demo` 设为 Archived
- [ ] `SZCGKX/innov-algo-demo` 设为 Archived
- [ ] `SZCGKX/topic_demo` 设为 Archived

### 2.2 老根本地保护
- [ ] `E:/gkx_src/` 整个目录设为只读（`attrib +R /S /D`）
- [ ] 在老根根目录创建 `ARCHIVED-MOVED-TO-gkx-lumen.md` 指引文件
- [ ] 在每个老仓根目录创建 `MOVED-TO.md` 指向新仓 URL

### 2.3 coordinator-agent 派单规则
- [ ] 更新 `task-registry.yaml` 派单字段：100% 派到新根
- [ ] coordinator 拒派任何老根 task
- [ ] 在 `team-collaboration-playbook.md` 加 M6 完成里程碑记录

### 2.4 团队通告
- [ ] 群通告：M6 切换完成，老根 read-only
- [ ] Cursor 工作区切换：所有人改用 `E:/gkx-lumen`
- [ ] 邮件给团队管理者 + leads：M6 验收报告

---

## 3. 老仓 → 新仓映射（按 RFC-002 §7.3）

| 老仓 (SZCGKX/) | 新仓 (gkx-lumen/) | 改名理由 |
|---|---|---|
| `demo2` | `demo-ui-science` | 科技信息展示系统前端 demo |
| `ent-analysis-demo` | `demo-algo-ent-analysis` | 企业维度算法 demo |
| `gkx_dataease` | `dataease` | 开源 fork，去 gkx_ 前缀 |
| `gkx_demo_ui` | `demo-ui-system-test` | 系统级实验前端 |
| `gkx_lumen_backend` | `lumen-svc-platform` | 后端 Java 微服务正式仓 |
| `gkx_lumen_fronted_pc` | `lumen-ui-science-pc` | PC 前端正式仓（修正 fronted → ui） |
| `gkx_lumen_fronted_mobile` | `lumen-ui-science-mobile` | 移动端前端正式仓 |
| `gkx_service_demo` | `demo-svc-platform` | demo 环境后端服务 |
| `innov-algo-demo` | `demo-algo-science` | 创新监测算法 demo |
| `topic_demo` | `demo-ui-topic` | 科技专题服务前端 demo |
| `gkx_ui_demo` | （不迁移）| 4 月以来零活跃 |
| `gkx_demo_python` | （不迁移）| 3 commits，已废弃 |

---

## 4. 老根访问指引（M6 后只读）

老根仍可访问（GitLab archive 模式 = 可读不可写）：

```bash
# 查看老 commit 历史
git -C E:/gkx_src/{repo-name} log

# 浏览老仓
访问 https://gitlab.htmisoft.net/SZCGKX/{repo-name}（标记为 Archived）

# 如需老分支恢复（不应该）：
# 1. 请团队管理者签字
# 2. 由 architect-lead 在新仓创建对应 feature/* 分支
# 3. cherry-pick 老 commit 到新分支
```

---

## 5. 退路（万一切换出问题）

| 问题等级 | 处理 |
|------|------|
| 新根不可用 | 立即在 GitLab 把 SZCGKX 仓取消 archive，团队切回老根 |
| 数据丢失 | 老根本地保留 ≥ 12 个月 + GitLab 永久（archived） |
| 引用断链 | coordinator-agent 启动 cross-repo-refs lint，1 小时修复 |

---

## 6. 老根本地最终 archive 时间表

| 时刻 | 动作 |
|------|------|
| M6 + 0 月 | 老根本地 read-only，GitLab archived |
| M6 + 3 月 | 团队管理者评审是否可以本地删除 |
| M6 + 6 月 | 老根本地完全删除（仅保 GitLab archived 版） |
| M6 + 12 月 | GitLab archived 仓评估是否可以彻底删除（默认永久保留作为审计）|

---

**填写人 / 日期**：（M6 当日填写）

```
M6 触发日期：____-__-__
M6 操作人：__________
M6 验收人（架构师）：__________
M6 验收人（PM）：__________
M6 验收人（QA）：__________
团队管理者签发：__________
```
