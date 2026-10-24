# 全球服务机构产业布局（M_SVC_INDUSTRY_LAYOUT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_INDUSTRY_LAYOUT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_INDUSTRY_LAYOUT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_INDUSTRY_LAYOUT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_INDUSTRY_LAYOUT |
| 指标名称 | 全球服务机构产业布局 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | 产业服务链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2026] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_INDUSTRY_LAYOUT.md` |

## 口径定义

地理三轴（省→市→区）与产业门类轴均可算且覆盖率 ≥ 90%，但「全球」轴在 gkx 库内无任何字段支撑（池内 44,132 家非空省份机构 100% 为广东省），产业维只到门类不到中类，故按「部分支持」定档，不抬档。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_INDUSTRY_LAYOUT.md` §二（M_SVC_INDUSTRY_LAYOUT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_org_product_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：地理维（省→市→区）、产业维（国民经济行业门类 20 类，覆盖 99.88%）、服务维（主服务类型 7 类 + 服务环节 6 类）三轴交叉全部在库内实测可算，格子数、HHI、CR3、香农熵、环节渗透率均已落盘；但「全球」轴实现不了——池内 44,132 家有省份的机构 100% 是广东省，库内无 country/境外机构字段，布局只能做到省域内 4 市 26 区，且产业维只到门类不到中类小类，故判部分支持。
- **基期声明**：布局是存量截面（工商登记在营状态），不对年度序列做拆分；inc_year 只用于结构描述，不作为基期。占比分母统一用池 44,153，不用「有该字段的机构数」，避免缺字段处被悄悄抬升。
- **复现实测耗时**：约 0.524 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_INDUSTRY_LAYOUT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_INDUSTRY_LAYOUT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_INDUSTRY_LAYOUT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

