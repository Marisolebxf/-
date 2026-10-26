> **历史包同文**：现行施工只认 [v2](../GDF-POLICY-WORKPACK-v2/12-DWD后加工-抽取产业与条款结构化.md)。本目录 `scripts/` 与 v2 同文，避免打开本文件仍按内部 HTTP 配置。调度说明在 [v2 的 15](../GDF-POLICY-WORKPACK-v2/15-GDF触发调度与回执.md)。

# 12 — Wave C：DWD 完成后的抽取产业与条款结构化

> **读者**：GDF。把本目录 `scripts/` 下两个 Python 文件复制到 GDF 的 Python 节点（人工拷贝或同步均可），在节点上配置并执行。  
> **前置**：国内、国际两张平面当日 Wave B 都 `success`。只完成贴源，或任一平面 Mapping 失败，不跑。  
> **不配置 HTTP**。GDF 不需要、也不要配置国科信内部地址。加工就是这两份脚本。  
> **与 Wave B 的边界**：09 只洗主表。本文件两作业不改 `policy_base_info` 任何列（含 `theme`、`policy_support`）。  
> **何时跑**：见 [v2 的 15](../GDF-POLICY-WORKPACK-v2/15-GDF触发调度与回执.md)。  
> **键**：关联表和条款表都只有 `policy_id`，没有 `source_plane`。两平面若 `policy_id` 相同，脚本先退出、不写。不改 UK 来绕。

派单口语里的「条件结构化」就是本文件的 **条款结构化**：从正文拆条款，并抽出额度与准入条件。不是把 `policy_support` 再洗一遍。

## 脚本（配进 GDF）

节点需要 Python 3.9+ 和 `pymysql`。本包不带安装清单，按 GDF 自己的 Python 环境准备。口令不进本包。

| 作业 | 文件 | 日批命令 |
|---|---|---|
| POLICY-C1 抽取产业 | `scripts/policy_c1_industry.py` | `python policy_c1_industry.py --limit 100` |
| POLICY-C2 条款结构化 | `scripts/policy_c2_clauses.py` | `python policy_c2_clauses.py --limit 100` |

重做一条：加上 `--policy-id <id> --force`。`--limit` 只能是 1 到 100。退出码 0 才算成功。

| 环境变量 | 含义 |
|---|---|
| `POLICY_MYSQL_HOST` / `POLICY_MYSQL_PORT` / `POLICY_MYSQL_USER` / `POLICY_MYSQL_PASSWORD` | 产线 MySQL。端口默认 3306 |
| `POLICY_DWD_DB` | 默认 `gkxlumenx_dwd` |
| `POLICY_ADS_DB` | 默认 `gkxlumenx_ads` |
| `EMBED_BASE_URL` / `EMBED_API_KEY` / `EMBED_MODEL` | C1 向量化。地址为空则本条不写 |
| `MILVUS_URI` / `MILVUS_TOKEN` / `MILVUS_COLLECTION_PREFIX` | C1 检索。地址为空则本条不写。集合前缀默认 `gkxlumen_industry_` |
| `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL` | 仅 C2 规则切不开时使用。密钥为空则不写假条款。模型默认 `glm-5.3-flash` |

不连库自检：`python policy_c1_industry.py --self-check` 与 `python policy_c2_clauses.py --self-check`。缺表时脚本不建表，直接失败。空表归 `SYSINT-06-03-DDL-L01`，DDL 在本包 `10/`。

禁止把 `demo_gkxlumenx_*` 配成目标库。禁止在 CDC / SeaTunnel 里再写一套切条或对码。

---

## 0. 总流程

```mermaid
flowchart TD
  A[国内与国际两张平面当日 Wave B] --> B{两张都是 success}
  B -->|否| Z[不跑 C]
  B -->|是| C1[POLICY-C1 抽取产业]
  B -->|是| C2[POLICY-C2 条款结构化]
  C1 --> R1{C1 退出码}
  C2 --> R2{C2 退出码}
  R1 -->|非 0| F1[只记 C1 失败。不回滚 B。C2 照常]
  R2 -->|非 0| F2[只记 C2 失败。不回滚 B。C1 照常]
```

1. Wave A 贴源，Wave B 把两张源洗进 `gkxlumenx_dwd.policy_base_info`。
2. 两张平面当天都 `success` 之后，C1、C2 各跑一次。两作业互不依赖。
3. 任一作业失败只记该作业。已成功的 B 不回滚，另一作业不跟着标失败。
4. 不写进 09 的字段矩阵，也不做成 CDC SQL。

---

## 1. POLICY-C1 抽取产业

```mermaid
flowchart TD
  S[读 policy_base_info] --> K{已有有效链码且未加 force}
  K -->|是| SK[跳过]
  K -->|否| CH[切块：标题、关键词、正文]
  CH --> E{有可用块}
  E -->|否| NW1[不写]
  E -->|是| SE[每块向量检索，取前 5]
  SE --> D{任一块检索失败}
  D -->|是| NW2[不写，不造链码]
  D -->|否| SC[同一 vid 取最高分，最多留 5 条]
  SC --> G{分不低于 0.55，或分不低于 0.45 且名称出现在该块}
  G -->|否| NW3[不写空链码]
  G -->|是| W[DWD：新链码插入，同码复活，本次没有的有效行改为 is_deleted=1]
  W --> ADS[同一事务按 policy_id 替换 ADS 同名表，id 与 is_deleted 一致]
```

1. 只读 `is_deleted=0` 且 `IFNULL(is_history,0)=0` 的行。这是用数过滤，不是 Wave A/B 的取数条件。`is_history` 为 `NULL` 视为当前，不改写成 0。
2. 查询文本只用 `title`、`keywords`，以及 `content`（空则用 `abstract`）。标题和关键词各一块；正文按 `。；;` 和换行切开，丢掉套话，每块最多 120 字，正文最多 12 块。不用 `theme`，也不用 `keypoints`。
3. 每块先做向量，再在集合 `gkxlumen_industry_anchor`（前缀可改）里检索。向量地址或 Milvus 地址缺失、调用失败，这条政策不写。
4. 同一 `vid` 取各块最高分。分 ≥ 0.55 就留下；分 ≥ 0.45 且链名（不少于 3 字、不是套话）出现在打出该分的那一块里，也留下。最多 5 条。没有过线的不插入空 `industry_link_code`。
5. 增量：该 `policy_id` 已有 `is_deleted=0` 且 `industry_link_code` 非空则跳过。不用主表 JSON 判断已抽过。`--force` 重做。
6. 写入见下表。不改主表。

| 库 | 表 | 动作 |
|---|---|---|
| `gkxlumenx_dwd` | `policy_industry_rel` | 新链码插入；同一 `industry_link_code` 复活（`is_deleted` 改回 0，名称更新）；本次没有的有效行改为 `is_deleted=1`。不物理删除 |
| `gkxlumenx_ads` | `policy_industry_rel` | 同一事务内按 `policy_id` 整份替换，`id` 与 `is_deleted` 与 DWD 一致 |

列见 [policy_industry_rel-MySQL.md](10-DWD-MySQL-DDL/policy_industry_rel-MySQL.md)。

---

## 2. POLICY-C2 条款结构化（条件结构化）

```mermaid
flowchart TD
  S[读同一批主表行] --> H{已有条款且未加 force}
  H -->|是| SK[跳过]
  H -->|否| A{正文或摘要能按第X条切开}
  A -->|能| R1[保留原文条头并分类，source=rule]
  A -->|不能| B{能按 一、 或 （一） 或 1. 切开}
  B -->|能| R1
  B -->|不能| C{policy_support 里有适用对象、支持方式或申报条件}
  C -->|有| R2[抬成一条。不编条号，不编金额。source=elements]
  C -->|没有| L{同一正文哈希已经试过模型且未加 force}
  L -->|是| SK2[跳过]
  L -->|否| M{配了模型地址和密钥}
  M -->|没有| NW[不写假条款]
  M -->|有| LLM[只送标题、摘要前 400 字、正文前 1200 字]
  LLM --> OK{摘录是窗口里的连续原文}
  OK -->|不是| DROP[丢掉该条。金额或条号不在原文里也丢掉]
  OK -->|是| KEEP[留下]
  R1 --> WR[按 policy_id 合并 ADS policy_text_parse]
  R2 --> WR
  KEEP --> WR
```

1. 行范围与 C1 相同。读 `title`、`abstract`、`content`，以及 `policy_support` 里的适用对象、支持方式、申报条件。
2. 先按「第X条」切，条头用原文，不编「第一条」。没有再按「一、」「（一）」「1.」或「1、」切。
3. 规则没切开，才看 `policy_support`。能抬出对象、方式或条件时写一条，`source=elements`，条号和金额留空。
4. 仍然没有，才调模型。无密钥、调用失败，或摘录不是原文连续片段：不写假条款。同一正文哈希已经试过则跳过，`--force` 才重试。模型返回空时只记下 `llm_tried` 和哈希，不编条款。
5. 类别只在这六类里：责任主体、保障机制、补贴标准、准入条件、政策目标、扶持措施。金额只认原文里的「亿元 / 万元 / 元 / % / 个百分点」。
6. 日批每次最多处理 100 条尚未写过条款、且不是「同一哈希已试过模型」的行。已经写过的不占这 100 条名额。

只更新 `gkxlumenx_ads.policy_text_parse`：

| 字段 | 内容 |
|---|---|
| `structured_elements.clauses` | 条款数组 |
| `structured_elements.clause_meta` | `source`（`rule` / `elements` / `llm`）、`content_hash`、`llm_tried` |
| `title` / `model_version` | 与本次结果一致 |
| `update_time` | 本次写入时间 |

按 `policy_id` 合并 JSON。没有行则插入，只写上表这些列。表上若另有无默认值的必填列，本条失败并退出，不猜列。禁止 `TRUNCATE`。不写 ES。不回写 DWD。

---

## 3. 验收

| 检查 | 通过 |
|---|---|
| 抽一条国内政策 | DWD 与 ADS `policy_industry_rel` 该 `policy_id` 行一致（含 `is_deleted`） |
| 主表 | `policy_base_info` 行内容与 Wave B 抽样一致，没有被 C1/C2 改写 |
| 条款 | `clause_meta.source` 为 `rule`、`elements` 或 `llm`。无正文或模型失败时不落假条 |
| 失败 | B 未成功时 C 不跑；C 失败不回滚已成功的 B |
| 脚本 | GDF 节点上跑的是本目录 `scripts/` 两份文件。`--self-check` 通过。不配置内部 HTTP |
