# 要素分项指标值与得分（M_SYNTH_ELEM_INDICATOR）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_INDICATOR.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_INDICATOR.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_INDICATOR_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_ELEM_INDICATOR |
| 指标名称 | 要素分项指标值与得分 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新要素分析／创新要素数据汇聚 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_ELEM_INDICATOR.md` |

## 口径定义

叶子的**结构与算法**都不缺：极值归一、维内均值、三层聚合三步在本批 4 城上全部闭合（面板 `checks.z_range` 为 true、`type_index_is_dim_mean` 为 true）。卡住的是**三个叶子的数据面**：研发人员占比的分子列 `development_employee` 在 90,926 行年报里 0 行有值（列建好、未灌数），创新空间面积与创新空间密度两格在 gkx 全库列名字典里检索 `%space%area%`／`%park_area%`／`%regional_area%`／`%land_area%` 返回 0 行。这不是「覆盖低」，是「没有」。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_INDICATOR.md` §二（M_SYNTH_ELEM_INDICATOR.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_heis`
- `dwd_macro_index_data`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_org_product_info`
- `dwd_patent`
- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：17 个类型叶子中 7 个直读（ok）、5 个代理（proxy）、1 个退化（degenerate）、1 个样本不足（insufficient）、3 个无承载（missing），进加权 12 个；7 个类型维中 6 个可算（创新人才维全缺），5 个领域维中 3 个可算。缺的部分不是覆盖率低，是列建好未灌数（development_employee 0/90,926）或全库无此列（空间面积/区域面积），故只能判部分支持。
- **基期声明**：统计年=2024（专利授权、年报、融资完成日、论文、政策存量五类源里唯一完整的年）。2021—2023 未入集不是缺数，是本族按要求做单年截面；2025 专利与年报尚未完整、2026 为残年（专利 74,810 件），均不进分母、不按 0 摊。政策叶子是存量口径，不带年份——按年截断会把覆盖率打成 0（DATA_FACTS §3.7）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_INDICATOR.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_INDICATOR.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_INDICATOR_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

