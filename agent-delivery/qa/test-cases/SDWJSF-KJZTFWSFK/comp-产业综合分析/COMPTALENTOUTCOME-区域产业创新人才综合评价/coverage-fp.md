# 区域产业创新人才综合评价 · 功能点覆盖（comp.talent-outcome / L53）

> catalog `comp.talent-outcome` · path `#/industry-comp/talent-outcome`  
> A 线真源：`fp-split-by-api-run/work/L53.md`（只读，未改 work）  
> **B 线用例**：`FUNC-区域产业创新人才综合评价-用例.md`（第三轮 **FUNC-01026**～**FUNC-01037**）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.talent-outcome`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

> **path 独占**：`GET /comp/v1/comp/region-talent-outcome` 为本页 `人才成果评价` 独占。`POST /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute` 只挂 title「区域产业创新人才综合评价模型」。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.talent-outcome.main | GET | /comp/v1/comp/region-talent-outcome | FUNC-01026～01030 | unavailable |
| comp.talent-outcome.m_synth_184_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_184_1/compute | FUNC-01031～01035 | available |

---

## 功能点 → 用例矩阵（挂 L53.md）

同一 field_key 的多种场景挂在同一组 FUNC 号上，不按 field_key 各写一条用例。`人才成果评价` 的 sampleResponse 另有 `rank`、`yoy`、`adv`、`radar`（人才规模 / 人才结构 / 人才成果）、`bar_items`、`pie_items`、`rows`（name / score / rank / tag / note），已写入 01026～01028 正向预期；A 线未单列这些 field_key。`responseFields` 只声明顶层 `index`（人才指数）。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L53 \| comp.talent-outcome.main \| region \| 算法输入-region区域标签 | catalog region | FUNC-01026、01027、01029 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L53 \| comp.talent-outcome.main \| year \| 算法输入-year年份 | catalog year | FUNC-01026、01028、01030 | 已覆盖 | 主路径 year=2025 + 省略可选 year + 非法 year=-1 |
| L53 \| comp.talent-outcome.main \| index \| 算法输出-index人才创新成果指数 | catalog index | FUNC-01026、01027、01028 | 已覆盖 | 主流程与两条备选断言 index（number，示例 66.3）及 sampleResponse 其余字段；catalog unavailable |
| L53 \| comp.talent-outcome.main \| _empty \| 人才成果评价无数据空态 | 契约空结果 | — | 未覆盖 | sampleResponse 为非空指数与名单，无稳定空结果构造条件，不单开空态用例 |
| L53 \| comp.talent-outcome.main \| _fail \| 人才成果评价查询失败 | 契约错误态 | FUNC-01029、01030 | 部分覆盖 | 仅非法 region、非法 year；预期 message 或 msg 指出该参数非法。省略参数记备选。上游或网关失败未单开 |
| （页面清单） \| comp.talent-outcome \| 接口信息 / 算法测试 | 联调台清单 | FUNC-01036、01037 | 已覆盖 | 双接口页清单 2 条 |

---

## req_only 行（无 endpoint 挂接）

L53.md 中下列 11 行 **req_only**，endpoint 为空，B 线记 **无对应功能点**，不单独开 FUNC 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L53 \| （req_only） \| etl_clean_standardize \| 多源人才数据清洗标准化 | 需规（1）采集预处理 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| four_dim_indicators_threshold \| 四维人才指标体系与阈值 | 需规指标体系阈值 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| standardize_weight_synthesis \| 维度指标标准化与权重合成 | 需规标准化权重 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| dimension_sub_eval_results \| 各维度分项评价结果 | 需规（2）分项评价 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| regional_rank_compare \| 区域排名与横向对比 | 需规区域对比排名 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| viz_chart_analysis_report \| 可视化图表与对比分析报告 | 需规可视化报告 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| historical_time_series \| 历史对比与时间序列分析 | 需规历史时序 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| region_time_dimension_scope \| 区域标签时间维度类型查询语义 | 需规（3）调用范围 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| realtime_monitor_refresh \| 自动化监测与结果刷新 | 需规（3）监测刷新 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| index_sub_rank_report_outputs \| 指数分项排名报告四类输出 | 需规（2）四类输出 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L53 \| （req_only） \| api_sdk_talent_platform \| API SDK 与人才平台对接 | 需规（3）系统对接 | — | 无对应功能点 | 不单开 FUNC 用例 |

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| comp.talent-outcome.m_synth_184_1 | FUNC-01031～01035 | 无对应功能点 | L53 未列该 POST endpoint 的 field_key。01031 主流程 sampleRequest（region=440300、year=2025），断言 metric_id、hint 与 responseFields 的 index；01032 省略 region；01033 省略 year；01034 非法 region；01035 非法 year |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 3（`region`、`year`、`index`）+ 清单 2 |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 11 |
| B 线独有 endpoint | 1（`comp.talent-outcome.m_synth_184_1`，5 条用例） |
| FUNC 用例条数 | **12**（01026～01037） |
| 主流程 | 2（01026 人才成果评价；01031 区域产业创新人才综合评价模型） |
| 备选 | 4（01027、01028、01032、01033） |
| 反向 | 4（01029、01030、01034、01035） |
| 清单 | 2（01036、01037） |
| 编号闭区间 | **FUNC-01026**～**FUNC-01037** |
| 旧 API 册 | API-01782～01791 作废，见 FUNC 册 §4 |
