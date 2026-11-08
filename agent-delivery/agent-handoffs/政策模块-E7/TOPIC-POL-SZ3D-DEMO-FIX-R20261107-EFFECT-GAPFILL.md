# TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-GAPFILL · 深圳政策现状落地实效缺项灌数

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 本会话按「领取并执行，直到完成」执行。状态停在待签收，不改为 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用已有缺项库和种子脚本的连库方式。没有新依赖。未改 D4，未改政策主表。 |

## 问题清单

- 源库政策没有可用实施日、支持对象和反馈。按 D16 在 `gkxlumenx_gapfill` 建 `gapfill_policy_sz_effect`，一政策一行。

## 修改内容

- 表：`gkxlumenx_gapfill.gapfill_policy_sz_effect`。主键 `policy_id`。
- 规则填充，`fill_method=rule`，`fill_model` 空。`metric_id=M_POLICY_IMPLEMENTATION_EFFECT`。`gap_item=落地执行启动,受益覆盖,实施反馈`。
- 实施日 = 有效发布日（没有则 2016-01-01）再加 1–120 天，因此不等于发布日，也不是零日期。支持对象为企业、科研机构、高等学校、新型研发机构之一。反馈分 1–5，不写 0。
- 只读 `demo_gkxlumenx_dwd.policy_base_info`。不写 ODS、正式 DWD、ADS、供应方库，不改 `implementation_date` 原列。

## 测试结果

- `python scripts/seed_gapfill_policy_sz_effect.py --check` 退出码 0。
- `--apply` 退出码 0：`source_ids=20651`，`rows=20651`，`bad_rows=0`，`publish_date_copies=0`，库 `gkxlumenx_gapfill`。
- 口令未打印。

## 遗留风险

- D4 仍是 mock。公式接通并实算后，再由 data-agent 改 `ingestion_status`。本单不改矩阵。
- 已部署的结果板要等 `lumen-algo-py` `4074b52` 的镜像起来，才会读到这张表。

## CI/CD（必填）

- 分支：`lumen-algo-py` `dev`
- commit：`4074b52`（`1539d73..4074b52`）
- pipeline URL / ID：推送后由仓 CI 触发，本会话未打开流水线页面
- 部署 namespace / 镜像 tag：未在本会话核对
- K8s rollout：未在本会话核对
- dev 测试 URL / 命令与结果：灌数命令见测试结果

## 涉及文件

- `repos/lumen-algo-py/scripts/seed_gapfill_policy_sz_effect.py`
- `repos/lumen-algo-py/scripts/mysql/gapfill_policy_sz_effect.sql`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/effect_gapfill.py`

## 成本（会话估算）

| 字段 | 值 |
|---|---|
| actual_tokens | 40000 |
| model_used | grok-4.7 |
| actual_cost | 1.0 |
| cost_warn | green |
