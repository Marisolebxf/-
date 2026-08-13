# CDC 校准生成报告（v1）

- 工作包: `agent-delivery/data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1`
- Wave A 表: 40（P0=17）；索引按 `02` + 校准规则重填
- Wave B 目标表: 17（`09` v3 解析；字段事件见 `scripts/gdf-cdc/v1_calibrate_catalogs.json`）
- 产出: `校准生成/1、贴源_模板.xlsx` / `2、明细数据_模板.xlsx`
- 对照: `执行结果/` ；`DIFF.md` **total_diffs=0**

## 这不是要投递给 GDF 的新执行结果

只用于验证技能能从空壳复现 v1 回件。未写入 `执行结果/`。

## 填写方式

- 克隆 CDC 壳后**先清空全部格子**，再写入。
- Wave A：`02` yaml 顺序 + 缺表/末行经营信息/无过滤/三张转换页。
- Wave B：数据结果页左右栏拉链；`09` v3 无逐列的部分用校准目录事件。

## warnings

- workpack marked 已作废 — 仅 `--calibrate` 允许生成
- enterprise_risk_summary: v1 宽表预聚合（校准复现；v2 不得照抄）
