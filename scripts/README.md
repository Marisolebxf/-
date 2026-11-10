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
| [find-supervisor-slot.mjs](find-supervisor-slot.mjs) | Node 18+ | **监管亲和参考**：推荐 `supervised_by`（`max_agent_concurrency`=本机 Cursor 会话上限；load≠派单门禁） |
| [bugflow-state.mjs](bugflow-state.mjs) | Node 18+ | **飞书缺陷 P0 账本**：schema、精确 gate、claim/session、真实 Git/evidence、版本化 policy、状态机、cycle 和报告 |
| [bugflow-state.selfcheck.mjs](bugflow-state.selfcheck.mjs) | Node 18+ | `bugflow-state` 离线回归自检 |
| [sync-bugfix-skill.mjs](sync-bugfix-skill.mjs) | Node 18+ | 从 `agent-delivery/bugfix-runs/SKILL.md` 检查/同步 Codex、Cursor、Trae 三份缺陷修复 Skill 适配副本 |
| [worktree-helper.sh](worktree-helper.sh) | 全平台（git-bash） | 管理 worktree（add/list/remove/prune） |
| [recover-expired-leases.mjs](recover-expired-leases.mjs) | Node 18+ | **lease 回收**：过期 `claimed` → `ready`；可选处理过期 `in_progress` |
| [detect-convoy-conflicts.mjs](detect-convoy-conflicts.mjs) | Node 18+ | **Convoy**：`touched_files` / 显式 convoy 组冲突检测 |
| [coordinator-loop.mjs](coordinator-loop.mjs) | Node 18+ | **Mayor 轻量循环**：lease→ready→convoy→亲和建议→scan（不自动开 agent；不因会话上限拒派） |
| [coordinator-loop-watch.ps1](coordinator-loop-watch.ps1) / [.sh](coordinator-loop-watch.sh) | Win / macOS·Linux | **A3 定时建议**：pull + loop；默认不 apply-leases；结果写 `_tmp/coordinator-loop-latest.txt` |
| [register-coordinator-loop-watch.ps1](register-coordinator-loop-watch.ps1) / [.sh](register-coordinator-loop-watch.sh) | Win Task / macOS launchd | 注册本机 Mayor 计划任务（默认每 120 分钟） |
| [refinery-enqueue.mjs](refinery-enqueue.mjs) | Node 18+ | **Refinery 脚手架**：soft-record 入队（默认不启用自动 push） |
| [normalize-legacy-paths.mjs](normalize-legacy-paths.mjs) | Node 18+ | 老根/老仓名规范化（A1 债务工具，可幂等复跑） |
| [sync-feishu-bitable.ps1](sync-feishu-bitable.ps1) | Windows | **Phase 0** task-registry → 飞书多维表格 |
| [sync-feishu-metric-board.mjs](sync-feishu-metric-board.mjs) | Node 18+ | 指标对象表出站（registry seed/矩阵） |
| [lib/metric-progress-export.mjs](lib/metric-progress-export.mjs) | Node 18+ | 「指标进度统计」离线 xlsx（MCP `metric-progress-export`） |
| [lib/metric-srs-export.mjs](lib/metric-srs-export.mjs) | Node 18+ | 先重建 SRS map，再导出「指标需求来源」xlsx（MCP `metric-srs-export`） |
| [build-metric-srs-map.mjs](build-metric-srs-map.mjs) | Node 18+ | 从 A1/A2 生成 `metrics/registry/metric-srs-map.yaml`（需求来源，不进 8 件套） |
| [apply-t0x-a2-metric-ids.mjs](apply-t0x-a2-metric-ids.mjs) | Node 18+ | T0X 正式 `M_*` 回写 A2 `metric_id: null`（不改差集判定；`--dry-run` 可预览） |
| [sync-feishu-algo-leaf-board.mjs](sync-feishu-algo-leaf-board.mjs) | Node 18+ | A1 算法库叶子出站 |
| [sync-feishu-algo-gap-board.mjs](sync-feishu-algo-gap-board.mjs) | Node 18+ | A2 页面指标差集出站 |
| [sync-feishu-wbs-board.mjs](sync-feishu-wbs-board.mjs) | Node 18+ | 指标算法 WBS 出站（§5 工作包 + 点名任务） |
| [feishu-bitable-discover.ps1](feishu-bitable-discover.ps1) | Windows | 探测 Bitable 列字段 |
| [update-task-status.ps1](update-task-status.ps1) | Windows | **近实时**：改 registry 状态 + 推飞书（Node） |
| [update-task-status.sh](update-task-status.sh) | macOS / Linux | 同上（不强制 WSL） |
| [board-sync-watch.ps1](board-sync-watch.ps1) / [.sh](board-sync-watch.sh) | 投影机 | 每 1 小时看板兜底 + registry commit/push |
| [lib/git-push-registry.ps1](lib/git-push-registry.ps1) / [.sh](lib/git-push-registry.sh) | 投影机 / K8s Webhook | 同步或 confirm 后提交推送 registry + `pending-dispatch` + 变更的 `*派单条.md` / `*派单包.md` |
| [register-board-sync-watch.ps1](register-board-sync-watch.ps1) / [.sh](register-board-sync-watch.sh) | 投影机 | 注册计划任务 / launchd |
| [lib/board-task-status.mjs](lib/board-task-status.mjs) | 全平台 Node 18+ | 状态写入 + Feishu upsert 核心（自动刷 `update_time`） |
| [backfill-update-time.mjs](backfill-update-time.mjs) | Node 18+ | 历史任务补标 `update_time`（飞书「更新时间」排序） |
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
# 推荐一键 Mayor 循环（B4 light）
node scripts/coordinator-loop.mjs
node scripts/coordinator-loop.mjs --apply-leases   # 连同回收过期 claimed

# A3 本机定时（投影机）
.\scripts\coordinator-loop-watch.ps1 -DryRun
.\scripts\coordinator-loop-watch.ps1
.\scripts\register-coordinator-loop-watch.ps1              # 每 120 min
.\scripts\register-coordinator-loop-watch.ps1 -Unregister
# macOS: ./scripts/register-coordinator-loop-watch.sh

# 预览过期 claimed（不写库）
node scripts/recover-expired-leases.mjs --dry-run
# 回收过期 claimed → ready
node scripts/recover-expired-leases.mjs --apply

# Convoy / touched_files（B3）
node scripts/detect-convoy-conflicts.mjs
node scripts/detect-convoy-conflicts.mjs --task ENT-FE-SEARCH-REGION-FILTER

# 按 agent / subcoord 推荐 supervised_by（本机 Cursor 会话上限 ≠ 派单上限；free 仅参考）
node scripts/find-supervisor-slot.mjs --agent frontend
node scripts/find-supervisor-slot.mjs --subcoord lineage-subcoord --json
```

### 飞书缺陷 P0 账本

```bash
node scripts/bugflow-state.mjs --help
node scripts/bugflow-state.selfcheck.mjs
```

设计、字段和数据策略见 `agent-delivery/bugfix-runs/README.md` 与 `P0-DESIGN.md`。

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
```

### 飞书多维表格看板（Phase 0，推荐）

```powershell
# 见 agent-delivery/feishu/feishu-bitable-integration.md
.\scripts\feishu-bitable-discover.ps1 -AppToken "xxx" -TableId "tblxxx"
.\scripts\sync-task-ready-status.ps1
.\scripts\sync-feishu-bitable.ps1 -DryRun -SprintId 2026-W28
.\scripts\sync-feishu-bitable.ps1 -DryRun:$false -SprintId 2026-W28

# 指标 / 算法投影（同一 Bitable 应用；无凭据软失败）
node scripts/sync-feishu-metric-board.mjs --dry-run
node scripts/sync-feishu-algo-leaf-board.mjs --dry-run
node scripts/sync-feishu-algo-gap-board.mjs --dry-run
node scripts/sync-feishu-wbs-board.mjs --dry-run
```

### 看板近实时（跨平台 · 不强制 WSL）

见 `agent-delivery/feishu/feishu-bitable-near-realtime.md`。需 **Node 18+**。

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
# 见 agent-delivery/feishu/feishu-project-integration.md
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
