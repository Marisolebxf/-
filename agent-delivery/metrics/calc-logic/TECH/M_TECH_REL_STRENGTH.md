# 技术关联强度（M_TECH_REL_STRENGTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_REL_STRENGTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_REL_STRENGTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_REL_STRENGTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_REL_STRENGTH |
| 指标名称 | 技术关联强度 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术关联网络（TOPIC-TECH-09 / DS-02-TECHGRAPH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_REL_STRENGTH.md` |

## 口径定义

以**深圳主体**唯一口径（77,846 个申请人名称），用「同一申请人在两个 IPC4 域都有 ≥3 件专利」构造共主体矩阵，再用 NPMI 算 238 个域两两关联，得到 **12,797 条边**、**0 个孤立节点**、度中位数 114、最强边 C01B—C01G（NPMI 0.8187、强度 90.94）；但共类关联做不了（1,720,243 个 pn 中跨 IPC4 的 pn = 0，面板按主分类落盘），关系流向（引用、许可、上下游）无字段，故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_REL_STRENGTH.md` §二（M_TECH_REL_STRENGTH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：关联强度可复算（12,797 条边、238 个节点），但两条关键证据缺源：① 共类关联做不了——面板只保留主分类，跨域 pn = 0；② 关系流向（引用、许可、上下游方向）无字段，`dwd_patent_transfer` 的 pn 为公开号、与面板内部哈希不同码域，无法落域。故只能交付「深圳主体共同布局强度」无向图，不能交付弦线图的关系流向。
- **基期声明**：域件数只遍历 2021—2024（2017—2020 零行），申请人集合用全期件数（含 2021 前申请、但在库内只存在于 2021—2026 记录中）；2025/2026 残年不参与门槛判断。缺失年未按 0 摊入任何统计量。
- **复现实测耗时**：约 1.9 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_REL_STRENGTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_REL_STRENGTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_REL_STRENGTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

