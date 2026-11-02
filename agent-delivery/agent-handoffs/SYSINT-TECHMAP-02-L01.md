# SYSINT-TECHMAP-02-L01 · 技术节点与产业关联：落实可同步表与新建 DWD

> 范围真源：`agent-delivery/工程过程/04-系统集成/02-对接三要素/方案-SYSINT-TECHMAP-02-L01.md`（以 `origin/dev` 已推送正文为准）。2026-10-31 用户下令分三步执行，同日下令完成任务。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 开工时按 data-agent 花名册默认写成徐滕强。2026-10-31 用户纠正为淮政玮。依赖 `SYSINT-SURVEY-02-L01` 当时仍是 `in_progress`，用户明令已认领。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 方案正文按定义任务写，不缩。编码沿用已有字典通道、gkx-innov 写库和 lumen-algo-py 已有客户端。未新加 npm / Maven / pip 包。未跳过调用链、可观测和本 handoff。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无。调用方向写在方案正文，没有单独 Mermaid |
| 图 diff | 未改图 |
| 会签态 | 方案未标 `approved`。按用户开工令和完成令收口，不把会签态改绿 |
| 说明 | 同步走已有字典，关联走 `lumen-algo-py` `/internal`，查询只读本侧表。Java 不写向量 |

## 范围与实现

技术路线锁定为候选技术节点，主键 `technology_node_id`。正式 `tech_id`、路径、簇群、子学科都不是这条主键。

可同步的只有久新 `ads_technology_profile`（约 19,430 行）。论文、专利、边、路径、簇群、评估结果不同步。`ads_technology_commercial_value_simulation` 不能当主数据。政策证据和正式目录还没有。

一个菜单「技术节点与产业映射」，与「子学科与专题映射」并列。按钮是【同步】【关联】。打开页面和查询不触发这两步。结果表 `dwd_tech_node_industry_map`。现网读写都落在 `demo_gkxlumenx_dwd`。不写入 `subfield_topic_map`。

中文名原样进 `name_zh`，英文进 `name_en`。空中文不抄英文。未关联的节点保留一行，`node_id` 为空。

已推送的关联是名称向量最近邻：人点击才算。一次请求最多 20 个尚未关联的节点，页面点一次可以连续多批；整批一条都没写上就停下。每个技术点用名称向量，和本批候选产业节点的向量做余弦，只留最近的一条。候选带产业名称和集群名称。`node_id` 只从这批候选里出。向量服务不可用就整批失败，不编造关联。Java 不写向量。已经映射上的行不重算。

列表合成一张表。已映射产业可以统计，并按节点反查。统计行带已映射的产业节点名称。

全景「主流技术路线」改读这张表。表空时显示「暂无已发布主流技术路线」，不再用子学科名称充技术路线。

## 偏离

派单原文写「本叶只出记录，不写同步代码」。2026-10-31 用户把执行改成三步：出方案、开发到算法中台、纠正已上 lumen 的全景。代码按这个命令写了。

方案初稿允许一个技术节点对应多条产业关联。后续提交收成每个技术节点只留一条最近关联。本收口不回退这些提交。

编排仓 `6c919236` 把方案正文改成名称向量最近邻。算法仓 `dcb5edc`、页面 `dfeaf3c` 已按这个口径推上 `origin/dev`。

GDF 上的同语义两过程另开 `SYSINT-06-20-L01`，不并进本叶，本叶也不把它标成已跑。

本叶没有把约 1.9 万个节点同步进表，也没有点过【关联】灌数。菜单和网关路由已经能接到服务。全景在表有关联行之前保持空态。

## 产物清单

均在各仓 `origin/dev`。

| 仓 | commit | 内容 |
|---|---|---|
| `lumen-algo-py` | `da0bc57`、`c2c073c`、`dcb5edc` | 关联只在 Python。`dcb5edc` 起改为名称向量余弦，每个技术节点只留最近的一个产业节点 |
| `lumen-topic-py` | `a955c7c` | 字典 `op=technology_node_page`，空中文不抄英文 |
| `demo-svc-platform` | `894d80e`、`58c28d4`、`ac32e3f`、`952af2e` | 同步写入映射表；候选改为产业名称和集群名称；每节点只留一条关联；统计行带产业节点名称 |
| `demo-ui-system-test` | `309a0c3`、`4f20f6c`、`52a40ed`、`1abb1f6`、`dfeaf3c` | 菜单 `/ops/tech-node-map`；一次连续多批关联；统计与按节点反查；列表合成一张表；提示改为向量最近邻 |
| `lumen-svc-platform` | `e41b995`、`8b79c0e` | 全景改读映射表；测试按注解原文查找 `@Value` |
| `lumen-ui-topic` | `5fd876e` | 卡片主键改为 `technology_node_id` |
| `gkx-orchestration` | `acd0a525`、`6c919236` | 监管人改为淮政玮；方案正文改成名称向量最近邻 |

网关：`/ops/v1/tech-node-maps` 与 `/**` 转到 `gkx-innov`，过滤器为空。路由在 `gkxx.sys_route_conf`，也在当前网关缓存。未登录访问返回 424，不再是网关 404。

## 测试结果

- 更早一次在当时版本上：`tests/test_tech_node_industry_link.py` 2 通过，空中文名用例 1 通过。
- `dcb5edc` 的 `tests/test_tech_node_industry_link.py` 4 个用例通过：无候选失败、最近候选、同分留第一条、空批次不向量化。
- `lumen-svc-platform`：`IndustryClusterSchemaBindTest` 曾因最后一个 `@Value` 被新库名盖住而红，`8b79c0e` 按注解原文查找。本收口没有重查该流水线。
- 本收口没有再点【同步】【关联】，也没有重开浏览器走全景。

## 验收证据

2026-10-31 用户下令完成。代码在各仓 `origin/dev`。网关抽查：`GET /api/ops/v1/tech-node-maps/stats` 为 424 `token expired`，带 `X-Trace-Id`。证据路径即本 handoff。签收操作人仍是 human:淮政玮，本叶不自签 `done`。

## 架构合规自检

- ✅ 调用链：算法中台 → demo 网关 → gkx-innov；同步再走字典；关联再走 `lumen-algo-py` `/internal`
- ✅ 算法只在 Python。Java 不写向量，不直连向量服务
- ✅ 图谱：本叶不写图库
- ✅ 可观测：沿用已有 Java / Python 应用。网关 404 那次的 trace 是 `63ac65198c6b245300d81e750c15768a`，请求没有离开网关
- ✅ D12：lumen 全景只读本侧映射表，不调久新，不调 demo 服务
- ✅ 不把企业当成科研机构。不把英文抄进中文名
- ✅ 维护页统计不加指标 ⓘ。全景卡片沿用页上已有追溯，本叶不新造口径

## 遗留

- 表还没有这批技术节点的同步和关联行。全景在有行之前是空态。
- `SYSINT-06-20-L01` 仍是 backlog，GDF 作业未建。监管人仍是徐滕强，本条不改。
- `lumen-svc-platform` 的 `8b79c0e` 流水线本收口未复看。
- 线上要等 `lumen-algo-py` 的 `dcb5edc` 发版后，页面【关联】才会按向量匹配。已经映射上的行不会重算。

## Cost 回填

没有 Console 精确数。按会话量级估算，价表没有 Grok 档，沿用主力档（输入 $3/M、输出 $15/M，75/25）。

- actual_tokens: 200000
- model_used: grok-4.7
- actual_cost: 1.20
- cost_warn: green

ponytail: full
