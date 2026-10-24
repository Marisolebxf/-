# 明星企业基础画像（M_ENT_STAR_BASIC_INFO）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_BASIC_INFO.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_BASIC_INFO.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_BASIC_INFO_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_STAR_BASIC_INFO |
| 指标名称 | 明星企业基础画像 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 智慧服务门户「企业发展 → 明星企业介绍」列表页与详情页头部 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_STAR_BASIC_INFO.md` |

## 口径定义

画像八字段里，行业、属地、成立日期、注册资本、规模档、登记状态六项在 `dwd_org_base_info` 近满覆盖（最低的区县字段 83.0081%），可直算；营收与员工两项靠上市财务表与年报财务表拼，覆盖率 11.66% 与 2.35%；而**名单本身**在 gkx 280 张表里没有任何 star/honor/award 语义表承载，只能用专利授权阈值造代理。名单与规模两维缺，故按 §〇 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_BASIC_INFO.md` §二（M_ENT_STAR_BASIC_INFO.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_stock_finance_info`
- `dwd_org_tech_tag`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：gkx 280 张表无任何 star/honor/award/recogni 语义表，明星名单只能用「专利授权≥50」造代理；画像的属地/行业/成立年/规模字段近满覆盖，但营收 11.66%、员工 6.64%，规模画像基本空白。
- **基期声明**：截面件：名单为当期专利聚合快照（2021—2026 申请年），画像字段取各企业最新可得财务年，不做年度序列，故不设基期；财务覆盖率低（营收 11.66%）本身就是结论，不用早期年份补零。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_BASIC_INFO.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_BASIC_INFO.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_BASIC_INFO_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

