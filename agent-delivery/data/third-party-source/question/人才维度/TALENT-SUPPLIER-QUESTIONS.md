# 人才库 — 本期不向久新开口

```yaml
---
doc_id: TALENT-SUPPLIER-QUESTIONS
element: TALENT
role: source
status: draft
version: "2026-09-02"
updated: 2026-09-02
owner: human:郭万迎
audience: 内部（合同边界） / 不发给久新
---
```

> **对接：久新**（人才专题 `TALENT`）。  
> **2026-09-02 合同边界判定：本期不开口。** 智树专题五维 = 企业 / 产业链 / 政策 / 服务机构 / 综合；人才分析不在本期智树实现范围（总集计划负责方=久新；外部接口摘要「技术链、科研机构、人才不进入本期」）。  
> 综合五维若要用人才稳定码，走 [SYNTH-SUPPLIER-QUESTIONS.md](../综合维度/SYNTH-SUPPLIER-QUESTIONS.md) 的三方库边/主键题（P0-3 / P2-1），**不等本叶、不向久新另开 `M_TALENT_*` 书面题**。  
> 方法见 [../README.md](../README.md)。sidecar：[`../source-gap-index.yaml`](../source-gap-index.yaml)（本叶 **未** upsert）。

---

# 现行待回复（滚动）

**本期不向久新索要。** 下表故意留空，避免再出一组非五维、`third_party` 书面题。

| Q-id | 优先级 | 入站表.列 | 问什么 | 卡住的 metric_id | 最近分析日 |
|------|--------|-----------|--------|------------------|------------|
| | | | | | |

<!-- MIXED 本波不进。合同外 third_party 指数题不开。 -->

---

# 分析日志（新的在上）

## 2026-09-02

- 任务：`DATA-SUPPLIER-Q-TALENT-L01`（`in_progress`；`supervised_by=human:郭万迎`；`claimed_by=agent:data-agent`）。叶不标 `done`。
- 合同边界：专题五维不含人才分析 → **不开口**。
- 本批算法类型（registry 32 条，MCP `metric-query domain=TALENT`；未打开 seed YAML）：STAT 1 / COMPUTE 0 / GRAPH 0 / MODEL 0 / third_party 31 / UNKNOWN 0 / MIXED 0
- 本批指标（全量，未切 cap，因判定后整叶跳过对外题）：
  - STAT：`M_TALENT_STRUCT_QUERY`（查询结果·人才结构；总集「数据查询」亦为久新）
  - third_party：其余 31 条 `M_TALENT_*`（学术力/招引/培育/流动/图谱/深圳供需等；`ALGO-LIB-METRIC-DEPS` 人才维 13/13 为 third_party）
- D1：draft 32 / aligned 0。未探库。
- 拟新 Q：0。拟复用 Q：0。
- 跳过：MIXED 0；二次未核细稿（无 `calc-logic/TALENT` 本波不猜列）；CMS-only 未判。**合同外 + kit 几乎全 third_party → 整叶不进对外清单。**
- 甲方 Q093 / Q102 等口径题不改写。
- sidecar：无，仅日志（不把 32 条写成久新缺口游标）。
- 智树要用的人才端：综合协同边 SYNTH-P0-3 / P2-1（三方库）。

---

## 请对方每条按此格式回

本期无对外题，不使用回复模板。
