# 政策级别分布（M_POLICY_LEVEL_DIST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_LEVEL_DIST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_LEVEL_DIST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_LEVEL_DIST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_LEVEL_DIST |
| 指标名称 | 政策级别分布 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技专题服务系统「政策级别指标」柱状图、科技信息展示系统政策追踪页的层级筛选、政策专题页「国家/省/市/区」四段占比条 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_LEVEL_DIST.md` |

## 口径定义

`rank` 列 20,000 行全部有值——19,643 行是明确的层级数组，357 行是只含一个空字符串的 `[""]`；把空字符串过滤后记为「未标注」，五档合计恰好 20,000，国家级 2,174 行的 `province`/`city` 又全部为空，结构自证成立，故判**完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_LEVEL_DIST.md` §二（M_POLICY_LEVEL_DIST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：`rank` 列 20,000 行全部有值（357 行为空数组），可确定派生四级+未标注；五档合计 20,000 与 COUNT(*) 完全一致，国家级 2,174 行的 province/city 全部为空，结构自证成立。多值仅「省级+市级」2,473 条需要一条归并规则，本件按最高层级优先并在产物里给出另一归并的敏感性。结构与数据量都足够，故判完全转换支持。
- **基期声明**：截面指标：统计库内全部政策的层级分布，不做年度序列、不设年度分母。publish_year 的 3 行缺失不进入任何年度口径。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_LEVEL_DIST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_LEVEL_DIST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_LEVEL_DIST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

