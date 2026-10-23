# 要素影响力（期刊侧）（M_INNOV_DS_FACTORS_015）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_015.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_015.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_015_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_FACTORS_015 |
| 指标名称 | 要素影响力（期刊侧） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（科技信息展示系统） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 科技全域态势 → 要素影响力分析（期刊要素） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_FACTORS_015.md` |

## 口径定义

开发库无「期刊影响力评分」结果面 → 非完全直接支持；`gkx` 侧 `impact_score` 在中文 2,796 本、英文 605 本刊上**非空值均为 0**（整列空壳）→ 占 0.50 权重的主维结构性缺测；重归一后仅剩「发文量 0.5 + 累计被引 0.5」两个规模量，可对 2,796 本中文刊出稳定排序，但语义已从「影响力」退化为「体量」；英文刊更退化为发文量单维 → 三维缺一维且另两维语义偏移，判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_015.md` §二（M_INNOV_DS_FACTORS_015.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_journal`
- `dwd_en_paper`
- `dwd_zh_author`
- `dwd_zh_journal`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：期刊影响力三维中占 0.50 权重的影响指数（impact_score）在 gkx.dwd_zh_journal / dwd_en_journal 为 0 非空值，属结构性缺测；缺测维重归一后只剩「发文量 0.5 + 累计被引 0.5」，实际可算 2,796 本中文期刊（英文 605 本退化为发文量单维）。两维均为规模量，故判部分支持：可出相对排序，不可宣称复现影响指数。
- **基期声明**：期刊侧指标为 dwd_zh_journal 全量截面汇总（载文量/基金论文占比/被引），不构造年度序列，因此不使用基期分母；不存在把缺失年份按 0 摊入分母的情形。
- **复现实测耗时**：约 9.8 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_015.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_015.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_015_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

