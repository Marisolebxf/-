# 技术产业化潜力评分（M_TECH_POTENTIAL_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_POTENTIAL_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_POTENTIAL_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_POTENTIAL_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_POTENTIAL_SCORE |
| 指标名称 | 技术产业化潜力评分 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术潜力评分（TOPIC-TECH-08 / DS-02-TECHGRAPH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_POTENTIAL_SCORE.md` |

## 口径定义

以**深圳**为唯一主体（份额维的 LQ 分母用全国），在 238 个 IPC4 合格域上按「规模 20%、四年增长 30%、LQ 25%、发明占比 15%、转让主体覆盖 10%」打分，得到 **H04W 87.75、H01M 74.47、H04L 71.81** 的头部榜；但需求点名的「基础科研（论文）」与「产品市场（销售、市场调研）」两维在本库无可用键，转化维只能用 **134 家**深圳转让活跃主体作代理（覆盖率中位 **4.6%**），故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_POTENTIAL_SCORE.md` §二（M_TECH_POTENTIAL_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_patent_transfer`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：专利侧四维与 LQ 可复算，但需求点名的「基础科研（论文）」与「产品市场（销售、市场调研）」两维缺源：论文表无 IPC/技术域标引，库内无市场销售或市场规模表；转化维只能用 134 家深圳转让活跃主体作代理，覆盖率中位 4.79%，单家企业即可把一个域推到 80% 以上。故只能交付「专利侧产业化潜力分」。
- **基期声明**：增长维用 2021→2024 首尾比，基期只能是 2021（2017—2020 零行）；2025/2026 为残年，不进入分母。缺失年未按 0 摊入任何均值；LQ 只用 2024 单年，不跨年。
- **复现实测耗时**：约 1.4 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_POTENTIAL_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_POTENTIAL_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_POTENTIAL_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

