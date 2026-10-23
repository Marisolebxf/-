# 科研机构产业领域覆盖（M_ORG_INDUSTRY_COVER）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ORG-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_INDUSTRY_COVER.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_INDUSTRY_COVER.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_INDUSTRY_COVER_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ORG_INDUSTRY_COVER |
| 指标名称 | 科研机构产业领域覆盖 |
| 所属域 | ORG（科研机构） |
| 一级模块 | 科研机构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/ORG/M_ORG_INDUSTRY_COVER.md` |

## 口径定义

本件把 2,074 家科研机构中 194 家（9.35%）有 IPC4 证据的机构，按 IPC 首字母归入 8 个技术部类，共 5,781 件专利入图，用到 259 个 IPC4 小类（全库 634 个的 40.85%）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_INDUSTRY_COVER.md` §二（M_ORG_INDUSTRY_COVER.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件把 2,074 家科研机构中 194 家（9.35%）有 IPC4 证据的机构，按 IPC 首字母归入 8 个技术部类，共 5,781 件专利入图，用到 259 个 IPC4 小类（全库 634 个的 40.85%）。
- **基期声明**：专利为 2021—2026 存量口径（库内 apdt_year 仅此六年，2017—2020 零行，不按 0 摊入；2026 为残年）。本件不跨年比较，不做趋势。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ORG_INDUSTRY_COVER.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_INDUSTRY_COVER.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ORG_INDUSTRY_COVER_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

