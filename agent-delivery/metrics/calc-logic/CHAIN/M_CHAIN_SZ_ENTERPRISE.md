# 深圳企业维度（M_CHAIN_SZ_ENTERPRISE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_ENTERPRISE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ENTERPRISE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ENTERPRISE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_ENTERPRISE |
| 指标名称 | 深圳企业维度 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／深圳产业发展分析／深圳产业现状／综合优势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链全景页「深圳产业现状」企业维度得分卡（优势评分的四个输入维之一）｜ **数据支持度**：**部分支持**｜ **wanghui**: true |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_SZ_ENTERPRISE.md` |

## 口径定义

三个三级里，「企业数量」可用（12 链 100–8,402 家），「企业规模」与「企业质量」都是**稀疏样本聚合**——四城合计只有 1,225 家企业有正营收（占底册 **0.65%**）、876 家上市企业有研发记录，深圳侧营收覆盖 901 家 / 95,600 = **0.94%**；两个稀疏维的排序由「个别龙头是否入库」决定，而非由产业规模决定，故判 **部分支持**。

## 计算逻辑说明

```text
企业维度 =（数量得分 + 规模得分 + 质量得分）/ 3，各三级在四城集合 min-max 至 0–100
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_ENTERPRISE.md` §二（M_CHAIN_SZ_ENTERPRISE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：企业数量维可用底册现算（12 链 100–8,402 家）；企业规模维虽有真实年报营收，但四城合计仅 1,225 家企业有正营收（占底册 0.65%），深圳仅 0.94%（901/95,600）；企业质量维仅 876 家上市企业有研发投入记录（深圳 559 家）。三个三级中两个是稀疏样本聚合，城市间排序由个别龙头是否入库决定，不满足『依赖维都能得到足够数据』，故判『部分支持』。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.0 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_ENTERPRISE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ENTERPRISE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ENTERPRISE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

