# 深圳科研机构痛难点（M_ORG_SZ_PAINPOINT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ORG-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_SZ_PAINPOINT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_SZ_PAINPOINT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_SZ_PAINPOINT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ORG_SZ_PAINPOINT |
| 指标名称 | 深圳科研机构痛难点 |
| 所属域 | ORG（科研机构） |
| 一级模块 | 科研机构 |
| 更新频率 | 季度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 深圳科研机构画像卡、四市科研产出对比、机构培育建议 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ORG/M_ORG_SZ_PAINPOINT.md` |

## 口径定义

痛点分析要回答「这家机构卡在哪」。gkx 里能当作「卡点」观测面的有五路：纵向项目（拿不拿得到钱）、专利转让（成果卖不卖得掉）、论文（学术产出）、专利（技术产出）、政策提及（政府关不关注）。五路都能算，所以不是一个「无数据」的件；但产学研合作这一路（机构与企业联合攻关）在 gkx 没有边表，而它恰恰是「痛点」最常见的成因，缺了它就只能看结果、看不到过程。按四档定义，这属于「始终有部分依赖维度无法得到」，判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_SZ_PAINPOINT.md` §二（M_ORG_SZ_PAINPOINT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_patent_transfer`
- `dwd_policy_base`
- `dwd_research_institute_base_info`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：痛点分析要回答「这家机构卡在哪」。gkx 里能当作「卡点」观测面的有五路：纵向项目（拿不拿得到钱）、专利转让（成果卖不卖得掉）、论文（学术产出）、专利（技术产出）、政策提及（政府关不关注）。五路都能算，所以不是一个「无数据」的件；但产学研合作这一路（机构与企业联合攻关）在 gkx 没有边表，而它恰恰是「痛点」最常见的成因，缺了它就只能看结果、看不到过程。按四档定义，这属于「始终有部分依赖维度无法得到」，判**部分支持**。
- **基期声明**：机构级快照口径（2026-10-21 面板），无年度基期；论文年列受 §3.74 采集批次峰影响，本件只作存量总量，不画年度趋势。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_SZ_PAINPOINT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_SZ_PAINPOINT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_SZ_PAINPOINT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

