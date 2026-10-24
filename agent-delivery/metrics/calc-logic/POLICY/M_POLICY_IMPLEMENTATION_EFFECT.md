# 落地实效性（M_POLICY_IMPLEMENTATION_EFFECT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_IMPLEMENTATION_EFFECT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_IMPLEMENTATION_EFFECT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_IMPLEMENTATION_EFFECT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_IMPLEMENTATION_EFFECT |
| 指标名称 | 落地实效性 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 政策分析页「落地实效」城市对比卡（设计位）、深圳政策现状分析指标体系（设计位） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md` |

## 口径定义

三维各要一个输入：启动维要有效实施日、覆盖维要支持对象清单、反馈维要调查表。第一个字段在表内但 100% 是零日期，第二个在 JSON null 里，第三个两库都没有。**三维全断**，不是「缺一维」，是「一维都拼不起来」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_IMPLEMENTATION_EFFECT.md` §二（M_POLICY_IMPLEMENTATION_EFFECT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：三维全部不可算：启动维的 implementation_date 全为 0000-00-00（归零后 0 行有效），覆盖维的 support_object 在 20,000 行 JSON null 里取不到，反馈维两库均无调查表。按正本「缺维不进平均」，可进平均的完整维 0 个，分数不存在；强行出 0 分等于把导入缺陷写成政策事实。
- **基期声明**：截面评估：正本按「统计日」取当前有效政策，不设年度序列；本件不出分，故无基期年。若将来补数后按年出分，须先解决 2022-09 起 16 个月的发布断档，否则某年启动率为 0 会是断档而不是真实归零。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_IMPLEMENTATION_EFFECT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_IMPLEMENTATION_EFFECT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_IMPLEMENTATION_EFFECT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

