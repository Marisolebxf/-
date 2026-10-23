# 市场规模（M_CHAIN_MARKET_SIZE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_MARKET_SIZE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_MARKET_SIZE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_MARKET_SIZE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_MARKET_SIZE |
| 指标名称 | 市场规模 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链全景／规模体量 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 链详情页「市场规模」卡位（当前应显示「数据不足」而非 0） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_MARKET_SIZE.md` |

## 口径定义

产业链下全部关联企业的年度营业收入合计（只计企业主体，不计机构/人才），单位亿元，统计年与 ENT 年报字段对齐。

> 一句话口径（源件 §0.3）：「部分支持」的定义是「**部分**依赖维可得、其余缺」。本件的**唯一核心依赖维就是金额**：链归属有了（12 链、1,714,457 家）、统计年有了（2024）、企业主键也有了（credit_code），但没有可加的金额，等于核心维不具备。金额缺失不是「少一列辅助信息」，而是「被加数不存在」——$0$ 个可加项之和不是 0，是**未定义**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_MARKET_SIZE.md` §二（M_CHAIN_MARKET_SIZE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_stock_finance_info`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：「部分支持」的定义是「**部分**依赖维可得、其余缺」。本件的**唯一核心依赖维就是金额**：链归属有了（12 链、1,714,457 家）、统计年有了（2024）、企业主键也有了（credit_code），但没有可加的金额，等于核心维不具备。金额缺失不是「少一列辅助信息」，而是「被加数不存在」——$0$ 个可加项之和不是 0，是**未定义**。
- **基期声明**：本件不产出任何年度序列，故无基期可用/缺失之说。年报营收覆盖的年份实测为 2013—2025（299 家、532 条链内记录），但每年样本都是不同企业，不存在可比的同主体两期，未按任何年份摊入分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_MARKET_SIZE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_MARKET_SIZE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_MARKET_SIZE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

