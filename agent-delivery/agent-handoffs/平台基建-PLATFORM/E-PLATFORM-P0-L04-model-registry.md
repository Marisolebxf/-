# Algorithm handoff · E-PLATFORM-P0-L04 模型注册中心

| 项 | 值 |
|---|---|
| 任务 | E-PLATFORM-P0-L04 |
| Epic | E-PLATFORM-P0 |
| 角色 | algorithm-agent |
| 仓 | `F:/gkx-lumen/repos/demo-algo-ent-analysis` |
| 分支 | `feat/E-PLATFORM-P0-L04` |
| 基线 | `feat/E-PLATFORM-P0-L03` @ `6b4428e` |
| 日期 | 2026-06-20 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 产物 |
|--------|------|------|
| cfg_model_registry 表/配置 | ✅ | `scripts/schema_cfg.sql` + `conf/cfg_model_registry.yaml` |
| GET `/internal/models/registry` | ✅ | `api/main.py` + `entan/models/registry.py` |
| ≥1 条 E7 政策占位模型 | ✅ | 3 条 E7 placeholder（焦点/力度/效果）+ 2 条 ENT active 对照 |
| 文档 L3 深度模型对接 | ✅ | `docs/model-registry-l3-integration.md` |
| 不破坏 P0-L03 `/internal/graph/subgraph` | ✅ | 图谱代码未改，仅在其前追加 models 路由 |
| push → py:smoke 绿 | 🟡 | 本地 import 通过；待 push 后 GitLab CI 确认 |

## 产物清单

| 路径 | 说明 |
|------|------|
| `conf/cfg_model_registry.yaml` | Git 真源；5 models（3×E7 placeholder + 2×ENT active） |
| `scripts/schema_cfg.sql` | `gkx_cfg.cfg_model_registry` DDL（PG jsonb 扩展字段） |
| `entan/models/registry.py` | 加载/查询/seed；PG 优先、YAML 兜底 |
| `entan/common/db.py` | `cfg_schema` + DDL 纳入 `init_schema()` |
| `api/main.py` | GET registry / GET by id / POST seed |
| `docs/model-registry-l3-integration.md` | L3 对接时序、版本灰度、E7 handler 路线图 |
| `.gitlab-ci.yml` | `py:smoke` 增 `entan.models.registry`；L04 分支可 package/deploy |

## 内部 API 契约

### GET `/internal/models/registry`

查询：`element`（E7/ENT）、`status`（active/placeholder）

```json
{
  "registry_version": "0.1.0",
  "count": 3,
  "source": "yaml",
  "filters": {"element": "E7", "status": null},
  "models": [{ "model_id": "E7_POLICY_FOCUS", "element": "E7", ... }]
}
```

### GET `/internal/models/registry/{model_id}`

### POST `/internal/models/registry/seed?force=false`

YAML → PG 幂等同步。

## E7 占位模型

| model_id | metric_ids | status |
|----------|------------|--------|
| E7_POLICY_FOCUS | M_POLICY_FOCUS_INDEX | placeholder |
| E7_POLICY_INTENSITY | M_POLICY_INTENSITY_INDEX | placeholder |
| E7_POLICY_EFFECT | M_POLICY_EFFECT_INDEX | placeholder |

Wave 1 实现：`E-E7-POLICY-M1-L03` → `POST /internal/analysis/policy/{modelId}`

## 架构合规自检（§2 十条）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 算法只在 Python | ✅ registry 为元数据层 |
| 2 | 调用链 | ✅ `/internal/*` 供 Java Feign |
| 4 | 可观测性 | ✅ 沿用 P0-L03 OTel middleware |
| 8 | D7 Mock | ✅ E7 ext.is_mock=true |
| 10 | D9 血缘 | ✅ metric_ids + evaluation 元数据 |

## Convoy 隔离

- **ENT-PY-ALGO**：本任务为 convoy 第二步；未修改 `entan/graph/*`、`/internal/graph/subgraph`
- 与 P0-L03 同仓串行，无 merge 冲突点

## 阻塞项

| 项 | 说明 | Owner |
|----|------|-------|
| CI py:smoke | 待 `feat/E-PLATFORM-P0-L04` push 后 GitLab runner 确认 | coordinator |
| PG seed 验收 | agent 环境 PG 外网可达性不定；API 默认 YAML 兜底 | qa / devops |
| E7 推理 handler | Wave 0 仅注册；实现阻塞于 E-E7-POLICY-M1-L03 | algorithm-agent |

## 接力清单

| 下游 | 动作 |
|------|------|
| **api-agent P0-L05** | gkxlumen-topic Feign 调 `/internal/models/registry` + health |
| **algorithm-agent E-E7-POLICY-M1-L03** | 实现 3 个 policy analysis handler + POST 推理 |
| **qa-agent** | dev 验证 registry 与 subgraph 并存 |

## cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 400_000 |
| actual_tokens | （session 回填） |
| model_used | claude-sonnet-4.5 |
| actual_cost | （session 回填） |
| cost_warn | green |

## git

- 分支：`feat/E-PLATFORM-P0-L04`
- commit：`[agent:algorithm-agent] E-PLATFORM-P0-L04`

---

*handoff · algorithm-agent · E-PLATFORM-P0-L04*
