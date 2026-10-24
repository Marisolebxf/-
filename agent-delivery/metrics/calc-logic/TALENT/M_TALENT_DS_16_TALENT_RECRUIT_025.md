# 团队组合与协同分析（M_TALENT_DS_16_TALENT_RECRUIT_025）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_025.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_025.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_025_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DS_16_TALENT_RECRUIT_025 |
| 指标名称 | 团队组合与协同分析 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才洞察页「团队组合 / 互补配对」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DS_16_TALENT_RECRUIT_025.md` |

## 口径定义

237 名当前在深学者中 59 人有 20+8 聚类（方向覆盖与重叠可算）、全池可算引用均衡、2,250 条 coauthor 边可算合作密度；但团队产出、项目共担、角色分工、年龄职级全库无字段，深圳机构内部合作边只有 7 条（密度 0—0.4762%）。「协同效应」本身无法验证，判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_025.md` §二（M_TALENT_DS_16_TALENT_RECRUIT_025.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_`
- `dwd_scholar`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：在深 237 名学者中 59 人有 20+8 聚类（可算方向覆盖与重叠）、全池可算引用均衡、coauthor 边 2,250 条可算内部合作密度；但团队产出、项目共担、角色分工、年龄职级全库无字段，关键词仅 1/237 非空，深圳机构内部合作边仅 7 条（密度 0.0%—0.4762%），协同效应本身无法验证。
- **基期声明**：截面口径：聚类来自全时段锚定论文，引用为生涯累计，合作为全时段边；不做年度团队存续/流动分析，故无基期。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_025.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_025.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_025_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

