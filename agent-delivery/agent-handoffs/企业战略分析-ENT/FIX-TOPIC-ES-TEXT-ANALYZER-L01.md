# FIX-TOPIC-ES-TEXT-ANALYZER-L01 · handoff

> claimed_by: `agent:data-agent`  
> supervised_by: `human:徐滕强`  
> claim_type: `pull`  
> ponytail: `full`  
> 日期：2026-08-11

## 范围与实现

对照 DoD + 范围扩容（`FIX-TOPIC-ES-TEXT-ANALYZER-L01-范围扩容.md`）+ 设计 `企业搜索-ES索引设计.md` v3.7：

| DoD | 结果 |
|-----|------|
| `min_length_2` + `ik_max_word_min2` / `ik_smart_min2`（不改共享 analyzer） | ✅ `app/es.py` |
| `main_prod` / `main_activities` / `description` 用 min2；保持 text、不加 `.keyword` | ✅ mapping |
| `country_code` / `city_code` 顶层 keyword | ✅ mapping |
| 智能检索长文本 match_phrase + 单字不查 | ✅ `demo-svc-topic-py` `enterprise_compare.py`（扩到三字段） |
| 重建 playbook；现网不强制 recreate | ✅ `docs/PLAYBOOK-enterprise-index-recreate.md` |
| 单测 settings/mapping | ✅ `tests/test_es_index_settings.py`（5 绿） |

## Mapping 差集（相对改前）

| 字段 | 改前 | 改后 |
|------|------|------|
| `main_prod` | text + `ik_max_word_analyzer` | text + `ik_max_word_min2` / search `ik_smart_min2` |
| `main_activities` | 同上 | 同上 |
| `description` | text + `ik_smart_analyzer` | text + `ik_smart_min2` |
| `country_code` | 无 | keyword |
| `city_code` | 无 | keyword |
| `address` | text only | text + `fields.keyword`（双字段冻结补精确） |

## 偏离说明

- **现网索引**：未 recreate；新 analyzer / 字段仅在下次 `init?recreate=true` 或新建索引生效（符合 DoD）。  
- **灌数**：本单只定 mapping/契约；forg→alpha-3 / UN/LOCODE 写 ES 值仍走后续 ETL（DWD §4.13），不阻塞 mapping 就绪。  
- **未改**共享 `ik_*_analyzer`；高筛 `enterprise_region` 不动。

## 产物清单

- `lumen-etl-es-py`：`app/es.py`、`conf/es/gkx_enterprise_mappings.json`、`tests/test_es_index_settings.py`、`docs/PLAYBOOK-enterprise-index-recreate.md`
- `demo-svc-topic-py`：`gkx_search_service/views/enterprise_compare.py`
- 本 handoff

## 验收证据

- `python3 -m unittest tests.test_es_index_settings -v` → 5 OK  
- 本地断言：关键词「米」不生成长文本 match_phrase；「小米」含 `main_prod`/`main_activities`/`description` 三字段 match_phrase

## 架构合规自检

1. 算法只在 Python：✅（本单 ETL/mapping + search 查询侧）  
2. 调用链：✅ 未越层  
3. 图谱：N/A  
4. 可观测：N/A（无新服务）  
5. CI/CD：push `origin/dev` 后由 Pipeline 部署  
6. demo→lumen merge：N/A  
7. 共享聚合：N/A  
8. 数据策略 ADS/Mock：N/A（ES mapping）  
9. D8 Design：N/A  
10. D9/D10：N/A  

## 解锁下游

- `PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01` / `PY-ENT-RECOMMEND-GEO-COUNTRY-L01`：mapping 就绪；仍需 recreate 后才有字段可写，且查询 OR 仍 backlog  
- Java `bind_country_code` 透传：不在本单

## Cost（回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | （会话估算，coordinator 可校正） |
| model_used | cursor-grok-4.5 |
| actual_cost | ~1.5 |
| cost_warn | green |
