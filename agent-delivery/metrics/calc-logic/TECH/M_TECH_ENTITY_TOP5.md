# 根节点 Top5 关键实体与关联强度（M_TECH_ENTITY_TOP5）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_ENTITY_TOP5.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_TOP5.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_TOP5_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_ENTITY_TOP5 |
| 指标名称 | 根节点 Top5 关键实体与关联强度 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | TOPIC-TECH（技术点实体） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 智慧认知大脑/深度挖掘算法/算法工具库/科技专题服务算法库/技术领域深度分析模型构建/技术点头部实体 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| 缺失年份 | [2017, 2018, 2019, 2020, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_ENTITY_TOP5.md` |

## 口径定义

四类实体里两类（机构/企业）有全量 IPC4×申请人可算，一类（论文）有 10.09 万篇标题关键词桥可算但歧义大，一类（人才）完全无表——gkx 无「发明人×IPC」落盘，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_ENTITY_TOP5.md` §二（M_TECH_ENTITY_TOP5.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_patent`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：5 个根技术点、5 组卡片可出：机构/企业卡有全量 IPC4×申请人（581,585 行），论文卡有 100,900 篇标题+关键词桥；但**人才卡整类不可算**——gkx 无「发明人×IPC」落盘，dwd_patent 聚合被 DATA_FACTS §3.13 禁止；专利卡无标题字段（快照未落 title），只能给公开号。四类实体缺一类、弱一类，判部分支持。
- **基期声明**：根技术点用 2024 单年（深圳最新完整年）；机构/企业边权为全期累计（2021—2026），专利卡限定 2024（唯一有 pn 清单的年份）；论文卡不限年（库内以 2019—2024 为主）。2017—2020 在 dwd_patent 为零行，未补 0、未外推。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_ENTITY_TOP5.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_TOP5.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_ENTITY_TOP5_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

