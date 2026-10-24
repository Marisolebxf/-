# 专家科研活跃度（M_INNOV_EXPERT_ACTIVITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EXPERT_ACTIVITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EXPERT_ACTIVITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EXPERT_ACTIVITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_EXPERT_ACTIVITY |
| 指标名称 | 专家科研活跃度 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技指数可视化 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 专家活跃度可视化（热力图/时间轴）、专家画像、专家 H 指数排行旁位｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_EXPERT_ACTIVITY.md` |

## 口径定义

四维信号全部落在真表、1,842 位学者可现算出有区分度的分，但「有 ID 无姓名」的 1.9 万人无法展示、需求提的「学术活动参与度」无任何源表 —— 两项结构性缺口，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EXPERT_ACTIVITY.md` §二（M_INNOV_EXPERT_ACTIVITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar`
- `dwd_scholar_coauthor`
- `dwd_scholar_paper_relation`
- `dwd_scholar_talent_flag`
- `dwd_scholar_work_experience`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维信号本身全部落在白名单真表（近窗论文与引用 106.5 万条关系、合著 118.8 万条边、项目 5.85 万条），在 1,842 位「主档∩关系表」学者上现转可得 0–100 分且有区分度；但① 学者主档 21,316 人与论文关系表 20,015 人的 scholar_id 仅 1,842 人重合（8.65%），其余 1.9 万人有 ID 无姓名/机构/h 指数，无法展示、无法与项目表按姓名对齐；② 需求原句还含「学术活动参与度（会议/讲座/交流）」，开发库与三方库均无任何会议/报告源表。两项均属结构性缺口，故判「部分支持」，不因脚本跑通升档。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EXPERT_ACTIVITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EXPERT_ACTIVITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EXPERT_ACTIVITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

