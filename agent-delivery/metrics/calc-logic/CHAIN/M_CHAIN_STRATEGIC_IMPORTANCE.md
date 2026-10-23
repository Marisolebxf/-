# 战略重要性（M_CHAIN_STRATEGIC_IMPORTANCE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_STRATEGIC_IMPORTANCE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_STRATEGIC_IMPORTANCE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_STRATEGIC_IMPORTANCE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_STRATEGIC_IMPORTANCE |
| 指标名称 | 战略重要性 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链概览战略重要性评分、重点链筛选｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_STRATEGIC_IMPORTANCE.md` |

## 口径定义

三维只剩两维：研发人员整列为空、L2 环节无法归属，12 条链只有 8 条有营收；人工智能 100 分、传感器 0 分，HHI 0.3794，只能判部分支持。

## 计算逻辑说明

```text
Score(c)=100×[0.5×minmax(链营收份额)+0.5×minmax(max(0,利润总额/营收))]；营收为 0 的链 score=null，不参与排名
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_STRATEGIC_IMPORTANCE.md` §二（M_CHAIN_STRATEGIC_IMPORTANCE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_industry_product_tags`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：公式可复现，但三维只剩两维：D2 研发人员占比整列 0/90,926 行非空，直接不可算；D1 依赖的年报正营收全库仅 2,191 行（2.41%），2024 年 47 行，落到 12 条链后只有 8/12 条链有营收、4 条链（智能网联汽车/低空经济/数字创意/生物医药）为零；链归属只有顶层码，旧稿的 L2 环节评价无法复现，本件已上移评价单元；营收高度集中（HHI=0.3794，人工智能占 58.0%），min-max 后排名对单一巨头敏感。四项叠加，只能判部分支持，且不能对外发布为评级。
- **基期声明**：主口径 2024（最后一整年），敏感性 2025。更早年份不采用：正营收记录全库仅 2,191 条、分散在 2013—2025，单年落进 12 链后可比企业只有个位数，且企业集合逐年换人；这是「不采用」而非「缺年补 0」。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_STRATEGIC_IMPORTANCE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_STRATEGIC_IMPORTANCE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_STRATEGIC_IMPORTANCE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

