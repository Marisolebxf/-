# DEMO-SVC-SEED-MOCK-ENRICH-L01 · Demo MOCK 补全贴合原型

> 日期：2026-08-17  
> Task：`DEMO-SVC-SEED-MOCK-ENRICH-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）  
> 用户诉求：已通页面补 MOCK，使门户/查询内容更完整贴合原型

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 seed 脚本与 ADS 表；不改 DDL、不扩 Job 白名单 |

## 范围与实现

- **灌数**：`demo-algo-ent-analysis` `scripts/seed_svc_demo_mock.py` → batch `svc-mock-20260818`
  - 对齐 `demo-ui-topic` `SERVICE_ORGS` **24** 家机构
  - DWD：`service_org` / type_tag / chain_rel / org_rel
  - ADS：`svc_org_profile_card`×24（`ext_json` 含 type/segment/foundedYear/fieldNames/patents/experts/cases/standards）
  - ADS：`svc_rec_ranking` ATTRACT×8 + CULTIVATE×8
  - 全部 `verification_status=pending_client_confirm`；GAP Q-SVC-010 保留
- **读面**：`lumen-topic-py` `gkx_svc_service/repo.py` 展开 `ext_json` → 查询卡字段；修正 `total` 为 COUNT
- **非范围**：正式库；WORKSPACE 深 Job；Q-SVC-010 闭合

## 偏离说明

- 无。`service_type_primary` 改为原型中文机构类型（企业/高校/科研院所），以贴合查询卡 `type` 展示。

## 产物清单

| 产物 | 路径 / 提交 |
|------|-------------|
| 种子脚本 | `repos/demo-algo-ent-analysis` `c44f319` |
| 读面展开 | `repos/lumen-topic-py` `053d092` |
| live 灌数 | Demo ADS/DWD batch `svc-mock-20260818` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-SEED-MOCK-ENRICH-L01.md` |

## 验收证据

- [x] live：`svc_org_profile_card` SVC-MOCK-* = **24**；name_cn UTF-8 校验「华大基因科技服务」
- [x] ranking ATTRACT/CULTIVATE 各 8
- [x] 外网 overview `data_source=demo_ads` · `org_in_pool=24`（灌数后即时）
- [ ] search-py 发布后 patents/segment 等字段透出（pipeline `5147` / `deploy:search-py` `22512`）
- [x] 零写正式 `gkxlumenx_*`

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 调用链 | FE→Java→Python | ✅ 未越层 |
| demo 不污染正式 | ✅ |
| D9 待核验不伪闭合 | ✅ pending + GAP |
| D12 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~45000 |
| actual_cost | 估 <$3 |
| cost_warn | false |

## 联调确认

联调通过：Demo MOCK 密度已对齐原型 24 家；门户 KPI=24 可读。等 search-py `053d092` 发布后查询卡五维字段完整透出。
