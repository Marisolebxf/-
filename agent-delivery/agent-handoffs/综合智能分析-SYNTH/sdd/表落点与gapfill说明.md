# 综合智能分析 · 表落点与 gapfill 说明

- 日期：2026-11-05（对齐总册 v1.0-draft）
- 配套：`综合智能分析-系统详细设计说明书.md` §11
- 状态：DRAFT

## 1. 本质区别（定稿口径）

| | **gapfill**（D16） | **`*_ai` 库** |
|---|---|---|
| 一句话 | **真源缺失**（没有正式口径/源列/源行），但需规仍要求有这块能力 → 用独立库表做**合规用 mock 承载** | **真能生产出来的算法指标结果表**；库表是正式产出面，只是运算暂时没跑（或行暂时空/预填） |
| 性质 | 「没有真源，为过需规而 mock 的表」 | 「有真生产路径的表，算子尚未接通」 |
| 库 | `gkxlumenx_gapfill` | demo：`demo_gkxlumenx_ai`；正式：`gkxlumenx_ai` |
| 表名 | 必须以 `gapfill_` 开头（血缘 §2.4），如 `gapfill_synth_rd_employee` | **不加** `gapfill_` / **不加** `ai_` 前缀（库名已标识）；域前缀 `synth_`，如 `synth_vit_index` |
| 换真源后 | 停读该 gapfill 表；行**不并入** ODS/DWD/供应方 | 算子接通后写同一张表；D4 可按实算改 live |
| 生产配置 | **不读** gapfill 库 | 正式环境读 `gkxlumenx_ai` |

二者**不是**「一个假一个真」的程度差，而是：

- gapfill：**源侧不可能先有正式数**（缺口径/缺源），表本身就是缺项补位；
- `_ai`：**设计上就是算法产物落点**，假的只是「还没算」，不是「永远没有真源」。

## 2. gapfill 举例（本模块已有）

活力三个输入缺项（真源无列）：

- `gkxlumenx_gapfill.gapfill_synth_new_product_sales_ratio`
- `gkxlumenx_gapfill.gapfill_synth_rd_employee`
- `gkxlumenx_gapfill.gapfill_synth_policy_effect`

命名已对齐：`gapfill_` + 域 `synth_` + 缺项语义。存量 `LUMEN-INTEL-VIT-GAPFILL-*` 继续有效。

## 3. `_ai` 表命名规范（本模块）

对齐现网习惯：

- gapfill：`gapfill_{域}_{语义}`（见政策 `gapfill_policy_*`、综合 `gapfill_synth_*`）
- 产业链 ADS 结果：业务语义表名，**库名分层、表名不再叠库前缀**
- 综合 `_ai`：**库 = `gkxlumenx_ai`，表 = `synth_{叶缩写}_{语义}`**

| 规则 | 做 | 不做 |
|---|---|---|
| 库 | `demo_gkxlumenx_ai` / `gkxlumenx_ai` | 写进 ODS/DWD/ADS/供应方冒充贴源 |
| 表前缀 | `synth_` | `ai_synth_`（与库名重复）、`gapfill_`（性质错库）、`ads_`（本落点不在 ADS） |
| 叶缩写 | `vit` / `elem` / `collab` | 中文拼音混用、随意缩写 |
| 引用全文 | `gkxlumenx_ai.synth_vit_index` | 口头简称漏库名 |

建议表名见说明书 §11.3（已按本规范改掉草稿里的 `ai_synth_*`）。

`entan` 侧 `TABLE_MAP: metric_id → 表名` 建成后登记短表名（如 `synth_vit_index`），连接串指向 `*_ai` 库。

## 4. 代码与数据

- **代码**：一律真路径（SELECT / 装包 / Feign）。`USE_MOCK=false` 禁止前端 fixture。
- **gapfill 行**：内容是 mock 补位，带 `gap_item` / `fill_method` / `gapfill_batch_id`。
- **`_ai` 行**：结构按生产表；运算未上时允许空表或预填，预填须 `is_mock` / `calc_batch_id` 可区分；接通实算后写同表并收敛批次前缀。

## 5. 和 D18 的关系

D18「做不到真算时建表、灌行、接口读表」在本模块落点优先解释为：**落在 `*_ai` 的生产表结构上**（可先空/预填），而不是再造一套 gapfill 结果表。  
只有「真源永远没有、仅为需规占位」的输入，才进 gapfill。
