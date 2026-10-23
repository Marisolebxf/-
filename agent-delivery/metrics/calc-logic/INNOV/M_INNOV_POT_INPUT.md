# 产业投入（M_INNOV_POT_INPUT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POT_INPUT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_INPUT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_INPUT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POT_INPUT |
| 指标名称 | 产业投入 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（创新机会） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业潜力 → 投入维度 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_POT_INPUT.md` |

## 口径定义

行业横截面指数 0—100：0.45·研发投入强度 + 0.30·研发投入规模(log10) + 0.25·创新载体密度；固投增长率与人才投入强度因整列为空未入式

> 一句话口径（源件 §0.3）：王惠把「产业投入」拆成三个子维：研发投入强度、固定资产投资增长率、人才投入强度。本库只交付第一个——利润表 `dwd_org_income_statement` 的 `yysr`（营业收入）与 `yffy`（研发费用）在 2024 年合并报表口径下有 1,559 家企业可用，合计研发 5,412.96 亿元、营收 146,772.60 亿元、加权强度 3.69%；固定资产投资与研发人员两组字段在 `dwd_org_annual_financial_info`（90,926 行）里**整列为空**（`fixed_assets`、`arch_development_am`、`development_employee` 非空均为 0）。结构与量都够出行业横截面分，但三子维只交付 1 维，判**部分支持**。本档位与 `code/M_INNOV_POT_INPUT_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POT_INPUT.md` §二（M_INNOV_POT_INPUT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_income_statement`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`
- `dwd_org_tech_tag`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠把「产业投入」拆成三个子维：研发投入强度、固定资产投资增长率、人才投入强度。本库只交付第一个——利润表 `dwd_org_income_statement` 的 `yysr`（营业收入）与 `yffy`（研发费用）在 2024 年合并报表口径下有 1,559 家企业可用，合计研发 5,412.96 亿元、营收 146,772.60 亿元、加权强度 3.69%；固定资产投资与研发人员两组字段在 `dwd_org_annual_financial_info`（90,926 行）里**整列为空**（`fixed_assets`、`arch_development_am`、`development_employee` 非空均为 0）。结构与量都够出行业横截面分，但三子维只交付 1 维，判**部分支持**。本档位与 `code/M_INNOV_POT_INPUT_out.json` 的 `support_judgment` 一致。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 1.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POT_INPUT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_INPUT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POT_INPUT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

