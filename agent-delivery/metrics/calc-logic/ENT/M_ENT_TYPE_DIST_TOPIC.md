# 重点企业类型分布（M_ENT_TYPE_DIST_TOPIC）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TYPE_DIST_TOPIC.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_DIST_TOPIC.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_DIST_TOPIC_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_TYPE_DIST_TOPIC |
| 指标名称 | 重点企业类型分布 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 二级模块 | 重点企业类型分析 |
| 三级模块 | 类型 × 行业主题分布图 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 重点企业类型分析·类型 × 行业主题分布图｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_TYPE_DIST_TOPIC.md` |

## 口径定义

名单内三类（高企 2,804、科技型中小 1,663、上市 425）都能按 `org_id` 直取，占比与重叠也闭得上；但四类里的「外资」在 gkx 6,312 列中没有任何 `foreign` 标签列，只有 226 家工商登记文本可作旁证，且名单与标签都没有 `stat_year`，环比无上年格。再加上 calc-logic 的 `sme`（科技型中小企业）与需规原文的「小微（注册资本 + 员工人数）」不是同一个分类，判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TYPE_DIST_TOPIC.md` §二（M_ENT_TYPE_DIST_TOPIC.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_base`
- `dwd_org_tech_tag`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：名单内三类（高企 2,804、科技型中小 1,663、上市 425）都能按 `org_id` 直取，占比与重叠也闭得上；但四类里的「外资」在 gkx 6,312 列中没有任何 `foreign` 标签列，只有 226 家工商登记文本可作旁证，且名单与标签都没有 `stat_year`，环比无上年格。再加上 calc-logic 的 `sme`（科技型中小企业）与需规原文的「小微（注册资本 + 员工人数）」不是同一个分类，判 **部分支持**。
- **基期声明**：本件是单期截面：名单与标签均无 stat_year，环比没有上年格。used/missing 为空，不是把缺年按 0 摊入；同比按空处理。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TYPE_DIST_TOPIC.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_DIST_TOPIC.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TYPE_DIST_TOPIC_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

