# 营收（最新年度营业收入）（M_ENT_REVENUE_LATEST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REVENUE_LATEST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REVENUE_LATEST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REVENUE_LATEST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_REVENUE_LATEST |
| 指标名称 | 营收（最新年度营业收入） |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业查询／企业画像 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业详情·营收 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_REVENUE_LATEST.md` |

## 口径定义

gkx 里有 **1,302 家**机构能算出「最新年度营业收入」，中位数 **16,553.27 元**、均值 **138,963,840.3824 元**、P90 **80,058,401.21 元**、最大 **29,800,924,733.43 元**（深圳市燃气集团 2025 年）；但占底册 189,116 家的 **0.6885%**，且 2,032 对跨表可比记录里 **70.62%** 的金额因「元/万元」混填相差整 10,000 倍，真正可对外排名（≥1 亿元）的只有 **118 家**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REVENUE_LATEST.md` §二（M_ENT_REVENUE_LATEST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_foreign_org_annual_financial_info`
- `dwd_org_annual_financial_info`
- `dwd_org_annual_report_asset`
- `dwd_org_stock_finance_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：gkx 里有 **1,302 家**机构能算出「最新年度营业收入」，中位数 **16,553.27 元**、均值 **138,963,840.3824 元**、P90 **80,058,401.21 元**、最大 **29,800,924,733.43 元**（深圳市燃气集团 2025 年）；但占底册 189,116 家的 **0.6885%**，且 2,032 对跨表可比记录里 **70.62%** 的金额因「元/万元」混填相差整 10,000 倍，真正可对外排名（≥1 亿元）的只有 **118 家**。
- **基期声明**：按企取「最新年」，各企锚年不同（见 latest_year_dist）；库内财务年表年份区间 2013—2025 全部在扫描范围内，无排除年。某企最新年营收为空时该企不计入，不向前补年、不写 0

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REVENUE_LATEST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REVENUE_LATEST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REVENUE_LATEST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

