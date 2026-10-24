# 服务机构产业领域覆盖评分（M_SVC_ORG_COVERAGE_DEPTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_COVERAGE_DEPTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_COVERAGE_DEPTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_COVERAGE_DEPTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_ORG_COVERAGE_DEPTH |
| 指标名称 | 服务机构产业领域覆盖评分 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业领域覆盖度） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业服务链分析·服务机构画像·覆盖评分 / 算法库·服务机构基础指标模型（序号 101） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_ORG_COVERAGE_DEPTH.md` |

## 口径定义

本件是「广度 × 深度」两轴等权评分：广度轴取六类服务类型（M_SVC_ORG_COVERAGE_BREADTH），深度轴取六环节（research/transfer/ip/testing/market/pilot），各归一化到 0—1 后 50/50 合成 0—100。两轴都全池可算，但都已语义降级——原广度是 15 产业集群，原深度是 1,261 个 `link_code`；gkx 既无集群字典，`tags` 的 INB13xx 与 `chain_info` 的 INB12xx 也不是同一码域。故落 **部分支持**。本件与 `M_SVC_ORG_TOTAL` 等九件同池（44,153 家）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_COVERAGE_DEPTH.md` §二（M_SVC_ORG_COVERAGE_DEPTH.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：两轴可算但都已语义降级：广度轴由 15 产业集群降为六类服务类型（gkx 无集群字典），深度轴由产业服务链 1,261 个 link_code 降为六环节（tags 与 chain_info 码域不通、底册对齐仅 3.5%）；评分只适合同池相对比较，不能当原口径的绝对覆盖评分
- **基期声明**：截面评分：两轴都取自当前经营范围文本，无年度分母；成立年不参与评分。不按年补 0、不做年度序列

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_COVERAGE_DEPTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_COVERAGE_DEPTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_COVERAGE_DEPTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

