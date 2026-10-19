# 科技创新评估 · A 线功能点覆盖（innov.tech-evaluation）

> **catalog_page_id**：`innov.tech-evaluation` · path `/innov/tech-evaluation`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-科技创新评估-用例.md`（第二轮 **API-01902**～**01976**，共 75 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.tech-evaluation`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.tech-evaluation.metrics | GET | /innov/v1/innov/metrics | API-01902、API-01903、API-01904 | unavailable |
| innov.tech-evaluation.m_innov_pg_composite | POST | /innov/v1/innov/metric/M_INNOV_PG_COMPOSITE/compute | API-01905、API-01906、API-01907 | available |
| innov.tech-evaluation.m_innov_pg_guide | POST | /innov/v1/innov/metric/M_INNOV_PG_GUIDE/compute | API-01908、API-01909、API-01910 | available |
| innov.tech-evaluation.m_innov_pot_composite | POST | /innov/v1/innov/metric/M_INNOV_POT_COMPOSITE/compute | API-01911、API-01912、API-01913 | available |
| innov.tech-evaluation.m_innov_pot_maturity | POST | /innov/v1/innov/metric/M_INNOV_POT_MATURITY/compute | API-01914、API-01915、API-01916 | available |
| innov.tech-evaluation.m_innov_pot_sci_infl | POST | /innov/v1/innov/metric/M_INNOV_POT_SCI_INFL/compute | API-01917、API-01918、API-01919 | available |
| innov.tech-evaluation.m_innov_pot_tech_infl | POST | /innov/v1/innov/metric/M_INNOV_POT_TECH_INFL/compute | API-01920、API-01921、API-01922 | available |
| innov.tech-evaluation.m_innov_tinn_composite | POST | /innov/v1/innov/metric/M_INNOV_TINN_COMPOSITE/compute | API-01923、API-01924、API-01925 | available |
| innov.tech-evaluation.m_innov_tinn_forecast | POST | /innov/v1/innov/metric/M_INNOV_TINN_FORECAST/compute | API-01926、API-01927、API-01928 | available |
| innov.tech-evaluation.m_innov_tinn_market | POST | /innov/v1/innov/metric/M_INNOV_TINN_MARKET/compute | API-01929、API-01930、API-01931 | available |
| innov.tech-evaluation.m_innov_tinn_patent_quality | POST | /innov/v1/innov/metric/M_INNOV_TINN_PATENT_QUALITY/compute | API-01932、API-01933、API-01934 | available |
| innov.tech-evaluation.m_innov_ds_07_sci_create_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_07_SCI_CREATE_004/compute | API-01935、API-01936、API-01937 | available |
| innov.tech-evaluation.m_innov_sci_forecast | POST | /innov/v1/innov/metric/M_INNOV_SCI_FORECAST/compute | API-01938、API-01939、API-01940 | available |
| innov.tech-evaluation.m_innov_sci_frontier | POST | /innov/v1/innov/metric/M_INNOV_SCI_FRONTIER/compute | API-01941、API-01942、API-01943 | available |
| innov.tech-evaluation.m_innov_pg_effect | POST | /innov/v1/innov/metric/M_INNOV_PG_EFFECT/compute | API-01944、API-01945、API-01946 | available |
| innov.tech-evaluation.m_innov_pg_intensity | POST | /innov/v1/innov/metric/M_INNOV_PG_INTENSITY/compute | API-01947、API-01948、API-01949 | available |
| innov.tech-evaluation.m_innov_sci_centrality | POST | /innov/v1/innov/metric/M_INNOV_SCI_CENTRALITY/compute | API-01950、API-01951、API-01952 | available |
| innov.tech-evaluation.m_innov_keyd_competitiveness | POST | /innov/v1/innov/metric/M_INNOV_KEYD_COMPETITIVENESS/compute | API-01953、API-01954、API-01955 | available |
| innov.tech-evaluation.m_innov_keyd_potential | POST | /innov/v1/innov/metric/M_INNOV_KEYD_POTENTIAL/compute | API-01956、API-01957、API-01958 | available |
| innov.tech-evaluation.m_innov_plan_growth | POST | /innov/v1/innov/metric/M_INNOV_PLAN_GROWTH/compute | API-01959、API-01960、API-01961 | available |
| innov.tech-evaluation.m_innov_plan_heat | POST | /innov/v1/innov/metric/M_INNOV_PLAN_HEAT/compute | API-01962、API-01963、API-01964 | available |
| innov.tech-evaluation.m_innov_res_ci_compare | POST | /innov/v1/innov/metric/M_INNOV_RES_CI_COMPARE/compute | API-01965、API-01966、API-01967 | available |
| innov.tech-evaluation.m_tech_ds_07_tech_innov_002 | POST | /innov/v1/innov/metric/M_TECH_DS_07_TECH_INNOV_002/compute | API-01968、API-01969、API-01970 | available |
| innov.tech-evaluation.m_tech_ds_07_tech_innov_004 | POST | /innov/v1/innov/metric/M_TECH_DS_07_TECH_INNOV_004/compute | API-01971、API-01972、API-01973 | available |
| innov.tech-evaluation.m_tech_ds_07_tech_innov_006 | POST | /innov/v1/innov/metric/M_TECH_DS_07_TECH_INNOV_006/compute | API-01974、API-01975、API-01976 | available |

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传 `module` 挂备选；`module` 恰好 1 条非法反向。同名 title 按 endpoint_id 分行。GET metrics 的 catalog `status=unavailable`，备注注明未交付。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.tech-evaluation.metrics \| 科技创新评估指标清单 | API-01902、API-01903、API-01904 | 无对应功能点 | 01902 主流程 sampleRequest（module=tech-evaluation），断言 metrics 元素 metric_id、name、algorithm_type、formula_status、pending_ref 与 total=24；01903 不传 module；01904 非法 module。catalog status=unavailable |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pg_composite \| 政策与条件保障力综合评估 | API-01905、API-01906、API-01907 | 无对应功能点 | 01905 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PG_COMPOSITE、hint，以及 responseFields 的 metrics、total；01906 不传 module；01907 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pg_guide \| 发展战略引导力 | API-01908、API-01909、API-01910 | 无对应功能点 | 01908 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PG_GUIDE、hint，以及 responseFields 的 metrics、total；01909 不传 module；01910 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pot_composite \| 产业发展潜力综合评估 | API-01911、API-01912、API-01913 | 无对应功能点 | 01911 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_POT_COMPOSITE、hint，以及 responseFields 的 metrics、total；01912 不传 module；01913 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pot_maturity \| 技术产品成熟度 | API-01914、API-01915、API-01916 | 无对应功能点 | 01914 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_POT_MATURITY、hint，以及 responseFields 的 metrics、total；01915 不传 module；01916 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pot_sci_infl \| 产业科学影响力 | API-01917、API-01918、API-01919 | 无对应功能点 | 01917 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_POT_SCI_INFL、hint，以及 responseFields 的 metrics、total；01918 不传 module；01919 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pot_tech_infl \| 产业技术影响力 | API-01920、API-01921、API-01922 | 无对应功能点 | 01920 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_POT_TECH_INFL、hint，以及 responseFields 的 metrics、total；01921 不传 module；01922 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_tinn_composite \| 技术创新力综合评估 | API-01923、API-01924、API-01925 | 无对应功能点 | 01923 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_TINN_COMPOSITE、hint，以及 responseFields 的 metrics、total；01924 不传 module；01925 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_tinn_forecast \| 技术创新趋势预测 | API-01926、API-01927、API-01928 | 无对应功能点 | 01926 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_TINN_FORECAST、hint，以及 responseFields 的 metrics、total；01927 不传 module；01928 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_tinn_market \| 技术市场潜力 | API-01929、API-01930、API-01931 | 无对应功能点 | 01929 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_TINN_MARKET、hint，以及 responseFields 的 metrics、total；01930 不传 module；01931 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_tinn_patent_quality \| 专利质量 | API-01932、API-01933、API-01934 | 无对应功能点 | 01932 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_TINN_PATENT_QUALITY、hint，以及 responseFields 的 metrics、total；01933 不传 module；01934 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_ds_07_sci_create_004 \| 科学创造力趋势预测 | API-01935、API-01936、API-01937 | 无对应功能点 | 01935 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_DS_07_SCI_CREATE_004、hint，以及 responseFields 的 metrics、total；01936 不传 module；01937 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_sci_forecast \| 科学创造力趋势预测 | API-01938、API-01939、API-01940 | 无对应功能点 | 01938 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_SCI_FORECAST、hint，以及 responseFields 的 metrics、total；01939 不传 module；01940 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_sci_frontier \| 科学研究前沿性 | API-01941、API-01942、API-01943 | 无对应功能点 | 01941 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_SCI_FRONTIER、hint，以及 responseFields 的 metrics、total；01942 不传 module；01943 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pg_effect \| 政策实施效果 | API-01944、API-01945、API-01946 | 无对应功能点 | 01944 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PG_EFFECT、hint，以及 responseFields 的 metrics、total；01945 不传 module；01946 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_pg_intensity \| 政策扶持力度 | API-01947、API-01948、API-01949 | 无对应功能点 | 01947 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PG_INTENSITY、hint，以及 responseFields 的 metrics、total；01948 不传 module；01949 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_sci_centrality \| 科学网络中心性 | API-01950、API-01951、API-01952 | 无对应功能点 | 01950 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_SCI_CENTRALITY、hint，以及 responseFields 的 metrics、total；01951 不传 module；01952 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_keyd_competitiveness \| 区域科技创新竞争力水平 | API-01953、API-01954、API-01955 | 无对应功能点 | 01953 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_KEYD_COMPETITIVENESS、hint，以及 responseFields 的 metrics、total；01954 不传 module；01955 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_keyd_potential \| 区域科技创新发展潜力 | API-01956、API-01957、API-01958 | 无对应功能点 | 01956 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_KEYD_POTENTIAL、hint，以及 responseFields 的 metrics、total；01957 不传 module；01958 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_plan_growth \| 增长速度 | API-01959、API-01960、API-01961 | 无对应功能点 | 01959 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PLAN_GROWTH、hint，以及 responseFields 的 metrics、total；01960 不传 module；01961 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_plan_heat \| 热度指数 | API-01962、API-01963、API-01964 | 无对应功能点 | 01962 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_PLAN_HEAT、hint，以及 responseFields 的 metrics、total；01963 不传 module；01964 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_innov_res_ci_compare \| 多企业竞争情报比对 | API-01965、API-01966、API-01967 | 无对应功能点 | 01965 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_INNOV_RES_CI_COMPARE、hint，以及 responseFields 的 metrics、total；01966 不传 module；01967 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_tech_ds_07_tech_innov_002 \| 专利质量评估 | API-01968、API-01969、API-01970 | 无对应功能点 | 01968 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_TECH_DS_07_TECH_INNOV_002、hint，以及 responseFields 的 metrics、total；01969 不传 module；01970 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_tech_ds_07_tech_innov_004 \| 技术创新力综合评估 | API-01971、API-01972、API-01973 | 无对应功能点 | 01971 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_TECH_DS_07_TECH_INNOV_004、hint，以及 responseFields 的 metrics、total；01972 不传 module；01973 非法 module |
| （无 Lxx） \| innov.tech-evaluation.m_tech_ds_07_tech_innov_006 \| 技术创新趋势预测 | API-01974、API-01975、API-01976 | 无对应功能点 | 01974 主流程 sampleRequest（module=tech-evaluation），断言 metric_id=M_TECH_DS_07_TECH_INNOV_006、hint，以及 responseFields 的 metrics、total；01975 不传 module；01976 非法 module |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 25 |
| title 数 | 25（同名不合并） |
| API 用例数 | 75 |
| 主流程 | 25 |
| 备选-参数组合 | 25（均不传 module） |
| 反向 | 25（均非法 module） |
| 编号 | API-01902～01976 连续 |
| A 线 Lxx | 无 |

