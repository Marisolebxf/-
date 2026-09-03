# DATA-ENT-DWD-ALIGN-ETL-L01 · lumen-etl-es-py 改读正式库列名

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只改六模块 `SELECT`/`row.get`；不改 ES params 键名、不改 Java、不加依赖 |

## 范围

`lumen-etl-es-py` 六模块改读正式库 `gkxlumenx_dwd` 现网列。ES params 键名不动。

| 模块 | DWD 读 | ES 仍写 |
|------|--------|---------|
| `bid` | `bid_title` `event_date` `bid_amount` | `announcement_title` `announcement_date`；`role` 固定「中标方」 |
| `news` | `title` `publish_time` `summary` | `title` `date` |
| `invest` | `inv_org_name` `invest_amount` `invest_ratio` | `related_name` |
| `finance` | `revenue` `net_profit` `total_assets` `total_liabilities` | `pure_profit`←`net_profit`；停 `total_profit` 双写 |
| `executive` | `gender`（不读 `data_source`） | `name` `position` |
| `reg_info` | 去掉 extra 七列；补读 `revenue_latest` `is_foreign` | 顶层键不变 |

## 偏离

- DDL 后已补读：extra 七列、财务三列、`bid.project_no`（只作 nested `id`）。
- `news.original_url`：ES news 无对应键，不灌、不新开字段。
- 灌数仓 `demo-algo-science` 无列名映射，未改。

## 测试结果

- `python3 -m py_compile` 六模块：通过。
- 抽检：上述 SELECT 列均在正式库 `information_schema`（finance 现网有 `net_profit`；bid 有 `bid_title`/`event_date`/`bid_amount`）。
- `lumen-svc-platform` 企业 API：**未改文件**。

## 遗留风险

- 对正式库跑 ETL 前，未 ADD 列不得 SELECT。
- demo DWD 仍是设计列名；本叶 ETL 配置目标是正式库。demo 灌数不走这六模块列映射。

## CI/CD

- 分支：`origin/dev`
- commit：`9692851` `fix(etl): 六模块改读正式库 DWD 列名 [agent:data-agent]`
- pipeline：随 `lumen-etl-es-py` `dev` CI
- K8s rollout：等 CI；本叶不宣称已灌绿
- 验证：`py_compile` 六文件；SQL 列 ∈ 正式库

## 成本

- actual_tokens：22000（会话估算）
- model_used：cursor-grok-4.6
- actual_cost：0.12
- cost_warn：green

## 架构合规

| 铁律 | 结果 |
|------|------|
| 调用链 | ✅ 只改 Python ETL 读列 |
| D12 | ✅ 未调 demo 服务 |
| Java REST | ✅ 零 diff |
| ES 字段名 / 别名 `gkx_enterprise` | ✅ 不动 |
| GDF 不写 ES | ✅ |

## 涉及文件

- `etl/modules/bid.py`
- `etl/modules/news.py`
- `etl/modules/invest.py`
- `etl/modules/finance.py`
- `etl/modules/executive.py`
- `etl/modules/reg_info.py`
