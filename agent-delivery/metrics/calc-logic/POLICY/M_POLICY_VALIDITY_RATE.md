# 政策有效率（M_POLICY_VALIDITY_RATE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_VALIDITY_RATE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_VALIDITY_RATE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_VALIDITY_RATE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_VALIDITY_RATE |
| 指标名称 | 政策有效率 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 周 |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 政策分析页「现行有效政策占比」指标卡、政策库筛选器的「有效/失效」分档 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_VALIDITY_RATE.md` |

## 口径定义

结构在、数据不在：`status` 与 `expire_date` 两列都在 `information_schema` 里，类型也对，但一列的取值域只有 1 个值、另一列 20,000 行全空。公式可执行、结果恒为 100.00%，**没有任何判别力**，因此判**完全不支持**，而不是「完全转换支持」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_VALIDITY_RATE.md` §二（M_POLICY_VALIDITY_RATE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：结构在、数据不在：`status` 与 `expire_date` 两列都在 `information_schema` 里，类型也对，但一列的取值域只有 1 个值、另一列 20,000 行全空。公式可执行、结果恒为 100.00%，**没有任何判别力**，因此判**完全不支持**，而不是「完全转换支持」。
- **基期声明**：截面指标，不设年度分母。本件不设基期不是因为「不需要时间」，而是因为失效判定所需的 expire_date 整列为空，任何按年切分都不会改变结论。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_VALIDITY_RATE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_VALIDITY_RATE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_VALIDITY_RATE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

