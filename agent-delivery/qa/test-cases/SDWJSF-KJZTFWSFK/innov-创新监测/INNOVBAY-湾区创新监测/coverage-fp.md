# 湾区创新监测 · A 线功能点覆盖（innov.bay-area-monitoring）

> **catalog_page_id**：`innov.bay-area-monitoring` · path `/innov/bay-area-monitoring`  
> **A 线**：**无对应 Lxx**。`fp-split-by-api-run/_l6-to-catalog-map.yaml` 的 `catalog_skip` 登记 `innov.*`（原因：创新监测不在本轮 60 六级）。L01–L60 的 `pages` 均未挂本页。不改 `work/`。  
> **用例册**：`FUNC-湾区创新监测-用例.md`（第三轮 **FUNC-01426**～**01478**，共 53 条；旧 API-02142～02192 作废）  
> **契约**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.bay-area-monitoring`  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/（FUNC 联调台步骤）

---

## endpoint → 用例

| endpoint_id | METHOD | path | 用例编号 | catalog status |
|-------------|--------|------|----------|----------------|
| innov.bay-area-monitoring.metrics | GET | /innov/v1/innov/metrics | FUNC-01426、01427、01428 | unavailable |
| innov.bay-area-monitoring.m_innov_gba_capacity_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_CAPACITY_INDEX/compute | FUNC-01429～01431 | available |
| innov.bay-area-monitoring.m_innov_gba_env_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_ENV_INDEX/compute | FUNC-01432～01434 | available |
| innov.bay-area-monitoring.m_innov_gba_hotspot | POST | /innov/v1/innov/metric/M_INNOV_GBA_HOTSPOT/compute | FUNC-01435～01437 | available |
| innov.bay-area-monitoring.m_innov_gba_mech_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_MECH_INDEX/compute | FUNC-01438～01440 | available |
| innov.bay-area-monitoring.m_innov_gba_org_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_ORG_INDEX/compute | FUNC-01441～01443 | available |
| innov.bay-area-monitoring.m_innov_gba_res_index | POST | /innov/v1/innov/metric/M_INNOV_GBA_RES_INDEX/compute | FUNC-01444～01446 | available |
| innov.bay-area-monitoring.m_innov_gba_subindex_contrib | POST | /innov/v1/innov/metric/M_INNOV_GBA_SUBINDEX_CONTRIB/compute | FUNC-01447～01449 | available |
| innov.bay-area-monitoring.m_innov_gba_swot_opportunity | POST | /innov/v1/innov/metric/M_INNOV_GBA_SWOT_OPPORTUNITY/compute | FUNC-01450～01452 | available |
| innov.bay-area-monitoring.m_innov_gba_swot_strength | POST | /innov/v1/innov/metric/M_INNOV_GBA_SWOT_STRENGTH/compute | FUNC-01453～01455 | available |
| innov.bay-area-monitoring.m_innov_gba_swot_threat | POST | /innov/v1/innov/metric/M_INNOV_GBA_SWOT_THREAT/compute | FUNC-01456～01458 | available |
| innov.bay-area-monitoring.m_innov_gba_swot_weakness | POST | /innov/v1/innov/metric/M_INNOV_GBA_SWOT_WEAKNESS/compute | FUNC-01459～01461 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_achieve_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ACHIEVE_004/compute | FUNC-01462～01464 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_003 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ANALYSIS_003/compute | FUNC-01465～01467 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_004 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ANALYSIS_004/compute | FUNC-01468～01470 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_005 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ANALYSIS_005/compute | FUNC-01471～01473 | available |
| innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_006 | POST | /innov/v1/innov/metric/M_INNOV_DS_05_GBA_ANALYSIS_006/compute | FUNC-01474～01476 | available |

页面清单：**FUNC-01477**（接口信息）、**FUNC-01478**（算法测试）。

---

## 功能点 → 用例矩阵

本页不在 60 六级挂接表，**无对应 Lxx**，B 线记 **无对应功能点**。不按 `field_key` 拆行。每个 title 各 3 条（主流程 module=bay-area-monitoring、不传 module、非法 module），预期字段与旧 API 册一致，步骤改为 algovwz 联调台操作。

| 功能点键 | 对应用例编号 | 状态 | 说明 |
|----------|--------------|------|------|
| （无 Lxx） · innov.bay-area-monitoring.metrics · 湾区创新监测指标清单 | FUNC-01426、01427、01428 | 无对应功能点 | 01426 主流程 MET-01（金样）；01427 不传 module；01428 非法 module；catalog status=unavailable |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_capacity_index · 粤港澳大湾区创新能力指标 | FUNC-01429～01431 | 无对应功能点 | CAP-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_env_index · 创新环境指数 | FUNC-01432～01434 | 无对应功能点 | ENV-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_hotspot · 湾区创新热点区域 | FUNC-01435～01437 | 无对应功能点 | HOT-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_mech_index · 创新机制指数 | FUNC-01438～01440 | 无对应功能点 | MEC-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_org_index · 创新机构指数 | FUNC-01441～01443 | 无对应功能点 | ORG-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_res_index · 创新资源指数 | FUNC-01444～01446 | 无对应功能点 | RES-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_subindex_contrib · 子指标贡献度 | FUNC-01447～01449 | 无对应功能点 | SUB-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_swot_opportunity · 湾区创新能力机会因素 | FUNC-01450～01452 | 无对应功能点 | OPP-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_swot_strength · 湾区创新能力优势因素 | FUNC-01453～01455 | 无对应功能点 | STR-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_swot_threat · 湾区创新能力威胁因素 | FUNC-01456～01458 | 无对应功能点 | THR-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_gba_swot_weakness · 湾区创新能力短板因素 | FUNC-01459～01461 | 无对应功能点 | WEA-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_ds_05_gba_achieve_004 · 创新热点区域识别 | FUNC-01462～01464 | 无对应功能点 | ACH-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_003 · 优势因素分析 | FUNC-01465～01467 | 无对应功能点 | AN3-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_004 · 短板因素分析 | FUNC-01468～01470 | 无对应功能点 | AN4-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_005 · 机会因素分析 | FUNC-01471～01473 | 无对应功能点 | AN5-01/02/03 |
| （无 Lxx） · innov.bay-area-monitoring.m_innov_ds_05_gba_analysis_006 · 威胁因素分析 | FUNC-01474～01476 | 无对应功能点 | AN6-01/02/03 |
| （页面清单） | FUNC-01477、01478 | 无对应功能点 | 十七接口页接口信息 / 算法测试 tab 清单 |

---

## 计数

| 项 | 值 |
|----|-----|
| catalog endpoint 数 | 17 |
| title 数 | 17 |
| FUNC 用例数 | 53 |
| 主流程 | 17 |
| 备选-参数组合 | 17 |
| 反向 | 17 |
| 清单 | 2 |
| 编号 | FUNC-01426～01478 连续 |
| A 线 Lxx | 无 |
| 金样 | FUNC-01426 |
