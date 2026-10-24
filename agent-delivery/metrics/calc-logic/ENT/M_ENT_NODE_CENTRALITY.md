# 供应链中心性（M_ENT_NODE_CENTRALITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_NODE_CENTRALITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_NODE_CENTRALITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_NODE_CENTRALITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_NODE_CENTRALITY |
| 指标名称 | 供应链中心性 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业供应链关系分析「关键节点与断链风险识别」、企业详情页「供应链位置」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_NODE_CENTRALITY.md` |

## 口径定义

中心度公式 $C(v)=deg(v)/(|V|-1)$ 只要有一张「企业×企业」边表就能算，图算法一侧完全闭合；问题全部落在边表语义上——gkx 280 张表里没有任何 supply/customer/upstream/downstream 语义的企业级边表，链域只有 1,273 行链定义（`dwd_industry_chain_info`，无 org 对列），所以本件用投资、股东、子公司三类工商股权边建代理图，产物里显式标注 `proxy_is_supply_chain=false`。语义维始终无源，故按 §〇 判**部分支持**。

## 计算逻辑说明

```text
centrality(v) = deg(v) / (|V| - 1)
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_NODE_CENTRALITY.md` §二（M_ENT_NODE_CENTRALITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_purchase_agency_out`
- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_invest_info`
- `dwd_org_shareholder_info`
- `dwd_org_subsidiary_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：公式 deg/(|V|-1) 与建图流程可复现，但 gkx 无企业×企业供应链边表，只能用投资/股东/子公司三类股权边建代理图；供应链语义维度整块缺失。
- **基期声明**：截面件：图快照为 2026-10-22 一次性拉取的三表全量边，不按年份切分，因此无年度基期；分母 |V|-1 用的是当期节点数，跨期不可直接比较。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_NODE_CENTRALITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_NODE_CENTRALITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_NODE_CENTRALITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

