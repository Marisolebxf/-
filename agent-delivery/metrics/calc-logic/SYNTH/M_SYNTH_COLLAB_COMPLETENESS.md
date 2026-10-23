# 协同网络完整度（M_SYNTH_COLLAB_COMPLETENESS）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_COMPLETENESS.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_COMPLETENESS.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_COMPLETENESS_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_COLLAB_COMPLETENESS |
| 指标名称 | 协同网络完整度 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·综合智能分析 / 区域创新协同分析 / 协同度计算模型｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_COLLAB_COMPLETENESS.md` |

## 口径定义

无完整度结果面 → 非完全直接支持；覆盖率公式可执行、四城可出数，但「三类协同」只覆盖两类、主体名册缺失、覆盖口径不可复核 → **部分支持**。

## 计算逻辑说明

```text
Completeness = n_covered / N × 100；N=企业∪科研机构∪学者所属机构（含无边主体）
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_COMPLETENESS.md` §二（M_SYNTH_COLLAB_COMPLETENESS.py 零改语义复算）。

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
- **判档理由**：完整度公式可执行、四城覆盖率可算；但①分子侧三类边仅两类可建（合作项目边 funded_institution 全空），完整度是『两类协同』而非『三类协同』的覆盖率；②分母含无边主体，京沪企业主档 163/16 家、深广 95,600/49,605 家，分母口径双向失真；③覆盖节点缓存值与 2E 图论上界冲突（3 城超界），且无 window 主体名册表（calc-logic 登记的 ads.synth_collab_subject 缺口），分子不可复核。按四档口径判部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_COMPLETENESS.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_COMPLETENESS.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_COMPLETENESS_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

