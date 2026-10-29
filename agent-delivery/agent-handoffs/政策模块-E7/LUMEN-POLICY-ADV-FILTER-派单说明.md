# 派单说明 · 政策查询高级筛选补齐

> 日期：2026-10-24
> 管线：[`LUMEN-POLICY-ABCDE-长任务总控.md`](./LUMEN-POLICY-ABCDE-长任务总控.md)
> 监管人：`human:淮政玮`。`claim_type=coordinator_dispatch`。总控「后续认领不必再问」仍有效，但**本文件只列计划，不建单、不认领、不开工**。
> 条数依据：[`qa/test-cases/SDWJSF-KJZTFWSFK/policy-政策分析/产业检索政策条数-20261024.md`](../../qa/test-cases/SDWJSF-KJZTFWSFK/policy-政策分析/产业检索政策条数-20261024.md)

界面参照企业查询高级筛选：`lumen-ui-topic` 的 `EnterpriseSearch.vue`、`FilterPanel`、`fixtures/enterprise/filterFieldSchema.ts`、`applyEntMetaToFieldLibrary.ts`。政策页已经用了同一个 `FilterPanel`，缺的是「字段进查询、筛不了的不假装命中」。

## 现状

| 已有 | 缺口 |
|---|---|
| `LUMEN-POLICY-D-POL-01C-L01` 已做 `/policy/search`，状态 `pending_test` | `dslToSearchQuery` 只把 `keyword` / `level` / `policy_type` / `region` / `ministry` / `publish_code` 传给 Java。`status`、`publish_year`、支持强度、关键词多选被拼进 `keyword` |
| Python `search_policies` 已能按 `industry_vid` 等值查 `demo_gkxlumenx_ads.policy_industry_rel` | 字段库没有产业集群 / 产业 / 产业节点。选产业码 `chain:INB170106` 命中不了其下 `segment:INB170106…` |
| 集群目录已有 `useIndustryClusters`（`cluster_id` + `l0[]`） | 查询不能把 `CL-*` 当链码。节点不在这份目录里 |
| 金路径 #1 多次冒烟 PASS | 只测了关键词「半导体」，没测高级筛选 |
| `LUMEN-POLICY-C-SEARCH-L01` | 注册表无此 ID。Java `gkxlumen-topic-policy` 已透传现有参数，本轮只加参数，不重做门面 |

同仓排队：`LUMEN-POLICY-D-POL-01-L01` 仍是 `in_progress`，占着 `lumen-ui-topic`。前端叶等它离开该仓再领。Python、Java 不占这个仓，可以先做。

不改：分析配置页（金路径 #2–#5）、门户政策扶持、支持强度口径（QPOL-02）、算子 `run()`。

## 本轮筛选条件

字段之间是并且。同一字段多选是或者。不实现任意条件分组。

| 界面字段 | 查询参数 | 数据 | 本轮 |
|---|---|---|---|
| 政策标题 | `keyword` | `title` / `keywords` / `abstract` | 保持 |
| 政策级别 | `level` | `policy_base_info.level` | 保持，补多选 |
| 政策类型 | `policy_type` | `ext1` | 保持，补多选。角标仍是 QPOL-01 |
| 所属地区 | `region` | `region` | 保持，补多选。省份不另造列，并进本字段 |
| 发布机关 | `ministry` | `publish_organization` | 保持 |
| 文号 | `publish_code` | `issued_number` | 保持 |
| 发布年份 | `publish_year_from` / `publish_year_to` | `publish_year` | 新增 |
| 时效状态 | `status` | `status` | 新增。选项只读库内去重，不沿用手写「已发布 / 即将失效 / 已撤销」 |
| 产业集群 | 不进 SQL | `industry_cluster` | 只用来收窄产业名单 |
| 产业 | `industry_code`（`INB…`，不要 `CL-*`） | `policy_industry_rel.industry_link_code` | 新增。命中 `chain:{码}` 以及 `segment:{码}` 开头的节点码 |
| 产业节点 | `industry_code` 传到节点全码 | 同上，等值 `segment:{节点码}` | 新增。节点名单只读链节点，不手写 |

不上筛、也不再拼进关键词：综合支持强度、资金扶持、税收优惠、土地供给、人才支持（QPOL-02，`factors` 不是筛列）。字段库里去掉这些项。手写关键词词表（合成生物、专项资金等）去掉。

产业命中规则：选集群且未选产业时，展开该集群映射里的全部 `INB` 码再按上表匹配。选产业时只匹配该码及其节点。选节点时只等值该 `segment:` 码。一条政策在结果里只出现一次。

## 顺序

```text
PY-SEARCH-FILTER  →  C-SEARCH-FILTER  →  （等 POL-01-L01 让出 lumen-ui-topic）
  →  D-POL-01C-FILTER  →  验收后推 dev、E0 发布  →  E-QA-SMOKE-FILTER
```

四张都还没建。开工时由 coordinator `task-create` 再认领。Epic `E-POLICY-PDR`。`supervised_by=human:淮政玮`。`depends_on` 按上表。完工停在本地，不自行 commit / push；专题仓人工验收闸门不因总控旧句自动推送。

---

## 1. 检索读面（先领）

```text
/goal algorithm-agent
身份：你是经验丰富、遵循最佳实践的资深算法工程师。只扩政策检索读面，不改算子方法。
强度：ponytail full
上下文：headroom 可选。search.py 与本派单说明必须读原文。
图：必含 POLICY-STORAGE-FLOW。只读 DWD policy_base_info 与 ADS policy_industry_rel，不改工厂边。

任务：LUMEN-POLICY-PY-SEARCH-FILTER-L01（开工前 task-create；本说明未建单）
标题：政策检索高级筛选参数
监管人：human:淮政玮
执行：agent:algorithm-agent
仓：${GKX_ROOT}/repos/lumen-algo-py，分支 dev。只改这个仓。
认领：claimed_by=agent:algorithm-agent，supervised_by=human:淮政玮，claim_type=coordinator_dispatch。

目标：GET /internal/policy/search 在现有 keyword、ministry、publish_code、level、policy_type、region、industry_vid、limit、offset 上增加：
- publish_year_from、publish_year_to（闭区间，空端不限制）
- status、level、policy_type、region、ministry 接受重复参数，同字段或者
- industry_code：INB 码。匹配 chain:{码} 等值，以及 segment:{码} 为前缀的关联行。禁止接收 CL-*。多个 industry_code 是或者
- 未知字段写入 honesty.ignored_fields，不得改写成 keyword
另给只读选项：level、status、policy_type 的库内去重，以及某 INB 码下的节点码与名称。选项来自 demo_gkxlumenx_*，不写死词表。

不做：不改 eval/、models/、打分函数；不写支持强度筛选；不让 Java 直连 MySQL。

DoD：
1. 上表新参数有请求就按列筛选；没有就与现在的检索一致。
2. 用产业检索政策条数-20261024 里至少一条有数的产业码（如 INB170106）能命中，且命中包含挂在其节点上的政策。
3. 传入 support_strength 时出现在 ignored_fields，结果不被关键词化。
4. handoff：agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-PY-SEARCH-FILTER-L01.md。ponytail: full。留一条可跑的自检。
```

## 2. Java 透传（PY 联调闸门之后）

```text
/goal api-agent
身份：你是经验丰富、遵循最佳实践的资深 Java 后端工程师。只做透传，不在 Java 写算法，不直连 nGQL，不填筛选 fixture。
强度：ponytail full
上下文：headroom 推荐。未挂载可跳过，handoff 注明 headroom: skip。
图：必含 POLICY-STORAGE-FLOW。浏览器只到 Java，Java 只打 lumen-algo-py /internal/policy/**。

任务：LUMEN-POLICY-C-SEARCH-FILTER-L01
标题：政策检索高级筛选透传
监管人：human:淮政玮
执行：agent:api-agent
depends_on：LUMEN-POLICY-PY-SEARCH-FILTER-L01 达到联调闸门（不等 done）
仓：${GKX_ROOT}/repos/lumen-svc-platform，只动 gkxlumen-topic-policy。分支 dev。
认领：claimed_by=agent:api-agent，supervised_by=human:淮政玮，claim_type=coordinator_dispatch。

目标：GET /topic/v1/policy/search 原样转发本说明第 1 节的新参数与选项接口。空列表保持空列表。不新增支持强度字段。不调用 demo-* 服务。

DoD：
1. 新参数能到达 Python，Java 不改写、不丢弃 industry_code。
2. CL-* 与未知字段的处理与 Python 一致（拒绝或 ignored_fields），Java 不自行解释集群。
3. handoff：agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-C-SEARCH-FILTER-L01.md。ponytail: full。
```

## 3. 查询页（让出 lumen-ui-topic 之后）

```text
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师。复刻企业高级筛选的交互，不另起一套控件。
强度：ponytail full
复刻：布局/交互/样式/评审/Mock 对照 EnterpriseSearch 的 FilterPanel 页，范围只限 /policy/search 高级筛选。见 templates/fe-replica-visual-dod.md。
范围清单：字段库、条件行、应用后检索、产业集群-产业-节点级联、结果仍走现有政策卡。不改分析配置页，不改详情抽屉。
上下文：headroom 可选。
图：必含 POLICY-STORAGE-FLOW。只调 Java。USE_MOCK=false 时禁止 fixture 填结果。

任务：LUMEN-POLICY-D-POL-01C-FILTER-L01
标题：政策查询高级筛选对齐企业字段进查询
监管人：human:淮政玮
执行：agent:frontend-agent
depends_on：LUMEN-POLICY-C-SEARCH-FILTER-L01 联调闸门。领取前确认 LUMEN-POLICY-D-POL-01-L01 已不再占用 lumen-ui-topic。
仓：${GKX_ROOT}/repos/lumen-ui-topic，分支 dev。
认领：claimed_by=agent:frontend-agent，supervised_by=human:淮政玮，claim_type=coordinator_dispatch。

目标：/policy/search 高级筛选只保留本说明「本轮筛选条件」表中的字段。dslToSearchQuery 按字段传参，禁止把 status、年份、产业、支持强度拼进 keyword。产业集群复用 useIndustryClusters，只作名单，查询键是 INB 码。节点选项走第 2 节的只读接口。支持强度四项从字段库删除。政策类型保留 QPOL-01 角标。卡片仍无「加入对比篮」「深度分析」。

DoD：
1. 选 INB170106（软件与信息服务）或条数材料中另一条有数产业，应用后请求带 industry_code，结果条数与该产业可检索政策一致（允许分页，total 对齐）。
2. 只选集群、不选产业时，请求不出现 CL-*。
3. 无命中是空态，不是 5xx。
4. pnpm type-check 通过。handoff 含 V1–V7。ponytail: full。
5. handoff：agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-D-POL-01C-FILTER-L01.md。
完工停本地，不自行 commit / push。
```

## 4. 金路径 #1 重跑（发布之后）

```text
/goal qa-agent
身份：你是经验丰富的测试工程师。只测已发布前端，不改代码。
强度：ponytail full

任务：LUMEN-POLICY-E-QA-SMOKE-FILTER-L01
标题：政策查询高级筛选冒烟
监管人：human:淮政玮
执行：agent:qa-agent
depends_on：D-POL-01C-FILTER 已推 dev，且 E0 点名 lumen-ui-topic、gkxlumen-topic-policy、lumen-algo-py 发布为绿。
环境：http://10.50.69.111:30892 的 /policy/search。禁止 localhost。

期望（未发生即红）：
1. 关键词「半导体」仍能出卡，卡上无「加入对比篮」「深度分析」。
2. 高级筛选选择条数材料中的一条有数产业（软件与信息服务或优势传统产业升级），应用后出卡，total 大于 0。
3. 选一个没有关联政策的节点，空态可见，响应不是 5xx。
4. 请求里没有 support_strength、fund、tax、land、talent，也没有 CL-*。

DoD：handoff 写 PASS/FAIL 与请求参数。失败先按长任务规约分 C1–C6，QA 不改代码。
handoff：agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-E-QA-SMOKE-FILTER-L01.md。
```
