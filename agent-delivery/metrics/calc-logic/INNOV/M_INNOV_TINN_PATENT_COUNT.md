# 专利数量（M_INNOV_TINN_PATENT_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_PATENT_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_PATENT_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_PATENT_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_TINN_PATENT_COUNT |
| 指标名称 | 专利数量 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 技术创新力指标展示页「专利数量统计分析」卡片（柱/折），切片为时间、技术类别、地域、申请人 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_TINN_PATENT_COUNT.md` |

## 口径定义

两个子项一好一坏。**申请量**完全可算：全量面板 2,939,895 行与主表逐行一致，IPC4 × 年共 2,456 格，2021—2024 窗口内主分类已标注 2,009,365/2,424,684 = 82.87%，Top 20 领域四年合计从 G06F 的 148,698 件到 A61K 的 19,747 件，增速与 CAGR 均可算。**授权量**只有全域一个数：`star_applicant_agg_gkx.json` 的 `agg[nm][1]` 合计 2,140,420 件、授权率 72.81%，**没有任何缓存带「IPC4 × 年 × 授权」**；要拆必须对 294 万行主表按 `granted_number` 做全表聚合，实测该类查询 600 秒断连（`DATA_FACTS_gkx21.md` §3.6/§3.12），故不执行。两个子项缺一，按档位定义落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_PATENT_COUNT.md` §二（M_INNOV_TINN_PATENT_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_patent_family`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：两个子项一好一坏。**申请量**完全可算：全量面板 2,939,895 行与主表逐行一致，IPC4 × 年共 2,456 格，2021—2024 窗口内主分类已标注 2,009,365/2,424,684 = 82.87%，Top 20 领域四年合计从 G06F 的 148,698 件到 A61K 的 19,747 件，增速与 CAGR 均可算。**授权量**只有全域一个数：`star_applicant_agg_gkx.json` 的 `agg[nm][1]` 合计 2,140,420 件、授权率 72.81%，**没有任何缓存带「IPC4 × 年 × 授权」**；要拆必须对 294 万行主表按 `granted_number` 做全表聚合，实测该类查询 600 秒断连（`DATA_FACTS_gkx21.md` §3.6/§3.12），故不执行。两个子项缺一，按档位定义落**部分支持**。
- **基期声明**：gkx.dwd_patent 的 apdt_year 只有 2021—2026；2017—2020 零行，任何「五年基线」都不成立，CAGR 分母只能用 2021 单年

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_PATENT_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_PATENT_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_PATENT_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

