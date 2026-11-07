# TOPIC-POL-SZ3D-DEMO-FIX-R20261107-BOARD · 深圳政策结果板按已有金额与实效字段计算

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 只改深圳政策现状结果板的读取与计算。不改第 3 章链名匹配，不改前端，不改 `effect.py`。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 有非空金额、真实实施日或非空支持对象才出数。全空仍为 null，不出 0。档位切点是临时线性分位，正式切点等 QPOL-02。未用 YAGNI 跳过调用链与可观测边界。 |

## 图

不改调用链。结果仍由 `polan/shenzhen_board.py` 的 `build_shenzhen_board` 组装。城市截面 SQL 不选 `amount`，不读 `dwd_bid_*`。

## 修改内容

- `support_from_rows`：行上有非空 `amount` 时，按城市算非空金额均值。入榜城市（至少 30 条政策，且该市有非空 amount）按截面分位给临时 1–4 档。`tier.value` 为该档，`tier.reason` 含 QPOL-02。深圳没有金额时 `tier.value` 仍为 null，`reason` 仍是「无金额列」。支持力度的分数、名次、条数、层级均值公式未改。
- `effect_from_rows`：`implementation_date` 为真实日期（排除空和 `0000-00-00`）时计入启动率；`policy_support` 的「适用对象」或 `support_object` 非空时计入覆盖种类。各维先做城市截面 min-max，缺的维不进平均。没有 `feedback_score` 则反馈维跳过。两维都空时 `computable` 仍为 false，`reason` 仍是「实施日、支持对象、反馈全缺」，不写 `score`。
- `build_shenzhen_board` 改为调用 `effect_from_rows`。`fit_from_rows` 未改。
- `CITY_SECTION_SQL` 增选 `implementation_date`、`policy_support`，仍然不含 `amount` 和 `bid`。

## 测试结果

- 命令：`python -m pytest tests/test_policy_shenzhen_board.py -q`
- 结果：10 passed（含原 `test_tier_not_zero_and_no_composite`，以及新的 `test_amount_and_effect_emit_when_present`）
- 有数样例：深圳金额均值 100，档位 1，落地实效分 75.0
- 无数样例：档位 null，实效不可算，无 score

## 遗留风险

- 政策主表 SQL 不带 `amount`。线上行没有金额字段时，档位仍为 null。金额入库不在本单。
- 1–4 档是临时分位，不是已会签切点。
- 反馈维没有调查表，继续跳过，不补 0。

## CI/CD

- 分支：`lumen-algo-py` `origin/dev`
- 代码 commit：`5ab0d6dc12508644d380455e414846ff477de4a0`
- 推送尖端：`af1db41af92aa9aef6325d0cde5ef477800a0d4d`（并入当时的 `origin/dev`）
- 不推 `main`
- 本地测试已通过。流水线由该仓 dev 推送触发。

## 架构合规

| 项 | 结果 |
|---|---|
| 算法仍在 Python | 是 |
| 不在 Java 里算档位或实效 | 是 |
| 不读 `dwd_bid_*` | 是 |
| 全空不出 0 | 是 |
| 未改前端、未改 `effect.py`、未改链名匹配 | 是 |

## 涉及文件

- `repos/lumen-algo-py/vendor/entan-py/polan/shenzhen_board.py`
- `repos/lumen-algo-py/tests/test_policy_shenzhen_board.py`

## 成本（会话估算）

| 字段 | 值 |
|---|---|
| actual_tokens | 80000 |
| model_used | grok-4.7 |
| actual_cost | 1.5 |
| cost_warn | green |
