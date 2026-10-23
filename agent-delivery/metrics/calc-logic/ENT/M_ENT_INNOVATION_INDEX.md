# 创新能力指数（M_ENT_INNOVATION_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_INNOVATION_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INNOVATION_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INNOVATION_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_INNOVATION_INDEX |
| 指标名称 | 创新能力指数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 算法库「深圳企业竞争力水平分析模型」§1.1.1.1.1.1.1.5.1 创新能力评估分支（SRS 需规清单序号 141）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_INNOVATION_INDEX.md` |

## 口径定义

无「创新能力指数」结果面（calc-logic 落表 `ads_ent_innovation_index` 待建）→ 非完全直接支持；14 个三级指标中——专利三项原料足（`dwd_patent` 294 万行 + 法务 20,000 行），财务侧薄填充（研发投入 0/90,926、研发人员 0、从业 3,184/90,926），五项 calc-logic 自标待建复核确认零承载（资本化研发/科研平台/学历结构/软件著作权/无形资产明细四空一误中），获奖类标签 LIKE 探针 0 命中 → 三准则层中投入层半缺、产出层两项缺、可持续层薄 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_INNOVATION_INDEX.md` §二（M_ENT_INNOVATION_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `ads_ent_innovation_index`
- `dwd_org_annual_financial_info`
- `dwd_org_rd_achiev_info`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_patent_legal`
- `dwd_scholar_education_background`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：14 项三级指标中：专利三项原料足（294 万专利+法务 20,000 行）；财务侧薄填充（研发 0/90926、研发人员 0、从业 3184）；五项 calc-logic 自标待建复核确认零承载（{'capitalized_rd_field': 0, 'research_platform_table': 0, 'education_structure_field': 2, 'software_copyright_table': 0, 'intangible_asset_detail': 0} 全空）；获奖类标签 LIKE 探针 0 类命中（待口径确认）。三准则层中投入层半缺、产出层两项缺、可持续层薄 → 部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_INNOVATION_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INNOVATION_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_INNOVATION_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

