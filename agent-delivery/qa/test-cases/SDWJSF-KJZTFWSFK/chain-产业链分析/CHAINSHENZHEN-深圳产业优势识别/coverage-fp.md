# 深圳产业优势识别 · 功能点覆盖（chain.shenzhen / L18）

> catalog `chain.shenzhen` · 50897 · path `#/chain/shenzhen`  
> 用例 `API-深圳产业优势识别-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/chain.json`（页 `chain.shenzhen`）  
> 功能点键：`L18 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

> **同 path 说明**：`chain.sz-problem.main`、`chain.sz-opportunity.main` 与 `chain.shenzhen.main` 共用 path；B 线以 `catalog_page_id` + `endpoint_id` 区分矩阵，禁止与 L24/L25 用例混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| chain.shenzhen.main | GET | /innov/v1/industry/{chainId}/shenzhen | API-00374～00378 | catalog `unavailable`；§0 **未试调**；本批为 **金样 5 条** |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L18 \| chain.shenzhen.main \| chainId \| 算法输入-chainId产业标识 | catalog chainId | API-00374、00376、00377 | 已覆盖 | 主路径占位 + 非法/缺 path |
| L18 \| chain.shenzhen.main \| panorama.enterprise_count \| 算法输出-panorama.enterprise_count深圳企业数 | catalog panorama.enterprise_count | — | **未覆盖** | unavailable 金样批未写 live 成功形态；升档后补 |
| L18 \| chain.shenzhen.main \| panorama.nodes \| 算法输出-panorama.nodes深圳环节节点 | catalog panorama.nodes | — | **未覆盖** | 同上 |
| L18 \| chain.shenzhen.main \| _empty \| 深圳优势识别无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L18 \| chain.shenzhen.main \| _fail \| 深圳优势识别查询失败 | 契约错误态 | API-00375、00376、00377、00378 | 已覆盖 | 鉴权、非法 id、缺 path、畸形 id |
| L18 \| chain.shenzhen.main \| etl_clean_standardize \| 深全国产业数据清洗一致化 | 需规（1）采集清洗 | — | 无对应功能点 | req_only |
| L18 \| chain.shenzhen.main \| advantage_indicator_threshold \| 优势评价指标与权重阈值 | 需规指标体系 | — | 无对应功能点 | req_only |
| L18 \| chain.shenzhen.main \| sz_national_compare_score \| 深全国对比优势评分 | 需规分析阶段评分 | — | 无对应功能点 | req_only |
| L18 \| chain.shenzhen.main \| advantage_domain_identify \| 优势产业领域锁定 | 需规优势识别 | — | 无对应功能点 | req_only |
| L18 \| chain.shenzhen.main \| advantage_industry_list \| 深圳优势产业清单 | 需规（2）优势清单 | — | 无对应功能点 | req_only（样例 nodes 非单独 list 字段） |
| L18 \| chain.shenzhen.main \| advantage_score_detail \| 优势评分与详细指标 | 需规（2）评分指标 | — | 无对应功能点 | req_only |
| L18 \| chain.shenzhen.main \| indicator_analysis_report \| 详细指标分析报告 | 需规（2）分析报告 | — | 无对应功能点 | req_only |
| L18 \| chain.shenzhen.main \| trend_visual_chart_data \| 趋势变化可视化图表数据 | 需规（2）趋势图表 | — | 无对应功能点 | req_only |
| L18 \| chain.shenzhen.main \| scheduled_refresh_monitor \| 持续监测与动态更新 | 需规动态更新 | — | 无对应功能点 | req_only |
| L18 \| chain.shenzhen.main \| industry_tag_report_export \| 产业标签与报告导出 | 需规（3）调用导出 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 2（chainId、_fail） |
| 未覆盖（契约 field / _empty） | 3（enterprise_count、nodes、_empty） |
| 无对应功能点（req_only） | 10 |
| API 用例条数 | 5（00374～00378） |
| 金样 | API-00374 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00374 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
