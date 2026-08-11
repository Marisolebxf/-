# 派单包 · PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01 + PY-ENT-RECOMMEND-GEO-COUNTRY-L01

> 2026-08-11 · 监管建议 human:徐滕强  
> 前置：`DATA-ENT-CODE-COUNTRY-APPLY-L01`（含 **L05**）+ `FIX-TOPIC-ES-TEXT-ANALYZER-L01`（`country_code` + `city_code`）  
> 城市码：`agent-delivery/data/ddl/CITY-CODE-G20.md`

## 共同约定

- **高筛不动**：`enterprise_region` / `/meta/regions` 仍只用国内国标。
- 国家码：ISO **alpha-3**（`bind_country_code`）。
- 海外城市码：**UN/LOCODE** 五位（`bind_city_code`，如 `JPTYO`）。
- 中国城市：走 `region_id` ← `bind_admin_code`（不要把 `CN-1100` 当 ES city_code）。
- 混选：**三分 OR**（`region_id` ∪ `country_code` ∪ `city_code`）。
- **禁止**把 `JPN` / `JPTYO` 写入 `region_id`。
- 选国家叶 = 整国 `country_codes`，**不要**展开成样例城市并集。

## A. 重点企业分析 `PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01`

仓：`demo-svc-topic-py` · `gkx_search_service/views/key_analysis.py`

1. `_build_common_filter` 增加 `country_codes: string[]` + `city_codes: string[]`
2. DSL：

```json
{ "bool": { "should": [
  { "prefix": { "region_id": "440300" } },
  { "terms": { "country_code": ["JPN", "USA"] } },
  { "terms": { "city_code": ["JPTYO", "USNYC"] } }
], "minimum_should_match": 1 } }
```

3. Java Request 透传两数组（collaborator: api-agent）
4. 单测：仅国内 / 仅国家 / 仅城市 / 混选 / 皆空

## B. 招引推荐 `PY-ENT-RECOMMEND-GEO-COUNTRY-L01`

仓：`demo-svc-topic-py` · `gkx_ai_service/views/recommend.py`

1. `filters.geographicSources[]` 可含：6 位国标 / alpha-3 / UN/LOCODE 五位
2. 分流：`^[A-Z]{3}$` → country；`^[A-Z]{5}$` → city_code；`^\d{6}$` → region_id
3. 混选 OR；契约补字段说明
4. 样例：`geographicSources: ["440300","JPN","JPTYO"]`

## 依赖顺序

```text
DIM（code_country + L04 + L05）→ ES mapping/灌数 → 本两单 Python → FE 三分取码
```
