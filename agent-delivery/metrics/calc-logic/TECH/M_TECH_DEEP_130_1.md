# 全景技术链模型（M_TECH_DEEP_130_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DEEP_130_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_130_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_130_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_DEEP_130_1 |
| 指标名称 | 全景技术链模型 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术链全景视图（DS-02-TECHGRAPH / TOPIC-TECH-05）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_DEEP_130_1.md` |

## 口径定义

节点面（634 个 IPC4 域、2,009,365 件基期专利）与边面（同专利共类共现、五段等距抽样 58,165 行）可以在 gkx 上当日重建，图结构指标（连通分量、度分布、密度）可复算；但结果面 `tech_chain_node` / `tech_chain_edge` / `tech_chain_events` 与域名字典 `tech_domain` 在 280 张基表中零命中，需求点名的论文、技术标准、产品三类节点属性也找不到可挂接键——结构缺结果面、数据缺三维属性，按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DEEP_130_1.md` §二（M_TECH_DEEP_130_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_event`
- `dwd_id`
- `dwd_merger_acquisition_events_party_info`
- `dwd_patent`
- `dwd_patent_title`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：节点面（634 个 IPC4 域）与边面（同专利共类共现，抽样）可当日重建，图结构指标可复算；但结果面 tech_chain_* 三表在 gkx 不存在，需求点名的论文/标准/产品三类节点属性均无可挂接键，边集为抽样共类而非标注依赖——结构与数据两侧都始终缺维。
- **基期声明**：dwd_patent.apdt_year 全库只有 2021—2026；2025（440,401）与 2026（74,810）为采集残年，不进入同比与基期。2017—2020 零行，不得按 0 摊入分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DEEP_130_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_130_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_130_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

