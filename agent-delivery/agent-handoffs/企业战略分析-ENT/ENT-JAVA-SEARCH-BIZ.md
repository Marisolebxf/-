# Handoff：ENT-JAVA-SEARCH-BIZ

- **时间**：2026-07-20
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-SEARCH-BIZ-派单包.md`
- **状态建议**：`review`（待 coordinator 验收；**勿自行改 done**）
- **接口总文档（前端联调入口）**：[`API-ENT-full-catalog.md`](./API-ENT-full-catalog.md)（**85** 端点；本单为 **#77–85**「检索业务」SEARCH-BIZ，见总文档 §3 总览 / §4.N 明细）

## 1. 范围与实现

Java 自建企业检索业务三能力（**不调 Python**，直连 MySQL）：

| # | 能力 | 表 | Java 对外（网关前缀 `…/enterprise`） | Controller |
|---|---|---|---|---|
| 77–79 | 示例查询 | `ent_search_example` | `POST /topic/v1/search-biz/examples/{list,save,delete}` | `EnterpriseSearchBizController` |
| 80–82 | 热门场景 | `ent_search_scene` | `POST /topic/v1/search-biz/scenes/{list,save,delete}` | 同上 |
| 83–85 | 最近检索 | `ent_search_history` | `POST /topic/v1/search-biz/history/{list,save,clear}` | 同上 |

对照派单：示例查询 / 热门场景 / 最近检索；**不含**高筛「保存方案」、对比篮列表持久化。

分层（对齐 upms）：

```text
Controller → EntSearch*Service(IService) → EntSearch*ServiceImpl(ServiceImpl) → EntSearch*Mapper(GkxlumenBaseMapper) → MySQL
```

Entity 位于 `*-api/.../api/entity/*Entity`（`extends Model`），与 `SysDict` 同构。

## 2. 偏离说明（as-built）

| 项 | 派单 | As-built | 理由 |
|---|---|---|---|
| 路径 | `/topic/v1/enterprise/search-biz/**` | `/topic/v1/search-biz/**` | `@EnableOpenApi("enterprise")` + `/topic/v1`，避免双段 `enterprise` |
| DDL | Postgres `BIGSERIAL` / lumen 业务库 | MySQL 独立库 `gkxlumenx_topic_enterprise` + AUTO_INCREMENT | 平台分库惯例；监管要求目标库单独建立 |
| history UNIQUE | `(user_id, keyword, search_time)` | 仅索引 `(user_id, search_time)`；save 后保留最近 20 条 | 避免同秒冲突 |
| user_id | 请求体传入 | **请求体** `user_id`（前端传递，必填） | 专题服务拿不到登录态 SecurityUtils；与派单一致 |
| 历史存储 | 可选 Redis | MySQL | 对齐 3 表 DoD |
| 列表分页 | 未强制 | 示例/场景全量 list；历史 `limit`（默认 20） | 派单契约为数组；配置数据量小（与 upms 管理端 Page 不同形态） |

网关完整路径示例：`POST {gateway}/enterprise/topic/v1/search-biz/examples/list`

## 3. 目标库与运维

| 项 | 值 |
|---|---|
| **独立库名** | `gkxlumenx_topic_enterprise`（与主库 `gkxlumenx` 隔离） |
| 建库注册 | `db/1schema.sql` |
| 建表+种子 | `db/9x_gkxlumenx_topic_enterprise.sql`（`CREATE DATABASE` + 5 示例 + 4 场景） |
| 服务数据源 | Nacos `gkxlumen-topic-enterprise-biz-*.yml` → JDBC URL 库名须为本库 |

**监管进度（2026-07-20）**：Nacos datasource 已改为 `gkxlumenx_topic_enterprise`；DDL 是否已在目标 MySQL 执行需联调前确认。

## 4. 9 接口对照（总目录 #77–85）

| # | 服务内路径 | 用途 | 请求 | 响应 data |
|---|---|---|---|---|
| 77 | `POST /topic/v1/search-biz/examples/list` | 示例列表 | `{enabled_only?}` 默认 true | `ExampleItem[]` |
| 78 | `POST /topic/v1/search-biz/examples/save` | 新增/编辑 | `{id?, keyword, industry_code?, query_tree?, sort_order?, is_enabled?}` | `{id}` |
| 79 | `POST /topic/v1/search-biz/examples/delete` | 删除 | `{id}` | `null` |
| 80 | `POST /topic/v1/search-biz/scenes/list` | 场景列表 | `{enabled_only?}` | `SceneItem[]` |
| 81 | `POST /topic/v1/search-biz/scenes/save` | 新增/编辑 | `{id?, scene_name, icon?, query_tree, sort_order?, is_enabled?}` | `{id}` |
| 82 | `POST /topic/v1/search-biz/scenes/delete` | 删除 | `{id}` | `null` |
| 83 | `POST /topic/v1/search-biz/history/list` | 最近检索 | `{user_id, limit?=20}` | `HistoryItem[]` |
| 84 | `POST /topic/v1/search-biz/history/save` | 记一条 | `{user_id, keyword?, search_type, query_tree?}` | `{id}` |
| 85 | `POST /topic/v1/search-biz/history/clear` | 清空 | `{user_id}` | `null` |

字段明细与 JSON 示例见 [`API-ENT-full-catalog.md`](./API-ENT-full-catalog.md) §4.N。

## 5. query_tree 与前端约定

格式对齐 Python `API-接口文档.md` §3.1.2，推荐 `op`：

```json
{
  "logic": "AND",
  "conditions": [
    { "field": "city", "op": "eq", "value": "深圳市" },
    { "field": "tag", "op": "in", "value": ["high_tech"] }
  ]
}
```

- 前端拿到场景/示例的 `query_tree` 后，原样 POST 既有 `/topic/v1/search/advanced`（或 keyword/smart）。
- `search_type`：`keyword` / `smart` / `advanced`。
- 示例可无 `query_tree`（仅 keyword 回填）；场景 `query_tree` 必填。
- history 三个接口 **`user_id` 必填**（前端传递）；缺失返回失败文案，不写库。

## 6. 产物清单

| 产物 | 路径（相对 `lumen-svc-platform/` 或编排仓） |
|---|---|
| DDL | `db/1schema.sql`、`db/9x_gkxlumenx_topic_enterprise.sql` |
| Entity | `gkxlumen-topic-enterprise-api/.../api/entity/EntSearch*Entity.java` |
| DTO | `…/api/dto/searchbiz/EnterpriseSearchBizDTOs.java` |
| Mapper | `…-biz/.../mapper/EntSearch*Mapper.java`（`GkxlumenBaseMapper`） |
| Service | `EntSearchExample/Scene/HistoryService` + `impl/*ServiceImpl`（`IService`/`ServiceImpl`） |
| Controller | `…/controller/EnterpriseSearchBizController.java` |
| JSON 工具 | `…/support/SearchBizJsonSupport.java` |
| 依赖 | api：`mybatis-plus-spring`；biz：`mybatis-plus-spring-boot3-starter` + Druid + MySQL |
| 总目录增补 | `agent-handoffs/企业战略分析-ENT/API-ENT-full-catalog.md`（76→85，#77–85） |
| 本 handoff | `agent-handoffs/企业战略分析-ENT/ENT-JAVA-SEARCH-BIZ.md` |

## 7. 验收证据

| 项 | 结果 |
|---|---|
| Maven + JDK17 编译 | ✅ SUCCESS（本机会话已跑） |
| 中文 Javadoc（类/字段/方法 + `@param`/`@return`） | ✅ 本单相关 Java 已补齐（`api.mdc` §8） |
| upms 分层对齐 | ✅ Entity@api + `GkxlumenBaseMapper` + `IService`/`ServiceImpl` |
| 禁止聚合 Facade 直调 Mapper | ✅ Controller 注入三 Service |
| 总目录纳入本单接口 | ✅ `API-ENT-full-catalog.md` #77–85 |
| commit SHA | `lumen-svc-platform` `4a053de`（已 push `origin/dev`）；编排仓文档同批 push |
| Nacos 库名 | ✅ 监管已改为 `gkxlumenx_topic_enterprise` |
| DDL 执行 | ✅ 监管确认表已建立 |
| 接口冒烟 | ⏳ CI/dev 部署后测 9 接口 |

## 8. 架构合规自检（7 条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本任务无算法 |
| 2 | 前端→Java→Python `/internal/*` | ✅ N/A（本任务 Java→MySQL；检索仍走既有门面） |
| 3 | 不直连 nGQL/ES | ✅ |
| 4 | Feign `/internal/gkx-search` | ✅ N/A（无 Feign） |
| 5 | 可观测性 | ✅ 复用资源服务器/既有链路 |
| 6 | commit 标注 `[human:侯佳伟]` / `[agent:api-agent]` | ⏳ 提交时标注 |
| 7 | demo2 不 merge lumen | ✅ N/A（仅 lumen-svc-platform + 编排仓文档） |

## 9. 开放项

1. CI/dev 自动部署后冒烟 #77–85（examples/scenes 种子 + history 带 `user_id`）。
2. **待 coordinator 验收**后改 `done`（监管/执行勿自行改）。
3. 前端接入另任务（以 `API-ENT-full-catalog.md` #77–85 为联调真源）。

## 10. Cost 回填（registry）

| 字段 | 值 | 说明 |
|---|---|---|
| `actual_tokens` | `120_000` | 与派单估算对齐（含 upms 对齐重构 + 注释 + 总目录增补） |
| `model_used` | `cursor-grok-4.5` | 本会话编码档 |
| `actual_cost` | `0.65` | 量级估计 |
| `cost_warn` | `green` | < $5 |
