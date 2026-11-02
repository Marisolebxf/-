# 本轮要在产线执行的 SQL

在 GDF 代理机上执行。本仓不代跑。不要 `DROP`。

| 顺序 | 文件 | 做什么 |
|---|---|---|
| 1 | [update_round1.sql](update_round1.sql) | 本轮全部变更。只执行这一份 |

这一份里按顺序做四件事：

1. 在 `gkxlumenx_dwd` 新建 `script_state`（`CREATE TABLE IF NOT EXISTS`）。
2. 按文件头的清重口径，删掉 `policy_industry_rel`（DWD、ADS）的重复行，再加唯一键 `uk_pid_code (policy_id, industry_link_code)`。
3. 删掉 ADS `policy_text_parse` 里完整 `policy_id` 相同的重复行，再加 `uk_ptp_pid (policy_id(64))`。完整 `policy_id` 不同、只是前 64 字相同的行不删；有这种行时脚本停住，不要改前缀。
4. 给 `gkxlumenx_dwd.policy_base_info` 加普通索引 `idx_pid (policy_id)`。不删行，不改已有唯一键 `(source_plane, policy_id)`。

`script_state.sql` 只是建表片段，内容已在 `update_round1.sql` 里。不要再单独执行。

DWD 的 `policy_text_parse` 本轮不改。`policy_support` 不做回刷。
