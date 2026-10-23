# 政策类型分布（M_POLICY_TYPE_DIST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TYPE_DIST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TYPE_DIST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TYPE_DIST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_TYPE_DIST |
| 指标名称 | 政策类型分布 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统「政策类型指标」饼图、科技信息展示系统政策检索页的「文种」筛选、政策专题页的「管理办法/申报通知/公示公告」快捷入口 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_TYPE_DIST.md` |

## 口径定义

**文种维度（`type`）**：14 种取值、20,000 行全覆盖、未标注 1,862 行——结构与数据都够，**这一半是完全转换支持**。 **主题维度（`theme` / `keywords` / `keypoints`）**：`theme` 仅 2 行有值，`keywords` 与 `keypoints` 为 0——**这一半是数据不足**。 两者合成，按「始终有部分维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TYPE_DIST.md` §二（M_POLICY_TYPE_DIST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：需求要的「产业政策/人才政策/企业扶持政策」是主题分类，对应 `theme`；该列全表只有 2 行有效值（0.01%），`keywords`/`keypoints` 各 0 行，`policy_support` 20,000 行全为小写字符串 'null'。现能算的 `type` 是文种（其他通知/公示公告/申报通知/政策文件-…），不是政策主题。主题维始终不可得，只能交付「文种分布」降级口径，故判部分支持。
- **基期声明**：截面指标：统计库内全部政策的文种分布，不设年度分母。publish_year 缺 3 行，不影响本件（本件不按年切分）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TYPE_DIST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TYPE_DIST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TYPE_DIST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

