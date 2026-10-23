# 创新点价值评估（M_INNOV_DS_04_MONITOR_002）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_MONITOR_002.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_MONITOR_002.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_MONITOR_002_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_04_MONITOR_002 |
| 指标名称 | 创新点价值评估 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技发展态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 全球创新监测 → 创新监测与分析 → 创新点发现（**详情视角**） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_04_MONITOR_002.md` |

## 口径定义

对 MONITOR_001 的候选词条逐条打分：新颖性 1/(1+T−t0)、影响潜力（专利被引+论文被引）、成熟度（授权/件数），极值归一后加权平均 ×100；缺测维不补 0，剩余维重归一。

> 一句话口径（源件 §0.3）：三维里只有一维是**逐件实测**的：新颖性（`t0` 来自 634 个小类的全量逐年件数）。成熟度**结构上有、数据要估**：逐件授权号在 `granted_number` 上确实有，但按 IPC 小类聚合需要对 294 万行无索引表做 `GROUP BY`（DATA_FACTS §3.6 明令禁止），只能用「申请人授权率 × 该 IPC 件数」分摊，全表两类聚合（`star_applicant_agg` 2,939,895 件 / `patent_ipc4_by_name` 2,420,915 件）对得上，但这是**估算**不是实测。影响潜力**结构性缺失**：`dwd_patent_cited` 20,515 行里只有 **467 个 pn** 能在 `dwd_patent` 命中（2.28%），词条级「被引合计」在 gkx 上不成立。三维只能用两维，按 §〇 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_MONITOR_002.md` §二（M_INNOV_DS_04_MONITOR_002.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_annual_financial_info`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_zh_author`
- `dwd_zh_journal`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维里只有一维是**逐件实测**的：新颖性（`t0` 来自 634 个小类的全量逐年件数）。成熟度**结构上有、数据要估**：逐件授权号在 `granted_number` 上确实有，但按 IPC 小类聚合需要对 294 万行无索引表做 `GROUP BY`（DATA_FACTS §3.6 明令禁止），只能用「申请人授权率 × 该 IPC 件数」分摊，全表两类聚合（`star_applicant_agg` 2,939,895 件 / `patent_ipc4_by_name` 2,420,915 件）对得上，但这是**估算**不是实测。影响潜力**结构性缺失**：`dwd_patent_cited` 20,515 行里只有 **467 个 pn** 能在 `dwd_patent` 命中（2.28%），词条级「被引合计」在 gkx 上不成立。三维只能用两维，按 §〇 判**部分支持**。
- **基期声明**：基窗公式要求 2017—2021，但 gkx.dwd_patent.apdt_year 只有 2021—2026，2017—2020 零行；因此基窗实际只用 2021 一年，均值只除 1，缺失的 4 年不进分母。专利年份序列只遍历库内真实存在的 2021—2026，不做 .get(y, 0) 式补零。
- **复现实测耗时**：约 2.7 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_MONITOR_002.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_MONITOR_002.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_MONITOR_002_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

