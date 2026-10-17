# 企业技术力评估 · 功能点覆盖（entan.tech / L31）

> catalog `entan.tech` · 50897 · path `/entan/tech`  
> **用例册**：`API-企业技术力评估-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00110`～`00125`，共 **16** 条）  
> A 线范围：**L31**（`fp-split-by-api-run/work/L31.md`）  
> 功能点键：`L31 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.tech.rank | POST | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | API-00110～00114、00122、00125 | catalog `status=unavailable` |
| entan.tech.detail | GET | /entan/v1/tech-power/{orgId} | API-00115、00116、00123 | catalog `status=unavailable` |
| entan.tech.weights | GET | /entan/v1/eval/weights | API-00117～00119、00124 | catalog `status=unavailable` |
| entan.tech.report | GET | /entan/v1/enterprises/{orgId}/report | API-00120、00121 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L31 \| entan.tech.rank \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00111、00112、00113、00114 | 部分覆盖 | 缺省/空集合/非法/类型；live 合法集合成功校验待 endpoint available 后补 |
| L31 \| entan.tech.rank \| enterprises \| 算法输出-enterprises企业技术力结果集 | catalog enterprises | API-00110、00125 | 契约占位 | unavailable，禁止 sample 指数数值作通过条件 |
| L31 \| entan.tech.rank \| _empty \| 技术力得分无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable，无稳定「合法非空集合必空」试调证据 |
| L31 \| entan.tech.rank \| _fail \| 技术力得分计算失败 | 契约错误态 | API-00110、00111、00112、00113、00114 | 已覆盖 | 含 catalog 不可用与入参失败哨兵 |
| L31 \| entan.tech.detail \| orgId \| 算法输入-orgId企业标识 | catalog orgId | API-00116、00123 | 部分覆盖 | 非法与格式异常；live 合法 orgId 成功校验待 available 后补 |
| L31 \| entan.tech.detail \| talent_score \| 算法输出-talent_score人才维度得分 | catalog talent_score | API-00115 | 契约占位 | unavailable |
| L31 \| entan.tech.detail \| trend \| 算法输出-trend技术力趋势 | catalog trend | API-00115 | 契约占位 | 同上 |
| L31 \| entan.tech.detail \| _empty \| 技术力详情无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| L31 \| entan.tech.detail \| _fail \| 技术力详情查询失败 | 契约错误态 | API-00115、00116、00123 | 已覆盖 | |
| L31 \| entan.tech.weights \| model \| 算法输入-model模型标识 | catalog model | API-00118、00119、00124 | 部分覆盖 | 缺省/非法/未知 model |
| L31 \| entan.tech.weights \| weight \| 算法输出-weight权重配置 | catalog weight | API-00117 | 契约占位 | unavailable |
| L31 \| entan.tech.weights \| _empty \| 模型权重无数据空态 | 契约空结果 | — | 未覆盖 | 无试调证据区分空 weight 与失败 |
| L31 \| entan.tech.weights \| _fail \| 模型权重查询失败 | 契约错误态 | API-00117、00118、00119、00124 | 已覆盖 | |
| L31 \| entan.tech.report \| orgId \| 算法输入-orgId企业标识 | catalog orgId | API-00121 | 部分覆盖 | 非法 orgId |
| L31 \| entan.tech.report \| markdown \| 算法输出-markdown评估报告正文 | catalog markdown | API-00120 | 契约占位 | unavailable |
| L31 \| entan.tech.report \| _empty \| 评估报告无数据空态 | 契约空结果 | — | 未覆盖 | 同上 |
| L31 \| entan.tech.report \| _fail \| 评估报告生成失败 | 契约错误态 | API-00120、00121 | 已覆盖 | |
| L31 \| （无 endpoint） \| etl_clean_standardize \| 多源专利项目研发与合作数据标准化清洗 | 需规（1）采集清洗 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| five_dimension_indicator_threshold \| 五维度核心指标与判定阈值 | 需规指标体系 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| tech_power_model_train_optimize \| 技术力评估模型训练与优化 | 需规模型训练 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| weighted_tech_power_index \| 加权综合技术力指数计算 | 需规加权综合 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| dimension_tech_power_analysis \| 各维度技术力分项分析 | 需规维度分析 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| strength_weakness_analysis \| 优势与短板分析语义 | 需规优短板 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| improvement_suggestion_generate \| 改进建议生成 | 需规改进建议 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| dynamic_tech_power_refresh \| 持续监测与自动更新 | 需规动态监测 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| benchmark_assessment_semantics \| 对标评估语义 | 需规对标 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| enterprise_id_name_query_scope \| 企业标识或名称评估语义 | 需规（3）调用方式 | — | 未覆盖 | req_only |
| L31 \| （无 endpoint） \| viz_report_data_export \| 可视化报告与数据导出 | 需规（3）API/SDK导出 | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 4（四 endpoint `_fail` 契约行） |
| 部分覆盖 | 4（enterprise_codes、orgId×2、model） |
| 契约占位 | 5（enterprises、talent_score、trend、weight、markdown） |
| 未覆盖 | 15（含 `_empty` 4 + req_only 11） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 16 |
| 编号 | API-00110～API-00125 |
| `_empty` 未覆盖 | 4 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
| FUNC 条数 | 0 |
