# 区域创新要素领域指数（M_SYNTH_ELEM_DOMAIN_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_DOMAIN_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_DOMAIN_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_DOMAIN_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_ELEM_DOMAIN_INDEX |
| 指标名称 | 区域创新要素领域指数 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新要素分析／要素评价模型构建 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_ELEM_DOMAIN_INDEX.md` |

## 口径定义

领域指数的**算法面**没有障碍：10 个叶子先做四城极值归一，再按维内等权平均出 3 个可用维，最后按「缺维不进分母」取三维均值，四城结果与面板 `domain.index` 逐城差 < 1e-6。卡住的是**输入面**：5 个维只有 3 个有承载，且其中两个维各只有 1 个加权叶子（相当于没有维内平均）。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_DOMAIN_INDEX.md` §二（M_SYNTH_ELEM_DOMAIN_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_macro_index_data`
- `dwd_patent_transfer`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：领域指数要求的五个维里只有 3 个能从 gkx 侧凑出可加权叶子（产业领域覆盖广度、技术领域应用深度、创新产出强度），人才结构合理性与经济贡献度两维在 2024 年四城上零承载：规上工业增加值与地区生产总值在 dwd_macro_index_data 里四城均无 2024 行，研发人员列整列为空、硕博学者四城仅 111 人。三条可用维的等权均值可复算且与面板逐城一致，但指数只覆盖 3/5 维、其中 2 个维只有 1 个加权叶子，且 D2_1 分母为存续口径——按「始终有部分依赖维度无法得到足够数据」判部分支持。
- **基期声明**：领域指数是 2024 单年截面：分子侧专利为 2024 授权年、政策为全库存量（不按年截断，见 DATA_FACTS §3.7）、高企与服务机构池为当前名录。2021—2023 未入集是本族单年截面设计，不是缺数；2025/2026 专利与年报不完整，不进分母。极值归一 min/max 取本批 4 城，换一批城市同一城的分数必然变。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_DOMAIN_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_DOMAIN_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_DOMAIN_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

