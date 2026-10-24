# 查询结果·服务类型分布（M_SVC_TYPE_DIST_QUERY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_TYPE_DIST_QUERY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_TYPE_DIST_QUERY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_TYPE_DIST_QUERY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_TYPE_DIST_QUERY |
| 指标名称 | 查询结果·服务类型分布 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（科技专题数据查询 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·数据查询·推荐图表分析·服务生态多样性图 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_TYPE_DIST_QUERY.md` |

## 口径定义

查询结果·服务类型分布是查询链路上的实时分桶逻辑，不是全库统计：对象是当前查询命中的 `org_id` 集合、度量是每桶去重计数、结果不落 ADS。gkx 没有 `svc_type` 主数据列，六类只能由经营范围词表重建，且「INNOV 优先」与「IP 优先」两套优先级给出的分布整体换形（INNOV 19,879 vs 1,544），故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_TYPE_DIST_QUERY.md` §二（M_SVC_TYPE_DIST_QUERY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：查询结果·服务类型分布是查询链路上的实时分桶逻辑，不是全库统计：对象是当前查询命中的 `org_id` 集合、度量是每桶去重计数、结果不落 ADS。gkx 没有 `svc_type` 主数据列，六类只能由经营范围词表重建，且「INNOV 优先」与「IP 优先」两套优先级给出的分布整体换形（INNOV 19,879 vs 1,544），故判 **部分支持**。
- **基期声明**：查询态指标，无年度基期：度量是当前查询会话命中的 org_id 集合在六类上的即时分桶，随查询条件实时变，不落 ADS、不预聚合。used / missing 均为空表；正文给的是若干可复算查询集合的示例分布，不是某年的全库统计。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_TYPE_DIST_QUERY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_TYPE_DIST_QUERY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_TYPE_DIST_QUERY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-08-27: 侯佳伟 1A 2A 3A（边界锁定、过渡分桶列、空态语义）
- 2026-10-13: 徐滕强定性"查询代码逻辑非统计指标"，选 A 转查询态口径卡（不废止，保留指标身份作查询页口径真源），seed v0.2.0
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

