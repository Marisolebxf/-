# 专利总量（M_ENT_PATENT_TOTAL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PATENT_TOTAL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PATENT_TOTAL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PATENT_TOTAL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_PATENT_TOTAL |
| 指标名称 | 专利总量 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业评估／技术力评估 |
| 更新频率 | 日 |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 专利总量 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_PATENT_TOTAL.md` |

## 口径定义

企业作为专利权人（受让人映射到 org_id）的专利去重件数；不过滤法律状态，不按产业过滤

> 一句话口径（源件 §0.3）：gkx 有 **2,939,895 件**专利，其中能按名称归到企业主档的有 **2,557,248 件（86.9843%）**，落到 **157,363 家**企业（占底册 189,116 家的 83.2098%）；另有 382,647 件（13.0157%）因申请人名称对不上而按口径 drop。平均每家 16.2506 件、中位 5 件、P99 135 件、最大 81,376 件（华为）。授权口径 1,903,793 件，授权率 74.4469%。其中高校/院所/医院 1,123 家占 199,436 件（7.7989%），纯企业口径为 2,357,812 件。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PATENT_TOTAL.md` §二（M_ENT_PATENT_TOTAL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_patent`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_assignees`
- `dwd_patent_family`
- `dwd_patent_legal`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：gkx 有 **2,939,895 件**专利，其中能按名称归到企业主档的有 **2,557,248 件（86.9843%）**，落到 **157,363 家**企业（占底册 189,116 家的 83.2098%）；另有 382,647 件（13.0157%）因申请人名称对不上而按口径 drop。平均每家 16.2506 件、中位 5 件、P99 135 件、最大 81,376 件（华为）。授权口径 1,903,793 件，授权率 74.4469%。其中高校/院所/医院 1,123 家占 199,436 件（7.7989%），纯企业口径为 2,357,812 件。
- **基期声明**：截面累计件，无报告期。dwd_patent.apdt_year 仅 2021—2026（2017—2020 零行），故「总量」实为六年窗口累计；2026 为残年（74,810 行）。本指标不按年报期，因此 used/missing 留空，年份窗口在此说明。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_PATENT_TOTAL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PATENT_TOTAL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_PATENT_TOTAL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

