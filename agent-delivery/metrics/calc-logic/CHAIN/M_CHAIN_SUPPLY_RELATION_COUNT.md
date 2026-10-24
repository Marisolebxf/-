# 产业链供应链关系数（M_CHAIN_SUPPLY_RELATION_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SUPPLY_RELATION_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SUPPLY_RELATION_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SUPPLY_RELATION_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SUPPLY_RELATION_COUNT |
| 指标名称 | 产业链供应链关系数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链图谱／供应链关系 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 图谱供应链视图、链主企业上下游面板 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_SUPPLY_RELATION_COUNT.md` |

## 口径定义

供应方与采购方在 gkx 内**都**可识别（中标方 `external_id` 39,403/39,520 行；采购方 `credit_no` 39,628/39,975 行），但两端按 `project_number` 只能连上 **106/32,029（0.33%）**——关系边 99.67% 无法闭合，属零等价可算面。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SUPPLY_RELATION_COUNT.md` §二（M_CHAIN_SUPPLY_RELATION_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_base_out`
- `dwd_bid_purchase_agency_out`
- `dwd_bid_win_candidate_out`
- `dwd_en_paper_related`
- `dwd_id`
- `dwd_scholar_paper_relation`
- `dwd_zh_paper_related`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：gkx 有采购方表 `dwd_bid_purchase_agency_out`（39975 行、带信用代码 39628 行），也有中标方表（39520 行、带 external_id 39403 行，99.70%），但两端按 project_number 连接时，公告侧 32029 个不同项目号只有 106 个命中（覆盖率 0.33%）。关系边只能在 0.33% 的子集上成立，不足以支撑「供应链关系数」；gkx 亦无任何企业—企业关系表（模式扫描 5 张，全为论文/学者关系）。按先例 M_INNOV_TINN_MARKET（覆盖 0.776% 判完全不支持）同档判完全不支持。
- **基期声明**：截面指标：关系数是「当前存量边数」，不构造年度序列；招投标表本身无生效年字段，故不声明任何基期年份。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SUPPLY_RELATION_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SUPPLY_RELATION_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SUPPLY_RELATION_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

