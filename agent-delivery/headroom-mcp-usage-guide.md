# Headroom MCP + Proxy 使用说明

> **读者**：全员（尤其长会话 / 大日志 / 多工具输出的 coding 与联调角色）；coordinator 做工具宣贯时可引用本文。  
> **上游**： [headroomlabs-ai/headroom](https://github.com/headroomlabs-ai/headroom)（Apache 2.0）  
> **配置模板**：`.cursor/mcp.json.example`  
> **调度 MCP**：见 `task-mcp-usage-guide.md`（Headroom **不是**任务调度器）

---

## 1. 一句话

Headroom = **压缩进模型的上下文**（工具输出、日志、检索结果、HTTP 流量），降低 token / 拉长有效上下文窗口。

| 能力 | 做什么 | 本仓策略 |
|------|--------|----------|
| **Proxy** | HTTP 层自动压缩进出 LLM 的流量 | 推荐：本机 `127.0.0.1:8787` 常驻 |
| **MCP** | 按需 `headroom_compress` / `headroom_retrieve` / `headroom_stats` | 可选：每人本地挂载，不写进全员强制 `mcp.json` |

### 与 Ponytail / task-registry 的边界

| 工具 | 管什么 | 不管什么 |
|------|--------|----------|
| **Headroom** | 进模型的上下文体积 | 写多少代码、派哪张单 |
| **Ponytail** | 写出的代码量（懒阶梯） | 上下文压缩；见 `ponytail-usage.md` |
| **task-registry MCP** | 任务查询 / 认领 / 状态机 | token 压缩 |

官方亦推荐 Headroom + Ponytail 搭配使用；二者互补，勿互相替代。

---

## 2. 团队落地策略

1. **默认试点（推荐先做）**：**仅 MCP**——`headroom mcp serve`，按需压缩大日志 / 检索结果；**不**改 Cursor Base URL、**不**要求常驻 Proxy。适合 Cursor「Override OpenAI Base URL」改不动 / 有 bug 时。  
2. **进阶（可选）**：MCP + Proxy（全流量自动压）。需本机 `headroom proxy` / `headroom wrap cursor`，并把 Cursor OpenAI Base URL 指到 Proxy（如 `http://127.0.0.1:8787/p/<user>/v1`）。  
3. **范围**：仓内文档 / 模板 + **每人本地挂载**（多机 PATH / Python 环境不一致）。  
4. **仓内强制项**：`.cursor/mcp.json` 至少保证可移植 `task-registry`；`headroom` 为可选本地挂载（见 `mcp.json.example`）。  
5. **Proxy**：先本机 `127.0.0.1`，不做团队共享远端 Proxy。

---

## 3. 安装

Python 3.10+。按本机 OS 选一节；安装目标相同：`headroom` 在 PATH 上可执行。

### 3.1 Windows + PowerShell

```powershell
# 推荐：Proxy + MCP
pip install "headroom-ai[proxy]"

# 或用 uv 装到全局 PATH（避免 MCP 找不到命令）
uv tool install "headroom-ai[proxy]"
```

确认 CLI 可见：

```powershell
where.exe headroom
headroom --help
```

若 `where.exe` 无输出：把 Python `Scripts` 目录加入用户 PATH，或在 MCP 配置里把 `command` 写成 `where.exe headroom` 得到的**绝对路径**。

### 3.2 macOS（zsh / bash）

前置：本机已有 Python 3.10+（Homebrew 示例：`brew install python@3.12`）。Apple Silicon / Intel 均可。

```bash
# 推荐：Proxy + MCP
pip3 install "headroom-ai[proxy]"
# 若用 venv：先 source .venv/bin/activate 再 pip install

# 或用 uv 装到用户工具 PATH（Cursor 拉起 MCP 时更稳）
# brew install uv   # 尚未安装时
uv tool install "headroom-ai[proxy]"
```

确认 CLI 可见：

```bash
which headroom
headroom --help
```

常见 PATH 位置（`which` 无输出时逐个查）：

| 安装方式 | 典型路径 |
|----------|----------|
| `uv tool install` | `~/.local/bin/headroom` |
| Homebrew Python + pip | `/opt/homebrew/bin/headroom`（Apple Silicon）或 `/usr/local/bin/headroom`（Intel） |
| pyenv / 用户 pip | `~/.local/bin/headroom` 或 `$(python3 -m site --user-base)/bin/headroom` |

把缺失目录写入 shell 配置后重开终端：

```bash
# zsh（默认）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

仍不可见时：在 MCP 配置里把 `command` 写成 `which headroom` 的**绝对路径**（Cursor 启动 MCP 时不一定继承你交互式 shell 的 PATH）。

---

## 4. 启动 Proxy（仅进阶 MCP+Proxy；仅 MCP 试点可跳过）

**仅 MCP 试点**：跳过本节，也不要改 Cursor Base URL；可关掉已开的 `headroom wrap cursor`（`Ctrl+C`）。

进阶时另开终端常驻其一（Win / Mac 命令相同）：

```bash
# 默认 :8787
headroom proxy

# 或：启动 Proxy 并打印 Cursor 配置指引（不替你打开 IDE）
headroom wrap cursor
```

### 4.1 环境变量（OpenAI 兼容客户端）

**Windows PowerShell：**

```powershell
$env:OPENAI_BASE_URL = "http://127.0.0.1:8787/v1"
```

**macOS / Linux：**

```bash
export OPENAI_BASE_URL="http://127.0.0.1:8787/v1"
```

### 4.2 Cursor 模型入口

按 `headroom wrap cursor` 打印的说明，把模型侧 OpenAI-compatible **Base URL** 指到 `http://127.0.0.1:8787/v1`（以当次 CLI 输出为准）。改完后重启 Cursor 或重载窗口。macOS 与 Windows 的 Cursor 设置项相同。

---

## 5. 本地挂载 MCP

### 5.1 试点推荐：仅 MCP（无 Proxy）

不改 Cursor Base URL、不必开 `headroom proxy`。复制 `.cursor/mcp.json.example` 或合并如下段：

```json
"headroom": {
  "type": "stdio",
  "command": "headroom",
  "args": ["mcp", "serve"]
}
```

保存后 **重启 Cursor / Reload Window** → MCP 面板应出现 `headroom` 的 3 个工具。大日志 / 长检索后让 agent 调用 `headroom_compress`；需要原文时用返回的 `hash` 调 `headroom_retrieve`。

`command: "headroom"` 仅在 PATH 可见时可用；否则改成绝对路径：

| OS | 查绝对路径 |
|----|------------|
| Windows | `where.exe headroom` |
| macOS | `which headroom` |

Windows 绝对路径示例：

```json
"headroom": {
  "type": "stdio",
  "command": "C:\\Users\\你的用户名\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\headroom.exe",
  "args": ["mcp", "serve"]
}
```

### 5.2 进阶：MCP + Proxy（需能改 Cursor Base URL）

Proxy 常驻且 Cursor Override Base URL 可用时，给 MCP 加上 `--proxy-url`，以便 `retrieve` / `stats` 读 Proxy 缓存：

```json
"headroom": {
  "type": "stdio",
  "command": "headroom",
  "args": ["mcp", "serve", "--proxy-url", "http://127.0.0.1:8787"]
}
```

若使用 `headroom wrap cursor`，以 CLI 打印为准（可能是 `http://127.0.0.1:8787/p/<user>` 形态）；**仅 MCP 试点时不要加这些参数**。

### 5.3 三个工具

| 工具 | 用途 |
|------|------|
| `headroom_compress` | 按需压缩大段文本（grep / 日志 / JSON） |
| `headroom_retrieve` | 按 hash 取回原文（可带 `query` 局部检索） |
| `headroom_stats` | 本会话节省量；Proxy 运行时含 proxy 字段 |

TTL 提示：MCP 本地压缩约 1h；Proxy 缓存约 5min。过期后 `retrieve` 会失败，需重新压缩或重跑工具。

---

## 6. 验收清单

**仅 MCP 试点：**

1. Cursor MCP 面板：`headroom` 显示 **3** 个工具（可与 `task-registry` 的 10 个并存）。  
2. 对话里对大段文本调用 `headroom_compress`，得到 `hash` + `savings_percent`。  
3. 需要细节时用 `hash` 调 `headroom_retrieve`；`headroom_stats` 有压缩次数即可（无 proxy 字段也正常）。

**进阶 MCP+Proxy 另加：** Proxy 常驻、`headroom_stats` 含 proxy 字段、Cursor Base URL 已指向 Proxy。

---

## 7. 红线

1. **禁止**在 Cursor `alwaysApply` 规则里强制每步调用 `headroom_compress`——MCP 往返本身会占上下文，过度调用可能「越压越贵」。  
2. **定义类 / 会签 / 必读全文**（USM、Wireframe、Design、血缘矩阵等）**禁止**用压缩摘要替代原文阅读。  
3. **禁止**把 API Key、`.env`、密码写进仓内 mcp 配置或本说明的示例。  
4. Headroom **不替代** `task-registry` MCP；状态机与派单仍走任务工具。  
5. Headroom **不替代** Ponytail；coding 派单强度行仍按 `ponytail-usage.md`。

---

## 8. 故障排查（简表）

| 现象 | 处理 |
|------|------|
| MCP 启动失败 `No such file` | Win：`where.exe headroom`；Mac：`which headroom` → 改绝对路径，或 `uv tool install "headroom-ai[proxy]"` |
| Mac 终端有 `headroom`、Cursor MCP 起不来 | Cursor 未继承 shell PATH → MCP `command` 改用绝对路径；确认 `~/.local/bin` 等已写入 |
| Proxy not running | 另开终端 `headroom proxy` |
| Entry not found or expired | 重压或缩短会话内依赖；注意 TTL |
| MCP 面板无 headroom | 检查本机 mcp 配置 → 重启 Cursor |
| Cursor 流量未走 Proxy | 核对 Base URL / `wrap cursor` 指引是否已应用 |
| Mac 端口占用 | `lsof -i :8787`；换端口：`headroom proxy --port 8788`，并同步改 MCP `--proxy-url` 与 Cursor Base URL |

---

## 9. 维护

| 动作 | 路径 |
|------|------|
| 改本文 | `agent-delivery/headroom-mcp-usage-guide.md` |
| 改模板 | `.cursor/mcp.json.example` |
| 共享 MCP 池登记 | `team-collaboration-playbook.md` §4.4 |
| 上游文档 | https://headroomlabs-ai.github.io/headroom/mcp/ |
