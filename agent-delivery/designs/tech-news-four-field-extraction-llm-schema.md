# 科技新闻四要素抽取实现方案（方案 6：LLM + JSON Schema）

> **文档定位**：详细设计说明（Design Spec），非运行代码。  
> **业务领域（硬约束）**：**科技新闻信息抽取**。语料、字段语义、样例、Prompt、评估集一律面向科技/产业技术报道；**与金融业务无关**。  
> **方案基线**：调研结论中的 **S6 — LLM Schema / JSON 结构化抽取**。下文引用的部分开源/论文原属金融或其他垂直域，**仅借鉴其工程结构与抽取范式，不继承其业务目标、事件类型或评估口径**。  
> **目标字段**：`公司名称` · `完成时间` · `完成事项` · `作用与影响`  
> **版本**：v0.3 · 2026-07-26（v0.3：按文档示例固化「完成时间」「作用与影响」科技口径）
---

## 1. 背景与目标

### 1.0 领域边界（必读）

| 维度 | 本项目 | 明确排除 |
|------|--------|----------|
| 语料 | 科技新闻、产业技术报道、科研/产品/工程成果通稿 | 财经公告、证券资讯、投研研报、行情解读 |
| 关注点 | 谁（机构）在何时完成了什么科技事项，有何技术/应用作用 | 股价涨跌、融资并购、股权质押、监管处罚、市场情绪 |
| 「影响」含义 | 技术价值、应用效果、对产业能力/用户体验/科研进展的作用 | 对二级市场、估值、资金面的影响 |
| 外部参考 | 可借鉴通用 IE / 事件抽取的流水线与 Schema 约束手法 | 不得把金融事件 Schema（质押、减持、中标金额等）当作本任务标签集 |

**原则**：方法可跨域借鉴，业务不可跨域漂移。实现、标注、Prompt、验收时若出现「涨跌、市值、募资、股权」等金融解读，视为偏离，应拒绝或忽略。

### 1.1 问题定义

给定一篇**科技新闻**正文（可附标题、发布时间、来源），自动抽取并结构化输出以下四部分内容：

| 字段 | 英文键名 | 语义定义 | 抽取形态 |
|------|----------|----------|----------|
| 公司名称 | `company_name` | 完成该科技事项的主体企业/科研机构/高校院所等（可多主体） | 优先原文 span |
| 完成时间 | `completion_time` | 事项完成、发布、上线、攻关突破或交付的时间点/时间段 | 原文 span + 规范化日期 |
| 完成事项 | `completed_matter` | 主体完成了什么科技/工程/产品成果（动作 + 对象），一句可核验事实 | 优先原文 span / 短句压缩 |
| 作用与影响 | `impact` | 该事项的技术作用、应用价值，或对产业能力/用户/科研的影响（**非金融影响**） | **允许归纳生成**，必须附 evidence |

### 1.1.1 「完成时间」「作用与影响」口径（已按示例确认）

> **决策状态**：已确认（2026-07-26）。以本文档 §13 端到端示例为口径真源，实现与标注均按此执行，不再另开业务拍板项。

**示例锚点（§13）**

| 原文线索 | 字段取值 | 口径结论 |
|----------|----------|----------|
| 「已于 **2024 年 3 月**完成首批客户交付」 | `completion_time.raw = "2024年3月"`，`normalized = "2024-03"` | **完成时间**取「科技成果实际完成/交付/落地」的时间，不是发稿日「今日」 |
| 「有助于提升质检效率并降低人工复检成本」 | `impact` 原句归纳/摘录 | **作用与影响**取原文明确写出的**技术或应用效果**，可一句概括，须能回溯证据 |

**完成时间（操作规则）**

1. 优先取与「完成事项」直接绑定的时间（完成、交付、上线、突破、投运、发布成果等）。  
2. 示例中「今日宣布」是报道动作，**不算**完成时间；「2024年3月完成交付」才是。  
3. 粒度随原文：有年到年、有月到月、有日到日；规范化写入 `normalized` + `granularity`。  
4. 仅当正文完全没有事项时间时，才回退 `published_at`，并打 `time_fallback_to_publish`。

**作用与影响（操作规则）**

1. 只抽取技术/应用层面的作用（效率、成本、能力、体验、科研价值等），如示例中的「提升质检效率」「降低人工复检成本」。  
2. 必须能在原文找到支撑句；无支撑则 `impact = null`。  
3. 不把「完成事项」本身重复写成影响；不编造原文未出现的指标数字。  
4. 允许在证据句基础上做短句归纳（paraphrase），但不得扩展事实。

### 1.2 成功标准（DoD 草案）

1. 输入一篇中文科技新闻，稳定输出符合 JSON Schema 的结构化结果。  
2. `company_name` / `completion_time` / `completed_matter` 尽可能可回溯到原文证据句。  
3. `impact` 不引入原文未支持的事实；若原文无明确影响表述，输出 `null` 或标注 `insufficient_evidence`。  
4. 提供可运行的单测样例集（≥20 篇）与人工抽检清单。  
5. 接口形态可被上层 Java REST 调用（符合「前端 → Java → Python `/internal/*`」调用链；算法仅在 Python）。

---

## 2. 方案选型说明

### 2.1 为何以方案 6 为主

| 维度 | 方案 6（LLM + JSON Schema）优势 |
|------|--------------------------------|
| 冷启动 | 无需大规模 BIO/论元标注即可出 demo |
| 字段语义 | 「作用与影响」天然适合生成式摘要，传统 span 抽取难以覆盖 |
| 工程速度 | Prompt + Schema 校验 + 少量规则即可闭环 |
| 可演进 | 后续可蒸馏为小模型，或把前三字段替换为 MRC/NER 模块 |

### 2.2 从代表性实现吸收的设计点（仅方法，不继承业务域）

> 下表「来源」中部分项目名称带有金融背景，**此处只抽取可复用的工程模式**；落地 Prompt、词表、样例必须换成科技新闻语境。

| 来源（原域可能不同） | 仅吸收的工程点 | 在本方案中的落点（科技域） |
|------|--------|------------------|
| 通用 LLM 结构化抽取包（如 fintextract 一类） | 单函数 API：原文 → 结构化字段；LLM 可插拔 | `extract(news_text) -> ExtractionResult` |
| LlamaExtract 等 Schema 抽取框架 | JSON Schema 约束 + **evidence / citations** | 每个字段附科技新闻原文证据片段 |
| 严格 JSON +「事实/影响分阶段」流水线（部分开源监测系统采用） | 规范化 → 抽取 → **事实与影响解耦** | 前三字段事实锁定后，再生成「技术/应用作用」 |
| NewsPilot 等情报系统 | 事件级抽取（非整篇糊成一段摘要） | 一篇科技新闻可输出 0..N 个成果四元组 |
| 篇章级事件抽取框架（如 DCFEE 提出的关键句+论元补全） | 长文关键句定位，避免全文硬塞 | 科技长通稿先定位候选句，再喂给 LLM |
| MRC/问答式论元抽取（竞赛中常见写法） | 角色问句模板 | Prompt 中固定四问：主体/时间/事项/科技作用 |

### 2.3 总体策略（Hybrid）

```
主路径：LLM Schema 抽取（方案 6）
辅路径：规则/词典校验（公司名、时间格式）
可选：轻量 NER 交叉验证（ORG/TIME）
影响字段：独立生成 + 一致性校验（禁止无据发挥）
```

---

## 3. 总体架构

### 3.1 逻辑架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Caller (Java REST)                      │
│              POST /internal/tech-news/extract               │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Python Extraction Service                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐ │
│  │ Ingest   │→ │ Locate   │→ │ LLM      │→ │ Validate &  │ │
│  │ Normalize│  │ Candidates│  │ Extract  │  │ Normalize   │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────┬──────┘ │
│                                                   │         │
│                          ┌────────────────────────┘         │
│                          ▼                                  │
│                   ┌─────────────┐                           │
│                   │ Impact Pass │  (可选第二轮 LLM)          │
│                   └──────┬──────┘                           │
│                          ▼                                  │
│                   ExtractionResult (JSON)                   │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 模块职责

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| **Ingest / Normalize** | 清洗 HTML、去广告噪声、统一空白与全半角 | 原始新闻 | `NormalizedDoc` |
| **Locate Candidates** | 启发式/轻量模型选出含主体、时间、成果、影响表述的候选句 | `NormalizedDoc` | `candidate_sentences[]` |
| **LLM Extract** | 按 Schema 抽取四字段 + evidence + confidence | 标题+候选句（或全文，有长度上限） | 原始 JSON |
| **Validate & Normalize** | Schema 校验、时间规范化、公司名清洗、证据句是否子串 | 原始 JSON + 原文 | 合法结果或错误码 |
| **Impact Pass（可选）** | 仅根据事实字段 + 原文影响句生成/改写 `impact` | 事实三字段 + 原文 | 最终 `impact` |

### 3.3 部署与调用约束（若接入 GKX 体系）

- **算法只在 Python**：本服务实现于 Python algo 仓（如 `demo-algo-science` / 正式 algo 服务）。  
- **调用链**：前端 → Java REST → Python `/internal/tech-news/extract`。  
- **Java 不写 NLP**：Java 只做鉴权、限流、落库、转发。  
- **可观测性**：Python 侧增加 tracing / structured logging（请求 ID、模型名、token、耗时、校验失败原因）。

---

## 4. 数据模型

### 4.1 输入模型

```json
{
  "request_id": "uuid",
  "title": "可选，新闻标题",
  "content": "必填，新闻正文纯文本",
  "published_at": "可选，ISO8601 或原文时间字符串",
  "source": "可选，媒体来源",
  "options": {
    "max_events": 3,
    "require_evidence": true,
    "enable_impact_pass": true,
    "language": "zh-CN"
  }
}
```

### 4.2 输出模型（核心 Schema）

```json
{
  "request_id": "uuid",
  "model": "qwen-xxx / gpt-xxx",
  "events": [
    {
      "company_name": ["示例科技股份有限公司"],
      "completion_time": {
        "raw": "2024年3月",
        "normalized": "2024-03",
        "granularity": "month"
      },
      "completed_matter": "发布新一代工业视觉检测平台并完成首批客户交付",
      "impact": "有助于提升制造业质检效率，降低人工复检成本",
      "evidence": {
        "company": ["……示例科技股份有限公司今日宣布……"],
        "time": ["……于2024年3月正式交付……"],
        "matter": ["……发布新一代工业视觉检测平台……"],
        "impact": ["……可显著降低人工复检成本……"]
      },
      "confidence": {
        "company_name": 0.92,
        "completion_time": 0.81,
        "completed_matter": 0.88,
        "impact": 0.74,
        "overall": 0.84
      },
      "flags": []
    }
  ],
  "meta": {
    "used_candidate_sentences": true,
    "candidate_count": 12,
    "latency_ms": 1820,
    "token_usage": { "prompt": 1200, "completion": 350 }
  }
}
```

### 4.3 字段级约定

#### 4.3.1 `company_name`

- 类型：`string[]`（一篇新闻可能有多方：发布方、合作方、客户）。  
- **主主体优先**：若存在明确「完成事项」的动作发出者，放在数组第一位。  
- 清洗：去除书名号外噪声；保留官方全称优先，简称可放在同事件的 `aliases`（可选扩展字段）。  
- 若无法判定：返回 `[]`，并加 flag `missing_company`。

#### 4.3.2 `completion_time`

- **口径**：已按 §1.1.1 / §13 示例确认——取成果完成/交付/落地时间，不取「今日宣布」类报道时间。  
- 保留 `raw`（原文）+ `normalized`（尽量 ISO 粒度：`YYYY` / `YYYY-MM` / `YYYY-MM-DD`）。  
- 优先级：事项完成时间 > 产品发布/上线时间 > 新闻发布时间（仅作回退，且需 flag `time_fallback_to_publish`）。  
- 相对时间（「昨日」「本周」）：结合 `published_at` 解析；无发布时间则保留 raw，`normalized=null`，flag `relative_time_unresolved`。

#### 4.3.3 `completed_matter`

- 一句话事实陈述，建议结构：`[主体] + [动作] + [对象/成果]`。  
- **禁止**混入评价性影响语（影响放到 `impact`）。  
- 长度建议 ≤ 80 汉字；过长则压缩，但不得改变事实。

#### 4.3.4 `impact`

- **口径**：已按 §1.1.1 / §13 示例确认——取原文中的技术/应用效果句（如「提升质检效率并降低人工复检成本」），非金融影响。  
- 语义限定为：**技术作用、应用效果、产业能力或科研进展层面的影响**。  
- 允许 paraphrase（归纳），但每条影响主张应能在 `evidence.impact` 找到支撑句；无支撑则：  
  - `impact = null`  
  - flag `insufficient_impact_evidence`  
- 禁止编造原文未出现的性能指标、用户规模、排名等数字。  
- 若原文无科技作用表述：`impact = null`，可加 flag `non_tech_impact_ignored`（忽略非科技影响）。

### 4.4 错误与 Flag 枚举（节选）

| code | 含义 |
|------|------|
| `schema_invalid` | LLM 输出无法解析/不符合 Schema |
| `missing_company` | 未识别公司 |
| `missing_matter` | 未识别完成事项 |
| `time_fallback_to_publish` | 时间回退到发稿时间 |
| `relative_time_unresolved` | 相对时间无法落地 |
| `insufficient_impact_evidence` | 影响无据 |
| `evidence_not_in_source` | 证据句不是原文子串 |
| `multi_event_truncated` | 事件数超过 `max_events` 被截断 |
| `low_confidence` | overall < 阈值（默认 0.55） |
| `non_tech_impact_ignored` | 原文影响表述为非科技向，已忽略 |
| `finance_content_skipped` | 识别为无关科技成果的内容，事件为空或降权（可选策略） |

---

## 5. 处理流水线（逐步设计）

### 5.1 Step A — 文本规范化（Ingest）

**方法参考**：通用新闻流水线中的 Normalize（清洗/去噪）阶段。

处理项：

1. HTML → 纯文本（去 script/style/导航）。  
2. 合并多余空行；统一中英文标点周围空白。  
3. 可选：移除「相关阅读 / 广告 / 免责声明」尾部模板。  
4. 计算 `content_hash`，便于日志去重与回归测试。

输出：

```python
NormalizedDoc(
  title: str,
  content: str,
  published_at: Optional[datetime],
  source: Optional[str],
  content_hash: str,
)
```

### 5.2 Step B — 候选句定位（Locate）

**方法参考**：篇章级事件抽取中的「关键句定位」思路；避免把整篇长文一次性塞进上下文。词表必须用**科技成果向**，不用金融事件词表。

启发式（v0.1 足够）：

1. 按句号/问号/叹号/分号分句。  
2. 打分特征（科技向）：  
   - 含机构名线索（公司/集团/科技/研究院/大学/实验室等）  
   - 含时间表达式（年/月/日、昨日、近日等）  
   - 含成果动词（发布、上线、开源、攻关、突破、量产、交付、试验成功、获批、投运、发表等）  
   - 含科技作用词（有助于、提升效能、降低能耗、填补空白、支撑应用、实现国产化替代等）  
3. **降权/忽略**：明显非科技语句不作为成果候选（除非同句同时描述明确技术成果）。  
4. 取 Top-K（默认 K=12）句，并保留前后各 1 句作为上下文窗口。  
5. 若正文很短（< 800 字），可跳过定位，直接全文抽取。

> **说明**：v0.1 不强制上 NER 模型；若后续精度不足，可插入轻量中文 NER 提升机构 ORG/TIME 召回。

### 5.3 Step C — LLM Schema 抽取（主抽取）

**方法参考**：LLM 单次 Schema 抽取 + evidence 约束 + 角色问句写法（通用 IE 手法）。

#### 5.3.1 Prompt 结构

```
[System]
你是「科技新闻」信息抽取助手。
只根据给定科技新闻文本抽取结构化成果事件，禁止编造。
必须输出合法 JSON，符合给定 Schema。
对每个科技成果事件回答四个角色：
1) 公司名称：哪个企业/机构完成了该科技事项？
2) 完成时间：何时完成/发布/上线/突破/交付？
3) 完成事项：完成了什么技术/产品/工程成果（事实，不含评价）？
4) 作用与影响：技术或应用上有何作用（必须有原文依据，否则 null；禁止写金融影响）？
每个字段尽量给出 evidence 原文句子（逐字拷贝）。

[User]
标题：{title}
发布时间：{published_at}
正文候选片段：
{candidate_block}

请抽取最多 {max_events} 个科技成果事件，输出 JSON。
```

#### 5.3.2 模型调用参数建议

| 参数 | 建议值 | 原因 |
|------|--------|------|
| temperature | 0 ~ 0.2 | 结构化抽取要稳定 |
| response_format | json_object / schema | 降低解析失败率 |
| max_tokens | 按事件数估算（如 1024~2048） | 避免截断 |
| timeout | 30s（可配） | 服务可用性 |

#### 5.3.3 LLM Provider 抽象

采用可插拔 LLM 客户端（不绑定某一厂商或某一垂域产品）：

```text
LLMClient.generate(messages, schema) -> str(JSON)
```

支持：OpenAI 兼容 API、通义/DeepSeek/Qwen、本地 vLLM 等。  
配置项：`model_name`、`base_url`、`api_key`（环境变量注入，禁止写死仓库）。

### 5.4 Step D — 校验与规范化（Validate）

顺序建议：

1. **JSON 解析** → 失败则触发 1 次「repair prompt」重试（仅修格式，不改事实）。  
2. **JSON Schema 校验**（Pydantic / jsonschema）。  
3. **Evidence 子串校验**：`evidence.*` 必须是原文（或候选拼接文本）的子串；失败则清空该 evidence 并降 confidence，严重时 flag `evidence_not_in_source`。  
4. **时间规范化**：调用 `dateparser` / 自研中文时间解析；写入 `normalized` + `granularity`。  
5. **公司名清洗**：去首尾空白、统一括号样式；可选对接企业别名表。  
6. **字段互斥检查**：`completed_matter` 中若大量出现「有助于/将推动」等影响措辞，尝试剥离到 `impact` 或降权。  
7. **置信度门槛**：`overall < threshold` → flag `low_confidence`（默认不丢弃，由调用方决定是否人工复核）。

### 5.5 Step E — 影响字段二阶段（Impact Pass，可选但推荐）

**方法参考**：将「事实字段」与「影响表述」分阶段处理，降低一次生成时的串扰。本阶段只产出**科技/应用作用**，不产出市场影响。

动机：一次 Prompt 同时抽四字段时，模型容易把宣传套话写进 `impact`，或把事项本身重复成影响，甚至漂移成财经评论。

流程：

1. 冻结已校验的 `company_name` / `completion_time` / `completed_matter`。  
2. 仅抽取原文中含**科技作用词**的句子作为 `impact_candidates`（过滤金融句）。  
3. 第二次 LLM 调用：  

```
已知科技事实：{fact_json}
作用/影响候选句：{impact_candidates}
请生成 impact（技术或应用层面）；若候选句无法支撑，返回 null。
禁止新增数字/客户名/排名；禁止金融解读（股价、融资、市值等）。
```

4. 再次做 evidence 校验。

开关：`options.enable_impact_pass`（默认 `true`）。

### 5.6 Step F — 响应封装

- 附 `request_id`、模型名、耗时、token。  
- 不在响应中回传 API Key / 原始 System Prompt（可按调试开关返回）。  
- 对调用方返回稳定错误码：`400` 参数错误、`422` 抽取不可用（正文空）、`500` 上游模型失败（可重试）。

---

## 6. 接口设计（Python 服务）

### 6.1 HTTP

```
POST /internal/tech-news/extract
Content-Type: application/json
X-Request-Id: <uuid>
```

**成功 200**：见 §4.2。  

**失败示例**：

```json
{
  "request_id": "uuid",
  "error": {
    "code": "empty_content",
    "message": "content must not be empty"
  }
}
```

### 6.2 Python SDK 形态（供单测/离线批处理）

```python
from tech_news_ie import extract_events

result = extract_events(
    title="……",
    content="……",
    published_at="2024-03-18",
    max_events=3,
)
print(result.model_dump_json(indent=2))
```

---

## 7. Prompt 与 Schema 细则（可直接落地）

### 7.1 JSON Schema（摘要）

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["events"],
  "properties": {
    "events": {
      "type": "array",
      "maxItems": 3,
      "items": {
        "type": "object",
        "required": [
          "company_name",
          "completion_time",
          "completed_matter",
          "impact",
          "evidence"
        ],
        "properties": {
          "company_name": {
            "type": "array",
            "items": { "type": "string" }
          },
          "completion_time": {
            "type": "object",
            "properties": {
              "raw": { "type": ["string", "null"] },
              "normalized": { "type": ["string", "null"] },
              "granularity": {
                "type": ["string", "null"],
                "enum": ["year", "month", "day", "range", null]
              }
            }
          },
          "completed_matter": { "type": ["string", "null"] },
          "impact": { "type": ["string", "null"] },
          "evidence": {
            "type": "object",
            "properties": {
              "company": { "type": "array", "items": { "type": "string" } },
              "time": { "type": "array", "items": { "type": "string" } },
              "matter": { "type": "array", "items": { "type": "string" } },
              "impact": { "type": "array", "items": { "type": "string" } }
            }
          },
          "confidence": {
            "type": "object",
            "properties": {
              "company_name": { "type": "number", "minimum": 0, "maximum": 1 },
              "completion_time": { "type": "number", "minimum": 0, "maximum": 1 },
              "completed_matter": { "type": "number", "minimum": 0, "maximum": 1 },
              "impact": { "type": "number", "minimum": 0, "maximum": 1 },
              "overall": { "type": "number", "minimum": 0, "maximum": 1 }
            }
          }
        }
      }
    }
  }
}
```

### 7.2 Few-shot 样例策略

- 准备 3~5 条短样例（覆盖：单公司单事件、多公司合作、无明确影响、只有相对时间）。  
- 样例放入 System Prompt 后半段或独立 messages（注意 token 预算）。  
- **不要**把测试集文章放进 few-shot，避免评估泄漏。

---

## 8. 工程目录建议（Python）

```text
tech_news_ie/
  README.md
  pyproject.toml / requirements.txt
  src/tech_news_ie/
    __init__.py
    api.py                 # FastAPI routes
    schemas.py             # Pydantic models
    pipeline.py            # A→F 编排
    normalize.py
    candidates.py
    llm/
      base.py
      openai_compatible.py
    prompts/
      extract_v1.txt
      impact_v1.txt
      repair_v1.txt
    validate.py
    time_normalize.py
    company_normalize.py
  tests/
    fixtures/              # 新闻原文 + 期望 JSON
    test_pipeline.py
    test_validate.py
  scripts/
    batch_extract.py
    eval_report.py
```

---

## 9. 评估与质检

### 9.1 标注规范（人工金标）

每篇样例标注：

- 事件列表（可 0 条：纯评论/无成果新闻）  
- 四字段金标 + 可选 evidence  
- 争议项记录（如「完成时间到底取签约日还是上线日」）

业务口径若有歧义（例如「完成」算发布还是交付），应登记决策项，试点期 UI/结果加「待确认」标记；**不可由实现方擅自替业务拍板**。

### 9.2 自动指标

| 字段 | 指标 | 说明 |
|------|------|------|
| 公司名称 | Exact / Soft-F1 | Soft：别名表归一后比对 |
| 完成时间 | Exact on normalized | 粒度不同时按更粗粒度匹配 |
| 完成事项 | ROUGE-L / LLM-as-Judge（辅助） | 主指标建议人工抽检 |
| 作用与影响 | 有据率 + 幻觉率 | 幻觉率优先于文采 |
| 系统 | Schema 合法率、证据命中率、P95 延迟 | 工程健康度 |

### 9.3 回归集分层

1. **Smoke**（5 篇）：每次 PR 必跑。  
2. **Core**（20~50 篇）：版本发布前必跑。  
3. **Hard**（长文、多事件、无影响、相对时间）：专项分析。

---

## 10. 风险与缓解

| 风险 | 表现 | 缓解 |
|------|------|------|
| 幻觉 | 捏造指标、用户数、技术效果 | evidence 强制；Impact Pass；无据则 null |
| **金融域漂移** | 把科技新闻抽成涨跌/融资/市值叙事 | Prompt 领域约束；金融句降权；评估集加负例 |
| 多事件混淆 | 把 A 机构事项安到 B 机构 | 事件数组化；主体与事项共现检查 |
| 长文截断 | 关键句落在后半部 | Candidate 定位；超长分段 map-reduce 再合并 |
| 时间歧义 | 「近日」「今年」 | 结合 published_at；保留 raw |
| 模型漂移 | 换模型后字段风格变化 | Schema 固化 + 科技新闻回归集门禁 |
| 成本 | token 费用高 | 候选句压缩上下文；缓存 content_hash 结果 |
| 隐私/合规 | 新闻含未公开信息被外发 | 私有化模型 / 合规网关；日志脱敏 |

---

## 11. 分阶段实施计划

### Phase 0 — 设计固化（本文档）

- [x] 字段语义与 Schema  
- [x] 流水线与模块边界  
- [x] 领域边界：科技新闻（非金融）  
- [x] 「完成时间」「作用与影响」科技口径：按 §13 示例确认（见 §1.1.1），无需再登记决策清单

### Phase 1 — 可运行原型（1~3 天）

> **沙箱落地**：`agent-delivery/designs/tech_news_ie/`（本地原型，未入 registry）

1. [x] Pydantic Schema + FastAPI 接口。  
2. [x] OpenAI 兼容 LLM 客户端（+ mock 模式）。  
3. [x] Prompt v1（含科技域约束）+ 单次抽取。  
4. [x] Schema 校验 + evidence 子串检查。  
5. [x] 5 篇**科技新闻**手工样例跑通。

### Phase 2 — 工程硬化（3~7 天）

> **沙箱落地**：`agent-delivery/designs/tech_news_ie/`（本地原型，未入 registry）

1. [x] Candidate 定位。  
2. [x] Impact Pass。  
3. [x] 时间/公司名规范化。  
4. [x] 回归测试与简单评估脚本。  
5. [x] 结构化日志与超时/重试。

### Phase 3 — 精度提升（按需）

> **沙箱落地**：`agent-delivery/designs/tech_news_ie/`（本地原型，未入 registry）

1. [x] 引入轻量 NER 交叉验证。  
2. [x] 企业别名表。  
3. [x] 难例 hard set 分析与 Prompt 迭代。  
4. [ ] 可选：用金标微调/蒸馏小模型降低推理成本（暂缓）。

### Phase 4 — 接入业务系统（按需）

> **沙箱落地**：`agent-delivery/designs/tech_news_ie/`（本地原型；正式 Java/前端仓尚未改）

1. [x] Java 对接契约文档（`docs/java-integration.md`；正式 Feign/Controller 待 registry 任务）。  
2. [x] 结果落库（沙箱 SQLite 模拟 ADS：`ads_tech_news_*`）。  
3. [x] 前端复核页展示四字段 + 证据展开（`/review`）。

---

## 12. 配置清单（示例）

```yaml
tech_news_ie:
  llm:
    base_url: ${LLM_BASE_URL}
    api_key: ${LLM_API_KEY}
    model: qwen2.5-72b-instruct
    temperature: 0.1
    timeout_sec: 30
  extract:
    max_events: 3
    candidate_top_k: 12
    short_doc_char_threshold: 800
    enable_impact_pass: true
    confidence_threshold: 0.55
    max_repair_retries: 1
  normalize:
    prefer_full_company_name: true
```

---

## 13. 示例：端到端期望行为

> **口径真源**：本示例同时作为「完成时间」「作用与影响」的操作样板（见 §1.1.1）。

**输入（节选）**

> 标题：示例科技发布工业视觉平台  
> 正文：示例科技股份有限公司今日宣布，其新一代工业视觉检测平台已于 2024 年 3 月完成首批客户交付。该平台可自动识别产线缺陷，有助于提升质检效率并降低人工复检成本。

**期望输出（简化）**

```json
{
  "events": [
    {
      "company_name": ["示例科技股份有限公司"],
      "completion_time": {
        "raw": "2024年3月",
        "normalized": "2024-03",
        "granularity": "month"
      },
      "completed_matter": "新一代工业视觉检测平台完成首批客户交付",
      "impact": "有助于提升质检效率并降低人工复检成本",
      "evidence": {
        "company": ["示例科技股份有限公司"],
        "time": ["已于 2024 年 3 月完成首批客户交付"],
        "matter": ["新一代工业视觉检测平台已于 2024 年 3 月完成首批客户交付"],
        "impact": ["有助于提升质检效率并降低人工复检成本"]
      }
    }
  ]
}
```

---

## 14. 参考实现与文献（方法借鉴清单）

> **再次声明**：下列资料用于学习「怎么做结构化抽取」，**不是本项目的业务需求来源**。本项目验收只认科技新闻四字段，不认金融事件标签体系。

| # | 资料 | 可借鉴 | 不可照搬 |
|---|------|--------|----------|
| 1 | 通用 LLM Schema 抽取实践（含部分开源新闻抽取包） | 单次调用出 JSON、LLM 可插拔 | 其默认「财经字段」或投研摘要目标 |
| 2 | LlamaExtract 等 | Schema + evidence/citations | 财报/SEC 字段模板 |
| 3 | 严格 JSON 分阶段流水线类开源项目 | 事实与影响解耦、校验门禁 | 「市场影响评分」、交易向推送 |
| 4 | NewsPilot 等 | 事件级抽取思路 | 投资日报/持仓洞察 |
| 5 | 篇章级事件抽取论文（如 DCFEE） | 关键句 + 论元补全 | 股权质押等金融事件类型与论元角色 |
| 6 | MRC 式论元抽取竞赛方案 | 角色问句写法 | 金融事件 Schema 与迁移设定 |
| 7 | IBM IE 综述等 | NER / 事件抽取任务边界 | — |

配套调研画布：`tech-news-ie-survey.canvas.tsx`（阅读时同样以**科技域**理解，忽略其中金融示例的业务含义）。

---

## 15. 下一步建议

沙箱 Phase 0–4 已完成。建议顺序：

1. 阅读 `tech_news_ie/docs/HANDOFF-sandbox.md` 与 `formal-migration-plan.md`  
2. 新建 registry 任务并指定 `supervised_by`  
3. Phase A：迁入 `demo-algo-science`  
4. Phase B：Java 转发 + ADS  
5. Phase C：正式复核 UI（Design.md / Arco）

本地演示：

```powershell
cd agent-delivery/designs/tech_news_ie
$env:TECH_NEWS_IE_MODE = "mock"
.\.venv\Scripts\uvicorn tech_news_ie.api:app --host 127.0.0.1 --port 8010
# 打开 http://127.0.0.1:8010/review
```
