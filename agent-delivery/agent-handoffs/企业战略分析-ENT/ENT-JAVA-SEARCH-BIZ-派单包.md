# 企业检索业务功能派单包（ENT-JAVA-SEARCH-BIZ）

- **派单方**：architect-agent + coordinator
- **时间**：2026-07-20
- **下游 agent**：api-agent（Java 侧实现）
- **监管人**：human:侯佳伟
- **仓库**：`lumen-svc-platform`（分支 `dev`）

## 1. 背景

原型图企业检索首页左侧搜索区下方有三个业务功能，属于**交互/运营层**，不在 Python 基础数据接口范围内，需 Java 侧自建表 + 自实现接口，并与前端约定字段。

| 功能 | 说明 | 数据性质 |
|---|---|---|
| **示例查询** | 首页预设的几个查询词/产业标签（如"人工智能""集成电路"），点击直接触发对应搜索 | 运营配置，半静态 |
| **热门场景** | 运营配置的高频场景入口，点击跳转带预设条件的检索 | 运营配置，半静态 |
| **最近检索** | 当前用户的搜索历史，按用户维度展示最近 N 条 | 用户行为数据，动态 |

**这三个功能不依赖 Python `/internal/gkx-search/**`**，Java 独立建表 + CRUD。

## 2. 建议表结构（Java 侧自建，放 lumen 业务库）

### 2.1 示例查询配置表 `ent_search_example`

```sql
CREATE TABLE ent_search_example (
  id          BIGSERIAL PRIMARY KEY,
  keyword     VARCHAR(100) NOT NULL,          -- 示例词，如"人工智能"
  industry_code VARCHAR(50),                  -- 关联产业 code（可选，点击时带入高筛）
  query_tree  TEXT,                           -- 预设查询条件 JSON（可选，高级筛选用）
  sort_order  INT NOT NULL DEFAULT 0,         -- 排序
  is_enabled  SMALLINT NOT NULL DEFAULT 1,    -- 1启用 0停用
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE ent_search_example IS '企业检索-示例查询配置';
```

### 2.2 热门场景配置表 `ent_search_scene`

```sql
CREATE TABLE ent_search_scene (
  id           BIGSERIAL PRIMARY KEY,
  scene_name   VARCHAR(100) NOT NULL,         -- 场景名，如"深圳头部科技企业"
  icon         VARCHAR(255),                  -- 图标 URL 或 icon name
  query_tree   TEXT NOT NULL,                 -- 预设查询条件 JSON（点击跳转带此条件）
  sort_order   INT NOT NULL DEFAULT 0,
  is_enabled   SMALLINT NOT NULL DEFAULT 1,
  create_time  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  update_time  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE ent_search_scene IS '企业检索-热门场景配置';
```

### 2.3 用户搜索历史表 `ent_search_history`

```sql
CREATE TABLE ent_search_history (
  id           BIGSERIAL PRIMARY KEY,
  user_id      VARCHAR(64) NOT NULL,          -- 用户 ID
  keyword      VARCHAR(200),                  -- 搜索关键词（关键词搜索时记）
  search_type  VARCHAR(20) NOT NULL,          -- keyword / smart / advanced
  query_tree   TEXT,                          -- 完整查询条件 JSON（高级筛选时记）
  search_time  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uk_user_keyword_time UNIQUE (user_id, keyword, search_time)
);
CREATE INDEX idx_ent_search_history_user ON ent_search_history(user_id, search_time DESC);
COMMENT ON TABLE ent_search_history IS '企业检索-用户搜索历史';
```

> 最近检索也可考虑走 Redis 缓存（ZSet 按时间排序，限 20 条），减轻 DB 压力。Java agent 可自行选择方案，但需在 handoff 中说明选型理由。

## 3. 接口设计建议

Java 对外路径统一 `/topic/v1/enterprise/search-biz/**`，POST + JSON body。

| # | Java 对外路径 | 用途 | 请求 | 响应 |
|---|---|---|---|---|
| 1 | `/search-biz/examples/list` | 示例查询列表 | `{enabled_only?: bool}` | `[{id, keyword, industry_code, query_tree, sort_order}]` |
| 2 | `/search-biz/examples/save` | 新增/编辑示例 | `{id?, keyword, industry_code?, query_tree?, sort_order, is_enabled}` | `{id}` |
| 3 | `/search-biz/examples/delete` | 删除示例 | `{id}` | `{}` |
| 4 | `/search-biz/scenes/list` | 热门场景列表 | `{enabled_only?: bool}` | `[{id, scene_name, icon, query_tree, sort_order}]` |
| 5 | `/search-biz/scenes/save` | 新增/编辑场景 | `{id?, scene_name, icon, query_tree, sort_order, is_enabled}` | `{id}` |
| 6 | `/search-biz/scenes/delete` | 删除场景 | `{id}` | `{}` |
| 7 | `/search-biz/history/list` | 最近检索 | `{user_id, limit?: int=20}` | `[{id, keyword, search_type, query_tree, search_time}]` |
| 8 | `/search-biz/history/save` | 记录一次搜索 | `{user_id, keyword?, search_type, query_tree?}` | `{id}` |
| 9 | `/search-biz/history/clear` | 清空历史 | `{user_id}` | `{}` |

## 4. 与前端的约定要点（handoff 中必须写明）

1. **示例查询/热门场景**的 `query_tree` 字段格式，必须与高级筛选的 `query_tree`（Python 侧 `/enterprises/advanced` 接受的格式）**完全一致**，前端拿到后直接透传给 `/search/advanced`，无需二次转换
2. **最近检索**的 `search_type` 枚举：`keyword`（关键词搜索）/ `smart`（智能搜索）/ `advanced`（高级筛选）
3. 示例查询和热门场景的**管理后台接口**（save/delete）本期是否实现？如前端仅需 list，可只做 list + 表初始化数据，管理接口留到后台管理模块

## 5. 架构铁律

1. Java 只做 CRUD + 配置管理，不写算法
2. 这三个功能不调 Python，Java 直连自己的业务库
3. `query_tree` 格式与 Python 高筛接口对齐（字段名/操作符/树结构）
4. commit 标注 `[agent:api-agent]`
5. OTel instrumentation 必加

## 6. DoD

- 3 张表 DDL（放 `lumen-svc-platform` 的 `db/` 或 flyway migration）
- 9 个接口三层齐全（Controller→Service→Mapper）
- `query_tree` 格式与 Python 高筛接口对齐，handoff 中附对照说明
- 与前端字段约定文档（handoff 内含）
- 本地 Maven+JDK17 编译通过
- handoff：`agent-handoffs/企业战略分析-ENT/ENT-JAVA-SEARCH-BIZ.md`
  含表结构 + 接口对照表 + commit SHA + 架构合规自检 + cost 四字段

## 7. 依赖

- 无硬依赖（不依赖 Python 接口）
- 软依赖：`ENT-ARCH-API-CONTRACT`（复用其 Controller/Service 分层范式）

## 8. 预估

- effort_points: 3
- difficulty: S
- estimated_tokens: 120_000
