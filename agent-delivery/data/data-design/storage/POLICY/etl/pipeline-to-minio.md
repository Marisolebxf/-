# 管道 · → MinIO（政策维引用）

> **平台正文**：[`../../platform/minio.md`](../../platform/minio.md)（勿复制）  
> **任务**：`DATA-POLICY-STORAGE-S2-L01`  
> **本单不写对象、不灌数。**

## 本域约定

| 项 | 值 |
|---|---|
| 政策原始文件 | 桶 `gkx-lumen` 目录 `gkx-source-reports`，键 `gkx-source-reports/policy/{文件}` |
| Demo 桶 | `demo-gkx-analysis-results`。Demo 不写 `gkx-lumen` |
| 典型对象 | 政策原始文件进 `gkx-source-reports`。解析中间结果 JSON 进同桶目录 `gkx-analysis-results`。用户生成的 HTML/PDF 进 `gkx-user-reports` |

禁止在本文件粘贴现网 Endpoint / 密钥。
