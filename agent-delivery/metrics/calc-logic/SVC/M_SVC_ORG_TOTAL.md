# 入库服务机构总数（M_SVC_ORG_TOTAL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_TOTAL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_TOTAL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_TOTAL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_ORG_TOTAL |
| 指标名称 | 入库服务机构总数 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业服务链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技信息展示系统·产业服务链分析（§1.1.1.2.4.2.7）/ 科技专题服务系统·算法库·基础指标分析模型→服务机构基础指标模型构建（§1.1.1.1.1.1.1.1.4，序号 101，六大体系的人口底座） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_ORG_TOTAL.md` |

## 口径定义

服务机构库的「唯一键计数」在 gkx 侧没有同名池表，但 `dwd_org_org_product_info` 提供了可复算的机构域：45,011 行经营范围文本、按 `org_id` 去重得 44,153 家；再以 `org_id` 回联 `dwd_org_base_info`（189,116 行）命中 44,132 家，回联率 99.95%。人口结构、唯一键与当前数据量三者都足，现在即可经转换得到计数，故判 **完全转换支持**。本件与 `M_SVC_ORG_CNT`、`M_SVC_NEW_CNT`、`M_SVC_ORG_NEW_COUNT`、`M_SVC_ORG_MARKET_HEAT`、`M_SVC_INVEST_Y`、`M_SVC_ORG_TECH_SCORE`、`M_SVC_ORG_COVERAGE_BREADTH`、`M_SVC_ORG_COVERAGE_DEPTH` 共用同一机构池（44,153 家），池规则以本件 §2.2 为准。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_TOTAL.md` §二（M_SVC_ORG_TOTAL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：gkx 无 svc_org_circle，但 dwd_org_org_product_info 有 45,011 行经营范围文本、按 org_id 去重得 44,153 家；与底册 189,116 行回联命中 44,132 家（99.95%）。人口结构+当前数据量均足，现在即可经转换得到唯一键计数
- **基期声明**：截面指标：总数是「当前在池」的唯一键计数，不含年度分母。成立年分布仅作披露（见 M_SVC_NEW_CNT），不参与本件计数。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_TOTAL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_TOTAL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_TOTAL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-13: 库钉 `svc_org_circle`；唯一键所以 `COUNT(*)`
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

