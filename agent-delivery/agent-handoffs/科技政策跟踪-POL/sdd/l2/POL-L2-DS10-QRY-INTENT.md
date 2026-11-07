# POL-L2-DS10-QRY-INTENT · 科创政策全景 · 智能检索意图拆解

- 日期：2026-11-08
- 监管：`human:淮政玮`
- 性质：检索条件预处理（同步）。挂在多维检索查询旁，**不**新造 `metric_id`，**不**改 D4。
- 上游：`POL-L2-DS10-QRY-ARCH` / `POL-L2-DS10-QRY-API`；SRS 197 检索条件设置（智能检索 Tab）
- 边界：不是序号 237 政策文本解析，也不是核增 606 政策语义理解。不做向量召回。

## 1. 目标

用户在「智能检索」输入一句自然语言（如「深圳近三年市级人工智能扶持政策」）。服务端同步拆成现有筛选项 + 残差关键词；前端填 chips / filters 后仍走 `GET .../panorama/search`。

## 2. 调用链

浏览器 → `gkxlumen-display` → `gkxlumen-topic-policy` → `lumen-algo-py`。Java 不调模型、不连库、不做 NLP。

| 层 | 路径 |
|---|---|
| 浏览器 | `POST /display/v1/policy/panorama/query-intent` |
| 专题门面 | `POST /topic/v1/policy/query-intent` |
| Python | `POST /internal/policy/query-intent` |

超时建议 ≤ 5s。超时、无 Key、非法 JSON 均降级：返回 `understood=false`、`narration` 为 `fallback` 或 `no_key`，HTTP 仍成功。前端再跑本地词表 `parseDisplayPolicyQuery`，再不行整句当 keyword。

## 3. 请求

```json
{ "text": "深圳近三年市级人工智能扶持政策" }
```

`text` 为空则不调 LLM，直接 `understood=false`、`narration=fallback`。

## 4. 响应（闭集）

```json
{
  "understood": true,
  "chips": [
    { "fieldKey": "region", "fieldLabel": "适用地区", "displayValue": "深圳" },
    { "fieldKey": "level", "fieldLabel": "政策效力级别", "displayValue": "市级" },
    { "fieldKey": "industry", "fieldLabel": "行业领域", "displayValue": "人工智能" },
    { "fieldKey": "publishYear", "fieldLabel": "发布年份", "displayValue": "2023–2025" }
  ],
  "filters": {
    "category": "all",
    "industry": ["人工智能"],
    "department": "all",
    "region": "shenzhen",
    "level": "municipal"
  },
  "publish_year_from": "2023",
  "publish_year_to": "2025",
  "keyword_residual": "扶持政策",
  "narration": "ok"
}
```

字段约定：

| 字段 | 说明 |
|---|---|
| `filters.region` / `level` / `category` / `department` | 与展示页 filters 码一致（如 `shenzhen`、`municipal`、`sci-tech`）；未识别为 `all` |
| `filters.industry` | 展示用文案或产业码列表；禁止编造不存在的 `INB*` |
| `publish_year_*` | 四位年。相对短语（近三年）由 **服务端日历规则** 落年，不以模型口述数字为准 |
| `keyword_residual` | 去掉已结构化片段后的残差；可空 |
| `narration` | `ok` \| `fallback` \| `no_key`。业务 UI 可不展示 |

Prompt 资产：`lumen_common/prompts/policy/query_intent.v1.txt`。改语义升版本。

## 5. 与 197 / 606 的关系

- 197 结构化筛选与关键词检索不变；本资源只服务智能检索 Tab 的预处理。
- 606 / `M_POLICY_TEXT_PARSE` 仍是政策正文语义，不挂本资源，不写成已上线。

## 6. 实现叶（本页签收后）

`POL-L2-DS10-QRY-INTENT-IMPL-PY` → `…-IMPL-JAVA`（topic + display 透传）→ `…-WIRING-L01`（前端）→ 合规用例追加一行。
