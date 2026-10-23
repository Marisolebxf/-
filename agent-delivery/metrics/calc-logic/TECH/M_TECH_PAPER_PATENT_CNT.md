# 技术点论文量 / 专利量（M_TECH_PAPER_PATENT_CNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_PAPER_PATENT_CNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PAPER_PATENT_CNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PAPER_PATENT_CNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_PAPER_PATENT_CNT |
| 指标名称 | 技术点论文量 / 专利量 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术点详情（论文数/专利数双计数）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_PAPER_PATENT_CNT.md` |

## 口径定义

两侧的「全量计数」都能算：论文 100,900 篇（doi 去重后仍 100,900）、专利 2,939,895 件（IPC 覆盖 82.35%）。但需求要的是**按技术点对齐后的双计数**：gkx 280 张表里没有任何 `technology_id` / 技术点实体表（`domain`、`technology`、`tech_point`、`techpoint` 四组关键词全零命中），机构桥只能精确同名覆盖 10.85% 的论文机构，标题桥 0.75 以上命中 0/200。技术点粒度不成立，只能交付机构级双计数与双侧总量，落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_PAPER_PATENT_CNT.md` §二（M_TECH_PAPER_PATENT_CNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_patent_family`
- `dwd_patent_title`
- `dwd_zh_paper`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：两侧计数都能算（论文 100,900 / 专利 2,939,895），但需求要求按 technology_id 输出技术点粒度：gkx 无技术点实体表；主体桥精确同名覆盖 10.85% 的论文机构、42.88% 的论文；标题桥 0.75 以上命中 0/200，上限 0.6829 低于强匹配线——技术点粒度对齐不成立，只能交付机构级双计数与双侧总量。
- **基期声明**：dwd_patent.apdt_year 全库只有 2021—2026；2025（440,401）与 2026（74,810）为采集残年，不进入同比与基期。2017—2020 零行，不得按 0 摊入分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_PAPER_PATENT_CNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PAPER_PATENT_CNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PAPER_PATENT_CNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

