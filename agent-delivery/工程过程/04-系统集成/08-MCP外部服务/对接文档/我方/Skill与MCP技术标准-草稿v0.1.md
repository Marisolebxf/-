# Skill 与 MCP 技术标准（草稿 v0.1）

> 状态：草稿，供 2026-11-11 讨论。技术标准负责人李瑞（WBS-08-41），本稿由淮政玮侧起草供修订。
> 日期：2026-11-09
> 适用：展示系统、专题系统、新型高端智库系统对外提供给 zmate（及同类智能体客户端）的全部 MCP 与 Skill。
> 上位材料：[GKX-12-01 建设范围公示](../../德金提供的参考材料/GKX-12-01_Skill与MCP建设范围公示及确认.md)、[GKX-12-02 四批建设计划](../../德金提供的参考材料/GKX-12-02_Skill四批建设计划.md)、[GKX-12-03 首批场景方案](../../德金提供的参考材料/GKX-12-03_首批三系统重点场景建设方案.md)、[GKX-12-04 统一评测与验收规范](../../德金提供的参考材料/GKX-12-04_Skill统一评测与验收规范.md)。
> 配套：[业务场景评测标准-草稿v0.1](./业务场景评测标准-草稿v0.1.md)。

## 0. 用语

- **必须**：不满足即不能进入评测和演示。
- **应**：默认要做；不做须在接口文档里写明原因。
- **可**：按需。

本标准只定「怎么建才合格」。建什么由 GKX-12-01 的范围清单定，评得怎么样由评测标准定。

---

## 1. 分层与职责

| 层 | 负责 | 不负责 |
|---|---|---|
| 业务系统 | 真实数据、业务计算、数据权限 | 面向模型的措辞和编排 |
| MCP | 把已有业务能力封装成可调用的工具：参数、输出结构、鉴权、超时、错误码、版本、日志 | 业务算法；把未建成的能力包装成已具备 |
| Skill | 完成业务任务的方法：触发条件、步骤、用哪些 MCP、判断规则、人工确认点、失败处理、证据要求、输出规范 | 直接访问数据库或业务内部接口 |

调用链必须是：智能体客户端 / Skill → MCP → 业务系统 Java 网关 → 算法服务。MCP 不得直连算法服务、图数据库或数据库，不得调用 `demo-*` 原型服务（国科信 D12）。

### 1.1 阶与依赖等级

每个 MCP 工具和每个 Skill 必须标两个属性：

- **阶**：一阶 = 垂向域查询；二阶 = 垂向域专题战略分析；三阶 = 综合分析（某产业综合战略分析，某技术的科研、产业化、政策支持情况）。
- **数据依赖等级**：D0 方法论型 / D1 低依赖 / D2 中依赖 / D3 高依赖，定义以 GKX-12-02 §1.1 为准。

一般对应关系：一阶多为 MCP 工具；二阶是 MCP 工具，或「一个 Skill + 少量工具」；三阶必须是 Skill，由它编排多个一、二阶工具。三阶不应做成一个黑盒大工具，否则无法评测中间步骤，也无法回查证据。

---

## 2. MCP 协议与部署

| 编号 | 要求 | 级别 |
|---|---|---|
| P-1 | 目标协议版本 `2026-07-28`。zmate 客户端若尚未支持，向下兼容 `2025-11-25`；版本协商结果写入日志 | 必须 |
| P-2 | 对外正式服务用 Streamable HTTP，部署在 lumen 网关之后，统一 HTTPS 入口。stdio 只用于本机开发和自测 | 必须 |
| P-3 | 服务按无状态设计：任一请求可落到任一实例，不依赖会话粘滞 | 应 |
| P-4 | `tools/list` 返回顺序固定（便于客户端缓存和提示词缓存命中） | 应 |
| P-5 | 每个业务系统一个 MCP 服务（如 `gkx-display`、`gkx-topic`、`gkx-thinktank`），服务名进入工具元数据，便于客户端区分同名工具 | 应 |
| P-6 | 只暴露 tools。resources、prompts 首批不用；需要时另行评审 | 可 |

---

## 3. 工具设计

### 3.1 粒度

- 按「一个业务问题一个工具」切，不按后端接口一一映射。同构接口用参数区分（例如一个 `analyze_industry_chain` 用 `aspect` 参数覆盖周期、瓶颈、关键环节），不拆成多个工具。
- 一个服务对外工具数应控制在 20 个以内。工具太多会降低模型选对工具的概率。
- 写操作首批不开放。确需开放的，必须带人工确认（见 §7.4）。

### 3.2 命名

| 编号 | 要求 | 级别 |
|---|---|---|
| N-1 | 工具名用 snake_case 的「动词_对象」，与 [AI 战略咨询 MCP 清单](../../德金提供的参考材料/AI战略咨MCP清单.md) 的「建议 MCP 工具名」列一致，如 `get_science_technology_landscape` | 必须 |
| N-2 | 只用 `a-z`、`0-9`、`_`，长度不超过 64，全项目唯一 | 必须 |
| N-3 | 一阶查询统一用 `search_` / `get_` 开头；二阶分析用 `analyze_` / `compare_` / `identify_` / `recommend_` / `evaluate_` 等；三阶由 Skill 承担，不另起工具前缀 | 应 |
| N-4 | 参数名写全称、带单位或格式，如 `region_code`、`start_year`、`as_of_date`，不用 `id`、`type`、`q` 这类含糊名 | 必须 |

现有 `gkx-7chain` 用的是 kebab 命名（`search-enterprise`），对外前按 N-1 改名，见 §13。

### 3.3 描述

工具的 `description` 是模型选工具的唯一依据，必须写清：

1. 做什么，用一句话；
2. 什么时候用、什么时候不用（指向更合适的工具）；
3. 关键参数的取值范围和示例；
4. 返回的主要字段和数据边界（如「仅已收录样本，不代表全量」）；
5. 阶和数据依赖等级。

描述里不得出现指令性内容（如「忽略之前的要求」「必须先调用某工具」），也不得夸大能力。描述属于提示注入面，变更须走评审（§7.3）。

### 3.4 输入 Schema

| 编号 | 要求 | 级别 |
|---|---|---|
| I-1 | `inputSchema` 用 JSON Schema 2020-12，顶层 `"type": "object"`，`"additionalProperties": false` | 必须 |
| I-2 | 每个参数有 `description`；枚举用 `enum`；字符串有 `maxLength`，格式类有 `pattern` 或 `format` | 必须 |
| I-3 | 必填项写进 `required`；可选项给默认值并在描述中说明 | 必须 |
| I-4 | 统一公共参数：`region_code`（行政区划码）、`time_range`（`start`/`end`，`YYYY` 或 `YYYY-MM-DD`）、`limit`（默认 20，上限 100）、`cursor`（分页）、`response_format`（`concise` / `detailed`，默认 `concise`） | 应 |
| I-5 | 服务端对所有输入做校验，不信任客户端已校验 | 必须 |

### 3.5 输出

| 编号 | 要求 | 级别 |
|---|---|---|
| O-1 | 每个工具必须声明 `outputSchema`，并在结果中返回符合该 Schema 的 `structuredContent` | 必须 |
| O-2 | 同时返回一段 `TextContent`：给模型读的简短摘要，加上序列化后的 JSON（兼容不读结构化结果的客户端） | 必须 |
| O-3 | 结构化结果使用 §4 的统一信封 | 必须 |
| O-4 | 只返回下一步决策需要的字段。内部主键尽量换成可读名称，同时保留轻量 ID 供下一步调用 | 应 |
| O-5 | 单次响应控制在约 25k token 以内。超出时分页或截断，并在 `meta.truncated` 和 `warnings` 里说明如何取剩余部分 | 必须 |
| O-6 | 图谱类结果默认节点数上限 80（与现有实现一致），可通过参数放宽，硬上限由服务端控制 | 应 |

### 3.6 行为标注

每个工具必须填 `annotations`：`readOnlyHint`、`destructiveHint`、`idempotentHint`、`openWorldHint`。首批工具应全部是 `readOnlyHint: true`。标注只是提示，不能代替服务端鉴权。

---

## 4. 统一返回信封

所有工具的 `structuredContent` 必须是如下结构。`meta` 中前九个字段来自 GKX-12-03 §6，其余为国科信补充。

```json
{
  "data": {},
  "evidence": [
    {
      "evidence_id": "ev-001",
      "type": "record | document | metric | graph_edge",
      "source": "来源系统或文献",
      "locator": "表/文档定位或 URL",
      "excerpt": "可选，原文片段",
      "as_of_date": "2026-10-31"
    }
  ],
  "meta": {
    "data_dependency_level": "D2",
    "data_sources": ["..."],
    "data_version": "2026-11-01.r3",
    "as_of_date": "2026-10-31",
    "coverage_scope": { "region": "...", "subjects": "...", "time": "...", "sample_size": 0 },
    "known_gaps": ["..."],
    "confidence": { "level": "high | medium | low", "reason": "..." },
    "allowed_use": "demo | research_reference | production",
    "refresh_required": true,

    "data_status": "real | mock | mixed",
    "metric_ids": ["M_..."],
    "tool_name": "compare_policy_details",
    "tool_version": "1.2.0",
    "tier": 2,
    "trace_id": "32 位十六进制",
    "truncated": false,
    "next_cursor": null
  },
  "warnings": []
}
```

字段规则：

- `data_status`：只要有一个数字来自 mock，就必须标 `mock` 或 `mixed`，不得写成 `real`。这是国科信 D9/D4 诚实性要求在 MCP 层的落点。
- `metric_ids`：结果里有统计数字的，必须带指标库的 `metric_id`。没有登记的写 `"UNREGISTERED"`，不得留空或编造。
- `evidence`：二阶、三阶结果里的每个结论性字段，必须能通过 `evidence_id` 回查到至少一条证据。一阶查询结果本身就是记录，`evidence` 可以只给来源和定位。
- `allowed_use`：总集真实数据接入前，D2、D3 能力只能填 `demo` 或 `research_reference`（GKX-12-04 §7）。
- 无数据不是错误：返回空 `data`、`confidence.level = "low"`，并在 `known_gaps` 写明缺什么，不得补 0 或用默认值冒充。

---

## 5. 错误处理

按 MCP 规范分两类：

| 类型 | 何时用 | 怎么返回 |
|---|---|---|
| 协议错误 | 工具不存在、请求结构不合法、服务内部故障 | JSON-RPC `error`（如 `-32602`） |
| 执行错误 | 参数取值不对、下游接口失败、无权限、超时、业务规则不满足 | 正常 `result`，`isError: true`，`content` 里写可执行的修正提示 |

执行错误的 `structuredContent` 用统一结构：

```json
{
  "error": {
    "code": "INVALID_ARGUMENT",
    "message": "start_year 必须早于 end_year，收到 start=2025, end=2023",
    "retryable": true,
    "hint": "示例：{\"start_year\": 2021, \"end_year\": 2025}"
  },
  "partial": null,
  "meta": { "trace_id": "...", "tool_name": "...", "tool_version": "..." }
}
```

统一错误码（首批）：`INVALID_ARGUMENT`、`NOT_FOUND`、`UNAUTHENTICATED`、`PERMISSION_DENIED`、`RATE_LIMITED`、`UPSTREAM_TIMEOUT`、`UPSTREAM_UNAVAILABLE`、`DATA_NOT_READY`、`PARTIAL_RESULT`、`INTERNAL`。

- `message` 必须告诉模型错在哪、怎么改，不得只给状态码或堆栈。
- 下游部分成功时用 `PARTIAL_RESULT`，`partial` 放已得到的结果，`warnings` 写缺失部分。
- 错误信息不得泄露内部地址、SQL、密钥或其他用户数据。

---

## 6. 认证与授权

| 编号 | 要求 | 级别 |
|---|---|---|
| A-1 | 远程 MCP 服务作为 OAuth 2.1 资源服务器，接入统一用户中心。客户端注册优先用 Client ID Metadata Document（CIMD），校验授权响应中的 `iss` | 必须 |
| A-2 | 校验 token 的签发方、受众（audience 必须是本 MCP 服务）、有效期和 scope；用成熟库校验，不自写 | 必须 |
| A-3 | 禁止 token 透传：不得把客户端带来的 token 原样转发给 Java 网关。MCP 用自己的服务凭证调用网关，同时以受信方式传递最终用户身份，由网关和业务系统做数据权限 | 必须 |
| A-4 | scope 按系统和读写最小化，如 `gkx.display.read`、`gkx.topic.read` | 必须 |
| A-5 | 本机 stdio 调试允许用环境变量提供临时凭证；凭证不得写入仓库、配置样例或日志 | 必须 |

---

## 7. 安全

### 7.1 输入与输出

- 所有输入按 Schema 严格校验，拒绝多余字段。
- 输出中来自外部文档或网页的文本（政策原文、新闻摘录等）必须放在 `evidence.excerpt` 之类的数据字段里，不得拼进工具描述或系统提示；必要时对可疑指令性文本做标记。
- 输出前过滤个人敏感信息（身份证号、手机号等），人才类能力尤其注意。

### 7.2 限流与配额

按用户和客户端两级限流；超限返回 `RATE_LIMITED`，并带 `retry_after`。

### 7.3 工具定义锁定

工具定义的全部内容（名称、描述、`inputSchema`、`outputSchema`、`annotations`）随版本计算哈希并登记。定义变化必须重新评审并升版本，防止上线后悄悄改描述或改标注（rug pull）。

### 7.4 人工确认

- 写操作、批量导出、对外发送类工具必须由客户端弹出人工确认，并展示完整参数。
- Skill 里标明的「人工确认点」（如三阶报告的关键结论）不得被模型自动跳过。

### 7.5 审计

每次调用记录：时间、用户、客户端、工具名与版本、参数摘要（敏感字段脱敏）、结果状态、耗时、`trace_id`。日志保留期按项目安全要求执行（默认 180 天，待定）。

---

## 8. 性能与可靠性

| 指标 | 一阶 | 二阶 | 三阶（Skill 端到端） |
|---|---|---|---|
| 单次工具调用 P95 | ≤ 3 s | ≤ 15 s | 不适用 |
| 单次工具调用超时上限 | 10 s | 60 s | 不适用 |
| Skill 端到端完成时间 | — | — | ≤ 10 min（报告生成类另定） |
| 调用成功率（不含参数错误） | ≥ 99% | ≥ 99% | ≥ 99%（GKX-12-03 §8） |

- 超过 60 秒的分析用异步：先返回任务号，再轮询；在 2026-07-28 规范下按 Tasks 扩展实现，客户端不支持时退回「提交 + 查询」两个工具。
- 只读工具必须幂等；重试不改变结果。
- 下游失败时优先返回部分结果和待补项，而不是整体失败（GKX-12-02 §3.7）。

以上数值是草稿起点，以首批压测结果修订。

---

## 9. 可观测性

- 支持 `_meta` 中的 `traceparent` / `tracestate`（2026-07-28 规范约定），没有则生成；调用 Java 网关时透传 `traceparent` 和 `X-Trace-Id`。
- 每次调用产生一个 OpenTelemetry span，属性至少含：`mcp.tool.name`、`mcp.tool.version`、`gkx.tier`、`gkx.data_status`、`gkx.user_hash`、结果状态。
- 指标至少有：调用量、错误率（按错误码）、P50/P95 耗时、截断率、mock 结果占比。
- 结果信封里的 `trace_id` 与日志一致，评测和用户反馈都靠它回查。

---

## 10. 版本与兼容

- 服务和工具都用语义化版本。改参数含义、删字段、改默认值属于不兼容变更，升主版本。
- 不兼容变更至少提前一个批次通知，旧版本保留不少于 30 天。
- 每次发布附变更说明，并重跑该工具的回归评测集（评测标准 §6）。

---

## 11. Skill 规范

### 11.1 格式

Skill 遵循 Agent Skills 开放标准：一个目录，含必需的 `SKILL.md`（YAML 头 + Markdown 正文），可选 `scripts/`、`references/`、`assets/`。

| 字段 | 要求 |
|---|---|
| `name` | 必须。1–64 位小写字母、数字、连字符，不以连字符开头或结尾，不连写连字符；与目录名一致。如 `solid-state-battery-strategy` |
| `description` | 必须。≤ 1024 字符，写清「做什么 + 什么时候用」，带用户会说的关键词 |
| `compatibility` | 应。写明依赖的 MCP 服务和最低版本 |
| `metadata` | 必须。至少含 `version`、`owner`、`tier`、`hv_ids`（如 `HV-13,HV-14`）、`data_dependency_level`、`systems` |
| `allowed-tools` | 应。列出本 Skill 允许调用的 MCP 工具 |

### 11.2 正文必备章节

按 GKX-12-01 §3 的要求，`SKILL.md` 正文必须有：

1. **触发条件**：什么请求该用本 Skill，什么请求不该用；
2. **输入澄清**：缺区域、时间、对象、决策问题时先问用户，不自行假定；
3. **步骤**：每步调用哪个工具、传什么参数、拿回什么；
4. **判断规则**：各步结果如何组合成结论，冲突时如何处理；
5. **人工确认点**：哪些结论必须用户或专家确认；
6. **失败处理**：工具报错、无数据、部分结果时怎么继续、怎么告知；
7. **证据要求**：每个结论引用哪些 `evidence_id`；
8. **输出规范**：章节结构、必须出现的限制声明（数据范围、`data_status`、样本限定语）。

### 11.3 写法

- `SKILL.md` 正文控制在 500 行以内，细节放 `references/`，按需加载。
- 不内嵌密钥、内部地址或测试账号。
- 不在 Skill 里硬编码业务结论或参考答案（会污染评测）。
- 引用的工具名和参数必须与当前 MCP 版本一致，Skill 发布前跑一次自检。

---

## 12. 交付物与准入

每个 MCP 工具 / Skill 进入评测前必须提交：

| 交付物 | 内容 |
|---|---|
| 数据依赖与能力边界卡 | GKX-12-02 §1.1 规定的全部项 |
| 接口文档 | 工具清单、参数、输出 Schema、错误码、示例请求与响应、阶、依赖等级、版本 |
| 样例 | 每个工具至少 3 组真实可复现的输入输出（正常、无数据、错误各一） |
| 自检脚本 | 不连后端也能跑的契约自检：工具都在、Schema 合法、缺参不发请求、错误码正确 |
| 部署说明 | 地址、鉴权方式、scope、限流、依赖服务 |
| 能力状态 | 已完成 / 需改造 / 新建 / 暂不具备，附页面、接口或测试证据（GKX-12-01 §3） |

准入检查清单（全部满足才进评测）：

- [ ] 工具名、参数名符合 §3.2
- [ ] 有 `outputSchema`，结果符合 §4 信封，`data_status` 和 `metric_ids` 如实
- [ ] 错误按 §5 分类，消息可执行
- [ ] 鉴权符合 §6，无 token 透传
- [ ] 工具定义已登记哈希
- [ ] trace 可从客户端串到 Java 网关
- [ ] 调用链不越层、不调用 demo 服务
- [ ] 边界卡、接口文档、样例、自检脚本齐全

---

## 13. 现有 gkx-7chain 的差距（供改造排期）

| 项 | 现状 | 本标准要求 |
|---|---|---|
| 传输 | stdio，本机拉起 | 对外用 Streamable HTTP（P-2） |
| 后端 | 除政策检索外打 demo 网关 | 全部切 lumen 网关（§1，D12） |
| 命名 | kebab，如 `search-enterprise` | snake_case「动词_对象」（N-1） |
| 输出 | 无 `outputSchema`；有 `data_source`、`metric_id`、`truncated` | 补 `outputSchema` 和 §4 全信封 |
| 鉴权 | 本机环境变量 token | OAuth 2.1 资源服务器，无透传（§6） |
| 错误 | 部分返回 HTTP 状态 | 按 §5 分两类、统一错误码 |
| 可观测 | 已带 `X-Trace-Id`、`traceparent` | 补 span 属性与指标（§9） |

---

## 14. 待讨论

1. zmate 客户端支持的 MCP 协议版本和传输方式（决定 P-1、P-2 能否一步到位）。
2. 统一用户中心能否作为 MCP 的 OAuth 授权服务器，或需要中间层。
3. 工具名是否全项目统一 snake_case，还是允许各系统前缀（如 `display_`）。
4. §8 性能数值和审计日志保留期。
5. 三阶 Skill 由哪个系统承载：首批方案里是高端智库报告工作台，展示和专题系统是否也各出一个三阶 Skill。

---

## 参考

- MCP 规范 2026-07-28：<https://modelcontextprotocol.io/specification/2026-07-28>；工具：<https://modelcontextprotocol.io/specification/2026-07-28/server/tools>；变更记录：<https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/changelog.mdx>
- MCP 安全最佳实践：<https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices>
- OWASP MCP Security Cheat Sheet：<https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html>
- Agent Skills 规范：<https://agentskills.io/specification>
- Anthropic，Writing effective tools for AI agents：<https://www.anthropic.com/research/writing-tools-for-agents>
- YD/T 6925-2026《人工智能 关键基础技术 智能体基础技术能力要求》及同系列 5 项行业标准（2026-12-01 实施）
- AIIA/T 0290-2026《智能助理智能体（Claw）技术和应用要求 第1部分 产品可信能力》（MCP 管理、技能管理、权限管理）
