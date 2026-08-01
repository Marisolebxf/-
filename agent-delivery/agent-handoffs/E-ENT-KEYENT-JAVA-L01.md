# Handoff — E-ENT-KEYENT-JAVA-L01

> **status**: review  
> **claimed_by**: agent:java-agent  
> **supervised_by**: human:侯佳伟  
> **agent**: java-agent  
> **completed_at**: 2026-08-01T18:06:00+08:00  
> **repo**: lumen-svc-platform / `gkxlumen-topic-enterprise`  
> **design**: `重点企业分析-功能设计.md` v2.3；`深圳企业现状分析-功能设计.md` v1.3  
> **方案**: `repos/lumen-svc-platform/E-ENT-KEYENT-JAVA-L01-实施方案.md`

---

## 1. 范围与实现

| DoD | 证据 |
|-----|------|
| `GkxSearchKeyAnalysisFeignClient`（10） | `…/feign/GkxSearchKeyAnalysisFeignClient.java` |
| `GkxSearchSzStatusFeignClient`（5） | `…/feign/GkxSearchSzStatusFeignClient.java` |
| 全部 DTO（snake_case，对齐 Python） | `api/dto/keyanalysis/*`、`api/dto/szstatus/*` |
| 门面 Controller + Service（子目录 + 行级中文注释） | `controller/keyanalysis|szstatus`、`service/keyanalysis|szstatus` |
| 对比篮不新增 | 领域 Tab `org_ids` 复用 `#91 GET /compare-basket` |
| `mvn compile` 绿 | `mvn -pl gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz -am compile -DskipTests` |
| 总接口文档 | `API-ENT-full-catalog.md` #122–#136（每端点独立入参/出参表+示例） |
| 推 `origin/dev` | 见下方 commits |

### 对外路径

- 网关：`POST /enterprise/topic/v1/key-analysis/**`（10）、`/enterprise/topic/v1/sz-status/**`（5）
- 服务内：`/topic/v1/key-analysis/**`、`/topic/v1/sz-status/**`
- Python：`/internal/gkx-search/key-analysis/**`、`/sz-status/**`（与企业搜索同一 Python 服务，复用 `EnterprisePythonFeignConfig`）

### 边界（勿混用）

- ≠ `#66–70` `/key-enterprise/**` 全景  
- ≠ `#73–76` `/shenzhen/**` 概况  

---

## 2. 偏离

- 无业务偏离。相对派单「仅 Feign+DTO」，按监管人方案补齐了 Controller/Service 门面以便前端联调（与企业其他门面一致）。
- `domain-evidence` / 部分深圳对标仍依赖 Python Mock/ADS，Java 仅透传。

---

## 3. 产物清单

| 仓 | 产物 |
|----|------|
| `lumen-svc-platform` | Feign×2、DTO 子目录、Controller/Service 子目录、实施方案 |
| `gkx-orchestration` | `API-ENT-full-catalog.md` #122–#136；registry → review；本 handoff |

---

## 4. 验收证据

```bash
cd repos/lumen-svc-platform
mvn -pl gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz -am compile -DskipTests
# EXIT 0

# 路径对齐自检：Feign 15 = Python 15 = Controller 15
```

链路：前端 → Gateway `/enterprise/**` → `gkxlumen-topic-enterprise-biz` → Feign → `gkx_search_service`。

---

## 5. 架构合规自检

1. 算法只在 Python ✅（Java 透传）  
2. 前端 → Java REST → Python `/internal/*` ✅  
3. 未引入 Neo4j ✅  
4. Feign 复用企业搜索寻址 ✅  
5. 推 `origin/dev` ✅  
6. demo2 未 merge lumen ✅  
7. 对比篮复用、无越层 ✅  

---

## 6. Cost 回填

| 字段 | 值 |
|------|-----|
| `actual_tokens` | 95000 |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | 2.80 |
| `cost_warn` | green |

---

## 7. 开放项

- 前端 `E-ENT-KEYENT-UI-L01`：对接 `#122–#136`；领域 Tab 将对比篮 `enterprise_code` 填入 `org_ids`
- 联调依赖 Python KEYENT/SZSTATUS 已部署版本（缺路由则 Feign 404）
- ES `peer_regions[].region_id` 空串时前端先用 `region_name`（PY handoff 已说明）
