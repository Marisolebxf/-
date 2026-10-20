# 平台对象存储（MinIO）

> **级别**：平台级唯一正文  
> **企业维**：只引用本文，在 `storage/ENT/etl/pipeline-to-minio.md` 写本域前缀/生命周期，**禁止复制**本文全文  
> **桶名与对象键的规约真源**：`agent-delivery/architecture-baseline.md` **§2.1（D14）**。本文与之保持一致；冲突时以基线为准。

```yaml
---
doc_id: PLATFORM-MINIO
role: store-minio
status: aligned
version: "2026-10-20"
updated: 2026-10-20
engine: minio
---
```

## 1. 职责

- 存放分析报告、导出 PDF/HTML、任务产物等**对象字节**
- 不替代 MySQL 业务表；元数据（task_id、路径、权限）落关系库任务/资产表

## 2. 谁写 / 谁读

| 角色 | 权限 |
|---|---|
| Python 算法 / 报告流水线 | 写对象（约定前缀） |
| Java 下载门面 | 读（经鉴权）；不扫 DWD |
| 前端 | 禁止直连 MinIO |

## 3. 现网

| 项 | 值 |
|---|---|
| Endpoint | `http://10.50.69.111:19000`（路径风格；控制台 `:19001`） |
| 凭证 | K8s Secret `gkxlumen-platform-rustfs`；主机 `/data/middleware/.env`。不进本仓明文 |
| 正式业务桶 | `gkx-lumen`。六个用途是目录，不是独立桶 |
| Demo | `demo-gkx-analysis-results`。Demo 不写 `gkx-lumen` |
| TTL | 未设生命周期。用户报告、政策原文与采购原文按长期保留；头像和 CMS 图随记录删除 |

可观测桶 `tempo-blocks`、`loki-chunks` 在旧集群 `rustfs-svc`（`:30900`）。同实例上的 `gpustack`、`plane` 本项目不使用。`milvus` 桶只给 Milvus 进程，业务不写。

## 5. 正式桶

正式业务只有桶 `gkx-lumen`。元数据（谁能下、对应哪条业务记录）留在 MySQL，桶里只放字节。

| 目录 | 放什么 | 对象键 |
|---|---|---|
| `gkx-analysis-results` | 展示系统、专题系统分析中间结果 JSON | `gkx-analysis-results/analysis/{type}/{parentTaskId}/{taskId}/{file}` |
| `gkx-user-reports` | 展示系统、专题系统用户生成的 HTML 和 PDF | `gkx-user-reports/science/html/`、`science/pdf/`、`topic/html/`、`topic/pdf/`，后面接 `{userId}/{yyyyMMdd}/{file}` |
| `gkx-source-reports` | 政策原始文件，以及采购的三方报告 PDF。中文 `dwd_zh_report.file_path`（约 1.4 万，样例 `\E8A04BD6-….pdf`），外文 `dwd_en_report.file_path`（约 1.0 万，样例 `\AD\2018\AD1177190.pdf`） | 政策 `gkx-source-reports/policy/{file}`。采购原文去掉开头的 `\`，反斜杠改成 `/`：`gkx-source-reports/zh/E8A04BD6-….pdf`、`gkx-source-reports/en/AD/2018/AD1177190.pdf` |
| `gkx-cms-images` | CMS 写进 HTML 的图片 | `gkx-cms-images/{contentId}/{file}` |
| `gkx-user-assets` | 用户头像和其他零碎上传 | `gkx-user-assets/avatar/{userId}/{file}`、`gkx-user-assets/misc/{yyyyMMdd}/{file}` |
| `gkx-others` | 放不进上面五个目录的其他杂项 | `gkx-others/{用途}/{yyyyMMdd}/{file}` |

分析中间结果 JSON 进 `gkx-analysis-results`。用户生成的 HTML/PDF 进 `gkx-user-reports`。可观测对象不进 `gkx-lumen`，分别进 `tempo-blocks`、`loki-chunks`。UPMS 的 `SysFile` 仍是单桶上传，头像和 CMS 图要按上表分目录后再改上传入口。

## 4. 企业维引用

见 `../ENT/etl/pipeline-to-minio.md`（对象前缀、与分析任务表关联）。
