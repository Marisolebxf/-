# 痛难点改进差距（M_ENT_PAINPOINT_GAP）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PAINPOINT_GAP.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_GAP.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_GAP_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_PAINPOINT_GAP |
| 指标名称 | 痛难点改进差距 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业服务／企业诊断／经营痛难点 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业画像「改进差距」雷达 + 差距明细表｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2014, 2015, 2016, 2017, 2025] |
| 缺失年份 | [2018, 2019, 2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_PAINPOINT_GAP.md` |

## 口径定义

六项原料四项可算、两项废（研发人员占比 0 家、营收增长率 17 家），8 个行业门类 × 28 个指标-组配对的 P25/P75 在线算出，1,131 家企业可打分；但基线配置表在库内 0 张、分组键用行业门类代理产业链（Q018 未闭合）、金额单位疑元与万元混用（最大值 29,800,924,733.43 与中位数 16,554.99 并存），故判部分支持，差值只作组内排序提示。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PAINPOINT_GAP.md` §二（M_ENT_PAINPOINT_GAP.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_income_statement`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：差值的分组基线在库内无配置表（名称含 baseline/p25/p75/quantile/percentile/diagnosis 的表 0 张），只能在线算分位；六项原料里研发人员占比整列为空（development_employee 非空 0/90926），营收增长率配对仅 17 家；其余四项可算但覆盖 699—1,242 家，行业门类样本≥30 的组 8 个、可打分主体 1131 家。有算子、有真数、缺维度与样本，故判部分支持。
- **基期声明**：每企取「最新一个有营收的年」，取到的年份集中在 2014—2017（最新年分布见 compute.dims 与主体样本的 year 字段），故 used 只列实际承载主体的年份；2018—2024 虽在表内存在，但承载主体极少（营收>0 行集中于早期），单列 missing 以免被读成可用基期。增长率维用 2023→2024 两年配对（17 家），与本截面基期不同源。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PAINPOINT_GAP.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_GAP.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PAINPOINT_GAP_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

