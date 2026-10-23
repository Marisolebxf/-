# M_TALENT_UNIV_NEW（M_TALENT_UNIV_NEW）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_UNIV_NEW.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_UNIV_NEW.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_UNIV_NEW_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_UNIV_NEW |
| 指标名称 | M_TALENT_UNIV_NEW |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技人才态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2025] |
| 缺失年份 | [2016, 2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_UNIV_NEW.md` |

## 口径定义

第一，建校年只覆盖 46.13%。3,501 行里 1,353 所有 `est_year`，其余为空。更麻烦的是 `est_year` 是"现校名成立年"，合并、更名、升格的院校会显得很新——例如某专科 2016 年升格为学院，`est_year` 就记 2016，但它并不是新设。因此"2016 年后建校 25 所"是下限，且混有"更名"。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_UNIV_NEW.md` §二（M_TALENT_UNIV_NEW.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：第一，建校年只覆盖 46.13%。3,501 行里 1,353 所有 `est_year`，其余为空。更麻烦的是 `est_year` 是"现校名成立年"，合并、更名、升格的院校会显得很新——例如某专科 2016 年升格为学院，`est_year` 就记 2016，但它并不是新设。因此"2016 年后建校 25 所"是下限，且混有"更名"。
- **基期声明**：论文侧只取 2021—2025 五年（面板覆盖到 2025）；「新建校」用建校年≥2016 判定，但没有 2016—2020 的作者首发序列，算不出「新校带来的净增」相对基期；新增作者是「面板内首次出现」，不等于人生第一次发文

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_UNIV_NEW.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_UNIV_NEW.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_UNIV_NEW_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

