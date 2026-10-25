# GitLab CI 变量 MCP

改 `lumen-algo-py` 上智谱模型那三条 CI 变量时用。操作约定在 [devops/发布注意事项.md](./devops/发布注意事项.md) §1。Agent 步骤在 skill `gkx-gitlab-ci-var`。

## 挂载

`.cursor/mcp.json`：

```json
"gitlab-ci-var": {
  "type": "stdio",
  "command": "node",
  "args": ["scripts/gitlab-ci-var-mcp-server.mjs"]
}
```

令牌只读 `gkx-orchestration/.env` 的 `GKX_GITLAB_TOKEN` 和 `GKX_GITLAB_BASE`。改完 `mcp.json` 后重启 Cursor 才会出现这个服务器。

## 工具

| 工具 | 作用 |
|---|---|
| `gitlab-ci-var-list` | 名称、masked、protected、raw、作用域、`value_length`。没有 value |
| `gitlab-ci-var-set` | 写入或更新一条。默认 Masked、不勾 Protected、raw、作用域 `*` |

`project` 传 `sz-gkx/gkx-lumen/lumen-algo-py`。服务器自己查数字 ID。不要用带 `%2F` 的项目路径调 API，本实例会 404。

自检：`node scripts/gitlab-ci-var-selfcheck.mjs`（不访问 GitLab，不读 `.env`）。
