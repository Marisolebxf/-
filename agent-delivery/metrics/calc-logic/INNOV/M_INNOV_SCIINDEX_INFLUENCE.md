# 科技影响力趋势（M_INNOV_SCIINDEX_INFLUENCE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCIINDEX_INFLUENCE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCIINDEX_INFLUENCE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCIINDEX_INFLUENCE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCIINDEX_INFLUENCE |
| 指标名称 | 科技影响力趋势 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统／科技发展态势／科技创新评估 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 影响力趋势图、领域并排对比 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_SCIINDEX_INFLUENCE.md` |

## 口径定义

结构口径的影响力指数从 2021 年的 **100.00** 降到 2023 年的 **95.22**（净 **−4.78%**，年均 **−2.42%**），跌幅几乎全部来自论文规模（**0.8714**），机构多样性几乎不动（**0.999715**）、前沿占比小幅回落（**0.9911**）；被引口径因 2021—2023 覆盖率仅 **0.31%**（62 / 19,740）而不能用于趋势，只能给 2014—2015 成熟队列的存量锚点 **CPP 16.35**。

## 计算逻辑说明

```text
index_t = 100 · (scale_t/scale_2021 · div_t/div_2021 · front_t/front_2021)^(1/3)
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCIINDEX_INFLUENCE.md` §二（M_INNOV_SCIINDEX_INFLUENCE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_zh_author`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：结构口径的影响力指数从 2021 年的 **100.00** 降到 2023 年的 **95.22**（净 **−4.78%**，年均 **−2.42%**），跌幅几乎全部来自论文规模（**0.8714**），机构多样性几乎不动（**0.999715**）、前沿占比小幅回落（**0.9911**）；被引口径因 2021—2023 覆盖率仅 **0.31%**（62 / 19,740）而不能用于趋势，只能给 2014—2015 成熟队列的存量锚点 **CPP 16.35**。
- **基期声明**：专利表 2017—2020 零行；2024 论文断点、2025—2026 申请人分年缺失。结构指数以 2021 为基年，只用 2021—2023 三个可比年。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCIINDEX_INFLUENCE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCIINDEX_INFLUENCE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCIINDEX_INFLUENCE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

