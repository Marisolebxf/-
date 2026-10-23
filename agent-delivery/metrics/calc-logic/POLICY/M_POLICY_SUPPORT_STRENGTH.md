# 支持力度（M_POLICY_SUPPORT_STRENGTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_SUPPORT_STRENGTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_SUPPORT_STRENGTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_SUPPORT_STRENGTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_SUPPORT_STRENGTH |
| 指标名称 | 支持力度 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 区域政策创新成果综合评价页「支持力度」指标卡、城市政策对比页的三维之一、政策全景页城市榜 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_SUPPORT_STRENGTH.md` |

## 口径定义

正本的三维里，「扶持力度档位」需要金额或档位字段。政策表 33 列里**一个金额类列都没有**（全库 123 个金额类列全部落在 `dwd_bid_*` 招标表），`policy_support` 20,000 行全为 JSON null；「政策层级」与「政策数量」两维可从 `rank`/`city` 直接算。**三维缺一维，且缺的正是最核心的那一维**，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_SUPPORT_STRENGTH.md` §二（M_POLICY_SUPPORT_STRENGTH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：正本的三维里，「扶持力度档位」需要金额或档位字段。政策表 33 列里**一个金额类列都没有**（全库 123 个金额类列全部落在 `dwd_bid_*` 招标表），`policy_support` 20,000 行全为 JSON null；「政策层级」与「政策数量」两维可从 `rank`/`city` 直接算。**三维缺一维，且缺的正是最核心的那一维**，故判**部分支持**。
- **基期声明**：截面件：政策池取 20,000 条存量全表，不按年度切窗。支持力度度量的是存量供给结构，与单一年份无关；若改按年度切分，2023/2024 的零行会被误读成「支持力度归零」，而那是采集断档（publish_year 分布见 policy_dims_20261023.json）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_SUPPORT_STRENGTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_SUPPORT_STRENGTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_SUPPORT_STRENGTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

