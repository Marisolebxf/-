# 节点优先级/重要度（M_INNOV_DS_02_PATH_003）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_02_PATH_003.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_02_PATH_003.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_02_PATH_003_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_02_PATH_003 |
| 指标名称 | 节点优先级/重要度 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（科技信息展示系统） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 科学技术全景 → 展示关键路径和关键节点 → 节点优先级/重要度 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_02_PATH_003.md` |

## 口径定义

开发库无「节点优先级」现成结果面 → 非完全直接支持；`gkx.dwd_scholar_coauthor` 提供**真实学者合著边**（两端 ID + 合著篇数），1,187,606 行可清洗为 822,018 条去重无向边、620,839 个节点，最大连通块占 98.42%，度/加权度/中介/接近/PageRank 五类量全部非退化（最大度 109、最大中介 0.019213、最大 PageRank 1.74e-4）→ **现在即可经转换得到**，判**完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_02_PATH_003.md` §二（M_INNOV_DS_02_PATH_003.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar`
- `dwd_scholar_coauthor`
- `dwd_scholar_paper_relation`
- `dwd_scholar_papers`
- `dwd_scholar_research_direction`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：开发库无「节点优先级」现成结果面 → 非完全直接支持；`gkx.dwd_scholar_coauthor` 提供**真实学者合著边**（两端 ID + 合著篇数），1,187,606 行可清洗为 822,018 条去重无向边、620,839 个节点，最大连通块占 98.42%，度/加权度/中介/接近/PageRank 五类量全部非退化（最大度 109、最大中介 0.019213、最大 PageRank 1.74e-4）→ **现在即可经转换得到**，判**完全转换支持**。
- **基期声明**：图结构指标取 gkx.dwd_scholar_coauthor 全量截面，不消费任何年份列；无增速、无同比、无基期，故不涉及时序分母，也不存在缺失年被按 0 摊入的风险。
- **复现实测耗时**：约 240.1 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_02_PATH_003.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_02_PATH_003.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_02_PATH_003_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

