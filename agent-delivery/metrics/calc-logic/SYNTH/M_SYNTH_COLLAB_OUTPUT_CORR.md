# 协同—创新产出关联结果（M_SYNTH_COLLAB_OUTPUT_CORR）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_OUTPUT_CORR.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_OUTPUT_CORR.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_OUTPUT_CORR_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_COLLAB_OUTPUT_CORR |
| 指标名称 | 协同—创新产出关联结果 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·综合智能分析 / 区域创新协同分析 / 协同效果评估｜ **数据支持度**：**部分支持**（本次交付状态：`insufficient`） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_COLLAB_OUTPUT_CORR.md` |

## 口径定义

结构齐全、单窗 X 与 Y 均可取，但王惠口径要求「同一区域按年组样本、n≥3 且不做跨区域截面」——年度序列不存在，故本次交付 `insufficient`；又因表结构与数据量具备补齐条件、并非结构性不可得，判 **部分支持** 而非「完全不支持」。

## 计算逻辑说明

```text
r_k = Pearson(X_{k,t}, Y_t)，n>=3、双侧方差>0；X∈{Index, Density, Centrality_avg}，Y=联合发明专利授权去重数
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_OUTPUT_CORR.md` §二（M_SYNTH_COLLAB_OUTPUT_CORR.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_applicants`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：协同侧 X 三件套可由 191 单窗事实算出，产出侧 Y（发明专利授权存量）按城可得；但①缺区域×年序列，无法按王惠口径组 n>=3 的年样本，交付状态 insufficient；②合作项目边 0 条使 X 的结构维不完整；③X 与 Y 均受分母/归属采集缺口影响，4 城截面 r 为负且不可解释。按四档口径判部分支持（有结构、有部分量，但关键年度序列与边维始终不足）。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_OUTPUT_CORR.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_OUTPUT_CORR.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_OUTPUT_CORR_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

