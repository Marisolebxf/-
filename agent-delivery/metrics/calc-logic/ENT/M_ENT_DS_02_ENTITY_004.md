# [新增] 技术点影响力（M_ENT_DS_02_ENTITY_004）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DS_02_ENTITY_004.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_02_ENTITY_004.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_02_ENTITY_004_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DS_02_ENTITY_004 |
| 指标名称 | [新增] 技术点影响力 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·科技发展态势·科学技术全景「技术点关联实体排序」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_DS_02_ENTITY_004.md` |

## 口径定义

正本点名的六张承载表里，`graph_node` / `graph_edge` / `enterprise_graph_rel` / `dwd_org_base_info_patent_rel` / `tech_power` / `enterprise_centrality` 在 gkx 一张都不存在：表名扫 280 张，graph/edge/node 语义 0 命中、patent_rel 语义 0 命中；列名扫全库，`tech_power` / `centrality` / `pagerank` / `influence` / `tech_point` 五组前缀 0 命中。技术点本体、技术点—实体边、影响力字段三者皆无源。本件用 IPC 小类与资质覆盖率做两处代理，规模与质量两个子项可算，语义维缺，故按 §〇 判**部分支持**。

## 计算逻辑说明

```text
influence = 100 × (0.5·log1p 归一后的关联企业数 + 0.5·关联企业资质覆盖率)
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DS_02_ENTITY_004.md` §二（M_ENT_DS_02_ENTITY_004.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_base_info_patent_rel`
- `dwd_org_tech_tag`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：技术点本体（graph_node 的技术实体类型）、技术点—实体边、tech_power_index 三者在 gkx 均无源；本件用 IPC 小类 + 关联企业资质覆盖率做两处代理，只交付「规模×质量」的代理影响力，不交付甲方口径的综合影响力。
- **基期声明**：IPC×年 快照覆盖 2021—2026（dwd_patent 只有这六年，2017—2020 零行，见 DATA_FACTS §3.13）；本件是截面排序，不用年份做分母，2026 为残年，不参与任何「近 N 年均值」计算。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DS_02_ENTITY_004.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_02_ENTITY_004.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_02_ENTITY_004_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

