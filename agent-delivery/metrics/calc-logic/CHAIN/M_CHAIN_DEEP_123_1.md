# 产业阶段分析模型（M_CHAIN_DEEP_123_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_123_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_123_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_123_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_123_1 |
| 指标名称 | 产业阶段分析模型 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业周期分析／发展阶段评估 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链详情页「发展阶段」徽标、区域产业报告「阶段对比」小节 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_DEEP_123_1.md` |

## 口径定义

旧稿的「产业阶段」要六个输入：生产能力（资产）、销售规模（营收）、市场份额、利润率、高技术占比、投资强度。本库能算后三个里的两个半——高技术占比可算但分母只有可匹配子集，投资强度可算但只能数事件不能求和金额，市场份额只有四城 + 省外桶；前三个（资产、营收、利润率）在财务表覆盖率 2.41%—2.89%。**六个输入缺三个、两个打折，故判部分支持。**

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_123_1.md` §二（M_CHAIN_DEEP_123_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_annual_financial_info`
- `dwd_org_financing_info`
- `dwd_org_industry_tags`
- `dwd_org_tech_tag`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：企业规模、增长、投资强度、技术密度、结构完整度五个横截面维度可从 gkx 快照构造，12 条链全部出阶段；但旧稿的「生产能力=资产合计」「销售规模=营收合计」「利润率」三项，在 gkx 财务表分别只有 2,629 / 2,193 / 2,349 行有值（占 90,926 行的 2.6%~2.9%），且无 chain_enterprise_stat / enterprise_industry_summary 汇总面（280 张表 absent），故阶段只能按结构与资本强度判定，不能按产值与利润判定。
- **基期声明**：增长项与投资强度项都用 2013—2018 对 2019—2024 两窗；2025/2026 为不完整年，主动排除（2025 新设 429 家、2026 新设 14 家，已写入 122 的同源计数），不按 0 摊入分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_123_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_123_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_123_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

