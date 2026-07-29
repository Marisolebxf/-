# AI Token 预算估算与回填台账

> **读者**：PM、各团队 lead、coordinator-agent  
> **作用**：建立项目级 AI token 消耗模型 / 团队分摊预算 / 告警阈值 / 实测回填机制  
> **关联**：`team-collaboration-playbook.md`（团队公约）· `task-registry.yaml`（实测回填）· `orchestration-maturity-and-roadmap.md`（Phase 2 上预算护栏）  
> **维护**：PM + coordinator-agent  
> **日期**：2026-06-17  
> **修订**：v1.1（补齐文档组任务量；下次首个 Epic 完成后重校准）

---

## 0. 一句话结论

> **混合模型档（核心 Opus + 量产 Sonnet）全项目约 $1,230，月度约 $308 / 25–35 人团队，人均月 $9–12，与 Cursor Pro 个人订阅 $20 相当。**

---

## 1. 单位经济基线（基于实测）

### 1.1 实测样本（2026-06-17）

| 会话样本 | 产出 | 估算 in tokens | 估算 out tokens | 估算成本（Sonnet 4.5） |
|---------|------|---------------:|---------------:|----------------------:|
| 写公约 + 11 rules + onboarding + README 改 | 21.5 KB md | ~110 K | ~18 K | $0.60 |
| UX 沙箱 DS-15（4 个 md）| 12 KB md + 图 | ~80 K | ~10 K | $0.40 |

> 后续每次会话用 coordinator 工具自动回填到 `task-registry.yaml` 的 `actual_*` 字段。

### 1.2 模型价格档位（2026-06 公开价）

| 档位 | 模型 | 输入 $/M | 输出 $/M | 适合场景 |
|------|------|--------:|--------:|---------|
| **A 经济** | Haiku 4 / GPT-5 mini | $0.25 | $1.25 | coordinator 派单、doc 整理 |
| **B 主力** | Sonnet 4.5 / GPT-5 | $3 | $15 | 所有量产编码、设计、测试 |
| **C 旗舰** | Opus 4.7 / GPT-5 Pro | $15 | $75 | architect 评审、algorithm 选型 |

---

## 2. 单任务消耗模型

> 实测 + Anthropic 公开数据（多 agent 比单 agent 贵 ~15x）+ SOTA 项目经验值。**已含修正系数 ×2.0**（修订迭代 ×1.5 + 长会话累积 ×1.3）。

| 任务类型 | 平均 in+out（K） | Sonnet 4.5 单次 $ | Opus 4.7 单次 $ |
|---------|---------------:|------------------:|----------------:|
| coordinator 派单 | 60 | $0.10 | $0.50 |
| architect 评审 | 200 | $0.40 | $2.00 |
| ux IA + wireframe | 300 | $0.60 | $3.00 |
| ui demo2 沙箱页 | 600 | $1.20 | $6.00 |
| frontend lumen 复刻 | 500 | $1.00 | $5.00 |
| api 单接口实现 | 300 | $0.60 | $3.00 |
| api Epic（多接口） | 1000 | $2.00 | $10.00 |
| algorithm 工程化 | 800 | $1.60 | $8.00 |
| data ADS + Mock | 400 | $0.80 | $4.00 |
| devops CI/Helm 一仓 | 160 | $0.30 | $1.60 |
| qa 测试套件（一 Epic） | 500 | $1.00 | $5.00 |
| doc 文档/汇编（一份） | 200 | $0.40 | $2.00 |

---

## 3. 全项目预算矩阵

### 3.1 项目规模假设

| 项 | 值 |
|---|---|
| 功能点 | 58（展示 30 + 专题 13 + 算法 15） |
| 涉及仓 | 6（lumen 3 + demo2 + algo 2） |
| 估计周期 | 4 个月（16 周） |
| 团队规模 | 26–37 人 |

### 3.2 各团队任务量 × 预算（修正后）

| 团队 | 任务类型 × 数量 | 总 tokens | Sonnet $ | Opus $ |
|------|--------------|--------:|--------:|--------:|
| coordinator | 派单 ×200（含重派） | 12 M | $20 | $100 |
| architect | Epic + 里程碑评审 ×30 | 6 M | $12 | $60 |
| ux | IA/wireframe ×50 | 15 M | $30 | $150 |
| ui | demo2 沙箱页 ×50 | 30 M | $60 | $300 |
| frontend | lumen 复刻 + 联调 ×50 | 25 M | $50 | $250 |
| api | 接口实现 ×120 | 36 M | $72 | $360 |
| algorithm | 算法工程化 ×25 | 20 M | $40 | $200 |
| data | ADS + Mock ×30 | 12 M | $24 | $120 |
| devops | CI/Helm/OTel ×40 | 6.4 M | $12 | $64 |
| qa | 测试套件 ×58 | 29 M | $58 | $290 |
| **doc (修正后)** | **周报16 + 月报4 + 里程碑4 + 验收5 + 答疑10 + 模板/索引维护11 ≈ 50** | **10 M** | **$20** | **$100** |
| **小计** | — | **201 M** | **$398** | **$1994** |

### 3.3 +50% 缓冲（学习曲线 / PoC / 失败重试 / 突发需求）

| 模型策略 | 全项目 4 月 | 月预算 | 人均月（按 30 人） |
|---------|------------:|------:|------:|
| 全 Sonnet 4.5 | $597 | $150 | $5 |
| **🟢 混合（核心 Opus + 量产 Sonnet，推荐）** | **$1,230** | **$308** | **$10** |
| 全 Opus 4.7 | $2,991 | $748 | $25 |

---

## 4. 团队月度预算分摊（混合档，$308 / 月）

| 团队 | 月预算 $ | 占比 | 关键控制点 |
|------|----:|----:|------|
| api 后端 | 90 | 29% | 最大头，多接口实现 |
| ui 设计实现 | 75 | 24% | 页面数量大 |
| qa 测试 | 58 | 19% | e2e 套件耗 token |
| frontend 工程 | 50 | 16% | 复刻 + 联调 |
| algorithm 算法 | 40 | 13% | 模型评估反复跑 |
| ux 设计 | 30 | 10% | 一次性 |
| data 数据 | 24 | 8% | ADS + Mock |
| **doc 文档** | **22** | **7%** | **修正：原 $8，被低估 2.7×** |
| coordinator | 20 | 7% | 派单消耗低 |
| architect | 12 | 4% | 评审型 |
| devops | 12 | 4% | 模板复用率高 |
| **总（含缓冲）** | **433** | — | （扣除重叠后 ≈ $308） |

> 注：单团队加和 > $308 是因为已在每项含 +50% 缓冲；实际按 $308 月预算池 + 各团队按比例分配。

---

## 5. 模型策略推荐表（投产比最高的配方）

| 场景 | 模型 | 理由 |
|------|------|------|
| coordinator 派单 | **A 经济** | 决策简单，便宜 5x |
| architect 评审 | **C 旗舰** | 一次错全盘错，必须好的 |
| algorithm 选型决策 | **C 旗舰** | 选错算法烧大钱 |
| ux IA/wireframe | B 主力 | 结构清晰，量产 |
| ui demo2 页 | B 主力 | 量产 |
| frontend 复刻 | B 主力 | 量产 |
| api 实现 | B 主力 | 量产 |
| algorithm 工程化 | B 主力 | 跑通即可 |
| data ADS / Mock | B 主力 | 模板化 |
| devops CI | B 主力 | 高度模板化 |
| qa 测试 | B 主力 | 量产 |
| doc 周报 / 月报 / 答疑 | **A 经济** | 简单整理 |
| doc 验收 docx / 里程碑材料 | B 主力 | 关键对外件 |

---

## 6. 降本 8 条铁律

| # | 铁律 | 预期省幅 |
|---|------|-------:|
| 1 | 共享 `.cursor/rules/` 减输入 token | 30% |
| 2 | 任务粒度 < 1h（超过强制拆分） | 50% |
| 3 | OpenAPI / ADS 契约先行 | 30% |
| 4 | Mock 数据先行 | 15% |
| 5 | 失败立即停（agent 跑歪 5 min 内 stop） | 20% |
| 6 | 模型选对（核心 Opus + 量产 Sonnet） | 60% |
| 7 | 长任务上 Background Agents（云） | 15% |
| 8 | 每周 retro token 排行榜 + 复盘 prompt | 10% |

> 单独看每条 10–60%，叠加不可乘（实际综合 50–70% 较真实）。

### 6.1 工作区瘦身（2026-07-30）

| 措施 | 路径 / 规则 | 预期效果 |
|------|-------------|----------|
| 瘦工作区 | `gkx-orchestration/workspaces/*.code-workspace` | 避免默认打开 17 根 `gkx-lumen.code-workspace`，减少多仓 `CLAUDE.md` / `AGENTS.md` 同时注入 |
| 工作区说明 | `gkx-orchestration/workspaces/README.md` | 按任务选 orch / fe-science / fe-topic / java-api / algo-py / admin-ui |
| 索引忽略 | 各仓根 `.cursorignore` + 编排仓额外忽略 `agent-handoffs/**/evidence/`、`验收文档/` | 降低 node_modules、构建产物、Office/图片、`.env` 等进入索引的 token |
| 长文档归档 | Java：`docs/upstream-pigx-CLAUDE.full.md`；Vue 管理台：`docs/CLAUDE.full.md` | 根目录 `CLAUDE.md` 保持 ~40–60 行 GKX 指针 |
| **folder 命名** | `*.code-workspace` 的 `folders[].name` **仅用短英文 id**（如 `gkx-orchestration`） | 禁止括号、斜杠、长中文；否则 Ctrl+Click / 部分工具会把显示名拼进路径 |

> 与 §6 铁律 #1（共享 rules）叠加使用；全量工作区仅用于跨仓大重构 / 全局检索。

---

## 7. 告警阈值（Phase 2 接入 Slack / GitLab）

> ⚠️ 当前阶段：人工监控；Phase 2 起 Background Agents 时改自动接入。

| 等级 | 阈值 | 自动处理 | 人工处理 |
|------|------|---------|---------|
| ⚠️ 黄 | 单任务 > $5 | 系统在 task-registry 标 `cost_warn: yellow` | PM 知会 |
| 🟧 橙 | 单任务 > $10 | 暂停 + 通知 lead | 复盘 prompt + 决定是否继续 |
| 🔴 红 | 单任务 > $20 | hard stop + 通知 architect + PM | 必须 architect 评审是否拆分 |
| 🔴 红 | 单日团队总 > $50 | team standdown | 全团队复盘 |
| 🔴 红 | 月度项目总 > $500 | 通知 PM | PM 评审是否超范围 / 调预算 |

---

## 8. 实测回填机制（task-registry 联动）

每个 task 完成时，coordinator-agent **必须** 回填 5 个字段（详见 `task-registry.yaml` cost_tracking_policy.fields）：

```yaml
- id: T-DS-15-ux-pilot
  agent: ux-agent
  status: done
  # ↓ 预算跟踪字段（必填，5 项缺一不可，否则 validation 阻止 status→done）
  estimated_tokens: 300_000      # 派单前估
  actual_tokens: 285_000         # 完工后实测（in+out）
  model_used: claude-sonnet-4.5  # 用了哪个模型（必须为 valid_model_enum 成员）
  actual_cost: 0.57              # 美元，按 model_used 的价表算
  cost_warn: green               # green(<$5) / yellow(>$5) / orange(>$10) / red(>$20)
```

### 8.1 自动校验（v1.2 新增）

`task-registry.yaml` 的 `cost_tracking_policy.validation` 节定义了 5 项必检规则：

| 检查项 | 条件 | 失败动作 |
|--------|------|---------|
| 估算有值 | `estimated_tokens > 0` | 阻止 status→done |
| 实测有值 | `actual_tokens > 0` | 阻止 status→done |
| 模型合法 | `model_used in valid_model_enum` | 阻止 status→done |
| 成本有值 | `actual_cost > 0` | 阻止 status→done |
| 告警等级 | `cost_warn` 与 `cost_thresholds` 匹配 | 自动修正 |

### 8.2 统一计算口径（v1.2 修订）

`task-registry.yaml` 的 `cost_tracking_policy` 新增 `cost_formula` / `pricing` / `default_ratios` 三节，
所有 `actual_cost` 一律按以下公式计算，不再接受手工估算：

```
actual_cost = actual_tokens × input_ratio × input_price/$M / 1_000_000
            + actual_tokens × output_ratio × output_price/$M / 1_000_000
```

| 参数 | 来源 |
|------|------|
| `actual_tokens` | task 完工回填（in+out 之和） |
| `input_ratio` / `output_ratio` | 按 agent 类型从 `default_ratios` 取（如 coordinator 95/5, algorithm 75/25） |
| `input_price` / `output_price` | 从 `pricing` 表取（对齐 §1.2 公开价） |

**精确值优先**：如 agent 可从 Console 获取 in/out 分离值，填 `actual_input_tokens` / `actual_output_tokens`，
此时用精确值代替 `default_ratios` 计算（handoff 注明 `source: console_precise`）。

### 8.3 结构化阈值（v1.2 新增）

`cost_tracking_policy.cost_thresholds` 可被脚本解析执行，替代原 hard_stop_rules 中的纯文本描述：

| 等级 | 单任务阈值 | 自动动作 | 人工动作 |
|------|-----------|---------|---------|
| ⚠️ 黄 | > $5 | 标 cost_warn: yellow | PM 知会 |
| 🟧 橙 | > $10 | 暂停 + 通知 lead | 复盘 prompt + 决定是否继续 |
| 🔴 红 | > $20 | hard stop + 通知 architect + PM | architect 评审是否拆分 |
| 🔴 红 | 团队日 > $50 | team standdown | 全团队复盘 |
| 🔴 红 | 月度项目 > $500 | 通知 PM | PM 评审是否超范围 / 调预算 |

### 8.3 回填来源
- Cursor IDE 右下角 token 计数器（粗略）
- Cursor Teams Analytics 仪表盘（精确，需 Team 订阅）
- Anthropic / OpenAI Console（精确，需访问 API key）

---

## 9. 每周 retro 模板

```markdown
# Week {N} 预算 retro
- 本周总成本：$X / 预算 $77（周）
- TOP 5 最贵任务：
  1. T-xxx ($X) - agent - 原因 - 改进建议
  2. ...
- TOP 5 估算偏差最大：
  1. T-xxx 估 $Y 实 $X，偏 ±Z%
- 模型用量分布：Haiku X% / Sonnet Y% / Opus Z%
- 本周触发告警：黄 N / 橙 N / 红 N
- 下周改进：
  - prompt 优化：...
  - 任务拆分：...
  - 模型重选：...
```

---

## 10. 可信度声明（首个 Epic 后必须重校准）

| 维度 | 数据来源 | 可信度 |
|------|---------|------|
| 单会话 token 量 | 本次实测 + UX DS-15 实测 | 高 |
| 单任务 token 量 | Anthropic 公开 + 业界 SOTA + 内推估 | 中 |
| 修订系数 ×2 | 业界平均 | 中 |
| 任务数量 ×N | 基于 58 功能点 + 6 仓推算 | 中低 |

**实际偏差可能 ±50%。强烈建议第一个 Epic 跑完后用 task-registry 的 `actual_tokens` 重校准本预算表（更新 v1.2）。**

---

## 11. 修订历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-17 | 初稿 |
| v1.1 | 2026-06-17 | 修正文档组任务量（20 → 50），月预算占比 3% → 7% |
| v1.2 | 2026-06-22 | **预算跟踪机制修复 + 统一口径**：①所有 leaf task 补齐 5 个预算字段；②修正 model_used 非法值；③修正 cost_warn 与阈值不匹配；④新增 cost_thresholds / budget_aggregation / validation 结构化节；⑤新增 cost_summary 汇总节；⑥**统一 actual_cost 计算口径**：新增 cost_formula + pricing + default_ratios（按 agent 类型设定 in/out 比例），14 个任务 actual_cost 按公式重算；⑦budget-estimate.md §8 扩充为 8.1~8.4 |
