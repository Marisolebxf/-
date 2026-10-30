# 本轮要在产线执行的 SQL

库：`gkxlumenx_dwd`。在 GDF 代理机上执行。本仓不代跑。

| 顺序 | 文件 | 做什么 |
|---|---|---|
| 1 | [script_state.sql](script_state.sql) | 新建 `script_state`。`CREATE TABLE IF NOT EXISTS`，可重复执行 |

没有别的语句。不要 `DROP`。不要给 `policy_industry_rel`、`policy_text_parse`、`policy_base_info` 加索引：清重口径还没定，那些只写在设计旁注里。

`policy_support` 源上就没有结构化要素，不做回刷。
