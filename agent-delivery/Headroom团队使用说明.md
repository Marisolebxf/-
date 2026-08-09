# Headroom 团队使用说明

> **给谁看**：全体 Cursor 使用者（前端 / 后端 / 算法 / 数据 / QA / 协调等）  
> **做什么**：省 token、拉长有效上下文——压缩大日志、检索结果、工具输出  
> **详细技术说明**：[`headroom-mcp-usage-guide.md`](./headroom-mcp-usage-guide.md)  
> **配置模板**：编排仓根目录 [`.cursor/mcp.json.example`](../.cursor/mcp.json.example)  
> **上游**：https://github.com/headroomlabs-ai/headroom  

---

## 0. 先分清三样东西

| 工具 | 作用 | 是否必装 |
|------|------|----------|
| **task-registry MCP** | 查任务 / 认领 / 改状态（调度） | **必装**（团队已有） |
| **Headroom** | 压缩**进模型的上下文** | **可选**，强烈建议长会话 / 联调角色装 |
| **Ponytail** | 约束**写出的代码量**（懒阶梯） | coding 派单已有强度行；见 `ponytail-usage.md` |

Headroom **不是**任务调度器，也**不能**替代必读全文（USM / Design / 血缘矩阵等）。

---

## 1. 推荐接入方式（两档）

| 档位 | 适合谁 | 做什么 |
|------|--------|--------|
| **A. 仅 MCP（先试点）** | 改不动 Cursor Base URL、或只想按需压缩 | 挂 `headroom mcp serve`，大输出时调 `headroom_compress` |
| **B. MCP + Proxy（推荐完整）** | Base URL 能改、愿意本机开 Proxy | 自动压 LLM 流量 + 仍可按需压缩 |

当前团队策略：**每人本机挂载**，不强制写进公共 `mcp.json`；模板见 `mcp.json.example`。

---

## 2. 安装（一次性，约 5 分钟）

需要 **Python 3.10+**。

### Windows（PowerShell）

```powershell
pip install "headroom-ai[proxy]"
where.exe headroom
headroom --help
```

`where.exe` 无输出时：把  
`%LOCALAPPDATA%\Programs\Python\Python312\Scripts`  
加入用户 PATH，或下面 MCP 里改用绝对路径。

### macOS（终端）

```bash
pip3 install "headroom-ai[proxy]"
# 或：uv tool install "headroom-ai[proxy]"
which headroom
headroom --help
```

PATH 常见位置：`~/.local/bin`、`/opt/homebrew/bin`。Cursor 拉起 MCP 时可能读不到 shell PATH，**优先在 MCP 配置里写绝对路径**。

---

## 3. 挂上 MCP（必做）

### 3.1 配置放哪

任选其一（不要重复挂两份）：

1. **Cursor User MCP**（推荐，不污染仓库）：Settings → MCP → 添加 server  
2. **项目** `gkx-orchestration/.cursor/mcp.json`：从 `mcp.json.example` 复制后本地改（**勿提交本机绝对路径**）

同时保留 **task-registry**（调度）+ **headroom**（压缩）。

### 3.2 仅 MCP（档位 A）

```json
"headroom": {
  "type": "stdio",
  "command": "headroom",
  "args": ["mcp", "serve"]
}
```

### 3.3 MCP + Proxy（档位 B）

```json
"headroom": {
  "type": "stdio",
  "command": "headroom",
  "args": ["mcp", "serve", "--proxy-url", "http://127.0.0.1:8787"]
}
```

`command` 找不到时改成绝对路径，例如：

- Win：`C:\\Users\\你\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\headroom.exe`
- Mac：`/Users/你/.local/bin/headroom`

保存后 **重启 Cursor**，打开 MCP 面板，确认：

- `task-registry` → 约 **10** 个工具，状态 Ready  
- `headroom` → **3** 个工具（`headroom_compress` / `headroom_retrieve` / `headroom_stats`），状态 Ready  

---

## 4. 启 Proxy（仅档位 B）

另开终端，**保持不关**：

```powershell
headroom wrap cursor
```

终端会打印 Cursor 要用的 Base URL，形如：

```text
http://127.0.0.1:8787/p/<你的用户名>/v1
```

然后在 Cursor：

1. Settings → **Models**  
2. 填好 **OpenAI API Key**（真实 key）  
3. 打开 **Override OpenAI Base URL**  
4. 粘贴上一步打印的 URL（不要用文档里的占位符瞎猜）  
5. 重启 Cursor  

Dashboard（可选）：浏览器打开 `http://127.0.0.1:8787/dashboard` 看是否有请求。

**注意**：Override 打开后，走 OpenAI 协议的请求会进本机 Proxy；要用 Cursor 自带云端模型时，先关掉 Override。

若 Base URL **改不动**：先用档位 A；部分 Cursor 版本有 UI bug，可回退一小版本后再试档位 B（下载页：https://cursor.com/download ）。

---

## 5. 日常怎么用

### 5.1 自动（档位 B）

Proxy 开着且 Base URL 指对时：**不用记命令**，大段上下文会在进模型前被压缩。

### 5.2 按需（档位 A / B 都可用）

在 Agent 对话里对大输出说即可，例如：

- 「把这段 grep / 日志用 `headroom_compress` 压一下」  
- 「用刚才的 hash 做 `headroom_retrieve`，只看和 XXX 相关的行」  
- 「调一下 `headroom_stats` 看本会话省了多少」

| 工具 | 何时用 |
|------|--------|
| `headroom_compress` | 日志、检索、大 JSON、长工具输出 |
| `headroom_retrieve` | 压缩后还要看原文细节（用返回的 hash） |
| `headroom_stats` | 看节省量；档位 B 还可看到 proxy 信息 |

压缩结果有时效：MCP 本地约 **1 小时**，Proxy 缓存约 **5 分钟**；过期需重新压缩。

---

## 6. 验收（装完勾一遍）

- [ ] `where.exe headroom` / `which headroom` 有路径  
- [ ] MCP 面板：`headroom` Ready + 3 工具；`task-registry` Ready  
- [ ] （档位 A）对话里 `headroom_compress` 能返回 `hash` / `savings_percent`  
- [ ] （档位 B）`headroom wrap cursor` 常驻；Base URL 已按打印配置；dashboard 有流量；`headroom_stats` 可见 proxy  

---

## 7. 如何落实到派单（coordinator）

> **手册真源**：[`智能体编排与派单手册.md`](./智能体编排与派单手册.md) **§9.0b**（推荐行，非硬闸）+ §10.1/§10.2 软检查。

### 7.1 与 Ponytail 对照

| | Ponytail（§9.0） | Headroom（§9.0b） |
|--|------------------|-------------------|
| `/goal` | coding **必带**强度行，缺则拒派 | **推荐** `上下文：` 行，缺不拒派 |
| handoff | coding 必有 `ponytail:`，缺则 needs-revision | 可选 `headroom: mcp\|proxy\|skip`，缺不拒收 |

### 7.2 `/goal` 复制即用

**coding / 联调 / 大日志**（贴在强度行后）：

```text
上下文：headroom 推荐（MCP 按需 compress 大日志/检索；有 Proxy 则保持常驻）。禁止用压缩替代必读规范全文。未挂载可跳过并在 handoff 注明 `headroom: skip`。
```

**定义类**（ux / product / architect / doc）：

```text
上下文：headroom 可选。USM/TRACE/Wireframe/Design/血缘矩阵必须读原文，禁止 compress 代替精读。
```

### 7.3 何时写、何时省略

| 任务 | Headroom 行 |
|------|-------------|
| 联调、CI/K8s 日志、大 grep、大 JSON | ✅ 建议写 |
| 日常小改、单文件 bugfix | 可省略 |
| 门1/门3、USM、PDR、会签 | ✅ 写「禁止压缩代替精读」 |

### 7.4 禁止

- 未挂载 Headroom → 拒派  
- 规则里强制每步 `headroom_compress`  
- 用压缩摘要代替必读规范全文  

---

## 8. 红线（违反勿用）

1. 不要在规则里强制「每一步都 compress」——MCP 调用本身也占上下文。  
2. 产品定义 / 会签 / 必读规范 **禁止**用压缩摘要代替读原文。  
3. 不要把 API Key、`.env`、密码写进仓内配置或群聊截图。  
4. 不要用 Headroom 替代 `task-registry` 做派单 / 改状态。  
5. coding 派单强度行仍按 Ponytail，Headroom 管不了代码量。  

---

## 9. 常见问题

| 问题 | 处理 |
|------|------|
| MCP 面板没有 headroom | 检查配置 → 绝对路径 → 重启 Cursor；确认打开的是编排仓或已配 User MCP |
| `No such file` / 起不来 | Win `where.exe headroom`，Mac `which headroom`，MCP `command` 改绝对路径 |
| Base URL 改不了 | 先填 OpenAI API Key；仍不行用档位 A，或回退 Cursor 版本 |
| Proxy 起来又自动升 Cursor | Settings 搜 `update.mode` → `none`；并处理 `%LOCALAPPDATA%\cursor-updater`（只读/删除） |
| 想临时不用 Proxy | 关 Override Base URL，并可 `Ctrl+C` 停掉 wrap；MCP 仍可按需压缩 |

---

## 10. 仓库路径速查

| 文件 | 用途 |
|------|------|
| `agent-delivery/Headroom团队使用说明.md` | **本文**（团队宣贯 / 上手 / 派单落地表） |
| `agent-delivery/智能体编排与派单手册.md` §9.0b | 派单条款真源 |
| `agent-delivery/headroom-mcp-usage-guide.md` | 更细的安装与排障 |
| `.cursor/mcp.json.example` | MCP 配置模板 |
| `agent-delivery/ponytail-usage.md` | 写代码的懒模式 |
| `agent-delivery/task-mcp-usage-guide.md` | 任务注册表 MCP |

问题反馈：先贴 MCP 面板截图 + `headroom --help` 是否成功 + 本机 OS（Win/Mac），找协调人协助。
