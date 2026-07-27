# 派单包：ENT-ALGO-EVAL-INTERACTIVE — entan 扩展交互式评估接口

- **任务 ID**：ENT-ALGO-EVAL-INTERACTIVE
- **派发角色**：architect-agent（[human:徐滕强] 监管）
- **承接角色**：algorithm-agent
- **仓**：`demo-algo-ent-analysis`（entan）
- **依赖**：无（算法组独立）；被 `ENT-PY-EVAL-TASK` 硬依赖
- **派发时间**：2026-07-21
- **v3.2 修订**：2026-07-27 监管人 human:徐滕强 确认（对齐 ARCH-ANALYSIS-TASK v3.2 §9 三套 sub_type 结果契约）

---

> **⚠️ v3.2 结果契约变更（重要）**
>
> 本派单包原始版本（2026-07-21）基于旧四维统一结构（`innovation`/`operation`/`growth`/`risk`）。
> 架构文档 v3.2 §9 已将评估结果契约定为 **三套差异化 sub_type schema**：
> - `technology`：五维雷达（技术创新/技术人才/技术投入/技术合作/技术转化）+ 排名 + 技术诊断表
> - `business`：经营指标对比（非雷达）+ 排名 + 经营诊断/营收趋势/行业对标 Tab
> - `competitiveness`：三维雷达（创新能力/经营能力/成长能力）+ 排名 + 综合诊断 + 参照均值/龙头
>
> **旧四维结构（innovation/operation/growth/risk）仅作为算法内部评分计算的中间态**，
> 不得作为对外结果 schema。entan 返回给 gkx_ai_service 的结果须按 sub_type 组装为对应 schema；
> gkx_ai_service 透传给 Java，Java 原样落库不组装。
>
> 下方 §2.1 出参契约、§3.2 维度映射中的四维描述**仅保留作内部计算参考**，最终对外结构以 v3.2 §9 为准。

---

## 1. 背景

数据侧 `gkx_ai_service`（`demo-svc-topic-py`）已落地企业评估任务编排层（7 端点 `/internal/gkx-ai/evaluation/*`），当前用 **Mock 优先** 策略运行（entan_client 返回确定性 Mock 评分）。

要切真实评估，需算法组在 entan 侧扩展**交互式评估接口**：按指定企业集合 + 自定义权重计算，返回可解释结果。

### 现状盘点（entan 已有 5 个 GET 接口）

| 接口 | 类型 | 局限 |
|---|---|---|
| `GET /v1/score` | 列表查询型 | level/chain/city/keyword 过滤全表，权重写死 `S=0.40*innov+0.40*operate+0.20*growth` |
| `GET /v1/ranking` | 列表查询型 | 按 rank_dim 全表排名，不能限定企业集合 |
| `GET /v1/diagnosis` | 列表查询型 | level/chain/keyword 过滤全表 |
| `GET /v1/centrality` | 列表查询型 | 全表 PageRank |
| `GET /v1/risk` | 列表查询型 | 全表风险 |

**核心缺口**：无法接收 `enterprise_codes[]`（精确企业集合）+ `weights`（自定义权重）做交互式计算。

### gkx_ai_service 已约定的调用契约

`entan_client.py` 当前在联调模式下会 POST：

```
POST {entan_base_url}/v1/evaluation/score
Content-Type: application/json

{
  "enterprise_codes": ["6bc50eca...", "6eeabc49..."],
  "weights": {"innovation": 0.5, "operation": 0.2, "growth": 0.2, "risk": 0.1},
  "template_id": "TPL-INNOVATION",   // 可选
  "sub_type": "technology"                // technology|business|competitiveness
}
```

期望响应：

```json
{
  "code": 0,
  "data": {
    "scores": [
      {
        "enterprise_code": "6bc50eca...",
        "total_score": 82.5,
        "rank": 1,
        "dimensions": {"innovation": 88.0, "operation": 76.5, "growth": 85.2, "risk": 80.1},
        "calc_process": { ... },        // D9 血缘
        "confidence": "high"            // high|medium|low
      }
    ],
    "model_version": "entan-v1.0",
    "data_source": "entan"
  }
}
```

---

## 2. 任务范围

### 2.1 必做（DoD）

1. **新增交互式评估接口**（POST，区别于现有 GET 列表查询）：

   | 接口 | 方法 | 作用 |
   |---|---|---|
   | `/v1/evaluation/score` | POST | 按企业集合 + 自定义权重计算评分 + 排名 |
   | `/v1/evaluation/diagnosis` | POST | 按企业集合生成诊断（优势/短板/建议） |
   | `/v1/evaluation/radar` | POST | 按企业集合生成雷达维度数据 |

   > 三个接口可合并为一个 `/v1/evaluation/compute`（返回 score+diagnosis+radar），由算法组按内部实现便利决定；但 gkx_ai_service 侧只调一个入口，建议合并。

2. **入参契约**：
   - `enterprise_codes`: `list[str]`（必填，1-50 个）
   - `weights`: `dict[str, float]`（可选，缺省用 sub_type 默认权重）
   - `sub_type`: `"technology" | "business" | "competitiveness"`（必填，对齐 UI 三模式）
   - `template_id`: `str`（可选，算法侧可忽略，透传用）

3. **出参契约**（与 gkx_ai_service 的 `entan_client.py` 对齐）：
   - `scores[]`：每家企业 `enterprise_code` / `total_score` / `rank` / `dimensions{}` / `confidence`
   - `model_version`: 算法版本号
   - `data_source`: `"entan"`
   - **内部计算维度键名**（四维，仅用于 `dimensions{}` 评分中间态）：`innovation` / `operation` / `growth` / `risk`
   - **对外结果结构**：按 `sub_type` 组装为 v3.2 §9 三套 schema（technology 五维雷达 / business 经营指标 / competitiveness 三维雷达）；四维→对外维度的映射由算法侧或 gkx_ai_service 完成，Java 不组装。

4. **权重可自定义**：权重从请求体读，不写死 `settings.yaml`；缺省时按 sub_type 给默认值。

5. **三模式支持**（内部计算侧重不同，对外结果 schema 不同）：
   - `technology`（技术力）：内部侧重 innovation；对外输出五维雷达（技术创新/技术人才/技术投入/技术合作/技术转化）
   - `business`（商业力）：内部侧重 operation；对外输出经营指标对比（非雷达）+ 排名 + 诊断 Tab
   - `competitiveness`（综合竞争力）：内部四维均衡计算；对外输出三维雷达（创新能力/经营能力/成长能力）+ 参照均值/龙头

6. **D9 数据血缘**：每条结果的 `calc_process` 含 `metric_id` / `formula` / `source_tables` / `model_version`（沿用现有 `_calc_process` 函数范式）。

7. **响应包络**：统一 `{code, msg, data}`，与 entan 现有接口一致。

8. **handoff 文档** + 架构合规自检 + cost 四字段回填。

### 2.2 可选（非阻塞）

- 雷达维度轴归一化到 0-100（FULL 前逐轴登记 metric_id，受 Q014 阻断的轴标注 GAP）
- 数据覆盖度/可信度计算（gkx_ai_service 当前自己做预检，entan 可选返回）

---

## 3. 实现建议（非强制，算法组可自行设计）

### 3.1 复用现有数据

entan 现有 `ads.enterprise_score` / `ads.tech_power` / `ads.biz_power` / `ads.enterprise_diagnosis` 表已有预计算得分。交互式接口可：
- 按 `enterprise_codes` 过滤这些表
- 用请求 `weights` 重新加权汇总（而非读写死的 `score_total`）
- 诊断复用 `ads.enterprise_diagnosis` 的优势/短板逻辑

### 3.2 维度映射

| gkx_ai_service 维度键 | entan 数据源 | 说明 |
|---|---|---|
| `innovation` | `ads.tech_power` / `ads.enterprise_score.score_innov` | 创新能力 |
| `operation` | `ads.biz_power` / `ads.enterprise_score.score_operate` | 经营能力 |
| `growth` | `ads.enterprise_score.score_growth` | 成长性 |
| `risk` | `ads.realdata_enterprise_risk.risk_score`（反向归一） | 风险水平（低风险=高分） |

### 3.3 路由文件

建议新建 `api/entan_evaluation_routes.py`，在 `main.py` 注册，与现有 `entan_analysis_routes.py` 平级，避免 Convoy Risk（不混改列表查询接口）。

---

## 4. 禁止项

1. ❌ 不改现有 5 个 GET 接口（`/v1/score` `/v1/ranking` `/v1/diagnosis` `/v1/centrality` `/v1/risk`）—— 保持向后兼容
2. ❌ 不写死权重到 `settings.yaml` —— 权重从请求体读
3. ❌ 不替甲方拍板 Q014（临时默认权重标注 ⚠️，不升 🟢）
4. ❌ Java 不直连 entan —— 只经 gkx_ai_service 屏蔽层调用
5. ❌ 不碰 `demo-svc-topic-py` 仓 —— 那是数据侧，本任务只动 `demo-algo-ent-analysis`

---

## 5. 与 gkx_ai_service 的对接点

gkx_ai_service 的 `entan_client.py` 已实现联调占位：

```python
# 联调模式（GKX_MOCK_ENABLED=false）会 POST：
POST {entan_base_url}/v1/evaluation/score
{
  "enterprise_codes": [...],
  "weights": {...},
  "template_id": "...",  # 可选
  "sub_type": "technology"
}
```

算法组实现接口后，**无需通知 data-agent 改代码**（gkx_ai_service 已预留 HTTP 调用）；只需确保：
1. 接口路径 = `/v1/evaluation/score`（或告知 data-agent 改 `entan_client.py` 的 URL 常量）
2. 入参/出参字段名与本派单包契约一致
3. entan 服务地址对 gkx_ai_service 可达（K8s dev 同 namespace 或配置 `GKX_ENTAN_BASE_URL`）

联调验证时，data-agent 会把 `GKX_MOCK_ENABLED` 切 false，用同一批企业 codes 跑 gkx_ai_service → entan 全链路。

---

## 6. 架构合规自检（§2 铁律）

| # | 铁律 | 本次 | 说明 |
|---|---|---|---|
| 1 | 算法只在 Python | ✅ | 评估计算在 entan（Python） |
| 2 | 调用链前端→Java→Python | ✅ | entan 被 gkx_ai_service(Python) 调用，Java 不直连 |
| 3 | 图谱 NebulaGraph | N/A | 本任务不涉图 |
| 4 | 可观测性 | ✅ | 沿用 entan 现有日志；新接口加结构化日志 |
| 5 | CI/CD | ✅ | demo-algo-ent-analysis main 直推（POC 阶段） |
| 6 | demo2 不 merge lumen | ✅ | 本任务在算法 demo 仓 |
| 7 | 共享聚合核心 | ✅ | 评估经 gkx_ai_service 屏蔽层 |
| 8 | 数据走 ADS | ✅ | entan 读 ads.* 表 |
| 9 | D8 前端规范 | N/A | 本任务不涉前端 |
| 10 | D9 数据血缘 | ✅ | calc_process 含 metric_id/formula/source_tables |

---

## 7. DoD 清单

- [ ] entan 新增 POST `/v1/evaluation/score`（或 `/v1/evaluation/compute`）交互式评估接口
- [ ] 入参：enterprise_codes[] + weights{} + sub_type + template_id?
- [ ] 出参：scores[]（enterprise_code/total_score/rank/dimensions/confidence）+ model_version + data_source
- [ ] **对外结果按 sub_type 组装为 v3.2 §9 三套 schema**（technology 五维 / business 经营指标 / competitiveness 三维）；旧四维仅内部计算
- [ ] 权重从请求体读，不写死
- [ ] 支持 technology/business/competitiveness 三模式
- [ ] calc_process 含 D9 血缘（metric_id/formula/source_tables）
- [ ] 响应包络 {code,msg,data}
- [ ] 不改现有 5 个 GET 接口
- [ ] 本地启动 + curl 冒烟通过（3 家企业 + 自定义权重 → 返回排名+维度+可信度）
- [ ] handoff 文档 + 架构合规自检 + cost 四字段

---

## 8. cost 预估

- estimated_tokens: 150_000
- effort_points: 8
- difficulty: L
- 预计耗时：1-2 天
