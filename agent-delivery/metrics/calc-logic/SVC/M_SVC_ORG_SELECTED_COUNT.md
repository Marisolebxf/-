# 当前分析机构数（M_SVC_ORG_SELECTED_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_SELECTED_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_SELECTED_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_SELECTED_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_ORG_SELECTED_COUNT |
| 指标名称 | 当前分析机构数 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（服务机构库 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 产业服务链分析·服务机构库·页面右上角「当前分析 N 家」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_ORG_SELECTED_COUNT.md` |

## 口径定义

「当前分析 N 家」的 N 是前端会话里 `selection.length`，即用户勾选了几家机构。它没有总体、没有参考期、没有去重规则、不持久化、跨用户不可比，**不是统计指标**；gkx 280 张表里也没有任何 `svc_*` 表族可以承载它。2026-10-13 徐滕强拍板废止，本件按 **完全不支持** 归档，不补数、不替代、不灌库。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_SELECTED_COUNT.md` §二（M_SVC_ORG_SELECTED_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_org_product_info`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：不适用（已废止）：页面 N = 前端会话 selection.length，不是统计指标；gkx 无 svc_* 表，无会话态承载，也不应为它灌数。存量替代（44,153）与 selection.length 的相关性按定义为 0，不能冒充
- **基期声明**：不适用：会话语义无参考期。若改为「机构关注度」类产品行为指标，须另立条目并重新定义总体/参考期/去重规则，不能沿用本 ID

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_ORG_SELECTED_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_SELECTED_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_ORG_SELECTED_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-13: 先钉会话数组 length
- 2026-10-13: 判定为 UI 勾选家数，废止指标身份
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

