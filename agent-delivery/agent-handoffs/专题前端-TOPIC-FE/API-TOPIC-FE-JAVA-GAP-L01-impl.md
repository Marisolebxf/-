# API-TOPIC-FE-JAVA-GAP-L01

> 实现交接。需求真源仍是同目录 `API-TOPIC-FE-JAVA-GAP-L01.md`。接口总文档：`API-TOPIC-FE-GAP-CATALOG.md`（一份，按模块分章）。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 专题前端企业 + 产业链 P0/P2；P1 本次不做 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过调用链 / 可观测 / D12；字典不硬编码、不替甲方拍板 |

## 范围与实现

- **ENT-N1/N2**：`DELETE /enterprise/topic/v1/compare-basket/{recruit|cultivate}-candidates/**`（Java MySQL）
- **ENT-N3**：`POST /enterprise/topic/v1/search/meta/policy-orientations`（Python 出数 + Java 透传）
- **ENT-N4**：`DELETE /topicAsync/topic/v1/analysis/tasks/{taskId}` 软删，≠ cancel；运行中先 cancel
- **ENT-F1–F4**：评估树 / compare / result / KPI 补别名或显式 `null`，不造数
- **CHAIN-N1–N4**：`GET /chain/topic/v1/industry/meta`；对标清单空（Q016）
- **CHAIN-F2/F4**：search `classification`、snapshot `as_of`
- **P1（ENT-O1/O2、CHAIN-O1–O3）本次不做**

## 偏离

- 产业链 meta 复用存量 chain Feign，未新开 Java→算法直连。
- 本机不到 `192.168.88.50` NodePort；dev 验收以 CI rollout / 仓内单测 / `e2e:chain-gold` 为准。

## 产物清单

| 仓 | 分支 | commit |
|---|---|---|
| lumen-svc-platform | `origin/dev` | `868987d6` |
| lumen-topic-py | `origin/dev` | `c73d8a0e` |
| lumen-algo-py | `origin/dev` | `62aa025c` |
| gkx-orchestration | `origin/dev` | catalog `4c92b98c` + 本 handoff |

## 验收证据

- Java pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5943
  - `backend:build` 绿；`deploy:topic-enterprise` / `topic-async-service` / `topic-chain` 绿（镜像 tag `868987d6`）
- topic-py：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5941
  - 手动点了 `deploy:search-py` / `deploy:ai-py`，healthz ok
- algo-py：https://gitlab.htmisoft.net/gkx-lumen/lumen-algo-py/-/pipelines/5942
  - `deploy:api` / `deploy:worker` 自动绿，healthz ok
- `e2e:chain-gold` 首次随 async 滚动出现 503（`/topicAsync/.../tasks/running`）；rollout 稳定后重跑 **6 passed** https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/jobs/26307

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 前端→Java→Python `/internal/*` | ✅ |
| 算法只在 Python | ✅ |
| Nebula 未改 | ✅ |
| D12 不调 demo-* | ✅ |
| 口径未定不硬编码 | ✅ Q016 对标空 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 220000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 6.50 |
| cost_warn | green |

## 遗留风险

- P1 本次不做，见 catalog §9.3。
- 评估覆盖率 / 商业力趋势 / 风险点边 / 真实 `dataTime` 等 P2 空槽等算法，禁止 FE/Java 造数。
