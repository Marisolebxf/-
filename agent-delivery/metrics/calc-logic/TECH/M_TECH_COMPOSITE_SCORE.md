# 技术域综合评价分（M_TECH_COMPOSITE_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_COMPOSITE_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_COMPOSITE_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_COMPOSITE_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_COMPOSITE_SCORE |
| 指标名称 | 技术域综合评价分 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术分析／技术域评价 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 技术域总览页的六边形雷达、「优先布局技术域」卡片 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_COMPOSITE_SCORE.md` |

## 口径定义

综合分的**算法面**没有任何障碍：归一、加权、排序三步都能落地，10 个域都能出分。卡住的是**权重该乘什么**——11 个子指标里 4 个无源（前沿论文机构、技术交易额、区域交易额、技术资讯），4 个只有代理（论文四维都靠学科上界与机构归属），只有 3 个专利维是真值。也就是说，一个「综合评价」里六成以上的语义（前沿性、市场化、动态性）没有数据承接。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_COMPOSITE_SCORE.md` §二（M_TECH_COMPOSITE_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_deal`
- `dwd_deal_bak_20260912`
- `dwd_patent`
- `dwd_patent_transfer`
- `dwd_scholar_paper_relation`
- `dwd_zh_paper`
- `dwd_zh_paper_classification`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：综合分的计算面（归一 + 加权 + 排序）完全可实现，10 个域都能出分；但 11 个子指标里 4 个无源（前沿质量、技术交易额两项、资讯），2 个只有机构代理且城市覆盖 37.09%，可用维只有 5 个；且主分与「只看专利规模」的秩相关达 0.9 以上——说明缺的那几维本来承担区分，去掉后综合分退化为专利规模的不同写法。按「始终有部分依赖维无法得到」判部分支持。
- **基期声明**：专利侧六个年份（2021—2026）全部计入域件数，2026 为残年（69,747 件，约为 2025 的 20.4%）只做端点披露、不用于增速；论文侧上界无年份字段，不做域×年双轴。跨年不摊 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_COMPOSITE_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_COMPOSITE_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_COMPOSITE_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

