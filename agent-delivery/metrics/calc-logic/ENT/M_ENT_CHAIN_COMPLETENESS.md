# 产业链完整度（M_ENT_CHAIN_COMPLETENESS）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CHAIN_COMPLETENESS.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CHAIN_COMPLETENESS.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CHAIN_COMPLETENESS_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_CHAIN_COMPLETENESS |
| 指标名称 | 产业链完整度 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技专题·「产业链全景图谱」页（识别链完整性与断点）+「深圳企业现状分析」对标表 ｜ **数据支持度**：**完全转换支持**｜ wanghui：false（非王惠系，口径真源为算法 2026-09 COVER-STAT-L01） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_CHAIN_COMPLETENESS.md` |

## 口径定义

结果列 `sz_city_benchmark.chain_completeness` 现网 8 行 mock（深圳 75.0 等，禁读）→ 非完全直接支持；三方侧链目录 1,273 码（12 链根、**叶子 K=954**）+ 企业上链 tags **2,283,762 行**全量拆解后 k/K 已现转算出（全国 940/954=98.53%、深圳探针 712/954=74.63%）→ **完全转换支持**；DWD 侧 `node_id` 空、`chain_code=IC-*` 是灌数缺口而非源侧无数据。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CHAIN_COMPLETENESS.md` §二（M_ENT_CHAIN_COMPLETENESS.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：gkx 目录 1273 码（12 链根、叶子 K=954）；tags 2,283,762 行全量拆解后 全国层面 k=940/954（完整度 98.53%）；深圳探针（credit_code JOIN LIMIT 20 万）k=712/954（74.63%）。结构+当前数据量均足，k/K 已现转算出。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CHAIN_COMPLETENESS.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CHAIN_COMPLETENESS.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CHAIN_COMPLETENESS_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

