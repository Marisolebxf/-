# 派单包：FE-ENT-DICT-WIRE-L05

- **派单方**：coordinator（`human:淮政玮` · 2026-07-29）
- **监管人**：`human:淮政玮`
- **执行 Agent**：`frontend-agent`
- **仓**：`lumen-ui-topic`（专题 Track-MS；push `origin/dev`）
- **依赖**：`API-ENT-DICT-JAVA-L04` done 后升 `ready`
- **性质**：实现类（`cicd: required`）

## 范围（对齐 Q056–Q059）

1. `RegionSelect` / 结果区级联改读 Java meta（region-scopes）；去掉写死权威
2. 高筛：工商类型 + 资质标签 **双字段**（Q057）
3. 规模：大中小微 + 规上可叠加（Q058）
4. 上市：`上市` / `未上市` / `退市`（Q059；不加「已」）

只调 Java，不直连 Python `/internal/*`。

## 必读

`Design.md`、`UX-UE 通用交互组件规范.md`、`ENT-DICT-CATALOG-L01.md`、JAVA-L04 handoff

## 不做

改 Java/Python 契约真源、全量国标灌数

## 派单话术

```markdown
/goal frontend-agent
任务 ID：FE-ENT-DICT-WIRE-L05
监管：human:淮政玮
认领：先按 gkx-task-claim-supervision 写入 claimed
派单包：agent-handoffs/企业战略分析-ENT/FE-ENT-DICT-WIRE-L05-派单包.md
依赖：API-ENT-DICT-JAVA-L04 done
目标：lumen-ui-topic 字典接线（RegionSelect + 双字段 + 规模/上市对齐 Q056–Q059）
不做：改后端契约、全量国标
DoD：见 task-registry
Handoff：agent-handoffs/企业战略分析-ENT/FE-ENT-DICT-WIRE-L05.md
架构铁律：前端→Java→Python；Design.md + 交互规范；push origin/dev
```
