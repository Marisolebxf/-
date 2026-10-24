# 发展战略引导力评估（M_POLICY_DS_07_POLICY_GUARD_001）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DS_07_POLICY_GUARD_001.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DS_07_POLICY_GUARD_001.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DS_07_POLICY_GUARD_001_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_DS_07_POLICY_GUARD_001 |
| 指标名称 | 发展战略引导力评估 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·科技创新评估·政策与条件保障力指标展示（原型页不挂本 metricId） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_DS_07_POLICY_GUARD_001.md` |

## 口径定义

三维里前瞻性可算（标题层命中 1,085 条，5.42%），系统性只有 2 条政策有引用（0.01%），针对性依赖的 `policy_support` 全表 0 行有效、整维不可算。按王惠「缺维不进平均」合成得 2.72 分（2/3 维参与）。分数低不是「政策前瞻性差」，而是三维里两维的真实值都接近 0、等权平均被单维拖平；故落**部分支持**，并把「分数不可读成质量」写进 §四。

## 计算逻辑说明

```text
三维比率等权 ×100；缺维不进平均（D3 不参与分母）
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DS_07_POLICY_GUARD_001.md` §二（M_POLICY_DS_07_POLICY_GUARD_001.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维中前瞻性可算（1,085/20,000=5.42%，标题层）；系统性只有 2 条政策有引用（0.01%）；针对性 policy_support 全表 0 行有效，整维不可算。缺一个必需维 → 部分支持。
- **基期声明**：本指标为截面文本标记率，不设跨年基期。政策表年份只用于背景描述，不进入任何分母；2022 年后为采集残片（2023 年 0 行），不外推。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DS_07_POLICY_GUARD_001.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DS_07_POLICY_GUARD_001.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DS_07_POLICY_GUARD_001_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

