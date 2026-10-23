# 候选机构数（M_SVC_REC_CANDIDATE_CNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_REC_CANDIDATE_CNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_REC_CANDIDATE_CNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_REC_CANDIDATE_CNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_REC_CANDIDATE_CNT |
| 指标名称 | 候选机构数 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业服务链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 招引/培育页「共 N 家候选」文案 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_REC_CANDIDATE_CNT.md` |

## 口径定义

「候选机构数」不是统计量，而是招引/培育页在当前筛选条件下 `results.length` 的显示值：产业方向、机构类型、服务环节、规模任意一项变化，N 就变。注册表已于 2026-10-13 由徐滕强判 retired，指标身份撤销；本件不计算任何值，只交付「为什么不可算」的否定性证据。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_REC_CANDIDATE_CNT.md` §二（M_SVC_REC_CANDIDATE_CNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_win_candidate_out`
- `dwd_bid_win_candidate_out_bak_20260911`
- `dwd_org_org_product_info`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：「候选机构数」不是统计量，而是招引/培育页在当前筛选条件下 `results.length` 的显示值：产业方向、机构类型、服务环节、规模任意一项变化，N 就变。注册表已于 2026-10-13 由徐滕强判 retired，指标身份撤销；本件不计算任何值，只交付「为什么不可算」的否定性证据。
- **基期声明**：本件不是年度指标，无基期：注册表 2026-10-13 已判 retired，指标身份被撤销。正文给的是表结构/列名证据与筛选条件阶梯，不是某年的统计值，故 used / missing 均为空表。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_REC_CANDIDATE_CNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_REC_CANDIDATE_CNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_REC_CANDIDATE_CNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-08-28: 侯佳伟 1B 不写 ADS（仍挂 STAT）
- 2026-10-13: human:徐滕强 判定为实时筛选结果集 length，废止指标身份（同 SELECTED_COUNT）
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

