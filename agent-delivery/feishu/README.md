# 飞书集成文档与配置

编排仓内**飞书相关 Markdown + 运行时 YAML** 归集于此，避免 `agent-delivery/` 根目录被开通说明和看板配置打散。

| 层 | 位置 | 说明 |
|----|------|------|
| 说明文档 / 开通教练 / 配置 YAML | **本目录** | 人类阅读、开通步骤、运维手册、看板列字典 |
| RFC | `agent-delivery/RFC/RFC-003-feishu-bitable-webhook.md` | 方案评审件，留在 RFC/ |
| K8s 部署 | `deploy/feishu-sync/` | 与清单同仓 |
| 同步脚本 | `scripts/sync-feishu-*.ps1` / `*.mjs` | 不随文档搬家 |

## 文档索引

| 文档 | 读者 | 作用 |
|------|------|------|
| [feishu-bitable-integration.md](./feishu-bitable-integration.md) | PM / coordinator / 全员 | Phase 0 多维表格 Kanban 开通 |
| [feishu-bitable-bidirectional-ops.md](./feishu-bitable-bidirectional-ops.md) | 站会主持 / coordinator | 双向 sync 操作手册 |
| [feishu-bitable-near-realtime.md](./feishu-bitable-near-realtime.md) | 工程师 / 投影机 | 近实时出站（不强制 WSL） |
| [feishu-bitable-webhook-handler.md](./feishu-bitable-webhook-handler.md) | coordinator / DevOps | Webhook Handler 运维 |
| [feishu-metric-board.md](./feishu-metric-board.md) | 数据 / PM | 指标与数据开发进度看板 |
| [feishu-project-integration.md](./feishu-project-integration.md) | PM / coordinator | 飞书项目（⏸ 待企业审批） |
| [feishu-bitable-setup-checklist.md](./feishu-bitable-setup-checklist.md) | 开通教练会话 | Bitable 开通步骤清单 |
| [feishu-bitable-setup-coach-prompt.md](./feishu-bitable-setup-coach-prompt.md) | 开通教练会话 | Bitable 教练 Prompt（整段复制） |
| [feishu-project-setup-checklist.md](./feishu-project-setup-checklist.md) | 开通教练会话 | 飞书项目开通步骤清单 |
| [feishu-project-setup-coach-prompt.md](./feishu-project-setup-coach-prompt.md) | 开通教练会话 | 飞书项目教练 Prompt（⏸ 暂缓） |

## 配置 YAML

| 文件 | 用途 |
|------|------|
| [feishu-bitable.yaml](./feishu-bitable.yaml) | 任务看板列名 / inbound / webhook |
| [feishu-project.yaml](./feishu-project.yaml) | 飞书项目（待审批） |
| [feishu-user-map.yaml](./feishu-user-map.yaml) | 人员 open_id 映射 |
| [feishu-metric-board.yaml](./feishu-metric-board.yaml) | 指标看板投影 |
| [feishu-decision-board.yaml](./feishu-decision-board.yaml) | 甲方决策清单投影 |
| [feishu-golive-board.yaml](./feishu-golive-board.yaml) | 上线前必办投影 |
| [feishu-user-story-board.yaml](./feishu-user-story-board.yaml) | 用户故事库投影 |
| [feishu-wanghui-progress-board.yaml](./feishu-wanghui-progress-board.yaml) | 王惠指标建模进度表配置快照（字段/选项配色/视图） |

入站提案队列仍在 `agent-delivery/bitable-inbound-proposals.yaml`（与 `registry-gap-proposals.yaml` 同类，不随看板配置搬家）。

## 相关入口

- 部署：[`../../deploy/feishu-sync/README.md`](../../deploy/feishu-sync/README.md)
- 方案：[`../RFC/RFC-003-feishu-bitable-webhook.md`](../RFC/RFC-003-feishu-bitable-webhook.md)
- 脚本索引：[`../../scripts/README.md`](../../scripts/README.md)
