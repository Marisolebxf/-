# 社群发现（图算法）（M_SYNTH_DS_23_GRAPH_ALGO_011）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_23_GRAPH_ALGO_011.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_011.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_011_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_DS_23_GRAPH_ALGO_011 |
| 指标名称 | 社群发现（图算法） |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合／知识图谱算法 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 图谱页「社群发现」按钮、社群着色、社群列表 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_DS_23_GRAPH_ALGO_011.md` |

## 口径定义

图算法类的判档不看「结果表在不在」，看「**边在不在**」。本件的边只有一种可重建来源：同一篇论文的共同署名。这一种边是真实派生（不是自造），量也够（36,965 条巨片边）；供应、合作、技术流三类业务边在 gkx 均无表承接，本件不补也不拿专利共现顶替。所以判**完全转换支持**，同时把「社群只读作学术共著社群」写成硬边界。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_23_GRAPH_ALGO_011.md` §二（M_SYNTH_DS_23_GRAPH_ALGO_011.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_invest_info`
- `dwd_org_subsidiary_info`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：三张图表在 gkx 均不存在，但边源可重建：dwd_zh_paper 的 author_info_list 提供同篇共著关系，100,900 篇论文建成 20,436 节点 / 38,208 边，巨连通片 15,223 节点 / 36,965 边；四种社群发现算法在巨片上全部跑通，模块度 0.5—0.7 区间，社群成员表可全量落盘。结构与数据量都够，现在就能算出该指标，故判完全转换支持。
- **基期声明**：合著图用 2021—2024 四个完整年的论文（WINDOW 见 _collab_graph21.py）；2025/2026 论文未完整入库，未参与建图；不是库内不存在，是本指标未取用。
- **复现实测耗时**：约 0.0 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_DS_23_GRAPH_ALGO_011.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_011.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_DS_23_GRAPH_ALGO_011_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

