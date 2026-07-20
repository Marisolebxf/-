# 派单包：ENT-MOD-SEARCH-UX-L01

- **派单方**：coordinator
- **时间**：2026-07-21
- **执行 Agent**：`ux-agent`
- **监管人**：human:高颖
- **Sprint**：2026-W30
- **上游**：`ENT-MOD-SEARCH-PACK-L01` ✅ done（2026-07-21 淮政玮）

## 1. 目标

产出企业查询 **UX 交互规格**，闭合 `ENT-MOD-SEARCH-V1-HIFI` 的 UX 依赖，覆盖：

- 智能检索 + 简化高筛 + 横向长卡片列表
- 初始 / 结果 / 空 / 错误 / 无权限 / 导出异步态
- **Q033~Q037** 交互降级与 ⚠️ 提示位（口径未定不阻塞线框，须标注 pending_ref）

## 2. 输入真源

| 文件 | 用途 |
|------|------|
| `E1-企业查询/IA-*.md`、`Wireframe-*.md` | PACK 四件套 |
| `repos/demo-ui-topic/docs/ia/enterprise/ENT-search-design.md` | 现有 IA/交互草案 |
| `PM-PDR-ENT-SEARCH-评审纪要.md` | 门1 定稿（非 NL、导出≤1000、菜单升级） |
| `TRACE-ENT-SEARCH.yaml` | 故事 ID / 开放项 |
| `UX-UE 通用交互组件规范.md` §19 | 走查清单 |

## 3. 交付物

**主产出**（二选一 + handoff 说明选用）：

- `agent-handoffs/产品整体定义/E1-企业查询/UX-SPEC-ENT-SEARCH.md`（推荐），或
- 升版 `ENT-search-design.md` 并在 handoff 声明真源路径

**须含**：

- 主路径 + 异常路径（导出失败、超 1000 条、无结果）
- 高筛字段与 Q033~Q037 对应表
- 与总览 ContextBar **分离** 的导航行为
- Arco 组件选型边界（D10）
- 字段表第 6 列 `metric_id` 与 PACK wireframe 一致

## 4. Definition of Done

1. UX 规格与 IA/Wireframe/TRACE **故事 ID 一致**
2. Q033~Q037 均有交互处理说明（🟡 可挂 PendingBadge 占位）
3. handoff：`ENT-MOD-SEARCH-UX-L01.md`
4. 高颖 review ✅
5. **不**改 demo 代码（UI 实现属 V1-HIFI / V2）

## 5. 下游

| 任务 | 关系 |
|------|------|
| `ENT-MOD-SEARCH-V1-HIFI` | **直接依赖** 本任务 |
| `ENT-MOD-SEARCH-METRIC-OPEN-L01` | 并行，不阻塞 |

## 6. 认领话术

```text
/goal ENT-MOD-SEARCH-UX-L01
监管：human:高颖
交付 UX-SPEC-ENT-SEARCH.md；对齐 Q033~Q037 与 ENT-search-design.md
```
