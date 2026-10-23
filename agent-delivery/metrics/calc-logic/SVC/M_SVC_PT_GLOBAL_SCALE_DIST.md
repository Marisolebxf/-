# 全球服务机构规模分布（M_SVC_PT_GLOBAL_SCALE_DIST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_GLOBAL_SCALE_DIST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_SCALE_DIST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_SCALE_DIST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_PT_GLOBAL_SCALE_DIST |
| 指标名称 | 全球服务机构规模分布 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（全球供给面 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·专题服务门户 SVCCHAIN-PORTAL（TOPIC-PT-004）；展示侧呼应科技信息展示系统·产业服务链分析→服务机构库 §1.1.1.2.4.2.7.2（规模筛选位） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_PT_GLOBAL_SCALE_DIST.md` |

## 口径定义

注册资本兜底链覆盖 **44,083/44,153（99.84%）**，六桶合计与池全对账（487＋4,594＋3,000＋34,413＋1,589＋70＝44,153），可当日出数；但规模刻画的第一指标——员工数——主链只有 **1,582 家（3.58%）** 有值，只能用注册资本顶替。叠加「全球」境外轴无源，判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_GLOBAL_SCALE_DIST.md` §二（M_SVC_PT_GLOBAL_SCALE_DIST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：注册资本兜底链覆盖 99.84%（44,032/44,153 入桶，含 foreign/unknown 单列），六桶合计与池全对账；但员工数主链只有 1,582 家（3.58%）有值，规模刻画的第一指标不可用，且「全球」轴境外机构无源 → 部分支持
- **基期声明**：截面指标：规模分布取「最近一个有值年」的员工数/当前注册资本，不做跨年比较；年报年份在产物 latest_emp_year_dist 中披露，缺失年不补 0、不参与分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_GLOBAL_SCALE_DIST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_SCALE_DIST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_SCALE_DIST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

