# 深圳优势评分（M_CHAIN_SZ_ADVANTAGE_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_ADVANTAGE_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ADVANTAGE_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ADVANTAGE_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_ADVANTAGE_SCORE |
| 指标名称 | 深圳优势评分 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／深圳产业情况分析对比／综合优势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链全景页「深圳产业现状」综合优势评分卡（总分 + 四分项条）｜ **数据支持度**：**部分支持**｜ **wanghui**: true |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_SZ_ADVANTAGE_SCORE.md` |

## 口径定义

四维中只有**企业维与专利维可算**：企业维受营收 0.65% 稀疏所限（见 `M_CHAIN_SZ_ENTERPRISE.md`），专利维是 20 万件样本（占 293.99 万件的 6.80%）的名称匹配计数；政策维 `keywords/keypoints` 全为 NULL，只能 title 字面命中，12 链合计 **15 条**（10 条链为 0）；人才维要求「链上高校/科研机构所属学者」，实测链上机构挂接 **0 行**。按 §〇「始终有部分依赖维得不到足够数据」判 **部分支持**。

## 计算逻辑说明

```text
每三级在四城集合 min-max 至 0–100；企业维=(数量+规模+质量)/3；可得维口径 =（企业+专利）等权；王惠满配口径 =0.25×(企业+专利+政策+人才)，缺维填 50
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_ADVANTAGE_SCORE.md` §二（M_CHAIN_SZ_ADVANTAGE_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_heis_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`
- `dwd_patent`
- `dwd_policy_base`
- `dwd_research_institute_base_info`
- `dwd_scholar`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维中只有企业维与专利维可算（企业维仍受营收 0.65%、研发 876 家稀疏所限；专利维为 6.80% 抽样），政策维 10/12 链无任何命中、人才维链级完全无数据；按 §〇「始终有部分依赖维得不到足够数据」判『部分支持』。另：需求原文要求『深圳与全国产业数据对比』，本库省外样本 0.18%，全国对标不可实现。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.0 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_ADVANTAGE_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ADVANTAGE_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ADVANTAGE_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

