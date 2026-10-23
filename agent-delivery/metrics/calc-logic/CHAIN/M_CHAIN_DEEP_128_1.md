# 深圳机遇分析模型（M_CHAIN_DEEP_128_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_128_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_128_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_128_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_128_1 |
| 指标名称 | 深圳机遇分析模型 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／区域机遇分析／深圳产业布局 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 区域产业报告「深圳机遇清单」、链详情页「深圳布局建议」徽标 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_DEEP_128_1.md` |

## 口径定义

旧稿的 `opportunity_index = 0.4×趋势 + 0.3×政策 + 0.3×市场`。本库趋势可算（融资两窗、新设两窗）、市场不可算（链级营收覆盖 2.41%）、政策不可算（20,000 条政策只有城市/主题，无链标签，深圳 879 条拆不到 12 条链）。**三维缺两维，故判部分支持；本件用「优势 + 缺口」替换政策与市场，指数不是旧稿口径。**

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_128_1.md` §二（M_CHAIN_DEEP_128_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_industry_tags`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：趋势（融资/新设两窗增速）与优势（LQ、专利/融资超配）两维可从 gkx 快照算，12 条链全部出机会指数与名次；但旧稿三维里的政策维（政策 20,000 条无链标签、深圳 879 条无法拆链）与市场维（链级营收不可得，财务表营收仅 2,193/90,926 行）均不可算，且 chain_sz_opportunity / chain_sz_advantage / chain_sz_problem 三张结果表不存在，故只交付「趋势×优势×缺口」的替代指数，不冒充旧稿 opportunity_index。
- **基期声明**：趋势项用 2013—2018 对 2019—2024 两窗；2025/2026 为不完整年，主动排除，不按 0 摊入分母。优势项与缺口项是当前时点快照，不按年切分。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_128_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_128_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_128_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

