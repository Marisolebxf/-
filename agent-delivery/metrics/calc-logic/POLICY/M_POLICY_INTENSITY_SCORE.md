# 政策力度评分（M_POLICY_INTENSITY_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_INTENSITY_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_INTENSITY_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_INTENSITY_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_INTENSITY_SCORE |
| 指标名称 | 政策力度评分 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 政策详情页「政策力度」刻度条（设计位）、政策库列表「力度」排序列（设计位） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_INTENSITY_SCORE.md` |

## 口径定义

五项子指标要四个字段：`implementation_date`、`policy_support.support_way`、`policy_support.support_object`、`policy_support.support_behavior`，外加 `district`。前四个**全部为空**（日期是零值、JSON 是 null），只有 `district` 有 1,165 行。三维里效果与成本两维整块空、覆盖维只剩半个子项，**没有一个完整维**，按正本「缺维不进平均」的规则，可进平均的维为 0，分数不存在。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_INTENSITY_SCORE.md` §二（M_POLICY_INTENSITY_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_`
- `dwd_global_policy_base`
- `dwd_global_policy_base_bak_20260923`
- `dwd_policy_base`
- `dwd_policy_base_bak_20260923`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：五项子指标要四个字段：`implementation_date`、`policy_support.support_way`、`policy_support.support_object`、`policy_support.support_behavior`，外加 `district`。前四个**全部为空**（日期是零值、JSON 是 null），只有 `district` 有 1,165 行。三维里效果与成本两维整块空、覆盖维只剩半个子项，**没有一个完整维**，按正本「缺维不进平均」的规则，可进平均的维为 0，分数不存在。
- **基期声明**：截面件：本件不出分、不设基期。政策池为 20,000 条存量全表；若将来补数后要按年出分，须先解决 2023/2024 的采集断档，否则「某年力度为 0」会是断档而不是真实归零。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_INTENSITY_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_INTENSITY_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_INTENSITY_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

