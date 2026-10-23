# 配套服务（M_CHAIN_SUPPORT_POWER）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SUPPORT_POWER.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SUPPORT_POWER.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SUPPORT_POWER_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SUPPORT_POWER |
| 指标名称 | 配套服务 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 / 产业链分析 / 区域产业指数评价 / 区域产业指数 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_SUPPORT_POWER.md` |

## 口径定义

政策侧依赖 `dwd_policy_base`（20,000 条存量），但环节命中所需的 `keywords`、`keypoints`、`theme` 三列全部为占位 `'NULL'`，实际只能匹配 `title`，41 个 L1 环节里 19 个退化为链级词、23 个零命中；融资侧依赖 `dwd_org_financing_info`（25,654 行），可用链上企业匹配 15,405 行，但表内**无事件 ID**，无法做事件级去重。两维都能算出数，但都带不可修复的维度退化，故判**部分支持**。本档位与 `code/M_CHAIN_SUPPORT_POWER_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SUPPORT_POWER.md` §二（M_CHAIN_SUPPORT_POWER.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_industry_tags`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：政策侧依赖 `dwd_policy_base`（20,000 条存量），但环节命中所需的 `keywords`、`keypoints`、`theme` 三列全部为占位 `'NULL'`，实际只能匹配 `title`，41 个 L1 环节里 19 个退化为链级词、23 个零命中；融资侧依赖 `dwd_org_financing_info`（25,654 行），可用链上企业匹配 15,405 行，但表内**无事件 ID**，无法做事件级去重。两维都能算出数，但都带不可修复的维度退化，故判**部分支持**。本档位与 `code/M_CHAIN_SUPPORT_POWER_out.json` 的 `support_judgment` 一致。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.39 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SUPPORT_POWER.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SUPPORT_POWER.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SUPPORT_POWER_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

