# 资讯正面情感占比（M_CHAIN_NEWS_SENTIMENT_RATIO）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_NEWS_SENTIMENT_RATIO.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NEWS_SENTIMENT_RATIO.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NEWS_SENTIMENT_RATIO_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_NEWS_SENTIMENT_RATIO |
| 指标名称 | 资讯正面情感占比 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链详情页「资讯」区三件套之二（情感极性条） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_NEWS_SENTIMENT_RATIO.md` |

## 口径定义

链资讯表 `gkx.dwd_industry_chain_news_info` 有 **108,052 行标题**、结构与挂链键齐备，但 `information_schema` 在 `gkx` 全库检索 `sentiment` / `polarity` / `emotion` **零命中**——没有任何情感列，也没有一条带极性的金标样本。词典代理能算出总体正面占比 **0.9202**、给出 9/12 条链的排序，但准确率无法在库内校验，且 3 条链因资讯标签体系与链树根码不重合而无样本 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_NEWS_SENTIMENT_RATIO.md` §二（M_CHAIN_NEWS_SENTIMENT_RATIO.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_news_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：链资讯 108,052 条标题可取，但 gkx 全库没有任何情感/极性列（information_schema 检索 sentiment/polarity/emotion 零命中），40 词词典代理值只能作排序参考、不能作验收值；另有 3 条链因资讯标签体系与链树根码不重合而无样本。
- **基期声明**：截面指标：统计当前存量资讯的极性分布，不设年度分母；资讯表无年度字段。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_NEWS_SENTIMENT_RATIO.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NEWS_SENTIMENT_RATIO.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NEWS_SENTIMENT_RATIO_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

