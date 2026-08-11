# FIX-TOPIC-ES-TEXT-ANALYZER-L01 · handoff

> claimed_by: `agent:data-agent`  
> supervised_by: `human:徐滕强`  
> claim_type: `pull`  
> ponytail: `full`  
> 日期：2026-08-11  
> **收口**：原 DoD（analyzer / mapping / match_phrase / playbook）已交付 → 建议 `pending_test`  
> **边界**：`country_code`/`city_code` **灌数**与 **索引 recreate** 已外派其他 agent，**不**并入本单关单条件

## 范围与实现

对照 DoD + 范围扩容（`FIX-TOPIC-ES-TEXT-ANALYZER-L01-范围扩容.md`）+ 设计 `企业搜索-ES索引设计.md` v3.7：

| DoD | 结果 |
|-----|------|
| `min_length_2` + `ik_max_word_min2` / `ik_smart_min2`（不改共享 analyzer） | ✅ `app/es.py` |
| `main_prod` / `main_activities` / `description` 用 min2；保持 text、不加 `.keyword` | ✅ mapping |
| 无 `.keyword` 的长文本一律 min2（补 `business_scope` / `stock_noun`；`address` 正文 min2） | ✅ `311f119` |
| `country_code` / `city_code` 顶层 keyword（**仅 mapping**） | ✅ mapping |
| 智能检索长文本 match_phrase + 单字不查 | ✅ `demo-svc-topic-py` `573429c` |
| 重建 playbook；现网不强制 recreate | ✅ `docs/PLAYBOOK-enterprise-index-recreate.md` |
| 单测 settings/mapping | ✅ `tests/test_es_index_settings.py`（6 绿，2026-08-11 复跑） |

## Mapping 差集（相对改前）

| 字段 | 改前 | 改后 |
|------|------|------|
| `main_prod` | text + `ik_max_word_analyzer` | text + `ik_max_word_min2` / search `ik_smart_min2` |
| `main_activities` | 同上 | 同上 |
| `description` | text + `ik_smart_analyzer` | text + `ik_smart_min2` |
| `business_scope` / `stock_noun` | 共享 ik_smart | `ik_smart_min2` |
| `country_code` | 无 | keyword |
| `city_code` | 无 | keyword |
| `address` | text only | text `ik_smart_min2` + `fields.keyword` |

## 偏离说明

- **现网索引**：未由本单 recreate；新 analyzer / 字段等外派重建任务生效（符合原 DoD「不强制 recreate」）。  
- **灌数**：本单只定 mapping/契约；forg→alpha-3 / UN/LOCODE **写 ES 值**已交其他 agent（DWD §4.13），**不阻塞本单原 DoD 验收**。  
- **未改**共享 `ik_*_analyzer`；高筛 `enterprise_region` 不动；`region_id` 保持纯 keyword（`prefix`/`term`）。

## 产物清单

| 仓 | commit | 说明 |
|----|--------|------|
| `lumen-etl-es-py` | `133cac5` | min2 + country/city_code keyword + playbook |
| `lumen-etl-es-py` | `311f119` | 裸 text 全覆盖 min2 |
| `demo-svc-topic-py` | `573429c` | 三长文本 match_phrase |
| 编排仓 | `73adcb3` + 本文件修订 | handoff |

## 验收证据

- `python3 -m unittest tests.test_es_index_settings -q` → **6 OK**（2026-08-11 复跑）  
- 本地断言：关键词「米」不生成长文本 match_phrase；「小米」含三字段 match_phrase

## 架构合规自检

1. 算法只在 Python：✅  
2. 调用链：✅ 未越层  
3. 图谱：N/A  
4. 可观测：N/A  
5. CI/CD：已 push `origin/dev`  
6–10：N/A（mapping / 查询侧 bugfix）

## 解锁下游

- 外派：索引 recreate + `country_code`/`city_code` 灌数  
- 其后：`PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01` / `PY-ENT-RECOMMEND-GEO-COUNTRY-L01`  
- Java `bindCountryCode`：api-agent（不在本单）

## Cost（回填）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~45000（估） |
| model_used | cursor-grok-4.5 |
| actual_cost | ~1.5 |
| cost_warn | green |
