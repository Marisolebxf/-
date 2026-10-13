# Handoff — E-ENT-SZSTATUS-PY-L01

> **status**: done  
> **claimed_by**: human:徐滕强  
> **supervised_by**: human:徐滕强  
> **agent**: data-agent（architect 打回后补齐 DoD）  
> **completed_at**: 2026-07-29T19:30:00+08:00  
> **accepted_at**: 2026-07-29T23:35:00+08:00  
> **accepted_by**: architect（human:徐滕强 复验）  
> **repo**: demo-svc-topic-py  
> **design**: agent-delivery/data/data-design/企业/深圳企业现状分析-功能设计.md v1.3

---

## 1. 范围与实现

| DoD | 证据 |
|-----|------|
| 5 个 `/sz-status/*` 接口 | `gkx_search_service/views/sz_status.py` |
| 角色枚举 | upstream/midstream/downstream/unlabeled = 上游/中游/下游/暂未标注 |
| pytest 全绿 | `tests/test_key_analysis_sz_status.py` sz_* 用例 |
| API 文档更新 | `docs/API-接口文档.md` v16.0 §24 #84-#88 |
| 推 origin/dev | 与 KEYENT 同仓 `70f1111` ancestor |

## 产物清单

| 产物 | 路径 |
|------|------|
| 深圳现状 5 接口 | `gkx_search_service/views/sz_status.py` |
| 测试 | `tests/test_key_analysis_sz_status.py`（`sz_` 用例） |
| API 文档 | `docs/API-接口文档.md` v16.0 §24 |
| 仓/提交 | `demo-svc-topic-py@70f1111` origin/dev |

> 2026-08-21：关单日 architect 复验通过。2026-08-03 存量 done→integration。**2026-08-21 正式门面 INT 已补**（见 §8）。

---

## 2. 偏离

- ES 路径 `key_node_enterprise_count` 在缺 `node_imp_level` 时可为 0（demo 可接受，正式需 ETL）。
- Tab B `city-benchmark` 走 ADS/Mock，禁止实时跨城聚合。

---

## 3. 验收命令

```bash
cd repos/demo-svc-topic-py
.venv/bin/pytest tests/test_key_analysis_sz_status.py -k sz_ -v
```

---

## 4. 架构合规自检

1. 算法只在 Python ✅  
2. `/internal/*` 未越层 ✅  
3. 未引入 Neo4j ✅  
4. 对标读 ADS/Mock ✅  
5. 产业链筛选用 `industry_chains_flat` ✅  
6. 已推 origin/dev（关单 commit `70f1111`） ✅  
7. 本叶无 UI（D8/D10 不适用） ✅  

---

## 5. 开放项

- Java Feign：`E-ENT-KEYENT-JAVA-L01`（deps 已解除）
- `node_imp_level` ETL 补齐后修正 key_node_enterprise_count

---

## 6. Architect 复验（2026-07-29T23:35）

| 项 | 结果 |
|----|------|
| 5 接口冒烟 | ✅ |
| 角色枚举 | ✅ 无「智库标注」 |
| pytest / API §24 / handoff | ✅ |

**决议：通过 → done**

---

## 7. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 40k |
| actual_cost | ~$0.3 |
| cost_warn | green |

---

## 8. 正式联调（2026-08-21）

| 项 | 内容 |
|----|------|
| 环境 | `http://111.198.38.90:50199` `/enterprise/topic/v1/sz-status/**` |
| 下游 | `gkxlumen-platform-search-py` `/internal/gkx-search/sz-status/**` |
| 结论 | 5 门面调用链联调通过（有条件） |
| 条件 | QUANTUM KPI/清单为 0；city-benchmark 结构齐但 `data_status=无数据` |
| 记录 | `agent-delivery/qa/test-records/KJZTFWXT/R0/INT-深圳企业现状联调-记录-20260821.md` |
| 证据 | `agent-delivery/qa/evidence/KJZTFWXT/R0/E-ENT-SZSTATUS-PY-L01-20260821.json` |
| 抽样 trace | chain-kpi `f98b123847cbaa974a5646d67024e38a`；benchmark `f3f1a81e54cf1c4f1e9070e792d3e596` |

ponytail: off（联调文档，不改业务代码）
