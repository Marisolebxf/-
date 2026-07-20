# Feishu Bitable Webhook Handler 运维手册

> 设计真源：[`RFC/RFC-003-feishu-bitable-webhook.md`](RFC/RFC-003-feishu-bitable-webhook.md)  
> 全员规约：[`自动派单与确认规约.md`](自动派单与确认规约.md)

## 1. 做什么？

飞书看板拖状态 → Bitable 自动化 POST → **本 Handler** → 写 `task-registry.yaml` → 若 `done` 则自动 `coordinator-dispatch scan` → pending 队列 → PM `confirm`。

## 2. 前置条件

| 项 | 说明 |
|----|------|
| Node 18+ | 与编排仓其它脚本一致 |
| `.env` | `FEISHU_APP_ID` / `FEISHU_APP_SECRET`（拉 record 用） |
| `.env` | **`FEISHU_BITABLE_WEBHOOK_SECRET`**（Webhook 鉴权，**团队自建**，飞书开放平台无此字段） |

### 2.1 生成 `FEISHU_BITABLE_WEBHOOK_SECRET`（首次配置）

**不是飞书发的**，PM/coordinator 本地生成一串随机口令，三处填**完全相同**的值：

1. `gkx-orchestration/.env` → `FEISHU_BITABLE_WEBHOOK_SECRET=...`
2. K8s `deploy/feishu-sync/k8s/secret.yaml`（从 `secret.example.yaml` 复制，勿 commit）
3. 飞书 Bitable 自动化 → HTTP 请求头 → `X-GKX-Webhook-Secret`

```powershell
# 生成示例（复制输出到 .env）
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }) -as [byte[]])
```

```bash
# macOS / Linux
openssl rand -base64 32
```

| 变量 | 从哪来 |
|------|--------|
| `FEISHU_APP_ID` / `FEISHU_APP_SECRET` | 飞书开放平台 · 应用凭证 |
| `FEISHU_BITABLE_WEBHOOK_SECRET` | **自己生成** · 仅用于校验自动化 POST |
| `feishu-bitable.yaml#webhook.enabled` | `true` |
| 公网 HTTPS | 飞书自动化需能访问（内网穿透 / K8s Ingress） |

## 3. 启动服务

```powershell
cd gkx-orchestration

# 常驻 HTTP（默认 0.0.0.0:8787）
.\scripts\start-feishu-bitable-webhook.ps1

# 指定端口
.\scripts\start-feishu-bitable-webhook.ps1 -Port 8787
```

健康检查：`GET http://localhost:8787/health`

## 4. 飞书 Bitable 自动化配置

**dev 外网地址（2026-07-21 已验收）**：

```text
http://111.198.38.90:12287/internal/feishu-bitable/webhook
```

健康检查：`http://111.198.38.90:12287/health` → `{"ok":true}`

1. 打开多维表格 → **自动化** → 触发器：**修改记录时**（建议只勾 **状态**）
2. 动作：**发送 HTTP 请求**
3. 方法：`POST`
4. URL：`http://111.198.38.90:12287/internal/feishu-bitable/webhook`
5. Header：`X-GKX-Webhook-Secret: <FEISHU_BITABLE_WEBHOOK_SECRET>`
6. **请求体（JSON）** — ⚠️ **不要手打** `"{{record_id}}"` 字面量（会 422）

在 JSON 编辑器里：

1. 先写固定骨架：

```json
{
  "record_id": "",
  "app_token": "JI94bBxwsaIzyMsMBrYcPJscnDc",
  "table_id": "tblb65lPULz31h9U"
}
```

2. 光标放在 `"record_id": "` 与 `"` 之间  
3. 点编辑器 **「+」/「插入变量」** → 选 **「记录 ID」**（或「当前记录 · 记录 ID」）  
4. 保存后运行日志里 body 应类似 `"record_id":"recvp57uv2wgMI"`，**不能**仍是 `{{record_id}}`

**临时验证**（用你截图里那条记录）：

```json
{
  "record_id": "recvp57uv2wgMI",
  "app_token": "JI94bBxwsaIzyMsMBrYcPJscnDc",
  "table_id": "tblb65lPULz31h9U"
}
```

Handler 会用 `record_id` 调 OpenAPI 拉全行，映射 `status` / `claimed_by` / `sprint_id` / `priority` 回 registry。

## 5. 本地调试

```powershell
# 单条 record（需 FEISHU_APP_*）
.\scripts\start-feishu-bitable-webhook.ps1 -Once -RecordId recvpVKbBOJrfH

# 模拟 status 变更（dry-run）
node scripts/feishu-bitable-webhook-handler.mjs --once --task-id ENT-MOD-SEARCH-UX-L01 --status 已完成 --dry-run

# curl 模拟 webhook（skip_verification: true 时）
curl -X POST http://localhost:8787/internal/feishu-bitable/webhook `
  -H "Content-Type: application/json" `
  -H "X-GKX-Webhook-Secret: your-secret" `
  -d '{"record_id":"recxxx","app_token":"...","table_id":"..."}'
```

## 6. 鉴权模式

| 模式 | 用途 |
|------|------|
| `X-GKX-Webhook-Secret` / `Bearer` | **Bitable 自动化（推荐）** |
| `X-Lark-Signature` + timestamp/nonce | 飞书开放平台事件订阅 |
| `verification_token` | url_verification / header token |
| `skip_verification: true` | **仅本地** |

## 7. 审计与日志

| 文件 | 内容 |
|------|------|
| `agent-delivery/_tmp/feishu-webhook-audit.jsonl` | 每次请求结果 JSONL |
| `agent-delivery/_tmp/feishu-webhook-handler.log` | 服务运行日志 |

## 8. 与 confirm / dispatch 衔接

- Webhook **只**写 registry + scan；**不**自动 confirm
- `status=done` → `coordinator-dispatch scan --cause-task {id}`
- PM 仍须：`node scripts/coordinator-dispatch.mjs confirm --all --approved-by human:郭万迎`

## 9. auto git push（默认开启）

`feishu-bitable.yaml` → `webhook.auto_git_push: true`（**默认**）：成功 inbound 后自动 `git pull --rebase` → commit → push `task-registry.yaml`。

团队其它成员 / CI / `board-sync-watch` 以 GitLab 上的 registry 为准；若关 `auto_git_push`，Webhook 只改本机 YAML，别人看不到。

## 10. K8s 部署（已有 Ingress 域名）

**清单**：[`deploy/feishu-sync/README.md`](../../deploy/feishu-sync/README.md)

| 资源 | 作用 |
|------|------|
| `Deployment` | 常驻 Webhook Handler |
| `CronJob`（30min） | 替代投影机 `board-sync-watch`（双向 + git push + scan） |
| `Ingress` path | 在**已有域名**上追加 `/internal/feishu-bitable` |

飞书自动化 URL：

```text
https://{你们已有Ingress域名}/internal/feishu-bitable/webhook
```

只需在同 host 上 **加一条 path**，不必新申请域名。
