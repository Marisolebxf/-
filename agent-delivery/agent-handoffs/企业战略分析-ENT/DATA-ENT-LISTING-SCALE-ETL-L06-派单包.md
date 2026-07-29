# 派单包：DATA-ENT-LISTING-SCALE-ETL-L06

- **派单方**：coordinator（`human:淮政玮` · 2026-07-29）
- **监管人**：`human:淮政玮`
- **执行 Agent**：`data-agent`（可协同 algorithm / etl 仓）
- **仓**：`demo-svc-topic-py` / `lumen-etl-es-py`（按现有 ES 同步路径择一主改）
- **依赖**：`DATA-ENT-DICT-IMPL-L02`（**done**）→ 本单已升 **`ready`**，可认领（P2）
- **优先级**：P2（不挡接口先通；挡筛选结果与 ODS 一致）

## 范围

1. **Q059**：`dwd_org_base_info.stock_type` / `listed_status` 逗号多值 → 拆证券明细 → 企业级 `listing_status`（有在市→上市；全退市→退市；无证券→未上市）
2. **Q058**：`is_above_scale`（或等价）写入检索可用字段；口径写清源字段与工业营收门槛

## 不做

前端、全量国标区划、Java Facade（契约字段名变更须在 handoff 通知 JAVA/FE）

## 派单话术

```markdown
/goal data-agent
任务 ID：DATA-ENT-LISTING-SCALE-ETL-L06
监管：human:淮政玮
认领：先按 gkx-task-claim-supervision 写入 claimed
派单包：agent-handoffs/企业战略分析-ENT/DATA-ENT-LISTING-SCALE-ETL-L06-派单包.md
依赖：DATA-ENT-DICT-IMPL-L02 done
目标：listing_status / is_above_scale ODS→ES（或检索层）派生落地（Q058/Q059）
不做：前端、全量国标
DoD：见 task-registry
Handoff：agent-handoffs/企业战略分析-ENT/DATA-ENT-LISTING-SCALE-ETL-L06.md
架构铁律：算法/ETL 只在 Python；调用链不越层
```
