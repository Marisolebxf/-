# 服务机构影响力（M_SVC_ORG_TECH_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_TECH_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_TECH_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_TECH_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_ORG_TECH_SCORE |
| 指标名称 | 服务机构影响力 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（机构技术力/影响力画像） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·服务机构画像·技术力评分 / 算法库·服务机构基础指标模型（序号 101） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_ORG_TECH_SCORE.md` |

## 口径定义

王惠五维等权模型中，gkx 只有三维可算：专利覆盖 52.97%、研发（仅上市主体）覆盖 3.12%、案例资讯代理覆盖 55.80%；专家维依赖的 `development_employee` 整列为空，标准维无承载表。评分实为**三维合成**（缺维不入平均、按可用维重新归一），且 min-max 原始值被头部极值支配（中位分 0.01），故落 **部分支持**。本件与 `M_SVC_ORG_TOTAL` 等九件同池（44,153 家），池规则见其 §2.2。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_TECH_SCORE.md` §二（M_SVC_ORG_TECH_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_important_news_info`
- `dwd_org_stock_finance_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：五维中专利（52.97% 覆盖）、研发（仅上市主体 3.12%）、案例资讯代理（55.8%）三维可现转；专家维依赖的 development_employee 整列为空、标准维无承载表，两维始终缺，评分实为三维合成，按部分支持定档
- **基期声明**：截面评分：各维取当前存量/最近年报年，不做年度序列。专利件数为全量存量（dwd_patent.apdt_year 只有 2021—2026，不做年份拆分）；研发维取 2023/2024 年报最近值

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_TECH_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_TECH_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_TECH_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

