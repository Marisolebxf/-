# 派单包 · TOPIC-METRIC-INVENTORY-L01

> **状态**：ready · **认领类型**：`coordinator_dispatch` 或监管人 `pull`  
> **Agent**：`algorithm-agent` · **supervised_by**：`human:唐绍祖` · **lock**：4h  
> **仓**：`gkx-orchestration`（只写编排资产，不碰业务仓）  
> **说明**：[`给人说明-指标盘点-2026-08-20.md`](./给人说明-指标盘点-2026-08-20.md)

## 1. 目标

从需规抽出**专题系统**指标需求框架 + 逐条清单：优先服务机构 / 政策 / 综合；**产业链、企业对照现有 seed，缺则补抽**。只列需求，不写公式、不改种子。

## 2. 必读（只读）

1. `agent-delivery/bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/README.md` 及维度目录：`产业服务/` `政策/` `综合/` `产业链/` `企业/`
2. `agent-delivery/bid-reference/srs/04-科技专题服务系统/科技专题战略分析/` 对应 `*分析.md`
3. 对照勿当已闭合：`metrics/cfg_metric-ENT-seed.yaml`、`cfg_metric-CHAIN-seed.yaml`、`metric-readiness-matrix-*.yaml`
4. `agent-delivery/data-lineage-policy.md` §2（知道 8 件套，本叶不填满 formula）

## 3. 禁止

- 写 Python / 改 demo-algo / 改 `cfg_metric-*-seed.yaml`
- 把人才/科研机构/技术/燕大知识图谱算进「我方公式」
- 用 CHAIN-SZ demo 种子冒充产业链九维基础指标已齐全
- `git commit` / `git push`（除非唐绍祖另令）

## 4. 产出（必须全部落盘）

目录：`agent-delivery/metrics/indicator-inventory/2026-08-20/`

| 文件 | 内容 |
|------|------|
| `README.md` | 维度 × 层（基础指标/图谱/深度或综合）× 专题页功能点框架 |
| `hierarchy.md` | **给人看的树**：每个维度下列一级 → 二级 → 三级（如有）；无下级写「本级止」 |
| `inventory.yaml` | 每条必填：`level`（1/2/3）、`parent_id`（一级为空）、候选 id、中文名、维度、层、bid_ref、srs_path、excel_seq、原始短语、owner |
| `gaps.md` | 需规点了能力但未点名指标的条目 |
| `coverage-check.md` | 产业链九维 / 企业五类 与现有 seed 对照：已有引用 / 补抽条数 |

handoff：`agent-handoffs/算法库联调-ALGO-LIB/TOPIC-METRIC-INVENTORY-L01.md`

## 5. DoD

- [ ] 服务机构、政策、综合：算法库「（N）xxx」类标题均为 **一级** 行，组内可独立统计量落 **二级**（销售额/增长率等）；原文再切片才建 **三级**
- [ ] `hierarchy.md` 可按维度展开一/二/三级；禁止无原文依据编造三级
- [ ] 产业链、企业：`coverage-check.md` 写明缺什么并已补进 inventory（或证明 seed 已覆盖并引用 metric_id）
- [ ] 每条能回指 srs 路径 + 序号；每条有 `level` + `parent_id`
- [ ] handoff 含：一级 N 条 / 二级 N 条 / 三级 N 条

## 6. `/goal`（整段粘贴到新 Agent 会话）

```text
/goal
task: TOPIC-METRIC-INVENTORY-L01
agent: algorithm-agent
supervised_by: human:唐绍祖
claim_type: pull
强度：本叶为 definition/spike 文档盘点，禁止用 ponytail 砍文档完整性；不写代码。

先读：
- agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/给人说明-指标盘点-2026-08-20.md
- agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/TOPIC-METRIC-INVENTORY-L01-派单包.md
- agent-delivery/bid-reference/srs/05-深度挖掘算法/科技专题服务算法库/README.md

动作：
1. MCP task-claim TOPIC-METRIC-INVENTORY-L01（supervised_by=human:唐绍祖）后开工
2. 从算法库+专题需规抽出 inventory：服务机构、政策、综合全量；产业链与企业对照 cfg_metric-CHAIN/ENT-seed，缺则补抽
3. 落盘 agent-delivery/metrics/indicator-inventory/2026-08-20/{README.md,hierarchy.md,inventory.yaml,gaps.md,coverage-check.md}；inventory 每条必须有 level(1/2/3)+parent_id，hierarchy.md 按树展示
4. 写 handoff；status → review。不改 cfg_metric 种子、不 commit（除非监管人另令）
```
