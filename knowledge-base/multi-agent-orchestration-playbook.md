# 多智能体工程化交付剧本（Playbook）

> **作者沉淀**：基于「智谱-国科信 科技信息展示系统」项目的实战提炼，对标 2026 业界 SOTA（Anthropic / GitHub Spec Kit / amux / Gastown）。  
> **用途**：任何中大型软件交付项目启动多智能体编排时的"开箱模板"。直接复制本目录到新项目，按 §7 启动 Checklist 推进即可。  
> **维护者**：本人  
> **首版**：2026-06-17

---

## 0. 一句话心智

> **规范驱动（SDD）定义"做什么" + 编排者-工人（fresh context）拆解"谁来做" + Git Worktree 做"隔离" + 合并队列/验证者 + 人审 CI 门禁 做"收口"。**

---

## 1. 适用 / 不适用

### 适用场景
- 中大型项目（多人月、多模块、多仓库）
- 有明确范围文档（招标书 / PRD / 需求规格）
- 需要可追溯的验收（甲方/合同/合规）
- 团队希望并行加速 + 控制质量

### 不适用场景
- 单人小项目 / POC（编排开销 > 收益）
- 强烈紧耦合、所有改动必须同时落地的任务
- 上下文极度依赖人脑直觉、无法文档化的探索性研究

> **代价提醒**：多 agent token 成本 ≈ 单 agent 的 **15 倍**；用对了省 50–80% 工时，用错了纯烧钱。

---

## 2. 核心心智模型（5 句话）

1. **编排者不干活**：Lead/Coordinator 只规划、派单、综合、签收，不写代码。
2. **工人拿干净上下文**：每个子任务新开会话，给"目标 + 输出格式 + 工具指引 + 任务边界"（**Anthropic 四要素**，缺一则漂移）。
3. **按切面而非步骤拆**：让任务彼此正交，最大化并行、最小化依赖。
4. **隔离靠 Git Worktree**：文件级隔离把冲突推到 merge 阶段，由 Git 工具识别。
5. **人审 + CI 是不可省的门禁**：任何 agent 输出合并到 main 之前必须人审且 CI 全绿。

---

## 3. SOTA 模式速览（带引用）

| 模式 | 来源 | 一句话 |
|------|------|--------|
| Orchestrator-Worker | [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system) | Lead 不干活，并行 Subagents fresh context，提速 90%、耗 15x token |
| Spec-Driven Dev (SDD) | [github/spec-kit (112k★)](https://github.com/github/spec-kit) | `constitution → specify → clarify → plan → tasks → analyze → implement` |
| Git Worktree 并行 | [Augment Code](https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution) · [Zylos](https://zylos.ai/research/2026-02-22-git-worktree-parallel-ai-development) | worktree-per-task 默认，最多 8 路并行（Cursor v3 原生支持） |
| Gastown 自治模式 | [Speckle](https://github.com/JulianDouma/speckle) | Mayor + Polecats + Refinery + Convoy；Mayor 跑成自治循环 |
| 编排架构 5 层栈 | [amux 2026](https://amux.io/guides/ai-agent-orchestration-2026/) | 任务/认领/隔离/通信/观测 五层各自最佳实践 |

---

## 4. 落地清单（10 个必备件）

> 在任何新项目里，至少这 10 件齐了，编排才稳。

| # | 件 | 文件示例 | 关键点 |
|---|----|----------|--------|
| 1 | **真源目录** | `agent-delivery/` 或 `.specify/` | 所有 agent 的"项目记忆"在此；CLAUDE.md 式启动指南 |
| 2 | **范围基线** | `scope-baseline.yaml`（带 ±X% 浮动） | 防止 agent 任意扩大范围；甲方/合同对齐 |
| 3 | **架构基线** | `architecture-baseline.md`（决策表 + mermaid + 依赖规则） | Epic 开工前必读；架构师/coordinator 评审依据 |
| 4 | **任务队列** | `task-registry.yaml`（id/agent/repo/depends_on/DoD/evidence） | 机器可读；coordinator 唯一派单源 |
| 5 | **Agent 角色表 + 身份话术** | `agent-handbook.md §5 §9` | 每角色"经验丰富 + 遵循最佳实践"身份注入 |
| 6 | **Handoff 模板** | `templates/handoff-template.md` | 任务完成后的标准交付物，含证据链 |
| 7 | **验收分层** | FULL / INTEG / DEMO 三档 + `demo-fallback-registry.yaml` | 明确什么算真做完、什么允许占位 |
| 8 | **全栈可观测** | OpenTelemetry 强制：Java Agent + Python instrument + 前端 traceId | Tempo/Loki/Prometheus 三联查，验收必查 |
| 9 | **CI/CD 闭环** | 每任务 push → Pipeline 绿 → dev rollout → 对 dev 测试 | 设计类任务 `cicd: skip_design_only` 例外 |
| 10 | **数据契约先行** | 应用层标准表冻结 + 算法侧写 Mock 至 ADS + 数据工厂解耦三方源 | 三方源未定时上层零阻塞、零返工 |

---

## 5. 关键铁律（粘贴即用清单）

复制到项目的"项目工程化交付模式.md"或类似总控文档：

```text
1. 算法只在 Python；业务 API 只在 Java（或对应分层）；前端只调网关后的 Java。
2. 调用链：前端 → 网关 → 业务API（只读契约面/ADS + RPC 调算法）→ 算法层
3. 图谱统一一家产品（如 NebulaGraph），不在项目中途切换。
4. 全栈可观测：Java Agent + Python instrument + 前端 traceId 注入。
5. 每任务 push → Pipeline 绿 → K8s dev rollout → 对 dev 测试。
6. demo / 参考实现只读，禁止 merge 到正式仓。
7. 共享聚合核心：上层多个 BFF / 端复用同一组聚合服务，不重复造。
8. 数据契约先行 + Mock 先行：标准表稳定，三方源经数据工厂接入，不传导契约面。
9. 范围 ±X%：超出基线必须走变更评审。
10. Epic 首任务开工前 + 里程碑签收：调架构师做合规评审。
```

---

## 6. 派单话术模板

### 6.1 通用模板（粘到任何子 agent 会话开头）

```markdown
你正在 {项目代号} 多智能体工程化交付模式中工作。

## 身份
你是 **{agent-name}** —— 一名**经验丰富、严格遵循业界最佳实践**的资深 {角色}。
- 以高内聚低耦合、可维护、可测试、可观测、安全为默认工程标准。
- 决策前先读架构基线与铁律；遇歧义按最佳实践选默认值并在 handoff 说明，不无谓打断。
- 产出生产级质量：命名规范、错误处理完备、关键路径有日志/trace、关键逻辑有测试。
- 严守任务边界（见 task-registry agent 字段与 DoD），不越权改他人职责范围的代码。

## 任务
- ID：{task-id} · Epic：{epic-id} · 标题：{title}

## 路径
- 代码根 / 编排目录 / 文档根（见 paths.yaml）

## 仓库
见 repo-registry.yaml → {repo}

## 必读
- task-registry 本任务 DoD · 架构基线 · 范围基线 · 相关设计参考

## 交付
1. 完成 DoD
2. handoff：agent-handoffs/{task-id}.md
3. push → CI 绿 → dev 测试（设计类除外）
4. 不要反复问；阻塞写 handoff 说明
```

### 6.2 按角色补充身份（一句话）

| 角色 | 身份注入 |
|------|---------|
| coordinator | 资深交付协调人/技术负责人，统筹派单、解阻塞、里程碑签收 |
| architect | 资深系统架构师，精通分层架构/微服务/数据架构/可观测性，**只评审、不写业务代码** |
| algorithm | 资深算法/数据科学工程师，幂等可复现、结果可解释，算法仅 Python |
| api（后端） | 资深 Java/Go 后端，精通 REST/OpenAPI/整洁架构；只读契约面、不写算法、不直连图库 |
| frontend | 资深前端，组件化复用、只经网关调后端、统一 traceId 注入 |
| devops | 资深 DevOps/SRE，CI/Helm/K8s/OTel；IaC、可重复构建、最小权限 |
| data | 资深数据工程师，数仓分层、数据建模、质量血缘；数据契约先行 + Mock |
| integration | 资深集成工程师，网关/SSO/契约测试；外部 API 未就绪先 Mock |
| qa | 资深测试工程师，接口/端到端/性能 + 三联查；基于证据验收 |
| doc | 资深技术文档工程师，借版式不抄原文，可追溯 |

---

## 7. 项目启动 Checklist

### D0（启动当天）
- [ ] 创建 `agent-delivery/`（或 `.specify/`）真源目录
- [ ] 起 `paths.yaml`：`code_root` / `docs_root` / 各 registry
- [ ] 起 `repo-registry.yaml`：所有相关仓的角色 + remote + 本地路径
- [ ] 起 `architecture-baseline.md` 骨架：目标拓扑（mermaid）+ 6–8 项锁定决策 + 机器可读依赖规则
- [ ] 起 `scope-baseline.yaml`：从范围 MD/PRD 抽叶子节点，定 ±X% 浮动
- [ ] 起 `COORDINATOR-START.md`：项目代号、身份、可派单清单、禁止事项

### D1–D3（第一周前段）
- [ ] 起 `task-registry.yaml`：把当前可做的 leaf 任务列全，每条带 `id/agent/repo/depends_on/DoD/evidence/cicd`
- [ ] 起 `agent-handbook.md`：§5 角色表 + §8 通用话术 + §9 各角色话术（含身份注入）
- [ ] 起 `templates/handoff-template.md`
- [ ] 起 `cicd-pipeline.md`：各仓 CI 现状表 + 缺口
- [ ] 起 `observability.md`：OTel 接入约定（Java Agent / Python instrument / 前端 traceId）
- [ ] 起 `数据库设计.md`：分层 + 契约面 + 数据契约先行（如适用）

### Week 1 末
- [ ] 跑通 1 个 leaf 任务全流程（派单 → handoff → CI → dev → 签收），形成模板
- [ ] 架构师做 Epic 0 设计评审，确认基线无歧义
- [ ] 决定并发上限（建议 ≤ 4）与模型分层策略

### 进入稳态后
- [ ] 每个 Epic 首任务开工前调架构师评审
- [ ] 每个里程碑签收调架构师合规评审
- [ ] 每周回顾 task-registry 完成率、阻塞项、token 成本

---

## 8. 反模式（这些坑别踩）

| 反模式 | 为什么坑 | 正确做法 |
|--------|----------|----------|
| 编排者亲自写代码 | 上下文污染、丢全局视角 | Lead 只规划/派单/综合 |
| 工人继承编排者全部对话 | 上下文爆炸、答非所问 | 每个工人 fresh context + 明确边界 |
| 让工人再派工人 | 成本组合爆炸 | 限制递归深度（最多 1 层嵌套） |
| 不分仓不分支同时跑多 agent | 文件级冲突灾难 | Git Worktree per task |
| 任务边界模糊（"实现用户管理"） | 工人漂移 | 具体到接口/页面/文件 + 输出格式 + DoD |
| 没有 DoD 也没有 Handoff | 不知道做没做完 | 每任务必有 DoD + handoff 证据链 |
| 在 Java/前端造假数据 mock | 换真源时全套返工 | 数据契约先行：Python 写 Mock 至 ADS |
| agent 输出直接合 main | 质量灾难 | 必须人审 + CI 全绿门禁 |
| 多 agent 抢同一文件 | 静默覆盖 | Convoy 分组：碰同一文件集 → 同一个 worker 串行 |
| 用 PDF/截图作范围真源 | agent 抽取不准 | 改用 MD/CSV，PDF 仅归档 |

---

## 9. 升级路径（编排成熟度）

| 阶段 | 动作 | 价值 |
|------|------|------|
| **Phase 1**（≤1 周） | task-registry 加 `claimed_by/lock_until` 原子认领字段；写并发≤4 + token 15x + 模型分层规范 | 防双派、控成本 |
| **Phase 2**（2–3 周） | Git Worktree 并行（worktree-per-task）+ Convoy 分组 | 同仓多任务真并行 |
| **Phase 3**（4–6 周） | 自治 coordinator 循环：自研 `scripts/coordinator_loop.py`（用 Cursor SDK）或桥接 [Speckle](https://github.com/JulianDouma/speckle) | 人只在里程碑评审 |
| **Phase 4**（评估后） | 对接 [GitHub Spec Kit](https://github.com/github/spec-kit) 生态（11k★、105 个社区扩展） | 复用开源工具/模板 |

---

## 10. 工具 / 参考链接（精选）

### 编排平台
- [amux](https://amux.io/) — 编排架构 5 层栈 + 看板 + 自愈
- [Speckle](https://github.com/JulianDouma/speckle) — Gastown 模式开源实现（Mayor/Polecat/Convoy）
- Cursor v3 — 原生 8 路并行 + worktree
- Claude Code Agent Teams — Anthropic 官方
- Google Antigravity 2.0 / GitHub Copilot multi-agent workspace

### 规范驱动
- [github/spec-kit](https://github.com/github/spec-kit) — SDD 事实标准
- [Beads](https://github.com/steveyegge/beads) — Issue tracking for AI agents

### 阅读必读
- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Augment — Git Worktrees for Parallel AI Agent Execution](https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution)
- [Mike Mason — AI Coding Agents in 2026](https://mikemason.ca/writing/ai-coding-agents-jan-2026/)

---

## 11. 起步文件模板清单（命名约定）

复制到新项目 `agent-delivery/` 或 `.specify/` 下：

```text
agent-delivery/
├── COORDINATOR-START.md              # 协调者启动指南（项目代号、身份、首批可派单）
├── 项目工程化交付模式.md              # 总控 Prompt（铁律 + 子 Agent 规划）
├── 智能体编排与派单手册.md            # 角色表 + 工作流 + §9 各角色话术
├── architecture-baseline.md          # 架构基线（拓扑 + 锁定决策 + 依赖规则）
├── scope-baseline.yaml               # 范围基线（叶子节点 + ±X%）
├── repo-registry.yaml                # 仓库映射
├── paths.yaml                        # 双根路径（code_root + docs_root）
├── task-registry.yaml                # 任务队列（机器可读）
├── system-wbs.yaml                   # WBS（如适用）
├── 数据库设计.md                      # 含 §数据契约先行（如适用）
├── graph-engine.md                   # 图谱选型（如适用）
├── observability.md                  # OTel 接入约定
├── cicd-pipeline.md                  # 各仓 CI 现状 + 缺口
├── data-source-mapping-registry.yaml # 三方源 → 标准表映射（如适用）
├── acceptance-compliance-policy.md   # 验收分层策略
├── acceptance-authority.yaml         # 验收真源
├── acceptance-review-workflow.md     # qa/doc 验收工作流
├── demo-fallback-registry.yaml       # DEMO 占位登记
├── orchestration-maturity-and-roadmap.md # 编排成熟度 + 升级路线
├── bid-reference/                    # 范围真源 MD（招标/PRD 转写）
├── templates/                        # handoff / acceptance / e2e demo 模板
├── agent-handoffs/                   # 各任务 handoff 产出（运行时填充）
├── 验收文档/                          # 里程碑验收文档（运行时填充）
└── scripts/
    ├── apply_overlay.py              # 同步后自愈脚本
    ├── worktree_spawn.ps1            # 并行 worktree 创建（Phase 2）
    └── coordinator_loop.py           # 自治循环（Phase 3，可选）
```

---

## 12. 变更日志

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-17 | 初版：基于智谱-国科信项目沉淀；融合 2026 SOTA（Anthropic / Spec Kit / Worktree / Gastown）；含落地清单、铁律、话术、Checklist、反模式、起步模板 |

---

> **使用提示**：直接 `Read` 本文给新项目的首个 coordinator 会话作为上下文，再按 §7 Checklist 推进 D0 工作，1 天内即可建起完整编排骨架。
