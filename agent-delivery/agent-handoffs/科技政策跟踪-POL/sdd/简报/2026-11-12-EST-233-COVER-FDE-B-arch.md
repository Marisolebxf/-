# POL-L2-DS12-EST-233-COVER-FDE · B 波次 · arch

- 总单：`POL-L2-DS12-EST-233-COVER-FDE-L01`
- 日期：2026-11-12
- 身份：arch（本会话代写；监管人要求同窗连跑）
- 承接：A 产品稿；卡1=A / 卡2=A

## 定档

**中档**。缺项表 ALTER 两列 + 扩 `time_trend_text` 格式；SELECT 扩列；不新 `metric_id`；D4 仍 mock；不退定义规程。

## 读法（采纳 A §5 方案 1）

| 列 | 约定 |
|---|---|
| `similar_items` | `名称|匹配|效果；…` ≥2 |
| `term_kpi_text` | `短期|gdp|产业|科创；中期|…；长期|…` |
| `time_trend_text` | `2026-06月45/85、…`（/后为置信度百分数） |
| `industry_text` | 仅柱图名+分；不兼 KPI |
| `similar_basis_text` | 可选总述；界面列表以 `similar_items` 为准 |

## 要动的层

- DATA / ARCH / 说明书：已回写
- API：element `FORECAST_COLUMNS` 加 `similar_items, term_kpi_text`
- gapfill SQL + `simulation.py` upsert 列
- FE：解析 + 真轨左栏 + 置信度 tooltip
- 合规用例 233 行：已冻列表 / KPI / 置信度

## B 收口

下一步 D 实现已同窗推进；C 会签以说明书差表 + DATA 修订为据，本窗不另开对抗会话（监管人显式同窗完成）。
