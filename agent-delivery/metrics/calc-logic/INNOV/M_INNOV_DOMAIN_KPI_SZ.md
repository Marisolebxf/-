# 深圳科技领域明细指标（M_INNOV_DOMAIN_KPI_SZ）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DOMAIN_KPI_SZ.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DOMAIN_KPI_SZ.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DOMAIN_KPI_SZ_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DOMAIN_KPI_SZ |
| 指标名称 | 深圳科技领域明细指标 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统·科技发展态势·深圳创新监测→深圳市各科技领 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·科技发展态势·深圳创新监测→深圳市各科技领域分布展示→详细数据指标展示｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DOMAIN_KPI_SZ.md` |

## 口径定义

本指标是「一个科技领域 × 四个 KPI（企业数量、专利数量、研发投入、人才数量）」的明细面，无现成结果表；实测可对 608 个 IPC4 技术领域稳定产出**企业数量**与**专利数量**两列，但 `research_development_amount` 挂在企业财报（无领域键）、`dwd_scholar` 无领域列且深圳机构名对齐仅 165 人——后两个 KPI **只有深圳总量、没有领域分解**，故不论如何构建都始终有两维缺领域信息，按 §〇 落入**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DOMAIN_KPI_SZ.md` §二（M_INNOV_DOMAIN_KPI_SZ.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_base_info`
- `dwd_org_stock_finance_info`
- `dwd_patent`
- `dwd_scholar`
- `dwd_zh_author`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本指标是「一个科技领域 × 四个 KPI（企业数量、专利数量、研发投入、人才数量）」的明细面，无现成结果表；实测可对 608 个 IPC4 技术领域稳定产出**企业数量**与**专利数量**两列，但 `research_development_amount` 挂在企业财报（无领域键）、`dwd_scholar` 无领域列且深圳机构名对齐仅 165 人——后两个 KPI **只有深圳总量、没有领域分解**，故不论如何构建都始终有两维缺领域信息，按 §〇 落入**部分支持**。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 1633.0 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DOMAIN_KPI_SZ.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DOMAIN_KPI_SZ.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DOMAIN_KPI_SZ_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

