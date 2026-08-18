# 产业服务链（SVC）· Gate-1 全量派单包（已授权）

> **日期**：2026-08-18  
> **授权**：`human:侯佳伟`（`DEMO-SVC-FULL-底座后全量-长任务总控.md` · 后续认领不必再问）  
> **Gate-0**：外网已绿（见下）→ 本包开 Gate-1  
> **目标站**：http://111.198.38.90:50892/  
> **对标**：`demo-ui-topic` service-portal / service-center  
> **强度**：ponytail full（coding 叶）

## Gate-0 放行证据（2026-08-18）

| 项 | 结果 |
|----|------|
| Demo batch | `svc-gate0-20260818` · profile/service_org=35 |
| search-py | `9b86f81` · deploy job **22686** success |
| overview | `trend`×8 · `scale_dist`×4 · `by_service_type`×3 · kpi.org_in_pool=35 |
| search | total=35 · patents/segment 等卡面字段齐 |
| 50100 | 端口为算法台 SPA；与 50892 共用 Demo ADS，不挡 Gate-0 |

## 叶清单（一次建齐）

| 序 | ID | Agent | 仓 | 依赖 | 一句话 |
|----|----|-------|-----|------|--------|
| 1 | `DEMO-SVC-PY-PORTAL-AGG-L01` | algorithm-agent | lumen-topic-py | Gate-0 | 门户 sections 补齐（产业/区域/深圳/能力） |
| 2 | `LUMEN-SVC-JAVA-PORTAL-EXT-L01` | api-agent | lumen-svc-platform | 1（可并行探） | Feign/门面透传扩展字段 |
| 3 | `LUMEN-SVC-FE-PORTAL-FULL-L01` | frontend-agent | lumen-ui-topic | 1+2 | 五 Tab + 产业级联 + 有数图 |
| 4 | `LUMEN-SVC-JAVA-JOB-WHITELIST-L01` | api-agent | lumen-svc-platform | — | Job 白名单按分析页扩 |
| 5 | `DEMO-SVC-PY-SVCAN-MODELS-L01` | algorithm-agent | lumen-algo-py | 4 | 短板/技术力读 ADS 出结果 |
| 6 | `LUMEN-SVC-FE-ANALYSIS-FULL-L01` | frontend-agent | lumen-ui-topic | 4+5 | 分析/生态/招引有数 |
| 7 | `LUMEN-SVC-E-FULL-SMOKE-L01` | qa-agent | devops+qa | 3+6 | 金路径有数冒烟 |

**监管**：一律 `supervised_by=human:侯佳伟` · `claim_type=coordinator_dispatch` · lock 24h。

## 金路径（有数才绿）

1. overview：级联可选；趋势≥2；类型环；规模四档  
2. industry / region / shenzhen：主图有数  
3. search：total≥池；卡面 segment/patents  
4. 分析三视图：可点 + 结果或诚实 Job 态  
5. 短板或招引：终态可解释  

## 执行纪律

- 只写 demo_*；FE→Java→Python；D12；Q-SVC-010 待核验不伪闭合  
- 同仓 Convoy 串行；lumen push `origin/dev`  
- 每叶 handoff + cost；Gate-1 完成前不开「全量完成」话术  

## 首波认领（本轮）

1. `DEMO-SVC-PY-PORTAL-AGG-L01` → algorithm-agent  
2. `LUMEN-SVC-JAVA-PORTAL-EXT-L01` → api-agent（探现有透传是否已够）  
3. 其后 FE / Job / svcan 按依赖升 ready 后认领  
