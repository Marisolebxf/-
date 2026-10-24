# 专家H指数排行（M_INNOV_EXPERT_HINDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EXPERT_HINDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EXPERT_HINDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EXPERT_HINDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_EXPERT_HINDEX |
| 指标名称 | 专家H指数排行 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | DS-08 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技人才 → 专家画像（柱/雷达，按学科/机构/地域筛选） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_EXPERT_HINDEX.md` |

## 口径定义

`gkx.dwd_scholar` 有 `h_index` 列且 **21,316 行 100% 非空**（min 0 / max 286 / median 18 / mean 21.0），排行本体（按 h 排序取 Top N）**现在就能出**；但口径要求的「按学科/机构/地域筛选」三件事分别只有 8.69%（研究兴趣关键词）、100%（`org` 名称列，但 `scholar_org_id` 全空）、4.97%（按机构名匹配底册得城市）可用，且学科不是学科分类体系、地域匹配严重偏向广东高校。**排行能出、筛选不能出**，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EXPERT_HINDEX.md` §二（M_INNOV_EXPERT_HINDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_scholar`
- `dwd_scholar_paper_relation`
- `dwd_scholar_research_direction`
- `dwd_scholar_talent_flag`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：`gkx.dwd_scholar` 有 `h_index` 列且 **21,316 行 100% 非空**（min 0 / max 286 / median 18 / mean 21.0），排行本体（按 h 排序取 Top N）**现在就能出**；但口径要求的「按学科/机构/地域筛选」三件事分别只有 8.69%（研究兴趣关键词）、100%（`org` 名称列，但 `scholar_org_id` 全空）、4.97%（按机构名匹配底册得城市）可用，且学科不是学科分类体系、地域匹配严重偏向广东高校。**排行能出、筛选不能出**，故判**部分支持**。
- **基期声明**：h_index / paper_nums / citation_nums 均为库内累计值（学者全生涯截面），不按年度切分，因此不构造基期；也无缺失年份可被摊入分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EXPERT_HINDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EXPERT_HINDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EXPERT_HINDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

