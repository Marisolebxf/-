# 科技创新评估 · A 线功能点覆盖（innov.tech-evaluation）

> **catalog_page_id**：`innov.tech-evaluation` · path `/innov/tech-evaluation`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-科技创新评估-用例.md`（第三轮 **FUNC-01176**～**01252**，共 77 条；旧 API-01902～01976 作废）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.tech-evaluation`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.tech-evaluation.metrics | GET | /innov/v1/innov/metrics | FUNC-01176、FUNC-01177、FUNC-01178 | unavailable |
| innov.tech-evaluation.m_innov_pg_composite | POST | /innov/v1/innov/metric/M_INNOV_PG_COMPOSITE/compute | FUNC-01179、FUNC-01180、FUNC-01181 | available |
| innov.tech-evaluation.m_innov_pg_guide | POST | /innov/v1/innov/metric/M_INNOV_PG_GUIDE/compute | FUNC-01182、FUNC-01183、FUNC-01184 | available |
| innov.tech-evaluation.m_innov_pot_composite | POST | /innov/v1/innov/metric/M_INNOV_POT_COMPOSITE/compute | FUNC-01185、FUNC-01186、FUNC-01187 | available |
| innov.tech-evaluation.m_innov_pot_maturity | POST | /innov/v1/innov/metric/M_INNOV_POT_MATURITY/compute | FUNC-01188、FUNC-01189、FUNC-01190 | available |
| innov.tech-evaluation.m_innov_pot_sci_infl | POST | /innov/v1/innov/metric/M_INNOV_POT_SCI_INFL/compute | FUNC-01191、FUNC-01192、FUNC-01193 | available |
| innov.tech-evaluation.m_innov_pot_tech_infl | POST | /innov/v1/innov/metric/M_INNOV_POT_TECH_INFL/compute | FUNC-01194、FUNC-01195、FUNC-01196 | available |
| innov.tech-evaluation.m_innov_tinn_composite | POST | /innov/v1/innov/metric/M_INNOV_TINN_COMPOSITE/compute | FUNC-01197、FUNC-01198、FUNC-01199 | available |
| innov.tech-evaluation.m_innov_tinn_forecast | POST | /innov/v1/innov/metric/M_INNOV_TINN_FORECAST/compute | FUNC-01200、FUNC-01201、FUNC-01202 | available |
| innov.tech-evaluation.m_innov_tinn_market | POST | /innov/v1/innov/metric/M_INNOV_TINN_MARKET/compute | FUNC-01203、FUNC-01204、FUNC-01205 | available |
| innov.tech-evaluation.m_innov_tinn_patent_quality | POST | /innov/v1/innov/metric/M_INNOV_TINN_PATENT_QUALITY/compute | FUNC-01206、FUNC-01207、FUNC-01208 | available |
| innov.tech-evaluation.m_innov_ds_07_sci_create_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_07_SCI_CREATE_004/compute | FUNC-01209、FUNC-01210、FUNC-01211 | available |
| innov.tech-evaluation.m_innov_sci_forecast | POST | /innov/v1/innov/metric/M_INNOV_SCI_FORECAST/compute | FUNC-01212、FUNC-01213、FUNC-01214 | available |
| innov.tech-evaluation.m_innov_sci_frontier | POST | /innov/v1/innov/metric/M_INNOV_SCI_FRONTIER/compute | FUNC-01215、FUNC-01216、FUNC-01217 | available |
| innov.tech-evaluation.m_innov_pg_effect | POST | /innov/v1/innov/metric/M_INNOV_PG_EFFECT/compute | FUNC-01218、FUNC-01219、FUNC-01220 | available |
| innov.tech-evaluation.m_innov_pg_intensity | POST | /innov/v1/innov/metric/M_INNOV_PG_INTENSITY/compute | FUNC-01221、FUNC-01222、FUNC-01223 | available |
| innov.tech-evaluation.m_innov_sci_centrality | POST | /innov/v1/innov/metric/M_INNOV_SCI_CENTRALITY/compute | FUNC-01224、FUNC-01225、FUNC-01226 | available |
| innov.tech-evaluation.m_innov_keyd_competitiveness | POST | /innov/v1/innov/metric/M_INNOV_KEYD_COMPETITIVENESS/compute | FUNC-01227、FUNC-01228、FUNC-01229 | available |
| innov.tech-evaluation.m_innov_keyd_potential | POST | /innov/v1/innov/metric/M_INNOV_KEYD_POTENTIAL/compute | FUNC-01230、FUNC-01231、FUNC-01232 | available |
| innov.tech-evaluation.m_innov_plan_growth | POST | /innov/v1/innov/metric/M_INNOV_PLAN_GROWTH/compute | FUNC-01233、FUNC-01234、FUNC-01235 | available |
| innov.tech-evaluation.m_innov_plan_heat | POST | /innov/v1/innov/metric/M_INNOV_PLAN_HEAT/compute | FUNC-01236、FUNC-01237、FUNC-01238 | available |
| innov.tech-evaluation.m_innov_res_ci_compare | POST | /innov/v1/innov/metric/M_INNOV_RES_CI_COMPARE/compute | FUNC-01239、FUNC-01240、FUNC-01241 | available |
| innov.tech-evaluation.m_tech_ds_07_tech_innov_002 | POST | /innov/v1/innov/metric/M_TECH_DS_07_TECH_INNOV_002/compute | FUNC-01242、FUNC-01243、FUNC-01244 | available |
| innov.tech-evaluation.m_tech_ds_07_tech_innov_004 | POST | /innov/v1/innov/metric/M_TECH_DS_07_TECH_INNOV_004/compute | FUNC-01245、FUNC-01246、FUNC-01247 | available |
| innov.tech-evaluation.m_tech_ds_07_tech_innov_006 | POST | /innov/v1/innov/metric/M_TECH_DS_07_TECH_INNOV_006/compute | FUNC-01248、FUNC-01249、FUNC-01250 | available |

页面清单：**FUNC-01251**（接口信息）、**FUNC-01252**（算法测试）。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传 `module` 挂备选；`module` 恰好 1 条非法反向。同名 title 按 endpoint_id 分行。GET metrics 的 catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.tech-evaluation.metrics \| 科技创新评估指标清单 | FUNC-01176、FUNC-01177、FUNC-01178 | 无对应功能点 | 01176 主流程 sampleRequest（module=tech-evaluation，金样 MET-01），断言 metrics 元素 metric_id、name、algorithm_type、formula_status、pending_ref 与 total=24；01177 不传 module；01178 非法 module。catalog status=unavailable |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pg_composite \| 政策与条件保障力综合评估 | FUNC-01179、FUNC-01180、FUNC-01181 | 无对应功能点 | 01179 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PG_COMPOSITE、hint，以及 responseFields 的 metrics、total；01180 不传 module；01181 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pg_guide \| 发展战略引导力 | FUNC-01182、FUNC-01183、FUNC-01184 | 无对应功能点 | 01182 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PG_GUIDE、hint，以及 responseFields 的 metrics、total；01183 不传 module；01184 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pot_composite \| 产业发展潜力综合评估 | FUNC-01185、FUNC-01186、FUNC-01187 | 无对应功能点 | 01185 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_POT_COMPOSITE、hint，以及 responseFields 的 metrics、total；01186 不传 module；01187 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pot_maturity \| 技术产品成熟度 | FUNC-01188、FUNC-01189、FUNC-01190 | 无对应功能点 | 01188 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_POT_MATURITY、hint，以及 responseFields 的 metrics、total；01189 不传 module；01190 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pot_sci_infl \| 产业科学影响力 | FUNC-01191、FUNC-01192、FUNC-01193 | 无对应功能点 | 01191 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_POT_SCI_INFL、hint，以及 responseFields 的 metrics、total；01192 不传 module；01193 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pot_tech_infl \| 产业技术影响力 | FUNC-01194、FUNC-01195、FUNC-01196 | 无对应功能点 | 01194 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_POT_TECH_INFL、hint，以及 responseFields 的 metrics、total；01195 不传 module；01196 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_tinn_composite \| 技术创新力综合评估 | FUNC-01197、FUNC-01198、FUNC-01199 | 无对应功能点 | 01197 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_TINN_COMPOSITE、hint，以及 responseFields 的 metrics、total；01198 不传 module；01199 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_tinn_forecast \| 技术创新趋势预测 | FUNC-01200、FUNC-01201、FUNC-01202 | 无对应功能点 | 01200 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_TINN_FORECAST、hint，以及 responseFields 的 metrics、total；01201 不传 module；01202 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_tinn_market \| 技术市场潜力 | FUNC-01203、FUNC-01204、FUNC-01205 | 无对应功能点 | 01203 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_TINN_MARKET、hint，以及 responseFields 的 metrics、total；01204 不传 module；01205 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_tinn_patent_quality \| 专利质量 | FUNC-01206、FUNC-01207、FUNC-01208 | 无对应功能点 | 01206 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_TINN_PATENT_QUALITY、hint，以及 responseFields 的 metrics、total；01207 不传 module；01208 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_ds_07_sci_create_004 \| 科学创造力趋势预测 | FUNC-01209、FUNC-01210、FUNC-01211 | 无对应功能点 | 01209 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_DS_07_SCI_CREATE_004、hint，以及 responseFields 的 metrics、total；01210 不传 module；01211 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_sci_forecast \| 科学创造力趋势预测 | FUNC-01212、FUNC-01213、FUNC-01214 | 无对应功能点 | 01212 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_SCI_FORECAST、hint，以及 responseFields 的 metrics、total；01213 不传 module；01214 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_sci_frontier \| 科学研究前沿性 | FUNC-01215、FUNC-01216、FUNC-01217 | 无对应功能点 | 01215 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_SCI_FRONTIER、hint，以及 responseFields 的 metrics、total；01216 不传 module；01217 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pg_effect \| 政策实施效果 | FUNC-01218、FUNC-01219、FUNC-01220 | 无对应功能点 | 01218 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PG_EFFECT、hint，以及 responseFields 的 metrics、total；01219 不传 module；01220 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pg_intensity \| 政策扶持力度 | FUNC-01221、FUNC-01222、FUNC-01223 | 无对应功能点 | 01221 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PG_INTENSITY、hint，以及 responseFields 的 metrics、total；01222 不传 module；01223 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_sci_centrality \| 科学网络中心性 | FUNC-01224、FUNC-01225、FUNC-01226 | 无对应功能点 | 01224 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_SCI_CENTRALITY、hint，以及 responseFields 的 metrics、total；01225 不传 module；01226 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_keyd_competitiveness \| 区域科技创新竞争力水平 | FUNC-01227、FUNC-01228、FUNC-01229 | 无对应功能点 | 01227 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_KEYD_COMPETITIVENESS、hint，以及 responseFields 的 metrics、total；01228 不传 module；01229 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_keyd_potential \| 区域科技创新发展潜力 | FUNC-01230、FUNC-01231、FUNC-01232 | 无对应功能点 | 01230 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_KEYD_POTENTIAL、hint，以及 responseFields 的 metrics、total；01231 不传 module；01232 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_plan_growth \| 增长速度 | FUNC-01233、FUNC-01234、FUNC-01235 | 无对应功能点 | 01233 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PLAN_GROWTH、hint，以及 responseFields 的 metrics、total；01234 不传 module；01235 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_plan_heat \| 热度指数 | FUNC-01236、FUNC-01237、FUNC-01238 | 无对应功能点 | 01236 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PLAN_HEAT、hint，以及 responseFields 的 metrics、total；01237 不传 module；01238 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_res_ci_compare \| 多企业竞争情报比对 | FUNC-01239、FUNC-01240、FUNC-01241 | 无对应功能点 | 01239 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_RES_CI_COMPARE、hint，以及 responseFields 的 metrics、total；01240 不传 module；01241 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_tech_ds_07_tech_innov_002 \| 专利质量评估 | FUNC-01242、FUNC-01243、FUNC-01244 | 无对应功能点 | 01242 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_TECH_DS_07_TECH_INNOV_002、hint，以及 responseFields 的 metrics、total；01243 不传 module；01244 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_tech_ds_07_tech_innov_004 \| 技术创新力综合评估 | FUNC-01245、FUNC-01246、FUNC-01247 | 无对应功能点 | 01245 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_TECH_DS_07_TECH_INNOV_004、hint，以及 responseFields 的 metrics、total；01246 不传 module；01247 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_tech_ds_07_tech_innov_006 \| 技术创新趋势预测 | FUNC-01248、FUNC-01249、FUNC-01250 | 无对应功能点 | 01248 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_TECH_DS_07_TECH_INNOV_006、hint，以及 responseFields 的 metrics、total；01249 不传 module；01250 非法 module |
| （页面清单） | FUNC-01251、FUNC-01252 | 无对应功能点 | 二十五接口页接口信息 / 算法测试 tab 清单 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 25 |
| title 数 | 25（同名不合并） |
| FUNC 用例数 | 77 |
| 主流程 | 25 |
| 备选-参数组合 | 25（均不传 module） |
| 反向 | 25（均非法 module） |
| 清单 | 2（01251、01252） |
| 编号 | FUNC-01176～01252 连续 |
| A 线 Lxx | 无 |
| 金样 | FUNC-01176（MET-01） |
