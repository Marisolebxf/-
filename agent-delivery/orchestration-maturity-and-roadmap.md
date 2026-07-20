# 多智能体编排成熟度自评与升级路线（2026 SOTA 对标）

> **作用**：把本项目当前的多智能体编排做法与 2026 业界最佳实践（SOTA）做对标，识别差距，给出可执行的升级路线图。  
> **关联**：`architecture-baseline.md`（架构基线）· `task-registry.yaml`（升级 Epic `E-PLATFORM-ORCH`）· `智能体编排与派单手册.md`  
> **维护**：architect-agent + coordinator-agent  
> **日期**：2026-06-17

---

## 1. 2026 多智能体编排 SOTA 速览

经互联网检索（2025–2026），业界共识可概括为一句话：

> **规范驱动（SDD）定义"做什么" + 编排者-工人（fresh context）拆解"谁来做" + Git Worktree 做"隔离" + 合并队列/验证者 + 人审 CI 门禁 做"收口"。**

### 1.1 核心范式：Orchestrator-Worker（Anthropic）

来源：[Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)

- Lead Agent（编排者）：分析任务、规划、把计划写入 Memory、派发子任务、综合结果、决定是否再派发。**不亲自干活**。
- Subagents（工人）：每个工人拿到独立、**干净的上下文**，明确的目标 / 输出格式 / 工具指引 / 任务边界（**Anthropic 四要素，缺一则漂移**）。
- 实测复杂任务比单 agent 提速 **90%**，但消耗约 **15 倍 token**。

### 1.2 规范驱动（SDD）：GitHub Spec Kit

来源：[github/spec-kit（112k star）](https://github.com/github/spec-kit)

固定阶段：`constitution → specify → clarify → plan → tasks → analyze → implement`。每阶段产出 Markdown 工件，下一阶段消费上一阶段的产物。**让规范成为可执行的资产**，而不是一次性文档。

### 1.3 并行隔离：Git Worktree

来源：[Augment — Git Worktrees for Parallel AI Agent Execution](https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution) · [Zylos — Git Worktree Isolation Patterns](https://zylos.ai/research/2026-02-22-git-worktree-parallel-ai-development)

- 业界常见：每个并行 agent 在自己的 worktree 里（共享同一 `.git` 对象库），文件级隔离。
- **本项目长期默认**：主工作区 + lumen-* `dev` 直推；**不强制** worktree / feature。worktree-per-task 仅在同仓并行 / Convoy 冲突风险时启用；worktree-per-agent 适合长会话 + 暖缓存。
- Cursor 2.0 已原生支持多路并行；本项目仍以本地并发 ≤4 为监管上限。

### 1.4 自治协调：Gastown / Speckle

来源：[JulianDouma/speckle](https://github.com/JulianDouma/speckle)（实现了 Steve Yegge 的 Gastown 模式）

- **Mayor**（协调者，从不写代码）+ **Polecats**（用完即弃的临时工人）+ **Refinery**（合并队列）+ **Convoy**（按文件分组防冲突）。
- 把 Mayor 跑成循环（`/loop`），人只在里程碑评审。

### 1.5 编排平台生态

来源：[amux — AI Agent Orchestration in 2026](https://amux.io/guides/ai-agent-orchestration-2026/) · [Mike Mason — AI Coding Agents in 2026](https://mikemason.ca/writing/ai-coding-agents-jan-2026/)

- **专用编排器**：amux（原子任务认领 + 看板 + 自愈）、Claude Squad、Microsoft Conductor、workmux。
- **IDE 内建**：Cursor v3（8 路并行）、Google Antigravity Agent Teams、GitHub Copilot multi-agent workspace。
- **运维纪律**：本地并发 ≤4；rebase 优于 merge；**任何 agent 输出合并到 main 之前必须人审 + CI**。

---

## 2. 本项目成熟度自评

| 维度 | SOTA 做法 | 本项目现状 | 评分 |
|------|-----------|------------|------|
| 编排者-工人 | Lead 不干活，工人并行 fresh context | `coordinator-agent` 派单签收不写代码；每次 `/goal` 新会话 | ✅ 完全命中 |
| 规范驱动（SDD） | 阶段化产出工件，下一阶段消费 | `项目工程化交付模式` + `bid-reference` + `scope-baseline` + `architecture-baseline` + `task-registry` | ✅ **超过多数公开实践**（有机器可读依赖规则 + 范围±10%铁律） |
| Anthropic 四要素契约 | 目标/输出格式/工具指引/任务边界 | DoD + handoff 模板 + 身份话术 | ✅ 命中 |
| 共享真源 | 项目根 CLAUDE.md 式记忆 | `agent-delivery/*` + `COORDINATOR-START.md` | ✅ 命中 |
| 验证者层 | Verifier/Reviewer 独立校验 | `qa-agent` + `architect-agent`（开工评审 + 里程碑评审） | ✅ 三层质量门 |
| 人审 + CI 门禁 | 合并前强制 | coordinator 签收 + architect 评审 + 每任务 CI（铁律 5） | ✅ 命中 |
| 全栈可观测 | （多数实践没强调） | OTel 全栈作为交付硬性要求（铁律 4）| ✅ **超前** |
| 数据契约先行 | （新兴最佳实践） | D7 + 数据库设计.md §12 + Mock 写 ADS + 数据工厂 | ✅ **超前** |
| **Git Worktree 并行** | 冲突时可选 worktree；日常主工作区 | ✅ 长期默认主工作区 + lumen `dev` 直推；worktree 为冲突例外（见公约 §4.2） | ✅ 与阶段匹配 |
| **自动化协调循环** | Mayor 自治认领-派发-合并 | ❌ 人工复制 `/goal` 到新会话 | ⚠️ **落后** |
| **任务原子认领** | 任务板加锁防双派 | ❌ 仅靠人脑判断，未加 `claimed_by/lock_at` | ⚠️ 落后 |
| **模型分层** | 强模型规划 + 快模型执行 | 未显式区分 | ⚠️ 可优化 |
| **成本/并发护栏** | 并发 2–4，多 agent ≈15x token | 未量化 | ⚠️ 需写进规范 |

**结论**：方法论在 2026 第一梯队（编排者-工人 + 规范驱动 + 三层验证 + 全栈可观测）；**真正差距在"执行层的隔离与自动化工具链"**，补齐即工业级。

---

## 3. 升级路线图（4 阶段）

> 全部升级动作以 Epic `E-PLATFORM-ORCH` 在 `task-registry.yaml` 中追踪。

### Phase 1 · 立即（≤1 周，零工具改造）

**目标**：把"成本/并发/模型分层"等运维纪律写进规范，task-registry 加最小原子认领字段。

- **ORCH-L01**：`task-registry.yaml` 任务模型扩展 `claimed_by` / `claimed_at` / `lock_until`（轻量原子认领）；状态机扩 `pending → claimed → in_progress → review → done`。
- 在 `智能体编排与派单手册.md` 新增「§14 并发与成本护栏」：
  - 本地并发 ≤ **4**（cursor v3 最多 8，但人脑监管能力是瓶颈）。
  - 多 agent token ≈ **15x** 单 agent，**紧耦合/强依赖任务不拆并行**。
  - **模型分层**：架构/规划 = 强模型（如 Opus/Codex GPT-5 high），脚手架/重复执行 = 快模型；qa 验收 = 中等。

### Phase 2 · 短期（2–3 周）· Git 作业默认 + 可选 Worktree

**目标**：日常主工作区直推；仅在同仓并行冲突时启用 worktree 隔离。

- **ORCH-L02**：制定规范——**默认** `${GKX_ROOT}/repos/{repo}` + lumen-* push `origin/dev`；**可选** worktree-per-task / worktree-per-agent；脚本化创建/清理；写入 `智能体编排与派单手册.md` §十四。
- 约束：**Convoy 分组**——同 Wave 中触碰同一目录/同一文件集的任务打包给同一个 worker，源头防合并冲突。
- 派单话术：`worktree_branch: feat/{task-id}` 为**可选**字段（冲突时才写）。
- 多实例同仓并行时再用 `git worktree add` / `worktree-helper`。

### Phase 3 · 中期（4–6 周）· 自动化 coordinator 循环

**目标**：从"人工复制 /goal"升级为"半自治循环"，人只在里程碑评审。

- **ORCH-L03**：评估两条路径并选型——
  - **A 路径（自研轻量）**：写 `scripts/coordinator_loop.py`：扫 task-registry → 选可派任务 → 调 Cursor SDK 启动 agent → 监听 handoff → 更新状态。
  - **B 路径（桥接开源）**：评估 [Speckle](https://github.com/JulianDouma/speckle) / [amux](https://amux.io/) 是否能把现有 yaml 任务板对接进去。
- 决策标准：是否能复用现有 `task-registry.yaml` schema、是否支持 Cursor、是否过度复杂。

### Phase 4 · 远期（评估后启动）· 规范驱动桥接

**目标**：可选——把 `bid-reference → scope-baseline → architecture-baseline → task-registry` 流程与 Spec Kit 的 `constitution → specify → plan → tasks` 对齐，蹭社区工具/模板/扩展。

- 评估对接成本与收益（Spec Kit 11.2k star 生态、105 个社区扩展），如收益高再做。
- 关键：**不能丢掉现有的范围±10%、验收分层、数据契约先行等本项目特化**。

---

## 4. 与架构基线的关系

| 关联点 | 说明 |
|--------|------|
| **D6 横切统一** | 升级不破横切：OTel、NebulaGraph、缓存键、鉴权 都不动 |
| **D7 数据契约先行** | worktree 并行不影响契约面（ADS 标准表），Python Mock 流水线本就是独立仓 |
| **方案 A 共享聚合核心** | 并行执行的"分仓边界"与方案 A 服务边界一致，天然适合 worktree-per-repo |

升级**只动执行层**，不动决策层。架构基线 D1–D7 全部保留。

---

## 5. 已识别的落地约束（提醒）

- **Convoy 必须按文件集划分**：当前 task-registry 的 `repo` 字段已隐式划分，但同仓内的 leaf 任务可能碰同一目录（如 `src/views/topic/**`），并行前需人工 Convoy 一次。
- **Cursor 限制**：v3 的 8 路并行依赖订阅与机器配置，本地实际并发以"人脑能监管的数量"为准（建议 ≤4）。
- **Token 成本**：升级后单 Wave 推进成本会上升 5–15 倍，但实际工时降 50–80%；权衡按 Epic 决定。

---

## 6. 引用（2026 SOTA 来源）

| 来源 | 链接 | 关键贡献 |
|------|------|----------|
| Anthropic Engineering | https://www.anthropic.com/engineering/multi-agent-research-system | 编排者-工人范式 + 四要素契约 |
| GitHub Spec Kit | https://github.com/github/spec-kit | 规范驱动 SDD 事实标准 |
| amux | https://amux.io/guides/ai-agent-orchestration-2026/ | 编排架构 5 层栈 + 工具对比 |
| Augment Code | https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution | Worktree 并行模式 |
| Zylos Research | https://zylos.ai/research/2026-02-22-git-worktree-parallel-ai-development | Worktree 隔离深度分析 |
| Mike Mason | https://mikemason.ca/writing/ai-coding-agents-jan-2026/ | 2026 编排趋势综述 |
| Speckle（Gastown 实现） | https://github.com/JulianDouma/speckle | Mayor/Polecat/Convoy/Refinery 自治模式 |

---

## 7. 变更日志

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-17 | 初版：2026 SOTA 对标 + 4 阶段升级路线（ORCH-L01/L02/L03） |
