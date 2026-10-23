# M_TALENT_CULTIVATE_SCORE（M_TALENT_CULTIVATE_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_CULTIVATE_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_CULTIVATE_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_CULTIVATE_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_CULTIVATE_SCORE |
| 指标名称 | M_TALENT_CULTIVATE_SCORE |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 深圳人才态势页「本地留存与培育」卡（分档 + 四维雷达 + 深圳署名占比） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_CULTIVATE_SCORE.md` |

## 口径定义

182 名深圳在册学者里，学术力 A 与平台资源 R 两维 100% 可算、专利 P 维 87 人可算（95 人因同名/两字/无命中缺测）、留深黏性 Po 维只有 139 人有值——其中「深圳任职年限」只覆盖 21 人、「深圳求学」覆盖 **0** 人（学历子表与主档 ID 不同域）、真正撑起 Po 维的是「深圳署名论文占比」136 人，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_CULTIVATE_SCORE.md` §二（M_TALENT_CULTIVATE_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_heis_info`
- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_scholar_talent_flag`
- `dwd_scholar_work_experience`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维中三维修（A 学术力、P 专利、R 平台资源）有可算数据；Po 留深黏性维的三个子信号里，「任职年限」与「深圳求学」受子表 scholar_id 跨域影响只覆盖可连子集，「深圳署名论文占比」可算但仅对有论文署名者；专利维两字姓名/池内同名一律缺测 → 部分支持。
- **基期声明**：本指标为截面黏性指数，不涉基期与 CAGR；§3.16 两项按空集申报。
- **复现实测耗时**：约 2.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_CULTIVATE_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_CULTIVATE_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_CULTIVATE_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

