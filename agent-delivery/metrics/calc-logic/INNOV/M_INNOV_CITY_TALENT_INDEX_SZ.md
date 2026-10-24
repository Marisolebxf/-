# 深圳重点人才指数（M_INNOV_CITY_TALENT_INDEX_SZ）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CITY_TALENT_INDEX_SZ.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CITY_TALENT_INDEX_SZ.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CITY_TALENT_INDEX_SZ_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CITY_TALENT_INDEX_SZ |
| 指标名称 | 深圳重点人才指数 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统／科技人才智慧服务／深圳重点人才 |
| 更新频率 | 待确认 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 深圳人才指数卡、人才池画像 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_CITY_TALENT_INDEX_SZ.md` |

## 口径定义

深圳人才池的综合指数是 **69.21**（全国 38 城参照、五叶等权百分位）；四叶在 98.68 百分位（h 中位数 23、h≥50 占比 16.9014%、国际化率 13.615%），但"近三年活跃率"只有 **29.5775%**，落在 **1.32 百分位**——比全国均值 50.9158% 低 **21.3383** 个百分点，是 38 城里的最低档。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CITY_TALENT_INDEX_SZ.md` §二（M_INNOV_CITY_TALENT_INDEX_SZ.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_scholar`
- `dwd_scholar_talent_flag`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：深圳人才池的综合指数是 **69.21**（全国 38 城参照、五叶等权百分位）；四叶在 98.68 百分位（h 中位数 23、h≥50 占比 16.9014%、国际化率 13.615%），但"近三年活跃率"只有 **29.5775%**，落在 **1.32 百分位**——比全国均值 50.9158% 低 **21.3383** 个百分点，是 38 城里的最低档。
- **基期声明**：活跃率叶的「近三年」窗口锁 2021—2023：2024 年中文论文语料是回填孤峰（32,379 篇，为 2023 年 4.87 倍），2025—2026 为残年；2017—2020 专利零行（DATA_FACTS §3.13），故不进任何分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CITY_TALENT_INDEX_SZ.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CITY_TALENT_INDEX_SZ.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CITY_TALENT_INDEX_SZ_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

