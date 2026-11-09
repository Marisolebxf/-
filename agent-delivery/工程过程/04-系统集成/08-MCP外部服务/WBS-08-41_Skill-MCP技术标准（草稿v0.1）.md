# Skill / MCP 技术标准（草稿 v0.1）

> 对应 WBS-08-41（负责人：李瑞，2026-11-11 交付）。本草稿由 agent 按 WBS-08-41 起草，供讨论定稿。
> 上游依据：`GKX-12-01`（能力边界）、`GKX-12-02`（D0–D3 数据依赖与能力边界卡）、`GKX-12-03`（首批三系统场景与元数据要求）。
> 行业参考：MCP 官方规范（2025-03-26）、OWASP MCP Top 10（2025）、Block / Webex MCP 工程实践、OpenTelemetry。

## 1. 定位与适用范围

- **适用对象**：三系统供应商交付的全部对外 Skill/MCP，以及智树侧网关与平台层。
- **本标准管**：MCP 工具的接口契约、错误处理、安全、版本、可观测、数据诚实性——即「工具必须长什么样、怎么行为」。
- **本标准不管**：业务功能边界（见 GKX-12-01 逐项确认）、建设批次（GKX-12-02）、评测怎么打分（见评测标准草稿 WBS-08-42）。
- **总原则**：MCP 是给 LLM 用的 API。一切设计以「模型能选对、参数能填对、结果能用对、失败能自愈」为准，不以人用 UI 的标准替代。

## 2. 工具设计标准

| 项 | 标准 | 依据 |
|---|---|---|
| 工具命名 | `snake_case` 动词短语，1–64 字符，仅 `[a-z0-9_]`；同一能力域内前缀统一（如 `chain_*`、`policy_*`、`talent_*`）；名称必须表达「做什么」而非「哪个系统哪个页面」 | MCP 规范允许 1–128 字符，本项目收紧到 64 保证检索与防撞名 |
| 设计粒度 | **面向任务/工作流设计，不按后端 API 一比一暴露**。一个工具 = 一次可独立使用的业务动作（查询、对比、识别、推荐、生成）；相关联的小调用在服务端聚合 | Block Playbook：combine related calls |
| 工具描述 | 必须写清：用途、何时该用、何时不该用（不适用范围）、返回什么、参数约束。**描述是模型选型的唯一依据**，禁止空泛描述 | MCP 官方 / Webex 实践 |
| 幂等与破坏性 | 查询类工具必须幂等（同参数同结果）；写/生成类工具须在描述中显式标注副作用；**破坏性操作必须在服务端二次确认，不依赖客户端弹窗** | OWASP MCP03 / 生产实践 |
| 输出体量 | 单次返回控制在 token 预算内（建议 ≤ 8K token）；超限自动截断并标注 `truncated: true` + 补取参数（`offset`/`cursor`），或提供分页工具 | Block Playbook：check size before returning |

## 3. 接口契约标准

### 3.1 输入（inputSchema，强制）

- 每个工具必须定义合法 **JSON Schema（2020-12）**；无参工具用 `{"type":"object","additionalProperties":false}`。
- 字段必须：显式类型、枚举（能枚举的必须枚举，如区域码、路线名）、长度上限、数值边界（`minimum`/`maximum`）、必填项标注；每个字段带 `description`。
- **服务端运行时校验**：拒绝未知字段、拒绝超限值，校验失败返回结构化错误（见 §4），不得静默截断或采用默认值蒙混。
- 禁止 free-form 字符串承载结构化语义（能用枚举/结构体就不用长文本）。

### 3.2 输出（结构化 + 证据元数据，强制）

- 输出为结构化 JSON，**字段命名与本清单（HV-xx）的「标准输出」列对齐**，禁止返回渲染好的 HTML/纯文本段落冒充数据。
- 每个统计数字透传 `metric_id`（智树侧 D9 血缘要求）；mock 数据原样标注 mock 状态，**不得剥掉标识冒充真数**。
- **每个响应必须携带 GKX-12-03 §6 的 9 项元数据**（D2/D3 能力强制，D0/D1 建议）：

```json
{
  "data": { "...": "业务数据" },
  "meta": {
    "data_dependency_level": "D3",
    "data_sources": ["ads_chain_xxx"],
    "data_version": "2026-11-08",
    "as_of_date": "2026-10-31",
    "coverage_scope": "地域/主体/时间/样本规模",
    "known_gaps": ["..."],
    "confidence": "low|medium|high + 理由",
    "allowed_use": "demo|research|production",
    "refresh_required": true
  }
}
```

## 4. 错误处理标准

- **两类错误严格区分**（MCP 规范）：
  - 协议错误（JSON-RPC error）：未知工具、参数不合法、服务端故障——模型修不了的问题；
  - 工具执行错误（`isError: true`）：业务失败——**错误消息必须让模型能自救**：说清什么失败、为什么、下一步怎么办（改参数？换工具？还是放弃转人工？）。
- **结构化错误码**：每类错误有稳定 `code`（如 `UPSTREAM_TIMEOUT`、`NO_DATA_IN_SCOPE`、`INVALID_PARAM`），附 `retryable` 与 `retryAfterSeconds`；禁止把堆栈或内部日志直接抛给模型。
- **超时**：每个工具显式设超时（无默认值兜底的裸等待是事故源）；超时阈值按下游 **P99** 而非 P50 设定。
- **重试**：瞬时错误指数退避 + 抖动，服务端自查自愈；永久错误不重试、直接结构化上报。
- **降级即诚实**：数据不足 / 部分失败时返回**可解释的部分结果 + 待补项清单**（`partial: true` + `missing` 列表），禁止返回编造的完整结果，禁止把降级结果伪装成正常结果。对齐 GKX-12-02「数据不足时降级为『信息不足 / 待真实数据验证』」。

## 5. 安全标准（对标 OWASP MCP Top 10）

| 风险 | 本项目强制要求 |
|---|---|
| MCP01 凭据暴露 | token 只放使用人本机环境变量，不进 git、不进日志、不进工具描述；凭据最小作用域、可过期 |
| MCP02 权限蔓延 | 每个工具只授予完成任务所需最小数据权限；读分析类工具不配写权限；权限变更走评审 |
| MCP03 工具投毒 / rug pull | 工具描述、schema 变更纳入版本管理并公示；客户端展示完整工具清单，不接受摘要 |
| MCP05/06 注入 | 所有外部输入按不可信处理：参数化查询、禁动态拼接 SQL/nGQL、禁 `eval`；工具输出过注入消毒再进上下文 |
| MCP07 认证鉴权 | MCP 服务端校验调用方身份与数据权限（按用户/租户），不只依赖网关外层 |
| MCP08 审计缺失 | 每次调用记审计日志（谁、何时、哪个工具、什么参数摘要、结果状态） |
| MCP10 上下文过共享 | 跨用户/跨任务数据严格隔离；响应不含其他用户可见字段 |

## 6. 版本与兼容标准

- **schema 不做原地破坏性变更**：入参/出参不兼容时新增版本化工具名（`search_talent_v2`），旧版保留一个过渡期后下线并公告。
- 每个工具有 `version` 字段（语义化 `MAJOR.MINOR`）；MAJOR 变更 = 参数或输出不兼容。
- 工具清单（名称、描述、schema、版本、数据依赖等级）随每批建设冻结归档，作为评测基线。

## 7. 可观测性标准

- 每次工具调用埋点（对齐智树 OTel 体系）：`tool.name`、耗时、输入/输出字节数、成败、错误码、trace 透传（zmate → MCP → Java 网关 → Python 全链同 traceId）。
- 最低指标集：调用 QPS、成功率、P95/P99 时延、错误码分布、token 消耗——评测「三系统调用成功率 ≥99%」与线上巡检均依赖此数据。
- 日志保留窗口与脱敏规则由平台统一，供应商不私自决定。

## 8. 数据诚实性标准（GKX 特有，高于行业基线）

1. D2/D3 能力的输出**必须**带样本限定语，且 `allowed_use` 不得填 production（总集真实数据接入前）。
2. mock 一律透传 mock 标识；评测与演示材料中禁止把 mock 结果表述为真实数据结论（对齐评测红线）。
3. 引用/证据字段必须可回查：返回 `evidence` 数组（来源 ID + 定位信息），不允许只给结论不给出处。
4. 数据版本变化（`data_version` 跳变）触发该工具回归测试，结果不自动继承。

## 9. 交付验收清单（每工具必过）

- [ ] inputSchema 完整（类型/枚举/边界/必填/描述），运行时校验生效
- [ ] 输出结构化 + 9 项元数据（D2/D3 强制）
- [ ] 两类错误区分 + 结构化错误码 + P99 超时 + 降级部分结果
- [ ] 最小权限 + 审计日志 + 注入消毒
- [ ] 版本号 + 变更记录 + 工具清单冻结
- [ ] OTel 埋点 + trace 透传
- [ ] mock 透传 + metric_id 透传 + 证据可回查
- [ ] 能力边界卡已提交（GKX-12-02 要求，未提交不得进演示验收）

## 10. 参考来源

- MCP Specification 2025-03-26 — Tools：https://spec.modelcontextprotocol.io/specification/2025-03-26/server/tools/
- OWASP MCP Top 10 (2025)：https://owasp.org/projects/mcp-top-10
- OWASP MCP Security Cheat Sheet：https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html
- Block, Playbook for Designing MCP Servers：https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers
- Webex, Best Practices for Building MCP and A2A Servers：https://developer.webex.com/mcp/docs/best-practices-for-building-mcp-and-a2a-servers
- Microsoft, MCP Development Best Practices（OWASP 指南 Azure 版）：https://microsoft.github.io/mcp-azure-security-guide/adoption/development-best-practices/
- MCP Servers in Production: Lessons Learned：https://dev.to/x1y1co/mcp-servers-in-production-lessons-learned-3hk7
