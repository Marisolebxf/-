# 产业实体关系抽取（M_CHAIN_GRAPH_103_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GRAPH_103_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GRAPH_103_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GRAPH_103_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_GRAPH_103_1 |
| 指标名称 | 产业实体关系抽取 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业全要素图谱 · 关系抽取与图谱关系管理 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_GRAPH_103_1.md` |

## 口径定义

需求点名的六族关系里，**只有「产业—企业」（1,714,458 条）与「产业—技术」（29,631 个企业—链对，对应 1,127,340 件专利）** 在 gkx 有链键、可现算；「产业—人才」「产业—科研机构」「产业—服务机构」「产业—政策」四族的源表有行数但**没有 chain_id / industry_code**，无法定边 → 六族覆盖 **2/6**，判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GRAPH_103_1.md` §二（M_CHAIN_GRAPH_103_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_financing_info`
- `dwd_org_industry_tags`
- `dwd_patent`
- `dwd_policy_base`
- `dwd_research_institute_base_info`
- `dwd_scholar`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：需求点名的六族关系中，只有「产业—企业」（1,714,458 条）与「产业—技术」（29,631 个企业—链对，经专利申请人名称桥）可由 gkx 现算；产业—人才、产业—科研机构、产业—服务机构、产业—政策四族在 gkx 均无链码（源表有行数但没有 chain_id / industry_code），六族只能覆盖 2/6，故判部分支持。
- **基期声明**：截面指标：统计当前存量，不设年度分母。
- **复现实测耗时**：约 0.13 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GRAPH_103_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GRAPH_103_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GRAPH_103_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

