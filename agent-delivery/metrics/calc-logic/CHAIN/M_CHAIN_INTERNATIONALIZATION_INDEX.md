# 产业链国际化程度（M_CHAIN_INTERNATIONALIZATION_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_INTERNATIONALIZATION_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INTERNATIONALIZATION_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INTERNATIONALIZATION_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_INTERNATIONALIZATION_INDEX |
| 指标名称 | 产业链国际化程度 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN（产业链分析） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 产业链详情页「全球布局」区·国际化程度 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_INTERNATIONALIZATION_INDEX.md` |

## 口径定义

三条候选路径同时断裂：海外企业主档 20,000 行只有 GB/US/CA 三国、与产业链交集 0（科研机构/高校表虽有 186/219 国，但无行业码、主体非企业）；专利表只有「公开国别」没有「申请人国别」，WO 公开的申请人 94.15% 是国内企业；进出口/贸易表全库不存在。原口径本身处于挂起状态（无公式、无权重、无 QC 号）→ **完全不支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_INTERNATIONALIZATION_INDEX.md` §二（M_CHAIN_INTERNATIONALIZATION_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_enterprise_industry_chain`
- `dwd_forg_`
- `dwd_forg_base_info`
- `dwd_forg_executive_info`
- `dwd_forg_product_info`
- `dwd_forg_research_org_info`
- `dwd_forg_shareholder_info`
- `dwd_forg_university_org_info`
- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_important_news_info`
- `dwd_org_industry_tags`
- `dwd_patent`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：三条候选路径全部断裂：① 海外主体 dwd_forg_base_info 20,000 行仅 GB 19,832 / US 159 / CA 9 三国，与国内主档 org_id 交集 0、与产业标签 credit_code 交集 0、与企业—链归属交集 0，无法挂到任何产业链；② 专利表无申请人国别字段，country_code 实为公开国别，WO 公开的申请人 94.15% 直接命中国内企业主档名（华为、OPPO、中兴等），用它算「海外专利占比」会把中国企业的 PCT 申请算成国际化；③ 进出口/贸易表全库不存在，w3 因子无载体。原口径本身处于挂起状态、无公式无权重，故该指标及其关键依赖在三方库 gkx 均不可构建。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_INTERNATIONALIZATION_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INTERNATIONALIZATION_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_INTERNATIONALIZATION_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

