# 技术成熟度等级（M_TECH_MATURITY_LEVEL）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_MATURITY_LEVEL.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_MATURITY_LEVEL.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_MATURITY_LEVEL_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_MATURITY_LEVEL |
| 指标名称 | 技术成熟度等级 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术成熟度（TOPIC-TECH-07 / DS-02-TECHGRAPH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_MATURITY_LEVEL.md` |

## 口径定义

以**深圳**为唯一主体，用 2021—2024 年 IPC4 面板在五个维度打分（规模 25%、授权比 25%、发明占比 15%、集中度 15%、近端稳定性 20%），按 30/42/50/58 四条切线分 **L1 2、L2 54、L3 89、L4 67、L5 26**；L5 只占域数 10.92%、却占 2024 年件数 46.45%。但成熟度的核心证据（TRL、被引、标准/中试、市场渗透）在本库均不存在，授权数只能按申请人份额分摊、无 pn 级授权位，故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_MATURITY_LEVEL.md` §二（M_TECH_MATURITY_LEVEL.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：五维里规模、授权比、发明占比、集中度、稳定性都有结构，但成熟度的核心证据（技术就绪度 TRL、被引、标准/中试、市场渗透）在本库不存在：被引表仅 20,515 行（覆盖 0.70%），无 TRL、无技术标准表；授权数只能按申请人份额分摊、无 pn 级授权位。故只能交付「专利形态五级」，不是 TRL 1—9。
- **基期声明**：专利年序列只遍历库内真实存在的 2021—2024 四年（2025/2026 为采集残年，不进入稳定性分母）；2017—2020 在 dwd_patent 零行，未按 0 补入任何均值或斜率。授权与发明件数是全期累计值（非逐年年份队列），因此 S2/S3 是「跨期平均」，不是 2024 单年队列授权率。
- **复现实测耗时**：约 1.3 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_MATURITY_LEVEL.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_MATURITY_LEVEL.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_MATURITY_LEVEL_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

