# 政策文本解析（M_POLICY_TEXT_PARSE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TEXT_PARSE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TEXT_PARSE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TEXT_PARSE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_TEXT_PARSE |
| 指标名称 | 政策文本解析 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 政策详情页「政策标签」区、政策库检索页左侧「支持工具／对象类型／产业方向／时间节点」四组复选筛选项 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_TEXT_PARSE.md` |

## 口径定义

正本把「政策文本解析」拆成三支：结构化要素抽取（要 `policy_entity` 系三张表）、自动摘要（要生成模型）、自动标签（要关键词/主题/要点三列）。三张实体表在 `gkx` **一张都没有**，三列辅助字段里 `keywords`、`keypoints` 各 0 行、`theme` 只有 2 行，模型权重本机也没有。剩下能做的，只有「在正文上跑闭集词表」这一条路——它属于「部分支持」：有文本、有可复现规则，但没有实体级结构化输出，也没有摘要。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TEXT_PARSE.md` §二（M_POLICY_TEXT_PARSE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_`
- `dwd_global_policy_base`
- `dwd_global_policy_base_bak_20260923`
- `dwd_industry_chain_info`
- `dwd_policy_base`
- `dwd_policy_base_bak_20260923`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：正本把「政策文本解析」拆成三支：结构化要素抽取（要 `policy_entity` 系三张表）、自动摘要（要生成模型）、自动标签（要关键词/主题/要点三列）。三张实体表在 `gkx` **一张都没有**，三列辅助字段里 `keywords`、`keypoints` 各 0 行、`theme` 只有 2 行，模型权重本机也没有。剩下能做的，只有「在正文上跑闭集词表」这一条路——它属于「部分支持」：有文本、有可复现规则，但没有实体级结构化输出，也没有摘要。
- **基期声明**：截面件：政策文本解析对 20,000 条存量政策逐条执行，不按年份切窗、无时间分母。publish_year 跨 1981—2024，2023/2024 的零行是采集断档（DATA_FACTS §3.49 邻域），不得读成「政策文本归零」。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TEXT_PARSE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TEXT_PARSE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TEXT_PARSE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

