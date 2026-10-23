# 专利质量（M_INNOV_TINN_PATENT_QUALITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_PATENT_QUALITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_PATENT_QUALITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_PATENT_QUALITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_TINN_PATENT_QUALITY |
| 指标名称 | 专利质量 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 技术创新力指标展示页「专利质量评估」卡片（五维雷达 + 领域排名） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| 缺失年份 | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_TINN_PATENT_QUALITY.md` |

## 口径定义

五维**全部无法落到 IPC4**：家族规模维的 `other_Versions` 前缀样本 0/3,000 非空、同族表只有 20,593 行；权利要求维的 `original_text` 是 mediumtext、20,026 行全量取文本 60 秒超时；被引维 20,515 行里只有 475 件能按 `patent_id` 回连主表（0.0162%）；技术宽度维的附加分类未进面板、按 IPC4 统计需全表 294 万行聚合（600 秒断连）；法律状态维 20,000 行覆盖 0.68%、按 `patent_id` 回连 60 秒超时。三张价值附表按 `patent_id` 回连主表的三条查询各跑满 60 秒被中断（4 次复现，错误码 3024）。**不是「分低」，是「算不出」**，故判**完全不支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_PATENT_QUALITY.md` §二（M_INNOV_TINN_PATENT_QUALITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_patent_claim`
- `dwd_patent_family`
- `dwd_patent_legal`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：五维**全部无法落到 IPC4**：家族规模维的 `other_Versions` 前缀样本 0/3,000 非空、同族表只有 20,593 行；权利要求维的 `original_text` 是 mediumtext、20,026 行全量取文本 60 秒超时；被引维 20,515 行里只有 475 件能按 `patent_id` 回连主表（0.0162%）；技术宽度维的附加分类未进面板、按 IPC4 统计需全表 294 万行聚合（600 秒断连）；法律状态维 20,000 行覆盖 0.68%、按 `patent_id` 回连 60 秒超时。三张价值附表按 `patent_id` 回连主表的三条查询各跑满 60 秒被中断（4 次复现，错误码 3024）。**不是「分低」，是「算不出」**，故判**完全不支持**。
- **基期声明**：价值附表无申请年字段且无法回连主表，任何年度分母都不成立

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_PATENT_QUALITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_PATENT_QUALITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_PATENT_QUALITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

