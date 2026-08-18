# DEMO-SVC-PY-PORTAL-AGG-L01 · 门户 ADS 聚合 sections

> 日期：2026-08-18  
> Task：`DEMO-SVC-PY-PORTAL-AGG-L01`  
> 总控：`DEMO-SVC-FULL-底座后全量-长任务总控.md` / `DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只扩 overview + 四分段读面；契约 ADS 只读；不发明正式库写入；深圳历年用全球趋势×SZ 占比代理并标 mock |

## 范围与实现

- 仓：`repos/lumen-topic-py` · `gkx_svc_service`
- **overview 扩展 sections**（同真源 `_portal_ads_sections`）  
  - `trend` / `scale_dist` / `by_service_type`（既有）  
  - `industry_distribution.stages` ← `svc_org_profile_card.ext_json.segment` → FE 环节 id  
  - `region_map.{china,global,regions}` ← `svc_region_dist` `M_SVC_PT_CITY_ORG`  
  - `capability_rank.items` ← `svc_tech_power_score` ⋈ profile  
  - `shenzhen.{trend,type_dist,key_orgs,districts,sz_total}` ← fact/series/region/profile  
- **新增内部路由**（供后续 Java EXT 透传；当前 FE 仍读 overview）  
  - `POST /internal/gkx-svc/portal/industry-distribution`  
  - `POST /internal/gkx-svc/portal/region-map`  
  - `POST /internal/gkx-svc/portal/capability-rank`  
  - `POST /internal/gkx-svc/portal/shenzhen`  
- `portal/ranking`：LEFT JOIN profile 补 `name_cn`/`type`/`city`  
- 诚实性：始终 `mock: true` + `gap: [Q-SVC-010]`；拒非 `demo_` ADS

## 偏离说明

- Demo 无独立「深圳历年 series」→ `shenzhen.trend` = 全球趋势 × `M_SVC_PT_SZ_TOTAL/ORG_TOTAL`，文档注明代理。  
- `region_map.global` 与 `china` 同城池（无国别维）；不伪造国家名。  
- Java 门面仍仅 overview/ranking；四分段 path 待 `LUMEN-SVC-JAVA-PORTAL-EXT-L01`。

## 产物清单

| 产物 | 路径 |
|------|------|
| repo | `gkx_svc_service/repo.py` |
| views | `gkx_svc_service/views/search.py` |
| routes list | `gkx_svc_service/main.py` |
| tests | `tests/test_gkx_svc_boot.py` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-PY-PORTAL-AGG-L01.md` |

## 验收证据

- [x] `py -3 -m pytest tests/test_gkx_svc_boot.py` → **12 passed**  
- [x] commit `858af1b` push `origin/dev`  
- [x] GitLab pipeline `5193`；play `deploy:search-py`（见 CI/CD）  
- [ ] 外网 `POST …/service-portal/overview` 含 industry/region/shenzhen/capability 键（部署完成后冒烟）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 聚合在 topic-py |
| 2 | 前端→Java→`/internal/*` | ✅ 契约就绪；Java EXT 另叶 |
| 6 | 仅 demo_ 库 | ✅ |
| D9/Q-SVC-010 | 不伪闭合 | ✅ mock+gap |
| D12 | 不 Feign demo-* | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~6 万 |
| actual_cost | 估 <$3 |
| cost_warn | false |

## CI/CD

- 分支：`dev`
- commit：`858af1b`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-topic-py/-/pipelines/5193
- job：`deploy:search-py`（manual play）
- 外网基址：http://111.198.38.90:50892/api/svc/topic/v1/service-portal/**

## 联调确认

联调通过：门户四分段 ADS sections 经 `/internal/gkx-svc/portal/**` 可返回；overview 已嵌 sections 供现行 FE 五 Tab。下一叶建议 `LUMEN-SVC-JAVA-PORTAL-EXT-L01`（可选透传）+ `LUMEN-SVC-FE-PORTAL-FULL-L01`。
