# 看板近实时同步（跨平台 · 不强制 WSL）

> **日期**：2026-07-28（v1.2：飞书纯看板）  
> **状态**：已落地  
> **真源分层**：`task-registry.yaml` = **唯一任务真源**；飞书 Bitable = **只读看板投影**（飞书上的拖拽/改列**不回写** git）  
> **关联**：`feishu-bitable-bidirectional-ops.md` · [`../task-claiming-guide.md`](../task-claiming-guide.md) · `feishu-bitable.yaml#inbound.enabled=false`

---

## 1. 目标

任务状态变更后，飞书看板在**秒级（主动 SyncBoard）**或**≤1 小时（投影机兜底）**可见。

**不做**：换真源、强制 WSL、全员守护进程、自动 spawn Agent。

---

## 2. 谁装什么

| 角色 | OS | 必须 | 不必须 |
|------|-----|------|--------|
| 工程师 | Win / macOS | **Node 18+**；会跑 `update-task-status` | 计划任务、WSL、pwsh |
| 投影机（1～2 台） | Win 或 macOS | Node 18+ + `.env` 的 `FEISHU_*` + 注册 watch | 第二种 OS、WSL |
| Coordinator Agent | 任意 | 按 OS 选 `.ps1` / `.sh` | 假设单一 shell |

**禁止**把 WSL 写成团队标准。

---

## 3. 主路径：改状态就推板

### Windows

```powershell
cd F:\gkx-lumen\gkx-orchestration
.\scripts\update-task-status.ps1 -TaskId ENT-MOD-SEARCH-V1-HIFI -Status review `
  -Evidence "agent-handoffs/产品整体定义/UI-HIFI-ENT-SEARCH-会签单.md"
```

### macOS / Linux

```bash
cd ~/work/gkx-lumen/gkx-orchestration
./scripts/update-task-status.sh --task-id ENT-MOD-SEARCH-V1-HIFI --status review \
  --evidence "agent-handoffs/产品整体定义/UI-HIFI-ENT-SEARCH-会签单.md"
```

### 常用参数

| 参数 | 说明 |
|------|------|
| `--status` / `-Status` | backlog/ready/claimed/in_progress/review/blocked/done/needs-revision |
| `--claimed-by` / `--supervised-by` | `human:姓名` |
| `--blocked-by` | 阻塞原因 |
| `--heartbeat` | 刷新 `lock_until` / `last_seen_at` |
| `--no-sync` / `-NoSync` | 只写 YAML，不推飞书 |
| `--dry-run` / `-DryRun` | 预览 |

**默认推板**（`--sync-board`）。若无 `FEISHU_APP_ID/SECRET`：**软失败**——YAML 已写，警告依赖投影机兜底。

底层：`scripts/lib/board-task-status.mjs`（Node，跨平台共用）。

---

## 4. 辅路径：投影机 1 小时兜底（长开机）

仅 **PM / coordinator 常开本机** 注册（工程师不必）。

同步完成后若 `task-registry.yaml`（或 `bitable-inbound-proposals.yaml`）有变更，会自动：

```text
git pull --rebase → git add → commit [agent:coordinator] → git push
```

无变更则跳过。push 失败只记日志（本地 commit 保留），不阻断下次 watch。

### 前置（投影机）

- 本机已 `git login` / Credential Manager / SSH，**非交互**可 `git push`
- 工作区在 `dev`（或约定集成分支），与 `origin` 可快进/rebase

### Windows

```powershell
.\scripts\register-board-sync-watch.ps1
# 卸载：.\scripts\register-board-sync-watch.ps1 -Unregister
# 单次：.\scripts\board-sync-watch.ps1
# 只同步不推 git：.\scripts\board-sync-watch.ps1 -NoGitPush
```

默认跑完整 **bidirectional + FeishuAuthoritative**（inbound 吸收飞书看板字段 → outbound **不覆盖** 状态/认领等 → 仅投影 Agent/Epic/Handoff 等）再 **commit/push registry**。  
站会若要把 YAML 状态全量盖回飞书：`.\scripts\board-sync-watch.ps1 -NoFeishuAuthoritative`。

### macOS

```bash
./scripts/register-board-sync-watch.sh
# 卸载：./scripts/register-board-sync-watch.sh uninstall
# 建议有 pwsh 时用双向：编辑 launchd 或手动
./scripts/board-sync-watch.sh --bidirectional
```

默认 Node outbound-only + git push（registry 常无变更则 skip）。需要吸收飞书手拖时用 `--bidirectional`。

---

## 5. 架构示意

```text
工程师 / Agent
  └─ update-task-status(.ps1|.sh) → registry + Feishu（软失败）

投影机（长开机 · 每 1 小时）
  └─ board-sync-watch → Feishu 双向/出站
  └─ 有 registry 变更 → commit + push [agent:coordinator]

站会
  └─ 仍可跑 sync-feishu-bitable-bidirectional.ps1 作审计
```

---

## 6. Agent / coordinator 话术（必带双 OS）

```text
状态变更统一入口（禁止只手改 YAML 结束会话）：
- Windows: .\scripts\update-task-status.ps1 -TaskId {ID} -Status {status} ...
- macOS:   ./scripts/update-task-status.sh --task-id {ID} --status {status} ...
先判断平台再选命令。不要求 WSL。
无 FEISHU 密钥时允许软失败，handoff 注明「待投影机同步」。
```
