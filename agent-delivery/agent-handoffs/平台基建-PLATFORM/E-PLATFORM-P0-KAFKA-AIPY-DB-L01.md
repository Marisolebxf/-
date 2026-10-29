# E-PLATFORM-P0-KAFKA-AIPY-DB-L01 · lumen ai-py 数据库地址与 search-py 对齐

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:devops-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 名词与流程见 [`task-claiming-guide.md`](../../task-claiming-guide.md) |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改 1 个值 + 1 行注释；未用 YAGNI 跳过可观测 / 架构铁律（OTel env 未动，D12/D13 自检见下） |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单文件一行改动，上下文小，无需压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `ARCH-MSG-KAFKA` |
| 图 diff | 无边变更：发布者 `gkxlumen-platform-ai-py` → Kafka `10.50.11.76:9092` / `gkx.analysis.result` 不变；本叶只修发布者侧 MySQL 依赖地址，使任务能跑到发布那一步 |
| 会签态 | `draft`（抄 `architecture-baseline.md` §ARCH-MSG-KAFKA `signoff_status`） |

## 问题清单

- `lumen-topic-py/k8s/dev-ai-py.yaml` 中 `GKX_MYSQL_HOST="10.50.11.76"`，集群内不可达 → 异步分析任务全部 `failed`，ai-py 无法走到 Kafka 发布。
- 同仓 `k8s/dev-search-py.yaml` 已于 `0b1309f` 改为 `10.50.11.76`；两文件 USER / DATABASE / 口令行一致（coordinator 核实）。

## 修改内容

- `k8s/dev-ai-py.yaml`：`GKX_MYSQL_HOST` 值 `10.50.11.76` → `10.50.11.76`，上方加注释「与 dev-search-py.yaml 对齐，勿写回旧内网地址」。
- 未动其他行（口令行、PORT/USER/DATABASE、OTel、Kafka、MinIO env 均不变）；未改其他文件。

## 偏离说明

- 无。

## 测试结果 / 验收证据

| DoD | 结果 | 证据 |
|-----|------|------|
| 1. ai-py MySQL 地址改为 10.50.11.76 并 push origin/dev | ✅ | commit `a11364eebad521a4012b15888e414204125e7395`（`21cc71e..a11364e dev -> dev`），diff 仅 +2/-1 |
| 2. CI：py:smoke 与 py:image:ai 成功 | ✅ | pipeline `2556`：`py:smoke`(13420) success、`py:image:ai`(13422) success（另 image:search 13421 / image:worker 13423 也 success） |
| 3. deploy:ai-py 手动触发并 rollout 成功、镜像为新短 SHA | ✅ | job `13425` success（12.8s）；trace：`image=harbor.test.com/zp-tts/gkxlumen-ai-service:a11364ee`、`deployment "gkxlumen-platform-ai-py" successfully rolled out`；健康检查 `{"status":"ok","service":"gkx-ai-service","mock_enabled":false,...}` |

- 未点 `deploy:ai-worker`(13426, manual) 与 `deploy:search-py`(13424, manual)，按派单保持现网（worker 21cc71e8）。
- trace 中无 pod 启动日志 / MySQL 连接错误；但 `/health` 不探测 DB，**MySQL 连通性未在本叶实证**，需下一次异步分析任务（或 E2E 叶）确认 `failed` 消失。
- 未向 Kafka 生产任何消息。

## 遗留风险（其他 192.168.88.* 运行时地址，只报告未改）

| 位置 | 值 | 影响 |
|------|-----|------|
| `conf/settings.yaml:9` `es.host` | 10.50.11.76 | **ai-py 有影响**：`gkx_ai_service/views/recommend.py` 用 `ESClient`，而 `dev-ai-py.yaml` 未注入 `GKX_ES_HOST` → 推荐模块集群内会连 10.50.11.76（search-py 已注入 `10.50.11.76`）。建议另开叶补 `GKX_ES_HOST`（+ ES 账号 env 走 secret） |
| `conf/settings.yaml:17` `db.host` | 10.50.11.76 | 被 env 覆盖的服务（ai-py、search-py）无影响；`dev-ai-worker.yaml` 未注入 MySQL env，但 worker 代码未引用 db 模块，暂无影响 |
| `conf/settings.yaml:53` `java_callback.base_url` | http://10.50.69.111:30899/topicAsync | ai-py / worker 均注入 `GKX_JAVA_CALLBACK_BASE_URL`，集群内无影响；仅本地默认 |
| `conf/settings.yaml:65` `minio.endpoint` | 10.50.11.76:9900 | ai-py / worker 均注入 `GKX_MINIO_ENDPOINT`（rustfs svc），集群内无影响 |
| `.env.example:9,16` | 10.50.11.76 | 模板，非运行时 |

- 另：`conf/settings.yaml` 与 `dev-ai-py.yaml` 仍有明文凭据入 git（与 D13「口令不进 git」冲突），属既有债，本叶红线不动口令行。

## CI/CD（必填）

- 分支：`dev`
- commit：`a11364e` — `fix(k8s): ai-py 数据库地址与 search 对齐到 10.50.11.76 [agent:devops-agent]`（正文含任务 ID，无口令）
- pipeline ID：`2556`（项目 9，lumen-topic-py）
- deploy job：`deploy:ai-py` = `13425`（success）
- 部署 namespace / 镜像 tag：`zhipu-tts` / `harbor.test.com/zp-tts/gkxlumen-ai-service:a11364ee`
- K8s rollout：成功
- dev 测试：CI 内健康检查返回 status ok

## 可观测性

- OTEL_SERVICE_NAME：`gkxlumen-ai-service`（未改）
- traceId（dev 抽样）：未取（本叶无业务请求）
- Tempo / Loki：未查

## 架构合规自检

| 铁律 | 结果 | 说明 |
|------|------|------|
| 算法只在 Python | ✅ | 未涉及 |
| 调用链 前端→Java→Python | ✅ | 未改调用链 |
| 图谱 Nebula | ✅ | 未涉及 |
| 可观测 | ✅ | OTel env 保持不变 |
| CI/CD | ✅ | push → pipeline 2556 绿 → K8s dev rollout |
| demo2 只读 | ✅ | 未碰 demo 仓 |
| D12 demo/lumen 隔离 | ✅ | lumen ai-py 连 lumen 自用 MySQL 10.50.11.76，无 `demo-*` 服务回落 |
| D13 Kafka | ✅ | 未改 bootstrap / topic；未生产消息；未动 MySQL root / 口令行 |
| git 安全 | ✅ | 无 force push；commit 带 `[agent:devops-agent]` |

## 涉及文件

- `${GKX_ROOT}/repos/lumen-topic-py/k8s/dev-ai-py.yaml`

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ~120k |
| model_used | claude-opus（Cursor agent） |
| actual_cost | ~$1.5 |
| cost_warn | false |
| source | session_estimate |
