# 核心供应商数（M_ENT_CORE_SUPPLIER_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CORE_SUPPLIER_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CORE_SUPPLIER_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CORE_SUPPLIER_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_CORE_SUPPLIER_COUNT |
| 指标名称 | 核心供应商数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业供应链关系 |
| 更新频率 | 周 |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 企业画像「核心供应商数」卡｜ **数据支持度**：**完全不支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_CORE_SUPPLIER_COUNT.md` |

## 口径定义

核心供应商 = 供应商集合 S 内按「本企出资额」取 TOP5；S 在 gkx 与开发库均无数据（同名表 0 行），核心标记列 0 个。用投资边顶替 S 会退化成「出度截断」（19,611 家投资方里 1,952 家恒得 5），不是核心供应商数，故判完全不支持。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CORE_SUPPLIER_COUNT.md` §二（M_ENT_CORE_SUPPLIER_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_win_candidate_out`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：指标 = 在供应商集合内筛 is_core_supplier=1 的计数。gkx 既无供应商边表（母集合 S 缺失），也无 is_core_supplier / purchase_amount / supplier_rank 类核心标记；把投资边按出资额 TOP5 试算得到的是『投资方 → 被投企业』榜，方向与供应边相反，且金额列单位不自洽 → 结构与数据都不具备可算闭环。
- **基期声明**：负结论件，无指标值，不涉及基期；核心标记是时点属性而非年度量，本件不构造任何年度序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CORE_SUPPLIER_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CORE_SUPPLIER_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CORE_SUPPLIER_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

