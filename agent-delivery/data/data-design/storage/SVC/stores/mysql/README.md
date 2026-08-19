# SVC · MySQL 存储

| 文档 | 内容 | S3 状态 |
|---|---|---|
| [`dwd-svc.md`](./dwd-svc.md) | 项目 DWD：圈定池 / 图 hang / 投融资事件 hang | draft |
| [`ads.md`](./ads.md) | **ADS 契约面（必须）**：A1–A6 + 十模型回写 | draft |
| [`dim.md`](./dim.md) | 六类枚举 / 指标指针 | draft |
| [`ddl-demo-empty.sql`](./ddl-demo-empty.sql) | Demo **空表 CREATE**（`demo_gkxlumenx_dwd` / `_ads`） | draft · 本单不灌数 |

库名约定：正式 `gkxlumenx_*` 本总控禁写；Demo 上列两库。引擎：**MySQL 8 only**。  
**细表不得仅因流图会签标 approved**（`DATA-SVC-STORAGE-S3-L02`）。  
**禁止**用 `demo_gkxlumenx_ods.dwd_org_base_info` 冒充本目录项目 DWD。  
**禁止** `svc_org_base` / 全列复制 ODS 主表 / `enterprise_*` 主路径。
