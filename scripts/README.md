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
| [verify-paths.sh](verify-paths.sh) | 全平台（git-bash） | 扫描硬编码路径残留（RFC-002 §6） |
| [worktree-helper.sh](worktree-helper.sh) | 全平台（git-bash） | 管理 worktree（add/list/remove/prune） |

---

## 典型用法

### 新人 onboarding（首次拉仓）

```powershell
# Windows
cd E:\gkx-lumen\gkx-orchestration
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
./scripts/worktree-helper.sh prune
```

---

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
