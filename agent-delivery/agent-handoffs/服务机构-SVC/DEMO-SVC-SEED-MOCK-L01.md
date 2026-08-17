# DEMO-SVC-SEED-MOCK-L01 · 产业服务链 A — Demo 最小 MOCK 灌数

> 日期：2026-08-17  
> Task：`DEMO-SVC-SEED-MOCK-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md`（已授权 · human:侯佳伟）

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
| 说明 | 最小种子脚本 + 复用 ODS 取样；顺带修 DDL APPLY 标记粘连导致 `service_org` 未建 |

## 范围与实现

- **缺列修复**：`apply_svc_demo_ddl.py --rebuild-mismatch` 将旧同名表旁路为 `*_legacy_pre_svc`，并修 CREATE 解析（marker 残留不再吞掉首表）
- **灌数**：`scripts/seed_svc_demo_mock.py` → batch `svc-mock-20260817`
  - DWD：`service_org`×3 + type_tag + chain_rel + org_rel(COOPERATE)
  - ADS：`svc_org_profile_card`×3 + `svc_rec_ranking`×1
  - 全部 `verification_status=pending_client_confirm`；ext/note 标 mock+GAP（Q-SVC-010 未关）
- **对照**：`miss_control_org_id=demo-org-tw` 不入池（SEED-02）
- **非范围**：正式库；规则正文；Q-SVC-010 关闭

## 偏离说明

- Demo 库原 `service_org` / `service_org_financing` 为 ENT 旁路旧列；`CREATE IF NOT EXISTS` 未覆盖。本叶旁路重建，旧表保留为 `*_legacy_pre_svc`（仅 demo）。

## 产物清单

| 产物 | 路径 |
|------|------|
| 种子脚本 | `repos/demo-algo-ent-analysis/scripts/seed_svc_demo_mock.py` |
| DDL APPLY（含 rebuild） | `repos/demo-algo-ent-analysis/scripts/apply_svc_demo_ddl.py` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-SEED-MOCK-L01.md` |

## 验收证据

- [x] live：`SVC-MOCK-001..003` 在 `demo_gkxlumenx_dwd.service_org`
- [x] ADS profile + ranking 同 batch
- [x] 零写正式 `gkxlumenx_*`
- [x] 待核验态诚实保留

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 6 | demo 不污染正式 | ✅ |
| 8 | ADS | ✅ Demo ADS 样例 |
| D9 | 待核验不伪闭合 | ✅ pending + GAP |
| D12 | 正式路径隔离 | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~3 万 |
| actual_cost | 估 <$2 |
| cost_warn | false |

## 联调确认

联调通过：Demo DWD/ADS 可读 MOCK 圈定池；下游 B MIDDLE 可接空态/样例。下一叶：`DEMO-SVC-PY-MIDDLE-BOOT-L01`。
