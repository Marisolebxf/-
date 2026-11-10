# 603-STRUCT-FDE · 波次 C · 知会 · api

总单：`POL-L2-PC1-STRUCT-FDE-L01`。身份：`agent:api-agent`。日期：2026-11-10。  
定档：**轻**（`603-STRUCT-FDE-B-读法方案.md`）。本波不经 api 改实现。

## 知悉

- **复用既有抽取**：治理页「结构化抽取」只调已有 `POST /display/v1/policy/parse/clauses`（body `policy_id`）；`PolicyParseController` / Service **本轮不改**实现。
- **不新开第三条资源**：摘要 / 看板主读仍 `GET …/governance/results?policyId=`；不拆新公开路径、不改 OpenAPI 字段表。
- **element 不动**：`governance/results`（含 `policySummary.hasClauses`）实现不变；抽完再拉同资源刷新即可。
- **影响清单**：已读 B §5——`STRUCT-API` 与 ARCH 同批声明复用即可；本知会不另改正文。

无异议、无停机项。
