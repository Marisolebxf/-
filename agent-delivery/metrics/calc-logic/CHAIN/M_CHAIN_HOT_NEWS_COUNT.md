# 链热门资讯数（M_CHAIN_HOT_NEWS_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HOT_NEWS_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOT_NEWS_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOT_NEWS_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_HOT_NEWS_COUNT |
| 指标名称 | 链热门资讯数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链概览「热门资讯」卡片、链详情资讯流排序｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_HOT_NEWS_COUNT.md` |

## 口径定义

资讯量与链归属都可算，但 heat_score 整库不存在；用跨源转载、周报道峰值、标题显著度三项代理后，12 链共 1,972 条热门（1.83%），只能判部分支持。

## 计算逻辑说明

```text
hot_item = I_reprint + I_burst + I_salience ≥ 2；hot_count(c) = Σ hot_item·[标题命中链 c 的实体词表]
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HOT_NEWS_COUNT.md` §二（M_CHAIN_HOT_NEWS_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_news_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：链资讯 108,052 行真实、可计数，2025-02 至 2026-07 连续 18 个月；但 heat_score 字段整库不存在，本件只能用三项可观测替代量定义热度，代理在 12 条链上产出 1,972 条热门资讯（1.83%），热度语义（读者触达/传播效果）无法与原文口径对齐；标题词表只覆盖 31.89% 的资讯，industry_code 多值且 48.2% 被截断，不能作为链归属依据；窗口仅 18 个月，无法支撑年度趋势。故最高判部分支持。
- **基期声明**：本指标不做年度同比，分母不是年度序列：资讯窗口为 2025-02-01—2026-07-27 的全量截面。used/missing 为空表示没有年度基期，不是「缺年按 0 摊入」。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HOT_NEWS_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOT_NEWS_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOT_NEWS_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

