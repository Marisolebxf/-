# 14 — DWD → 图谱（Nebula）更新逻辑

> **读者**：GDF 只读边界；**实施写图**不是 GDF CDC、不是 Java、不是本包 Wave A/B。  
> **真源**：`data-design/storage/ENT/etl/pipeline-to-nebula.md`（2026-09-01 as-built + 步2 契约）。  
> **本包诚实句**：v3 原先**没有**本卷。图谱更新**不是**「DWD 洗完自动灌图」。灌数流水线**不准顺带建图**。

## 0. 一句话

GDF 本波只把企业事实洗进 `gkxlumenx_ods` / `gkxlumenx_dwd`。图上的点边在**图谱菜单**被点时，由 Python 按独立 `op_id` 从 DWD/ADS 投影到 Nebula。Java 只转发 `/internal/*`，**禁止直连 nGQL**。禁止 Neo4j。

```text
GDF：gkx → ODS → DWD                    ← 本包 Wave A/B
ES： DWD → lumen-etl-es-py → 别名       ← 见 12；批调度 OPEN
图谱：菜单 A/B/C → 前端 → Java → Python
      /internal/entan/graph* → ADS + Nebula
灌数流水线：只装 ODS/DWD（+可选基础指标），不准 NER/RE/写 Nebula
```

---

## 1. 谁写、谁不写

| 角色 | 做 | 不做 |
|------|----|------|
| GDF | 保证下表 DWD 事实表有稳定 `org_id`、对端 ID、`update_time` | 连 graphd；跑 nGQL；在 CDC 作业里 INSERT VERTEX/EDGE |
| `lumen-etl-es-py` | 写 ES（见 `12`） | 写 Nebula |
| 企业分析 Python | 菜单触发的 NER/RE/投影 | 在灌数 `run_all` 里顺带建图（目标态禁止） |
| Java | Feign 转发 `/internal/entan/graph*` | NLP、nGQL、自造 VID |
| 前端 | 图谱菜单点 A/B/C | 直连 Python / 直连 Nebula |

现网 Demo 链（**不是**正式 lumen 链）：

```text
demo-ui-system-test
  → demo 网关（/entan/** 前插 graph Path）
  → demo-svc-platform gkx-innov
  → Feign demo-platform-entan-py:8000
  → /internal/entan/graph*
仓：demo-algo-ent-analysis
```

正式 `lumen-ui-*` / `lumen-algo-py` 写图**不在本叶设计范围内**（D12：正式链禁止回落到 `demo-*`）。正式空间名目标是一张 G `gkx_chain`；**本管线零写入正式 `gkx_chain`**。未另开 lumen 图谱叶之前，禁止在本包里编造正式 cron。

---

## 2. 触发：不是水位批，是菜单

| 档 | 何时更新图 | HTTP（前端经 Java） | Python |
|----|------------|---------------------|--------|
| A 实体识别 | 用户点「实体识别」 | `POST /v1/entan/graph/ner` | `POST /internal/entan/graph/ner` |
| B 本域边 | 用户点「本域关系」 | `POST /v1/entan/graph/intra` | `POST /internal/entan/graph/intra` |
| C 跨域挂接 | 用户点「跨域挂接」 | `POST /v1/entan/graph/hang` | `POST /internal/entan/graph/hang` |
| D 浏览 | 只读 | `GET /v1/entan/graph` | `GET /internal/entan/graph` |

- 切筛选条件**不自动**建图（与分析工作区 I2-12 同口径：要人点）。  
- B/C **必须**带 `op_id` 或 `relation_whitelist`；空白名单 = 拒绝，禁止一次 hang 偷偷写齐九种边。  
- 禁止继续用一个 `entity.run()` / `load_nebula_safe()` 当对外契约。  
- 现网灌数脚本里的「B 实体识别 + 灌 Nebula」是 **as-built 债**，目标态要从灌数剥离。

公共入参：`op_id`、`scope=one|batch`、`id=org_id`（禁止用名称/信用代码冒充）、`filter`（batch）、`mode=rule|llm`（默认 rule）、`dry_run`、`relation_whitelist`、`calc_batch_id`。

`dry_run=true`：不写 ADS、不写 Nebula、不 `ensure_schema`。

---

## 3. 空间与 VID

| | as-built（现网，不得假装已并） | 目标态（步2） |
|---|---|---|
| space | settings `entan` / 文档名 `demo_entan` | 仅 `demo_gkx_chain`（已存在才 `USE`） |
| vid 长度 | `FIXED_STRING(64)`，超长 MD5 截断 | 必须 80；超长 → `skipped.reason=vid_too_long`，禁止静默截断当成功 |
| 企业 VID | `ent:{org_id}` | 同左；值只来自 DWD `org_id` |
| 跨域点 | 名称当 VID（`ind:` / `tech:` …） | **只 FETCH** 一张 G 已有 `chain:` / `segment:` / `pol:` / `inst:` |
| 正式库 | 模型注册仍见过渡名 `gkx_enterprise` | **零写入** `gkx_chain` |
| Schema | 现网可 `CREATE SPACE` | **禁止** `CREATE SPACE` / `DROP SPACE`；只 `IF NOT EXISTS` 增量补 Tag/Edge |

`OPEN-ENT-GRAPH-VID`：64 vs 80 未并，接入一张 G 时按 80 校验，不得假装已是 80。

---

## 4. 更新什么（op_id × DWD 源）

GDF 洗好这些表，菜单才能投影。缺 ID 的行 **不上图并记账**，禁止为提高覆盖率造 `org_id` / 用名称猜 VID。

| op_id | 档 | 边/点 | DWD 源 | 上图条件 |
|-------|----|-------|--------|----------|
| `ENT_NER_ORG` | A | 点 `enterprise` `ent:{org_id}` | `enterprise_base` | 有 `org_id`；属性进 ADS `entity_recognition` / `props`，**属性不上图、A 不挂边** |
| `ENT_RE_COOP` | B | `cooperate` | `enterprise_cooperation` | 两端 `FETCH ent:` |
| `ENT_RE_INVEST` | B | `invest` | **`enterprise_invest`**（`org_id`→`inv_org_id`） | 对端须在 `enterprise_base` 且 FETCH；**股东 ODS 本波不画** |
| `ENT_RE_BELONG` | B | `parent_sub` | `enterprise_parent_subsidiary` | 母/子都有 `ent:` |
| `ENT_RE_SUPPLY` | B′ 加性 | `supply` | `enterprise_supply_chain` | 须显式白名单；**不得顶替投资** |
| `ENT_RE_INDUSTRY` | C | `industry_belong` / `located_in` | `enterprise_industry_chain` | FETCH 已有 `chain:` / `segment:`；只有产业名 → `no_stable_id` |
| `ENT_RE_TECH` | C | `produces` | 现网多靠推理 | 有稳定技术点才上；禁止 `tech:{名}` / 专利号当 VID |
| `ENT_RE_TALENT` | C | `talent_coop` | 合作表 `partner_type=talent` | 有稳定人才 ID |
| `ENT_RE_POLICY` | C | 待拍板 | **无企业→政策 DWD 边** | **本波不上图** `OPEN-ENT-GRAPH-POLICY` |
| `ENT_RE_RESEARCH` / `ENT_RE_SERVICE` | C | `research_coop` / `service_provide` | 合作表对应 partner_type | FETCH `inst:` |
| `ENT_GRAPH_BROWSE` | D | — | — | 只读 |

投资 as-built schema **没有** `invest` Edge：目标补 `CREATE EDGE IF NOT EXISTS invest (...)`，不另开 space。现网灌图脚本还没吃 `enterprise_invest`——那是实现债，不是「改用 supply 顶替」。

跳过原因对外只四码：`empty_field` / `no_stable_id` / `not_in_wave` / `vid_too_long`。禁止静默删源行。

---

## 5. 写入与幂等（更新时怎么落到图上）

```
1. Java 原样转发 op_id + scope
2. Python 按 op_id 只抽一类边/点（禁止包打天下）
3. 先写 ADS：entity_recognition / graph_node / graph_edge
4. 对将上图的 VID 做 FETCH PROP ON *；不存在 → skipped，不按名称新建他域点
5. INSERT VERTEX / INSERT EDGE（chunk=100）；同 calc_batch_id + 主键可重跑覆盖
6. source 只有真实 nGQL 成功才标 nebula；否则 ads / dry_run / rule_fallback
```

- 默认**不做删除**，**不清空**既有底图（`chain` / `pol` / `inst` 禁止 DROP）。  
- `mode=llm` 无 Key 或失败必须回退规则，出参标 `llm_fallback`。LLM 不改 DWD 源列、不发明持股比例、不造悬挂 `pol:`。  
- 失败 fail-soft：Nebula 关则跳过投影，读路径可回退 ADS `graph_node` / `graph_edge`。

目标态禁止：`DROP SPACE`、`CREATE SPACE gkx_enterprise`、继续把 `demo_entan` 当目标、名称相似度伪造 VID、灌数路径 `INSERT VERTEX|EDGE`。

---

## 6. 和 ES / GDF 的关系

| 层 | 更新节奏 | 本包要求 |
|----|----------|----------|
| ODS/DWD | GDF 贴源 + Mapping（可按 `updated_time` 增量） | Wave A/B |
| ES | 模块水位 + 10 分钟时间片 | `12`；GDF 不写 |
| 图谱 | **人点菜单**按 op 投影 | 本卷；GDF 不写 |

DWD 没洗出 `enterprise_invest.inv_org_id` / 合作对端 `partner_org_id` / 主档 `org_id`，菜单点了也只是 `skipped`，不是图库故障。

`enterprise_patent_org_rel`：给多申请人/权利人治理用，**本波不是上图边**（技术应用仍走 `ENT_RE_TECH`，且禁止专利号当 VID）。

---

## 7. 仍开的图谱 OPEN（点名，不假装已关）

| 项 | 含义 | 本包处置 |
|----|------|----------|
| `OPEN-ENT-GRAPH-VID` | as-built 64 vs 目标 80 | 只点名 |
| `OPEN-ENT-GRAPH-POLICY` | 无企业→政策边 | 本波不上图 |
| `OPEN-ENT-GRAPH-SHAREHOLDER` | 股东仅 ODS | 本波不画；不拿股东顶替投资 |
| 正式 lumen 写图链 | 未进本叶 | 禁止把 Demo Feign 写进 lumen |
| `OPEN-ENT-FLOW-01/04` | ES 批调度 / SLA | 与图谱无关，见 `12` |

---

## 8. GDF 要做什么 / 不要做什么

- **要**：按 `09`/`10`/`13` 洗出上表 DWD；投资对端 `inv_org_id` 必须能回连 `enterprise_base`；缺 ID 进治理清单。  
- **不要**：在 GDF 作业写 Nebula；把「贴源完成」理解成「图谱已更新」；用名称或信用代码冒充 VID；为图谱另建第二套企业空间。
