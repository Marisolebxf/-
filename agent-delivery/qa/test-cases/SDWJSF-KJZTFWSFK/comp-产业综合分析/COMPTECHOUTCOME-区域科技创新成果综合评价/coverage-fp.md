# 区域科技创新成果综合评价 · 功能点覆盖（comp.tech-outcome / L51）

> catalog `comp.tech-outcome` · path `#/industry-comp/tech-outcome`  
> A 线真源：`fp-split-by-api-run/work/L51.md`（只读，未改）  
> B 线用例：`API-区域科技创新成果综合评价-用例.md`（第二轮 **API-01767**～**01776**，R2-批17 重派）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.tech-outcome`

> **path 独占**：`GET /comp/v1/comp/region-tech-outcome` 为本页「科技成果评价」独占，与同模块其它 `region-*-outcome` path 分开验收。`POST /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute` 只挂 title「区域科技创新成果综合评价模型」。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.tech-outcome.main | GET | /comp/v1/comp/region-tech-outcome | API-01767～01771 | unavailable |
| comp.tech-outcome.m_synth_182_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_182_1/compute | API-01772～01776 | available |

---

## 功能点 → 用例矩阵（挂 L51.md）

同一 field 多条场景挂在同一组 API 号上，不按 field_key 各写一条用例。`科技成果评价` 的 sampleResponse 另有 `rank`、`yoy`、`adv`、`radar`（基础科学 / 应用科技 / 科研机构）、`bar_items`、`pie_items`，以及 rows 元素 `name`、`score`、`rank`、`tag`、`note`，已写入 01767～01769 正向预期；A 线未单列这些 field_key。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L51 \| comp.tech-outcome.main \| region \| 算法输入-region区域标签 | catalog region | API-01767、01768、01770 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L51 \| comp.tech-outcome.main \| year \| 算法输入-year年份 | catalog year | API-01767、01769、01771 | 已覆盖 | 主路径 year=2025 + 省略可选 year + 非法 year=-1 |
| L51 \| comp.tech-outcome.main \| index \| 算法输出-index科技创新成果指数 | catalog index | API-01767、01768、01769 | 已覆盖 | 主流程与两条备选断言 index（number，示例 66.3）。文档标记未交付 |
| L51 \| comp.tech-outcome.main \| rows \| 算法输出-rows区域明细行集 | catalog rows | API-01767、01768、01769 | 已覆盖 | 主流程与两条备选断言 rows 及 name、score、rank、tag、note |
| L51 \| comp.tech-outcome.main \| _empty \| 科技成果评价无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L51 \| comp.tech-outcome.main \| _fail \| 科技成果评价查询失败 | 契约错误态 | API-01770、01771 | 部分覆盖 | 仅非法 region、非法 year；可选省略按备选正向，不把「不传」写成失败 |

---

## req_only 行（无 endpoint 挂接）

L51.md 下列 11 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L51 \| （req_only） \| etl_clean_standardize \| 技术专题库多源成果清洗标准化 | 需规（1）采集预处理 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| three_dim_indicators_threshold \| 三维成果指标体系与阈值权重 | 需规指标体系阈值 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| standardize_weight_synthesis \| 指标标准化与加权综合指数 | 需规加权综合 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| strength_weakness_identify \| 优势领域与短板识别 | 需规优短板 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| trend_forecast_report \| 趋势分析与趋势预测报告 | 需规（2）趋势报告 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| policy_resource_allocation_advice \| 政策与资源配置建议 | 需规（2）政策建议 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| composite_eval_detail_outputs \| 综合评价结果与详细指标 | 需规（2）综合与明细 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| region_outcome_type_time_scope \| 区域标签成果类型时间查询语义 | 需规（3）调用范围 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| continuous_monitor_year_refresh \| 持续监测与年份结果刷新 | 需规持续监测 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| index_rows_report_advice_outputs \| 指数明细趋势建议多类输出 | 需规（2）多类输出 | — | 无对应功能点 | 不单开 API 用例 |
| L51 \| （req_only） \| api_sdk_tech_decision_platform \| API SDK 与科技管理平台对接 | 需规（3）系统对接 | — | 无对应功能点 | 不单开 API 用例 |

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| comp.tech-outcome.m_synth_182_1 | API-01772～01776 | 无对应功能点 | L51 未列该 POST endpoint 的 field_key。01772 主流程 sampleRequest（region=440300、year=2025），断言 metric_id、hint 与 responseFields 的 index、rows；01773 省略 region；01774 省略 year；01775 非法 region；01776 非法 year |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 4（`region`、`year`、`index`、`rows`） |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 11 |
| B 线 endpoint | 1（`m_synth_182_1`，无 field_key 行） |
| L51 矩阵行 | 17 |
| API 用例 | 10（01767～01776；主流程 2、备选 4、反向 4） |
| 金样 | API-01767 |
