# 管道 · → MinIO（服务机构引用）

> **平台正文**：[`../../platform/minio.md`](../../platform/minio.md)（勿复制）  
> **任务**：`DATA-SVC-STORAGE-GAP-L02` · 关闭 OPEN-SVC-FLOW-03 **写作**（现网 Endpoint / TTL 仍跟 OPEN-SVC-FLOW-02 / OPEN-ENT-FLOW-02）  
> **本单不写对象、不灌数。**

## 本域约定

| 项 | 值 |
|---|---|
| 对象前缀（建议） | `svc/{task_id}/` |
| Demo 桶（目标） | 与平台 demo 分析结果桶一致（见平台文；ENT 常见 `demo-gkx-analysis-results`） |
| 典型对象 | 用户生成的服务机构报告 HTML/PDF → 桶 `gkx-lumen` 目录 `gkx-user-reports` 的 `topic/`；分析中间结果 JSON → 同桶目录 `gkx-analysis-results` |
| 关联元数据 | 分析/导出任务表（MySQL）；路径与可下载态必须与对象存在一致 |

## 指针

| 项 | 路径 |
|---|---|
| 平台 MinIO | `storage/platform/minio.md` |
| 流图对象产物 | [`../01-data-flow.md`](../01-data-flow.md) §1 / §7 |
| ENT 同构 | [`../../ENT/etl/pipeline-to-minio.md`](../../ENT/etl/pipeline-to-minio.md) |

禁止在本文件粘贴现网 Endpoint / 密钥。
