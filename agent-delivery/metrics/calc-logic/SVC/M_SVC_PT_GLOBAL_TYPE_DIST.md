# 全球服务机构类型分布（M_SVC_PT_GLOBAL_TYPE_DIST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_GLOBAL_TYPE_DIST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_TYPE_DIST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_TYPE_DIST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_PT_GLOBAL_TYPE_DIST |
| 指标名称 | 全球服务机构类型分布 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（全球供给面 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·专题服务门户 SVCCHAIN-PORTAL（TOPIC-PT-004）；展示侧呼应科技信息展示系统·产业服务链分析→服务机构库 §1.1.1.2.4.2.7.2（服务类型筛选位） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_PT_GLOBAL_TYPE_DIST.md` |

## 口径定义

机构**本体**三分类在 gkx 可实算且三类互斥闭合（企业 44,095＋高校 37＋科研院所 21＝44,153）；**服务类型**六类词表也可现转（六类多命中合计 101,335 家次）。但「全球」的境外侧无源，`dwd_forg_base_info` 20,000 行只有 GB/US/CA 三值、不是机构名录，境外机构的类型分布不可得 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_GLOBAL_TYPE_DIST.md` §二（M_SVC_PT_GLOBAL_TYPE_DIST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_org_base_info`
- `dwd_org_org_product_info`
- `dwd_research_institute_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：机构本体三分类在 gkx 可实算且闭合（企业 44,095＋高校 37＋科研院所 21＝44,153），六类服务词表亦可现转；但「全球」轴的境外机构在 gkx 无源（dwd_forg_base_info 仅 GB/US/CA 三值且非服务名录），类型分布在境外面不可得 → 部分支持
- **基期声明**：截面指标：类型分布是当前时点存量的横截面，不含年度分母；池内成立年序列由 M_SVC_PT_GLOBAL_TOTAL 承担，本件不重复计入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_PT_GLOBAL_TYPE_DIST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_TYPE_DIST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_PT_GLOBAL_TYPE_DIST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

