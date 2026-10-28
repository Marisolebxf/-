# ENT-KEY-PANO-BACKEND-L01 · E-33 重点企业全景 · 按链 scoped 接口契约与实现（#66/#67/#69）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 契约 DTO + Python 读数 + seed 增量；未新加依赖；#66/#69 scoped、#67 domain_evidence、#69 scale_items；legacy 无 chain_code 路径保留 |

## 任务背景与目标

在 `PORTAL-ENT-DEV-SRS-API-L01` 联调态门面上，闭合 E-33（需规 76）：页内统计统一 `chain_code`；#69 返回资质四类 × 国省市 `scale_items[]`；#67 返回 `domain_evidence[]`；#66 带 `chain_code` 时 `key_enterprise_total` 与链内重点企业同口径。

真源：`PORTAL-ENT-DEV-API-REQUIREMENTS.md` §2、`PORTAL-ENT-DEV-SRS-API-L01.md`。

## 范围与实现（DoD 对照）

| DoD 条目 | 状态 | 证据 |
|----------|------|------|
| `EnterpriseKeyChainScopeRequest` + #66/#69 入参 scoped | ✅ | Java `EnterpriseKeyChainScopeRequest.java`；Controller/Feign 已切换 |
| #69 `scale_items[]` 四资质 × 国省市 | ✅ 代码 | Python `_build_scale_items`；Java `KeyQualificationSummaryResponse.scaleItems` |
| #67 `domain_evidence[]` | ✅ | Python `_load_domain_evidence`；Java `KeyChainListResponse.domainEvidence`；dev `INB1309` 返回 12 条 |
| #66 链内 `key_enterprise_total` | ✅ | dev scoped KPI `27705`（与同链 chain-subject 一致） |
| legacy 无 `chain_code` 不破坏 | ✅ | `#69 {}` → `items=6`、`scale_items=0`；`code=0` |
| seed / `stat_value` | ✅ | `db/9y_portal_ent_dev_seed.sql` |
| CI + deploy + 网关三接口同链 | ⚠️ | 双仓已 push dev；**dev 上 scoped `#69` 曾 HTTP 500**（见测试结果）；需确认 search-py 已 rollout `92e1b41` 后复测 |
| handoff + 架构自检 + cost | ✅ | 本节 |

## 修改内容

### Java（lumen-svc-platform · `0a56108`）

| 项 | 说明 |
|----|------|
| `EnterpriseKeyChainScopeRequest` | `chain_code` + 可选 `region_id`（深圳默认 440300 由 Python 兜底） |
| `#66` / `#69` 门面 | 入参改为 `EnterpriseKeyChainScopeRequest`（Controller / Service / Feign） |
| `EnterpriseExtendedDTOs` | `KeyQualificationScaleItem`、`KeyDomainEvidenceItem`；`domainEvidence` / `scaleItems` |

### Python（lumen-topic-py · `cc4cbe7` + `92e1b41`）

| 接口 | 行为 |
|------|------|
| `POST .../kpi` | 有 `chain_code`：链内重点企业总数（`key_enterprise_chain` / DISTINCT） |
| `POST .../qualification-summary` | 有 `chain_code`：`scale_items` 四行，`items=[]`；无 `chain_code`：legacy `items` |
| `POST .../chain-list` | `domain_evidence[]`（链内环节 DWD 聚合） |
| `92e1b41` | DWD 列校准：`enterprise_type` / `enterprise_name`、深圳区划谓词（gkxlumenx 真源） |

### 灌数（`db/9y_portal_ent_dev_seed.sql`）

- `enterprise_stat_summary` 使用 `stat_value`；新增 `key_qual_scale` 按链预聚合（可选加速）。

## 契约 JSON 样例（scoped，`chain_code=INB1309`）

**请求（#66 / #69 共用）**

```json
{ "chain_code": "INB1309", "region_id": "440300" }
```

**#66 响应（dev 实测 2026-10-28）**

```json
{
  "key_enterprise_total": 27705,
  "high_tech_total": "<ES 实值>",
  "covered_chain_nodes": 22,
  "covered_districts": 1
}
```

**#69 响应（结构；数值以 deploy 后实包为准）**

```json
{
  "items": [],
  "scale_items": [
    {
      "qualification": "foreign",
      "qualification_label": "外企",
      "levels": { "national": 0, "province": 0, "city": 0 }
    },
    {
      "qualification": "high_tech",
      "qualification_label": "高新技术企业",
      "levels": { "national": 0, "province": 0, "city": 0 }
    },
    {
      "qualification": "sme",
      "qualification_label": "小微企业",
      "levels": { "national": 0, "province": 0, "city": 0 }
    },
    {
      "qualification": "listed",
      "qualification_label": "上市企业",
      "levels": { "national": 0, "province": 0, "city": 0 }
    }
  ]
}
```

**#67 `domain_evidence`（dev 实测条数 12，字段结构）**

```json
{
  "domain": "…",
  "stage": "上游|中游|下游",
  "paper_keywords": ["…"],
  "patent_keywords": ["…"],
  "coverage": 82,
  "evidence_status": "证据充分|证据不足",
  "summary": "…",
  "enterprises": [{ "org_id": "…", "name_cn": "…" }]
}
```

## 偏离说明

| 项 | 说明 |
|----|------|
| `domain_evidence` 关键词 | 链内环节聚合 + 模板关键词（D4 灌数语义）；非语料实算 |
| 前端 E-33 | `ENT-KEY-PANO-FRONTEND-L01` 负责同链 `#66/#69/#67` wire；本单后端契约已就绪 |
| Author 历史 commit | `cc4cbe7` Author 误为上一机器配置；后续 `92e1b41` 已为 `kongdong` |

## 测试结果

**网关**：`http://10.50.69.111:30892/api/enterprise/topic/v1/key-enterprise`（`USE_MOCK=false` 环境）

| 调用 | body | 结果（2026-10-28 傍晚） |
|------|------|------------------------|
| `#66` kpi | `{"chain_code":"INB1309"}` | ✅ `code=0`，`key_enterprise_total=27705` |
| `#67` chain-list | `{"chain_code":"INB1309","page":1,"page_size":3}` | ✅ `code=0`，`domain_evidence` 长度 **12** |
| `#69` qual（legacy） | `{}` | ✅ `code=0`，`items=6`，`scale_items` 空 |
| `#69` qual（scoped） | `{"chain_code":"INB1309"}` | ⚠️ **HTTP 500**（线上 search-py 镜像/ DWD 列需与 `92e1b41` 对齐后复测） |
| `#68` chain-subject-stats | `{}` | ✅ `code=0`（回归） |
| `#70` type-scale-stats | `{"region_level":"city"}` | ✅ `code=0`（回归） |

**复测命令（PowerShell）**

```powershell
$base = "http://10.50.69.111:30892/api/enterprise/topic/v1/key-enterprise"
$h = @{ "Content-Type" = "application/json" }
$b = '{"chain_code":"INB1309"}'
Invoke-RestMethod -Uri "$base/kpi" -Method Post -Headers $h -Body $b
Invoke-RestMethod -Uri "$base/qualification-summary" -Method Post -Headers $h -Body $b
Invoke-RestMethod -Uri "$base/chain-list" -Method Post -Headers $h -Body '{"chain_code":"INB1309","page":1,"page_size":3}'
```

签收前建议：确认 GitLab **deploy:search-py** 已含 `92e1b41`，scoped `#69` 返回 `scale_items.Count -eq 4` 且 `code=0`。

## CI/CD

| 项 | 值 |
|----|-----|
| 分支 | `origin/dev`（lumen-svc-platform、lumen-topic-py） |
| commit | svc-platform **`0a56108`**；topic-py **`cc4cbe7`**（E-33 主实现）、**`92e1b41`**（DWD 列校准，`human:kongdong`） |
| pipeline | 以 GitLab 双仓最新 pipeline 为准（push 后 `backend:build` + `py:smoke`） |
| 部署 | 手动 `deploy:topic-enterprise` + `deploy:search-py`（ns 同 PORTAL 单） |
| dev URL | 见上表 |

## 架构合规自检

| 铁律 | 结论 |
|------|------|
| 1 算法只在 Python | ✅ |
| 2 调用链 前端→Java→Python | ✅ |
| 5 CI/CD | ✅ push dev；deploy 由运维/监管手动触发 |
| 8 汇总表先行 | ✅ seed + 在线 SQL 补算 |
| 12 demo/lumen 隔离 | ✅ |
| D9 | ✅ 未改 8 件套口径 |

## 遗留风险 / 移交

1. **scoped `#69` dev 500**：签收前务必 rollout `92e1b41` 并复测；若仍 500，查 DWD `enterprise_base` 列（`enterprise_type` / `is_little_giant` 等）与 Python 谓词。
2. 数据侧：正式 ETL 接管 `key_qual_scale` / `key_enterprise_chain` 灌数。
3. 前端：`ENT-KEY-PANO-FRONTEND-L01` 传 `chain_code` 联调规模图。
4. `domain_evidence` 待语料链替换模板关键词。

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../EnterpriseKeyChainScopeRequest.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../EnterpriseExtendedDTOs.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../EnterpriseKeyEnterpriseController.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../EnterpriseKeyEnterpriseService*.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../RemoteEnterprisePythonClient.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../RemoteTopicEnterpriseService.java`
- `repos/lumen-svc-platform/db/9y_portal_ent_dev_seed.sql`
- `repos/lumen-topic-py/gkx_search_service/views/enterprise_key_enterprise.py`

## 任务关闭

| 项 | 值 |
|----|-----|
| 开发结论 | 后端契约与实现已合 **dev**；#66/#67 scoped 网关已验；#69 scoped 待 search-py 镜像与 DWD 对齐复测 |
| 建议状态 | **`ready_to_sign`**（待监管人/淮政玮签收；`tech_task` 无 mandatory QA 闸门） |
| 联调确认 | 后端实现完成，前端 wire 由 `ENT-KEY-PANO-FRONTEND-L01` 跟进；本单不阻塞前端任务依赖的后端 commit |

## Cost（按 budget-estimate.md 四字段）

| actual_tokens | model_used | actual_cost | cost_warn |
|---------------|------------|-------------|-----------|
| 120000 | composer | ~$1.0 | false |
