# Cursor 多实例 × 多角色并行实战

> **适用范围**：gkx-lumen 工作区全员（人 + AI agent）
> **维护**：orchestration-lead
> **最后更新**：2026-07-17
> **关联文档**：[RFC-002 §6](RFC/RFC-002-gkx-v2-greenfield-rebuild.md) · [team-onboarding §1.4](team-onboarding.md) · [scripts/worktree-helper.sh](../scripts/worktree-helper.sh) · [团队公约 §4.2](../.cursor/rules/00-team-constitution.mdc)
> **预计宣讲时长**：30 分钟（含演示 10 分钟）
>
> **Git 默认（2026-07-17）**：**单任务默认不用 worktree**——在 `${GKX_ROOT}/repos/{repo}` 主工作区作业，lumen-* 直推 `origin/dev`。本文的 worktree SOP **仅用于多实例同仓并行**（或监管人明确要求隔离时）。

---

## TL;DR（30 秒看完核心）

| 你想做什么 | 怎么做 |
|---|---|
| 一台电脑同时开 2 个 Cursor，扮演不同角色 | 完全可以。开第二个用 `cursor --new-window <path>` 或 `File → New Window` |
| 不同 Cursor 看到不同的"角色规约" | **错觉**。`.cursor/rules/*.mdc` 是**项目级**，在哪个工作区打开都加载同一份；区分角色靠**你在 chat 里指定角色 + 打开对应子仓让 globs 自动命中** |
| 单个 task | **默认主工作区**，不用 worktree；lumen-* push `origin/dev` |
| 多个 task 同仓并行不撞车 | 此时才用 worktree：**每个 task 一个 worktree + 一个 Cursor 实例** |
| 同一 workspace 第二次打开没反应 | 这是 Cursor 默认行为（聚焦已有窗口）。绕过：`cursor --new-window <path>` 或先 `File → New Window` 再 Open |

**一句话**：日常「主目录 + 指定角色」即可；「不同 worktree + 各自 chat」只服务同仓多任务并行。

---

## 1. 背景：我们为什么需要这个？

gkx-lumen 工作区按 [RFC-002 §6](RFC/RFC-002-gkx-v2-greenfield-rebuild.md) 切分为：

- **1 个主仓** `gkx-orchestration`（编排 / RFC / agent-delivery）
- **10 个业务子仓**（前端 / 后端 / 算法 / BI，详见 [repo-registry.yaml](repo-registry.yaml) `migration_to_gkx_lumen`）
- **worktree 池** `${GKX_ROOT}/worktrees/`（并行 task 分支区）

一个人很难同时盯 11 个仓 + 多个 in-progress task。AI agent 帮我们解决"多线作业"，但前提是：

1. **每个 agent 上下文要专注** —— 一个 chat 一个 task，agent 不要被无关代码干扰
2. **物理隔离** —— 多任务并发时避免文件 / 分支 / dev server 端口冲突
3. **统一总览** —— 编排者仍需要"看全局"的入口

多 Cursor 实例 + worktree 就是工程上的实现方式，本文给你 SOP。

---

## 2. 核心概念厘清（讲讲机制，避免误用）

### 2.1 Cursor 实例（Window）

Cursor 基于 VS Code，多窗口是原生能力。

**每个窗口独立的**：
- 工作区配置 / 编辑器状态 / 终端
- **Agent chat 会话**（每个 tab 一个独立上下文，跨窗口不互通）
- 当前打开的文件 / undo 历史 / 搜索结果

**所有窗口共享的**（注意，这是潜在的"撞车点"）：
- 你的 Cursor 账号 + 模型 API 配额 —— **两实例并发跑 agent ≈ 费用翻倍**
- 全局 settings / 扩展安装
- 文件系统本身 —— 同一文件、同一端口、同一 git lock 都会冲突

### 2.2 角色 `.cursor/rules/*.mdc` 是项目级，不是实例级

很容易踩的认知坑：

| 误以为 | 实际 |
|---|---|
| 我打开 backend 子仓，Cursor 就"变成" backend-agent | Cursor 实例本身没有角色概念 |
| 不同 Cursor 自动加载不同角色规约 | 所有打开同一 workspace 的实例**加载同一套 `.mdc`** |
| 我要切换角色，得换 Cursor | 切角色靠**对 agent 说"你是 xxx-agent"** + **打开对应子仓让 globs 触发** |

**`.mdc` 的实际匹配机制**（简化版）：

```
agent 接到 prompt
   |
   v
扫描所有 .cursor/rules/*.mdc
   |
   v
按以下顺序匹配（前面优先）：
1. prompt 里你明确指定的角色（"你是 frontend-agent"）
2. globs 字段命中（当前打开文件路径匹配，如 globs: ["**/*.vue", "**/*.tsx"]）
3. agent type 字段（如果文件头声明了 agent type）
4. 默认 fallback (.cursorrules 或 root rule)
```

所以「一个 Cursor 充当一个角色」=「**这个 Cursor 的 chat 上下文专注于某个角色 + 打开的目录天然命中该角色的 globs**」。

---

## 3. 三种玩法对比

### 玩法 A：两个 Cursor，各打开一个**子仓**（强隔离，最简单）

```
Cursor 实例 1: 打开 F:/gkx-lumen/repos/lumen-svc-platform        → backend agent
Cursor 实例 2: 打开 F:/gkx-lumen/repos/lumen-ui-science-pc       → frontend agent
```

**适用场景**：你要长期专注做某一个仓的某一个大功能（不需要跨仓查）。

| 优点 | 缺点 |
|---|---|
| rules globs 自动命中（路径就是 frontend / backend 子仓内部） | 看不到 `agent-delivery/` / RFC / repo-registry（编排资产） |
| git 操作完全独立，零撞车 | 跨仓需求时要在文件系统手工切 |
| 设置最简单（Open Folder 就行） | 无法享受 multi-root workspace 的"排除 node_modules"配置 |

### 玩法 B：两个 Cursor，都打开 multi-root workspace（推荐主力）

```
Cursor 实例 1: 打开 gkx-lumen.code-workspace
            → chat: "你是 backend-agent，帮我做 task T-001-api"
Cursor 实例 2: 打开同一个 .code-workspace（用 --new-window）
            → chat: "你是 frontend-agent，帮我做 task T-002-ui"
```

**适用场景**：日常多 task 并行 + 经常跨仓查引用 / 接口契约。

| 优点 | 缺点 |
|---|---|
| 两实例都看到 agent-delivery + 11 仓 + 全部 rules | 同 workspace 第二次打开默认"聚焦已有窗口"，要用 `--new-window` |
| 跨仓搜索一个面板搞定 | 两实例改同一文件会冲突（按子仓/task 分工即可避免） |
| `.code-workspace` 已配 `files.exclude` 排除 node_modules，索引不爆 | 两实例都索引一遍仓，内存翻倍 |

**打开第二实例的命令**：

```powershell
# Windows PowerShell
cursor --new-window F:\gkx-lumen\gkx-orchestration\gkx-lumen.code-workspace

# Mac / Linux
cursor --new-window ~/work/gkx-lumen/gkx-orchestration/gkx-lumen.code-workspace
```

> 也可以：先打开 Cursor → `File → New Window` 开空窗口 → 再 `File → Open Workspace from File`。

### 玩法 C：worktree + 两个 Cursor（最适合"同仓不同分支"并行）

利用 RFC-002 §6 设计的 worktree 机制：

```bash
# 在主 Cursor 的终端创建 2 个 worktree（同仓不同分支）
cd ${GKX_ROOT}/gkx-orchestration
bash scripts/worktree-helper.sh add lumen-svc-platform feature/T-001-api
bash scripts/worktree-helper.sh add lumen-svc-platform feature/T-002-auth
```

然后：

```
Cursor 1: 打开 ${GKX_ROOT}/worktrees/lumen-svc-platform--feature-T-001-api
Cursor 2: 打开 ${GKX_ROOT}/worktrees/lumen-svc-platform--feature-T-002-auth
```

**适用场景**：你在同一个仓里有 2 个 in-progress 任务（如一个 hotfix + 一个 feature），不想反复 `git stash / git checkout` 切来切去。

| 优点 | 缺点 |
|---|---|
| 同仓两分支**物理隔离**，互不阻塞 | 多一个目录，新人初见会困惑（看本文件就好） |
| 各有独立 node_modules / target，依赖不串台 | 占磁盘（node_modules × N 份）；用 pnpm 可缓解 |
| 一边等 CI / 编译，另一边继续写新代码 | task 跨 worktree 需要 cherry-pick |

完成后清理：

```bash
bash scripts/worktree-helper.sh remove lumen-svc-platform--feature-T-001-api
```

---

## 4. 推荐工作流（你一个人 + AI 多角色）

```
                  ┌────────────────────────────────────────┐
                  │           主 Cursor (常驻)              │
                  │  打开: gkx-lumen.code-workspace        │
                  │  用途: 编排 / RFC 编辑 / 跨仓查 / 总览  │
                  │  chat: 跟 coordinator-agent 对话，派单 │
                  └──────────────────┬─────────────────────┘
                                     │
                                     │ 派出 task
                                     ▼
                  ┌────────────────────────────────────────┐
                  │     第二个 Cursor (按 task 开关)        │
                  │  打开: worktrees/<repo>--feat-T-xxx   │
                  │  用途: 单 task 专注开发                 │
                  │  chat: 跟 frontend/backend/algo agent 谈│
                  │  完成: 提 MR / push 后关闭             │
                  └──────────────────┬─────────────────────┘
                                     │
                                     │ 并行需要时
                                     ▼
                  ┌────────────────────────────────────────┐
                  │    第三个 Cursor (并行 task 才开)       │
                  │  打开: 另一个 worktree                  │
                  │  chat: 另一个 role agent                │
                  └────────────────────────────────────────┘
```

### 4.1 具体一天的工作示例

| 时间 | 主 Cursor | 副 Cursor 1 | 副 Cursor 2 |
|---|---|---|---|
| 09:00 | 看 task-registry / 选 2 个 task 派出 | — | — |
| 09:10 | 开终端，建 2 个 worktree | — | — |
| 09:15 | 跟 coordinator agent 对齐 handoff | — | — |
| 09:30 | （监督）查 RFC 引用 | 开打 worktree-T001，chat "你是 backend-agent，做 T-001" | — |
| 10:00 | （监督）回 PM 问题 | agent 在写 controller | 开打 worktree-T002，chat "你是 frontend-agent，做 T-002" |
| 11:30 | 看 T-001 PR diff | 完成，提 MR，关闭 | agent 还在画页面 |
| 14:00 | 评审 T-001 MR | — | 完成，提 MR，关闭 |

---

## 5. 必须避坑的清单（do / don't）

| 坑 | 触发条件 | 规避方式 |
|---|---|---|
| **dev server 端口冲突** | 2 个前端实例都 `npm run dev` 默认 5173 | 第二个用 `npm run dev -- --port 5174`，或在 `vite.config.ts` 用 `process.env.VITE_PORT` |
| **同仓并发 git push** | 两实例同时 push 同分支 | **按子仓 / worktree 分工**，永远不让两实例操作同一目录 |
| **同仓并发 `npm install` / `mvn install`** | 两实例同时跑包管理 | 一个跑完再跑另一个；或用 worktree（各有独立依赖目录） |
| **同 workspace 二次打开失败** | 默认聚焦已有窗口 | `cursor --new-window <path>` |
| **AI 配额翻倍** | 两实例同时让 agent 跑长任务 | 心里有数；或一个跑 agent 一个只看代码；可观察 settings → Usage |
| **内存压力** | 每个 Cursor 实例 0.5-2GB | 8GB 内存机器开 2 个会卡，16GB+ 无压力 |
| **rules 没命中** | 打开了不对的子仓，agent 用了 fallback 规约 | **明确在 chat 第一句指定角色**："你是 backend-agent，必读 rules/backend.mdc" |
| **跨实例文件 race** | 两实例都开了同一个 `architecture-baseline.md` 编辑 | 共用文件（RFC / 架构图）只在主 Cursor 改，副 Cursor 只读 |
| **chat 会话丢失** | 关闭 Cursor 窗口 | Cursor 不持久化 chat（按设计），重要 prompt 截图或粘到 task-registry `handoff` 字段 |

---

## 6. 团队约定（避免协作时撞车）

为了让多人多 Cursor 并行不出乱子，团队约定：

1. **同一子仓同一分支同时只能一个人占用**（看 task-registry `assignee` + `branch` 字段）
2. **worktree 命名规约**：`<repo>--<branch-name>`（已由 `worktree-helper.sh` 强制）
3. **worktree 寿命 ≤ task 寿命**：task 完成 / abandon 立即 `remove`，避免 worktree 堆积
4. **dev server 端口固定**：前端 base = 5173 + task 编号末位，后端 base = 8080 + task 编号末位（详见 [team-collaboration-playbook.md](team-collaboration-playbook.md)）
5. **同 workspace 二次打开记日志**：在你的 work-log 里写明"开了第 N 个 Cursor 做 T-XXX"，方便事后追溯
6. **agent 长时间任务前同步给团队**：要让 agent 跑 30 分钟+ 的 codegen 前，在 IM 群发"我现在让 agent 跑 T-XXX 大约 30 分钟"，避免别人同时跑撞 git lock

---

## 7. FAQ

### Q1：我只是看代码，不让 agent 写，是不是不用开第二个 Cursor？

对。**纯读 = 一个 Cursor 多 tab 就够**；要让 agent 并行写代码 = 才需要多实例（chat 上下文需要物理隔离）。

### Q2：3 个 Cursor 行不行？4 个呢？

技术上行，**实操上不建议超过 3 个**。你脑子的注意力切换 + AI 配额 + 内存都会成为瓶颈。RFC-002 § 6 的 worktree 目录最多展示 3-5 个并发也是这个考虑。

### Q3：每个 Cursor 都要重新跑 `bootstrap.ps1` 吗？

不用。bootstrap 只在**第一次** clone 11 个子仓 + 装 hooks 时跑。多 Cursor 实例都用同一份磁盘上的工作区，bootstrap 已经做过的事不需要重复。

### Q4：可以一个 Cursor 开 main，另一个 Cursor 开 feature 分支吗？

**同一个 git 仓的两个分支**要用 **worktree**（玩法 C），**不要**两实例同时打开同一仓再 `git checkout` 切分支 —— 第二实例切了第一实例就乱了。

### Q5：chat 会话能在两个 Cursor 之间转吗？

不能。每个 Cursor 实例的 chat 上下文独立、不持久化。**重要 prompt / 决策务必沉淀到 markdown**（如 `agent-handoffs/<task-id>.md`），下次别的 Cursor / 别的人才能 pickup。

### Q6：我用 `.code-workspace` 打开，agent 能看到所有 11 个仓的代码吗？

能。multi-root workspace 把 11 个仓都挂在一个 Cursor 实例下，agent 的"工作区上下文" = 全部 11 个仓。这是跨仓任务的优势，也是为什么我们**强烈推荐**用 `.code-workspace` 而不是 Open Folder 单仓。

### Q7：手机上 / 平板上能开第二个 Cursor 吗？

Cursor 目前没有移动端。但你可以在 iPad 上用 Tailscale 远程 SSH 到你的工作机 + 用 Cursor CLI 模式 —— 这是另一个话题，本文不展开。

---

## 8. 实战演练（宣讲时现场跑一遍）

> 给宣讲人：建议在第二台屏幕投影实操，让团队看真实效果。

### 步骤 1：从 0 开 multi-root workspace（主 Cursor）

```powershell
# Cursor → File → Open Workspace from File
# 选: F:/gkx-lumen/gkx-orchestration/gkx-lumen.code-workspace
# 左侧 Explorer 应看到 12 个 folder
```

### 步骤 2：在主 Cursor 终端建 worktree

```bash
cd ${GKX_ROOT}/gkx-orchestration
bash scripts/worktree-helper.sh add lumen-svc-platform feature/demo-multi-cursor
```

### 步骤 3：开第二个 Cursor 实例，指向 worktree

```powershell
cursor --new-window F:\gkx-lumen\worktrees\lumen-svc-platform--feature-demo-multi-cursor
```

### 步骤 4：在第二实例的 chat 里指定角色

> 你是 backend-agent。本仓是 lumen-svc-platform 的 worktree `feature/demo-multi-cursor`，
> 帮我在 `gkxlumen-metrics` 模块加一个 `/api/v1/demo` 端点（GET, return `{"hello":"world"}`），
> 完成后输出 unified diff。

### 步骤 5：观察主 Cursor 不受任何影响

回到主 Cursor，继续编辑 RFC / 看 git 面板 / 跟 coordinator agent 对话，**完全互不干扰**。

### 步骤 6：演示完 cleanup

```bash
bash scripts/worktree-helper.sh remove lumen-svc-platform--feature-demo-multi-cursor
# 第二个 Cursor 关掉即可
```

---

## 9. 附录：把这一切关联到 RFC-002

| 本文档讲的 | RFC-002 哪里 |
|---|---|
| multi-root workspace `.code-workspace` | §6 + 2026-06-19 follow-up commit `fd96472` |
| worktree 池 `${GKX_ROOT}/worktrees/` | §6 + scripts/worktree-helper.sh |
| 11 仓清单（含老→新映射） | §7.3 + `agent-delivery/repo-registry.yaml` |
| Agent 角色规约位置 | §6 + `.cursor/rules/*.mdc` |
| 团队 onboarding 1 小时承诺 | §3 G2 + scripts/bootstrap.ps1/.sh |

---

## 10. 维护说明

- 本文档随团队工作流演进迭代，看到新坑就来加
- 大改动走 RFC 流程（参考 RFC-001 / RFC-002）
- 小补丁直接 PR 进主仓 `agent-delivery/`，commit 信息标 `docs(cursor-guide): xxx`

---

**最后一句忠告**：工具是用来**减少思考负担**的。如果你发现自己天天在 5 个 Cursor 间切来切去，那不是炫技 —— 而是**任务粒度太碎**了。建议回到 [team-collaboration-playbook.md](team-collaboration-playbook.md) §5 重审 task 拆分。
