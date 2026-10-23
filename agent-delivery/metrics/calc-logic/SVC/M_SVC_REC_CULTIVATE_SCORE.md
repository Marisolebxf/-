# 培育综合评分（M_SVC_REC_CULTIVATE_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_REC_CULTIVATE_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_REC_CULTIVATE_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_REC_CULTIVATE_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_REC_CULTIVATE_SCORE |
| 指标名称 | 培育综合评分 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业服务链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·本土服务机构培育列表评分列 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| 缺失年份 | [2007, 2008, 2009, 2010, 2011, 2012] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_REC_CULTIVATE_SCORE.md` |

## 口径定义

培育综合评分四维里，现有规模只覆盖 1,030 家（4.0239%）、技术创新能力**恒缺**（两分子列在 90,926 行中 0 行非空）、服务成效只能拿新闻条数代理、市场缺口只能用池内同门类营收份额代理——四维中有一维结构性不可得，故判 **部分支持**，只发布 981 家三维/两维可算机构的分布，不发布全市培育排序。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_REC_CULTIVATE_SCORE.md` §二（M_SVC_REC_CULTIVATE_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_important_news_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：培育综合评分四维里，现有规模只覆盖 1,030 家（4.0239%）、技术创新能力**恒缺**（两分子列在 90,926 行中 0 行非空）、服务成效只能拿新闻条数代理、市场缺口只能用池内同门类营收份额代理——四维中有一维结构性不可得，故判 **部分支持**，只发布 981 家三维/两维可算机构的分布，不发布全市培育排序。
- **基期声明**：非固定年窗：现有规模取每家机构最近一个有值的年报年（从业人员/资产总额），窗口随机构而异；财务表在池内非空值只落 2013—2025，2007—2012 池内 0 行非空，列入 missing，不按 0 摊入。服务成效的新闻条数无年份窗口（全历史累计）；市场缺口取最近一个有值年的营业收入，同门类分母只汇总同一年的有值机构。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_REC_CULTIVATE_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_REC_CULTIVATE_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_REC_CULTIVATE_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

