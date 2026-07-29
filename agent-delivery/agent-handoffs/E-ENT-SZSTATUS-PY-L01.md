# Handoff — E-ENT-SZSTATUS-PY-L01

> **status**: review  
> **claimed_by**: human:徐滕强  
> **supervised_by**: human:徐滕强  
> **agent**: data-agent（architect 打回后补齐 DoD）  
> **completed_at**: 2026-07-29T19:30:00+08:00  
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
| 推 origin/dev | 本 handoff 对应 commit（见产物） |

冒烟此前 5/5 HTTP 200 已过；本次补 pytest + 文档 + handoff。

---

## 2. 偏离

- ES 路径 `key_node_enterprise_count` 在缺 `node_imp_level` 时可为 0（demo 可接受，正式需 ETL）。
- Tab B `city-benchmark` 走 ADS/Mock（v1 `ent_sz_status`），禁止实时跨城聚合。

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
5. demo-svc-topic-py ✅  

---

## 5. 开放项

- Java Feign 与 KEYENT 同单 `E-ENT-KEYENT-JAVA-L01`
- `node_imp_level` ETL 补齐后修正 key_node_enterprise_count

---

## 6. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 40k（与 KEYENT 同会话分摊） |
| actual_cost | ~$0.3 |
| cost_warn | green |
