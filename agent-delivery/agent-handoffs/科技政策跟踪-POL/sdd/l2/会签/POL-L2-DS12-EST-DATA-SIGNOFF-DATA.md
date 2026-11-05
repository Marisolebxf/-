# POL-L2-DS12-EST-DATA-SIGNOFF-DATA · 政策效果推演 · 效果预估 · 数据落点数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-L2-DS12-EST-DATA`
- 监管：`human:淮政玮`
- 对照：`POL-L2-DS12-EST-ARCH` 第 5.1–5.3 节（表归属并看第 9 节）；`is_mock` 对照 `POL-L2-DS11-PLAN-DATA` 第 2 节
- 范围：SRS 232–234
- 结论：**同意会签**

本页只核对 DATA 分册：只一张 forecast 表，列覆盖 232–234，不写 235/236 的列，不写入 ODS、DWD、ADS、供应方库，不灌文本解析，空态是空，新出台临时默认与架构「待甲方确认」一致。`is_mock` 与 DS11 数据分册同句，D4 仍是 mock。不改 DATA 分册，不改架构稿，不改任务状态，不建库，不灌数。

## 库表核对

| 口径 | DATA 分册 | 判定 |
|---|---|---|
| 只一张表 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`。232、233、234 共用。不拆成三张。不写 ODS、DWD、ADS、供应方库 | 第 1、2 节。库只允许 `gkxlumenx_gapfill`。表名以 `gapfill_` 开头。`row_kind` 只有 `未出台仿真`、`新出台预测`、`区域空间`。不复制 `ads.policy_simulate`、`ads.policy_text_parse` | 一致。架构第 5.1–5.3、9 节同这一张、这三种 |
| 列覆盖 232 | `policy_type`、`coverage_scope`、`support_intensity`、`implement_time`、`econ_text`、`social_text`、`innovation_text`、`yearly_trend`、`explain_text`。预测值与变化率写在三列正文里，逐年趋势与一句解释另列。查询原样返回，不按弹性公式现算 | 一致。架构第 5.1 节的四类参数档、三方面预测值、一句解释，以及第 9 节要灌的逐年趋势，都有列可放。字段名按架构归本分册 |
| 列覆盖 233 | `policy_id`、`policy_title`、`short_effect_text`、`long_effect_text`、`growth_text`、`industry_text`、`tech_effect_text`、`time_trend_text`、`space_feature_text`、`similar_basis_text`。依据是行内一句说明 | 一致。架构第 5.2 节的短长期效果、三类影响、时间趋势、空间特征、相似政策依据都有列。行挂在已有政策的 `policy_id` 上 |
| 列覆盖 234 | `region_name`、`policy_type`、`gdp_text`、`industry_change_text`、`employment_text`、`spatial_items`。区域粒度是一段名称。空间分布是同一行上的若干组。服务端只返回行 | 一致。架构第 5.3 节的区域 × 政策类型、GDP、产业结构、就业率、空间分布都有列。热力图与三维地图留在前端 |
| 不写 235、236 的列 | 第 1 节末句只点名归属：`gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` 归 `POL-L2-DS12-SIM-DATA`。第 2、7、8 节写明这两类行不进本表，本文不写那两张表的列 | 一致。列清单没有评估分、主体、渠道、意见正文 |
| 不灌文本解析 | `similar_basis_text` 不存放解析标题、摘要、标签或条款。不调 `parse/jobs`，不调 `policy_text_parse`，不读 `ads.policy_text_parse` 来顶替预测行。不把 `M_POLICY_TEXT_PARSE` 写进行上 | 一致。架构第 5.2 节同句 |
| 空态是空 | 无行或条件对不上则该区空。查询不插入。四类都没提交不返回全部未出台行，对不上不补默认档。未选区域则空间结果空。不造全国兜底行。不把空表写成 501，不直接返回写死的预测。真模型未注册如何返回仍以架构为准，不落在本表 | 一致。架构第 5.1–5.3 节：对不上则空，无行则该区空，不造全国通用行 |
| 新出台临时默认与「待甲方确认」一致 | 第 4 节：需规未定义按颁布日期还是按状态。临时默认是行上不设是否新出台、不设颁布日期截断；`policy_id` 对上全景检索目录已有政策；查询只按 `policy_id` 拣，不在查询里判断颁布日期。甲方确认之前保持这个默认。本单不改客户决策清单 | 一致。架构第 5.2 节把确认前的候选范围与挂哪些政策交给本分册和灌数单按临时默认定 |
| `is_mock` | `tinyint`，非空，每行必须为 1。D4 仍是 mock。三种行 `metric_id` 固定已有 `M_POLICY_SIMULATE`，不新注册，不改 D4。`fill_method=manual` | 一致。与 `POL-L2-DS11-PLAN-DATA` 第 2 节同句。`GDF-POLICY-MOCK-GATE-L01` 仍是 blocked，本单不写成已解开 |
| 灌数单未执行 | `POL-L2-DS12-EST-GAPFILL-L01` 仍是 backlog。本单只点名，不认领，不执行，不建库，不插入。查询请求不灌数。空表返回空 | 一致。架构第 9 节同 |

## 不灌清单

| 种类 | 不灌 |
|---|---|
| 未出台仿真 | 中台三条情景原文、弹性现算、用户模拟历史、布局推荐条数 |
| 新出台预测 | 独立文本解析行、顶替用的解析结果、政策正文、布局推荐条数 |
| 区域空间 | 全国通用兜底行、地图文件、布局推荐条数 |
| 235、236 | 不写入 `gapfill_policy_sim_forecast`。本文不写 `gapfill_policy_sim_result`、`gapfill_policy_sim_stakeholder` 的列 |

`POL-L2-DS12-EST-GAPFILL-L01` 未执行。本页不执行。查询请求不灌数。

## 签收边界

本页不把任务标 done，不改任务状态，不改 DATA 分册，不改架构稿，不建库，不灌数。D4 保持 mock。签收仍由 human:淮政玮 做。
