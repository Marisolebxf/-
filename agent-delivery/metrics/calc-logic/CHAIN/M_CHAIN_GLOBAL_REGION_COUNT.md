# 全球分布区域数（M_CHAIN_GLOBAL_REGION_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GLOBAL_REGION_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GLOBAL_REGION_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GLOBAL_REGION_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_GLOBAL_REGION_COUNT |
| 指标名称 | 全球分布区域数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN（产业链基础指标模型） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 产业链一张图 → 全球产业区域分布 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_GLOBAL_REGION_COUNT.md` |

## 口径定义

需求要「每个国家对应的企业和机构总数」，库内没有任何一张表能按国家数企业；唯一带国别的主体表是境外企业名录（20,000 行，GB/US/CA 三国），但它与 12 条链的标签交集为 0。专利表虽有国别，却既不代表申请人国籍，也几乎不分散（CN 96.90% / WO 3.06% / HK 0.03% / JP、TW、MO 合计 103 行），12 条链算出来的区域数只有 2 或 3，没有区分度 → **完全不支持**。本档位与 `code/M_CHAIN_GLOBAL_REGION_COUNT_out.json` 的 `support_judgment.data_support_level` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GLOBAL_REGION_COUNT.md` §二（M_CHAIN_GLOBAL_REGION_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_forg_research_org_info`
- `dwd_forg_university_org_info`
- `dwd_org_base_info`
- `dwd_org_heis_info`
- `dwd_patent`
- `dwd_research_institute_base_info`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：需求定义是「每个国家对应的企业和机构总数」，而 gkx 侧企业底册 189,116 行只有省/市、无国别字段，境内科研机构 2,074 家全在中国境内，三张境外主体表各 20,000 行却无产业链列，外国企业表与工业标签交集为 0、与链上企业名交集为 0；唯一带国别的 `dwd_patent.country_code` 只有 6 个代码，China 占 96.9%、WO(PCT) 占 3.06%，其余四码合计不足 0.04%。按链聚合后，12 条链里 11 条只覆盖 2 个区域（CN + WO），仅传感器链因 1 家企业有日本专利而达到 3 个，剔除 WO 后 11 条链的境外区域数为 0，既不能给出企业/机构的国家分布，也没有任何区分度，故判完全不支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.38 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_GLOBAL_REGION_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GLOBAL_REGION_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_GLOBAL_REGION_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版（模拟王惠调研；region_code/scope 伪字段 + 老表漂移）
- 2026-10-14: 0.2.0 口径钉死（语义=链上主体总部国家去重数；现阶段国内档 CN 恒 1）；发现并实核海外主档族（2 万企业 3 国 + 222 国院所高校，零挂接）；开 CHAIN-P0-7；补矩阵行 aligned/D3=none。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

