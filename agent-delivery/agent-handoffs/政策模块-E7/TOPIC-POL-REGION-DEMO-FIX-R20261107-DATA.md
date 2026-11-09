# TOPIC-POL-REGION-DEMO-FIX-R20261107-DATA · 区域政策对比粤港澳源行核对

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 开工时已认领，本单未再认领 |
| 说明 | 只读核对已签发结果 `POLICY-20261107-008`（`industry_vid=chain:INB1303`）里粤港澳（除深）为何是 0。不改代码，不新签发分析任务。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A` |
| 说明 | 定义核对，没有改业务代码。 |

ponytail: N/A

## 图

不改调用链，不改图。

## 缺口与现况

- 缺口键：`policy_base_info.INB1303.粤港澳（除深）`
- 查库时间：2026-11-07 17:47:33（库 `NOW()`）
- 主机 `10.50.11.76:3306`，用户 `gkxlumenx`，取自 `lumen-algo-py/scripts/seed/seed_synth_elem.py` 缺省。口令只进本次进程，未打印，未写入文件。
- 只读 `SELECT`。未写 ODS、供应方库、`gapfill_`、新 ADS。未执行 `--apply`。未造政策、补贴或准入条件。

产业筛选与 `polan/timeseries_board.py` 的 `resolve_policies` → `default_load_policies` 相同：`demo_gkxlumenx_dwd.policy_base_info` 且 `COALESCE(is_deleted,0)=0`，并用 `demo_gkxlumenx_ads.policy_industry_rel` 等值筛 `industry_link_code=chain:INB1303`、`is_deleted=0`。归区调用 `polan/regional_board.py` 的 `zone_of`（地区字段非空时只看 `region`，否则看 `publish_organization`），内部规则是 `assign_zone`。

现况行数（合计 57，与已签发「关联政策 57 条」一致）：

| 归区 | 行数 |
|---|---|
| 深圳（大湾区） | 7 |
| 长三角 | 23 |
| 粤港澳（除深） | 0 |
| 京津冀 | 7 |
| 成渝 | 1 |
| 对不上 | 19 |
| 该产业政策总行数 | 57 |

## 结论

源里为 0，不能造数。粤港澳（除深）没有可归入的政策行，因此没有地区字段样例。已签发结果里该区 `policy_count=0`、`scores=[0,0,0,0,0]`、`composite=0` 与源行一致。本单不改算法、不改前端。

补贴标准、准入条件：用例已经规定不派补数。本单不把这两列的空值写成待补数，也不补假条款。

## 修改内容

- 只新增本 handoff。未改业务仓。

## 测试结果

- 只读查询 1 次，库时间 2026-11-07 17:47:33。五区加对不上等于 57。

## 遗留风险

- 粤港澳（除深）要出现非 0，只能等源里有能按 `assign_zone` 归入该区的政策行。本单不造数。

## CI/CD

- 分支：未提交
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：无代码变更

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/TOPIC-POL-REGION-DEMO-FIX-R20261107-DATA.md`
