# 技术力排名（M_ENT_TECH_RANK）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TECH_RANK.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TECH_RANK.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TECH_RANK_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_TECH_RANK |
| 指标名称 | 技术力排名 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业评估／技术力评估 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业详情页「技术力排名」徽标、企业榜单页 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_TECH_RANK.md` |

## 口径定义

RANK 这层是纯计算，**算法面 100% 可落地**：降序、同分并列、无分不进榜、盘内重算，一条 SQL 就能表达。真正卡住的是**被排的那个分**：`tech_power_index` 在 `gkx` 无表、无列、五维十一子指标里 10 项结构性无源（表不存在／列全空／项目表只命中 2 家），只剩「专利量」一组量可代理。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**——注意这不是「差不多能用」，而是「名次能出、键不是原键」，两者在交付口径上必须分开写。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TECH_RANK.md` §二（M_ENT_TECH_RANK.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_project`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_rd_achiev_info`
- `dwd_org_stock_finance_info`
- `dwd_org_tech_score`
- `dwd_patent`
- `dwd_patent_legal`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：RANK 的算法面完全可实现（降序、同分并列、无分不进榜、盘内重算），四个盘也都能出；但排序键 tech_power_index 的 11 个子指标里 10 个结构性无源（表不存在、列全空、项目表只命中 2/4561 家），只剩专利量与授权率可代理，故本件交付的是「可观测代理键」的名次，不是 tech_power_index 的名次，不得以 M_ENT_TECH_RANK 名义发布。
- **基期声明**：专利量是 2021—2026 六年累计（库内专利表只有这六年，§3.13），不做年度切分；名次是时点截面，没有跨年分母，故 used 列六年、missing 为空。2026 年未过完，其件数已计入累计（企业间同口径，不影响盘内相对位置）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TECH_RANK.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TECH_RANK.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TECH_RANK_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

