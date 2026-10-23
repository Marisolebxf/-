# 12 — Wave C：DWD 完成后的抽取产业与条款结构化

> **读者**：GDF 调度。算法不在 CDC / SeaTunnel 里写。  
> **前置**：Wave B `policy_base_info` 当日作业 `success`。Mapping 失败或只完成贴源时 **不触发**。  
> **调用链**：GDF → Java REST → Python `/internal/*`。禁止 GDF 直连 Python、直连模型、直连向量库。  
> **与 Wave B 的边界**：09 只洗主表。本文件两作业 **不改** `policy_base_info` 任何列（含 `theme`、`policy_support`）。

派单口语里的「条件结构化」就是本文件的 **条款结构化**：从正文拆条款，并抽出额度与准入条件。不是把 `policy_support` 再洗一遍。

## 脚本规约（生产）

抽取产业、条款结构化的交付物是 **Python 脚本**。逻辑与算法 demo 中台同一套实现，禁止在本包、CDC 或 SeaTunnel 里另写一版切条、对码或落库。

| 作业 | 中台模块（`repos/demo-algo-ent-analysis`） | 中台入口 |
|---|---|---|
| POLICY-C1 抽取产业 | `polan/industry_enrich.py` 的 `enrich_policies`；跑批 `polan/industry_job.py` 的 `run_enrich_job` | `POST /internal/policy/industry/enrich`；日批 `POST /internal/industry/jobs/enrich` |
| POLICY-C2 条款结构化 | `polan/clause_job.py` 的 `run_clause_button`、`run_clause_job` | `POST /v1/policy/clauses/enrich`；日批 `POST /v1/policy/clauses/jobs` |

- **一致**：切条顺序、对码、增量跳过、失败不写假结果、落库字段都走上表函数。中台改了规则，脚本跟同一模块，不在派单包留一份拷贝。
- **库**：读写仍是本文的 `gkxlumenx_dwd` / `gkxlumenx_ads`。禁止把 `demo_gkxlumenx_*` 配成产线目标。中台 `assert_demo_mysql_targets` 只拦 demo 菜单误写正式库，不是产线库名。
- **调度**：脚本是算法实现，由 Java 转发后调用。禁止 GDF 调度直连该脚本、直连模型。Java 门面未落地前，状态仍是可排期，不可当产线已接通。日批走 Job，`limit`≤100，不在调度线程里同步死等模型。

---

## 0. 顺序

```text
Wave A 贴源
    → Wave B Mapping（09）→ gkxlumenx_dwd.policy_base_info
         ├─ POLICY-C1 抽取产业 → DWD policy_industry_rel → 同步 ADS 同名表
         └─ POLICY-C2 条款结构化 → ADS policy_text_parse.structured_elements.clauses
```

C1 与 C2 互不依赖，都只等 B 成功。不要写进 09 的字段矩阵，也不要做成 CDC SQL。实现只认上面的 Python 脚本规约。

---

## 1. POLICY-C1 抽取产业

### 读

`gkxlumenx_dwd.policy_base_info`，`is_deleted=0`。  
对码文本用 `title`、`abstract`、`keywords`、`keypoints`、`content`、`policy_support`。  
**不用** `theme` 当查询词，也不把主题写进产业关联。

### 写

只写关联表，列见 [policy_industry_rel-MySQL.md](10-DWD-MySQL-DDL/policy_industry_rel-MySQL.md)。

| 库 | 表 | 动作 |
|---|---|---|
| `gkxlumenx_dwd` | `policy_industry_rel` | 本次槽位：新链码插入；同一 `industry_link_code` 复活（`is_deleted` 改回 0，名称更新）；本次没有的有效行改为 `is_deleted=1`。不物理删除 |
| `gkxlumenx_ads` | `policy_industry_rel` | 同一事务内按 `policy_id` 整份替换，`id` 与 `is_deleted` 与 DWD 一致 |

增量跳过：该 `policy_id` 已有 `is_deleted=0` 且 `industry_link_code` 非空的行。不要用主表 JSON 判断「已抽过」。主表没有 `related_entities`，也不要为了产业新建这一列。

无链码只留名称行（`industry_link_code` 空串）。检索降级或失败 **不写**。

### 中台入口（脚本须调用同一函数，正式 Java 门面仍缺）

| 用途 | 方法 |
|---|---|
| 按政策小批 | `POST /internal/policy/industry/enrich`（只带 `policy_id`，不带 `cursor` / `mode`） |
| 日批 | `POST /internal/industry/jobs/enrich`（`mode=incremental\|full`，`cursor`，`limit`≤100） |

GDF 日批走 Job，禁止在调度线程里同步等模型返回。正式面须经 Java 转发上述内部路径；在 Java 门面落地前，本作业状态是 **可排期、不可当产线已接通**。

---

## 2. POLICY-C2 条款结构化（条件结构化）

### 读

同一张 `policy_base_info`：`title`、`abstract`、`content`，以及已洗入的 `policy_support`（看里面有没有适用对象 / 支持方式 / 申报条件）。

### 规则

1. 正文能按「第X条」切开，就用条文头（用原文里的头，不编「第一条」）。
2. 没有「第X条」时，再按「一、」「（一）」「1.」切。
3. 规则没切开，且 `policy_support` 里也没有适用对象、支持方式、申报条件时，才把标题、摘要和正文前 1200 字送模型兜底。
4. 无密钥或模型失败：不写假条款。同一正文哈希已经试过模型则跳过，`force` 才重试。

### 写

只更新 `gkxlumenx_ads.policy_text_parse`：

| 字段 | 内容 |
|---|---|
| `structured_elements.clauses` | 条款数组 |
| `structured_elements.clause_meta` | `source`（`rule` 或 `llm`）、`content_hash`、`llm_tried` |
| `title` / `model_version` | 与本次结果一致 |

按 `policy_id` 合并。没有行则插入。**禁止** `TRUNCATE` 这张表。不写 ES。不回写 DWD。

增量跳过：`structured_elements` 已含 `clauses`。`mode=full` 或 `force` 才重做。单批 `limit`≤100。

### 中台入口（脚本须调用同一函数）

| 用途 | 方法 |
|---|---|
| 按政策 | `POST /v1/policy/clauses/enrich` |
| 日批 | `POST /v1/policy/clauses/jobs` |

网关 `/policy/**` 转到算法服务。与 C1 一样：正式日批要 Java 门面，当前 Demo 路由不能直接配进生产 DAG。

---

## 3. 验收

| 检查 | 通过 |
|---|---|
| 抽一条国内政策 | DWD 与 ADS `policy_industry_rel` 该 `policy_id` 行一致（含 `is_deleted`） |
| 主表 | `policy_base_info` 行内容与 Wave B 抽样一致，没有被 C1/C2 改写 |
| 条款 | `policy_text_parse.structured_elements.clause_meta.source` 为 `rule` 或 `llm`，`clauses` 非空或诚实跳过（无正文 / 模型失败不落假条） |
| 失败 | B 未成功时 C 不跑；C 失败不回滚已成功的 B |
| 脚本 | 两作业都是 Python，调用中台 `industry_enrich` / `industry_job`、`clause_job`；包内无第二套切条或对码 |
