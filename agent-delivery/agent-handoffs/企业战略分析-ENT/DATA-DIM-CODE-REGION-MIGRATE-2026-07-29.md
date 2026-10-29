# DATA · code_region 迁入 MySQL DIM（2026-07-29）

- **监管**：`human:淮政玮`
- **执行**：`agent:data-agent`
- **目标表**：`gkxlumenx_dim.code_region`
- **源**：PostgreSQL `demo_gdf_data.dim.admin_division`（**PG 无 `code_region` 表**；与 innov 侧 `gkxlumenx_dim.admin_division` 同源）

## 做了什么

1. 在 MySQL `10.50.11.76` 创建 `gkxlumenx_dim.code_region`（DDL：`agent-delivery/data/ddl/gkxlumenx_dim_code_region.sql`）
2. 从 PG `dim.admin_division` 映射灌入 **11** 行（`parent_code IS NULL` → `parent='0'`；`lng,lat` → `lnglat`）
3. 更新 `demo-svc-topic-py`：
   - `gkx_search_service/views/meta.py` SQL → `gkxlumenx_dim.code_region`
   - `gkx_common/mock.py` / `docs/API-接口文档.md` 数据源说明
4. 编排文档：DWD 设计 changelog、本 handoff、DDL 落盘

## 字段映射

| PG `dim.admin_division` | MySQL `gkxlumenx_dim.code_region` |
|---|---|
| `admin_code` | `code` |
| `parent_code`（NULL→`0`） | `parent` |
| `name` | `name` / `fulltitle` |
| `level` (smallint) | `level` (varchar) |
| `center_lng` + `center_lat` | `lnglat`（`lng,lat`） |
| — | `zipcode` / `tel` / `area` / `people`（空） |

## 验证

```text
SHOW TABLES FROM gkxlumenx_dim LIKE 'code_region';  -- 有
SELECT COUNT(*) FROM gkxlumenx_dim.code_region;     -- 11
SELECT * FROM gkxlumenx_dim.code_region WHERE parent='0';  -- 100000 中国
SELECT * FROM gkxlumenx_dim.code_region WHERE parent='100000'; -- 10 城
```

## 开放项

1. 当前种子仅为 innov 样例 11 行（中国 + 若干城市），**不是完整省市区国标树**；全国树需另开灌数任务。
2. 与 `gkxlumenx_dim.admin_division` 并存：后者保留 innov 原契约；企业检索 `/meta/regions` 读 `code_region`。
3. topic-py 代码改动待监管人确认后 commit / push `demo-svc-topic-py`。
