# ALGO-ENT-fullset-system-test —— 企业算法全集 + /entan 对齐 /policy

> 任务：ENT-ALGO-DEMO-L01（Epic: E-ENT-ALGO-DEMO）｜ 监管人：唐绍祖 ｜ 日期：2026-07-14
> 算法仓：`demo-algo-ent-analysis` ｜ UI 仓：`demo-ui-system-test`（dev 分支）
> 镜像范式：`agent-handoffs/政策模块-E7/ALGO-POLICY-fullset.md` + `FE-POLICY-system-test-demo.md`

---

## 1. 缺口矩阵（算法设计说明 × /v1 × /entan Tab × calc_process）

| 算法章 | 模块 | /v1 路由 | /entan Tab | calc_process | mock 灌数 | realdata |
|--------|------|----------|------------|--------------|-----------|----------|
| Ch1 A1 综合评分 | entan.depth / realdata.a1_score | `GET /v1/score` | 综合评分 | ✅ steps/weights/source_tables | ✅ run_all Step D | ✅ run_realdata_ent a1 |
| Ch2 A2 排名 | entan.depth / realdata.a2_ranking | `GET /v1/ranking` | 多维排名 | ✅ | ✅ | ✅ |
| Ch3 A3 诊断 | entan.depth / realdata.a3_diagnosis | `GET /v1/diagnosis` | 诊断找短板 | ✅ | ✅ | ✅ |
| Ch4 A4 中心性 | entan.depth / realdata.a4_centrality | `GET /v1/centrality` | 链主/中心性 | ✅ | ✅ | ✅ |
| Ch13 B1 风险 | entan.depth / realdata.b1_risk | `GET /v1/risk` | 风险评分 | ✅ | ✅ mock 伪随机 | ✅ ODS 风险表 |
| 基础指标 A1-A5 | entan.basic | `/v1/key-enterprises` 等 | 基础指标 | 部分 | ✅ | demo-A* 可选 |
| 重点资讯 | entan.basic | `/v1/news` | 重点资讯 | — | ✅ | demo-A4 |
| 图谱 B1/B2 | entan.graph | `/v1/graph` | 企业图谱 | — | ✅ | — |
| 技术力 C1 | entan.eval.tech_power | `/v1/tech-power/*` | 技术力评估 | advantages/weaknesses | ✅ | — |
| 商业力 C2 | entan.eval.biz_power | `/v1/biz-power/*` | 商业力评估 | 同上 | ✅ | — |

> **命名说明**：设计说明第5章「B1」= 政策匹配（polan）；DoD「风险 B1」= **第13章** `ENT-B1`。

---

## 2. API 全集（企业 /v1 + internal）

### 2.1 深度分析（新增 `api/entan_analysis_routes.py`）

| 端点 | 说明 | metric_ids |
|------|------|------------|
| `GET /v1/score` | 综合评分列表 + level_dist | M_ENT_COMPETITIVENESS_SCORE, M_ENT_INNOVATION_INDEX |
| `GET /v1/ranking?dim=` | 多维排名 + available_dims | M_ENT_COMPETITIVENESS_RANK |
| `GET /v1/diagnosis` | 优势/短板/建议 | M_ENT_SHORTBOARD_COUNT |
| `GET /v1/centrality` | PageRank 中心性/链主 | M_ENT_NODE_CENTRALITY |
| `GET /v1/risk` | 风险加权评分 | M_ENT_SUPPLY_CHAIN_RISK |
| `GET /v1/analysis/metrics` | headline + metric 清单 | 全部深度 metric |

每条 `rows[]` 含 **`calc_process`**：`steps` / `formula` / `weights` / `intermediate` / `source_tables` / `metric_ids` / `model_version` / `d9_spec`。

### 2.2 灌数据（镜像 /policy）

| 端点 | 说明 |
|------|------|
| `POST /internal/run-pipeline` | 异步触发企业全流水线（含 Step D 深度分析） |
| `GET /internal/status` | running + tables 行数（含 enterprise_score 等 5 张新表） |

### 2.3 响应样例（/v1/score 节选）

```json
{
  "code": 0,
  "data": {
    "total": 120,
    "rows": [{
      "enterprise_code": "1",
      "enterprise_name": "示例科技",
      "score_total": 72.5,
      "score_level": "B",
      "metric_ids": ["M_ENT_COMPETITIVENESS_SCORE", "M_ENT_INNOVATION_INDEX"],
      "calc_process": {
        "formula": "S_total = 0.40*S_innov + 0.40*S_operate + 0.20*S_growth",
        "weights": {"innov": 0.4, "operate": 0.4, "growth": 0.2},
        "source_tables": ["ads.enterprise_score", "ads.tech_power", "ads.biz_power", "dwd.enterprise"],
        "steps": [{"name": "域内打分", "intermediate": {"innov": 68, "operate": 75, "growth": 72}}]
      }
    }]
  }
}
```

---

## 3. 流水线变更

`scripts/run_all.py` STEPS 新增：

```
D 深度分析(A1评分/A2排名/A3诊断/A4中心性/B1风险) → entan.depth.pipeline.run
```

`entan/common/db.py` DDL 纳入 `schema_ent_score.sql`。

`scripts/run_realdata_ent.py` 补全 `b1` / `demoa4` 任务。

---

## 4. 模型注册（cfg_model_registry.yaml）

新增 5 个 ENT 深度模型：

- `ENT_SCORE` / `ENT_RANK` / `ENT_DIAGNOSIS` / `ENT_CENTRALITY` / `ENT_RISK`

保留既有 `ENT_TECH_POWER` / `ENT_BIZ_POWER`。

---

## 5. UI /entan（demo-ui-system-test · dev）

### 5.1 Tab 对照（10 Tab，对齐 /policy 完整度）

| # | Tab | 组件 | API |
|---|-----|------|-----|
| 1 | 基础指标 | BasicIndicators.vue | 既有 |
| 2 | **综合评分** | ScoreView.vue | `/v1/score` |
| 3 | **多维排名** | RankingView.vue | `/v1/ranking` |
| 4 | **诊断找短板** | DiagnosisView.vue | `/v1/diagnosis` |
| 5 | **链主/中心性** | CentralityView.vue | `/v1/centrality` |
| 6 | **风险评分** | RiskView.vue | `/v1/risk` |
| 7 | 重点资讯 | NewsView.vue | 既有 |
| 8 | 企业图谱 | GraphView.vue | 既有 |
| 9 | 技术力评估 | TechPower.vue | 既有 |
| 10 | 商业力评估 | BizPower.vue | 既有 |

### 5.2 灌数据 + 计算过程展示

- `index.vue` 右上角「灌数据」→ `POST /entan/internal/run-pipeline` + 轮询 `status`（镜像 policy）
- 各深度 Tab 内嵌 `<CalcProcessPanel :process="row.calc_process" />`
- `entanHelp.ts` 扩写 score/ranking/diagnosis/centrality/risk 五主题（D9 8 件套）

---

## 6. 架构合规自检

| # | 铁律 | 自检 |
|---|------|------|
| 1 | 算法只在 Python | ✅ A1-A4/B1 均在 entan.depth / realdata |
| 2 | 调用链不越层 | ✅ UI → /api → 网关 → Python /v1/** |
| 3 | Nebula 非 Neo4j | ✅ 图谱仍走 Nebula/PG 兜底 |
| 4 | OTel | ✅ 复用 TraceHeaderMiddleware |
| 6 | 不 merge 进 lumen | ✅ 仅 demo 仓 |
| D9 | 血缘 8 件套 | ✅ calc_process.d9_spec + entanHelp metric 表 |

---

## 7. 本地验证命令

```bash
# 算法仓：mock 全链路
cd demo-algo-ent-analysis
python scripts/run_all.py

# realdata（需 ODS 连通）
python scripts/run_realdata_ent.py all

# UI 构建
cd demo-ui-system-test
pnpm install --node-linker=hoisted
pnpm build
```

---

## 8. 阻塞与后续

| 项 | 说明 |
|----|------|
| realdata 与 mock 双轨 | 部署默认 mock 灌数；realdata 需 `database_env.yaml` ODS 可达 |
| cfg_metric seed formula | 部分 M_ENT_* 仍为 pending_algorithm，需在编排仓更新 formula 后同步 |
| 网关 | 确保 `/entan/**` 路由已配置（与 policy 同进程） |

---

**签收**：企业侧已具备与政策侧对等的「全集 API + calc_process + 灌数据 + system-test Tab」闭环。
