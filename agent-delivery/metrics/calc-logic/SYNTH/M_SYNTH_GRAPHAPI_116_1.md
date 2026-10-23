# 图谱 API 节点/边供给能力（M_SYNTH_GRAPHAPI_116_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_GRAPHAPI_116_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_GRAPHAPI_116_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_GRAPHAPI_116_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_GRAPHAPI_116_1 |
| 指标名称 | 图谱 API 节点/边供给能力 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 图数据库 |
| 二级模块 | 图谱 API |
| 更新频率 | 待确认 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_GRAPHAPI_116_1.md` |

## 口径定义

本件把「图谱 API 能不能做」拆成供给面与契约面。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_GRAPHAPI_116_1.md` §二（M_SYNTH_GRAPHAPI_116_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`
- `dwd_patent`
- `dwd_patent_assignees`
- `dwd_policy_base`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件把「图谱 API 能不能做」拆成供给面与契约面。供给面统计 7 个节点域、9 类关系：节点域合计 3,570,548 行，其中论文 100,900、专利 2,939,895、企业 189,116、申请人 169,226、发明人 69,647、学者 21,316、政策 20,000。
- **基期声明**：图谱 API 是截面能力清单，不做年度切片；各节点域的行数来自各自快照，域间重叠，不能相加当单一图规模。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_GRAPHAPI_116_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_GRAPHAPI_116_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_GRAPHAPI_116_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

