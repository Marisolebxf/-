# 飞书私信 MCP（第一期 · 出站通知）

> 给 Cursor agent 用：按花名册真名给项目成员发飞书私信。  
> **不是聊天室**。人回复不会自动回到 Cursor。  
> 实现：`scripts/feishu-im-mcp-server.mjs` · 护栏：`scripts/lib/feishu-im-guard.mjs`

## 能做什么

| 工具 | 作用 |
|------|------|
| `im-resolve` | 查可发成员；不发消息 |
| `im-send` | 发给指定 `human:姓名`，必须带 `task_id` |
| `im-notify-task` | 按任务 `supervised_by` / `claimed_by`（仅真人）发 |

## 护栏

- 收件人 = `team-roster.yaml` ∩ `feishu/feishu-user-map.yaml`（有 `open_id`）
- **禁止**传入 `open_id`；禁止给甲方发
- **必须**有登记表 `task_id`；任务不存在则拒发
- 同人同任务 **30 分钟**内去重（记录在 `agent-delivery/_tmp/feishu-im-rate.json`）
- `claimed_by` 为 `agent:*` 时 `im-notify-task` 不会发给机器人

## 配置

`.cursor/mcp.json`（及 `mcp.json.example`）增加：

```json
"feishu-im": {
  "type": "stdio",
  "command": "node",
  "args": ["scripts/feishu-im-mcp-server.mjs"]
}
```

本机 `.env` 已有 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`。飞书应用需：`im:message`（或 `im:message:send_as_bot`）、可用性覆盖收件人、机器人已启用。

改完 **重启 Cursor MCP**，面板里应出现 `feishu-im` 三个工具。

## 用法

```
把 ENT-FE-I2-12-ANALYSIS-GATE-L01 的抽查结果私信给监管人
→ im-notify-task  task_id=…  text=…  audience=supervisor
```

```
发给徐滕强，任务 ENT-X，请回填 cost
→ im-send  to=徐滕强  task_id=ENT-X  text=请回填 cost 四字段
```

`dry_run: true` 只校验不调用飞书。

## 自检

```powershell
node --experimental-strip-types --test scripts/feishu-im-guard.test.mts
```

缺映射：先跑 `scripts/feishu-bitable-harvest-person-ids.ps1`，再把人加进花名册。
