# TS-L2-DS02-ARCH-SIGNOFF-ARCH · 科学技术全景 · 架构会签

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 对象：`TS-L2-DS02-ARCH`
- 监管：`human:淮政玮`
- 对照：父说明书 `科学技术全景-系统详细设计说明书.md`、`功能拆解.md`、需规 `科学技术全景.md`（序号 17–47）。本页不改架构稿，不改说明书，不改代码，不改 task-registry

## 结论

不同意会签

第 2 节调用图、同节正文、说明书第 3 节不是同一条调用链。接口单无法选定 Java 下游。

要改的段落：

1. 第 2 节 Mermaid（`flowchart LR`）。`gkxlumen-display` 与图之间必须画出 `lumen-algo-py` 的 `POST /internal/tech-graph/read`，下一跳才是空间 `demo_gkx_chain`。三个数字仍由 display 按编号只读 `ads_technology_panorama_score`。同节正文要写上：不经 `gkxlumen-graph`；不调用任何 `demo-*` 服务；空间不是 `demo_gkx_chain` 就拒绝，不改去 `gkx_chain` 或 `entan`。
2. 第 2 节末段上限。选中技术点之后，关系最多 200 条，默认只要高、中证据。与说明书第 3 节对齐。未选点最多 200 个技术点且不带边、每类实体最多 20、路径最多 20、超出截断，这几句保持。

第 3 节数据流图与说明书第 4 节同口径，表示数据从哪来，不是运行时服务跳。不要求把这张图改成调用链。

## 核对

| 项 | 架构稿 | 判定 |
|---|---|---|
| 浏览器只打 `POST /display/v1/situation/panorama/graph`；网关 `/display/**` → `gkxlumen-display`；Java 不写算法、不写 nGQL、不直连图库、不经 `gkxlumen-graph` | 第 2 节正文写浏览器只打这一次 `graph`。图上有网关 `/display/**` 和 `gkxlumen-display`。正文写 display 不直连图库、不在请求里现算关系、Java 不写 nGQL。全文没有「不经 `gkxlumen-graph`」。第 2 节图从 display 直接连到「已准备好的技术点图」 | 正文的 URL 与「不直连图库、不写 nGQL」一致。图与「不经 `gkxlumen-graph`」不一致。接口单不能从这张图定下游 |
| 图只读 `demo_gkx_chain`，经 Python `POST /internal/tech-graph/read`；空间不对就拒绝；lumen 不调用 `demo-*`（D12） | 第 2 节正文写「图由 Python 只读 `demo_gkx_chain`。空间不是这个就拒绝」。第 8 节写不改去 `gkx_chain` 或 `entan`。没有内部路径，没有 `lumen-algo-py`，没有「不调用 `demo-*`」。说明书第 3 节是 display → `lumen-algo-py` `POST /internal/tech-graph/read` → `demo_gkx_chain`，并写明不经 `gkxlumen-graph` | 不一致。空间名写对了，服务跳没锁死。`demo_gkx_chain` 是图空间，不是 `demo-*` 服务；稿未禁止把这一跳落到 `demo-*` 或 `gkxlumen-graph` |
| 一次返回七个已有字段，不增第八块 | 第 2 节：`nodes`、`relations`、`keyPathOptions`、`timeline`、`listRecords`、`relationTypeOptions`、`factorItems`。三个功能分用，不拆三套接口。第 6 节不改字段名。与说明书第 3 节相同 | 一致 |
| 展示只做序号 17–33。34–40 不落库不建单。41–47 归维护管理。入图是第 2 项，不是本页写入 | 第 1 节与第 5 节末行。34–40 报价划掉、不落库、本页不提供增删改。41–47 菜单 `/trend/tech-situation-maintain`。入图、边上图、挂产业在 WBS-02-19 / 02-20 / 02-21。与功能拆解、说明书第 1、2.4 节相同。需规文件仍保留 34–47 的功能描述，范围裁剪以功能拆解为准 | 一致 |
| D18：三个数字只新建 `ads_technology_panorama_score`，Python 灌 mock 行，Java 只读。禁止接口直接返回写死 mock。`USE_MOCK=false` 时不用 fixture。读失败不回退种子。空图是 `GRAPH_EMPTY`，不用 `GRAPH_NOT_READY` 冒充已接入 | 开篇与第 7 节写明表名、库（现读 ADS 同库，不进 ODS / DWD / 供应方库，不用 `gapfill_`）、行种类 `influence` / `centrality` / `path_priority`、灌数方为 Python 且不在 `graph` 请求里写、读取为同一次 `graph` 按编号只读、无行则该格空、D4 保持 mock 并留 MockBadge。第 2、3、6 节：读失败不用演示种子填画布；不把 `mock/modules/panorama.ts` 的节点灌进图；接入前空壳可以是 `GRAPH_NOT_READY`，接入后空图用 `GRAPH_EMPTY`，读失败不用空壳冒充成功。图上 display → 分数表这一跳与「Java 只读 ADS」相同 | 一致 |
| 上限：未选点 ≤200 技术点且不带边；选中后关系 ≤200（默认高/中）、每类实体 ≤20、路径 ≤20，超出截断 | 第 2 节末段：未选点最多 200 个技术点、不铺边；选中后默认高/中证据、低证据须用户明确要求；每类实体最多 20；路径最多 20；超出标明截断。没有「关系最多 200 条」。说明书第 3 节有这一句 | 不一致。其余上限一致。读图单会看到两套关系上限 |
| 序号 17 与 26 是 501。19 / 32 / 33 是页面内交互。不新造 `metric_id`。不把 IPC4 / 深圳卡位函数挂到本页 | 第 4.1 节第 4 步、第 4.2 节第 5 步、第 5 节：17 写请求 501，26 返回 501；19 不另发请求；32 在已取回路径上并排或重叠；33 按步播放，不按 `currentYear` 换图。第 7 节不新造 ID，不调用已在册计算；三个数字只用 `M_TECH_ENTITY_INFLUENCE`、`M_TECH_PATH_CENTRALITY`、`M_TECH_PATH_PRIORITY` 作列身份，行不是 IPC4 PageRank 或深圳卡位函数的输出，未由 `human:唐绍祖` 另签前 D4 不得改 live。与功能拆解、说明书第 2、5 节相同 | 一致 |
| 第 2 节 Mermaid、正文、说明书是否同一条调用链 | 见本表前两行。第 3 节数据流图与说明书第 4 节相同 | 调用图不一致，作为阻塞。数据流图一致 |
| 现码是否已经走通这条链（只读抽查，不改代码） | `lumen-ui-science-pc` 的 `fetchPanoramaGraph` 打 `POST /display/v1/situation/panorama/graph`，空形状是上述七个字段。`gkxlumen-display` 的 `SituationPanoramaController` 返回七个空数组和 `emptyReason=GRAPH_NOT_READY`。该方法不调 Python，不引用 `gkxlumen-graph`，不写 `gkx_chain` 或 `entan` | 与第 6 节「接入前空壳」相符。现码不能代替第 2 节把 Python 只读画出来 |

## 铁律

1. 算法只在 Python。正文写 Java 不在这次请求里现算关系、不写 nGQL。三个数字没有真模型，不在请求里算。通过。第 2 节图把读图画成 display 直达技术点图，读图这一跳不通过，并入第 2 条。
2. 调用链应是浏览器 → 网关 `/display/**` → `gkxlumen-display` → `lumen-algo-py` `POST /internal/tech-graph/read` → `demo_gkx_chain`；分数表由 Java 只读。第 2 节图没有 Python，也没有内部路径。不通过。
3. 图谱空间只读 `demo_gkx_chain`，不是 `gkx_chain` 或 `entan`。正文第 2、8 节写了拒绝条件。通过。服务名未锁，见第 4 条。
4. D12。正式下游只能是 lumen 服务。稿没有写 `lumen-algo-py`，没有写不调用 `demo-*`，没有写不经 `gkxlumen-graph`。按第 2 节图可以实现成 Java 直连图库。不通过。
5. D14。本叶不写对象存储，不新建桶，前端不直连 RustFS。通过。
6. D17。不改唐绍祖锁定算法的调用闭包，不把 IPC4 / 深圳卡位函数挂到本页，不新造 `metric_id`，D4 保持 mock。通过。
7. D18。表名、灌数方、读取接口齐全。禁止接口直接返回写死 mock。读失败不回退 `mock/modules/panorama.ts`。接入后空图用 `GRAPH_EMPTY`。通过。
8. D8。不新开页面，不重做 `FE-TS-02A`，不改七个字段名和三个区域。本定义单不改视觉 token。通过。
9. 序号 17、26 为 501；19、32、33 在页面内完成。通过。
10. 未选点 200 且不带边、实体每类 20、路径 20、超出截断、默认高/中证据。通过。选中后关系 200 条未写入第 2 节末段。不通过。

## 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。上面点名的第 2 节未改之前，本页维持不同意会签。同意会签不是签收。

## 第二轮（2026-11-05 返工后）

- 角色：`agent:arch-agent`
- 日期：2026-11-05
- 监管：`human:淮政玮`
- 对象：返工后的 `TS-L2-DS02-ARCH` 第 2 节。本轮只核第一轮点名的两处。不改架构稿，不改说明书，不改代码，不改 task-registry
- 对照：说明书第 3 节调用链与上限

### 结论

同意会签

### 核对

| 项 | 返工后的架构稿第 2 节 | 判定 |
|---|---|---|
| Mermaid 为页 → 网关 `/display/**` → `gkxlumen-display` → `lumen-algo-py` `POST /internal/tech-graph/read` → `demo_gkx_chain`；分数仍由 display 只读 `ads_technology_panorama_score` | `flowchart LR`：`page` → `gw` → `bff`；`bff` 以「技术点、关系、实体名单、路径步」连到 `py`（`lumen-algo-py` / `POST /internal/tech-graph/read`）再连到 `graph`（`demo_gkx_chain`）；`bff` 以「影响力、中心度、路径优先级」连到 `score`（`ads_technology_panorama_score`）。与说明书第 3 节同一条跳 | 一致 |
| 正文写不经 `gkxlumen-graph`、不调用 `demo-*`、空间不是 `demo_gkx_chain` 就拒绝且不改去 `gkx_chain` 或 `entan` | 同节正文：display 不直连图库，不经 `gkxlumen-graph`，不调用任何 `demo-*` 服务；图由 `lumen-algo-py` 的 `POST /internal/tech-graph/read` 只读 `demo_gkx_chain`；空间不是 `demo_gkx_chain` 就拒绝，不改去 `gkx_chain` 或 `entan`；Java 不写 nGQL。与说明书第 3 节同口径，并写明不调用 `demo-*` | 一致 |
| 选中后关系最多 200 条，默认高/中证据 | 末段：选中一个点之后，该点的关系最多 200 条（默认只要高、中证据；用户明确要低证据才带上）。未选点最多 200 个且不铺边，每类实体最多 20，路径最多 20，超出标明截断。与说明书第 3 节相同 | 一致 |

### 签收边界

本页不把任务标 done，签收仍由 human:淮政玮 做。同意会签不是签收。
