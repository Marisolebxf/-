# 区域创新要素层次指数（M_SYNTH_ELEM_LEVEL_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_LEVEL_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_LEVEL_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_LEVEL_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_ELEM_LEVEL_INDEX |
| 指标名称 | 区域创新要素层次指数 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新要素分析／要素评价模型构建 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_ELEM_LEVEL_INDEX.md` |

## 口径定义

层次指数的算法链是「成熟度（维内等权）+ 均衡度（Shannon 熵比）→ 结构分 → 六结构均值」，四城复算与面板差 < 1e-6，且与类型指数存在恒等式（成熟度均值 = 类型指数）。卡住的是结构覆盖与均衡度的可算性：人才结构整结构空缺、两个结构 n=1 使均衡度恒 60。按 §0.1 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_LEVEL_INDEX.md` §二（M_SYNTH_ELEM_LEVEL_INDEX.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：七个结构里 6 个可算（企业、政策、服务机构、科研机构、资金、空间），人才结构整结构空缺（叶子同类型指数：研发人员列整列为空、硕博学者样本不足）；成熟度、熵均衡度、结构得分与六结构等权均值全部可复算，与面板逐城一致。但两个结构（服务机构、空间）只有 1 个叶子，均衡度按规则恒记 60，结构得分实际是「成熟度与常数 60 的平均」；加上人才结构空缺，故判部分支持。
- **基期声明**：层次指数是 2024 单年截面：叶子口径与类型指数完全一致（本件不另取数）。2021—2023 未入集是单年截面设计；2025/2026 不完整不进分母。极值归一的 min/max 取本批 4 城，换区域集合分数必变。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_LEVEL_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_LEVEL_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_LEVEL_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

