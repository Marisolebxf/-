# 研究领域等级划分（M_INNOV_DS_09_RESEARCH_002）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_09_RESEARCH_002.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_RESEARCH_002.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_RESEARCH_002_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_09_RESEARCH_002 |
| 指标名称 | 研究领域等级划分 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科学技术全景 / 科技发展态势 → 科技发展规划 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科学技术全景 → 研究领域分析 → 研究领域等级划分 ｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_09_RESEARCH_002.md` |

## 口径定义

开发库**没有**「研究领域等级」结果面（无任何表带 `research_domain_grade` / `grade` 语义），故不是完全直接支持；依赖侧 `dwd_patent`（293.99 万件、IPC 主分类 242.09 万件、关键词 293.98 万件）与 `dwd_org_base_info`（18.91 万家）结构与量都足，可现算 IPC4 与关键词两维；但**学者维只有 15/60 家企业能对上 `dwd_scholar`**、**论文→企业机构边只能对上 357 篇**，第三维在多数企业对上缺失 → 按 §〇 落 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_09_RESEARCH_002.md` §二（M_INNOV_DS_09_RESEARCH_002.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_author`
- `dwd_en_paper`
- `dwd_en_paper_classification`
- `dwd_id`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_scholar`
- `dwd_scholar_coauthor`
- `dwd_scholar_talent_flag`
- `dwd_zh_author`
- `dwd_zh_paper`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维重叠度均可算（IPC4/关键词/学者），但学者维覆盖率仅 15/60，论文→企业机构边仅 357 篇，且等级阈值在零膨胀下退化（zero_share=0.0）——始终有一维数据不足。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_09_RESEARCH_002.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_RESEARCH_002.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_RESEARCH_002_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

