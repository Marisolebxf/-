# 明星企业数（M_ENT_STAR_ENTERPRISE_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_ENTERPRISE_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_ENTERPRISE_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_ENTERPRISE_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_STAR_ENTERPRISE_COUNT |
| 指标名称 | 明星企业数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业总览／明星企业介绍 |
| 更新频率 | 日 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 门户「共 N 家」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_STAR_ENTERPRISE_COUNT.md` |

## 口径定义

gkx 无 CMS 名单表，本件交付的是「专利授权数≥50」构造的代理名单计数 **4,561 家**（候选 4,724、剔除高校/科研/医院 163 家），占底册 189,116 家的 **2.4117%**；深圳 2,590 家（56.7858%）、广州 1,020 家（22.3635%）、东莞 775 家（16.9919%）、惠州 176 家（3.8588%）。阈值从 50 改到 30 立刻变成 9,813 家、改到 100 变成 1,630 家，说明这个「共 N 家」完全由阈值决定，不是名单事实。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_ENTERPRISE_COUNT.md` §二（M_ENT_STAR_ENTERPRISE_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_tech_tag`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：名单真源在门户 CMS（star_roster_item / ads.ent_star_roster_count），gkx 280 张表与 live 开发库均无该结果面；本件交付的是以专利授权数≥50 构造的代理名单计数，语义与 CMS 已发布名单不等价（calc-logic 明禁以此当明星）。计数本身可复算，但名单维度始终无源，故判部分支持。
- **基期声明**：截面件：名单无年度字段，口径是「当前名单里有谁算谁」，不含年度序列；因此不设基期。代理名单依赖的专利快照覆盖 apdt_year 2021—2026，但本指标不用年份切分，2017—2020 零行不影响本读数。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_ENTERPRISE_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_ENTERPRISE_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_ENTERPRISE_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

