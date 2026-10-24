# 科研机构扶持推荐指数（M_ORG_CULTIVATE_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ORG-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_CULTIVATE_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_CULTIVATE_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_CULTIVATE_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ORG_CULTIVATE_SCORE |
| 指标名称 | 科研机构扶持推荐指数 |
| 所属域 | ORG（科研机构） |
| 一级模块 | 科研机构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"] |
| 缺失年份 | ["2024"] |
| calc-logic 引用 | `metrics/calc-logic/ORG/M_ORG_CULTIVATE_SCORE.md` |

## 口径定义

按需求原文三维（成果 0.35 / 经费效率 0.25 / 人才 0.20）算出来的分数与招引指数秩相关 0.95，即两个页面会给出几乎相同的排序。这不是实现问题，而是需求问题：§6.6（引入推荐）与 §6.7（扶持推荐）在维度定义上高度同构，都是「成果 + 经费 + 人才」，只是权重不同。

## 计算逻辑说明

```text
score = 0.35S + 0.25F + 0.20T + 0.20G（缺维重归一，≥2 维出分）
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_CULTIVATE_SCORE.md` §二（M_ORG_CULTIVATE_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_scholar`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：按需求原文三维（成果 0.35 / 经费效率 0.25 / 人才 0.20）算出来的分数与招引指数秩相关 0.95，即两个页面会给出几乎相同的排序。这不是实现问题，而是需求问题：§6.6（引入推荐）与 §6.7（扶持推荐）在维度定义上高度同构，都是「成果 + 经费 + 人才」，只是权重不同。
- **基期声明**：作者已声明基期：used=['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']，missing=['2024']。缺失年不计入分母、未按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_CULTIVATE_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_CULTIVATE_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_CULTIVATE_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

