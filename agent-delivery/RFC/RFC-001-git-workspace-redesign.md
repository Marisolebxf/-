# RFC-001 · Git 工作区布局升级：为团队级 AI 编排与 Worktree 并行铺路

| 字段 | 值 |
|------|------|
| Status | **✅ Reviewed (2026-06-19) → Superseded by [RFC-002](./RFC-002-gkx-v2-greenfield-rebuild.md)（同日）** — 7 项 OPEN 设计原则评审全部通过（详见 §11），但最终采用 RFC-002 的 greenfield rebuild 路径而非 in-place 改造；本 RFC 的设计原则被 RFC-002 §6 / §7 / §10 继承落地 |
| Author | coordinator（AI 辅助起草） |
| Created | 2026-06-19 |
| Reviewed | 2026-06-19（团队管理者一审通过；§11 Q1-Q7 全部勾选"接受"，含 worktree-per-agent / kb-archive / AI 主导实施 / 周扫描 cross-repo-refs 等关键设计原则）|
| Superseded At | 2026-06-19（同日被 RFC-002 替代为执行方案）|
| 保留理由 | RFC-001 §5 目标布局 / §6 路径解耦 / §7 worktree 工作流 / §8 跨仓一致性机制 / §9 onboarding 升级 — 被 RFC-002 §6 直接继承；§11 评审决议被 RFC-002 §15 决策记录引用 |
| Target Phase | 编排成熟度 Phase 0 → Phase 1 → Phase 2 |
| 关联文档 | `orchestration-maturity-and-roadmap.md` §3 Phase 2 · `智能体编排与派单手册.md` §15 · `repo-registry.yaml` · `paths.yaml` · `team-onboarding.md` |
| 评审人 | architect-lead / frontend-lead / backend-lead / algo-lead / qa-lead / PM |
| 评审截止 | （由 PM 设定，建议 1 周内） |
| 决策 OPEN | 见 §10 |

---

## 1. 摘要（Abstract）

当前 `E:\gkx_src` 平面布局在团队 AI 编排 **Phase 1**（共享 rules + 派单手册）阶段是合理的，但在向 **Phase 2**（worktree 并行 + 多 agent 协作 + 跨平台团队上手）推进时暴露 6 个真实阻塞：

1. **`E:\gkx_src` 硬编码到 `paths.yaml` / README / 12+ mdc**——Mac/Linux 用户、D 盘用户、路径带空格用户上手即卡
2. **没有"一键拉齐 13 仓"脚本**——新人 onboarding 手动 clone 13 次 + 手动切分支 + 手动装依赖
3. **Worktree 完全未启用**——多 agent 跑同一仓必须切分支 = 串行
4. **编排仓 ↔ 子仓信息双向同步缺失**（已发生真实案例：本地 ENT IA handoff 与 `topic_demo` 远端代码不同步且互不知情）
5. **分支策略碎片化**（main/dev/feature/* 混用，无规约保证）
6. **`team-onboarding.md` stale**（`gkx_lumen_fronted_display` 实际是 `gkx_lumen_fronted_pc` 等）

本 RFC 提出**最小破坏性的目录重构 + 配置解耦 + 工具脚本化方案**，让团队任意成员（任意 OS / 任意盘符 / 任意盘内路径）能 **1 小时内完成 onboarding 并跑通第一个 AI 任务**，同时为 Phase 2 worktree 并行铺平道路。

---

## 2. 背景与动机（Background & Motivation）

### 2.1 团队规模与协作模式（实际推进时）

| 角色 | 人数估算 | 工作内容 |
|------|---------|---------|
| 架构师 / lead | 3-5 | 跨仓评审 + 派单 + 决策 |
| 后端 Java | 4-6 | gkx_lumen_backend + gkx_service_demo |
| 前端 React | 3-5 | gkx_lumen_fronted_pc / mobile + demo2 + topic_demo |
| 算法 Python | 3-5 | innov-algo-demo + ent-analysis-demo + gkx_demo_python |
| QA | 2-3 | 全仓视觉/集成回归 |
| PM / UE | 2-3 | 编排资产 + 客户沟通 |
| **AI agents（虚拟"工人"）** | **同时并行 ≤ 8** | 12 角色（见编排手册 §9） |

**实际并发量级**：人 (≈25) + agent (≤8) × **多 worktree** = 单一仓内可能同时有 4-6 个 working tree 在改不同分支。

### 2.2 当前布局的"良性 vs 阻塞"二象

```
当前：E:\gkx_src/
├── gkx-orchestration（root 本身）        ← 编排仓 ✅
│   ├── agent-delivery/                   ← 编排资产 ✅
│   ├── .cursor/rules/                    ← 共享 AI 规约 ✅（Phase 1 已达成）
│   ├── 企业分析/、情报检索-甲方承接包/    ← 杂项资料 ⚠️（不属于 agent-delivery）
│   └── README.md                          ← onboarding 入口
│
├── demo2/                                ← 12 个独立 git 仓平铺
├── ent-analysis-demo/                    ← .gitignore 排除 ✅
├── gkx_dataease/
├── gkx_demo_python/
├── gkx_demo_ui/
├── gkx_lumen_backend/                    ← feature/ent-metrics-catalog 分支无 upstream ❌
├── gkx_lumen_fronted_mobile/
├── gkx_lumen_fronted_pc/
├── gkx_service_demo/
├── gkx_ui_demo/
├── innov-algo-demo/
├── topic_demo/                           ← 远端删 ENT IA / 本地团队还在改 ❌
└── （未来 worktree？散乱无统一区） ❌
```

### 2.3 6 个真实阻塞的影响量化

| # | 阻塞 | 影响人天 / 月 | 阻塞 Phase 2 启用 |
|---|------|--------------|--------------------|
| P1 | 硬编码 `E:\gkx_src` | 每个新人 0.5d 摩擦 × 平均 2 人/月 = 1d/月 + 平台被限制为 Windows | ⚠️ Mac/Linux 团队无法加入 |
| P2 | 无 bootstrap 脚本 | 新人 0.5d + 老人换机 0.5d × 每月 2 次 = 2d/月 | ⚠️ |
| P3 | Worktree 未启用 | 多 agent 串行损失 ≈ 30% 并发能力 × 项目 4 周 = 大量延期 | 🔴 **直接阻塞 Phase 2** |
| P4 | 跨仓信息双向同步缺失 | ENT IA 案例：~1 天工作可能白做（如未及时发现） | 🔴 高风险 |
| P5 | 分支策略碎片 | qa-agent 跑错分支 / merge 出错的隐患 | 🟡 |
| P6 | onboarding stale | 每次 stale 1 处 = 1 个新人卡 30 min | 🟡 |

---

## 3. 目标（Goals）

| # | 目标 | 验收 |
|---|------|------|
| G1 | 路径解耦：任意 OS / 任意盘符 / 任意盘内路径都能跑 | 设 `$GKX_ROOT` 环境变量即可，所有 agent / 脚本 / mdc 自动解析 |
| G2 | 1 小时新人 onboarding | `clone orchestration → 一键 bootstrap → 跑首个 AI 任务` 全程 ≤ 60 min |
| G3 | Worktree-per-task 可用 | coordinator 调用 `worktree-spawn` 后，agent 在独立 worktree 干活，不污染主 working tree |
| G4 | 跨仓信息双向一致性 | 编排仓登记的子仓文件被改 / 删时，CI 或周扫描发出告警 |
| G5 | 分支策略规约化 | 每仓在 `repo-registry.yaml` 显式声明 `default_branch` / `feature_prefix` / `protected_branches` |
| G6 | onboarding 文档与代码同步 | 文档由脚本自动生成；命令通过 CI 烟测 |

## 4. 非目标（Non-goals）

| 非目标 | 原因 |
|--------|------|
| 把 12 子仓合并为 monorepo | 子仓已独立 GitLab + 独立 CI/CD + 独立 owner，合并代价 >>> 收益 |
| 改子仓内部目录结构 | 各仓有自己的 owner 和历史，本 RFC 不介入业务代码组织 |
| 引入 git submodule / git subrepo | 跨仓引用问题不靠 submodule 解，靠"显式引用契约 + 跨仓 lint"（见 §6.4） |
| 强制所有人换工具 | 不强制 Cursor 之外的 IDE；脚本兼容 PowerShell 7+ / Bash 4+ |

---

## 5. 设计方案（Proposed Design）

### 5.1 目录布局（目标态）

```
{ANYWHERE}/gkx-workspace/                    ← 任意路径，由用户自选
├── .env                                     ← 🆕 GKX_ROOT 等环境变量（不入 git）
├── .env.example                             ← 🆕 模板（入 git）
│
├── gkx-orchestration/                       ← 主仓（本仓）保持不变
│   ├── agent-delivery/
│   │   ├── ... (现有所有资产)
│   │   └── RFC/                             ← 🆕 本 RFC 所在
│   ├── .cursor/rules/
│   └── scripts/                             ← 🆕 团队级脚本（已有 scripts/ 目录可复用）
│       ├── bootstrap.ps1                    # Windows 一键 onboarding
│       ├── bootstrap.sh                     # macOS/Linux 一键 onboarding
│       ├── sync-all.ps1                     # 一键 fetch + 状态报告
│       ├── worktree-spawn.ps1               # 给 task 创 worktree
│       ├── worktree-cleanup.ps1             # 回收 worktree
│       ├── lint-cross-repo-refs.ps1         # 跨仓引用扫描
│       └── doctor.ps1                       # 体检脚本（路径 / 分支 / 依赖）
│
├── repos/                                   ← 🆕 业务代码父目录
│   ├── demo2/
│   ├── ent-analysis-demo/
│   ├── gkx_dataease/
│   ├── gkx_demo_python/
│   ├── gkx_demo_ui/
│   ├── gkx_lumen_backend/
│   ├── gkx_lumen_fronted_mobile/
│   ├── gkx_lumen_fronted_pc/
│   ├── gkx_service_demo/
│   ├── gkx_ui_demo/
│   ├── innov-algo-demo/
│   └── topic_demo/
│
└── worktrees/                               ← 🆕 worktree 集中区
    ├── lumen_backend.E-INNOV-M1-L03/        # 每个 task 一个 worktree
    ├── lumen_fronted_pc.E-PLATFORM-P0-L07/
    ├── topic_demo.E-E7-POLICY-M1-L05/
    └── ...
```

**关键设计决定**：

| 决定 | 选择 | 不选的原因 |
|------|------|-----------|
| 子仓放在 `repos/` 而非 root | ✅ root 清爽（只剩 orchestration + scripts + worktrees + .env） | 平铺 13 个目录视觉拥挤、和 worktrees/ 混淆 |
| Worktree 单独 `worktrees/` 父目录 | ✅ 集中管理 + 易批量清理 + 不与 repos/ 混 | 散落在各 repo 旁会让 `ls` 输出爆炸 |
| 主仓 `gkx-orchestration/` 不动 | ✅ 保持现有 git 历史 + 现有引用 | 改名 / 移位会破坏所有外部链接 |
| 配置走 `.env` 而非 yaml | ✅ shell + powershell + node 通用，且 .gitignore 自动屏蔽敏感 | yaml 需各语言解析器 |

### 5.2 `.env` 与路径解析

`.env.example`（入 git，新人复制一份为 `.env`）：

```bash
# === 必填 ===
GKX_ROOT=/Users/me/work/gkx                  # macOS 示例
# GKX_ROOT=D:\work\gkx                       # Windows 示例
# GKX_ROOT=/home/me/work/gkx                 # Linux 示例

# === 可选 ===
GKX_DEFAULT_REMOTE=origin                    # 默认 remote
GKX_PARALLEL_LIMIT=4                         # 本地并发 worktree 数上限（团队公约 ≤4）
GKX_BACKGROUND_AGENT_ENDPOINT=               # 留空 = 不用云端 background agent
```

`paths.yaml` 升级为支持环境变量插值：

```yaml
# 旧（硬编码）
code_root: E:/gkx_src
orchestration_dir: E:/gkx_src/agent-delivery

# 新（环境变量插值）
code_root: ${GKX_ROOT}
orchestration_dir: ${GKX_ROOT}/gkx-orchestration/agent-delivery
repos_root: ${GKX_ROOT}/repos
worktrees_root: ${GKX_ROOT}/worktrees
```

mdc 里所有路径占位符同步替换：

```
旧：e:/gkx_src/demo2/src/sandbox/...
新：${GKX_ROOT}/repos/demo2/src/sandbox/...
```

agent / 脚本 / Cursor 读 `.env` → 解析 `${GKX_ROOT}` 即可。

### 5.3 Bootstrap 脚本接口（解开 P1 P2 P6）

```powershell
# 新人入职：
mkdir D:\work\gkx; cd D:\work\gkx
git clone https://gitlab.htmisoft.net/SZCGKX/gkx-orchestration.git
cd gkx-orchestration

# 一键 bootstrap（按角色，可选）
.\scripts\bootstrap.ps1 -Role frontend     # 只拉前端相关 4 仓
.\scripts\bootstrap.ps1 -Role full         # 全 13 仓
.\scripts\bootstrap.ps1 -Role backend -DryRun  # 看会发生什么，不执行

# bootstrap 自动：
# 1. 推断 GKX_ROOT = 当前目录的父级
# 2. 生成 .env（位于 GKX_ROOT 根）
# 3. 读 repo-registry.yaml 按 role 筛仓
# 4. clone 到 ../repos/{repo-name}
# 5. 切到每仓的 default_branch（来自 repo-registry）
# 6. 装依赖（npm / mvn / pip 按 repo 类型）
# 7. 自检：所有仓远端可达 / .cursor/rules 加载到位 / agent 试运行
# 8. 输出 onboarding-report.md 给新人 + mentor

# bootstrap 不做的事：
# - 不创建 worktrees（按需调用 worktree-spawn）
# - 不修改任何子仓内容（只 clone）
# - 不强制装 IDE / shell（脚本兼容 PS7+/Bash4+）
```

### 5.4 Worktree 工作流（解开 P3）

**派单时 coordinator-agent 调用**：

```powershell
.\scripts\worktree-spawn.ps1 `
    -Repo lumen_backend `
    -TaskId E-INNOV-M1-L03 `
    -BaseBranch dev `
    -Agent algorithm-agent

# 自动执行：
# cd $GKX_ROOT/repos/gkx_lumen_backend
# git fetch origin
# git worktree add $GKX_ROOT/worktrees/lumen_backend.E-INNOV-M1-L03 \
#     -b feat/E-INNOV-M1-L03 origin/dev
# 输出 agent 派单卡：
#   cwd: $GKX_ROOT/worktrees/lumen_backend.E-INNOV-M1-L03
#   branch: feat/E-INNOV-M1-L03
#   base: origin/dev (commit 28a1914)
#   handoff: agent-handoffs/平台基建-PLATFORM/E-INNOV-M1-L03-java-build.md
```

**agent 完工后回收**：

```powershell
.\scripts\worktree-cleanup.ps1 -TaskId E-INNOV-M1-L03 -Action push-and-mr

# 自动执行：
# - 推 feat/E-INNOV-M1-L03 到 origin
# - glab mr create / gh pr create（按 repo 类型）
# - 等评审通过后 git worktree remove $GKX_ROOT/worktrees/lumen_backend.E-INNOV-M1-L03
```

**Convoy 防冲突**（与 roadmap 一致）：

`task-registry.yaml` 增加字段：

```yaml
- id: E-INNOV-M1-L03
  worktree_files_touched:
    - "src/main/java/com/gkx/innov/**"
    - "pom.xml"
  convoy_group: backend-pom-touchers  # 同 group 的 task 必须串行
```

`worktree-spawn.ps1` 检查 convoy_group 内是否已有活跃 worktree，有则报错（防双派）。

### 5.5 跨仓信息一致性机制（解开 P4）

新增 `agent-delivery/cross-repo-refs.yaml`：

```yaml
# 编排仓对子仓文件的"显式引用契约"
# 子仓动这些文件时必须 [notify-orchestration]
# coordinator-agent / BugBot 定期 lint 失效引用

version: 1
refs:
  - referenced_from: agent-delivery/agent-handoffs/企业战略分析-ENT/UX-ENT-elements-ia-wireframe-gap.md
    repo: topic_demo
    files:
      - docs/ia/enterprise/ENT-IA.md
      - docs/ia/enterprise/ENT-functional-design-v2.md
      - docs/ia/enterprise/ENT-userflow.md
    severity: hard   # hard=失效=破坏；soft=失效=告警
    owner: ux-lead

  - referenced_from: agent-delivery/data/企业域数据库设计(v1).md
    repo: gkx_lumen_backend
    files:
      - src/main/resources/db/migration/V*__ent_*.sql
    severity: soft
    owner: backend-lead
```

`scripts/lint-cross-repo-refs.ps1` 周扫描：
- 对每个 ref，`cd $GKX_ROOT/repos/{repo}` → 检查文件是否存在 + 内容是否大幅变化
- 失效则告警到 coordinator + owner（可走 Slack / Teams webhook）

子仓的 `.pre-push` hook（可选，未来 Phase 2 加）：
- 扫本次推送是否动 cross-repo-refs.yaml 登记的文件
- 动了就要求 commit message 含 `[notify-orchestration]`

### 5.6 分支规约（解开 P5）

`repo-registry.yaml` 每仓增加 `branch_strategy`：

```yaml
repos:
  - id: ui_pc
    name: gkx_lumen_fronted_pc
    branch_strategy:
      default_branch: main         # bootstrap 后默认 checkout
      dev_branch: dev              # 集成分支
      feature_prefix: feat/        # feature 分支命名前缀
      protected_branches: [main]   # 不允许 force push
      mr_target: dev               # feature → dev → main
```

`worktree-spawn.ps1` 按此规约创建 feature 分支。

---

## 6. 落地路线（Rollout Plan）

### Phase 0 · 立即（半天） · 无破坏性

| Step | 内容 | 验收 |
|------|------|------|
| 0.1 | 写 `scripts/bootstrap.ps1` / `bootstrap.sh` / `sync-all.ps1` / `doctor.ps1` | 自检脚本能跑过 |
| 0.2 | 写 `.env.example` + 改 `paths.yaml` 支持 `${GKX_ROOT}` | 老路径 `E:\gkx_src` 仍能工作（向后兼容） |
| 0.3 | 写 `cross-repo-refs.yaml` 初始版本（含 ENT IA 案例） | 跑一次 `lint-cross-repo-refs.ps1` 出报告 |
| 0.4 | RFC-001 本文档评审 + 决策（见 §10） | 团队 leads 签字（电子） |

**不动现有目录、不动现有 mdc 路径**。

### Phase 1 · 本周（1-2 天） · 目录迁移

| Step | 内容 | 验收 |
|------|------|------|
| 1.1 | 全员 commit + push 本地所有未提交工作 | git status 全员 clean |
| 1.2 | 用 `scripts/migrate-to-repos-subdir.ps1` 把 12 子仓挪到 `repos/` | 13 仓在 `repos/` + worktrees/ 空目录建立 |
| 1.3 | 改 README + onboarding + mdc 路径占位符为 `${GKX_ROOT}/repos/...` | 跑 `doctor.ps1` 全绿 |
| 1.4 | 给 12 仓的 GitLab webhook 加上 cross-repo notify（如能力允许） | 推一次 commit 触发 notify 看效果 |
| 1.5 | 全员重新跑一次 `.\scripts\bootstrap.ps1 -Update` 同步新布局 | 全员可正常 commit / pull |

### Phase 2 · 短期（2-3 周，与 roadmap 同步） · Worktree 启用

| Step | 内容 | 验收 |
|------|------|------|
| 2.1 | 完成 `worktree-spawn.ps1` / `worktree-cleanup.ps1` | 试创建 1 个 worktree 跑通 |
| 2.2 | 编排手册 §15 落地（worktree-per-task 默认） | task-registry 新派单都用 worktree |
| 2.3 | 在 E-INNOV-M1 剩余可并行 task 上演练 4 路并行 | 4 agent 同时跑、合并无冲突 |
| 2.4 | task-registry 增加 `worktree_files_touched` + `convoy_group` 字段 | Convoy 防冲突生效 |
| 2.5 | `lint-cross-repo-refs.ps1` 接 CI 周扫描 + Slack/Teams 告警 | 失效引用自动报告 |

### Phase 3 · 中期（与 roadmap Phase 3 同步） · 自动化

- coordinator 循环：从 task-registry 拉 leaf → 调 worktree-spawn → 派 agent → 收 handoff → cleanup
- 跨仓 BugBot 双层评审
- onboarding 报告自动化生成 + 入职质量度量

---

## 7. 风险评估（Risks & Mitigations）

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| **R1** Phase 1 迁移日全员本地工作丢失 | 低 | 高 | 强制 §1.1 全员 push + 由 PM 验证 commit hash 全员一致后再迁移 |
| **R2** 老路径硬链接外部依赖（如别人的脚本 / IDE 工作区）失效 | 中 | 中 | Phase 0 升级 `paths.yaml` 时同时保留旧 key 别名（如 `legacy_code_root: ${GKX_ROOT}`），N 周后再删 |
| **R3** worktree 创建后 agent 不清理，磁盘膨胀 | 中 | 低 | `doctor.ps1` 周自检：worktree 列表 + 各 worktree 最后活动时间，>14d 未活动告警 |
| **R4** cross-repo-refs.yaml 维护成本高 | 中 | 中 | 初版只覆盖 P0 痛点（如 ENT IA、Design.md）；其余按需扩 |
| **R5** Convoy 分组判断错误导致 agent 互锁 | 低 | 中 | `worktree-spawn.ps1` 默认非 dry-run 时强制人审 convoy_group 配置；提供 `--force` 走特殊情况 |
| **R6** 跨平台 PowerShell / Bash 行为差异 | 中 | 中 | 用 PS7+（跨平台）+ 关键脚本同时提供 .ps1 / .sh 两版 + CI 跑两套 |
| **R7** 团队不愿意改路径 | 中 | 高 | Phase 0 完全向后兼容（老 `E:\gkx_src` 仍可用）；Phase 1 迁移由 lead 主导、提供"换机即顺便迁"的契机 |

---

## 8. 替代方案对比（Alternatives Considered）

| 方案 | 优 | 劣 | 是否采用 |
|------|---|---|---------|
| **A1 不动布局，仅解耦路径 + 加脚本** | 风险最小 | 不解决 worktree 散乱、不解决目录拥挤 | 否（Phase 0 实际是 A1 的子集，作为过渡） |
| **A2 本 RFC 推荐方案：repos/ + worktrees/ 子目录** | 解决全部 6 个阻塞、为 Phase 2/3 铺路 | 一次性迁移成本（Phase 1 半天） | ✅ |
| **A3 全 monorepo（用 Lerna/Turborepo 合并 12 仓）** | 极致一致性、单 PR 跨仓改动 | 与各仓独立 owner / 独立 CI / 独立 GitLab 完全冲突 | 否（违反非目标 §4） |
| **A4 git submodule 把 12 仓挂到 orchestration** | 单 clone 拉齐全部 | submodule 操作复杂、新人理解成本高、跨仓 commit 体验差 | 否 |
| **A5 worktree 散在各 repo 旁** | 不需要 worktrees/ 子目录 | `ls` 输出爆炸、批量清理难、agent 找 cwd 不便 | 否 |

---

## 9. 影响评估（Impact Assessment）

| 涉及方 | 影响 | 工作量 |
|--------|------|--------|
| 全员 | 一次性迁移本地路径（Phase 1） | 0.5 人天/人 |
| architect lead | 评审 RFC + 监督 Phase 1 迁移 + 维护 cross-repo-refs.yaml | 1-2 人天 |
| DevOps（如有） | bootstrap.ps1/sh + doctor + CI 接入 | 2-3 人天 |
| 现有 mdc / 编排手册 / paths.yaml | 路径占位符全量替换 | 0.5 人天（一次性） |
| 现有 task-registry | 增加 worktree_files_touched / convoy_group 字段（增量） | 渐进，每个新 task 派单时加 |
| onboarding 文档 | 改写为基于 bootstrap | 0.5 人天 |

总计：**约 5-7 人天，分摊到 2-3 周**。

---

## 10. 等待团队 leads 决策的 OPEN 问题

### Q1 · 目录布局接受度

> §5.1 推荐的 `gkx-workspace/{gkx-orchestration, repos/, worktrees/, .env}` 布局，是否接受？

- [x] ✅ 接受，按 §6 路线推进
- [ ] ⚠️ 接受布局但调整命名（请注明：____）
- [ ] ❌ 不接受，保持现状

### Q2 · 路径解耦策略

> §5.2 推荐用 `.env + ${GKX_ROOT}` 替代硬编码 `E:\gkx_src`，是否接受？

- [x] ✅ 接受
- [ ] ⚠️ 接受但偏好其他方案（如纯 `~/.gkx/config.yaml`？请注明）
- [ ] ❌ 保持硬编码（请说明为什么 Mac/Linux 用户不进入团队也 OK）

### Q3 · Phase 1 迁移日

> §6 Phase 1 需要全员配合一次"commit + 迁移目录"，建议日期？

- [x] 本周内（具体日期：____）
- [ ] 下周内（具体日期：____）
- [ ] 与某个 milestone 合并（如某次 release 后，请注明：____）

### Q4 · Worktree 启用范围

> §6 Phase 2 worktree 默认模式，是 worktree-per-task 还是 worktree-per-agent？

- [ ] worktree-per-task（每个 task 一个 worktree，roadmap 推荐）
- [x] worktree-per-agent（每个 agent 一个长期 worktree，长会话 + 暖缓存）
- [ ] 混合（短任务 per-task，长任务 per-agent）

### Q5 · 跨仓引用 lint 触发频率

> §5.5 cross-repo-refs.yaml lint 频率？

- [x] 周扫描（默认推荐）
- [ ] 日扫描
- [ ] 每次 push 触发 webhook 实时扫描
- [ ] 仅人工触发

### Q6 · 编排仓"杂项目录"清理

> 当前 root 还有 `企业分析/` / `情报检索-甲方承接包/` 等不属于 agent-delivery 的资料目录，是否在 Phase 1 一并归位？

- [ ] 归到 `agent-delivery/wbs-archive/` 子目录
- [x] 归到新建 `kb-archive/`（与 knowledge-base/ 并列）
- [ ] 保持现状

### Q7 · DevOps 资源

> §9 总计 5-7 人天，谁主导？

- [x] AI agent（coordinator + devops-agent + 人审）
- [ ] 指定某 lead 人工实施
- [ ] 等到有 DevOps 团队再做

---

## 11. 附录

### A1 · 脚本接口设计草案

```
scripts/
├── bootstrap.ps1            # 参数：-Role <full|frontend|backend|algo|qa> -Update -DryRun
├── bootstrap.sh             # 同 bootstrap.ps1
├── sync-all.ps1             # 参数：-FetchOnly -ReportOnly
├── worktree-spawn.ps1       # 参数：-Repo -TaskId -BaseBranch -Agent
├── worktree-cleanup.ps1     # 参数：-TaskId -Action <push-and-mr|discard|archive>
├── lint-cross-repo-refs.ps1 # 参数：-Severity <hard|soft|all> -Output <md|json|console>
├── doctor.ps1               # 参数：-Verbose
└── migrate-to-repos-subdir.ps1  # 一次性脚本，Phase 1 执行
```

### A2 · `.env.example` 完整版

```bash
# === 必填 ===
# 工作区根目录的绝对路径（任意 OS / 任意盘符）
GKX_ROOT=

# === 可选 ===
# 默认 git remote 名（一般无需改）
GKX_DEFAULT_REMOTE=origin

# 本地并发 worktree 上限（团队公约 ≤4）
GKX_PARALLEL_LIMIT=4

# Background Agent endpoint（云端长任务，留空 = 不启用）
GKX_BACKGROUND_AGENT_ENDPOINT=

# 跨仓 lint 告警 webhook（Slack / Teams 等）
GKX_LINT_ALERT_WEBHOOK=
```

### A3 · 与 `orchestration-maturity-and-roadmap.md` 的对齐

| roadmap 项 | 本 RFC 对应 |
|------------|------------|
| Phase 2 · ORCH-L02 worktree-per-task | §5.4 + §6 Phase 2 |
| Phase 2 · Convoy 分组 | §5.4 末段 |
| Phase 2 · 派单话术加 worktree_branch | §5.6 + §5.4 |
| Phase 3 · 自动 coordinator 循环 | §6 Phase 3 |

本 RFC **不替代** roadmap，是 roadmap Phase 2 的**目录与脚本层落地方案**。

### A4 · 与 `team-collaboration-playbook.md §4.5` 的对齐

playbook 已提"Worktree + 多 agent 面板（Cursor v3 最多 8 路）"+ "本地并发上限 4"，本 RFC 提供具体目录 / 脚本 / Convoy 实现。

---

## 12. 变更记录（Change Log）

| 版本 | 日期 | 改动 |
|------|------|------|
| v0.1 | 2026-06-19 | 初稿（coordinator 起草） |
