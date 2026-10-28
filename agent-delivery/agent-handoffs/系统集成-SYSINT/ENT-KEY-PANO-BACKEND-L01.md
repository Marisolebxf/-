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

## 修改内容

### Java（lumen-svc-platform · gkxlumen-topic-enterprise）

| 项 | 说明 |
|----|------|
| `EnterpriseKeyChainScopeRequest` | 新增：`chain_code` + 可选 `region_id`（深圳默认 440300 由 Python 侧兜底） |
| `#66` / `#69` 门面 | 入参由 `EnterpriseStatsRegionRequest` 改为 `EnterpriseKeyChainScopeRequest`（Controller / Service / Feign 全链） |
| `EnterpriseExtendedDTOs` | `KeyQualificationScaleItem`、`KeyDomainEvidenceItem`；`KeyChainListResponse.domainEvidence`；`KeyQualificationSummaryResponse.scaleItems` |

### Python（lumen-topic-py）

| 接口 | 行为 |
|------|------|
| `POST .../kpi` | 有 `chain_code`：`key_enterprise_total` ← `key_enterprise_chain` 汇总 / 链上 DISTINCT；高企仍 ES nested 计数 |
| `POST .../qualification-summary` | 有 `chain_code`：`scale_items` 四行（foreign/high_tech/sme/listed × national/province/city），`items=[]`；无 `chain_code`：legacy `qualification_count` 扁平 `items`，`scale_items=[]` |
| `POST .../chain-list` | 响应增加 `domain_evidence[]`（链内环节 DWD 聚合 + 样例企业；关键词为汇总 seed 文案） |
| `chain-subject-stats` | 计数列统一读 `stat_value` |

模块内 `python enterprise_key_enterprise.py` 自检 `scale_items` 结构（四资质 × 三国省市）。

### 灌数（`db/9y_portal_ent_dev_seed.sql`）

- `enterprise_stat_summary` 写入列改为 `stat_value`（对齐 ORM / Python）。
- 新增 `key_qual_scale`（按链 `high_tech:national` / `high_tech:city` 预聚合；其余层级 Python 可在线补算）。

## 契约 JSON 样例（scoped，`chain_code=INB1309`）

**#66 kpi**

```json
{
  "chain_code": "INB1309",
  "region_id": "440300"
}
```

```json
{
  "key_enterprise_total": 27705,
  "high_tech_total": 12345,
  "covered_chain_nodes": 22,
  "covered_districts": 1
}
```

（`high_tech_total` / 节点区数为环境实值；`key_enterprise_total` 应与 `chain-subject-stats` 同链 `key_enterprise_count` 一致。）

**#69 qualification-summary**

```json
{
  "items": [],
  "scale_items": [
    {
      "qualification": "foreign",
      "qualification_label": "外企",
      "levels": { "national": 120, "province": 80, "city": 45 }
    },
    {
      "qualification": "high_tech",
      "qualification_label": "高新技术企业",
      "levels": { "national": 5000, "province": 4800, "city": 3200 }
    },
    {
      "qualification": "sme",
      "qualification_label": "小微企业",
      "levels": { "national": 8000, "province": 7500, "city": 6000 }
    },
    {
      "qualification": "listed",
      "qualification_label": "上市企业",
      "levels": { "national": 200, "province": 180, "city": 120 }
    }
  ]
}
```

（数字为结构示例；以 deploy 后 dev 实包为准。）

**#67 chain-list（片段）**

```json
{
  "chain_code": "INB1309",
  "chain_name": "人工智能",
  "groups": [ "..." ],
  "domain_evidence": [
    {
      "domain": "基础层",
      "stage": "上游",
      "paper_keywords": ["基础层机理", "基础层方法", "上游技术"],
      "patent_keywords": ["基础层装置", "基础层系统", "上游工艺"],
      "coverage": 82,
      "evidence_status": "证据充分",
      "summary": "基于链内重点企业分布与公开技术语料，将证据关联至上游环节「基础层」。",
      "enterprises": [{ "org_id": "ORG001", "name_cn": "示例企业" }]
    }
  ]
}
```

## 偏离说明

| 项 | 说明 |
|----|------|
| `domain_evidence` 关键词 | 算法/语料链未闭合；当前为链内环节聚合 + 模板关键词（D4 灌数/mock 语义）；非 ES 论文专利实算 |
| 前端 `#66/#69` | `KeyEnterprisesPanel.vue` 仍可能不传 `chain_code`；规模图需前端 wire 同链参数（非本单阻塞后端交付） |
| deploy 前 dev 网关 | 2026-10-28 探测：scoped `#69` 尚无 `scale_items`、`chain-list` 无 `domain_evidence`（旧镜像）；**本 handoff 推送后需 CI deploy 再验** |

## 测试结果

| 层 | 结果 |
|----|------|
| 本地 | 本机无 Python/Maven；依赖 CI |
| deploy 前 dev 冒烟 | `POST .../key-enterprise/{kpi,qualification-summary,chain-list,chain-subject-stats,type-scale-stats}` 均 `code=0`（旧包兼容路径） |
| deploy 后验收 | 同 `chain_code` curl：`scale_items` 4 行、`domain_evidence` 非空、`key_enterprise_total>0`（见 §6 PORTAL-ENT-DEV-API-REQUIREMENTS） |

PowerShell 冒烟脚本见本单对话「集成冒烟」节（网关 `http://10.50.69.111:30892/api/enterprise/topic/v1/key-enterprise`）。

## CI/CD

- 分支：双仓 `origin/dev`
- commit：svc-platform `0a56108`；topic-py `cc4cbe7`
- pipeline：待 GitLab `backend:build` + `py:smoke` 绿
- 部署：手动 `deploy:topic-enterprise` + `deploy:search-py`（与 PORTAL-ENT-DEV-SRS-API-L01 相同）
- dev URL：`http://10.50.69.111:30892/api/enterprise/topic/v1/key-enterprise/**`

## 架构合规自检

| 铁律 | 结论 |
|------|------|
| 1 算法只在 Python | ✅ 聚合与读数在 topic-py |
| 2 调用链 前端→Java→Python | ✅ Java 仅 DTO/透传 |
| 8 ADS/汇总表先行 | ✅ seed + stat_summary；在线补算为过渡 |
| 12 demo/lumen 隔离 | ✅ 仅 lumen-* |
| D9 | ✅ 未改指标口径；灌数为 D4 填数 |

## 遗留风险 / 移交

1. 重跑 `9y_portal_ent_dev_seed.sql` 后 `key_qual_scale` 与链 KPI 一致性问题由数据侧 ETL 正式化。
2. 前端 E-33 须对 `#66/#69` 传当前产业 `chain_code`。
3. `domain_evidence` 待算法/语料链接入后替换模板关键词与 `evidence_status`。

## 涉及文件

- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../EnterpriseKeyChainScopeRequest.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../EnterpriseExtendedDTOs.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../EnterpriseKeyEnterpriseController.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../EnterpriseKeyEnterpriseService*.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../RemoteEnterprisePythonClient.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/.../RemoteTopicEnterpriseService.java`
- `repos/lumen-svc-platform/db/9y_portal_ent_dev_seed.sql`
- `repos/lumen-topic-py/gkx_search_service/views/enterprise_key_enterprise.py`

## Cost（按 budget-estimate.md 四字段）

| actual_tokens | model_used | actual_cost | cost_warn |
|---------------|------------|-------------|-----------|
| ~95000 | composer | ~$0.8 | false |
