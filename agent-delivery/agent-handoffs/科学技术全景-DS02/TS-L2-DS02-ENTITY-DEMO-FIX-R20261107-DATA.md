# TS-L2-DS02-ENTITY-DEMO-FIX-R20261107-DATA · DS02 关联实体 LOOP · 覆盖不到（强度/中文名/年份）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`（LOOP 2026-11-07 首轮 ENTITY DATA） |
| 说明 | 不开工 `SYSINT-TECHGRAPH-02-L02`/`L03`。QUERY `influence` null 挂 `TS-L2-DS02-GRAPH-DEMO-FIX-R20261107-QUERY`，本单不重复建 QUERY。不改前端。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只核对 schema / 抽样与 L02 去重；未另造边属性灌数捷径。 |

## 结论

**blocked**，hung-on **`SYSINT-TECHGRAPH-02-L02`**（边属性与实体列表写入面）。另有 **无源** 项需用例回写，不能靠本单灌 ADS。

## 缺口键与实测

| 缺口键 / 现象 | 实测（2026-11-07） |
|---------------|-------------------|
| `nebula.demo_gkx_chain.tech_has_*.{weight\|relationStrength}` | `_EDGES` 中 `tech_has_paper` / `tech_has_patent` / `tech_has_institution` 的 `props` 为 **空**。边已大量存在（paper 108337 / patent 172644 / institution 51000），但**无可写强度列**。 |
| 实体 `name_zh` | Tag 有 `name_zh` 列。抽样 20：`tech_paper`/`tech_patent` 非空 **0**；`tech_institution` 约 1/20；`tech_point` 20/20 有中文名。用例「name 退为编号」与论文/专利空名一致。 |
| 实体年份 / `updatedAt` | 实体 Tag **无** year / updatedAt；读图 `listRecords` 将 `summary`/`updatedAt` **硬编码空串**（`tech_graph_read.py`）。`tech_rel` 上的 `first_evidence_year` 属点-点关系，**不用于** `tech_has_*` 实体行（见 ENTITY-DATA as-built）。 |

覆盖不到行对照用例：22 初始化与强度、24 描述时间线、25 按时间、27 按强度时间 —— 与上表一致，本单无法在「只改后端图/属性且不开工 L02」下闭合。

## 与 SYSINT-TECHGRAPH-02-L02 去重

| 项 | 值 |
|----|-----|
| L02 状态 | `backlog`；**本单未开工** |
| 去重结论 | 关联实体边上图与列表属 L02。但现行 L02/`tech_graph.py` 对 `tech_has_*` 仍 **无** weight 类 props；即便 L02 按现行稿写完，**强度字段仍无源**，需扩 EDGE schema 或改读口径（人拍板）。 |
| name_zh 空 | 更偏 L01 顶点灌值质量；仍挂 L02 作「实体可见性」去重锚，补中文名需写顶点任务，**非本单代开**。 |

## 用例回写建议（勿静默改期望）

对象：`TS-L2-DS02-ENTITY-合规演示用例.md` 覆盖不到行 22/24/25/27。

建议文案（确认后改用例）：

> 关联强度：`tech_has_*` Edge 无 weight/relationStrength（DESCRIBE / `_EDGES` 已核）；在扩边属性并入图前，相关「按强度」行标 **设计无资源**，勿期望 DATA 单灌出强度。  
> 实体年份 / 时间线：实体 Tag 与读图契约无 year/updatedAt；「按时间」排序/筛选行标 **设计无资源**，直至契约扩字段。  
> `name_zh`：列存在但论文/专利抽样多为空 —— 保留 **覆盖不到（顶点灌值缺口）**，挂顶点入图/补名任务，不把空名改成可演。

## 修改内容

- 无代码、无写图、无写 ADS。  
- 仅本 handoff。

## 测试结果

- 经 algo-py pod：边 count + 实体 `name_zh` 抽样 + schema 对照仓内 `_EDGES`/`_TAGS`。  
- ADS `influence` 行仍在（252363）；本单不宣称 QUERY 层已叠到 UI。

## 遗留风险 / DoD 开项

1. 强度 / 年份 / 描述时间线 —— **开**，hung-on L02 + 无源回写。  
2. name_zh —— **开**，顶点灌值。  
3. QUERY influence —— 不归本单。  
4. 未改前端、未改 D4。

## CI/CD（必填）

- 仅编排仓 handoff；无业务镜像。

## 架构合规自检

未越层写图；未开工 L02/L03；D18/D4 未伪绿。✅

## Cost 回填（建议）

- actual_tokens: ~9000  
- model_used: claude-sonnet-4.5  
- actual_cost: 0.05  
- cost_warn: green

## 人下一步

1. 拍板：强度/年份是「扩 schema」还是「用例改设计无资源」。  
2. 等 L02 ready 后再验收实体边上图；同时单独立项补论文/专利 `name_zh`。  
3. 本 DATA 勿 done，直至上述闭合或用例回写签收。

## 监管人拍板 2026-11-07

human:淮政玮：**另开 Tag/Edge 扩列**。登记 Q072；挂 `TS-L2-DS02-SCHEMA-EXPAND-L01`。本 DATA 继续 blocked；不开工 L02/L03。
