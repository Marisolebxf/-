# POL-CLAUSE-BATCH-L01 · 政策条款结构化跑批

> 联调台菜单。页面走 `demo-ui-system-test` → `demo-platform-gateway` `/policy/**` → `demo-algo-ent-analysis`。不新建 Java 门面。不是 lumen 复刻单。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 接单时已 `in_progress`。同会话把未提交的「抽取产业」菜单一并推上 `dev`。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用产业跑批的 limit≤100、live 禁写和 `SeedHelpBadge`。模型只接已有 `entan.common.llm_client`，灌数模块不引用。未跳过失败不编条款、正式库禁写。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单叶联调台，本机未挂 Headroom。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | 无新图 |
| 图 diff | 未改存储流图。调用边仍是联调台：`demo-ui-system-test` → `demo-platform-gateway` `/policy/**` 剥前缀 → `demo-algo-ent-analysis` `/v1/policy/clauses/*`。 |
| 会签态 | 不适用（本叶不改已会签图） |

## 范围与实现

**做**：政策分析算法库左侧增加「条款结构化」。规则先切条；明细已有要素就回显；只对残量调一次模型。灌数不调模型。

### 菜单

- 「抽取产业」`/policy/enrich`：原基础指标上的产业跑批整块移出。
- 「条款结构化」`/policy/clauses`：指定 `policy_id`（最多 20）或增量/全量跑批，limit≤100，正式库禁用。

### 规则与模型

1. 先认「第X条」；没有再认「一、」「（一）」「1.」。条号用原文标记，不编「第一条」。
2. 已有适用对象 / 支持方式 / 申报条件时只回显，不调模型。
3. 正文还在、规则没切开、要素为空时，才送标题、摘要和正文前 1200 字。摘录必须是这段原文的连续片段；原文没有的金额和条款号丢掉。同一正文哈希已经试过则跳过，`force` 才重试。没密钥不记「已试过」。调用失败或抽空不编条款。

### 存储

- 写入 Demo ADS `policy_text_parse.structured_elements.clauses`，附 `clause_meta`（`source` / `content_hash` / `llm_tried`）。
- `model_version`：规则 `clause-rule-v1`，模型 `clause-llm-{模型名}`。
- 不 `TRUNCATE`。基础指标「重灌」仍会清空该表，页内已说明。

### API

| 用途 | 路径 |
|------|------|
| 指定政策 | `POST /policy/v1/policy/clauses/enrich` |
| 跑批 | `POST /policy/v1/policy/clauses/jobs` |

网关剥掉 `/policy` 后打到 Python `/v1/policy/clauses/enrich` 与 `/jobs`。

**不做**：灌数调用模型、新建 Java、放开 100 封顶、展示页条款抽屉改接这张表。

## 偏离

| # | 相对建单 DoD | 理由 / as-built |
|---|--------------|-----------------|
| 1 | 建单写「只切第X条、不做 LLM」 | 用户 2026-10-21 裁定：规则加宽；模型兜底只存在于「条款结构化」菜单。灌数 `polan/text/parse.py` 仍无模型调用。 |
| 2 | 未打现网网关 | 单测覆盖切条、禁假条款、同哈希不重试、limit>100。本机前端无 `node_modules`，页面未做浏览器走查。 |

## 产物清单

- `demo-ui-system-test` `e7659a0311765ad64e21f28e32a15dd83be690d1`
- `demo-algo-ent-analysis` `1fae9e037a37224a2b920490ec0e5f22ae8fe5cb`
- 本 handoff

## 验收证据

- `python -m pytest tests/test_policy_clause_job.py -q` → `11 passed`
- 灌数文件断言：`polan/text/parse.py` 无 `llm_client`；`scripts/run_all_policy.py` 无 `clause_job`

### 人怎么点一遍

1. 顶栏「政策」保持 Demo，打开 **政策分析 → 条款结构化**。
2. 输入一条已在 DWD 的 `policy_id`，点 **抽取条款**。有「第X条 / 一、 / （一） / 1.」应看到 coded；只有适用对象时应看到要素回显。
3. limit≤100 点 **开始跑批**。无密钥时残量显示「无模型密钥」，不写假条款。

## 问题清单

- 展示系统政策详情抽屉里的条款仍是 Mock，本叶没有改那条读路径。
- 现网网关若未把 `/policy/v1/policy/clauses/**` 剥到算法服务，页面会 404。本叶未新增 Java 路由。

## 修改内容

- 联调台：基础指标去掉产业跑批；新增「抽取产业」「条款结构化」。
- 算法：`polan/clause_job.py` 规则切条 + 残量模型；路由挂到 `api/main.py`。
- 灌数：`polan/text/parse.py` 只加「禁止调模型」说明，解析逻辑未改。

## 测试结果

- `tests/test_policy_clause_job.py`：11 passed（2026-10-21）
- 未起前端，未打网关，未对 Demo MySQL 实写

## 遗留风险

- 基础指标重灌会 `TRUNCATE policy_text_parse`，条款结果会被清掉。
- 模型摘录必须整段出现在送入窗口里；模型改写句子会被丢掉，残量可能显示「模型未抽出」。
- 增量用 `structured_elements` 是否包含 `"clauses"` 判断已处理。模型抽空也会写入空数组，同一正文不再自动重试，除非 `force`。

## CI/CD（必填）

- 分支：两仓均为 `origin/dev`
- commit：
  - `demo-ui-system-test` `e7659a0311765ad64e21f28e32a15dd83be690d1`
  - `demo-algo-ent-analysis` `1fae9e037a37224a2b920490ec0e5f22ae8fe5cb`
- pipeline URL / ID：push 已成功，未回读 GitLab pipeline
- 部署：两仓 CI 跟踪 `dev`；本叶未确认 rollout
- dev 测试：见上面三步；本机未点

## 可观测性（建议）

- 前端沿用 `src/utils/request.ts` 的 `X-Trace-Id` / `traceparent`
- Python 本叶未新增 span。模型失败只打 `clause llm fallback failed` 日志

## 涉及文件

- `demo-ui-system-test/src/views/policy/policyMenuConfig.ts`
- `demo-ui-system-test/src/views/policy/pages/BasicPage.vue`
- `demo-ui-system-test/src/views/policy/pages/EnrichPage.vue`
- `demo-ui-system-test/src/views/policy/pages/ClausePage.vue`
- `demo-ui-system-test/src/router/index.ts`
- `demo-ui-system-test/src/api/policy/index.ts`
- `demo-algo-ent-analysis/polan/clause_job.py`
- `demo-algo-ent-analysis/polan/text/parse.py`
- `demo-algo-ent-analysis/api/policy_clause_routes.py`
- `demo-algo-ent-analysis/api/main.py`
- `demo-algo-ent-analysis/tests/test_policy_clause_job.py`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python | ✅ 切条与模型调用都在 `demo-algo-ent-analysis` |
| 调用链 | ✅ 联调台前端 → demo 网关 `/policy/**` → Python。无新 Java，前端不直连 Python |
| 图谱 | ✅ 未写图 |
| 可观测 | ✅ 前端沿用 request 头；Python 未加新 span |
| CI/CD | ✅ 两仓已推 `origin/dev`，未 force |
| D12 | ✅ 只改 demo 联调台与 demo 算法仓，未调用 lumen 服务 |
| D14 | ✅ 未写对象存储 |
| 数据 | ✅ 只准备写 Demo ADS；`assert_demo_mysql_targets` 拒绝非 demo MySQL；失败不填假条款 |
| D8 / D9 / D10 | N/A（Element Plus 联调台，不是 lumen 复刻页，无指标卡） |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 140000 |
| model_used | grok-4.7 |
| actual_cost | 0.76 |
| cost_warn | green |

口径：按 frontend 80/20、B 档 `$3/$15` per 1M 估算。`140000×0.80×3/1e6 + 140000×0.20×15/1e6 = 0.756`。会话模型是 Grok 4.7，无控制台分项 token。
