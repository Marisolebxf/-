# 深圳企业竞争力水平分析 · 功能点覆盖（entan.competitiveness / L27）

> catalog `entan.competitiveness` · 50897 · path `#/entan/competitiveness`  
> **用例册**：`API-深圳企业竞争力水平分析-用例.md`（第二轮 `ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00943`～`00948`，共 **6** 条）  
> A 线范围：**L27**（`fp-split-by-api-run/work/L27.md`）  
> 功能点键：`L27 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 A～I  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | status |
|-------------|--------|------|----------|--------|
| entan.competitiveness.score | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | API-00943、00944 | unavailable |
| entan.competitiveness.ranking | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | API-00945、00946 | unavailable |
| entan.competitiveness.score.m_ent_city_compare_topic | POST | /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute | API-00947、00948 | available |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L27 \| entan.competitiveness.score \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00943、00944 | 已覆盖 | 主流程 + 缺必填反向 |
| L27 \| entan.competitiveness.score \| enterprises \| 算法输出-enterprises企业竞争力结果集 | catalog enterprises | API-00943 | 已覆盖 | 正向预期写 value.enterprises 与契约 enterprises |
| L27 \| entan.competitiveness.score \| _empty \| 综合竞争力得分无数据空态 | 契约空结果 | — | 未覆盖 | 本轮 6 条配额未构造合法空结果场景 |
| L27 \| entan.competitiveness.score \| _fail \| 综合竞争力得分计算失败 | 契约错误态 | API-00944 | 部分覆盖 | 仅缺 enterprise_codes；空集合/非法/类型未单开 |
| L27 \| entan.competitiveness.ranking \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00945、00946 | 已覆盖 | 主流程 + 非法编码反向 |
| L27 \| entan.competitiveness.ranking \| enterprises \| 算法输出-enterprises企业竞争力排名集 | catalog enterprises | API-00945 | 已覆盖 | 排名排序语义执行期补强 |
| L27 \| entan.competitiveness.ranking \| _empty \| 综合竞争力排名无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| L27 \| entan.competitiveness.ranking \| _fail \| 综合竞争力排名计算失败 | 契约错误态 | API-00946 | 部分覆盖 | 仅非法 enterprise_codes |
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

## 3. B 线独有（catalog 有、L27 未列 endpoint）

| endpoint_id | 对应用例 | 状态 | 说明 |
|-------------|----------|------|------|
| entan.competitiveness.score.m_ent_city_compare_topic | API-00947、00948 | 已覆盖 | 主流程 + 缺 enterprise_codes；L27 矩阵无对应 field 行 |

---

## 4. 覆盖统计

| 维度 | 计数 |
|------|------|
| A 线表行（L27） | **19** |
| 有 endpoint 的 field 行 | **8** |
| 已覆盖 / 部分覆盖（API 挂接） | **6** 行（enterprise_codes×2、enterprises×2、_fail×2 部分） |
| 未覆盖（_empty×2 + req_only×11） | **13** |
| catalog endpoint 数 | **3** |
| API 用例数（本轮） | **6** |

---

## 5. 版本映射

| 轮次 | 用例编号 | 说明 |
|------|----------|------|
| 第一轮（作废） | API-00075～00084 | 鉴权/契约占位口径，不复用 |
| 第二轮 R2-批1 | API-00943～00948 | 本文件真源 |
