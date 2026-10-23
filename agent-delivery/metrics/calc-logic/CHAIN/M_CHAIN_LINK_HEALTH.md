# 环节健康度（M_CHAIN_LINK_HEALTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_LINK_HEALTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LINK_HEALTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LINK_HEALTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_LINK_HEALTH |
| 指标名称 | 环节健康度 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 / 产业关键环节识别 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链全景页「环节健康度」热力格、环节详情页五维雷达 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_LINK_HEALTH.md` |

## 口径定义

五维里技术、资本两维有节点级可算路径；人才列（`development_employee`）在 90,926 行年报财务表里 0 行有值，营收在 L1 层最高覆盖 3.57%，政策表没有环节码列——**三维永久不可得，两维可得**，故判**部分支持**，且不输出总分。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_LINK_HEALTH.md` §二（M_CHAIN_LINK_HEALTH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_industry_chain_pat_dtl`
- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：五维里只有技术成熟度与融资资本两维能在 L1 节点层闭合（合计权重 2/5=0.40）；人才列整列为空、营收覆盖 <1%、政策无环节码，三维永久不可得，故不能输出 0—100 总分。
- **基期声明**：专利面板完整覆盖 2021—2024（2025 年 440,401 件、2026 年 74,810 件为残年，不进分母）；本件用全量专利存量（2021—2026 年申请合计）算密度，不做年度增速，故基期用于说明「专利面板从 2021 年才有数据、2017—2020 年零行」，不把缺失年按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_LINK_HEALTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LINK_HEALTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LINK_HEALTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

