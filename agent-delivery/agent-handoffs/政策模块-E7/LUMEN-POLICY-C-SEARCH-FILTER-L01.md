# LUMEN-POLICY-C-SEARCH-FILTER-L01 · 政策检索高级筛选透传

> 派单：[`LUMEN-POLICY-ADV-FILTER-派单说明.md`](./LUMEN-POLICY-ADV-FILTER-派单说明.md) §2  
> 逻辑依赖：`LUMEN-POLICY-PY-SEARCH-FILTER-L01`（2026-10-24 已到联调闸门，代码停在本地未发布。本叶仍未打到运行中的 Python，不把透传说成已通）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 开工前已认领并处于 `in_progress`。本叶不建单、不改状态、不 commit / push。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 沿现有 `GET /topic/v1/policy/search` 门面把查询参数改成多值原样转发，并加同一个只读选项路径。未新建 DTO，未在 Java 写筛选、未填词表、未解释 `CL-*`、未新增支持强度字段。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `mcp` |
| 说明 | `user-headroom` 已挂载。本叶无大段日志，未 compress。派单说明与 Python 路由按原文阅读。 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 未改图、未翻签。高级筛选与只读选项仍走已有边：浏览器 → 网关 `/policy/**` → `gkxlumen-topic-policy` → Feign `lumen-algo-py` `/internal/policy/**`。Java 不直连 DWD/ADS，不写 nGQL。 |
| 会签态 | `approved`（`storage/POLICY/01-data-flow.md` frontmatter；本叶不翻签） |
| 说明 | 工厂 ODS→GDF→DWD→ADS→`demo_gkx_chain` 拓扑未改。 |

## 格式参考（可选）

| 项 | 对齐来源 |
|----|---------|
| 章节结构 | templates/handoff-template.md |
| 范围边界 | 派单说明 §1–§2 |
| 时序图版式 | 无新时序图 |

## 问题清单

- 端到端未打到运行中的 Python。`LUMEN-POLICY-PY-SEARCH-FILTER-L01` 已在联调闸门，新参数只在本地工作区，没有发布、本叶也没有探测已加载的进程。
- 本机没有 JDK 17 / Maven，单测未执行。
- Feign 13.6 不会把 size=0 的查询集合写进 URL。Java 不删这个键；线上缺省与空列表在 Python 侧都是「不加该条件」。

## 修改内容

- `GET /topic/v1/policy/search` 的查询参数从 `Map<String, String>` 改为 `MultiValueMap<String, String>`，原样交给 `GET /internal/policy/search`。重复键不再被收成一个值。
- 新增 `GET /topic/v1/policy/search/options`，原样转发到 `GET /internal/policy/search/options`（level / status / policy_type 去重，以及该 `industry_code` 下的节点，都在这一条上，与当前 Python 一致）。
- Python 返回 HTTP 4xx 且 JSON 带 `code` 时，Java 用 `R.code=1` 带回 `msg` / `data`，不把拒绝改成空命中。5xx 与连接失败仍是 HTTP 200 + 诚实空 + `degraded=true`。
- 未新增 `support_strength` 字段。客户端若自己带上未知字段，Java 原样转发，由 Python 写入 `honesty.ignored_fields` 或按它的规则拒绝。

## 转发参数

原样转发，Java 不改写、不丢弃、不解释：

| 参数 | 说明 |
|------|------|
| `keyword` / `q` | 保持 |
| `publish_code` | 保持 |
| `industry_vid` | 保持 |
| `limit` / `offset` | 保持 |
| `publish_year_from` / `publish_year_to` | 新增，字符串原样转发 |
| `status` / `level` / `policy_type` / `region` / `ministry` | 重复参数保留，同字段或者由 Python 做 |
| `industry_code` | 可多个。`INB…` 与 `CL-*` 都原样转发。Java 不把 `CL-*` 当产业码展开 |
| 其它未知字段 | 原样转发（例如 `support_strength`）。Java 不拼进 `keyword` |
| 空列表 | 调用 Feign 前不删键、不填默认码。Feign 对 size=0 的集合不写 URL |
| 选项 `industry_code` | `GET /search/options` 上原样转发，供 Python 返回该码下的节点码与名称 |

## 测试结果

- 单测已写、未跑（本机无 JDK 17 / Maven）：
  - `PolicyFacadeControllerTest.searchKeepsRepeatedFiltersAndUnknownFields`：MockMvc 绑定后 `industry_code` 仍是 `INB170106`、`CL-01`、空串；level/status/policy_type/region/ministry 重复值都在；年份与 `support_strength` 在。
  - `PolicyFacadeControllerTest.searchOptionsForwardsIndustryCode`：`/search/options` 把 `INB170106` 与 `CL-09` 一起交给门面。
  - `PolicyFacadeServiceImplTest.searchForwardsFiltersWithoutRewritingIndustryCode`：交给 Feign 的是同一个 map；空列表键还在；`honesty.ignored_fields` 原样上送。
  - `PolicyFacadeServiceImplTest.searchRelaysPythonRejectForClusterCode`：Python `400` + `{code:1,msg,data:null}` 变成 `R.code=1`，`industry_code` 仍是 `CL-01`。
  - `PolicyFacadeServiceImplTest.searchOptionsForwardsIndustryCodeAndNodes`：选项响应里的 `nodes` 原样上送。
  - `PolicyFacadeServiceImplTest.searchOptionsFeignFailureDoesNotInventWords`：下游挂时 level/status/policy_type/nodes 皆空。
- Feign 路径断言：`name=lumen-algo-py`，`/internal/policy/search` 与 `/internal/policy/search/options`，url/path 不含 `demo-`。
- **不能证明参数已经到达运行中的 Python。** 只证明 Java 门面把多值查询原样交给 Feign 方法。查询串展开依赖 Feign 13.6（Iterable 会展开；空集合不进 URL）。

## 遗留风险

- PY 未到联调闸门前，现网 Python 若仍是旧签名，多出来的查询参数会被旧进程忽略或按未知字段处理，筛选不会生效。
- 带 `code` 的 4xx 现在返回 `R.code=1`（HTTP 仍是 200，与本门面其它接口一样用 `R` 包络）。这覆盖 `CL-*` 拒绝，也覆盖 Python 对其它非法值（如非法年份、非法 `industry_vid`）的 400。5xx 不走这条。
- 只读选项与节点名单都在 `/search/options`。不要再加 `/search/nodes`。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `dev`（本地改动，未 commit）
- commit：无
- pipeline URL / ID：无（未推送）
- 部署 namespace / 镜像 tag：未部署
- K8s rollout：未执行
- dev 测试 URL / 命令与结果：未打现网。预期入口仍是 `GET /policy/topic/v1/policy/search` 与 `GET /policy/topic/v1/policy/search/options`

## 可观测性（建议）

- OTEL_SERVICE_NAME：`gkxlumen-topic-policy-biz`（既有 Java Agent，本叶未改）
- traceId（dev 抽样）：无
- Tempo / Loki：随平台 Collector；本叶未抽样

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-topic-policy/gkxlumen-topic-policy-biz/src/main/java/com/topcomm/gkxlumen/topic/policy/controller/PolicyFacadeController.java`
- `repos/lumen-svc-platform/gkxlumen-topic-policy/gkxlumen-topic-policy-biz/src/main/java/com/topcomm/gkxlumen/topic/policy/service/PolicyFacadeService.java`
- `repos/lumen-svc-platform/gkxlumen-topic-policy/gkxlumen-topic-policy-biz/src/main/java/com/topcomm/gkxlumen/topic/policy/service/impl/PolicyFacadeServiceImpl.java`
- `repos/lumen-svc-platform/gkxlumen-topic-policy/gkxlumen-topic-policy-biz/src/main/java/com/topcomm/gkxlumen/topic/policy/feign/RemotePolicyPythonClient.java`
- `repos/lumen-svc-platform/gkxlumen-topic-policy/gkxlumen-topic-policy-api/src/main/java/com/topcomm/gkxlumen/topic/policy/api/feign/RemoteTopicPolicyService.java`
- `repos/lumen-svc-platform/gkxlumen-topic-policy/gkxlumen-topic-policy-biz/src/test/java/com/topcomm/gkxlumen/topic/policy/controller/PolicyFacadeControllerTest.java`
- `repos/lumen-svc-platform/gkxlumen-topic-policy/gkxlumen-topic-policy-biz/src/test/java/com/topcomm/gkxlumen/topic/policy/service/impl/PolicyFacadeServiceImplTest.java`

## 范围与实现

- 只动 `gkxlumen-topic-policy`。浏览器只到 Java；Java 只声明 `lumen-algo-py` 的 `/internal/policy/**`。
- 对照派单 §1：年份闭区间、同字段重复参数、多个 `industry_code`、未知字段、只读选项，都是转发，不是在 Java 里筛。

## 偏离说明

- 选项与节点没有拆成两个 Java 路径。当前 Python 是一条 `GET /internal/policy/search/options?industry_code=`，同时返回去重项和节点。
- 带 `code` 的 Python 4xx 改为拒绝体上送。此前 Feign 任何失败都收成空列表，会把 `CL-*` 拒绝伪装成「没有命中」。

## 产物清单

- 代码：本地工作区，未 commit
- 本文 handoff
- 流图：未改

## 验收证据

- 见「测试结果」。单测未执行。没有现网请求证据。

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ Java 无筛选 SQL / NLP |
| 前端→Java→Python `/internal/*` | ✅ `/internal/policy/search` 与 `/internal/policy/search/options` |
| 图谱 Nebula | ✅ 本叶不写 nGQL |
| 可观测 | ✅ 复用既有 Java Agent |
| CI/CD | ✅ 未 push；禁止 force |
| demo2 不 merge lumen | ✅ |
| 共享聚合 / 不直连 nGQL | ✅ |
| 数据策略 | ✅ Java 不填 fixture、不直连库 |
| D8 / D10 | N/A 无 UI |
| D9 | N/A 本叶无新统计数字；未知字段不在 Java 改口径 |
| D12 | ✅ Feign `name=lumen-algo-py`；未调用 `demo-*` 服务 |

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 无 Console 计数，不造数 |
| model_used | grok-4.7 |
| actual_cost | 未按公式计算（缺 in/out 精确值） |
| cost_warn | green |
