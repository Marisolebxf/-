# 空间密度与集聚度（M_INNOV_KEYD_SPATIAL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KEYD_SPATIAL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_SPATIAL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_SPATIAL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_KEYD_SPATIAL |
| 指标名称 | 空间密度与集聚度 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新评价 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技发展态势 · 科技发展规划 · 重点领域规划 · 区域科技创新空间布局分析（序号 185）｜ **数据支持度**：**完全转换支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_KEYD_SPATIAL.md` |

## 口径定义

无现成「空间密度/集聚度」结果面，故非完全直接支持；但企业坐标 187,983 个点（覆盖底册 99.40%）、四城全部可落格，1 km 网格、网格基尼、Top 格占比、Clark-Evans R 四项全部现算成功且四城结果非退化，**结构 + 当前数据量都够，现在就能算**，判**完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KEYD_SPATIAL.md` §二（M_INNOV_KEYD_SPATIAL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_tech_tag`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：无现成「空间密度/集聚度」结果面，故非完全直接支持；但企业坐标 187,983 个点（覆盖底册 99.40%）、四城全部可落格，1 km 网格、网格基尼、Top 格占比、Clark-Evans R 四项全部现算成功且四城结果非退化，**结构 + 当前数据量都够，现在就能算**，判**完全转换支持**。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 1.2 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KEYD_SPATIAL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_SPATIAL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_SPATIAL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

