# Evidence · Java/FE 联调盘点（L04 附属）

日期：2026-07-28

## Java 超时

| 仓 | 变更 | SHA（本地 dev） |
|----|------|-----------------|
| demo-svc-platform | Feign `readTimeout` + `read-timeout-ms` → 120000 | `d8f2456` |
| lumen-svc-platform | `application-tech-news.yml` `read-timeout-ms` → 120000 | `59d9f6c` |

透传：`TechNewsExtractService` 返回 Python 完整 Map（含 `error`），门控 HTTP 200 可到达前端。

## 前端（lumen-ui-science-pc `origin/dev`）

- 已有页：`src/views/tech-news/index.vue`
- 已识别 `payload.error` 并 Alert
- **缺口**：门控仍走 error 语气；`impact ?? 'null'` 字面量

## 建议

1. push 上述两仓 timeout commit  
2. 开前端 L05：gate warning + impact 空文案
