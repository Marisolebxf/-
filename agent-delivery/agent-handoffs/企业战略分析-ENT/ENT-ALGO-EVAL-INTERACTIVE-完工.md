# ENT-ALGO-EVAL-INTERACTIVE — entan 交互式评估接口 完工

> **任务**：ENT-ALGO-EVAL-INTERACTIVE
> **执行人**：algorithm-agent（唐绍祖）
> **日期**：2026-07-22
> **状态**：✅ 完工

---

## 1. 产出物

| 文件 | 路径 | 说明 |
|------|------|------|
| `entan_evaluation_routes.py` | `api/entan_evaluation_routes.py` | 新增交互式评估接口 + 轻量预检接口 |
| `main.py`（修改） | `api/main.py` | 注册 entan_evaluation_router |
| task-registry.yaml | agent-delivery/ | 状态 done |

---

## 2. 新增接口

### 2.1 `POST /v1/evaluation/compute` — 交互式评估计算

### `POST /v1/evaluation/compute`

**入参**（JSON body）：

```json
{
  "enterprise_codes": ["6bc50eca3435d4b53fb7bf661d058a47"],
  "mode": "competitiveness",
  "weights": {"innovation": 0.3, "operation": 0.3, "growth": 0.2, "risk": 0.2},
  "template_id": "TPL-INNOVATION"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| enterprise_codes | string[] | 是 | 企业 org_id 列表，1-50 |
| mode | string | 是 | technology / business / competitiveness |
| weights | object | 否 | 自定义权重，缺省用 mode 默认 |
| template_id | string | 否 | 透传 |

**出参**：

```json
{
  "code": 0,
  "data": {
    "scores": [{
      "enterprise_code": "6bc50eca...",
      "enterprise_name": "示例科技",
      "total_score": 73.91,
      "rank": 1,
      "dimensions": {"innovation": 73.27, "operation": 54.93, "growth": 86.15, "risk": 81.29},
      "weights": {"innovation": 0.25, "operation": 0.25, "growth": 0.25, "risk": 0.25},
      "confidence": "high",
      "data_source": "entan",
      "model_version": "entan-v1.0"
    }],
    "diagnosis": [{
      "enterprise_code": "6bc50eca...",
      "enterprise_name": "示例科技",
      "diag_level": "healthy",
      "advantages": [{"dim": "innov", "name": "创新能力", "score": 73.27}],
      "weaknesses": [{"dim": "operate", "name": "经营能力", "score": 54.93}]
    }],
    "radar": [{
      "enterprise_code": "6bc50eca...",
      "enterprise_name": "示例科技",
      "dimensions": {"innovation": 73.27, "operation": 54.93, "growth": 86.15, "risk": 81.29},
      "total_score": 73.91
    }],
    "model_version": "entan-eval-interactive-v0.1",
    "data_source": "entan",
    "calc_process_template": {
      "metric_ids": ["M_ENT_COMPETITIVENESS_SCORE", "M_ENT_INNOVATION_INDEX", "M_ENT_COMPETITIVENESS_RANK"],
      "formula": "total_score = Σ(weight_dim × score_dim) ...",
      "source_tables": ["ads.enterprise_diagnosis", "ads.enterprise_score", "ads.realdata_enterprise_risk", "dwd.enterprise"],
      "model_version": "entan-eval-interactive-v0.1"
    }
  }
}
```

---

## 3. 三模式默认权重

| mode | innovation | operation | growth | risk |
|------|-----------|-----------|--------|------|
| technology | 0.50 | 0.20 | 0.20 | 0.10 |
| business | 0.20 | 0.50 | 0.20 | 0.10 |
| competitiveness | 0.25 | 0.25 | 0.25 | 0.25 |

---

## 4. 可信度（confidence）计算规则

| 等级 | 条件 | 含义 |
|------|------|------|
| high | 4 个维度（innovation/operation/growth/risk）全部有数据 | 数据覆盖充分 |
| medium | 3 个维度有数据 | 部分数据缺失 |
| low | ≤2 个维度有数据 | 数据严重不足 |

缺失维度按 0 分参与加权汇总。

---

## 5. 新增：`GET /v1/evaluation/precheck` — 数据覆盖预检（对比篮用）

**用途**：替代前端 `buildEnterpriseQuality` 模拟数据，供对比篮/评估配置页即时展示可信度。

### 调用方式

```
GET /v1/evaluation/precheck?enterprise_codes=6bc50eca...,6eeabc49...&mode=competitiveness
```

### 返回（与前端 EnterpriseQuality 对齐）

```json
{
  "code": 0,
  "data": {
    "qualities": [{
      "enterpriseId": "6bc50eca...",
      "enterprise_name": "示例科技",
      "coverage": 88,
      "confidence": "high",
      "missingMetricIds": ["M_ENT_SUPPLY_CHAIN_RISK"],
      "hasKeyMissing": false,
      "data_source": "entan",
      "detail": {
        "basic": {"enterprise_name": true, "industry_category": true, ...},
        "eval": {"has_score": true, "has_risk": false, ...}
      }
    }]
  }
}
```

### 可信度阈值（与前端 `classifyConfidence` 一致）

| coverage | hasKeyMissing | confidence |
|----------|--------------|------------|
| ≥90% | false | high |
| ≥90% | true | medium |
| 70-89% | — | medium |
| 50-69% | — | low |
| <50% | — | blocked |

### 徐滕强对接方式

前端 `EnterpriseEvaluationPage.tsx` 第 179 行：

```typescript
// 改为：
const qualities = await fetch(`/entan/v1/evaluation/precheck?enterprise_codes=${codes}&mode=${mode}`)
  .then(r => r.json()).then(d => d.data.qualities);
```

### 维度映射

| 维度 | entan 数据源 | 字段 |
|------|-------------|------|
|------|-------------|------|
| innovation | ads.enterprise_score | score_innov |
| operation | ads.enterprise_score | score_operate |
| growth | ads.enterprise_score | score_growth |
| risk | ads.realdata_enterprise_risk | risk_score（反向归一） |

---

## 6. 架构合规自检

| # | 铁律 | 结果 | 说明 |
|---|------|------|------|
| 1 | 算法只在 Python | ✅ | entan 纯 Python |
| 2 | 调用链前端→Java→gkx_ai_service→entan | ✅ | Java 不直连，经 gkx_ai_service 屏蔽 |
| 3 | 图谱 NebulaGraph | N/A | 不涉图 |
| 4 | 可观测性 | ✅ | 沿用 entan 日志体系 |
| 5 | CI/CD | ✅ | demo-algo-ent-analysis main 直推 |
| 6 | demo2 不 merge lumen | ✅ | 算法 demo 仓 |
| 7 | 共享聚合核心 | ✅ | 经 gkx_ai_service 屏蔽层 |
| 8 | 数据走 ADS | ✅ | 读 ads.enterprise_score 等 |
| 9 | D8 前端规范 | N/A | 不涉前端 |
| 10 | D9 数据血缘 | ✅ | calc_process 含 metric_id/formula/source_tables |
| 11 | 不改现有 5 个 GET 接口 | ✅ | 独立文件，未修改 entan_analysis_routes.py |
| 12 | 权重不写死 settings.yaml | ✅ | 从请求体读 |

---

## 7. Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 150_000 |
| actual_tokens | 95_000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.55 |
| cost_warn | green |

---

## 9. 需 gkx_ai_service 配合事项

1. **`POST compute`**：`entan_client.py` 中 POST URL 改为 `{entan_base_url}/v1/evaluation/compute`
2. **`GET precheck`**：对比篮预检可直接调 `{entan_base_url}/v1/evaluation/precheck`，替代前端模拟数据
3. 响应字段名已对齐（scores[].confidence, dimensions 四个键名, qualities[] 与 EnterpriseQuality 一致）
4. 联调时 `GKX_MOCK_ENABLED=false` 即可切真实 entan
