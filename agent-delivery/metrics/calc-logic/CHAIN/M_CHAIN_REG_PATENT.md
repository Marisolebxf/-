# 专利（链维/区域维）（M_CHAIN_REG_PATENT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_PATENT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_PATENT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_PATENT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_PATENT |
| 指标名称 | 专利（链维/区域维） |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 区域页「专利」卡片 + 12 链×区域矩阵 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | ["2021", "2022", "2023", "2024"] |
| 缺失年份 | ["2025", "2026"] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_PATENT.md` |

## 口径定义

专利主表 `gkx.dwd_patent` 当日 **2,939,895 件**（窗口 2021—2024）真实可用，名称桥接后 12 条链全部有值、合计 **1,127,340 件**、深圳 **682,209 件**；但官方口径要求的机构—专利关系表 `enterprise_patent_org_rel` 与机构—链关系表 `enterprise_industry_chain` 在 gkx **均不存在**（`information_schema` 零命中），名称桥会漏计更名/同名主体，链归属只能单链、城市归属只能作代理 → **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_PATENT.md` §二（M_CHAIN_REG_PATENT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：专利主表 293.9 万件真实可用，名称桥接后 12 条链均有值；但官方口径要求的机构—专利关系键与机构—链关系表在 gkx 均不存在（information_schema 零命中），名称匹配会漏计更名/同名主体，链归属与城市归属都只能作代理。
- **基期声明**：统计期 2025 年，专利按申请年 ≤2024 截断：`dwd_patent.apdt_year` 只有 2021—2026，且 2025/2026 申请量因公开滞后不完整，纳入会系统性低估近年值；2025/2026 仅作观察不入正式值。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_PATENT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_PATENT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_PATENT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

