# M_TALENT_DEEP_160_1（M_TALENT_DEEP_160_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_160_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_160_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_160_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DEEP_160_1 |
| 指标名称 | M_TALENT_DEEP_160_1 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才画像页「合作者链路 + 跨城连接 + 枢纽识别」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| 缺失年份 | [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DEEP_160_1.md` |

## 口径定义

关系边（1,187,606 行 / 20,011 个 ego / 899,662 个合作者节点）与机构名可全量现读，深圳子图、跨城连接、枢纽识别都能算；但每个 ego 只保留前 100 个合作者（34.03% 已顶满）、合作者姓名非空仅 16.19%、ego 侧根本没有姓名列、表内无年份，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_160_1.md` §二（M_TALENT_DEEP_160_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar`
- `dwd_scholar_coauthor`
- `dwd_scholar_research_direction`
- `dwd_scholar_work_experience`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：关系边（1,187,606 行 / 20,011 ego / 899,662 合作者）与机构名可全量现读，深圳子图、跨城连接、枢纽识别都能算；但（a）每个 ego 只保留前 100 个合作者，（b）ego 侧无姓名、只能靠履历表补机构，（c）表内无年份，趋势链不可算，（d）ego id 与主档 dwd_scholar 只有 1,839 个交集 → 部分支持。
- **基期声明**：关系链表无任何年份字段：dwd_scholar_coauthor 只有 create_time（数据物化时点，实测区间见 probes.create_time_span），无合作年份、无合著首发年。故本文只交截面链路，不交时间序列；2017—2026 全部年份在 missing 中声明，不按 0 摊入任何比率。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_160_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_160_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_160_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

