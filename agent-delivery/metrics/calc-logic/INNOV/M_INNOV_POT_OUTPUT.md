# 产业产值（重建为创新产出读数：专利/论文）（M_INNOV_POT_OUTPUT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POT_OUTPUT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_OUTPUT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_OUTPUT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POT_OUTPUT |
| 指标名称 | 产业产值（重建为创新产出读数：专利/论文） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新分析 |
| 更新频率 | 年度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 创新产出概览卡、区域创新能力对比、年度创新报告「产出」章 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_POT_OUTPUT.md` |

## 口径定义

注册表原义是「特定产业总产值、增加值、利润」，这是一个经济核算指标，需要企业财务或产业统计结果面。gkx 是创新主题库，专利、论文、商标、政策、链上企业都有，唯独没有经济产出表，所以原义在 gkx 不可算。派单书要求把「产出」落到可算的创新产出上，本件因此重建为「专利公开量 + 中文论文量」两个读数，并把服务机构产出维单列为拒拟。两维能算、第三维缺表，故判 **部分支持**，不判完全转换支持。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POT_OUTPUT.md` §二（M_INNOV_POT_OUTPUT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_indicator`
- `dwd_kpi`
- `dwd_org_org_product_info`
- `dwd_patent`
- `dwd_zh_paper`
- `dwd_zh_paper_classification`
- `dwd_zh_paper_year`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：专利与论文两个产出维都能从 gkx 现算（2,939,895 件 / 100,900 篇），但服务机构产出维的源表 `svc_org_card` 在 gkx 逐字命中 0 张表，整维拒拟；注册表原定义「产业总产值/增加值/利润」也没有经济产出表可算。有整维缺失，故判部分支持，不判完全转换支持。
- **基期声明**：专利侧 2017—2020 在 dwd_patent.apdt_year 零行，不按 0 摊入；2025（440,401）与 2026（74,810）是采集残年，不进 CAGR。论文侧基期取 2021—2023，2024 是入库批次峰（32,379 篇，占全库 32.09%），不摊入趋势；2025/2026 为残年。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POT_OUTPUT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_OUTPUT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_OUTPUT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

