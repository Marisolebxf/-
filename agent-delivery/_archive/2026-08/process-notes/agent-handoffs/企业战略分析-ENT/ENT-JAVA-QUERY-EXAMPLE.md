# ENT-JAVA-QUERY-EXAMPLE — 查企业企业名示例 CRUD

- **日期**：2026-08-04
- **执行**：`human:侯佳伟`
- **仓**：`lumen-svc-platform` / `gkxlumen-topic-enterprise`
- **库**：`gkxlumenx_topic_enterprise`（表 `ent_query_example`）

## 1. 与智能搜索示例对照

| 项 | 智能搜索（既有） | 查企业（本单） |
|---|---|---|
| 表 | `ent_search_example` | `ent_query_example` |
| 路径 | `/topic/v1/search-biz/examples/**` | `/topic/v1/query-examples/**` |
| 网关 | `/enterprise/topic/v1/search-biz/examples/**` | `/enterprise/topic/v1/query-examples/**` |
| 语义 | 产业/技术词 chip | 企业名 chip（小米/华为等） |
| catalog | #77–79 | #139–141 |

## 2. 接口

1. `POST /topic/v1/query-examples/list`
2. `POST /topic/v1/query-examples/save`
3. `POST /topic/v1/query-examples/delete`

## 3. 代码落点

- Entity：`api/entity/EntQueryExampleEntity.java`
- DTO：`api/dto/queryexample/EnterpriseQueryExampleDTOs.java`
- Controller：`controller/queryexample/EnterpriseQueryExampleController.java`
- Service：`service/queryexample/**`
- Mapper：`mapper/EntQueryExampleMapper.java`
- DDL：`db/9x_gkxlumenx_topic_enterprise_ent_query_example.sql`（主脚本文末已同步）

## 4. 种子

小米、华为、比亚迪、腾讯、大疆、中兴（`org_id` 可空，按 keyword 幂等插入）。

## 5. 部署注意

目标库执行增量 SQL 后再发版；前端查企业页调 `query-examples/list`，勿复用 `search-biz/examples`。

## 6. 提交

- `lumen-svc-platform@b85a419` — `feat(topic-enterprise): 查企业企业名示例 CRUD（ent_query_example）[human:侯佳伟]`（已 push `origin/dev`）
