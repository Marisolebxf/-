# 开放项 2 · 联调 / 烟测证据

- 采集说明见同目录 `02-smoke-evidence.json`
- Python（本地 `:8000`）：`POST /internal/tech-news/extract` + `GET /extractions` → HTTP 200
- Java HttpClient 契约烟测（复刻 lumen RestTemplate）：此前 `TechNewsJavaFacadeSmoke` **SMOKE_PASS**
- 完整 Spring Boot + 网关在线：本机 `192.168.88.50:9999` / `127.0.0.1:9999` **不可达**；配置层已确认 `/innov/**` 覆盖 tech-news
- UI 页面截图：依赖登录态 + 网关，本会话以 JSON 响应作为联调证据替代；监管人可在网关恢复后补截图
