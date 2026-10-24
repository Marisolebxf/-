# 环节平均服务深度（M_SVC_CHAIN_SEGMENT_AVG_DEPTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_CHAIN_SEGMENT_AVG_DEPTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_CHAIN_SEGMENT_AVG_DEPTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_CHAIN_SEGMENT_AVG_DEPTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_CHAIN_SEGMENT_AVG_DEPTH |
| 指标名称 | 环节平均服务深度 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·全链路可视化（SRS seq 123）的节点深度标签 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_CHAIN_SEGMENT_AVG_DEPTH.md` |

## 口径定义

这个指标的结构最干净：分母是六环节机构数（可算），分子是「机构×环节服务深度分」（不存在）。公式 avg_depth = AVG(depth_i) 本身没有争议，争议在于 depth_i 从哪来——需规只给了维度名，旧稿登记为待建（SVC 侧 `svc_*` 深度表未建、口径 Q-SVCCHAIN-02 未签）。

## 计算逻辑说明

```text
avg_depth(s) = AVG(depth_i), i ∈ {org: stage(org)=s}；空 → null（不伪造 0）
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_CHAIN_SEGMENT_AVG_DEPTH.md` §二（M_SVC_CHAIN_SEGMENT_AVG_DEPTH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_company_punish`
- `dwd_org_important_news_info`
- `dwd_org_invest_info`
- `dwd_org_org_product_info`
- `dwd_org_recruit_info`
- `dwd_org_risk_shixin`
- `dwd_org_shareholder_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：分母与分组可算（六环节 44,153 家口径）；分子「机构×环节服务深度分」无源：口径未签（Q-SVCCHAIN-02）且 gkx 无任何 svc_* 深度表/列 → 全部分格为「—」
- **基期声明**：本件不产出任何深度数值：分子（机构×环节服务深度分）在 gkx 与 live 均无来源，口径未签（Q-SVCCHAIN-02），故不存在可声明的基期窗口；分母侧的环节计数为截面存量。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_CHAIN_SEGMENT_AVG_DEPTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_CHAIN_SEGMENT_AVG_DEPTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_CHAIN_SEGMENT_AVG_DEPTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版（演示态）
- 2026-10-13: 0.2.0 目标口径锁定（六环节 + circle 人口 + AVG(depth)）；不挂 MODEL 引用；双缺口写明
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

