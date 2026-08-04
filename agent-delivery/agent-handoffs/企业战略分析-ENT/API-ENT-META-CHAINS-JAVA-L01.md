# API-ENT-META-CHAINS-JAVA-L01 — Java 透传工单（java-agent）

> **task-id**：`API-ENT-META-CHAINS-JAVA-L01`（task-registry / 飞书看板真源）  
> 派单：`[agent:data-agent]` → **api-agent**（监管 `human:侯佳伟`，`claim_type=coordinator_dispatch`）  
> 日期：2026-08-04  
> 仓：`lumen-svc-platform` / `gkxlumen-topic-enterprise`  
> 分支：`origin/dev`（禁止动 main）  
> GitLab Issue：https://gitlab.htmisoft.net/gkx-lumen/lumen-svc-platform/-/issues/1  
> **禁止范围外改动**：本工单仅补产业链字典透传；Python 侧已就绪

---

## 1. 背景

前端「重点企业分析 / 深圳企业现状」需要**产业链**下拉词典。  
Python 已新增：

`POST /internal/gkx-search/meta/chains` → `{ items: [{code, name}] }`

昨日拆出的 DIM 独立字典（industries/regions/tags/…）**Java 门面已有**，但前端缺一份统一契约说明（见同目录 `API-ENT-META-DICT-FRONTEND.md`）。  
本工单只补 **仍缺的** `/meta/chains` 透传。

---

## 2. DoD

1. Feign：`RemoteEnterprisePythonClient` 增加  
   `POST /internal/gkx-search/meta/chains`
2. Controller：`EnterpriseOpenApiController` 增加  
   `POST /topic/v1/search/meta/chains`（`@Inner(false)`，风格对齐 `industries`）
3. DTO：
   - Request：可空 `EnterpriseMetaRequest` 或新建 `EnterpriseChainRequest`（字段 `keyword` 可选）
   - Response：`{ items: List<{code, name}> }`（可用 `OptionsResponse` 若已有 `code/name`；否则新建 `ChainsResponse`）
4. RemoteTopicEnterpriseService（api 模块）同步声明，供网关/其它服务发现
5. snake_case 入参透传，不改 Python 字段名
6. 本地/联调：网关  
   `POST /api/enterprise/topic/v1/search/meta/chains` + `{}` → `code=0` 且 `items` 非空（或兜底清单）
7. handoff 回写本文件 §5 + commit `[agent:java-agent]`

---

## 3. 参考实现（对齐 industries）

现成路径可抄：

- Feign：`RemoteEnterprisePythonClient#industries`
- Controller：`EnterpriseOpenApiController#industries`
- Service：`EnterpriseOpenApiServiceImpl#industries`

契约样例见 `API-ENT-META-DICT-FRONTEND.md` §2。

---

## 4. 非目标

- 不改 Python
- 不改 `/hot` 语义、不把热词改成企业列表
- 不重复实现 industries/regions 等已透传字典

---

## 5. 验收留空（java-agent 填）

- [ ] Feign / Controller / DTO 已合入 `dev`
- [ ] 联调 URL：
- [ ] 响应摘录：
- [ ] commit：
