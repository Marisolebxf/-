# 平台对象存储（MinIO）

> **级别**：平台级唯一正文  
> **企业维**：只引用本文，在 `storage/ENT/etl/pipeline-to-minio.md` 写本域前缀/生命周期，**禁止复制**本文全文  
> **状态**：draft · 待架构师/平台补全现网 bucket 约定

```yaml
---
doc_id: PLATFORM-MINIO
role: store-minio
status: draft
version: "2026-08-12"
updated: 2026-08-12
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

## 3. 待填（现网）

| 项 | 值 |
|---|---|
| Endpoint | （待填） |
| 默认 bucket | （待填） |
| Demo bucket | `demo_**`（与正式结构/前缀约定一致，仅桶名隔离；见 ENT `pipeline-demo-mock.md`） |
| 路径约定 | `{element}/{task_id}/...`（建议） |
| TTL / 生命周期 | （待填） |
| 凭证落点 | 配置中心 / K8s Secret（禁止进本仓明文） |

## 4. 企业维引用

见 `../ENT/etl/pipeline-to-minio.md`（对象前缀、与分析任务表关联）。
