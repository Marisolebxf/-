# 湾区创新投入（M_INNOV_GBA_INVEST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_INVEST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_INVEST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_INVEST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_INVEST |
| 指标名称 | 湾区创新投入 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（湾区创新监测） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 湾区创新监测 → 粤港澳大湾区创新指标数据 → 创新投入 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2019, 2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_INVEST.md` |

## 口径定义

无「创新投入」现成结果面 → 非完全直接支持；依赖表 `gkx.dwd_org_stock_finance_info` 结构可用、40,239 行、研发金额非空 17,504 行，但**只覆盖上市公司**（四城 856 家有年报研发费用，占四城底册 188,774 家的 **0.45%**），且 11 城中仅 4 城有机构底册、港澳在 `dwd_forg_base_info` 中为 0 → **部分支持**。本档位与 `code/M_INNOV_GBA_INVEST_out.json` 的 `support_judgment` 字段一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_INVEST.md` §二（M_INNOV_GBA_INVEST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`
- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：研发金额口径存在且可年度对齐，但只覆盖上市公司（856 家 / 四城底册 188,774 家 = 0.45%）；11 城仅 4 城有机构与研发数据，港澳在 gkx.dwd_forg_base_info 中为 0；24.8% 的公司-年存在「12 月 < 9 月」数值矛盾；无全社会 R&D、无财政科技支出表 —— 故判部分支持，对外只能称「湾区上市公司研发费用合计」，不可当全社会创新投入发布
- **基期声明**：由产物中实际出现的年度键反推：used=[2019, 2020, 2021, 2022, 2023, 2024]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 0.7 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_INVEST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_INVEST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_INVEST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

