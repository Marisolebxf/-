# 服务机构维 · 现网加工链路与分场景流程图

```yaml
---
doc_id: SVC-ASBUILT-PROCESS-CHAIN
element: SVC
role: asbuilt-process
status: draft
version: "2026-11-02"
updated: "2026-11-02"
task_id: SYSINT-06-21-01-L02
input_handoff: agent-delivery/agent-handoffs/SYSINT-06-21-01-L01.md
signoff_status: pending
signoff_note: "新图。不写入 01-data-flow.md §1 已会签工厂拓扑。01-data-flow 的 signoff_status 仍是 approved。"
---
```

> 输入是 `SYSINT-06-21-01-L01` 的现网核对（2026-11-02）和本目录已有存储设计。本文件不建表、不灌数、不建 GDF 作业。  
> 缺口写「未闭合」。调研里没有的表不编造。未跑通不写成已跑通。  
> 指标库查询（域 `SVC` / 产业服务，2026-11-02）返回 51 条。其中 `M_SVC_BASE_101_1` 是基础指标的整体过程，不是一条指标，对照表已去掉。叶指标 50 条。D1–D4 不是 8 件套字段。

## 1. 一条加工链路

服务机构现在能对上的加工，是 **Python 在 demo 库上分三次人工触发**，再加上 **一次 ES 同步** 和 **一条内容运营接口**。GDF 作业不存在。正式库同名表是空的。

圈定从 `demo_gkxlumenx_ods.dwd_org_base_info` 读机构（`org_id` 非空且未删，2026-11-02 该表 189116 行）。规则 `svc_rule_demo_kw_v1.1`。同一作业还读 ODS 的 `dwd_org_financing_info`、`dwd_org_invest_info`，以及年报 `dwd_org_annual_financial_info` 的最新一行（只要 `org_id` / `year` / `employees_number` / `operating_revenue` 这些列存在）。年报缺行时，人数和营收只在内存里合成，**不写回 ODS**。合成占比本叶未数，未闭合。

写入只允许 `demo_` 开头的库。`assert_demo_mysql_targets` 拒绝 `gkxlumenx_ods` / `gkxlumenx_dwd` / `gkxlumenx_ads`。触发是人手调用 `POST /internal/svc/run-pipeline`（`append` 或 `replace`），或命令行 `python -m entan.svcseed`。仓库里未见定时任务。50100「灌数据」按钮在存储设计里是同一引擎的界面入口；L01 核对到的批次是接口/命令写出的记录，没有单独证明那一次点击来自 50100 页面。

这一次写入的是：

| 库.表 | 2026-11-02 行数 | 批次 |
|---|---:|---|
| `demo_gkxlumenx_dwd.svc_org_circle` | 43296 | `svc-fseed-20261020`，圈定写入 2026-10-20 11:57 |
| `demo_gkxlumenx_ads.svc_org_card` | 43296 | 卡面 `update_time` 最晚 2026-10-22 23:17 |
| `demo_gkxlumenx_dwd.svc_org_finance_event` | 15755 | 同一次圈定 |
| `demo_gkxlumenx_ads` 的 `svc_metric_fact` / `svc_metric_series` / `svc_metric_dist` / `svc_region_dist` | 同一次写入 | 分 `metric_id` 行数未单列，未闭合 |

卡面六类候选：INNOV 29321，空 9650，FINANCE 2062，CONSULT 1387，MKT 570，HR 210，IP 96。圈定池、投融资事件、图谱挂表这三张 DWD 的逐步加工见 §1.1。

十模型是 **另一次** `POST /internal/svc/run-models`，不在 `run-pipeline` 里。它读 circle / card，写 `demo_gkxlumenx_ads`：`svc_tech_power_score` 400 行（批次 `svcmodels_20261022_212916` 300 行，`aaa_fill_fill_20261022_profile` 100 行），`svc_attraction_recommend` 50，`svc_cultivation_recommend` 50，`svc_chain_gap` 6，`svc_relation_chain` 51。不是 43296 家全量。技术力行按六类 `model_id` 拆开的行数，L01 未单列，未闭合。

图谱是 **再另一次**。入口包括 `POST /internal/svc/run-graph`，以及 `POST /internal/svc/graph/{ner|intra|hang}`。空请求默认 `dry_run=true`，不落库。`run-pipeline` 不进这条。NER 写点：删掉本 space 下这些 `org_id` 的 hang 再插入，`written_edges` 为空，然后尝试向 Nebula 写 Tag。Nebula 失败时来源记成 `ads`，不报假成功。intra 才把同城同环节的机构对记成 `participates`，`mapped_from=cooperation`，写进 `svc_org_graph_hang.ext.peers`。批次号前缀 `svcgraph_` 是这组 op 共用的，不能把 peers 单独说成 NER 函数写出。

2026-11-02 hang 表 `demo_gkxlumenx_dwd.svc_org_graph_hang` 43296 行，`space_name=demo_gkx_chain`，`tag_name=institution`，VID `institution:{org_id}`，批次 `svcgraph_20261030_022647`（2026-10-30 02:27–02:52）。ext 里 33861 行有 `peers`，边名 `participates`，对端前缀 `institution:`。`belongs_to` 是 0，`service_provide` 是 0，`segment:` / `chain:` / `ent:` 是 0。图库 graphd `10.50.75.136:9669` 本机超时，Tag `institution` 在图里有没有行，**未闭合**。不能把 hang 的 43296 行写成图库已经写入。

`service_provide` 不在服务机构图谱允许边里（允许的是 `belongs_to` / `participates` / `supplies` / `depends_on`）。企业合作代码在 `partner_type=service_org` 时会写边 `service_provide`，点类型是 `service`，不是 `institution`。它先写 ADS `graph_node` / `graph_edge`，再走企业图谱装载。禁止从服务机构 `run-pipeline` 进入。现网 demo ADS `graph_edge` 的 `relation_type` 只有 `cooperate`（94827 行），没有这三条边。`demo_gkxlumenx_dwd.graph_edge` 是另一小图（event / scholar / org / domain），不是这套挂表。

检索索引不在圈定作业里。`lumen-etl-es-py` 作业名 `service_org`：先 `POST /internal/etl/indexes/svc-org` 建物理索引 `gkx_svc_org_v1` 并绑别名 `gkx_svc_org`，再 `POST /internal/etl/svc-org` 灌文档。五路连接是卡面 `svc_org_card`、圈定 `svc_org_circle`、技术力 `svc_tech_power_score`（同一 `org_id` 取当前最大批次最高分）、ODS `dwd_org_industry_tags`（`company_name = card.name_cn`）、DWD `enterprise_patent_history`（按 `org_id` 求和 `patent_valid_count`）。没有名叫 `svc_org_tech` / `svc_org_tags` / `svc_org_patent` 的表。配置默认三套库都是 `demo_gkxlumenx_*`。仓库里未见定时任务。水位在 `gkxlumenx_cfg.es_sync_watermark`，`module_name=svc_org_card`，只有一条：`last_sync_time=2026-10-20 14:23:49`，`last_sync_count=43296`。别名文档数 43296，与当天 demo 卡面行数一致。正式库卡面是 0 行，解释不了这 43296 篇。本叶没有拿到当时进程的环境变量，没有把「默认配置」写成「那次进程必然读了 demo」。卡面在 2026-10-22 还有更新，索引没有第二条水位。

内容运营不写 ADS，也不写 `svc_org_circle`。写接口在 `lumen-svc-platform` 的 `ServiceOrgService`，落到 `gkxlumenx_cms.cms_entity_overlay`，`entity_type=SVC`（2026-11-02 该类型 7 行）。`gkxlumenx_cms.cms_svc_business_domain` 已建，0 行。读视图 `gkxlumenx_cms.v_cms_svc` 43299 行：从 `demo_gkxlumenx_dwd.svc_org_circle` 左连 `demo_gkxlumenx_ads.svc_org_card`，再左连 overlay；虚拟机构走 overlay 的另一段 `UNION`。这是运营覆盖，不是圈定加工。

专题读路径在 `lumen-topic-py/gkx_svc_service/repo.py`，只读，库名必须匹配 `demo_*_ads` / `demo_*_dwd`，默认 `demo_gkxlumenx_ads`。不写 ADS。

正式库 `gkxlumenx_ads` / `gkxlumenx_dwd` 里同名服务机构表已建（约 2026-10-14），自增仍是 1，行数是 0，`update_time` 为空。`gkxlumenx_ads.graph_node` / `graph_edge`、`gkxlumenx_dwd.graph_node` / `graph_edge`、`gkxlumenx_dwd.enterprise_patent_history` 也是 0 行。`gkxlumenx_ods.dwd_org_base_info` 189116 行，与 demo ODS 行数相同；服务机构灌数不写这张表。`gkxlumenx_ods.dwd_org_industry_tags` 1000 行，不是服务机构作业写入的证据。仓内 DDL 只写 `demo_gkxlumenx_*`。谁执行了正式库建表，未闭合。

GDF 派单包里没有这条加工。GDF 不直写图库。本叶也未见 GDF 写 `demo_gkx_chain`。GDF 团队执行派单时只操作 `gkxlumenx_*`。那一步还没有作业，不能写成已跑通。企业 v4 里的 `org_type=service_org` 是企业类型枚举，不是本链路。

`gkxlumenx_ods.dwd_org_base_info` 与 demo 同为 189116 行。本叶没有逐行比对，未闭合。

### 1.1 服务机构 DWD 怎么加工出来

服务机构 DWD 是 `demo_gkxlumenx_dwd` 里的三张挂表：`svc_org_circle`（圈定池）、`svc_org_finance_event`（投融资事件）、`svc_org_graph_hang`（图谱挂表）。供方贴源表名也带 `dwd_`，物理库是 `demo_gkxlumenx_ods`。那是圈定的原料，不是这三张结果表。机构名称、地区、行业、人数、营收写在 ADS 卡面 `svc_org_card`。

`diagram_id=SVC-PROC-LOGIC-DWD-20261102`

```mermaid
flowchart TB
  ODS["读 demo_gkxlumenx_ods.dwd_org_base_info<br/>org_id 非空且未删"]
  RULE["规则 svc_rule_demo_kw_v1.1<br/>should_circle 圈定从宽"]
  MODE["append：已有 org_id 不重复插入<br/>replace：先清空再全量写入"]
  CIR["demo_gkxlumenx_dwd.svc_org_circle<br/>org_id + 圈定元数据"]
  CLS["classify 写六类候选<br/>对不上则候选为空"]
  FIN["融资表、投资表<br/>只挂本批要写的 org_id"]
  EVT["demo_gkxlumenx_dwd.svc_org_finance_event"]
  ANN["年报最新一行，缺行只在内存合成"]
  CARD["demo_gkxlumenx_ads.svc_org_card"]
  HANG["另一次图谱作业"]
  GH["demo_gkxlumenx_dwd.svc_org_graph_hang"]

  ODS --> RULE --> MODE --> CIR
  CIR --> CLS
  CIR --> FIN --> EVT
  CIR --> ANN --> CARD
  CIR --> HANG --> GH
```

圈定池和投融资事件由同一次 `run-pipeline` / `python -m entan.svcseed` 写出。代码在 `demo-algo-ent-analysis/entan/svcseed.py`。写入前先执行仓内 `scripts/mysql/svc_ddl_demo_empty.sql`，连接目标仍须是 `demo_` 前缀。图谱挂表不在这次作业里。

**圈定池**

1. 读 `dwd_org_base_info`。条件是 `org_id` 非空；表上有 `is_deleted` 时只留 `0`。读出的列限于：`org_id`、`name_cn`、省市区、`industry`、行业四层名称和代码、`business_scope`、成立日期和成立年、`org_size`、`is_deleted`。列不存在就跳过该列。2026-11-02 这张源表 189116 行。
2. 用 `should_circle` 决定谁进池。规则号 `svc_rule_demo_kw_v1.1`，词表在同文件的 `CLASS_INDUSTRY`、`NAME_TIGHT`、`CIRCLE_WIDE_EXTRA`，说明见 `seeds/svc_rule_demo_kw_v1.md`。
   - 行业列或经营范围里有字：一级行业等于「科学研究和技术服务业」，或一级行业含「金融」，或行业/经营范围命中六类词，或命中放宽词「咨询」「广告」，这家就进池。
   - 行业和经营范围都空：只看 `name_cn` 是否命中收紧名称词。名称里单独出现「投资」或「广告」，不够进池。
   - `org_type` 不参与这一步。高校表、科研院所表也不参与；那两路只在后面给 ADS 的机构类型分布计数。
3. ~~命中不足 10 家时整张源表进入~~ **已废止（2026-11-04 Q9）**。正式口径：命中多少入多少，禁止全库入池。现网当时圈定 43296 行、源表 189116 行，当时未触发整表回退。代码 `svcseed` 内 fallback 须后续对齐关掉。
4. 默认 `append`：圈定池里已经有的 `org_id` 不再插一行。`replace` 先清空圈定、事件、卡面和四张基础指标表，再写入当次全部命中。批次号按运行当天生成，形如 `svc-fseed-YYYYMMDD`，现网是 `svc-fseed-20261020`。当次走的是 append 还是 replace，没有从库里的清空痕迹再判定，未闭合。
5. 圈定行只落这些列：`org_id`、`rule_version`、`hit_fields`（哪些源列碰到了词）、`service_type_candidate`、`pending_client_confirm`（固定 1）、`etl_batch_id`。
6. `service_type_candidate` 用 `classify`，比进池更紧，顺序是 FINANCE、IP、HR、MKT、CONSULT、INNOV。有行业文本时，一级行业含「金融」记 FINANCE，否则取第一组命中的词；对不上就空。一级行业是「科学研究和技术服务业」只说明可以进池，不能单凭这一句记成 INNOV。没有行业文本时，只按名称收紧词分类。卡面上的空类 9650 行，就是这次分类留下的空候选。

**投融资事件**

同一作业、同一批次，只挂本批要写入的 `org_id`。`replace` 用清空之后的全池；`append` 只用本批新插入圈定池的 `org_id`，已有事件行不在这一步删除。融资表须同时有 `org_id` 和 `funding_amount`，事件类型 `FINANCING`，日期取 `completion_date`。投资表须同时有 `org_id` 和 `investment_amount`，事件类型 `INVEST`。金额文本解析成元，解析不了就空。同一 `org_id` + `event_id` + `event_type` 在本批内只留一行。现网 15755 行。这张表不写 Nebula。

**年报不进 DWD**

`dwd_org_annual_financial_info` 只取每个 `org_id` 年份最新的一行，列限于 `org_id` / `year` / `employees_number` / `operating_revenue`。缺行时按 `org_id` 在内存里合成人数和营收，合成结果只进卡面三列。合成行数未数，未闭合。

**图谱挂表**

`svc_org_graph_hang` 由另一次 `POST /internal/svc/graph/{ner|intra|hang}` 写出，读的是已经落库的圈定池。空请求默认不落库。现网 43296 行，批次 `svcgraph_20261030_022647`。点、边和 peers 的差别见上文图谱段。

正式库 `gkxlumenx_dwd` 同名三表是 0 行。这次作业拒绝写入非 `demo_` 库。GDF 还没有对应作业。派单要走的源切换见 §1.2。

### 1.2 抽取源计划：GDF 派单读第三方 dwd 机构表

算法中台「维护管理 / 服务机构抽取」上的「开始抽取」仍调用 `POST /entan/internal/svc/run-pipeline`（追加）。它现在读 `demo_gkxlumenx_ods`，只写 `demo_gkxlumenx_*`。页面上的字段表是迁移对照，按钮没有改连接。

计划是把抽取读取从 `demo_gkxlumenx_ods.dwd_org_base_info` 换成第三方数据源里、表名以 `dwd` 开头的相关机构表。表名和字段先与现网读取列相同，只换库。代码和连接都还没改。第三方库的库名、账号，以及这四张表是否已在供应方库里，本叶没有再连库核对，未闭合。不新起库名，不新起表名。

`SYSINT-06-21-01-L03` 生成 GDF 派单包时走下面这条，不把 demo 库写成产线源，包里不出现对 `demo_gkxlumenx_*` 的操作。

`diagram_id=SVC-PROC-LOGIC-DWD-PLAN-20261102`

```mermaid
flowchart LR
  SRC["第三方数据源<br/>dwd_org_base_info<br/>dwd_org_annual_financial_info<br/>dwd_org_financing_info<br/>dwd_org_invest_info"]
  RULE["圈定规则 svc_rule_demo_kw_v1.1<br/>步骤同 §1.1"]
  DWD["gkxlumenx_dwd<br/>svc_org_circle<br/>svc_org_finance_event"]
  ADS["gkxlumenx_ads<br/>svc_org_card 与基础指标"]

  SRC --> RULE --> DWD --> ADS
```

| 计划源表 | 计划抽取字段 | 落到哪里 |
|---|---|---|
| `dwd_org_base_info` | `org_id`、`is_deleted`、`name_cn`、`province`、`city`、`area`、`district`、`industry`、`industry_l1_name` 至 `industry_l4_name`、`industry_l1_code` 至 `industry_l4_code`、`business_scope`、`incorporation_date`、`incorporation_year`、`org_size` | 圈定池只留 `org_id` 与圈定元数据。名称、地区、行业、规模原文进 `gkxlumenx_ads.svc_org_card` |
| `dwd_org_annual_financial_info` | `org_id`、`year`、`employees_number`、`operating_revenue` | 每个机构取最新一年，人数和营收进卡面。缺行留空。demo 里按 `org_id` 在内存合成人数和营收的做法不带进 GDF，不回写供应方库 |
| `dwd_org_financing_info` | `org_id`、`id`、`funding_amount`、`completion_date`、`funding_round`、`investors_name` | `gkxlumenx_dwd.svc_org_finance_event`，类型 `FINANCING`。只挂本批圈定机构 |
| `dwd_org_invest_info` | `org_id`、`id`、`investment_amount`、`inv_org_id`、`inv_name`、`created_time` | 同表，类型 `INVEST` |

GDF 执行时只操作 `gkxlumenx_*`。圈定和投融资事件进 `gkxlumenx_dwd`，卡面和基础指标进 `gkxlumenx_ads`。图谱挂表、Nebula 不在这条抽取里。GDF 不直写图库。§3.6 内容运营不进 GDF 派单：它仍是现网 CMS 写接口，不写 ADS，也不由 GDF 作业承接。

## 2. 谁触发、写哪套库

| 加工 | 谁触发 | 读 | 写 | 2026-11-02 |
|---|---|---|---|---|
| 圈定、卡面、投融资事件、基础指标 | 人手 `POST /internal/svc/run-pipeline` 或 `python -m entan.svcseed`。无定时任务。顶栏切到正式库时接口拒绝 | `demo_gkxlumenx_ods` | `demo_gkxlumenx_dwd` / `demo_gkxlumenx_ads` | 已有上表行数 |
| 十模型 | 另一次 `POST /internal/svc/run-models` | demo 的 circle / card | `demo_gkxlumenx_ads` 模型表 | 抽样行数，不是全量 |
| 图谱挂表 | 另一次 `POST /internal/svc/graph/ner` 等。空请求默认不落库 | demo 的 circle / card | hang 写 `demo_gkxlumenx_dwd`；图库 space 代码固定 `demo_gkx_chain` | hang 有行；图库行数未闭合 |
| ES | 人手 `POST /internal/etl/svc-org` | 配置默认 `demo_gkxlumenx_*` | 索引别名 `gkx_svc_org`；水位在 `gkxlumenx_cfg` | 文档 43296；之后卡面更新未再记水位 |
| 内容运营 | CMS 写接口。不进 GDF 派单（§3.6） | 视图跨库读 demo circle/card | `gkxlumenx_cms`，不写 ADS | overlay 7 行；视图 43299 行 |
| 专题查询 | 专题服务读 | 只读 `demo_gkxlumenx_ads` / `_dwd` | 不写 | 代码如此，不是产线 ADS |
| GDF | 无作业 | — | 执行时只应操作 `gkxlumenx_*`，且不直写图库 | 未跑通 |

## 3. 流程图

每张图单独看。箭头在「加工类型」里只表示分类，不表示一次作业做完所有事。数据先后看后面的加工逻辑图。这些图不放进 `01-data-flow.md` §1。

### 3.1 加工类型

`diagram_id=SVC-PROC-TYPE-20261102`

```mermaid
flowchart TB
  ROOT["服务机构加工类型<br/>2026-11-02 现网"]
  ROOT --> A["圈定与卡面"]
  ROOT --> B["基础指标聚合"]
  ROOT --> C["十模型"]
  ROOT --> D["图谱挂表"]
  ROOT --> E["检索索引"]
  ROOT --> F["内容运营覆盖"]
  ROOT --> G["GDF 产线作业<br/>未建，未跑通"]
```

圈定和基础指标在同一次 `run-pipeline` 里。十模型、图谱、ES、内容运营都是另外的触发。内容运营不进 GDF 派单。GDF 还没有这条作业。

### 3.2 加工逻辑 · 圈定、卡面、事件

`diagram_id=SVC-PROC-LOGIC-SEED-20261102`

```mermaid
flowchart TB
  TRIG["人手触发<br/>POST /internal/svc/run-pipeline<br/>或 python -m entan.svcseed"]
  ODS["demo_gkxlumenx_ods<br/>dwd_org_base_info"]
  FIN["demo_gkxlumenx_ods<br/>融资表与投资表"]
  ANN["demo_gkxlumenx_ods<br/>dwd_org_annual_financial_info<br/>只取最新一行"]
  MEM["年报缺行：内存合成人数和营收<br/>不写回 ODS"]
  RULE["规则 svc_rule_demo_kw_v1.1"]
  CIR["demo_gkxlumenx_dwd.svc_org_circle"]
  CARD["demo_gkxlumenx_ads.svc_org_card"]
  EVT["demo_gkxlumenx_dwd.svc_org_finance_event"]
  REFUSE["目标库不是 demo_ 前缀则拒绝"]

  TRIG --> RULE
  ODS --> RULE
  RULE --> CIR
  RULE --> CARD
  FIN --> EVT
  ANN --> CARD
  MEM --> CARD
  TRIG --> REFUSE
```

这一步不写 hang，不写 Nebula，不写十模型，不写 ES，不写 `gkxlumenx_dwd` / `gkxlumenx_ads`。

### 3.3 加工逻辑 · 十模型

`diagram_id=SVC-PROC-LOGIC-MODEL-20261102`

```mermaid
flowchart LR
  TRIG["另一次触发<br/>POST /internal/svc/run-models"]
  SRC["读 demo 的 circle 与 card"]
  TECH["svc_tech_power_score<br/>model_id 为六类 SVC_*_TECH_POWER"]
  ATT["svc_attraction_recommend"]
  CUL["svc_cultivation_recommend"]
  GAP["svc_chain_gap"]
  REL["svc_relation_chain<br/>列 density 与 centrality"]

  TRIG --> SRC
  SRC --> TECH
  SRC --> ATT
  SRC --> CUL
  SRC --> GAP
  SRC --> REL
```

2026-11-02 行数是技术力 400、引入 50、培育 50、短板 6、关系链 51。人口是圈定 43296，模型不是全量重算。

### 3.4 加工逻辑 · 图谱三条边

`diagram_id=SVC-PROC-LOGIC-GRAPH-20261102`

```mermaid
flowchart TB
  TRIG["另一次触发<br/>POST /internal/svc/graph/ner 等<br/>空请求默认 dry_run 不落库"]
  POOL["读 demo 的 circle 与 card"]
  NER["NER 写点<br/>Tag institution<br/>VID institution 加 org_id"]
  HANG["demo_gkxlumenx_dwd.svc_org_graph_hang"]
  INTRA["intra 写机构到机构<br/>participates<br/>mapped_from=cooperation"]
  NEB["Nebula space demo_gkx_chain"]
  MISS["belongs_to 与 service_provide<br/>现网 hang 里是 0 行"]
  ENT["企业合作代码另写 service_provide<br/>点类型 service<br/>不从本链路进入"]

  TRIG --> POOL --> NER --> HANG
  POOL --> INTRA --> HANG
  NER --> NEB
  HANG --> MISS
  ENT --> MISS
```

图库是否已经有点，2026-11-02 未闭合。Nebula 失败时来源记 `ads`。`belongs_to` 的目标前缀在代码里是 `segment:` / `chain:`，这次 hang 里是 0。`service_provide` 不是本链路的边。

### 3.5 加工逻辑 · 检索索引

`diagram_id=SVC-PROC-LOGIC-ES-20261102`

```mermaid
flowchart LR
  TRIG["人手触发<br/>POST /internal/etl/svc-org"]
  CARD["svc_org_card"]
  CIR["svc_org_circle"]
  TECH["svc_tech_power_score<br/>同机构取最大批次最高分"]
  TAG["dwd_org_industry_tags<br/>按企业名对卡面中文名"]
  PAT["enterprise_patent_history<br/>按 org_id 求和有效专利"]
  IDX["别名 gkx_svc_org<br/>物理索引 gkx_svc_org_v1"]
  WM["gkxlumenx_cfg.es_sync_watermark<br/>module_name=svc_org_card"]

  TRIG --> CARD --> IDX
  TRIG --> CIR --> IDX
  TRIG --> TECH --> IDX
  TRIG --> TAG --> IDX
  TRIG --> PAT --> IDX
  IDX --> WM
```

配置默认源库是 `demo_gkxlumenx_*`。正式卡面 0 行解释不了 43296 篇文档。当时进程的环境变量未见，未闭合。

### 3.6 加工逻辑 · 内容运营

这一节只记现网。`SYSINT-06-21-01-L03` 的 GDF 加工派单不包含本节：不建 CMS 表，不写 `ServiceOrgService`，不把 `cms_entity_overlay` / `cms_svc_business_domain` / `v_cms_svc` 写进派单包。

`diagram_id=SVC-PROC-LOGIC-CMS-20261102`

```mermaid
flowchart LR
  API["内容运营写接口<br/>ServiceOrgService"]
  OV["gkxlumenx_cms.cms_entity_overlay<br/>entity_type=SVC"]
  BODY["gkxlumenx_cms.cms_svc_business_domain<br/>0 行"]
  VIEW["视图 v_cms_svc"]
  CIR["demo_gkxlumenx_dwd.svc_org_circle"]
  CARD["demo_gkxlumenx_ads.svc_org_card"]

  API --> OV
  API --> BODY
  CIR --> VIEW
  CARD --> VIEW
  OV --> VIEW
```

视图读 demo 圈定和卡面。写路径不写 ADS。这张图不进入 §3.7 的 GDF 目标态。

### 3.7 加工逻辑 · GDF 目标态

`diagram_id=SVC-PROC-LOGIC-GDF-20261102`

```mermaid
flowchart LR
  ODS["gkxlumenx_ods<br/>只读贴源"]
  GDF["GDF 作业<br/>2026-11-02 未建"]
  DWD["gkxlumenx_dwd<br/>同名表已建，0 行"]
  ADS["gkxlumenx_ads<br/>同名表已建，0 行"]
  ES["ES 与图谱"]
  NO["GDF 不直写图库"]

  ODS --> GDF --> DWD --> ADS
  GDF -.-> NO
  ADS -.-> ES
```

实线是 GDF 团队以后只操作 `gkxlumenx_*` 时的边界。虚线表示现在没有这条作业，ES 和图谱也不是 GDF 直接写的。§3.6 内容运营不在这张图里，也不进派单包。demo 库上已经跑过的 Python，不能填进这张图当成产线已跑通。

### 3.8 库分隔

`diagram_id=SVC-PROC-LIB-SPLIT-20261102`

```mermaid
flowchart TB
  DEMO["demo_gkxlumenx_ods / _dwd / _ads<br/>圈定、模型、hang 的现网行在这里"]
  PROD["gkxlumenx_ods / _dwd / _ads<br/>服务机构结果表 0 行"]
  CMS["gkxlumenx_cms<br/>运营覆盖"]
  CFG["gkxlumenx_cfg<br/>ES 水位一条"]
  ES["gkx_svc_org 文档 43296"]
  GRAPH["demo_gkx_chain<br/>图库行数未闭合"]

  DEMO --> ES
  DEMO --> GRAPH
  DEMO --> CMS
  ES --> CFG
  PROD -.->|"同名空表，解释不了 ES 文档"| ES
```

### 3.9 失败时停在哪

`diagram_id=SVC-PROC-FAIL-20261102`

```mermaid
flowchart TB
  SEED["圈定失败"] --> NOCARD["不发布半成品卡面"]
  NEBFAIL["Nebula 写入失败"] --> ADSRC["hang 可仍在<br/>来源记 ads<br/>不得报图库成功"]
  ESOLD["卡面后来又更新"] --> NOWATER["没有新的水位行<br/>索引不自动跟上"]
  DRY["图谱空请求"] --> NOROW["dry_run 不落库"]
```

### 3.10 专题八个分析菜单

图 1 红框是 `http://10.50.69.111:30892`（`lumen-ui-topic`）侧栏「产业服务链分析」的八个菜单。菜单在 `src/router/menu.ts`。三条路由：

| 菜单 | 路由 | 查询 |
|---|---|---|
| 服务机构产业领域分析 | `/service/institution-judgment` | `workspace=field&tab=coverage` |
| 服务机构新增趋势分析 | 同上 | `workspace=trend&tab=trend` |
| 服务机构技术力评估分析 | 同上 | `workspace=capability&tab=capability` |
| 服务链短板分析 | `/service/chain-analysis` | `workspace=chain&tab=chain` |
| 服务链图谱分析 | 同上 | `workspace=graph&tab=graph` |
| 深圳服务链现状分析 | 同上 | `workspace=shenzhen&tab=shenzhen` |
| 引入服务机构推荐分析 | `/service/institution-decision` | `workspace=attract&tab=attract` |
| 培育服务机构推荐分析 | 同上 | `workspace=cultivate&tab=cultivate` |

`demo-ui-topic` 同名菜单把阶段写进浏览器本地任务，用页内样本出数。那条路径不服务 30892，本节不展开。

八页共用这一条展示链。改筛选不建任务。点「开始分析」才 `POST /topicAsync/topic/v1/analysis/tasks`。同用户同条件已有在跑任务就打开那条；当天已成功就打开结果。过程页只显示阶段，不显示结果数字。用户点「查看结果」后，前端 `GET /topicAsync/topic/v1/analysis/tasks/{id}/result`，只画这次快照。

Java `gkxlumen-topic-async-service` 把叶子交给 `lumen-topic-py` 的 `POST /internal/gkx-svc/analysis/tasks/create`。topic-py 再调 `lumen-algo-py`：

| 叶子 | 算法路径 |
|---|---|
| `org_coverage` | `/internal/v1/svcan/analysis/org_coverage` |
| `org_trend` | `/internal/v1/svcan/analysis/org_trend` |
| `tech_power` | `/internal/v1/svcan/analysis/tech_power` |
| `shortboard` | `/internal/v1/svcan/analysis/shortboard` |
| `graph` | `/internal/v1/svcan/analysis/graph` |
| `shenzhen` | `/internal/v1/svcan/analysis/shenzhen` |
| `attract` | `/internal/v1/svcan/analysis/attract` |
| `cultivate` | `/internal/v1/svcan/analysis/cultivate` |

装配只读，不写 ADS。库名是连接上的 `{ods}` / `{dwd}` / `{ads}`。L01 核对到的专题读面落在 `demo_gkxlumenx_*`。下面表里的物理表按这个前缀理解。角标上的 `metric_id` 是页面挂的身份证；种子作业没有把其中若干 ID 写成 ADS 行，§5 仍把那些 ID 标成未覆盖。口径未确认的项保持未闭合，本文不改 D4。

图上任务 `SVC-20261030-…` 的快照本叶没有重放。条上的具体分数不写入本文。

这八页不进 §1.2 的 GDF 抽取，也不进 §3.6 的内容运营。

#### 服务机构产业领域分析

`diagram_id=SVC-MENU-FIELD-20261102`。叶子 `org_coverage`。

```mermaid
flowchart TB
  OPEN["打开菜单<br/>workspace=field"]
  PICK["对比篮选定 1 到 50 家机构<br/>产业下拉只筛展示字段"]
  BTN["开始分析"]
  JAVA["Java 建任务 org_coverage"]
  ALGO["算法装配覆盖矩阵<br/>再润色结论文字"]
  GET["查看结果 GET result"]
  BOARD["热力图或矩阵图<br/>广度 TOP3 / 深度 TOP / 合作建议"]

  OPEN --> PICK --> BTN --> JAVA --> ALGO --> GET --> BOARD
```

过程四步：任务提交与分析对象冻结；装载机构领域覆盖与服务深度快照；计算服务广度与深度矩阵；生成领域覆盖结论与可视化。

空对比篮不能开始。未传机构时，算法按命中产业领域数从服务机构卡面里取候选，最多 50 家。页面自己的开始按钮要求对比篮里已有机构。

| 结果项 | 页面上怎么来 | 数据血缘 |
|---|---|---|
| 机构名称、城市 | 结果矩阵里的机构行 | `{ads}.svc_org_card` 的 `name_cn` / `city`。只保留卡面里真实存在的 `org_id` |
| 产业领域轴 | 矩阵字段，最多 12 个，按覆盖机构数降序 | `{dwd}.enterprise_industry_chain` 的 `chain_code` / `chain_name` |
| 色块或条上的服务深度 | 格子分值，1 到 100 | 同一行 `chain_score` 乘 100 后取整并夹到 1–100。未命中的格子不下发，页面留白。角标 `M_SVC_ORG_COVERAGE_DEPTH`。口径 Q-SVCCHAIN-02 未闭合 |
| 服务广度 | 该机构在当前可见领域里的格子数 | 上表格子计数。角标 `M_SVC_ORG_COVERAGE_BREADTH`。种子作业不写这个 `metric_id` |
| 产业下拉之后的图 | 前端用下拉的产业编码或名称去对 `chain_code` / `chain_name` | 对上了只留这些领域，广度和深度 TOP 按可见格子重数。一个都对不上就仍画全部领域。这一步不再查库 |
| 服务广度 TOP3 | 可见格子的广度降序取 3 | 同源格子，无第二张表 |
| 服务深度 TOP 领域（按机构） | 每家取可见格子里深度最高的领域，再按该深度降序取 3 | 同源格子 |
| 合作建议 | 润色状态为 ok 时显示模型写的叙述和建议句；否则显示规则句 | 规则句只用上面的广度、深度和机构名。模型只改 `narration.text` 和建议句，不改矩阵数字。无覆盖或无模型密钥则跳过，任务仍成功 |
| 暂无覆盖数据 | 选中机构在可见领域里没有格子 | 不参与 TOP。不补 0 |

#### 服务机构新增趋势分析

`diagram_id=SVC-MENU-TREND-20261102`。叶子 `org_trend`。

```mermaid
flowchart TB
  OPEN["打开菜单<br/>workspace=trend"]
  PICK["选定主领域、对比领域和时间窗"]
  BTN["开始分析"]
  JAVA["Java 建任务 org_trend"]
  ALGO["按成立年份聚合年度新增<br/>再算热度档"]
  GET["查看结果 GET result"]
  BOARD["折线、年度明细、热度星级"]

  OPEN --> PICK --> BTN --> JAVA --> ALGO --> GET --> BOARD
```

过程四步：任务提交与趋势窗口冻结；装载主领域与对比领域新增序列；计算年度新增与热度研判；生成趋势曲线与研判结论。

算法把全量年度点放进快照。前端按 3 / 5 / 8 年窗口截断展示。

| 结果项 | 页面上怎么来 | 数据血缘 |
|---|---|---|
| 分领域年度新增 | 折线和年度明细的点数 | `{dwd}.enterprise_industry_chain` 连接 `{ads}.svc_org_card`，再连接 `{ods}.dwd_org_base_info`。按 `chain_code`、`chain_name`、`incorporation_year` 对 `org_id` 去重计数。角标 `M_SVC_NEW_CNT`。口径 Q-SVC-010 未闭合 |
| 全量年度新增 | 未指定领域时的总序列 | 先读 `{ads}.svc_metric_series`，`metric_id` 为 `M_SVC_NEW_CNT` 或 `M_SVC_ORG_NEW_COUNT`。这张序列没有点时，按成立年份回算 |
| 市场热度星级 | 近 3 年均值相对再往前 3 年均值的增幅 | 增幅 ≥20% 为 5 星高热，≥10% 为 4 星较高，≥0 为 3 星平稳，≥−10% 为 2 星降温，其余 1 星低迷。不足 3 个年度点，或没有前序基期，不评级。页面角标走 `GAP-SVC-ORG-HEAT`。`M_SVC_ORG_MARKET_HEAT` 种子不写。Q-SVCCHAIN-02 未闭合 |
| 热度研判文字 | 润色只改叙述 | 星级和档位词保持上面的规则。失败则留下规则稿，任务仍成功 |
| 曲线上的机构画像入口 | 点名称打开机构抽屉 | 名称来自序列点上的机构，抽屉另读机构卡面。趋势图本身不另算一张评分表 |

#### 服务机构技术力评估分析

`diagram_id=SVC-MENU-CAP-20261102`。叶子 `tech_power`。

```mermaid
flowchart TB
  OPEN["打开菜单<br/>workspace=capability"]
  PICK["对比篮 2 到 5 家<br/>页面上的维度权重只作配置展示"]
  BTN["开始分析"]
  JAVA["Java 建任务 tech_power<br/>产业编码进入任务指纹"]
  ALGO["读技术力得分最新批次<br/>产业只筛机构名单"]
  GET["查看结果 GET result"]
  BOARD["综合得分、维度、排名、雷达、核心结论"]

  OPEN --> PICK --> BTN --> JAVA --> ALGO --> GET --> BOARD
```

过程四步：任务提交与分析条件冻结；装载对比机构与技术力指标快照；计算维度得分并合成技术力评价；生成横向对比排名与雷达结果。

少于 2 家不能开始。页面权重不写入 CREATE 参数，前端不做加权求和。

| 结果项 | 页面上怎么来 | 数据血缘 |
|---|---|---|
| 机构名称 | 得分行左连卡面 | `{ads}.svc_tech_power_score` 最新 `calc_batch_id` 左连 `{ads}.svc_org_card.name_cn` |
| 技术力综合得分、排名、雷达 | 行上的 `score`，按分排序 | 同一张 `svc_tech_power_score`。角标 `M_SVC_ORG_TECH_SCORE`。五维在 `dimension_scores`。代码注明当前等权 20。Q060、Q-SVCCHAIN-01 未闭合 |
| 产业下拉 | 只留下该产业挂链上的 `org_id` | `{dwd}.enterprise_industry_chain`。挂链上没有机构则整页空，不回退全量 |
| 核心结论文字 | 润色只改叙述 | 少于 2 家跳过。得分、排名、权重保持规则结果 |
| 暂无技术力评估结果 | 快照 `tech` 为空 | 不补 0 分 |

#### 服务链短板分析

`diagram_id=SVC-MENU-SHORT-20261102`。叶子 `shortboard`。

```mermaid
flowchart TB
  OPEN["打开菜单<br/>workspace=chain"]
  PICK["选定产业"]
  BTN["开始分析"]
  JAVA["Java 建任务 shortboard"]
  ALGO["有产业则按挂链重算六环节<br/>无产业则读短板表最新批次"]
  GET["查看结果 GET result"]
  BOARD["链路轨道、环节机构数、平均深度、瓶颈列表"]

  OPEN --> PICK --> BTN --> JAVA --> ALGO --> GET --> BOARD
```

过程四步：任务提交与产业领域冻结；装载服务链环节与机构覆盖快照；计算环节强度并识别短板瓶颈；生成链路短板结论与可视化。

| 结果项 | 页面上怎么来 | 数据血缘 |
|---|---|---|
| 六环节轨道 | 快照 `gap` / `shortboard.stages` | 选定产业时：先用 `{dwd}.enterprise_industry_chain` 取出该产业机构，再按服务环节汇总覆盖格。未选产业时：`{ads}.svc_chain_gap` 最新 `calc_batch_id` |
| 环节服务机构数 | 行上 `org_count_in_stage` | 上一步的环节行。页面角标 `GAP-SVC-CHAIN-SEGMENT`。种子不写 `M_SVC_CHAIN_SEGMENT_ORG_COUNT` |
| 平均服务深度 | 行上 `avg_depth` | 产业重算时，是该环节覆盖格深度的平均。深度与覆盖矩阵同一套 `chain_score×100`。种子不写 `M_SVC_CHAIN_SEGMENT_AVG_DEPTH` |
| 瓶颈堵点 | `runtime_flag` 非空的环节 | 0 家为 blank，不多于 1 家为 weak，平均深度低于 55 为 bottleneck。规则号 Q-SVCCHAIN-03，未闭合。页面角标 `GAP-SVC-CHAIN-BOTTLENECK`。种子不写 `M_SVC_CHAIN_BOTTLENECK` |
| 供给不足 | 产业挂链上没有机构，或没有环节行 | 文案「该产业服务供给数据不足，暂无法判定」。不补 0 |
| 未发现明显短板 | 有环节行且没有 flag | 文案「当前演示规则下未发现明显短板」 |
| 短板研判文字 | 润色只改叙述 | 档位词保持上面的 flag。Q-SVCCHAIN-03 的声明随叙述下发 |

#### 服务链图谱分析

`diagram_id=SVC-MENU-GRAPH-20261102`。叶子 `graph`。画布另走同步读面。

```mermaid
flowchart TB
  OPEN["打开菜单<br/>workspace=graph"]
  PICK["选定产业和滤镜<br/>切滤镜不建任务"]
  DRAW["出图 POST /svc/topic/v1/service/eco-graph"]
  PY["topic-py GET /internal/v1/svcan/models/relation"]
  HANG["只取包络里的 hang 点边"]
  CANVAS["画布、两列密度、度中心性"]
  BTN["开始分析另建 graph 任务"]
  LEAF["算法 /analysis/graph 装配另一份点边"]

  OPEN --> PICK --> DRAW --> PY --> HANG --> CANVAS
  PICK --> BTN --> LEAF
```

过程四步仍登记在任务上：任务提交与产业领域冻结；装载主体节点与关系边快照；构建服务生态关系图谱；生成图谱统计与探索视图。页面画布只渲染 eco-graph 返回的 `nodes` / `edges`。`relation_top` 不画成图。

| 结果项 | 页面上怎么来 | 数据血缘 |
|---|---|---|
| 画布上的点 | eco-graph 的 `hang_nodes`，或历史包络 `hang.nodes` | 带产业时锁定该切片，切片为空不回退全量。当前 `fetch_models(kind=relation)` 填的是 `{ads}.svc_relation_chain` 最新批次的 `relation_top`（`org_id` / `density` / `centrality` / `hop_level`），查询本身不下发 `hang_nodes`。没有 hang 点时画布为空 |
| 画布上的边 | 同一包络的 `hang_edges`，两端都必须在 hang 点内 | 允许的展示类型是 `belongs_to`、`participates`、`supplies`、`depends_on`。投资、合作、人才流动在展示层并进 `participates`。图库 `demo_gkx_chain` 的实际点数、边数仍是 §7 未闭合 |
| 子网密度、生态密度 | 两列只显示 eco-graph 返回值 | topic-py 按可见点边算 `2E/(N×(N−1))`。N 小于 2 时页面显示 0。角标 `M_SVC_RELATION_DENSITY`。Q062 未闭合。前端不用自己的公式覆盖这两列 |
| 度中心性 TOP5 | 跟当前可见子网一致 | 点的度来自当前边集。角标仍是 `M_SVC_RELATION_DENSITY` |
| 生态影响力 | 页面挂红问号 | 角标 `GAP-SVC-GRAPH-INFLUENCE`。种子不写 `M_SVC_GRAPH_INFLUENCE`，页面不输出评分 |
| 异步叶子里的另一份点边 | `GET result` 的 graph 装配 | `{ads}.svc_org_card`，加上 `{ods}.dwd_org_invest_info`、`dwd_org_shareholder_info`、`dwd_org_subsidiary_info`，以及 `{dwd}.enterprise_supply_chain`。选定产业时先用挂链限定机构。这份点边不替代上面的画布 |

#### 引入服务机构推荐分析

`diagram_id=SVC-MENU-ATTRACT-20261102`。叶子 `attract`。名单数字走同步接口。

```mermaid
flowchart TB
  OPEN["打开菜单<br/>workspace=attract"]
  PICK["选定产业和筛选<br/>页面权重不进任务参数"]
  BTN["开始分析"]
  JAVA["Java 建任务 attract"]
  VIEW["查看结果之后才要名单"]
  LIST["POST /svc/topic/v1/service/rec-list<br/>kind=attract"]
  BOARD["招引名单、优先级、推荐理由、AI 叙述"]

  OPEN --> PICK --> BTN --> JAVA --> VIEW --> LIST --> BOARD
```

过程五步：任务提交与推荐条件冻结；权限与配置校验；候选机构数据汇聚；推荐算法计算；招引推荐名单组装。

页面上的四维权重只展示，不重算名单分。

| 结果项 | 页面上怎么来 | 数据血缘 |
|---|---|---|
| 招引综合分、优先级、名次 | rec-list 行 | `{ads}.svc_attraction_recommend` 最新 `calc_batch_id` 的 `attraction_index`、`priority_level`、`rank_no`，按 `rank_no` 升序。角标 `M_SVC_REC_ATTRACT_SCORE`。Q063、Q-SVC-010、Q-SVCCHAIN-05 未闭合。装配注释里的权重是 35/30/20/15，页面不按这个权重重算已落库的分 |
| 机构名称、城市、服务类型 | 同一查询左连卡面 | `{ads}.svc_org_card` |
| 推荐理由 | 行上 `recommend_reason` | 同一张推荐表。页面标注演示口径 |
| 产业筛选后的名单 | 链码过滤 | `{dwd}.enterprise_industry_chain`。链码对不上挂链时按 2026-10-22 的名称映射降到旧码；仍对不上则空名单，不回退全量。映射是静态快照，重灌后应删 |
| AI 叙述 | 只在润色状态为 ok 时显示 | 叙述来自 rec-list 包络顶层。模型不改分数 |
| 候选机构数 | 页面没有单独的计数按钮 | `M_SVC_REC_CANDIDATE_CNT` 已退出统计，本节不给它做结果项 |

异步叶子 `/analysis/attract` 读的是同一张 `svc_attraction_recommend`，选定产业时再用挂链过滤。页面名单以 rec-list 为准。

#### 培育服务机构推荐分析

`diagram_id=SVC-MENU-CULT-20261102`。叶子 `cultivate`。

```mermaid
flowchart TB
  OPEN["打开菜单<br/>workspace=cultivate"]
  PICK["四维权重默认 25/30/25/20<br/>权重合计不是 100 不能开始"]
  BTN["开始分析"]
  JAVA["Java 建任务 cultivate<br/>权重不写入任务参数"]
  VIEW["查看结果之后才要名单"]
  LIST["POST /svc/topic/v1/service/rec-list<br/>kind=cultivate"]
  BOARD["培育名单、成长阶段、建议、AI 叙述"]

  OPEN --> PICK --> BTN --> JAVA --> VIEW --> LIST --> BOARD
```

过程五步：任务提交与培育条件冻结；权限与配置校验；本土机构数据汇聚；培育评估计算；培育名单与建议组装。

| 结果项 | 页面上怎么来 | 数据血缘 |
|---|---|---|
| 培育综合分 | rec-list 行上的分 | `{ads}.svc_cultivation_recommend` 最新 `calc_batch_id` 的 `cultivation_index`，按分降序。页面权重不重算这列。角标 `GAP-SVC-REC-CULTIVATE-SCORE`。Q063、Q-SVCCHAIN-05 未闭合。装配注释里的默认权重是 25/30/25/20 |
| 优先级、成长阶段、建议 | 同行的 `priority_level`、`growth_stage`、`advice` | 同一张培育推荐表。建议文本标注演示口径 |
| 机构名称、城市、服务类型 | 左连卡面 | `{ads}.svc_org_card` |
| 产业筛选后的名单 | 与引入名单同一套链码过滤 | `{dwd}.enterprise_industry_chain`。对不上则空名单 |
| AI 叙述 | 润色状态为 ok 才显示 | 不改分数 |
| 候选机构数 | 页面没有单独计数 | 同引入菜单，`M_SVC_REC_CANDIDATE_CNT` 不作为本页结果项 |

#### 深圳服务链现状分析

`diagram_id=SVC-MENU-SZ-20261102`。叶子 `shenzhen`。

```mermaid
flowchart TB
  OPEN["打开菜单<br/>workspace=shenzhen"]
  PICK["勾选对比指标<br/>完整度不在可选项里"]
  BTN["开始分析"]
  JAVA["Java 建任务 shenzhen"]
  ALGO["装配四城对比和梯队"]
  GET["查看结果 GET result"]
  BOARD["评价框架、城市柱、梯队仪表"]

  OPEN --> PICK --> BTN --> JAVA --> ALGO --> GET --> BOARD
```

过程四步：任务提交与对比指标冻结；装载五城市服务链基准数据；计算深圳横向对比与梯队位置；生成现状对比结论与图表。

全不选对比指标时，页面提示至少选一个，并保留上次图形。没有城市场景时图表区为空。缺城不补列，缺值显示「无数据」，不填 0。

| 结果项 | 页面上怎么来 | 数据血缘 |
|---|---|---|
| 统一评价框架说明 | 快照里的框架名和口径句 | 文案是「同一产业、同一统计周期、同一指标口径」。Q-SVCCHAIN-04 未闭合。无框架字段时仍显示这张说明卡 |
| 服务机构数量 | 城市柱的规模 | 深圳、北京、广州取 `{ads}.svc_org_card` 按 `city` 计数。上海在卡面为 0 行时该格为空。角标 `M_SVC_SZ_SCALE`。选定产业时，深圳列改按 `{dwd}.enterprise_industry_chain` 计数 |
| 平均技术力 | 城市柱的技术力 | 跨城可比值取 `{dwd}.sz_city_benchmark.avg_tech_power`。另有 `tech_local`：本库 `{ads}.svc_tech_power_score` 的均值，样本注释为 300 家，口径不同，只作参照。角标 `M_SVC_ORG_TECH_SCORE` |
| 服务网络密度 | 只有深圳格有数 | `{ads}.svc_relation_chain` 最新批次的汇总 `density`。其他城市为空。角标 `M_SVC_RELATION_DENSITY`。Q062 未闭合 |
| 服务链完整度 | 快照里有，页面不放进可选列表、柱图和结论 | 深圳按 `{ads}.svc_chain_gap` 里有机构的环节数除以 6。其他城市取对标表 `chain_completeness` 除以 100。页面角标走缺口问号。种子不写 `M_SVC_SZ_CHAIN_COMPLETENESS` |
| 梯队仪表 | 只认快照里的 `tier` | `{dwd}.sz_city_benchmark` 各城 `avg_tech_power` 从高到低排序。深圳排前 2 为第一梯队，前 4 为第二梯队，其余第三梯队。对标表没有深圳行则「梯队待定」，仪表无数值。`GAP_SZ_TIER` 未闭合。页面不把 `M_SVC_SZ_TIER` 写进种子 |
| 对比结论文字 | 润色只改叙述 | 梯队措辞保持上面的排序。基准城演示口径随叙述下发 |
| 全国平均列 | 快照里的对照列 | 规模是卡面城市均值。技术力是对标表均值。密度和完整度这两格标缺失 |

## 4. 指标计算

指标库产业服务域查询日 2026-11-02：返回 51 条，seed 与矩阵都在，D1 全部 `aligned`，D4 全部 `mock`。`M_SVC_BASE_101_1`（服务机构基础指标模型构建）是整体过程，不进入下面的指标对照。其余 50 条是叶指标。D4=`mock` 与 demo 表里已有行可以同时成立。本叶不把 demo 行数改写成 `live`。分 `metric_id` 的现网行数，除模型表的表级行数外，L01 没有逐个去数，下表「现网」列写的是代码落点和 L01 的表级事实。

### 4.1 指标计算落在哪次作业

`diagram_id=SVC-METRIC-CALC-20261102`

```mermaid
flowchart TB
  REG["叶指标 50 条<br/>D1=aligned D4=mock<br/>不含整体过程 M_SVC_BASE_101_1"]
  SEED["run-pipeline 写入 metric_id<br/>16 条"]
  MODEL["run-models 写物理表<br/>注册 ID 多数不落列"]
  GRAPH["图谱 hang<br/>112 点、113 只见到 participates"]
  NONE["本链路不写该 ID"]
  READ["读路径有表映射<br/>模块写明不是新口径实算"]

  REG --> SEED
  REG --> MODEL
  REG --> GRAPH
  REG --> READ
  REG --> NONE
```

### 4.2 指标计算逻辑 · 种子批

`diagram_id=SVC-METRIC-SCENE-SEED-20261102`

```mermaid
flowchart LR
  POP["人口 = svc_org_circle 的 org_id"]
  ODS["再读 ODS 主表列<br/>不把主体拷进 DWD"]
  FACT["svc_metric_fact"]
  SER["svc_metric_series"]
  DIST["svc_metric_dist"]
  REGN["svc_region_dist"]

  POP --> ODS
  ODS --> FACT
  ODS --> SER
  ODS --> DIST
  ODS --> REGN
```

这次作业在代码里写入的 `metric_id` 是：`M_SVC_INDUSTRY_LAYOUT`、`M_SVC_ORG_CNT`（`geo_level=province`，不是国家）、`M_SVC_ORG_TOTAL`、`M_SVC_PT_GLOBAL_TOTAL`、`M_SVC_NEW_CNT`、`M_SVC_ORG_NEW_COUNT`、`M_SVC_PT_GLOBAL_TYPE_DIST`、`M_SVC_PT_REGION_ORG`、`M_SVC_PT_GLOBAL_SCALE_DIST`、`M_SVC_SZ_SCALE`、`M_SVC_PT_SZ_TOTAL`、`M_SVC_SZ_COMPARE_METRIC`、`M_SVC_PT_SZ_TYPE_DIST`、`M_SVC_SZ_DISTRICT`、`M_SVC_PT_SZ_REGION_ORG`、`M_SVC_INVEST_Y`。承载表在 2026-10-20 那次 pipeline 写入过。每个 ID 多少行，未闭合。

`M_SVC_ORG_CNT` 的中文名是「按国家计数」。ODS 无国家列，代码写的是省。这是口径降级，不是已经算出全球国家分布。

### 4.3 指标计算逻辑 · 十模型抽样

`diagram_id=SVC-METRIC-SCENE-MODEL-20261102`

```mermaid
flowchart TB
  ALL["圈定 43296 家"]
  RUN["run-models 另一次触发"]
  TECH["技术力 400 行<br/>model_id=SVC_*_TECH_POWER"]
  REC["引入 50、培育 50"]
  GAP["短板 6 行"]
  REL["关系链 51 行<br/>有 density、centrality 列"]

  ALL --> RUN
  RUN --> TECH
  RUN --> REC
  RUN --> GAP
  RUN --> REL
```

短板运行时仍是 Q-SVCCHAIN-03，不切到 Q061。关系链密度公式仍是切法 A 的 `2E/(N*(N-1))`。列表抽样不是全量，和公式冻结「列表 N=50、hang 全量」一致的是推荐表 50 行；技术力 400、关系链 51、短板 6，都不是 43296。

### 4.4 指标计算逻辑 · 正式库空表

`diagram_id=SVC-METRIC-SCENE-PROD-EMPTY-20261102`

```mermaid
flowchart LR
  DEMO["demo 库已有圈定和指标行"]
  PROD["gkxlumenx_dwd / gkxlumenx_ads<br/>同名表 0 行"]
  D4["指标库 D4 仍是 mock"]

  DEMO -.->|"不能当成产线已算"| PROD
  PROD --> D4
```

GDF 尚未向 `gkxlumenx_*` 灌这些表。demo 有数不改变 D4。

### 4.5 指标计算逻辑 · 读路径不能当成已算

`diagram_id=SVC-METRIC-SCENE-READMAP-20261102`

```mermaid
flowchart LR
  ID["注册表 metric_id"]
  MAP["svc_metrics.py 指向一张 ADS 表"]
  NOTE["模块注明：现网表是旧演示口径<br/>禁止伪装成新口径正式结果"]
  ID --> MAP --> NOTE
```

`M_SVC_DEEP_174_1` 至 `M_SVC_DEEP_179_1` 的读路径指向 `svc_metric_dist`。模型作业实际写入的是 `svc_tech_power_score`，列 `model_id` 为 `SVC_FINANCE_TECH_POWER` 等六类，不是这六个注册 ID。两套名字对不齐。

## 5. 覆盖对照

「覆盖」只表示：种子作业会写这个 `metric_id`，或模型/图谱作业写出了对应物理结果。不表示 D4 已是 live，也不表示正式库已有数。下表 50 行，已去掉整体过程 `M_SVC_BASE_101_1`。

| metric_id | 中文名 | 类型 | 对照 |
|---|---|---|---|
| M_SVC_INDUSTRY_LAYOUT | 全球服务机构产业布局 | STAT | 种子写入该 ID，落 `svc_metric_dist`。分 ID 行数未闭合 |
| M_SVC_ORG_CNT | 全球服务机构分布（按国家计数） | STAT | 种子写入该 ID，`geo_level=province`。不是国家计数 |
| M_SVC_INVEST_Y | 服务机构投融资动态 | STAT | 种子写入该 ID，落 `svc_metric_series`。事件 hang 15755 行。分 ID 行数未闭合 |
| M_SVC_NEW_CNT | 新增服务机构动态 | STAT | 种子写入该 ID |
| M_SVC_ORG_NEW_COUNT | 年度新增服务机构数 | STAT | 种子写入该 ID，与上条同一套按年计数 |
| M_SVC_SZ_SCALE | 深圳服务机构规模 | STAT | 种子写入该 ID，落 `svc_metric_fact` |
| M_SVC_SZ_DISTRICT | 深圳服务机构分布 | STAT | 种子写入该 ID，`geo_level=sz_district` |
| M_SVC_ORG_TOTAL | 入库服务机构总数 | STAT | 种子写入该 ID |
| M_SVC_PT_GLOBAL_TOTAL | 全球服务机构总数 | STAT | 种子写入该 ID |
| M_SVC_PT_GLOBAL_TYPE_DIST | 全球服务机构类型分布 | STAT | 种子写入该 ID |
| M_SVC_PT_GLOBAL_SCALE_DIST | 全球服务机构规模分布 | STAT | 种子写入该 ID |
| M_SVC_PT_REGION_ORG | 区域服务机构数 | STAT | 种子写入该 ID，省粒度 |
| M_SVC_PT_SZ_TOTAL | 深圳产业服务机构数量 | STAT | 种子写入该 ID |
| M_SVC_PT_SZ_TYPE_DIST | 深圳服务机构类型分布 | STAT | 种子写入该 ID |
| M_SVC_PT_SZ_REGION_ORG | 深圳机构区域分布 | STAT | 种子写入该 ID |
| M_SVC_SZ_COMPARE_METRIC | 城市对比指标值 | STAT | 种子写入该 ID，切片 `shenzhen_org_count` |
| M_SVC_ORG_TECH_SCORE | 服务机构影响力 | MODEL | 技术力表 400 行。注册 ID 未作为 `metric_id` 落列。读路径映射到该表，并注明不是新口径实算 |
| M_SVC_CHAIN_BOTTLENECK | 瓶颈堵点判定 | MODEL | 短板表 6 行。注册 ID 未落列 |
| M_SVC_DEEP_172_1 | 服务链短板分析模型 | MODEL | 同上，物理表 `svc_chain_gap` |
| M_SVC_DEEP_173_1 | 服务关系链模型 | MODEL | 关系链表 51 行。注册 ID 未落列 |
| M_SVC_DEEP_174_1 | 金融服务机构技术力评价模型 | MODEL | 读路径指向 `svc_metric_dist`。模型行在 `svc_tech_power_score`，`model_id=SVC_FINANCE_TECH_POWER`。未按 ID 对上 |
| M_SVC_DEEP_175_1 | 知识产权服务机构技术力评价模型 | MODEL | 同上，`model_id=SVC_IP_TECH_POWER` |
| M_SVC_DEEP_176_1 | 人力资源服务机构技术力评价模型 | MODEL | 同上，`model_id=SVC_HR_TECH_POWER` |
| M_SVC_DEEP_177_1 | 市场营销服务机构技术力评价模型 | MODEL | 同上，`model_id=SVC_MKT_TECH_POWER` |
| M_SVC_DEEP_178_1 | 咨询服务机构技术力评价模型 | MODEL | 同上，`model_id=SVC_CONSULT_TECH_POWER` |
| M_SVC_DEEP_179_1 | 科技创新服务机构技术力评价模型 | MODEL | 同上，`model_id=SVC_INNOV_TECH_POWER` |
| M_SVC_DEEP_180_1 | 服务机构引入推荐模型 | MODEL | 引入表 50 行。注册 ID 未落列 |
| M_SVC_DEEP_181_1 | 服务机构培育推荐模型 | MODEL | 培育表 50 行。注册 ID 未落列 |
| M_SVC_REC_ATTRACT_SCORE | 招引综合评分 | MODEL | 引入表有行。注册 ID 未落列 |
| M_SVC_REC_CULTIVATE_SCORE | 培育综合评分 | MODEL | 培育表有行。注册 ID 未落列 |
| M_SVC_GRAPH_112_1 | 服务机构实体识别构建 | GRAPH | hang 点 43296。图库行数未闭合。不是指标事实表里的一行 |
| M_SVC_GRAPH_113_1 | 服务机构实体关系抽取 | GRAPH | hang 里只见到机构到机构的 `participates` 33861 行。`belongs_to`、`service_provide` 为 0。七类跨域关系未抽出 |
| M_SVC_GRAPH_DENSITY | 服务网络密度 | GRAPH | 关系链表有 `density` 列，51 行。注册 ID 未落列 |
| M_SVC_RELATION_DENSITY | 服务关系链密度 | STAT | 同上列，不是另一个作业 |
| M_SVC_GRAPH_CENTRALITY | 节点度中心性 | GRAPH | 关系链表有 `centrality` 列。注册 ID 未落列 |
| M_SVC_ORG_COVERAGE_DEPTH | 服务机构产业领域覆盖评分 | MODEL | 读路径指向 `svc_metric_dist`。种子作业不写该 ID |
| M_SVC_ORG_MARKET_HEAT | 市场热度评级 | MODEL | 读路径指向 `svc_metric_series`。种子作业不写该 ID |
| M_SVC_GRAPH_INFLUENCE | 生态影响力评分 | MODEL | 读路径指向 `svc_metric_dist`。种子作业不写该 ID |
| M_SVC_SZ_TIER | 深圳梯队位置 | MODEL | 读路径指向 `svc_metric_dist`。种子作业不写该 ID |
| M_SVC_CHAIN_SEGMENT_AVG_DEPTH | 环节平均服务深度 | STAT | 本链路不写该 ID |
| M_SVC_CHAIN_SEGMENT_ORG_COUNT | 环节服务机构数 | STAT | 本链路不写该 ID |
| M_SVC_ORG_COVERAGE_BREADTH | 服务广度 | STAT | 本链路不写该 ID |
| M_SVC_ORG_SELECTED_COUNT | 当前分析机构数 | STAT | 本链路不写该 ID |
| M_SVC_PT_CHAIN_NODE_ORG | 产业链节点服务机构数 | STAT | 本链路不写该 ID。2026-10-24 产业检索里链码关联为 0，见 ETL 索引所引实查，不是本叶新测 |
| M_SVC_PT_KEYORG_SCALE | 重点机构规模档案值 | STAT | 本链路不写该 ID |
| M_SVC_PT_SZ_FIELD_DIST | 深圳机构产业领域分布 | STAT | 本链路不写该 ID |
| M_SVC_REC_CANDIDATE_CNT | 候选机构数 | STAT | 本链路不写该 ID。引入/培育表各 50 行，不能倒推成这个 ID 已落库 |
| M_SVC_RELATION_RISK | 服务关系风险 | STAT | 本链路不写该 ID |
| M_SVC_SZ_CHAIN_COMPLETENESS | 服务链完整度 | STAT | 本链路不写该 ID |
| M_SVC_TYPE_DIST_QUERY | 查询结果·服务类型分布 | STAT | 本链路不写该 ID。卡面六类候选是圈定列，不是这个查询指标 |

域外检索词「服务机构」还命中 `M_CHAIN_REG_SERVICE_ORG`（产业链，区域服务机构）。本链路不写它。同一次检索还命中若干口径文本里带相近词的域外 ID（`M_CHAIN_DEEP_126_1`、`M_CHAIN_GRAPH_103_1`、`M_INNOV_FACTOR_COUNT`、`M_INNOV_POT_OUTPUT`、`M_SYNTH_183_1`、`M_SYNTH_187_1`、`M_TECH_GRAPH_105_1`），不列入服务机构加工覆盖。

存储设计 `ads.md` 里的 A1–A6 六条，都在种子写入清单里。设计里的十模型 ID（`SVC_SERVICE_CHAIN_GAP` 等）是模型表的 `model_id` 或设计名，和注册表 `M_SVC_DEEP_*` 不是同一个字符串。

## 6. 和已会签流图不一致的地方

`01-data-flow.md` 的 `signoff_status` 保持 `approved`。§1 工厂拓扑图不改。下面这些是 2026-11-02 现网和该正文的差别，正文里的补记标了待会签：

| 已会签正文 | 现网 |
|---|---|
| §1.1 / §7 把圈定、卡面、模型、上图画成同一条灌数时序 | 三次触发：pipeline、run-models、graph。pipeline 不写 hang |
| §1 工厂图有 GDF 方框 | 这条加工没有 GDF 作业。demo 是 Python 直接写 |
| 只写 `demo_gkxlumenx_*`，禁正式库 | 代码仍拒绝写正式 DWD/ADS。正式库同名表已经建着，且是 0 行。谁建的，未闭合 |
| 阶段 F 不碰 lumen 四仓 | 设计禁令仍在。现网 `lumen-topic-py` 只读 demo，`lumen-etl-es-py` 已同步过 ES，`lumen-svc-platform` 写 CMS |
| ES 在工厂图里有框，细表写阶段 F 不建索引 | 别名 `gkx_svc_org` 已有 43296 篇。正式 ADS 解释不了 |
| 图 hang 画成已经进入 Nebula | hang 有行。图库行数未闭合 |

## 7. 未闭合

- 图库 `demo_gkx_chain` 里 Tag `institution` 的点数、边数。
- ES 那次同步的进程环境变量。不能由默认配置单独证明读的是 demo；正式卡面 0 行仍然解释不了文档数。
- 正式库空表的建表脚本。仓内 DDL 只写 demo 库名。
- 种子指标每个 `metric_id` 的行数。年报内存合成写进卡面的行数。技术力 400 行按六类 `model_id` 的分布。
- `gkxlumenx_ods.dwd_org_base_info` 与 demo 同为 189116 行，未逐行比对。
- `belongs_to`、`service_provide` 在图库里是否另有边。MySQL hang 与 demo ADS `graph_edge` 里是 0。
- 图 1 任务 `SVC-20261030-…` 的结果快照未重放。条上的分数不作为本文实测值。
- `GET /internal/v1/svcan/models/relation` 当前查询只填 `relation_top`。图谱菜单画布要的 `hang_nodes` 从哪一次上图写入，未闭合。

## 8. 交给下游，本叶不做

`SYSINT-06-21-01-L03` 才能写 GDF 派单包。包按 §1.2，不收录 §3.6 内容运营。父任务 `SYSINT-06-21-L01` 使用本链路，不在本叶落地作业。不代替 `SYSINT-06-15-L01`。不改企业 v4、产业链 v2、政策 v2，不改 06-19 / 06-20 派单包。
