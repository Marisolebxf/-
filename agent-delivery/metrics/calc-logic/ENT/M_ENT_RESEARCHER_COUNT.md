# 企业科研人数（M_ENT_RESEARCHER_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RESEARCHER_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RESEARCHER_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RESEARCHER_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_RESEARCHER_COUNT |
| 指标名称 | 企业科研人数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／创新能力／投入侧 |
| 更新频率 | 年 |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 创新能力卡片（企业科研人数）｜ **数据支持度**：**完全不支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_RESEARCHER_COUNT.md` |

## 口径定义

国内 `development_employee` 90,926 行全 NULL（0 个非空、0 个正值）、海外 `rd_staff` 51 行全 NULL、工商年报 `yfrysl` 527,034 行全为空串；全库 32 个相关列命中里只有 5 条候选（含 2 张 `_bak` 备份），生产候选 3 条全部空列；唯一「看起来能顶」的从业人数 `employees_number` 也只有 3,170/90,926 行正值（3.4864%），且口径明令禁止顶替。故判完全不支持，产物为否定性证据（`verdict_kind="negative_evidence"`），不输出 0 值合计。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RESEARCHER_COUNT.md` §二（M_ENT_RESEARCHER_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_foreign_org_annual_financial_info`
- `dwd_foreign_org_annual_financial_info_bak_20260911`
- `dwd_org_annual_financial_info`
- `dwd_org_annual_financial_info_bak_20260911`
- `dwd_org_annual_report_asset`
- `dwd_org_stock_finance_info`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：口径所需的两个字段在 gkx 内均为整列空值：国内 dwd_org_annual_financial_info.development_employee 在 90,926 行中非空 0 行、>0 0 行；国外 dwd_foreign_org_annual_financial_info.rd_staff 在 51 行中非空 0 行、>0 0 行。第三候选 dwd_org_annual_report_asset.yfrysl 在 527,034 行中非空 0 行。三张表覆盖了国内工商年报、上市财务、海外机构三个来源，全部无值，且库内不存在其它研发人员字段，故不是覆盖率不足，而是结构+数据双缺。
- **基期声明**：无基期：口径要求「每企取最新一个有值自然年」，但没有一个有值年份（development_employee 全表 0 行非空），故不声明基期。国内表实测年份区间 2007—2025，仅作字段存在性证据，不构成可用序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RESEARCHER_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RESEARCHER_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RESEARCHER_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

