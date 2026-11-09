# SYSINT-06-05-L01 · 市场研究宏观行业同步（CDC 预填阶段）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full`（脚本只做最小通用化，企业包 v2 重解析 wave_a/wave_b 与既有 inventory 一致） |

## 状态说明

**本叶未完成。** 只完成 CDC 预填草稿。Wave A/B 回传与 ②a ADS 仍待 GDF；DoD「执行结果回传后 Java 只读 ADS」未满足，不是跑通。

## 修改内容

- 预填产物：`agent-delivery/data/GDF/派单包/宏观行业/GDF-MACRO-WORKPACK-v1/预填作业/`
  - `1、贴源_预填-DRAFT.xlsx`（6 表，抽取过滤为空）
  - `2、明细数据_预填-DRAFT.xlsx`（6 表，维度先于事实）
  - `inventory.json`、`GENERATION-REPORT.md`
- 模板来源：宏观包无模板，仅借 `企业/GDF-ENT-WORKPACK-v1/执行结果/` 两张模板的布局壳，内容全部清空重写。
- 脚本：`scripts/gdf-cdc/parse_workpack.py`、`fill.py` 通用化（识别宏观 02/09 格式、过滤与业务主题参数化）。

## 待 GDF 导入核对

1. `macro_index_data` 四个派生列（`area_resolve/city_code/city_name/province_code`）预填仅 `NULL` 占位，须按 09 §3.1.1 实现。
2. 类型列为默认 VARCHAR，以 `10-DWD-MySQL-DDL/` 预建表为准。
3. `SRC_ENT` / `MACRO` 字典值、作业频率、事实表增量配置需确认。
4. 完整清单见 `预填作业/GENERATION-REPORT.md`。

## 遗留风险

- 未在 GDF 实际导入验证；预填表只做了与 09 的字段数、顺序、过滤抽检。
- 派生列未实现前不得投产。
