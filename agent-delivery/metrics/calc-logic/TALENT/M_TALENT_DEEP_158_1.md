# M_TALENT_DEEP_158_1（M_TALENT_DEEP_158_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_158_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_158_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_158_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DEEP_158_1 |
| 指标名称 | M_TALENT_DEEP_158_1 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才洞察页「高校学院培育产出 + 校×年 + 学科方向」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DEEP_158_1.md` |

## 口径定义

培养机构名单（教育部名录深圳 11 校 + 4 个深圳研究生院/院所）与全国培养分母（名录内博士学历段 1,802 段 / 1,769 人）可全量现转，产出层（深圳机构署名中文论文 1,205 篇、近五年 894 篇）可算；但「新培育」的核心时序腿几乎不存在——全库学历表中命中深圳培养机构的记录只有 15 段、覆盖 13 人，2019 年后仅 3 段，无法支撑逐年新增序列，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_158_1.md` §二（M_TALENT_DEEP_158_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_heis_info`
- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：培养机构名单（教育部名录深圳 11 校 + 4 个深圳研究生院/院所）与全国培养分母（名录内博士学历段）可全量现转，产出层（深圳机构署名中文论文 1,188 篇）可算；但「新培育」的核心时序腿在库内近乎不存在——全库学历表中命中深圳培养机构的记录只有 15 段、覆盖 13 名学者、2019 年后仅 3 段，无法支撑逐年新增序列；且学历表与身份主档只有 9.25% 可挂、无学科代码 → 部分支持。
- **基期声明**：产出层窗口取 2021—2025 五个真实存在的年份；2026 在采集时点只有残年数据（56 篇，占 4.65%），不进窗口、也不按比例外推。学历层的毕业年只统计表内真实出现的年份（2010—2022，共 8 个年），不补 0。
- **复现实测耗时**：约 9.4 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_158_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_158_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_158_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

