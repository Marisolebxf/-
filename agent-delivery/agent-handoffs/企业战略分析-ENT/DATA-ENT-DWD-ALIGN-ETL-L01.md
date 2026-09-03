# DATA-ENT-DWD-ALIGN-ETL-L01

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |
| ponytail | `full` |

## 范围

`lumen-etl-es-py` 六模块改读正式库 `gkxlumenx_dwd` 现网列。ES params 键名不动。

| 模块 | DWD 读 | ES 仍写 |
|------|--------|---------|
| `bid` | `bid_title` `event_date` `bid_amount` | `announcement_title` `announcement_date` |
| `news` | `title` `publish_time` `summary` | `title` `date` |
| `invest` | `inv_org_name` `invest_amount` `invest_ratio` | `related_name` |
| `finance` | `revenue` `net_profit` `total_assets` `total_liabilities` | `pure_profit`←`net_profit`；停 `total_profit` 双写 |
| `executive` | `gender`（不读 `data_source`） | `name` `position` |
| `reg_info` | 去掉 extra 七列；补读 `revenue_latest` `is_foreign` | 顶层键不变 |

## 偏离

- `project_no` / `original_url` / extra 七列 / 财务 `main_business_revenue` 等正式库尚未 ADD，本叶不 SELECT。DDL 后再补读。
- 灌数仓 `demo-algo-science` 无列名映射，未改。

## 架构合规

D12 ✅ 未调 demo 服务。Java REST 零改。GDF 不写 ES。
