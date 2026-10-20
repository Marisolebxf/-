# 管道 · → MinIO（企业维引用）

> **平台正文**：[`../../platform/minio.md`](../../platform/minio.md)（勿复制）  
> S2 回填 · OPEN-ENT-FLOW-03 **推进**

## 本域约定

| 项 | 值 |
|---|---|
| 对象前缀（建议） | `ent/{task_id}/` 或 `topic/ent/{task_id}/` |
| Demo 桶（目标） | `demo-gkx-analysis-results` |
| 正式位置 | 桶 `gkx-lumen` 内的目录，见平台正文。不再单开 `gkx-analysis-results` 桶或 `gkxlumen-topic-analysis-results` |
| 关联元数据 | 分析/导出任务表（MySQL）；路径与可下载态必须与对象存在一致 |
| 典型对象 | 用户生成的企业报告 HTML/PDF → 桶 `gkx-lumen` 目录 `gkx-user-reports`（`topic/html/`、`topic/pdf/`）；分析中间结果 JSON → 同桶目录 `gkx-analysis-results` |

## 指针

| 项 | 路径 |
|---|---|
| 平台 MinIO | `storage/platform/minio.md` |
| 流图对象产物 | `ENT/01-data-flow.md` §3 |
| 现网配置参考 | `repos/demo-svc-topic-py/conf/settings.yaml`（`bucket`） |

Endpoint / TTL / 凭证 → **OPEN-ENT-FLOW-02**（平台补全，本单不关）。
