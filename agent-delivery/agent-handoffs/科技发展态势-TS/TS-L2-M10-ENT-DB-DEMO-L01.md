# TS-L2-M10-ENT-DB-DEMO-L01 · handoff

- 任务：`TS-L2-M10-ENT-DB-DEMO-L01`（data · M10「关键实体与关系」写回库迁至中台库）
- 日期：2026-11-10 · 监管：`human:刘剑锋` · 认领：`agent:data-agent`
- 依据：`agent-delivery/data/GDF/库边界-产线与中台-2026-10-19.md`（开发代码只连 `demo_gkxlumenx_*`，开发写入不进产线库 `gkxlumenx_*`）；孔东「维护页数据不走真实库」；监管人 2026-11-10 确认迁库。

## 问题

M10 写回链（`api/tech_graph_maintain_routes.py`）和 seed 脚本按 8 月 D12 口径把库名默认写死为产线库 `gkxlumenx_dwd` / `gkxlumenx_ads`。同服务 entan-py 其余功能在 lumen helm 里早已指向 `demo_gkxlumenx_*`（2026-10-20），M10 是唯一例外。冒烟写入和示范数据因此落在了 GDF 验收用的产线库。

## 改动

| 位置 | 内容 |
|---|---|
| lumen-algo-py `7176a44` | `_schemas()`：`GKX_M10_ENT_*_DB` → `ENTAN_MYSQL_*_DB`（lumen helm=demo_*）→ 默认 `demo_gkxlumenx_dwd/ads`；路由与 seed 两处一致；DDL 库名改为 demo_；单测 16/16 |
| MySQL 10.50.11.76 | 在 `demo_gkxlumenx_dwd/ads` 执行 DDL 建 12 张表（库内原无同名表；既有 `graph_node/graph_edge` 未动），按列名整表复制产线库现状 |
| helm | 不改。M10 直接跟随已配好的 `ENTAN_MYSQL_DWD_DB/ADS_DB`，无需 `helm:chart` |

复制核对（产线 / 中台）：technology_master 3/3，graph_change_set 21/21，graph_change_log 21/21，graph_version 22/22，graph_version_change_set 21/21，graph_tombstone 1/1，graph_entity_overlay 61/61，graph_entity_node 1/1，graph_entity_edge 60/60，其余空表 0/0。新代码本地读 R2：中台库与产线库输出逐字段一致（base_version=22）。

## 未做 / 待定

- **产线库 `gkxlumenx_*` 中 M10 残留表与数据未删**。清理属正式库写操作，需监管人另行确认。
- Java（topic Feign）、前端不涉及：Java 不直读这些表，只经 entan-py。

## 验收

- [ ] edu 部署生效后，页面一次挂接/解挂：中台库 `demo_gkxlumenx_dwd.graph_version` 版本 +1，产线库不变。
