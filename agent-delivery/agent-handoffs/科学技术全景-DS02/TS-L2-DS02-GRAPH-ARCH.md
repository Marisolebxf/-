# TS-L2-DS02-GRAPH-ARCH · 科学技术全景 · 展示技术点图谱 · 架构 as-built

ponytail: off（定义任务）

## 任务认领

| 字段 | 值 |
|---|---|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 派单直写。本单不改 task-registry |
| 说明 | as-built 稿已落盘，待四角色会签，未签收。不标 done |

## Ponytail

ponytail: off（定义任务）

不缩文档。未用 YAGNI 跳过调用链、空态、上限和 D12。

## 图即契约

| 字段 | 值 |
|---|---|
| diagram_id | `TS-L2-DS02-GRAPH-SEQ`、`TS-L2-DS02-GRAPH-DATA` |
| 图 diff | 在说明书 §3 调用图上补 as-built 的子学科字典跳（display → `lumen-topic-py` `/internal/gkx-svc/dict/query`）。数据图只画 `tech_point`、`tech_rel` 两类 |
| 会签态 | 源文件无 frontmatter，记 `draft` |
| 说明 | 图在 `sdd/l2/TS-L2-DS02-GRAPH-ARCH.md` 第 2、3 节 |

## 范围与实现

需规二级「展示技术点图谱」，序号 17–21。菜单 `/trend/tech-panorama`。对照说明书 §2.1、§3、§4、§6、§7 与 `功能拆解.md` 17–21。

按已实现代码写：调用链（页 → 网关 `/display/**` → `gkxlumen-display` → `lumen-algo-py` `POST /internal/tech-graph/read` → `demo_gkx_chain`）、数据流、边界、空态与失败态（200 `GRAPH_EMPTY` / 502 / 501）、上限（未选 200 点不带边；选中后关系 200）、现状（截至 2026-11-05）。

## 偏离

无设计偏离，本稿不改说明书决策。as-built 与说明书有四处不一致，已写进分册第 6 节，交会签：

1. 领域筛选改成子学科多选，经 `lumen-topic-py` 换技术点编号，不读挂产业表；另有 `POST .../subfields`。
2. display 下发选中点用 `techPointId`，Python 只认 `technology_node_id` / `technologyNodeId`，选中点到不了 Python。
3. Java 不透传 Python 的 `truncated`，截断标记丢失。
4. `IndexNotFound` 被当空，查询缺口表现为空态。

## 产物清单

- `agent-delivery/agent-handoffs/科学技术全景-DS02/sdd/l2/TS-L2-DS02-GRAPH-ARCH.md`
- 本 handoff

## 验收证据

- 分册已落盘，含两张 Mermaid、空态失败态表、上限表、偏离表、现状小节。
- 只读核对：`lumen-algo-py` `a03c52b` / `4e7f453` / `07ffa9f`；`lumen-svc-platform` `cbd6f10` / `271109c`；`lumen-ui-science-pc` `e6fb1dd` / `b603e63` / `5e6e96e`。三仓相关文件工作区无未提交改动。
- 定义单，无业务代码，无 PR，无 CI。未 commit。

## 架构合规自检

| 公约 §2 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ Java 只装配，不算结构、强度、中心度 |
| 2 调用链 | ✅ 前端 → Java REST → Python `/internal/*`。子学科字典也是 Java → Python `/internal/gkx-svc/dict/query`，不越层 |
| 3 图谱 Nebula | ✅ 只读 `demo_gkx_chain`，不用 Neo4j |
| 4 可观测 | ✅ 沿用 display Java Agent、Python `TraceHeaderMiddleware`、前端 `createTraceId`。本稿不新设观测点 |
| 5 CI/CD | ✅ 定义稿，`cicd: skip` |
| 6 demo2 只读 merge | ✅ 未 merge 任何 demo 产物 |
| 7 共享聚合核心 | ✅ 前端只调 Java；Java 不写 nGQL；分数只读 ADS |
| 8 数据策略 | ✅ 不用 fixture 填图；点未写入时空 |
| 9 D8 | ✅ 不改页面区域与 token |
| 10 D9 | ⚠️ 本二级不挂 `metric_id`。详情抽屉「中心度」卡无 ⓘ / MockBadge，见 METRIC 分册第 3 节，待会签 |
| 11 D10 | ✅ 交互在页面内，不改 |
| 12 D12 | ✅ 不调用 `demo-*`，不经 `gkxlumen-graph`，Feign 名 `lumen-platform-algo-py`、`gkxlumen-platform-search-py` |
| 13 D14 | ✅ 不写对象存储 |
| 14 D16 | ✅ 不用 `gapfill_` 表 |
| 15 D17 | ✅ 不改锁定合规算法 |
| 16 D18 | ✅ 中心度只读 `ads_technology_panorama_score`，接口不返回写死分数 |

## Cost 回填

| 字段 | 值 |
|---|---|
| actual_tokens | 25000（估算） |
| model_used | claude-opus |
| actual_cost | 0.68 |
| cost_warn | green |

按 C 档 `$15/$75`、80/20：`25000×0.8×15/1e6 + 25000×0.2×75/1e6 = 0.675`，记 `0.68`。本单不写 registry，由 coordinator 回填。

## 未做事项

- 未改代码、库、task-registry；未 commit，未 push。
- 未在线上复测读图，未核镜像与 rollout。
- 未修上面四处不一致，只记录。
