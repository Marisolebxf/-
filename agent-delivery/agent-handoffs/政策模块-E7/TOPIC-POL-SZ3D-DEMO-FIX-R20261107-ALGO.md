# TOPIC-POL-SZ3D-DEMO-FIX-R20261107-ALGO · 深圳政策现状结果板是否改公式

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 与数据单同一轮。只判断结果板该不该改。 |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 源列全空时不改公式。改了也要等非空源，本轮不会让演示多出一个数。 |

## 图

不改调用链。`polan/shenzhen_board.py` 的城市截面 SQL 只取 `policy_id, title, rank, province, city, district, region`。档位固定 `{value: null, reason: 无金额列}`。落地实效固定 `computable: false`。

## 运行 2026-11-07

- 缺口键：`shenzhen_board.tier_effect`
- 现况：结果板不读金额，也不取实施日、支持对象、反馈
- 数据单结论：这些源是空的，不是算错
- 动作：不改 `shenzhen_board.py`，不把空列换成 0，不重签 `POLICY-20261107-004`
- 结果：源列一旦有非空值，才需要改结果板去读。本轮没有这种列，任务停在待签收

## 调研 2026-11-07：现有实现与可算条件

监管人要求本单补上：现有算法怎么实现、数据缺什么、什么样的表和数据就能算。下面按代码和口径说明写，不把空值写成 0。

### 现在怎么实现

`polan/shenzhen_board.py` 不读取金额、实施日、支持对象、反馈。

- 城市截面 SQL 只有 `policy_id, title, rank, province, city, district, region`。
- 扶持档位写死 `{value: null, reason: 无金额列}`。
- 落地实效写死 `computable: false`，原因「实施日、支持对象、反馈全缺」。
- 支持力度的分数、名次、条数、层级均值只用来自 `city` 和 `rank`，这两项已经能算。

`polan/eval/effect.py` 的 v2 公式（有效率、力度均值）是展示系统政策实施效果跟踪的临时基线，不覆盖深圳结果板，也不覆盖落地实效正本的三维。本单不把那条公式搬过来。

### 缺什么

| 项 | 表和字段 | 现况 |
|---|---|---|
| 扶持档位 | 政策表没有金额列。`dwd_bid_*` 的金额是招标中标额，不能当扶持金额。`policy_support` 全是 JSON null | 档位置空 |
| 落地实效·启动 | `policy_base_info.implementation_date` 列在，值是 `0000-00-00`。零日期不是空，也不能当成已实施 | 这一维不可算 |
| 落地实效·覆盖 | `policy_base_info.policy_support` 列在，JSON 类型是 null，取不到支持对象 | 这一维不可算 |
| 落地实效·反馈 | 没有调查表。缺了这一维可以不进平均 | 没有表 |

### 有什么就能算

扶持档位要一张新表，不接招标表。一行一条政策：

| 列 | 要求 |
|---|---|
| `policy_id` | 对得上 `policy_base_info.policy_id` |
| `amount` | 数值，非 null。0 只在条款写明金额为 0 时才允许 |
| `caliber` | 补贴、奖励或资助，写明是哪一种 |
| `source_clause` | 金额从哪条政策原文来 |

一座城市至少 30 条政策带非空 `amount`，这座城市才进档位截面。分档切点还没有会签（QPOL-02）。有金额后先出该市非空金额的均值；档位标签用截面分位做临时 1–4 档，结果里带 `pending_ref=QPOL-02`。没有金额的城市档位仍是 null。

落地实效三维持有一维有效值就可以出分，缺的维不补 0、不进平均。

| 维 | 要的数据 |
|---|---|
| 启动 | `policy_base_info.implementation_date` 是真实日期，不是 `0000-00-00`，也不是 NULL。对比城市都要有，才能做截面 |
| 覆盖 | `policy_support` 不是 JSON null，子键「适用对象」或 `support_object` 有非空文本。分数用去重种类数 |
| 反馈 | 单独一张表，至少 `city` 和 `feedback_score`（0–100）。没有这张表时，这一维跳过 |

结果板现在不读这些列。表里有数之后，还要改 `shenzhen_board.py` 才会出结果。没有数时仍不可算。

### 派出的子任务

| ID | 做什么 |
|---|---|
| `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-TIER-DATA` | 只从政策原文或已有非空字段抽取真实金额，写入扶持金额表。没有就停，不拿招标额顶上 |
| `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-EFFECT-DATA` | 只回填已有的真实实施日和非空支持对象。零日期和 JSON null 不改成假值。本轮不建反馈表 |
| `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-BOARD` | 结果板改为：上述数据有非空值才计算；全空仍为 null，不出 0 |

## 架构合规

| 项 | 结果 |
|---|---|
| 算法仍在 Python | 是 |
| 不在 Java 里算档位或实效 | 是 |
| 不出造数分数 | 是 |

后续读数落在 `TOPIC-POL-SZ3D-DEMO-FIX-R20261107-BOARD.md` 的「补读 2026-11-07」。金额表只挂具体资助，发布日副本不进启动率。
