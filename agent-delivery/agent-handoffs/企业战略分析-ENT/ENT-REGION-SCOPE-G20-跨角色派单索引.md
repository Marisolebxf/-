# 企业区位 G20 · 跨角色派单索引

> 日期：2026-08-11  
> 用途：统一说明地区树、ES、Python、Java、前端之间的任务边界，避免把数据、算法适配、Java 透传和 UI 取码混成一张单。  
> 当前动作：两张新单已建为 `backlog` 并已推送归档，待人工审阅；未认领、未派发。

## 1. 任务总览

| 顺序 | Task ID | 角色/仓 | 内容边界 | 当前状态 |
|---:|---|---|---|---|
| 1 | `DATA-ENT-CODE-COUNTRY-APPLY-L01` | data-agent / agent-delivery | `code_country`、G20 国家/城市树 L04/L05 落库 | `ready_to_sign` |
| 2 | `FIX-TOPIC-ES-TEXT-ANALYZER-L01` | data-agent / lumen-etl-es-py | ES analyzer + `country_code`/`city_code` mapping | `pending_test` |
| 3 | `PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01` | data-agent / demo-svc-topic-py | key-analysis 三分 OR | `ready_to_sign` |
| 4 | `PY-ENT-RECOMMEND-GEO-COUNTRY-L01` | data-agent / demo-svc-topic-py + lumen-algo-py | Python 适配层解析 ES 候选；算法消费候选 ID | `ready_to_sign` |
| 5 | `API-ENT-REGION-SCOPE-G20-COUNTRY-L01` | api-agent / lumen-svc-platform | `bind_country_code`、key-analysis 三数组 DTO、recommend 透传回归 | `backlog`（新建，待审） |
| 6 | `FE-ENT-REGION-SCOPE-G20-COUNTRY-L01` | frontend-agent / lumen-ui-topic | Cascader 保留 bind、三分取码、key-analysis/recommend 接线 | `backlog`（新建，待审） |

## 2. 不再重复建的任务

### 2.1 不新建 algorithm-agent 实现单

`PY-ENT-RECOMMEND-GEO-COUNTRY-L01` 已包含两段已完成实现：

- `demo-svc-topic-py`：按三类区位条件查询 ES，解析候选企业 ID；
- `lumen-algo-py`：消费 `geo_enterprise_codes`，并与其他推荐条件做 AND。

算法服务不负责读取 ES 或解释地区树。再建一张“算法做 ES 区位过滤”单会违反架构边界；再建一张同内容实现单会重复已完成工作。后续由 QA 在现有任务流验证，不倒填历史认领。

### 2.2 不重开既有大包

- `API-ENT-DICT-JAVA-L04`：只负责原 meta Facade，G20 增量另列 API L01；
- `FE-ENT-META-DICT-SCENE-WIRE`：负责 chains/tags/场景裁剪/全国 path，G20 三分取码另列 FE L01；
- `PY-ENT-KEYANALYSIS-RECOMMEND-COUNTRY-派单包.md`：保留为已执行的 Python 契约包，不再混入 Java/前端实现。

## 3. 依赖关系

```text
DATA L01 ─┐
ES FIX ───┼─→ Python key-analysis / recommend ─→ API G20 L01 ─→ FE G20 L01
API L04 ──┤                                      ↑
KEYENT JAVA L01 ─────────────────────────────────┘（API DTO 同文件串行前置）
FE META WIRE ─────────────────────────────────────────────────→ FE G20 L01
SEARCH FE WIRE ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─→ 认领前检查 touched_files
```

状态门禁：

1. 两张新单先保持 `backlog`；
2. 前置全部 `done` 后，由 coordinator 升 `ready`；
3. 真人确认监管人后再 claim；
4. 同仓同文件任务串行：API 单须等待 `API-ENT-DICT-JAVA-L04` 和 `E-ENT-KEYENT-JAVA-L01`；FE 单须等待 `FE-ENT-META-DICT-SCENE-WIRE`，并在认领前复核 `ENT-MOD-SEARCH-FE-WIRE-L01` 的文件重叠；
5. 实现完成按 feature 流程进入 integration → pending_test → testing → ready_to_sign。

## 4. 对外接口分工

| 层 | 输入/输出 | 负责什么 | 不负责什么 |
|---|---|---|---|
| Data/DIM | G20 国家/城市树、三类 bind | 编码与树结构 | 查询逻辑 |
| ETL/ES | `region_id`/`country_code`/`city_code` | mapping 与字段供数 | UI 选码 |
| Python 适配/搜索 | 三数组或 `geographicSources` | ES 三分 OR、候选 ID 解析 | 前端交互 |
| Algorithm | `geo_enterprise_codes` | 与其他推荐条件联合筛选 | ES 查询、地区树解析 |
| Java | DTO、校验、snake_case、Feign | 契约保真与透传 | 拆码、OR、ES、算法 |
| Frontend | Cascader 选中节点 | 从 bind 字段取码、构造请求 | 把 `scope_code` 当筛码 |

## 5. 本轮待审文件

1. `API-ENT-REGION-SCOPE-G20-COUNTRY-L01-派单包.md`
2. `FE-ENT-REGION-SCOPE-G20-COUNTRY-L01-派单包.md`
3. 本索引

审阅重点：

- Java recommendation 是否仅补回归测试、不重复造 DTO；
- FE `global/global-all` 是否按国家码展开，选国家是否不展开城市；
- FE key-analysis 三数组与 recommend `geographicSources` 的 wire 形态；
- 建议监管人是否调整；
- 依赖是否需等待 ES FIX `done` 后再放行 API/FE。

> 派单资料已按用户指令推送归档；用户完成内容审阅前不派发、不认领。
