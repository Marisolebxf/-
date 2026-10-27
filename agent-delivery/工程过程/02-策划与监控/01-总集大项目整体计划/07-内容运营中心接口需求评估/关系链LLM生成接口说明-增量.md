# 关系链 LLM 策略/分析意见接口说明（增量）

> 2026-10-27 新增。此接口隶属于图谱·关系链模块，**已上线**。其余接口见《CMS-JX-接口文档-live-久新对接.md》主文档。

## 端点

```
POST /api/open/cms/v1/kg/{entityType}/relations/insight
```

`{entityType}` ∈ `enterprise | policy | service`（industry 关系暂无生成需求，传了报 400）

经网关调用时前缀加 `/cms`：`http://10.50.69.111:30895/cms/api/open/cms/v1/kg/...`

## 功能

对**已存在**的一条关系链，调用大模型生成「策略/分析意见」文本。

## 请求体

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 是 | 关系行 id（从 `/relations/list` 返回的 `id` 取） |
| force | boolean | 否 | `true`=忽略缓存强制重新生成；缺省 false |

## 响应 `data`

| 字段 | 说明 |
|---|---|
| id | 关系行 id |
| insight | 生成的策略/分析意见文本（中文） |
| model | 生成模型（如 glm-5.3-flash） |
| cached | `true`=本次命中缓存直接返回（未调 LLM）；`false`=新生成 |
| generatedAt | 生成时间（缓存命中时返回上次生成时间） |

## 缓存与失效规则

- 生成结果**落库保存**（挂在关系行上），同一条关系再次调用**直接秒回缓存**，不重复调 LLM
- 关系链内容被**编辑后**（源实体/类型/目标实体任一变更），缓存自动失效，下次调用重新生成
- `force: true` 可跳过缓存强制重生成
- LLM 失败/超时（约 60s）→ 返回 `insight: ""` 且 `degraded: true`（HTTP 仍 200），稍后重试即可；失败结果**不落缓存**

## curl 示例

```bash
curl -X POST 'http://10.50.69.111:30895/cms/api/open/cms/v1/kg/policy/relations/insight' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -H 'X-CMS-Api-Key: <Key>' \
  -d '{"id":"1"}'
```

响应示例：

```json
{ "code": 0, "msg": "ok",
  "data": { "id": "1",
    "insight": "政策策略分析：依据关系链事实……实现政策效益最大化。",
    "model": "glm-5.3-flash", "cached": false } }
```

## 前端对接建议

- 「生成策略/分析意见」按钮 → 调本接口，转圈期间提示"AI 生成中（约 10-30 秒）"
- 响应里 `cached: true` 时可秒开；`degraded: true` 时提示"生成暂时不可用，请稍后重试"
- 展示与编辑回显都读本接口/库内结果，**不要每次进页面自动调**（会重复消耗 LLM 配额）；明确点「重新生成」才传 `force: true`
