# 创新价值（M_INNOV_DS_04_ACHIEVE_OVERVIEW_001）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_04_ACHIEVE_OVERVIEW_001 |
| 指标名称 | 创新价值 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新成果 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 创新成果综合展示 → 创新价值排序 / 创新价值分类展示 ｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001.md` |

## 口径定义

三型成果（专利、中文论文、国内项目）各有三维、共 9 个观测量，其中**专利型三维全部有数据**（被引 20,515 行、转化 22,809 行、专利价值非空），而**论文型**的 `impact_score` 与 `jn_zone` 在 2,796 行期刊表里 100% 为空、`download_num` 在 100,900 行论文里 100% 为 0，**项目型**的 `project_level` 在 58,453 行里只有 1 个取值——三分之一有区分度，故落 **部分支持**。20261021 改源后在同一口径下重算，四型统计量与旧版逐项一致（专利 33.33–66.67、论文恒 50.0、项目 17.42–83.33、深圳切片 2,353），说明 `gkx` 与旧开发库是逐表镜像；本版不再引用任何旧 out.json 的数字。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001.md` §二（M_INNOV_DS_04_ACHIEVE_OVERVIEW_001.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_journal`
- `dwd_en_paper`
- `dwd_en_project`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_patent_transfer`
- `dwd_zh_journal`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三型成果（专利、中文论文、国内项目）各有三维、共 9 个观测量，其中**专利型三维全部有数据**（被引 20,515 行、转化 22,809 行、专利价值非空），而**论文型**的 `impact_score` 与 `jn_zone` 在 2,796 行期刊表里 100% 为空、`download_num` 在 100,900 行论文里 100% 为 0，**项目型**的 `project_level` 在 58,453 行里只有 1 个取值——三分之一有区分度，故落 **部分支持**。20261021 改源后在同一口径下重算，四型统计量与旧版逐项一致（专利 33.33–66.67、论文恒 50.0、项目 17.42–83.33、深圳切片 2,353），说明 `gkx` 与旧开发库是逐表镜像；本版不再引用任何旧 out.json 的数字。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 34.2 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_ACHIEVE_OVERVIEW_001_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

