# 派单说明 · KG-GRAPH-API-04（包 D · 燕大 · 展示图接口实现）

> 2026-11-13。淮政玮派。P0，第一批。**这是「有契约没实现」的空档**：T12 的 23 项契约签得很漂亮，但至今没有一个端点能调。
> 一句话：按你自己签的 T12 契约，把 12 个可用端点实现出来，走案 2（燕大服务），Java 只透传。

```text
/goal api-agent
身份：你是接口实现工程师，最熟悉 T12 契约（本单执行人就是 T12 作者）。本单只做实现，不改契约字段。禁止用 ponytail 删减端点，禁止用 headroom compress 代替精读 T12 契约原文。

任务：KG-GRAPH-API-04
标题：展示图接口实现（41 + 428/432/435/437 + 400–407）
Epic：E-SCI-INT
优先级：P0
类型：feature
负责人：human:李周（监管 human:淮政玮）。claimed_by=human:李周 或 agent:api-agent，supervised_by=human:淮政玮。
状态：ready。依赖 KG-GRAPH-COVER-01、KG-GRAPH-RECALC-02（榜单数据面）。
同时接手：KG-COMPLY-LOAD-T14（41 的关键实体推荐读接口），本单即 T14 的实质执行，建单时把 T14 并入本单或在 T14 上挂本单号。
仓：gkx-orchestration（契约表与 curl）+ lumen-algo-py（Python /internal）+ lumen-svc-platform（Java 透传）。前端不在本单。
完成日期要求：2026-11-18（P0 窗口，必须早于系统测试 11-19）。

强度：medium。

架构定案（不改）：
- 走案 2：燕大服务出 `/internal/kg/*`，Java 只透传，不写 nGQL。
- 对外前缀：`/api/kg/*`（Java 网关），对内：`/internal/kg/*`（Python）。
- 三态照 T12：`status` + `reason.code` + `availability`（missing/deferred/unreachable）；501 用 `unsupported.code`。
- 取数原则：**在线只做单点/小范围查询；榜单与大聚合读 RECALC-02 归档 JSON，不在线算。**

范围（12 个可用端点 + 4 个 501）：

一、中心性与社群（读归档，不从图里现算）
1. `GET /api/kg/metrics/degree`（428）：分页整榜 19,430 点；`topN` 是每页条数，默认 20，正整数；游标续页，末页 `nextCursor=null`；`meta.scope=full_graph`；`degreeBasis=weight_sum_incident`。
2. `GET /api/kg/metrics/closeness`（429）、`/betweenness`（430）、`/pagerank`（431）：同结构，读 RECALC-02 对应归档。
3. `GET /api/kg/metrics/composite`（432）：1,500 点等权榜；返回 raw{degree,pagerank,closeness,betweenness}、normalized、weights 固定 0.25（契约常量，不从归档取）。
4. `GET /api/kg/community/{id}`（435）：社群属性（规模/内部边/平均度/密度/核心点）。
5. `GET /api/kg/community/view`（437）：社群划分可视化载荷（社群号 + 代表点 + 边）。

二、分析展示（400–407）
6. `GET /api/kg/search`（400）：关键词/实体属性/时间范围检索；分页排序。
7. `GET /api/kg/search/filters`（401）：地域/时间/技术分类/作者/合作关系多维过滤；**维度无数据的返回 `availability=missing`，不返回假 0**。
8. `GET /api/kg/analyze`（402）：按 dim=institution|field|year|cooperate 切片；每维返回计数与 Top 子集。
9. `GET /api/kg/visualize`（403）：返回 nodes/edges 载荷，供前端网络图直接渲染；子图上限 500 点，超限返回 `truncated=true` 与总数。
10. `GET /api/kg/cluster`（406）：复用 437 社群结果做分类聚类，**不新写聚类算法**。

三、维护管理 41（**不新建端点，改为验收**）
11. 41「关键实体推荐列表」：我方 M10 R1 已实现（`TS-L2-M10-ENT-PY-IMPL-01`，pending_test）。按 PLAT-09 裁定，**以 M10 R1 为准**；本单只做「读接口一致性验收」——用 T14 的 B 档脚本验接口 200、契约字段齐全、有数非空、排序筛选可用，并把差异写清。**不新建第二套推荐端点，不做推荐模型。**

四、501（不许返回空数组冒充可用）
12. `GET /api/kg/mode-detect`（404）、`/predict`（405）、`/recommend/user`（407）：501，`unsupported.code=NO_MODEL`，`reason` 写明「本期未训练模型」。
13. `GET /api/kg/community/evolution`（436）：501，`unsupported.code=MULTI_SNAPSHOT_REQUIRED`，写明「只有单份快照」。

五、实现规矩
1. 每个端点必须有 `dry_run`（返回将执行什么，不取数）。
2. 每个端点必须有 `meta.metric_source`（space/快照起止/nodes_sha256/edges_sha256/method/formula）。
3. Java 侧：网关 `kg` 路由插在 catch-all 之前；只透传，不拼 nGQL；禁止直连 graphd。
4. 压测：按 T12 §5 阈值跑，至少覆盖 428 整榜续页、437 社群视图两个重档；结果写进交付文档。
5. 契约表落 `对接文档/我方/KG-GRAPH-API-04-端点清单.md`：每端点一行（方法/路径/入参/出参/状态码/数据来源/空态条件）。

主文路径（新建）：
agent-delivery/工程过程/04-系统集成/07-图数据库集成/派单-20261113-图谱100/KG-GRAPH-API-04-实现与联调.md
端点清单、经网关 curl 输出、压测结果同目录。

Handoff：
agent-delivery/agent-handoffs/KG-GRAPH-API-04.md
写清：12 个可用端点 + 4 个 501 的 curl 证据、压测数据、未完成项、与 T12 契约的差异（应为 0）。
evidence 指向主文。task-update-status 到 integration，不写 done。

禁止：
- 改 T12 契约字段名、结构、三态枚举。
- 在线现算大图中心性/社群（读归档）。
- 404/405/407/436 返回空数组或 200 冒充可用。
- 41 的 `reasons` 留空或编造分数。
- Java 直连 nGQL、catch-all 抢路由、直连 Python 写图。
- 把口令、连接串写进 git。
```

---

## 附：为什么要「读归档」而不是「现算」

T09 的中介中心性在 54 万条边上跑过一次；如果每个请求都现算，一个用户点两下就把 graphd 打死（现在内存已经 80%）。**预计算 + 接口读榜**是 T09 已经验证过的模式，本单沿用，不创新。
