# 深圳科研机构现状解读（M_ORG_SZ_STATUS）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ORG-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_SZ_STATUS.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_SZ_STATUS.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_SZ_STATUS_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ORG_SZ_STATUS |
| 指标名称 | 深圳科研机构现状解读 |
| 所属域 | ORG（科研机构） |
| 一级模块 | TOPIC-ORG（深圳科研机构现状） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 智慧认知大脑/深度挖掘算法/算法工具库/科技专题服务算法库/科研机构深度分析模型构建/深圳科研机构现状分析 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/ORG/M_ORG_SZ_STATUS.md` |

## 口径定义

七维里三维（规模、结构、成长）在 1,014 家深圳机构上可全量计算，四城同口径可比；另外三维（产出、经费、人才）只对有证据子集可算——专利 87 家、国基金 20 家、学者 12 家，覆盖率 8.58%/1.97%/1.18%，且「经费」只是 NSFC 资助额而非全口径科研经费，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_SZ_STATUS.md` §二（M_ORG_SZ_STATUS.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_research_institute_base_info`
- `dwd_scholar`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：规模/结构/成长三维在 1014 家深圳机构上可直接计算，四城同口径可比；产出/经费/人才三维只对有证据子集可算：专利 87 家、国基金 20 家、学者 12 家，分别占深圳机构 8.58% / 1.97% / 1.18%，且经费只是 NSFC 资助额、不是全口径科研经费；需求要求的「在该产业」切片无法闭合（机构×产业领域标签仅命中 1 家），只能给城市级总体现状。
- **基期声明**：成长维只取 2021—2025 登记年（2026 为残年，不进分母）；专利件数为存量口径，库内申请年只覆盖 2021—2026，2017—2020 零行，未按 0 摊入。项目/论文/学者为截面总量，不设年度基期。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_SZ_STATUS.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_SZ_STATUS.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_SZ_STATUS_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

