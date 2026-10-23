# 多维度排名展示（M_INNOV_DS_04_CARRIER_RANK_002）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_CARRIER_RANK_002.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_CARRIER_RANK_002.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_CARRIER_RANK_002_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_04_CARRIER_RANK_002 |
| 指标名称 | 多维度排名展示 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV / DS_04 创新载体 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 创新载体排行榜 → 多维度排名展示、排名筛选功能 ｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_04_CARRIER_RANK_002.md` |

## 口径定义

多维度排名展示（M_INNOV_DS_04_CARRIER_RANK_002）把创新载体的创新能力指数转换为名次，并按总体、地区、领域三个宇宙分别呈现，对应需求原文「提供创新载体的多维度排名，包括总体排名、领域排名、地区排名等，用户可切换查看不同维度的排名情况」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_CARRIER_RANK_002.md` §二（M_INNOV_DS_04_CARRIER_RANK_002.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_research_institute_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：多维度排名展示（M_INNOV_DS_04_CARRIER_RANK_002）把创新载体的创新能力指数转换为名次，并按总体、地区、领域三个宇宙分别呈现，对应需求原文「提供创新载体的多维度排名，包括总体排名、领域排名、地区排名等，用户可切换查看不同维度的排名情况」。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_CARRIER_RANK_002.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_CARRIER_RANK_002.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_CARRIER_RANK_002_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

