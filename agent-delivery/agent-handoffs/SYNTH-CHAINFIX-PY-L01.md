# SYNTH-CHAINFIX-PY-L01 Handoff — 跨层链路修复第①站（PY 段）

- **任务**：SYNTH-CHAINFIX-PY-L01（跨层链路修复①：PY 段；后续 JAVA/FE 两站依赖本单新契约）
- **执行**：agent:algorithm（claimed_by=agent:algorithm-agent，supervised_by=human:徐滕强）
- **仓**：`lumen-algo-py`（origin/dev，**已 commit 未 push**：`4828c06`，等人工确认推送）
- **强度**：ponytail: full（最短 diff；不新增依赖；复用既有 connect/seed/check 模式）
- **设计真源**：`SYNTH-L2-VIT-AI-TABLES.md` v1.0.6 §1/§3、`SYNTH-L2-COLLAB.md` v1.0.8 §2/§3.2
- **日期**：2026-11-06

## 1. 范围与实现（逐项修法）

### A. weight_profile 全链贯通（PY 段）✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| 三档权重常量+归一 | `entan/synth_vitality/pack.py` | `PROFILE_WEIGHTS`（INDEX_MAIN=0.30/0.30/0.20/0.20、WEIGHT_MAIN=0.30/0.35/0.20/0.15、EQUAL=0.25×4）+ `normalize_weight_profile()`（缺省归一 INDEX_MAIN；大小写敏感；非法 400） |
| compute 按档算 | 同上 | `_equal_weight_index` → `_weighted_index(board, cities, profile, artifact_index)`：INDEX_MAIN 档优先消费 186_1 产物 `index_0_100`（同核唯一计算点），其它档按档公式合成；缺维分母收缩不补 0 |
| 回显口径对齐 | `pack.py` + `api/synth_vitality_routes.py` | dimScores.weight / metrics.M_SYNTH_VIT_WEIGHT / gradeNote / `result.weight_profile` 全部按档产出；**按哪档算标哪档，禁 EQUAL 算标 INDEX_MAIN** |
| jobs 透传 | `api/synth_jobs_routes.py` | vitality 分支 `execute_vitality_job(body)` 透传 `body.weight_profile`（归一后参与四段分析指纹） |
| by_batch WHERE 修正 | `api/synth_vitality_routes.py` | 显式批号回溯 WHERE **只按 calc_batch_id+calc_status**（去掉条件与请求档过滤；批号全局唯一）；profile 由新增 `_batch_profile()` 从行内 `weight_profile_code` 回读；最新批路由保持条件4+profile 定位 |
| compute 兜底按档 | 同上 | 无 ADS 批兜底 `build_vitality_result(..., weight_profile=profile)`（请求档实算） |

### B. synth_vit 五表 DDL + seed ✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| 五张 DDL | `scripts/mysql/synth_vit.sql`（新） | index/dim_score/weight/indicator/rank；唯一键均含 `weight_profile_code+calc_batch_id`（rank 另含 rank_city_code；index/rank 按 v1.0.6 §2 含 profile）；公共列对齐总册 §11.2（15 列）；INDEX_MAIN 权重行带 `weight_provenance_metric_id='M_SYNTH_VIT_INDEX'`；血缘 COMMENT 齐；demo_gkxlumenx_ads；CREATE IF NOT EXISTS 幂等 |
| 三档 seed | `scripts/seed/seed_synth_vit.py`（新） | 三档并存预填（`mock_20261106_vit_seed`，219 行：index 3/dim 48/weight 12/indicator 144/rank 12）；数值冻结自 `metrics/repro/out/` 正本（dim_scores×四城 + 12 leaves raw/score 全量）；指数按各档同公式实算（EQUAL 档对照 186_1 `index_0_100` 74.9981/60.6822/12.3667/1.9012 通过）；同批同 `calc_batch_created_at` 写五表（TC-2/AR-6）；`is_mock=1` 整批事务失败回滚；幂等同批先删后插 |
| _DEFAULT_REPRO 治理 | `pack.py` | 个人绝对路径已移除；`_DEFAULT_REPRO = os.environ.get(_REPRO_ENV, "")`，无 ENV → 空串 → `_repro_dir()=None` → 诚实降级不读盘（compute 全 null 格），容器不受影响 |

### C. graph 端点（新）✅
| 改动点 | 文件 | 修法 |
|---|---|---|
| graph 读路径 | `entan/synth_collab/pack.py` | `build_collab_graph()`：批次解析（snapshotId 精确读 meta / 未传读 `is_latest=1`，找不到 → 200 `reason=batch_meta_missing` 禁回落）；只读 `metric_id=M_SYNTH_COLLAB_RELATION_INPUT`；节点 canonical 去重（entity_id）、industry_code 精确过滤、entity_types/relation_types 多选子集校验（非法 400）；节点按 degree Top / 边按 weight Top 截断 + `truncated=true`；边不悬空（端点须在保留节点集）；响应边无 year |
| graph 路由 | `api/synth_collab_routes.py` | `GET /internal/v1/synth/collaboration/graph`；region/compare/window 必填（缺省不默改 → 400）；limit_nodes≤200/limit_edges≤500（越界 400）；**无 gapfill_batch_id 参数**（v1.0.8 已废止，响应亦无该键） |

### D. batch_meta 回显补全 ✅
- `build_collab_snapshot` 外壳补 **isLatest + region/compare/window**（九列对齐：snapshotId / calc_batch_id / graph_batch_id / cache_key / region / compare / window / publishedAt / isLatest）；条件列与 is_latest 从命中 meta 行回读（未命中 meta → 请求归一值 + `isLatest=null`）。

## 2. ⚡ 新契约签名清单（②③站 JAVA/FE 对齐依据）

> **以下是本单固化的稳定签名；JAVA/FE 两站按此实现，勿另造字段名。**

### 2.1 graph 请求（GET /internal/v1/synth/collaboration/graph，Java Feign 透传）
| 参数 | 必填 | 说明 |
|---|---|---|
| `region` / `compare` / `window` | ✅ | 缺省不默改，缺失→400；window=1y/3y/5y 或中文 |
| `snapshot_id`（query 名）/ `snapshotId` | ❌ | 从 `synth_collab_batch_meta.snapshot_id` 解析 `graph_batch_id`；无映射→200+`reason=batch_meta_missing` |
| `industry` | ❌ | 过滤节点 `industry_code`（**精确匹配**；v1.0.8：industry=industry_code） |
| `entity_types` | ❌ | 逗号分隔 `enterprise,institution,talent`；缺省全部；非法 400 |
| `relation_types` | ❌ | 逗号分隔 `co_patent,co_project,talent_flow`；缺省全部；非法 400 |
| `limit_nodes` / `limit_edges` | ❌ | 默认 200/500，上限同值；越界 400；超限按 degree/weight Top 截断 |
| ~~`gapfill_batch_id`~~ | — | **已废止（v1.0.8），请求与响应均无此键** |

### 2.2 graph 响应（包络 `data`）
```json
{ "region": "深圳市", "compare": "全国重点城市", "window": "最近3年",
  "snapshotId": "task:xxx | null", "calc_batch_id": "...", "graph_batch_id": "graph:...",
  "nodes": [{"id","name","type","industry","industryLabel","degree"}],
  "edges": [{"source","target","sourceType","targetType","relationType","sourceEventId","weight"}],  // 无 year
  "truncated": false, "reason": null | "batch_meta_missing" | "no_year_on_source" }
```
- 本期 node/edge 0 行（C-05）→ 恒 `nodes=[]+edges=[]+truncated=false`；无 meta → `reason=batch_meta_missing`；有 meta 无行 → `reason=no_year_on_source`；均 **HTTP 200**。
- node 对象 `industry` 键 = 表列 `industry_code` 值；edge 键名 `sourceEventId` 对应 `source_event_id`。

### 2.3 vitality batch-snapshot 新参数/行为（GET /internal/v1/synth/vitality/batch-snapshot）
| 参数 | 说明 |
|---|---|
| `weight_profile` | `INDEX_MAIN\|WEIGHT_MAIN\|EQUAL`（大小写敏感）；缺省归一 INDEX_MAIN；非法 400 |
| `calc_batch_id` / `snapshotId` | 显式批号回溯：WHERE 只按 batch+calc_status（批号全局唯一）；**profile 从行内回读并回显**（外壳与 `result.weight_profile` 均标行内档） |
| 外壳 `weight_profile` | 回显口径=实际计算档（禁 EQUAL 算标 INDEX_MAIN）；`cache_key` 第四段=该档 |
| compute 兜底 | 无 ADS 批 → 按请求档实算（`batch_reason=batch_not_published`，批号 `mock_vit_latest`） |

### 2.4 jobs execute（POST /internal/v1/synth/jobs/execute，vitality 分支）
- 请求 body 新增可选 `weight_profile`（同 2.3 枚举；归一后参与四段分析指纹 `region|compare|window|weight_profile_norm`）。
- 响应 `result.weight_profile` 恒回显实际档。

### 2.5 collab batch-snapshot 外壳（九列，D 项固化）
```json
{ "snapshotId", "cache_key", "computedAt", "methodVersion",
  "calc_batch_id", "graph_batch_id", "region", "compare", "window",
  "publishedAt", "isLatest", "batchMetaReason", "result": { …, "_meta": {...} } }
```
- `isLatest`：0/1（来自 meta 行）/null（无 meta）；`region/compare/window`：meta 行内值（未命中 meta → 请求归一值）；FE/Java 消费九列，`result._meta` 仅内部源。

### 2.6 seed 批号格式
- 活力 seed 批号：**`mock_20261106_vit_seed`**（五表同批；`is_mock=1`；`calc_status='succeeded'`；`method_version='synth-vitality-v1.0'`）。
- 格式约定：`mock_YYYYMMDD_vit_seed`（对照 elements `mock_20261105_elem_seed` / collab `mock_20261105_collab_seed`）。
- 权重档键：`INDEX_MAIN` / `WEIGHT_MAIN` / `EQUAL`（synth_vit_* 五表 `weight_profile_code` 列值，大小写敏感）。
- 三档指数（深圳，seed 实算落库）：INDEX_MAIN=75.1478 / WEIGHT_MAIN=74.4224 / EQUAL=74.9981（EQUAL 对照 186_1 `index_0_100` 逐城一致）。

## 3. 自检结果（全绿）

| 自检 | 结果 | 关键断言 |
|---|---|---|
| `seed_synth_vit.py --check` | ✅ ok | 5 表清单/唯一键含 profile+batch/行数/三档互异/EQUAL 同核对照/权重合计=1 |
| `seed_synth_vit.py --apply`（demo 库实跑） | ✅ ok:true | 219 行落库、is_mock=1、succeeded、三档并存、EQUAL 深圳=74.9981 |
| `check_synth_vitality.py`（带 DB） | ✅ 39 PASS 0 FAIL | [6] 三档外壳/result 各标各档+权重矩阵正确+jobs 透传/非法档 400；[7] 非默认条件×EQUAL 批异档直读出数 36.3636+行内回读 EQUAL+snap: 跨条件可读；[8] 默认三元组走 seed 真批 `mock_20261106_vit_seed`（**替代 mock_vit_latest 兜底**）出数 75.1478+INDEX_MAIN 权重按档；邻叶 [5] 按批回溯不回归 |
| `check_synth_collab.py`（带 DB） | ✅ 76 PASS 0 FAIL | [7] graph 空图契约/必填 400/无 gapfill_batch_id 键/meta_missing 不回落；[8] 有行探针：canonical 去重/industry 精确过滤/边不悬空/entity_types/relation_types/limit 截断+truncated/snapshotId 精确读；[9] 九列回显 isLatest=1+条件列；[1]–[6] 既有断言不回归 |
| `check_synth_elements.py`（带 DB） | ✅ 38 PASS 0 FAIL | 邻叶回归 |

> 本机无 `SYNTH_VIT_REPRO_DIR` 时 compute 兜底为全 null 诚实降级（新治理行为）；三档指数互异断言由 seed 落库后的 ADS 真批路径覆盖（[8]）。

## 4. 架构合规自检（铁律逐条）

| 铁律 | 合规 |
|---|---|
| ①算法只在 Python | ✅ 全部改动在 lumen-algo-py |
| ②调用链 前端→Java REST→Python /internal/* | ✅ 新端点在 /internal/v1/synth/*；Java 只透传（FE 差距在 COLLAB 册 §6，由 FE 站接线） |
| ⑦共享聚合核心 | ✅ 只读 ADS |
| ⑧ADS 先行 Mock 填充 | ✅ 五表 ADS+seed is_mock=1 |
| ⑩D9 血缘 | ✅ 唯一键含 profile+batch；INDEX_MAIN 行 provenance=M_SYNTH_VIT_INDEX；缺行 null 不补 0 禁常量回填（装包读 ADS 时权重只读行） |
| ⑫demo/lumen 隔离 | ✅ 只写 demo_gkxlumenx_ads |
| ⑬对象存储 | ✅ 不涉及 |
| ⑭D16 gapfill | ✅ 未建 gapfill 表；不写供应方库 |
| D17 合规锁定闭包 | ✅ 未触碰 |
| D18 可实现 | ✅ 空图/空态=读表后诚实结果非写死 JSON |
| 多会话保护 | ✅ 未动他人 WIP（`scripts/mock_stage_health_scores.py`、`scripts/seed_supply_chain_relations.py`、`lumen_common/algorithms/svcan/assembly/graph.py` 均未入本 commit） |

## 5. 偏离说明

> **未修清单：无。** 派单范围 A/B/C/D 四项全部完成（weight_profile 贯通 / vit 五表 DDL+seed / graph 端点 / 九列回显）；范围外事项见 §9 移交清单（Java 门面、FE 接线、legacy_unknown 任务链口径属②③站）。

1. **`_dim_score_payload` 未加 source 参数**：维分不随档变（档只决定合成权重），按 ponytail 最短 diff 原则未引入无效分支。
2. **186_1 `index_0_100` 实为四维等权合成**（实测验证），故「同核对照」断言挂 EQUAL 档（seed `--check`/`--apply` 双断言）；INDEX_MAIN 档由装包 `_weighted_index` 优先消费该产物（同核唯一计算点），与 v1.0.6 §1「同核只算一处」一致。
3. **dim_score 产业维已灌行**：186_1 盘 dim_scores 含产业维（77.7925/39.7686/18.777/7.6049），非 183_1 维分口径的场景由后续实算覆盖；`ind-talent-edu` 有值未进维（status=proxy，score=null），如实落行。
4. **TC-2 五表同批时间戳**：seed 以同 `calc_batch_id`+同 `calc_batch_created_at` 写五表（采纳会签建议条款）；路由读取只按 batch+created_at 排序，不受影响。

## 6. 产物清单

| 类型 | 产物 |
|---|---|
| commit | `4828c06`（dev，11 文件 +1247/−65；**未 push**，等人工确认） |
| 新文件 | `scripts/mysql/synth_vit.sql`、`scripts/seed/seed_synth_vit.py` |
| 改文件 | `vendor/entan-py/`：`entan/synth_vitality/{pack,__init__}.py`、`entan/synth_collab/{pack,__init__}.py`、`api/synth_{vitality,jobs,collab}_routes.py`、`scripts/check_synth_{vitality,collab}.py` |
| DB | demo_gkxlumenx_ads 新建 5 表 + seed 批 `mock_20261106_vit_seed`（219 行） |

## 7. 验收证据

- 上表 §3 自检输出（`/tmp/check_vit_out3.txt` / `/tmp/check_collab_final2.txt` 可复查）。
- seed apply JSON：`{"rows":{"synth_vit_index":3,"synth_vit_dim_score":48,"synth_vit_weight":12,"synth_vit_indicator":144,"synth_vit_rank":12},"ok":true}`。
- CI：未 push，push 后由 GitLab CI 验证（本单不涉及 K8s dev 行为变化——新端点需 Java 门面后才对外）。

## 8. cost（待 task-update-fields 回填）

| 字段 | 值 |
|---|---|
| actual_tokens | ≈128k（含读规约/现状代码/三轮自检迭代） |
| model_used | glm-5.3-Flash |
| actual_cost | ≈$0.6（< $10 阈值，不触发复盘） |
| cost_warn | false |

## 9. 移交②③站（JAVA/FE）注意事项

1. Java 门面只需透传 graph 参数（Python 执行筛选/截断）；batch_meta 九列已在快照外壳，Java `#105 resultData` 直接透出。
2. FE 报告页消费快照时沿用快照内 `weight_profile`（v1.0.6 §3 同请求一致铁律），禁止报告另选档。
3. `legacy_unknown` 旧任务识别（v1.0.3/v1.0.4）属任务链口径，PY 段 jobs execute 已支持 weight_profile 入参，冻结/复用逻辑在 Java async-service 侧落地（②站范围）。
4. vitality seed 批 `mock_20261106_vit_seed` 落库后默认三元组已走真批；`mock_vit_latest` 兜底仅剩无批条件触发。
