# POLICY · DWD

```yaml
---
doc_id: POLICY-STORE-MYSQL-DWD
element: POLICY
role: store-mysql
status: draft
version: "2026-08-21"
updated: 2026-08-21
engine: mysql
task_id: DATA-POLICY-STORAGE-S3-L01
---
```

> **贴源结构**：[`../../sources/ods-ddl.md`](../../sources/ods-ddl.md)。  
> **落库名**：`demo_gkxlumenx_dwd.policy_base_info`。主键 `policy_id` ← ODS `id`。  
> 对照：[`../../etl/ods-to-dwd-mapping.md`](../../etl/ods-to-dwd-mapping.md)。本叶不 APPLY。  
> 勿把 `gkx.dwd_policy_base` 当项目 DWD 表名。旧稿 v1 37 列 **过期**。

项目 DWD 列以能承接贴源为准：`status` 用有效/失效文案；`rank`/`type`/`province|city|district`/`policy_support` JSON 必须能落到库，禁止再压成旧 smallint `level`。国际行同表 + 平面标记。
