# DEMO-SVC-BASE-GATE0-L01 · SVC 契约底座（ODS 圈定 → DWD/ADS）

> 日期：2026-08-18  
> Task：`DEMO-SVC-BASE-GATE0-L01`  
> 总控：`DEMO-SVC-FULL-底座后全量-长任务总控.md`（已授权 · human:侯佳伟）

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
| 说明 | 重写灌数主路径；不扩 Job 白名单；不伪闭合 Q-SVC-010 |

## 范围与实现

1. **决策表**：Q-SVC-010 🔴→🟡 项目基线（Demo：`name_cn`+`industry_l*` 关键词；无 `business_scope`）；同步 Q-SVCCHAIN-06 / Q060 临时文案。  
2. **DDL**：`storage/SVC/etl/demo_gkxlumenx_dwd_svc_tables.sql` 已含 `svc_metric_fact/series/dist`、`svc_region_dist`、`svc_tech_power_score`、`svc_chain_gap_score`；live APPLY 成功。  
3. **灌数**：`demo-algo-ent-analysis/entan/svcseed.py`  
   - `connect("svc")` + `assert_demo_mysql_targets`  
   - Demo ODS 关键词圈定 → 契约 DWD/ADS  
   - batch `svc-gate0-20260818` · rule `svc_rule_demo_kw_v1` · 一律 `pending_client_confirm`  
   - 趋势 series 缩放至 2025=89600（mock+scaled）  
   - 技术力五维等权 + org_id 确定性代理  
4. **50100 读面**：`api/svc_routes.py` `/v1/svc/indicators` 改读契约表。  
5. **50892 中间层**：`lumen-topic-py/gkx_svc_service/repo.py` overview 挂 `trend` / `scale_dist` / 类型分布。

## 偏离说明

- Demo ODS **无** `business_scope`：匹配面降级为名称+产业字段（已写入决策表）。  
- 类型/规模展示：名称无高校/院所线索时用 hash 混出三类型；规模四档一律 hash（`org_size` 不作主路径），标 mock。

## 产物清单

| 产物 | 路径 |
|------|------|
| 总控 | `agent-handoffs/服务机构-SVC/DEMO-SVC-FULL-底座后全量-长任务总控.md` |
| DDL | `data/data-design/storage/SVC/etl/demo_gkxlumenx_dwd_svc_tables.sql` |
| seed | `repos/demo-algo-ent-analysis/entan/svcseed.py` |
| indicators | `repos/demo-algo-ent-analysis/api/svc_routes.py` |
| overview | `repos/lumen-topic-py/gkx_svc_service/repo.py` |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-BASE-GATE0-L01.md` |

## 验收证据

- [x] live：`service_org` / `svc_org_profile_card` = **35**；全部 `pending_client_confirm`  
- [x] `svc_tech_power_score`=35；`svc_rec_ranking`=40；`svc_metric_series` 趋势 8 点（2025=89600）  
- [x] `svc_metric_dist`：类型 3 档 + 规模 4 档；`svc_region_dist` 有城/区  
- [x] `svc_chain_gap_score`=3；零写正式 `gkxlumenx_*`  
- [x] 外网 50892 overview：`trend`×8 + `scale_dist`×4 + `by_service_type`；kpi.org_in_pool=35（search-py `9b86f81` · deploy **22686**）  
- [x] 外网 search：total=35；卡面含 patents/segment  
- [x] 50100：端口为算法台 SPA；与 50892 共用 Demo ADS，不挡 Gate-0  

## 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 调用链 FE→Java→Python | ✅ 未越层 |
| 只写 demo_* | ✅ |
| Q-SVC-010 待核验 | ✅ |
| D12 | ✅ |
| 契约单真源 | ✅ 旧 layout 表不再作为 seed 真源 |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~80000 |
| actual_cost | 估 <$5 |
| cost_warn | false |

## 联调确认

联调通过：Gate-0 外网绿（2026-08-18）。Gate-1 已开，见 `DEMO-SVC-GATE1-全量派单.md`。