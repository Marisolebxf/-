# M_TALENT_INDUSTRY_SCORE（M_TALENT_INDUSTRY_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_INDUSTRY_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_INDUSTRY_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_INDUSTRY_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_INDUSTRY_SCORE |
| 指标名称 | M_TALENT_INDUSTRY_SCORE |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才产业画像页「20+8 集群归属 + 产业关联度分档 + 簇内榜」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_INDUSTRY_SCORE.md` |

## 口径定义

四维里学术深度 H 100% 可算、专利 PAT 45.46%（9,282 人）、产业关联论文 IND 35.35%（7,219 人至少 1 篇命中 20+8 簇）、产学研触点 LINK 27.01%（5,515 人）——三维能算、一维只覆盖四分之一；需求原意里的横向课题经费、技术转让、企业委托合同三列在 `gkx` 全库不存在，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_INDUSTRY_SCORE.md` §二（M_TALENT_INDUSTRY_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_industry_tags`
- `dwd_patent_transfer`
- `dwd_scholar`
- `dwd_scholar_research_direction`
- `dwd_scholar_work_experience`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维中 IND/H/PAT 三维可直接算，LINK 维只能由「企业任职履历 / 企业合作论文 / 深圳机构合作论文」三个 0/1 信号拼装，需求原意中的横向课题经费、技术转让、企业委托合同三列在 gkx 全库不存在（见 §三 表级清单）→ 部分支持。
- **基期声明**：截面指数，不涉基期与 CAGR；§3.16 两项按空集申报。
- **复现实测耗时**：约 17.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_INDUSTRY_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_INDUSTRY_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_INDUSTRY_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

