# API-TOPIC-FE-JAVA-GAP-SVC-L01

> 实现交接。需求真源仍是同目录 `API-TOPIC-FE-JAVA-GAP-SVC-L01.md`。接口总文档：`API-TOPIC-FE-GAP-CATALOG.md` §6。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 专题前端服务链 P0/P2；P1 本次不做 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 对比篮不写 ADS；六类服务从 Python `_CLASS_LABELS` 出，Java 不写死「金融服务」 |

## 范围与实现

- **SVC-N1–N3**：`POST /svc/topic/v1/service/meta`（Python + Java 透传；Feign 失败 HTTP 200 + 空列表）
- **SVC-N4**：`/svc/topic/v1/service/compare-basket/**` → Feign enterprise → `svc_compare_basket_item`（可写企业库，不写 ADS）；`source` 含 `external` 拒绝
- **SVC-F1–F6**：门户 / 检索 / 画像 / 图谱 / 名单 / 任务结果空槽；缺数据不造数
- **P1（SVC-O1–O4）本次不做**

## 偏离

- K8s 只发 search-py：`gkx_svc` 已挂在 `gkx_search_service/main.py`。
- **运维**：`svc_compare_basket_item` DDL 须在 `gkxlumenx_topic_enterprise` 执行后写篮才成功（`lumen-svc-platform/db/9x_gkxlumenx_topic_enterprise.sql`）。

## 产物清单

| 仓 | 分支 | commit |
|---|---|---|
| lumen-svc-platform | `origin/dev` | `868987d6` |
| lumen-topic-py | `origin/dev` | `c73d8a0e` |
| gkx-orchestration | `origin/dev` | catalog + 本 handoff |

## 验收证据

- Java：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/pipelines/5943
  - `deploy:topic-svc` / `deploy:topic-enterprise` 绿（tag `868987d6`）
- topic-py：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5941
  - 手动 `deploy:search-py` 绿；in-pod `/healthz` `gkx-search-service` ok
- 本机不到 88.50；未在工作站 curl 网关。对比篮写路径待 DDL。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 调用链 前端→Java→Python `/internal/*` | ✅ 读面 |
| 对比篮写 MySQL 企业库，不写 ADS | ✅ |
| D12 不调 demo-* | ✅ |
| 环节↔六类 `service_types=[]` | ✅ 不替甲方拍板 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 150000 |
| model_used | Cursor Grok 4.6 |
| actual_cost | 4.50 |
| cost_warn | green |

## 遗留风险

- 未跑 DDL 则对比篮写入会失败。
- P1 对标城 / 联想 / 导出 / 跨端已查看：本次不做。
