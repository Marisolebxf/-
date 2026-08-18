# DEMO-SVC-PY-SVCAN-MODELS-L01 · svcan 八叶子读 Demo ADS

> 日期：2026-08-18  
> Task：`DEMO-SVC-PY-SVCAN-MODELS-L01`  
> 总控：`DEMO-SVC-FULL-底座后全量-长任务总控.md` / `DEMO-SVC-GATE1-全量派单.md`（已授权 · human:侯佳伟）  
> 上游：`LUMEN-SVC-JAVA-JOB-WHITELIST-L01`（`ac5df68` · integration）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 CHAIN `demo_guard` 只读 Demo ADS；八叶子 handler + 最小单测；不新依赖、不写正式库、不伪闭合 Q-SVC-010 |

## 范围与实现

仓：`repos/lumen-algo-py`

| leaf | analysis_key | ADS 真源 | 说明 |
|------|--------------|----------|------|
| `org_coverage` | `svcan.org_coverage.v0` | `svc_org_profile_card` GROUP BY type | 机构类型覆盖 |
| `org_trend` | `svcan.org_trend.v0` | `svc_metric_series` `M_SVC_PT_GLOBAL_TREND` | 新增趋势 |
| `tech_power` | `svcan.tech_power.v0` | `svc_tech_power_score` ⋈ profile | 可解释分/模型 |
| `shortboard` | `svcan.shortboard.v0` | `svc_chain_gap_score` | 环节短板（替换 BOOT 硬 mock） |
| `graph` | `svcan.graph.v0` | — | 诚实空（无图谱快照灌数表） |
| `shenzhen` | `svcan.shenzhen.v0` | profile(深圳) + region_dist + fact | 深圳生态 |
| `attract` | `svcan.attract.v0` | `svc_rec_ranking` ATTRACT | 招引 |
| `cultivate` | `svcan.cultivate.v0` | `svc_rec_ranking` CULTIVATE | 培育 |

路由：

- `GET /internal/v1/svcan/health` — 列出 8 leaves + keys  
- `POST /internal/v1/svcan/analyze` — `{analysis_key, params}` 统一入口  
- `POST /internal/v1/svcan/sample/{leaf}` — 含兼容 `…/sample/shortboard`

诚实性：一律 `mock: true` + `gap: [Q-SVC-010]` + `verification_status: pending_client_confirm`；拒非 `demo_` ADS。

### 样例响应形（tech_power）

```json
{
  "key": "svcan.tech_power.v0",
  "leaf": "tech_power",
  "status": "demo_ready",
  "items": [
    {
      "rank_no": 1,
      "service_org_code": "…",
      "name_cn": "…",
      "score": 88.0,
      "model_id": "…",
      "model_version": "…",
      "explain": "技术力分=88.0（模型 …）；Q060 临时等权",
      "verification_status": "pending_client_confirm"
    }
  ],
  "mock": true,
  "gap": ["Q-SVC-010"],
  "data_source": "demo_ads"
}
```

空表时：`status`/`data_source` 为 `empty`，`items: []`，仍带 mock+gap。

## 偏离说明

- `graph`：DDL 无图谱快照灌数 → 诚实空壳（nodes/edges=[]），不伪造。  
- **topic-py 仍硬编码** `POST …/sample/shortboard`（不传 `analysis_key`）→ Job 链路上目前只有 shortboard 会命中 ADS 新实现；其余 7 叶需中间层改调 `/analyze`（见开放项，**不认领 FE**）。

## 产物清单

| 产物 | 路径 |
|------|------|
| handlers | `lumen_common/algorithms/svcan/handlers.py` |
| routes | `lumen_algo_service/views/svcan.py` |
| tests | `tests/test_svcan_boot.py`（6 passed） |
| 本 handoff | `agent-handoffs/服务机构-SVC/DEMO-SVC-PY-SVCAN-MODELS-L01.md` |

## 验收证据

- [x] 八叶子 handler + key 映射齐  
- [x] 短板/技术力读契约 ADS（空则诚实空）  
- [x] `pending_client_confirm` / mock / gap  
- [x] `py -3 -m pytest tests/test_svcan_boot.py` → **6 passed**  
- [x] commit + push `origin/dev`  
- [ ] CI 绿（待 pipeline）  
- [ ] 外网 Job 八叶子（待 topic-py 路由 + FE）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ |
| 2 | FE→Java→Python `/internal/*`；Java 不写算法 | ✅ |
| 6 | 仅 demo_ MySQL | ✅ `assert_demo_mysql_targets` |
| D9/Q-SVC-010 | 不伪闭合 | ✅ |
| D12 | 不 Feign demo-* | ✅（本仓 algo） |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~5.5 万 |
| actual_cost | 估 <$3 |
| cost_warn | false |

## CI/CD

- 分支：`dev`
- commit：`10ece369308f215f4e55c56b3d6787a5ca272a4a`
- pipeline：push 后 GitLab CI（algo api+worker）
- 部署：随 lumen-algo-py K8s dev

## 开放项 / 下游 backlog（不认领）

1. **lumen-topic-py** `gkx_svc_service/views/task.py`：按 `analysis_key` 调 `/internal/v1/svcan/analyze`（勿再写死 shortboard）— 建议新建中间层叶，**非 FE**。  
2. **`LUMEN-SVC-FE-ANALYSIS-FULL-L01`**：分析/生态/招引 FE 接线 — **不认领**，留给 frontend-agent。

## 联调确认

联调通过（algo 侧）：八叶子 `/sample/{leaf}` 与 `/analyze` 可返回 ADS 或诚实空包络；未知 key 422。下一闸：topic-py 路由 + FE 有数页。
