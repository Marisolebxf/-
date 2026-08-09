# Ponytail 使用说明（编码人员 + coding agent）

> **读者**：前端 / 后端 / 算法 / DevOps / QA（写测）工程师，以及 `frontend` / `ui` / `api` / `algorithm` / `devops` / `qa` agent。  
> **不读者主责**：PM / product / coordinator / architect / doc / ux（定义与派单不以缩代码为目标）。  
> **真源规则**：`.cursor/rules/ponytail.mdc`（编排仓；业务仓有同步副本）  
> **上游项目**：[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)（MIT）

---

## 1. 一句话

Ponytail = **写最少够用的代码**：先读懂再爬「懒阶梯」，不砍安全 / 校验 / 可观测 / 团队铁律必交付件。

团队默认：**full**。公约（D8/D9/D10、调用链、handoff）**永远优先于**「再少写几行」。

---

## 2. 重要：我们用的是 Cursor，不是 Claude Code 插件档

| 环境 | `/ponytail …` 斜杠指令 | 实际用法 |
|------|------------------------|----------|
| **Cursor（国科信主战场）** | **无官方插件档**；规则始终生效（`alwaysApply`） | 对话里用下表「Cursor 话术」；或调用项目 Skill（见 §4） |
| Claude Code / Codex / 等 | 上游插件支持 `/ponytail`、`/ponytail-review` | 可按上游 README 安装后用原生命令 |

因此：聊天里直接打 `/ponytail full` **不一定**会被 Cursor 识别成模式切换；**请用下面等价话术，或调用 Skill。**

---

## 3. 模式与指令对照（给人对 agent 说）

### 3.1 强度档位

| 意图 | 上游写法（Claude Code 等） | **Cursor / 本仓推荐话术**（复制即用） | 何时用 |
|------|---------------------------|--------------------------------------|--------|
| 标准（日常首选） | `/ponytail full` | `按 ponytail full` / `ponytail 标准模式` | 日常 feature、bugfix、demo→lumen 复刻 |
| 轻度精简 | `/ponytail lite` | `按 ponytail lite`：实现所求，并**一行**点出更懒替代方案供我选 | 大型业务首版、需要适度分层 / 契约骨架 |
| 极限极简 | `/ponytail ultra` | `按 ponytail ultra`（慎用） | 明显过度设计、大段样板待删；**易过度删逻辑** |
| 临时关闭 | `/ponytail off` | `本次关闭 ponytail` / `normal mode` / `stop ponytail` | 架构/OpenAPI/ADS 首版闭合、联调攻坚、按规范必须铺全骨架时 |
| 过度工程审查 | `/ponytail-review` | `ponytail-review：只审过度工程，给删除清单` | PR 前 / 自检 diff；**不改代码，只列可删项** |
| 查看帮助 | `/ponytail-help` | `ponytail-help` 或打开本文 | 新人 / 忘了档位时 |

### 3.2 各档位行为（与上游一致）

| 档位 | 行为 |
|------|------|
| **full**（默认） | 强制懒阶梯：YAGNI → 仓内复用 → stdlib → 原生能力 → 已装依赖 → 一行 → 最小实现。最短有效 diff。 |
| **lite** | 照做所求；另用**一行**说明更懒的替代，由人决定是否换成懒版。 |
| **ultra** | 先质疑需求是否该做；优先删除；先交一行解，并挑战其余范围。 |
| **off** | 本会话不再主动压代码量；仍须遵守架构铁律与 Design/血缘。 |

档位在**当前会话**内保持，直到你改口或新开会话（新会话回到规则默认 = full）。

### 3.3 懒阶梯（写代码前）

1. 要不要做？（YAGNI）  
2. 仓里有没有现成的？  
3. 标准库？  
4. 平台原生？（如原生控件、CSS、DB 约束）  
5. 已安装依赖？  
6. 能否一行？  
7. 否则：最小可工作实现  

**先读懂再爬阶梯。** 修 bug = 修根因，并扫所有 caller。

### 3.4 永远不要「懒」掉的（含 GKX）

- 信任边界校验、防丢数据错误处理、安全、无障碍  
- 架构铁律：前端 → Java → Python `/internal/*`；Nebula；可观测埋点  
- D8 Design / D10 交互 / D9 指标 8 件套与就绪度角标 / handoff  
- demo→lumen：对齐已评审页，禁止另起一套「更简 UI」

---

## 4. Cursor 里怎么用（编码人员操作）

1. **打开含编排仓或已同步 `ponytail.mdc` 的业务仓 / workspace**（单开业务仓时依赖仓内副本）。  
2. **默认不必说任何话**：规则已始终生效 ≈ **full**。  
3. **要切换强度**：在任务开头贴一句 §3.1 的 Cursor 话术。  
4. **审查过度工程**：说 `ponytail-review`，或调用 Skill `ponytail-review`（见下）。  
5. **帮助**：说 `ponytail-help`，或打开本文。

### 项目 Skill（编排仓）

路径：`gkx-orchestration/.cursor/skills/`

| Skill | 作用 |
|-------|------|
| `ponytail` | 设定 lite / full / ultra / off（参数写在对话里） |
| `ponytail-review` | 只产出过度工程删除清单 |
| `ponytail-help` | 打印本说明摘要 |

在 Cursor Agent 中通过 Skills / 斜杠菜单选用（以当前 Cursor 版本 UI 为准）；若菜单无项，直接把话术贴进对话即可。

### 派单给 coding agent 时（监管人 / coordinator）— **硬约束**

真源：`智能体编排与派单手册.md` **§9.0** + `coordinator.mdc` 派单铁律 **1b**。

派 ui / frontend / api / algorithm / devops / qa / integration（及 data 写 SQL/ETL）时，`/goal` **必须**含强度行，**缺则拒派**：

```text
强度：ponytail full（默认）。禁止用 YAGNI 跳过 D8/D9/D10 与可观测。
```

特殊任务：

```text
强度：ponytail lite — OpenAPI 与聚合契约先闭合，再压实现。
```

```text
完成后跑 ponytail-review，只贴删除清单，先别改。
```

收单：coding 任务 handoff 须有 `ponytail:` 行（见 `templates/handoff-template.md`）；缺则 `needs-revision`。定义类 agent **不要**写强度行压文档。

---

## 5. 场景速查

| 场景 | 建议 |
|------|------|
| 日常功能 / 修 bug | **full** |
| 新模块契约、ADS 表、图谱对接首版 | 先 **lite** 或短暂 **off**，闭合后再 **full** 收 diff |
| 明显过度封装 / 样板成灾 | **ultra** 或 **ponytail-review** 后按清单删 |
| 联调卡死、必须铺全路径 | **off** 到绿，再考虑压缩 |
| USM / Wireframe / 产品定义 | **不要**对定义 agent 开 ponytail；完整性优先 |
| PR / 签收前 | **ponytail-review**（复杂度）+ 常规正确性 / 安全审查（另做） |

---

## 6. 审查格式（`ponytail-review`）

一行一条，只谈可删复杂度：

```text
path:L12-38: yagni: 单实现工厂。内联到调用方。
path:L4: native: 为日期选型装了第三方。改用原生 input type=date / dayjs（仓内已有）。
net: -N lines possible.
```

标签：`delete:` / `stdlib:` / `native:` / `yagni:` / `shrink:`  
**不做**正确性 / 安全 / 性能审查；无事可删则回复：`Lean already. Ship.`

---

## 7. 与 Headroom 的分工（可选配套）

| | **Ponytail**（本文） | **Headroom** |
|--|----------------------|--------------|
| 管什么 | **写出的代码量**（懒阶梯） | **进模型的上下文**（Proxy + MCP 压缩） |
| 是否强制 | coding 派单必带强度行 | 全员可选，本地挂载 |
| 说明 | 本文 | `agent-delivery/headroom-mcp-usage-guide.md` |

二者互补；官方亦推荐搭配。勿用 Headroom 替代必读全文，勿用 Ponytail 砍掉公约必交付件。

---

## 8. 维护

| 动作 | 命令 / 路径 |
|------|-------------|
| 改规则真源 | 编辑 `gkx-orchestration/.cursor/rules/ponytail.mdc` |
| 同步到业务仓 | `powershell -NoProfile -File scripts/sync-ponytail.ps1` |
| 上游对照 | https://github.com/DietrichGebert/ponytail |

---

## 9. 给 coding agent 的硬约束（摘要）

1. 默认 **full**；用户明确 lite / ultra / off 时切换。  
2. GKX 护栏 > 懒阶梯。  
3. 用户说 `ponytail-review` → 只列删除清单，不擅自大改。  
4. 用户说 `ponytail-help` → 输出 §3 对照表，不改模式、不写代码。  
5. 非编码任务（纯文档 / 派单 / 产品定义）→ 不要主动压篇幅到损害完整性。
