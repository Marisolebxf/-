# 年度新增服务机构数（M_SVC_ORG_NEW_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_NEW_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_NEW_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_NEW_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_ORG_NEW_COUNT |
| 指标名称 | 年度新增服务机构数 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（新增服务机构动态的计数版） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业服务链分析·新增服务机构动态·年度柱图 / 算法库·服务机构基础指标模型（序号 101） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022] |
| 缺失年份 | [2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_ORG_NEW_COUNT.md` |

## 口径定义

本件是 `M_SVC_NEW_CNT` 的计数孪生件：同一机构池（44,153 家）、同一成立年字段、同一 2013—2022 窗口，输出年度计数、累计区间与近年结构切片；差异只在本件更强调「纯计数与累计」而不做叙事。毛出生可算，净新增与近三年不可算，故落 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_NEW_COUNT.md` §二（M_SVC_ORG_NEW_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：出生存量序列可现转（成立年覆盖 99.95%、2013—2022 十个完整年）；但出清侧（注销/吊销）缺失、2023—2025 成立年右截断，「净新增」与近年趋势均不可算
- **基期声明**：2013—2022 为十个完整年，进趋势与环比；2023—2025 成立年右截断（218/66/12 家）按缺失处理、不进分母；2026 无行。序列为「出生存量」口径：历年新设且至今仍在池，不含已退出机构

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_NEW_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_NEW_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_NEW_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-13: 钉死工商成立年、全库一条按年
- 2026-10-13: formula 拆成 [SEED]/[SERVE]/[PAGE] 可执行 SQL，版本 0.2.1
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

