# calc-logic/POLICY/ —— 政策域指标计算逻辑真源（王惠口径）

> **真源**：王惠《政策分析指标字段清单》20260829 V2 底稿（Excel 工作底稿，不进 git）。
> **本目录**：底稿经 data-agent 正式化后的 md 文件，供编排智能体按需读取。
> **生成日期**：2026-08-29
> **指标总数**：15 个唯一指标 ID（MODEL 类型）

## 文件清单

| # | 指标ID | 指标名称 | 算法类型 | 文件 |
|---|--------|---------|---------|------|
| 1 | `M_POLICY_EFFECT_SCORE` | 政策效果评分 | MODEL | [M_POLICY_EFFECT_SCORE.md](./M_POLICY_EFFECT_SCORE.md) |
| 2 | `M_POLICY_FOCUS_INDEX` | 政策焦点指数 | MODEL | [M_POLICY_FOCUS_INDEX.md](./M_POLICY_FOCUS_INDEX.md) |
| 3 | `M_POLICY_IMPLEMENTATION_EFFECT` | 落地实效性 | MODEL | [M_POLICY_IMPLEMENTATION_EFFECT.md](./M_POLICY_IMPLEMENTATION_EFFECT.md) |
| 4 | `M_POLICY_INDUSTRY_FIT` | 产业适配性 | MODEL | [M_POLICY_INDUSTRY_FIT.md](./M_POLICY_INDUSTRY_FIT.md) |
| 5 | `M_POLICY_INTENSITY_INDEX` | 政策力度指数 | MODEL | [M_POLICY_INTENSITY_INDEX.md](./M_POLICY_INTENSITY_INDEX.md) |
| 6 | `M_POLICY_INTENSITY_SCORE` | 政策力度评分 | MODEL | [M_POLICY_INTENSITY_SCORE.md](./M_POLICY_INTENSITY_SCORE.md) |
| 7 | `M_POLICY_DEEP_166_1` | 政策焦点识别模型 | MODEL | [M_POLICY_DEEP_166_1.md](./M_POLICY_DEEP_166_1.md) |
| 8 | `M_POLICY_DEEP_167_1` | 政策力度评估模型 | MODEL | [M_POLICY_DEEP_167_1.md](./M_POLICY_DEEP_167_1.md) |
| 9 | `M_POLICY_DEEP_168_1` | 政策效果评估模型 | MODEL | [M_POLICY_DEEP_168_1.md](./M_POLICY_DEEP_168_1.md) |
| 10 | `M_POLICY_DEEP_169_1` | 政策短板识别模型 | MODEL | [M_POLICY_DEEP_169_1.md](./M_POLICY_DEEP_169_1.md) |
| 11 | `M_POLICY_DEEP_170_1` | 政策机遇识别模型 | MODEL | [M_POLICY_DEEP_170_1.md](./M_POLICY_DEEP_170_1.md) |
| 12 | `M_POLICY_DEEP_171_1` | 政策布局推荐模型 | MODEL | [M_POLICY_DEEP_171_1.md](./M_POLICY_DEEP_171_1.md) |
| 13 | `M_POLICY_DS_07_POLICY_GUARD_001` | 发展战略引导力评估 | MODEL | [M_POLICY_DS_07_POLICY_GUARD_001.md](./M_POLICY_DS_07_POLICY_GUARD_001.md) |
| 14 | `M_POLICY_DS_07_POLICY_GUARD_008` | 政策与条件保障力综合评估 | MODEL | [M_POLICY_DS_07_POLICY_GUARD_008.md](./M_POLICY_DS_07_POLICY_GUARD_008.md) |
| 15 | `M_POLICY_DS_11_POLICY_EVAL_012` | 智能摘要与结论推送 | MODEL | [M_POLICY_DS_11_POLICY_EVAL_012.md](./M_POLICY_DS_11_POLICY_EVAL_012.md) |

## 维护规则

1. **口径变更流程**：王惠更新 Excel 底稿 → data-agent 重新生成对应 md → commit 标注「正式化自 王惠 政策分析 20260829 V2 底稿」。
2. **与 seed yaml 的关系**：`cfg_metric-POLICY-seed.yaml` 中 `calc_logic_ref` 指向本目录 md 文件。
3. **文件命名**：`{metric_id}.md`，与 `metric_id` 一一对应。
4. **算法库模型身份**：`M_POLICY_DEEP_*` 为算法库深度分析模型身份（与 `M_POLICY_FOCUS_INDEX`/`INTENSITY_SCORE`/`EFFECT_SCORE` 同维同词表，多数「原型页不挂本 metricId」）；`M_POLICY_DS_*` 为科技信息展示系统缺口身份（PG-D01 / PG-D07 / EVAL-012）。
