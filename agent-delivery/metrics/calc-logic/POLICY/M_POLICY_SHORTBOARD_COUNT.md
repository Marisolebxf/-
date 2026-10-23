# 政策短板清单条数（M_POLICY_SHORTBOARD_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_SHORTBOARD_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_SHORTBOARD_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_SHORTBOARD_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_SHORTBOARD_COUNT |
| 指标名称 | 政策短板清单条数 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·政策分析评价·政策短板诊断卡片 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_SHORTBOARD_COUNT.md` |

## 口径定义

合规维有真值、真触发（34.16% < 90%），覆盖维与有效维分别被「八类词表全中」与「status 单值」代理成 100%，而它们的原生子项（主题覆盖、时效）都不可算。因此条数 = 1 是「一维真短板 + 两维不可判」的合成，不是「三维体检后只有一处问题」。落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_SHORTBOARD_COUNT.md` §二（M_POLICY_SHORTBOARD_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维里合规性可算并实际触发（文号 34.16% < 90%）；覆盖性的主题子项因 theme 仅 2 行不可算、退化为八类词表后 100%；有效性的时效子项因零日期不可算。有必需子项始终无法取值 → 部分支持。
- **基期声明**：本指标为截面阈值计数，不设跨年基期。政策表年份不进入任何分母；2023 年库内 0 行、2022 年后为采集残片，故不做「短板数逐年变化」的时序结论。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_SHORTBOARD_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_SHORTBOARD_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_SHORTBOARD_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

