# 科技发展规划 · A 线功能点覆盖（innov.tech-planning）

> **catalog_page_id**：`innov.tech-planning` · path `/innov/tech-planning`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-科技发展规划-用例.md`（第三轮 **FUNC-01253**～**01296**，共 44 条；旧 API-01977～02018 作废）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.tech-planning`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.tech-planning.metrics | GET | /innov/v1/innov/metrics | FUNC-01253、01254、01255 | running |
| innov.tech-planning.m_innov_plan_direction_alert | POST | /innov/v1/innov/metric/M_INNOV_PLAN_DIRECTION_ALERT/compute | FUNC-01256～01258 | available |
| innov.tech-planning.m_innov_plan_local_adv | POST | /innov/v1/innov/metric/M_INNOV_PLAN_LOCAL_ADV/compute | FUNC-01259～01261 | available |
| innov.tech-planning.m_innov_plan_talent_flow | POST | /innov/v1/innov/metric/M_INNOV_PLAN_TALENT_FLOW/compute | FUNC-01262～01264 | available |
| innov.tech-planning.m_innov_res_ci_level | POST | /innov/v1/innov/metric/M_INNOV_RES_CI_LEVEL/compute | FUNC-01265～01267 | available |
| innov.tech-planning.m_innov_res_grade | POST | /innov/v1/innov/metric/M_INNOV_RES_GRADE/compute | FUNC-01268～01270 | available |
| innov.tech-planning.m_innov_res_overlap | POST | /innov/v1/innov/metric/M_INNOV_RES_OVERLAP/compute | FUNC-01271～01273 | available |
| innov.tech-planning.m_innov_ds_09_comprehensive_005 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_COMPREHENSIVE_005/compute | FUNC-01274～01276 | available |
| innov.tech-planning.m_innov_ds_09_comprehensive_006 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_COMPREHENSIVE_006/compute | FUNC-01277～01279 | available |
| innov.tech-planning.m_innov_ds_09_comprehensive_008 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_COMPREHENSIVE_008/compute | FUNC-01280～01282 | available |
| innov.tech-planning.m_innov_ds_09_research_001 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_RESEARCH_001/compute | FUNC-01283～01285 | available |
| innov.tech-planning.m_innov_ds_09_research_002 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_RESEARCH_002/compute | FUNC-01286～01288 | available |
| innov.tech-planning.m_innov_ds_09_research_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_RESEARCH_003/compute | FUNC-01289～01291 | available |
| innov.tech-planning.m_innov_ds_09_research_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_09_RESEARCH_004/compute | FUNC-01292～01294 | available |

页面清单：**FUNC-01295**（接口信息）、**FUNC-01296**（算法测试）。

---

## 功能点 → 用例矩阵

本页不在六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行。每个 title 各 3 条（主流程 module=tech-planning、不传 module、非法 module），预期字段与旧 API 册一致，步骤改为 algovwz 联调台操作。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） · innov.tech-planning.metrics · 科技发展规划指标清单 | FUNC-01253、01254、01255 | 无对应功能点 | 01253 主流程 MET-01（金样）；01254 不传 module；01255 非法 module |
| （无 Lxx） · innov.tech-planning.m_innov_plan_direction_alert · 潜在科技发展方向预警 | FUNC-01256～01258 | 无对应功能点 | DIR-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_plan_local_adv · 本地科技创新特色与优势 | FUNC-01259～01261 | 无对应功能点 | ADV-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_plan_talent_flow · 科技人才流动（产业界↔学术界） | FUNC-01262～01264 | 无对应功能点 | TAL-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_res_ci_level · 竞争情报等级 | FUNC-01265～01267 | 无对应功能点 | CI1-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_res_grade · 研究领域等级划分 | FUNC-01268～01270 | 无对应功能点 | GR1-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_res_overlap · 研究领域重叠度 | FUNC-01271～01273 | 无对应功能点 | OV1-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_comprehensive_005 · 本地特色与优势分析 | FUNC-01274～01276 | 无对应功能点 | C05-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_comprehensive_006 · 科技人才流动监控 | FUNC-01277～01279 | 无对应功能点 | C06-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_comprehensive_008 · 潜在科技发展方向预警 | FUNC-01280～01282 | 无对应功能点 | C08-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_research_001 · 研究领域重叠度 | FUNC-01283～01285 | 无对应功能点 | R01-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_research_002 · 研究领域等级划分 | FUNC-01286～01288 | 无对应功能点 | R02-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_research_003 · 竞争情报等级 | FUNC-01289～01291 | 无对应功能点 | R03-01/02/03 |
| （无 Lxx） · innov.tech-planning.m_innov_ds_09_research_004 · 多企业竞争情报比对 | FUNC-01292～01294 | 无对应功能点 | R04-01/02/03 |
| （页面清单） | FUNC-01295、01296 | 无对应功能点 | 十四接口页接口信息 / 算法测试 tab 清单 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 14 |
| title 数 | 14 |
| FUNC 用例数 | 44 |
| 主流程 | 14 |
| 备选-参数组合 | 14 |
| 反向 | 14 |
| 清单 | 2 |
| 编号 | FUNC-01253～01296 连续 |
| A 线 Lxx | 无 |
| 金样 | FUNC-01253 |
