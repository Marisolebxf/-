# TS-L2-M10-GRAPH-PY-IMPL-01 · 全景读图叠加人工层（Python 侧）

- 日期：2026-11-13
- 认领：`agent:algorithm-agent` · 仓库：`repos/lumen-algo-py`（dev）
- 设计真源：`sdd/l2/TS-L2-M10-GRAPH-ARCH.md` §4、`TS-L2-M10-GRAPH-API.md` v2.1「全景读图出口增量」、`TS-L2-M10-GRAPH-DATA.md` v2.1、`会签/TS-L2-M10-GRAPH-L2-裁定.md` B4/B6/B7
- 授权：监管人 `human:刘剑锋` 2026-11-13 决定，DS02 知会回执先按默认许可本地实现，上线前以回执为准
- 状态：**实现完成，未 commit / 未 push、未连库**

## 1. 改动文件

| 文件 | 改动 |
|---|---|
| `lumen_common/algorithms/tech_graph_read.py` | `read_graph` 增加 `overlay_factory=None`；`_read` 两条 return 分支叠加；补 `_points_by_ids_ngql` 的 `id(v) IN [...]` 分支（OR 整体加括号）；新增属性覆盖、已删点/边/路径过滤、新建点与改名补读、200 先合并再截断、人工边与端点补点、选中新点 / 已删点、失败降级 |
| `lumen_common/algorithms/tech_graph_overlay.py`（新建） | 只读叠加数据源：库名解析与 `demo_gkxlumenx_` 前缀校验、只读 SELECT、`connect_timeout=2` / `read_timeout=3`、`Master`/`Edge`/`Overlay` 与 id 映射、`open_overlay` factory、启动库名日志 |
| `lumen_algo_service/views/tech_graph_read.py` | 生产显式传 `overlay_factory=open_overlay`；模块导入时 `log_schemas()` |
| `tests/test_tech_graph_read.py` | 新增 11 个叠加用例（假 factory，不连库）；原 8 个用例保持全绿 |

未触碰 `vendor/entan-py/**`、`scripts/seed/seed_technology_panorama_score.py`、任务注册表与设计稿。

## 2. 测试结果

本地无现成 pytest 环境，用临时 venv（`/tmp/lumen-venv`）按 `requirements.txt` 安装后运行：

```bash
/tmp/lumen-venv/bin/python -m pytest tests/test_tech_graph_read.py tests/test_tech_graph_vertex.py tests/test_contracts.py -q
```

- **40 passed, 0 failed**（`test_tech_graph_read.py` 20 个：原 8 + 新 12；`test_tech_graph_vertex.py` 9；`test_contracts.py` 12）
- 覆盖：叠加关闭无 `overlay` 且输出不变；属性覆盖空值不覆盖；`all_*` 按较短长度配对、多出项跳过并 warning；已删点/已删边（`rel_code`、NULL 回退 `rel_type`、无向）/路径过滤；新建点与关键词命中改名点；200 先合并后截断；人工边字段（`origin`/`strengthManual`/`timeRange`，无 `evidenceLevel`/`weight`/`strength`/`year`）与两端补点；选中 `tm:` 新点跳过 Nebula 关系/实体/路径；选中已删点空图；MySQL 失败回落 Nebula 原结果 + `overlay.status=unavailable`；非 demo 库名不建连接直接降级；叠加模块只发 SELECT 且超时常量 2/3。

## 3. 与设计的出入 / 需确认

1. **`all_*` 多出项（已按裁定修正）**：以 DATA §6.4 / ALGO-DATA-C7 为准，配对取较短长度，多出的 tnid / VID **一律跳过并 `logger.warning`**，不单独加入；ARCH §4.2 已由协调人改为同口径。策略在 `tech_graph_overlay._panorama_ids`，单测 `test_overlay_skips_extra_external_ids` 断言跳过。
2. **人工边 `timeRange`**（保留）：采用 ENT `/current` `time_range` 的整数形状 `{"from": int, "to": int}`，仅输出非空端（只填 `from` 时不出 `to`）。全景侧字段名为 `timeRange`。
3. **补点兜底**（保留）：人工边另一端在 Nebula 补读不到时，按主表构造节点（避免 Java 因端点不在 `nodes` 删边）；选中点若主表 active 但 Nebula 补读不到，也按主表构造。属 ALGO-C2 的防御性落地，不改既有出口字段。
4. **关键词匹配**：主表 `name_cn` / `name_en` 用 case-insensitive contains；补读时按 ALGO-N4 传空关键词。
5. **200 截断标记**：原 Nebula 已截断或合并后超 200 都置 `truncated.nodes=true`，取合并后的前 200（新建点 → 改名命中点 → 存量点）。
6. **失败口径**：MySQL 不通 / 超时 / 表缺失 / 库名不合规一律 Nebula 原结果 + `overlay={"status":"unavailable"}`，不改 503；成功置 `{"status":"ok"}`。Java `assemble` 已按「仅 Python 输出该键时追加」实现，两边一致。
7. **库名解析**：`GKX_M10_ENT_DWD_DB`/`ADS_DB` → `LUMEN_ALGO_MYSQL_DWD_DB`/`ADS_DB`，无环境变量时回退 `demo_gkxlumenx_dwd/ads`；前缀校验在建立连接之前，绝不读 `gkxlumenx_*`。
8. 未做缓存、未写 Nebula、人工强度不进 `weight`/`strength`、人工边不进 timeline。

## 4. cost 估算

约 55k input tokens / 18k output tokens（4 份设计稿相关章节精读、4 个源码/测试文件、临时 venv 依赖安装、3 轮测试）；实际耗时约 25 分钟。
