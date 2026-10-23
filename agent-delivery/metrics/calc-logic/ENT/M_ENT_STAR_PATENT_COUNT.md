# 明星企业专利数（M_ENT_STAR_PATENT_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_PATENT_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_PATENT_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_PATENT_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_STAR_PATENT_COUNT |
| 指标名称 | 明星企业专利数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业总览／企业整体概况 |
| 更新频率 | 日 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 明星企业介绍·专利数列 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_STAR_PATENT_COUNT.md` |

## 口径定义

明星企业（CMS 名单，本件以代理名单替代）名下累计专利件数（授权口径）

> 一句话口径（源件 §0.3）：代理名单 4,561 家名下累计**授权专利 699,284 件**（王惠「授权口径」），占全库授权 2,140,420 件的 **32.6704%**；若按 calc-logic 的 SQL 不过滤法律状态，同一批企业有**累计公开 1,069,438 件**，占全库 2,939,895 件的 **36.3767%**。两个数差 370,154 件（34.612%），差在「申请公开但未见授权公告」的那部分。名单 4,561 家占底册 2.4117%，却握着三成以上授权件，集中度是这条指标唯一稳的结论。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_PATENT_COUNT.md` §二（M_ENT_STAR_PATENT_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_bak_20260912`
- `dwd_patent_legal`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：代理名单 4,561 家名下累计**授权专利 699,284 件**（王惠「授权口径」），占全库授权 2,140,420 件的 **32.6704%**；若按 calc-logic 的 SQL 不过滤法律状态，同一批企业有**累计公开 1,069,438 件**，占全库 2,939,895 件的 **36.3767%**。两个数差 370,154 件（34.612%），差在「申请公开但未见授权公告」的那部分。名单 4,561 家占底册 2.4117%，却握着三成以上授权件，集中度是这条指标唯一稳的结论。
- **基期声明**：截面累计件，无报告期。专利侧 dwd_patent 的 apdt_year 只覆盖 2021—2026（2017—2020 零行，DATA_FACTS §3.13），故「累计」实为 2021—2026 六年累计；2026 为残年（74,810 行）。名单无年度字段，不构成年度序列，故 used/missing 均为空。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_PATENT_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_PATENT_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_PATENT_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

