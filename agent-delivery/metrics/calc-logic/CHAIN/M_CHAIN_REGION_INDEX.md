# 区域产业指数（区域产业指数评价页壳指标）（M_CHAIN_REGION_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REGION_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REGION_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REGION_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REGION_INDEX |
| 指标名称 | 区域产业指数（区域产业指数评价页壳指标） |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 / 产业链分析 / 区域产业指数评价 / 区域产业指数 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REGION_INDEX.md` |

## 口径定义

区域产业指数是「壳指标」，它的成立完全取决于 8 个子项能否算。当日逐个验收的结果是 4 个可直算、1 个可算但缺失过多、3 个不可直算（学术生态维），因此只能交付「两维四子项版」，判**部分支持**。

## 计算逻辑说明

```text
I(c,r)=100×mean(available_dim_scores)；维内子项等权；子项在链内 4 市截面 min-max
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REGION_INDEX.md` §二（M_CHAIN_REGION_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_heis_info`
- `dwd_org_industry_tags`
- `dwd_patent`
- `dwd_policy_base`
- `dwd_research_institute_base_info`
- `dwd_scholar`
- `dwd_scholar_paper_relation`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：8 个子项只有 4 个在链×城粒度可算（企业数、专利、政策覆盖率、融资事件），48 个单元全部闭合；学术生态维 3 个子项不可算——2,074 家科研机构与 3,501 家高校与工业标签的链码交集 0、0，`dwd_scholar_info.scholar_org_id` 21,316 行全为空串。营收子项可算但 29/48 单元无披露。可算部分合成的两维指数分布 0.0–100.0（中位 24.1，31 个不同取值），可区分但缺一整个维度，故判部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 19.14 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REGION_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REGION_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REGION_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

