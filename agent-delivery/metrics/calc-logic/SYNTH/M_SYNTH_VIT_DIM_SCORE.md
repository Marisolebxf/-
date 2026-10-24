# 四维单维评分（M_SYNTH_VIT_DIM_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_DIM_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_DIM_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_DIM_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_VIT_DIM_SCORE |
| 指标名称 | 四维单维评分 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新活力分析／综合评价模型 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_VIT_DIM_SCORE.md` |

## 口径定义

本件是四个子模型（182 科技、183 产业、184 人才、185 政策）的**分维出口**：不做归一、不做加权、不做二次加工，只把上游已发布的综合分按「城市 × 维度」摆成一张表。所以它自己不会「算不出来」，卡住的是**上游每一维的子维齐不齐**：人才维 4 个子维只剩 2 个，政策维 3 个只剩 2 个，产业维的三级指标缺第三产业占比重。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_DIM_SCORE.md` §二（M_SYNTH_VIT_DIM_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_paper`
- `dwd_macro_index_data`
- `dwd_org_annual_financial_info`
- `dwd_org_industry_product_tags`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_policy_base`
- `dwd_research_institute_base_info`
- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维分全部可算（四城 4/4 有值），但只有科技维是满维（3/3 子维）；产业维 5 个三级指标缺 1（第三产业占比重）、人才维 4 个子维只有 2 个有值、政策维 3 个子维只有 2 个有值。四维「有值」不等于四维「齐」，按 §0.1 判部分支持。
- **基期声明**：四维均为统计年 2024（专利完整年）；产业维的产品标签为当前截面、服务机构为覆盖率族快照，二者无年份维度；第三产业占比重因四城无同期间事实未进任何维，故 2017 不作为基期
- **复现实测耗时**：约 0.001 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_DIM_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_DIM_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_DIM_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

