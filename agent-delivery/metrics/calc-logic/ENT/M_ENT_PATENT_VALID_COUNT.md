# 有效专利数（M_ENT_PATENT_VALID_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PATENT_VALID_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PATENT_VALID_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PATENT_VALID_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_PATENT_VALID_COUNT |
| 指标名称 | 有效专利数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·企业查询·企业画像（知识产权卡片与重点企业提取阈值项）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_PATENT_VALID_COUNT.md` |

## 口径定义

公式所需的**三张表全部存在**（`dwd_patent_legal.status`、`dwd_patent_assignees.name`、`dwd_org_base_info.name_cn`），链路可现算；但 `dwd_patent_legal` 只有 **20,000 行**（主表 2,939,895 件的 **0.68%**），且与主表按 `patent_id`/`pn` 仅 **3.0%** 可连接（500 条探针命中 15 条），样本内 12,658 件「授权」经权利人名称归一映射后只落到 **147 家**底册企业、**471 件**专利（对 189,116 家覆盖率 **0.08%**）——**结构与公式闭合、数据量不足**，按 §〇 判**部分支持**。

## 计算逻辑说明

```text
COUNT(DISTINCT patent_id) WHERE legal.status='授权'；assignee name → org_id
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PATENT_VALID_COUNT.md` §二（M_ENT_PATENT_VALID_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_`
- `dwd_patent_assignees`
- `dwd_patent_cited`
- `dwd_patent_family`
- `dwd_patent_legal`
- `dwd_patent_transfer`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：法律状态表仅 20,000 行（主表 2,939,895 件的 0.68%），且与主表按 patent_id / pn 仅 3.0% 可连接（500 条探针命中 15 条），说明该样本是独立抽样、不是主表子集；样本内 12,658 件可判「授权」，经权利人名称归一映射仅落到 147 家底册企业、471 件专利，对 189,116 家底册覆盖率 0.07%——属抽样级证据，不能支撑企业级全量有效专利数。公式与链路闭合、可现算，但数据量不足以全量交付 → 部分支持。
- **基期声明**：由产物中实际出现的年度键反推：used=[2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 22.8 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PATENT_VALID_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PATENT_VALID_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PATENT_VALID_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

