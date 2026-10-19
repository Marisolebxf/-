# SCI-INT-Z02 handoff

- 任务：SCI-INT-Z02 · 角色：agent:architect-agent · 监管：human:淮政玮 · claim_type=coordinator_dispatch
- 对端：久新
- ponytail: N/A
- 日期：2026-10-19
- 会签结论：附条件通过
- 李伟清单：55
- 附条件：6
- 打回：0

## 范围

架构会签。核对 Z01 handoff 数字、总表「判据 / 勘误 / 结构升级项」、久新说明开头与「本管线未消费」行、总控 §5。未重做汇总。未改卡片 yaml，未改总表，未扫业务仓。

## 判据 1–5 核对

Z01 与总表「判据」一致：1 差集 0（P00 283 / A 段覆盖 283）；2 指标 93/93、模式不符 0；3 差集 0（B 引用 38、未消费 13）；4 检查 366、空链路 0；5 应覆盖 273、覆盖缺 0、契约降级缺 0。久新说明「本管线未消费」13 行，38+13=51。判据 6 由本叶完成。

## 铁律

1. 调用链：通过。判据 4 空链路 0；结构升级项 Java 列为 gkxlumen-* 只读门面，Python 列为 lumen-algo-py `/internal/*`；INT-C-TECH-425 写明 nGQL 只在 Python，INT-C-X-490 写明 Java 不直连 nGQL。
2. 图谱：通过。三表无 Neo4j；INT-C-X-490 落点为 NebulaGraph TRSGraph。
3. D12：附条件通过。勘误 7 条「正式落点」把 demo- 改记为 lumen-algo-py / gkxlumen ADS，未把 demo- 判通过；INT-C-X-490 正式空间仍写 demo_gkx_chain，括号标明正式 gkx_chain 待定。
4. 可观测：附条件通过。测试表 398 行仅 INT-D-X-003 的 java 列出现「透传 trace」，没有前端、Java、Python 三端 trace 检查点。
5. 算法只在 Python：通过。INT-C-TECH-429 / 430 的写者是 lumen-algo-py 图算法 Job；Java 列无算法实现。
6. 判据 6：通过。Z01 写「说明已齐，会签未做」；久新说明开头为待确认、会签未做；本叶完成会签。差集为 0，模式编号均在 IP-01…IP-13（结构升级项无非法编号；C01/C02 的 TBD 只记录、不发明编号）。

## 给 human:李伟

只列 C05 规范卡（escalate_to=human:李伟）。A/B 重复提法不单列。INT-C-X-476、INT-C-X-478 为复用且 structure_escalation=false，不进本清单。55 条：

- INT-C-TAL-400 · gkxlumenx_dim.talent_master
- INT-C-TAL-401 · gkxlumenx_dim.person_id_map
- INT-C-TAL-402 · gkxlumenx_ads.sci_talent_flow
- INT-C-TAL-403 · gkxlumenx_ads.sci_talent_override
- INT-C-TAL-404 · gkxlumenx_ads.sci_talent_relation
- INT-C-TAL-405 · gkxlumenx_ads.sci_talent_base
- INT-C-TAL-406 · gkxlumenx_ads.sci_talent_flow_od
- INT-C-TAL-407 · gkxlumenx_ads.sci_talent_ext
- INT-C-TECH-420 · gkxlumenx_dim.technology_master
- INT-C-TECH-421 · gkxlumenx_dim.tech_domain
- INT-C-TECH-422 · gkxlumenx_dim.map_tech_domain_anchor
- INT-C-TECH-423 · gkxlumenx_ads.sci_technology_doc_rel
- INT-C-TECH-424 · gkxlumenx_ads.sci_tech_relation
- INT-C-TECH-425 · gkxlumenx_ads.sci_graph_change_set
- INT-C-TECH-426 · gkxlumenx_ads.sci_graph_manual
- INT-C-TECH-427 · gkxlumenx_ads.sci_graph_change_log
- INT-C-TECH-428 · gkxlumenx_ads.sci_graph_version
- INT-C-TECH-429 · gkxlumenx_ads.sci_graph_metric_snapshot
- INT-C-TECH-430 · gkxlumenx_ads.sci_graph_path_snapshot
- INT-C-TECH-431 · gkxlumenx_ads.sci_tech_base
- INT-C-TECH-432 · gkxlumenx_ads.sci_region_tech_eval
- INT-C-TECH-433 · gkxlumenx_cfg.lumen_analysis_task
- INT-C-TECH-434 · gkxlumenx_cfg.sci_eval_param_template
- INT-C-ORG-440 · gkxlumenx_dim.research_org
- INT-C-ORG-441 · gkxlumenx_dim.map_org_alias
- INT-C-ORG-442 · gkxlumenx_ads.sci_rel_doc_org
- INT-C-ORG-443 · gkxlumenx_ads.sci_org_base
- INT-C-X-460 · gkxlumenx_ads.sci_graph_node
- INT-C-X-461 · gkxlumenx_ads.sci_graph_entity_membership
- INT-C-X-462 · gkxlumenx_ads.sci_graph_entity_override
- INT-C-X-463 · ES alias sci_factor
- INT-C-X-464 · gkxlumenx_ads.sci_achievement
- INT-C-X-465 · ES alias sci_achievement
- INT-C-X-466 · gkxlumenx_ads.sci_factor_geo
- INT-C-X-467 · gkxlumenx_ods.user_layer_fill
- INT-C-X-468 · gkxlumenx_cfg.layer_datasource
- INT-C-X-469 · gkxlumenx_cfg.sys_user_layer_group
- INT-C-X-470 · gkxlumenx_cfg.sys_user_favorite
- INT-C-X-471 · gkxlumenx_cfg.sys_user_subscription
- INT-C-X-472 · gkxlumenx_ads.sci_kpi_agg
- INT-C-X-474 · gkxlumenx_dim.code_region
- INT-C-X-475 · gkxlumenx_dim.region_scope
- INT-C-X-477 · gkxlumenx_dim.map_region_alias
- INT-C-X-480 · gkxlumenx_ads.sci_result_snapshot
- INT-C-X-481 · Redis jx_api_cache
- INT-C-X-482 · gkxlumenx_cfg.sci_snapshot_version
- INT-C-X-490 · NebulaGraph TRSGraph space demo_gkx_chain
- INT-C-X-491 · gkxlumenx_ads.sci_index_rank_snapshot
- INT-C-TECH-492 · gkxlumenx_ads.sci_tech_graph_node_metric
- INT-C-X-493 · gkxlumenx_ads.sci_async_task
- INT-C-TECH-494 · gkxlumenx_ads.sci_tech_stat_preagg
- INT-C-ORG-495 · gkxlumenx_ads.sci_org_perf_query
- INT-C-ORG-496 · gkxlumenx_ads.sci_carrier_index
- INT-C-X-497 · gkxlumenx_ads.sci_city_index
- INT-C-X-498 · gkxlumenx_ads.sci_innov_spatial

## 不挡本次分析会签、挡上线

不重开 A/B 叶。

1. 铁律 3：勘误 7 条把 demo- 改记为 lumen；INT-C-X-490 正式图空间仍为 demo_gkx_chain（gkx_chain 待定）。
2. 铁律 4：测试卡未要求前端、Java、Python 三端 trace 检查点。
3. 甲方未拍板：久新说明确认状态一律为待确认。
4. 供应方主键未齐。
5. DN-D01-01 测试库落点。
6. A09 的 INT-A-X-0817 标 IP-10，B08 的 INT-B-ORG-704 为 IP-08；总表指标行以 B08 为准（勘误「模式」）。

## 打回

无。差集为 0，模式编号未越出 IP-01…IP-13，正式落点未把 demo- 判通过。

## 产物

- `agent-delivery/agent-handoffs/展示系统三要素集成-SCI-INT/SCI-INT-Z02.md`

未改业务仓。未 commit，未 push。未点 done。

## 架构合规

- 调用链：前端 → Java REST → Python `/internal` → 久新 / ADS / TRSGraph。Java 不做算法、不写 nGQL。✅（附条件见铁律 4 可观测）
- Nebula 只作 TRSGraph。三表无 Neo4j。✅
- 算法只在 Python。✅
- D12：正式落点改记 lumen；demo_gkx_chain 待定，未判通过。附条件 ✅
- 可观测：测试卡三端 trace 检查点未齐，挡上线。附条件 ✅

## 成本

- actual_tokens: 95000
- model_used: grok-4.7
- actual_cost: 2.40
- cost_warn: green

ponytail: N/A
