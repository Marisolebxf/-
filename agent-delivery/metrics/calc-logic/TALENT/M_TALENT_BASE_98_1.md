# M_TALENT_BASE_98_1（M_TALENT_BASE_98_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_BASE_98_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_BASE_98_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_BASE_98_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_BASE_98_1 |
| 指标名称 | M_TALENT_BASE_98_1 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才分布图页「区域分布概览 / 城市详情 / 学历结构」三张统计卡 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2015, 2024] |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_BASE_98_1.md` |

## 口径定义

四族分组计数全部能出数：学者 **21,316**、机构 **2,108**、方向标签 **97,249**、学历行 **43,766**；但三处硬缺口始终存在——①「人才」只有学者口径，企业研发人员与技能人才无表；② 学历族是**存量学者的毕业年回溯**、不是当年毕业生流量，且无学科码；③ 三张子表的 `scholar_id` 与主档只有 **9.3%** 可连，四族不能交叉切片、D2/D3 无年份列故增长率不可算，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_BASE_98_1.md` §二（M_TALENT_BASE_98_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_heis_info`
- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_scholar_research_direction`
- `dwd_scholar_talent_flag`
- `dwd_scholar_work_experience`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四族分组计数都能出数（学者 21,316、机构 2,108、方向标签 97,249、学历行 43,766），但三处硬缺口始终存在：①「人才」只有学者口径，企业研发人员/技能人才无表；② D4 是存量学者学历回溯，不是学科×年份的官方供给流量，且无学科码；③ D3/D4 的 scholar_id 与主档仅 9.3% 可连，四族不能交叉切片、D2/D3 无年份列故增长率不可算 → 部分支持。
- **基期声明**：仅取 2015 与 2024 两个完整年对比；2025/2026 为残年不计入任何分母。注意该序列是「存量学者的毕业年回溯」，不是当年全口径毕业生流量。
- **复现实测耗时**：约 1.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_BASE_98_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_BASE_98_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_BASE_98_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

