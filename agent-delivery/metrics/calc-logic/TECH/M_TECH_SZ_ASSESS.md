# 深圳技术潜力与阶段综合评估（M_TECH_SZ_ASSESS）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_SZ_ASSESS.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_SZ_ASSESS.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_SZ_ASSESS_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_SZ_ASSESS |
| 指标名称 | 深圳技术潜力与阶段综合评估 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | TOPIC-TECH（技术领域评估） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 智慧认知大脑/深度挖掘算法/算法工具库/科技专题服务算法库/技术领域深度分析模型构建/深圳技术领域评估 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_SZ_ASSESS.md` |

## 口径定义

238 个 IPC4 技术点在「深圳 2024 年 ≥100 件」门槛上可算六项指标，四象限与三阶段可复现；但「产业化潜力」只有专利结构代理——转让密度算不出、营收/订单/技术合同无表，区位商也只能是「语料内」而非全国，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_SZ_ASSESS.md` §二（M_TECH_SZ_ASSESS.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_patent_transfer`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：238 个 IPC4 技术点可算：规模、区位商、增速、授权率、发明占比、申请人结构六项均有落盘数据，四象限与阶段分级可复现；但需求要的「产业化」只有专利侧代理——转让密度不可算（转让表只有 pn，专利缓存已哈希去 pn），市场/营收/政策维度未进入算路，「潜力」是专利结构分而非商业潜力分。
- **基期声明**：dwd_patent 的 apdt_year 只有 2021—2026：2017—2020 零行（§3.13），2025—2026 不完整，故窗口固定 2021—2024，增速用 (2023+2024)/(2021+2022)−1，未把缺失年按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_SZ_ASSESS.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_SZ_ASSESS.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_SZ_ASSESS_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

