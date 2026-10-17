# 深圳企业竞争力水平分析 · 功能点覆盖（entan.competitiveness / L27）

> catalog `entan.competitiveness` · 50897 · path `#/entan/competitiveness`  
> **用例册**：`API-深圳企业竞争力水平分析-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00075`～`00084`，共 **10** 条）  
> A 线范围：**L27**（`fp-split-by-api-run/work/L27.md`）  
> 功能点键：`L27 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.competitiveness.score | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | API-00075～00080 | unavailable |
| entan.competitiveness.ranking | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | API-00081～00084 | unavailable |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L27 \| entan.competitiveness.score \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00075、00077、00078、00079、00080 | 契约占位 / 入参异常 | endpoint unavailable；合法集合主路径见 00075 |
| L27 \| entan.competitiveness.score \| enterprises \| 算法输出-enterprises企业竞争力结果集 | catalog enterprises | API-00075 | 契约占位 | 禁止 sample total_score 作通过条件；可用后需补 live 主路径 |
| L27 \| entan.competitiveness.score \| _empty \| 综合竞争力得分无数据空态 | 契约空结果 | — | 未覆盖 | 父控未试调，无稳定「合法 codes 无得分」构造证据 |
| L27 \| entan.competitiveness.score \| _fail \| 综合竞争力得分计算失败 | 契约错误态 | API-00077、00078、00079、00080 | 已覆盖 | 缺必填、空集合、非法编码、类型错误 |
| L27 \| entan.competitiveness.ranking \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00081、00082、00083、00084 | 契约占位 / 入参异常 | 鉴权见 API-00076 |
| L27 \| entan.competitiveness.ranking \| enterprises \| 算法输出-enterprises企业竞争力排名集 | catalog enterprises | API-00081 | 契约占位 | 排名语义待 endpoint 可用后补排序断言 |
| L27 \| entan.competitiveness.ranking \| _empty \| 综合竞争力排名无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造 |
| L27 \| entan.competitiveness.ranking \| _fail \| 综合竞争力排名计算失败 | 契约错误态 | API-00082、00083、00084 | 已覆盖 | 缺必填、空集合、非法编码 |
| L27 \| （无 endpoint） \| etl_clean_standardize \| 多源企业数据标准化清洗 | 需规（1）采集清洗 | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| quad_dimension_indicator_weights \| 四维度指标与权重设定 | 需规指标体系 | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| sz_national_compare_weighted \| 深全国指标对比加权整合 | 需规对比加权 | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| four_dimension_strength_weakness \| 四维优短板系统化分析 | 需规优短板分析 | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| dynamic_monitor_refresh \| 动态监测与自动更新 | 需规动态监测 | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| index_strength_weakness_report \| 竞争力指数与优短板报告输出 | 需规（2）指数与报告 | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| competitiveness_ranking_semantics \| 竞争力排名语义 | 需规（2）排名 | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| trend_change_monitor \| 趋势变化监测语义 | 需规（2）趋势图表 | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| name_industry_region_query_scope \| 企业名称行业区域查询语义 | 需规（3）多维筛选 | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| api_sdk_invocation \| RestfulAPI 与 SDK 调用 | 需规（3）API/SDK | — | 未覆盖 | req_only |
| L27 \| （无 endpoint） \| analysis_report_export \| 分析报告与数据导出 | 需规（3）导出 | — | 未覆盖 | req_only |

---

## 3. 覆盖统计

| 维度 | 计数 |
|------|------|
| A 线表行（L27） | **19** |
| 有 endpoint 的 field 行 | **8** |
| 已覆盖 / 契约占位 | **6**（enterprises×2 契约占位；enterprise_codes×2；_fail×2） |
| 未覆盖（_empty×2 + req_only×11） | **13** |
| API 用例数 | **10** |

---

## 4. B 线独有

| 说明 |
|------|
| 无（本页 endpoint 均已在 L27 登记） |
