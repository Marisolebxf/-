# Handoff：ENT-JAVA-KEY-STAR-SZ

- **时间**：2026-07-20
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-INTEGRATION-派单包.md` §5.4
- **状态建议**：`review`
- **接口总文档（前端联调入口）**：[`API-ENT-full-catalog.md`](./API-ENT-full-catalog.md)（76 端点全量；本单对应「重点企业 / 明星企业 / 深圳企业」，见总文档 §3 / §4）

## 1. 范围与实现

重点 **5** + 明星 **2** + 深圳 **4** = **11** 端点。

| 模块 | Java 前缀 | 端点 | Controller |
|---|---|---|---|
| 重点企业 | `/topic/v1/key-enterprise` | `kpi` · `chain-list` · `chain-subject-stats` · `qualification-summary` · `type-scale-stats` | `EnterpriseKeyEnterpriseController` |
| 明星企业 | `/topic/v1/star-enterprise` | `kpi` · `list` | `EnterpriseStarEnterpriseController` |
| 深圳企业 | `/topic/v1/shenzhen` | `kpi` · `growth-trend` · `industry-distribution` · `key-enterprise-list` | `EnterpriseShenzhenController` |

Python 前缀分别为 `/internal/gkx-search/key-enterprise/**`、`…/star-enterprise/**`、`…/shenzhen/**`。

## 2. 偏离说明

1. 网关路径 as-built：`gateway/enterprise/topic/v1/{key-enterprise|star-enterprise|shenzhen}/…`。
2. `type-scale-stats` 已按 §16.5 拆为 `TypeScaleRowItem` + `TypeScaleCell`；列表企业行用 `FeaturedEnterpriseItem`。

## 3. 产物清单

- Controllers / Services / Impl ×3
- Request：`EnterpriseKeyChainListRequest`、`EnterpriseTypeScaleRequest`、`EnterpriseStarListRequest`、`EnterpriseShenzhenTrendRequest`、`EnterpriseChainCodeRequest` 等
- `EnterpriseExtendedDTOs` 对应响应类型；Feign 追加；契约 §3.5

## 4. 验收证据

| 项 | 结果 |
|---|---|
| 11 端点三层 | ✅ |
| 编译 | ✅ |
| commit SHA | `05bddb3`（已 push `origin/dev`）|

## 5. 架构合规自检（7 条）

算法 Python ✅ · 调用链 ✅ · 不直连 ✅ · Feign 前缀 ✅ · OTel 复用 ✅ · commit 标注 `05bddb3` · demo2 N/A ✅

## 6. 开放项

联调对照 Mock；已 commit/push：`05bddb3`

## 7. Cost 回填

| 字段 | 值 |
|---|---|
| `actual_tokens` | `180_000` |
| `model_used` | `claude-sonnet-4.5` |
| `actual_cost` | `0.97` |
| `cost_warn` | `green` |
