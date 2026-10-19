# 科技发展规划 · A 线功能点覆盖（innov.tech-planning）

> **catalog_page_id**：`innov.tech-planning` · path `/innov/tech-planning`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-科技发展规划-用例.md`（第二轮 **API-01977**～**02018**，共 42 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.tech-planning`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.tech-planning.metrics | GET | /innov/v1/innov/metrics | API-01977、API-01978、API-01979 | unavailable |
| innov.tech-planning.m_innov_plan_direction_alert | POST | /innov/v1/innov/metric/M_INNOV_PLAN_DIRECTION_ALERT/compute | API-01980、API-01981、API-01982 | available |
| innov.tech-planning.m_innov_plan_local_adv | POST | /innov/v1/innov/metric/M_INNOV_PLAN_LOCAL_ADV/compute | API-01983、API-01984、API-01985 | available |
| innov.tech-planning.m_innov_plan_talent_flow | POST | /innov/v1/innov/metric/M_INNOV_PLAN_TALENT_FLOW/compute | API-01986、API-01987、API-01988 | available |
| innov.tech-planning.m_innov_res_ci_level | POST | /innov/v1/innov/metric/M_INNOV_RES_CI_LEVEL/compute | API-01989、API-01990、API-01991 | available |
| innov.tech-planning.m_innov_res_grade | POST | /innov/v1/innov/metric/M_INNOV_RES_GRADE/compute | API-01992、API-01993、API-01994 | available |
| innov.tech-planning.m_innov_res_overlap | POST | /innov/v1/innov/metric/M_INNOV_RES_OVERLAP/compute | API-01995、API-01996、API-01997 | available |
| innov.tech-planning.m_innov_ds_09_comprehensive_005 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_COMPREHENSIVE_005/compute | API-01998、API-01999、API-02000 | available |
| innov.tech-planning.m_innov_ds_09_comprehensive_006 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_COMPREHENSIVE_006/compute | API-02001、API-02002、API-02003 | available |
| innov.tech-planning.m_innov_ds_09_comprehensive_008 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_COMPREHENSIVE_008/compute | API-02004、API-02005、API-02006 | available |
| innov.tech-planning.m_innov_ds_09_research_001 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_RESEARCH_001/compute | API-02007、API-02008、API-02009 | available |
| innov.tech-planning.m_innov_ds_09_research_002 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_RESEARCH_002/compute | API-02010、API-02011、API-02012 | available |
| innov.tech-planning.m_innov_ds_09_research_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_RESEARCH_003/compute | API-02013、API-02014、API-02015 | available |
| innov.tech-planning.m_innov_ds_09_research_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_RESEARCH_004/compute | API-02016、API-02017、API-02018 | available |

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。同名 title 按 endpoint 分列，不合并。每个接口的 sampleResponse 与 responseFields 都挂在该接口主流程上；与 sample 相反的不传可选 `module` 挂备选；`module` 恰好 1 条非法反向。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） · innov.tech-planning.metrics · 科技发展规划指标清单 | API-01977、API-01978、API-01979 | 无对应功能点 | API-01977 主流程 sampleRequest module=tech-planning，断言 data.metrics（元素 metric_id、name、algorithm_type、formula_status、pending_ref 共 13 行）与 total=13；API-01978 不传 module，结构同类；API-01979 非法 module=__invalid__。catalog status=unavailable，备注未交付 |
| （无 Lxx） · innov.tech-planning.m_innov_plan_direction_alert · 潜在科技发展方向预警 | API-01980、API-01981、API-01982 | 无对应功能点 | API-01980 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_PLAN_DIRECTION_ALERT、hint，以及 responseFields 声明的 metrics、total；API-01981 不传 module；API-01982 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_plan_local_adv · 本地科技创新特色与优势 | API-01983、API-01984、API-01985 | 无对应功能点 | API-01983 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_PLAN_LOCAL_ADV、hint，以及 responseFields 声明的 metrics、total；API-01984 不传 module；API-01985 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_plan_talent_flow · 科技人才流动（产业界↔学术界） | API-01986、API-01987、API-01988 | 无对应功能点 | API-01986 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_PLAN_TALENT_FLOW、hint，以及 responseFields 声明的 metrics、total；API-01987 不传 module；API-01988 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_res_ci_level · 竞争情报等级 | API-01989、API-01990、API-01991 | 无对应功能点 | API-01989 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_RES_CI_LEVEL、hint，以及 responseFields 声明的 metrics、total；API-01990 不传 module；API-01991 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_res_grade · 研究领域等级划分 | API-01992、API-01993、API-01994 | 无对应功能点 | API-01992 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_RES_GRADE、hint，以及 responseFields 声明的 metrics、total；API-01993 不传 module；API-01994 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_res_overlap · 研究领域重叠度 | API-01995、API-01996、API-01997 | 无对应功能点 | API-01995 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_RES_OVERLAP、hint，以及 responseFields 声明的 metrics、total；API-01996 不传 module；API-01997 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_comprehensive_005 · 本地特色与优势分析 | API-01998、API-01999、API-02000 | 无对应功能点 | API-01998 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_DS_09_COMPREHENSIVE_005、hint，以及 responseFields 声明的 metrics、total；API-01999 不传 module；API-02000 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_comprehensive_006 · 科技人才流动监控 | API-02001、API-02002、API-02003 | 无对应功能点 | API-02001 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_DS_09_COMPREHENSIVE_006、hint，以及 responseFields 声明的 metrics、total；API-02002 不传 module；API-02003 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_comprehensive_008 · 潜在科技发展方向预警 | API-02004、API-02005、API-02006 | 无对应功能点 | API-02004 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_DS_09_COMPREHENSIVE_008、hint，以及 responseFields 声明的 metrics、total；API-02005 不传 module；API-02006 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_research_001 · 研究领域重叠度 | API-02007、API-02008、API-02009 | 无对应功能点 | API-02007 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_DS_09_RESEARCH_001、hint，以及 responseFields 声明的 metrics、total；API-02008 不传 module；API-02009 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_research_002 · 研究领域等级划分 | API-02010、API-02011、API-02012 | 无对应功能点 | API-02010 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_DS_09_RESEARCH_002、hint，以及 responseFields 声明的 metrics、total；API-02011 不传 module；API-02012 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_research_003 · 竞争情报等级 | API-02013、API-02014、API-02015 | 无对应功能点 | API-02013 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_DS_09_RESEARCH_003、hint，以及 responseFields 声明的 metrics、total；API-02014 不传 module；API-02015 非法 module=__invalid__ |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_research_004 · 多企业竞争情报比对 | API-02016、API-02017、API-02018 | 无对应功能点 | API-02016 主流程 sampleRequest module=tech-planning，断言 metric_id=M_INNOV_DS_09_RESEARCH_004、hint，以及 responseFields 声明的 metrics、total；API-02017 不传 module；API-02018 非法 module=__invalid__ |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 14 |
| title 数 | 14（同名不合并） |
| API 用例数 | 42 |
| 主流程 | 14（API-01977、API-01980、API-01983、API-01986、API-01989、API-01992、API-01995、API-01998、API-02001、API-02004、API-02007、API-02010、API-02013、API-02016） |
| 备选-参数组合 | 14（API-01978、API-01981、API-01984、API-01987、API-01990、API-01993、API-01996、API-01999、API-02002、API-02005、API-02008、API-02011、API-02014、API-02017） |
| 反向 | 14（API-01979、API-01982、API-01985、API-01988、API-01991、API-01994、API-01997、API-02000、API-02003、API-02006、API-02009、API-02012、API-02015、API-02018） |
| 编号 | API-01977～02018 连续用满 |
| A 线 Lxx | 无 |
| 同名 title 主流程 | 潜在科技发展方向预警 API-01980 / API-02004；竞争情报等级 API-01989 / API-02013；研究领域等级划分 API-01992 / API-02010；研究领域重叠度 API-01995 / API-02007；多企业竞争情报比对 API-02016（本页仅 1 个 endpoint） |
