# 区域技术成熟度（M_CHAIN_REG_TECH_MATURITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_TECH_MATURITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TECH_MATURITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TECH_MATURITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_TECH_MATURITY |
| 指标名称 | 区域技术成熟度 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN（产业链） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链分析 → 区域技术竞争力 → 技术成熟度 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_TECH_MATURITY.md` |

## 口径定义

专利面板 `patent_panel_innov_20261021.json` 有 2,939,895 行「申请人×年」记录，覆盖 2021—2024 四个申请年；链上企业按 `credit_code` 落主档 35,046 家，专利按第一申请人名匹配 25,294 家、933,873 件（31.77%）。结构和量都够跑 48 个单元，但三个受限点——时间轴只有申请年、无 2025、2017—2020 零行——使「公开年 + 近 k 年」的原式无法完整执行，故判**部分支持**。本档位与 `code/M_CHAIN_REG_TECH_MATURITY_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_TECH_MATURITY.md` §二（M_CHAIN_REG_TECH_MATURITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：专利面板 `patent_panel_innov_20261021.json` 有 2,939,895 行「申请人×年」记录，覆盖 2021—2024 四个申请年；链上企业按 `credit_code` 落主档 35,046 家，专利按第一申请人名匹配 25,294 家、933,873 件（31.77%）。结构和量都够跑 48 个单元，但三个受限点——时间轴只有申请年、无 2025、2017—2020 零行——使「公开年 + 近 k 年」的原式无法完整执行，故判**部分支持**。本档位与 `code/M_CHAIN_REG_TECH_MATURITY_out.json` 的 `support_judgment` 一致。
- **基期声明**：由产物中实际出现的年度键反推：used=[2021, 2022, 2023, 2024]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 0.45 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_TECH_MATURITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TECH_MATURITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TECH_MATURITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

