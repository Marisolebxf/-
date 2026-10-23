# 政策实体识别构建（M_POLICY_GRAPH_106_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_GRAPH_106_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_GRAPH_106_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_GRAPH_106_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_GRAPH_106_1 |
| 指标名称 | 政策实体识别构建 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 政策图谱页「实体标签」层（设计位）、政策详情页「发文机关 / 适用对象 / 涉及产业」三块标签（设计位） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_GRAPH_106_1.md` |

## 口径定义

「政策实体识别」不依赖任何外部结果面，它消费的是 `dwd_policy_base` 的 `title`、`content`、`type`、`province`、`city`、`publish_date`——这些字段在 gkx 都有、且 20,000 行齐备。因此本件的判档只取决于一件事：**源侧量是否够**。答案是够：18,763 条正文、45,737,165 字，六类实体的词典与正则都已就位。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_GRAPH_106_1.md` §二（M_POLICY_GRAPH_106_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：两库均无政策实体结果表（gkx 280 表中无 policy_entity 一类表；live 同名表为造数面），但源侧 `dwd_policy_base` 的标题与正文 20,000 条（正文 18,763 条、45,737,165 字）结构完整、量足够，规则+词典识别现在即可产出六类实体及属性，属「结构+数据量均足够、现可转换生成」。精度只能用抽检验证，不用精度不足降档。
- **基期声明**：截面构建：把 20,000 条政策一次性建成实体表，不按年出值，故无基期年；发布年（1981—2024）只作属性，不进入任何分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_GRAPH_106_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_GRAPH_106_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_GRAPH_106_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

