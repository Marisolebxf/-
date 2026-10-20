# 管道 · → MinIO（产业链引用）

> **平台正文**：[`../../platform/minio.md`](../../platform/minio.md)（勿复制）

## 本域约定

| 项 | 值 |
|---|---|
| 对象前缀（建议） | `chain/{task_id}/` |
| Demo 桶（目标） | 与平台 demo 分析结果桶一致 |
| 典型对象 | 用户生成的产业链报告 HTML/PDF → `gkx-user-reports` 的 `topic/`；分析 JSON 仍在 `gkx-analysis-results` |

## 指针

| 项 | 路径 |
|---|---|
| 平台 MinIO | `storage/platform/minio.md` |
| ENT 参考 | [`../../ENT/etl/pipeline-to-minio.md`](../../ENT/etl/pipeline-to-minio.md) |
