# 科学创造力趋势预测（M_INNOV_DS_07_SCI_CREATE_004）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_07_SCI_CREATE_004.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_07_SCI_CREATE_004.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_07_SCI_CREATE_004_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_07_SCI_CREATE_004 |
| 指标名称 | 科学创造力趋势预测 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统·科学创造力指标展示·科学创造力趋势预测（S |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技信息展示系统·科学创造力指标展示·科学创造力趋势预测（SRS 序号 139） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_07_SCI_CREATE_004.md` |

## 口径定义

三方库 `gkx`（280 张表）与本项目自建 ADS 均无「科学创造力趋势预测」结果表，故非完全直接支持；但王惠三维所需的题名、发表年、作者机构三类字段在 `gkx.dwd_zh_paper` 全量齐备，脚本已现算出年度三维序列、合成指数与 Holt 点预测及 80% 区间 → **完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_07_SCI_CREATE_004.md` §二（M_INNOV_DS_07_SCI_CREATE_004.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_index_attribute`
- `dwd_dim_index_cal`
- `dwd_dim_index_dur`
- `dwd_en_author`
- `dwd_en_paper`
- `dwd_macro_index_data`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_zh_author`
- `dwd_zh_paper`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：无现成「科学创造力趋势预测」结果面（三方库 gkx 与 live 开发库均无该指标物化表）；但王惠三维所需字段（论文题名、发表年、作者机构）在 gkx.dwd_zh_paper 全量 100,900 篇、零坏 JSON 下齐备，且已现算出三维年度序列与 Holt 点预测+80% 区间，故判完全转换支持。
- **基期声明**：由产物中实际出现的年度键反推：used=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_07_SCI_CREATE_004.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_07_SCI_CREATE_004.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_07_SCI_CREATE_004_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

