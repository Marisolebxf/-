# SVC · ODS/ENT → 本域 DWD（圈定）

```yaml
---
doc_id: SVC-ETL-ODS-TO-DWD
element: SVC
role: etl
status: draft
version: "2026-08-14"
---
```

> 读 ENT 机构主体键 + 约定 ODS 特征 → Python 圈定 → `service_org*`（**待核验**）。  
> 表清单：[`../stores/mysql/dwd-svc.md`](../stores/mysql/dwd-svc.md)。  
> **禁止**复制 `dwd_org_base_info`；**禁止**伪闭合 Q-SVC-010。  
> Demo：[`pipeline-demo-mock.md`](./pipeline-demo-mock.md)。
