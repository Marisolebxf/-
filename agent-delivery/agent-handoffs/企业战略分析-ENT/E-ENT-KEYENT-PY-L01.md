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

## 产物清单

| 产物 | 路径 |
|------|------|
| 重点企业 10 接口 | `gkx_search_service/views/key_analysis.py` |
| 测试 | `tests/test_key_analysis_sz_status.py`（关单 16 passed） |
| API 文档 | `docs/API-接口文档.md` v16.0 §23 |
| 仓/提交 | `demo-svc-topic-py@70f1111` origin/dev |

> 2026-08-21：关单日 architect 复验通过。2026-08-03 存量 done→integration。**2026-08-21 正式门面 INT 已补**（见 §8）。

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

---

## 8. 正式联调（2026-08-21）

| 项 | 内容 |
|----|------|
| 环境 | `http://111.198.38.90:50199` `/enterprise/topic/v1/key-analysis/**` |
| 下游 | `gkxlumen-platform-search-py` `/internal/gkx-search/key-analysis/**`（不走 `50105`） |
| 结论 | 10 门面调用链联调通过（有条件） |
| 条件 | Tab A 因 ES 无 `key_enterprise` 标签计数为 0；brief-card 用检索真实 org 可取到 `name_cn` |
| 记录 | `agent-delivery/qa/test-records/KJZTFWXT/R0/INT-重点企业分析联调-记录-20260821.md` |
| 证据 | `agent-delivery/qa/evidence/KJZTFWXT/R0/E-ENT-KEYENT-PY-L01-20260821.json` |
| 抽样 trace | overview `ae213247e3294ddb11149786a0d2a688`；brief-card `5d0a17eeef520be26ac05e48eea07c96` |

ponytail: off（联调文档，不改业务代码）
