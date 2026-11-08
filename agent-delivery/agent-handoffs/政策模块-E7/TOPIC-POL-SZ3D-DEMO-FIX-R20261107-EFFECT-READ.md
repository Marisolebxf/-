# TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-READ · 深圳结果板改读落地实效缺项表

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 缺项表已灌 20651 行后改读。状态停在待签收，不改为 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只在 DWD 加载路径补内存字段。调用方自带 items 的单测不读库。缺项表不存在时保持原行，缺维仍不可算。 |

## 问题清单

- 城市截面 SQL 读不到实施日、支持对象和反馈。缺项行不能写回主表，也不能把空值当成 0。

## 修改内容

- `default_load_city_section` 读出 DWD 后，查询 `gkxlumenx_gapfill.gapfill_policy_sz_effect`，只补尚未启动、没有支持对象、没有反馈的行。
- 等于发布日的日期不补。反馈 0 不补。已有真值不覆盖。
- 三维仍按原公式：启动、覆盖、反馈。缺的维不进平均。三样都空则不可算。不出综合分。不改 QPOL-02 权重。
- 城市截面 SQL 仍不含金额，不读招标表。
- 不改 D4。实算镜像起来后，可交 data-agent 把该指标 `ingestion_status` 从 mock 改走。本单不改矩阵。

## 测试结果

- `python -m pytest tests/test_policy_shenzhen_board.py -q` → 13 passed。
- 新增用例确认：发布日副本、空对象、0 分不写入；已有实施日、对象和反馈不被缺项行覆盖。

## 遗留风险

- 线上分数要等 `4074b52` 镜像 rollout 之后才会变。本会话没有重发分析任务。
- 工作区里 `synth.py` 另有未提交的真实政策抽样改动，不属于本单，没有进 `4074b52`。

## CI/CD（必填）

- 分支：`lumen-algo-py` `dev`
- commit：`4074b52`（`1539d73..4074b52`）
- pipeline URL / ID：推送后由仓 CI 触发，本会话未打开流水线页面
- 部署 namespace / 镜像 tag：未在本会话核对
- K8s rollout：未在本会话核对
- dev 测试 URL / 命令与结果：单测 13 passed

## 涉及文件

- `repos/lumen-algo-py/vendor/entan-py/polan/shenzhen_board.py`
- `repos/lumen-algo-py/tests/test_policy_shenzhen_board.py`

## 成本（会话估算）

| 字段 | 值 |
|---|---|
| actual_tokens | 20000 |
| model_used | grok-4.7 |
| actual_cost | 0.5 |
| cost_warn | green |
