# 服务广度（M_SVC_ORG_COVERAGE_BREADTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_COVERAGE_BREADTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_COVERAGE_BREADTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_COVERAGE_BREADTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_ORG_COVERAGE_BREADTH |
| 指标名称 | 服务广度 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（服务机构覆盖度） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业服务链分析·服务机构画像·服务广度 / 算法库·服务机构基础指标模型（序号 101） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_ORG_COVERAGE_BREADTH.md` |

## 口径定义

原口径是「机构覆盖的 15 个产业集群数」，gkx 没有 `industry_cluster` 与 `industry_cluster_map` 两张字典表，`dwd_org_industry_tags` 与底册信用码仅约 3.5% 对齐且码域不通，无法重建集群广度。本件改用**六类服务类型**（IP/FINANCE/HR/MKT/CONSULT/INNOV）的去重个数作代理，公式同构（去重计数）、语义降级（集群→服务类型），故落 **部分支持**。本件与 `M_SVC_ORG_TOTAL` 等九件同池（44,153 家）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_COVERAGE_BREADTH.md` §二（M_SVC_ORG_COVERAGE_BREADTH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_industry_tags`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：原口径的 15 产业集群字典（industry_cluster / industry_cluster_map）在 gkx 不存在；dwd_org_industry_tags 与底册信用码仅 3.5% 对齐、且 INB13xx 与 chain_info 的 INB12xx 不是同一码域，无法重建集群广度。改用六类服务类型去重个数作代理，公式同构但语义降级，按部分支持定档
- **基期声明**：截面指标：经营范围是当前状态，没有历史版本；广度计数不含年度分母。成立年只用于披露池龄结构，不参与广度

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_COVERAGE_BREADTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_COVERAGE_BREADTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_COVERAGE_BREADTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版
- 2026-10-13: 挂起 / 自建表误写已撤回
- 2026-10-13: 0.3.0 对齐企业 15 集群
- 2026-10-13: 0.3.1 正文去掉对演示 8 领域字典的叙述；领域键只认 `industry_cluster`
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

