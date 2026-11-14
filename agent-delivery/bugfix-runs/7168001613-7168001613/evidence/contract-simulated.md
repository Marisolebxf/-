# 契约级 SIMULATED 集成验证（三仓字段链路对照）

方法：逐仓读取真实源码，对照三方对同一字段的序列化名与读取名（非运行时联调，标 SIMULATED）。

## 证据链（逐仓源码引用）

### 1. ui_topic（发送方）
`src/api/enterprise/types/search.ts` `EntMetaRequest`：
- `chain_code?: string`、`chain_codes?: string[]`
`src/api/enterprise/types/stats-featured.ts` `EntDistributionRequest`：
- `chain_code?: string`
`DevelopmentOverviewPanel.vue`：`entStatsOverviewIndustryKpi({ chain_code: scopeChainCode.value })` —— HTTP body 键 = `chain_code`（snake）。

### 2. backend（透传方）
`EnterpriseMetaRequest.java`：`@JsonProperty("chain_code") private String chainCode;` `@JsonProperty("chain_codes") private List<String> chainCodes;`
`EnterpriseDistributionRequest.java`：`@JsonProperty("chain_code") private String chainCode;`
- 反序列化：前端 `chain_code` → 字段 chainCode ✓（@JsonProperty 双向）
- 序列化（Feign 转发 Python）：chainCode → `chain_code` ✓（同名注解）
- Controller/ServiceImpl 为 `@RequestBody DTO` 整体转发，无手工映射，无丢失路径。

### 3. topic_py（接收方）
`enterprise_overview.py` `_chain_codes_from(body)`：读 `body["chain_codes"]` / `body["chain_code"]` ✓
`enterprise_distribution.py`：读 `body.get("chain_code")` ✓

## 结论
三仓对 `chain_code` / `chain_codes` 的字段名完全一致（snake_case 全链路）；无大小写/命名策略分歧。契约级集成 PASS（SIMULATED：非运行时调用）。运行时验证待 dev 部署（EV-INT-DEV-PENDING 步骤）。
