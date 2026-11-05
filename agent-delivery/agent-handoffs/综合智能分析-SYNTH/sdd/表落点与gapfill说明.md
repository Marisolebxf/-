# 综合智能分析 · 表落点与 gapfill 说明

- 日期：2026-11-05（对齐总册 v1.0.5-draft）
- 配套：`综合智能分析-系统详细设计说明书.md` §11
- 状态：DRAFT

## 1. 本质区别（定稿口径）

| | **gapfill**（D16，只作输入） | **ADS 结果表**（D18） |
|---|---|---|
| 一句话 | 已登记的输入缺项 | 做不到真算或真查时，新建 ADS 表，Python 灌行，接口只读 |
| 库 | `gkxlumenx_gapfill` | demo：`demo_gkxlumenx_ads`；正式：`gkxlumenx_ads` |
| 本模块 | 只有活力三张既有输入 | `synth_*` 指标、图事实、`synth_collab_batch_meta` |
| 禁止 | 把图谱查询结果放进 `gapfill_` | 把本模块结果放进 `gkxlumenx_ai`、ODS、DWD、供应方库 |

gapfill 只补已登记的输入缺项。结果和图谱演示都不进 gapfill。做不到真算时，mock 行进 ADS。

## 2. gapfill 举例（本模块已有）

活力三个输入缺项（真源无列）：

- `gkxlumenx_gapfill.gapfill_synth_new_product_sales_ratio`
- `gkxlumenx_gapfill.gapfill_synth_rd_employee`
- `gkxlumenx_gapfill.gapfill_synth_policy_effect`

命名已对齐：`gapfill_` + 域 `synth_` + 缺项语义。存量 `LUMEN-INTEL-VIT-GAPFILL-*` 继续有效。

## 3. 表名

| 规则 | 做 | 不做 |
|---|---|---|
| 结果库 | `demo_gkxlumenx_ads` / `gkxlumenx_ads` | `gkxlumenx_ai` |
| 表前缀 | `synth_` | `gapfill_`（结果与图）、`ai_synth_` |
| 引用 | `gkxlumenx_ads.synth_vit_index` | 漏库名 |

表清单以总册 §11.3 为准。

## 4. 代码与数据

- **代码**：一律真路径（SELECT / 装包 / Feign）。`USE_MOCK=false` 禁止前端 fixture。
- **gapfill 行**：内容是 mock 补位，带 `gap_item` / `fill_method` / `gapfill_batch_id`。
- **ADS 行**：预填须 `is_mock=1`。装包只读表，缺行不填常量。

## 5. 和 D18 的关系

做不到真算或真查时，新建 ADS 表，Python 灌 mock 行，接口只读该表。该表不是 `gapfill_`。本模块不再把 `*_ai` 当作 D18 的替代落点。图谱无真源时返回空图，不把演示行放进 gapfill。
