# 深圳技术发展重点布局领域推荐模型（M_TECH_DEEP_140_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DEEP_140_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_140_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_140_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_DEEP_140_1 |
| 指标名称 | 深圳技术发展重点布局领域推荐模型 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·重点领域推荐（TOPIC-TECH-10 / DS-02-TECHGRAPH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_DEEP_140_1.md` |

## 口径定义

以**深圳**为主体，把 IPC4 域按 `SZ208_MAP` 归入 20+8 产业的 28 个集群，用 LQ、四年增长、规模、政策供给四维打分，24 个产业可评分、Top8 可推荐（网络与通信 72.01 分居首）。但 28 个产业里有 4 个（数字创意、细胞与基因、量子信息、区块链）在 `SZ208_MAP` 中没有 IPC4 前缀，无法进入专利面板；科技项目、技术文献、专家策略三维也没有产业级键。故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DEEP_140_1.md` §二（M_TECH_DEEP_140_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_policy`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：以**深圳**为主体，把 IPC4 域按 `SZ208_MAP` 归入 20+8 产业的 28 个集群，用 LQ、四年增长、规模、政策供给四维打分，24 个产业可评分、Top8 可推荐（网络与通信 72.01 分居首）。但 28 个产业里有 4 个（数字创意、细胞与基因、量子信息、区块链）在 `SZ208_MAP` 中没有 IPC4 前缀，无法进入专利面板；科技项目、技术文献、专家策略三维也没有产业级键。故按四档口径落**部分支持**。
- **基期声明**：dwd_patent 只有 2021—2026；2021 是唯一可用基期，2017—2020 不得按 0 摊入分母。
- **复现实测耗时**：约 1.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_DEEP_140_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_140_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_DEEP_140_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

