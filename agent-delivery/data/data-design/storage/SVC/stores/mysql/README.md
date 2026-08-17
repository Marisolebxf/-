# SVC · MySQL 存储

| 文档 | 内容 | 状态 |
|---|---|---|
| [`dwd-svc.md`](./dwd-svc.md) | 项目 DWD · **字段级**键/列/索引意图 | draft · DDL-L01 |
| [`ads.md`](./ads.md) | **ADS 契约面** · `svc_*` 十表 + 联动键 | draft · DDL-L01 |
| [`dim.md`](./dim.md) | 六类枚举 / verification / CHAIN_STAGES 指针 | draft · DDL-L01 |

库名约定：正式 `gkxlumenx_dwd` / `gkxlumenx_ads`；Demo `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads`。  
DDL 草稿：[`../../etl/demo_gkxlumenx_dwd_svc_tables.sql`](../../etl/demo_gkxlumenx_dwd_svc_tables.sql)（**不对正式库默认 APPLY**）。  
**细表不得仅因流图会签标 approved**。  
**结构优先**：字段可 draft 锁定；**灌数 / Q-SVC-010 准入**另轨，不挡结构。  
**禁止**把 ENT `dwd_org_*` / `enterprise_*` 整套复制进本目录。
