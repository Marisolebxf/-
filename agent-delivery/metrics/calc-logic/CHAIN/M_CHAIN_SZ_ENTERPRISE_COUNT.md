# 深圳产业链企业数（M_CHAIN_SZ_ENTERPRISE_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_ENTERPRISE_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ENTERPRISE_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ENTERPRISE_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_ENTERPRISE_COUNT |
| 指标名称 | 深圳产业链企业数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／深圳产业发展分析／深圳产业现状 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链全景页「深圳产业现状」家底卡 / 链对比柱 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_SZ_ENTERPRISE_COUNT.md` |

## 口径定义

链归属与企业规模都能在 gkx 单库内闭合，12 条链的深圳企业数当日全部非零（263–60,045 家）；但「深圳」这一维只能按统一社会信用代码第 3—6 位 `4403` 判定，语义是**登记机关辖区**而不是实际经营地，且 12 链深圳挂接 136,326 次只对应去重企业 116,017 家（跨链重复 20,309 次），底册 `city` 路径只覆盖 95,600 家、与挂链桥交集约 3.5 万家，无法作为独立校验 → 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_ENTERPRISE_COUNT.md` §二（M_CHAIN_SZ_ENTERPRISE_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：链归属与企业规模都可在 gkx 单库内闭合，12 条链的深圳企业数全部非零；但「深圳」只能按统一社会信用代码第 3—6 位 4403 判定，是登记机关辖区而非实际经营地，且 12 链深圳挂接 136,326 次对应去重企业 116,017 家（多链重复计 20,309 次），跨链不可加总当总量；底册 city 路径只覆盖 95,600 家、与挂链桥交集约 3.5 万家，无法作为独立校验。注册地口径的系统性偏差不可在本库内修复，故判部分支持。
- **基期声明**：截面存量指标，不设统计期；挂链桥无统计期字段，年度序列不在本件范围（见 M_CHAIN_ENTERPRISE_NEW_COUNT）。
- **复现实测耗时**：约 0.16 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_ENTERPRISE_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ENTERPRISE_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_ENTERPRISE_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版（模拟王惠调研，ADS 壳路线）
- 2026-10-14: v0.2.0 口径迁移（注册地 + 真源链桥直数；human:徐滕强 拍板）
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

