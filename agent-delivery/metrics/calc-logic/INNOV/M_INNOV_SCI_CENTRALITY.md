# 科学网络中心性（M_INNOV_SCI_CENTRALITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCI_CENTRALITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_CENTRALITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_CENTRALITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCI_CENTRALITY |
| 指标名称 | 科学网络中心性 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_SCI_CENTRALITY.md` |

## 口径定义

本件在中文论文机构共著图上计算度、接近、中介、PageRank 四类中心性，主口径点集为 P2 巨型连通分量（15,223 节点 / 36,965 边），归一化分母为 n−1。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCI_CENTRALITY.md` §二（M_INNOV_SCI_CENTRALITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件在中文论文机构共著图上计算度、接近、中介、PageRank 四类中心性，主口径点集为 P2 巨型连通分量（15,223 节点 / 36,965 边），归一化分母为 n−1。
- **基期声明**：全量截面图（论文年份 1980—2026），不做年度切片；2025/2026 是滞后/残年，只影响边权，不改变 2024 年前已形成的机构节点集合。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCI_CENTRALITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_CENTRALITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_CENTRALITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

