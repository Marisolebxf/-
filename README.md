# gkx-lumen — 团队 AI 编排工作区

> **本仓库是 gkx-lumen GitLab group 的主仓**，作为团队 AI 编排的入口。
> 由 RFC-002 决议，gkx-lumen 工作区是 `${GKX_ROOT}` 老根的 greenfield 重做版本，
> 目标在 6 个月内完全替代老根（详见 [RFC-002](agent-delivery/RFC/RFC-002-gkx-v2-greenfield-rebuild.md)）。

---

## 1. 工作区结构

```
${GKX_ROOT}/                                # 你的本地工作区根（在 .env 配置）
├── gkx-orchestration/                      # ★ 本仓库（编排核心）
│   ├── .cursor/rules/                      # 13 个 .mdc agent 规则
│   ├── agent-delivery/                     # 编排资产 + 任务队列 + 验收文档
│   │   ├── RFC/                            # 团队级技术评审提案
│   │   ├── 智能体编排与派单手册.md
│   │   ├── Design.md                       # 前端 UI 权威规范（D8）
│   │   ├── repo-registry.yaml
│   │   ├── task-registry.yaml
│   │   └── ...
│   ├── knowledge-base/                     # 团队知识库
│   ├── scripts/                            # bootstrap / sync / verify 等工具
│   ├── .git-template/hooks/                # commit hooks 模板（按 RFC-002 R11）
│   ├── .env.example                        # 环境变量模板
│   └── README.md                           # 本文件
│
├── repos/                                  # 业务子仓挂载点（由 bootstrap 自动 clone）
│   ├── demo-ui-science/                    # 老 demo2
│   ├── demo-ui-topic/                      # 老 demo-ui-topic
│   ├── lumen-svc-platform/                 # 老 lumen-svc-platform
│   ├── ...
│   └── （共 10 个业务子仓，详见 paths.yaml）
│
└── worktrees/                              # AI 多 worktree 区（由 worktree-helper 创建）
    └── （按需，例：demo-ui-topic--E-ENT-IA/）
```

---

## 2. 新人 1 小时上手（onboarding）

按顺序执行（任意 OS、任意盘符）：

### Step 1：拉主仓（5 分钟）

```bash
# 创建工作区根（路径自定，必须与 .env GKX_ROOT 一致）
mkdir -p ~/work/gkx-lumen          # Mac/Linux
# 或 mkdir F:/gkx-lumen            # Windows
cd ~/work/gkx-lumen

# clone 主仓
git clone https://gitlab.htmisoft.net/gkx-lumen/gkx-orchestration.git
cd gkx-orchestration
```

# Step 2：配置 .env（2 分钟）— ★ 路径唯一真源

```bash
cp .env.example .env
# 编辑 .env，至少填 GKX_ROOT（指向你的工作区根，例 ${GKX_ROOT} 或 ~/work/gkx-lumen）
# 如有 GitLab PAT，也填 GKX_GITLAB_TOKEN
# 核对：.\scripts\resolve-path.ps1  或  ./scripts/resolve-path.sh
```

### Step 3：一键 bootstrap（30 分钟）

```powershell
# Windows
.\scripts\bootstrap.ps1
```

```bash
# Mac / Linux
./scripts/bootstrap.sh
```

bootstrap 会自动：
- 验证 `.env` 配置
- 安装 commit hooks 到本地（按 RFC-002 R11）
- clone 10 个业务子仓到 `repos/`
- 提示后续步骤（装依赖、装 IDE 插件等）

### Step 4：跟 mentor 跑 1 个完整 task（剩余时间）

详见 `agent-delivery/team-onboarding.md`。

---

## 3. 关键文件索引

| 文件 | 读者 | 作用 |
|---|---|---|
| `paths.yaml` | 全 agent | 路径真源（`${GKX_ROOT}` 解耦版） |
| `agent-delivery/智能体编排与派单手册.md` | coordinator + 全 agent | 操作手册 |
| `agent-delivery/team-collaboration-playbook.md` | 全员 | 团队公约 |
| `agent-delivery/team-onboarding.md` | 新人 + mentor | 1 天上手 |
| `agent-delivery/Cursor-多实例多角色并行实战.md` | 全员（特别是要多 task 并行的同事）| 一台机开多 Cursor + worktree 并行 SOP |
| **`agent-delivery/Design.md`** | ux / ui / frontend / qa / architect | **前端 UI 权威规范** |
| `agent-delivery/repo-registry.yaml` | dev / api / front | 仓路径 + 命名规约 |
| `agent-delivery/task-registry.yaml` | coordinator | 任务队列 |
| **`agent-delivery/RFC/RFC-002-gkx-v2-greenfield-rebuild.md`** | 团队管理者 + 全 lead | **本工作区的设计依据** |
| `.cursor/rules/*.mdc` | 全 agent（按角色） | 13 个 agent 规则 |

---

## 4. 与老根 `E:/gkx_src` 的关系

| 维度 | 老根 (gkx-lumen) | 新根 (gkx-lumen) |
|------|---|---|
| 状态 | Deprecating（M0-M6）| **Active** |
| 团队工作 | M4 起仅 bugfix | 新 task 主战场 |
| 切换日 | M6 触发后 read-only | — |
| 文档参考 | 仅历史查阅 | **以本仓为准** |

详见：
- `agent-delivery/RFC/RFC-002-gkx-v2-greenfield-rebuild.md` §8 路线图
- `ARCHIVE-OLD-ROOT.md` M6 切换日 checklist

---

## 5. 命名规约（新增仓必读）

新业务仓必须按 `{stage}-{layer}-{domain}[-{variant}]` 命名：

| 段 | 取值 |
|---|---|
| stage | `demo` (原型) / `lumen` (工程正式) |
| layer | `ui` (前端) / `svc` (后端) / `algo` (算法) |
| domain | `science` / `topic` / `platform` / `system-test` / `ent-analysis` |
| variant | `pc` / `mobile` (仅前端) |

例外：开源 fork（如 `dataease`）保持原名。

详见 [RFC-002 §7.3](agent-delivery/RFC/RFC-002-gkx-v2-greenfield-rebuild.md#73-仓库改名)。

---

## 6. 常见问题

**Q1：我装好了 `.env`，但 `bootstrap.ps1` 报"GKX_ROOT 未设置"？**
A：检查 `.env` 是否在 `gkx-orchestration/` 根目录下，且变量没有空格 / 引号包裹错误。

**Q2：bootstrap 卡在某个仓 clone？**
A：（a）检查 `GKX_GITLAB_TOKEN` 是否有效；（b）跳过该仓继续，事后 `cd repos/{repo-name}` 手动 clone。

**Q3：我看到 agent 在引用 `${GKX_ROOT}/...`，怎么办？**
A：这是老根残留引用 / agent 路径硬编码 bug。运行 `scripts/verify-paths.sh` 检测；发现新例请提 issue。

**Q4：我能在老根工作吗？**
A：M0-M3 期间可以；M4 起仅允许在老根做 bugfix；M6 后老根 read-only。

**Q5：worktree 怎么用？**
A：见 `scripts/worktree-helper.sh --help`，典型：
```bash
./scripts/worktree-helper.sh add demo-ui-topic E-ENT-IA feat/ent-elements
# 创建 worktrees/demo-ui-topic--E-ENT-IA/
```

---

**本仓库由 RFC-002 评审通过后建立（2026-06-19）。**
**维护：团队管理者 + coordinator-agent + 各 lead。**
