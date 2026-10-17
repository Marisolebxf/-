# 企业供应链关系分析 · 功能点覆盖（entan.supply-chain / L30）

> catalog `entan.supply-chain` · 50897 · path `/entan/supply-chain`  
> **用例册**：`API-企业供应链关系分析-用例.md`（`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00105`～`00109`，共 **5** 条）  
> A 线范围：**L30**（`fp-split-by-api-run/work/L30.md`）  
> 功能点键：`L30 | endpoint_id | field_key | 功能点中文`  
> 编排：`algo-lib-api-case-playbook.md` §S1  

---

## 1. endpoint → 用例

| endpoint_id | METHOD | path | 对应用例 | 备注 |
|-------------|--------|------|----------|------|
| entan.supply-chain.risk | POST | /entan/v1/entan/metric/M_ENT_SUPPLY_CHAIN_RISK/compute | API-00105～00109 | catalog `status=unavailable` |

---

## 2. 功能点 → 用例（主矩阵）

| 功能点键 | 规则来源 | 对应用例 | 状态 | 说明 |
|----------|----------|----------|------|------|
| L30 \| entan.supply-chain.risk \| enterprise_codes \| 算法输入-enterprise_codes企业编码集合 | catalog enterprise_codes | API-00106、00107、00108 | 部分覆盖 | 缺省/空集合/非法；live 合法集合成功校验待 endpoint available 后补 |
| L30 \| entan.supply-chain.risk \| break_risks \| 算法输出-break_risks断链风险结果体 | catalog break_risks | API-00105 | 契约占位 | unavailable，禁止 sample 风险等级/节点名作为通过条件 |
| L30 \| entan.supply-chain.risk \| _empty \| 断链风险无数据空态 | 契约空结果 | — | 未覆盖 | endpoint unavailable，无稳定「合法非空集合必空」试调证据 |
| L30 \| entan.supply-chain.risk \| _fail \| 断链风险计算失败 | 契约错误态 | API-00105、00106、00107、00108 | 已覆盖 | 含 catalog 不可用与入参失败哨兵 |
| L30 \| （无 endpoint） \| etl_clean_standardize \| 图谱关系与专题数据标准化清洗 | 需规（1）采集清洗 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| supply_chain_network_build \| 供应链网络网络化构建 | 需规网络化构建 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| graph_position_importance \| 图论位置与重要性判定 | 需规图论分析 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| graph_algorithm_params \| 图论算法参数设定 | 需规输入图论参数 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| supply_chain_structure_metrics \| 供应链结构五类指标计算 | 需规指标计算阶段 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| distribution_structure_features \| 分布特征与结构特点揭示 | 需规结构揭示 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| break_chain_risk_metric_compute \| 断链风险指标计算语义 | 需规风险量化 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| dynamic_supply_chain_refresh \| 供应链关系动态更新 | 需规动态更新 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| supply_chain_network_graph_semantic \| 供应链网络结构图输出语义 | 需规（2）网络结构图 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| position_importance_report \| 位置与重要性分析报告 | 需规（2）分析报告 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| map_topology_viz \| 地图或拓扑可视化展示 | 需规（2）可视化 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| enterprise_id_name_query_scope \| 企业标识或名称查询语义 | 需规（3）调用方式 | — | 未覆盖 | req_only |
| L30 \| （无 endpoint） \| online_monitor_report_export \| 在线监测与报告图表导出 | 需规（3）API/SDK | — | 未覆盖 | req_only |

---

## 3. 统计

| 状态 | 条数 |
|------|------|
| 已覆盖 | 1（`_fail` 契约行） |
| 部分覆盖 | 1（`enterprise_codes`） |
| 契约占位 | 1（`break_risks`） |
| 未覆盖 | 14（含 `_empty` 1 + req_only 13） |

---

## 4. B 线交卷摘要

| 项 | 值 |
|----|-----|
| API 用例条数 | 5 |
| 编号 | API-00105～API-00109 |
| `_empty` 未覆盖 | 1 |
| 试调 | **未试调**（§0；金样执行期复核信封） |
| FUNC 条数 | 0 |
