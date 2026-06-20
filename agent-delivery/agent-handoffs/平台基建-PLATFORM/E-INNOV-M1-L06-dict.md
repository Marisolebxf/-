# API handoff · E-INNOV-M1-L06 GET /dict/event-types 图例对齐

| 项 | 值 |
|---|---|
| 任务 | E-INNOV-M1-L06 |
| Epic | E-INNOV-M1 |
| 角色 | api-agent |
| 仓 | `F:/gkx-lumen/repos/lumen-svc-platform` |
| 分支 | `feat/E-INNOV-M1-L06` |
| 基线 | `feat/E-INNOV-M1-L04` |
| 日期 | 2026-06-20 |
| Pipeline / mvn | **deferred** — PM waiver v2 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 说明 |
|--------|------|------|
| `dim_event_type` 字典返回 `nameZh` + `color` | ✅ | `InnovDao` snake_case→camelCase；响应字段 `eventType` / `nameZh` / `color` |
| 与 `EventMap.vue` legend 一致 | ✅ | 色值与 `demo-algo-science/innov/mockgen/seed_dims.py` EVENT_TYPES 12 类对齐；图例顺序固定 |

## 接口契约

| 外部（网关） | 内部 | 响应 `data` 元素 |
|--------------|------|------------------|
| `GET /innov/v1/dict/event-types` | `GET /v1/dict/event-types` | `{ eventType, nameZh, color, produceMode, importancePrior }` |

前端 `EventMap.vue` 使用字段：

- 筛选下拉：`t.eventType`、`t.nameZh`
- 图例：`t.color`（背景色）、`t.nameZh`（文案）
- 地图点位：`colorOf(p.eventType)` → `color`

## 图例色对齐表（真源 = seed_dims.py）

| eventType | nameZh | color |
|-----------|--------|-------|
| tech_break | 技术突破 | #e63946 |
| achievement | 成果发布 | #f4a261 |
| financing | 融资 | #2a9d8f |
| invest | 对外投资 | #264653 |
| ma | 并购 | #9b5de5 |
| bid | 中标 | #00b4d8 |
| biz_dynamic | 企业动态 | #8d99ae |
| policy | 政策发布 | #e76f51 |
| fund_project | 科研立项 | #43aa8b |
| talent_flow | 人才流动 | #f72585 |
| award | 获奖荣誉 | #ffd166 |
| industry_event | 产业活动 | #6c757d |

## 产物清单

| 路径 | 说明 |
|------|------|
| `gkxlumen-innov/.../support/EventTypeLegendCatalog.java` | 12 类图例真源 + Wave 0 Mock 回退 |
| `gkxlumen-innov/.../support/DictSupport.java` | 查询维表、按图例顺序排序、空表回退 |
| `gkxlumen-innov/.../controller/DictController.java` | `/dict/event-types` 走 DictSupport |

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| D1 算法只在 Python | ✅ 只读维表 SELECT |
| D2 调用链 前端→Java→Python | ✅ 字典来自 MySQL dim_event_type |
| D3 NebulaGraph | N/A |
| D4 可观测性 OTel | ✅ 继承 L03 innov 服务 |
| D5 CI/CD | 🟡 mvn/push 后 CI deferred（waiver v2） |
| D9 数据血缘 | 🟡 字典项非统计指标；事件地图指标 ⓘ 由 L07+ 验收 |

## 测试结果

| 项 | 结果 |
|----|------|
| 本地 `mvn package` | **跳过**（PM waiver v2） |
| curl `/innov/v1/dict/event-types` | **deferred**（L10 补验） |
| 静态审查 | ✅ camelCase 字段与 EventMap.vue 一致 |

## L10 补验 curl

```bash
curl -s -H "Authorization: Bearer <token>" \
  "<dev-gateway>/innov/v1/dict/event-types" | jq '.data[0]'
# 期望含 eventType / nameZh / color；tech_break.color = "#e63946"
```

## 下一任务

- **L07** frontend-agent：lumen-ui-science-pc innov 模块接网关
- **L09** frontend-agent：demo2 vs lumen EventMap 对照
- **L10** qa：本接口 + M1 全套补验

## Commit

- 分支：`feat/E-INNOV-M1-L06`
- message：`[agent:api-agent] E-INNOV-M1-L06 event-types dict nameZh+color legend align`

---

*handoff · api-agent · E-INNOV-M1-L06*
