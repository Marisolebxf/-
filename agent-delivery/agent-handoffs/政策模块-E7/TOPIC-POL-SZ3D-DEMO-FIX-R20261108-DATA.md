# TOPIC-POL-SZ3D-DEMO-FIX-R20261108-DATA · 恢复深圳 879 基线（调查结论：数据侧不可修）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| 状态 | `blocked`（等监管人拍板读取口径，见结论） |

## Ponytail

| 字段 | 值 |
|---|---|
| ponytail | `full` |
| 说明 | 本轮零代码、零写库。结论是「不动数据」，调查证据如下。 |

## 背景

LOOP 验收轮（2026-11-08 凌晨）发现：接口 `POLICY-20261107-009/011` 三卡仍绿（16:01/16:44 旧基线快照），但库已回归。按 LOOP §4 建 DATA 单调查。

## 库证据（全部只读 SELECT，10.50.11.76）

- 存活总数 20666（基线时 20008）。
- `city='深圳市'` 1458 行 = 原生 879（`etl_batch_id IS NULL`、`source_plane='domestic'`）+ 一张图调试 540（`etl_batch_id='debug_one_map_20261107_v1'`、`source_plane='debug'`）+ 图2 合成 49（批次 `SYNTH-*`，`source='llm-synth'`）。
- 原生 879 行 rank 分布未动：`["市级"]`757 / `["区级"]`96 / `["园区级"]`26。按 `shenzhen_board._LEVEL_W`（市级 0.5、区级区县级园区级 0.25）算均值 = 0.4653 ✓。
- 1458 行全量均值 = 564.75/1458 = **0.3873** ✗（区县级 553、市级 34、园区级 2 来自非原生行）。下次重算 count=1458、level_mean=0.3873，必红。
- 无城市名行从上一轮记录的 9713 降到 46：16:44 之后有会话对全表做了城市回填，约 9667 行（非深圳）新增城市值。这些行是原生 domestic 行，无批次标记。下次重算的城市截面还会变，score 33.5585 / 名次 5 也对不上。

## 归属确认（不删别人演示的数据）

| 批次 | 归属 | 证据 |
|---|---|---|
| debug 540 | 深圳一张图调试（`SYSINT-04-01-DATA-EMP-L01`，human:徐滕强 会话灌数） | `agent-handoffs/系统集成-SYSINT/SYSINT-04-01-DATA-EMP-L01.md`：`policy_base_info` 540 行，ID 前缀 `DEBUG-ONEMAP-`，12 产业×9 区×5 年 |
| SYNTH 49 | 图2 政策 Mock（`POL-L2-DS10-SRCMON-SYNTH-L01`） | handoff：D16 例外由 `human:淮政玮` 2026-11-07 批准，合成行「检索与统计计入」，删除走三标记协议（`SYN%`+`llm-synth`+`SYNTH-*`） |
| 城市回填 ~9667 行 | 执行会话未查明（registry 按城市关键词未命中对应任务） | 16:44 后发生；原生行 updated_time 变为 11-07 |

此前展示系统侧曾按用户指令删过一次 debug 540（备份在当时的 agent store），之后另一会话 18:39 重灌。再次物理删除 = 与在跑会话互相清数据，违反多会话保护铁律。

## 结论：数据侧不可修

- 删 debug 540 → 破坏一张图演示。
- 删 SYNTH 49 → 破坏图2 演示，且违背已批准的 D16 例外语义。
- `is_deleted=1` 隔离或改 city/source_plane → 同样破坏上述两个演示的读取。
- 城市回填行无批次标记，无法按批次恢复截面。
- 原生 879 行本身没坏；坏的是「全表截面」这个读取口径在共表演示环境下不再稳定。

## 建议（待 human:淮政玮 拍板，二选一或另定）

1. **读取侧收窄（推荐）**：`shenzhen_board` 的 `CITY_SECTION_SQL` / `_GRANT_AMOUNT_SQL` 加原生过滤（`source_plane='domestic' AND etl_batch_id IS NULL`），LOOP 计划 §1 的库核对行同步改口径。可精确恢复 count=879、level_mean=0.4653；score/rank 仍会因城市回填漂移，需接受新值或一并限定基线城市集合。这是 ALGO 代码改动 + 口径修订，拍板后另派 ALGO 单。
2. **放宽通过线**：接受共表演示数据的现状，把 879/0.4653 改成动态基线（如「原生 879 不变、count 允许 ≥879、均值按当批重算」）。

拍板前本单 `blocked`，不动库、不动代码、不建 ALGO 单（避免预设口径决策）。

## 架构合规自检

- D12 demo 沙箱：✅ 只读 demo 库。
- D16：✅ 未写 gapfill，未写 0。
- 多会话保护：✅ 未删除/未隔离任何其他会话的数据行。
- 正式库只读：✅ 全程 SELECT/SHOW。
