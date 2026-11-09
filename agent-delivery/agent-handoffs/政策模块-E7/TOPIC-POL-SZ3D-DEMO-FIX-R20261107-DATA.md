# TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA · 深圳政策现状档位与落地实效补源

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 验收单裁定档位、落地实效没有结果。本单只核对能不能补到非空源。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A` |
| 说明 | 没有改业务代码，没有写库。 |

## 图

不改调用链。结果板仍读 `demo_gkxlumenx_dwd.policy_base_info`。

## 运行 2026-11-07

- 缺口键：`policy_base_info.support.tier`、`policy_base_info.effect`
- 现况：已签发结果里档位为空，原因「无金额列」；落地实效不可算，原因「实施日、支持对象、反馈全缺」
- 本机再连 `10.50.11.76` 超时，没有第二遍 `SELECT`
- 口径：`metrics/calc-logic/POLICY/M_POLICY_SUPPORT_STRENGTH.md` 写明政策表没有金额列，`policy_support` 全空。`metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md` 写明实施日为零日期、支持对象取不到、没有反馈表，三维都空时分数无定义
- 动作：不写 `policy_base_info`，不写 ODS、正式库、供应方库，不把空写成 0
- 结果：源补不上。任务阻塞，不进入待签收

## 架构合规

| 项 | 结果 |
|---|---|
| 不写 ODS / 正式 DWD / 供应方库 | 是 |
| 不把缺数写成 0 分 | 是 |
| 不签 `LUMEN-POLICY-SZ3D-DATA-DEMO-L01` | 是 |

## 执行 2026-11-07

ponytail: full

直连 `10.50.11.76:3306`，用户 `gkxlumenx`，只读核对正式库 `gkxlumenx_dwd` 与 demo 库 `demo_gkxlumenx_dwd`。没有写库。没有改结果板、算法仓、第 3 章链名匹配、前端或展示系统效果预估。没有签 `LUMEN-POLICY-SZ3D-DATA-DEMO-L01`。

`policy_base_info` 行数：正式库 40000，demo 库 20008。两库 `city='深圳市'` 都是 879 行。

| 位置 | 列或表 | 是否存在 | 非空行数 |
|---|---|---|---|
| 两库 `policy_base_info` | 金额语义列 | 不存在 | 0 |
| 正式库 `policy_base_info` | `implementation_date` | 存在，date | 深圳市 0；全表 40000 行均为 NULL，零日期 0 |
| 正式库 `policy_base_info` | `policy_support` | 存在，json | 深圳市 0（879 行 JSON null）；`support_object` 0，`support_way` 0；全表非空 0 |
| demo `policy_base_info` | `implementation_date` | 存在，date | 深圳市 879 行非零日期，但 879/879 等于 `publish_date`，不是独立实施日 |
| demo `policy_base_info` | `policy_support` | 存在，json | 深圳市 0（879 行 SQL NULL）；`support_object` 0，`support_way` 0 |
| 两库 | `policy_effect_eval` | 表存在 | 0 |
| 两库 | `policy_support_assessment` | 表存在 | 0（`funding_support_score` 等分数列非空 0） |
| 两库 | `policy_support_assessment_indicator` | 表存在 | 0 |
| 两库 | `policy_support_overview` | 表存在 | 0 |
| 两库 | `policy_support_rank` | 表存在 | 0（`fund_scale` 非空 0） |

结果板当前只读 `policy_id`、`title`、`rank`、`province`、`city`、`district`、`region`。这些列里没有金额、实施日、支持对象或反馈。主表也没有同名金额列可补。

没有可映射的非空金额、独立实施日、支持对象或反馈。未执行 INSERT/UPDATE。未把发布日写成实施日，未把空写成 0，未使用招标金额。

任务最终状态：`blocked`。
