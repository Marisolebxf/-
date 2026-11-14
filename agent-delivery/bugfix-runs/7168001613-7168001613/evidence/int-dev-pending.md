# integration 证据：dev 部署后补验（SKIPPED 说明）

本地（Windows 开发机）无 K8s/网关/Python 服务运行环境，三仓全链路联调无法本地执行。

## 已完成的替代验证
- 契约字段名双侧对照：前端 `chain_code`/`chain_codes`（EntMetaRequest/EntDistributionRequest 类型）↔ Java `@JsonProperty("chain_code"/"chain_codes")`（对照仓内 EnterpriseStatsRegionRequest 同款约定）↔ Python `body["chain_code"]/body["chain_codes"]`（`_chain_codes_from`）
- 三仓各自单侧验证全绿（见 EV-IMPL-SELFTEST-V2）

## dev 部署后补验步骤
1. CI 部署 dev（push 已触发）
2. `curl -X POST <gateway>/gkxlumen/topic/enterprise/stats/overview/industry-kpi -d '{"chain_code":"INB13"}'` → 断言 enterprise_total < 全局 189115
3. 前端 /enterprise/development 选「新能源」→ KPI 卡、排名高亮、趋势、分布地图全部随链收窄
