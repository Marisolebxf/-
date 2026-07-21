# 高级筛选模板派单包（ENT-JAVA-FILTER-TEMPLATE）

- **派单方**：architect-agent + coordinator
- **时间**：2026-07-21
- **下游 agent**：api-agent（Java 侧实现）
- **监管人**：human:侯佳伟
- **仓库**：`lumen-svc-platform`（分支 `dev`）

## 1. 背景

原型图高级筛选面板右上角有"保存为模板"功能：用户配好一组高级筛选条件（query_tree）后，可存成命名模板，下次直接加载使用。这属于**用户个性化配置层**，不在 Python 基础数据接口范围内，需 Java 侧自建表 + 自实现接口。

与 `ENT-JAVA-SEARCH-BIZ`（示例查询/热门场景）的区别：
- 示例查询/热门场景 = **运营配置**（全用户共享，后台维护）
- 高筛模板 = **用户个人配置**（按用户隔离，用户自己保存/管理）

## 2. 建议表结构（Java 侧自建，放 lumen 业务库）

```sql
CREATE TABLE ent_filter_template (
  id           BIGSERIAL PRIMARY KEY,
  template_name VARCHAR(100) NOT NULL,        -- 模板名，用户自定义
  user_id      VARCHAR(64) NOT NULL,          -- 所属用户
  query_tree   TEXT NOT NULL,                 -- 高筛查询条件 JSON（与 Python /enterprises/advanced 的 query_tree 格式完全一致）
  description  VARCHAR(500),                  -- 模板描述（可选）
  is_default   SMALLINT NOT NULL DEFAULT 0,   -- 是否默认模板（每用户最多 1 个）
  sort_order   INT NOT NULL DEFAULT 0,
  create_time  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_ent_filter_template_user ON ent_filter_template(user_id, sort_order);
COMMENT ON TABLE ent_filter_template IS '企业检索-高级筛选模板（用户个人配置）';
```

## 3. 接口设计

Java 对外路径统一 `/topic/v1/enterprise/filter-template/**`，POST + JSON body。

| # | Java 对外路径 | 用途 | 请求 | 响应 |
|---|---|---|---|---|
| 1 | `/filter-template/list` | 当前用户的模板列表 | `{user_id}` | `[{id, template_name, query_tree, description, is_default, sort_order, update_time}]` |
| 2 | `/filter-template/save` | 新增/编辑模板 | `{id?, template_name, user_id, query_tree, description?, is_default?, sort_order?}` | `{id}` |
| 3 | `/filter-template/delete` | 删除模板 | `{id, user_id}` | `{}` |
| 4 | `/filter-template/get` | 获取单个模板详情 | `{id, user_id}` | `{id, template_name, query_tree, description, is_default, sort_order, create_time, update_time}` |
| 5 | `/filter-template/set-default` | 设为默认模板 | `{id, user_id}` | `{}` |

共 5 个接口。

## 4. 关键设计约束

1. **`query_tree` 格式必须与 Python 高筛 `/internal/gkx-search/enterprises/advanced` 完全一致**——前端拿到模板的 `query_tree` 后直接透传给 `/search/advanced`，无需二次转换。格式参考 `repos/demo-svc-topic-py/docs/API-接口文档.md` §5.4
2. **用户隔离**：list/get/delete/set-default 必须校验 `user_id`，禁止越权访问他人模板
3. **默认模板**：每用户最多 1 个 `is_default=1`，set-default 时需先把该用户其他模板的 is_default 清零（事务）
4. **模板数量上限**：建议每用户最多 50 个模板，超出时 save 返回错误提示

## 5. 架构铁律

1. Java 只做 CRUD，不写算法
2. 不调 Python，Java 直连业务库
3. `query_tree` 格式与 Python 高筛接口对齐
4. commit 标注 `[agent:api-agent]`
5. OTel instrumentation 必加
6. 用户隔离校验必做（安全）

## 6. DoD

- 1 张表 DDL（lumen 业务库 migration）
- 5 个接口三层齐全（Controller→Service→Mapper）
- `query_tree` 格式与 Python 高筛接口对齐，handoff 附对照说明
- 用户隔离校验（list/get/delete/set-default 均校验 user_id）
- 默认模板互斥逻辑（事务）
- 本地 Maven+JDK17 编译通过
- handoff：`agent-handoffs/企业战略分析-ENT/ENT-JAVA-FILTER-TEMPLATE.md`
  含表结构 + 接口对照表 + commit SHA + 架构合规自检 7 条 + cost 四字段

## 7. 依赖

- 无硬依赖（不依赖 Python 接口）
- 软依赖：`ENT-ARCH-API-CONTRACT`（复用其 Controller/Service 分层范式）
- 与 `ENT-JAVA-SEARCH-BIZ` 无冲突（不同表、不同 Controller，可并行）

## 8. 预估

- effort_points: 2
- difficulty: S
- estimated_tokens: 80_000

## 9. Convoy 分文件约束

- 新增独立 Controller：`EnterpriseFilterTemplateController.java`
- 新增独立 Service/Mapper：`EntFilterTemplateService.java` + `EntFilterTemplateMapper.java`
- 禁止修改已有的 `EnterpriseOpenApiController.java` 等文件
