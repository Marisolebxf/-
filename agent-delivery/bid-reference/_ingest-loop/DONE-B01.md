# DONE B01 · 覆盖率对账

| 项 | 值 |
|----|----|
| role | Wave B coverage |
| DONE-A01 … DONE-A18 | 18/18 均存在 |
| written_leaves 加总（DONE 表） | **2315** |
| srs 树 `###` 叶子实点 | **2315**（8 系统目录 walk） |
| expected `SOURCE.yaml data_rows_total` | 2315 |
| 系统 README.md | 8/8 存在 |
| officecli 抽检 | **24/24 PASS**（每系统 3 行，首/中/末 excel_row） |
| SOURCE.yaml status | **coverage_ok**（未改 cutover） |
| scope-baseline.yaml | **未改** |
| 旧招标 MD | **未删** |
| git | 未 commit / 未 push |

## Wave A 分叶加总

| ID | written_leaves |
|----|----------------|
| A01 | 285 |
| A02 | 196 |
| A03 | 102 |
| A04 | 87 |
| A05 | 125 |
| A06 | 63 |
| A07 | 45 |
| A08 | 151 |
| A09 | 174 |
| A10 | 141 |
| A11 | 239 |
| A12 | 79 |
| A13 | 116 |
| A14 | 143 |
| A15 | 130 |
| A16 | 146 |
| A17 | 84 |
| A18 | 9 |
| **合计** | **2315** |

独立 walk：01=285，02=769，03=174，04=459，05=116，06=419，07=9，08=84。

## 抽检（officecli `view text --range`，只读）

需规列：多数表 **M**；深度挖掘 **N**；超大规模智算引擎 **N**；亿级图谱 13 列 **M**。  
对比：MD「需规功能描述」与单元格原文（去叶子后多余 `---` 分隔）。Excel 未 set/add。

| 系统 | sheet | 列 | excel_row | 结果 |
|------|-------|----|-----------|------|
| 01 | 智慧服务门户系统 | M | 4, 146, 288 | PASS |
| 02 | 科技信息展示系统 | M | 4, 388, 772 | PASS |
| 03 | 新型高端智库系统 | M | 4, 91, 177 | PASS |
| 04 | 科技专题服务系统 | M | 4, 233, 462 | PASS |
| 05 | 深度挖掘算法 | N | 4, 62, 119 | PASS（含 N4 6046 字长文） |
| 06 | 超大规模智算引擎 | N | 4, 213, 422 | PASS |
| 07 | 亿级科技知识图谱引擎 | M | 4, 8, 12 | PASS |
| 08 | 科技情报挖掘与知识服务 | M | 4, 46, 87 | PASS |

## gaps（不阻断 coverage_ok）

- Wave A 已登记：招标描述空行写「（本行空）」+ inherited；六级 `/` 占位保留；门户 M14 源截断等。抽检未复现「MD 改写需规正文」。
- 父 README 完整度不齐：`02`/`04`/`06` 系统 README 仍标 `状态：empty`（仅模块期望行表，缺四级文件闭区间明细）；子目录 README 多数已写。未在本叶补写（B01 范围是对账，不是回填 A 叶 README）。
- `SOURCE.yaml` 原 `common_14col` 把智算需规写成 M；抽检确认智算为 **N**。已加 `compute_engine_14col` 注释，未改 cutover。
- 与 62 叶子基线的差异见 [`MEMO-vs-62-baseline.md`](./MEMO-vs-62-baseline.md)（只记录）。

## 已改文件

- `srs/INDEX.md`：状态 `coverage_ok` + 八系统 README 链接
- `srs/SOURCE.yaml`：`status=coverage_ok`；智算列注
- `bid-reference/README.md`：顶部「srs 覆盖已对账，待人宣布 cutover」
- `_ingest-loop/MEMO-vs-62-baseline.md`
- 本文件

**cutover：否。等人宣布。**
