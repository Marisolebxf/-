# 创新要素关联（专利—论文—政策同城同年共现）（M_INNOV_FACTOR_RELATION）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_FACTOR_RELATION.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_RELATION.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_RELATION_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_FACTOR_RELATION |
| 指标名称 | 创新要素关联（专利—论文—政策同城同年共现） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技创新评估 |
| 二级模块 | 要素关联 |
| 更新频率 | 待确认 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_FACTOR_RELATION.md` |

## 口径定义

共现 = 同一城市同一年份三类要素的计数同时>0；关联强度用 Pearson/Spearman/余弦，去城市均值后看年际同向；共现不是合作、不是因果。

> 一句话口径（源件 §0.3）：本件在 4 市 × 4 年（深圳、广州、东莞、惠州，2021—2024）上构建城市年面板：专利—论文两要素 16 个城市年，三要素（加政策）只有 6 个城市年。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_FACTOR_RELATION.md` §二（M_INNOV_FACTOR_RELATION.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_patent`
- `dwd_policy_base`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件在 4 市 × 4 年（深圳、广州、东莞、惠州，2021—2024）上构建城市年面板：专利—论文两要素 16 个城市年，三要素（加政策）只有 6 个城市年。
- **基期声明**：专利侧只覆盖 2021—2026（2017—2020 零行）；论文侧 2024 是采集批次峰（32.09%），2025/2026 为滞后/残年；政策侧 2023/2024 城市标签为 0。因此两要素矩阵用 2021—2024，三要素矩阵只用 2021—2022。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_FACTOR_RELATION.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_RELATION.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_RELATION_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

