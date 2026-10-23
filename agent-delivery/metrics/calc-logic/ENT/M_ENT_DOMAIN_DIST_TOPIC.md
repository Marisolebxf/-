# 企业领域分布（M_ENT_DOMAIN_DIST_TOPIC）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DOMAIN_DIST_TOPIC.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_DIST_TOPIC.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_DIST_TOPIC_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DOMAIN_DIST_TOPIC |
| 指标名称 | 企业领域分布 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 专题企业 |
| 二级模块 | TOPIC-ENT-05 |
| 三级模块 | 企业领域分布 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 专题企业页「各领域企业数量」条形/饼图与逐年趋势线｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_DOMAIN_DIST_TOPIC.md` |

## 口径定义

本件能给出**单期 × 12 条产业链**的家数与占比，不能给出**年度 × 15 集群**的分布与同比：链归属表没有 `stat_year`，15 集群目录与 map 两库均无，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DOMAIN_DIST_TOPIC.md` §二（M_ENT_DOMAIN_DIST_TOPIC.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_id`
- `dwd_industry_chain_info`
- `dwd_org_industry_tags`
- `dwd_org_tech_tag`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件能给出**单期 × 12 条产业链**的家数与占比，不能给出**年度 × 15 集群**的分布与同比：链归属表没有 `stat_year`，15 集群目录与 map 两库均无，故判 **部分支持**。
- **基期声明**：本件无年度键：链归属表没有 stat_year，created_time 只有单一批次。因此既没有「进入分母的年份」，也没有「缺哪一年」，used/missing 为空；同比按「上年格不存在」记空，不按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DOMAIN_DIST_TOPIC.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_DIST_TOPIC.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_DIST_TOPIC_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

