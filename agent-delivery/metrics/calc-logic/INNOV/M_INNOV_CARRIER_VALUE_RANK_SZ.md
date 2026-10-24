# 深圳创新载体创新价值排名（M_INNOV_CARRIER_VALUE_RANK_SZ）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CARRIER_VALUE_RANK_SZ.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CARRIER_VALUE_RANK_SZ.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CARRIER_VALUE_RANK_SZ_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CARRIER_VALUE_RANK_SZ |
| 指标名称 | 深圳创新载体创新价值排名 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统·科技发展态势·深圳创新监测→深圳市创新载体 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·科技发展态势·深圳创新监测→深圳市创新载体综合展示→创新价值排名展示｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_CARRIER_VALUE_RANK_SZ.md` |

## 口径定义

无现成「深圳创新价值排名」结果面 → 非完全直接支持；技术价值维（专利 value）结构数据双足（537/2,000 载体覆盖），但**应用价值维近乎全缺**（论文下载量全 0、专利转移名称对齐命中仅 1）且**潜在影响力维完全无命中**（2024 窗内被引 0 家）——三维中两维当前无数据区分度，排名实质退化为技术维单维排序 → 按定义落入**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CARRIER_VALUE_RANK_SZ.md` §二（M_INNOV_CARRIER_VALUE_RANK_SZ.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_patent_transfer`
- `dwd_policy_base`
- `dwd_research_institute_base_info`
- `dwd_scholar`
- `dwd_zh_journal`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：无现成「深圳创新价值排名」结果面 → 非完全直接支持；技术价值维（专利 value）结构数据双足（537/2,000 载体覆盖），但**应用价值维近乎全缺**（论文下载量全 0、专利转移名称对齐命中仅 1）且**潜在影响力维完全无命中**（2024 窗内被引 0 家）——三维中两维当前无数据区分度，排名实质退化为技术维单维排序 → 按定义落入**部分支持**。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CARRIER_VALUE_RANK_SZ.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CARRIER_VALUE_RANK_SZ.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CARRIER_VALUE_RANK_SZ_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

