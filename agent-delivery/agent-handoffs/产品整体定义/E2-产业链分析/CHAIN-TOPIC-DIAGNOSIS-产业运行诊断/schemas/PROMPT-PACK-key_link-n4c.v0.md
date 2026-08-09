# PROMPT PACK · key_link N4c（竞争格局 + 技术趋势）v0

> **prompt_pack_version**：`key_link.n4c.prompts.v1`  
> **挂载节点**：GRAPH `annotate` 子步 **N4c**（对外仍报 `stage_code=annotate`）  
> **Context Pack Schema**：`chain.key_link.n4c_context_pack.v1.schema.json`  
> **LLM 输出 Schema**：`chain.key_link.n4c_llm_output.v1.schema.json`  
> **落盘映射**：输出 → `sections.competition` + `sections.tech_trends`（补 `schema_version` / `degraded`）  
> **状态**：讨论草稿；不接真模型也可按本包做 Mock LLM。

---

## 0. 入门：Context vs Prompt

| 概念 | 是什么 | 变不变 |
| --- | --- | --- |
| **Context Pack** | 这一次任务「允许模型看见的事实托盘」 | 每 Job 不同（跟对象/分数走） |
| **Prompt Pack** | 系统角色、任务说明、禁止项、输出格式（版本化模板） | 跨 Job 相对稳定，升版改 `prompt_pack_version` |

口诀：**数字在 Context 里算好；Prompt 只教模型怎么说话、怎么填 JSON。**

---

## 1. 何时跑 N4c / 何时降级

| 条件 | 行为 |
| --- | --- |
| LLM 可用 + Context Pack 校验通过 | 调模型；Loop ≤ `llm_retry_max`（默认 2） |
| LLM 超时/不可用 | **降级**：`competition`/`tech_trends` 空内容 + `degraded=true`，**不**让整个 Job 失败（除非产品改为硬失败） |
| Context 缺五环节或关键依据自相矛盾 | 不调模型；N4 失败或降级（推荐：降级叙述，保留 4a/4b） |
| 输出不过 Schema / 事实冲突 | regenerate；用尽则降级或 `LLM_SCHEMA_FAILED` / `LLM_FACT_CONFLICT` |

推荐默认：**叙述可降级，关键判定不可降级假成功**（4a 已是规则）。

---

## 2. System Prompt（模板）

```text
你是产业链分析助手，服务于政府与园区决策场景。
你的唯一任务：根据给定 Context Pack，生成「竞争格局」与「技术趋势」的结构化 JSON。

硬性规则：
1. 只使用 Context 中出现的事实；不得发明数字、企业或比例。
2. key_nodes（关键环节）只读，不得增删改。
3. 只输出一个 JSON 对象，键为 competition 与 tech_trends，不要 Markdown、不要代码围栏、不要解释性前后文。
4. 语言：简体中文；表述克制、可核对，避免营销口号。
5. 禁止出现：已完成实时全网检索、断链、以及任何可编辑正式权重/阈值的建议。
6. 遵守 Context.output_contract 中的长度上限。
```

---

## 3. User Prompt（模板，运行时填充）

```text
【任务】为下列产业链生成竞争格局与技术趋势 JSON。
【产业链】{{chain.chain_name}}（id={{chain.chain_id}}）
【输出契约】schema={{output_contract.schema_ref}}；overview≤{{output_contract.max_overview_chars}}字；每环节 points≤{{output_contract.max_points_per_stage}}；trends≤{{output_contract.max_trend_items}}。

【五环节事实】
{{#each stages}}
- {{label_zh}}({{stage_key}}): 关键={{is_key_node}} tag={{key_tag}} 高端化={{high_end_index_display}} 企业数={{enterprise_count}} 边界={{function_boundary}}
{{/each}}

【已判定关键（只读）】
{{#each key_nodes}}
- {{label_zh}}: {{reason_text}}
{{/each}}

【代表企业短名单】
{{#each enterprises_shortlist}}
- {{name}} @ {{related_stage_keys}} {{industry_direction}}
{{/each}}

【检索摘要】
{{#if retrieval_snippets}}
{{#each retrieval_snippets}}
- [{{date}}] {{title}}: {{summary}} ({{source_label}})
{{/each}}
{{else}}
（无检索摘要；请仅基于上述结构化事实归纳，勿声称已检索全网。）
{{/if}}

【禁止项】
{{#each prohibitions}}
- {{this}}
{{/each}}

请直接输出 JSON。
```

> 实现可用任意模板引擎；关键是**字段来自 Context Pack**，不要手写第二套事实。

---

## 4. 期望输出示例（合法）

```json
{
  "competition": {
    "overview": "研发与设计环节主体相对集中，制造环节参与者更多、竞争更分散。",
    "by_stage": [
      { "stage_key": "rd", "points": ["专利与样品能力向头部集中"] },
      { "stage_key": "manufacturing", "points": ["封装模组参与主体多", "价格竞争更明显"] }
    ]
  },
  "tech_trends": {
    "items": [
      {
        "title": "Mini/Micro LED 渗透",
        "summary": "显示与车灯需求带动上游研发与设计投入。",
        "stage_keys": ["rd", "design"]
      }
    ]
  }
}
```

映射到 Result section 时由 Worker 追加：

```text
competition.schema_version = chain.key_link.competition.v1
competition.degraded = false
tech_trends.schema_version = chain.key_link.tech_trends.v1
tech_trends.degraded = false
```

---

## 5. Loop（校验 → 重试）

每次模型返回后：

1. **JSON 解析**失败 → retry（附错误：「输出不是合法 JSON」）  
2. **对照** `n4c_llm_output.v1` Schema 失败 → retry（附 validator 路径）  
3. **事实冲突检查**（实现侧）：  
   - `by_stage[].stage_key` / `tech_trends.stage_keys` ⊆ 五码  
   - overview/points/summary 中抽取的数字必须出现在 Context.stages / key_nodes / enterprises 文本中（简单子串或规范化匹配）  
   - 不得出现 Context 没有的企业名（若做了抽名）  
4. 仍失败且 retry 用尽 → **降级空叙述**（推荐）或 `Complete` 前让 N4 带 `LLM_*` 失败（产品可选）

重试 User 追加段：

```text
【上次输出不合格】
原因：{{validation_error}}
请仅修正 JSON，仍遵守全部禁止项与 Context 事实。
```

---

## 6. 降级载荷（不调模型时）

```json
{
  "competition": {
    "schema_version": "chain.key_link.competition.v1",
    "overview": "",
    "by_stage": [],
    "degraded": true,
    "degrade_reasons": ["llm_unavailable"]
  },
  "tech_trends": {
    "schema_version": "chain.key_link.tech_trends.v1",
    "items": [],
    "degraded": true,
    "degrade_reasons": ["llm_unavailable"]
  }
}
```

同步写入 Result.`honesty.degraded` / `degrade_reasons`（可与 section 级降级合并去重）。

---

## 7. 可观测（建议埋点字段）

| 字段 | 说明 |
| --- | --- |
| `prompt_pack_version` | 本包版本 |
| `context_pack_hash` | Context JSON 规范化哈希（不含密钥） |
| `llm_model` | 模型名 |
| `llm_attempt` | 1..N |
| `llm_latency_ms` | |
| `validation_error_code` | schema / fact_conflict / parse |
| `degraded` | bool |

---

## 8. 与前后文的边界

| 会做 | 不会做 |
| --- | --- |
| 写竞争格局、技术趋势文案 | 改 `is_key_node` / 高端化指数 |
| 引用 Context 内企业名做定性描述 | 编造新企业或融资额 |
| 降级为空 | 假装「实时全网检索完成」 |

4a/4b **不走**本 Prompt Pack。

---

## 9. 修订

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0 | 2026-08-09 | N4c Context/Prompt/Output/Loop/降级初稿 |
