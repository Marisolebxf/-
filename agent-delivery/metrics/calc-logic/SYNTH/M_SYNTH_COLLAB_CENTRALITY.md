# 协同网络中心度（平均点度中心性）（M_SYNTH_COLLAB_CENTRALITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_CENTRALITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_CENTRALITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_CENTRALITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_COLLAB_CENTRALITY |
| 指标名称 | 协同网络中心度（平均点度中心性） |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·综合智能分析 / 区域创新协同分析 / 协同度计算模型｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_COLLAB_CENTRALITY.md` |

## 口径定义

无现成中心度结果面 → 非完全直接支持；平均点度中心性四城可算但三边缺一、节点分母不可比、节点级度清单未落盘 → **部分支持**。

## 计算逻辑说明

```text
C_avg = (1/n) * sum_i k_i = 2m/n；归一化 C'_avg = C_avg/(n-1) = 2m/[n(n-1)]
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_CENTRALITY.md` §二（M_SYNTH_COLLAB_CENTRALITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_patent_applicants`
- `dwd_research_institute_base_info`
- `dwd_scholar`
- `dwd_scholar_work_experience`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：联合专利边（dwd_patent_applicants 28,964 行）与人才流动边（dwd_scholar_work_experience 57,117 行）可现转，平均点度中心性四城可算；但①合作项目边结构性缺失（dwd_zh_project.funded_institution 58,453 行全空，0 边），三边并集缺一类；②节点分母失真（京沪企业主档仅 163/16 家，深广全量 95,600/49,605 家），中心度均值由分母口径主导；③节点级度清单未落盘，覆盖节点缓存值（深 128 > 2E=26）超出图论上界，枢纽节点无法复核。故按四档口径判部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_CENTRALITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_CENTRALITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_CENTRALITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

