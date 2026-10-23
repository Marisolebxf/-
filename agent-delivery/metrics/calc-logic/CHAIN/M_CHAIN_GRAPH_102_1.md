# 产业实体识别构建（M_CHAIN_GRAPH_102_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GRAPH_102_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GRAPH_102_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GRAPH_102_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_GRAPH_102_1 |
| 指标名称 | 产业实体识别构建 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链图谱／实体接入 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 图谱后台「实体接入」面板；图谱检索的实体类型筛选 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_GRAPH_102_1.md` |

## 口径定义

六类实体源表全部存在且有量，接入是纯 ETL；但 6 类中仅 2 类有链级键（企业、专利），另 4 类无链码 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GRAPH_102_1.md` §二（M_CHAIN_GRAPH_102_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_heis_info`
- `dwd_org_industry_tags`
- `dwd_patent`
- `dwd_policy_base`
- `dwd_research_institute_base_info`
- `dwd_scholar`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：六类实体在 gkx 均有源表且量足（3,175,902 条：企业 189,116、高校 3,501、科研机构 2,074、人才 21,316、政策 20,000、专利 2,939,895）；但只有企业与专利存在链级挂接面（企业走 industry_code、专利走申请人名称桥，挂链率 75.07% / 38.35%），高校、科研机构、人才、政策四类没有 chain_id 或 industry_code，链挂接只能覆盖 2/6，故判部分支持。
- **基期声明**：截面指标：统计当前存量，不设年度分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GRAPH_102_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GRAPH_102_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GRAPH_102_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

