# Handoff — E-ENT-KEYENT-PY-L01

> **status**: done  
> **claimed_by**: human:徐滕强  
> **supervised_by**: human:徐滕强  
> **agent**: data-agent（architect 打回后修复）  
> **completed_at**: 2026-07-29T19:30:00+08:00  
> **accepted_at**: 2026-07-29T23:35:00+08:00  
> **accepted_by**: architect（human:徐滕强 复验）  
> **repo**: demo-svc-topic-py  
> **design**: agent-delivery/data/data-design/企业/重点企业分析-功能设计.md v2.3

---

## 1. 范围与实现

| DoD | 证据 |
|-----|------|
| 10 个 `/key-analysis/*` 接口 | `gkx_search_service/views/key_analysis.py` + `main.py` include |
| region-insight peer_regions 口径修复 | 市=下属区县 TOP；区=兄弟区 TOP（排除自身）；Mock 补齐深圳 `district` |
| pytest 全绿 | `tests/test_key_analysis_sz_status.py`（含 city peers 非空断言） |
| API 文档更新 | `docs/API-接口文档.md` v16.0 §23 #74-#83 |
| 推 origin/dev | `demo-svc-topic-py@70f1111`（仍为当前 `origin/dev` ancestor） |

### peer_regions 修复说明（architect blocker）

原逻辑对当前 `region_id` 做 `must_not prefix`，导致 `440300` 时同市企业全被排除 → `peer_regions=[]`。

现口径：
- `_peer_scope_region_id`：区县上溯到市；市 scope=自身
- 按 `district` terms 聚合 TOP5
- Mock：提升 `region_id=440300` 的样本同步写入深圳区县名

---

## 2. 偏离

- ES 正式路径 peer `region_id` 回填依赖码表；Mock 用内置深圳区县码映射。ES 路径 `peer_regions[].region_id` 当前可为空字符串（前端可先用 `region_name`）。
- `domain-evidence` 正式 5 表 DWD 未建，仍 Mock。

---

## 3. 验收命令

```bash
cd repos/demo-svc-topic-py
.venv/bin/pytest tests/test_key_analysis_sz_status.py -v
# 16 passed
```

---

## 4. 架构合规自检

1. 算法只在 Python ✅  
2. 前端 → Java → `/internal/*` ✅  
3. 未引入 Neo4j ✅  
4. 只读 ADS/ES/Mock ✅  
5. 已推 origin/dev ✅  
6. 产业链筛选用 `industry_chains_flat` ✅  
7. 领域归属用 `core_tech_tags_flat` ✅  

---

## 5. 开放项

- Java Feign：`E-ENT-KEYENT-JAVA-L01`（PY deps 已解除）
- ES peer `region_id` 码表回填；领域证据 DWD 5 表落地

---

## 6. Architect 复验（2026-07-29T23:35）

| 上次打回项 | 结果 |
|-----------|------|
| peer_regions 空 | ✅ 440300 → 南山/福田/龙岗；440305 排除南山 |
| 缺 pytest | ✅ 16 passed |
| API 文档 | ✅ v16.0 §23 |
| handoff | ✅ 本文件 |

**决议：通过 → done**

---

## 7. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 80k |
| actual_cost | ~$0.6 |
| cost_warn | green |
