# 区域科技创新成果综合评价 · 功能点覆盖（comp.tech-outcome / L51）

> catalog `comp.tech-outcome` · 50897 · path `#/industry-comp/tech-outcome`  
> 用例 `API-区域科技创新成果综合评价-用例.md`  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json`（页 `comp.tech-outcome`）  
> 功能点键：`L51 | endpoint_id | field_key | 功能点中文`（矩阵键与 A 线 by-api 对齐）  
> 编排：`algo-lib-api-case-playbook.md` §编写细则 H、§I  

> **path 独占**：`GET /comp/v1/comp/region-tech-outcome` 为本页独占；与同模块 `region-industry-outcome` 等其它 outcome path 禁止混抄预期。

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| comp.tech-outcome.main | GET | /comp/v1/comp/region-tech-outcome | API-00654～00658 | catalog `unavailable`；§0 **未试调**；本批 **金样 5 条**；非 kind 套餐 |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L51 \| comp.tech-outcome.main \| region \| 算法输入-region区域标签 | catalog region | API-00654、00656 | 已覆盖 | 主路径占位 + 非法 region |
| L51 \| comp.tech-outcome.main \| year \| 算法输入-year年份 | catalog year | API-00654、00657 | 已覆盖 | 主路径占位 + 非法 year |
| L51 \| comp.tech-outcome.main \| index \| 算法输出-index科技创新成果指数 | catalog index | API-00658 | 部分覆盖 | unavailable 金样批仅写字段形态；live 成功数值语义待升档补 |
| L51 \| comp.tech-outcome.main \| rows \| 算法输出-rows区域明细行集 | catalog rows | API-00658 | 部分覆盖 | 同上（array 形态） |
| L51 \| comp.tech-outcome.main \| _empty \| 科技成果评价无数据空态 | 契约空结果 | — | **未覆盖** | 无稳定空态构造；§0 未试调 |
| L51 \| comp.tech-outcome.main \| _fail \| 科技成果评价查询失败 | 契约错误态 | API-00655、00656、00657 | 已覆盖 | 鉴权、非法 region、非法 year |
| L51 \| comp.tech-outcome.main \| etl_clean_standardize \| 技术专题库多源成果清洗标准化 | 需规（1）采集预处理 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| three_dim_indicators_threshold \| 三维成果指标体系与阈值权重 | 需规指标体系阈值 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| standardize_weight_synthesis \| 指标标准化与加权综合指数 | 需规加权综合 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| strength_weakness_identify \| 优势领域与短板识别 | 需规优短板 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| trend_forecast_report \| 趋势分析与趋势预测报告 | 需规（2）趋势报告 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| policy_resource_allocation_advice \| 政策与资源配置建议 | 需规（2）政策建议 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| composite_eval_detail_outputs \| 综合评价结果与详细指标 | 需规（2）综合与明细 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| region_outcome_type_time_scope \| 区域标签成果类型时间查询语义 | 需规（3）调用范围 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| continuous_monitor_year_refresh \| 持续监测与年份结果刷新 | 需规持续监测 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| index_rows_report_advice_outputs \| 指数明细趋势建议多类输出 | 需规（2）多类输出 | — | 无对应功能点 | req_only |
| L51 \| comp.tech-outcome.main \| api_sdk_tech_decision_platform \| API SDK 与科技管理平台对接 | 需规（3）系统对接 | — | 无对应功能点 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖（可测 API field / 哨兵） | 4（region、year、_fail；index/rows 形态部分） |
| 未覆盖（契约 field / _empty） | 2（index/rows live 语义、_empty） |
| 无对应功能点（req_only） | 11 |
| API 用例条数 | 5（00654～00658） |
| 金样 | API-00654 |

---

## 4. §I 计数

| 项 | 值 |
|----|-----|
| FUNC | 0 |
| API | 5 |
| 金样 | API-00654 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
