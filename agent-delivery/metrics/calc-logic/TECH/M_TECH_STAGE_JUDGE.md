# 技术阶段判定（M_TECH_STAGE_JUDGE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_STAGE_JUDGE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_STAGE_JUDGE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_STAGE_JUDGE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_STAGE_JUDGE |
| 指标名称 | 技术阶段判定 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术阶段判定（TOPIC-TECH-09 / DS-02-TECHGRAPH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_STAGE_JUDGE.md` |

## 口径定义

以**深圳**为唯一主体，在 238 个 IPC4 合格域上按「规模 40%、成熟度 40%、动能 20%」打分，按 40 / 60 两个切点分成 **初级 113 域、中级 99 域、高级 26 域**，头部为 **H04W 83.19、H01M 82.54、G06F 77.76**；但需求点名的「技术成熟度指数、技术创新度指数、专家阈值」三项本库都没有现成登记表，成熟度只能用五维专利形态替代、创新度依赖被引（覆盖 0.70%），故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_STAGE_JUDGE.md` §二（M_TECH_STAGE_JUDGE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：「阶段判定」在算法库要求「成熟度指数 + 技术创新度指数 + 专家阈值」，本库三项都不完整：成熟度只能用五维专利形态替代（无 TRL/被引/标准），创新度依赖被引（20,515 行、覆盖 0.70%），专家阈值无登记表。因此本件交付「得分表 + 瓶颈 + 潜力位」，阶段阈值是经验值，不是专家口径。
- **基期声明**：四项年序列只遍历库内真实存在的 2021—2024（2017—2020 零行）；2025/2026 为采集残年，不进动能与稳定性分母。缺失年未按 0 摊入，基期只能是 2021。
- **复现实测耗时**：约 1.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_STAGE_JUDGE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_STAGE_JUDGE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_STAGE_JUDGE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

