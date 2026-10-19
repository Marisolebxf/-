# 科技全域态势 · A 线功能点覆盖（innov.tech-landscape）

> **catalog_page_id**：`innov.tech-landscape` · path `/innov/tech-landscape`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`API-科技全域态势-用例.md`（第二轮 **API-02019**～**02063**，共 45 条）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.tech-landscape`  

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.tech-landscape.metrics | GET | /innov/v1/innov/metrics | API-02019～02021 | unavailable |
| innov.tech-landscape.m_innov_conference_influence | POST | /innov/v1/innov/metric/M_INNOV_CONFERENCE_INFLUENCE/compute | API-02022～02024 | available |
| innov.tech-landscape.m_innov_enterprise_influence | POST | /innov/v1/innov/metric/M_INNOV_ENTERPRISE_INFLUENCE/compute | API-02025～02027 | available |
| innov.tech-landscape.m_innov_event_attention | POST | /innov/v1/innov/metric/M_INNOV_EVENT_ATTENTION/compute | API-02028～02030 | available |
| innov.tech-landscape.m_innov_event_influence | POST | /innov/v1/innov/metric/M_INNOV_EVENT_INFLUENCE/compute | API-02031～02033 | available |
| innov.tech-landscape.m_innov_factor_anomaly | POST | /innov/v1/innov/metric/M_INNOV_FACTOR_ANOMALY/compute | API-02034～02036 | available |
| innov.tech-landscape.m_innov_factor_cluster | POST | /innov/v1/innov/metric/M_INNOV_FACTOR_CLUSTER/compute | API-02037～02039 | available |
| innov.tech-landscape.m_innov_factor_forecast | POST | /innov/v1/innov/metric/M_INNOV_FACTOR_FORECAST/compute | API-02040～02042 | available |
| innov.tech-landscape.m_innov_journal_influence | POST | /innov/v1/innov/metric/M_INNOV_JOURNAL_INFLUENCE/compute | API-02043～02045 | available |
| innov.tech-landscape.m_innov_org_influence | POST | /innov/v1/innov/metric/M_INNOV_ORG_INFLUENCE/compute | API-02046～02048 | available |
| innov.tech-landscape.m_innov_patent_influence | POST | /innov/v1/innov/metric/M_INNOV_PATENT_INFLUENCE/compute | API-02049～02051 | available |
| innov.tech-landscape.m_innov_project_influence | POST | /innov/v1/innov/metric/M_INNOV_PROJECT_INFLUENCE/compute | API-02052～02054 | available |
| innov.tech-landscape.m_innov_scholar_influence | POST | /innov/v1/innov/metric/M_INNOV_SCHOLAR_INFLUENCE/compute | API-02055～02057 | available |
| innov.tech-landscape.m_innov_ds_factors_016 | POST | /innov/v1/innov/metric/M_INNOV_DS_FACTORS_016/compute | API-02058～02060 | available |
| innov.tech-landscape.m_innov_ds_factors_018 | POST | /innov/v1/innov/metric/M_INNOV_DS_FACTORS_018/compute | API-02061～02063 | available |

GET `/innov/v1/innov/metrics` 与其它创新监测指标页共用 path。本页三条只挂 `endpoint_id=innov.tech-landscape.metrics`，主路径 `module=tech-landscape`。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行，也不按字段各写一条用例。每个 title 的 sampleResponse 与 responseFields 都挂在该接口主流程与备选上；可选 `module` 与 sample 相反的不传挂备选；`module` 恰好 1 条非法反向。同名 title「监测趋势预测」不合并。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） \| innov.tech-landscape.metrics \| 科技全域态势指标清单 | API-02019、API-02020、API-02021 | 无对应功能点 | 02019 主流程 sampleRequest（module=tech-landscape），断言 metrics（元素 metric_id、name、algorithm_type、formula_status、pending_ref，sample 23 行）与 total（number，示例 23）；02020 不传 module；02021 非法 module。文档标记未交付 |
| （无 Lxx） \| innov.tech-landscape.m_innov_conference_influence \| 会议影响力 | API-02022、API-02023、API-02024 | 无对应功能点 | 02022 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_CONFERENCE_INFLUENCE）、hint，以及 responseFields 声明的 metrics、total；02023 不传 module；02024 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_enterprise_influence \| 企业影响力 | API-02025、API-02026、API-02027 | 无对应功能点 | 02025 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_ENTERPRISE_INFLUENCE）、hint，以及 responseFields 声明的 metrics、total；02026 不传 module；02027 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_event_attention \| 事件关注度 | API-02028、API-02029、API-02030 | 无对应功能点 | 02028 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_EVENT_ATTENTION）、hint，以及 responseFields 声明的 metrics、total；02029 不传 module；02030 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_event_influence \| 事件影响力 | API-02031、API-02032、API-02033 | 无对应功能点 | 02031 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_EVENT_INFLUENCE）、hint，以及 responseFields 声明的 metrics、total；02032 不传 module；02033 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_factor_anomaly \| 监测异常点识别 | API-02034、API-02035、API-02036 | 无对应功能点 | 02034 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_FACTOR_ANOMALY）、hint，以及 responseFields 声明的 metrics、total；02035 不传 module；02036 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_factor_cluster \| 要素聚类 | API-02037、API-02038、API-02039 | 无对应功能点 | 02037 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_FACTOR_CLUSTER）、hint，以及 responseFields 声明的 metrics、total；02038 不传 module；02039 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_factor_forecast \| 监测趋势预测 | API-02040、API-02041、API-02042 | 无对应功能点 | 02040 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_FACTOR_FORECAST）、hint，以及 responseFields 声明的 metrics、total；02041 不传 module；02042 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_journal_influence \| 期刊影响力 | API-02043、API-02044、API-02045 | 无对应功能点 | 02043 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_JOURNAL_INFLUENCE）、hint，以及 responseFields 声明的 metrics、total；02044 不传 module；02045 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_org_influence \| 科研机构影响力 | API-02046、API-02047、API-02048 | 无对应功能点 | 02046 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_ORG_INFLUENCE）、hint，以及 responseFields 声明的 metrics、total；02047 不传 module；02048 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_patent_influence \| 专利影响力 | API-02049、API-02050、API-02051 | 无对应功能点 | 02049 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_PATENT_INFLUENCE）、hint，以及 responseFields 声明的 metrics、total；02050 不传 module；02051 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_project_influence \| 项目（含课题）影响力 | API-02052、API-02053、API-02054 | 无对应功能点 | 02052 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_PROJECT_INFLUENCE）、hint，以及 responseFields 声明的 metrics、total；02053 不传 module；02054 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_scholar_influence \| 专家学者影响力 | API-02055、API-02056、API-02057 | 无对应功能点 | 02055 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_SCHOLAR_INFLUENCE）、hint，以及 responseFields 声明的 metrics、total；02056 不传 module；02057 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_ds_factors_016 \| 要素聚类分析 | API-02058、API-02059、API-02060 | 无对应功能点 | 02058 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_DS_FACTORS_016）、hint，以及 responseFields 声明的 metrics、total；02059 不传 module；02060 非法 module |
| （无 Lxx） \| innov.tech-landscape.m_innov_ds_factors_018 \| 监测趋势预测 | API-02061、API-02062、API-02063 | 无对应功能点 | 02061 主流程 sampleRequest（module=tech-landscape），断言 metric_id（示例 M_INNOV_DS_FACTORS_018）、hint，以及 responseFields 声明的 metrics、total；02062 不传 module；02063 非法 module |

---

## 同名 title

| title | 主流程 | endpoint_id | metric |
|-------|--------|-------------|--------|
| 监测趋势预测 | API-02040 | innov.tech-landscape.m_innov_factor_forecast | M_INNOV_FACTOR_FORECAST |
| 监测趋势预测 | API-02061 | innov.tech-landscape.m_innov_ds_factors_018 | M_INNOV_DS_FACTORS_018 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 15 |
| title 数 | 15（其中「监测趋势预测」同名 2 条，不合并） |
| API 用例数 | 45 |
| 主流程 | 15（02019、02022、02025、02028、02031、02034、02037、02040、02043、02046、02049、02052、02055、02058、02061） |
| 备选-参数组合 | 15（各接口不传 module） |
| 反向 | 15（各接口非法 module） |
| 编号 | API-02019～02063 连续 |
| A 线 Lxx | 无 |
