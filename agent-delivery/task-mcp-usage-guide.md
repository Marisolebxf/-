# Task Registry MCP 使用说明

> 本文档介绍如何通过 MCP 工具操作任务注册表（`task-registry.yaml`），避免直接读写 YAML 文件带来的 token 消耗和并发冲突问题。

---

## 一、背景

任务注册表 `task-registry.yaml` 是团队的核心任务数据库，记录了所有任务的状态、依赖、负责人等信息。之前直接读写该文件存在以下问题：

- **token 消耗大**：YAML 文件随任务增多逐渐庞大，AI 每次加载都要消耗大量 token
- **并发冲突**：多人同时操作 YAML 文件可能导致数据丢失
- **操作不统一**：团队成员通过不同方式修改，流程混乱

**解决方案**：封装为 MCP 服务器，提供 7 个工具化接口，AI 通过工具调用完成操作，按需查询、增量更新，无需加载整个文件。

---

## 二、安装配置

### 2.1 确保配置文件存在

检查以下两个文件是否存在：

| 文件 | 用途 |
|------|------|
| `.cursor/mcp.json` | 注册 MCP 服务器，让 Cursor 识别 |
| `.cursorignore` | 屏蔽 AI 直接读取 YAML 文件（已在其中添加 `agent-delivery/task-registry.yaml`） |

### 2.2 验证 MCP 服务器已加载

1. 打开 Cursor
2. 打开项目根目录 `gkx-orchestration`
3. 点击右下角或菜单栏的 **MCP 面板**（插头图标）
4. 确认列表中显示 **`task-registry`**，且有 **9 个工具**：
   - `task-query`
   - `task-get`
   - `task-summary`
   - `task-update-status`
   - `task-claim`
   - `task-set-blocked`
   - `task-update-fields`
   - `task-review`（自动验收单个任务）
   - `task-review-batch`（批量自动验收）

如果未显示，重启 Cursor 后重试。若仍不显示，检查 `.cursor/mcp.json` 内容是否正确：

```json
{
  "mcpServers": {
    "task-registry": {
      "type": "stdio",
      "command": "node",
      "args": ["scripts/task-mcp-server.mjs"]
    }
  }
}
```

### 2.3 前置依赖

- Node.js 18+
- 无需安装额外 npm 包（仅使用 Node.js 内置模块）

---

## 三、工具说明与使用示例

### 3.1 task-query — 查询任务列表

按模块名、状态、Agent、Epic 等条件筛选任务，支持模块名模糊搜索。

**常用场景**：

```
查询"企业"相关的所有任务
  → 调用 task-query, module="企业"

查询所有 ready 状态、待认领的任务
  → 调用 task-query, status="ready"

查询某个 Agent 的所有进行中任务
  → 调用 task-query, agent="api-agent", status="in_progress"

查看完整信息（含 blocked_by, claimed_by, note 等）
  → 调用 task-query, module="政策", fields="full"
```

**参数说明**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `module` | 否 | 模块名模糊搜索，如"企业"、"政策"、"科技" |
| `status` | 否 | 按状态筛选：backlog/ready/claimed/in_progress/review/done/blocked |
| `agent` | 否 | 按 Agent 角色筛选：api-agent/frontend-agent/data-agent 等 |
| `epic` | 否 | 按 Epic 精确匹配：E-ENT-PROTOTYPE |
| `sprint` | 否 | 按 Sprint ID 筛选 |
| `limit` | 否 | 最大返回条数，默认 20 |
| `fields` | 否 | `summary`（精简）或 `full`（完整），默认 summary |

### 3.2 task-get — 查询单个任务

按任务 ID 获取完整信息。

```
查看任务 E-INNOV-M1-L03 的详情
  → 调用 task-get, id="E-INNOV-M1-L03"
```

### 3.3 task-summary — 任务概览统计

按状态、Epic、Agent 聚合统计，不返回具体任务列表。

```
查看整体概览
  → 调用 task-summary

查看"企业"模块的概览
  → 调用 task-summary, module="企业"
```

返回：各状态数量、各 Epic 数量、各 Agent 数量、待认领任务列表。

### 3.4 task-update-status — 更新任务状态

更新任务状态流转，支持追加备注。

```
将任务标记为 in_progress
  → 调用 task-update-status, id="E-ENT-PROTOTYPE-L01", status="in_progress"

任务完成
  → 调用 task-update-status, id="E-ENT-PROTOTYPE-L01", status="done"

任务需要修改
  → 调用 task-update-status, id="E-ENT-PROTOTYPE-L01", status="needs-revision", note="UI 样式需调整"
```

**状态流转图**：

```
backlog → ready → claimed → in_progress → testing → ready_to_sign → done
                          ↘              ↙            ↑
                        blocked → needs-revision    (auto-verify)
```

| 状态 | 语义 |
|------|------|
| `backlog` | 待排期 |
| `ready` | 依赖满足，待认领 |
| `claimed` | 已认领，待开工 |
| `in_progress` | 开发中 |
| `testing` | 代码已交付，自动测试进行中或已通过 |
| `ready_to_sign` | 自动验收通过，只差监管人签收 |
| `review` | **legacy 汇总态**，新任务优先用 testing/ready_to_sign；用 `review_phase` 子状态分类 |
| `done` | 完成 |
| `blocked` | 阻塞 |
| `needs-revision` | 需返工 |

**review 子状态（review_phase 字段）**：

| review_phase | 语义 |
|--------------|------|
| `pending_test` | 待测试/CI 验证 |
| `pending_sign` | 已测试通过，待监管人签收 |
| `pending_business` | 待业务口径/甲方确认 |
| `blocked_by_dep` | 依赖未满足 |

### 3.5 task-claim — 认领任务

设置任务负责人和监管人，自动锁定防止重复认领。

```
认领任务，自己负责
  → 调用 task-claim, id="E-ENT-PROTOTYPE-L01", claimed_by="human:张三"

认领任务，指定监管人
  → 调用 task-claim, id="E-ENT-PROTOTYPE-L01", claimed_by="human:张三", supervised_by="human:李四"

自定义锁定时间
  → 调用 task-claim, id="E-ENT-PROTOTYPE-L01", claimed_by="human:张三", lock_hours=8
```

**注意**：认领时会自动将 `backlog`/`ready` 状态的任务设为 `claimed`。

### 3.6 task-set-blocked — 设置阻塞

将任务标记为阻塞，记录原因。

```
标记阻塞，记录原因
  → 调用 task-set-blocked, id="E-ENT-PROTOTYPE-L01", blocked_by="依赖 E-INNOV-M1-L02 未完成"
```

### 3.7 task-update-fields — 更新附加字段

更新证据、绩效、成本等附加字段，不改状态（handoff 时使用）。

```
填写 handoff 证据
  → 调用 task-update-fields, id="E-ENT-PROTOTYPE-L01", evidence="agent-handoffs/E-ENT-PROTOTYPE-L01.md"

填写绩效信息
  → 调用 task-update-fields, id="E-ENT-PROTOTYPE-L01", effort_points="5", difficulty="L"

填写成本信息
  → 调用 task-update-fields, id="E-ENT-PROTOTYPE-L01", actual_tokens=15000, model_used="claude-sonnet-4.5", actual_cost=0.75
```

### 3.8 task-review — 自动验收单个任务

对单个任务执行自动验收检查，返回通过/失败报告。

**检查项**：
1. handoff 文件存在（`agent-handoffs/` 下含任务 ID 的 `.md`）
2. DoD 列表非空（`definition_of_done` 至少 1 条）
3. cost 四字段回填（`actual_tokens` / `model_used` / `actual_cost` / `cost_warn`）
4. 架构合规自检（note 或 handoff 含"架构合规"关键词）
5. `supervised_by` 已设置

```
验收单个任务
  → 调用 task-review, id="E-ENT-PROTOTYPE-L01"
```

### 3.9 task-review-batch — 批量自动验收

对所有 `review` / `testing` / `in_progress` 状态的任务批量执行自动验收。

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `auto_fix` | 否 | `true` 时通过后自动推进状态（默认 `false`，仅出报告） |
| `module` | 否 | 仅检查某模块（如"企业"） |
| `target_status` | 否 | `auto_fix=true` 时推进到的目标状态：`ready_to_sign`（默认，半自动）或 `done`（全自动） |

```
查看企业模块所有待验收任务的报告
  → 调用 task-review-batch, module="企业"

半自动：通过后推进到 ready_to_sign（等监管人签收）
  → 调用 task-review-batch, module="企业", auto_fix=true, target_status="ready_to_sign"

全自动：通过即 done（仅限 demo 仓 + CI 全绿的非关键任务）
  → 调用 task-review-batch, module="企业", auto_fix=true, target_status="done"
```

---

## 四、典型工作流程

### 4.1 开发人员：开始新任务

1. 查询待认领任务：`task-query status="ready"`
2. 认领任务：`task-claim id="XXX" claimed_by="human:张三"`
3. 开始开发，更新状态：`task-update-status id="XXX" status="in_progress"`
4. 开发完成，提交 review：`task-update-status id="XXX" status="review"`
5. 填写 handoff 和成本：`task-update-fields id="XXX" evidence="...", actual_tokens=..., ...`
6. 最终确认完成：`task-update-status id="XXX" status="done"`

### 4.2 Coordinator：日常派单

1. 查看概览：`task-summary`
2. 筛选待派单任务：`task-query status="ready"`
3. 查看单个任务详情：`task-get id="XXX"`
4. 认领并派发：`task-claim id="XXX" claimed_by="human:张三" supervised_by="human:李四"`

### 4.3 PM：查看进度

1. 查看整体进度：`task-summary`
2. 按模块查看：`task-summary module="企业"`
3. 查看某个 Epic 的所有任务：`task-query epic="E-ENT-PROTOTYPE"`

---

## 五、注意事项

### 5.1 禁止直接操作 YAML

- **禁止**直接读取或修改 `agent-delivery/task-registry.yaml`
- 该文件已在 `.cursorignore` 中屏蔽，AI 无法直接读取
- 所有操作必须通过上述 MCP 工具完成

### 5.2 并发安全

- MCP 服务器使用文件锁机制（基于 mkdir 原子操作），保证并发安全
- 如果遇到锁超时（5秒），稍后重试即可
- 锁文件为 `task-registry.yaml.lock`，正常情况下应自动清理

### 5.3 模块名搜索

- `task-query` 的 `module` 参数支持模糊搜索
- 匹配范围：Epic 名称、任务标题、任务 ID
- 示例：`module="企业"` 可匹配 Epic 名为"企业原型"、"企业Scrum"及其下的所有任务

### 5.4 故障排查

| 现象 | 可能原因 | 解决 |
|------|---------|------|
| MCP 面板未显示 `task-registry` | 未配置 `.cursor/mcp.json` | 检查文件是否存在，重启 Cursor |
| 工具调用返回错误 | MCP 服务器未启动 | 查看 Cursor 的 MCP 日志 |
| 锁超时错误 | 另一个进程正在操作 YAML | 稍后重试，或检查 `.lock` 文件残留 |
| 找不到任务 | 任务 ID 或模块名不正确 | 先用 `task-query` 搜索确认 |

### 5.5 MCP 服务器日志

MCP 服务器的日志输出到 Cursor 的 MCP 面板，可查看启动信息和错误堆栈。

---

## 六、自动验收（review-agent）

新增 `task-review` 和 `task-review-batch` 工具，可自动检查 handoff 的机械性完整性。

### 6.1 检查内容

| 检查项 | 说明 |
|--------|------|
| handoff 文件存在 | 在 `agent-handoffs/` 下找到对应任务 ID 的 .md 文件 |
| 模板章节完整 | 范围与实现 / 偏离 / 产物清单 / 验收证据 / 架构合规自检 / Cost 回填 |
| 架构合规自检 | 7 条是否逐条 ✅ |
| Cost 回填 | handoff 和 registry 中 `actual_tokens`/`model_used`/`actual_cost`/`cost_warn` 是否已填 |
| PR/CI 链接 | handoff 中是否包含 github/gitlab/CI 相关链接 |
| 偏离说明 | handoff 中是否有偏离说明 |

### 6.2 使用方式

```
# 单个任务验收
  → 调用 task-review, id="ENT-MOD-EVAL-V2-LUMEN-S3"

# 批量验收所有 review 任务
  → 调用 task-review-batch

# 批量验收 + 自动标记通过的任务
  → 调用 task-review-batch, auto_fix=true

# 只验收某个模块的任务
  → 调用 task-review-batch, module="企业"
```

### 6.3 验收流程

```
review → [task-review] → review-passed → [人工确认] → done
                      ↘ needs-revision → [修复] → review
```

- **自动检查通过** → 状态标记为 `review-passed`，人只需做**业务判断**
- **自动检查不通过** → 附缺失清单，需要修复后重新提交 review
- **人确认业务无误** → `task-update-status` → `done`

---

## 七、参考

- MCP 服务器源码：`scripts/task-mcp-server.mjs`
- 任务注册表操作库：`scripts/lib/task-registry-lib.mjs`
- 团队公约 §7：`.cursor/rules/00-team-constitution.mdc`
- Coordinator 职责：`.cursor/rules/coordinator.mdc`