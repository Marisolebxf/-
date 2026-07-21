# Handoff：ENT-JAVA-FILTER-TEMPLATE

- **时间**：2026-07-21
- **执行**：agent:api-agent（监管：human:侯佳伟）
- **仓库 / 分支**：`lumen-svc-platform` / `dev`
- **派单包**：`ENT-JAVA-FILTER-TEMPLATE-派单包.md`
- **状态建议**：`review`（待 coordinator 验收；**勿自行改 done**）
- **接口总文档**：[`API-ENT-full-catalog.md`](./API-ENT-full-catalog.md)（**90** 端点；本单 **#86–90**）

## 1. 范围与实现

Java 自建高级筛选模板 CRUD（**不调 Python**，直连 MySQL `gkxlumenx_topic_enterprise`）：

| # | 服务内路径 | 用途 |
|---|---|---|
| 86 | `POST /topic/v1/filter-template/list` | 当前用户模板列表 |
| 87 | `POST /topic/v1/filter-template/save` | 新增/编辑（每用户 ≤50；默认互斥） |
| 88 | `POST /topic/v1/filter-template/delete` | 删除（归属校验） |
| 89 | `POST /topic/v1/filter-template/get` | 详情（归属校验） |
| 90 | `POST /topic/v1/filter-template/set-default` | 设默认（事务互斥） |

分层（对齐 upms / SEARCH-BIZ）：

```text
Controller → EntFilterTemplateService(IService) → ServiceImpl → Mapper(GkxlumenBaseMapper) → MySQL
```

Entity：`*-api/.../api/entity/EntFilterTemplateEntity`（`extends Model`）。

## 2. 偏离说明（as-built）

| 项 | 派单 | As-built | 理由 |
|---|---|---|---|
| 路径 | `/topic/v1/enterprise/filter-template/**` | `/topic/v1/filter-template/**` | `@EnableOpenApi("enterprise")` 避免双段 `enterprise`（api.mdc §9） |
| DDL | Postgres `BIGSERIAL` / lumen 业务库 | MySQL 独立库 `gkxlumenx_topic_enterprise` + `CREATE TABLE IF NOT EXISTS` | 对齐 SEARCH-BIZ 分库惯例 |
| HTTP | 未强制 | 全 `POST` + JSON | 对齐 SEARCH-BIZ / 企业门面惯例 |
| `user_id` | 请求体 | **请求体必填**（前端传递） | 专题服务无登录态 SecurityUtils |

网关完整路径示例：`POST {gateway}/enterprise/topic/v1/filter-template/list`

## 3. query_tree 与前端约定

格式对齐 Python `API-接口文档.md` 高筛 / §3.1.2，例如：

```json
{
  "logic": "AND",
  "conditions": [
    { "field": "city", "op": "eq", "value": "深圳市" },
    { "field": "tag", "op": "in", "value": ["high_tech"] }
  ]
}
```

前端加载模板后可将 `query_tree` **原样** POST `/topic/v1/search/advanced`，无需二次转换。

## 4. 产物清单

| 产物 | 路径 |
|---|---|
| DDL | `db/9x_gkxlumenx_topic_enterprise.sql`（`ent_filter_template`） |
| Entity | `…/api/entity/EntFilterTemplateEntity.java` |
| DTO | `…/api/dto/filtertemplate/EnterpriseFilterTemplateDTOs.java` |
| Mapper/Service/Controller | `EntFilterTemplateMapper` / `EntFilterTemplateService(+Impl)` / `EnterpriseFilterTemplateController` |
| 总目录 | `API-ENT-full-catalog.md`（85→90，#86–90） |
| 本 handoff | `ENT-JAVA-FILTER-TEMPLATE.md` |

## 5. 验收证据

| 项 | 结果 |
|---|---|
| Maven + JDK17 编译 | ✅ `mvn -pl gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz -am compile -DskipTests` SUCCESS |
| 中文 Javadoc | ✅ 本单相关类/字段/方法已补 |
| 用户隔离 + 默认互斥 + 上限 50 | ✅ Service 实现 |
| upms 分层 | ✅ Entity@api + GkxlumenBaseMapper + IService/ServiceImpl |
| 代码 SHA | 待 push 后回填（工作区未 commit 时以本地变更为准） |
| DDL 执行 | ⏳ 需在目标库执行 `CREATE TABLE IF NOT EXISTS ent_filter_template`（或重跑脚本增量段） |
| 接口冒烟 | ⏳ CI/dev 部署后测 5 接口 |

## 6. 架构合规自检（7 条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 本单无算法 |
| 2 | 调用链前端→Java→Python | ✅ 本单不调 Python（用户配置 CRUD） |
| 3 | 图谱 NebulaGraph | N/A |
| 4 | 可观测性 | ✅ 沿用服务 OTel Agent |
| 5 | CI/CD | ✅ push 后走 Pipeline |
| 6 | demo2 不 merge lumen | ✅ 仅改 lumen-svc-platform |
| 7 | 方案 A / 独立 Controller | ✅ 新建 `EnterpriseFilterTemplateController`，未改 OpenApiController |

## 7. cost 四字段（预估回填）

| 字段 | 值 |
|---|---|
| `actual_tokens` | ~80_000（会话级估计） |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | <$5（估计） |
| `cost_warn` | false |

## 8. 开放项

1. 目标 MySQL 执行 DDL（独立库已存在则只建表）
2. coordinator 验收后改 `done`
3. 前端联调另开任务
