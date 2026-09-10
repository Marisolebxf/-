# 派单包 · CROSS-VEC-POLICY-L0-L01

```yaml
task_id: CROSS-VEC-POLICY-L0-L01
dispatcher: agent:coordinator-agent
suggested_supervised_by: human:唐绍祖
claim_type: coordinator_dispatch
date: 2026-09-10
status: backlog
ponytail: full
repo: lumen-algo-py
```

## 1. 为什么派

政策 `theme`（监督管理/产业发展）被写入产业槽，时序板 LIKE `chain:INB*` 命中 0。P0 **不依赖 Milvus**。

## 2. 范围 / 不做

**做**：`ods_to_dwd`：`theme` → 仅 `ext5`；产业槽只来自 L1 图名规则（标题/摘要/关键词/要点 + 已有 `match_industry_anchors`）。单测。

**不做**：调 Milvus；调 LLM；rebuild 索引；Hang 上图；改 Java/前端（文案另叶已部分完成）；逐条 embed。

夜班位置：本叶 = **同步短链**；其后才是 Job A → Hang（见派单 README）。

## 3. 必读

- SAD `02-概要设计.md` §1.1、§3、§3.1
- `vendor/entan-py/polan/mockgen/incr.py` · `polan/graph/entity.py`
- `tests/test_industry_vid_enrich.py`
- 架构铁律：算法只在 Python；push `origin/dev`

## 4. 步骤

1. 认领 MCP `task-claim`（supervised_by 花名册真人）。
2. Grep `theme` / `related_entities` / `ext5` 全调用链，只改共享映射，禁止只改一条灌数入口。
3. 单测：纯主题标签不得出 VID；标题含集成电路且锚点存在仍可对码。
4. handoff + cost。

## 5. /goal

```text
/goal algorithm-agent
身份：资深 Python 算法工程师。算法只在 Python；Java 禁止 NLP。
强度：ponytail full。禁止用 YAGNI 跳过可观测与架构铁律。
任务：CROSS-VEC-POLICY-L0-L01
仓库：${GKX_ROOT}/repos/lumen-algo-py
必读：agent-delivery/agent-handoffs/产品整体定义/跨系统-向量库/02-概要设计.md §1.1 §3；本派单包。
目标：政策 ODS→DWD 重灌 L0 — theme 只进 ext5，退出 related_entities.industry；L1 字面对图名保留。
不做：Milvus、LLM、embed/rebuild、假 VID。
验收：pytest 证明纯 theme 无 chain:INB*；handoff 含 ponytail: full 与 cost。
分支：push origin/dev；commit [agent:algorithm-agent]。
```
