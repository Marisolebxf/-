# 瘦工作区（降 Token）

> **不要默认打开** 上级目录的 `gkx-lumen.code-workspace`（16 根，已不含 dataease）。  
> 多根会把各仓 `CLAUDE.md` / `AGENTS.md` 全部注入 always-applied，单轮可白烧 ~15k tokens。

## 怎么用

Cursor / VS Code：`File → Open Workspace from File` → 选本目录下对应文件。

| 文件 | 适用任务 | 打开的 folder |
|------|----------|---------------|
| `orch-only.code-workspace` | 派单 / 文档 / 编排 | 仅主仓 |
| `fe-science.code-workspace` | 科技展示前端 | 主仓 + science-pc + demo-ui-science |
| `fe-topic.code-workspace` | 专题前端 | 主仓 + topic + demo-ui-topic |
| `java-api.code-workspace` | Java API | 主仓 + lumen-svc-platform |
| `algo-py.code-workspace` | Python 算法 / ETL | 主仓 + algo 仓 + etl |
| `admin-ui.code-workspace` | 管理后台 UI | 主仓 + lumen-ui-admin（需要对照再临时加 demo） |
| `../gkx-lumen.code-workspace` | 跨仓大重构 / 检索 | **全量 16 根，慎用** |

## 命名约定

`folders[].name` **只用短英文 id**（如 `gkx-orchestration`），禁止括号、斜杠、长中文说明。  
否则 Ctrl+Click / 部分工具会把显示名拼进路径导致「Unable to open …」。

## 相关

- `.cursorignore`：各仓根目录（编排仓已有）
- `agent-delivery/budget-estimate.md` §6 / §6.1
