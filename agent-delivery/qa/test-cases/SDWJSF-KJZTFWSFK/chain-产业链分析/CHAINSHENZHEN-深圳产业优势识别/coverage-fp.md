# 深圳产业优势识别 · 功能点覆盖（chain.shenzhen / L18）

> catalog `chain.shenzhen` · path `#/chain/shenzhen`  
> A 线真源：`fp-split-by-api-run/work/L18.md`  
> B 线用例：`API-深圳产业优势识别-用例.md`（第二轮 **API-01280**～**01283**，已删除）  
> C 线用例：`FUNC-深圳产业优势识别-用例.md`（第三轮 **FUNC-00481**～**00486**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | API 用例 | FUNC 用例 | catalog status |
|-------------|--------|------|----------|-----------|----------------|
| chain.shenzhen.main | GET | /innov/v1/industry/{chainId}/shenzhen | API-01280、01281 | FUNC-00481、00482 | unavailable |
| chain.shenzhen.m_chain_deep_121_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_121_1/compute | API-01282、01283 | FUNC-00483、00484 | available |

---

## 功能点 → 用例矩阵（挂 L18.md）

多条 field 挂同一用例。不按 field 另开用例。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L18 \| chain.shenzhen.main \| chainId \| 算法输入-chainId产业标识 | API-01280、01281；FUNC-00481、00482 | 已覆盖 | 合法 path chainId=INB170101 + 缺 chainId；规则来源 catalog chainId |
| L18 \| chain.shenzhen.main \| panorama.enterprise_count \| 算法输出-panorama.enterprise_count深圳企业数 | API-01280；FUNC-00481 | 已覆盖 | 主流程按 sampleResponse 断言 panorama.enterprise_count（number，responseFields 深圳企业数）；规则来源 catalog panorama.enterprise_count |
| L18 \| chain.shenzhen.main \| panorama.nodes \| 算法输出-panorama.nodes深圳环节节点 | API-01280；FUNC-00481 | 已覆盖 | 同条主流程断言 panorama.nodes（array，元素含 node_name、position、enterprise_count）；规则来源 catalog panorama.nodes |
| L18 \| chain.shenzhen.main \| _empty \| 深圳优势识别无数据空态 | — | 未覆盖 | 无稳定「合法 chainId 且 panorama 为空」构造条件；规则来源 契约空结果 |
| L18 \| chain.shenzhen.main \| _fail \| 深圳优势识别查询失败 | API-01281；FUNC-00482 | 部分覆盖 | 仅缺 chainId 反向（message/msg 指出缺少 chainId）；规则来源 契约错误态 |

---

## req_only 行（无 endpoint 挂接）

L18.md 中下列 field 的 endpoint_id 为空、`catalog_status=req_only`，catalog 无对应入参或 responseFields。B/C 线记 **无对应功能点**，不单独开 API 用例：

`etl_clean_standardize`（深全国产业数据清洗一致化）、`advantage_indicator_threshold`（优势评价指标与权重阈值）、`sz_national_compare_score`（深全国对比优势评分）、`advantage_domain_identify`（优势产业领域锁定）、`advantage_industry_list`（深圳优势产业清单）、`advantage_score_detail`（优势评分与详细指标）、`indicator_analysis_report`（详细指标分析报告）、`trend_visual_chart_data`（趋势变化可视化图表数据）、`scheduled_refresh_monitor`（持续监测与动态更新）、`industry_tag_report_export`（产业标签与报告导出）。

---

## B/C 线独有（catalog 有、L18 未挂 endpoint）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L18 \| chain.shenzhen.m_chain_deep_121_1 \| — \| 深圳产业优势识别模型 | API-01282、01283；FUNC-00483、00484 | 无对应功能点 | 下拉 title 仍写主流程（metric_id、hint）与缺 chainId；L18 未给该 endpoint 挂 field 行 |
| （页面清单）接口信息 / 算法测试 | FUNC-00485、00486 | 无对应功能点 | 联调台 tab 与 catalog 下拉一致性 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 2 |
| title 数 | 2 |
| API 用例数 | 4（API-01280～01283，册已删保留号段） |
| FUNC 用例数 | 6（FUNC-00481～00486） |
| FUNC 主流程 | 2（00481 深圳产业优势识别、00483 深圳产业优势识别模型） |
| FUNC 反向 | 2（00482、00484，均为缺 chainId） |
| FUNC 清单 | 2（00485 接口信息、00486 算法测试） |
| 编号 | FUNC-00481～00486 |
| L18 挂接行 | 5（已覆盖 3、部分覆盖 1、未覆盖 1） |
| L18 req_only | 10（无对应功能点） |
