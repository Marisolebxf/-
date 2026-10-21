# 科技全域态势 · A 线功能点覆盖（innov.tech-landscape）

> **catalog_page_id**：`innov.tech-landscape` · path `/innov/tech-landscape`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-科技全域态势-用例.md`（第三轮 **FUNC-01297**～**01343**，共 47 条；旧 API-02019～02063 作废）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.tech-landscape`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.tech-landscape.metrics | GET | /innov/v1/innov/metrics | FUNC-01297、01298、01299 | unavailable |
| innov.tech-landscape.m_innov_conference_influence | POST | /innov/v1/innov/metric/M_INNOV_CONFERENCE_INFLUENCE/compute | FUNC-01300～01302 | available |
| innov.tech-landscape.m_innov_enterprise_influence | POST | /innov/v1/innov/metric/M_INNOV_ENTERPRISE_INFLUENCE/compute | FUNC-01303～01305 | available |
| innov.tech-landscape.m_innov_event_attention | POST | /innov/v1/innov/metric/M_INNOV_EVENT_ATTENTION/compute | FUNC-01306～01308 | available |
| innov.tech-landscape.m_innov_event_influence | POST | /innov/v1/innov/metric/M_INNOV_EVENT_INFLUENCE/compute | FUNC-01309～01311 | available |
| innov.tech-landscape.m_innov_factor_anomaly | POST | /innov/v1/innov/metric/M_INNOV_FACTOR_ANOMALY/compute | FUNC-01312～01314 | available |
| innov.tech-landscape.m_innov_factor_cluster | POST | /innov/v1/innov/metric/M_INNOV_FACTOR_CLUSTER/compute | FUNC-01315～01317 | available |
| innov.tech-landscape.m_innov_factor_forecast | POST | /innov/v1/innov/metric/M_INNOV_FACTOR_FORECAST/compute | FUNC-01318～01320 | available |
| innov.tech-landscape.m_innov_journal_influence | POST | /innov/v1/innov/metric/M_INNOV_JOURNAL_INFLUENCE/compute | FUNC-01321～01323 | available |
| innov.tech-landscape.m_innov_org_influence | POST | /innov/v1/innov/metric/M_INNOV_ORG_INFLUENCE/compute | FUNC-01324～01326 | available |
| innov.tech-landscape.m_innov_patent_influence | POST | /innov/v1/innov/metric/M_INNOV_PATENT_INFLUENCE/compute | FUNC-01327～01329 | available |
| innov.tech-landscape.m_innov_project_influence | POST | /innov/v1/innov/metric/M_INNOV_PROJECT_INFLUENCE/compute | FUNC-01330～01332 | available |
| innov.tech-landscape.m_innov_scholar_influence | POST | /innov/v1/innov/metric/M_INNOV_SCHOLAR_INFLUENCE/compute | FUNC-01333～01335 | available |
| innov.tech-landscape.m_innov_ds_factors_016 | POST | /innov/v1/innov/metric/M_INNOV_DS_FACTORS_016/compute | FUNC-01336～01338 | available |
| innov.tech-landscape.m_innov_ds_factors_018 | POST | /innov/v1/innov/metric/M_INNOV_DS_FACTORS_018/compute | FUNC-01339～01341 | available |

页面清单：**FUNC-01342**（接口信息）、**FUNC-01343**（算法测试）。

GET `/innov/v1/innov/metrics` 与其它创新监测指标页共用 path。本页三条只挂 `endpoint_id=innov.tech-landscape.metrics`，主路径 `module=tech-landscape`。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行。每个 title 各 3 条（主流程 module=tech-landscape、不传 module、非法 module），预期字段与旧 API 册一致，步骤改为 algovwz 联调台操作。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） · innov.tech-landscape.metrics · 科技全域态势指标清单 | FUNC-01297、01298、01299 | 无对应功能点 | 01297 主流程 LST-01（金样）；01298 不传 module；01299 非法 module。文档标记未交付 |
| （无 Lxx） · innov.tech-landscape.m_innov_conference_influence · 会议影响力 | FUNC-01300、01301、01302 | 无对应功能点 | 01300 主流程 CONF-01；01301 不传 module；01302 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_enterprise_influence · 企业影响力 | FUNC-01303、01304、01305 | 无对应功能点 | 01303 主流程 ENTI-01；01304 不传 module；01305 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_event_attention · 事件关注度 | FUNC-01306、01307、01308 | 无对应功能点 | 01306 主流程 EATT-01；01307 不传 module；01308 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_event_influence · 事件影响力 | FUNC-01309、01310、01311 | 无对应功能点 | 01309 主流程 EINF-01；01310 不传 module；01311 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_factor_anomaly · 监测异常点识别 | FUNC-01312、01313、01314 | 无对应功能点 | 01312 主流程 ANOM-01；01313 不传 module；01314 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_factor_cluster · 要素聚类 | FUNC-01315、01316、01317 | 无对应功能点 | 01315 主流程 CLUS-01；01316 不传 module；01317 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_factor_forecast · 监测趋势预测 | FUNC-01318、01319、01320 | 无对应功能点 | 01318 主流程 FCST-01（M_INNOV_FACTOR_FORECAST）；01319 不传 module；01320 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_journal_influence · 期刊影响力 | FUNC-01321、01322、01323 | 无对应功能点 | 01321 主流程 JOUR-01；01322 不传 module；01323 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_org_influence · 科研机构影响力 | FUNC-01324、01325、01326 | 无对应功能点 | 01324 主流程 ORG-01；01325 不传 module；01326 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_patent_influence · 专利影响力 | FUNC-01327、01328、01329 | 无对应功能点 | 01327 主流程 PAT-01；01328 不传 module；01329 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_project_influence · 项目（含课题）影响力 | FUNC-01330、01331、01332 | 无对应功能点 | 01330 主流程 PROJ-01；01331 不传 module；01332 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_scholar_influence · 专家学者影响力 | FUNC-01333、01334、01335 | 无对应功能点 | 01333 主流程 SCH-01；01334 不传 module；01335 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_ds_factors_016 · 要素聚类分析 | FUNC-01336、01337、01338 | 无对应功能点 | 01336 主流程 F016-01；01337 不传 module；01338 非法 module |
| （无 Lxx） · innov.tech-landscape.m_innov_ds_factors_018 · 监测趋势预测 | FUNC-01339、01340、01341 | 无对应功能点 | 01339 主流程 F018-01（M_INNOV_DS_FACTORS_018）；01340 不传 module；01341 非法 module |
| （页面清单） · 接口信息 / 算法测试 | FUNC-01342、01343 | 无对应功能点 | 联调台 tab 与 catalog 下拉一致性 |

---

## 同名 title

| title | 主流程 | endpoint_id | metric |
|-------|--------|-------------|--------|
| 监测趋势预测 | FUNC-01318 | innov.tech-landscape.m_innov_factor_forecast | M_INNOV_FACTOR_FORECAST |
| 监测趋势预测 | FUNC-01339 | innov.tech-landscape.m_innov_ds_factors_018 | M_INNOV_DS_FACTORS_018 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 15 |
| title 数 | 15（其中「监测趋势预测」同名 2 条，不合并） |
| FUNC 用例数 | 47（接口 45 + 清单 2） |
| 主流程 | 15 |
| 备选-参数组合 | 15 |
| 反向 | 15 |
| 页面清单 | 2 |
| 编号 | FUNC-01297～01343 连续 |
| A 线 Lxx | 无 |
