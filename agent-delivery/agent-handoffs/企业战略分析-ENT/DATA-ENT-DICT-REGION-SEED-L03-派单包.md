# 派单包：DATA-ENT-DICT-REGION-SEED-L03

- **派单方**：coordinator（`human:淮政玮` · 2026-07-29）
- **监管人**：`human:淮政玮`
- **执行 Agent**：`data-agent`
- **依赖**：`DATA-ENT-DICT-IMPL-L02`（**done** · 2026-07-29T19:50）→ 本单已升 **`ready`**，可认领
- **性质**：数据灌数（`cicd: skip` 以编排/SQL 为主；若改 topic-py 脚本则跟仓 CI）

## 范围

1. `gkxlumenx_dim.code_region` **全量国标**省→市→区县（替代仅 11 行样例）
2. 校正 `region_scope.bind_admin_code` / `region_scope_member`（含深圳区县）
3. G20 / 热门科创城市 Mock 扩种（Q056）

## 不做

前端、Java、改 meta 枚举契约（除非回归修复）

## 派单话术

```markdown
/goal data-agent
任务 ID：DATA-ENT-DICT-REGION-SEED-L03
监管：human:淮政玮
认领：先按 gkx-task-claim-supervision 写入 claimed
派单包：agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-REGION-SEED-L03-派单包.md
依赖：DATA-ENT-DICT-IMPL-L02 done
目标：code_region 全量国标灌数 + region_scope bind 校正 + G20/热门 Mock 扩种
不做：前端、Java
DoD：见 task-registry
Handoff：agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-REGION-SEED-L03.md
```
