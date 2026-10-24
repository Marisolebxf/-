# 产业链热点综合评分（M_CHAIN_HOTSPOT_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HOTSPOT_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOTSPOT_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOTSPOT_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_HOTSPOT_SCORE |
| 指标名称 | 产业链热点综合评分 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业热点领域识别 |
| 更新频率 | 周 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链页「热点评分」卡与链级热度排名 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_HOTSPOT_SCORE.md` |

## 口径定义

按四维等权（企业增速／投融资／专利密度／资讯热度，各 0.25）计算，12 条链均值 **30.23**、标准差 **14.17**；具身智能 **69.94** 居首、人工智能 **39.20** 次之、智能网联汽车 **16.90** 垫底。首名在 1,771 组权重网格里占 **75.381%**，对权重不算敏感；但四维原始值全是代理、资讯数组近半截断，分数只能作链间相对热度，不是模型原分。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HOTSPOT_SCORE.md` §二（M_CHAIN_HOTSPOT_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_industry_chain_news_info`
- `dwd_org_industry_chain_pat_dtl`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：calc-logic 的四维结果表 chain_hotspot 在 gkx 侧 0 张（280 表里 hotspot 关键词零命中），live 侧只有 8 行未来产业种子样例、与 12 链仅 1 条重名，不能当结果面。企业增速、投融资、专利、资讯四个原始字段都没有真源，只能用可核代理重建：成立年分布、融资事件、申请人专利、资讯挂链次数。四维结构与 min-max 合成方式对得上，但每个代理与模型原分不是同一把尺（事件数不是热度、专利件数不是密度分、资讯条数不是关注度），且权重未冻结（本件等权为自定义），故判部分支持。
- **基期声明**：增速维用 2021—2025 成立企业数（2026 残年不进增速分母）；资讯维用 2025—2026 两个完整/残年，2026 按资讯表实际覆盖计、不折算年化。2019 及更早的成立年只进「有成立年企业数」分母，不单独做基期。库内无更早的资讯年份（2024 及以前 0 行），故 missing 为空而非摊 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HOTSPOT_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOTSPOT_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HOTSPOT_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

