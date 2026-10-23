# 技术点影响力 / 实体优先级（M_TECH_ENTITY_INFLUENCE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_ENTITY_INFLUENCE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_INFLUENCE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_INFLUENCE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_ENTITY_INFLUENCE |
| 指标名称 | 技术点影响力 / 实体优先级 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技信息展示系统 · 技术评估 · 技术关系网络「核心节点」+ 创新主体评估（实体排序） ｜ **数据支持度**：**完全转换支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_ENTITY_INFLUENCE.md` |

## 口径定义

「技术点影响力 / 实体优先级」在库内**没有结果面**（无「技术影响力分」「实体优先级」字段），但依赖侧齐备：IPC4 共类网络（378 节点 / 3,855 条 co≥5 边）可算出**尺度一致**的 PageRank（$d=0.85$、40 轮、和恒为 1.0），叠加规模对数与 2021→2024 增速后得技术点影响力（G06F 92.59、G06N 72.06、G06V 52.37，中位约 18，跨 0-93 有区分度）；再以「实体在各技术点上的 PR 加权计数」得实体优先级（4,200 家 ≥5 件实体，华为 83.05、华南理工 80.08、广东工大 76.72，中位 18.8、p90 25.65、≥50 仅 46 家）——**结构与量双足、当日可算**，按四档口径落 **完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_ENTITY_INFLUENCE.md` §二（M_TECH_ENTITY_INFLUENCE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_patent_applicants`
- `dwd_patent_cited`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：「技术点影响力 / 实体优先级」在库内**没有结果面**（无「技术影响力分」「实体优先级」字段），但依赖侧齐备：IPC4 共类网络（378 节点 / 3,855 条 co≥5 边）可算出**尺度一致**的 PageRank（$d=0.85$、40 轮、和恒为 1.0），叠加规模对数与 2021→2024 增速后得技术点影响力（G06F 92.59、G06N 72.06、G06V 52.37，中位约 18，跨 0-93 有区分度）；再以「实体在各技术点上的 PR 加权计数」得实体优先级（4,200 家 ≥5 件实体，华为 83.05、华南理工 80.08、广东工大 76.72，中位 18.8、p90 25.65、≥50 仅 46 家）——**结构与量双足、当日可算**，按四档口径落 **完全转换支持**。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_ENTITY_INFLUENCE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_INFLUENCE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_INFLUENCE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

