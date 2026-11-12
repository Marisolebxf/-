# POL-L2-DS10-CMP-213-ANALYSIS-FDE · A 波次 · product

- 总单：`POL-L2-DS10-CMP-213-ANALYSIS-FDE`
- 日期：2026-11-12
- 身份：product
- 裁定真源：监管人确认计划「Python LLM 写 gapfill → 展示只读」；废止 COVER-FDE「213 非独立分析列」

## 1. 功能点 · 界面必见

| 分句 | 界面必见 | 空态 / 失败 |
|---|---|---|
| 213-3 变化统计与分析 | 新旧对比 live：查询出 diff 行后，同屏见标题「变化统计与分析」、三色 Tag（新增/修改/删除计数）、一句演变趋势说明（`analysis_text`） | 无 diff 行 → 整块空；有 diff 但无分析文 → Tag 仍见，分析文位空态「暂无演变趋势说明」，不造假趋势句 |

## 2. 状态清单

| 状态 | 表现 |
|---|---|
| 未点查询 | 无统计块 |
| 有 diff + 有分析文 | Tag + 一句趋势说明（含两时点日期） |
| 有 diff + 无分析文 | Tag + 空态一句 |
| 读失败 | Alert；保留已读行 |

## 3. 影响清单

| 层 | 影响 |
|---|---|
| 说明书 / 四单 | 回写 213-3：Tag + 分析文；废止「非独立分析列」 |
| gapfill | 新表 `gapfill_policy_version_analysis` |
| Python | `/internal/policy/version-analysis/enrich`（LLM 写表）；synth 挂写 |
| element / display | `version-diff` 透传 `analysis_text` |
| FE | live 补齐「变化统计与分析」块 |
| 合规用例 | 形态期望补非空分析说明 |

## 4. 废止声明

COVER-FDE A 波次「213：变化统计 = diff 行聚合，非独立分析列」**废止**。现行口径：计数仍由 diff 聚合；**配对级分析文**独立落 `gapfill_policy_version_analysis`，由 LLM（或 seed 预灌）写入，读面只读。
