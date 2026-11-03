# POL-L2-DS10-QRY-PY-PLANE-GATE-FIX · 政策判存开关与读路径同库 · hotfix

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent`（口头派单 hotfix，不建 task-id、不走 task-claim/task-update-status，按派单指令执行） |
| supervised_by | `human:淮政玮` |
| 状态流转 | 无 registry 单（hotfix 口头派单）；修复已推送 `lumen-algo-py` `origin/dev`，本 handoff 即交付证据 |
| 说明 | 派单明确：不改任何任务登记，不 task-claim，不 task-update-status |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用既有 `_qualified_count` 骨架只换 schema 来源；连接失败/缺表语义逐字保留；新增一个最小根因回归测试文件锁死「判存与读同库」 |

## 根因（trace `bee37a67…`，2026-11-04）

`gkxlumen-entan-py-api` 处理 `GET /internal/policy/search?q=电池` 时三条 SQL 落三个库：

1. `SELECT COUNT(*) FROM gkxlumenx_dwd.policy_base_info` —— 判存开关，写死**正式库**
2. 后两条实际读 `demo_gkxlumenx_dwd.policy_base_info` —— 读路径用 `connect()` 解析后的 `conn.dwd/conn.ads`（请求级数据面 `x-gkx-plane-policy`，无头默认 demo；部署 helm values 也配 `demo_gkxlumenx_*`）

根因在 `vendor/entan-py/api/policy_routes.py`：`_qualified_count(_FORMAL_DWD/_FORMAL_ADS, ...)` 用常量 `gkxlumenx_dwd`/`gkxlumenx_ads` 做目录开关，而读路径（`polan.search.search_policies` / `get_policy` / indicators）用的是连接对象解析后的库名。开关与读路径不同库。

**拍板口径（human:淮政玮 2026-11-04）**：现在代码都应该读 demo 库；开关必须与读路径同库。

## 修改（只动 `lumen-algo-py` Python 仓，commit `cb72707`）

`vendor/entan-py/api/policy_routes.py`：

1. `_qualified_count(conn, table, *, kind="dwd")`：schema 改由传入连接的 `conn.dwd`（缺省）/`conn.ads`（`kind="ads"`）决定，与读路径同库。表不存在→0（走缺项表回退）；连接失败→`None`（调用方走原读路径）——原语义逐字保留。
2. 新增 `_catalog_gated()`：search/docs 两处判存入口收敛于此——自建连接判存主目录，无行/缺表→`True`（gapfill 回退），连接失败→`False`（原读路径）。
3. 删除写死的 `_FORMAL_DWD`/`_FORMAL_ADS`/`_FORMAL_CATALOG` 常量（无残留引用，不留死代码）；表名常量改 `_CATALOG_TABLE`。
4. 第 144 行过期注释（「只认正式库。…不读 demo_」）改为如实描述：判存开关与读路径同库，跟随数据面（当前部署 demo）。文件内 6 处「正式目录」措辞同步改为「数据面目录」；写闸门（run-pipeline/sync-ods 的「灌数禁止写入正式库」）语义未动。

### 调用点清单（全部对齐）

| 调用点 | 原写法 | 新写法 |
|---|---|---|
| `policy_indicators` 主目录（catalog_n） | `_qualified_count(_FORMAL_DWD, _FORMAL_CATALOG)`（自建连） | `_qualified_count(conn, _CATALOG_TABLE)`（复用端点 conn） |
| `policy_indicators` level/type/timeseries/national/sz 5 处 | `_qualified_count(_FORMAL_ADS, ...)` | `_qualified_count(conn, ..., kind="ads")` |
| `policy_metrics` active 主目录 | `_qualified_count(_FORMAL_DWD, _FORMAL_CATALOG)` | `_qualified_count(conn, _CATALOG_TABLE)` |
| `policy_metrics` level_dist / national_dist / timeseries / graph_node / graph_edge 5 处 | `_qualified_count(_FORMAL_ADS, ...)` | `_qualified_count(conn, ..., kind="ads")` |
| `policy_search` 入口判存 | `_qualified_count(_FORMAL_DWD, _FORMAL_CATALOG) == 0` | `_catalog_gated()` |
| `policy_doc_get` 入口判存 | `_qualified_count(_FORMAL_DWD, _FORMAL_CATALOG) == 0` | `_catalog_gated()` |

修后行为（trace 场景）：无头请求 → conn.dwd 解析为 `demo_gkxlumenx_dwd` → 判存 SQL 变为 `SELECT COUNT(*) FROM demo_gkxlumenx_dwd.policy_base_info`，与后两条读 SQL 同库。数据面切 live（如未来开禁）时同样同库跟随，不再有开关/读错配窗口。

## 不动项（有意）

- `gkxlumenx_gapfill` 缺项表库**不动**：独立回退源，不属于 ods/dwd/ads 数据面（派单明确）。
- `/internal/policy/rank` 的 `gapfill_policy_qry_rank` 读法不动（只读缺项名次表语义未变）。
- 空态诚实语义不变：查询失败仍诚实空、不造数、不 5xx。
- Java / helm / k8s / 前端零改动。
- `polan/common/db.py` 的连接/数据面解析（`apply_plane`）不动——那是真源，开关层对齐它即可。

## 测试

`tests/test_policy_job.py` 对齐新语义：

- `_formal_count` stub 改为 `(conn, table, *, kind)` 签名，断言 `conn.dwd == "demo_gkxlumenx_dwd"` / `conn.ads == "demo_gkxlumenx_ads"`（开关库名来自连接数据面）；原 `assert "demo_" not in sql` 按「判存 SQL 现在就应该带 demo 前缀」反转。
- search/docs/indicators/metrics 各 fake `Conn` 补 `.dwd/.ads` 属性（`demo_gkxlumenx_dwd`/`demo_gkxlumenx_ads`）。
- 原有测试意图全部保留：①目录有行→读目录不读缺项表；②空→回退 gapfill；③缺项表不盖住真数据；④CL- 码拒绝、未知字段只进 ignored_fields、smartScore 不出现。

新增 `tests/test_policy_plane_gate.py`（根因回归，2 用例）：

1. `test_gate_and_read_use_same_plane_db`：模拟 trace 场景（`q=电池`），断言判存 COUNT 落在 `demo_gkxlumenx_dwd.policy_base_info`，不再出现写死 `gkxlumenx_dwd` 的 COUNT。
2. `test_qualified_count_schema_follows_conn`：`_qualified_count` 的 schema 完全由 conn 决定（demo conn→demo 库；live conn→正式库），无常量参与。

`tests/test_policy_search_filter.py` 无需改动（不触判存开关，其 monkeypatch 的是 `polan.search.connect` 读路径）。

### 命令与退出码（2026-11-04，工作机）

```
python -m pytest tests/test_policy_job.py tests/test_policy_search_filter.py -x -q   → 47 passed, exit 0
python -m pytest tests/test_policy_portal_gaps.py -q                                 → 17 passed, exit 0
python -m pytest tests/test_policy_plane_gate.py -q                                  →  2 passed, exit 0
python -m pytest tests/test_policy_job.py tests/test_policy_search_filter.py tests/test_policy_plane_gate.py tests/test_policy_portal_gaps.py -q → 66 passed, exit 0
```

离线说明：全部为离线用例（fake Conn / stub），不依赖真实 MySQL 语义断言；测试机恰可连 192.168.88.43 但用例行为不因连通性变化（未 stub connect 的用例在连接失败时走原读路径，与改前一致）。

## 验收证据

- 修复 commit：`lumen-algo-py` dev `cb72707`（`855e1fa..cb72707` 已推 `origin/dev`，非 force）
- 测试全绿：66 passed（命令与退出码见上）
- 线上验证：待 CI/CD 段 E 复测 `GET /internal/policy/search?q=电池`，确认判存 SQL 与读 SQL 同落 `demo_gkxlumenx_dwd`

## CI/CD

- 分支：`lumen-algo-py` `dev`，push 成功（`855e1fa..cb72707`）
- pipeline：push 已触发（仓默认 CI → K8s dev rollout；hotfix 走正常发布链）
- 部署：随下一次 `gkxlumen-entan-py-api` dev rollout 生效；生效后按上节做线上复测

## 架构合规自检

- ✅ 调用链：只改 Python 算法仓内部判存逻辑，未动 `/internal/*` 契约、未动 Java/前端
- ✅ 算法只在 Python：改动全部在 `lumen-algo-py`
- ✅ 数据策略（D16 相关）：读 `demo_gkxlumenx_*` + `gkxlumenx_gapfill` 回退，未写任何 ODS/DWD/ADS/供应方库
- ✅ 不造数：空态诚实语义、`fabricated: false`、不 5xx 全部保留
- ✅ 可观测：未动日志埋点；判存失败仍 `logger.warning`
- ✅ 图谱：未写 nGQL，未碰 Nebula
- ✅ git 纪律：commit 带 `[agent:algorithm-agent]`，直推 `origin/dev`，无 force；只提交 3 个相关文件
- ✅ 多会话保护：编排仓主工作区有他人未提交 `task-registry.yaml` 与 screenshots，本 handoff 在临时 worktree（`origin/dev` 基线 `fb1ac393`）提交推送，未触碰他人产物

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | ~55k（估算） |
| model_used | glm-5.3 |
| actual_cost | ~0.18（估算） |
| cost_warn | green |

（无 registry 任务，cost 不回填系统；本表供追溯。）

## 未做的事

- 未改 Java/helm/k8s/前端（派单限定只动 Python 仓；部署 values 本就配 `demo_gkxlumenx_*`，无需改）
- 未动 `gkxlumenx_gapfill` 缺项表库（独立回退源）
- 未建/未改任何 task-registry 登记（派单明确禁止）
- 未做线上复测（需等 dev rollout；步骤见「验收证据」）
