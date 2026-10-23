# 技术基础指标模型——领先专利主体机构（王惠口径：技术创新力综合评估）（M_TECH_DS_07_TECH_INNOV_004）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DS_07_TECH_INNOV_004.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DS_07_TECH_INNOV_004.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DS_07_TECH_INNOV_004_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_DS_07_TECH_INNOV_004 |
| 指标名称 | 技术基础指标模型——领先专利主体机构（王惠口径：技术创新力综合评估） |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | DS-07 技术基础指标（专题库技术发展分析） ｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_DS_07_TECH_INNOV_004.md` |

## 口径定义

王惠 11 子项中 **4 项全量可算**（专利申请量 / 专利授权量 / 技术宽度 / 转让占比）、**3 项为 0.68%-0.70% 抽样级**（家族规模 / 被引次数 / 法律状态稳定性）、**4 项近零或缺列**（权利要求数、许可 2 例、诉讼 0 例、质押 10 例、开放许可 1 例，均出自 2,000 条 legal_events 抽样）——因此 **0-100 综合分不可闭合**，但「领先主体机构」的阈值识别（需求 (8) 的原始语义）当日可交付：220 家 ≥60 件主体中，按「≥500 件且授权率 ≥40%」筛出 **10 家**领先机构。按四档口径落 **部分支持**（out.json `support_judgment` 同档）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DS_07_TECH_INNOV_004.md` §二（M_TECH_DS_07_TECH_INNOV_004.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_patent_claim`
- `dwd_patent_family`
- `dwd_patent_legal`
- `dwd_patent_transfer`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠 11 子项中 **4 项全量可算**（专利申请量 / 专利授权量 / 技术宽度 / 转让占比）、**3 项为 0.68%-0.70% 抽样级**（家族规模 / 被引次数 / 法律状态稳定性）、**4 项近零或缺列**（权利要求数、许可 2 例、诉讼 0 例、质押 10 例、开放许可 1 例，均出自 2,000 条 legal_events 抽样）——因此 **0-100 综合分不可闭合**，但「领先主体机构」的阈值识别（需求 (8) 的原始语义）当日可交付：220 家 ≥60 件主体中，按「≥500 件且授权率 ≥40%」筛出 **10 家**领先机构。按四档口径落 **部分支持**（out.json `support_judgment` 同档）。
- **基期声明**：由产物中实际出现的年度键反推：used=[2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DS_07_TECH_INNOV_004.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DS_07_TECH_INNOV_004.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DS_07_TECH_INNOV_004_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

