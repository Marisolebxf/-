# M_TALENT_DEEP_156_1（M_TALENT_DEEP_156_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_156_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_156_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_156_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DEEP_156_1 |
| 指标名称 | M_TALENT_DEEP_156_1 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才洞察页「重点人才名单 + 分数分档 + 深圳切片」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DEEP_156_1.md` |

## 口径定义

三因子（h / 被引 / 论文数）在 `dwd_scholar` 21,316 行上 **100% 非空**、20,420 名有姓名学者可全量打分，院士标识 112 行可作外部校验——识别主链成立；但需求点名的「企业人才库」「招聘/薪资市场信号」在 `gkx` 全库无表（`dwd_job` 仅 10 行），学历/履历/研究方向三张子表与身份主档只有 9.25%—9.5% 可对齐，识别池只能退化为「学者口径」，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_156_1.md` §二（M_TALENT_DEEP_156_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_job`
- `dwd_org_annual_financial_info`
- `dwd_org_recruit_info`
- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_scholar_research_direction`
- `dwd_scholar_talent_flag`
- `dwd_scholar_work_experience`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：学术影响力三列（h / citation_nums / paper_nums）在 gkx.dwd_scholar 21,316 行上 100% 非空、可全量打分，院士标识与中文论文面可作外部校验，识别主链成立；但需求输入第一项「企业人才库数据」与「招聘/薪资市场信号」在库内无表（dwd_job 仅 10 行），学历/履历/研究方向三张子表与身份主档只有 9.3% 可行对齐，识别池退化为学者口径 → 部分支持。
- **基期声明**：截面口径：K 用三列的生涯累计值（paper_nums / citation_nums / h_index），不含年度窗口，也不做任何跨年基准或增长率，故无基期年份。论文面的年度数据只用于 158/161，不参与本件打分。
- **复现实测耗时**：约 6.2 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_156_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_156_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_156_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

