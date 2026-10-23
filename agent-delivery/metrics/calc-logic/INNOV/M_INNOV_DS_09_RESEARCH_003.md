# 竞争情报等级（M_INNOV_DS_09_RESEARCH_003）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_09_RESEARCH_003.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_RESEARCH_003.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_RESEARCH_003_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_09_RESEARCH_003 |
| 指标名称 | 竞争情报等级 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科学技术全景 / 科技发展态势 → 科技发展规划 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科学技术全景 → 研究领域分析 → 多企业竞争情报比对（分值/等级层）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_09_RESEARCH_003.md` |

## 口径定义

库内**没有任何竞争情报分值或等级结果表**（无 `ci_score` / `ci_level` 字段），故不是完全直接支持；依赖侧 `dwd_patent`（293.99 万件）、`dwd_org_base_info`（18.91 万家）、`dwd_scholar`（2.13 万位）可现算，1,770 个企业对已跑出 1.95–46.18 的分值与健康分档；但**分值只由研究领域重合驱动，无市场份额/价格/渠道/交易数据**，学者维仅 15/60，按 §〇「始终有部分依赖维度无法得到足够数据」判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_09_RESEARCH_003.md` §二（M_INNOV_DS_09_RESEARCH_003.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_author`
- `dwd_en_paper`
- `dwd_en_paper_classification`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_scholar`
- `dwd_scholar_talent_flag`
- `dwd_zh_author`
- `dwd_zh_paper`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：分值与等级可对 1770 个企业对现算并给出矩阵，但（1）学者维覆盖率过低（15/60）、（2）论文→企业机构边仅 357 篇，（3）竞争情报仅含研究领域重合这一维度，缺市场/交易数据；按 §〇「始终有部分依赖维得不到足够数据」判部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_09_RESEARCH_003.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_RESEARCH_003.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_09_RESEARCH_003_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

