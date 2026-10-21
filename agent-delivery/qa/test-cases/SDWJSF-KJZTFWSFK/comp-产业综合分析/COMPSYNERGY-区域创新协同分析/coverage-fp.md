# 区域创新协同分析 · 功能点覆盖（comp.synergy / L60）

> catalog `comp.synergy` · path `#/industry-comp/synergy`  
> A 线真源：`fp-split-by-api-run/work/L60.md`（只读，未改 work）  
> **B 线用例**：`FUNC-区域创新协同分析-用例.md`（第三轮 **FUNC-01078**～**FUNC-01085**）  
> 契约：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.synergy`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

> **path 独占**：`GET /comp/v1/comp/innov-synergy` 为本页 title「创新协同」独占，与同模块 `region-vitality`、`element-synthesis` 等 path 分开验收。`POST /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute` 只挂 title「区域创新协同分析模型」。

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| comp.synergy.main | GET | /comp/v1/comp/innov-synergy | FUNC-01078～01080 | unavailable |
| comp.synergy.m_synth_191_1 | POST | /entan/v1/synth-metric/metric/M_SYNTH_191_1/compute | FUNC-01081～01083 | available |

---

## 功能点 → 用例矩阵（挂 L60.md）

同一 field_key 的多种场景挂在同一组 FUNC 号上，不按 field_key 各写一条用例。`创新协同` 的 sampleResponse 另有 `link`、`cross`、`effect`、`radar`（产学研 / 供应链 / 资本协同 / 跨城协同）、`bar_items`、`pie_items`、`rows`（元素 `name`、`score`、`rank`、`tag`、`note`），以及 nodes 元素 `id`、`node_key`、`name`、`node_type`、`weight`，edges 元素 `source`、`target`、`src_key`、`dst_key`、`relation`，已写入 01078、01079 正向预期；A 线未单列这些 field_key。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L60 \| comp.synergy.main \| region \| 算法输入-region区域标签 | catalog region | FUNC-01078、01079、01080 | 已覆盖 | 主路径 region=440300 + 省略可选 region + 非法 region=__invalid__ |
| L60 \| comp.synergy.main \| index \| 算法输出-index区域创新协同指数 | catalog index | FUNC-01078、01079 | 已覆盖 | 主流程与备选断言 index（number，示例 68.5）。文档标记未交付 |
| L60 \| comp.synergy.main \| nodes \| 算法输出-nodes创新网络节点 | catalog nodes | FUNC-01078、01079 | 已覆盖 | 主流程与备选断言 nodes 及 id、node_key、name、node_type、weight。文档标记未交付 |
| L60 \| comp.synergy.main \| edges \| 算法输出-edges合作关系边 | catalog edges | FUNC-01078、01079 | 已覆盖 | 主流程与备选断言 edges 及 source、target、src_key、dst_key、relation。文档标记未交付 |
| L60 \| comp.synergy.main \| _empty \| 创新协同无数据空态 | 契约空结果 | — | 未覆盖 | 无稳定空结果构造条件，不单开空态用例 |
| L60 \| comp.synergy.main \| _fail \| 创新协同查询失败 | 契约错误态 | FUNC-01080 | 部分覆盖 | 仅非法 region 的 message 或 msg；可选省略按备选正向，不把「不传」写成失败 |
| （页面清单） \| comp.synergy \| 接口信息 / 算法测试 | 联调台清单 | FUNC-01084、01085 | 已覆盖 | 双接口页清单 2 条 |

---

## req_only 行（无 endpoint 挂接）

L60.md 下列 12 行 **req_only**，无 catalog endpoint，B 线记 **无对应功能点**，不单独开 FUNC 用例。

| 功能点键 | 规则来源 | 对应用例编号 | 状态 | 说明 |
|----------|----------|--------------|------|------|
| L60 \| （req_only） \| etl_clean_standardize \| 多源合作关系采集与预处理 | 需规（1）采集预处理 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| innov_synergy_network_model \| 区域创新协同网络建模 | 需规（1）网络建模 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| completeness_centrality_density \| 完整度中心度密度三类指标 | 需规三类核心指标 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| weighted_calibrate_synthesis \| 综合加权与历史数据校准 | 需规（1）指数合成 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| structured_analysis_report \| 结构化分析报告输出 | 需规（2）分析报告 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| synergy_strength_weakness_diag \| 协同优势与不足诊断 | 需规（2）优劣势诊断 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| trend_change_analysis \| 趋势变化分析 | 需规（2）趋势分析 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| cross_region_longitudinal_semantics \| 横向对比与纵向趋势语义 | 需规（1）对比趋势 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| network_viz_semantics \| 创新网络可视化展示语义 | 需规调用展示 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| region_time_scope \| 区域标签与时间范围查询语义 | 需规（3）调用范围 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| auto_monitor_strategy_integration \| 自动化监测与策略生成对接 | 需规（3）系统对接监测 | — | 无对应功能点 | 不单开 FUNC 用例 |
| L60 \| （req_only） \| api_sdk_policy_platform \| API SDK 与政策规划平台集成 | 需规（3）API SDK | — | 无对应功能点 | 不单开 FUNC 用例 |

---

## B 线独有（A 线未列 field_key）

| endpoint_id | 对应用例编号 | 状态 | 说明 |
|-------------|--------------|------|------|
| comp.synergy.m_synth_191_1 | FUNC-01081～01083 | 无对应功能点 | L60 未列该 POST endpoint 的 field_key。01081 主流程 sampleRequest（region=440300），断言 metric_id、hint 与 responseFields 的 index、nodes、edges；01082 省略 region；01083 非法 region |

---

## 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 4（`region`、`index`、`nodes`、`edges`）+ 清单 2 |
| 部分覆盖 | 1（`_fail`） |
| 未覆盖 | 1（`_empty`） |
| req_only 无对应功能点 | 12 |
| B 线独有 endpoint | 1（`comp.synergy.m_synth_191_1`，3 条用例） |
| FUNC 用例条数 | **8**（01078～01085） |
| 主流程 | 2（01078 创新协同；01081 区域创新协同分析模型） |
| 备选 | 2（01079、01082 不传 region） |
| 反向 | 2（01080、01083 非法 region） |
| 清单 | 2（01084、01085） |
| 编号闭区间 | **FUNC-01078**～**FUNC-01085** |
| 金样 | FUNC-01078 |
