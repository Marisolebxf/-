# 断链风险等级（M_ENT_SUPPLY_CHAIN_RISK）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SUPPLY_CHAIN_RISK.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SUPPLY_CHAIN_RISK.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SUPPLY_CHAIN_RISK_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_SUPPLY_CHAIN_RISK |
| 指标名称 | 断链风险等级 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／风险洞察／供应链关系 |
| 更新频率 | 月度/事件触发 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业画像「断链风险」卡 + 风险清单｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | ["1989—2026（occur_period 实际覆盖，D4 取各企业最近 8 期）"] |
| 缺失年份 | ["2026 年后续季度（库内止于 202603）"] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_SUPPLY_CHAIN_RISK.md` |

## 口径定义

四维韧性指数里，应收账款、前五大客户、存货周转三维在 gkx 无字段（全库 0 列），仅绩效波动维可由 40,239 行财务序列真算、覆盖 918 家上市公司；等级不可出，故判部分支持。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SUPPLY_CHAIN_RISK.md` §二（M_ENT_SUPPLY_CHAIN_RISK.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_main_business_composition_area`
- `dwd_org_company_abnormal`
- `dwd_org_company_illegal`
- `dwd_org_company_punish`
- `dwd_org_risk_shixin`
- `dwd_org_risk_zhixing`
- `dwd_org_stock_finance_info`
- `dwd_safety`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维韧性指数中 D1 应收账款、D2 前五大客户、D3 存货周转三个维度在 gkx 与开发库均无字段/无表；仅 D4 经济绩效敏感性（营收/利润波动）可由 gkx.dwd_org_stock_finance_info 真算，覆盖 972 家上市公司。等级需要四维加权 + 归一化总体，缺三维不可出，故判部分支持、只交付 D4 单维得分。
- **基期声明**：D4 不用固定自然年窗口，而是每家取最近 8 个有值期次（季度），避免早年稀疏年份被当成 0；occur_period 为 YYYYMM 文本，198912 起有值，202603 为库内最新期。没有把缺失年份按 0 摊入分母：期次不足 4 期的企业直接不进样本。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SUPPLY_CHAIN_RISK.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SUPPLY_CHAIN_RISK.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SUPPLY_CHAIN_RISK_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

