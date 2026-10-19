# 企业供应链关系分析 · 功能点覆盖（entan.supply-chain / L30）

> catalog `entan.supply-chain` · path `#/entan/supply-chain`  
> A 线真源：`fp-split-by-api-run/work/L30.md`  
> B 线用例：`API-企业供应链关系分析-用例.md`（第二轮 **API-00964**～**00965**）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| entan.supply-chain.risk | POST | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute | API-00964、00965 | unavailable |

---

## 功能点 → 用例矩阵（挂 L30.md）

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| L30 \| entan.supply-chain.risk \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | API-00964、00965 | 已覆盖 | 规则来源 catalog enterprise_codes；合法全参 + 缺 enterprise_codes |
| L30 \| entan.supply-chain.risk \| break_risks \| 算法输出-break_risks断链风险结果体 | API-00964 | 已覆盖 | 规则来源 catalog break_risks；主流程断言 value.result.break_risks 及子字段 |
| L30 \| entan.supply-chain.risk \| _empty \| 断链风险无数据空态 | — | 未覆盖 | 规则来源 契约空结果；无稳定空结果构造条件 |
| L30 \| entan.supply-chain.risk \| _fail \| 断链风险计算失败 | API-00965 | 部分覆盖 | 规则来源 契约错误态；仅缺 enterprise_codes 反向 |
| L30 \| （无 endpoint） \| etl_clean_standardize \| 图谱关系与专题数据标准化清洗 | — | 未覆盖 | 规则来源 需规（1）采集清洗；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| supply_chain_network_build \| 供应链网络网络化构建 | — | 未覆盖 | 规则来源 需规网络化构建；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| graph_position_importance \| 图论位置与重要性判定 | — | 未覆盖 | 规则来源 需规图论分析；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| graph_algorithm_params \| 图论算法参数设定 | — | 未覆盖 | 规则来源 需规输入图论参数；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| supply_chain_structure_metrics \| 供应链结构五类指标计算 | — | 未覆盖 | 规则来源 需规指标计算阶段；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| distribution_structure_features \| 分布特征与结构特点揭示 | — | 未覆盖 | 规则来源 需规结构揭示；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| break_chain_risk_metric_compute \| 断链风险指标计算语义 | — | 未覆盖 | 规则来源 需规风险量化；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| dynamic_supply_chain_refresh \| 供应链关系动态更新 | — | 未覆盖 | 规则来源 需规动态更新；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| supply_chain_network_graph_semantic \| 供应链网络结构图输出语义 | — | 未覆盖 | 规则来源 需规（2）网络结构图；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| position_importance_report \| 位置与重要性分析报告 | — | 未覆盖 | 规则来源 需规（2）分析报告；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| map_topology_viz \| 地图或拓扑可视化展示 | — | 未覆盖 | 规则来源 需规（2）可视化；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| enterprise_id_name_query_scope \| 企业标识或名称查询语义 | — | 未覆盖 | 规则来源 需规（3）调用方式；req_only，无对应功能点 |
| L30 \| （无 endpoint） \| online_monitor_report_export \| 在线监测与报告图表导出 | — | 未覆盖 | 规则来源 需规（3）API/SDK；req_only，无对应功能点 |

---

## req_only 行（无 endpoint 挂接）

L30.md 中 `etl_clean_standardize`、`supply_chain_network_build`、`graph_position_importance`、`graph_algorithm_params`、`supply_chain_structure_metrics`、`distribution_structure_features`、`break_chain_risk_metric_compute`、`dynamic_supply_chain_refresh`、`supply_chain_network_graph_semantic`、`position_importance_report`、`map_topology_viz`、`enterprise_id_name_query_scope`、`online_monitor_report_export` 共 **13** 条 **req_only** 无 catalog endpoint，B 线记 **无对应功能点**，不单独开 API 用例。
