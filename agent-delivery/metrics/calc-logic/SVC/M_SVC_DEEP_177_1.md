# 市场营销服务机构技术力评价模型（M_SVC_DEEP_177_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_DEEP_177_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_DEEP_177_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_DEEP_177_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_DEEP_177_1 |
| 指标名称 | 市场营销服务机构技术力评价模型 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·服务机构技术力评估（SRS seq 121/122） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_DEEP_177_1.md` |

## 口径定义

三维里调研能力、策划能力在 gkx 没有任何承载表：既没有调研报告/样本量表，也没有方案数、比稿中标、执行验收表，连文本级的可代理字段都找不到。唯一有量的是成功项目案例，且只能用资讯条数代理（682 家、资讯合计 20,063 条）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_DEEP_177_1.md` §二（M_SVC_DEEP_177_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_company_punish`
- `dwd_org_important_news_info`
- `dwd_org_invest_info`
- `dwd_org_org_product_info`
- `dwd_org_recruit_info`
- `dwd_org_risk_shixin`
- `dwd_org_shareholder_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维中调研能力、策划能力在 gkx 无任何承载表（连弱代理都缺文本级命中），仅成功项目案例有资讯条数代理 → 只能出单维代理分、不能合成技术力指数；按「有部分维度可取」落部分支持，不因指数不可合成而降为完全不支持
- **基期声明**：资讯表无可靠业务年份口径（采集时点快照），故不设基期、不做趋势；若后续接入 publish_time 可补年度序列，届时需重新声明基期

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_DEEP_177_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_DEEP_177_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_DEEP_177_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

