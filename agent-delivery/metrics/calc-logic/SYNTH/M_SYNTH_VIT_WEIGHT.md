# 活力指数权重配置与权重弹性（M_SYNTH_VIT_WEIGHT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_WEIGHT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_WEIGHT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_WEIGHT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_VIT_WEIGHT |
| 指标名称 | 活力指数权重配置与权重弹性 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 区域活力榜的权重面板、「权重方案」下拉、名次稳定性提示 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| 缺失年份 | [2021, 2022, 2023, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_VIT_WEIGHT.md` |

## 口径定义

权重的**算法面**没有障碍：加权和、熵权、弹性、单纯形扫描四步都能落地，四维分也都有真值来源。卡住的是两件事：**官方权重读不到**（造数权重表在 gkx 不存在，权重只能自定义），**进盘的城市只有两个**（四维齐全的城市仅深圳、广州），任何权重下的「排名」都只是一次两两比较。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_WEIGHT.md` §二（M_SYNTH_VIT_WEIGHT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_scholar`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：权重公式（加权和 + 名次）完整可执行，四维分在 4 个城市上都是真值，熵权与弹性都能算；但三处结构性缺口把它压在『部分支持』：① 官方权重表 eval_weight 在 gkx 不存在，权重只能自定义，交付物里的 0.30/0.35/0.20/0.15 不是原系统标定值；② 四维齐全的城市只有 2 个（深圳市、广州市），东莞与惠州缺人才、政策两维，四维加权盘上永远只有两城，权重怎么调都只是一次两两比较；③ 熵权只能在这 2 城 × 4 维的矩阵上算，n=2 时熵权的区分度极不稳定，只能当参照不能当交付值。
- **基期声明**：四维分只取 2024 一个统计年（专利完整年），与 M_SYNTH_VIT_RANK 完全同源同池；其余年份未参与任何比值——不是库内不存在，是本指标未取用。
- **复现实测耗时**：约 0.0 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_WEIGHT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_WEIGHT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_WEIGHT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

