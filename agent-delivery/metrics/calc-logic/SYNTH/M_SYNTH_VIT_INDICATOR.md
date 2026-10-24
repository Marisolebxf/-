# 活力分项指标值与得分（M_SYNTH_VIT_INDICATOR）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_INDICATOR.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_INDICATOR.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_INDICATOR_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_VIT_INDICATOR |
| 指标名称 | 活力分项指标值与得分 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新活力分析／指标体系构建 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_VIT_INDICATOR.md` |

## 口径定义

本件的任务不是算分，是**把 12 个分项摆在一张表上，让读者看见四维分是怎么来的**。12 个分项中 8 个能进维、1 个有值但饱和、3 个四城全缺（两个整列空、一个指标码不存在）。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_INDICATOR.md` §二（M_SYNTH_VIT_INDICATOR.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_paper_reference`
- `dwd_macro_index_data`
- `dwd_org_annual_financial_info`
- `dwd_org_annual_org_financial_info`
- `dwd_org_org_product_info`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_patent_transfer`
- `dwd_policy_base`
- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_zh_paper_citation`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：12 个分项里 8 个有标准化得分并进维、1 个（高学历人才占比）有值但因饱和未进维、3 个（新产品销售收入占比 / 研发人员数量 / 政策实施效果指数）四城全缺；其中两个缺项是整列空（研发人员、政策日期），一个是指标码不存在（a77234）。按 §0.1 判部分支持。
- **基期声明**：统计年 2024；高质量论文为全历史累计的高被引池（阈值 6 次），与 2024 年授权专利不同源，故四维不是同一时间窗；政策存量是当前有效集而不是 2024 年出台量
- **复现实测耗时**：约 0.001 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_INDICATOR.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_INDICATOR.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_INDICATOR_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

