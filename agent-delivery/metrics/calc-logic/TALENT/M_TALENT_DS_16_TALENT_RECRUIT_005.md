# 沟通障碍智能检测（M_TALENT_DS_16_TALENT_RECRUIT_005）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_005.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_005.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_005_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DS_16_TALENT_RECRUIT_005 |
| 指标名称 | 沟通障碍智能检测 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 国际人才引进页「沟通障碍评估」（建议不上线，见 §5） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DS_16_TALENT_RECRUIT_005.md` |

## 口径定义

检测对象是「人的沟通行为」，标签是「障碍程度」，两者在 `gkx` 280 张表里都不存在：13 个 `language` 列全部描述论文/文档/政策语种，0 张语音/访谈/会议/邮件表，0 个障碍标签字段；退而求其次用「海外经历」当代理，方向还是反的（经历越多通常障碍越低）。故判**完全不支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_005.md` §二（M_TALENT_DS_16_TALENT_RECRUIT_005.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_paper`
- `dwd_en_paper_abstract`
- `dwd_en_paper_title`
- `dwd_global_policy_base`
- `dwd_global_policy_base_bak_20260923`
- `dwd_industry_analysis_documents`
- `dwd_org_recruit_info`
- `dwd_patent`
- `dwd_patent_bak_20260912`
- `dwd_scholar`
- `dwd_scholar_edu`
- `dwd_scholar_talent_flag`
- `dwd_zh_paper`
- `dwd_zh_paper_abstract`
- `dwd_zh_paper_title`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：全库无个人语言能力字段（13 个 language 列全部指向论文/文档语种），无访谈/语音/会议/邮件语料，无沟通障碍标签；bio 文本里提到英语的仅 28/19,109（0.15%），是自述且无等级。检测对象（沟通行为）与标签（障碍程度）双双缺席，任何打分都是造数。
- **基期声明**：纯截面判定，且不存在可计算的时间序列：语言能力字段与沟通语料均无，故无基期。论文摘要覆盖 1980—2026，但与本指标语义无关，不纳入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_005.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_005.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_005_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

