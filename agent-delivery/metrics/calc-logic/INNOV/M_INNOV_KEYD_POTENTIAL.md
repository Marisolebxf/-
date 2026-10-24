# 区域科技创新发展潜力（M_INNOV_KEYD_POTENTIAL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KEYD_POTENTIAL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_POTENTIAL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_POTENTIAL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_KEYD_POTENTIAL |
| 指标名称 | 区域科技创新发展潜力 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_KEYD_POTENTIAL.md` |

## 口径定义

本指标按王惠 ai-1020 的三维框架复算区域创新潜力：D1 产出增速（专利 CAGR + 论文增幅）、D2 新主体（新设强度）、D3 转化活跃（专利转让强度），三维等权合成 0—100 分。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KEYD_POTENTIAL.md` §二（M_INNOV_KEYD_POTENTIAL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_applicants`
- `dwd_patent_transfer`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：D1 的两个子项都可算（专利 CAGR 用 2021/2024 两个真实完整年，论文增幅用 2018-2020 对 2021-2023、四城均千级样本）；D2 已从『增速』降级为『新设强度』，规避底册近年覆盖衰减；但 D3 的属地可归率只有 2.70%（615/22809 条转让记录至少一侧能对上本地底册），且转让表是按件离散记录、不含技术合同登记，无法支撑『区域技术交易活跃度』的完整口径。三维能算、一维量不足，按四档定义判部分支持。
- **基期声明**：专利侧只用 2021/2024 两个真实完整年做 CAGR 端点（dwd_patent 2017—2020 零行，缺失年不按 0 摊入分母）；论文侧基窗 2018—2020、近窗 2021—2023；新设强度用 2024—2025；转让用 2021—2025 生效年。2026 为残年，全部排除。
- **复现实测耗时**：约 2.1 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_KEYD_POTENTIAL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_POTENTIAL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_KEYD_POTENTIAL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

