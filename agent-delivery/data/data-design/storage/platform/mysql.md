# 平台 MySQL · 异步分析底座（gkxlumenx_topic_enterprise）

> **级别**：平台级唯一正文。`analysis_task` 是 ENT 企业评估 / CHAIN 产业链 / SVC 服务机构 / POLICY 政策四模块共用的异步分析任务底座表，不归属单一模块，故放 `platform/`；各模块域内表仍归各自 `storage/{模块}/stores/mysql/`。
> **真源关系**：库表物理 DDL 工程真源在 `repos/lumen-svc-platform/db/9x_gkxlumenx_topic_enterprise.sql` + 增量 `db/*_alter.sql`；本文只记录存储设计与索引契约，冲突时以工程 DDL 为准。

```yaml
---
doc_id: PLATFORM-MYSQL-TOPIC
role: store-mysql
status: draft
version: "2026-11-04"
updated: 2026-11-04
engine: mysql
incident: INC-20261104-policy-job-out-of-sort
---
```

## 1. 职责与读写

- `gkxlumenx_topic_enterprise`（实例 `10.50.11.76:3306`）：异步分析任务真源。Java `gkxlumen-topic-async-service`（端口 7094）写，`gkxlumen-display` 经 `POST /topic/v1/analysis/tasks` 代理创建，Python 算法回调改状态。
- 写读矩阵：Java 写 / Java 读 / Python 回调写状态字段；前端禁止直连。

## 2. analysis_task 表 · 索引契约

| 索引 | 列 | 服务于 |
|---|---|---|
| `uk_analysis_task_task_id` | `task_id`（UK） | taskId 点查、回调幂等 |
| `idx_analysis_task_user_status` | `user_id, status` | running 任务查询、列表过滤 |
| `idx_analysis_task_user_type_ct` | `user_id, analysis_type, create_time` | **指纹复用 / 链任务互斥查询**：等值前缀 + `ORDER BY create_time DESC` 走索引序，免 filesort |
| `idx_user_type_sub` | `user_id, analysis_type, sub_type` | sub_type 维度过滤 |
| `idx_analysis_task_status` | `status` | 后台扫描 |
| `idx_analysis_task_create_time` | `create_time` | 全局时间序 |
| `idx_analysis_task_parent` | `parent_task_id` | 报告/导出挂父任务 |
| `idx_analysis_task_retry_of` | `retry_of_task_id` | force/失败重试真关联 |

### 2.1 索引变更记录（INC-20261104）

- **现象**：2026-11-04 15:25 CST，政策全景建任务链路 `display → topic-async-service` 返回「政策分析任务不可用」，trace `2def7be6d752468886633465e8982c80` 断点在 `SELECT ... FROM analysis_task WHERE user_id=? AND analysis_type=? ... ORDER BY create_time DESC`（指纹复用查询，无 LIMIT、全列 SELECT 含 `result_data` 大 JSON），MySQL 抛 `Out of sort memory`。
- **根因**：原 `idx_analysis_task_user_type(user_id, analysis_type)` 不含 `create_time`，排序无法走索引 → filesort 将含大字段的整行拉进 sort buffer 溢出。
- **修法**：新增 `idx_analysis_task_user_type_ct(user_id, analysis_type, create_time)`；旧 `idx_analysis_task_user_type` 为其前缀冗余，一并 DROP。在线 DDL（ALGORITHM=INPLACE, LOCK=NONE），Java/Python 零代码改动。
- **变更 SQL**：`lumen-svc-platform/db/9x_gkxlumenx_topic_enterprise_analysis_task_idx_alter.sql`（幂等，可重复执行）。

## 3. 宽行 / 大字段约束

- `result_data`（json）、`target_params`（json）、`error_msg`（text）为大字段。**复用 / 互斥 / 列表类查询必须**：
  1. 条件列命中 `idx_analysis_task_user_type_ct` 前缀；
  2. `ORDER BY create_time` 必须可走该索引序；
  3. 尽量带 LIMIT 截断；确实需要全列时（详情单条 `task_id` 点查）不受限。
- 违反以上任一条，行数增长后 `Out of sort memory` 会复发——届时按第 2 节索引契约补索引，而不是调大 `sort_buffer_size`。

## 4. 凭证与访问

- 实例 `10.50.11.76:3306`，账号 `gkxlumenx`（口令 K8s 部署清单同源，不进文档明文）；数据源走 Nacos 共享配置。
- `analysis_task` 库表 DDL 变更一律走 `repos/lumen-svc-platform/db/` 增量脚本（幂等 PREPARE 模式），回填记录到本文 §2.1。
