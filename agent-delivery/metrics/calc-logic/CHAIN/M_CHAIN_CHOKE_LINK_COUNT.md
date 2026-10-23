# 卡脖子环节数（M_CHAIN_CHOKE_LINK_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_CHOKE_LINK_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_CHOKE_LINK_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_CHOKE_LINK_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_CHOKE_LINK_COUNT |
| 指标名称 | 卡脖子环节数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链监测／补链强链 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 产业链监测页「卡脖子环节」清单、补链强链专题靶点 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_CHOKE_LINK_COUNT.md` |

## 口径定义

「卡脖子」= 环节 × 受制度量 × 阈值。三段里**只有第一段（环节）有数据**：链树 1,273 个节点、954 个叶；第二段（受制度量）在全库 6,312 列里找不到一个可用字段；第三段（阈值）没有参数表。三段缺两段，故判**完全不支持**，并留下可复核的计数证据。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_CHOKE_LINK_COUNT.md` §二（M_CHAIN_CHOKE_LINK_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_industry_analysis_countries`
- `dwd_industry_chain_info`
- `dwd_industry_chain_news_info`
- `dwd_macro_index_data`
- `dwd_org_important_news_info`
- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：环节级「对外技术受制」判定需要两类前提，gkx 两类都不成立。（N1 度量）全库 280 张表 / 6312 列：受制类 14 组列名模式（choke/self_suff/import_dep/selfsuffic/customs/tariff/hs_code/input_output/localization 等）命中 0 列；国别类 4 组（country/nation/overseas/abroad）命中 42 列、落在 28 张表，逐表核过只有 3 张真能落到国别——dwd_patent.country_code（2939895 件中境外 90990 件，3.09%）、dwd_industry_analysis_countries（1000 行，仅 document_id→country，无金额列、无行业列）、dwd_forg_base_info（20000 家、3 个国别，其中 GB 一家独大 19832 家，是单一来源样本）。三者都是「主体属性」，不是「环节的对外依存度」；唯一的贸易序列是 dwd_macro_index_data 的 dwjj_dwmy*（5129 行、3 个指数码、180 个 area_code），维度只有区域与年份，落不到行业或链节点。（N2 标注位）旧稿依赖的三张表精确同名命中 0 张；1,273 个链节点的 17 列里没有标注位列（level 全 0、node_company_count 全 0），节点名匹配「卡/瓶颈/断供/受制」仅 2 条且均为药品名误匹配。既无度量、也无环节级标注位，故判完全不支持。
- **基期声明**：截面否定性证据：本件不产出年度序列，故无基期口径。dwd_macro_index_data 的 dwjj_dwmy* 覆盖 1979—2026，但它是区域级贸易总额/增速，不含环节维度，不能作为本指标的基期序列。
- **复现实测耗时**：约 32.0 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_CHOKE_LINK_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_CHOKE_LINK_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_CHOKE_LINK_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

