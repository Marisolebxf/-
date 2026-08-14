# 新人 1 小时上手指引（gkx-lumen 工作区版）

> **读者**：新加入团队（任一角色）的成员
> **目标**：1 小时完成"装环境 + 跑通首个 AI 任务 + 加入团队节奏"
> **关联**：[../README.md](../README.md) · `team-collaboration-playbook.md` · `智能体编排与派单手册.md` · `../.cursor/rules/`  
> **GDF 产线（辜少彬 / 胡森泉）**：不要跑 `bootstrap`、不要开 16 根工作区。只 clone `gkx-orchestration`，读 [`data/GDF/GDF协作指南.md`](data/GDF/GDF协作指南.md)。GitLab **不要**开组级 Developer，只加本仓。

---

## 0. 入职前准备（由 lead 在你来之前 5 分钟做完）

- [ ] 在 GitLab `gkx-lumen/` group 给你开账号 + 各业务仓 reader 权限（**GDF 成员除外**：只加 `gkx-orchestration` Developer，见 GDF协作指南）
- [ ] 申请 GitLab Personal Access Token（PAT），权限 `read_repository` + `write_repository`
- [ ] 在 Cursor Teams 拉你入团队空间（如果你团队启用）
- [ ] 给你一台至少 16GB 内存、可访问 GitLab / K8s dev 的开发机
- [ ] 派一个 mentor（同团队的资深，1 v 1）

---

## 1. 第 1 小时（一键 onboarding）

### 1.1 装 Cursor（如未装，5 分钟）

下载安装：https://cursor.com/download
登录你公司账号，进入 Cursor Teams（如果有）。

### 1.2 拉主仓 + 配置 .env（5 分钟）

```bash
# Windows PowerShell
mkdir F:/gkx-lumen
cd F:/gkx-lumen

# Mac / Linux
# mkdir -p ~/work/gkx-lumen && cd ~/work/gkx-lumen

# clone 编排主仓
git clone https://gitlab.htmisoft.net/gkx-lumen/gkx-orchestration.git
cd gkx-orchestration

# 复制环境变量模板 + 编辑
copy .env.example .env       # Windows
# cp .env.example .env       # Mac/Linux

# 用你喜欢的编辑器打开 .env，至少填：
#   GKX_ROOT=F:/gkx-lumen           # 你的工作区根（绝对路径）
#   GKX_GITLAB_USER=<your_gitlab_user>
#   GKX_GITLAB_TOKEN=<your PAT>
```

### 1.3 一键 bootstrap（30 分钟，含装依赖）

```powershell
# Windows
.\scripts\bootstrap.ps1
```

```bash
# Mac / Linux
chmod +x ./scripts/*.sh
./scripts/bootstrap.sh
```

bootstrap 会自动：
1. 验证 `.env` 配置（GKX_ROOT 必填，其他可选）
2. 安装 git commit hooks 到本仓库
3. clone 10 个业务子仓到 `${GKX_ROOT}/repos/`（按 RFC-002 §7.3 新名）
4. 提示后续步骤（按你的角色装依赖）

### 1.4 用 Cursor 打开 multi-root 工作区 + 验证 rules 命中（5 分钟）

**Step 1 — 打开 workspace 文件（不是 Open Folder）：**

Cursor 顶栏 → `File → Open Workspace from File...` → 选：

```
${GKX_ROOT}/gkx-orchestration/gkx-lumen.code-workspace
```

打开后左侧 Explorer 应看到 **12 个 folder**：

- `gkx-orchestration  (主仓 / agent-delivery / RFC / scripts)` ← 编排资产
- 10 个业务子仓（`demo-ui-science` / `lumen-svc-platform` / ...）
- `worktrees  (并行 task 分支区)`

> **为什么用 .code-workspace 而不是 Open Folder？**
> - 自动挂上主仓 + 11 子仓 + worktrees，**一个 SCM 面板看到所有 git 仓**
> - 已配置 `files.exclude` / `search.exclude` 排除 `node_modules` / `target` / `.venv` / `__pycache__` —— 不然 Cursor 索引会爆，搜索几秒变几分钟
> - 已配置推荐扩展（Volar / Java / Python / YAML）—— Cursor 会提示安装
> - 跨机器跨盘符通用（相对路径）—— 团队成员不论 `E:` `F:` `~/work` 都同一份配置
>
> **缺失的子仓**会显示 ⚠️ folder missing，重跑 `bootstrap.ps1` / `bootstrap.sh` 补齐即可。

**Step 2 — 验证 `.cursor/rules/` 命中：**

- 在 Cursor 新开 Agent 会话，输入：`你是哪个角色？必读哪些文件？`
- AI 应自动回答你对应角色的 `.mdc` 规约（如 frontend / ui / ux 等）
- 若没命中 → 检查 `.cursor/rules/` 是否同步到本地 + Cursor settings 是否启用 rules

> **进阶**：要一台机同时开多个 Cursor 并行做多 task？看 [`Cursor-多实例多角色并行实战.md`](Cursor-多实例多角色并行实战.md)（30 分钟可读，含实战演练）。

### 1.5 读你的角色规约（10 分钟）

按顺序读：

1. `[../README.md](../README.md)` —— 工作区结构总览
2. `agent-delivery/team-collaboration-playbook.md` —— 团队公约（重点 §0-§7）
3. **`agent-delivery/task-claiming-guide.md`** —— **任务认领**（claimed_by / supervised_by 名词 + 5 步流程，10 分钟）  
   过夜连跑另读 **`agent-delivery/长任务执行规约.md`**（总控一次授权，仍要每叶认领）
4. `agent-delivery/项目工程化交付模式.md` —— 总控铁律
5. **你团队对应的 `../.cursor/rules/{role}.mdc`** —— 你的 AI 公约
6. **`agent-delivery/角色AI协作对比手册.md` 找你的角色那一节** —— 5 分钟看清"AI 之前 vs AI 之后"

> 不必背下来。知道遇到问题去哪查就行。

---

## 2. 第 2-4 小时（跟 mentor 跑首个 task）

mentor 选一个**已完成**的 task（从 `task-registry.yaml` 找 `status=done`），带你走一遍：

0. **看认领**：registry 里 `claimed_by` / `supervised_by` 怎么填（见 `task-claiming-guide.md`）
1. **看派单**：从话术（编排手册 §9）到 agent 接到的 `/goal` prompt
2. **看 agent 产出**：agent 怎么读 bid-reference、怎么生成代码、怎么写 handoff
3. **看评审**：team lead 怎么评审 PR、怎么发现问题、怎么打回
4. **看 CI**：pipeline 怎么跑、绿了之后 K8s dev 怎么看
5. **看 handoff**：handoff 文件怎么写、coordinator 怎么收

> 重点：**看 AI 产物的眼光**。不是"对不对"，而是"哪里可能藏雷"。

---

## 3. 第 1 天剩余时间（独立跑 1 个简单 task）

mentor 帮你选一个**适合上手**的 task（小、独立、有先例），你独立跑：

1. 用对应角色话术开新会话，下发 `/goal`
2. **盯着看 agent 跑**：每个工具调用、每个文件读写
3. 若 agent 跑歪 → **打断**，调整 prompt 重来（不要让它瞎跑烧 token）
4. 完成后写 handoff，请 mentor 评审

**常见首日任务建议**：

| 角色 | 推荐首个任务 |
|------|----------|
| UI/UE | 给一个新功能点出 wireframe（参考 DS-15 范例） |
| 前端 | 复刻 `demo-ui-science` 一个已评审的沙箱页到 `lumen-ui-science-pc` |
| 后端 | 给一个已有 OpenAPI 契约的接口写 controller + service |
| 算法 | 复用现有模型，包一个新 `/internal/xxx` 接口 |
| 数据 | 给一张已设计的 ADS 表生成 Mock 数据 |
| DevOps | 给一个新服务复制 `.gitlab-ci.yml` 模板 |
| QA | 给一个已实现的接口补单元测试 |

---

## 4. 第 1 周（建立熟练度）

| 周次 | 目标 |
|------|------|
| 第 1 周 | 跑通 3 个完整任务；评审 5 个 PR |
| 第 2 周 | 独立处理 1 个 Epic 的子任务；参与 1 次架构对齐 |
| 第 3 周 | 能给团队优化 `.cursor/rules/{role}.mdc` 提建议 |
| 第 1 月 | 能 mentor 下一个新人 |

---

## 5. 红线（违反必处理）

| # | 红线 | 处理 |
|---|------|------|
| 1 | 不读规约就开始跑 agent | mentor 暂停权限，要求重读 |
| 2 | 把 AI 输出直接发给甲方 | 立即撤回 + PM 处置 |
| 3 | 不写 handoff 就关任务 | 任务退回 `needs-revision` |
| 4 | 直接 push 到 main | revert + 培训（commit hooks 会拦） |
| 5 | commit 不标 `[agent:xxx]` 或 `[human:xxx]` | commit-msg hook 拒绝 |
| 6 | 让 agent 跑超过 1 小时不监管 | mentor 介入 |
| 7 | 在老根 `E:/gkx_src` 改任何东西（M4 后） | revert + 培训 |
| 8 | 硬编码绝对路径（如 `${GKX_ROOT}/...`） | `verify-paths.sh` 检出，拒绝合并 |

---

## 6. 常见问题

**Q1：AI 跑出来的代码我看不懂怎么办？**
A：**这是必须解决的问题，不要合并**。要么让 agent 解释，要么改写到你能看懂为止。"不可维护" = 未来的债。

**Q2：agent 跟我说"我已经做完了"，但 CI 没绿？**
A：DoD 不满足 = 没做完。退回让 agent 修，不要自己手动绕过 CI。

**Q3：agent 一直跑偏，怎么办？**
A：检查三件事：(1) `.cursor/rules/{role}.mdc` 是否命中；(2) 你的 prompt 是否清晰；(3) 必读文件是否在上下文。三者都对还跑偏 → 升级到 mentor / 架构师。

**Q4：我能不能让 agent 跨角色干活（比如 frontend-agent 改后端）？**
A：**不能**。跨角色一定走派单 → 新会话 → 对应角色 agent。同会话跨角色 = 上下文污染 + 违反铁律。

**Q5：本地能开几个 agent 并行？**
A：≤ 4（编排手册 §14）。超过就上 Background Agents 云端。

**Q6：Mock 数据怎么生成？**
A：找 data-agent 派单，给定 ADS 表名 + 规模。不要自己手写 mock。

**Q7：我发现一个铁律不合理，怎么改？**
A：写到 retro 议题，里程碑评审时由架构师 + PM 决定。**不要擅自破例**。

**Q8：bootstrap 失败怎么办？**
A：看错误信息：
- `GKX_ROOT 未设置` → 编辑 `.env` 加上
- `GitLab clone 失败` → 检查 `GKX_GITLAB_TOKEN` 是否有效，可手动 `git clone` 单仓
- `Permission denied` → 让 lead 加 GitLab 仓权限

**Q9：worktree 怎么用？**
A：`./scripts/worktree-helper.sh --help`，典型：
```bash
./scripts/worktree-helper.sh add demo-ui-topic E-ENT-IA feat/ent-elements
```

**Q10：我能在老根 `E:/gkx_src` 临时干活吗？**
A：M0-M3 期间可以；M4 起仅允许 bugfix；M6 后老根 read-only（详见 RFC-002 §8）。

---

## 7. 入职第 1 天检查表（mentor 用）

- [ ] 新人能独立打开 Cursor + 命中 `.cursor/rules/`
- [ ] 新人能找到本团队的 `.mdc` 规约
- [ ] 新人跑通了 1 个简单任务并写了 handoff
- [ ] 新人 review 了 1 个别人的 PR
- [ ] 新人加入了团队站会 + 飞书群
- [ ] 新人知道铁律 + 8 条红线
- [ ] 新人有 mentor 的微信 / 飞书直联
- [ ] 新人 .env 配置 ok，bootstrap 跑通

全部 ✅ → 可以独立工作；否则延期 1 天。

---

**本文档维护**：每次有新人入职后回顾，更新过时步骤。
**版本**：v2.0 (gkx-lumen) — 2026-06-19 — 替代老版 v1（gkx_src 硬编码版）
