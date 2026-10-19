# 湾区创新监测 · A 线功能点覆盖（innov.bay-area-monitoring）

> **catalog_page_id**：`innov.bay-area-monitoring` · path `/innov/bay-area-monitoring`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-湾区创新监测-用例.md`（第二轮 **API-02142**～**02192**，共 51 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.bay-area-monitoring`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.bay-area-monitoring.metrics | GET | /innov/v1/innov/metrics | API-02142、API-02143、API-02144 | unavailable |
| innov.bay-area-monitoring.m_innov_gba_capacity_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_CAPACITY_INDEX/compute | API-02145、API-02146、API-02147 | available |
| innov.bay-area-monitoring.m_innov_gba_env_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_ENV_INDEX/compute | API-02148、API-02149、API-02150 | available |
| innov.bay-area-monitoring.m_innov_gba_hotspot | POST | /innov/v1/innov/metric/M_INNOV_GBA_HOTSPOT/compute | API-02151、API-02152、API-02153 | available |
| innov.bay-area-monitoring.m_innov_gba_mech_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_MECH_INDEX/compute | API-02154、API-02155、API-02156 | available |
| innov.bay-area-monitoring.m_innov_gba_org_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_ORG_INDEX/compute | API-02157、API-02158、API-02159 | available |
| innov.bay-area-monitoring.m_innov_gba_res_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_RES_INDEX/compute | API-02160、API-02161、API-02162 | available |
| innov.bay-area-monitoring.m_innov_gba_subindex_contrib | POST | /innov/v1/innov/metric/M_INNOV_GBA_SUBINDEX_CONTRIB/compute | API-02163、API-02164、API-02165 | available |
| innov.bay-area-monitoring.m_innov_gba_swot_opportunity | POST | /innov/v1/innov/metric/M_INNOV_GBA_SWOT_OPPORTUNITY/compute | API-02166、API-02167、API-02168 | available |
| innov.bay-area-monitoring.m_innov_gba_swot_strength | POST | /innov/v1/innov/metric/M_INNOV_GBA_SWOT_STRENGTH/compute | API-02169、API-02170、API-02171 | available |
| innov.bay-area-monitoring.m_innov_gba_swot_threat | POST | /innov/v1/innov/metric/M_INNOV_GBA_SWOT_THREAT/compute | API-02172、API-02173、API-02174 | available |
| innov.bay-area-monitoring.m_innov_gba_swot_weakness | POST | /innov/v1/innov/metric/M_INNOV_GBA_SWOT_WEAKNESS/compute | API-02175、API-02176、API-02177 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_achieve_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ACHIEVE_004/compute | API-02178、API-02179、API-02180 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ANALYSIS_003/compute | API-02181、API-02182、API-02183 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ANALYSIS_004/compute | API-02184、API-02185、API-02186 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_005 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ANALYSIS_005/compute | API-02187、API-02188、API-02189 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_006 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ANALYSIS_006/compute | API-02190、API-02191、API-02192 | available |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传 `module` 挂备选；`module` 恰好 1 条非法反向。GET metrics 的 catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.bay-area-monitoring.metrics \| 湾区创新监测指标清单 | API-02142、API-02143、API-02144 | 无对应功能点 | 2142 主流程 sampleRequest（module=bay-area-monitoring），断言 metrics 元素 metric_id、name、algorithm_type、formula_status、pending_ref 与 total=16；2143 不传 module；2144 非法 module。catalog status=unavailable |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_capacity_index \| 粤港澳大湾区创新能力指标 | API-02145、API-02146、API-02147 | 无对应功能点 | 2145 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_CAPACITY_INDEX、hint，以及 responseFields 的 metrics、total；2146 不传 module；2147 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_env_index \| 创新环境指数 | API-02148、API-02149、API-02150 | 无对应功能点 | 2148 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_ENV_INDEX、hint，以及 responseFields 的 metrics、total；2149 不传 module；2150 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_hotspot \| 湾区创新热点区域 | API-02151、API-02152、API-02153 | 无对应功能点 | 2151 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_HOTSPOT、hint，以及 responseFields 的 metrics、total；2152 不传 module；2153 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_mech_index \| 创新机制指数 | API-02154、API-02155、API-02156 | 无对应功能点 | 2154 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_MECH_INDEX、hint，以及 responseFields 的 metrics、total；2155 不传 module；2156 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_org_index \| 创新机构指数 | API-02157、API-02158、API-02159 | 无对应功能点 | 2157 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_ORG_INDEX、hint，以及 responseFields 的 metrics、total；2158 不传 module；2159 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_res_index \| 创新资源指数 | API-02160、API-02161、API-02162 | 无对应功能点 | 2160 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_RES_INDEX、hint，以及 responseFields 的 metrics、total；2161 不传 module；2162 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_subindex_contrib \| 子指标贡献度 | API-02163、API-02164、API-02165 | 无对应功能点 | 2163 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_SUBINDEX_CONTRIB、hint，以及 responseFields 的 metrics、total；2164 不传 module；2165 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_swot_opportunity \| 湾区创新能力机会因素 | API-02166、API-02167、API-02168 | 无对应功能点 | 2166 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_SWOT_OPPORTUNITY、hint，以及 responseFields 的 metrics、total；2167 不传 module；2168 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_swot_strength \| 湾区创新能力优势因素 | API-02169、API-02170、API-02171 | 无对应功能点 | 2169 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_SWOT_STRENGTH、hint，以及 responseFields 的 metrics、total；2170 不传 module；2171 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_swot_threat \| 湾区创新能力威胁因素 | API-02172、API-02173、API-02174 | 无对应功能点 | 2172 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_SWOT_THREAT、hint，以及 responseFields 的 metrics、total；2173 不传 module；2174 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_gba_swot_weakness \| 湾区创新能力短板因素 | API-02175、API-02176、API-02177 | 无对应功能点 | 2175 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_GBA_SWOT_WEAKNESS、hint，以及 responseFields 的 metrics、total；2176 不传 module；2177 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_ds_05_gba_achieve_004 \| 创新热点区域识别 | API-02178、API-02179、API-02180 | 无对应功能点 | 2178 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_DS_05_GBA_ACHIEVE_004、hint，以及 responseFields 的 metrics、total；2179 不传 module；2180 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_003 \| 优势因素分析 | API-02181、API-02182、API-02183 | 无对应功能点 | 2181 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_DS_05_GBA_ANALYSIS_003、hint，以及 responseFields 的 metrics、total；2182 不传 module；2183 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_004 \| 短板因素分析 | API-02184、API-02185、API-02186 | 无对应功能点 | 2184 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_DS_05_GBA_ANALYSIS_004、hint，以及 responseFields 的 metrics、total；2185 不传 module；2186 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_005 \| 机会因素分析 | API-02187、API-02188、API-02189 | 无对应功能点 | 2187 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_DS_05_GBA_ANALYSIS_005、hint，以及 responseFields 的 metrics、total；2188 不传 module；2189 非法 module |
| （无 Lxx） \| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_006 \| 威胁因素分析 | API-02190、API-02191、API-02192 | 无对应功能点 | 2190 主流程 sampleRequest（module=bay-area-monitoring），断言 metric_id=M_INNOV_DS_05_GBA_ANALYSIS_006、hint，以及 responseFields 的 metrics、total；2191 不传 module；2192 非法 module |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 17 |
| title 数 | 17 |
| API 用例数 | 51 |
| 主流程 | 17 |
| 备选-参数组合 | 17（均不传 module） |
| 反向 | 17（均非法 module） |
| 编号 | API-02142～02192 连续 |
| A 线 Lxx | 无 |
