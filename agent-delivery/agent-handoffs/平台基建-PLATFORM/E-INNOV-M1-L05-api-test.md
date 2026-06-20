# API test handoff · E-INNOV-M1-L05 M1 事件 API 接口测试

| 项 | 值 |
|---|---|
| 任务 | E-INNOV-M1-L05 |
| Epic | E-INNOV-M1 |
| 角色 | qa-agent |
| 仓 | `F:/gkx-lumen/gkx-orchestration`（验收文档） |
| 依赖 | E-INNOV-M1-L04（网关路由 `/innov/**`） |
| 日期 | 2026-06-20 |
| Pipeline / curl | **deferred** — PM waiver v2 |

## 范围与实现（对照 DoD）

| DoD 项 | 状态 | 说明 |
|--------|------|------|
| GET /events mode=list\|geo 有数据（dev K8s 网关） | 🟡 **deferred** | 用例 M1-E-001～020 已编写；L10 补验 |
| GET /events/heatmap 有数据 | 🟡 **deferred** | 用例 M1-H-001～006 |
| GET /events/{id} + /relations 可访问 | 🟡 **deferred** | 用例 M1-D-001～006、M1-R-001～006 |
| GET /events/stats 时间桶正确 | 🟡 **deferred** | 用例 M1-S-001～009 |
| geo 模式 P95 ≤ 500ms | 🟡 **deferred** | M1-E-020、M1-H-005；L10 压测 |

## 产物清单

| 路径 | 说明 |
|------|------|
| `agent-delivery/验收文档/创新监测-M1-接口测试报告.md` | §1 全套 GET 用例（41 条）+ 预期；结果栏 DEFERRED |
| `agent-delivery/验收文档/创新监测-开发承接包/03-API接口契约.md` | 契约真源 §1 |
| `agent-delivery/templates/acceptance-test-report-template.md` | 报告模板 |

## 用例统计

| 接口 | 用例数 | 执行 |
|------|--------|------|
| GET /events | 20 | DEFERRED（L10 补验） |
| GET /events/heatmap | 6 | DEFERRED（L10 补验） |
| GET /events/{eventId} | 6 | DEFERRED（L10 补验） |
| GET /events/{eventId}/relations | 6 | DEFERRED（L10 补验） |
| GET /events/stats | 9 | DEFERRED（L10 补验） |
| **合计** | **41** | — |

## L10 补验 curl 清单（示例）

> 替换 `<dev-gateway>` 与 `<token>`；eventId 从 list 响应取样。

```bash
# list
curl -s -H "Authorization: Bearer <token>" \
  "<dev-gateway>/innov/v1/events?mode=list&pageNum=1&pageSize=20"

# geo（bbox 必传）
curl -s -H "Authorization: Bearer <token>" \
  "<dev-gateway>/innov/v1/events?mode=geo&bbox=113.8,22.4,114.5,22.8"

# heatmap
curl -s -H "Authorization: Bearer <token>" \
  "<dev-gateway>/innov/v1/events/heatmap?bbox=113.8,22.4,114.5,22.8"

# detail
curl -s -H "Authorization: Bearer <token>" \
  "<dev-gateway>/innov/v1/events/<eventId>"

# relations
curl -s -H "Authorization: Bearer <token>" \
  "<dev-gateway>/innov/v1/events/<eventId>/relations"

# stats
curl -s -H "Authorization: Bearer <token>" \
  "<dev-gateway>/innov/v1/events/stats?granularity=month&compare=ranges"
```

P95 采样：对上述 geo/heatmap 各跑 ≥20 次，记录 P95。

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| D1 算法只在 Python | ✅ 本任务仅验 Java REST 契约 |
| D2 调用链 前端→Java→Python | ✅ §1 均为 Java 查 ADS |
| D5 CI/CD | 🟡 curl/P95 deferred |
| D9 数据血缘 | N/A（接口测试层；指标 ⓘ 由前端 L07 验收） |

## 下一任务

- **L06** api-agent：`GET /dict/event-types` 与前端图例对齐（depends_on L05 ✅ 用例矩阵已交付）
- **L10** coordinator + qa：本报告全部 DEFERRED 项补验 + M1 里程碑签收

## Commit

- message：`[agent:qa-agent] E-INNOV-M1-L05 M1 events API test report (deferred L10)`

---

*handoff · qa-agent · E-INNOV-M1-L05*
