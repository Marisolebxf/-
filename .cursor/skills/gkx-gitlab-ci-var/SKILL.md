---
name: gkx-gitlab-ci-var
description: >
  Set or inspect GKX GitLab CI/CD variables, especially the single Zhipu LLM
  config (ZHIPU_LLM_API_KEY, ZHIPU_LLM_MODEL, ZHIPU_LLM_BASE_URL) on
  lumen-algo-py. Use when the user mentions GitLab CI 变量, ZHIPU_LLM,
  gkx-zhipu-llm, 改模型密钥, 换模型, or 发布时写入 Secret. Call the
  gitlab-ci-var MCP. Never print the token or the key, and never copy the
  key out of the cluster Secret.
---

# GKX GitLab CI 变量

模型发布约定在 `agent-delivery/devops/发布注意事项.md` §1。本 skill 只规定 agent 怎么改 GitLab 变量。挂载见 `agent-delivery/gitlab-ci-var-mcp-usage-guide.md`。

## 工具

先看 `gitlab-ci-var` 的 schema，再调用：

- `gitlab-ci-var-list`：只看名称和标志
- `gitlab-ci-var-set`：写入或更新一条

令牌在 `gkx-orchestration/.env` 的 `GKX_GITLAB_TOKEN`。不要把令牌或变量值放进参数以外的地方，不要写进命令行，不要复述到对话里。

项目用 `sz-gkx/gkx-lumen/lumen-algo-py`。不要自己把路径编成 `%2F` 去调 GitLab。

## 智谱这一份

| key | 值 |
|---|---|
| `ZHIPU_LLM_API_KEY` | 仅当用户给出新密钥时写入 |
| `ZHIPU_LLM_MODEL` | 默认 `glm-5.3-flash` |
| `ZHIPU_LLM_BASE_URL` | 默认 `https://open.bigmodel.cn/api/paas/v4`，不要加 `/chat/completions` |

三条都是 `masked=true`、`protected=false`、`raw=true`、`environment_scope=*`。勾了 Protected，`dev` 发布读不到。

没有新密钥时，不要 `set` `ZHIPU_LLM_API_KEY`，也不要从集群 Secret `gkx-zhipu-llm` 把 `api-key` 读出来。

## 写完之后

发布脚本 `lumen-algo-py/scripts/apply-zhipu-llm-secret.sh` 只在流水线里刷新 Secret。镜像标签没变时，挂了该 Secret 的 Deployment 还要 `rollout restart`。不要删 `tech-news-zhipu-llm`。
