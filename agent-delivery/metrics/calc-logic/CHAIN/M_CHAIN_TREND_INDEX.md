# 产业链变化趋势指数（M_CHAIN_TREND_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_TREND_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TREND_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TREND_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_TREND_INDEX |
| 指标名称 | 产业链变化趋势指数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 / 深圳产业发展分析 / 趋势监测 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链详情页「趋势指数」折线、首页链卡片升降箭头 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_TREND_INDEX.md` |

## 口径定义

四因子里专利与融资有 2021—2024 完整序列；企业增减只能对上 35,046 家（2.04%）底册成立年，资讯热度表只覆盖 2025-02 之后、窗口内 0 行——**两维可得、两维不可得**，故判**部分支持**，`trend_index_4f` 置 null。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_TREND_INDEX.md` §二（M_CHAIN_TREND_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_news_info`
- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_industry_chain_pat_dtl`
- `dwd_org_industry_tags`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四因子里企业增减（底册覆盖 2.04%）与资讯热度（窗口内零行）不可得，只剩专利增速与融资事件增速两维，且融资降幅无法区分真实降温与源表覆盖下降。
- **基期声明**：2021—2024 是唯一同时满足「专利面板四年齐全 + 融资事件完整」的窗口；专利 2025 年 440,401 件、2026 年 74,810 件为残年，2025 年融资 561 起也低于 2024 年，均不进 CAGR 分母。2017—2020 年专利表零行，不补 0、不做外推。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_TREND_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TREND_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TREND_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

