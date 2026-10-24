# 技术生命周期阶段（M_TECH_LIFE_STAGE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_LIFE_STAGE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_LIFE_STAGE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_LIFE_STAGE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_LIFE_STAGE |
| 指标名称 | 技术生命周期阶段 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术生命周期（TOPIC-TECH-06 / DS-02-TECHGRAPH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_LIFE_STAGE.md` |

## 口径定义

以**深圳**为唯一主体，用 2021—2024 年 IPC4 主分类面板的四年形态判四阶段：**萌芽 15、成长 27、成熟 109、衰退 87**（238 个合格域），2024 年件数占比分别为 1.98% / 13.24% / 60.92% / 20.17%；但生命周期本体需要技术替代关系、法律状态与更长序列，库内专利只有主分类、无替代关系字段，2017—2020 为零行，被引覆盖仅 0.70%，故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_LIFE_STAGE.md` §二（M_TECH_LIFE_STAGE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四年申请年面板可复算四阶段形态（238 域），但生命周期需要技术替代关系、法律状态与更长序列；库内 patent 只有主分类、无替代关系，2017—2020 零行，被引覆盖 0.70%，因此只能交付「申请量形态阶段」，不能交付技术生命周期本体。
- **基期声明**：dwd_patent.apdt_year 只有 2021—2026，2017—2020 零行；因此基期只能取 2021，四年窗口为 2021—2024。2025（440,401 件）与 2026（74,810 件）是采集残年，不进入增长分母；缺失年不按 0 摊入任何均值。
- **复现实测耗时**：约 1.1 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_LIFE_STAGE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_LIFE_STAGE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_LIFE_STAGE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

