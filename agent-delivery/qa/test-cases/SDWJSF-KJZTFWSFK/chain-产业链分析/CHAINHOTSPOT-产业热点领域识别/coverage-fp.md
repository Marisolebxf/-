# 产业热点领域识别 · 功能点覆盖（chain.hotspot / L17）

> catalog `chain.hotspot` · path `#/chain/hotspot`  
> A 线真源：`fp-split-by-api-run/work/L17.md`  
> C 线用例：`FUNC-产业热点领域识别-用例.md`（第三轮 **FUNC-00503**～**00508**）  
> 历史 R2 API 册：`API-产业热点领域识别-用例.md`（**API-01296**～**01299**，第三轮已删除）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.hotspot.hot | GET | /innov/v1/industry/{chainId}/hotspot | FUNC-00503、00504 | unavailable |
| chain.hotspot.m_chain_deep_120_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_120_1/compute | FUNC-00505、00506 | available |
| （页面清单） | — | — | FUNC-00507、00508 | — |

---

## 功能点 → 用例矩阵（挂 L17.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L17 \| chain.hotspot.hot \| chainId \| 算法输入-chainId产业标识 | FUNC-00503、00504 | 已覆盖 | 合法 path chainId=INB1702 + 缺 chainId；规则来源 catalog chainId |
| L17 \| chain.hotspot.hot \| hotspot_score \| 算法输出-hotspot_score热点分 | FUNC-00503 | 已覆盖 | 主流程断言 hotspot_score（number）；规则来源 catalog hotspot_score |
| L17 \| chain.hotspot.hot \| hot_news \| 算法输出-hot_news热点新闻 | FUNC-00503 | 已覆盖 | 同条主流程断言 hot_news（array）及元素 title、views；规则来源 catalog hot_news |
| L17 \| chain.hotspot.hot \| _empty \| 热点识别无数据空态 | — | 未覆盖 | 描述写 INB1701 无热点，无稳定空态构造条件；规则来源 契约空结果 |
| L17 \| chain.hotspot.hot \| _fail \| 热点识别查询失败 | FUNC-00504 | 部分覆盖 | 仅缺 chainId 反向（message/msg）；规则来源 契约错误态 |

主流程 FUNC-00503 的预期同时断言 sampleResponse 中未单独挂 L17 行的 `news_count`、`investment_total`、`new_enterprise_count` 及 `hot_news[].title`、`hot_news[].views`。不据此另开用例或矩阵行。

---

## req_only 行（无 endpoint 挂接）

L17.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields 挂接。C 线记 **无对应功能点**，不单独开用例：

`etl_clean_standardize`（多源资讯标准化清洗与过滤，规则来源 需规（1）采集清洗）、`hotspot_indicator_threshold`（热点指标与阈值体系，规则来源 需规指标体系）、`hotspot_domain_identify`（热点领域锁定识别，规则来源 需规热点识别）、`hotspot_structure_analysis`（热点结构特征分析，规则来源 需规结构特征）、`hotspot_trend_analysis`（热点变化趋势分析，规则来源 需规变化趋势）、`scheduled_refresh_monitor`（动态跟踪与周期更新，规则来源 需规动态更新）、`hotspot_structure_report`（热点结构分析报告，规则来源 需规（2）结构报告）、`hotspot_trend_chart_data`（热点变化趋势图表数据，规则来源 需规（2）趋势图表）、`sub_segment_scope`（细分领域识别范围，规则来源 需规调用方式）、`analysis_report_export`（分析报告与数据导出，规则来源 需规（3）导出）。

---

## C 线独有（catalog 有、L17 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L17 \| chain.hotspot.m_chain_deep_120_1 \| — \| 产业热点领域识别模型 | FUNC-00505、00506 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint）与缺 chainId；L17 未给该 endpoint 挂 field 行 |
| （页面清单）接口信息 / 算法测试 | FUNC-00507、00508 | 无对应功能点 | 2 接口下拉与 method/path 刷新 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| FUNC 用例数 | 6（FUNC-00503～00508） |
| FUNC 主流程 | 2（00503 产业热点领域识别、00505 产业热点领域识别模型） |
| FUNC 反向 | 2（00504、00506，均为缺 chainId） |
| FUNC 清单 | 2（00507 接口信息、00508 算法测试） |
| 历史 API 用例数 | 4（API-01296～01299，R2，册已删） |
| L17 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L17 req_only | 10（无对应功能点） |
