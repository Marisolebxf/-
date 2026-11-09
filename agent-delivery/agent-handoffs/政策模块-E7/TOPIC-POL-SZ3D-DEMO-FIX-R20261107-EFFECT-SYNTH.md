# TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-SYNTH · 合成与手工政策写入落地实效缺项行

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 与缺项灌数同一会话执行。状态停在待签收，不改为 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 合成、新增、编辑、删除接到同一张缺项表。不改按钮条数，不改原有 ODS / DWD 写入。自检注入 `insert_fn` 时不碰库。 |

## 问题清单

- 算法库事后新增或合成的政策，不在一次性灌数范围内。写入时要补同一张表的一行，删除时只删该政策的行。

## 修改内容

- `polan/mockgen/effect_gapfill.py`：规则与灌数脚本相同。批次号 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-SYNTH`。
- 合成 `_attach` 为新政策和历史版本各写一行。`delete_all` 只按本次要删的合成 `policy_id` 删缺项行，不整表清空。
- `save_policy` 在提交前写入一行。`delete_policy` 删这一行。表还没建时，删除政策仍完成。
- `lumen-algo-py/vendor/entan-py` 与 `demo-algo-ent-analysis` 两处同文。

## 测试结果

- 两仓 `polan.mockgen.synth.self_check` 均打印 `policy synth self_check OK`。
- 未改合成按钮条数，未调用线上合成。

## 遗留风险

- 算法库进程要重新部署后，页面上的新增和合成才会写这张表。已经在库里的 20651 条由灌数单覆盖。

## CI/CD（必填）

- 分支：`demo-algo-ent-analysis` `dev`；`lumen-algo-py` `dev` 的 vendor 副本同一改动
- commit：demo `06f7267`（`e6ee212..06f7267`）；lumen `4074b52`
- pipeline URL / ID：推送后由仓 CI 触发，本会话未打开流水线页面
- 部署 namespace / 镜像 tag：未在本会话核对
- K8s rollout：未在本会话核对
- dev 测试 URL / 命令与结果：离线自检见上

## 涉及文件

- `repos/demo-algo-ent-analysis/polan/mockgen/effect_gapfill.py`
- `repos/demo-algo-ent-analysis/polan/mockgen/synth.py`
- `repos/demo-algo-ent-analysis/polan/mockgen/incr.py`
- `repos/lumen-algo-py/vendor/entan-py/polan/mockgen/` 下同名三文件

## 成本（会话估算）

| 字段 | 值 |
|---|---|
| actual_tokens | 30000 |
| model_used | grok-4.7 |
| actual_cost | 0.8 |
| cost_warn | green |
