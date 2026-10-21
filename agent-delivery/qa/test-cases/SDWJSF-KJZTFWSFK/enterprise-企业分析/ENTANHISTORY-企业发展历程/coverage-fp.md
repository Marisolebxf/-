# 企业发展历程 · 功能点覆盖（entan.history / L28）

> catalog `entan.history` · 联调台 `https://edu.itic-sci.com/dma/algovwz/` · path `#/entan/history`  
> **用例册**：`FUNC-企业发展历程-用例.md`（第三轮 **`FUNC-00108`～`00116`**，共 **9** 条；旧 API-00949～00955 作废）  
> A 线范围：**L28**（`fp-split-by-api-run/work/L28.md`）  
> 功能点键：`L28 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.history.enterprises | GET | /entan/v1/enterprises | FUNC-00108～00111 | unavailable；正向按 sampleResponse |
| entan.history.timeline | GET | /entan/v1/history | FUNC-00112～00114 | unavailable；正向按 sampleResponse |
| （页面清单） | — | — | FUNC-00115、00116 | — |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L28 \| entan.history.enterprises \| keyword \| 算法输入-keyword关键词 | catalog keyword | FUNC-00108、00109、00111 | 已覆盖 | 主/备选正向 + 非法 keyword 反向 |
| L28 \| entan.history.enterprises \| limit \| 算法输入-limit条数上限 | catalog limit | FUNC-00108、00109、00110 | 已覆盖 | 主/备选正向 + 非法 limit 反向 |
| L28 \| entan.history.enterprises \| org_id \| 算法输出-org_id企业标识 | catalog org_id | FUNC-00108、00109 | 已覆盖 | 正向预期含 string 型 org_id 字段形态 |
| L28 \| entan.history.enterprises \| enterprise_name \| 算法输出-enterprise_name企业名称 | catalog enterprise_name | FUNC-00108、00109 | 已覆盖 | 正向预期含 string 型 enterprise_name |
| L28 \| entan.history.enterprises \| _empty \| 企业搜索无匹配空态 | 契约空结果 | FUNC-00108、00109 | 部分覆盖 | 正向允许空数组；无单独 keyword 必空构造 |
| L28 \| entan.history.enterprises \| _fail \| 企业搜索查询失败 | 契约错误态 | FUNC-00110、00111 | 已覆盖 | limit/keyword 单参数反向 |
| L28 \| entan.history.timeline \| org_id \| 算法输入-org_id企业标识 | catalog org_id | FUNC-00112、00113、00114 | 已覆盖 | 主流程 + 缺/非法反向 |
| L28 \| entan.history.timeline \| timeline \| 算法输出-timeline重大事件时间线 | catalog timeline | FUNC-00112 | 已覆盖 | array 及 year/type/title/detail 形态 |
| L28 \| entan.history.timeline \| _empty \| 发展历程无数据空态 | 契约空结果 | FUNC-00112 | 部分覆盖 | 主流程预期允许 timeline 空数组 |
| L28 \| entan.history.timeline \| _fail \| 发展历程查询失败 | 契约错误态 | FUNC-00113、00114 | 已覆盖 | 缺 org_id、非法 org_id |
| L28 \| （无 endpoint） \| etl_clean_standardize \| 多源运营与舆情标准化清洗 | 需规（1）采集清洗 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| event_indicator_threshold \| 基础资讯与重大事件指标阈值 | 需规指标体系阈值 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| event_identification_detect \| 超阈值重大事件识别 | 需规事件识别 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| major_event_type_detection \| 并购上市等类型事件检测 | 需规事件类型 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| evolution_path_semantics \| 演化路径与战略节点语义 | 需规历程视图 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| dynamic_timeline_refresh \| 历程动态监测与新事件标识 | 需规动态监测 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| major_event_list_semantics \| 重大事件列表语义 | 需规（2）事件列表 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| history_viz_view \| 发展历程可视化视图 | 需规（2）可视化 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| analysis_report \| 发展历程分析报告 | 需规（2）分析报告 | — | 未覆盖 | req_only |
| L28 \| （无 endpoint） \| api_result_sync \| API 结果服务化同步 | 需规（3）API | — | 未覆盖 | req_only（catalog 两 endpoint 由本册 FUNC 覆盖） |
| L28 \| （无 endpoint） \| sdk_report_chart_export \| SDK 调用与报告图表导出 | 需规（3）SDK导出 | — | 未覆盖 | req_only |

---

## 3. 计数摘要

| 项 | 数量 |
|----|------|
| A 线 catalog 挂接行（含 _empty/_fail） | **10** |
| 已覆盖 / 部分覆盖（catalog 行） | **8** / **2** |
| req_only 未覆盖 | **11** |
| 用例条数 | **9**（FUNC-00108～00116） |
| 鉴权用例 | **0** |
| 试调 | **未试调**（S1 编写期） |

---

## 4. B 线独有

| 说明 | 对应用例 |
|------|----------|
| 联调台接口信息/算法测试 tab 清单 | FUNC-00115、00116 |
