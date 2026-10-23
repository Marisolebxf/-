# 科学研究前沿性（M_INNOV_SCI_FRONTIER）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCI_FRONTIER.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_FRONTIER.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_FRONTIER_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCI_FRONTIER |
| 指标名称 | 科学研究前沿性 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科学创造力评估页「科学研究前沿性」卡片（前沿主题图谱 + 主题时间演变 + 空间分布） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2015, 2016, 2017, 2018, 2019, 2022, 2023, 2024] |
| 缺失年份 | [2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_SCI_FRONTIER.md` |

## 口径定义

四子项里**只有两个能出数**：时间演变（799 篇有年份）与空间分布（733 篇可落城市，91.74%）。**研究前沿**要求「共被引 ≥2 的连通分量」，而池内 9,391 个被引 ID 只有 121 个（1.288%）落在本库论文池内，268,982 个共被引对在 w≥2 过滤后只剩 32 条边、且池内边数为 **0**、连通分量 **0** 个；**热点方向**要求「词对共现 ≥2」，24 条边只连出 220 个节点、词频中位数为 1，拓扑不成立。结构与字段都在，缺的是**量**，故判**部分支持**，不判「完全不支持」（两个子项确实能算），也不判「完全转换支持」（主路径不可闭合）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCI_FRONTIER.md` §二（M_INNOV_SCI_FRONTIER.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_paper`
- `dwd_en_paper_reference`
- `dwd_org_base_info`
- `dwd_zh_author`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四子项里**只有两个能出数**：时间演变（799 篇有年份）与空间分布（733 篇可落城市，91.74%）。**研究前沿**要求「共被引 ≥2 的连通分量」，而池内 9,391 个被引 ID 只有 121 个（1.288%）落在本库论文池内，268,982 个共被引对在 w≥2 过滤后只剩 32 条边、且池内边数为 **0**、连通分量 **0** 个；**热点方向**要求「词对共现 ≥2」，24 条边只连出 220 个节点、词频中位数为 1，拓扑不成立。结构与字段都在，缺的是**量**，故判**部分支持**，不判「完全不支持」（两个子项确实能算），也不判「完全转换支持」（主路径不可闭合）。
- **基期声明**：时间演变用近窗 2022—2024、基线 2015—2019；2025/2026 在 799 篇样本里记录过少，不进任何分母

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCI_FRONTIER.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_FRONTIER.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_FRONTIER_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

