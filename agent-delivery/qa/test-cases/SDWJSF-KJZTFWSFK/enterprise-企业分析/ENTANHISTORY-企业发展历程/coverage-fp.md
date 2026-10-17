# 企业发展历程 · 功能点覆盖（entan.history / L28）

> catalog `entan.history` · 50897 · path `#/entan/history`  
> **用例册**：`API-企业发展历程-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00085`～`00094`，共 **10** 条）  
> A 线范围：**L28**（`fp-split-by-api-run/work/L28.md`）  
> 功能点键：`L28 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.history.enterprises | GET | /entan/v1/enterprises | API-00085～00089、00094 | unavailable |
| entan.history.timeline | GET | /entan/v1/history | API-00090～00093 | unavailable |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L28 \| entan.history.enterprises \| keyword \| 算法输入-keyword关键词 | catalog keyword | API-00087、00089 | 契约占位 | endpoint unavailable；空 keyword 见 ENT-04 |
| L28 \| entan.history.enterprises \| limit \| 算法输入-limit条数上限 | catalog limit | API-00087、00088、00094 | 契约占位 | 非法/越界见 ENT-03、ENT-05 |
| L28 \| entan.history.enterprises \| org_id \| 算法输出-org_id企业标识 | catalog org_id | API-00085、00087 | 契约占位 | 禁止 sample org_id 作通过条件 |
| L28 \| entan.history.enterprises \| enterprise_name \| 算法输出-enterprise_name企业名称 | catalog enterprise_name | API-00085、00087 | 契约占位 | 禁止样例企业名称作通过条件 |
| L28 \| entan.history.enterprises \| _empty \| 企业搜索无匹配空态 | 契约空结果 | API-00089 | 契约占位 | 与空 keyword/无匹配合并验收，未试调无稳定必空条件 |
| L28 \| entan.history.enterprises \| _fail \| 企业搜索查询失败 | 契约错误态 | API-00088、00094 | 契约占位 | 非法 limit、越界 limit |
| L28 \| entan.history.timeline \| org_id \| 算法输入-org_id企业标识 | catalog org_id | API-00090、00091、00092、00093 | 契约占位 | 缺必填、非法 id |
| L28 \| entan.history.timeline \| timeline \| 算法输出-timeline重大事件时间线 | catalog timeline | API-00090、00093 | 契约占位 | 仅断言字段形态，不写样例事件数值 |
| L28 \| entan.history.timeline \| _empty \| 发展历程无数据空态 | 契约空结果 | API-00090、00093 | 契约占位 | unavailable 无 live 空态构造，与契约合并 |
| L28 \| entan.history.timeline \| _fail \| 发展历程查询失败 | 契约错误态 | API-00091、00092 | 契约占位 | 缺 org_id、非法 org_id |
| L28 \| （无 endpoint） \| etl_clean_standardize \| 多源运营与舆情标准化清洗 | 需规（1）采集清洗 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| event_indicator_threshold \| 基础资讯与重大事件指标阈值 | 需规指标体系阈值 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| event_identification_detect \| 超阈值重大事件识别 | 需规事件识别 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| major_event_type_detection \| 并购上市等类型事件检测 | 需规事件类型 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| evolution_path_semantics \| 演化路径与战略节点语义 | 需规历程视图 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| dynamic_timeline_refresh \| 历程动态监测与新事件标识 | 需规动态监测 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| major_event_list_semantics \| 重大事件列表语义 | 需规（2）事件列表 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| history_viz_view \| 发展历程可视化视图 | 需规（2）可视化 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| analysis_report \| 发展历程分析报告 | 需规（2）分析报告 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| api_result_sync \| API 结果服务化同步 | 需规（3）API | — | 未覆盖 | req_only（本册 API 用例覆盖 catalog 两 endpoint 契约，不重复挂本行） |
| L28 \| （无 endpoint） \| sdk_report_chart_export \| SDK 调用与报告图表导出 | 需规（3）SDK导出 | — | 未覆盖 | req_only |

---

## 3. 计数摘要

| 项 | 数量 |
|----|------|
| A 线 catalog 挂接行（含 _empty/_fail） | **10** |
| 契约占位（两 endpoint 全字段） | **10** |
| req_only 未覆盖 | **11** |
| 用例条数 | **10**（API-00085～00094） |
| FUNC | **0** |
| 金样 | **1**（API-00085，完整信封） |
| 试调 | **未试调**（§0） |

---

## 4. B 线独有

| 说明 | 对应用例 |
|------|----------|
| 全页异常-鉴权（enterprise 侧代表） | API-00086 |
