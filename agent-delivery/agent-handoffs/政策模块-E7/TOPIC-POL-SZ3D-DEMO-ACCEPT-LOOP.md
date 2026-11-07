# TOPIC-POL-SZ3D-DEMO-ACCEPT-LOOP · 深圳政策现状演示实例反复验收

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:qa-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-11-07 第一轮探测后，监管人裁定档位和落地实效没有结果不算通过。验收单仍留在 `ready`，不签完成。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `N/A` |
| 说明 | 本轮只读接口和库，没有改业务代码。 |

## 图

本轮不改调用链，没有图。

## 运行 2026-11-07

- 用例真源：`agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-SZ3D-DATA-DEMO-L01.md`
- 锚点：`industry_vid=chain:INB1303`
- 库：只读 `demo_gkxlumenx_dwd.policy_base_info`。未删除行 20008；`city='深圳市'` 879；这 879 行的 `rank` 都有值；无城市名 9713
- 样本满足：否（2026-11-07 监管人裁定：扶持档位、落地实效没有结果，不能算通过。下面「运行 2026-11-07 第二轮」是按这个裁定补上的）
- 停止：继续
- 探测：`GET http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks/POLICY-20261107-004/result`。不带 `user_id` 时 HTTP 200、`code=1`、`msg=未获取到当前用户`。按结果接口的实际参数加上 `user_id=guest` 后 HTTP 200、`code=0`，任务状态 `success`。没有新签发任务
- 结果：支持力度可算；条数 879；分数 33.5585；名次 5；层级均值 0.4653；档位原因「无金额列」，分值空。第 4 章不可算，原因「实施日、支持对象、反馈全缺」。第 5 章有供给结构，条数与分数同上。`honesty.source=dwd`，`fabricated=false`
- 第 3 章仍是「未提供链名」。留在缺陷包 `LUMEN-POLICY-SZ3D-E1-DEFECT-C1.md`，本轮不建查询单
- 子任务：见第二轮。本段只记录探测结果，裁定后改为不通过

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `policy_base_info.support.tier` | DATA | 档位值为空，原因「无金额列」 | 有结果，且不是把空写成 0 | 先核对政策表有没有非空金额或档位；没有则不能造 | `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA` |
| `policy_base_info.effect` | DATA | 第 4 章不可算，原因「实施日、支持对象、反馈全缺」 | 可算并有结果，且不是 0 分充数 | 先核对实施日、支持对象、反馈有没有非空源；三维都空则分数无定义 | `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA` |
| `shenzhen_board.tier_effect` | ALGO | 结果板不读金额、不取落地实效，原因写死 | 源列已有非空值时要按列算；源列全空时仍不可算，不得出 0 | 本轮源列没有非空值，不改公式出假分 | `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-ALGO` |

## 运行 2026-11-07 第二轮

- 用例：`agent-delivery/工程过程/04-系统集成/03-专题系统集成/编排计划/深圳政策现状分析-LOOP计划.md` 第 1 节（裁定后的通过线）
- 库：本轮没有再连上 `10.50.11.76`（连接超时）。现况以已签发结果和口径说明为准：`metrics/calc-logic/POLICY/M_POLICY_SUPPORT_STRENGTH.md`、`metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md`
- 样本满足：否
- 停止：重复缺口
- 子任务已建。数据单做了源核对，没有改库。算法单核对了结果板，没有改代码。没有把空写成 0
- 口径说明：政策表没有金额列，`policy_support` 全空；实施日是零日期，支持对象取不到，两库没有反馈表。三维都空时分数无定义。强行出 0 会把缺数写成政策事实
- 数据单 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-DATA` 因此停在阻塞：没有可回填的非空源。算法单 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-ALGO` 停在待签收：源列全空时改公式也出不了数
- 不重读 `POLICY-20261107-004`。库和代码都没变，结果不会变
- 同一缺口键还在。本轮不再新建第三张单。要在演示里出现数字，只能另建带 mock 标签的缺项表并让结果板去读，不能写进 `policy_base_info`。这一步等 `human:淮政玮` 点头

### 缺口

| 缺口键 | 类 | 现况 | 预期 | 建议 | 挂到任务 |
|---|---|---|---|---|---|
| `policy_base_info.support.tier` | DATA | 仍无金额源 | 有结果，不写 0 | 等监管人决定是否另开有标签的演示缺项表。不写进 `policy_base_info` | 已挂数据单，不新建 |
| `policy_base_info.effect` | DATA | 实施日、支持对象、反馈仍全缺 | 可算并有结果，不写 0 | 同上 | 已挂数据单，不新建 |
