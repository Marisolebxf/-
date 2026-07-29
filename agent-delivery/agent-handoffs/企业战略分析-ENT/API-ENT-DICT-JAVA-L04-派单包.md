# 派单包：API-ENT-DICT-JAVA-L04

- **派单方**：coordinator（`human:淮政玮` · 2026-07-29）
- **监管人**：`human:淮政玮`
- **执行 Agent**：`api-agent`
- **仓**：`lumen-svc-platform`（push `origin/dev`）
- **依赖**：`DATA-ENT-DICT-IMPL-L02` done 后升 `ready`
- **性质**：实现类（`cicd: required`）

## 范围

Java Facade 透传 Python `/internal/gkx-search/meta/*`：

- `region-scopes`（运营地域树）
- `regions` / `company-types` / `enterprise-scales`（四档 + 规上独立）
- `tags` / `filters`（listing=`上市|未上市|退市`）

铁律：前端只调 Java；Java 不写算法、不直连 nGQL。

## 不做

前端改码、全量国标灌数、改 Python 算法逻辑（契约回归除外）

## 派单话术

```markdown
/goal api-agent
任务 ID：API-ENT-DICT-JAVA-L04
监管：human:淮政玮
认领：先按 gkx-task-claim-supervision 写入 claimed
派单包：agent-handoffs/企业战略分析-ENT/API-ENT-DICT-JAVA-L04-派单包.md
依赖：DATA-ENT-DICT-IMPL-L02 done
目标：lumen-svc-platform 透传企业检索 meta 字典（含 region-scopes；对齐 Q056–Q059）
不做：前端、全量国标、Python 算法
DoD：见 task-registry
Handoff：agent-handoffs/企业战略分析-ENT/API-ENT-DICT-JAVA-L04.md
架构铁律：调用链前端→Java→Python /internal/*；push origin/dev
```
