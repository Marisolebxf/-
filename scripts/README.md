# gkx-lumen 工具脚本

> 本目录所有脚本都从 `gkx-orchestration/` 根目录执行（不要从 `scripts/` 内执行）。
> Windows 用户：使用 **git-bash**（Git for Windows 自带）跑 `.sh` 脚本；`.ps1` 脚本在 PowerShell 跑。

---

## 脚本清单

| 脚本 | 平台 | 作用 |
|---|---|---|
| [bootstrap.ps1](bootstrap.ps1) | Windows | 一键 onboarding（PowerShell 版） |
| [bootstrap.sh](bootstrap.sh) | Mac / Linux / git-bash | 一键 onboarding（Bash 版） |
| [sync-all.sh](sync-all.sh) | 全平台（git-bash） | 一键 git pull 主仓 + 10 子仓 |
| [resolve-path.ps1](resolve-path.ps1) | Windows | 打印 `.env` 解析后的路径（路径真源自检） |
| [resolve-path.sh](resolve-path.sh) | Mac / Linux / git-bash | 同上（Bash 版） |
| [lib/load-env.ps1](lib/load-env.ps1) | Windows | 供脚本 dot-source 加载 `.env` |
| [lib/load-env.sh](lib/load-env.sh) | git-bash | 同上（Bash 版） |
| [verify-paths.sh](verify-paths.sh) | 全平台（git-bash） | 扫描硬编码路径残留（RFC-002 §6） |
| [sync-task-ready-status.ps1](sync-task-ready-status.ps1) | Windows | Kanban 状态 refresh（backlog/ready/blocked） |
| [find-supervisor-slot.mjs](find-supervisor-slot.mjs) | Node 18+ | **监管容量**：按花名册 `max_agent_concurrency` + 活跃负载推荐 `supervised_by` |
| [recover-expired-leases.mjs](recover-expired-leases.mjs) | Node 18+ | **lease 回收**：过期 `claimed` → `ready`；可选处理过期 `in_progress` |
| [normalize-legacy-paths.mjs](normalize-legacy-paths.mjs) | Node 18+ | 老根/老仓名规范化（A1 债务工具，可幂等复跑） |
| [sync-feishu-bitable.ps1](sync-feishu-bitable.ps1) | Windows | **Phase 0** task-registry → 飞书多维表格 |
| [feishu-bitable-discover.ps1](feishu-bitable-discover.ps1) | Windows | 探测 Bitable 列字段 |
| [update-task-status.ps1](update-task-status.ps1) | Windows | **近实时**：改 registry 状态 + 推飞书（Node） |
| [update-task-status.sh](update-task-status.sh) | macOS / Linux | 同上（不强制 WSL） |
| [board-sync-watch.ps1](board-sync-watch.ps1) / [.sh](board-sync-watch.sh) | 投影机 | 每 1 小时看板兜底 + registry commit/push |
| [lib/git-push-registry.ps1](lib/git-push-registry.ps1) / [.sh](lib/git-push-registry.sh) | 投影机 / K8s Webhook | 同步或 confirm 后提交推送 registry + `pending-dispatch` + 变更的 `*派单包.md` |
| [register-board-sync-watch.ps1](register-board-sync-watch.ps1) / [.sh](register-board-sync-watch.sh) | 投影机 | 注册计划任务 / launchd |
| [lib/board-task-status.mjs](lib/board-task-status.mjs) | 全平台 Node 18+ | 状态写入 + Feishu upsert 核心 |
| [backfill-effort-points.mjs](backfill-effort-points.mjs) | Node 18+ | 历史任务补标 effort_points/difficulty |
| [report-contribution.mjs](report-contribution.mjs) | Node 18+ | 按人汇总贡献分（绩效） |
| [sync-feishu-project.ps1](sync-feishu-project.ps1) | Windows | task-registry → 飞书项目（待审批） |
| [feishu-project-discover.ps1](feishu-project-discover.ps1) | Windows | 探测飞书项目 field_key |

---

## 典型用法

### 新人 onboarding（首次拉仓）

```powershell
# Windows
cd F:\gkx-lumen\gkx-orchestration
.\scripts\bootstrap.ps1
```

```bash
# Mac/Linux/git-bash
cd ~/work/gkx-lumen/gkx-orchestration
./scripts/bootstrap.sh
```

### 每日开工前同步

```bash
./scripts/sync-all.sh                # 全量 pull
./scripts/sync-all.sh --dry-run      # 仅看要做什么
```

### 路径真源自检（agent / 人类）

```powershell
# Windows — 确认 GKX_ROOT 与关键 repos 展开
.\scripts\resolve-path.ps1
```

```bash
./scripts/resolve-path.sh
```

### 站会前：lease 回收 + 监管人空位（Graph Engineering B1）

```powershell
# 预览过期 claimed（不写库）
node scripts/recover-expired-leases.mjs --dry-run
# 回收过期 claimed → ready
node scripts/recover-expired-leases.mjs --apply

# 按 agent / subcoord 推荐 supervised_by（监管并发≠派单上限）
node scripts/find-supervisor-slot.mjs --agent frontend
node scripts/find-supervisor-slot.mjs --subcoord lineage-subcoord --json
```

### 提 PR 前自检

```bash
./scripts/verify-paths.sh            # 确保无硬编码路径残留
```

### 用 worktree 跑并行 task

```bash
# 在 demo-ui-topic 仓创建一个新 worktree 跑 E-ENT-IA
./scripts/worktree-helper.sh add demo-ui-topic E-ENT-IA feat/ent-elements
# → worktrees/demo-ui-topic--E-ENT-IA/

# 列出所有 worktree
./scripts/worktree-helper.sh list

# task 完成后清理
./scripts/worktree-helper.sh remove demo-ui-topic E-ENT-IA

# 定期清理失效引用
| [worktree-helper.sh](worktree-helper.sh) | 全平台（git-bash） | 管理 worktree（add/list/remove/prune） |

### 飞书多维表格看板（Phase 0，推荐）

```powershell
# 见 agent-delivery/feishu-bitable-integration.md
.\scripts\feishu-bitable-discover.ps1 -AppToken "xxx" -TableId "tblxxx"
.\scripts\sync-task-ready-status.ps1
.\scripts\sync-feishu-bitable.ps1 -DryRun -SprintId 2026-W28
.\scripts\sync-feishu-bitable.ps1 -DryRun:$false -SprintId 2026-W28
```

### 看板近实时（跨平台 · 不强制 WSL）

见 `agent-delivery/feishu-bitable-near-realtime.md`。需 **Node 18+**。

```powershell
# Windows — 改状态并推飞书（默认 SyncBoard；无密钥软失败）
.\scripts\update-task-status.ps1 -TaskId ENT-MOD-SEARCH-V1-HIFI -Status review -DryRun

# 投影机（可选，仅 1～2 台）
.\scripts\register-board-sync-watch.ps1
```

```bash
# macOS / Linux
./scripts/update-task-status.sh --task-id ENT-MOD-SEARCH-V1-HIFI --status review --dry-run
./scripts/register-board-sync-watch.sh   # 投影机可选
```

### 飞书项目（待企业审批后）

```powershell
# 见 feishu-project-integration.md
.\scripts\feishu-project-discover.ps1 -ProjectKey "your_project_key"
.\scripts\sync-feishu-project.ps1 -DryRun -SprintId 2026-W28
```

## Windows 用户：git-bash 在哪？

Git for Windows 安装时会自带 **git-bash**：

- 通过开始菜单：Git → Git Bash
- 通过 Cursor 终端：选 Terminal → New Terminal → 下拉选 "Git Bash"
- 通过 PowerShell 调用：`& "C:\Program Files\Git\bin\bash.exe" ./scripts/sync-all.sh`

git-bash 提供完整的 bash + grep + curl + sed 等 Unix 工具，无需 WSL。

---

## 已知限制

| 项 | 说明 |
|---|---|
| `verify-paths.sh` 用了 `grep` | git-bash 自带，但 macOS 默认 grep 与 GNU grep 略有差异；如需 GNU grep：`brew install grep`，用 `ggrep` 替代 |
| `pre-commit` hook 用了 `file` 命令 | macOS 自带；如缺失：`brew install file-formula` |
| 大文件检测用 `wc -c`（兼容） | 不依赖 GNU 工具 |
| `bootstrap.ps1` 用 PowerShell 5.1+ | Windows 10/11 自带；如旧版需升级 |

---

## 扩展（M2-M6 阶段补充）

预计后续会新增：

- `audit-commits.sh` —— coordinator 每周扫描各仓 commit（按 R11 mitigation b）
- `migration-diff.sh` —— M5 老根 vs 新根对账
- `m6-switch.sh` —— M6 切换日自动化（按 ARCHIVE-OLD-ROOT.md §2）

不在 M1 范围。
