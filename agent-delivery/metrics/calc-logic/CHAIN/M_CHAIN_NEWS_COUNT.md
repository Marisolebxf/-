# 动态资讯数（M_CHAIN_NEWS_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_NEWS_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NEWS_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NEWS_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_NEWS_COUNT |
| 指标名称 | 动态资讯数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链详情页「资讯」区池计数三件套之三 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_NEWS_COUNT.md` |

## 口径定义

表 `gkx.dwd_industry_chain_news_info` 有 108,052 行真实资讯、12 条链的链树也完整，但挂链列 `industry_code` 是 `varchar(255)` 的 JSON 数组串：46.70% 的行长度恰为 255 被截断，45.84% 的 JSON 解析不了，另有 3 条链的根码在全表一次都不出现（不是没资讯，是标签体系没这三个码）。能算出 9 条链、183,758 条链级计数，但标签层不可信，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_NEWS_COUNT.md` §二（M_CHAIN_NEWS_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_industry_chain_news_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：108,052 行资讯真实可取，industry_code 数组解析后 9/12 链有数（合计 183,758 条）；但 46.69% 的行 industry_code 恰为 255 字符被截断、45.85% 的 JSON 不可解析，且软件与信息服务、智能终端、智能网联汽车三条链的根码在全表 0 次出现（标签体系缺口，非真实无资讯），可计不可全信，故判部分支持。
- **基期声明**：截面指标：统计当前存量，不设年度分母（源表日期跨度 2020-01-13—2026-07-27，本件不按年切）。
- **复现实测耗时**：约 0.9 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_NEWS_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NEWS_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NEWS_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-24: 初版 v0.1.0（表名字段双漂移稿）
- 2026-10-14: v0.2.0 口径重写（human:徐滕强 拍板）
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

