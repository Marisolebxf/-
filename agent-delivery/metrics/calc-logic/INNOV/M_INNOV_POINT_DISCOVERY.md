# 创新点发现（M_INNOV_POINT_DISCOVERY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POINT_DISCOVERY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POINT_DISCOVERY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POINT_DISCOVERY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POINT_DISCOVERY |
| 指标名称 | 创新点发现 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（创新机会） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 创新机会 → 机会点发现 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2012, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_POINT_DISCOVERY.md` |

## 口径定义

词条级突现检测：burst=(近窗年均−基窗年均)/max(基窗年均,1)，is_new=首次出现年≥T−2，候选=(burst≥1 或 is_new)且近窗件数≥3

> 一句话口径（源件 §0.3）：三类词条里只有一类（IPC4）是**全量**：`patent_ipc4_year_20261021.json` 覆盖 2,420,915 件有 IPC 的专利、634 个小类、2021—2026 六个申请年。专利关键词只有 200,000 行主键切片（6.80%），论文关键词的分类表 20,048 篇里只有 **799 篇**能对上论文主表拿到年份。更重要的是基窗：`dwd_patent.apdt_year` 只有 2021—2026，公式要求的前 5 年均值在本库只能取到 **2021 一年**。结构与量都够跑出候选清单，但三类词条的可信度差一个数量级，判**部分支持**。本档位与 `code/M_INNOV_POINT_DISCOVERY_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POINT_DISCOVERY.md` §二（M_INNOV_POINT_DISCOVERY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_patent`
- `dwd_zh_paper`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三类词条里只有一类（IPC4）是**全量**：`patent_ipc4_year_20261021.json` 覆盖 2,420,915 件有 IPC 的专利、634 个小类、2021—2026 六个申请年。专利关键词只有 200,000 行主键切片（6.80%），论文关键词的分类表 20,048 篇里只有 **799 篇**能对上论文主表拿到年份。更重要的是基窗：`dwd_patent.apdt_year` 只有 2021—2026，公式要求的前 5 年均值在本库只能取到 **2021 一年**。结构与量都够跑出候选清单，但三类词条的可信度差一个数量级，判**部分支持**。本档位与 `code/M_INNOV_POINT_DISCOVERY_out.json` 的 `support_judgment` 一致。
- **基期声明**：由产物中实际出现的年度键反推：used=[2012, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 2.7 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_POINT_DISCOVERY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POINT_DISCOVERY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_POINT_DISCOVERY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

