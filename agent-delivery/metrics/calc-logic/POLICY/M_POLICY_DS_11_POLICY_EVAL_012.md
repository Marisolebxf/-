# 智能摘要与结论推送（M_POLICY_DS_11_POLICY_EVAL_012）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DS_11_POLICY_EVAL_012.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DS_11_POLICY_EVAL_012.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DS_11_POLICY_EVAL_012_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_DS_11_POLICY_EVAL_012 |
| 指标名称 | 智能摘要与结论推送 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·政策分析评价·结果解读报告多维展示（DS-11-POLICY-EVAL） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_DS_11_POLICY_EVAL_012.md` |

## 口径定义

三维里信息覆盖度与结论条数可算（主料 94.77%、上下文 99.98%、抽样 1,999/2,000 可出结论），推送就绪所需的 `dwd_policy_summary(push_status)` 与编辑日志表在 `gkx` 中均不存在，整维不可算。按「缺维不进平均」合成得 **94.99 分**（2/3 维参与）；该分数是「就绪度」而非「质量」，因为库内没有人工参考摘要、没有人工评分、没有推送回流。故落**部分支持**。

## 计算逻辑说明

```text
D1=(主料率+上下文率)/2；D2=min(1, 平均句数/3)；D3 缺维不进平均；可算维等权 ×100
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DS_11_POLICY_EVAL_012.md` §二（M_POLICY_DS_11_POLICY_EVAL_012.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_policy_base`
- `dwd_policy_summary`
- `dwd_policy_summary_edit_log`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：主料与上下文字段可算（正文 19,203 行、摘要 12,159 行、标题 20,000 行），结论句可抽取；推送就绪所需的 dwd_policy_summary(push_status) 与编辑日志表在 gkx 中均不存在 → 三维缺一维，判部分支持。
- **基期声明**：本指标为截面就绪度，不设跨年基期。结论句抽样按 id 随机（seed=42），不用年份分层；政策表 2023 年起无数据，不做年度外推。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DS_11_POLICY_EVAL_012.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DS_11_POLICY_EVAL_012.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DS_11_POLICY_EVAL_012_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

