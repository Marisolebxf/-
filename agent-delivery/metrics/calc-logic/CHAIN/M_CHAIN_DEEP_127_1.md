# 深圳问题识别模型（M_CHAIN_DEEP_127_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_127_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_127_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_127_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_127_1 |
| 指标名称 | 深圳问题识别模型 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链评价 |
| 二级模块 | 深圳专题诊断 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | ["2021", "2022", "2023", "2024"] |
| 缺失年份 | ["2025", "2026"] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_DEEP_127_1.md` |

## 口径定义

旧稿的结果面 `chain_sz_problem` 在 `gkx` 内零行，但五个判定位的原子量全部可得， 本件用「深圳 vs 全国强度差 + 完整度绝对线」现算，判 `部分支持`： 能给出逐链问题计数，但「问题」的定义是本件自定义，不是旧表的外部模型口径。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_127_1.md` §二（M_CHAIN_DEEP_127_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_financing_info`
- `dwd_org_industry_product_tags`
- `dwd_org_industry_tags`
- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：旧稿的结果面 `chain_sz_problem` 在 `gkx` 内零行，但五个判定位的原子量全部可得， 本件用「深圳 vs 全国强度差 + 完整度绝对线」现算，判 `部分支持`： 能给出逐链问题计数，但「问题」的定义是本件自定义，不是旧表的外部模型口径。
- **基期声明**：技术维按 application_year ≤2024 截断；产品/融资/政策/完整度四维无年度窗口，故为截面问题清单，不做年度对比。
- **复现实测耗时**：约 1.46 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_127_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_127_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_127_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

