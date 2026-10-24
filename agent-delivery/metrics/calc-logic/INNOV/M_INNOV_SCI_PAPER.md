# 科学论文数量（M_INNOV_SCI_PAPER）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCI_PAPER.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_PAPER.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_PAPER_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCI_PAPER |
| 指标名称 | 科学论文数量 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科学创造力评估页「科学论文数量分析」卡片（柱/折），支持年、季、月三种时间粒度与研究机构、地域两个切片 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2019, 2020, 2021, 2022, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_SCI_PAPER.md` |

## 口径定义

按时间（年/季/月）× 研究机构 × 地域统计特定领域论文发表数量；本批领域维未传参，输出全库分布，领域筛选用题名/关键词二次过滤

> 一句话口径（源件 §0.3）：`gkx.dwd_zh_paper` 100,900 行、100,900 个互异 `id`，`cover_year_start` 100% 可解析（1980—2026 共 47 个年份），作者串 `author_info_list` 可解析出 436,086 个署名实例、84,320 个互异机构名，其中 93,817 篇（92.98%）能按机构名或地址文本识别到城市；没有现成的论文计数面，但**结构与当日数据量都已足够**，脚本一条 SQL 拉窄列、54.6 秒跑完并落 `_out.json`，故判**完全转换支持**。唯一需要披露的是 2024 年存在采集批次尖峰（32,379 篇，占全库 32.09%，是 2023 年的 4.87 倍）与类型维只有「期刊论文」单值，这两点改变趋势图的读法，不改变「现在就能算」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCI_PAPER.md` §二（M_INNOV_SCI_PAPER.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_paper`
- `dwd_org_base_info`
- `dwd_rd`
- `dwd_zh_author`
- `dwd_zh_paper`
- `dwd_zh_paper_citation`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：`gkx.dwd_zh_paper` 100,900 行、100,900 个互异 `id`，`cover_year_start` 100% 可解析（1980—2026 共 47 个年份），作者串 `author_info_list` 可解析出 436,086 个署名实例、84,320 个互异机构名，其中 93,817 篇（92.98%）能按机构名或地址文本识别到城市；没有现成的论文计数面，但**结构与当日数据量都已足够**，脚本一条 SQL 拉窄列、54.6 秒跑完并落 `_out.json`，故判**完全转换支持**。唯一需要披露的是 2024 年存在采集批次尖峰（32,379 篇，占全库 32.09%，是 2023 年的 4.87 倍）与类型维只有「期刊论文」单值，这两点改变趋势图的读法，不改变「现在就能算」。
- **基期声明**：论文年序列自 1980 起连续；2019—2024 六年均为真实年份，无缺失年
- **复现实测耗时**：约 54.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCI_PAPER.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_PAPER.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCI_PAPER_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

