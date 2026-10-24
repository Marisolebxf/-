# 要素间影响程度（M_INNOV_FACTOR_EDGE_WEIGHT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_FACTOR_EDGE_WEIGHT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_EDGE_WEIGHT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_EDGE_WEIGHT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_FACTOR_EDGE_WEIGHT |
| 指标名称 | 要素间影响程度 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV / DS-01-FACTORS |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科创要素关系图线宽、节点大小、技术点影响力｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_FACTOR_EDGE_WEIGHT.md` |

## 口径定义

五类边与 PageRank 全部跑通（∑PR=1），但 E1 只覆盖 0.68% 专利、E2/E3/E4 只覆盖 62,002 行作者、E6 是机构组合层，判部分支持。

## 计算逻辑说明

```text
edge_weight=共现次数；node_influence=100×weighted_degree/max(type)；E6 另做 damping=0.85 的加权 PageRank，∑PR=1
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_FACTOR_EDGE_WEIGHT.md` §二（M_INNOV_FACTOR_EDGE_WEIGHT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent_applicants`
- `dwd_scholar`
- `dwd_zh_author`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：五类边全部可算，且 PageRank ∑PR=1.0 自洽；但 E1 只覆盖 20,000 个 pn（主表 2,939,895 件的 0.6803%），边权是 0.68% 样本；E2/E3/E4 只覆盖 62,002 行作者记录、20,048 篇论文，不是全部论文；E6 没有单件专利的 IPC 列表，只能做机构组合共现（89,149 家机构），不是同专利共类；学者按姓名聚合，存在同名合并。结构与算法闭环成立，但四个覆盖缺口使边权不能当全量真值，故判部分支持。
- **基期声明**：本指标是截面图结构：边权由当前快照的共现计数一次算出，公式与产物均无年度键；used/missing 为空表示无年度基期，不是「缺年按 0 摊入」。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_FACTOR_EDGE_WEIGHT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_EDGE_WEIGHT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_EDGE_WEIGHT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

