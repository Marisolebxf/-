# M_TALENT_SZ_SUPPLY_DEMAND（M_TALENT_SZ_SUPPLY_DEMAND）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_SZ_SUPPLY_DEMAND.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_SZ_SUPPLY_DEMAND.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_SZ_SUPPLY_DEMAND_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_SZ_SUPPLY_DEMAND |
| 指标名称 | M_TALENT_SZ_SUPPLY_DEMAND |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技人才态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2022, 2026] |
| 缺失年份 | [2019, 2020, 2021] |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_SZ_SUPPLY_DEMAND.md` |

## 口径定义

第一，需求侧的域分布被岗位名主导。深圳岗位里经管/人文社科占 35.02%、其他/未归类占 31.74%，两者合计 66.76%。这不是说深圳 67% 的岗位是文职，而是说"产品经理""销售经理""会计""招聘专员"这类泛称被归到了经管，而"工程师"类泛称大量落入"其他"。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_SZ_SUPPLY_DEMAND.md` §二（M_TALENT_SZ_SUPPLY_DEMAND.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_recruit_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：第一，需求侧的域分布被岗位名主导。深圳岗位里经管/人文社科占 35.02%、其他/未归类占 31.74%，两者合计 66.76%。这不是说深圳 67% 的岗位是文职，而是说"产品经理""销售经理""会计""招聘专员"这类泛称被归到了经管，而"工程师"类泛称大量落入"其他"。
- **基期声明**：招聘样本发布日 2022-01-01—2026-07-23，只有这一段；供给侧论文/履历是累计快照，没有同年度切片，因此供需只能同年截面比，不能做「2021 基期→2025 现期」的匹配度变化

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_SZ_SUPPLY_DEMAND.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_SZ_SUPPLY_DEMAND.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_SZ_SUPPLY_DEMAND_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

