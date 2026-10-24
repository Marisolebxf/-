# 查询结果·技术热度（M_TECH_HEAT_QUERY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_HEAT_QUERY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_HEAT_QUERY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_HEAT_QUERY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_HEAT_QUERY |
| 指标名称 | 查询结果·技术热度 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术搜索热词（TOPIC-TECH-02 / DS-02-TECHQUERY）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_HEAT_QUERY.md` |

## 口径定义

以**深圳**为规模与年度分布的分母，用 40 个 IPC4 × 各 3,000 件的专利关键词抽样（117,500 条有效数组）反查 9 个查询词，给出「命中样本数 / 覆盖域数 / 子标签 TF 与份额 / 术语集中度 HHI / 深圳年度估算件数」五列。9 个查询里 7 个非空、2 个零命中（生物医药、大模型）；需求另点名的资讯侧三项（资讯数量、发布时间、阅读量）在库内没有任何承载，故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_HEAT_QUERY.md` §二（M_TECH_HEAT_QUERY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：「子标签出现频次 + 出现时间」两要素在专利关键词侧可算（9 个查询里 7 个非空、TF/HHI/年度矩阵齐备）；需求另点名的资讯侧三项（资讯数量、发布时间、阅读量）在库内零承载，故落部分支持。
- **基期声明**：年度估算只覆盖库内真实存在的 2021—2024；2017—2020 在 dwd_patent 零行，不补零、不外推；2025/2026 属采集残年，不进年度矩阵。
- **复现实测耗时**：约 0.87 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_HEAT_QUERY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_HEAT_QUERY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_HEAT_QUERY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

