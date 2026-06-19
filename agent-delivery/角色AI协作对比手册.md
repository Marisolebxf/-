# 角色 AI 协作对比手册（AI 之前 vs AI 之后）

> **配套文档**：`team-collaboration-playbook.md`（团队公约）/ `.cursor/rules/*.mdc`（角色规约）/ `培训/2026-06-18_团队AI协作宣讲.pptx`（宣讲 PPT）  
> **覆盖角色**：12 个（architect / coordinator / pm / ux / ui / frontend / api / algorithm / data / devops / qa / doc）  
> **版本**：v1.0 / 2026-06-17  
> **用途**：新人 onboarding 第 1 天必读；各 Lead 季度对照；团队复盘和优化输入

---

## 0. 导言

### 0.1 为什么需要这份手册

宣讲讲了"团队整体怎么协作"，但**每个角色到具体每天怎么做，得有一份对照表**。

很多人困惑的不是"AI 能做什么"，而是：

- 我以前的工作流里，AI 应该插在哪几步？
- 哪些事我不能放手给 AI 做？
- 我的产出节奏会变吗？
- 出了问题，谁来兜底？

这份手册按 **12 角色 × 8 维度** 给出对照，让每个人 5 分钟就能找到自己。

### 0.2 怎么用

| 使用者 | 怎么用 |
|--------|--------|
| 新人（入职 D1） | 找到自己角色的章节，5 分钟通读；找到自己 mdc 文件路径，30 分钟跑通"必跑"动作 |
| Team Lead | 季度复盘前对照本手册"明天起该做什么"清单，自查团队节奏是否到位 |
| PM / 架构师 | 跨角色协同有疑问时，对照"跨岗依赖"和"错误检查点"两栏，定位接口问题 |
| 培训讲师 | 配合 PPT 第 13 页（11 角色矩阵）和第 14 页（人 vs AI 边界）做深挖讲解 |

### 0.3 8 个对比维度的统一定义

| 维度 | 定义 | 为什么重要 |
|------|------|----------|
| **需求入口** | 任务从哪儿来、谁派给我、用什么形式（口头/邮件/工单/yaml） | 决定你能不能"找到自己今天该干什么"；AI 时代变化最大 |
| **核心工具** | 每天打开率最高的 3–5 个工具 | 工具链决定你能不能用上 AI；老工具 + 老流程 = AI 用不起来 |
| **产出节奏** | 平均多久交一次东西（小时/天/周） | 节奏过慢 = 阻塞下游；过快 = 质量塌方 |
| **产物存放** | 我的产出放哪儿、能不能被追溯/复用 | 决定团队能不能"接力"；vibe coding 最大塌方点就在这里 |
| **跨岗依赖** | 我要等谁交、谁等我交、接口是什么 | 决定团队协作摩擦力；handoff 模板就是为这一栏存在 |
| **错误检查点** | 我做错了，会在哪一关被发现？谁负责发现？ | 决定 bug 漏到甲方的概率；架构铁律 + 验收门就是为此 |
| **交付周期** | 单个典型任务，从派单到接收，多久 | 决定项目能否按 4 个月闭环；AI 时代提速 5–10 倍是常态 |
| **质量保障设计** | 怎么证明我做对了？人审 + 自动化 + 留证 | 决定能不能扛甲方追溯和验收 |

---

## 1. 总览矩阵（12 角色 × 8 维度 一张大表）

> 一栏读完 8 行，5 分钟看完全团队。每格按 "AI 前 → AI 后" 写。  
> 详细节在 §2–§13，建议先扫这张表再看自己那一节。

### 1.1 设计与编排层（4 角色）

| 维度 | architect 架构师 | coordinator 编排（AI） | pm 项目经理 | ux UX 交互 |
|------|------------------|------------------------|-------------|------------|
| 需求入口 | 凭经验决定何时介入 → Epic 开工 + 里程碑触发评审清单 | 拍脑袋分活 → 读 `task-registry.yaml` 找可派 leaf | 邮件/电话临时接需求 → bid-reference + scope-baseline 真源 | Word 文档下发 → bid-reference 拆 IA |
| 核心工具 | Word + Visio + 头脑 | Excel/JIRA 手动追 → Cursor + task-registry + 编排手册 | 电话 + WeChat + Excel | Figma + Word |
| 产出节奏 | Epic 节点偶发 | 周/天散派 → 每日例行扫一轮，可派立即派 | 周报 + 月报 | 1 周 1 个模块 |
| 产物存放 | 个人电脑、PDF | `architecture-baseline.md`（可机读 + 可评审） | 邮件、文件服务器 → bid-reference + scope-baseline + git | Figma 私有空间 → `demo2/docs/ia/sandbox/` 沙箱 |
| 跨岗依赖 | 被找才出现 | 全员都依赖、但不依赖任何人 | 上游甲方 + 下游全员 | 下游 ui / frontend |
| 错误检查点 | 上线后回看 | 派单时（dependencies / DoD 检查）+ 验收时（7 条 checklist） | 月度复盘 | UE 评审后才发现 |
| 交付周期 | 评审 1–2 天 | 派单 < 5 分钟、收单 < 5 分钟 | 周/月 | 1 周/IA |
| 质量保障 | 主观、靠权威 | DoD + 7 条 checklist + cost 跟踪 + 拒绝合并权 | 客户签字 | UE 主观评审 |

### 1.2 工程实现层（4 角色）

| 维度 | ui UI 工程 | frontend 前端工程 | api Java 后端 | algorithm Python 算法 |
|------|------------|--------------------|---------------|-----------------------|
| 需求入口 | UE 口头 / Figma | 产品 PRD | Word 接口文档 → OpenAPI 契约 + task-registry | Excel 需求 → bid-reference 算法库章节 + algorithm-registry |
| 核心工具 | Sublime + Photoshop → Cursor + ui-agent + Vite HMR | VS Code + Postman → Cursor + frontend-agent + observability.ts | IDEA + Postman + Swagger 手维护 → Cursor + api-agent + OpenAPI 自动导出 | Jupyter + pip → Cursor + algorithm-agent + FastAPI + algorithm-registry |
| 产出节奏 | 静态切图 1–2 天 → 沙箱可演示页 4–8h | 1–2 天/页 | 接口 1 天 / 个 → 单 task 2–4h | 算法 1–2 周 / 个 → 单 task 1–2 天 |
| 产物存放 | UI 切片在网盘 → `demo2/src/sandbox/{topic}-{date}/*` | 直接进主菜单 → lumen 正式仓 + 沙箱可追溯 | 散在各 Service 类 → `gkxlumen-topic` 聚合层 + OpenAPI 契约 | Jupyter notebook → `innov-algo-demo` + `/internal/*` REST + algorithm-registry |
| 跨岗依赖 | 等 UE 给图 | 等 UI 给切片 + 等后端给假数据 | 等前端提需求 + 等算法给接口 | 自由发挥 → 必须配合 data（ADS） + api（Feign） |
| 错误检查点 | 上线被甲方看到 | code review + 用户反馈 | 测试环境联调 | 上线后效果不达标 |
| 交付周期 | 1 页 1–2 天 → 沙箱页 4–8h | 1 页 1–2 天 → 复刻 lumen 半天 | 接口 1 天 → 单接口 2–4h（含 CI 绿） | 算法 1–2 周 → 单 endpoint 1–2 天（含 K8s dev） |
| 质量保障 | UI lead 目测 | 前端 lead code review | 后端 lead + 联调 + 手测 | 上线观察 → algorithm-registry 评估指标 + Tempo trace |

### 1.3 数据 / 工程 / 质量 / 文档层（4 角色）

| 维度 | data 数据 | devops DevOps | qa QA | doc 文档 |
|------|-----------|---------------|-------|----------|
| 需求入口 | 算法 / API 临时要表 | 上线前才被拉群 → 每仓 push 自动触发 + push 即跑 CI | 上线前 1 周才介入 → 与开发并行；CI 每次回归 | 里程碑前临时写 → 与 qa 联动，里程碑日产 docx |
| 核心工具 | Navicat + Excel → Cursor + data-agent + Python ETL + DDL | shell + 手动 kubectl → Cursor + devops-agent + GitLab CI + Helm + OTel | Excel + 手测 → Cursor + qa-agent + Playwright + 三联查（Tempo/Loki/Prom） | Word 手写 → Cursor + doc-agent + officecli MCP |
| 产出节奏 | 接需求才动 | 上线前赶工 → 每次 push 自动 rollout | 测试周集中跑 → CI 每次都跑 + 夜间 e2e | 节点前赶工 → 周报 / 月报 / 里程碑日产 |
| 产物存放 | DDL 散在群 → `数据库设计.md §12` ADS 表 + Mock 脚本 + 映射登记 | 个人手脚本 → `.gitlab-ci.yml` + Helm chart + 自助平台 | Excel 测试用例 → `tests/` + `e2e/` + 验收报告与 bid-reference 章节挂钩 | 各自硬盘 → `验收文档/*.docx`（officecli 产）+ formal-docs-registry |
| 跨岗依赖 | 被动响应所有人 | 被动响应所有人 → CI 模板化让人自助 | 等开发全部完成 | 等 qa 出报告 + 等 PM 给口径 |
| 错误检查点 | 数据用了才发现错 | 上线挂了才发现 → CI 阶段拦截 + dev 环境验证 | 验收时才发现 → CI 拦截 + 三联查定位根因 | 客户回信才发现 → PM 终审 + 术语自检 |
| 交付周期 | 1 表 2–3 天 → 1 表 半天（含 1000+ mock + DQ 规则） | 1 仓上线 3–5 天 → 1 仓 CI 半天 | 1 模块 1 周手测 → CI 全绿 + 一份报告 半天 | 1 份验收报告 2–3 天 → 4–6h（含 PM 终审） |
| 质量保障 | 算法/API 投诉为主 | 上线观察 | 测试覆盖 + 人审 | 主观、靠经验 → 自动套版 + 证据链接 + PM 签字 |

---

## §下方说明

12 角色详细节在 §2–§13；每节包含：

- **一句话定位**
- **8 维度对照表**（AI 前 / AI 后 / 关键变化）
- **明天起，你该做什么**（3 件可立刻执行）
- **必读 / 必跑**（mdc + 文档 + 第一个 trial）
- **注意区分**（来自 mdc "你不做"，特别提醒别越界）

---

## 2. architect 架构师

> **一句话定位**：架构铁律的守门人。Epic 开工评审 + 里程碑合规扫描，**不写业务代码**。  
> **对应 rule**：`.cursor/rules/architect.mdc`

### 2.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | 凭经验决定何时介入；常被业务进度推着走 | Epic 开工 + 里程碑信号自动触发评审清单（coordinator 通知） | "被动救火 → 主动定位 + 自动触发" |
| 核心工具 | Word + Visio + 白板 + 个人头脑 | Cursor + `architecture-baseline.md`（D1–D7 决策） + Tempo / Loki / Prom 三联查 | 评审有 yaml 真源，不靠"我记得我说过" |
| 产出节奏 | 项目启动期高频、中后期消失 | Epic 节点 1 次开工评审 + 1 次里程碑合规扫描 + 季度 baseline 维护 | 节奏可预期、不消失 |
| 产物存放 | 个人电脑 PDF / 散落 PPT | `architecture-baseline.md` + `D1–D7 决策记录`（git 可追溯） | 决策有 RFC 形式、可被新人查阅 |
| 跨岗依赖 | 被找才出现 | 不被任何人依赖，但是所有人（特别是 api/algorithm/data/devops）的"上诉法院" | 不再是"被动找麻烦的人"，是"主动定边界的人" |
| 错误检查点 | 上线后才发现"架构腐化" | 派单时（rule 注入） + 合并前（PR review） + 里程碑（8 条扫描） | 3 层拦截，违反铁律 = 拒绝合并 |
| 交付周期 | 评审 1–2 天 + 邮件来回 1 周 | 1 次评审 1–2h（含 baseline 对照、7 条 checklist 输出） | 5 倍提速 |
| 质量保障 | 主观、靠权威 | 8 条 checklist + Tempo trace 实证 + handoff 联签 | 可量化、可追溯、可挑战 |

### 2.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**：`.cursor/rules/architect.mdc`（5 min），熟悉评审 8 条 checklist。
2. **打开 `architecture-baseline.md`**：确认 D1–D7 七条决策与你的认知一致；不一致就开 PR 改这份文档（不是改你的代码）。
3. **跑一次"模拟评审"**：找一个最近 done 的 task handoff（如 `agent-handoffs/科技人才态势-DS15/UX-DS-15-trial.md`），按 8 条 checklist 跑一遍，**找出至少 1 条可改进项**。

### 2.3 必读 / 必跑

- **必读**：`architecture-baseline.md` / `项目工程化交付模式.md` / `repo-registry.yaml` / `数据库设计.md` / `graph-engine.md` / `observability.md` / `cicd-pipeline.md`
- **必跑**：在 Cursor 开新对话，输入 `/goal architect 对 E-INNOV-M1 做一次架构 baseline 一致性扫描`，看 AI 怎么按 mdc 给出 8 条 checklist。

### 2.4 注意区分

- ❌ **不写业务代码**（轻量角色，写代码就忙不过来评审）
- ❌ **不直接派单**（那是 coordinator 的事；你只在评审里写"建议改派给 xxx"）
- ❌ **不对接甲方**（那是 PM / UE 的事；你只对内部对接技术决策）

---

## 3. coordinator 编排（AI 执行臂）

> **一句话定位**：PM 团队的 AI 执行臂。读 task-registry 找可派 leaf，派单、收 handoff、更状态、**不写代码**。  
> **对应 rule**：`.cursor/rules/coordinator.mdc`  
> **特别说明**：这是一个 **AI 角色**，由 PM 监管使用。

### 3.1 AI 前 vs AI 后

| 维度 | AI 之前（没有 coordinator） | AI 之后 | 关键变化 |
|------|------------------------------|---------|----------|
| 需求入口 | PM 拍脑袋分活 + 群里 @人 | 读 `task-registry.yaml`，找 `status=pending` + `dependencies` 全 done 的 leaf | 分活有真源、不漏不重 |
| 核心工具 | Excel / JIRA / 群消息 | `task-registry.yaml` + `编排手册.md§9` 派单话术 + 12 份 mdc | 派单话术标准化、复制粘贴改 3 参数 |
| 产出节奏 | 周散派 + 临时拉人 | 每日扫一轮，可派立即派；并发本地 ≤4 | 真正"流水线"：永不阻塞 |
| 产物存放 | 散在群、Excel、JIRA | `task-registry.yaml` 状态字段 + `agent-handoffs/*.md` 证据 | 全在 git，任何人 clone 就能看 |
| 跨岗依赖 | 上游靠 PM 给单、下游靠人接 | 上游 PM 维护 scope，下游所有 agent 都从这里接活 | 单点编排、多 agent 并行 |
| 错误检查点 | PM 月度复盘才发现"哎呀谁谁没做" | 派单时（DoD 检查） + 收单时（7 条 checklist，含 cost） | 自动质量门、不放水 |
| 交付周期 | 派单 半天（写邮件、约人开会） | 派单 < 5 分钟（话术 + Cursor 新会话） | 60 倍提速 |
| 质量保障 | 靠 PM 个人记忆 | DoD + 7 条 handoff checklist + cost 跟踪 + 拒绝合并权 | 可量化、可挑战、可重放 |

### 3.2 PM 起手如何用 coordinator（操作 SOP）

1. 在 Cursor 中打开 `E:\gkx_src`，新建一个 agent 会话。
2. 输入：`/goal coordinator 扫描 task-registry 找出今日可派 task 并按编排手册派单`
3. coordinator 会列出可派 task 清单 + 推荐 agent + 估算成本 → PM 拍板挑 1–4 个。
4. 对每个挑中的 task，再开 1 个新会话用对应专项 agent 执行（保持上下文隔离）。

### 3.3 明天起，你该做什么（3 件，针对 PM/Tech-PM）

1. **读 `COORDINATOR-START.md` + mdc**（5 min）：理解 coordinator 怎么工作。
2. **完成第一次自助派单**：在 Cursor 跑一次 `/goal coordinator ...`，把 1 个真实 task 派出去，记录耗时和成本。
3. **建立每日扫单习惯**：每天 10:00 跨团队同步会前 15 min，由你（PM）让 coordinator 扫一次，提前生成今日派单候选。

### 3.4 注意区分

- ❌ **不写代码**（写代码就转 specialist agent）
- ❌ **不擅自扩范围**（超 ±10% 必 PM 签字）
- ❌ **不对接甲方**（那是 PM 的事）
- ❌ **不评审架构**（那是 architect 的事；coordinator 只查"有没有按模板交"）

---

## 4. pm 项目经理（人主导）

> **一句话定位**：客户对接 + 范围守门 + 跨团队协调；AI 是助手不是替身。  
> **对应 rule**：`.cursor/rules/pm.mdc`  
> **特别说明**：**人是主体**，AI 在你起草文档 / 推 agent 时生效；重大决策永远是人。

### 4.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | 邮件 / 电话 / 微信 / 临时拉群，散落 | 仍是邮件 / 电话，但**当天**进 `bid-reference` 或 `scope-baseline.yaml`（增量）；coordinator 接管派单 | 客户语言落地为可机读真源 |
| 核心工具 | Excel + Outlook + WeChat + Word | + Cursor + `team-collaboration-playbook.md` + `scope-baseline.yaml` + `budget-estimate.md` | 决策有公约 / 范围 / 成本三件真源 |
| 产出节奏 | 周报 + 月报 + 节点汇报；常通宵赶 | 周报 / 月报由 doc-agent 起草、你终审；月度成本回顾 30 min | "产出节奏" 不变，"产出工作量" 降 60% |
| 产物存放 | 邮件、文件服务器、各种网盘 | bid-reference + scope-baseline + git 仓；对外发的版本号 + 双签留底 | 任何材料 3 个月后可回放 |
| 跨岗依赖 | 上游甲方 + 下游全员；自己是"中转站" | 仍然如此，但跨团队仲裁可用 `architect-agent` 协助 | 不再"事事亲为"，事事可委派、决策不可委派 |
| 错误检查点 | 月度复盘才发现"漏需求 / 超范围" | scope-baseline ±10% 实时告警；周五成本回顾发现超预算 | 月度漏 → 周级即查 |
| 交付周期 | 周/月节奏 | 不变 | — |
| 质量保障 | 客户签字 + 个人记忆 | 客户签字 + git diff + 双签留底 + AI 起草 / 人终审 | 可追溯 30 倍 |

### 4.2 AI 能帮你做什么（清单）

| 类型 | 能 / 不能 |
|------|---------|
| 起草需求澄清文档 | ✅ |
| 汇总 task-registry 状态 → 周报草稿 | ✅ |
| 扫描 scope-baseline 偏差 + 告警 | ✅ |
| 生成跨团队接口对照表 | ✅ |
| 起草甲方汇报材料**初稿** | ✅（你终审） |
| **擅自承诺范围 / 工期 / 验收** | ❌ |
| **直接发邮件给甲方** | ❌ |
| **决定商务条款** | ❌ |
| **解雇 / 招聘** | ❌ |

### 4.3 明天起，你该做什么（3 件）

1. **读自己的 mdc + playbook**（10 min）：`.cursor/rules/pm.mdc` + `team-collaboration-playbook.md`。
2. **跑一次周报**：让 `coordinator-agent` 扫 task-registry 起草周报 md → 你 5 min 终审 → doc-agent 转 docx → 你签字发。整个流程 30 min（旧流程半天）。
3. **建立周五 30 min 成本回顾**：和 `coordinator-agent` 一起读 `task-registry.yaml` 的 `actual_cost` 字段；超阈值的任务复盘。

### 4.4 周节奏（人的工作日历）

- **周一 9:30–10:30**：与架构师 + 各 lead 1 小时（架构对齐）
- **每日 10:00–10:15**：跨团队 lead 同步（15 min）+ AI 站会
- **周五 14:00–14:30**：成本回顾（含 budget warn 复盘）
- **周五 16:00–17:00**：给甲方发周报（doc-agent 起草 + 你审 + 你发）
- **隔周五 15:00–17:00**：客户演示（与 UI/UE 联合）

### 4.5 注意区分（红线）

- ⚠️ 任何范围变更 > ±10% → **必须客户签字**
- ⚠️ 任何架构铁律破例 → **架构师 + PM 双签**
- ⚠️ 任何 AI 输出对外发布 → **人评审 + 签字**

---

## 5. ux UX 交互

> **一句话定位**：把 bid-reference 功能点翻译成 IA / 用户旅程 / 低保真线框；**不写视觉代码**。  
> **对应 rule**：`.cursor/rules/ux.mdc`  
> **必读补充（D8）**：`Design.md` §1 设计定位、§3 页面骨架（§3.1 六骨架 + §3.2 三段工作区）、§7 通用组件 + §8 地图分析工作区（wireframe 区块命名必须复用 Figma 风格 class：`app-shell` / `app-frame` / `app-header` / `app-sidebar` / `content-shell` / `workspace-grid` / `layer-panel` / `map-stage` / `analysis-panel` / `filter-row`）；旧 v1.1 抽象组件命名（PageShell / GlobalWorkbenchTabs / AnalysisPanelTabs 等）已废止

### 5.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | PM 给 Word + 口头描述 | 自己读 `bid-reference/*.md`（真源），用 ux-agent 拆 IA | 不再"信息二手"，回到真源 |
| 核心工具 | Figma + Axure + Word | Cursor + `ux-agent` + Mermaid + ASCII wireframe + `demo2` 沙箱目录 | 沙箱可 git 追溯；wireframe 可机读 |
| 产出节奏 | 1 周 1 个模块（5 页 IA + 用户旅程 + 中保真） | 1 个 DS 模块 1 小时（IA + userflow + wireframe + README 共 4 份 md） | 40 倍提速 |
| 产物存放 | Figma 私有空间 + 自己电脑 PDF | `demo2/docs/ia/sandbox/{topic}-{date}/*.md`（git 追溯 + ui-agent 直接读） | 可接力、可回退（删目录即回退） |
| 跨岗依赖 | 上游 PM 给需求；下游 UI 等切图 | 上游 bid-reference 真源；下游 `ui-agent` 直接读 md 实现 | 设计 → 实现 中间没有"翻译损耗" |
| 错误检查点 | UE 评审才发现"想错了" | 自检 6 条（覆盖 / 路由 / 异常 / 埋点 / 开放项 / 隔离）；UE 评审第二关 | 2 关拦截，自检发现 70% 问题 |
| 交付周期 | 1 个模块 3–5 天 | 1 个模块 4–8h（含自检 + UE 评审等待） | 5–10 倍提速 |
| 质量保障 | UE 主观评审 + 客户反馈 | 自检 6 条 + UE 评审 + 与 bid-reference 章节号对照 | 可追溯到原始功能点 |

### 5.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**（5 min）：`.cursor/rules/ux.mdc`，记住"只写 `docs/ia/sandbox/` 子目录"。
2. **跑通试点**：参考 `agent-handoffs/科技人才态势-DS15/UX-DS-15-trial.md`（已跑过的样板），自己再拆一个 DS 模块（如 DS-16），1 小时内出 IA + userflow + wireframe。
3. **与 UI 工程对接**：把你的产物指向 ui-agent，让对方 4–8h 内出原型页。

### 5.3 必读 / 必跑

- **必读**：mdc + `bid-reference/科技信息展示系统和科技专题服务系统.md` + `repo-registry.yaml#demo2_proto`
- **必跑**：在 Cursor 中开新会话 `/goal ux 拆 DS-XX 模块为 IA + userflow + wireframe`，对照 mdc 自检 6 条。

### 5.4 注意区分

- ❌ **不写代码**（`.tsx` / `.jsx` / `.css` / `.json` 都不写）
- ❌ **不动 `src/`、`App.jsx`、`pageRouting.js`**（那是 ui-agent 的事）
- ❌ **不直接对甲方汇报**（产物经 UE 评审后才能展示）
- ❌ **不写视觉细节**（颜色、字号、间距是 UI 的事）

---

## 6. ui UI 工程（带设计感）

> **一句话定位**：把 ux-agent 的 IA / wireframe 翻译为 React 沙箱页，可浏览、可演示、可汇报。  
> **对应 rule**：`.cursor/rules/ui.mdc`  
> **沙箱仓**：`demo2`  
> **栈决策（D8 / 2026-06-17）**：  
> - **新页面**：React + Vite + **Arco Design** + ECharts + AntV G6 + Leaflet + dayjs  
> - **demo2 已有页面**：Ant Design v5（历史代码兼容保留）；**同页面禁止 Arco / AntD 混搭**  
> **必读补充（D8）**：`Design.md`（**首要必读**，权威 UI 规范，Figma 风格稿落地版）；§0 给 AI 的执行指令（强制 Arco React + 主色 `#165DFF`）/ §3 页面骨架 / §4 色彩（§4.3 业务要素 10 类固定映射）/ §7 通用组件 / §13 推荐实现映射 / §14 验收 14 条（8 检查 + 6 验收）

### 6.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | UE 口头 + Figma 切图 | 直接读 `docs/ia/sandbox/{topic}-{date}/*.md` 的 ux 产物 | 不靠口口相传 |
| 核心工具 | Sublime + Photoshop + Sketch + 手撸代码 | Cursor + `ui-agent` + Vite HMR + Ant Design v5 文档 MCP | AI 直接出页面 + 实时预览 |
| 产出节奏 | 静态切图 1–2 天 / 页 → 1 周 1 模块 | 沙箱可演示页 4–8h / 模块 | 10 倍提速 |
| 产物存放 | UI 切片 + 网盘 + 个人电脑 | `demo2/src/sandbox/{topic}-{date}/*` + `src/mocks/sandbox/{topic}-{date}/*` | 全在 git 沙箱、可回退 |
| 跨岗依赖 | 等 UE 给图 → 等前端来对接 | 上游 ux 直接给 md；下游 frontend 复刻到 lumen | 端到端可追溯，不靠对接会 |
| 错误检查点 | code review 时发现 | 自检 7 条（路由 / 覆盖 / 主菜单不动 / Mock 真实 / 响应式 / 埋点 / npm run dev） | 自检拦截 80% 问题 |
| 交付周期 | 1 页 1–2 天 | 1 页 1–2h；1 个 DS 模块 4–8h | 10 倍提速 |
| 质量保障 | UI lead 目测 → 等甲方看 | 7 条自检 + UE 评审 + 截图基线（与 qa 视觉回归对接） | 可量化、可挑战 |

### 6.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**（5 min）：`.cursor/rules/ui.mdc`，记住"允许写"和"禁止写"的清单。
2. **跑一次实操**：参考 `agent-handoffs/科技人才态势-DS15/UI-DS-15-trial-dispatch.md`，让 ui-agent 把 DS-15 的 ux 产物实现为沙箱页，全程不超 8h。
3. **验收清单 7 条全过 → commit（不 push）→ UE 评审 → 评审过才 push**。

### 6.3 必读 / 必跑

- **必读**：mdc + `demo2/package.json`（确认依赖版本）+ `demo2/src/App.jsx`（理解路由结构）+ `docs/ia/sandbox/{topic}-{date}/*.md`（上游产物）
- **必跑**：跑通一个 sandbox 页 → 在 `/sandbox/{topic}-{date}/*` 浏览 → 截图给 UE 评审

### 6.4 注意区分

- ❌ **不改 lumen 仓**（任何 `gkx_lumen_*`）
- ❌ **不接 lumen 真实 API**（只用 `src/mocks/sandbox/`）
- ❌ **不硬编码颜色 / 间距 / 字号**（用 design tokens）
- ❌ **不擅自加新组件库**（优先复用 `src/components/`）
- ❌ **不 git push**（仅 commit；push 由人触发）

---

## 7. frontend 前端工程

> **一句话定位**：把 demo2 沙箱页复刻到 lumen 正式仓，接真实 Java API，加可观测性，进主菜单。  
> **对应 rule**：`.cursor/rules/frontend.mdc`  
> **工作仓**：`gkx_lumen_fronted_display` / `gkx_lumen_fronted_topic` / `gkx_lumen_fronted_mobile`  
> **栈决策（D8 / 2026-06-17）**：新页面 Arco；lumen 已有 AntD 代码兼容保留；token 必须从规范 §7 导入，不允许硬编码；handoff 必带规范 §18 18 条对照  
> **必读补充（D8）**：`Design.md`（视觉与 demo2 沙箱页 1:1，token / 配色 / 组件清单完全对齐规范，不允许在 lumen 重新发明组件库；lumen 主题文件用 Arco token 覆盖如 `primary-6: #165DFF`，禁出现 `colorPrimary` 风格 AntD token）

### 7.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | 产品 PRD + UI 切图 + Postman 假数据 | `demo2/src/sandbox/*` 沙箱页（已 UE+甲方评审过）+ Java BFF OpenAPI 契约 | 不再"猜接口"，契约先行 |
| 核心工具 | VS Code + Postman + 个人本地起 mock | Cursor + `frontend-agent` + `observability.ts` 模板 + lumen CI | AI 直接复刻 + traceId 自动注入 |
| 产出节奏 | 1 页 1–2 天 | 复刻 + 接真 API + 加 OTel + 单测 共 4–8h | 4 倍提速 |
| 产物存放 | 散在各 page 文件 | `gkx_lumen_fronted_*` 主菜单 + 与 sandbox 一一对应注释 | 复刻关系可查 |
| 跨岗依赖 | 等切图 + 等后端接口 | 上游 ui（沙箱） + api（OpenAPI 契约）；下游 qa（e2e） | 接口契约 + 沙箱视觉 = 不撕逼 |
| 错误检查点 | code review + 用户反馈 | CI 5 检（lint + type + test + build + dev rollout）+ qa 三联查 | 5 关 + traceId 兜底 |
| 交付周期 | 1 页 1–2 天 | 1 页复刻 4–8h（含 CI 绿 + dev URL 可访问） | 4 倍提速 |
| 质量保障 | 前端 lead code review + 上线观察 | 7 条自检（视觉 / API 切换 / OTel / 单元+e2e / CI / dev URL / 章节对照） | 可量化、可追溯 |

### 7.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**（5 min）：`.cursor/rules/frontend.mdc`，记住 6 条铁律（特别是"只调 Java REST，禁直调 Python"）。
2. **跑一次复刻**：让 frontend-agent 把已评审过的 `demo2/src/sandbox/talent-2026-06-17/*` 复刻到 `gkx_lumen_fronted_topic/src/pages/talent/*`，目标 4–8h 内 CI 绿。
3. **验证 traceId**：复刻完成后，在 dev 环境点一次页面，去 Tempo 看是否能查到对应 trace（如果不能，加 `observability.ts`）。

### 7.3 必读 / 必跑

- **必读**：mdc + `architecture-baseline.md`（方案 A）+ `observability.md` + `cicd-pipeline.md` + 对应 demo2 沙箱页 + `gkxlumen-display` 的 OpenAPI yaml
- **必跑**：本地 `npm run dev` 起 + 调一个真 Java 接口 + 看 Tempo trace

### 7.4 注意区分

- ❌ **不直接调 Python `/internal/*`**（违反铁律 1，必经 Java BFF）
- ❌ **不复用 demo2 sandbox 路由**（必须重新映射到主菜单）
- ❌ **不在前端做业务逻辑**（评分计算、排序权重 → 后端 service）

---

## 8. api Java 后端

> **一句话定位**：写 controller / service / Feign，**只调 Python**不内嵌算法；OpenAPI 契约先行；只读 ADS。  
> **对应 rule**：`.cursor/rules/api.mdc`  
> **工作仓**：`gkx_lumen_backend` / `gkxlumen-topic` / `gkxlumen-display` / `gkxlumen-metrics`

### 8.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | 产品/前端口头 + Word 接口文档 | OpenAPI 契约（先写后实现）+ `task-registry.yaml` 派单 | 不再"接口边写边变"，契约先行 |
| 核心工具 | IDEA + Postman + Swagger 手维护 | Cursor + `api-agent` + OpenAPI 自动导出 + Java Agent OTel | 契约从 yaml 自动生成、不漂移 |
| 产出节奏 | 1 接口 1 天 + 改 bug 半天 | 1 接口 2–4h（含 CI 绿 + dev rollout） | 3–5 倍提速 |
| 产物存放 | 散在各 Service 类、命名不一 | 聚合到 `gkxlumen-topic`（共享聚合核心）+ `gkxlumen-display`（轻 BFF） | 服务边界清晰、可复用 |
| 跨岗依赖 | 等前端提需求 + 等算法给接口 | 上游 data（ADS） + algorithm（`/internal/*`）；下游 frontend（OpenAPI） | 4 边契约，不靠群聊对接 |
| 错误检查点 | 测试环境联调发现 | CI 7 检（unit/integration/ARQ/OpenAPI/OTel/dev rollout/章节对照）+ qa 三联查 | 7 关 + traceId 兜底 |
| 交付周期 | 1 接口 1 天 → 联调改 1 天 | 1 接口 2–4h | 3–5 倍提速 |
| 质量保障 | 后端 lead code review + 联调 | service 单测覆盖 ≥ 80% + Feign 降级 + traceId 全链路 + 章节对照 | 可量化、可挑战 |

### 8.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**（5 min）：`.cursor/rules/api.mdc`，记住 7 条铁律（特别是"算法只能调 Python"和"只读 ADS"）。
2. **跑一次 controller**：让 api-agent 实现一个简单接口（如 `GET /api/talent/{id}/profile`），要求 OpenAPI 契约 + service 单测 ≥ 80% + CI 绿。
3. **看一次 Tempo trace**：调一次接口，去 Tempo 找对应 trace，确认 Java Agent OTel 已注入。

### 8.3 必读 / 必跑

- **必读**：mdc + `architecture-baseline.md`（方案 A §5）+ `数据库设计.md`（ADS 表）+ `observability.md` + `bid-reference/*.md`
- **必跑**：在新会话 `/goal api 实现 GET /api/xxx，要求 OpenAPI 契约 + 单测 + Feign 调 algorithm-svc + OTel`，跑通 CI 绿 + dev URL Swagger 可访问

### 8.4 注意区分

- ❌ **不写 Python / NLP / 模型推理代码**（违反铁律 1）
- ❌ **不直连业务库**（只读 ADS；违反"数据策略 D6"）
- ❌ **不直连 Nebula nGQL**（通过 graph-service）
- ❌ **不在 controller 写业务逻辑**（service 层）
- ❌ **不擅自破事务边界**（动事务必带 architect-agent 评审）

---

## 9. algorithm Python 算法

> **一句话定位**：在 Python 仓做模型工程化 + ETL；通过 `/internal/*` REST 给 Java 调；模型 + 评估指标 + 注册三件套。  
> **对应 rule**：`.cursor/rules/algorithm.mdc`  
> **工作仓**：`innov-algo-demo` / `ent-analysis-demo` / `gkx_lumen_algo_*`

### 9.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | Excel 需求 + 个人理解 | `bid-reference/科技专题服务算法库.md`（业务真源）+ `algorithm-registry.yaml`（算法清单） | 不再"凭经验定算法"，有真源 |
| 核心工具 | Jupyter notebook + pip + 个人脚本 | Cursor + `algorithm-agent` + FastAPI + Pydantic v2 + algorithm-registry + Python OTel instrument | notebook → 服务化、可观测 |
| 产出节奏 | 1 个算法 1–2 周（含调参） | 单 endpoint 1–2 天（含 K8s dev + 评估指标） | 5 倍提速 |
| 产物存放 | notebook + 自己电脑模型文件 | `innov-algo-demo` / `ent-analysis-demo` + `/internal/*` REST + algorithm-registry + 评估报告 | 可被 api 直接 Feign 调用 |
| 跨岗依赖 | 自由发挥、临时找数据 | 上游 data（ADS 标准表 schema）；下游 api（Feign 调） | 数据/接口双契约 |
| 错误检查点 | 上线后效果不达标才发现 | algorithm-registry 评估指标基线 + qa 三联查 + 单测 ≥ 70% | 多关拦截 |
| 交付周期 | 1 算法 1–2 周 | 1 endpoint 1–2 天 | 5–10 倍提速 |
| 质量保障 | 上线观察 + 凭感觉 | 评估指标（precision/recall/F1/AUC...） + 与基线对比 + Tempo trace + 模型版本化（model + data + metric 三件套） | 可量化 / 可回滚 / 可审计 |

### 9.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**（5 min）：`.cursor/rules/algorithm.mdc`，记住 7 条铁律（特别是"不向 Java 暴露模型细节，只暴露 REST"和"算法内不做业务规则"）。
2. **把一个 notebook 服务化**：让 algorithm-agent 把你某个 Jupyter notebook 拆为 `/internal/{name}` 接口 + 评估脚本 + OTel instrument，目标 1–2 天上 K8s dev。
3. **更新 algorithm-registry**：在 `algorithm-registry.yaml` 注册你的新算法（名字、版本、ADS 读写表、评估指标基线）。

### 9.3 必读 / 必跑

- **必读**：mdc + `architecture-baseline.md`（方案 A）+ `bid-reference/科技专题服务算法库.md` + `数据库设计.md`（ADS schema） + `graph-engine.md` + `observability.md`
- **必跑**：本地 `uvicorn` 起一个 `/internal/test` → 用 curl 调 → 看 Tempo trace

### 9.4 注意区分

- ❌ **不在 Python 内写 Java 业务**（如订单流转）
- ❌ **不直连前端**（前端只调 Java）
- ❌ **不擅自改 ADS schema**（必须 data-agent + architect 评审）
- ❌ **不硬编码模型路径**（用配置中心 / 环境变量）
- ❌ **不在算法内做业务规则**（评分加权、过滤条件 → 在 Java 后端或配置中心）

---

## 10. data 数据工程

> **一句话定位**：维护 ADS 标准表 + Python ETL + Mock 数据 + 三方源映射 + DQ 规则；图谱 schema 与关系表对齐。  
> **对应 rule**：`.cursor/rules/data.mdc`

### 10.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | 算法 / API 临时群里要表 | `bid-reference` 业务字段口径 + 算法/API task 中"必读 ADS"指针 | 被动响应 → 主动定义标准 |
| 核心工具 | Navicat + Excel + 手写 DDL | Cursor + `data-agent` + Python ETL + Faker + 维度建模（Kimball） + SQLAlchemy | 全套 ETL 一键生成 |
| 产出节奏 | 接需求才动；急需 3 天 | 1 表 半天（含 DDL + 1000+ mock + DQ 规则 + 映射登记） | 5 倍提速 |
| 产物存放 | DDL 散在群、个人电脑 | `数据库设计.md §12 ADS 层` + DDL 文件 + Python mock 脚本 + `data-source-mapping-registry.yaml` | 全在 git、可回溯 |
| 跨岗依赖 | 被动响应所有人 | 上游 bid-reference + 三方源（数据工厂）；下游 algorithm（ETL 写） + api（只读） | "数据契约"标准化，不再"群里催" |
| 错误检查点 | 数据用了才发现错（脏数据 / 缺字段） | DDL 校验 + DQ 规则（唯一/非空/值域/参照） 进 CI + schema 变更三方评审 | CI 拦截 + 评审拦截 |
| 交付周期 | 1 表 2–3 天 | 1 表 半天 | 4–6 倍提速 |
| 质量保障 | 算法 / API 投诉为主 | DQ 规则 + 字段分布合理（非全 null） + 图谱 schema 对齐 + 三方源映射全覆盖 | 可挑战、可回滚 |

### 10.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**（5 min）：`.cursor/rules/data.mdc`，记住 7 条铁律（特别是"ADS 先行、Mock ≥ 1000 条 / 表、Schema 变更需三方评审"）。
2. **跑一次 mock 数据**：让 data-agent 给 ADS 某个表（如 `ads_talent_profile`）写 Python mock 脚本，目标 1000 条，字段分布合理（不是全 null）。
3. **更新映射登记**：当你接到一个三方源（哪怕只是文档），立刻在 `data-source-mapping-registry.yaml` 登记字段映射初稿。

### 10.3 必读 / 必跑

- **必读**：mdc + `数据库设计.md`（产出真源） + `architecture-baseline.md`（D6 数据策略） + `data-source-mapping-registry.yaml` + `graph-engine.md` + `bid-reference/*.md`
- **必跑**：本地 Python 跑一次 mock 脚本 → 看 DDL 是否能直接 `mysql -e` 执行 → 看数据分布是否合理

### 10.4 注意区分

- ❌ **不写算法**（那是 algorithm-agent）
- ❌ **不写业务 API**（那是 api-agent）
- ❌ **不直接对接三方源业务侧**（你只接落地后的数据；业务侧由集成 / 算法负责）
- ❌ **敏感字段不脱敏不交付**（按合规要求）

---

## 11. devops DevOps / SRE

> **一句话定位**：CI 模板化 + Helm 标准化 + OTel 注入 + 自助平台，让其他团队不必懂 K8s 也能部署。  
> **对应 rule**：`.cursor/rules/devops.mdc`

### 11.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | 上线前才被拉群、人肉 ssh | 每仓 push 自动触发 + 自助平台（`make deploy-dev`）；故障告警自动推 | 被动救火 → 平台自助 |
| 核心工具 | shell + 手动 kubectl + 手写 helm | Cursor + `devops-agent` + GitLab CI 模板 + Helm chart + OTel Collector + Argo | 全套模板化、可复用 |
| 产出节奏 | 上线前赶工通宵 | 每次 push 自动 rollout（< 15 min） | 永不"等上线" |
| 产物存放 | 个人手脚本 + ssh 文档 | `.gitlab-ci.yml` + `helm/` 目录 + `.cursor/rules/devops.mdc` 模板 + 自助平台脚本 | 全在 git、可被新人复用 |
| 跨岗依赖 | 所有人都来找你 | 模板让人自助；只在新仓 / 大改时介入 | 从"瓶颈"变"平台" |
| 错误检查点 | 上线挂了才发现 | CI 7 阶段拦截（命名 / 复现 / 层数 / lint / OTel / dev URL / git-secrets） | 7 关 + dev 环境验证 |
| 交付周期 | 1 仓上线 3–5 天 | 1 仓 CI + Helm + OTel 共 半天 | 6–10 倍提速 |
| 质量保障 | 上线观察 + 凭经验 | helm lint + 镜像层数 ≤ 15 + OTel 验证（Tempo 截图）+ git-secrets 扫描 + 回滚预案 | 可量化、可挑战 |

### 11.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**（5 min）：`.cursor/rules/devops.mdc`，记住 7 条铁律（特别是"禁用 latest、secret 不入 git、保留前 3 版回滚"）。
2. **给一个仓套模板**：让 devops-agent 给 `gkxlumen-topic` 套一份标准 `.gitlab-ci.yml` + Helm chart + OTel Java Agent 注入，目标半天内一次 push → dev URL 可访问。
3. **写自助平台 README**：让其他角色 5 分钟内学会 `make deploy-dev`，不必懂 K8s。

### 11.3 必读 / 必跑

- **必读**：mdc + `cicd-pipeline.md`（产出真源） + `observability.md` + `architecture-baseline.md`（部署架构） + `repo-registry.yaml`
- **必跑**：本地 `helm lint helm/{service}` → 模拟一次 push → 看 GitLab Pipeline 通过 → 看 Tempo trace

### 11.4 注意区分

- ❌ **不动业务代码**（除非加 OTel 注入这种全局改动）
- ❌ **不直接在生产改东西**（生产部署必须人审 + 多签）
- ❌ **不擅自删 K8s 资源**（删除前列清单 + 人审）

---

## 12. qa QA / 测试

> **一句话定位**：按 bid-reference 章节写测试用例 + 自动回归 + 三联查（Tempo / Loki / Prom）+ 出验收报告 docx。  
> **对应 rule**：`.cursor/rules/qa.mdc`

### 12.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | 上线前 1 周才介入；接 Word 测试用例 | 与开发并行；测试用例命名直挂 bid-reference 章节号（`DS-15.1.2_xxx_test`） | 测试与开发同步推进 |
| 核心工具 | Excel + 手测 + 个别 selenium | Cursor + `qa-agent` + Playwright/Cypress + Jest/Vitest/pytest + Pact 契约测试 + Tempo/Loki/Prom 三联查 | 全栈自动化 + 可观测 |
| 产出节奏 | 测试周集中跑 | CI 每次都跑（PR 合并门） + 夜间 e2e 套件 + 里程碑出 docx | "持续验收"而非"突击验收" |
| 产物存放 | Excel 测试用例 + 邮件报告 | `tests/` + `e2e/` + `验收文档/*.docx`（与 bid-reference 章节挂钩） | 可追溯 / 可复跑 / 可挑战 |
| 跨岗依赖 | 等开发全部完成才开始 | 上游各开发 task 完成；下游 doc-agent 出 docx + PM 终审 | 不再"上线前一周才忙" |
| 错误检查点 | 验收时才发现 → 漏到甲方 | CI 拦截 + 三联查根因（traceId 串 Tempo→Loki→Prom）+ 视觉回归 + 性能基线 | 多关拦截 + 自动定位 |
| 交付周期 | 1 模块 1 周手测 | CI 全绿 + 一份报告 半天 | 10 倍提速 |
| 质量保障 | 测试覆盖 + 人审 | 覆盖 ≥ 90% bid-reference 章节 + 三层（unit/integration/e2e）+ P95 < 500ms + 视觉回归基线 | 可量化、可挑战 |

### 12.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**（5 min）：`.cursor/rules/qa.mdc`，记住 6 条铁律（特别是"测试命名挂章节号、失败必带 traceId 三联查、性能基线 P95 < 500ms"）。
2. **跑一次模块回归**：让 qa-agent 为 DS-15 写 e2e + unit 测试，覆盖 bid-reference 对应章节，目标 ≥ 90% 覆盖 + CI 全绿。
3. **跑一次三联查**：故意触发一个失败用例 → 取 traceId → 在 Tempo / Loki / Prom 找到根因 → 写到测试报告。

### 12.3 必读 / 必跑

- **必读**：mdc + `bid-reference/*.md`（章节真源） + `acceptance-review-workflow.md` + `observability.md`（三联查 SOP） + `templates/acceptance-*.md` + `验收文档/*`（历史样本）
- **必跑**：在 `gkx_lumen_*` 仓 `npm run test` / `mvn test` / `pytest` 看 CI 是否绿 → 看 dev URL → 调一次接口 → 三联查 trace

### 12.4 注意区分

- ❌ **不改业务代码**（发现 bug → 开 issue 派给对应开发 agent）
- ❌ **不擅自跳过测试**（任何 skip 必有理由 + 票号）
- ❌ **不直接对甲方汇报**（验收报告经 PM 审）

---

## 13. doc 文档

> **一句话定位**：handoff 模板维护 + 验收 docx 汇编 + 对外材料起草 + 术语口径 + 文档索引；**docx 必走 officecli MCP**。  
> **对应 rule**：`.cursor/rules/doc.mdc`

### 13.1 AI 前 vs AI 后

| 维度 | AI 之前 | AI 之后 | 关键变化 |
|------|---------|---------|----------|
| 需求入口 | 里程碑前临时被叫去写 docx | 与 qa-agent 联动，qa handoff 一出立即开工；周报由 task-registry 自动汇总 | 不再"突击写报告" |
| 核心工具 | Word 手写 + Excel 整理 + 复制粘贴 | Cursor + `doc-agent` + officecli MCP + Markdown 模板 + bid-reference 术语库 | docx 命令式生成、可版本化 |
| 产出节奏 | 节点前赶工通宵 | 周报每周 1 次 / 月报每月 1 次 / 里程碑 docx 当日产出 | 节奏稳定、不熬夜 |
| 产物存放 | 各自硬盘 + 邮件 | `验收文档/*.docx`（officecli 产）+ `templates/*` + `formal-docs-registry.yaml` 索引 | 全在 git、版本号 / 双签留底 |
| 跨岗依赖 | 等 qa 出报告 + 等 PM 给口径 + 等架构师审 | 上游 qa-agent + 各开发 handoff + PM 答疑要点；下游 PM 终审 + 对外发 | 流水线、不阻塞 |
| 错误检查点 | 客户回信才发现术语错 / 数据错 | 术语自检（≥ 10 处关键词抽检）+ 证据链接校验 + officecli outline 对比 + PM 终审 | 多关拦截 |
| 交付周期 | 1 份验收报告 2–3 天 | 4–6h（含 PM 终审） | 4 倍提速 |
| 质量保障 | 主观、靠经验 | 7 条自检（officecli 出 / outline 对齐 / 术语一致 / 证据链接 / 版本+作者 / PM 审 / _tmp 清理） + 双签 | 可量化、可追溯 |

### 13.2 明天起，你该做什么（3 件）

1. **读自己的 mdc**（10 min）：`.cursor/rules/doc.mdc` + `officecli-doc-workflow.md`，记住 7 条铁律（特别是"docx 必走 officecli、不直发甲方、不擅自承诺"）。
2. **跑一次验收 docx**：让 doc-agent 把 qa-agent 上个里程碑的 handoff 汇编为 `验收文档/M{N}.docx`，要求 7 条自检全过 + PM 签字。
3. **维护术语统一表**：把 `bid-reference` ↔ lumen 实现 ↔ 验收报告三方的关键术语整理一张表，放 `formal-docs-registry.yaml` 旁边。

### 13.3 必读 / 必跑

- **必读**：mdc + `officecli-doc-workflow.md`（**首要工具规范**） + `templates/*` + `acceptance-review-workflow.md` + `formal-docs-registry.yaml` + `bid-reference/*.md` + `验收文档/`（历史样本）
- **必跑**：在 Cursor 调用 officecli MCP 工具 → 把任意 md 转成 docx → 看 outline 是否对齐 → 加版本号首页 → PM 审

### 13.4 注意区分

- ❌ **不直接发邮件给甲方**（任何对外稿件经 PM 审 + PM 发）
- ❌ **不写代码** / **不改业务实现** / **不评审架构**
- ❌ **不擅自改 bid-reference**（招标需求 MD 是真源，只读）
- ❌ **不擅自改 task-registry / scope-baseline**（那是 coordinator + PM）
- ❌ **不在 docx 嵌入未经 qa 验证的"实测结果"**

---

## 14. 跨角色反模式与红线（全员适用）

以下 8 个反模式 **每个角色都会踩**，对应红线 / 对策来自 `team-collaboration-playbook.md` 和 `.cursor/rules/00-team-constitution.mdc`。

| # | 反模式 | 典型表现 | 红线 / 对策 |
|---|--------|---------|-------------|
| 1 | **AI 写、人只 review** | 自己永远不动手，3 个月后失去独立思考能力 | 月度"AI off"1 天，全员手写 |
| 2 | **Lead 不亲跑 agent** | 派单不准、评审走形式 | Lead 每周必须亲跑 ≥ 3 个任务 |
| 3 | **个人 prompt 不沉淀** | 张三 AI 风格 ≠ 李四，产出漂移 | 成功 prompt 进 `.cursor/rules/`（PR 制度） |
| 4 | **Figma 与代码两套真源** | 设计与代码持续漂移 | Figma 一次性导 tokens 后弃用，代码维护 |
| 5 | **commit 不标作者** | 出 bug 找不到人 / agent | commit message 必带 `[agent:xxx]` 或 `[human:xxx]`，CI 检查 |
| 6 | **本地并发 > 4** | 人脑监管不过来，必漂移 | 本地 ≤ 4，超量必上 Background Agents |
| 7 | **cost 字段不回填** | 月底预算审计找不到出处 | task-registry 4 字段缺一不收（DoD 第 7 条） |
| 8 | **绕过 bid-reference 改需求** | scope 悄悄越界，月底超 ±10% | 任何需求变更必回 PM + bid-reference 评审 |

---

## 15. 落地清单（按层级展开）

### 15.1 个人级（每人，明天起）

- [ ] 读自己角色对应的 `.cursor/rules/{role}.mdc`（5–10 min）
- [ ] 读本手册自己那一节（5 min）+ 总览矩阵自己那一列（2 min）
- [ ] 完成"明天起你该做什么"3 件中的至少 1 件
- [ ] 在 Cursor 开新会话用对应 agent 跑通 1 个真实 task

### 15.2 Team Lead 级（本周内）

- [ ] 在 1v1 中检查每个组员"明天起 3 件"的完成度
- [ ] 给团队 mdc 提至少 1 个优化 PR（让它更贴自己团队）
- [ ] 主持 1 次 30 min 团队分享（讲 1 个跑通经验 / 1 个翻车经验）
- [ ] 选 1 名"AI 推进者"持续优化团队的 prompt / rules

### 15.3 PM / 架构师级（本季度内）

- [ ] 每月 1 次预算回顾（读 task-registry 的 `actual_cost` + budget-estimate v1.x 校准）
- [ ] 每 Epic 1 次架构 baseline 一致性扫描（architect-agent 出报告）
- [ ] 每里程碑 1 次手册自更新（本手册根据踩坑经验迭代到 v1.1 / v1.2）
- [ ] 季度复盘：12 角色"AI 之后"那一列是否所有人都达成

---

## 16. 手册版本记录

| 版本 | 日期 | 主要变化 | 维护者 |
|------|------|---------|--------|
| v1.0 | 2026-06-17 | 首版：12 角色 × 8 维度全覆盖；配合 2026-06-18 团队宣讲 | doc-agent + 架构师 |
| v1.1 | TBD | 根据宣讲后 1–2 周团队反馈迭代；补真实踩坑案例 | TBD |
| v2.0 | 项目复盘后 | 项目结束后总结：每角色实际 vs 预期差距 + 下一项目沿用建议 | PM + 架构师 |

---

## 17. 相关文档索引

| 类型 | 文档 | 路径 |
|------|------|------|
| 角色规约（机器读） | 12 份 mdc | `.cursor/rules/*.mdc` |
| 团队公约 | team-collaboration-playbook | `agent-delivery/team-collaboration-playbook.md` |
| 新人 1 天 onboarding | team-onboarding | `agent-delivery/team-onboarding.md` |
| 编排手册（派单话术） | 智能体编排与派单手册 | `agent-delivery/智能体编排与派单手册.md` |
| 架构基线 | architecture-baseline | `agent-delivery/architecture-baseline.md` |
| 成本预算 | budget-estimate | `agent-delivery/budget-estimate.md` |
| 任务真源 | task-registry | `agent-delivery/task-registry.yaml` |
| 范围基线 | scope-baseline | `agent-delivery/scope-baseline.yaml` |
| 业务真源 | bid-reference | `agent-delivery/bid-reference/*.md` |
| 培训宣讲 PPT | 2026-06-18 团队 AI 协作宣讲 | `agent-delivery/培训/2026-06-18_团队AI协作宣讲.pptx` |
| 培训宣讲逐字稿 | 2026-06-18 逐字稿 | `agent-delivery/培训/2026-06-18_逐字稿.md` |

---

> **结语**：这份手册不是死文档，是**活公约**。  
> 你踩了哪个角色的坑、发现哪条对照不准、想到更好的"明天起 3 件"——开 PR 改它。  
> 改的越多、团队越好。
