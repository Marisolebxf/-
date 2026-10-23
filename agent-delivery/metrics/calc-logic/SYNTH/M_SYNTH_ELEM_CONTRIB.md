# 要素贡献度与影响路径（M_SYNTH_ELEM_CONTRIB）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_CONTRIB.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_CONTRIB.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_CONTRIB_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_ELEM_CONTRIB |
| 指标名称 | 要素贡献度与影响路径 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新要素分析／要素影响关联分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_ELEM_CONTRIB.md` |

## 口径定义

正本要的是「四要素对两目标的贡献份额 + 影响路径」。份额能算，但**分子分母的边界在三个地方糊**：人才侧没有桥表（残差 0，只能用学者数做结构代理）、机构侧有两种分母（仅机构表 vs 含高校，差 29 倍）、产业侧四类主体互相重叠（高企也可能有研发投入）。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**；这不是算不出来，而是**算出来的数不能当归因读**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_CONTRIB.md` §二（M_SYNTH_ELEM_CONTRIB.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_ent_high_tech`
- `dwd_ent_patent`
- `dwd_paper`
- `dwd_talent_scholar`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：份额分解与 Top6 路径都能算，但两处口径退化：① 创新成果侧只能拆企业与科研机构，人才残余实测为 0（库内无作者级机构字段），按 calc-logic 转结构代理；② 产业侧四类主体规模互不互斥（高企同时可能有研发投入），份额是结构代理不是归因，论文侧无机构类型字段、无法进份额分解。再加「科研机构」两种口径差 29 倍，读者必须同时看到两组数，故判部分支持。
- **基期声明**：成果侧=2024 授权专利（去重公开号），产业侧=2024 时点的主体存量（高企/机构/学者/有研发投入机构四个数都不是年度流量），资金侧=2024 完成日融资与 2024 年报期研发额。2021—2023 未入集（单年截面设计）；2025/2026 不完整不进分母。四个数的时间语义不同（存量 vs 流量），故产业侧只作结构代理。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_CONTRIB.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_CONTRIB.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_CONTRIB_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

