# Handoff — E-ENT-KEYENT-PY-L01

> **status**: review  
> **claimed_by**: human:徐滕强  
> **supervised_by**: human:徐滕强  
> **agent**: data-agent（architect 打回后修复）  
> **completed_at**: 2026-07-29T19:30:00+08:00  
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
| 推 origin/dev | 本 handoff 对应 commit（见产物） |

### peer_regions 修复说明（architect blocker）

原逻辑对当前 `region_id` 做 `must_not prefix`，导致 `440300` 时同市企业全被排除 → `peer_regions=[]`。

现口径：
- `_peer_scope_region_id`：区县上溯到市；市 scope=自身
- 按 `district` terms 聚合 TOP5
- Mock：提升 `region_id=440300` 的样本同步写入深圳区县名

---

## 2. 偏离

- ES 正式路径 peer `region_id` 回填依赖码表；Mock 用内置深圳区县码映射。
- `domain-evidence` 正式 5 表 DWD 未建，仍 Mock。

---

## 3. 验收命令

```bash
cd repos/demo-svc-topic-py
.venv/bin/pytest tests/test_key_analysis_sz_status.py -v
# 16 passed（含 key-analysis 10 + sz-status 5 + peers 专项）
```

冒烟：

```bash
curl -s -X POST localhost:8080/internal/gkx-search/key-analysis/region-insight \
  -H 'Content-Type: application/json' \
  -d '{"region_id":"440300","region_name":"深圳市","region_level":"city"}'
# data.peer_regions 非空，含南山/福田等区县
```

---

## 4. 架构合规自检

1. 算法只在 Python ✅  
2. 前端 → Java → `/internal/*` ✅（本仓仅 Python）  
3. 未引入 Neo4j ✅  
4. 只读 ADS/ES/Mock，不写算法 ✅  
5. demo-svc-topic-py，可推 origin/dev ✅  

---

## 5. 开放项

- Java Feign：`E-ENT-KEYENT-JAVA-L01`（blocked 待本单 done）
- ES `node_imp_level` / 领域证据 DWD 表落地（正式环境）

---

## 6. Cost

| 字段 | 值 |
|------|-----|
| model_used | cursor-grok-4.5 |
| actual_tokens | ~估 80k |
| actual_cost | ~$0.6 |
| cost_warn | green |
