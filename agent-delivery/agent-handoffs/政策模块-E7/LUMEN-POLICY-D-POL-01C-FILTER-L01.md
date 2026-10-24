# LUMEN-POLICY-D-POL-01C-FILTER-L01 · 政策查询高级筛选对齐企业字段进查询

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 2026-10-24 监管人放行：Java 透传到 Python 的校验先滤过，前端按合同做完，线上 total 对齐由监管人统一处理。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用现有 FilterPanel 与 `useIndustryClusters`。不新造筛选控件，不改分析配置页。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶未调用 headroom。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `POLICY-STORAGE-FLOW` |
| 图 diff | 未改图。浏览器仍只到 Java `GET /policy/topic/v1/policy/search` 与 `/search/options`。 |
| 会签态 | 未改图，不新填会签态。 |
| 说明 | 产业集群不进查询参数。产业与节点只传 `INB` 码。 |

## 范围

`lumen-ui-topic` `/policy/search` 高级筛选。字段库、条件到查询参数、产业集群收窄产业名单、节点走只读选项。结果卡、详情抽屉、分析配置页未改。

## 实现

- `dslToSearchQuery` 按字段传 `level` / `policy_type` / `region` / `ministry` / `status` / `publish_year_from` / `publish_year_to` / `industry_code`。同字段多值保留为数组，请求序列化成重复查询键。
- 只选集群时，展开该集群 `l0` 里的 `INB` 码。选了产业则只传产业码。选了节点则只传节点码。`CL-*` 不进请求。
- `status`、年份、产业、支持强度不再拼进 `keyword`。
- 字段库去掉综合支持强度、资金、税收、土地、人才，以及手写关键词词表。省份并进所属地区，不再单列。政策类型保留 QPOL-01。
- 级别、时效、类型、节点选项来自 `GET /policy/topic/v1/policy/search/options`。接口失败时选项为空，不回退「已发布 / 即将失效 / 已撤销」。

## 偏离

线上 `industry_code=INB170106` 的 `total` 对齐未做。监管人明确：Java 透传校验先滤过，发布后统一处理。本叶停在本地，未 commit、未 push。

## 验收

| 项 | 结果 |
|----|------|
| `node src/views/policy/policySearchModel.selfcheck.mjs` | 通过。覆盖多选级别、只选集群不出现 `CL-*`、产业码、节点码、年份闭区间、支持强度不进 keyword。 |
| `vue-tsc --build` | 退出码 0。 |
| 浏览器走查 / 线上 total | 未做。代码未发布。 |
| V1–V7 | 沿用现有政策查询页皮肤与结果卡，本叶只改字段库和参数。未改卡片布局。 |
| R1–R5 | 仍用 FilterPanel / SearchHub / `@/review` 的 `POLICY-SEARCH-ADVANCED-TRACE`。`USE_MOCK=false` 不填检索 fixture。 |
| 空态 | 检索无命中仍走现有空态，不把下游失败改成 5xx。 |

## 产物

- `repos/lumen-ui-topic/src/views/policy/policySearchModel.ts`
- `repos/lumen-ui-topic/src/views/policy/policySearchModel.selfcheck.mjs`
- `repos/lumen-ui-topic/src/views/policy/PolicySearchPage.vue`
- `repos/lumen-ui-topic/src/api/policy/index.ts`
- `repos/lumen-ui-topic/src/api/policy/types.ts`
- `repos/lumen-ui-topic/src/api/policy/paths.ts`

## 架构合规

调用链仍是浏览器 → Java `/policy/topic/v1/policy/**`。未直连 Python，未调用 `demo-*` 服务。
