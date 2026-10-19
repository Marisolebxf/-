# 第一波 16 STAT（ADS）· A 线功能点覆盖（chain.wave1）

> **catalog_page_id**：`chain.wave1` · path `/chain/wave1`  
> **A 线**：**无对应 Lxx**。该页不在 60 六级挂接表。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 Lxx `pages` 与 `catalog_skip` 均无 `chain.wave1`。不改 `work/`。  
> **用例册**：`API-第一波16STAT-用例.md`（第二轮 **API-01157**～**01219**，共 63 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.wave1`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| chain.wave1.m_chain_total_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_TOTAL_COUNT/compute | API-01157、API-01158、API-01159 | available |
| chain.wave1.m_chain_enterprise_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_ENTERPRISE_COUNT/compute | API-01160、API-01161、API-01162 | available |
| chain.wave1.m_chain_enterprise_new_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_ENTERPRISE_NEW_COUNT/compute | API-01163、API-01164、API-01165 | available |
| chain.wave1.m_chain_national_region_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_NATIONAL_REGION_COUNT/compute | API-01166、API-01167、API-01168 | available |
| chain.wave1.m_chain_sz_region_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_REGION_COUNT/compute | API-01169、API-01170、API-01171 | available |
| chain.wave1.m_chain_sz_enterprise_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_ENTERPRISE_COUNT/compute | API-01172、API-01173、API-01174 | available |
| chain.wave1.m_chain_sz_enterprise_ratio | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_ENTERPRISE_RATIO/compute | API-01175、API-01176、API-01177 | available |
| chain.wave1.m_chain_market_size | POST | /innov/v1/industry/chainan/metric/M_CHAIN_MARKET_SIZE/compute | API-01178、API-01179、API-01180 | available |
| chain.wave1.m_chain_market_growth | POST | /innov/v1/industry/chainan/metric/M_CHAIN_MARKET_GROWTH/compute | API-01181、API-01182、API-01183 | available |
| chain.wave1.m_chain_invest_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_INVEST_COUNT/compute | API-01184、API-01185、API-01186 | available |
| chain.wave1.m_chain_reg_financing | POST | /innov/v1/industry/chainan/metric/M_CHAIN_REG_FINANCING/compute | API-01187、API-01188、API-01189 | available |
| chain.wave1.m_chain_reg_revenue | POST | /innov/v1/industry/chainan/metric/M_CHAIN_REG_REVENUE/compute | API-01190、API-01191、API-01192 | available |
| chain.wave1.m_chain_reg_patent | POST | /innov/v1/industry/chainan/metric/M_CHAIN_REG_PATENT/compute | API-01193、API-01194、API-01195 | available |
| chain.wave1.m_chain_sz_completeness | POST | /innov/v1/industry/chainan/metric/M_CHAIN_SZ_COMPLETENESS/compute | API-01196、API-01197、API-01198 | available |
| chain.wave1.m_chain_patent_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_PATENT_COUNT/compute | API-01199、API-01200、API-01201 | available |
| chain.wave1.m_chain_product_count | POST | /innov/v1/industry/chainan/metric/M_CHAIN_PRODUCT_COUNT/compute | API-01202、API-01203、API-01204 | available |
| chain.topic-panorama.m_chain_global_case_match | POST | /innov/v1/industry/chainan/metric/M_CHAIN_GLOBAL_CASE_MATCH/compute | API-01205、API-01206、API-01207、API-01208、API-01209、API-01210、API-01211、API-01212、API-01213、API-01214、API-01215、API-01216、API-01217、API-01218、API-01219 | available |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse（含嵌套）与 responseFields 多出字段都挂在该接口主流程上；可选参数的相反传/不传挂备选；每个参数恰好 1 条反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| chain.wave1.m_chain_total_count \| WAVE1 产业链环节总数 | API-01157、API-01158、API-01159 | 无对应功能点 | 01157 主流程空 body；01158 传入 chain_id；01159 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_enterprise_count \| WAVE1 链上企业数 | API-01160、API-01161、API-01162 | 无对应功能点 | 01160 主流程空 body；01161 传入 chain_id；01162 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_enterprise_new_count \| WAVE1 链上新增企业数 | API-01163、API-01164、API-01165 | 无对应功能点 | 01163 主流程空 body；01164 传入 chain_id；01165 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_national_region_count \| WAVE1 全国区域企业分布 | API-01166、API-01167、API-01168 | 无对应功能点 | 01166 主流程空 body；01167 传入 chain_id；01168 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_sz_region_count \| WAVE1 深圳区域企业分布 | API-01169、API-01170、API-01171 | 无对应功能点 | 01169 主流程空 body；01170 传入 chain_id；01171 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_sz_enterprise_count \| WAVE1 深圳企业数 | API-01172、API-01173、API-01174 | 无对应功能点 | 01172 主流程空 body；01173 传入 chain_id；01174 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_sz_enterprise_ratio \| WAVE1 深圳企业占比 | API-01175、API-01176、API-01177 | 无对应功能点 | 01175 主流程空 body；01176 传入 chain_id；01177 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_market_size \| WAVE1 产业市场规模 | API-01178、API-01179、API-01180 | 无对应功能点 | 01178 主流程空 body；01179 传入 chain_id；01180 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_market_growth \| WAVE1 产业市场增速 | API-01181、API-01182、API-01183 | 无对应功能点 | 01181 主流程空 body；01182 传入 chain_id；01183 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_invest_count \| WAVE1 投融资事件数 | API-01184、API-01185、API-01186 | 无对应功能点 | 01184 主流程空 body；01185 传入 chain_id；01186 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_reg_financing \| WAVE1 区域融资分布 | API-01187、API-01188、API-01189 | 无对应功能点 | 01187 主流程空 body；01188 传入 chain_id；01189 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_reg_revenue \| WAVE1 区域营收分布 | API-01190、API-01191、API-01192 | 无对应功能点 | 01190 主流程空 body；01191 传入 chain_id；01192 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_reg_patent \| WAVE1 区域专利分布 | API-01193、API-01194、API-01195 | 无对应功能点 | 01193 主流程空 body；01194 传入 chain_id；01195 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_sz_completeness \| WAVE1 深圳产业链完备度 | API-01196、API-01197、API-01198 | 无对应功能点 | 01196 主流程空 body；01197 传入 chain_id；01198 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_patent_count \| WAVE1 链上专利数 | API-01199、API-01200、API-01201 | 无对应功能点 | 01199 主流程空 body；01200 传入 chain_id；01201 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.wave1.m_chain_product_count \| WAVE1 链上产品数 | API-01202、API-01203、API-01204 | 无对应功能点 | 01202 主流程空 body；01203 传入 chain_id；01204 非法 chain_id。sampleResponse 字段挂主流程 |
| （无 Lxx） \| chain.topic-panorama.m_chain_global_case_match \| 全球成功案例匹配 | API-01205、API-01206、API-01207、API-01208、API-01209、API-01210、API-01211、API-01212、API-01213、API-01214、API-01215、API-01216、API-01217、API-01218、API-01219 | 无对应功能点 | 01205 主流程 sampleRequest；01206～01211 六个可选参数与 sample 相反；01212～01213 缺 op_id/scope；01214～01219 可选参数非法。sampleResponse 与 responseFields 挂主流程 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 17 |
| title 数 | 17 |
| API 用例数 | 63 |
| 主流程 | 17 |
| 备选-参数组合 | 22 |
| 反向 | 24 |
| 编号 | API-01157～01219 连续 |
| A 线 Lxx | 无 |

