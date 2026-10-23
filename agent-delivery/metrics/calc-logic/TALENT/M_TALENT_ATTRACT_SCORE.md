# M_TALENT_ATTRACT_SCORE（M_TALENT_ATTRACT_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_ATTRACT_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ATTRACT_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ATTRACT_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_ATTRACT_SCORE |
| 指标名称 | M_TALENT_ATTRACT_SCORE |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才引进推荐页「候选池排序 + 分维雷达 + 深圳关联标」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_ATTRACT_SCORE.md` |

## 口径定义

外部候选池 20,238 人里，学术力 A 维 100% 可算、专利 P 维 45.43%（9,195 人姓名唯一且不少于 3 字）、产业方向 M 维 70.94%（14,357 人）、深圳连接 C 维只有 **2.35%** 非零（476 人）——四维里三维能用、一维极稀；再加上招聘平台真源 `dwd_job` 只有 **10 行**、无投递/意向交互日志，「智能筛选」只能降级为规则化筛选，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_ATTRACT_SCORE.md` §二（M_TALENT_ATTRACT_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_job`
- `dwd_patent`
- `dwd_patent_inventors`
- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_scholar_research_direction`
- `dwd_scholar_work_experience`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：A/P/M 三维在外部池可算（A 全覆盖、P 约七成、M 约七成），但 C 维（深圳连接）只有约一成候选可测：深圳署名论文 10.3%、深圳履历受「子表 scholar_id 仅 9.3% 可连」限制；需求所指的招聘平台真源 `dwd_job` 仅 10 行、无投递/意向交互日志，「智能筛选」只能降级为规则化筛选 → 部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_ATTRACT_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ATTRACT_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ATTRACT_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

