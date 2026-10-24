# 产业链周期分析模型（M_CHAIN_DEEP_122_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_122_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_122_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_122_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_122_1 |
| 指标名称 | 产业链周期分析模型 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业周期分析／周期阶段判定 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链详情页「周期位置」标签、首页 12 链周期热力条 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_DEEP_122_1.md` |

## 口径定义

周期模型的四个状态量里，只有两个能用「事件计数」在本库重建：链内新设企业数（底册成立年 ∩ 链标签）与挂链融资事件数（融资表按企业名挂链）。市场规模、增长率、利润率三个金额量都在财务表，而财务表的营收只有 2,193/90,926 行有值（2.41%），链级汇总面 `chain_market` 不存在。**两条腿能算、四条腿缺两条，且缺的恰是旧稿的主状态量**，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_122_1.md` §二（M_CHAIN_DEEP_122_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：时间轴上的双动能（链内新设企业数、挂链融资事件数）可从 gkx 快照得到，12 条链全部出标签；但旧稿的「产业周期」以市场规模/增长率/利润率/投融资额为状态量，gkx 无 chain_market、无 chain_cycle 等 7 张结果表（information_schema 实测 absent），财务表营收仅 2,193/90,926 行有值，故只交付相对动能周期，不交付价格/产能/利润周期。
- **基期声明**：两窗各 6 年：2013—2018 与 2019—2024，端点年份在 params.windows 与 compute.national_by_year 双落盘。2025/2026 为不完整年，主动排除并已写入 counter_checks（新设 2025 年 429 家、2026 年 14 家），不按 0 摊入分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_122_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_122_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_122_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

