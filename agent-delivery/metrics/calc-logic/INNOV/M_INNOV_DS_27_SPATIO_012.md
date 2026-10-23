# 主题演化路径与创新前沿发现（M_INNOV_DS_27_SPATIO_012）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_27_SPATIO_012.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_27_SPATIO_012.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_27_SPATIO_012_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_27_SPATIO_012 |
| 指标名称 | 主题演化路径与创新前沿发现 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（科技时空演进展示） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技成果展示 → 科技时空演进展示 → 专业主题科研活动时空分布分析 → 主题演化路径与创新前沿发现 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_27_SPATIO_012.md` |

## 口径定义

开发库无「主题演化路径/前沿主题」结果面 → 非完全直接支持；**主题×时间**维可由 `dwd_patent` 的 IPC 小类 + 申请年直接构建（242.1 万件带 IPC、633 个小类、2021-2024 逐年份额已实测可算），结构与数据量均足；但需求要求「全球范围」的时空演化并联动论文/资金/人员，专利 96.9% 为中国申请、论文主题标签仅 19.87% 抽样、资金与人员流动无表 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_27_SPATIO_012.md` §二（M_INNOV_DS_27_SPATIO_012.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_industrial_fund_lp_info`
- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_scholar`
- `dwd_zh_author`
- `dwd_zh_paper`
- `dwd_zh_paper_abstract`
- `dwd_zh_paper_citation`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：主题×时间维可完整复现：2420915 件专利带 IPC（覆盖 82.3%），633 个 IPC 小类，2021-2024 年逐年份额可算，演化方向与前沿/新兴主题均可输出（结构+数据量均足，此维已达可现转水平）。但需求为「全球范围」的时空演化并联动论文/资金/人员：库内专利 96.9% 为中国申请（WO 仅 89935 件）、时间仅 2021-2026，论文主题标签仅 20048 条抽样（覆盖 19.87%），科技资金与人员流动无承载表 → 空间与多源维始终不足，故整体判部分支持。
- **基期声明**：由产物中实际出现的年度键反推：used=[2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_27_SPATIO_012.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_27_SPATIO_012.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_27_SPATIO_012_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

