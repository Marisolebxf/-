# 产业热点领域识别 · 功能点覆盖（chain.hotspot / L17）

> catalog `chain.hotspot` · 50897 · path `#/chain/hotspot`  
> 用例 `API-产业热点领域识别-用例.md`  
> A 线范围：**L17**（`fp-split-by-api-run/work/L17.md`）  
> 功能点键：`L17 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.hotspot.hot | GET | /innov/v1/industry/{chainId}/hotspot | API-00059～00062 | catalog `unavailable`；50897 as-built 见用例 §0 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L17 \| chain.hotspot.hot \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00059、API-00060 | 已覆盖 | 合法主路径 + 非法 id 单缺陷 |
| L17 \| chain.hotspot.hot \| hotspot_score \| 算法输出-hotspot_score热点分 | catalog hotspot_score | API-00059 | 已覆盖 | 金样断言 number 型存在；不写具体分值 |
| L17 \| chain.hotspot.hot \| hot_news \| 算法输出-hot_news热点新闻 | catalog hot_news | API-00059 | 已覆盖 | 金样断言 array 型存在 |
| L17 \| chain.hotspot.hot \| _empty \| 热点识别无数据空态 | 契约空结果 | — | **未覆盖** | catalog 示 INB1701 无热点；50897 试调仍返回 mock 非空，无稳定空态条件 |
| L17 \| chain.hotspot.hot \| _fail \| 热点识别查询失败 | 契约错误态 | API-00060、API-00062 | 已覆盖 | 00060 非法 chainId；00062 契约 unavailable 占位 |
| L17 \| chain.hotspot.hot \| hotspot_indicator_threshold \| 热点指标与阈值体系 | 需规指标体系 | — | 无对应功能点 | A 线 req_only，无独立 HTTP 字段 |
| L17 \| chain.hotspot.hot \| hotspot_domain_identify \| 热点领域锁定识别 | 需规热点识别 | — | 无对应功能点 | req_only |
| L17 \| chain.hotspot.hot \| hotspot_structure_analysis \| 热点结构特征分析 | 需规结构特征 | — | 无对应功能点 | req_only |
| L17 \| chain.hotspot.hot \| hotspot_trend_analysis \| 热点变化趋势分析 | 需规变化趋势 | — | 无对应功能点 | req_only |
| L17 \| chain.hotspot.hot \| hotspot_structure_report \| 热点结构分析报告 | 需规（2）结构报告 | — | 无对应功能点 | req_only |
| L17 \| chain.hotspot.hot \| hotspot_trend_chart_data \| 热点变化趋势图表数据 | 需规（2）趋势图表 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 4（chainId、hotspot_score、hot_news、_fail） |
| 未覆盖 | 1（_empty） |
| 无对应功能点（req_only） | 5 |
| API 用例条数 | 4（00059～00062） |
