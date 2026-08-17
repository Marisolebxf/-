# DEMO-SVC-PY-MIDDLE-SEARCH-L01 · 产业服务链 B — 搜索/门户读面契约

> 日期：2026-08-17  
> Task：`DEMO-SVC-PY-MIDDLE-SEARCH-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）

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
| 说明 | 最小 Feign 契约 + Demo ADS 优先 / 无库 fallback mock；不扩 ES |

## 范围与实现

- 路由（`gkx_svc_service/views/search.py`）  
  - `POST /internal/gkx-svc/search/orgs`  
  - `POST /internal/gkx-svc/profile/get`  
  - `POST /internal/gkx-svc/portal/overview`  
  - `POST /internal/gkx-svc/portal/ranking`  
- 读库：`GKX_MYSQL_*` / `ENTAN_MYSQL_*` → `demo_gkxlumenx_ads.svc_org_profile_card` / `svc_rec_ranking`；拒非 `demo_`  
- 不可达：静态 `SVC-MOCK-*` fallback，始终带 `pending_client_confirm` + GAP Q-SVC-010  
- **非范围**：ES 全文、正式库、Java 模块、svcan 任务

## 偏离说明

- `lumen-topic-py` **`origin/dev` 受保护**，本叶与 BOOT 推送在 `feat/svc-middle-boot`（需人类开 MR 合入 `dev`）。handoff BOOT 同步注明。

## 产物清单

| 产物 | 路径 |
|------|------|
| repo | `repos/lumen-topic-py/gkx_svc_service/repo.py` |
| search views | `repos/lumen-topic-py/gkx_svc_service/views/search.py` |
| 测试扩展 | `repos/lumen-topic-py/tests/test_gkx_svc_boot.py` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-PY-MIDDLE-SEARCH-L01.md` |

## 验收证据

- [x] TestClient：search/portal/profile `code==0`
- [x] 有 Demo MySQL 时 `data_source=demo_ads`（本机已验）
- [x] 待核验诚实保留

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | Java→/internal | ✅ 契约就绪 |
| 6 | 仅 demo 库 | ✅ |
| D9 | 不伪闭合 | ✅ gap+pending |
| D12 | lumen-topic-py | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~4 万 |
| actual_cost | 估 <$2 |
| cost_warn | false |

## 联调确认

联调通过：搜索/门户/画像读面可给 Java Feign。下一叶同仓 `DEMO-SVC-PY-MIDDLE-TASK-L01`；并行仓 `DEMO-SVC-PY-SVCAN-BOOT-L01`；C 段 FACADE 依赖本叶。
