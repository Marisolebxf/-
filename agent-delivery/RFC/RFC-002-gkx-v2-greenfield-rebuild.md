# RFC-002 · gkx-lumen 全新根目录重做方案（Greenfield Rebuild）

| 字段 | 值 |
|------|------|
| Status | **✅ Reviewed（已评审通过 2026-06-19）** — 团队管理者本轮 10 项 OPEN 决议已收口，详见 §13 与 §15 |
| Author | coordinator（AI 辅助起草，基于本轮 8 个战略+执行决议 + 评审反馈整合） |
| Created | 2026-06-19 |
| Reviewed | 2026-06-19（团队管理者一审通过；待 leads 异步追认 §13 中 architect / backend / PM 主导项） |
| Supersedes | **RFC-001（in-place 改造方案）** — 详见 §11 |
| Target Phase | 编排成熟度 Phase 1 → Phase 2 → Phase 3（直接跨越） |
| 关联文档 | `RFC-001-git-workspace-redesign.md`（被替代但其目标布局被继承）· `architecture-baseline.md` · `repo-registry.yaml` · `智能体编排与派单手册.md` |
| 评审人 | 团队管理者（决策✅） · architect-lead · frontend-lead · backend-lead · algo-lead · qa-lead · PM |
| 切换日（M6） | **触发式**（条件 = "老根所有未 push 内容已备份到老 GitLab"；默认目标窗口 2026-12-04 ± 2 周） — 详见 §8.3 |
| 已决议清单 | 见 §13（10 项全部已决） |
| 决议记录 | 见 §15 |
| **实际落地名（M1 后追加）** | **GitLab group = `gkx-lumen`，本地路径 = `E:/gkx-lumen`** — RFC 文件名保留 `RFC-002-gkx-v2-greenfield-rebuild.md` 仅作历史 ID；正文中原 `gkx-v2/` group 引用已全局替换为 `gkx-lumen/`（M1 commit 24f76b0 后） |

---

## 1. 摘要（Abstract）

本 RFC 提议**放弃在 `E:\gkx_src` 现有目录上做 in-place 改造**（即 RFC-001 方案），转而**在 GitLab 新建 `gkx-lumen/` group**，按业界最佳实践从零构建新根，6 个月内逐步把所有职责迁移过去，最终把老根 archive。

### 1.1 核心战略决议（本轮已定）

| ID | 问题 | 决议 | 工程含义 |
|----|------|------|---------|
| **S1** | 老根命运 | 6 个月内 deprecate | 新根是明确替代品，2026-12 前完成切换 |
| **S2** | 复用边界 | 选择性搬 + **不保 git history** | 用 `cp -r` 而非 `git filter-repo`，迁移成本大幅降低 |
| **S3** | 双轨期同步策略 | 不同步，切换日前一次性搬 | M4 起老根必须冻结新功能，否则切换日搬运量爆炸 |
| **E1** | 新根位置 | **GitLab 新 group `gkx-lumen/`** | 全团队可访问，本地 clone 使用 |
| **E2** | 子仓形态 | 待评估（本 RFC §7 给决策表） | 详见 §7 |
| **E5** | 本轮交付物 | 起草 RFC-002（本文件） | — |

### 1.2 三句话总结

1. **不在 `E:\gkx_src` 改造，新开 GitLab `gkx-lumen/`，4-6 周内做到"新人 1 小时上手"**
2. **选择性复用编排核心（agent-delivery + .cursor/rules + Design.md），不保 git history，业务子仓重新 clone**
3. **6 个月渐进迁移：M1 脚手架 → M2-M3 lead 试运行 → M3-M4 全员灰度 → M4-M5 老根冻结 → M6 切换日**

---

## 2. 背景与动机

### 2.1 为什么不走 RFC-001（in-place 改造）

RFC-001 提出在 `E:\gkx_src` 上改造，本质是"修房子"。审视后发现 3 个深层问题修不动：

| 问题 | RFC-001 能解决吗 | 根因 |
|------|---|---|
| 13 仓平铺、命名混乱（`gkx_lumen_fronted_pc` vs `gkx_demo_ui`）| ❌ 不能 | 改名会破坏所有外部引用、CI、PR |
| 老根 `.git` history 含大量过期文件（如 `.admin-ui.b64`、stale 文档） | ❌ 不能 | history 一旦提交无法 retro 清理 |
| `企业分析/`、`创新监测-开发承接包/` 等业务承接包混在编排根 | 部分能 | 仅能用 `.gitignore` 排除，仍在目录里碍眼 |
| 多 agent worktree 区缺位 | ✅ 能 | RFC-001 §5 已提案 |
| 硬编码路径 | ✅ 能 | RFC-001 §6 已提案 |

→ RFC-001 能解决 60% 痛点，但**结构性问题（仓库命名、历史包袱、根目录卫生）只有重做能根治**。

### 2.2 重做的契机

- 项目处于"编排手册稳态、Design.md v2 刚换、企业要素 IA 收尾"的中间窗口
- 团队尚未规模化（≈25 人），重新对齐成本可控
- 6 个月后正好对齐下一阶段（创新监测 / 政策模块）启动
- gkx_lumen_backend 多分支无 upstream 等历史伤口可以一次性愈合

### 2.3 不重做的代价

继续 in-place 改造 6 个月后：
- 老根 `.git` 累积更多过期文件，未来重做成本更高
- 仓库命名不规范进一步固化（如 `gkx_lumen_fronted_pc` 会被外部系统硬编码引用）
- 团队对"老根布局"产生路径依赖，未来抗拒迁移

---

## 3. 目标与非目标

### 3.1 目标（Must）

| # | 目标 | 验收 |
|---|------|------|
| G1 | 新根布局符合业界最佳实践（monorepo of rules + polyrepo of code + worktree-native） | architect-lead 签字 |
| G2 | 新根 onboarding ≤ 1 小时（任意 OS / 任意盘符） | 至少 2 名新人独立完成 |
| G3 | 老根 6 个月内完全 deprecate（read-only archive） | M6 切换日 `chmod -w` |
| G4 | 编排核心资产（agent-delivery / .cursor/rules / Design.md）100% 等价迁移 | 全部 .mdc 规则在新根可运行 |
| G5 | 双轨期甲方交付不受影响（老根继续主战场） | 当前 in-flight task 全部在老根收尾 |
| G6 | 新根 Phase 2 worktree 直接可用（无需后续重构） | 任意子仓可同时跑 ≥ 3 worktree |

### 3.2 非目标（Won't）

| # | 非目标 | 理由 |
|---|------|------|
| N1 | 保留所有 git history | S2 已定不保 |
| N2 | 合并所有 12 子仓为 monorepo | 风险大、收益小（见 §7） |
| N3 | 在新根重写 Design.md / 规则 | 已稳定，等价迁移 |
| N4 | M0-M3 期间把任何 in-flight task 强行搬到新根 | 干扰甲方交付 |
| N5 | 6 个月内启用 GitLab 新实例 | 用现有实例的新 group 即可 |

---

## 4. 现状 Inventory（2026-06-19 扫描）

### 4.1 12 个 git 仓库

| # | 仓库 | 当前分支 | Commits | 大小 | 最后活跃 | 业务定位 | 健康度 |
|---|---|---|---|---|---|---|---|
| 1 | **demo2** | main | 84 | 455 MB | 2026-06-18 | DS-25 软科学 Arco/D8/D9 试点 | 🟢 |
| 2 | **ent-analysis-demo** | main | 11 | 0.8 MB | 2026-06-18 | 企业分析 algorithm-agent 算法仓 | 🟢 |
| 3 | **gkx_dataease** | main | 22 | 218 MB | 2026-05-26 | 开源 DataEase fork | 🟢 |
| 4 | **gkx_demo_python** | main | 3 | 0.1 MB | 2026-05-06 | Python demo（极低活跃） | 🟡 |
| 5 | **gkx_demo_ui** | main | 24 | 4 MB | 2026-06-14 | UI demo（entan-graph 等） | 🟢 |
| 6 | **gkx_lumen_backend** | feature/ent-metrics-catalog ⚠️ | 6 | 31 MB | 2026-06-18 | Spring Cloud 后端 11 模块 | 🟡 分支无 upstream |
| 7 | **gkx_lumen_fronted_mobile** | main | 1 | 0 MB | 2026-06-08 | 移动端骨架（几乎空仓） | 🟡 |
| 8 | **gkx_lumen_fronted_pc** | main | 12 | 9 MB | 2026-06-10 | PC 前端 | 🟢 |
| 9 | **gkx_service_demo** | main | 58 | 25 MB | 2026-06-15 | Spring Cloud 后端 16 模块 + helm | 🟢 |
| 10 | **gkx_ui_demo** | main | 7 | 7 MB | 2026-04-26 | UI demo（旧版） | 🟡 久未维护 |
| 11 | **innov-algo-demo** | main | 7 | 240 MB | 2026-06-13 | 创新算法 demo（大数据） | 🟢 |
| 12 | **topic_demo** | feat/ent-elements-build | 16 | 350 MB | 2026-06-19 | 主战场专题前端（当下主力） | 🟢 |

**统计**：12 仓 / 1338 MB / 主战场 3-4 仓（topic_demo / demo2 / gkx_lumen_backend / ent-analysis-demo）

### 4.2 根目录非仓项

| 项 | 类型 | 大小 | 内容 | 处置（预案） |
|---|---|---|---|---|
| `agent-delivery/` | Dir | ~10 MB | 编排核心（必搬） | ✅ 白名单 |
| `.cursor/rules/` | Dir | 0.07 MB | 13 个 .mdc agent 规则 | ✅ 白名单 |
| `knowledge-base/` | Dir | 0 MB | 1 个 playbook | ✅ 白名单（轻量） |
| `企业分析/` | Dir | 0.2 MB | 2 文件（含 db/ 子目录、技术能力评估 demo） | 🟡 灰名单（评估归属） |
| `创新监测-开发承接包/` | Dir | 0.1 MB | 8 文件（00-总体、01-DB、02-算法...07-标注） | 🟡 灰名单（甲方承接包，可能归 agent-delivery/验收文档/） |
| `COORDINATOR-START.md` | File | 0 KB | 空占位 | ❌ 黑名单 |
| `.admin-ui.b64` | File | 11 KB | base64 编码（4 月未动） | ❌ 黑名单（疑似 dataease admin 模板，留老根） |
| `2gkxx.sql.b64` | File | 195 KB | base64 编码 SQL dump（4 月未动） | ❌ 黑名单（数据 dump，留老根 / 数据团队收回） |
| `README.md` | File | 78 行 | 根说明 | ✅ 白名单（搬，但重写为 gkx-lumen 版） |
| `.gitignore` | File | — | 根 ignore 规则 | ✅ 白名单（重写） |

---

## 5. 复用清单：白名单 / 灰名单 / 黑名单

### 5.1 ✅ 白名单（必搬 + 等价迁移）

#### A. 编排核心（agent-delivery/）

```
agent-delivery/
├── README.md                              ← 重写为 gkx-lumen 版
├── architecture-baseline.md               ← 全搬，更新 §changelog
├── repo-registry.yaml                     ← 全搬，paths 改为 $GKX_ROOT 相对
├── task-registry.yaml                     ← 全搬
├── 智能体编排与派单手册.md                ← 全搬
├── 角色AI协作对比手册.md                  ← 全搬
├── team-collaboration-playbook.md         ← 全搬
├── data-lineage-policy.md                 ← 全搬
├── Design.md                              ← 全搬
├── 项目工程化交付模式.md                  ← 全搬
├── orchestration-maturity-and-roadmap.md  ← 全搬
├── team-onboarding.md                     ← 重写（路径变化）
├── paths.yaml                             ← 重写（去硬编码）
├── data/                                  ← 全搬（企业域 DB 设计等）
├── 验收文档/                              ← 全搬
├── 培训/                                  ← 全搬
├── agent-handoffs/                        ← 全搬 6 个功能子目录（仅保最终态，删 .draft/.local）
└── RFC/                                   ← 仅搬 RFC-001（标 Superseded）+ RFC-002（本文件）
```

#### B. AI 规则（.cursor/rules/）

13 个 .mdc 全搬：
- `00-team-constitution.mdc`
- `algorithm.mdc`, `api.mdc`, `architect.mdc`, `coordinator.mdc`, `data.mdc`, `devops.mdc`, `doc.mdc`, `frontend.mdc`, `pm.mdc`, `qa.mdc`, `ui.mdc`, `ux.mdc`

#### C. 知识库

- `knowledge-base/multi-agent-orchestration-playbook.md` → 整体搬

#### D. 业务子仓（重新 clone，不搬代码）

详见 §7 决策表。

### 5.2 🟡 灰名单（评估后定）

| 项 | 待决问题 | 推荐 |
|---|---|---|
| `企业分析/` | 是否归入 `agent-delivery/验收文档/企业分析/` | **建议归入**（业务承接包属于编排资产） |
| `创新监测-开发承接包/` | 是否归入 `agent-delivery/验收文档/创新监测/` | **建议归入** |
| `gkx_ui_demo` 仓 | 是否搬到新根 | **建议 archive 不搬**（4 月以来未动） |
| `gkx_demo_python` 仓 | 是否搬到新根 | **建议 archive 不搬**（仅 3 commits） |
| `gkx_lumen_fronted_mobile` 仓 | 空仓是否搬 | **建议搬**（业务规划保留） |
| `agent-handoffs/` 中的 `.draft` / `.local` 文件 | 是否带过去 | **不带**（按 S2 决议） |

### 5.3 ❌ 黑名单（不搬，6 个月后随老根 archive）

| 类别 | 项 | 理由 |
|------|------|------|
| Git 内部 | 所有 `.git/` 目录 | S2 决议不保 history |
| 构建产物 | `node_modules/`, `dist/`, `build/`, `target/`, `.venv/`, `__pycache__/` | 必须重新构建 |
| 环境配置 | 各仓 `.env` 局部文件、`.env.local` | 必须重新配置（避免泄密） |
| 历史草稿 | `*.draft.md`, `*.local.md`, `_old_*` | 已 supersede |
| 终端日志 | `terminals/`, `*.log`, `debug-*.txt` | 临时文件 |
| 大型二进制 | `.admin-ui.b64`, `2gkxx.sql.b64` | 由数据团队/dataease lead 决定是否回收 |
| 空文件 | `COORDINATOR-START.md`（0 KB） | 已废弃 |
| 旧 UI 规范 | （已删）`AI可复用UI框架与设计规范.md` | 已被 Design.md 替代 |
| 老 PR / 评审日志 | 留在老根 GitLab MR | 不携带到新根 |

---

## 6. 新根目标布局

继承 RFC-001 §5 的设计，做小幅调整：

```
gkx-lumen/                          ← GitLab group（全员可访问）
│
├── gkx-orchestration/           ← 主仓（你 clone 后看到的第一个）
│   ├── .cursor/
│   │   └── rules/               ← 13 个 .mdc agent 规则
│   ├── agent-delivery/          ← 编排核心（全搬）
│   ├── knowledge-base/
│   ├── scripts/                 ← 🆕 新增：bootstrap / sync / verify 脚本
│   │   ├── bootstrap.sh         ← 一键 onboarding（Linux/Mac）
│   │   ├── bootstrap.ps1        ← 一键 onboarding（Windows）
│   │   ├── sync-all.sh          ← 一键 pull 所有子仓
│   │   ├── verify-paths.sh      ← 检查无硬编码路径残留
│   │   └── worktree-helper.sh   ← worktree 创建/清理
│   ├── .env.example             ← 🆕 GKX_ROOT 等环境变量模板
│   ├── .gitignore               ← 重写（含 /repos/ /worktrees/）
│   ├── README.md                ← 重写
│   └── ARCHIVE-OLD-ROOT.md      ← 🆕 老根 archive 指引（M6 启用）
│
├── repos/                       ← 业务子仓挂载点（每个独立 git，由 bootstrap clone）
│   ├── demo2/
│   ├── ent-analysis-demo/
│   ├── gkx_dataease/
│   ├── gkx_demo_ui/
│   ├── gkx_lumen_backend/
│   ├── gkx_lumen_fronted_mobile/
│   ├── gkx_lumen_fronted_pc/
│   ├── gkx_service_demo/
│   ├── innov-algo-demo/
│   └── topic_demo/
│   (gkx_demo_python / gkx_ui_demo 不搬，留老根 archive)
│
├── worktrees/                   ← 🆕 worktree 集中存放区（按 epic / agent 隔离）
│   ├── topic_demo--E-INNOV-M1/
│   ├── topic_demo--E-ENT-IA/
│   ├── gkx_lumen_backend--E-ENT-METRICS/
│   └── ...
│
└── .git-template/               ← 🆕 hooks 模板（统一 pre-commit / commit-msg 规约）
```

**与 RFC-001 §5 的差异**：
- 加入 `ARCHIVE-OLD-ROOT.md`（M6 启用）
- 加入 `.git-template/`（hooks 模板）
- 不带 `worktrees/{ai-1,ai-2,ai-3}` 通用编号（改用 `{repo}--{epic}` 命名，更可读）

---

## 7. E2 决策表：12 子仓在新根的形态

### 7.1 评估矩阵

| 仓库 | 体量 | 活跃 | 业务独立性 | 合并候选 | **决策** | 理由 |
|---|---|---|---|---|---|---|
| **gkx_dataease** | 218 MB | 中 | 高（开源 fork） | 无 | **独立** | fork 必须独立才能同步上游，合并即断 |
| **gkx_lumen_backend** | 31 MB | 高 | 高（11 模块 Spring Cloud） | gkx_service_demo | **独立** | 包名/模块名都不同，合并需重命名 200+ 文件，风险高、收益小 |
| **gkx_service_demo** | 25 MB | 中 | 高（16 模块 + helm） | gkx_lumen_backend | **独立** | 同上 |
| **gkx_lumen_fronted_pc** | 9 MB | 中 | 中 | gkx_lumen_fronted_mobile | **独立（Phase 1）** | mobile 几乎空，先独立；Phase 2 再考虑合 pnpm workspace |
| **gkx_lumen_fronted_mobile** | 0 MB | 极低 | 中 | gkx_lumen_fronted_pc | **独立（Phase 1）** | 同上 |
| **topic_demo** | 350 MB | 极高 | 高（主战场） | 无 | **独立** | 主战场仓，不可动 |
| **demo2** | 455 MB | 高 | 高（DS-25 试点） | 无 | **独立** | 试点仓独立 |
| **gkx_demo_ui** | 4 MB | 中 | 中 | 无 | **独立** | 活跃 demo |
| **ent-analysis-demo** | 0.8 MB | 高 | 高（企业算法） | innov-algo-demo | **独立** | 不同算法主题 |
| **innov-algo-demo** | 240 MB | 中 | 高（创新算法） | ent-analysis-demo | **独立** | 数据量大，独立管 |
| **gkx_ui_demo** | 7 MB | 极低（4月） | 低 | 无 | ❌ **不搬，archive** | 4 月以来零活跃 |
| **gkx_demo_python** | 0.1 MB | 极低（5月） | 低 | 无 | ❌ **不搬，archive** | 3 commits，已废弃 |

### 7.2 结论

- **新根采用 polyrepo of code 模式**（保持 10 个独立子仓）
- **不合并任何仓**（合并的工程成本远高于收益）
- **archive 2 个低活跃仓**（`gkx_ui_demo`, `gkx_demo_python`），保留在老根直至 M6
- **Phase 2 可选**：把 `gkx_lumen_fronted_pc` + `gkx_lumen_fronted_mobile` 合为 pnpm workspace（不在 RFC-002 范围）

### 7.3 仓库改名（OPEN-Q1 已决：✅ 做，团队管理者已在本节给出最终名）

老根仓名风格混乱（如 `gkx_demo_ui` vs `gkx_lumen_fronted_pc`、`fronted` 拼写错、缺少业务域语义）。团队管理者评审后，确立**统一命名规约**与 10 个仓的最终新名。

#### 7.3.1 命名规约 `{stage}-{layer}-{domain}[-{variant}]`

| 段 | 取值 | 含义 |
|---|---|---|
| **stage** | `demo` / `lumen` | `demo` = 原型/演示仓（探索与验证阶段）；`lumen` = 工程代码正式仓（稳定交付阶段，对应"光"的 Lumen 命名） |
| **layer** | `ui` / `svc` / `algo` | `ui` = 前端工程；`svc` = 后端服务（Spring Cloud 多模块）；`algo` = 算法（Python 等） |
| **domain** | `science` / `topic` / `platform` / `system-test` / `ent-analysis` | `science` = 科技信息展示系统；`topic` = 科技专题服务系统；`platform` = 跨两系统的基座平台；`system-test` = 系统级实验沙箱；`ent-analysis` = 企业分析专项 |
| **variant** | `pc` / `mobile`（仅前端用） | 前端形态 |

**例外**：`dataease`（开源 DataEase fork，是工具不是项目组件，不套此规约，且**可不迁移**）。

#### 7.3.2 10 个仓的最终改名表

| 老名 | 新名 | stage | layer | domain | variant | 含义 |
|---|---|---|---|---|---|---|
| `demo2` | `demo-ui-science` | demo | ui | science | - | 科技信息展示系统的前端 demo |
| `ent-analysis-demo` | `demo-algo-ent-analysis` | demo | algo | ent-analysis | - | 企业维度算法 demo |
| `gkx_dataease` | `dataease` | (开源 fork，不套规约) | — | — | — | 数据探索工具，**可不迁移** |
| `gkx_demo_ui` | `demo-ui-system-test` | demo | ui | system-test | - | 系统级实验前端（可观测/算法效果等演示） |
| `gkx_lumen_backend` | `lumen-svc-platform` | lumen | svc | platform | - | 工程正式仓-后端 Java 微服务（覆盖科技信息展示+专题服务两系统） |
| `gkx_lumen_fronted_pc` | `lumen-ui-science-pc` | lumen | ui | science | pc | 科技信息展示系统-PC 前端正式仓 |
| `gkx_lumen_fronted_mobile` | `lumen-ui-science-mobile` | lumen | ui | science | mobile | 科技信息展示系统-移动端前端正式仓 |
| `gkx_service_demo` | `demo-svc-platform` | demo | svc | platform | - | demo 环境-后端 Java 微服务（覆盖两系统所有微服务） |
| `innov-algo-demo` | `demo-algo-science` | demo | algo | science | - | 科技信息展示系统的非垂向算法 demo（如创新监测） |
| `topic_demo` | `demo-ui-topic` | demo | ui | topic | - | 科技专题服务的前端 demo |

#### 7.3.3 命名规约的演进锚点

- **未来新增仓**：必须按 `{stage}-{layer}-{domain}[-{variant}]` 命名，不再自由发挥
- **stage 从 demo → lumen 的升迁**：一个 demo 仓成熟到工程正式版时，**新建** `lumen-*` 仓（不重命名 demo-*），让两者并存到 demo 仓 deprecate
- **domain 词典进一步收敛**：建议未来仅允许 `science` / `topic` / `platform` 三个主域 + 若干临时专项域（如 `ent-analysis`）；新增主域需走 ADR
- **dataease 例外**：开源 fork 仓保持原名，体现"非项目组件"语义；如未来再 fork 其他开源工具，沿用该模式

---

## 8. 6 个月路线图（M0-M6）

### 8.1 阶段全景

| 阶段 | 时间窗口 | 周数 | 核心动作 | 决策点 |
|------|------|---|------|------|
| **M0** | 2026-06-19 → 2026-06-26 | 1 周 | 决策周：评审 RFC-002，定 OPEN 问题 | RFC-002 评审通过 |
| **M1** | 2026-06-29 → 2026-07-10 | 2 周 | 脚手架：建 GitLab group + 主仓搭好 + 白名单一次性搬 | lead 能用新根派 1 个 trivial task |
| **M2** | 2026-07-13 → 2026-08-21 | 6 周 | Lead 试运行：1-3 个真实 task 在新根跑通 | 新根承接 ≥ 1 个 epic 端到端 |
| **M3** | 2026-08-24 → 2026-10-02 | 6 周 | 灰度扩展：全员逐步把新 task 派到新根 | 新根新 task 占比 ≥ 50% |
| **M4** | 2026-10-05 → 2026-10-30 | 4 周 | 老根冻结：仅 bugfix，所有新功能必须在新根 | 老根新功能 commit = 0 |
| **M5** | 2026-11-02 → 2026-11-27 | 4 周 | 对账与收尾：二次差量搬运 + in-flight task 收口 | 老根 in-flight task = 0 |
| **M6** | **触发式**（默认窗口 2026-11-30 → 2026-12-04 ± 2 周） | 1 周 | 切换日：老根 read-only / archive | 老根 `chmod -w` + ARCHIVE.md |

**总周期**：约 24 周 / 6 个月（D+168，仅默认值；M6 实际由 §8.3 触发条件决定）

### 8.2 各阶段详细任务

#### M0 决策周（W26）

- [ ] **D1-D2**：本 RFC 评审会
- [ ] **D2**：lead 回答 §13 所有 OPEN 问题
- [ ] **D3**：在 GitLab 创建 `gkx-lumen/` group（仅创建，不放任何仓）
- [ ] **D4**：定 §7.3 仓名改名决议
- [ ] **D5**：定切换日（M6 具体日期）

#### M1 脚手架（W27-W28）

- [ ] 在 GitLab 创建 `gkx-lumen/gkx-orchestration` 主仓
- [ ] 编写 `bootstrap.ps1` / `bootstrap.sh`（一键 clone 主仓 + 子仓）
- [ ] 编写 `sync-all.sh`（一键 pull 全部子仓）
- [ ] 编写 `verify-paths.sh`（grep 检查无硬编码 `E:\` 残留）
- [ ] 把白名单 5.1.A 全搬入主仓 `agent-delivery/`
- [ ] 把白名单 5.1.B 全搬入主仓 `.cursor/rules/`
- [ ] 重写 `paths.yaml` → 引用 `$GKX_ROOT` 环境变量
- [ ] 重写 `README.md` → 新根 onboarding 流程
- [ ] 重写 `team-onboarding.md` → 1 小时上手脚本
- [ ] 把 10 个保留子仓（见 §7）在 GitLab 新 group 重新 clone / 推送
- [ ] **验收**：在干净的机器上跑 `bootstrap.ps1`，60 分钟内跑通

#### M2 Lead 试运行（W29-W34，6 周）

- [ ] coordinator-agent 在新根派 1 个 trivial task（如：写一份文档）
- [ ] coordinator-agent 在新根派 1 个真实算法 task（如：ent-analysis-demo 的某个 formula）
- [ ] coordinator-agent 在新根派 1 个真实前端 task（如：topic_demo 的某个组件）
- [ ] 每周 retro：新根痛点列 + 是否继续 / 调整 / 回退
- [ ] 老根：继续主战场，正常跑（不受影响）
- [ ] **验收**：新根端到端跑通 ≥ 1 个 epic（含 architect / ux / ui / frontend / qa 全流程）

#### M3 灰度扩展（W35-W40，6 周）

- [ ] 全员观看 lead 在新根的 demo
- [ ] coordinator-agent 派单规则更新：**新 epic 一律在新根**
- [ ] 老根仅接 in-flight task 的延续
- [ ] 周度统计：新根新 task 占比
- [ ] **验收**：新根新 task 占比 ≥ 50%

#### M4 老根冻结（W41-W44，4 周）

- [ ] 发布"老根冻结通告"：老根仅允许 bugfix
- [ ] coordinator-agent 派单规则更新：**老根不再派任何新 task**
- [ ] 老根 GitLab 仓库设置 protected branch（限制 push）
- [ ] **验收**：老根新功能 commit = 0（仅 bugfix）

#### M5 对账与收尾（W45-W48，4 周）

- [ ] 用 `rsync --dry-run` 对账老根 / 新根
- [ ] 二次差量搬运：M1 之后老根产生的合理新东西（如 bugfix 文档、补充 handoff）
- [ ] 收尾老根所有 in-flight task
- [ ] **验收**：老根 in-flight task = 0；二次对账 diff = 0 critical

#### M6 切换日（W49，1 周，**触发式**）

- [ ] 发布"切换日通告"
- [ ] 老根所有仓 GitLab 设置为 read-only / archived
- [ ] 老根添加 `ARCHIVE.md`（指引迁移到 gkx-lumen）
- [ ] 老根本地目录 `chmod -w`（防误改）
- [ ] coordinator-agent 派单规则更新：**完全只在新根**
- [ ] **验收**：所有团队成员当天起只工作在新根

### 8.3 M6 触发条件（OPEN-Q3 决议）

团队管理者决议：**M6 切换日不固定 2026-12-04**，改为**触发式启动**。

#### 触发条件（必须全部满足）

| # | 条件 | 验证方式 | 由谁确认 |
|---|------|------|------|
| T1 | **老根所有未 push 内容已全部推送到老 GitLab 备份完成** | 各仓 `git status` = clean + `git log origin/main..HEAD` 为空 | coordinator-agent 自动巡检（每周一）|
| T2 | M5 验收已通过（老根 in-flight task = 0；二次对账 diff = 0 critical） | qa-lead 签字 | qa-lead |
| T3 | 新根 M2 / M3 验收已通过（端到端 epic 可跑 + 50% 新 task 占比） | architect-lead 签字 | architect-lead |
| T4 | 团队管理者明确签发"切换日通告" | 邮件 / 群通告 | 团队管理者 |

#### 触发后流程

```
T1 + T2 + T3 全部满足
    ↓
coordinator-agent 输出《M6 触发就绪报告》
    ↓
团队管理者审阅 + 签发 T4 通告（建议提前 3 个工作日）
    ↓
M6 启动，1 周内完成 §8.2 M6 全部清单
```

#### 默认目标窗口

- **第一档（aggressive）**：2026-09 末（M3 末）— 适用条件：M2 验证非常顺利 + 团队主动加速
- **第二档（recommended）**：2026-12-04 ± 2 周 — 默认建议（6 个月路线图原值）
- **第三档（conservative）**：2027-02 前 — 适用条件：M2 / M3 期间出现 R1 / R2 等中等以上风险事件

→ **路线图 M0-M5 周期不变，仅 M6 日期由触发条件决定**。

---

## 9. 关键节奏与冻结策略

### 9.1 冻结分级（M4 实施）

| 等级 | 时间 | 老根允许什么 | 新根允许什么 |
|------|------|---|---|
| Lv0 | M0-M2 | 一切 | 仅 lead 试运行 |
| Lv1 | M3 | in-flight + bugfix + 必要小新功能 | 50% 新 task |
| **Lv2 冻结** | **M4** | **仅 bugfix** | 全部新 task |
| Lv3 | M5 | 仅 critical bugfix | 全部 |
| Lv4 切换 | M6 起 | 不接受 push（read-only） | 全部 |

### 9.2 双轨期治理

- **每周一**：coordinator-agent 发"双轨周报"，统计新/老根的 task 数、新增 commit 数、阻塞项
- **每月底**：lead 召开"迁移评审"，判断是否进入下一 milestone
- **若 M2 验证失败**：触发 §10 R1 应急方案

---

## 10. 风险与 Mitigation

| ID | 风险 | 概率 | 影响 | Mitigation |
|----|------|---|---|---|
| **R1** | M2 验证失败：新根反而比老根别扭 | 中 | 整个项目延迟 / 回退 | M2 内置 weekly retro；若 4 周无改善，回退 RFC-001 in-place 方案 |
| **R2** | M4 老根冻结失败：业务方塞新需求到老根 | 高 | 切换日搬运量爆炸 | M3 末期发"冻结通告"+ 写入项目章程；coordinator-agent 强制拒派 |
| **R3** | M5 对账漏搬：老根有合理新东西没带过来 | 中 | 新根缺历史决策上下文 | M5 用 `rsync --dry-run` 全量对账 + 人工 review diff |
| **R4** | agent 规则 1:1 复制后水土不服：路径变了引用断 | 高 | M1 卡住 | 白名单内每个 .mdc 用 verify-paths.sh 单独验证；M1 末做"端到端 lint" |
| **R5** | 甲方交付被双轨拖累：M2-M3 期间 lead 分心 | 中 | 项目延期 | M2-M3 严格保护老根产能，新根仅"额外验证"非"主战场" |
| **R6** | GitLab 新 group 权限配置失误 | 中 | 团队成员访问受阻 | M0 D3 创建后立即跑"全员 clone 测试" |
| **R7** | 业务子仓在新 group 重新 clone 时 PR 丢失关联 | 高 | 历史 PR 评审上下文断开 | 老根 GitLab 保留至少 12 个月只读，PR URL 仍可查 |
| **R8** | `企业分析/`、`创新监测-开发承接包/` 等业务承接包迁移决议拖延 | 中 | M1 漏搬资产 | M0 D2 必须定结论（详见 §13 OPEN-Q2） |
| **R9** | 二进制大文件（`.admin-ui.b64`、`2gkxx.sql.b64`）的真实归属未明 | 低 | 后续需要时找不到 | M0 D4 由数据团队 lead 认领 |
| **R10** | `gkx_lumen_backend` 的 `feature/ent-metrics-catalog` 分支无 upstream，迁移时遗漏 | 中 | 6 commits 工作丢失 | M1 单独处理：在新 group 创建 backend 仓时一并 push 该分支 |
| **R11** | OPEN-Q8 决议**不启用 Protected Branch + MR 审批硬规约** —— 误 push / 误 force-push / 团队规模扩大后协作冲突 | 中 | 主分支被污染 / 历史被改写 / 多人 push 冲突 | (a) 启用 GitLab **commit hooks** 拦截 `force push` 与高危正则提交（`secret` / `password` / `*.env`）；(b) coordinator-agent **每周 audit** 各仓 commit 历史，发现异常立即报警；(c) 仓库根部署 **pre-commit hook 模板**（统一 commit-msg 规约 + lint）；(d) 团队规模扩大到 ≥ 30 人或出现 1 次严重事件时**自动重审 OPEN-Q8**，可能升级为启用 MR 审批 |

---

## 11. 与 RFC-001 的关系

### 11.1 RFC-002 supersedes RFC-001

| 维度 | RFC-001（in-place） | RFC-002（greenfield） |
|------|---|---|
| 改造对象 | `E:\gkx_src` 现有 | GitLab 新 group `gkx-lumen/` |
| Git history | 全部保留 | S2 已定不保留 |
| 完成时间 | 4-8 周 | 6 个月 |
| 风险 | 中（要协调全员迁移） | 高（双轨期 6 个月） |
| 最终质量 | 受历史包袱限制 | 可彻底重做 |
| 团队学习成本 | 低 | 中（重新学新布局） |

### 11.2 RFC-001 哪些被继承

- **§5 目标布局**：仍是 `agent-delivery/ + repos/ + worktrees/ + scripts/ + .env` 五段式
- **§6 路径解耦**：仍用 `$GKX_ROOT` 环境变量
- **§7 worktree 工作流**：直接复用
- **§8 跨仓一致性机制**：直接复用
- **§9 onboarding 升级**：bootstrap 脚本设计直接复用

### 11.3 RFC-001 哪些被废弃

- **§4 迁移策略（in-place 路径调整）**：不适用（不在老根改）
- **§4 步骤"move 13 仓到 repos/"**：不需要（在新 group 重新 clone）
- **RFC-001 Status**：评审通过后改为 **Superseded by RFC-002**

### 11.4 文件处置

- 保留 RFC-001 在 `agent-delivery/RFC/RFC-001-git-workspace-redesign.md`
- 在 RFC-001 头部追加 Status 变更：`Superseded by RFC-002（2026-06-19）`

---

## 12. 影响评估

### 12.1 对各团队的影响

| 团队 | M0-M2 影响 | M3-M5 影响 | M6 之后 |
|------|---|---|---|
| **架构师 / lead** | 高（要评审 + 试运行） | 中（要带队迁） | 中（驻新根） |
| **后端 Java** | 低（继续老根工作） | 中（切换主战场） | 低 |
| **前端 React** | 低 | 中 | 低 |
| **算法 Python** | 低 | 中 | 低 |
| **QA** | 低 | 中（双仓回归） | 低 |
| **PM / UE** | 中（要管理双轨节奏） | 高（要协调切换） | 低 |
| **甲方** | 零（M0-M3 完全无感） | 低（M4 起冻结老根新功能） | 零（已切换） |

### 12.2 对编排成熟度的影响

| 阶段 | RFC-001 | RFC-002 |
|------|---|---|
| Phase 1（已达成）| ✅ | ✅ |
| Phase 2 worktree 并行 | M+1 月达成 | M2 末达成 |
| Phase 3 跨仓 agent 协作 | M+3 月 | M3 末达成 |
| Phase 4 全自动派单 + retrospective | M+6 月 | M5 末达成 |

→ RFC-002 在 Phase 演进上**比 RFC-001 早 1-2 月达成**，因为新根直接 worktree-native。

### 12.3 成本估算

| 项 | RFC-001 | RFC-002 |
|---|---|---|
| Lead 投入 | 2-4 人周 | 8-12 人周（分摊 6 个月） |
| 全员学习成本 | 0.5 人天 / 人 | 1-2 人天 / 人 |
| GitLab 资源 | 不变 | 新 group 12 仓 |
| 风险缓冲预算 | 1 周 | 4-6 周 |
| **总成本** | ~30 人天 | ~80-120 人天 |

→ RFC-002 成本约为 RFC-001 的 3-4 倍，但**消除 RFC-001 解决不了的结构性问题**。

---

## 13. 已决议清单（2026-06-19 团队管理者一审通过）

> 原 §13 为"OPEN 待决问题"；评审完成后已全部收口，含决议日期与执行人。

| ID | 问题 | **决议** | 决议人 | 决议日期 | 落地 |
|----|------|---------|------|---------|------|
| **Q1** | 仓库改名（§7.3）做不做？ | ✅ **做** —— 已在 §7.3 给出最终 10 仓新名 + `{stage}-{layer}-{domain}[-{variant}]` 命名规约 | 团队管理者 | 2026-06-19 | §7.3 已写定 |
| **Q2** | `企业分析/`、`创新监测-开发承接包/` 等业务承接包归属？ | ✅ **归入** `agent-delivery/验收文档/`（业务承接包属于编排资产） | 团队管理者 | 2026-06-19 | M1 阶段执行 |
| **Q3** | 切换日 M6 具体哪天？ | ✅ **触发式**（条件 = "老根所有未 push 内容已备份到老 GitLab" + M5 验收通过 + M2/M3 验收通过 + 团队管理者签发） — 详见 **§8.3** | 团队管理者 | 2026-06-19 | §8.3 已写定 |
| **Q4** | `gkx_ui_demo` 和 `gkx_demo_python` 是否真的不搬？ | ✅ **不搬** —— 原始独立 git 保留在老根 archive；新根不引用 | 团队管理者 | 2026-06-19 | M1 不创建对应新仓 |
| **Q4a** | M1/Phase B 执行时**新发现** `gkx1/datascreen` + `gkx1/demo` 两仓（2026-03 以来零活跃）是否迁移？ | ✅ **不迁，全部 archive** —— 经团队管理者快速判断"似乎不是本项目，不迁，但加 archive 公告防误用"；与 Q4 同等处理 | 团队管理者 | 2026-06-19（M1 执行中追加） | M1 Phase B5 已 archive 公告完成；详见 §15 |
| **Q5** | `.admin-ui.b64` 和 `2gkxx.sql.b64` 归属？ | ✅ **搬到新根 `gkx-lumen/gkx-orchestration/` 仓根** —— 暂时与现状一致放在仓根，未来由 data-lead 评估是否归位到 `agent-delivery/data/legacy-dumps/` | 团队管理者 | 2026-06-19 | M1 一并搬运 |
| **Q6** | `gkx_lumen_backend` 的 `feature/ent-metrics-catalog` 分支在新 group 是否合入 main？ | ✅ **不合入**（保持现状直至 owner 决策） | 团队管理者（同意默认推荐） | 2026-06-19 | M1 单独 push 该分支（见 R10） |
| **Q7** | 新根采用什么分支策略？ | ✅ **GitLab Flow**（main + feature/* + release/*）—— 默认推荐被接受 | 团队管理者（同意默认推荐） | 2026-06-19 | M1 在新 group 配置 |
| **Q8** | 是否启用 GitLab Protected Branch + MR 审批硬规约？ | ✅ **不启用** —— 团队规模较小、信任高、敏捷优先；以 commit hooks + 每周 audit 替代（详见 **R11**） | 团队管理者 | 2026-06-19 | M1 配置 commit hooks 模板；R11 mitigation 落地 |
| **Q9** | M2 试运行第一个真实 task 选哪个？ | ✅ **全新小 task**（避免被 in-flight 干扰）—— 默认推荐被接受；具体 task 由 PM + coordinator 在 M2 W29 第一周选定 | 团队管理者（同意默认推荐） | 2026-06-19 | M2 启动前定 |
| **Q10** | RFC-001 是否正式标 Superseded？ | ✅ **立即标** —— 已在 RFC-001 头部完成标记 | 团队管理者 | 2026-06-19 | 已落地（同日） |

### 13.1 待 lead 异步追认的项

以下决议虽已由团队管理者一审通过，但执行细节仍待对应 lead 在 M0-M1 期间确认：

| ID | 待追认 lead | 追认内容 |
|----|---|---|
| Q2 | PM | `验收文档/` 子目录命名 + 业务承接包归位 SOP |
| Q5 | data-lead | 二进制 dump 的最终归位决定（仓根 vs `legacy-dumps/`） |
| Q6 | backend-lead | `feature/ent-metrics-catalog` 分支在 lumen-svc-platform 仓内的演进策略 |
| Q7 | architect-lead | GitLab Flow 细则（如 release/* 触发规则、tag 命名） |
| Q8 | architect-lead + PM | commit hooks 具体策略 + audit 频率 + 升级触发条件（R11） |
| Q9 | PM + coordinator | M2 第一个 task 选型 |

→ M0-M1 期间 PM 收口异步追认；若某 lead 异议，触发"二审"（团队管理者拍板）。

---

## 14. 验收标准（Definition of Done）

### 14.1 M6 切换日验收

- [ ] 老根所有 12 个 GitLab 仓库 **archived 或 read-only**
- [ ] 老根本地目录 `E:\gkx_src` 不再接受任何 push
- [ ] 所有团队成员当天起 100% 工作在新根
- [ ] coordinator-agent 派单规则：100% 派到新根
- [ ] 新根 onboarding 文档完整、被至少 2 名新人验证（≤ 1 小时上手）
- [ ] 新根编排资产 100% 可运行（13 .mdc 全部生效，Design.md 引用全部正确）
- [ ] 老根添加 `ARCHIVE.md` 指引迁移到 gkx-lumen
- [ ] 新根添加 `MIGRATION-FROM-OLD-ROOT.md` 记录迁移历程

### 14.2 验收审计

由 architect-lead + QA-lead + PM 三方签字，输出《gkx-lumen 切换验收报告》。

---

## 15. 决策记录（M0-M6 持续更新）

| 日期 | 决议 ID | 决议内容 | 决策人 |
|---|---|---|---|
| 2026-06-19 | S1 | 老根 6 个月内 deprecate | 团队管理者 |
| 2026-06-19 | S2 | 选择性搬 + 不保 git history | 团队管理者 |
| 2026-06-19 | S3 | 不双写，切换日前一次性搬 | 团队管理者 |
| 2026-06-19 | E1 | GitLab 新 group `gkx-lumen/` | 团队管理者 |
| 2026-06-19 | E2 | 子仓形态：保持 10 个独立 + 2 个 archive（见 §7） | 团队管理者（评审追认草案推荐） |
| 2026-06-19 | E5 | 起草 RFC-002 | 团队管理者 |
| 2026-06-19 | **REVIEW-1** | **RFC-002 一审通过**：评审 §13 全部 10 项 OPEN，决议见 §13；同时追认 RFC-001 全部 7 项设计原则；同步加 §10 R11（OPEN-Q8 不启用 MR 审批的 mitigation）| 团队管理者 |
| 2026-06-19 | Q1 | 仓库改名：做（§7.3 给出 10 仓最终名 + `{stage}-{layer}-{domain}[-{variant}]` 规约） | 团队管理者 |
| 2026-06-19 | Q2 | 业务承接包归入 `agent-delivery/验收文档/` | 团队管理者 |
| 2026-06-19 | Q3 | M6 切换日：触发式（条件见 §8.3） | 团队管理者 |
| 2026-06-19 | Q4 | `gkx_ui_demo` / `gkx_demo_python` 不搬，原 git 保留老根 archive | 团队管理者 |
| 2026-06-19 | Q4a | M1 执行中新发现 `gkx1/datascreen` + `gkx1/demo`（2026-03 以来零活跃，"似乎不是本项目"）不迁移；与 Q4 同等处理，已在 Phase B5 加 archive 公告 | 团队管理者（M1 执行中追加） |
| 2026-06-19 | Q5 | 二进制 dump 搬到新根 `gkx-lumen/gkx-orchestration/` 仓根（暂保现状） | 团队管理者 |
| 2026-06-19 | Q6 | `feature/ent-metrics-catalog` 不合入 main（追认推荐） | 团队管理者 |
| 2026-06-19 | Q7 | 分支策略：GitLab Flow（追认推荐） | 团队管理者 |
| 2026-06-19 | Q8 | **不启用** Protected Branch + MR 审批；以 commit hooks + 每周 audit 替代（R11） | 团队管理者 |
| 2026-06-19 | Q9 | M2 第一个 task：全新小 task（追认推荐，具体由 PM + coordinator 在 M2 W29 选定） | 团队管理者 |
| 2026-06-19 | Q10 | RFC-001 立即标 Superseded（已落地） | 团队管理者 |
| TBD | LEAD-FOLLOWUP | §13.1 待 lead 异步追认项收口 | PM（M0-M1 收口） |

---

## 附录 A：M0 立即可执行清单（评审后已更新）

### A.1 已完成（评审通过当日）

- [x] **本 RFC 一审通过**（团队管理者 2026-06-19）
- [x] **§13 全部 10 项 OPEN 已决议**（见 §13）
- [x] **RFC-001 标 Superseded**（同日落地）
- [x] **§7.3 仓库改名最终表已写定**

### A.2 PM / coordinator 在 M0 周收口（异步追认）

- [ ] PM 把 §13.1 待 lead 异步追认表发给对应 lead，1 周内收口
- [ ] coordinator-agent 把"REVIEW-1"决议同步到 `team-collaboration-playbook.md` 与各 mdc 规则的"参考资料"段
- [ ] 老根 `README.md` 顶部加"我们正在迁往 gkx-lumen，详见 RFC-002"通告（PM 30 分钟）

### A.3 进入 M1 前必须完成（架构师 / DevOps）

- [ ] **创建 `gkx-lumen/` GitLab group**（架构师 1 小时）
- [ ] **盘点 `gkx_lumen_backend` 的 `feature/ent-metrics-catalog` 分支**（backend-lead 0.5 天，输出搬运 SOP）
- [ ] **data-lead 认领 `2gkxx.sql.b64` / `.admin-ui.b64`**（确认是否仍有业务价值；按 Q5 决议默认搬到新根仓根）
- [ ] **owner 确认 `gkx_ui_demo` / `gkx_demo_python` archive**（按 Q4 决议）
- [ ] **lead 评审 §7.3 命名规约**（在新 group 创建仓前最后确认）

### A.4 M1 第一周脚手架交付物

- [ ] `bootstrap.ps1` / `bootstrap.sh` 初版
- [ ] `gkx-lumen/gkx-orchestration` 主仓骨架（含白名单 §5.1 内容）
- [ ] 10 个保留子仓在新 group 完成 import
- [ ] commit hooks 模板（按 Q8 决议 + R11 mitigation）

---

**审批栏**

| 角色 | 姓名 | 签字日期 | 备注 |
|------|------|---|------|
| **团队管理者** | ✅ | **2026-06-19** | 一审通过，10 项 OPEN 决议见 §13；同步追认 RFC-001 设计原则 |
| Architect-lead | _____ | ____-__-__ | 异步追认 Q7 / Q8 细则 |
| Frontend-lead | _____ | ____-__-__ | 异步知会 §7.3 改名 |
| Backend-lead | _____ | ____-__-__ | 异步追认 Q6（`feature/ent-metrics-catalog`）|
| Algo-lead | _____ | ____-__-__ | 异步知会 §7.3 改名 |
| QA-lead | _____ | ____-__-__ | 异步知会 M5 对账职责 |
| PM | _____ | ____-__-__ | 异步追认 Q2 / Q9 + 收口 §13.1 |
| Data-lead | _____ | ____-__-__ | 异步追认 Q5（二进制 dump 归属）|
